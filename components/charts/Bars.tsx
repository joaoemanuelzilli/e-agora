"use client";
import { scaleBand, scaleLinear } from "d3-scale";
import { useState } from "react";
import { C, Frame, Tip, TipRow, YGrid, toFn, useWidth, type Fmt, type LegendItem, type TableSpec } from "./core";

/** Caminho de barra com ponta arredondada (4px) e base reta. */
function barPath(x: number, y0: number, y1: number, w: number, r = 4) {
  const up = y1 < y0;
  const h = Math.abs(y1 - y0);
  const rr = Math.min(r, h, w / 2);
  if (h < 0.5) return "";
  if (up) {
    return `M${x},${y0} V${y1 + rr} Q${x},${y1} ${x + rr},${y1} H${x + w - rr} Q${x + w},${y1} ${x + w},${y1 + rr} V${y0} Z`;
  }
  return `M${x},${y0} V${y1 - rr} Q${x},${y1} ${x + rr},${y1} H${x + w - rr} Q${x + w},${y1} ${x + w},${y1 - rr} V${y0} Z`;
}

export type Col = { label: string; value: number | null; projected?: boolean; note?: string };

/** Colunas: histórico (cor cheia) + projeção (mesma rampa, passo mais claro). */
export function ColumnChart({
  data,
  title,
  subtitle,
  height = 220,
  fmt: fmtIn,
  color = C.s1,
  table,
  labelLast = true,
  refLine,
}: {
  data: Col[];
  title?: string;
  subtitle?: string;
  height?: number;
  fmt?: Fmt;
  color?: string;
  table?: TableSpec;
  labelLast?: boolean;
  refLine?: { y: number; label: string };
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const fmt = toFn(fmtIn);
  const m = { t: 18, r: 12, b: 24, l: 48 };
  const iw = Math.max(40, w - m.l - m.r);
  const ih = height - m.t - m.b;
  const vals = data.map((d) => d.value ?? 0);
  const lo = Math.min(0, ...vals, refLine?.y ?? 0);
  const hi = Math.max(0, ...vals, refLine?.y ?? 0);
  const y = scaleLinear().domain([lo, hi === lo ? lo + 1 : hi]).range([ih, 0]).nice();
  const x = scaleBand<string>().domain(data.map((d) => d.label)).range([0, iw]).paddingInner(0.28).paddingOuter(0.1);
  const bw = Math.min(24, x.bandwidth());
  const off = (x.bandwidth() - bw) / 2;
  const firstProj = data.findIndex((d) => d.projected);
  const lastHist = firstProj === -1 ? data.length - 1 : firstProj - 1;
  const legend: LegendItem[] | undefined =
    firstProj > 0
      ? [
          { label: "Realizado", color, kind: "rect" },
          { label: "Projeção", color: C.proj, kind: "rect" },
        ]
      : undefined;
  const showLabel = (i: number) => labelLast && (i === lastHist || i === data.length - 1);
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "gráfico de colunas"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={y.ticks(4)} y={y} x0={0} x1={iw} fmt={fmt} />
            {firstProj > 0 && (
              <g>
                <line
                  x1={(x(data[firstProj].label) ?? 0) - (x.step() * x.paddingInner()) / 2}
                  x2={(x(data[firstProj].label) ?? 0) - (x.step() * x.paddingInner()) / 2}
                  y1={-12}
                  y2={ih}
                  stroke="var(--axis)"
                />
                <text x={(x(data[firstProj].label) ?? 0) + 2} y={-4} fontSize={11} fill="var(--muted)">
                  Projeção
                </text>
              </g>
            )}
            {data.map((d, i) => {
              if (d.value === null || d.value === undefined) return null;
              const bx = (x(d.label) ?? 0) + off;
              const p = barPath(bx, y(0), y(d.value), bw);
              return (
                <g key={d.label}>
                  <path d={p} fill={d.projected ? C.proj : color} opacity={hover && hover.i !== i ? 0.75 : 1} />
                  {showLabel(i) && (
                    <text x={bx + bw / 2} y={d.value >= 0 ? y(d.value) - 5 : y(d.value) + 12} textAnchor="middle" fontSize={11} fill="var(--ink)" fontWeight={600}>
                      {fmt(d.value)}
                    </text>
                  )}
                </g>
              );
            })}
            {refLine && (
              <g>
                <line x1={0} x2={iw} y1={y(refLine.y)} y2={y(refLine.y)} stroke="var(--ink-2)" strokeDasharray="1 3" />
                <text x={iw} y={y(refLine.y) - 4} textAnchor="end" fontSize={11} fill="var(--ink-2)">
                  {refLine.label}
                </text>
              </g>
            )}
            <line x1={0} x2={iw} y1={y(0)} y2={y(0)} stroke="var(--axis)" shapeRendering="crispEdges" />
            {data.map((d, i) => (
              <text
                key={d.label}
                x={(x(d.label) ?? 0) + x.bandwidth() / 2}
                y={ih + 16}
                textAnchor="middle"
                fontSize={11}
                fill={d.projected ? "var(--ink-2)" : "var(--muted)"}
              >
                {data.length > 14 && i % 2 === 1 ? "" : d.label}
              </text>
            ))}
            {data.map((d, i) => (
              <rect
                key={d.label}
                x={x(d.label) ?? 0}
                width={x.bandwidth()}
                y={0}
                height={ih}
                fill="transparent"
                onPointerMove={(e) => {
                  const r = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                  setHover({ i, px: e.clientX - r.left, py: e.clientY - r.top });
                }}
                onPointerLeave={() => setHover(null)}
              />
            ))}
          </g>
        </svg>
        {hover && data[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 text-[11px] text-muted">
              {data[hover.i].label}
              {data[hover.i].projected ? " · projeção" : ""}
            </div>
            <TipRow label={data[hover.i].note || "Valor"} value={data[hover.i].value === null ? "—" : fmt(data[hover.i].value as number)} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}

export type HBarItem = { label: string; value: number; sub?: string; highlight?: boolean };

/** Barras horizontais (divergentes quando há negativos): azul ≥ 0, vermelho < 0. */
export function HBarChart({
  items,
  title,
  subtitle,
  fmt: fmtIn,
  rowH = 22,
  table,
  domain,
  labelWidth,
}: {
  items: HBarItem[];
  title?: string;
  subtitle?: string;
  fmt?: Fmt;
  rowH?: number;
  table?: TableSpec;
  domain?: [number, number];
  labelWidth?: number;
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const fmt = toFn(fmtIn);
  const labelW = labelWidth ?? Math.min(200, Math.max(96, w * 0.34));
  const m = { t: 4, r: 56, b: 20, l: labelW };
  const iw = Math.max(40, w - m.l - m.r);
  const h = items.length * rowH + m.t + m.b;
  const lo = domain ? domain[0] : Math.min(0, ...items.map((d) => d.value));
  const hi = domain ? domain[1] : Math.max(0, ...items.map((d) => d.value));
  const x = scaleLinear().domain([lo, hi === lo ? lo + 1 : hi]).range([0, iw]).nice();
  const bh = Math.min(14, rowH - 8);
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "barras horizontais"}>
          <g transform={`translate(${m.l},${m.t})`}>
            {x.ticks(4).map((t) => (
              <g key={t}>
                <line x1={x(t)} x2={x(t)} y1={0} y2={items.length * rowH} stroke="var(--grid)" />
                <text x={x(t)} y={items.length * rowH + 14} textAnchor="middle" fontSize={11} fill="var(--muted)">
                  {fmt(t)}
                </text>
              </g>
            ))}
            <line x1={x(0)} x2={x(0)} y1={0} y2={items.length * rowH} stroke="var(--axis)" />
            {items.map((d, i) => {
              const yy = i * rowH + (rowH - bh) / 2;
              const x0 = x(0);
              const x1 = x(d.value);
              const neg = d.value < 0;
              const wbar = Math.abs(x1 - x0);
              const rr = Math.min(4, wbar / 2, bh / 2);
              const path = neg
                ? `M${x0},${yy} H${x1 + rr} Q${x1},${yy} ${x1},${yy + rr} V${yy + bh - rr} Q${x1},${yy + bh} ${x1 + rr},${yy + bh} H${x0} Z`
                : `M${x0},${yy} H${x1 - rr} Q${x1},${yy} ${x1},${yy + rr} V${yy + bh - rr} Q${x1},${yy + bh} ${x1 - rr},${yy + bh} H${x0} Z`;
              return (
                <g
                  key={d.label}
                  onPointerMove={(e) => {
                    const r = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - r.left, py: e.clientY - r.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-labelW} y={i * rowH} width={labelW + iw + m.r} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
                  <text x={-8} y={i * rowH + rowH / 2} dy="0.32em" textAnchor="end" fontSize={12} fill="var(--ink)" fontWeight={d.highlight ? 600 : 400}>
                    {d.label}
                  </text>
                  {wbar >= 0.5 && <path d={path} fill={neg ? C.neg : d.highlight ? C.s1 : C.s1} opacity={d.highlight === false ? 0.45 : 1} />}
                  {(() => {
                    const inside = neg && hi > 0 && Math.min(x0, x1) < 46 && wbar > 46;
                    const tx = neg ? (hi <= 0 ? x0 + 6 : inside ? x1 + 5 : Math.min(x0, x1) - 4) : Math.max(x0, x1) + 4;
                    return (
                      <text
                        x={tx}
                        y={i * rowH + rowH / 2}
                        dy="0.32em"
                        textAnchor={neg && hi > 0 && !inside ? "end" : "start"}
                        fontSize={11}
                        fill={inside ? "#ffffff" : "var(--ink-2)"}
                        fontWeight={inside ? 600 : 400}
                      >
                        {fmt(d.value)}
                      </text>
                    );
                  })()}
                </g>
              );
            })}
          </g>
        </svg>
        {hover && items[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <TipRow label={items[hover.i].label} value={fmt(items[hover.i].value)} />
            {items[hover.i].sub && <div className="mt-0.5 text-[11px] text-muted">{items[hover.i].sub}</div>}
          </Tip>
        )}
      </div>
    </Frame>
  );
}

export type WStep = { label: string; value: number; total?: boolean };

/** Ponte (waterfall): degraus somam até o total. */
export function Waterfall({ steps, title, subtitle, fmt: fmtIn, height = 240, table }: { steps: WStep[]; title?: string; subtitle?: string; fmt: Fmt; height?: number; table?: TableSpec }) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const m = { t: 16, r: 10, b: 34, l: 52 };
  const iw = Math.max(40, w - m.l - m.r);
  const ih = height - m.t - m.b;
  let run = 0;
  const bars = steps.map((s) => {
    if (s.total) {
      const b = { ...s, a: 0, b: s.value };
      run = s.value;
      return b;
    }
    const b = { ...s, a: run, b: run + s.value };
    run += s.value;
    return b;
  });
  const lo = Math.min(0, ...bars.flatMap((b) => [b.a, b.b]));
  const hi = Math.max(0, ...bars.flatMap((b) => [b.a, b.b]));
  const y = scaleLinear().domain([lo, hi]).range([ih, 0]).nice();
  const x = scaleBand<string>().domain(steps.map((s) => s.label)).range([0, iw]).paddingInner(0.3);
  const bw = Math.min(28, x.bandwidth());
  const off = (x.bandwidth() - bw) / 2;
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "ponte de valor"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={y.ticks(4)} y={y} x0={0} x1={iw} fmt={fmt} />
            {bars.map((b, i) => {
              const top = y(Math.max(b.a, b.b));
              const bot = y(Math.min(b.a, b.b));
              const fill = b.total ? C.s1 : b.value >= 0 ? C.proj : C.neg;
              const bx = (x(b.label) ?? 0) + off;
              return (
                <g
                  key={b.label}
                  onPointerMove={(e) => {
                    const r = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - r.left, py: e.clientY - r.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={bx} y={top} width={bw} height={Math.max(1, bot - top)} rx={3} fill={fill} />
                  {i < bars.length - 1 && (
                    <line x1={bx + bw} x2={bx + x.step()} y1={y(b.b)} y2={y(b.b)} stroke="var(--axis)" />
                  )}
                  <text x={bx + bw / 2} y={top - 4} textAnchor="middle" fontSize={10.5} fill="var(--ink-2)">
                    {fmt(b.value)}
                  </text>
                </g>
              );
            })}
            <line x1={0} x2={iw} y1={y(0)} y2={y(0)} stroke="var(--axis)" />
            {steps.map((s) => (
              <foreignObject key={s.label} x={x(s.label) ?? 0} y={ih + 4} width={x.bandwidth() + 8} height={30}>
                <div className="text-center text-[10.5px] leading-tight text-muted">{s.label}</div>
              </foreignObject>
            ))}
          </g>
        </svg>
        {hover && steps[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <TipRow label={steps[hover.i].label} value={fmt(steps[hover.i].value)} />
          </Tip>
        )}
      </div>
    </Frame>
  );
}
