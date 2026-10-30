"use client";
import { scaleBand, scaleLinear, scaleLog } from "d3-scale";
import { useState } from "react";
import { C, Frame, Tip, TipRow, YGrid, toFn, useWidth, type Fmt, type LegendItem, type TableSpec } from "./core";
import { ellipsize, fitTicks, lineSegs, textW } from "./measure";

const r2 = (v: number) => Math.round(v * 100) / 100;
const pctS = (v: number, d = 0) => `${v > 0 ? "+" : ""}${(v * 100).toLocaleString("pt-BR", { maximumFractionDigits: d, minimumFractionDigits: d })}%`;

export type DumbRow = {
  ticker: string;
  name: string;
  price: number;
  fair: number | null;
  pre: number | null; // fechamento pré-eleição (23/10)
  irr: number | null;
  href?: string;
  highlight?: boolean;
};

/** Hero: preço de hoje (0%) → valor justo, com o preço pré-eleição como anel. Escala log da razão. */
export function Dumbbell({ rows, ke, title, subtitle, table }: { rows: DumbRow[]; ke: number; title?: string; subtitle?: string; table?: TableSpec }) {
  const [ref, w] = useWidth<HTMLDivElement>(720);
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const rowH = 17;
  const labelW = 62;
  const irrW = 64;
  const m = { t: 22, r: irrW, b: 8, l: labelW };
  const iw = Math.max(80, w - m.l - m.r);
  const h = rows.length * rowH + m.t + m.b;
  const x = scaleLog().domain([0.2, 3.2]).range([0, iw]).clamp(true);
  const ticks = iw < 340 ? [0.5, 1, 2] : [0.25, 0.5, 1, 1.5, 2, 3];
  const legend: LegendItem[] = [
    { label: "Valor justo acima do preço", color: C.s1, kind: "dot" },
    { label: "Valor justo abaixo do preço", color: C.neg, kind: "dot" },
    { label: "Preço pré-eleição (23/10)", color: "var(--ink-2)", kind: "ring" },
  ];
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "preço versus valor justo"}>
          <g transform={`translate(${m.l},${m.t})`}>
            {ticks.map((t) => (
              <g key={t}>
                <line x1={x(t)} x2={x(t)} y1={-4} y2={rows.length * rowH} stroke={t === 1 ? "var(--axis)" : "var(--grid)"} strokeWidth={t === 1 ? 1.5 : 1} />
                <text x={x(t)} y={-9} textAnchor="middle" fontSize={11} fill="var(--muted)">
                  {t === 1 ? (iw < 340 ? "hoje" : "preço hoje") : pctS(t - 1)}
                </text>
              </g>
            ))}
            <text x={iw + irrW - 4} y={-9} textAnchor="end" fontSize={11} fill="var(--muted)">
              TIR dono
            </text>
            {rows.map((r, i) => {
              const yy = i * rowH + rowH / 2;
              const rf = r.fair && r.price ? r.fair / r.price : null;
              const rp = r.pre && r.price ? r.pre / r.price : null;
              const up = rf !== null && rf >= 1;
              const col = up ? C.s1 : C.neg;
              const meets = r.irr !== null && r.irr >= ke;
              return (
                <g
                  key={r.ticker}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-labelW} y={i * rowH} width={labelW + iw + irrW} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : meets ? "var(--accent-soft)" : "transparent"} />
                  <a href={r.href}>
                    <text x={-8} y={yy} dy="0.32em" textAnchor="end" fontSize={11.5} fill="var(--ink)" fontWeight={meets ? 600 : 500}>
                      {r.ticker}
                    </text>
                  </a>
                  {rf !== null && <line x1={r2(x(1))} x2={r2(x(rf))} y1={yy} y2={yy} stroke={col} strokeWidth={2} strokeLinecap="round" opacity={0.85} />}
                  {rp !== null && <circle cx={r2(x(rp))} cy={yy} r={3.5} fill="var(--surface)" stroke="var(--ink-2)" strokeWidth={1.5} />}
                  {rf !== null && <circle cx={r2(x(rf))} cy={yy} r={4} fill={col} stroke="var(--surface)" strokeWidth={2} />}
                  <text x={iw + irrW - 4} y={yy} dy="0.32em" textAnchor="end" fontSize={11.5} fill={meets ? "var(--ink)" : "var(--ink-2)"} fontWeight={meets ? 600 : 400} className="num">
                    {r.irr === null ? "—" : `${(r.irr * 100).toLocaleString("pt-BR", { maximumFractionDigits: 1, minimumFractionDigits: 1 })}%`}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
        {hover && rows[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">
              {rows[hover.i].ticker} <span className="font-normal text-muted">{rows[hover.i].name}</span>
            </div>
            <TipRow label="Preço" value={`R$ ${rows[hover.i].price.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`} />
            <TipRow
              label="Valor justo"
              value={rows[hover.i].fair ? `R$ ${(rows[hover.i].fair as number).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} (${pctS((rows[hover.i].fair as number) / rows[hover.i].price - 1, 1)})` : "—"}
            />
            <TipRow
              label="Pré-eleição"
              value={rows[hover.i].pre ? `R$ ${(rows[hover.i].pre as number).toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` : "—"}
            />
            <TipRow label="TIR de dono" value={rows[hover.i].irr === null ? "—" : pctS(rows[hover.i].irr as number, 1).replace("+", "")} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}

export type SPoint = { id: string; x: number; y: number; label?: string; highlight?: boolean; href?: string; sub?: string };

/** Dispersão com rótulos seletivos, hover por proximidade e linhas de referência. */
export function Scatter({
  points,
  title,
  subtitle,
  xFmt: xFmtIn,
  yFmt: yFmtIn,
  xLabel,
  yLabel,
  height = 320,
  diagonal = false,
  hRef,
  vRef,
  table,
  legend,
}: {
  points: SPoint[];
  title?: string;
  subtitle?: string;
  xFmt: Fmt;
  yFmt: Fmt;
  xLabel: string;
  yLabel: string;
  height?: number;
  diagonal?: boolean;
  hRef?: { y: number; label: string };
  vRef?: { x: number; label: string };
  table?: TableSpec;
  legend?: LegendItem[];
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const xFmt = toFn(xFmtIn);
  const yFmt = toFn(yFmtIn);
  const m = { t: 12, r: 16, b: 36, l: 52 };
  const iw = Math.max(60, w - m.l - m.r);
  const ih = height - m.t - m.b;
  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const pad = (a: number, b: number) => [a - (b - a) * 0.06, b + (b - a) * 0.06] as [number, number];
  let xd = pad(Math.min(...xs, vRef?.x ?? Infinity), Math.max(...xs, vRef?.x ?? -Infinity));
  let yd = pad(Math.min(...ys, hRef?.y ?? Infinity), Math.max(...ys, hRef?.y ?? -Infinity));
  if (diagonal) {
    const lo = Math.min(xd[0], yd[0]);
    const hi = Math.max(xd[1], yd[1]);
    xd = [lo, hi];
    yd = [lo, hi];
  }
  const x = scaleLinear().domain(xd).range([0, iw]).nice();
  const y = scaleLinear().domain(yd).range([ih, 0]).nice();
  const onMove = (e: React.PointerEvent<SVGRectElement>) => {
    const b = (e.currentTarget as SVGRectElement).getBoundingClientRect();
    const px = e.clientX - b.left;
    const py = e.clientY - b.top;
    let best = -1;
    let bd = Infinity;
    points.forEach((p, i) => {
      const d = (x(p.x) - px) ** 2 + (y(p.y) - py) ** 2;
      if (d < bd) {
        bd = d;
        best = i;
      }
    });
    setHover(best >= 0 && bd < 40 * 40 ? { i: best, px: px + m.l, py: py + m.t } : null);
  };
  const ordered = [...points.map((p, i) => ({ p, i }))].sort((a, b) => Number(!!a.p.highlight) - Number(!!b.p.highlight));
  return (
    <Frame title={title} subtitle={subtitle} table={table} legend={legend}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "dispersão"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={y.ticks(5)} y={y} x0={0} x1={iw} fmt={yFmt} />
            {x.ticks(6).map((t) => (
              <g key={t}>
                <line x1={x(t)} x2={x(t)} y1={0} y2={ih} stroke="var(--grid)" />
                <text x={x(t)} y={ih + 15} textAnchor="middle" fontSize={11} fill="var(--muted)">
                  {xFmt(t)}
                </text>
              </g>
            ))}
            <text x={iw} y={ih + 31} textAnchor="end" fontSize={11} fill="var(--ink-2)">
              {xLabel}
            </text>
            <text x={4} y={10} fontSize={11} fill="var(--ink-2)">
              {yLabel}
            </text>
            {diagonal && <line x1={x(xd[0])} y1={y(xd[0])} x2={x(xd[1])} y2={y(xd[1])} stroke="var(--axis)" strokeWidth={1} />}
            {hRef && (
              <g>
                <line x1={0} x2={iw} y1={y(hRef.y)} y2={y(hRef.y)} stroke="var(--ink-2)" strokeDasharray="1 3" />
                <text x={iw - 2} y={y(hRef.y) - 4} textAnchor="end" fontSize={11} fill="var(--ink-2)">
                  {hRef.label}
                </text>
              </g>
            )}
            {vRef && (
              <g>
                <line x1={x(vRef.x)} x2={x(vRef.x)} y1={0} y2={ih} stroke="var(--ink-2)" strokeDasharray="1 3" />
                <text x={x(vRef.x) + 4} y={ih - 4} fontSize={11} fill="var(--ink-2)">
                  {vRef.label}
                </text>
              </g>
            )}
            {ordered.map(({ p, i }) => (
              <g key={p.id}>
                <circle cx={x(p.x)} cy={y(p.y)} r={p.highlight ? 4.5 : 3.5} fill={p.highlight ? C.s1 : C.deemph} stroke="var(--surface)" strokeWidth={2} opacity={hover && hover.i !== i ? 0.7 : 1} />
                {p.label && (
                  <text x={x(p.x) + 6} y={y(p.y) - 5} fontSize={11} fill="var(--ink)" fontWeight={500}>
                    {p.label}
                  </text>
                )}
              </g>
            ))}
            <rect width={iw} height={ih} fill="transparent" onPointerMove={onMove} onPointerLeave={() => setHover(null)} />
          </g>
        </svg>
        {hover && points[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">{points[hover.i].id}</div>
            {points[hover.i].sub && <div className="mb-1 text-[12px] text-muted">{points[hover.i].sub}</div>}
            <TipRow label={xLabel} value={xFmt(points[hover.i].x)} />
            <TipRow label={yLabel} value={yFmt(points[hover.i].y)} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}

/** Histograma (Monte Carlo): barras à direita do preço em azul (valor > preço), resto em cinza. */
export function Histogram({
  counts,
  edges,
  price,
  fair,
  title,
  subtitle,
  fmt: fmtIn,
  height = 220,
  table,
  prob,
  legendItems,
  priceLabel,
  aboveColor,
}: {
  counts: number[];
  edges: number[];
  price: number | null;
  fair: number | null;
  title?: string;
  subtitle?: string;
  fmt: Fmt;
  height?: number;
  table?: TableSpec;
  prob?: number | null;
  legendItems?: LegendItem[] | null;
  priceLabel?: string;
  aboveColor?: string;
}) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const m = { t: 24, r: 24, b: 24, l: 40 };
  const iw = Math.max(60, w - m.l - m.r);
  const ih = height - m.t - m.b;
  const lo = Math.min(edges[0], price ?? Infinity);
  const hi = Math.max(edges[edges.length - 1], price ?? -Infinity);
  const x = scaleLinear().domain([lo, hi]).range([0, iw]).nice();
  const total = counts.reduce((a, b) => a + b, 0) || 1;
  const y = scaleLinear().domain([0, Math.max(...counts) / total]).range([ih, 0]).nice();
  const legend: LegendItem[] =
    legendItems === undefined
      ? [
          { label: "Cenários com valor acima do preço", color: C.s1, kind: "rect" },
          { label: "Abaixo do preço", color: C.deemph, kind: "rect" },
        ]
      : legendItems || [];
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "distribuição"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={y.ticks(3)} y={y} x0={0} x1={iw} fmt={(v) => `${Math.round(v * 100)}%`} />
            {counts.map((c, i) => {
              const x0 = x(edges[i]);
              const x1 = x(edges[i + 1]);
              const mid = (edges[i] + edges[i + 1]) / 2;
              const above = price !== null && mid > price;
              const bw = Math.max(1, x1 - x0 - 2);
              const top = y(c / total);
              return (
                <rect
                  key={i}
                  x={x0 + 1}
                  y={top}
                  width={bw}
                  height={Math.max(0, ih - top)}
                  rx={Math.min(2, bw / 2)}
                  fill={above ? (aboveColor ?? C.s1) : C.deemph}
                  opacity={hover && hover.i !== i ? 0.75 : 1}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                />
              );
            })}
            <line x1={0} x2={iw} y1={ih} y2={ih} stroke="var(--axis)" />
            {x.ticks(6).map((t) => (
              <text key={t} x={x(t)} y={ih + 15} textAnchor="middle" fontSize={11} fill="var(--muted)">
                {fmt(t)}
              </text>
            ))}
            {price !== null && (
              <g>
                <line x1={x(price)} x2={x(price)} y1={-14} y2={ih} stroke="var(--ink)" strokeWidth={1.5} />
                <text x={x(price) + 4} y={-6} fontSize={11} fill="var(--ink)" fontWeight={600}>
                  {priceLabel ?? `preço ${fmt(price)}`}
                  {prob !== null && prob !== undefined ? `, P(valor > preço) ${Math.round(prob * 100)}%` : ""}
                </text>
              </g>
            )}
            {fair !== null && (
              <g>
                <line x1={x(fair)} x2={x(fair)} y1={0} y2={ih} stroke={C.s1} strokeWidth={1.5} strokeDasharray="2 3" />
              </g>
            )}
          </g>
        </svg>
        {hover && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <TipRow label={`${fmt(edges[hover.i])} a ${fmt(edges[hover.i + 1])}`} value={`${((counts[hover.i] / total) * 100).toFixed(1)}%`} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}

/** Mapa de calor divergente em torno do preço: azul = valor acima do preço, vermelho = abaixo. */
export function Heatmap({
  rows,
  cols,
  values,
  price,
  title,
  subtitle,
  fmt: fmtIn,
  rowLabel,
  colLabel,
  table,
  baseCell,
}: {
  rows: string[];
  cols: string[];
  values: (number | null)[][];
  price: number | null;
  title?: string;
  subtitle?: string;
  fmt: Fmt;
  rowLabel: string;
  colLabel: string;
  table?: TableSpec;
  baseCell?: [number, number];
}) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ r: number; c: number; px: number; py: number } | null>(null);
  const m = { t: 38, r: 4, b: 4, l: 64 };
  const iw = Math.max(80, w - m.l - m.r);
  const cellH = 30;
  const h = rows.length * cellH + m.t + m.b;
  const x = scaleBand<string>().domain(cols).range([0, iw]).paddingInner(0.04);
  const y = scaleBand<string>().domain(rows).range([0, rows.length * cellH]).paddingInner(0.08);
  const color = (v: number | null) => {
    if (v === null || price === null || !price) return "var(--div-mid)";
    const r = v / price - 1;
    const t = Math.max(-1, Math.min(1, r / 0.6));
    const a = Math.abs(t);
    return t >= 0 ? `color-mix(in oklab, var(--series-1) ${Math.round(18 + a * 70)}%, var(--div-mid))` : `color-mix(in oklab, var(--div-neg) ${Math.round(18 + a * 70)}%, var(--div-mid))`;
  };
  const strong = (v: number | null) => v !== null && price !== null && Math.abs(v / price - 1) > 0.42;
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "sensibilidade"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <text x={iw / 2} y={-24} textAnchor="middle" fontSize={11} fill="var(--ink-2)" fontWeight={500}>
              {colLabel}
            </text>
            {cols.map((c) => (
              <text key={c} x={(x(c) ?? 0) + x.bandwidth() / 2} y={-4} textAnchor="middle" fontSize={11} fill="var(--muted)">
                {c}
              </text>
            ))}
            <text x={-m.l + 2} y={-4} fontSize={11} fill="var(--ink-2)" fontWeight={500}>
              {rowLabel}
            </text>
            {rows.map((rl, ri) => (
              <g key={rl}>
                <text x={-8} y={(y(rl) ?? 0) + y.bandwidth() / 2} dy="0.32em" textAnchor="end" fontSize={11} fill="var(--muted)">
                  {rl}
                </text>
                {cols.map((cl, ci) => {
                  const v = values[ri]?.[ci] ?? null;
                  const isBase = baseCell && baseCell[0] === ri && baseCell[1] === ci;
                  return (
                    <g
                      key={cl}
                      onPointerMove={(e) => {
                        const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                        setHover({ r: ri, c: ci, px: e.clientX - b.left, py: e.clientY - b.top });
                      }}
                      onPointerLeave={() => setHover(null)}
                    >
                      <rect x={x(cl)} y={y(rl)} width={x.bandwidth()} height={y.bandwidth()} rx={3} fill={color(v)} stroke={isBase ? "var(--ink)" : "none"} strokeWidth={isBase ? 1.5 : 0} />
                      <text
                        x={(x(cl) ?? 0) + x.bandwidth() / 2}
                        y={(y(rl) ?? 0) + y.bandwidth() / 2}
                        dy="0.32em"
                        textAnchor="middle"
                        fontSize={11}
                        fill={strong(v) ? "#ffffff" : "var(--ink)"}
                        fontWeight={isBase ? 600 : 400}
                      >
                        {v === null ? "—" : fmt(v)}
                      </text>
                    </g>
                  );
                })}
              </g>
            ))}
          </g>
        </svg>
        {hover && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 text-[12px] text-muted">
              {rowLabel} {rows[hover.r]} · {colLabel} {cols[hover.c]}
            </div>
            <TipRow label="Valor justo" value={values[hover.r]?.[hover.c] == null ? "—" : fmt(values[hover.r][hover.c] as number)} />
            {price !== null && values[hover.r]?.[hover.c] != null && <TipRow label="vs preço" value={pctS((values[hover.r][hover.c] as number) / price - 1, 1)} />}
          </Tip>
        )}
      </div>
    </Frame>
  );
}

export type FFRow = { label: string; lo: number | null; hi: number | null; point?: number | null; ref?: boolean; note?: string };

/** Football field: faixa de valor por método + preço atual e pré-eleição.
    Em telas estreitas o nome do método sobe para cima da faixa e as linhas verticais abrem espaço para o texto. */
export function FootballField({
  rows,
  price,
  pre,
  title,
  subtitle,
  fmt: fmtIn,
  table,
}: {
  rows: FFRow[];
  price: number | null;
  pre?: number | null;
  title?: string;
  subtitle?: string;
  fmt: Fmt;
  table?: TableSpec;
}) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const need = Math.ceil(Math.max(0, ...rows.map((r) => textW(r.label, 12)))) + 14;
  const stacked = w < 520 && need > w * 0.34;
  const labelW = stacked ? 0 : Math.round(Math.min(Math.max(need, 96), w * 0.4));
  const labels = rows.map((r) => ellipsize(r.label, stacked ? w - 2 : labelW - 12, 12));
  const rowH = stacked ? 40 : 30;
  const yC = (i: number) => (stacked ? i * rowH + 27 : i * rowH + rowH / 2);
  const H = rows.length * rowH;
  const r0 = { r: 18, l: labelW };
  const iw = Math.max(80, w - r0.l - r0.r);
  const vals = rows.flatMap((r) => [r.lo, r.hi, r.point]).filter((v): v is number => typeof v === "number" && Number.isFinite(v));
  const lo = Math.min(...vals, price ?? Infinity, pre ?? Infinity);
  const hi = Math.max(...vals, price ?? -Infinity, pre ?? -Infinity);
  const x = scaleLinear().domain([Math.max(0, lo * 0.9), hi * 1.06]).range([0, iw]).nice();
  const ticks = fitTicks(x, fmt, 5);

  // rótulos de "hoje" e "pré-eleição" no topo: um de cada lado das linhas; se ainda colidirem, em duas alturas
  type Ann = { key: string; v: number; text: string; fill: string; weight: number; x0: number; tw: number; row: number };
  const anns: Ann[] = [];
  if (pre) anns.push({ key: "pre", v: pre, text: `pré-eleição ${fmt(pre)}`, fill: "var(--ink-2)", weight: 400, x0: 0, tw: 0, row: 0 });
  if (price !== null) anns.push({ key: "now", v: price, text: `hoje ${fmt(price)}`, fill: "var(--ink)", weight: 600, x0: 0, tw: 0, row: 0 });
  anns.sort((a, b) => a.v - b.v);
  const clampX = (x0: number, tw: number) => Math.min(iw + r0.r - tw, Math.max(-r0.l, x0));
  for (const a of anns) {
    a.tw = textW(a.text, 11, a.weight);
    a.x0 = clampX(x(a.v) - a.tw / 2, a.tw);
  }
  if (anns.length === 2) {
    const [a, b] = anns;
    if (a.x0 + a.tw + 8 > b.x0) {
      a.x0 = clampX(x(a.v) + 3 - a.tw, a.tw);
      b.x0 = clampX(x(b.v) - 3, b.tw);
      if (a.x0 + a.tw + 8 > b.x0) (a.key === "pre" ? a : b).row = 1;
    }
  }
  const rowsUp = anns.some((a) => a.row === 1) ? 2 : 1;
  const m = { t: 14 + rowsUp * 13, r: r0.r, b: 22, l: r0.l };
  const h = H + m.t + m.b;
  const annY = (a: Ann) => -12 - a.row * 13;

  // no modo empilhado, linhas verticais se interrompem onde cruzariam o nome do método
  const gaps = stacked ? labels.map((l, i) => ({ x1: textW(l, 12) + 4, y0: i * rowH, y1: i * rowH + 17 })) : [];
  const segs = (xp: number, y0: number, y1: number) => lineSegs(xp, y0, y1, gaps);

  const legend: LegendItem[] = [
    { label: "Faixa (sensibilidade)", color: C.proj, kind: "rect" },
    { label: "Valor central", color: C.s1, kind: "dot" },
    { label: "Preço atual", color: "var(--ink)", kind: "line" },
    ...(pre ? [{ label: "Pré-eleição", color: "var(--ink-2)", kind: "line" as const, dashed: true }] : []),
  ];
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "faixas de valor"}>
          <g transform={`translate(${m.l},${m.t})`}>
            {ticks.map((t) => (
              <g key={t}>
                {segs(x(t), 0, H).map(([a, b]) => (
                  <line key={a} x1={x(t)} x2={x(t)} y1={a} y2={b} stroke="var(--grid)" />
                ))}
                <text x={Math.min(iw + m.r - textW(fmt(t), 11) / 2, x(t))} y={H + 15} textAnchor="middle" fontSize={11} fill="var(--muted)" className="num">
                  {fmt(t)}
                </text>
              </g>
            ))}
            {rows.map((r, i) => {
              const yy = yC(i);
              const a = r.lo ?? r.point ?? null;
              const b = r.hi ?? r.point ?? null;
              return (
                <g
                  key={r.label}
                  onPointerMove={(e) => {
                    const bb = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - bb.left, py: e.clientY - bb.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-m.l} y={i * rowH} width={w} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
                  {stacked ? (
                    <text x={0} y={i * rowH + 13} fontSize={12} fill={r.ref ? "var(--ink-2)" : "var(--ink)"}>
                      {labels[i] !== r.label && <title>{r.label}</title>}
                      {labels[i]}
                    </text>
                  ) : (
                    <text x={-10} y={yy} dy="0.32em" textAnchor="end" fontSize={12} fill={r.ref ? "var(--ink-2)" : "var(--ink)"}>
                      {labels[i] !== r.label && <title>{r.label}</title>}
                      {labels[i]}
                    </text>
                  )}
                  {a !== null && b !== null && Number.isFinite(a) && Number.isFinite(b) && (r.lo != null || r.hi != null || r.point == null) && (
                    <rect x={x(Math.min(a, b))} y={yy - 6} width={Math.max(3, Math.abs(x(b) - x(a)))} height={12} rx={4} fill={r.ref ? C.deemph : C.proj} />
                  )}
                  {r.point !== null && r.point !== undefined && Number.isFinite(r.point) && (
                    <circle cx={x(r.point)} cy={yy} r={4.5} fill={r.ref ? "var(--ink-2)" : C.s1} stroke="var(--surface)" strokeWidth={2} />
                  )}
                </g>
              );
            })}
            {anns.map((a) => {
              const ax = x(a.v);
              const top = annY(a) + 4;
              const now = a.key === "now";
              return (
                <g key={a.key} pointerEvents="none">
                  {segs(ax, top, H).map(([s0, s1]) => (
                    <line key={s0} x1={ax} x2={ax} y1={s0} y2={s1} stroke={now ? "var(--ink)" : "var(--ink-2)"} strokeWidth={now ? 1.5 : 1.25} strokeDasharray={now ? undefined : "2 3"} />
                  ))}
                  <text x={a.x0} y={annY(a)} fontSize={11} fill={a.fill} fontWeight={a.weight} className="num">
                    {a.text}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
        {hover && rows[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">{rows[hover.i].label}</div>
            {rows[hover.i].point != null && <TipRow label="Central" value={fmt(rows[hover.i].point as number)} />}
            {rows[hover.i].lo != null && <TipRow label="Mínimo" value={fmt(rows[hover.i].lo as number)} />}
            {rows[hover.i].hi != null && <TipRow label="Máximo" value={fmt(rows[hover.i].hi as number)} />}
            {rows[hover.i].note && <div className="mt-1 max-w-[260px] whitespace-normal text-[12px] text-muted">{rows[hover.i].note}</div>}
          </Tip>
        )}
      </div>
    </Frame>
  );
}

/** Sparkline de 52 semanas: linha discreta + último ponto destacado. */
export function Sparkline({ data, w = 96, h = 26, down }: { data: number[]; w?: number; h?: number; down?: boolean }) {
  const d = data.filter((v) => Number.isFinite(v));
  if (d.length < 2) return <span className="text-muted">—</span>;
  const lo = Math.min(...d);
  const hi = Math.max(...d);
  const x = (i: number) => (i / (d.length - 1)) * (w - 6) + 1;
  const y = (v: number) => h - 3 - ((v - lo) / (hi - lo || 1)) * (h - 6);
  const p = d.map((v, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join("");
  return (
    <svg width={w} height={h} aria-hidden className="block">
      <path d={p} fill="none" stroke="var(--ink-2)" strokeWidth={1.25} opacity={0.55} strokeLinejoin="round" />
      <circle cx={x(d.length - 1)} cy={y(d[d.length - 1])} r={2.75} fill={down ? "var(--div-neg)" : "var(--series-1)"} />
    </svg>
  );
}

/** Medidor TIR vs Ke (trilho do mesmo matiz, marca da meta). */
export function IrrMeter({ irr, ke, max = 0.5, w = 120 }: { irr: number | null; ke: number; max?: number; w?: number }) {
  const h = 8;
  const fx = (v: number) => r2(Math.max(0, Math.min(1, v / max)) * w);
  const meets = irr !== null && irr >= ke;
  return (
    <svg width={w} height={h + 6} aria-label={irr === null ? "sem TIR" : `TIR ${(irr * 100).toFixed(1)}% vs Ke ${(ke * 100).toFixed(0)}%`} className="block">
      <rect x={0} y={3} width={w} height={h} rx={4} fill="var(--accent-soft)" />
      {irr !== null && <rect x={0} y={3} width={Math.max(4, fx(irr))} height={h} rx={4} fill={meets ? "var(--series-1)" : "var(--proj)"} />}
      <line x1={fx(ke)} x2={fx(ke)} y1={0} y2={h + 6} stroke="var(--ink)" strokeWidth={1.5} />
    </svg>
  );
}

export { scaleBand };
