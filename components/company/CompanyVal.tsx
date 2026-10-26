"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ColumnChart, HBarChart, Waterfall } from "@/components/charts/Bars";
import { LineChart } from "@/components/charts/LineChart";
import { Heatmap, Histogram } from "@/components/charts/Points";
import { brl, isNum, mn, mult, num, pct, signClass } from "@/lib/format";
import { probAbove } from "@/lib/valuation";
import { useCompanyLive } from "./CompanyView";

const METHOD_LABEL: Record<string, string> = {
  dcf: "DCF (FCFF descontado ao WACC)",
  ddm: "DDM (dividendos + perpetuidade a Ke)",
  pe: "P/L alvo × LPA 2027E",
  ev_ebitda: "EV/EBITDA alvo × EBITDA 2027E",
  pbv: "P/VP alvo × VPA 2026E",
  multiples: "Múltiplos (média)",
  graham: "Graham √(22,5 × LPA × VPA)",
  bazin: "Bazin (DPA 2027E ÷ 6%)",
  sotp: "Soma das partes (valor justo)",
  nav_market: "Soma das partes a mercado",
};

function MultiplesHistory({ doc }: { doc: any }) {
  const mh = doc.market?.multiples_history;
  if (!mh?.series?.length) return null;
  const keys = (doc.row.template === "financial" ? ["pe", "pbv"] : ["pe", "ev_ebitda", "pbv"]) as string[];
  const names: Record<string, string> = { pe: "P/L (12 meses)", ev_ebitda: "EV/EBITDA (12 meses)", pbv: "P/VP" };
  return (
    <div className={`grid grid-cols-1 gap-4 ${keys.length === 3 ? "lg:grid-cols-3" : "lg:grid-cols-2"}`}>
      {keys.map((k) => {
        const st = mh.stats?.[`${k}_all`];
        const lim = k === "pbv" ? 30 : 80;
        const data: [number, number][] = mh.series.filter((r: any) => isNum(r[k]) && r[k] > 0 && r[k] < lim).map((r: any) => [Date.parse(r.date), r[k]]);
        if (data.length < 6) return null;
        const cur = mh.series[mh.series.length - 1];
        return (
          <LineChart
            key={k}
            title={names[k]}
            subtitle={st ? `Média ${num(st.mean, 1)}x, hoje ${num(st.current, 1)}x (z = ${num(st.z, 1)}; percentil ${pct(st.pctile, 0)})` : undefined}
            series={[{ key: k, label: names[k], color: "var(--series-1)", data, endLabel: !!cur?.live }]}
            bands={st ? [{ lo: Math.max(0, st.mean - st.std), hi: st.mean + st.std }] : []}
            hlines={st ? [{ y: st.mean, label: "média" }] : []}
            yFmt="num1"
            xFmt="date"
            height={210}
            table={{ columns: ["Mês", names[k]], rows: data.filter((_, i) => i % 6 === 0).map((d) => [new Date(d[0]).toISOString().slice(0, 7), num(d[1], 1)]) }}
          />
        );
      })}
    </div>
  );
}

export function Valuation({ doc }: { doc: any }) {
  const { row, price, L, ke } = useCompanyLive(doc);
  const v = doc.valuation || {};
  if (!doc.valuation) return <div className="panel p-4 text-[13px]">Modelo indisponível.</div>;
  const hold = row.template === "holding";
  const unit = row.per_unit || 1;
  const vals = v.values || {};
  const w = v.weights || {};
  const methods = Object.keys(METHOD_LABEL).filter((k) => isNum(vals[k]));
  const d = v.dcf || {};
  const e = row.engine || {};
  const sens = v.sensitivity;
  const mc = v.monte_carlo;
  const sc = v.scenarios;
  const nShares = e.n_sh || doc.profile?.shares?.outstanding / 1e6;
  const bridge =
    !hold && row.template !== "financial" && isNum(d.ev)
      ? [
          { label: "VP dos fluxos 2026–30", value: d.pv_explicit },
          { label: "VP da perpetuidade", value: d.pv_tv },
          { label: "Valor da firma", value: d.ev, total: true },
          { label: "Dívida líquida", value: -(e.nd_base ?? 0) },
          { label: "Minoritários", value: -(d.minority_value ?? 0) },
          { label: "Ajustes", value: (d.equity ?? 0) - ((d.ev ?? 0) - (e.nd_base ?? 0) - (d.minority_value ?? 0)) },
          { label: "Valor do equity", value: d.equity, total: true },
        ]
      : null;
  const probLive = mc ? probAbove(row.mc_q, price) : null;
  const rd = v.reverse_dcf;
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="panel overflow-x-auto p-4 lg:col-span-5">
          <div className="h3">Métodos</div>
          <table className="data mt-2 text-[13px]">
            <thead>
              <tr>
                <th>Método</th>
                <th>R$</th>
                <th>Peso</th>
                <th>vs preço</th>
              </tr>
            </thead>
            <tbody>
              {methods.map((k) => (
                <tr key={k}>
                  <td className={w[k] ? "" : "text-muted"}>{METHOD_LABEL[k]}</td>
                  <td>{num(vals[k])}</td>
                  <td>{w[k] ? pct(w[k], 0) : "ref."}</td>
                  <td className={signClass(isNum(price) ? vals[k] / price - 1 : null)}>{isNum(price) ? pct(vals[k] / price - 1, 0, true) : "—"}</td>
                </tr>
              ))}
              <tr>
                <td className="font-semibold">Valor justo (Ke {Math.round(ke * 100)}%)</td>
                <td className="font-semibold">{num(L.fair)}</td>
                <td />
                <td className={`font-semibold ${signClass(L.upside)}`}>{pct(L.upside, 0, true)}</td>
              </tr>
            </tbody>
          </table>
          {!hold && (
            <div className="mt-3 grid grid-cols-2 gap-3 border-t border-hairline pt-3 text-[12.5px]">
              {isNum(d.wacc) && (
                <div>
                  <div className="label">WACC</div>
                  <div className="num font-semibold">
                    {pct(d.wacc, 1)} <span className="font-normal text-muted">(Kd {pct(d.kd, 1)}, peso dívida {pct(d.wd, 0)})</span>
                  </div>
                </div>
              )}
              <div>
                <div className="label">Perpetuidade</div>
                <div className="num font-semibold">
                  g {pct(v.g, 1)}
                  {isNum(d.roic_T) ? <span className="font-normal text-muted">, ROIC {pct(d.roic_T, 0)}</span> : null}
                  {row.template === "financial" && isNum(v.roe_T) ? <span className="font-normal text-muted">, ROE {pct(v.roe_T, 0)}</span> : null}
                </div>
              </div>
              {isNum(d.tv_share) && (
                <div>
                  <div className="label">Perpetuidade no valor da firma</div>
                  <div className="num font-semibold">{pct(d.tv_share, 0)}</div>
                </div>
              )}
              {isNum(d.implied_exit_ev_ebitda) && (
                <div>
                  <div className="label">EV/EBITDA implícito na saída</div>
                  <div className="num font-semibold">{mult(d.implied_exit_ev_ebitda)}</div>
                </div>
              )}
              {isNum(v.justified_pbv) && (
                <div>
                  <div className="label">P/VP justo (ROE − g)/(Ke − g)</div>
                  <div className="num font-semibold">{mult(v.justified_pbv, 2)}</div>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="lg:col-span-7">
          {bridge ? (
            <Waterfall
              title="Do fluxo de caixa ao valor do equity (DCF)"
              subtitle={`R$ milhões. Por ação: ${brl(isNum(d.equity) && nShares ? (d.equity / nShares) * unit : null)}`}
              steps={bridge}
              fmt="mn"
              table={{ columns: ["Etapa", "R$ mi"], rows: bridge.map((b) => [b.label, mn(b.value)]) }}
            />
          ) : hold && v.components ? (
            <div className="panel overflow-x-auto p-4">
              <div className="h3">Soma das partes</div>
              <table className="data mt-2 text-[12.5px]">
                <thead>
                  <tr>
                    <th>Ativo</th>
                    <th>Participação</th>
                    <th>Método</th>
                    <th>Valor justo (100%)</th>
                    <th>Mercado (100%)</th>
                    <th>Contribuição justa</th>
                  </tr>
                </thead>
                <tbody>
                  {v.components.map((c: any) => (
                    <tr key={c.name}>
                      <td>{c.name}</td>
                      <td>{pct(c.stake, 1)}</td>
                      <td>{c.method === "fair" ? "valor justo" : c.method === "market" ? "mercado" : "fixo"}</td>
                      <td>{mn(c.value_fair_100)}</td>
                      <td>{mn(c.value_mkt_100)}</td>
                      <td>{mn(c.contrib_fair)}</td>
                    </tr>
                  ))}
                  <tr>
                    <td className="text-ink-2">Dívida líquida da holding</td>
                    <td colSpan={4} />
                    <td>{mn(-v.holding_net_debt)}</td>
                  </tr>
                  <tr>
                    <td className="text-ink-2">Custo de holding capitalizado</td>
                    <td colSpan={4} />
                    <td>{mn(-v.holding_cost_capitalized)}</td>
                  </tr>
                </tbody>
              </table>
              <div className="mt-3 text-[12.5px] text-ink-2">
                Desconto do preço sobre o NAV a mercado: <span className="num font-semibold text-ink">{pct(v.discount_to_nav_mkt, 0)}</span>
              </div>
            </div>
          ) : (
            <ColumnChart
              title="Dividendos projetados (valor presente)"
              data={((doc.projections?.dps || []) as number[]).map((x, i) => ({ label: `${2026 + i}E`, value: x * unit }))}
              fmt="num2"
            />
          )}
        </div>
      </div>
      {sens && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <Heatmap
            title="Sensibilidade: Ke × crescimento na perpetuidade"
            subtitle="Valor justo (R$). Azul acima do preço atual, vermelho abaixo; contorno no caso-base."
            rows={sens.ke_axis.map((k: number) => pct(k, 1))}
            cols={sens.g_axis.map((g: number) => pct(g, 1))}
            values={sens.ke_g}
            price={price}
            fmt="num2"
            rowLabel="Ke"
            colLabel="g"
            baseCell={[2, 2]}
            table={{ columns: ["Ke \\ g", ...sens.g_axis.map((g: number) => pct(g, 1))], rows: sens.ke_g.map((r: number[], i: number) => [pct(sens.ke_axis[i], 1), ...r.map((x) => num(x))]) }}
          />
          <Heatmap
            title="Sensibilidade: crescimento × margem"
            subtitle="Deslocamentos aplicados a todos os anos projetados (p.p.)"
            rows={sens.growth_shift_axis.map((g: number) => `${g > 0 ? "+" : ""}${Math.round(g * 100)} p.p.`)}
            cols={sens.margin_shift_axis.map((m: number) => `${m > 0 ? "+" : ""}${(m * 100).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} p.p.`)}
            values={sens.growth_margin}
            price={price}
            fmt="num2"
            rowLabel="Crescimento"
            colLabel={row.template === "financial" ? "ROE" : "Margem EBITDA"}
            baseCell={[2, 2]}
          />
        </div>
      )}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        {sc?.bear && (
          <div className="lg:col-span-5">
            <ColumnChart
              title="Cenários"
              subtitle={`Probabilidades: pessimista ${pct(sc.bear.probability, 0)}, base ${pct(sc.base?.probability, 0)}, otimista ${pct(sc.bull.probability, 0)}`}
              data={[
                { label: "Pessimista", value: sc.bear.fair_value, note: sc.bear.narrative || undefined },
                { label: "Base", value: L.fair ?? sc.base?.fair_value },
                { label: "Otimista", value: sc.bull.fair_value, note: sc.bull.narrative || undefined },
                { label: "Esperado", value: sc.expected_fair_value },
              ]}
              fmt="num2"
              labelLast={false}
              refLine={isNum(price) ? { y: price, label: `preço ${num(price)}` } : undefined}
            />
            <div className="mt-2 space-y-1 text-[12px] text-ink-2">
              {sc.bear.narrative && (
                <p>
                  <span className="font-medium text-ink">Pessimista: </span>
                  {sc.bear.narrative}
                </p>
              )}
              {sc.bull.narrative && (
                <p>
                  <span className="font-medium text-ink">Otimista: </span>
                  {sc.bull.narrative}
                </p>
              )}
            </div>
          </div>
        )}
        {mc && (
          <div className="lg:col-span-7">
            <Histogram
              title="Monte Carlo: distribuição do valor justo"
              subtitle={`${mc.n.toLocaleString("pt-BR")} cenários sorteando crescimento (σ ${pct(mc.params.revenue_growth_sd, 1)}), margem (σ ${pct(mc.params.ebitda_margin_sd, 1)}), capex e perpetuidade. p10 ${num(mc.p10)}, mediana ${num(mc.p50)}, p90 ${num(mc.p90)}.`}
              counts={mc.hist.counts}
              edges={mc.hist.edges}
              price={price}
              fair={L.fair}
              prob={probLive}
              fmt="num2"
              table={{ columns: ["Faixa", "Frequência"], rows: mc.hist.counts.map((c: number, i: number) => [`${num(mc.hist.edges[i])}–${num(mc.hist.edges[i + 1])}`, c]) }}
            />
          </div>
        )}
      </div>
      {rd && !rd.bounded && isNum(rd.implied_avg_growth) && (
        <div className="panel p-4 text-[13.5px]">
          <span className="font-semibold">DCF reverso. </span>
          {row.template === "financial"
            ? `Para valer o preço de hoje a Ke ${Math.round(ke * 100)}%, o banco precisaria de ROE médio de ${pct(rd.implied_avg_growth, 1)} (premissa: ${pct(rd.base_avg_growth, 1)}).`
            : `Para valer o preço de hoje a Ke ${Math.round(ke * 100)}%, a receita teria de crescer ${pct(rd.implied_avg_growth, 1)} ao ano em média até 2030 (premissa: ${pct(rd.base_avg_growth, 1)}).`}
        </div>
      )}
      <MultiplesHistory doc={doc} />
    </div>
  );
}

const FACTOR: Record<string, string> = {
  valor: "Valor (TIR de dono)",
  upside: "Upside",
  qualidade: "Qualidade (ROE 5 anos, Piotroski)",
  solidez: "Solidez (dívida, Altman)",
  sobrerreacao: "Sobrerreação (resíduo da queda)",
  probabilidade: "Probabilidade (Monte Carlo)",
  momentum: "Momentum (12 meses até a eleição)",
};

export function Quant({ doc }: { doc: any }) {
  const { row } = useCompanyLive(doc);
  const sc = row.scores || {};
  const items = Object.keys(FACTOR)
    .filter((k) => isNum(sc[k]))
    .map((k) => ({ label: FACTOR[k], value: sc[k] as number }));
  const pz = doc.quant?.piotroski;
  const az = doc.quant?.altman;
  const st = doc.market?.stats || {};
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <div className="lg:col-span-5">
        <HBarChart
          title={`Escore multifator: ${row.rank ? `${row.rank}º de 59` : "—"}`}
          subtitle="Desvios-padrão em relação à cobertura (z). Pesos: valor 30%, qualidade 20%, solidez 15%, probabilidade 15%, upside 10%, sobrerreação 10%."
          items={items}
          fmt="num1"
          rowH={32}
          domain={[-3, 3]}
          table={{ columns: ["Fator", "z"], rows: items.map((i) => [i.label, num(i.value, 2)]) }}
        />
      </div>
      <div className="panel p-4 lg:col-span-4">
        <div className="h3">Piotroski F-score {pz ? `${pz.score}/9` : "—"}</div>
        {pz ? (
          <ul className="mt-2 space-y-1 text-[12.5px]">
            {Object.entries(pz.signals as Record<string, boolean>).map(([k, ok]) => (
              <li key={k} className="flex items-center gap-2">
                <span className={`inline-flex h-4 w-4 items-center justify-center rounded-full text-[10px] font-bold text-white ${ok ? "bg-[var(--good)]" : "bg-[var(--critical)]"}`} aria-hidden>
                  {ok ? "✓" : "×"}
                </span>
                <span className={ok ? "text-ink" : "text-ink-2"}>{k}</span>
                <span className="sr-only">{ok ? "atende" : "não atende"}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-[12.5px] text-muted">Não se aplica a bancos.</p>
        )}
      </div>
      <div className="panel space-y-3 p-4 text-[12.5px] lg:col-span-3">
        <div>
          <div className="label">Altman Z″ (emergentes)</div>
          <div className="num text-[18px] font-semibold">{az ? num(az.z, 2) : "—"}</div>
          {az && <div className="text-muted">zona {az.zone} (segura acima de 5,85; risco abaixo de 4,35)</div>}
        </div>
        <div>
          <div className="label">Cobertura de juros (EBIT ÷ despesa financeira)</div>
          <div className="num text-[18px] font-semibold">{mult(doc.quant?.interest_cov)}</div>
        </div>
        <div>
          <div className="label">Beta de baixa (3 anos) e em crises</div>
          <div className="num text-[18px] font-semibold">
            {num(st.beta_down_3y, 2)}{" "}
            <span className="text-[13px] font-normal text-muted" title={st.beta_crash_10y_raw != null ? `bruto ${num(st.beta_crash_10y_raw, 2)}, encolhido em direção ao beta de baixa` : undefined}>
              / {num(st.beta_crash_10y, 2)}
              {st.n_crash_days ? ` em ${st.n_crash_days} dias de crash` : ""}
            </span>
          </div>
        </div>
        <div>
          <div className="label">Momentum 12–1 meses (pré-eleição)</div>
          <div className={`num text-[18px] font-semibold ${signClass(st.mom_12_1)}`}>{pct(st.mom_12_1, 0, true)}</div>
        </div>
      </div>
    </div>
  );
}
