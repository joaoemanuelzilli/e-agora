"use client";
import { useEffect, useLayoutEffect, useRef, useState, type ReactNode } from "react";

/** Largura do container (ResizeObserver). */
export function useWidth<T extends HTMLElement>(initial = 640) {
  const ref = useRef<T>(null);
  const [w, setW] = useState(initial);
  const iso = typeof window === "undefined" ? useEffect : useLayoutEffect;
  iso(() => {
    const el = ref.current;
    if (!el) return;
    setW(el.clientWidth || initial);
    const ro = new ResizeObserver((e) => {
      const cw = e[0]?.contentRect.width;
      if (cw) setW(cw);
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, w] as const;
}

export type LegendItem = { label: string; color: string; kind?: "line" | "rect" | "dot" | "ring"; dashed?: boolean };

export function Legend({ items }: { items: LegendItem[] }) {
  if (items.length < 2) return null;
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-1 text-[12px] text-ink-2">
      {items.map((it) => (
        <span key={it.label} className="inline-flex items-center gap-1.5">
          {it.kind === "rect" ? (
            <span style={{ width: 10, height: 10, borderRadius: 2, background: it.color, display: "inline-block" }} />
          ) : it.kind === "dot" ? (
            <span style={{ width: 8, height: 8, borderRadius: 8, background: it.color, display: "inline-block" }} />
          ) : it.kind === "ring" ? (
            <span style={{ width: 9, height: 9, borderRadius: 9, border: `2px solid ${it.color}`, display: "inline-block" }} />
          ) : (
            <span style={{ width: 14, height: 0, borderTop: `2px ${it.dashed ? "dotted" : "solid"} ${it.color}`, display: "inline-block" }} />
          )}
          {it.label}
        </span>
      ))}
    </div>
  );
}

export type TableSpec = { columns: string[]; rows: (string | number)[][] };

/** Moldura de gráfico: título, subtítulo, legenda, alternância gráfico/tabela (gêmeo acessível). */
export function Frame({
  title,
  subtitle,
  legend,
  table,
  children,
  right,
  className = "",
}: {
  title?: ReactNode;
  subtitle?: ReactNode;
  legend?: LegendItem[];
  table?: TableSpec;
  children: ReactNode;
  right?: ReactNode;
  className?: string;
}) {
  const [showTable, setShowTable] = useState(false);
  return (
    <figure className={`panel p-4 ${className}`}>
      {(title || table || right) && (
        <figcaption className="mb-2 flex items-start justify-between gap-3">
          <div className="min-w-0">
            {title && <div className="h3">{title}</div>}
            {subtitle && <div className="mt-0.5 text-[12px] text-muted">{subtitle}</div>}
          </div>
          <div className="flex shrink-0 items-center gap-2">
            {right}
            {table && (
              <button
                type="button"
                onClick={() => setShowTable((v) => !v)}
                className="no-print rounded border border-hairline px-2 py-0.5 text-[11px] text-ink-2 hover:bg-surface-2"
                aria-pressed={showTable}
              >
                {showTable ? "Gráfico" : "Tabela"}
              </button>
            )}
          </div>
        </figcaption>
      )}
      {legend && legend.length > 1 && (
        <div className="mb-2">
          <Legend items={legend} />
        </div>
      )}
      {showTable && table ? (
        <div className="max-h-[420px] overflow-auto">
          <table className="data text-[12px]">
            <thead>
              <tr>
                {table.columns.map((c) => (
                  <th key={c}>{c}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {table.rows.map((r, i) => (
                <tr key={i}>
                  {r.map((v, j) => (
                    <td key={j}>{v}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        children
      )}
    </figure>
  );
}

/** Tooltip posicionado dentro do container relativo. */
export function Tip({ x, y, w, children }: { x: number; y: number; w: number; children: ReactNode }) {
  const left = x > w * 0.6 ? undefined : x + 14;
  const right = x > w * 0.6 ? w - x + 14 : undefined;
  return (
    <div className="tooltip" style={{ left, right, top: Math.max(0, y - 10) }}>
      {children}
    </div>
  );
}

export function TipRow({ color, label, value, kind = "line" }: { color?: string; label: string; value: string; kind?: "line" | "dot" }) {
  return (
    <div className="flex items-center justify-between gap-4 py-[1px]">
      <span className="inline-flex items-center gap-1.5 text-ink-2">
        {color &&
          (kind === "dot" ? (
            <span style={{ width: 8, height: 8, borderRadius: 8, background: color, display: "inline-block" }} />
          ) : (
            <span style={{ width: 12, borderTop: `2px solid ${color}`, display: "inline-block" }} />
          ))}
        {label}
      </span>
      <span className="num font-semibold text-ink">{value}</span>
    </div>
  );
}

/** Eixo Y com grade em linha fina. */
export function YGrid({ ticks, y, x0, x1, fmt }: { ticks: number[]; y: (v: number) => number; x0: number; x1: number; fmt: (v: number) => string }) {
  return (
    <g>
      {ticks.map((t) => (
        <g key={t}>
          <line x1={x0} x2={x1} y1={y(t)} y2={y(t)} stroke="var(--grid)" strokeWidth={1} shapeRendering="crispEdges" />
          <text x={x0 - 6} y={y(t)} dy="0.32em" textAnchor="end" fontSize={11} fill="var(--muted)">
            {fmt(t)}
          </text>
        </g>
      ))}
    </g>
  );
}

export const C = {
  s1: "var(--series-1)",
  s2: "var(--series-2)",
  s3: "var(--series-3)",
  proj: "var(--proj)",
  deemph: "var(--deemph)",
  ink: "var(--ink)",
  ink2: "var(--ink-2)",
  muted: "var(--muted)",
  axis: "var(--axis)",
  grid: "var(--grid)",
  neg: "var(--div-neg)",
  pos: "var(--series-1)",
  surface: "var(--surface)",
  good: "var(--good)",
  critical: "var(--critical)",
};

/* Formatos serializáveis (para props vindas de componentes de servidor). */
export type FmtKind = "pct0" | "pct1" | "pct0s" | "pct1s" | "brl" | "num0" | "num1" | "num2" | "mult1" | "mn" | "idx" | "year" | "date";
export type Fmt = FmtKind | ((v: number) => string);
const nfmt = (d: number) => (v: number) => v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
const pfmt = (d: number, s: boolean) => (v: number) => `${s && v > 0 ? "+" : ""}${(v * 100).toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d })}%`;
export function toFn(f: Fmt | undefined, fallback: (v: number) => string = nfmt(0)): (v: number) => string {
  if (!f) return fallback;
  if (typeof f === "function") return f;
  switch (f) {
    case "pct0":
      return pfmt(0, false);
    case "pct1":
      return pfmt(1, false);
    case "pct0s":
      return pfmt(0, true);
    case "pct1s":
      return pfmt(1, true);
    case "brl":
      return (v) => `R$ ${nfmt(2)(v)}`;
    case "num1":
      return nfmt(1);
    case "num2":
      return nfmt(2);
    case "mult1":
      return (v) => `${nfmt(1)(v)}x`;
    case "mn":
      return (v) => (Math.abs(v) >= 1000 ? `${nfmt(1)(v / 1000)} bi` : `${nfmt(0)(v)} mi`);
    case "idx":
      return nfmt(0);
    case "year":
      return (v) => String(Math.round(v));
    case "date":
      return (v) => new Date(v).toLocaleDateString("pt-BR", { month: "short", year: "2-digit", timeZone: "UTC" }).replace(".", "");
    default:
      return nfmt(0);
  }
}
