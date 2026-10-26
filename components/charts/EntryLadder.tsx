"use client";
import { scaleLog } from "d3-scale";
import { useState } from "react";
import { C, Frame, Tip, TipRow, useWidth, type LegendItem } from "./core";

export type LadderRow = {
  ticker: string;
  price: number;
  ceiling: number | null; // TIR = Ke
  strong: number | null; // TIR = Ke + 5 p.p.
  fair: number | null; // valor justo (alvo)
  pre: number | null; // pré-eleição
};

const r2 = (v: number) => Math.round(v * 100) / 100;
const brl = (v: number) => `R$ ${v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
const pctS = (v: number) => `${v > 0 ? "+" : ""}${(v * 100).toLocaleString("pt-BR", { maximumFractionDigits: 1, minimumFractionDigits: 1 })}%`;

/** Faixa de compra por ação, em escala log da razão sobre o preço atual: zona entre "compra forte" e o preço-teto. */
export function EntryLadder({ rows, title, subtitle, keLabel }: { rows: LadderRow[]; title?: string; subtitle?: string; keLabel: string }) {
  const [ref, w] = useWidth<HTMLDivElement>(720);
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const rowH = 30;
  const labelW = 64;
  const m = { t: 24, r: 16, b: 8, l: labelW };
  const iw = Math.max(80, w - m.l - m.r);
  const h = rows.length * rowH + m.t + m.b;
  const ratios = rows.flatMap((r) => [r.ceiling, r.strong, r.fair, r.pre].filter((x): x is number => !!x && x > 0).map((x) => x / r.price));
  const lo = Math.min(0.5, ...ratios.map((x) => x * 0.92));
  const hi = Math.max(1.6, ...ratios.map((x) => x * 1.08));
  const x = scaleLog().domain([Math.max(0.2, lo), Math.min(4, hi)]).range([0, iw]).clamp(true);
  const ticks = [0.5, 0.75, 1, 1.25, 1.5, 2, 3].filter((t) => t >= x.domain()[0] && t <= x.domain()[1]);
  const legend: LegendItem[] = [
    { label: `Faixa de compra (Ke ${keLabel} a +5 p.p.)`, color: "var(--accent-soft)", kind: "rect" },
    { label: "Preço-teto", color: C.s1, kind: "ring" },
    { label: "Valor justo (alvo)", color: "var(--ink)", kind: "dot" },
    { label: "Pré-eleição", color: "var(--ink-2)", kind: "ring" },
  ];
  const cell = (v: number | null) => (v === null ? "—" : v.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
  const table = {
    columns: ["Ticker", "Preço agora", "Compra forte", "Preço-teto", "Valor justo", "Pré-eleição"],
    rows: rows.map((r) => [r.ticker, cell(r.price), cell(r.strong), cell(r.ceiling), cell(r.fair), cell(r.pre)]),
  };
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title || "faixa de compra"}>
          <g transform={`translate(${m.l},${m.t})`}>
            {ticks.map((t) => (
              <g key={t}>
                <line x1={r2(x(t))} x2={r2(x(t))} y1={-4} y2={rows.length * rowH} stroke={t === 1 ? "var(--ink)" : "var(--grid)"} strokeWidth={t === 1 ? 1.5 : 1} />
                <text x={r2(x(t))} y={-10} textAnchor="middle" fontSize={11} fill={t === 1 ? "var(--ink)" : "var(--muted)"} fontWeight={t === 1 ? 600 : 400}>
                  {t === 1 ? "preço agora" : pctS(t - 1).replace(",0", "")}
                </text>
              </g>
            ))}
            {rows.map((r, i) => {
              const yy = i * rowH + rowH / 2;
              const rc = r.ceiling ? r.ceiling / r.price : null;
              const rs = r.strong ? r.strong / r.price : null;
              const rf = r.fair ? r.fair / r.price : null;
              const rp = r.pre ? r.pre / r.price : null;
              const inside = rc !== null && rc >= 1;
              return (
                <g
                  key={r.ticker}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <rect x={-labelW} y={i * rowH} width={labelW + iw + m.r} height={rowH} fill={hover?.i === i ? "var(--surface-2)" : "transparent"} />
                  <text x={-8} y={yy} dy="0.32em" textAnchor="end" fontSize={12} fill="var(--ink)" fontWeight={600}>
                    {r.ticker}
                  </text>
                  {rc !== null && rs !== null && (
                    <rect x={r2(x(Math.min(rs, rc)))} y={yy - 7} width={Math.max(2, r2(Math.abs(x(rc) - x(rs))))} height={14} rx={4} fill="var(--accent-soft)" />
                  )}
                  {rc !== null && rs !== null && <rect x={r2(x(0.2))} y={yy - 1} width={Math.max(0, r2(x(Math.min(rs, rc)) - x(0.2)))} height={2} fill="var(--accent-soft)" />}
                  {rp !== null && <circle cx={r2(x(rp))} cy={yy} r={4} fill="var(--surface)" stroke="var(--ink-2)" strokeWidth={1.5} />}
                  {rf !== null && <circle cx={r2(x(rf))} cy={yy} r={4.5} fill="var(--ink)" stroke="var(--surface)" strokeWidth={2} />}
                  {rc !== null && <circle cx={r2(x(rc))} cy={yy} r={5.5} fill="var(--surface)" stroke={C.s1} strokeWidth={2.5} />}
                  <text x={iw + 4} y={yy} dy="0.32em" fontSize={11} fill={inside ? "var(--pos)" : "var(--ink-2)"} textAnchor="end" fontWeight={600}>
                    {rc === null ? "" : inside ? "na faixa" : ""}
                  </text>
                </g>
              );
            })}
          </g>
        </svg>
        {hover && rows[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">{rows[hover.i].ticker}</div>
            <TipRow label="Preço agora" value={brl(rows[hover.i].price)} />
            {rows[hover.i].ceiling && <TipRow color={C.s1} label={`Preço-teto (Ke ${keLabel})`} value={brl(rows[hover.i].ceiling as number)} />}
            {rows[hover.i].strong && <TipRow label="Compra forte (+5 p.p.)" value={brl(rows[hover.i].strong as number)} />}
            {rows[hover.i].fair && <TipRow color="var(--ink)" label="Valor justo (alvo)" value={brl(rows[hover.i].fair as number)} />}
            {rows[hover.i].pre && <TipRow label="Pré-eleição" value={brl(rows[hover.i].pre as number)} />}
          </Tip>
        )}
      </div>
    </Frame>
  );
}
