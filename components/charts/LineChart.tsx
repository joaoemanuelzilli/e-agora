"use client";
import { bisector, extent } from "d3-array";
import { scaleLinear, scaleTime } from "d3-scale";
import { area as d3area, curveMonotoneX, line as d3line } from "d3-shape";
import { useMemo, useState } from "react";
import { C, Frame, Tip, TipRow, YGrid, toFn, useWidth, type Fmt, type LegendItem, type TableSpec } from "./core";
import { textW } from "./measure";

export type LSeries = {
  key: string;
  label: string;
  color: string;
  data: [number, number][]; // [x (ms ou número), y]
  width?: number;
  muted?: boolean; // contexto (sem tooltip, cinza)
  area?: boolean;
  dashed?: boolean;
  endLabel?: boolean;
};

export type Band = { lo: number; hi: number; label?: string };
export type HLine = { y: number; label: string; color?: string };
export type VMark = { x: number; label: string };

export function LineChart({
  series,
  height = 260,
  xType = "time",
  yFmt: yFmtIn,
  xFmt: xFmtIn,
  title,
  subtitle,
  bands = [],
  hlines = [],
  vmarks = [],
  yDomain,
  legend,
  table,
  logY = false,
  right,
}: {
  series: LSeries[];
  height?: number;
  xType?: "time" | "linear";
  yFmt?: Fmt;
  xFmt?: Fmt;
  title?: string;
  subtitle?: string;
  bands?: Band[];
  hlines?: HLine[];
  vmarks?: VMark[];
  yDomain?: [number, number];
  legend?: LegendItem[];
  table?: TableSpec;
  logY?: boolean;
  right?: React.ReactNode;
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ x: number; px: number; py: number } | null>(null);
  const yFmt = toFn(yFmtIn);
  const xFmt = xFmtIn ? toFn(xFmtIn) : undefined;
  const ih = height - 10 - 24;

  const all = series.flatMap((s) => s.data);
  const xs = extent(all, (d) => d[0]) as [number, number];
  let ys = (yDomain ?? (extent([...all.map((d) => d[1]), ...bands.flatMap((b) => [b.lo, b.hi]), ...hlines.map((h) => h.y)]) as [number, number])) as [
    number,
    number,
  ];
  if (!yDomain) {
    const pad = (ys[1] - ys[0]) * 0.06 || 1;
    ys = [ys[0] - pad, ys[1] + pad];
  }
  const y = scaleLinear().domain(ys).range([ih, 0]).nice();
  const yt = y.ticks(5);
  // margem esquerda cresce com o maior rótulo do eixo Y (ex.: "200.000") para não cortar
  const m = { t: 10, r: 56, b: 24, l: Math.max(48, Math.ceil(Math.max(0, ...yt.map((t) => textW(yFmt(t), 11)))) + 10) };
  const iw = Math.max(50, w - m.l - m.r);
  const x = useMemo(
    () => (xType === "time" ? scaleTime().domain([new Date(xs[0]), new Date(xs[1])]).range([0, iw]) : scaleLinear().domain(xs).range([0, iw])),
    [xs[0], xs[1], iw, xType],
  ) as unknown as ((v: number | Date) => number) & { ticks: (n: number) => (number | Date)[]; invert: (p: number) => number | Date };
  const xfmt =
    xFmt ??
    ((v: number) =>
      xType === "time"
        ? new Date(v).toLocaleDateString("pt-BR", { month: "short", year: "2-digit", timeZone: "UTC" }).replace(".", "")
        : String(v));
  const xt = (x.ticks(Math.max(2, Math.floor(iw / 90))) as (number | Date)[]).map((t) => +t);

  const lineGen = d3line<[number, number]>()
    .x((d) => x(xType === "time" ? new Date(d[0]) : d[0]))
    .y((d) => y(d[1]))
    .curve(curveMonotoneX);
  const areaGen = d3area<[number, number]>()
    .x((d) => x(xType === "time" ? new Date(d[0]) : d[0]))
    .y0(ih)
    .y1((d) => y(d[1]))
    .curve(curveMonotoneX);

  const main = series.filter((s) => !s.muted);
  const bis = bisector<[number, number], number>((d) => d[0]).center;
  const onMove = (e: React.PointerEvent<SVGRectElement>) => {
    const rect = (e.currentTarget as SVGRectElement).getBoundingClientRect();
    const px = e.clientX - rect.left;
    const xv = +x.invert(px);
    setHover({ x: xv, px: px + m.l, py: e.clientY - rect.top + m.t });
  };
  const hv = hover
    ? main
        .map((s) => {
          if (!s.data.length) return null;
          const i = bis(s.data, hover.x);
          const d = s.data[Math.max(0, Math.min(s.data.length - 1, i))];
          return { s, d };
        })
        .filter(Boolean)
    : [];
  const snapX = hv[0] ? x(xType === "time" ? new Date(hv[0]!.d[0]) : hv[0]!.d[0]) : null;

  const leg: LegendItem[] = legend ?? main.map((s) => ({ label: s.label, color: s.color, kind: "line", dashed: s.dashed }));

  return (
    <Frame title={title} subtitle={subtitle} legend={leg} table={table} right={right}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "gráfico de linhas"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={yt} y={y} x0={0} x1={iw} fmt={yFmt} />
            {bands.map((b, i) => (
              <rect key={i} x={0} width={iw} y={y(b.hi)} height={Math.max(0, y(b.lo) - y(b.hi))} fill="var(--accent-soft)" />
            ))}
            {xt.map((t) => (
              <text key={t} x={x(xType === "time" ? new Date(t) : t)} y={ih + 16} textAnchor="middle" fontSize={11} fill="var(--muted)">
                {xfmt(t)}
              </text>
            ))}
            <line x1={0} x2={iw} y1={ih} y2={ih} stroke="var(--axis)" shapeRendering="crispEdges" />
            {vmarks.map((v, vi) => {
              const vx = x(xType === "time" ? new Date(v.x) : v.x);
              const flip = vx > iw - 70;
              return (
                <g key={v.label}>
                  <line x1={vx} x2={vx} y1={0} y2={ih} stroke="var(--axis)" shapeRendering="crispEdges" />
                  <text x={flip ? vx - 4 : vx + 4} y={10 + (vi % 2) * 13} textAnchor={flip ? "end" : "start"} fontSize={11} fill="var(--ink-2)">
                    {v.label}
                  </text>
                </g>
              );
            })}
            {hlines.map((h) => (
              <g key={h.label}>
                <line x1={0} x2={iw} y1={y(h.y)} y2={y(h.y)} stroke={h.color || "var(--ink-2)"} strokeWidth={1} strokeDasharray="1 3" />
                <text x={iw + 4} y={y(h.y)} dy="0.32em" fontSize={11} fill="var(--ink-2)">
                  {h.label}
                </text>
              </g>
            ))}
            {series.map((s) => (
              <g key={s.key}>
                {s.area && <path d={areaGen(s.data) || ""} fill={s.color} opacity={0.1} />}
                <path
                  d={lineGen(s.data) || ""}
                  fill="none"
                  stroke={s.muted ? C.deemph : s.color}
                  strokeWidth={s.width ?? (s.muted ? 1.25 : 2)}
                  strokeLinejoin="round"
                  strokeLinecap="round"
                  strokeDasharray={s.dashed ? "2 3" : undefined}
                  opacity={s.muted ? 0.9 : 1}
                />
                {s.endLabel && s.data.length > 0 && (
                  <g>
                    <circle
                      cx={x(xType === "time" ? new Date(s.data[s.data.length - 1][0]) : s.data[s.data.length - 1][0])}
                      cy={y(s.data[s.data.length - 1][1])}
                      r={4}
                      fill={s.color}
                      stroke="var(--surface)"
                      strokeWidth={2}
                    />
                    <text
                      x={x(xType === "time" ? new Date(s.data[s.data.length - 1][0]) : s.data[s.data.length - 1][0]) + 8}
                      y={y(s.data[s.data.length - 1][1])}
                      dy="0.32em"
                      fontSize={11}
                      fill="var(--ink)"
                      fontWeight={600}
                    >
                      {yFmt(s.data[s.data.length - 1][1])}
                    </text>
                  </g>
                )}
              </g>
            ))}
            {snapX !== null && (
              <g>
                <line x1={snapX} x2={snapX} y1={0} y2={ih} stroke="var(--ink-2)" strokeWidth={1} opacity={0.5} />
                {hv.map((h) => (
                  <circle key={h!.s.key} cx={snapX} cy={y(h!.d[1])} r={4} fill={h!.s.color} stroke="var(--surface)" strokeWidth={2} />
                ))}
              </g>
            )}
            <rect
              width={iw}
              height={ih}
              fill="transparent"
              onPointerMove={onMove}
              onPointerLeave={() => setHover(null)}
              style={{ cursor: "crosshair" }}
            />
          </g>
        </svg>
        {hover && hv.length > 0 && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 text-[12px] text-muted">{xfmt(hv[0]!.d[0]).length > 8 ? xfmt(hv[0]!.d[0]) : xType === "time" ? new Date(hv[0]!.d[0]).toLocaleDateString("pt-BR", { timeZone: "UTC" }) : xfmt(hv[0]!.d[0])}</div>
            {hv.map((h) => (
              <TipRow key={h!.s.key} color={h!.s.color} label={h!.s.label} value={yFmt(h!.d[1])} />
            ))}
          </Tip>
        )}
      </div>
    </Frame>
  );
}
