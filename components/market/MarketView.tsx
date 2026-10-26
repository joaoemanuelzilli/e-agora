"use client";
import { LineChart } from "@/components/charts/LineChart";
import { Histogram, Scatter } from "@/components/charts/Points";
import { num, pct, signClass } from "@/lib/format";
import { useMarket } from "@/lib/live";
import type { MarketStats, XSec } from "@/lib/types";

const COEF: Record<string, string> = {
  const: "Constante",
  beta: "Beta de baixa (3 anos)",
  lev_c: "Dívida líquida / EBITDA",
  log_mcap: "Porte (log do valor de mercado)",
  exporter: "Exportadora (dummy)",
  financial: "Financeiro (dummy)",
  state: "Estatal (dummy)",
  utility: "Utilidade pública (dummy)",
  consumo: "Consumo cíclico (dummy)",
};

function median(a: number[]) {
  const s = [...a].sort((x, y) => x - y);
  const m = Math.floor(s.length / 2);
  return s.length ? (s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2) : NaN;
}

export function DiCurve() {
  const m = useMarket(60000);
  const di = (m?.di || []).filter((d) => d.rate);
  const yr = (code: string) => 2000 + Number(code.slice(-2));
  const now: [number, number][] = di.map((d) => [yr(d.code), (d.rate as number) / 100]);
  const prev: [number, number][] = di.map((d) => [yr(d.code), (d.rate as number) / (1 + (d.chg ?? 0)) / 100]);
  if (!now.length) return <div className="panel p-4 text-[13px] text-muted">Carregando a curva de juros da B3…</div>;
  return (
    <LineChart
      title="Curva de juros futuros (DI1), ao vivo"
      subtitle="Taxa por vencimento em janeiro de cada ano. A curva longa subiu cerca de 3 p.p. em um dia."
      series={[
        { key: "now", label: "Hoje", color: "var(--series-1)", data: now, endLabel: true },
        { key: "prev", label: "Sexta (23/10)", color: "var(--deemph)", data: prev, dashed: true },
      ]}
      legend={[
        { label: "Hoje", color: "var(--series-1)", kind: "line" },
        { label: "Sexta (23/10)", color: "var(--ink-2)", kind: "line", dashed: true },
      ]}
      xType="linear"
      xFmt="year"
      yFmt="pct1"
      height={250}
      table={{ columns: ["Vencimento", "Hoje", "Sexta"], rows: now.map((d, i) => [`jan/${String(d[0]).slice(2)}`, pct(d[1], 2), pct(prev[i][1], 2)]) }}
    />
  );
}

export function MarketView({ market, xsec, sectors }: { market: MarketStats; xsec: XSec; sectors: Record<string, { setor?: string }> }) {
  const live = useMarket(60000);
  const today = live?.indices?.IBOV?.chg ?? market.ibov_today.chg ?? null;
  const hist = market.ibov_return_hist;
  const paths = market.crash_paths || [];
  const L = Math.min(252, ...paths.map((p) => p.path.length - 1));
  const med: [number, number][] = Array.from({ length: L + 1 }, (_, i) => [i, median(paths.map((p) => p.path[i]))]);
  const ep = market.election_paths || [];
  const lulaColors: Record<string, string> = { "2002-10-28": "var(--series-1)", "2006-10-30": "var(--series-2)", "2022-10-31": "var(--series-3)" };
  const elSeries = ep
    .filter((e) => e.path)
    .map((e) => ({
      key: e.date,
      label: `${e.label} (${e.date.slice(0, 4)})`,
      color: lulaColors[e.date] || "var(--deemph)",
      data: (e.path as number[]).map((v, i) => [i, v] as [number, number]),
      muted: !lulaColors[e.date],
      width: lulaColors[e.date] ? 2 : 1.25,
    }));
  const ibw = market.ibov_weekly.map(([d, v]) => [Date.parse(d), v] as [number, number]);
  const ibNow = live?.indices?.IBOV?.price ?? market.ibov_today.price;
  if (ibNow) ibw.push([Date.parse("2026-10-26"), ibNow]);
  const fwd = market.crash_forward_stats;
  return (
    <div className="space-y-8">
      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <Histogram
            title="Retornos diários do Ibovespa desde 1998"
            subtitle={`${market.ibov_daily_return_stats.n.toLocaleString("pt-BR")} pregões. Desvio-padrão diário ${pct(market.ibov_daily_return_stats.std, 2)}. Hoje: ${num(today !== null ? (today - market.ibov_daily_return_stats.mean) / market.ibov_daily_return_stats.std : null, 1)} desvios-padrão.`}
            counts={hist.counts}
            edges={hist.edges}
            price={today}
            fair={null}
            fmt="pct0"
            priceLabel={`hoje ${pct(today, 1)}`}
            legendItems={null}
            aboveColor="var(--series-1)"
          />
        </div>
        <div className="panel overflow-x-auto p-4 lg:col-span-5">
          <div className="h3">Os piores dias desde 1998 e o que veio depois</div>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Data</th>
                <th>Dia</th>
                <th>1 mês</th>
                <th>3 meses</th>
                <th>12 meses</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="font-semibold">26/10/2026</td>
                <td className="neg font-semibold">{pct(today, 1)}</td>
                <td colSpan={3} className="text-muted">hoje</td>
              </tr>
              {market.worst_days.slice(0, 12).map((d) => (
                <tr key={d.date}>
                  <td>{d.date.split("-").reverse().join("/")}</td>
                  <td className="neg">{pct(d.ret, 1)}</td>
                  <td className={signClass(d.f1m)}>{pct(d.f1m, 0, true)}</td>
                  <td className={signClass(d.f3m)}>{pct(d.f3m, 0, true)}</td>
                  <td className={signClass(d.f12m)}>{pct(d.f12m, 0, true)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <LineChart
            title="Ibovespa depois de cada crash (dias com queda de 7% ou mais)"
            subtitle={`${paths.length} episódios desde 1998, base 100 no fechamento do dia do choque. Linha azul: mediana.`}
            series={[
              ...paths.map((p) => ({ key: p.date, label: p.date, color: "var(--deemph)", data: p.path.slice(0, L + 1).map((v, i) => [i, v] as [number, number]), muted: true })),
              { key: "med", label: "Mediana dos episódios", color: "var(--series-1)", data: med, width: 2.5, endLabel: true },
            ]}
            legend={[
              { label: "Mediana dos episódios", color: "var(--series-1)", kind: "line" },
              { label: "Cada episódio", color: "var(--deemph)", kind: "line" },
            ]}
            xType="linear"
            xFmt={(v) => `${Math.round(v)}d`}
            yFmt="num0"
            hlines={[{ y: 100, label: "base 100" }]}
            height={300}
            table={{ columns: ["Episódio", "Queda no dia", "+63 pregões", "+252 pregões"], rows: paths.map((p) => [p.date, pct(p.ret, 1), num(p.path[63], 0), num(p.path[Math.min(252, p.path.length - 1)], 0)]) }}
          />
        </div>
        <div className="panel p-4 lg:col-span-5">
          <div className="h3">Retorno do Ibovespa após dias de queda de 5% ou mais</div>
          <table className="data mt-2 text-[13px]">
            <thead>
              <tr>
                <th>Horizonte</th>
                <th>Mediana</th>
                <th>Média</th>
                <th>% positivos</th>
                <th>p10</th>
                <th>p90</th>
              </tr>
            </thead>
            <tbody>
              {(["f1m", "f3m", "f6m", "f12m"] as const).map((k) => (
                <tr key={k}>
                  <td>{{ f1m: "1 mês", f3m: "3 meses", f6m: "6 meses", f12m: "12 meses" }[k]}</td>
                  <td className={signClass(fwd[k].median)}>{pct(fwd[k].median, 0, true)}</td>
                  <td>{pct(fwd[k].mean, 0, true)}</td>
                  <td>{pct(fwd[k].pct_pos, 0)}</td>
                  <td className={signClass(fwd[k].p10)}>{pct(fwd[k].p10, 0, true)}</td>
                  <td className={signClass(fwd[k].p90)}>{pct(fwd[k].p90, 0, true)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="mt-3 text-[12px] leading-relaxed text-muted">
            {fwd.f12m.n} pregões de queda ≥ 5% (muitos agrupados em 1998, 2008 e 2020; as janelas se sobrepõem, então a amostra efetiva é menor). Em 2008 a recuperação levou anos: a mediana esconde caudas longas.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <LineChart
            title="Ibovespa no ano seguinte a cada eleição presidencial"
            subtitle="Base 100 no último fechamento antes do resultado. Em cor, as três vitórias de Lula."
            series={elSeries}
            legend={elSeries.filter((s) => !s.muted).map((s) => ({ label: s.label, color: s.color, kind: "line" as const })).concat([{ label: "Outras eleições", color: "var(--deemph)", kind: "line" as const }])}
            xType="linear"
            xFmt={(v) => `${Math.round(v)}d`}
            yFmt="num0"
            hlines={[{ y: 100, label: "base 100" }]}
            height={300}
          />
        </div>
        <div className="panel overflow-x-auto p-4 lg:col-span-5">
          <div className="h3">Reação do Ibovespa a cada eleição</div>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Resultado</th>
                <th>Dia seguinte</th>
                <th>3 meses</th>
                <th>12 meses</th>
              </tr>
            </thead>
            <tbody>
              {market.elections.map((e) => (
                <tr key={e.date}>
                  <td>
                    {e.label} <span className="text-muted">({e.date.slice(0, 4)})</span>
                  </td>
                  <td className={signClass(e.ret_d1)}>{pct(e.ret_d1, 1, true)}</td>
                  <td className={signClass(e.f3m)}>{pct(e.f3m, 0, true)}</td>
                  <td className={signClass(e.f12m)}>{pct(e.f12m, 0, true)}</td>
                </tr>
              ))}
              <tr>
                <td className="font-semibold">Lula reeleito (2026)</td>
                <td className={`font-semibold ${signClass(today)}`}>{pct(today, 1, true)}</td>
                <td>—</td>
                <td>—</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <Scatter
            title="Beta de baixa explica a maior parte da queda"
            subtitle={`Cada ponto é uma ação do universo IBOV + IBrX-100 + SMLL. Só o beta: R² = ${pct(xsec.r2_beta_only, 0)}.`}
            points={xsec.points.map((p) => ({ id: p.ticker, x: p.predicted, y: p.actual, highlight: true, sub: sectors[p.ticker]?.setor }))}
            xFmt="pct0s"
            yFmt="pct0s"
            xLabel="Queda prevista (fatores)"
            yLabel="Queda observada"
            diagonal
            height={330}
          />
        </div>
        <div className="panel overflow-x-auto p-4 lg:col-span-5">
          <div className="h3">Regressão cross-section da queda de hoje</div>
          <div className="mt-1 text-[12px] text-muted">
            {xsec.n} ações; R² = {pct(xsec.r2, 1)}. Coeficientes em pontos percentuais de retorno.
          </div>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Variável</th>
                <th>Coeficiente</th>
                <th>Estatística t</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(xsec.coef).map(([k, v]) => (
                <tr key={k}>
                  <td>{COEF[k] || k}</td>
                  <td className={signClass(v)}>{pct(v, 1, true)}</td>
                  <td className={Math.abs(xsec.t[k]) >= 2 ? "font-semibold" : "text-muted"}>{num(xsec.t[k], 1)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="mt-3 text-[12px] leading-relaxed text-muted">
            |t| ≥ 2 em negrito. Cada ponto de beta tirou cerca de {pct(Math.abs(xsec.coef.beta), 0)} do preço; cada volta de dívida/EBITDA, {pct(Math.abs(xsec.coef.lev_c), 1)}. Ser estatal não foi significativo depois de controlar pelo beta.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <LineChart
            title="Ibovespa desde 1998 (semanal, nominal)"
            series={[{ key: "ib", label: "Ibovespa", color: "var(--series-1)", data: ibw, endLabel: true, area: true }]}
            vmarks={[
              { x: Date.parse("2002-10-28"), label: "Lula 2002" },
              { x: Date.parse("2008-10-15"), label: "2008" },
              { x: Date.parse("2020-03-12"), label: "Covid" },
            ]}
            yFmt="num0"
            height={280}
          />
        </div>
        <div className="lg:col-span-5">
          <DiCurve />
        </div>
      </section>

      <section className="panel overflow-x-auto p-4">
        <div className="h3">Quedas de 25% ou mais do Ibovespa e a recuperação</div>
        <table className="data mt-2 text-[12.5px]">
          <thead>
            <tr>
              <th>Pico</th>
              <th>Fundo</th>
              <th>Queda</th>
              <th>Recuperou em</th>
              <th>Dias até recuperar</th>
              <th>12 meses após o fundo</th>
            </tr>
          </thead>
          <tbody>
            {market.drawdowns_25.map((d) => (
              <tr key={d.peak}>
                <td>{d.peak.split("-").reverse().join("/")}</td>
                <td>{d.trough.split("-").reverse().join("/")}</td>
                <td className="neg">{pct(d.depth, 0)}</td>
                <td>{d.recovered.split("-").reverse().join("/")}</td>
                <td>{d.days_to_recover.toLocaleString("pt-BR")}</td>
                <td className={signClass(d.fwd12m_from_trough)}>{pct(d.fwd12m_from_trough, 0, true)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
