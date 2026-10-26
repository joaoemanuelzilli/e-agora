"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { useLiveRows, type LiveRow } from "@/components/Dashboard";
import { EntryLadder } from "@/components/charts/EntryLadder";
import { brl, num, pct, signClass } from "@/lib/format";
import { ddmPerShare, fairValue, irrImplied } from "@/lib/valuation";
import type { Row } from "@/lib/types";

export type Monitor = { kpi: string; threshold: string; next?: string };
type Scheme = "iguais" | "vol" | "tir";

const SCHEMES: { id: Scheme; label: string; note: string }[] = [
  { id: "iguais", label: "Pesos iguais", note: "mesmo valor em cada ação" },
  { id: "vol", label: "Inverso da volatilidade", note: "mais peso nas menos voláteis" },
  { id: "tir", label: "TIR acima da meta", note: "mais peso em quem rende mais que o Ke" },
];

const up2 = (v: number) => Math.ceil(v * 100 - 1e-6) / 100;
const down2 = (v: number) => Math.floor(v * 100 + 1e-6) / 100;

/** Preço máximo para render `ke`: o menor entre o preço com TIR de dono = ke e o valor justo calculado com esse ke. */
function priceAt(r: LiveRow, ke: number): number | null {
  const e = r.engine;
  if (!e || e.template === "holding") return null;
  const d = ddmPerShare(e, ke);
  if (d === null || !Number.isFinite(d) || d <= 0) return null;
  const ddm = d * (e.per_unit || 1);
  const f = fairValue(e, ke);
  return f !== null && f > 0 ? Math.min(ddm, f) : ddm;
}

// Mesmos filtros da seleção de oportunidades (pipeline/build.py), para avisar quando o preço está bom mas o risco não.
function lowConf(c: string | null | undefined): boolean {
  const s = (c || "").toLowerCase();
  return s.startsWith("baixa") && !s.startsWith("baixa-m") && !s.startsWith("baixa a m");
}
function caveat(r: LiveRow): string | null {
  if (r.altman?.zone === "risco") return "Altman em zona de risco";
  if (lowConf(r.confidence)) return "confiança do analista baixa";
  if (r.L.prob !== null && r.L.prob < 0.45) return "chance de valer mais que o preço abaixo de 45%";
  return null;
}

function capWeights(raw: Record<string, number>, cap: number): Record<string, number> {
  const keys = Object.keys(raw).filter((k) => raw[k] > 0);
  let w: Record<string, number> = {};
  const tot = keys.reduce((s, k) => s + raw[k], 0) || 1;
  keys.forEach((k) => (w[k] = raw[k] / tot));
  for (let it = 0; it < 20; it++) {
    const over = keys.filter((k) => w[k] > cap + 1e-9);
    if (!over.length) break;
    const excess = over.reduce((s, k) => s + (w[k] - cap), 0);
    over.forEach((k) => (w[k] = cap));
    const free = keys.filter((k) => w[k] < cap - 1e-9);
    const base = free.reduce((s, k) => s + w[k], 0);
    if (!free.length || base <= 0) break;
    w = { ...w };
    free.forEach((k) => (w[k] += (excess * w[k]) / base));
  }
  return w;
}

export function InvestView({ rows, opps, monitors }: { rows: Row[]; opps: string[]; monitors: Record<string, Monitor[]> }) {
  const { rows: live, ke, asOf } = useLiveRows(rows);
  const [amount, setAmount] = useState(100000);
  const [scheme, setScheme] = useState<Scheme>("iguais");
  const [cap, setCap] = useState(0.2);
  const [ladder, setLadder] = useState(false);
  const [sel, setSel] = useState<string[]>(opps);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    try {
      const s = JSON.parse(localStorage.getItem("investir") || "null");
      if (s) {
        if (s.amount > 0) setAmount(s.amount);
        if (SCHEMES.some((x) => x.id === s.scheme)) setScheme(s.scheme);
        if ([0.1, 0.15, 0.2, 0.25].includes(s.cap)) setCap(s.cap);
        if (Array.isArray(s.sel) && s.sel.length) setSel(s.sel.filter((t: unknown) => typeof t === "string"));
        setLadder(!!s.ladder);
      }
    } catch {}
    setReady(true);
  }, []);
  useEffect(() => {
    if (!ready) return;
    try {
      localStorage.setItem("investir", JSON.stringify({ amount, scheme, cap, sel, ladder }));
    } catch {}
  }, [ready, amount, scheme, cap, sel, ladder]);

  const enriched = useMemo(
    () =>
      live.map((r) => {
        const price = r.L.price;
        const holding = r.engine?.template === "holding";
        // holding: teto = soma das partes (já a Ke de 25% nas controladas), sem degraus
        const ceiling = holding ? (r.L.fair ?? null) : priceAt(r, ke);
        const mid = holding ? null : priceAt(r, ke + 0.025);
        const strong = holding ? null : priceAt(r, ke + 0.05);
        const status = !price || ceiling === null ? "sem preço-teto" : strong !== null && price <= strong ? "compra forte" : price <= ceiling ? "na faixa" : "acima do teto";
        const warn = status === "na faixa" || status === "compra forte" ? caveat(r) : null;
        return { r, price, ceiling, mid, strong, status, warn, dist: price && ceiling ? ceiling / price - 1 : null };
      }),
    [live, ke],
  );
  const byT = Object.fromEntries(enriched.map((x) => [x.r.ticker, x]));
  const chosen = sel.map((t) => byT[t]).filter((x) => x && x.price);
  const raw: Record<string, number> = {};
  chosen.forEach((x) => {
    if (scheme === "iguais") raw[x.r.ticker] = 1;
    else if (scheme === "vol") raw[x.r.ticker] = 1 / Math.max(0.15, x.r.vol_1y ?? 0.4);
    else raw[x.r.ticker] = Math.max(0.01, (x.r.L.irr ?? 0) - (ke - 0.05));
  });
  const weights = capWeights(raw, Math.max(cap, chosen.length ? 1 / chosen.length : 1));
  const orders = chosen.map((x) => {
    const wgt = weights[x.r.ticker] ?? 0;
    const value = amount * wgt;
    const now = x.price as number;
    const ceil = x.ceiling;
    const first = ceil === null ? up2(now) : now <= ceil ? Math.min(down2(ceil), up2(now)) : down2(ceil);
    const legs = ladder && ceil !== null
      ? [
          { share: 0.4, price: first },
          { share: 0.3, price: x.mid !== null ? down2(Math.min(x.mid, first)) : first },
          { share: 0.3, price: x.strong !== null ? down2(Math.min(x.strong, first)) : first },
        ]
      : [{ share: 1, price: first }];
    const legsQ = legs.map((l) => {
      const q = Math.floor((value * l.share) / l.price);
      return { ...l, qty: q, lot: Math.floor(q / 100) * 100, frac: q % 100, total: q * l.price, irr: irrImplied(x.r.engine, l.price) };
    });
    const now_ok = ceil !== null && now <= ceil;
    return { x, wgt, value, legs: legsQ, invested: legsQ.reduce((s, l) => s + l.total, 0), now_ok };
  });
  const invested = orders.reduce((s, o) => s + o.invested, 0);
  const legsAll = orders.flatMap((o) => o.legs.map((l) => ({ l, now: o.x.price as number })));
  const nowLegs = legsAll.filter((x) => x.l.qty > 0 && x.l.price >= x.now);
  const waitLegs = legsAll.filter((x) => x.l.qty > 0 && x.l.price < x.now);
  const sum = (a: typeof legsAll) => a.reduce((s, x) => s + x.l.total, 0);
  const keLabel = `${Math.round(ke * 100)}%`;
  const ladderRows = enriched
    .filter((x) => sel.includes(x.r.ticker) && x.price)
    .map((x) => ({ ticker: x.r.ticker, price: x.price as number, ceiling: x.ceiling, strong: x.strong, fair: x.r.L.fair, pre: x.r.prev_close }));
  const all = [...enriched].sort((a, b) => (b.dist ?? -9) - (a.dist ?? -9));
  const toggle = (t: string) => setSel((s) => (s.includes(t) ? s.filter((x) => x !== t) : [...s, t]));

  return (
    <div className="space-y-8">
      <section className="panel p-5">
        <div className="grid grid-cols-1 gap-5 lg:grid-cols-12">
          <div className="lg:col-span-4">
            <label className="label" htmlFor="valor">
              Quanto investir
            </label>
            <div className="mt-1 flex items-center gap-2">
              <span className="text-[18px] text-muted">R$</span>
              <input
                id="valor"
                type="number"
                min={100}
                step={1000}
                value={amount}
                onChange={(e) => setAmount(Math.max(0, Number(e.target.value) || 0))}
                className="num w-full rounded border border-hairline bg-surface px-3 py-2 text-[22px] font-semibold outline-none focus:border-accent"
              />
            </div>
            <div className="mt-2 text-[12px] text-muted">
              {chosen.length} ações, ordens somam {brl(invested, 0)}, sobra de {brl(amount - invested, 0)}
            </div>
          </div>
          <div className="lg:col-span-5">
            <div className="label">Como dividir</div>
            <div className="mt-1 flex flex-wrap gap-2">
              {SCHEMES.map((s) => (
                <button
                  key={s.id}
                  type="button"
                  onClick={() => setScheme(s.id)}
                  aria-pressed={scheme === s.id}
                  className={`rounded border px-3 py-1.5 text-left text-[13px] ${scheme === s.id ? "border-accent bg-accent text-white" : "border-hairline text-ink-2 hover:bg-surface-2"}`}
                >
                  <div className="font-medium">{s.label}</div>
                  <div className={`text-[11px] ${scheme === s.id ? "text-white/80" : "text-muted"}`}>{s.note}</div>
                </button>
              ))}
            </div>
          </div>
          <div className="space-y-3 lg:col-span-3">
            <div>
              <div className="label">Máximo por ação</div>
              <div className="mt-1 flex overflow-hidden rounded border border-hairline">
                {[0.1, 0.15, 0.2, 0.25].map((c) => (
                  <button key={c} type="button" onClick={() => setCap(c)} aria-pressed={cap === c} className={`num flex-1 px-2 py-1 text-[12px] ${cap === c ? "bg-accent text-white" : "text-ink-2 hover:bg-surface-2"}`}>
                    {Math.round(c * 100)}%
                  </button>
                ))}
              </div>
            </div>
            <label className="flex items-center gap-2 text-[13px] text-ink-2">
              <input type="checkbox" checked={ladder} onChange={(e) => setLadder(e.target.checked)} />
              Escalonar em 3 ordens: 40% no teto, 30% a Ke +2,5 p.p., 30% a Ke +5 p.p.
            </label>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <div className="panel p-4">
          <div className="label">Executa agora</div>
          <div className="num mt-1 text-[24px] font-semibold">{brl(sum(nowLegs), 0)}</div>
          <div className="text-[12px] text-muted">{nowLegs.length} ordens no preço de tela ou acima dele, sem passar do teto</div>
        </div>
        <div className="panel p-4">
          <div className="label">Fica aguardando</div>
          <div className="num mt-1 text-[24px] font-semibold">{brl(sum(waitLegs), 0)}</div>
          <div className="text-[12px] text-muted">{waitLegs.length} ordens abaixo do preço de agora, só executam se cair</div>
        </div>
        <div className="panel p-4">
          <div className="label">TIR média ponderada no preço das ordens</div>
          <div className="num mt-1 text-[24px] font-semibold">
            {pct(
              (() => {
                const v = legsAll.filter((x) => x.l.qty > 0 && x.l.irr !== null);
                const t = v.reduce((s, x) => s + x.l.total, 0);
                return t > 0 ? v.reduce((s, x) => s + (x.l.irr as number) * x.l.total, 0) / t : null;
              })(),
              1,
            )}
          </div>
          <div className="text-[12px] text-muted">meta (Ke) de {keLabel}</div>
        </div>
      </section>

      <section className="panel sticky-host">
        <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-hairline px-4 py-3">
          <h2 className="h2">Ordens sugeridas</h2>
          <span className="text-[12px] text-muted">
            Ordem limitada: nunca acima do preço-teto. Preços ao vivo{asOf ? ` às ${new Date(asOf).toLocaleTimeString("pt-BR")}` : ""}.
          </span>
        </div>
        <div className="freeze-wrap">
          <table className="data freeze min-w-[1100px] text-[13px]">
            <thead>
              <tr>
                <th className="freeze-col">Empresa</th>
                <th>Preço agora</th>
                <th>Preço-teto (Ke {keLabel})</th>
                <th>Compra forte (Ke +5 p.p.)</th>
                <th className="!text-left">Situação</th>
                <th>Peso</th>
                <th>Valor</th>
                <th>Preço da ordem</th>
                <th>Quantidade</th>
                <th className="!text-left">Como executar</th>
                <th>TIR no preço da ordem</th>
                <th>Alvo (valor justo)</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((o) =>
                o.legs.map((l, li) => (
                  <tr key={`${o.x.r.ticker}-${li}`}>
                    <td className="freeze-col">
                      {li === 0 ? (
                        <Link href={opps.includes(o.x.r.ticker) ? `/relatorio/${o.x.r.ticker}` : `/empresa/${o.x.r.ticker}`} className="font-semibold hover:text-accent">
                          {o.x.r.ticker}
                        </Link>
                      ) : (
                        <span className="pl-3 text-muted">ordem {li + 1}</span>
                      )}
                    </td>
                    <td>{li === 0 ? num(o.x.price) : ""}</td>
                    <td>{li === 0 ? num(o.x.ceiling) : ""}</td>
                    <td>{li === 0 ? num(o.x.strong) : ""}</td>
                    <td className="text-left">
                      {li === 0 && (
                        <span className={o.x.status === "acima do teto" ? "text-ink-2" : "pos font-medium"}>
                          {o.x.status}
                          {o.x.dist !== null && o.x.status === "acima do teto" ? ` (precisa cair ${pct(-o.x.dist, 1)})` : ""}
                        </span>
                      )}
                      {li === 0 && o.x.warn && (
                        <div className="text-[11.5px] font-normal text-muted">fora da seleção: {o.x.warn}</div>
                      )}
                    </td>
                    <td>{li === 0 ? pct(o.wgt, 1) : pct(o.wgt * l.share, 1)}</td>
                    <td>{brl(o.value * l.share, 0)}</td>
                    <td className="font-semibold">{num(l.price)}</td>
                    <td>{l.qty.toLocaleString("pt-BR")}</td>
                    <td className="whitespace-normal text-left text-[12px] text-ink-2">
                      {l.qty === 0 ? "valor não compra 1 ação" : ""}
                      {l.lot > 0 ? `${l.lot.toLocaleString("pt-BR")} em ${o.x.r.ticker}` : ""}
                      {l.lot > 0 && l.frac > 0 ? " + " : ""}
                      {l.frac > 0 ? `${l.frac} em ${o.x.r.ticker}F` : ""}
                      {l.qty > 0 && l.price < (o.x.price as number) ? " (aguarda o preço)" : ""}
                    </td>
                    <td className={(l.irr ?? 0) >= ke ? "font-semibold" : ""}>{pct(l.irr, 1)}</td>
                    <td>{li === 0 ? num(o.x.r.L.fair) : ""}</td>
                  </tr>
                )),
              )}
            </tbody>
          </table>
        </div>
      </section>

      {ladderRows.length > 0 && (
        <EntryLadder
          title="Onde está o preço em relação à faixa de compra"
          subtitle="Faixa azul: do preço de compra forte (Ke +5 p.p.) até o preço-teto. Escala logarítmica, relativa ao preço de agora."
          rows={ladderRows}
          keLabel={keLabel}
        />
      )}

      {Object.keys(monitors).length > 0 && (
        <section>
          <h2 className="h2 mb-3">Quando vender ou rever a posição</h2>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-3">
            {sel
              .filter((t) => monitors[t]?.length)
              .map((t) => {
                const x = byT[t];
                return (
                  <div key={t} className="panel p-4">
                    <div className="flex items-baseline justify-between gap-2">
                      <Link href={`/relatorio/${t}`} className="text-[15px] font-semibold hover:text-accent">
                        {t}
                      </Link>
                      <span className="text-[12px] text-muted">
                        alvo {num(x?.r.L.fair)} ({pct(x?.r.L.upside, 0, true)})
                      </span>
                    </div>
                    <ul className="mt-2 space-y-1.5 text-[12.5px] text-ink-2">
                      {monitors[t].slice(0, 3).map((m, i) => (
                        <li key={i}>
                          <span className="font-medium text-ink">{m.kpi}: </span>
                          {m.threshold}
                          {m.next ? <span className="text-muted"> ({m.next})</span> : null}
                        </li>
                      ))}
                    </ul>
                  </div>
                );
              })}
          </div>
        </section>
      )}

      <section className="panel sticky-host">
        <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-hairline px-4 py-3">
          <h2 className="h2">Preço-teto das 59</h2>
          <span className="text-[12px] text-muted">Marque para incluir na calculadora. Ordenado pela distância até o preço-teto.</span>
        </div>
        <div className="freeze-wrap">
          <table className="data freeze min-w-[900px] text-[13px]">
            <thead>
              <tr>
                <th className="freeze-col">Empresa</th>
                <th>Preço agora</th>
                <th>Preço-teto (Ke {keLabel})</th>
                <th>Distância até o teto</th>
                <th>Compra forte</th>
                <th>TIR de dono agora</th>
                <th>Valor justo</th>
                <th className="!text-left">Situação</th>
              </tr>
            </thead>
            <tbody>
              {all.map((x) => (
                <tr key={x.r.ticker}>
                  <td className="freeze-col">
                    <label className="flex items-center gap-2">
                      <input type="checkbox" checked={sel.includes(x.r.ticker)} onChange={() => toggle(x.r.ticker)} aria-label={`incluir ${x.r.ticker}`} />
                      <Link href={`/empresa/${x.r.ticker}`} className="font-semibold hover:text-accent">
                        {x.r.ticker}
                      </Link>
                      {opps.includes(x.r.ticker) && <span className="rounded px-1 text-[10.5px] text-accent-ink" style={{ background: "var(--accent-soft)" }}>oportunidade</span>}
                    </label>
                  </td>
                  <td>{num(x.price)}</td>
                  <td>{num(x.ceiling)}</td>
                  <td className={signClass(x.dist)}>{pct(x.dist, 1, true)}</td>
                  <td>{num(x.strong)}</td>
                  <td className={(x.r.L.irr ?? -1) >= ke ? "font-semibold" : ""}>{pct(x.r.L.irr, 1)}</td>
                  <td>{num(x.r.L.fair)}</td>
                  <td className="text-left">
                    <span className={x.status === "acima do teto" || x.status === "sem preço-teto" ? "text-ink-2" : "pos font-medium"}>{x.status}</span>
                    {x.warn && !opps.includes(x.r.ticker) && <div className="text-[11.5px] text-muted">fora da seleção: {x.warn}</div>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <p className="text-[12px] leading-relaxed text-muted">
        Preço-teto é o preço em que os dividendos projetados mais a perpetuidade rendem exatamente o Ke escolhido; abaixo dele a TIR de dono supera a meta. Use ordens limitadas: no pregão de hoje a liquidez está baixa e o spread, largo. Lote padrão de 100 ações; o restante vai no mercado fracionário (código com F). Estudo quantitativo com finalidade informativa, não é recomendação.
      </p>
    </div>
  );
}
