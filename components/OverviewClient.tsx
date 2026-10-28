"use client";
import { Hero, Screener, useLiveRows } from "@/components/Dashboard";
import { OppShowcase, type External } from "@/components/opps/OppShowcase";
import { num, pct } from "@/lib/format";
import { useMarket } from "@/lib/live";
import { ceilingPrice } from "@/lib/valuation";
import Link from "next/link";
import type { MarketStats, Row, XSec } from "@/lib/types";

function median(a: number[]) {
  const s = [...a].sort((x, y) => x - y);
  if (!s.length) return null;
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function Kpi({ label, value, note, emphasis }: { label: string; value: string; note?: string; emphasis?: boolean }) {
  return (
    <div className="border-b border-hairline py-3 [&:nth-last-child(-n+2)]:border-b-0">
      <div className="label">{label}</div>
      <div className={`mt-0.5 ${emphasis ? "text-[34px] leading-none" : "text-[22px] leading-tight"} font-semibold tracking-[-0.01em]`}>{value}</div>
      {note && <div className="mt-1 text-[12px] text-ink-2">{note}</div>}
    </div>
  );
}

function BuyNow({ rows, opps, ke, reports }: { rows: ReturnType<typeof useLiveRows>["rows"]; opps: string[]; ke: number; reports: string[] }) {
  const link = (t: string) => (reports.includes(t) ? `/relatorio/${t}` : `/empresa/${t}`);
  const byT = Object.fromEntries(rows.map((r) => [r.ticker, r]));
  const items = opps
    .map((t) => byT[t])
    .filter(Boolean)
    .map((r) => {
      const c = ceilingPrice(r.engine, ke);
      const p = r.L.price;
      return { t: r.ticker, inZone: !!(c && p && p <= c), gap: c && p ? 1 - c / p : null };
    });
  const inZ = items.filter((x) => x.inZone);
  const out = items.filter((x) => !x.inZone);
  if (!items.length) return null;
  return (
    <div className="mt-6 space-y-3">
      <div>
        <div className="label">Na faixa de compra agora</div>
        <div className="mt-1.5 flex flex-wrap gap-2">
          {inZ.length ? (
            inZ.map((x) => (
              <Link key={x.t} href={link(x.t)} className="inline-flex items-center gap-1.5 rounded-full border border-hairline bg-surface px-3 py-1 text-[13.5px] font-semibold hover:border-accent">
                <span className="h-2 w-2 rounded-full bg-[var(--pos)]" aria-hidden />
                {x.t}
              </Link>
            ))
          ) : (
            <span className="text-[13px] text-muted">nenhuma: todas acima do preço-teto</span>
          )}
        </div>
      </div>
      {out.length > 0 && (
        <div>
          <div className="label">Acima do preço-teto</div>
          <div className="mt-1.5 flex flex-wrap gap-2">
            {out.map((x) => (
              <Link key={x.t} href={link(x.t)} className="inline-flex items-center gap-1.5 rounded-full border border-hairline px-3 py-1 text-[13px] text-ink-2 hover:border-accent">
                <span className="h-2 w-2 rounded-full bg-[var(--deemph)]" aria-hidden />
                {x.t}
                {x.gap !== null && <span className="num text-[12px] text-muted">falta {pct(x.gap, 1)}</span>}
              </Link>
            ))}
          </div>
        </div>
      )}
      <Link href="/investir" className="inline-block text-[13px] font-medium text-accent hover:underline">
        Ver preços de ordem e quantidades
      </Link>
    </div>
  );
}

export function OverviewClient({ rows, opps, market, xsec, external, headlines, valLabel, reports = [] }: {
  rows: Row[]; opps: string[]; market: MarketStats; xsec: XSec; external?: External | null; headlines: Record<string, string>; valLabel?: string | null; reports?: string[];
}) {
  const { rows: live, ke, asOf } = useLiveRows(rows);
  const m = useMarket();
  const ibChg = m?.indices?.IBOV?.chg ?? market.ibov_today.chg;
  const rank = ibChg !== null && ibChg !== undefined ? 1 + market.worst_days.filter((d) => d.ret < ibChg).length : null;
  const z = ibChg !== null && ibChg !== undefined ? (ibChg - market.ibov_daily_return_stats.mean) / market.ibov_daily_return_stats.std : null;
  const sinceElection = live
    .map((r) => (r.L.price && r.prev_close ? r.L.price / r.prev_close - 1 : null))
    .filter((x): x is number => typeof x === "number" && Number.isFinite(x));
  const med = median(sinceElection);
  const ibNow = m?.indices?.IBOV?.price ?? null;
  const ibSince = ibNow && market.ibov_today.prev_close ? ibNow / market.ibov_today.prev_close - 1 : null;
  const n = live.length;
  const nKe = live.filter((r) => (r.L.irr ?? -1) >= ke).length;
  const f12 = market.crash_forward_stats.f12m;
  return (
    <div className="space-y-8">
      <section className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-6">
          <h1 className="h1 max-w-[30ch]">O dia seguinte à reeleição</h1>
          <p className="mt-2 max-w-[62ch] text-[15px] text-ink-2">
            Lula venceu com 51,8% e a bolsa acionou o circuit breaker em 26/10. Estas são {n} ações líquidas da bolsa, das que mais caíram no dia às maiores do índice, avaliadas uma a uma com dados oficiais da CVM e da B3, a um custo de capital de {Math.round(ke * 100)}%.
          </p>
          <div className="mt-2 text-[11.5px] text-muted">{asOf ? `Preços ao vivo, atualizados às ${new Date(asOf).toLocaleTimeString("pt-BR")}` : "Carregando preços ao vivo…"}</div>
          <BuyNow rows={live} opps={opps} ke={ke} reports={reports} />
        </div>
        <div className="panel grid grid-cols-2 gap-x-5 px-4 py-1 lg:col-span-6">
          <Kpi
            emphasis
            label="Ibovespa desde a eleição"
            value={pct(ibSince, 1, true)}
            note={`contra o fechamento de 23/10; hoje ${pct(ibChg, 1, true)}${rank && ibChg !== null && ibChg < -0.04 ? `, ${rank}º pior dia desde 1998` : ""}`}
          />
          <Kpi emphasis label={`Mediana das ${n} desde a eleição`} value={pct(med, 1, true)} note={`às 13h02 de 26/10 o Ibovespa caía ${pct(-(market.ibov_today.chg ?? 0), 1)}, o ${market.ibov_today.rank_since_1998 ?? "—"}º pior dia desde 1998`} />
          <Kpi label={`TIR de dono acima do Ke de ${Math.round(ke * 100)}%`} value={`${nKe} de ${n}`} note="ao preço de agora, recalculado ao vivo" />
          <Kpi label="Quanto da queda foi macro" value={pct(xsec.r2, 0)} note={`R² da regressão de ${xsec.n} ações em beta, alavancagem, porte e setor`} />
          <Kpi label="Ibovespa 12 meses depois de quedas de 5%+" value={pct(f12.median, 0, true)} note={`mediana de ${f12.n} episódios desde 1998, alta em ${pct(f12.pct_pos, 0)}`} />
          <Kpi label="Dia do crash, 26/10" value={pct(market.ibov_today.chg, 1, true)} note="Ibovespa às 13h02, a foto da análise de queda" />
        </div>
      </section>

      <section>
        <div className="mb-3 flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
          <h2 className="h2">Melhores oportunidades</h2>
          <span className="text-[12px] text-muted">
            {opps.length} de {n} passam na regra: TIR de dono ≥ 20%, chance ≥ 45%, solidez e confiança{valLabel ? `; seleção com o ${valLabel.toLowerCase()}` : ""}
          </span>
        </div>
        <OppShowcase rows={live} ke={ke} opps={opps} external={external} headlines={headlines} reports={reports} />
      </section>

      <section>
        <Hero rows={live} ke={ke} />
      </section>

      <Screener rows={live} ke={ke} opps={opps} />
    </div>
  );
}
