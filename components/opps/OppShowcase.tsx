"use client";
import { scaleLinear } from "d3-scale";
import Link from "next/link";
import { useState } from "react";
import type { LiveRow } from "@/components/Dashboard";
import { OppMap } from "@/components/charts/OppMap";
import { Tip, TipRow, useWidth } from "@/components/charts/core";
import { brl, num, pct, signClass } from "@/lib/format";
import { ceilingPrice } from "@/lib/valuation";
import { CallChip, callOf } from "@/components/ui/Rating";

export type ExtRow = {
  ticker: string;
  sinal: string;
  criterios?: string | null;
  etapa?: number;
  preco_2610?: number;
  valor_justo?: number;
  potencial?: number;
  tir_3a?: number;
  alerta?: string | null;
  decisao: "Comprar" | "Acompanhar" | "Evitar" | string;
  motivo_decisao?: string;
};
export type External = { titulo: string; autor: string; data: string; precos: string; aviso?: string; regra_combinada?: string; empresas: ExtRow[]; observacoes?: string[] };

const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);
const r2 = (v: number) => Math.round(v * 100) / 100;

/** Régua de preço: faixa de compra (compra forte → teto), preço de agora, valor justo e preço pré-eleição. */
export function PriceRail({ price, strong, ceiling, fair, pre }: { price: number; strong: number | null; ceiling: number | null; fair: number | null; pre: number | null }) {
  const [ref, w] = useWidth<HTMLDivElement>(320);
  const [hover, setHover] = useState<{ px: number; py: number } | null>(null);
  const vals = [price, strong, ceiling, fair, pre].filter(fin);
  const lo = Math.min(...vals);
  const hi = Math.max(...vals);
  const pad = (hi - lo) * 0.06 || hi * 0.05;
  const h = 44;
  const x = scaleLinear().domain([lo - pad, hi + pad]).range([6, Math.max(60, w - 6)]);
  const cy = 26;
  const inZone = fin(ceiling) && price <= ceiling;
  return (
    <div ref={ref} className="relative w-full" onPointerMove={(e) => {
      const b = e.currentTarget.getBoundingClientRect();
      setHover({ px: e.clientX - b.left, py: e.clientY - b.top });
    }} onPointerLeave={() => setHover(null)}>
      <svg width={w} height={h} role="img" aria-label="régua de preço" className="block">
        <line x1={6} x2={w - 6} y1={cy} y2={cy} stroke="var(--grid)" strokeWidth={2} />
        {fin(ceiling) && (
          <rect x={r2(x(fin(strong) ? Math.min(strong, ceiling) : lo - pad))} y={cy - 7} width={Math.max(3, r2(x(ceiling) - x(fin(strong) ? Math.min(strong, ceiling) : lo - pad)))} height={14} rx={1} fill="var(--buy-soft)" />
        )}
        {fin(ceiling) && <line x1={r2(x(ceiling))} x2={r2(x(ceiling))} y1={cy - 9} y2={cy + 9} stroke="var(--buy)" strokeWidth={2} />}
        {fin(fair) && <line x1={r2(x(fair))} x2={r2(x(fair))} y1={cy - 9} y2={cy + 9} stroke="var(--ink)" strokeWidth={2} />}
        {fin(pre) && <circle cx={r2(x(pre))} cy={cy} r={4} fill="var(--surface)" stroke="var(--ink-2)" strokeWidth={1.5} />}
        <circle cx={r2(x(price))} cy={cy} r={6.5} fill={inZone ? "var(--buy)" : "var(--wait)"} stroke="var(--surface)" strokeWidth={2} />
        <text x={r2(x(price))} y={10} textAnchor={x(price) < 40 ? "start" : x(price) > w - 40 ? "end" : "middle"} fontSize={11} fontWeight={600} fill="var(--ink)">
          {num(price)}
        </text>
      </svg>
      {hover && (
        <Tip x={hover.px} y={hover.py} w={w}>
          <TipRow label="Preço agora" value={brl(price)} />
          {fin(strong) && <TipRow label="Compra forte (Ke +5 p.p.)" value={brl(strong)} />}
          {fin(ceiling) && <TipRow color="var(--buy)" label="Preço-teto" value={brl(ceiling)} />}
          {fin(fair) && <TipRow color="var(--ink)" label="Valor justo" value={brl(fair)} />}
          {fin(pre) && <TipRow label="Pré-eleição (23/10)" value={brl(pre)} />}
        </Tip>
      )}
    </div>
  );
}

const DEC_TONE: Record<string, string> = { Comprar: "text-[var(--pos)]", Acompanhar: "text-ink", Evitar: "text-[var(--neg)]" };

function ThesisItem({ r, rank, ke, ext, headline, hasReport, name }: { r: LiveRow; rank: number; ke: number; ext?: ExtRow; headline?: string | null; hasReport: boolean; name?: string }) {
  const href = hasReport ? `/relatorio/${r.ticker}` : `/empresa/${r.ticker}`;
  const price = r.L.price;
  const ceiling = ceilingPrice(r.engine, ke);
  const strong = ceilingPrice(r.engine, ke + 0.05);
  const c = callOf(price, ceiling, strong);
  return (
    <article className="flex flex-col border-t border-hairline pt-4">
      <header className="flex flex-wrap items-start justify-between gap-x-4 gap-y-2">
        <div className="min-w-0">
          <div className="flex items-baseline gap-2">
            <span className="num text-[13px] text-muted">{rank}</span>
            <Link href={href} className="text-[17px] font-bold tracking-[-0.01em] hover:text-accent hover:underline">
              {r.ticker}
            </Link>
            <span className="truncate text-[12.5px] text-muted">{name ?? r.name}</span>
          </div>
        </div>
        <CallChip status={c.tone === "strong" ? "compra forte" : c.tone === "in" ? "na faixa" : c.tone === "out" ? "acima do teto" : "sem preço-teto"}>
          <span className="num text-[12px] text-ink-2">teto {num(ceiling)}</span>
        </CallChip>
      </header>
      {headline && <p className="mt-2.5 line-clamp-3 max-w-[68ch] text-[13.5px] leading-relaxed text-ink">{headline}</p>}
      {fin(price) && (
        <div className="mt-2">
          <PriceRail price={price} strong={strong} ceiling={ceiling} fair={r.L.fair} pre={r.prev_close} />
          <div className="flex justify-between text-[12px] text-muted">
            <span>{c.detail}</span>
            <span className="num">valor justo {num(r.L.fair)}</span>
          </div>
        </div>
      )}
      <div className="mt-auto flex flex-wrap items-center justify-between gap-x-4 gap-y-2 pt-3">
        <span className="text-[12px] text-ink-2">
          Segunda análise:{" "}
          {ext ? (
            <>
              <b className={DEC_TONE[ext.decisao] ?? ""}>{ext.decisao}</b> <span className="text-muted">({ext.sinal.toLowerCase()})</span>
            </>
          ) : (
            <span className="text-muted">não analisada</span>
          )}
        </span>
        <span className="flex gap-4 text-[13px]">
          <Link href={href} className="link">
            {hasReport ? "Ler o relatório" : "Análise completa"}
          </Link>
          <Link href="/investir" className="link">
            Montar ordem
          </Link>
        </span>
      </div>
    </article>
  );
}

function TwoOpinions({ ext, rows, opps }: { ext: External; rows: LiveRow[]; opps: string[] }) {
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const groups: { key: string; title: string; note: string }[] = [
    { key: "Comprar", title: "Comprar", note: "atrativa nas duas análises" },
    { key: "Acompanhar", title: "Acompanhar", note: "uma das duas não confirma" },
    { key: "Evitar", title: "Evitar", note: "nenhuma das duas vê margem" },
  ];
  return (
    <section>
      <div className="sec flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="h2">Duas análises independentes</h2>
        <span className="text-[12px] text-muted">
          {ext.autor}, {ext.data.split("-").reverse().join("/")}; preços de {ext.precos.split(" (")[0].toLowerCase()}
        </span>
      </div>
      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
        {groups.map((g) => {
          const items = ext.empresas.filter((e) => e.decisao === g.key);
          return (
            <div key={g.key}>
              <div className={`text-[14px] font-bold ${DEC_TONE[g.key]}`}>{g.title}</div>
              <div className="text-[12px] text-muted">{g.note}</div>
              <ul className="mt-2 space-y-3">
                {items.map((e) => {
                  const r = byT[e.ticker];
                  const inList = opps.includes(e.ticker);
                  return (
                    <li key={e.ticker} className="border-t border-hairline pt-2">
                      <div className="flex items-baseline justify-between gap-2">
                        <Link href={r ? `/empresa/${e.ticker}` : "#"} className="font-bold hover:text-accent">
                          {e.ticker}
                        </Link>
                        <span className="text-[12px] text-muted">{inList ? "na seleção do estudo" : "fora da seleção do estudo"}</span>
                      </div>
                      <div className="mt-1 grid grid-cols-2 gap-2 text-[12px]">
                        <div>
                          <div className="text-muted">Análise externa</div>
                          <div className="num">
                            VJ {num(e.valor_justo)} <span className={signClass(e.potencial)}>({pct(e.potencial, 0, true)})</span>
                          </div>
                        </div>
                        <div>
                          <div className="text-muted">Este estudo, agora</div>
                          <div className="num">
                            {r ? (
                              <>
                                VJ {num(r.L.fair)} <span className={signClass(r.L.upside)}>({pct(r.L.upside, 0, true)})</span>
                              </>
                            ) : (
                              "fora da cobertura"
                            )}
                          </div>
                        </div>
                      </div>
                      {(e.motivo_decisao || e.alerta) && <div className="mt-1 text-[12px] text-ink-2">{e.motivo_decisao ?? e.alerta}</div>}
                    </li>
                  );
                })}
              </ul>
            </div>
          );
        })}
      </div>
      {ext.regra_combinada && <p className="mt-4 text-[12px] text-muted">{ext.regra_combinada} {ext.aviso}</p>}
    </section>
  );
}

export function OppShowcase({ rows, ke, opps, external, headlines, reports = [], names = {} }: { rows: LiveRow[]; ke: number; opps: string[]; external?: External | null; headlines: Record<string, string>; reports?: string[]; names?: Record<string, string> }) {
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const extBy = Object.fromEntries((external?.empresas || []).map((e) => [e.ticker, e]));
  const list = opps.map((t) => byT[t]).filter(Boolean);
  const points = rows
    .filter((r) => r.engine?.template !== "holding" && fin(r.L.irr) && fin(r.L.prob))
    .map((r) => ({
      ticker: r.ticker,
      name: r.name,
      irr: r.L.irr as number,
      prob: r.L.prob as number,
      upside: r.L.upside,
      opp: opps.includes(r.ticker),
      inZone: (r.L.irr as number) >= 0.2 && (r.L.prob as number) >= 0.45,
    }));
  const inZoneNow = points.filter((p) => p.inZone).length;
  return (
    <div className="space-y-10">
      <section aria-labelledby="teses-h">
        <div className="sec flex flex-wrap items-baseline justify-between gap-3">
          <h2 id="teses-h" className="h2">
            A tese de cada recomendação
          </h2>
          <span className="max-w-[68ch] text-[12.5px] text-muted">Em cada régua: faixa de compra em verde, preço de agora no ponto, valor justo no traço escuro e preço pré-eleição no círculo vazio</span>
        </div>
        <div className="mt-3 grid grid-cols-1 gap-x-10 gap-y-6 md:grid-cols-2">
          {list.map((r, i) => (
            <ThesisItem key={r.ticker} r={r} rank={i + 1} ke={ke} ext={extBy[r.ticker]} headline={headlines[r.ticker] ?? r.summary} hasReport={reports.includes(r.ticker)} name={names[r.ticker]} />
          ))}
        </div>
      </section>
      <OppMap
        points={points}
        ke={ke}
        title="Onde estão as oportunidades"
        subtitle={`${points.length} empresas pela TIR de dono e pela chance de o valor justo superar o preço, ao preço de agora. ${inZoneNow} estão na zona da regra (TIR ≥ 20% e chance ≥ 45%); a seleção ainda exige solidez (Altman) e confiança do analista.`}
      />
      {external && external.empresas.length > 0 && <TwoOpinions ext={external} rows={rows} opps={opps} />}
    </div>
  );
}
