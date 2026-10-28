"use client";
import { scaleLinear } from "d3-scale";
import Link from "next/link";
import { useState } from "react";
import { C, Frame, Tip, TipRow, useWidth, type LegendItem } from "./core";

export type MapPoint = { ticker: string; name: string; irr: number; prob: number; upside: number | null; opp: boolean; inZone: boolean };

const r2 = (v: number) => Math.round(v * 100) / 100;
const p0 = (v: number) => `${Math.round(v * 100)}%`;
const p1 = (v: number) => `${(v * 100).toLocaleString("pt-BR", { maximumFractionDigits: 1, minimumFractionDigits: 1 })}%`;

/** TIR de dono × chance de o valor justo superar o preço, com a zona da regra de seleção e a linha do Ke. */
export function OppMap({ points, ke, irrMin = 0.2, probMin = 0.45, title, subtitle }: {
  points: MapPoint[]; ke: number; irrMin?: number; probMin?: number; title: string; subtitle?: string;
}) {
  const [ref, w] = useWidth<HTMLDivElement>(720);
  const [hover, setHover] = useState<{ i: number; px: number; py: number } | null>(null);
  const h = Math.max(300, Math.min(440, w * 0.55));
  const m = { t: 18, r: 18, b: 40, l: 46 };
  const iw = Math.max(120, w - m.l - m.r);
  const ih = h - m.t - m.b;
  const xs = points.map((p) => p.irr);
  const x = scaleLinear().domain([Math.min(0, ...xs) - 0.01, Math.max(ke + 0.06, ...xs) + 0.01]).range([0, iw]).nice().clamp(true);
  const y = scaleLinear().domain([0, 1]).range([ih, 0]);
  const legend: LegendItem[] = [
    { label: "Oportunidade selecionada", color: C.s1, kind: "dot" },
    { label: "Demais empresas", color: "var(--deemph)", kind: "dot" },
    { label: "Zona da regra de seleção", color: "var(--accent-soft)", kind: "rect" },
    { label: `Ke de ${Math.round(ke * 100)}%`, color: "var(--ink)", kind: "line", dashed: true },
  ];
  const sorted = [...points].sort((a, b) => Number(a.opp) - Number(b.opp));
  // rótulos das selecionadas sem sobreposição: tenta direita, acima, abaixo e esquerda
  const placed: { x0: number; x1: number; y0: number; y1: number }[] = points
    .filter((q) => q.opp)
    .map((q) => ({ x0: x(q.irr) - 7, x1: x(q.irr) + 7, y0: y(q.prob) - 7, y1: y(q.prob) + 7 }));
  const labelPos: Record<string, { x: number; y: number; anchor: "start" | "end" }> = {};
  for (const p of [...points].filter((q) => q.opp).sort((a, b) => b.prob - a.prob)) {
    const cx = x(p.irr);
    const cy = y(p.prob);
    const wTxt = p.ticker.length * 7.4;
    const cands: { x: number; y: number; anchor: "start" | "end" }[] = [
      { x: cx + 9, y: cy, anchor: "start" },
      { x: cx + 9, y: cy - 13, anchor: "start" },
      { x: cx + 9, y: cy + 13, anchor: "start" },
      { x: cx - 9, y: cy, anchor: "end" },
      { x: cx - 9, y: cy - 13, anchor: "end" },
      { x: cx - 9, y: cy + 13, anchor: "end" },
      { x: cx + 9, y: cy - 26, anchor: "start" },
      { x: cx + 9, y: cy + 26, anchor: "start" },
    ];
    const box = (c: { x: number; y: number; anchor: "start" | "end" }) => ({ x0: c.anchor === "start" ? c.x : c.x - wTxt, x1: c.anchor === "start" ? c.x + wTxt : c.x, y0: c.y - 7, y1: c.y + 7 });
    const ok = cands.find((c) => {
      const b0 = box(c);
      return b0.x1 <= iw + m.r && b0.x0 >= -m.l / 2 && !placed.some((q) => b0.x0 < q.x1 && b0.x1 > q.x0 && b0.y0 < q.y1 && b0.y1 > q.y0);
    }) ?? cands[0];
    placed.push(box(ok));
    labelPos[p.ticker] = ok;
  }
  const table = {
    columns: ["Ticker", "TIR de dono", "P(valor > preço)", "Upside", "Selecionada"],
    rows: [...points].sort((a, b) => b.irr - a.irr).map((p) => [p.ticker, p1(p.irr), p0(p.prob), p.upside === null ? "—" : p1(p.upside), p.opp ? "sim" : ""]),
  };
  return (
    <Frame title={title} subtitle={subtitle} legend={legend} table={table}>
      <div ref={ref} className="relative w-full">
        <svg className="chart block" width={w} height={h} role="img" aria-label={title}>
          <g transform={`translate(${m.l},${m.t})`}>
            <rect x={r2(x(irrMin))} y={0} width={Math.max(0, r2(iw - x(irrMin)))} height={r2(y(probMin))} fill="var(--accent-soft)" />
            {x.ticks(6).map((t) => (
              <g key={`x${t}`}>
                <line x1={r2(x(t))} x2={r2(x(t))} y1={0} y2={ih} stroke="var(--grid)" />
                <text x={r2(x(t))} y={ih + 16} textAnchor="middle" fontSize={11} fill="var(--muted)">
                  {p0(t)}
                </text>
              </g>
            ))}
            {[0, 0.25, 0.5, 0.75, 1].map((t) => (
              <g key={`y${t}`}>
                <line x1={0} x2={iw} y1={r2(y(t))} y2={r2(y(t))} stroke="var(--grid)" />
                <text x={-8} y={r2(y(t))} dy="0.32em" textAnchor="end" fontSize={11} fill="var(--muted)">
                  {p0(t)}
                </text>
              </g>
            ))}
            <line x1={r2(x(ke))} x2={r2(x(ke))} y1={0} y2={ih} stroke="var(--ink)" strokeWidth={1.25} strokeDasharray="4 3" />
            <text x={r2(x(ke)) + 4} y={10} fontSize={11} fill="var(--ink)">
              Ke {Math.round(ke * 100)}%
            </text>
            <text x={iw - 4} y={r2(y(probMin)) - 6} textAnchor="end" fontSize={11} fill="var(--accent-ink)" fontWeight={600}>
              zona de compra pela regra
            </text>
            {sorted.map((p) => {
              const i = points.indexOf(p);
              const cx = r2(x(p.irr));
              const cy = r2(y(p.prob));
              return (
                <g
                  key={p.ticker}
                  onPointerMove={(e) => {
                    const b = (e.currentTarget.ownerSVGElement as SVGSVGElement).getBoundingClientRect();
                    setHover({ i, px: e.clientX - b.left, py: e.clientY - b.top });
                  }}
                  onPointerLeave={() => setHover(null)}
                >
                  <circle cx={cx} cy={cy} r={12} fill="transparent" />
                  <circle cx={cx} cy={cy} r={p.opp ? 6 : 4} fill={p.opp ? C.s1 : "var(--deemph)"} stroke="var(--surface)" strokeWidth={p.opp ? 2 : 1} />
                  {p.opp && labelPos[p.ticker] && (
                    <text x={r2(labelPos[p.ticker].x)} y={r2(labelPos[p.ticker].y)} dy="0.32em" textAnchor={labelPos[p.ticker].anchor} fontSize={12} fontWeight={600} fill="var(--ink)">
                      {p.ticker}
                    </text>
                  )}
                </g>
              );
            })}
            <text x={iw / 2} y={ih + 34} textAnchor="middle" fontSize={11} fill="var(--ink-2)">
              TIR de dono ao preço de agora
            </text>
            <text transform={`translate(${-36},${ih / 2}) rotate(-90)`} textAnchor="middle" fontSize={11} fill="var(--ink-2)">
              Chance de valer mais que o preço
            </text>
          </g>
        </svg>
        {hover && points[hover.i] && (
          <Tip x={hover.px} y={hover.py} w={w}>
            <div className="mb-1 font-semibold">
              <Link href={`/empresa/${points[hover.i].ticker}`}>{points[hover.i].ticker}</Link>{" "}
              <span className="font-normal text-muted">{points[hover.i].name}</span>
            </div>
            <TipRow label="TIR de dono" value={p1(points[hover.i].irr)} />
            <TipRow label="P(valor > preço)" value={p0(points[hover.i].prob)} />
            {points[hover.i].upside !== null && <TipRow label="Upside" value={p1(points[hover.i].upside as number)} />}
            <div className="mt-1 text-[11px] text-muted">{points[hover.i].opp ? "Selecionada" : points[hover.i].inZone ? "Na zona, fora por outro filtro" : "Fora da zona"}</div>
          </Tip>
        )}
      </div>
    </Frame>
  );
}
