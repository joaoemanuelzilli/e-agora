"use client";
import Link from "next/link";
import { useState } from "react";
import type { LiveRow } from "@/components/Dashboard";
import { trackRecord, type Registro } from "@/components/registro/Registro";
import { Rating, callOf, type Tone } from "@/components/ui/Rating";
import { brl, num, pct, signClass } from "@/lib/format";
import { useMarket } from "@/lib/live";
import { ceilingPrice } from "@/lib/valuation";

const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);
const dataBR = (iso: string) => iso.slice(0, 10).split("-").reverse().join("/");

const SEG_SHORT: Record<string, string> = {
  "Serviços Educacionais": "Educação",
  "Carnes e Derivados": "Alimentos",
  Incorporações: "Construção",
  "Tecidos. Vestuário e Calçados": "Varejo de moda",
};
export function sectorShort(s?: { setor?: string; subsetor?: string; segmento?: string }) {
  if (!s) return "—";
  if (s.segmento && SEG_SHORT[s.segmento]) return SEG_SHORT[s.segmento];
  if (s.subsetor && s.subsetor !== "Diversos") return s.subsetor;
  return s.segmento ?? s.setor ?? "—";
}

export type Pick = {
  r: LiveRow;
  rank: number;
  tone: Tone;
  call: ReturnType<typeof callOf>;
  ceiling: number | null;
  weight: number | null;
  href: string;
  name: string;
  thesis: string | null;
  /** recomendação congelada no registro, quando mudou de lado (compra ↔ aguardar) desde então */
  was: string | null;
};

const frozenBuy = (situacao?: string) => (situacao ? situacao !== "acima do teto" : null);

export function usePicks(
  rows: LiveRow[],
  opps: string[],
  ke: number,
  reports: string[],
  reg?: Registro | null,
  names: Record<string, string> = {},
  theses: Record<string, string> = {},
): Pick[] {
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const recs = Object.fromEntries((reg?.recomendacoes ?? []).map((x) => [x.ticker, x]));
  const w = Object.fromEntries((reg?.recomendacoes ?? []).map((x) => [x.ticker, x.peso_capital]));
  const refDate = reg ? `${reg.data_ref.slice(8, 10)}/${reg.data_ref.slice(5, 7)}` : "";
  return opps
    .map((t, i): Pick | null => {
      const r = byT[t];
      if (!r) return null;
      const ceiling = ceilingPrice(r.engine, ke);
      const strong = ceilingPrice(r.engine, ke + 0.05);
      const call = callOf(r.L.price, ceiling, strong);
      const fb = frozenBuy(recs[t]?.situacao);
      const nowBuy = call.tone === "none" ? null : call.tone !== "out";
      const was = fb !== null && nowBuy !== null && fb !== nowBuy ? `era ${fb ? "Compra" : "Aguardar"} em ${refDate}` : null;
      return {
        r,
        rank: i + 1,
        tone: call.tone,
        call,
        ceiling,
        weight: w[t] ?? null,
        href: reports.includes(t) ? `/relatorio/${t}` : `/empresa/${t}`,
        name: names[t] ?? r.name,
        thesis: theses[t] ?? null,
        was,
      };
    })
    .filter((x): x is Pick => x !== null);
}

/** Setor visível, menos quando repete o nome da empresa ("Vitru Educação" + "Educação"). */
const sectorShown = (p: Pick) => {
  const sec = sectorShort(p.r.sector);
  return sec !== "—" && !p.name.toLowerCase().includes(sec.toLowerCase());
};

type Filter = "all" | "buy" | "wait";
const isBuy = (t: Tone) => t === "in" || t === "strong";

/** Tabela de top picks, com a caixa de recomendação na ponta de cada linha. */
export function PicksTable({ picks, reg }: { picks: Pick[]; reg?: Registro | null }) {
  const [f, setF] = useState<Filter>("all");
  const nBuy = picks.filter((p) => isBuy(p.tone)).length;
  const nWait = picks.filter((p) => p.tone === "out").length;
  const shown = picks.filter((p) => (f === "all" ? true : f === "buy" ? isBuy(p.tone) : p.tone === "out"));
  const opts: { k: Filter; label: string; n: number }[] = [
    { k: "all", label: "Todas", n: picks.length },
    { k: "buy", label: "Compra", n: nBuy },
    { k: "wait", label: "Aguardar", n: nWait },
  ];
  return (
    <section aria-labelledby="carteira-h" className="mt-6">
      <div className="flex flex-wrap items-center gap-x-5 gap-y-2">
        <h2 id="carteira-h" className="h2">
          Carteira recomendada
        </h2>
        <div role="group" aria-label="Filtrar recomendações" className="flex overflow-hidden rounded-[2px] border border-hairline">
          {opts.map((o) => (
            <button
              key={o.k}
              type="button"
              aria-pressed={f === o.k}
              onClick={() => setF(o.k)}
              className={`px-3 py-1 text-[13px] font-semibold transition-colors ${f === o.k ? "bg-[var(--navy)] text-white" : "text-ink-2 hover:bg-surface-2"}`}
            >
              {o.label} <span className={`num font-medium ${f === o.k ? "text-[var(--on-navy-2)]" : "text-muted"}`}>{o.n}</span>
            </button>
          ))}
        </div>
        {reg && (
          <span className="text-[12.5px] text-muted sm:ml-auto">
            Pesos somam {pct(reg.carteira.acoes, 0)} do capital; os outros {pct(reg.carteira.cdi, 0)} ficam em CDI
          </span>
        )}
      </div>

      {/* desktop: tabela */}
      <div className="mt-3 hidden md:block">
        <table className="data text-[13.5px]">
          <thead>
            <tr>
              <th className="w-8 !text-left">#</th>
              <th className="!text-left">Ação</th>
              <th className="!text-left">Tese</th>
              <th>Preço</th>
              <th>Valor justo</th>
              <th>
                TIR de dono
                <span className="block font-medium text-muted">chance</span>
              </th>
              <th>Peso</th>
              <th className="!text-right">Recomendação</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((p) => (
              <tr key={p.r.ticker} className={p.tone === "out" ? "text-ink-2" : ""}>
                <td className="text-left text-muted">{p.rank}</td>
                <td className="text-left">
                  <Link href={p.href} className="block font-bold text-ink hover:text-accent hover:underline">
                    {p.r.ticker}
                  </Link>
                  <span className="block max-w-[10rem] truncate text-[12px] text-muted" title={`${p.name}, ${sectorShort(p.r.sector)}`}>
                    {p.name}
                  </span>
                  {sectorShown(p) && <span className="block max-w-[10rem] truncate text-[12px] text-muted">{sectorShort(p.r.sector)}</span>}
                </td>
                <td className="min-w-[12rem] !whitespace-normal text-left text-[13px] leading-snug text-ink-2">{p.thesis ?? "—"}</td>
                <td>
                  <div className="font-semibold text-ink">{brl(p.r.L.price)}</div>
                  <div className={`text-[12px] ${p.r.src ? signClass(p.r.chgLive) : "text-muted"}`}>{p.r.src ? `${pct(p.r.chgLive, 1, true)} hoje` : "sem cotação ao vivo"}</div>
                </td>
                <td>{brl(p.r.L.fair)}</td>
                <td>
                  <div className="font-semibold">{pct(p.r.L.irr, 1)}</div>
                  <div className="text-[12px] text-muted">{pct(p.r.L.prob, 0)}</div>
                </td>
                <td>{pct(p.weight, 1)}</td>
                <td className="!py-2 text-right">
                  <Rating className="rating-fixed" c={p.call} ceiling={p.ceiling} upside={p.r.L.upside} />
                  {p.was && <div className="mt-1 text-[12px] text-muted">{p.was}</div>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* celular: lista */}
      <ul className="mt-3 divide-y divide-[var(--hairline)] border-y border-hairline md:hidden">
        {shown.map((p) => (
          <li key={p.r.ticker} className="py-3">
            <div className="flex items-baseline justify-between gap-3">
              <Link href={p.href} className="min-w-0">
                <span className="mr-2 text-[12px] text-muted">{p.rank}</span>
                <span className="text-[16px] font-bold text-ink">{p.r.ticker}</span>
                <span className="ml-2 text-[12px] text-muted">
                  {p.name}
                  {sectorShown(p) ? `, ${sectorShort(p.r.sector).toLowerCase()}` : ""}
                </span>
              </Link>
              <span className="num shrink-0 text-right">
                <span className="font-semibold">{brl(p.r.L.price)}</span>
                {p.r.src && <span className={`ml-1.5 text-[12px] ${signClass(p.r.chgLive)}`}>{pct(p.r.chgLive, 1, true)}</span>}
              </span>
            </div>
            {p.thesis && <p className="mt-1 text-[13px] leading-snug text-ink-2">{p.thesis}</p>}
            <Rating className="mt-2 w-full grid-cols-[auto_1fr_1fr]" c={p.call} ceiling={p.ceiling} upside={p.r.L.upside} />
            {p.was && <div className="mt-1 text-[12px] text-muted">{p.was}</div>}
            <dl className="num mt-2 grid grid-cols-4 gap-2 text-[12px]">
              <div>
                <dt className="text-muted">Valor justo</dt>
                <dd className="font-semibold">{num(p.r.L.fair)}</dd>
              </div>
              <div>
                <dt className="text-muted">TIR de dono</dt>
                <dd className="font-semibold">{pct(p.r.L.irr, 1)}</dd>
              </div>
              <div>
                <dt className="text-muted">Chance</dt>
                <dd className="font-semibold">{pct(p.r.L.prob, 0)}</dd>
              </div>
              <div>
                <dt className="text-muted">Peso</dt>
                <dd className="font-semibold">{pct(p.weight, 1)}</dd>
              </div>
            </dl>
          </li>
        ))}
      </ul>
      {shown.length === 0 && (
        <p className="border-b border-hairline py-6 text-[13px] text-ink-2">
          {f === "buy" ? "Nenhuma recomendação está na faixa de compra ao preço de agora. Veja quanto falta para cada uma em Aguardar." : "Todas as recomendações estão na faixa de compra ao preço de agora."}
        </p>
      )}
    </section>
  );
}

function Row({ label, value, cls = "", note }: { label: string; value: string; cls?: string; note?: string }) {
  return (
    <div className="flex items-baseline justify-between gap-3 border-b border-[var(--hairline)] py-1.5 last:border-b-0">
      <dt className="text-[13px] text-ink-2">
        {label}
        {note && <span className="block text-[12px] text-muted">{note}</span>}
      </dt>
      <dd className={`num shrink-0 text-[13.5px] font-bold ${cls}`}>{value}</dd>
    </div>
  );
}

/** Coluna lateral da nota: dados-chave, alocação e resultado desde a recomendação. */
export function KeyData({ items, reg, rows }: { items: { label: string; value: string; cls?: string; note?: string }[]; reg?: Registro | null; rows: LiveRow[] }) {
  const m = useMarket();
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const tr = reg ? trackRecord(reg, (t) => (byT[t]?.src ? byT[t].L.price : null), m?.indices?.IBOV?.price, m?.indices?.SMLL?.price) : null;
  const sc = (v: number | null) => signClass(v);
  return (
    <aside className="keybox rounded-none border-t-2 border-[var(--rule)] px-4 pb-4 pt-3" aria-label="Dados-chave">
      <h2 className="text-[15px] font-bold">Dados-chave</h2>
      <dl className="mt-1.5">
        {items.map((it) => (
          <Row key={it.label} {...it} />
        ))}
      </dl>

      {reg && (
        <>
          <h2 className="mt-5 text-[15px] font-bold">Alocação</h2>
          <div className="mt-2 flex h-2.5 overflow-hidden rounded-[1px]" role="img" aria-label={`Ações ${pct(reg.carteira.acoes, 0)}, CDI ${pct(reg.carteira.cdi, 0)}`}>
            <div className="bg-[var(--fill-1)]" style={{ width: `${reg.carteira.acoes * 100}%` }} />
            <div className="ml-[2px] flex-1 bg-[var(--axis)]" />
          </div>
          <div className="mt-1 flex justify-between text-[12px] text-ink-2">
            <span>Ações {pct(reg.carteira.acoes, 0)}</span>
            <span>CDI {pct(reg.carteira.cdi, 0)}</span>
          </div>
          <dl className="mt-1">
            {fin(reg.carteira.entrada_sugerida) && <Row label="Entrada sugerida agora" value={`${pct(reg.carteira.entrada_sugerida, 0)} do capital`} />}
            {fin(reg.carteira.retorno_esperado) && <Row label="Retorno esperado" value={`${pct(reg.carteira.retorno_esperado, 1)} a.a.`} />}
            {fin(reg.carteira.vol) && <Row label="Volatilidade" value={pct(reg.carteira.vol, 1)} />}
          </dl>
          <p className="mt-1 text-[12px] text-muted">Até {pct(reg.carteira.acoes_vol_normal ?? reg.carteira.acoes, 0)} em ações quando a volatilidade normalizar.</p>

          {tr && (
            <>
              <h2 className="mt-5 text-[15px] font-bold">
                Desde a recomendação <span className="text-[12.5px] font-medium text-muted">{tr.du === 1 ? "1 pregão" : `${tr.du} pregões`}</span>
              </h2>
              <dl className="mt-1.5">
                <Row label="Carteira (ações + CDI)" value={pct(tr.port, 1, true)} cls={sc(tr.port)} />
                <Row label="Só ações" value={pct(tr.eqW, 1, true)} cls={sc(tr.eqW)} />
                <Row label="Ibovespa" value={pct(tr.ib, 1, true)} cls={sc(tr.ib)} />
                <Row label="Small Caps" value={pct(tr.sm, 1, true)} cls={sc(tr.sm)} />
                <Row label="CDI" value={pct(tr.cdiAcc, 1, true)} cls={sc(tr.cdiAcc)} />
                <Row label={`Mediana das ${reg.universo.length - reg.recomendacoes.length} não selecionadas`} value={pct(tr.medOthers, 1, true)} cls={sc(tr.medOthers)} />
                {tr.beat !== null && <Row label="À frente do Ibovespa" value={`${tr.beat} de ${tr.nHave}`} />}
              </dl>
              <p className="mt-1 text-[12px] text-muted">
                Preços de {dataBR(reg.data_ref)} contra agora; retorno de preço, sem proventos.{" "}
                <Link href="/registro" className="link">
                  Ver registro
                </Link>
              </p>
            </>
          )}
        </>
      )}
    </aside>
  );
}
