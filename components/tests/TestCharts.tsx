"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { scaleLinear } from "d3-scale";
import { useState } from "react";
import { HBarChart } from "@/components/charts/Bars";
import { C, Frame, Tip, TipRow, useWidth, type LegendItem } from "@/components/charts/core";

const r2 = (v: number) => Math.round(v * 100) / 100;
const pctS = (v: number, d = 0) => `${v > 0 ? "+" : ""}${(v * 100).toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d })}%`;
const pctU = (v: number, d = 0) => `${(v * 100).toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d })}%`;
const dec = (v: number, d = 2) => v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);

type RRow = { label: string; lo: number | null; hi: number | null; mid: number | null; note?: string; strong?: boolean };

/** Faixa por linha (mínimo–máximo) com ponto central, em escala linear que aceita negativos e uma linha de referência. */
function RangeChart({ rows, title, subtitle, fmt, refValue, refLabel, legend, table, labelWidth = 150 }: {
  rows: RRow[]; title: string; subtitle?: string; fmt: (v: number) => string; refValue: number; refLabel: string;
  legend: LegendItem[]; table?: { columns: string[]; rows: (string | number)[][] }; labelWidth?: number;
}) {
  const [ref, w] = useWidth<HTMLDivElement>(720);
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const rowH = 26;
  const labelW = Math.min(labelWidth, Math.max(90, w * 0.32));
  const m = { t: 22, r: 16, b: 22, l: labelW };
  const iw = Math.max(80, w - m.l - m.r);
  const vals = rows.flatMap((x) => [x.lo, x.hi, x.mid]).filter(fin);
  const lo = Math.min(refValue, ...vals);
  const hi = Math.max(refValue, ...vals);
  const pad = (hi - lo) * 0.04 || 0.05;
  const x = scaleLinear().domain([lo - pad, hi + pad]).range([0, iw]).nice();
  const h = rows.length * rowH + m.t + m.b;
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title}>
          <g transform={`translate(${m.l},${m.t})`}>
            {x.ticks(6).map((t) => (
              <g key={t}>
                <line x1={r2(x(t))} x2={r2(x(t))} y1={0} y2={rows.length * rowH} stroke="var(--grid)" />
                <text x={r2(x(t))} y={rows.length * rowH + 15} textAnchor="middle" fontSize={11} fill="var(--muted)">
                  {fmt(t)}
                </text>
              </g>
            ))}
            {rows.map((d, i) => {
              const yy = i * rowH + rowH / 2;
              return (
                <g
                  key={d.label + i}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-labelW} y={i * rowH} width={labelW + iw + m.r} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
                  <text x={-8} y={yy} dy="0.32em" textAnchor="end" fontSize={12} fill="var(--ink)" fontWeight={d.strong ? 600 : 400}>
                    {d.label}
                  </text>
                  {fin(d.lo) && fin(d.hi) && (
                    <rect x={r2(x(Math.min(d.lo, d.hi)))} y={yy - 5} width={Math.max(3, r2(Math.abs(x(d.hi) - x(d.lo))))} height={10} rx={4} fill={C.proj} />
                  )}
                  {fin(d.mid) && <circle cx={r2(x(d.mid))} cy={yy} r={4.5} fill={C.s1} stroke="var(--surface)" strokeWidth={2} />}
                </g>
              );
            })}
            <line x1={r2(x(refValue))} x2={r2(x(refValue))} y1={-6} y2={rows.length * rowH} stroke="var(--ink)" strokeWidth={1.5} />
            <text x={r2(x(refValue))} y={-10} textAnchor="middle" fontSize={11} fill="var(--ink)" fontWeight={600}>
              {refLabel}
            </text>
          </g>
        </svg>
        {hover && rows[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">{rows[hover.i].label}</div>
            {fin(rows[hover.i].mid) && <TipRow color={C.s1} label="Central" value={fmt(rows[hover.i].mid as number)} />}
            {fin(rows[hover.i].lo) && <TipRow label="De" value={fmt(rows[hover.i].lo as number)} />}
            {fin(rows[hover.i].hi) && <TipRow label="Até" value={fmt(rows[hover.i].hi as number)} />}
            {rows[hover.i].note && <div className="mt-1 max-w-[260px] whitespace-normal text-[12px] text-muted">{rows[hover.i].note}</div>}
          </Tip>
        )}
      </div>
    </Frame>
  );
}

/** Mapa de calor divergente em torno de zero (azul positivo, vermelho negativo, cinza no meio). */
function ICHeatmap({ rows, cols, groups, title, subtitle, max = 0.4 }: {
  rows: { label: string; values: (number | null)[] }[]; cols: string[]; groups?: number[]; title: string; subtitle?: string; max?: number;
}) {
  const [ref, w] = useWidth<HTMLDivElement>(720);
  const [hover, setHover] = useState<{ r: number; c: number; px: number; py: number } | null>(null);
  const labelW = Math.min(160, Math.max(110, w * 0.24));
  const gap = 10;
  const nGap = groups?.length ?? 0;
  // cada cabeçalho quebra no último espaço: a célula precisa caber a linha mais longa (≈ 6,2px por caractere a 11px)
  const longestLine = Math.max(
    ...cols.map((c) => {
      const k = c.lastIndexOf(" ");
      return k > 0 ? Math.max(k, c.length - k - 1) : c.length;
    }),
    1,
  );
  const cellW = Math.max(34, longestLine * 6.2 + 10, (w - labelW - 8 - nGap * gap) / cols.length);
  const cellH = 24;
  const top = 46;
  const xOf = (c: number) => labelW + c * cellW + (groups ? groups.filter((g) => c >= g).length * gap : 0);
  const color = (v: number | null) => {
    if (!fin(v)) return "var(--surface-2)";
    const p = Math.round(Math.min(1, Math.abs(v) / max) * 100);
    return `color-mix(in oklab, ${v >= 0 ? "var(--series-1)" : "var(--div-neg)"} ${p}%, var(--div-mid))`;
  };
  const h = top + rows.length * cellH + 6;
  const table = { columns: ["Fator", ...cols], rows: rows.map((r) => [r.label, ...r.values.map((v) => (fin(v) ? dec(v) : "—"))]) };
  const legend: LegendItem[] = [
    { label: "IC positivo (o fator previu alta)", color: C.s1, kind: "rect" },
    { label: "IC negativo", color: C.neg, kind: "rect" },
  ];
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full overflow-x-auto">
        <svg className="chart block" width={Math.max(w, xOf(cols.length - 1) + cellW + 4)} height={h} role="img" aria-label={title}>
          {cols.map((c, j) => {
            const k = c.lastIndexOf(" ");
            const l1 = k > 0 ? c.slice(0, k) : c;
            const l2 = k > 0 ? c.slice(k + 1) : "";
            return (
              <text key={c} x={xOf(j) + cellW / 2} y={top - 22} textAnchor="middle" fontSize={11} fill="var(--muted)">
                <tspan x={xOf(j) + cellW / 2}>{l1}</tspan>
                <tspan x={xOf(j) + cellW / 2} dy={13}>
                  {l2}
                </tspan>
              </text>
            );
          })}
          {rows.map((r, i) => (
            <g key={r.label}>
              <text x={labelW - 8} y={top + i * cellH + cellH / 2} dy="0.32em" textAnchor="end" fontSize={12} fill="var(--ink)">
                {r.label}
              </text>
              {r.values.map((v, j) => (
                <g
                  key={j}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ r: i, c: j, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={xOf(j) + 1} y={top + i * cellH + 1} width={cellW - 2} height={cellH - 2} rx={3} fill={color(v)} stroke={hover?.r === i && hover?.c === j ? "var(--ink)" : "none"} />
                  <text x={xOf(j) + cellW / 2} y={top + i * cellH + cellH / 2} dy="0.32em" textAnchor="middle" fontSize={11} fill={fin(v) && Math.abs(v) / max > 0.62 ? "#ffffff" : "var(--ink)"}>
                    {fin(v) ? dec(v) : "—"}
                  </text>
                </g>
              ))}
            </g>
          ))}
        </svg>
        {hover && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">{rows[hover.r].label}</div>
            <TipRow label={cols[hover.c]} value={fin(rows[hover.r].values[hover.c]) ? dec(rows[hover.r].values[hover.c] as number) : "—"} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}

function Tiles({ items }: { items: { label: string; value: string; sub?: string }[] }) {
  return (
    <div className="panel grid grid-cols-2 gap-4 p-5 md:grid-cols-4">
      {items.map((t) => (
        <div key={t.label}>
          <div className="label">{t.label}</div>
          <div className="num text-[24px] font-semibold">{t.value}</div>
          {t.sub && <div className="text-[12px] text-muted">{t.sub}</div>}
        </div>
      ))}
    </div>
  );
}

export function FactorCharts({ f }: { f: any }) {
  if (!f) return null;
  const ic = [...(f.ic || [])].filter((x: any) => fin(x.h?.["12m"]?.ic)).sort((a: any, b: any) => b.h["12m"].ic - a.h["12m"].ic);
  const comps = [...(f.composites || [])].filter((c: any) => fin(c.oos)).sort((a: any, b: any) => b.oos - a.oos);
  const boot = f.bootstrap || [];
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <HBarChart
        title="Poder de previsão de cada fator em 12 meses"
        subtitle={`IC de Spearman médio, ${f.meta?.meses ?? ""} meses de ${f.meta?.de ?? ""} a ${f.meta?.ate ?? ""}; t de Newey-West ao lado`}
        items={ic.map((x: any) => ({ label: x.label, value: x.h["12m"].ic, sub: `t ${dec(x.h["12m"].t ?? 0, 1)}` }))}
        fmt={(v: number) => dec(v)}
        rowH={22}
        labelWidth={170}
        table={{ columns: ["Fator", "IC 1m", "IC 3m", "IC 6m", "IC 12m", "t 12m", "IC 12m 2017–22", "IC 12m 2023–26"], rows: ic.map((x: any) => [x.label, ...["1m", "3m", "6m", "12m"].map((h) => (fin(x.h[h]?.ic) ? dec(x.h[h].ic, 3) : "—")), fin(x.h["12m"]?.t) ? dec(x.h["12m"].t, 1) : "—", fin(x.is12) ? dec(x.is12, 3) : "—", fin(x.oos12) ? dec(x.oos12, 3) : "—"]) }}
      />
      <div className="space-y-4">
        <HBarChart
          title="Fora da amostra (2023–26), quem bateu o universo"
          subtitle="Excesso anual do quintil de cima sobre a média das ações; pesos estimados só em 2017–22"
          items={comps.map((c: any) => ({ label: c.label.length > 46 ? c.label.slice(0, 44) + "…" : c.label, value: c.oos, sub: fin(c.is) ? `2017–22 ${pctS(c.is, 1)}` : undefined }))}
          fmt={(v: number) => pctS(v, 1)}
          rowH={22}
          labelWidth={210}
          table={{ columns: ["Composto", "2017–22", "2023–26"], rows: comps.map((c: any) => [c.label, fin(c.is) ? pctS(c.is, 1) : "—", pctS(c.oos, 1)]) }}
        />
        <RangeChart
          title="Peso ótimo por bloco, com incerteza"
          subtitle="Bootstrap de 200 reamostragens: mediana e intervalo de 90%"
          rows={boot.map((b: any) => ({ label: b.label, lo: b.p05, hi: b.p95, mid: b.median, note: fin(b.prob_pos) ? `peso positivo em ${pctU(b.prob_pos)} das reamostragens` : undefined }))}
          fmt={(v: number) => pctU(v)}
          refValue={0}
          refLabel="zero"
          legend={[{ label: "Intervalo de 90%", color: C.proj, kind: "rect" }, { label: "Mediana", color: C.s1, kind: "dot" }]}
          labelWidth={110}
          table={{ columns: ["Bloco", "Mediana", "P5", "P95", "P(peso > 0)"], rows: boot.map((b: any) => [b.label, pctU(b.median ?? 0), pctU(b.p05 ?? 0), pctU(b.p95 ?? 0), fin(b.prob_pos) ? pctU(b.prob_pos) : "—"]) }}
        />
      </div>
    </div>
  );
}

export function CrashCharts({ c }: { c: any }) {
  if (!c) return null;
  const clusters: string[] = c.clusters || [];
  const order = ["Joesley 2017", "Greve 2018", "Covid 2020", "2ª onda 2020", "Petrobras 2021", "Eleição 2022", "Flávio 2025"].filter((x) => clusters.includes(x));
  const cols = [...order, "Média pânicos", "Média eleitorais"];
  const rows = (c.ic6 || []).map((x: any) => ({ label: x.label, values: [...order.map((cl) => x.per_cluster?.[cl] ?? null), x.panico ?? null, x.eleitoral ?? null] }));
  const rk = c.ranking || [];
  return (
    <div className="space-y-4">
      <ICHeatmap
        title="O que previu a recuperação em 6 meses, crise a crise"
        subtitle="IC de Spearman entre o fator no dia do choque e o retorno dos 6 meses seguintes. Beta muda de sinal: ajudou nos pânicos e atrapalhou nos choques eleitorais"
        rows={rows}
        cols={cols}
        groups={[order.length]}
      />
      <RangeChart
        title="Retorno esperado em 3 meses pelo modelo de crises"
        subtitle="15 maiores da cobertura, compra no preço de 26/10; faixa de 80% dominada pela trajetória do mercado"
        rows={rk.map((x: any) => ({ label: x.ticker, lo: x.lo, hi: x.hi, mid: x.exp, note: fin(x.vs_ibov) ? `contra o Ibovespa ${pctS(x.vs_ibov, 1)}` : undefined }))}
        fmt={(v: number) => pctS(v)}
        refValue={0}
        refLabel="zero"
        legend={[{ label: "Faixa de 80%", color: C.proj, kind: "rect" }, { label: "Esperado", color: C.s1, kind: "dot" }]}
        labelWidth={80}
        table={{ columns: ["Ticker", "Esperado 3m", "P10", "P90", "vs Ibovespa"], rows: rk.map((x: any) => [x.ticker, pctS(x.exp ?? 0, 1), pctS(x.lo ?? 0, 1), pctS(x.hi ?? 0, 1), fin(x.vs_ibov) ? pctS(x.vs_ibov, 1) : "—"]) }}
      />
    </div>
  );
}

export function RobustCharts({ rb }: { rb: any }) {
  if (!rb) return null;
  const grids = rb.grids || [];
  const joint = (rb.joint || []).filter((x: any) => fin(x.price) && x.price > 0);
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <HBarChart
        title="Quanto do top 7 por upside sobrevive a cada choque"
        subtitle="Fração média do top 7 da base que continua no top 7; a TIR de dono não depende dos pesos nem do Ke"
        items={grids.filter((g: any) => fin(g.top7_up)).map((g: any) => ({ label: g.label.length > 40 ? g.label.slice(0, 38) + "…" : g.label, value: g.top7_up, sub: fin(g.sp_up) ? `Spearman ${dec(g.sp_up)}` : undefined }))}
        fmt={(v: number) => pctU(v)}
        domain={[0, 1]}
        rowH={24}
        labelWidth={200}
        table={{ columns: ["Grade", "Combinações", "Spearman TIR", "Spearman upside", "Mínimo upside", "Top 7 TIR mantido", "Top 7 upside mantido", "Oportunidades mantidas"], rows: grids.map((g: any) => [g.label, g.n ?? "—", fin(g.sp_irr) ? dec(g.sp_irr) : "—", fin(g.sp_up) ? dec(g.sp_up) : "—", fin(g.sp_up_min) ? dec(g.sp_up_min) : "—", fin(g.top7_irr) ? pctU(g.top7_irr) : "—", fin(g.top7_up) ? pctU(g.top7_up) : "—", fin(g.kept) ? dec(g.kept, 1) : "—"]) }}
      />
      <RangeChart
        title="Valor justo contra o preço em todas as combinações"
        subtitle="P5 a P95 do valor justo nas 3.000 combinações conjuntas, em % do preço; ao lado, frequência no top 7 por TIR"
        rows={joint.map((x: any) => ({ label: `${x.ticker}  ${pctU(x.top7_irr ?? 0)}`, lo: x.p5 / x.price - 1, hi: x.p95 / x.price - 1, mid: x.p50 / x.price - 1, strong: (x.top7_irr ?? 0) >= 0.8 }))}
        fmt={(v: number) => pctS(v)}
        refValue={0}
        refLabel="preço"
        legend={[{ label: "P5 a P95", color: C.proj, kind: "rect" }, { label: "Mediana", color: C.s1, kind: "dot" }]}
        labelWidth={110}
        table={{ columns: ["Ticker", "Preço", "VJ P5", "VJ mediana", "VJ P95", "Top 7 TIR", "Top 7 upside"], rows: joint.map((x: any) => [x.ticker, dec(x.price), dec(x.p5), dec(x.p50), dec(x.p95), pctU(x.top7_irr ?? 0), pctU(x.top7_up ?? 0)]) }}
      />
    </div>
  );
}

export function AltCharts({ a }: { a: any }) {
  if (!a) return null;
  const bias = [...(a.bias || [])].filter((b: any) => fin(b.median)).sort((x: any, y: any) => x.median - y.median);
  const sch = a.schemes || [];
  return (
    <div className="space-y-4">
      <RangeChart
        title="Cada método contra o valor justo do estudo"
        subtitle="Mediana entre as empresas e faixa P25–P75. Intrínsecos confirmam DCF e DDM; múltiplos de mercado embutem Ke de 11–14% e ficam muito acima"
        rows={bias.map((b: any) => ({ label: b.label, lo: b.p25, hi: b.p75, mid: b.median, note: `${b.n} empresas` }))}
        fmt={(v: number) => pctS(v)}
        refValue={0}
        refLabel="valor justo do estudo"
        legend={[{ label: "P25 a P75", color: C.proj, kind: "rect" }, { label: "Mediana", color: C.s1, kind: "dot" }]}
        labelWidth={190}
        table={{ columns: ["Método", "Empresas", "Mediana", "P25", "P75"], rows: bias.map((b: any) => [b.label, b.n, pctS(b.median, 1), fin(b.p25) ? pctS(b.p25, 1) : "—", fin(b.p75) ? pctS(b.p75, 1) : "—"]) }}
      />
      <div className="panel sticky-host">
        <div className="freeze-wrap">
          <table className="data freeze min-w-[720px] text-[13px]">
            <thead>
              <tr>
                <th className="freeze-col">Esquema de pesos</th>
                <th>Upside mediano</th>
                <th>Empresas com upside</th>
                <th className="!text-left">Oportunidades pela regra</th>
              </tr>
            </thead>
            <tbody>
              {sch.map((s: any) => (
                <tr key={s.key}>
                  <td className="freeze-col font-medium">{s.label}</td>
                  <td>{fin(s.median_upside) ? pctS(s.median_upside) : "—"}</td>
                  <td>{s.n_pos ?? "—"}</td>
                  <td className="whitespace-normal text-left text-ink-2">{(s.opps || []).join(", ") || "nenhuma"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export function PortfolioCharts({ p }: { p: any }) {
  if (!p) return null;
  const m = p.metrics || {};
  const sz = p.sizing || {};
  const w = [...(p.weights || [])].sort((a: any, b: any) => b.w - a.w);
  const st = p.stress || [];
  return (
    <div className="space-y-4">
      <Tiles
        items={[
          { label: "Em ações na carteira-alvo", value: pctU(m.invested ?? 0), sub: `resto em CDI a ${pctU(p.cdi ?? 0, 2)}` },
          { label: "Entrada sugerida agora", value: pctU(sz.entry_equity ?? 0), sub: "meio Kelly em regime de choque" },
          { label: "Retorno esperado", value: pctU(m.exp_total_tir ?? 0, 1), sub: `vol ${pctU(m.vol ?? 0, 1)}, beta ${dec(m.beta ?? 0)}` },
          { label: "VaR 95% de 1 mês", value: pctU(m.var95_1m_param ?? 0, 1), sub: `Sharpe ${dec(m.sharpe_tir ?? 0)}` },
        ]}
      />
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <HBarChart
          title="Carteira-alvo"
          subtitle="% do capital; 50% máximo Sharpe pela TIR e 50% paridade de risco, até 20% por ação e 40% por setor"
          items={[...w.map((x: any) => ({ label: x.ticker, value: x.w, sub: fin(x.irr) ? `TIR ${pctU(x.irr, 1)}` : undefined })), { label: "CDI", value: m.cash_cdi ?? 0 }]}
          fmt={(v: number) => pctU(v, 1)}
          rowH={24}
          labelWidth={80}
          table={{ columns: ["Ativo", "% do capital", "TIR", "Contribuição ao risco"], rows: [...w.map((x: any) => [x.ticker, pctU(x.w, 1), fin(x.irr) ? pctU(x.irr, 1) : "—", fin(x.rc) ? pctU(x.rc, 1) : "—"]), ["CDI", pctU(m.cash_cdi ?? 0, 1), pctU(p.cdi ?? 0, 2), "0%"]] }}
        />
        <HBarChart
          title="Estresses na carteira-alvo"
          subtitle="Efeito imediato sobre o capital total, já com a parte em CDI"
          items={st.map((s: any) => ({ label: s.label, value: s.value }))}
          fmt={(v: number) => pctS(v, 1)}
          rowH={24}
          labelWidth={200}
          table={{ columns: ["Cenário", "Carteira"], rows: st.map((s: any) => [s.label, pctS(s.value, 1)]) }}
        />
      </div>
    </div>
  );
}

export function ConsensusChart({ rows }: { rows: any[] }) {
  if (!rows?.length) return null;
  const items = rows.filter((x) => fin(x.gap));
  return (
    <HBarChart
      title="Valor justo do estudo contra o preço-alvo mediano dos bancos"
      subtitle={`${items.length} empresas. O estudo fica abaixo do consenso em todas: a diferença vem sobretudo do Ke de 25% contra 12–16% das casas`}
      items={items.map((x) => ({ label: x.ticker, value: x.gap, sub: `${dec(x.fair)} × ${dec(x.consensus)}` }))}
      fmt={(v: number) => pctS(v)}
      rowH={18}
      labelWidth={70}
      table={{ columns: ["Ticker", "Preço", "Valor justo do estudo", "Consenso (mediana)", "Diferença"], rows: items.map((x) => [x.ticker, fin(x.price) ? dec(x.price) : "—", dec(x.fair), dec(x.consensus), pctS(x.gap, 1)]) }}
    />
  );
}

const BLOCKS: Record<string, string> = { cvm: "Dados da CVM", mercado: "Mercado e B3", modelo: "Saídas do modelo", paridade: "Motor TS × Python", app: "Rotas do site" };

export function SuiteTiles({ s }: { s: any }) {
  if (!s?.totals) return null;
  const t = s.totals;
  const bl = Object.entries(s.blocks || {}) as [string, any][];
  return (
    <div className="space-y-4">
      <Tiles
        items={[
          { label: "Testes", value: t.tests.toLocaleString("pt-BR") },
          { label: "Aprovados", value: t.passed.toLocaleString("pt-BR"), sub: pctU(t.passed / t.tests, 1) },
          { label: "Falhas", value: t.failed.toLocaleString("pt-BR"), sub: "a maioria em empresas fora da cobertura" },
          { label: "Build do site", value: s.next_build?.rc === 0 ? "ok" : "falhou", sub: s.next_build?.pages ? `${s.next_build.pages} páginas` : undefined },
        ]}
      />
      <HBarChart
        title="Falhas por bloco"
        subtitle={`Rodada de ${(s.generated_at || "").replace("T", " ").slice(0, 16)}`}
        items={bl.map(([k, v]) => ({ label: BLOCKS[k] ?? k, value: v.failed ?? 0, sub: `${(v.passed ?? 0).toLocaleString("pt-BR")} aprovados` }))}
        fmt={(v: number) => v.toLocaleString("pt-BR")}
        rowH={24}
        labelWidth={150}
      />
    </div>
  );
}
