"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { avg, useLiveRows } from "@/components/Dashboard";
import { HBarChart } from "@/components/charts/Bars";
import { CalendarHeatmap } from "@/components/charts/Calendar";
import { Scatter, Sparkline } from "@/components/charts/Points";
import { dateBR, monthYear, num, pct } from "@/lib/format";
import type { Row } from "@/lib/types";

export type DivEvent = { dc: string; tipo: string; valor: number; aprov?: string; preco_dc?: number | null; yield_dc?: number | null; pagamento?: string };
export type DivCo = {
  ticker: string;
  nome: string;
  eventos: DivEvent[];
  a_pagar: { dc: string | null; pagamento: string | null; a_definir?: boolean; tipo: string; valor: number | null; ref?: string; da_direito_hoje: boolean }[];
  annual: { ano: number; total: number; div: number; jcp: number; n: number }[];
  ttm: { total: number; n: number; dy: number | null; jcp_share: number | null };
  months: { mes: string; valor: number; eventos: { dc: string; tipo: string; valor: number }[] }[];
  season_2021_2025: number[];
  freq_3y: number;
  jcp_share_3y: number | null;
  anos_com_pagamento_10a: number;
  proj_dps: (number | null)[];
};
export type DivData = { gerado_em: string; fonte: string; hoje: string; empresas: DivCo[] };

const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
type SortKey = "dy" | "ticker" | "freq" | "jcp" | "anos" | "dy26" | "dy27" | "dy28" | "soma" | "roe" | "irr";

export function DividendMap({ rows, data, opps }: { rows: Row[]; data: DivData; opps: string[] }) {
  const { rows: live, ke } = useLiveRows(rows);
  const L = useMemo(() => Object.fromEntries(live.map((r) => [r.ticker, r])), [live]);
  const cos = data.empresas.map((c) => {
    const r = L[c.ticker];
    const price = r?.L.price ?? null;
    const dy = price && c.ttm.total ? c.ttm.total / price : 0;
    const proj = c.proj_dps.map((d) => (price && d !== null ? d / price : null));
    const soma = proj.slice(0, 3).reduce<number>((s, x) => s + (x ?? 0), 0);
    return { ...c, price, dy, proj, soma, roe: avg(r?.roe_3y), irr: r?.L.irr ?? null, chg: r?.chgLive ?? null };
  });
  const byDy = [...cos].sort((a, b) => b.dy - a.dy);
  const payers = cos.filter((c) => c.ttm.total > 0);
  const dys = payers.map((c) => c.dy).sort((a, b) => a - b);
  const medDy = dys.length ? dys[Math.floor(dys.length / 2)] : null;
  const upcoming = cos
    .flatMap((c) => c.a_pagar.map((u) => ({ ...u, ticker: c.ticker, nome: c.nome, price: c.price })))
    .sort((a, b) => (a.pagamento ?? "9999").localeCompare(b.pagamento ?? "9999"));
  // antecipação de dezembro de 2025 (antes da tributação de dividendos de 2026)
  const decHeavy = payers.filter((c) => {
    const dec = c.months.find((m) => m.mes === "2025-12")?.valor ?? 0;
    return c.ttm.total > 0 && dec / c.ttm.total > 0.5;
  }).length;
  const cols = cos[0]?.months.map((m) => monthYear(m.mes)) ?? [];
  const calRows = byDy.map((c) => ({
    id: c.ticker,
    label: c.ticker,
    href: `/empresa/${c.ticker}`,
    cells: c.months.map((m) => (c.price && m.valor ? m.valor / c.price : null)),
    detail: c.months.map((m) =>
      m.eventos.length ? (
        <div className="mt-1 space-y-0.5 text-[11px] text-ink-2">
          {m.eventos.map((e, i) => (
            <div key={i}>
              {e.tipo} de R$ {num(e.valor, 4)}, data-com {dateBR(e.dc)}
            </div>
          ))}
        </div>
      ) : null,
    ),
    total: c.dy ? pct(c.dy, 1) : "—",
  }));
  const seasonRows = byDy
    .filter((c) => c.season_2021_2025.some((x) => x > 0))
    .map((c) => ({ id: c.ticker, label: c.ticker, href: `/empresa/${c.ticker}`, cells: c.season_2021_2025.map((x) => (x > 0 ? x : null)), total: `${num(c.freq_3y, 1)}x` }));
  const [sort, setSort] = useState<{ k: SortKey; dir: 1 | -1 }>({ k: "dy", dir: -1 });
  const val = (c: (typeof cos)[number], k: SortKey): number | string => {
    switch (k) {
      case "ticker":
        return c.ticker;
      case "freq":
        return c.freq_3y;
      case "jcp":
        return c.jcp_share_3y ?? -1;
      case "anos":
        return c.anos_com_pagamento_10a;
      case "dy26":
        return c.proj[0] ?? -1;
      case "dy27":
        return c.proj[1] ?? -1;
      case "dy28":
        return c.proj[2] ?? -1;
      case "soma":
        return c.soma;
      case "roe":
        return c.roe ?? -9;
      case "irr":
        return c.irr ?? -9;
      default:
        return c.dy;
    }
  };
  const table = [...cos].sort((a, b) => {
    const va = val(a, sort.k);
    const vb = val(b, sort.k);
    return (va < vb ? -1 : va > vb ? 1 : 0) * sort.dir;
  });
  const th = (k: SortKey, label: string, title?: string) => (
    <th
      onClick={() => setSort((s) => ({ k, dir: s.k === k ? (s.dir === 1 ? -1 : 1) : k === "ticker" ? 1 : -1 }))}
      className={`cursor-pointer select-none hover:text-ink ${k === "ticker" ? "freeze-col" : ""}`}
      title={title}
      aria-sort={sort.k === k ? (sort.dir === 1 ? "ascending" : "descending") : "none"}
    >
      {label}
      {sort.k === k ? (sort.dir === 1 ? " ↑" : " ↓") : ""}
    </th>
  );
  const top20 = byDy.filter((c) => c.dy > 0).slice(0, 20);
  return (
    <div className="space-y-8">
      <section className="panel grid grid-cols-2 gap-4 p-5 md:grid-cols-4">
        <div>
          <div className="label">Pagaram nos últimos 12 meses</div>
          <div className="mt-0.5 text-[26px] font-semibold leading-tight">
            {payers.length} de {cos.length}
          </div>
        </div>
        <div>
          <div className="label">Yield mediano em 12 meses</div>
          <div className="mt-0.5 text-[26px] font-semibold leading-tight">{pct(medDy, 1)}</div>
          <div className="text-[12px] text-muted">entre as que pagaram, ao preço de agora</div>
        </div>
        <div>
          <div className="label">Maior yield em 12 meses</div>
          <div className="mt-0.5 text-[26px] font-semibold leading-tight">{byDy[0] ? `${byDy[0].ticker} ${pct(byDy[0].dy, 1)}` : "—"}</div>
        </div>
        <div>
          <div className="label">Pagamentos já aprovados a cair</div>
          <div className="mt-0.5 text-[26px] font-semibold leading-tight">{upcoming.length}</div>
          <div className="text-[12px] text-muted">de {new Set(upcoming.map((u) => u.ticker)).size} empresas</div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="panel overflow-x-auto p-4 lg:col-span-7">
          <div className="h3">Próximos pagamentos já aprovados</div>
          <p className="mt-0.5 text-[12px] text-muted">
            Recebe quem tinha a ação na data-com. Se a data-com já passou, comprar hoje não dá direito ao pagamento.
          </p>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Pagamento</th>
                <th>Empresa</th>
                <th>Tipo</th>
                <th>Data-com</th>
                <th>R$ por ação</th>
                <th>Yield ao preço atual</th>
                <th>Quem compra hoje</th>
              </tr>
            </thead>
            <tbody>
              {upcoming.map((u, i) => (
                <tr key={i}>
                  <td>{u.pagamento ? dateBR(u.pagamento) : "a definir"}</td>
                  <td>
                    <Link href={`/empresa/${u.ticker}`} className="font-semibold hover:text-accent">
                      {u.ticker}
                    </Link>
                  </td>
                  <td>{u.tipo}</td>
                  <td>{u.dc ? dateBR(u.dc) : "—"}</td>
                  <td>{num(u.valor, 4)}</td>
                  <td>{u.price && u.valor ? pct(u.valor / u.price, 2) : "—"}</td>
                  <td className={u.da_direito_hoje ? "pos font-medium" : "text-muted"}>{u.da_direito_hoje ? "ainda recebe" : "não recebe"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="lg:col-span-5">
          <HBarChart
            title="Maiores yields dos últimos 12 meses"
            subtitle="Proventos com data-com nos últimos 12 meses ÷ preço ao vivo (bruto, ajustado por eventos)"
            items={top20.map((c) => ({ label: c.ticker, value: c.dy, sub: `${c.ttm.n} pagamentos, R$ ${num(c.ttm.total, 2)} por ação`, highlight: opps.includes(c.ticker) }))}
            fmt="pct1"
            rowH={22}
            labelWidth={70}
            table={{ columns: ["Empresa", "Yield 12m", "R$ por ação"], rows: top20.map((c) => [c.ticker, pct(c.dy, 1), num(c.ttm.total, 4)]) }}
          />
        </div>
      </section>

      <CalendarHeatmap
        title="Calendário dos últimos 12 meses"
        subtitle={`Cada célula soma os proventos com data-com naquele mês, como yield sobre o preço de agora. Em ${decHeavy} das ${payers.length} pagadoras, mais da metade dos proventos de 12 meses teve data-com em dez/25: antecipação antes da tributação de dividendos de 2026, que infla o yield passado.`}
        cols={cols}
        rows={calRows}
        scaleMax={0.03}
        fmt={(v) => pct(v, 1)}
        totalLabel="12 meses"
        table={{ columns: ["Empresa", ...cols, "12 meses"], rows: calRows.map((r) => [r.label, ...r.cells.map((v) => (v ? pct(v, 2) : "")), r.total]) }}
      />

      <CalendarHeatmap
        title="Em que meses cada empresa costuma pagar"
        subtitle="Fração dos proventos de 2021 a 2025 por mês da data-com. Última coluna: pagamentos por ano (média 2023–25)."
        cols={MESES}
        rows={seasonRows}
        scaleMax={0.5}
        fmt={(v) => pct(v, 0)}
        totalLabel="por ano"
        legendNote="50% ou mais = mês concentra metade do ano"
      />

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <Scatter
            title="Yield projetado contra TIR de dono"
            subtitle={`Dividendos projetados para 2027 ÷ preço ao vivo contra a TIR de dono. Linha: Ke de ${Math.round(ke * 100)}%. Em azul, as oportunidades do estudo.`}
            points={cos
              .filter((c) => c.proj[1] !== null && c.irr !== null)
              .map((c) => ({ id: c.ticker, x: c.proj[1] as number, y: c.irr as number, highlight: opps.includes(c.ticker), label: opps.includes(c.ticker) ? c.ticker : undefined }))}
            xFmt="pct0"
            yFmt="pct0"
            xLabel="Yield projetado 2027"
            yLabel="TIR de dono"
            hRef={{ y: ke, label: `Ke ${Math.round(ke * 100)}%` }}
            height={340}
          />
        </div>
        <div className="panel p-4 text-[13px] leading-relaxed text-ink-2 lg:col-span-5">
          <div className="h3 text-ink">Como ler</div>
          <ul className="mt-2 list-disc space-y-1.5 pl-4">
            <li>Valores brutos por ação, em base de ações atual: proventos antigos foram divididos pelos desdobramentos e bonificações posteriores.</li>
            <li>JCP tem 17,5% de IR na fonte desde janeiro de 2026 (LC 224/2025). Dividendos têm 10% retidos sobre o total quando a mesma empresa paga mais de R$ 50 mil no mês à mesma pessoa física (Lei 15.270/2025).</li>
            <li>Yield de 12 meses olha para trás; o projetado vem do payout e do lucro das projeções de cada empresa.</li>
            <li>Parcelas de um mesmo dividendo aparecem separadas, como a MDNE3, que paga o dividendo de 2025 em 7 parcelas até setembro de 2027.</li>
            <li>Dezembro de 2025 concentrou dividendos antecipados para escapar da retenção de 2026; o yield de 12 meses dessas empresas tende a não se repetir. Para o futuro, use o yield projetado.</li>
          </ul>
          <p className="mt-3 text-[12px] text-muted">Fonte: B3, proventos em dinheiro e eventos corporativos. Atualizado em {dateBR(data.gerado_em.slice(0, 10))}.</p>
        </div>
      </section>

      <section className="panel sticky-host">
        <div className="flex flex-wrap items-baseline justify-between gap-3 border-b border-hairline px-4 py-3">
          <h2 className="h2">Quanto cada uma paga</h2>
          <span className="text-[12px] text-muted">Clique no título da coluna para ordenar</span>
        </div>
        <div className="freeze-wrap">
          <table className="data freeze min-w-[1040px] text-[13px]">
            <thead>
              <tr>
                {th("ticker", "Empresa")}
                {th("dy", "Yield 12m")}
                <th>R$ por ação 12m</th>
                {th("freq", "Pagamentos por ano")}
                {th("jcp", "Parcela em JCP")}
                {th("anos", "Anos com pagamento (10)")}
                <th className="!text-left">Por ação, 2016–2025</th>
                {th("dy26", "Yield 2026E")}
                {th("dy27", "Yield 2027E")}
                {th("dy28", "Yield 2028E")}
                {th("soma", "Soma 2026–28", "Dividendos projetados 2026–2028 ÷ preço ao vivo")}
                {th("roe", "ROE 2026–28")}
                {th("irr", "TIR de dono")}
              </tr>
            </thead>
            <tbody>
              {table.map((c) => {
                const hist = c.annual.filter((a) => a.ano >= 2016 && a.ano <= 2025);
                const series = Array.from({ length: 10 }, (_, i) => hist.find((a) => a.ano === 2016 + i)?.total ?? 0);
                return (
                  <tr key={c.ticker}>
                    <td className="freeze-col">
                      <Link href={`/empresa/${c.ticker}`} className="flex items-baseline gap-2 hover:text-accent">
                        <span className="font-semibold">{c.ticker}</span>
                        <span className="max-w-[120px] truncate text-[12px] text-muted">{c.nome}</span>
                      </Link>
                    </td>
                    <td className="font-semibold">{c.dy ? pct(c.dy, 1) : "—"}</td>
                    <td>{c.ttm.total ? num(c.ttm.total, 2) : "—"}</td>
                    <td>{c.freq_3y ? num(c.freq_3y, 1) : "—"}</td>
                    <td>{c.jcp_share_3y !== null ? pct(c.jcp_share_3y, 0) : "—"}</td>
                    <td>{c.anos_com_pagamento_10a}</td>
                    <td className="text-left">
                      <Sparkline data={series} w={88} />
                    </td>
                    <td>{pct(c.proj[0], 1)}</td>
                    <td>{pct(c.proj[1], 1)}</td>
                    <td>{pct(c.proj[2], 1)}</td>
                    <td className="font-medium">{pct(c.soma, 0)}</td>
                    <td>{pct(c.roe, 0)}</td>
                    <td className={(c.irr ?? -1) >= ke ? "font-semibold" : ""}>{pct(c.irr, 1)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
