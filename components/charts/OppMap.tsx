"use client";
import { scaleLinear } from "d3-scale";
import Link from "next/link";
import { useState } from "react";
import { C, Frame, Tip, TipRow, useWidth, type LegendItem } from "./core";
import { textW } from "./measure";

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
  type Box = { x0: number; x1: number; y0: number; y1: number };
  type Pos = { x: number; y: number; anchor: "start" | "end" | "middle"; far: boolean };
  const hit = (a: Box, b: Box) => a.x0 < b.x1 && a.x1 > b.x0 && a.y0 < b.y1 && a.y1 > b.y0;
  const area = (a: Box, b: Box) => Math.max(0, Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0)) * Math.max(0, Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0));
  const kx = x(ke);
  // rótulos das selecionadas: candidatos do mais perto ao mais longe; busca local que pune sobrepor
  // outro rótulo, cobrir um ponto e (de leve) cruzar a linha do Ke
  const opps = points.filter((q) => q.opp).sort((a, b) => b.prob - a.prob);
  const oppDots: Box[] = opps.map((q) => ({ x0: x(q.irr) - 7, x1: x(q.irr) + 7, y0: y(q.prob) - 7, y1: y(q.prob) + 7 }));
  const keLine: Box = { x0: kx - 1.5, x1: kx + 1.5, y0: 0, y1: ih };
  const options = opps.map((p) => {
    const cx = x(p.irr);
    const cy = y(p.prob);
    const wTxt = textW(p.ticker, 12, 600);
    const cands: Pos[] = [
      { x: cx + 9, y: cy, anchor: "start", far: false },
      { x: cx - 9, y: cy, anchor: "end", far: false },
      { x: cx, y: cy - 15, anchor: "middle", far: false },
      { x: cx, y: cy + 15, anchor: "middle", far: false },
      { x: cx + 9, y: cy - 13, anchor: "start", far: false },
      { x: cx + 9, y: cy + 13, anchor: "start", far: false },
      { x: cx - 9, y: cy - 13, anchor: "end", far: false },
      { x: cx - 9, y: cy + 13, anchor: "end", far: false },
      { x: cx + 9, y: cy - 26, anchor: "start", far: true },
      { x: cx + 9, y: cy + 26, anchor: "start", far: true },
      { x: cx - 9, y: cy - 26, anchor: "end", far: true },
      { x: cx - 9, y: cy + 26, anchor: "end", far: true },
    ];
    const box = (c: Pos): Box => {
      const x0 = c.anchor === "start" ? c.x : c.anchor === "end" ? c.x - wTxt : c.x - wTxt / 2;
      return { x0, x1: x0 + wTxt, y0: c.y - 6, y1: c.y + 6 };
    };
    const ok = cands.filter((c) => {
      const b0 = box(c);
      return b0.x1 <= iw + m.r && b0.x0 >= -m.l / 2 && b0.y0 >= -m.t && b0.y1 <= ih;
    });
    return (ok.length ? ok : cands).map((c, k) => ({ c, b: box(c), rank: k }));
  });
  const choice = options.map(() => -1);
  const cost = (i: number, k: number) => {
    const o = options[i][k];
    let s = o.rank * 1.5 + area(o.b, keLine) * 1.5;
    oppDots.forEach((d) => (s += area(o.b, d) * 6));
    choice.forEach((j, n) => {
      if (n !== i && j >= 0) s += area(o.b, options[n][j].b) * 4;
    });
    return s;
  };
  const best = (i: number) => options[i].reduce((bk, _, k) => (cost(i, k) < cost(i, bk) ? k : bk), 0);
  for (let i = 0; i < options.length; i++) choice[i] = best(i);
  for (let pass = 0; pass < 4; pass++) for (let i = 0; i < options.length; i++) choice[i] = best(i);
  const labelPos: Record<string, Pos> = {};
  const placed: Box[] = [...oppDots];
  opps.forEach((p, i) => {
    labelPos[p.ticker] = options[i][choice[i]].c;
    placed.push(options[i][choice[i]].b);
  });
  // rótulo afastado do ponto ganha um fio até ele
  const leader = (p: MapPoint) => {
    const i = opps.indexOf(p);
    const o = options[i][choice[i]];
    if (!o.c.far) return null;
    const cx = x(p.irr);
    const cy = y(p.prob);
    const tx = Math.max(o.b.x0, Math.min(o.b.x1, cx));
    const ty = o.c.y > cy ? o.b.y0 + 2 : o.b.y1 - 2;
    const d = Math.hypot(tx - cx, ty - cy) || 1;
    return { x1: cx + ((tx - cx) / d) * 7, y1: cy + ((ty - cy) / d) * 7, x2: tx, y2: ty };
  };
  // anotações (Ke e zona) depois dos tickers: evitam rótulos e pontos; se não couberem, ficam só na legenda
  // folga generosa: a anotação não pode parecer rótulo de um ponto vizinho
  const dots: Box[] = points.map((q) => {
    const r = (q.opp ? 7 : 5) + 5;
    return { x0: x(q.irr) - r, x1: x(q.irr) + r, y0: y(q.prob) - r, y1: y(q.prob) + r };
  });
  type Ann = { x: number; y: number; anchor: "start" | "end"; text: string };
  const annBox = (a: Ann, weight: number): Box => {
    const tw = textW(a.text, 11, weight);
    return { x0: a.anchor === "start" ? a.x : a.x - tw, x1: a.anchor === "start" ? a.x + tw : a.x, y0: a.y - 8, y1: a.y + 2.5 };
  };
  const grow = (b: Box, k: number): Box => ({ x0: b.x0 - k, x1: b.x1 + k, y0: b.y0 - k, y1: b.y1 + k });
  const pick = (cands: Ann[], weight: number) => {
    const ok = cands.find((c) => {
      const b = annBox(c, weight);
      const g = grow(b, 4);
      return b.x0 >= 0 && b.x1 <= iw && b.y0 >= 0 && b.y1 <= ih && !placed.some((q) => hit(g, q)) && !dots.some((q) => hit(b, q));
    });
    if (ok) placed.push(annBox(ok, weight));
    return ok ?? null;
  };
  const keText = `Ke ${Math.round(ke * 100)}%`;
  const keAnn = pick(
    [10, ih - 5, 24, ih - 19].flatMap((yy) => [
      { x: kx + 4, y: yy, anchor: "start" as const, text: keText },
      { x: kx - 4, y: yy, anchor: "end" as const, text: keText },
    ]),
    400,
  );
  const zx = x(irrMin);
  const zy = y(probMin);
  const zoneAnn = pick(
    ["zona de compra pela regra", "zona da regra"].flatMap((text) => [
      { x: iw - 4, y: zy - 6, anchor: "end" as const, text },
      { x: zx + 4, y: zy - 6, anchor: "start" as const, text },
      { x: zx + 4, y: 12, anchor: "start" as const, text },
      { x: iw - 4, y: 12, anchor: "end" as const, text },
      { x: iw - 4, y: zy + 14, anchor: "end" as const, text },
    ]),
    600,
  );
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
            {keAnn && (
              <text x={r2(keAnn.x)} y={r2(keAnn.y)} textAnchor={keAnn.anchor} fontSize={11} fill="var(--ink)">
                {keAnn.text}
              </text>
            )}
            {zoneAnn && (
              <text x={r2(zoneAnn.x)} y={r2(zoneAnn.y)} textAnchor={zoneAnn.anchor} fontSize={11} fill="var(--accent-ink)" fontWeight={600}>
                {zoneAnn.text}
              </text>
            )}
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
                  {p.opp &&
                    (() => {
                      const l = leader(p);
                      return l ? <line x1={r2(l.x1)} y1={r2(l.y1)} x2={r2(l.x2)} y2={r2(l.y2)} stroke="var(--ink-2)" strokeWidth={0.75} /> : null;
                    })()}
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
            <div className="mt-1 text-[12px] text-muted">{points[hover.i].opp ? "Selecionada" : points[hover.i].inZone ? "Na zona, fora por outro filtro" : "Fora da zona"}</div>
          </Tip>
        )}
      </div>
    </Frame>
  );
}
