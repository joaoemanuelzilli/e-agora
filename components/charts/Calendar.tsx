"use client";
import { useState, type ReactNode } from "react";
import { Frame, Tip, useWidth, type TableSpec } from "./core";

export type CalRow = { id: string; label: string; sub?: string; cells: (number | null)[]; detail?: (ReactNode | null)[]; total?: string; href?: string };

/** Calendário em mapa de calor sequencial (um matiz): intensidade = valor / escala. Células vazias = sem pagamento. */
export function CalendarHeatmap({
  rows,
  cols,
  title,
  subtitle,
  scaleMax,
  fmt,
  totalLabel,
  dividerAfter,
  table,
  legendNote,
}: {
  rows: CalRow[];
  cols: string[];
  title?: string;
  subtitle?: string;
  scaleMax: number;
  fmt: (v: number) => string;
  totalLabel?: string;
  dividerAfter?: number;
  table?: TableSpec;
  legendNote?: string;
}) {
  const [ref, w] = useWidth<HTMLDivElement>(900);
  const [hover, setHover] = useState<{ r: number; c: number; px: number; py: number } | null>(null);
  const labelW = 76;
  const totalW = totalLabel ? 58 : 0;
  const top = 22;
  const cellW = Math.max(14, (w - labelW - totalW - 6) / cols.length);
  const cellH = 17;
  const h = top + rows.length * cellH + 4;
  const color = (v: number | null) => {
    if (v === null || v <= 0) return "var(--surface-2)";
    const t = Math.max(0, Math.min(1, v / scaleMax));
    return `color-mix(in oklab, var(--series-1) ${Math.round(18 + t * 82)}%, var(--surface))`;
  };
  const steps = [0.25, 0.5, 0.75, 1];
  return (
    <Frame title={title} subtitle={subtitle} table={table}>
      <div className="mb-2 flex flex-wrap items-center gap-3 text-[11.5px] text-ink-2">
        <span className="inline-flex items-center gap-1.5">
          <span style={{ width: 12, height: 10, borderRadius: 2, background: "var(--surface-2)", display: "inline-block", border: "1px solid var(--hairline)" }} />
          sem provento
        </span>
        {steps.map((s) => (
          <span key={s} className="inline-flex items-center gap-1.5">
            <span style={{ width: 12, height: 10, borderRadius: 2, background: color(s * scaleMax), display: "inline-block" }} />
            {fmt(s * scaleMax)}
            {s === 1 ? " ou mais" : ""}
          </span>
        ))}
        {legendNote && <span className="text-muted">{legendNote}</span>}
      </div>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "calendário"}>
          {cols.map((c, i) => (
            <text key={c} x={labelW + i * cellW + cellW / 2} y={14} textAnchor="middle" fontSize={10.5} fill="var(--muted)">
              {cellW < 26 && i % 2 === 1 ? "" : c}
            </text>
          ))}
          {totalLabel && (
            <text x={labelW + cols.length * cellW + 6 + totalW / 2} y={14} textAnchor="middle" fontSize={10.5} fill="var(--ink-2)" fontWeight={500}>
              {totalLabel}
            </text>
          )}
          {dividerAfter !== undefined && (
            <line x1={labelW + (dividerAfter + 1) * cellW} x2={labelW + (dividerAfter + 1) * cellW} y1={top - 4} y2={h} stroke="var(--ink)" strokeWidth={1.5} />
          )}
          {rows.map((r, ri) => (
            <g key={r.id}>
              <a href={r.href}>
                <text x={labelW - 8} y={top + ri * cellH + cellH / 2} dy="0.32em" textAnchor="end" fontSize={11} fill="var(--ink)" fontWeight={500}>
                  {r.label}
                </text>
              </a>
              {r.cells.map((v, ci) => (
                <rect
                  key={ci}
                  x={labelW + ci * cellW + 1}
                  y={top + ri * cellH + 1}
                  width={Math.max(1, cellW - 2)}
                  height={cellH - 2}
                  rx={2}
                  fill={color(v)}
                  stroke={hover && hover.r === ri && hover.c === ci ? "var(--ink)" : "none"}
                  strokeWidth={1.5}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ r: ri, c: ci, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                />
              ))}
              {r.total && (
                <text x={labelW + cols.length * cellW + 6 + totalW / 2} y={top + ri * cellH + cellH / 2} dy="0.32em" textAnchor="middle" fontSize={11} fill="var(--ink)" className="num">
                  {r.total}
                </text>
              )}
            </g>
          ))}
        </svg>
        {hover && rows[hover.r] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">
              {rows[hover.r].label} <span className="font-normal text-muted">{cols[hover.c]}</span>
            </div>
            {rows[hover.r].cells[hover.c] ? (
              <div className="num font-semibold">{fmt(rows[hover.r].cells[hover.c] as number)}</div>
            ) : (
              <div className="text-muted">sem provento</div>
            )}
            {rows[hover.r].detail?.[hover.c]}
          </Tip>
        )}
      </div>
    </Frame>
  );
}
