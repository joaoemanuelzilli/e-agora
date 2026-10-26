"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { Dumbbell, IrrMeter, Sparkline } from "@/components/charts/Points";
import { brl, mult, num, pct, signClass } from "@/lib/format";
import { useKe, useQuotes } from "@/lib/live";
import type { Row } from "@/lib/types";
import { live, type LiveMetrics } from "@/lib/valuation";

export type LiveRow = Row & { L: LiveMetrics; chgLive: number | null; ts: string | null; src: string | null };

export function useLiveRows(rows: Row[]) {
  const { ke } = useKe();
  const tickers = useMemo(() => rows.map((r) => r.ticker), [rows]);
  const q = useQuotes(tickers, 30000);
  const out: LiveRow[] = useMemo(
    () =>
      rows.map((r) => {
        const lq = q.quotes[r.ticker];
        const price = lq?.price ?? r.price_ref;
        const chgLive = lq?.chg ?? r.chg_snapshot ?? null;
        return { ...r, L: live(r.engine, price, ke, r.mc_q, r.fair_value), chgLive, ts: lq?.ts ?? null, src: lq?.source ?? null };
      }),
    [rows, q.quotes, ke],
  );
  return { rows: out, ke, asOf: q.asOf, loading: q.loading, error: q.error };
}

type SortKey = "irr" | "upside" | "chg" | "pe" | "dy" | "prob" | "score" | "ticker" | "irr3" | "roe" | "vsrally";

function val(r: LiveRow, k: SortKey): number | string {
  switch (k) {
    case "irr":
      return r.L.irr ?? -9;
    case "irr3":
      return r.L.irr3 ?? -9;
    case "upside":
      return r.L.upside ?? -9;
    case "chg":
      return r.chgLive ?? 0;
    case "pe":
      return r.L.pe ?? 999;
    case "dy":
      return r.L.dy ?? -1;
    case "prob":
      return r.L.prob ?? -1;
    case "score":
      return r.score ?? -9;
    case "roe":
      return avg(r.roe_3y) ?? -9;
    case "vsrally":
      return r.now_vs_pre_rally ?? 9;
    default:
      return r.ticker;
  }
}

export const avg = (a?: (number | null)[] | null) => {
  const v = (a || []).filter((x): x is number => typeof x === "number" && Number.isFinite(x));
  return v.length ? v.reduce((s, x) => s + x, 0) / v.length : null;
};

export function Hero({ rows, ke }: { rows: LiveRow[]; ke: number }) {
  const sorted = [...rows].filter((r) => r.L.price).sort((a, b) => (b.L.irr ?? -1) - (a.L.irr ?? -1));
  return (
    <Dumbbell
      ke={ke}
      title="Preço de hoje contra valor justo, das 59 que mais caíram"
      subtitle={`Ordenado pela TIR de dono. Faixa azul: TIR acima do Ke de ${Math.round(ke * 100)}%. Escala logarítmica.`}
      rows={sorted.map((r) => ({ ticker: r.ticker, name: r.name, price: r.L.price as number, fair: r.L.fair, pre: r.prev_close, irr: r.L.irr, href: `/empresa/${r.ticker}` }))}
      table={{
        columns: ["Ticker", "Preço", "Valor justo", "Upside", "Pré-eleição", "TIR dono"],
        rows: sorted.map((r) => [r.ticker, brl(r.L.price), brl(r.L.fair), pct(r.L.upside, 1, true), brl(r.prev_close), pct(r.L.irr, 1)]),
      }}
    />
  );
}

export function Screener({ rows, ke, opps }: { rows: LiveRow[]; ke: number; opps: string[] }) {
  const [sort, setSort] = useState<{ k: SortKey; dir: 1 | -1 }>({ k: "irr", dir: -1 });
  const [sector, setSector] = useState<string>("Todos");
  const [onlyKe, setOnlyKe] = useState(false);
  const [qtext, setQtext] = useState("");
  const sectors = useMemo(() => ["Todos", ...Array.from(new Set(rows.map((r) => r.sector?.setor || "Outros"))).sort()], [rows]);
  const list = rows
    .filter((r) => sector === "Todos" || (r.sector?.setor || "Outros") === sector)
    .filter((r) => !onlyKe || (r.L.irr ?? -1) >= ke)
    .filter((r) => !qtext || `${r.ticker} ${r.name}`.toLowerCase().includes(qtext.toLowerCase()))
    .sort((a, b) => {
      const va = val(a, sort.k);
      const vb = val(b, sort.k);
      return (va < vb ? -1 : va > vb ? 1 : 0) * sort.dir;
    });
  const th = (k: SortKey, label: string, title?: string) => (
    <th
      onClick={() => setSort((s) => ({ k, dir: s.k === k ? (s.dir === 1 ? -1 : 1) : k === "ticker" || k === "pe" || k === "vsrally" ? 1 : -1 }))}
      className="cursor-pointer select-none hover:text-ink"
      title={title}
      aria-sort={sort.k === k ? (sort.dir === 1 ? "ascending" : "descending") : "none"}
    >
      {label}
      {sort.k === k ? (sort.dir === 1 ? " ↑" : " ↓") : ""}
    </th>
  );
  return (
    <section className="panel">
      <div className="flex flex-wrap items-center gap-3 border-b border-hairline px-4 py-3">
        <h2 className="h2 mr-2">Todas as empresas</h2>
        <input
          value={qtext}
          onChange={(e) => setQtext(e.target.value)}
          placeholder="Buscar ticker ou nome"
          className="w-44 rounded border border-hairline bg-surface px-2 py-1 text-[13px] outline-none focus:border-accent"
          aria-label="Buscar"
        />
        <select value={sector} onChange={(e) => setSector(e.target.value)} className="rounded border border-hairline bg-surface px-2 py-1 text-[13px]" aria-label="Setor">
          {sectors.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
        <label className="flex items-center gap-1.5 text-[13px] text-ink-2">
          <input type="checkbox" checked={onlyKe} onChange={(e) => setOnlyKe(e.target.checked)} />
          Só TIR ≥ Ke
        </label>
        <span className="ml-auto text-[12px] text-muted">{list.length} empresas</span>
      </div>
      <div className="overflow-x-auto">
        <table className="data min-w-[1180px] text-[13px]">
          <thead>
            <tr>
              {th("ticker", "Empresa")}
              <th className="text-left">52 semanas</th>
              <th>Preço</th>
              {th("chg", "Dia")}
              {th("vsrally", "vs pré-rali", "Preço atual contra o fechamento de 14/08/2026, antes do rali eleitoral")}
              <th>Valor justo</th>
              {th("upside", "Upside")}
              {th("irr", "TIR dono", "TIR implícita: dividendos projetados + perpetuidade ao preço de hoje")}
              {th("irr3", "TIR 3 anos", "Dividendos 2026–28 + saída ao P/L alvo em 2028")}
              {th("dy", "DY 27E")}
              {th("roe", "ROE 26–28")}
              {th("pe", "P/L 27E")}
              {th("prob", "P(valor > preço)", "Monte Carlo com 5.000 cenários")}
              {th("score", "Escore", "Escore multifator: valor, qualidade, solidez, sobrerreação e probabilidade")}
            </tr>
          </thead>
          <tbody>
            {list.map((r) => {
              const meets = (r.L.irr ?? -1) >= ke;
              const isOpp = opps.includes(r.ticker);
              return (
                <tr key={r.ticker}>
                  <td>
                    <Link href={`/empresa/${r.ticker}`} className="group flex items-baseline gap-2">
                      <span className="font-semibold group-hover:text-accent">{r.ticker}</span>
                      <span className="max-w-[150px] truncate text-[12px] text-muted">{r.name}</span>
                      {isOpp && <span className="rounded bg-accent-soft px-1 text-[10.5px] text-accent-ink" style={{ background: "var(--accent-soft)" }}>relatório</span>}
                    </Link>
                    <div className="text-[11px] text-muted">{r.sector?.subsetor}</div>
                  </td>
                  <td className="text-left">
                    <Sparkline data={[...r.spark.slice(0, -1), r.L.price ?? r.spark[r.spark.length - 1]]} down={(r.chgLive ?? 0) < 0} />
                  </td>
                  <td>{num(r.L.price)}</td>
                  <td className={signClass(r.chgLive)}>{pct(r.chgLive, 1, true)}</td>
                  <td className={signClass(r.now_vs_pre_rally)}>{pct(r.now_vs_pre_rally, 0, true)}</td>
                  <td>{num(r.L.fair)}</td>
                  <td className={signClass(r.L.upside)}>{pct(r.L.upside, 0, true)}</td>
                  <td>
                    <div className="flex items-center justify-end gap-2">
                      <IrrMeter irr={r.L.irr} ke={ke} w={64} />
                      <span className={meets ? "font-semibold" : ""}>{pct(r.L.irr, 1)}</span>
                    </div>
                  </td>
                  <td>{pct(r.L.irr3, 0)}</td>
                  <td>{pct(r.L.dy, 1)}</td>
                  <td>{pct(avg(r.roe_3y), 0)}</td>
                  <td>{mult(r.L.pe)}</td>
                  <td>{pct(r.L.prob, 0)}</td>
                  <td>{r.rank ? `${r.rank}º` : "—"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export function OppCards({ rows, ke, opps }: { rows: LiveRow[]; ke: number; opps: string[] }) {
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const list = opps.map((t) => byT[t]).filter(Boolean);
  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
      {list.map((r) => (
        <Link key={r.ticker} href={`/relatorio/${r.ticker}`} className="panel group block p-4 hover:border-accent">
          <div className="flex items-baseline justify-between gap-2">
            <div className="flex items-baseline gap-2">
              <span className="text-[16px] font-semibold group-hover:text-accent">{r.ticker}</span>
              <span className="truncate text-[12px] text-muted">{r.name}</span>
            </div>
            <span className={`num text-[12px] ${signClass(r.chgLive)}`}>{pct(r.chgLive, 1, true)}</span>
          </div>
          <div className="mt-3 grid grid-cols-3 gap-2">
            <div>
              <div className="label">Preço</div>
              <div className="num text-[15px] font-medium">{num(r.L.price)}</div>
            </div>
            <div>
              <div className="label">Valor justo</div>
              <div className="num text-[15px] font-medium">{num(r.L.fair)}</div>
            </div>
            <div>
              <div className="label">Upside</div>
              <div className={`num text-[15px] font-medium ${signClass(r.L.upside)}`}>{pct(r.L.upside, 0, true)}</div>
            </div>
          </div>
          <div className="mt-3 flex items-center justify-between gap-3">
            <div>
              <div className="label">TIR de dono vs Ke {Math.round(ke * 100)}%</div>
              <div className="mt-1 flex items-center gap-2">
                <IrrMeter irr={r.L.irr} ke={ke} w={110} />
                <span className="num text-[13px] font-semibold">{pct(r.L.irr, 1)}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="label">P(valor &gt; preço)</div>
              <div className="num text-[13px] font-semibold">{pct(r.L.prob, 0)}</div>
            </div>
          </div>
          {r.summary && <p className="mt-3 line-clamp-3 text-[12.5px] leading-snug text-ink-2">{r.summary}</p>}
          <div className="mt-3 text-[12px] font-medium text-accent">Ler relatório</div>
        </Link>
      ))}
    </div>
  );
}
