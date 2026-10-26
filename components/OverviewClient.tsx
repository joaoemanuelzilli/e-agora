"use client";
import { Hero, OppCards, Screener, useLiveRows } from "@/components/Dashboard";
import { num, pct } from "@/lib/format";
import { useMarket } from "@/lib/live";
import type { MarketStats, Row, XSec } from "@/lib/types";

function median(a: number[]) {
  const s = [...a].sort((x, y) => x - y);
  if (!s.length) return null;
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function Kpi({ label, value, note, emphasis }: { label: string; value: string; note?: string; emphasis?: boolean }) {
  return (
    <div className="border-b border-hairline py-3 last:border-b-0">
      <div className="label">{label}</div>
      <div className={`mt-0.5 ${emphasis ? "text-[34px] leading-none" : "text-[22px] leading-tight"} font-semibold tracking-[-0.01em]`}>{value}</div>
      {note && <div className="mt-1 text-[12px] text-ink-2">{note}</div>}
    </div>
  );
}

export function OverviewClient({ rows, opps, market, xsec }: { rows: Row[]; opps: string[]; market: MarketStats; xsec: XSec }) {
  const { rows: live, ke, asOf } = useLiveRows(rows);
  const m = useMarket();
  const ibChg = m?.indices?.IBOV?.chg ?? market.ibov_today.chg;
  const rank = ibChg !== null && ibChg !== undefined ? 1 + market.worst_days.filter((d) => d.ret < ibChg).length : null;
  const z = ibChg !== null && ibChg !== undefined ? (ibChg - market.ibov_daily_return_stats.mean) / market.ibov_daily_return_stats.std : null;
  const med = median(live.map((r) => r.chgLive).filter((x): x is number => typeof x === "number"));
  const nKe = live.filter((r) => (r.L.irr ?? -1) >= ke).length;
  const f12 = market.crash_forward_stats.f12m;
  return (
    <div className="space-y-8">
      <section className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-8">
          <h1 className="h1 max-w-[30ch]">O dia seguinte à reeleição</h1>
          <p className="mt-2 max-w-[68ch] text-[15px] text-ink-2">
            Lula venceu com 51,8% e a bolsa acionou o circuit breaker. Estas são as 59 ações líquidas que caíram 20% ou mais, avaliadas uma a uma com dados oficiais da CVM e da B3, a um custo de capital de {Math.round(ke * 100)}%.
          </p>
          <div className="mt-5">
            <Hero rows={live} ke={ke} />
          </div>
        </div>
        <aside className="lg:col-span-4">
          <div className="panel px-4 py-1 lg:sticky lg:top-[118px]">
            <Kpi
              emphasis
              label="Ibovespa hoje"
              value={pct(ibChg, 1, true)}
              note={rank ? `${rank}º pior dia desde 1998, ${num(z, 1)} desvios-padrão` : undefined}
            />
            <Kpi label="Queda mediana das 59" value={pct(med, 1, true)} note="contra o fechamento de sexta (23/10)" />
            <Kpi label={`TIR de dono acima do Ke de ${Math.round(ke * 100)}%`} value={`${nKe} de ${live.length}`} note="ao preço atual, recalculado ao vivo" />
            <Kpi
              label="Quanto da queda é macro"
              value={pct(xsec.r2, 0)}
              note={`R² da regressão das ${xsec.n} ações em beta, alavancagem, porte e setor; só o beta explica ${pct(xsec.r2_beta_only, 0)}`}
            />
            <Kpi
              label="Ibovespa 12 meses após quedas de 5% ou mais"
              value={pct(f12.median, 0, true)}
              note={`mediana de ${f12.n} episódios desde 1998, alta em ${pct(f12.pct_pos, 0)} deles`}
            />
            <div className="py-2 text-[11px] text-muted">{asOf ? `Preços atualizados às ${new Date(asOf).toLocaleTimeString("pt-BR")}` : "Carregando preços ao vivo…"}</div>
          </div>
        </aside>
      </section>

      <section>
        <div className="mb-3 flex items-baseline justify-between gap-4">
          <h2 className="h2">Melhores oportunidades</h2>
          <span className="text-[12px] text-muted">Maior TIR de dono, filtrada por solidez financeira e probabilidade no Monte Carlo</span>
        </div>
        <OppCards rows={live} ke={ke} opps={opps} />
      </section>

      <Screener rows={live} ke={ke} opps={opps} />
    </div>
  );
}
