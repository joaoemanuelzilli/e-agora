"use client";
import { scaleBand, scaleLinear } from "d3-scale";
import { useState } from "react";
import { C, Frame, Tip, TipRow, YGrid, toFn, useWidth, type Fmt, type LegendItem, type TableSpec } from "./core";
import { categoryLabels, ellipsize, fitTicks, lineSegs, textW, wrapText, type Gap } from "./measure";

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

/** Margem esquerda que cabe o maior rótulo do eixo Y (nunca menor que o padrão). */
function yAxisW(ticks: number[], fmt: (v: number) => string, min: number) {
  return Math.max(min, Math.ceil(Math.max(0, ...ticks.map((t) => textW(fmt(t), 11)))) + 10);
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
  const ih = height - 18 - 24;
  const vals = data.map((d) => d.value ?? 0);
  const lo = Math.min(0, ...vals, refLine?.y ?? 0);
  const hi = Math.max(0, ...vals, refLine?.y ?? 0);
  const y = scaleLinear().domain([lo, hi === lo ? lo + 1 : hi]).range([ih, 0]).nice();
  const m = { t: 18, r: 12, b: 24, l: yAxisW(y.ticks(4), fmt, 48) };
  const iw = Math.max(40, w - m.l - m.r);
  const x = scaleBand<string>().domain(data.map((d) => d.label)).range([0, iw]).paddingInner(0.28).paddingOuter(0.1);
  const bw = Math.min(24, x.bandwidth());
  const off = (x.bandwidth() - bw) / 2;
  // rótulos do eixo sem encostar: anos encurtados ou 1 a cada N quando as colunas ficam estreitas
  const xl = categoryLabels(data.map((d) => d.label), x.step());
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
                {xl[i]}
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
            <div className="mb-1 text-[12px] text-muted">
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

/** Formato mais curto para o eixo quando os ticks são redondos (−10% em vez de −10,0%). */
function axisFmt(fmtIn: Fmt | undefined, ticks: number[]): (v: number) => string {
  const step = ticks.length > 1 ? Math.abs(ticks[1] - ticks[0]) : 0;
  const whole = (k: number) => step > 0 && Math.abs(Math.round(step * k) - step * k) < 1e-9;
  if (fmtIn === "pct1" && whole(100)) return toFn("pct0");
  if (fmtIn === "pct1s" && whole(100)) return toFn("pct0s");
  if ((fmtIn === "num1" || fmtIn === "num2") && whole(1)) return toFn("num0");
  return toFn(fmtIn);
}

/** Barras horizontais (divergentes quando há negativos): azul ≥ 0, vermelho < 0.
    Rótulo à esquerda medido pelo maior texto; em telas estreitas o rótulo sobe para cima da barra. */
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
  const lo = domain ? domain[0] : Math.min(0, ...items.map((d) => d.value));
  const hi = domain ? domain[1] : Math.max(0, ...items.map((d) => d.value));
  const weight = (d: HBarItem) => (d.highlight ? 600 : 400);
  const need = Math.ceil(Math.max(0, ...items.map((d) => textW(d.label, 12, weight(d))))) + 12;
  const want = labelWidth ?? need;
  // telas estreitas: se a coluna de rótulos comeria mais de ~36% da largura, o rótulo vai para cima da barra
  const stacked = w < 480 && want > w * 0.36;
  const labelW = stacked ? 0 : labelWidth ?? Math.round(Math.min(Math.max(need, 64), w * 0.45));
  const valW = (d: HBarItem) => textW(fmt(d.value), 11) + 6;
  const posW = Math.max(0, ...items.filter((d) => d.value >= 0).map(valW));
  const negW = Math.max(0, ...items.filter((d) => d.value < 0).map(valW));
  const allNeg = hi <= 0;
  // tudo negativo: valores numa coluna à direita do zero; senão, à direita da ponta das positivas
  const m = { t: 4, r: Math.ceil(Math.max(12, allNeg ? negW : posW)) + 2, b: 20, l: stacked ? 0 : labelW };
  const iw = Math.max(40, w - m.l - m.r);
  // divergente: reserva espaço à esquerda para o rótulo das negativas ficar fora da barra
  const padL = lo < 0 && !allNeg ? Math.ceil(negW) : 0;
  const x = scaleLinear().domain([lo, hi === lo ? lo + 1 : hi]).range([padL, iw]).nice();
  const bh = Math.min(14, rowH - 8);
  const rH = stacked ? bh + 25 : rowH;
  const barY = (i: number) => (stacked ? i * rH + 17 : i * rH + (rH - bh) / 2);
  const h = items.length * rH + m.t + m.b;
  const raw = x.ticks(5);
  const tfmt = axisFmt(fmtIn, raw);
  const ticks = fitTicks(x, tfmt);
  const x0 = x(0);
  const labels = items.map((d) => (stacked ? ellipsize(d.label, w - 2, 12, weight(d)) : ellipsize(d.label, labelW - 10, 12, weight(d))));
  // empilhado: grade e eixo do zero se interrompem onde cruzariam o rótulo
  const gaps: Gap[] = stacked ? labels.map((l, i) => ({ x1: textW(l, 12, weight(items[i])) + 4, y0: i * rH, y1: i * rH + 16 })) : [];
  const H = items.length * rH;
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "barras horizontais"}>
          <g transform={`translate(${m.l},${m.t})`}>
            {ticks.map((t) => {
              const s = tfmt(t);
              const half = textW(s, 11) / 2;
              const tx = Math.min(iw + m.r - half, Math.max(-m.l + half, x(t)));
              return (
                <g key={t}>
                  {lineSegs(x(t), 0, H, gaps).map(([a, b]) => (
                    <line key={a} x1={x(t)} x2={x(t)} y1={a} y2={b} stroke="var(--grid)" />
                  ))}
                  <text x={tx} y={items.length * rH + 14} textAnchor="middle" fontSize={11} fill="var(--muted)" className="num">
                    {s}
                  </text>
                </g>
              );
            })}
            {lineSegs(x0, 0, H, gaps).map(([a, b]) => (
              <line key={a} x1={x0} x2={x0} y1={a} y2={b} stroke="var(--axis)" />
            ))}
            {items.map((d, i) => {
              const yy = barY(i);
              const cy = yy + bh / 2;
              const x1 = x(d.value);
              const neg = d.value < 0;
              const wbar = Math.abs(x1 - x0);
              const rr = Math.min(4, wbar / 2, bh / 2);
              const path = neg
                ? `M${x0},${yy} H${x1 + rr} Q${x1},${yy} ${x1},${yy + rr} V${yy + bh - rr} Q${x1},${yy + bh} ${x1 + rr},${yy + bh} H${x0} Z`
                : `M${x0},${yy} H${x1 - rr} Q${x1},${yy} ${x1},${yy + rr} V${yy + bh - rr} Q${x1},${yy + bh} ${x1 - rr},${yy + bh} H${x0} Z`;
              const label = labels[i];
              // valor: fora da ponta da barra quando há espaço, senão dentro (branco), senão do outro lado do zero
              const s = fmt(d.value);
              const tw = textW(s, 11);
              let tx: number;
              let anchor: "start" | "end";
              let inside = false;
              if (!neg) {
                if (x1 + 4 + tw <= iw + m.r) [tx, anchor] = [x1 + 4, "start"];
                else if (wbar >= tw + 10) [tx, anchor, inside] = [x1 - 5, "end", true];
                else [tx, anchor] = [x0 - 4, "end"];
              } else if (allNeg) [tx, anchor] = [x0 + 6, "start"];
              else if (x1 - 4 - tw >= -2) [tx, anchor] = [x1 - 4, "end"];
              else if (wbar >= tw + 10) [tx, anchor, inside] = [x1 + 5, "start", true];
              else [tx, anchor] = [x0 + 4, "start"];
              return (
                <g
                  key={d.label}
                  onPointerMove={(e) => {
                    const r = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - r.left, py: e.clientY - r.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-m.l} y={i * rH} width={w} height={rH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
                  {stacked ? (
                    <text x={0} y={i * rH + 12} fontSize={12} fill="var(--ink)" fontWeight={weight(d)}>
                      {label !== d.label && <title>{d.label}</title>}
                      {label}
                    </text>
                  ) : (
                    <text x={-8} y={cy} dy="0.32em" textAnchor="end" fontSize={12} fill="var(--ink)" fontWeight={weight(d)}>
                      {label !== d.label && <title>{d.label}</title>}
                      {label}
                    </text>
                  )}
                  {wbar >= 0.5 && <path d={path} fill={neg ? C.neg : C.s1} opacity={d.highlight === false ? 0.45 : 1} />}
                  <text
                    x={tx}
                    y={cy}
                    dy="0.32em"
                    textAnchor={anchor}
                    fontSize={11}
                    fill={inside ? "#ffffff" : "var(--ink-2)"}
                    fontWeight={inside ? 600 : 400}
                    className="num"
                  >
                    {s}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
        {hover && items[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <TipRow label={items[hover.i].label} value={fmt(items[hover.i].value)} />
            {items[hover.i].sub && <div className="mt-0.5 text-[12px] text-muted">{items[hover.i].sub}</div>}
          </Tip>
        )}
      </div>
    </Frame>
  );
}

export type WStep = { label: string; value: number; total?: boolean };

/** Ponte (waterfall): degraus somam até o total. Colunas quando os rótulos cabem em 2 linhas; senão, linhas horizontais. */
export function Waterfall({ steps, title, subtitle, fmt: fmtIn, height = 240, table }: { steps: WStep[]; title?: string; subtitle?: string; fmt: Fmt; height?: number; table?: TableSpec }) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const bars: (WStep & { a: number; b: number })[] = [];
  let run = 0;
  for (const s of steps) {
    bars.push(s.total ? { ...s, a: 0, b: s.value } : { ...s, a: run, b: run + s.value });
    run = s.total ? s.value : run + s.value;
  }
  const lo = Math.min(0, ...bars.flatMap((b) => [b.a, b.b]));
  const hi = Math.max(0, ...bars.flatMap((b) => [b.a, b.b]));
  const fill = (b: (typeof bars)[number]) => (b.total ? C.s1 : b.value >= 0 ? C.proj : C.neg);
  const onMove = (i: number) => (e: React.PointerEvent<SVGGElement>) => {
    const r = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
    setHover({ i, px: e.clientX - r.left, py: e.clientY - r.top });
  };

  // colunas: cada rótulo precisa caber em até 2 linhas na largura da coluna
  const ihV = height - 16 - 36;
  const yV = scaleLinear().domain([lo, hi]).range([ihV, 0]).nice();
  const mV = { t: 16, r: 10, b: 36, l: yAxisW(yV.ticks(4), fmt, 52) };
  const iwV = Math.max(40, w - mV.l - mV.r);
  const xb = scaleBand<string>().domain(steps.map((s) => s.label)).range([0, iwV]).paddingInner(0.3);
  const wraps = steps.map((s) => wrapText(s.label, xb.step() - 4, 12, 2));
  const vertical = wraps.every((r) => r.fits);

  let body: React.ReactNode;
  let svgH = height;
  if (vertical) {
    const m = mV;
    const ih = ihV;
    const y = yV;
    const bw = Math.min(28, xb.bandwidth());
    const off = (xb.bandwidth() - bw) / 2;
    body = (
      <g transform={`translate(${m.l},${m.t})`}>
        <YGrid ticks={y.ticks(4)} y={y} x0={0} x1={iwV} fmt={fmt} />
        {bars.map((b, i) => {
          const top = y(Math.max(b.a, b.b));
          const bot = y(Math.min(b.a, b.b));
          const bx = (xb(b.label) ?? 0) + off;
          return (
            <g key={b.label} onPointerMove={onMove(i)} onPointerLeave={() => setHover(null)}>
              <rect x={xb(b.label) ?? 0} y={0} width={xb.bandwidth()} height={ih + m.b} fill="transparent" />
              <rect x={bx} y={top} width={bw} height={Math.max(1, bot - top)} rx={3} fill={fill(b)} />
              {i < bars.length - 1 && <line x1={bx + bw} x2={bx + xb.step()} y1={y(b.b)} y2={y(b.b)} stroke="var(--axis)" />}
              <text x={bx + bw / 2} y={top - 4} textAnchor="middle" fontSize={11} fill="var(--ink-2)" className="num">
                {fmt(b.value)}
              </text>
              <text x={(xb(b.label) ?? 0) + xb.bandwidth() / 2} y={ih + 16} textAnchor="middle" fontSize={12} fill="var(--muted)">
                <title>{b.label}</title>
                {wraps[i].lines.map((l, k) => (
                  <tspan key={k} x={(xb(b.label) ?? 0) + xb.bandwidth() / 2} dy={k ? 14 : 0}>
                    {l}
                  </tspan>
                ))}
              </text>
            </g>
          );
        })}
        <line x1={0} x2={iwV} y1={y(0)} y2={y(0)} stroke="var(--axis)" />
      </g>
    );
  } else {
    // linhas: rótulo à esquerda (até 2 linhas), barra flutuante e valor na ponta
    const need = Math.ceil(Math.max(0, ...steps.map((s) => textW(s.label, 12)))) + 12;
    const labelW = Math.round(Math.min(need, Math.max(84, w * 0.36)));
    const lines = steps.map((s) => wrapText(s.label, labelW - 10, 12, 2).lines);
    const valW = Math.ceil(Math.max(...bars.map((b) => textW(fmt(b.value), 11)))) + 8;
    const m = { t: 4, r: valW, b: 22, l: labelW };
    const iw = Math.max(40, w - m.l - m.r);
    const rowH = lines.some((l) => l.length > 1) ? 34 : 28;
    const bh = 14;
    svgH = steps.length * rowH + m.t + m.b;
    const x = scaleLinear().domain([lo, hi]).range([0, iw]).nice();
    const tfmt = fmt;
    const ticks = fitTicks(x, tfmt, 4);
    body = (
      <g transform={`translate(${m.l},${m.t})`}>
        {ticks.map((t) => (
          <g key={t}>
            <line x1={x(t)} x2={x(t)} y1={0} y2={steps.length * rowH} stroke="var(--grid)" />
            <text x={Math.min(iw + m.r - textW(tfmt(t), 11) / 2, x(t))} y={steps.length * rowH + 15} textAnchor="middle" fontSize={11} fill="var(--muted)" className="num">
              {tfmt(t)}
            </text>
          </g>
        ))}
        <line x1={x(0)} x2={x(0)} y1={0} y2={steps.length * rowH} stroke="var(--axis)" />
        {bars.map((b, i) => {
          const yy = i * rowH + (rowH - bh) / 2;
          const xa = x(Math.min(b.a, b.b));
          const xz = x(Math.max(b.a, b.b));
          const s = fmt(b.value);
          const tw = textW(s, 11);
          const right = xz + 4 + tw <= iw + m.r;
          const left = xa - 4 - tw >= 0;
          const [tx, anchor, inside] = right ? [xz + 4, "start", false] : left ? [xa - 4, "end", false] : [xz - 5, "end", true];
          const cy = i * rowH + rowH / 2;
          return (
            <g key={b.label} onPointerMove={onMove(i)} onPointerLeave={() => setHover(null)}>
              <rect x={-m.l} y={i * rowH} width={w} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
              <text x={-8} y={cy} textAnchor="end" fontSize={12} fill={b.total ? "var(--ink)" : "var(--ink-2)"} fontWeight={b.total ? 600 : 400}>
                <title>{b.label}</title>
                {lines[i].map((l, k) => (
                  <tspan key={k} x={-8} dy={k ? 13 : lines[i].length > 1 ? -2.5 : 4}>
                    {l}
                  </tspan>
                ))}
              </text>
              <rect x={xa} y={yy} width={Math.max(1, xz - xa)} height={bh} rx={3} fill={fill(b)} />
              {i < bars.length - 1 && <line x1={x(b.b)} x2={x(b.b)} y1={yy + bh} y2={(i + 1) * rowH + (rowH - bh) / 2} stroke="var(--axis)" />}
              <text x={tx} y={cy} dy="0.32em" textAnchor={anchor as "start" | "end"} fontSize={11} fill={inside ? "#ffffff" : "var(--ink-2)"} fontWeight={inside ? 600 : 400} className="num">
                {s}
              </text>
            </g>
          );
        })}
      </g>
    );
  }
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={svgH} role="img" aria-label={title || "ponte de valor"}>
          {body}
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

export type StackCol = { label: string; a: number; b: number; projected?: number | null };

/** Colunas empilhadas (A embaixo, B em cima, 2px de respiro entre segmentos) + colunas de projeção. */
export function StackedColumns({
  data,
  title,
  subtitle,
  labels,
  height = 230,
  fmt: fmtIn,
  table,
}: {
  data: StackCol[];
  title?: string;
  subtitle?: string;
  labels: [string, string, string];
  height?: number;
  fmt?: Fmt;
  table?: TableSpec;
}) {
  const fmt = toFn(fmtIn);
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const ih = height - 18 - 24;
  const tot = data.map((d) => (d.projected ?? 0) || d.a + d.b);
  const y = scaleLinear().domain([0, Math.max(0.0001, ...tot)]).range([ih, 0]).nice();
  const m = { t: 18, r: 12, b: 24, l: yAxisW(y.ticks(4), fmt, 48) };
  const iw = Math.max(40, w - m.l - m.r);
  const x = scaleBand<string>().domain(data.map((d) => d.label)).range([0, iw]).paddingInner(0.28).paddingOuter(0.1);
  const bw = Math.min(24, x.bandwidth());
  const off = (x.bandwidth() - bw) / 2;
  const xl = categoryLabels(data.map((d) => d.label), x.step());
  const firstProj = data.findIndex((d) => d.projected !== undefined && d.projected !== null);
  const legend: LegendItem[] = [
    { label: labels[0], color: C.s1, kind: "rect" },
    { label: labels[1], color: C.s2, kind: "rect" },
    ...(firstProj >= 0 ? [{ label: labels[2], color: C.proj, kind: "rect" as const }] : []),
  ];
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={height} role="img" aria-label={title || "colunas empilhadas"}>
          <g transform={`translate(${m.l},${m.t})`}>
            <YGrid ticks={y.ticks(4)} y={y} x0={0} x1={iw} fmt={fmt} />
            {firstProj > 0 && (
              <line
                x1={(x(data[firstProj].label) ?? 0) - (x.step() * x.paddingInner()) / 2}
                x2={(x(data[firstProj].label) ?? 0) - (x.step() * x.paddingInner()) / 2}
                y1={-12}
                y2={ih}
                stroke="var(--axis)"
              />
            )}
            {data.map((d, i) => {
              const bx = (x(d.label) ?? 0) + off;
              if (d.projected !== undefined && d.projected !== null) {
                return <path key={d.label} d={barPath(bx, y(0), y(d.projected), bw)} fill={C.proj} />;
              }
              const ya = y(d.a);
              const yb = y(d.a + d.b);
              const gap = d.a > 0 && d.b > 0 ? 2 : 0;
              return (
                <g key={d.label} opacity={hover && hover.i !== i ? 0.75 : 1}>
                  {d.a > 0 && (d.b > 0 ? <rect x={bx} y={ya} width={bw} height={Math.max(0, y(0) - ya)} fill={C.s1} /> : <path d={barPath(bx, y(0), ya, bw)} fill={C.s1} />)}
                  {d.b > 0 && <path d={barPath(bx, ya - gap, yb, bw)} fill={C.s2} />}
                </g>
              );
            })}
            <line x1={0} x2={iw} y1={y(0)} y2={y(0)} stroke="var(--axis)" />
            {data.map((d, i) => (
              <text key={d.label} x={(x(d.label) ?? 0) + x.bandwidth() / 2} y={ih + 16} textAnchor="middle" fontSize={11} fill="var(--muted)">
                {xl[i]}
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
            <div className="mb-1 text-[12px] text-muted">{data[hover.i].label}</div>
            {data[hover.i].projected !== undefined && data[hover.i].projected !== null ? (
              <TipRow label={labels[2]} value={fmt(data[hover.i].projected as number)} />
            ) : (
              <>
                <TipRow color={C.s1} label={labels[0]} value={fmt(data[hover.i].a)} />
                <TipRow color={C.s2} label={labels[1]} value={fmt(data[hover.i].b)} />
              </>
            )}
          </Tip>
        )}
      </div>
    </Frame>
  );
}
