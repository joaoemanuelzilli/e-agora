"use client";
import { Hero, Screener, useLiveRows } from "@/components/Dashboard";
import { OppShowcase, type External } from "@/components/opps/OppShowcase";
import { pct, signClass } from "@/lib/format";
import { useMarket } from "@/lib/live";
import Link from "next/link";
import { KeyData, PicksTable, usePicks } from "@/components/painel/TopPicks";
import type { Registro } from "@/components/registro/Registro";
import type { MarketStats, Row, XSec } from "@/lib/types";

function median(a: number[]) {
  const s = [...a].sort((x, y) => x - y);
  if (!s.length) return null;
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

export function OverviewClient({ rows, opps, market, xsec, external, headlines, valLabel, reports = [], registro = null, names = {}, theses = {} }: {
  rows: Row[]; opps: string[]; market: MarketStats; xsec: XSec; external?: External | null; headlines: Record<string, string>; valLabel?: string | null; reports?: string[]; registro?: Registro | null; names?: Record<string, string>; theses?: Record<string, string>;
}) {
  const { rows: live, ke, asOf } = useLiveRows(rows);
  const m = useMarket();
  const ibChg = m?.indices?.IBOV?.chg ?? market.ibov_today.chg;
  const rank = ibChg !== null && ibChg !== undefined ? 1 + market.worst_days.filter((d) => d.ret < ibChg).length : null;
  const sinceElection = live
    .map((r) => (r.L.price && r.prev_close ? r.L.price / r.prev_close - 1 : null))
    .filter((x): x is number => typeof x === "number" && Number.isFinite(x));
  const med = median(sinceElection);
  const ibNow = m?.indices?.IBOV?.price ?? null;
  const ibSince = ibNow && market.ibov_today.prev_close ? ibNow / market.ibov_today.prev_close - 1 : null;
  const n = live.length;
  const nKe = live.filter((r) => (r.L.irr ?? -1) >= ke).length;
  const f12 = market.crash_forward_stats.f12m;
  const picks = usePicks(live, opps, ke, reports, registro, names, theses);
  const keItems = [
    { label: "Ibovespa desde a eleição", value: pct(ibSince, 1, true), cls: signClass(ibSince), note: "contra o fechamento de 23/10" },
    { label: "Ibovespa hoje", value: pct(ibChg, 1, true), cls: signClass(ibChg), note: rank && ibChg !== null && ibChg < -0.04 ? `${rank}º pior dia desde 1998` : undefined },
    { label: "Mediana da cobertura desde a eleição", value: pct(med, 1, true), cls: signClass(med) },
    { label: "Dia do crash, 26/10 às 13h02", value: pct(market.ibov_today.chg, 1, true), cls: signClass(market.ibov_today.chg), note: `${market.ibov_today.rank_since_1998 ?? "—"}º pior dia desde 1998` },
    { label: "Quanto da queda foi macro", value: pct(xsec.r2, 0), note: `R² em ${xsec.n} ações` },
    { label: "Ibovespa 12 meses após quedas de 5%+", value: pct(f12.median, 0, true), cls: signClass(f12.median), note: `mediana de ${f12.n} episódios, alta em ${pct(f12.pct_pos, 0)}` },
    { label: `TIR de dono acima do Ke de ${Math.round(ke * 100)}%`, value: `${nKe} de ${n}` },
    { label: "Passam na regra", value: `${opps.length} de ${n}` },
  ];
  return (
    <div className="space-y-10">
      <section className="grid grid-cols-1 gap-x-8 gap-y-6 lg:grid-cols-12">
        <div className="lg:col-span-9">
          <header className="flex flex-wrap items-start justify-between gap-x-6 gap-y-3">
            <div>
              <h1 className="h1">Top picks pós-eleição{registro ? `, ${registro.data_ref.split("-").reverse().join("/")}` : ""}</h1>
              <p className="mt-1.5 text-[13px] text-muted">
                Seleção com o {valLabel ? valLabel.toLowerCase() : "fechamento de 28/10/2026"}; {n} empresas cobertas; Ke de {Math.round(ke * 100)}%.{" "}
                {asOf ? `Preços ao vivo às ${new Date(asOf).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}.` : "Carregando preços ao vivo…"}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {registro && (
                <Link href="/registro" className="btn btn-secondary">
                  Registro de {registro.data_ref.slice(8, 10)}/{registro.data_ref.slice(5, 7)}
                </Link>
              )}
              <Link href="/investir" className="btn btn-primary">
                Ver ordens sugeridas
              </Link>
            </div>
          </header>
          <p className="mt-4 max-w-[68ch] text-[14.5px] leading-relaxed text-ink-2">
            Lula venceu com 51,8% e a bolsa acionou o circuit breaker em 26/10. Das {n} empresas cobertas, avaliadas uma a uma com dados da CVM e da B3, ficam as{" "}
            <b className="font-semibold text-ink">{opps.length} de maior escore multifator</b> entre as que têm TIR de dono de pelo menos 20%, chance de pelo menos 45% no Monte Carlo e nenhum risco de
            insolvência pelo Altman.
          </p>
          <PicksTable picks={picks} reg={registro} />
        </div>
        <div className="lg:col-span-3">
          <KeyData items={keItems} reg={registro} rows={live} />
        </div>
      </section>

      <OppShowcase rows={live} ke={ke} opps={opps} external={external} headlines={headlines} reports={reports} names={names} />

      <section>
        <Hero rows={live} ke={ke} />
      </section>

      <Screener rows={live} ke={ke} opps={opps} />
    </div>
  );
}
