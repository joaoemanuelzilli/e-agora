"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ColumnChart, StackedColumns, type Col, type StackCol } from "@/components/charts/Bars";
import { CalendarHeatmap } from "@/components/charts/Calendar";
import { LineChart } from "@/components/charts/LineChart";
import { dateBR, isNum, mn, monthYear, mult, num, pct } from "@/lib/format";
import { useCompanyLive } from "./CompanyView";

const H0 = 2016;

function histProj(doc: any, hk: string, pk: string | null, opts: { scale?: number; from?: number } = {}): Col[] {
  const h = doc.history || {};
  const p = doc.projections || {};
  const sc = opts.scale ?? 1;
  const out: Col[] = [];
  (h.years || []).forEach((y: number, i: number) => {
    if (y < (opts.from ?? H0)) return;
    const v = h[hk]?.[i];
    out.push({ label: String(y), value: isNum(v) ? v * sc : null });
  });
  if (pk && p.years) {
    p.years.forEach((y: number, i: number) => {
      const v = p[pk]?.[i];
      out.push({ label: `${String(y).slice(2)}E`, value: isNum(v) ? v * sc : null, projected: true });
    });
  }
  return out;
}

function lineHP(doc: any, hk: string, pk: string | null, label: string, color: string) {
  const h = doc.history || {};
  const p = doc.projections || {};
  const data: [number, number][] = [];
  (h.years || []).forEach((y: number, i: number) => {
    const v = h[hk]?.[i];
    if (y >= H0 && isNum(v) && Math.abs(v) <= 1.5) data.push([y, v]);
  });
  const pdata: [number, number][] = [];
  if (pk && p.years) {
    if (data.length) pdata.push(data[data.length - 1]);
    p.years.forEach((y: number, i: number) => {
      const v = p[pk]?.[i];
      if (isNum(v) && Math.abs(v) <= 1.5) pdata.push([y, v]);
    });
  }
  return [
    { key: hk, label, color, data },
    ...(pdata.length > 1 ? [{ key: hk + "p", label: `${label} (projeção)`, color, data: pdata, dashed: true }] : []),
  ];
}

const tbl = (cols: Col[], name: string, f: (v: number) => string) => ({ columns: ["Ano", name], rows: cols.map((c) => [c.label, c.value === null ? "—" : f(c.value)]) });

export function Financials({ doc }: { doc: any }) {
  const { row } = useCompanyLive(doc);
  const fin = row.template === "financial";
  const hold = row.template === "holding";
  const rev = histProj(doc, "revenue", hold || fin ? null : "revenue");
  const ebitda = histProj(doc, "ebitda", hold || fin ? null : "ebitda");
  const ni = histProj(doc, "ni_controlling", hold ? null : "ni_controlling");
  const eq = histProj(doc, "equity_controlling", fin ? "equity" : null);
  const nde = histProj(doc, "nd_ebitda", hold || fin ? null : "nd_ebitda");
  const fcf = histProj(doc, "fcf", hold || fin ? null : "fcff");
  const q = doc.history?.quarterly || {};
  const qrev: Col[] = (q.periods || []).map((p: string, i: number) => ({ label: p, value: q.revenue?.[i] ?? null }));
  const qni: Col[] = (q.periods || []).map((p: string, i: number) => ({ label: p, value: q.ni_controlling?.[i] ?? null }));
  const margins = [...lineHP(doc, "ebitda_margin", fin || hold ? null : "margin", "Margem EBITDA", "var(--series-1)"), ...lineHP(doc, "net_margin", null, "Margem líquida", "var(--series-2)")];
  const returns = [...lineHP(doc, "roe", hold ? null : "roe", "ROE", "var(--series-1)"), ...(fin ? [] : lineHP(doc, "roic", hold ? null : "roic", "ROIC", "var(--series-2)"))];
  const g = doc.growth || {};
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {!fin && <ColumnChart title="Receita líquida" subtitle={`CAGR 5 anos ${pct(g.revenue_cagr_5y, 1)} · R$ mi`} data={rev} fmt="mn" table={tbl(rev, "Receita", mn)} />}
        {!fin && !hold && <ColumnChart title="EBITDA (IFRS-16)" subtitle={`CAGR 5 anos ${pct(g.ebitda_cagr_5y, 1)} · EBIT + D&A`} data={ebitda} fmt="mn" table={tbl(ebitda, "EBITDA", mn)} />}
        <ColumnChart title="Lucro líquido do controlador" subtitle={`CAGR 5 anos ${pct(g.ni_cagr_5y, 1)}`} data={ni} fmt="mn" table={tbl(ni, "Lucro", mn)} />
        {fin && <ColumnChart title="Patrimônio líquido" data={eq} fmt="mn" table={tbl(eq, "PL", mn)} />}
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {!fin && <LineChart title="Margens" series={margins} xType="linear" xFmt="year" yFmt="pct0" height={240} vmarks={[{ x: 2025.5, label: "projeção" }]} />}
        <LineChart title={fin ? "ROE" : "Retorno sobre capital"} series={returns} xType="linear" xFmt="year" yFmt="pct0" height={240} vmarks={[{ x: 2025.5, label: "projeção" }]} hlines={[{ y: 0.25, label: "Ke 25%" }]} />
      </div>
      {!fin && !hold && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          <ColumnChart title="Dívida líquida / EBITDA" subtitle="Inclui arrendamentos (IFRS-16)" data={nde} fmt="mult1" table={tbl(nde, "DL/EBITDA", (v) => mult(v))} />
          <ColumnChart title="Fluxo de caixa livre" subtitle="Realizado: FCO − capex (CVM). Projeção: FCFF do modelo." data={fcf} fmt="mn" table={tbl(fcf, "FCL", mn)} />
        </div>
      )}
      {qrev.length > 0 && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {!fin && <ColumnChart title="Receita por trimestre" data={qrev} fmt="mn" table={tbl(qrev, "Receita", mn)} />}
          <ColumnChart title="Lucro por trimestre" data={qni} fmt="mn" table={tbl(qni, "Lucro", mn)} />
        </div>
      )}
    </div>
  );
}

type Line = { label: string; key: string; f: (v: number) => string; hist?: string; pct?: boolean };

export function Projections({ doc }: { doc: any }) {
  const { row } = useCompanyLive(doc);
  const p = doc.projections;
  const rs = doc.research || {};
  if (!p) {
    return <div className="panel p-4 text-[13px] text-ink-2">Holding avaliada por soma das partes; ver seção Valuation.</div>;
  }
  const fin = row.template === "financial";
  const h = doc.history || {};
  const last = (k: string) => {
    const i = (h.years || []).indexOf(2025);
    return i >= 0 ? h[k]?.[i] : null;
  };
  const lines: Line[] = fin
    ? [
        { label: "Lucro líquido", key: "ni_controlling", f: mn, hist: "ni_controlling" },
        { label: "Crescimento do lucro", key: "growth", f: (v) => pct(v, 1, true) },
        { label: "ROE", key: "roe", f: (v) => pct(v, 1), hist: "roe" },
        { label: "Payout", key: "payout", f: (v) => pct(v, 0), hist: "payout" },
        { label: "Dividendos", key: "dividends", f: mn },
        { label: "Patrimônio líquido", key: "equity", f: mn, hist: "equity_controlling" },
      ]
    : [
        { label: "Receita líquida", key: "revenue", f: mn, hist: "revenue" },
        { label: "Crescimento", key: "growth", f: (v) => pct(v, 1, true) },
        { label: "EBITDA", key: "ebitda", f: mn, hist: "ebitda" },
        { label: "Margem EBITDA", key: "margin", f: (v) => pct(v, 1), hist: "ebitda_margin" },
        { label: "EBIT", key: "ebit", f: mn, hist: "ebit" },
        { label: "Resultado financeiro", key: "fin_result", f: mn, hist: "fin_result" },
        { label: "Lucro líquido", key: "ni_controlling", f: mn, hist: "ni_controlling" },
        { label: "ROE", key: "roe", f: (v) => pct(v, 1), hist: "roe" },
        { label: "ROIC", key: "roic", f: (v) => pct(v, 1), hist: "roic" },
        { label: "Capex", key: "capex", f: mn, hist: "capex" },
        { label: "FCFF", key: "fcff", f: mn },
        { label: "Dividendos", key: "dividends", f: mn },
        { label: "Dívida líquida", key: "net_debt", f: mn, hist: "net_debt" },
        { label: "DL/EBITDA", key: "nd_ebitda", f: (v) => mult(v), hist: "nd_ebitda" },
      ];
  const unit = row.per_unit || 1;
  const perShare: Line[] = [
    { label: "LPA", key: "eps", f: (v) => num(v * unit) },
    { label: "DPA", key: "dps", f: (v) => num(v * unit) },
  ];
  const pj = (fin ? rs.financial_projection || rs.projection : rs.projection || rs.financial_projection) || {};
  const drivers: [string, unknown][] = fin
    ? [
        ["ROE", pj.roe],
        ["Payout", pj.payout],
      ]
    : [
        ["Crescimento da receita", pj.revenue_growth],
        ["Margem EBITDA", pj.ebitda_margin],
        ["Capex / receita", pj.capex_pct_revenue],
        ["D&A / receita", pj.da_pct_revenue],
        ["Custo da dívida líquida", pj.cost_of_net_debt],
        ["Alíquota efetiva", pj.tax_rate],
        ["Payout", pj.payout],
      ];
  const term = rs.terminal || {};
  return (
    <div className="space-y-4">
      <div className="panel overflow-x-auto p-4">
        <table className="data min-w-[720px] text-[13px]">
          <thead>
            <tr>
              <th>R$ milhões</th>
              <th>2025</th>
              {p.years.map((y: number) => (
                <th key={y}>{y}E</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {lines.map((l) => (
              <tr key={l.key}>
                <td className="text-ink-2">{l.label}</td>
                <td className="text-muted">{l.hist && isNum(last(l.hist)) ? l.f(last(l.hist)) : "—"}</td>
                {(p[l.key] || []).map((v: number | null, i: number) => (
                  <td key={i}>{isNum(v) ? l.f(v) : "—"}</td>
                ))}
              </tr>
            ))}
            {perShare.map((l) => (
              <tr key={l.key}>
                <td className="text-ink-2">{l.label} (R$)</td>
                <td className="text-muted">—</td>
                {(p[l.key] || []).map((v: number | null, i: number) => (
                  <td key={i}>{isNum(v) ? l.f(v) : "—"}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="panel p-4">
          <div className="h3">Premissas (2026E–2030E)</div>
          <table className="data mt-2 text-[12.5px]">
            <tbody>
              {drivers.map(([k, v]) => (
                <tr key={k}>
                  <td className="text-ink-2">{k}</td>
                  <td>{Array.isArray(v) ? v.map((x) => (isNum(x) ? pct(x, 1) : "—")).join("  ") : isNum(v) ? pct(v as number, 1) : "—"}</td>
                </tr>
              ))}
              <tr>
                <td className="text-ink-2">Perpetuidade</td>
                <td>
                  g {pct(term.g, 1)}
                  {isNum(term.roic) ? `, ROIC ${pct(term.roic, 0)}` : ""}
                  {isNum(term.roe) ? `, ROE ${pct(term.roe, 0)}` : ""}
                </td>
              </tr>
              {!fin && isNum(pj.nwc_pct_revenue) && (
                <tr>
                  <td className="text-ink-2">Capital de giro / receita</td>
                  <td>{pct(pj.nwc_pct_revenue, 0)}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="panel p-4 text-[13px] leading-relaxed text-ink-2">
          <div className="h3 text-ink">Como as premissas se comparam ao histórico</div>
          <p className="mt-2">{rs.history_check?.notes || "—"}</p>
          {rs.guidance && (
            <p className="mt-2">
              <span className="font-medium text-ink">Guidance: </span>
              {rs.guidance}
            </p>
          )}
          {rs.overrides?.notes && rs.overrides.notes.length > 20 && (
            <p className="mt-2">
              <span className="font-medium text-ink">Ajustes à base CVM: </span>
              {rs.overrides.notes}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export function Dividends({ doc }: { doc: any }) {
  const { row, price } = useCompanyLive(doc);
  const dv = doc.dividendos as any;
  const p = doc.projections || {};
  const unit = row.per_unit || 1;
  const rs = doc.research || {};
  const annual = ((dv?.annual || []) as any[]).filter((a) => a.ano >= H0 && a.ano <= 2025);
  const stack: StackCol[] = [
    ...annual.map((a) => ({ label: String(a.ano), a: a.div, b: a.jcp })),
    ...((p.years || []) as number[]).map((y, i) => ({ label: `${String(y).slice(2)}E`, a: 0, b: 0, projected: isNum(p.dps?.[i]) ? p.dps[i] * unit : null })),
  ];
  const payout: Col[] = [
    ...((doc.market?.dps_history || []) as any[]).filter((d) => d.year >= H0).map((d) => ({ label: String(d.year), value: isNum(d.payout) && d.payout < 3 ? d.payout : null })),
    ...((p.years || []) as number[]).map((y, i) => ({ label: `${String(y).slice(2)}E`, value: isNum(p.payout?.[i]) ? p.payout[i] : null, projected: true })),
  ];
  const months = (dv?.months || []) as any[];
  const calRow = {
    id: row.ticker,
    label: "12 meses",
    cells: months.map((m) => (isNum(price) && m.valor ? m.valor / price : null)),
    detail: months.map((m) =>
      m.eventos?.length ? (
        <div className="mt-1 space-y-0.5 text-[11px] text-ink-2">
          {m.eventos.map((e: any, i: number) => (
            <div key={i}>
              {e.tipo} de R$ {num(e.valor, 4)}
            </div>
          ))}
        </div>
      ) : null,
    ),
    total: isNum(price) && dv?.ttm?.total ? pct(dv.ttm.total / price, 1) : "—",
  };
  const season: Col[] = (dv?.season_2021_2025 || []).map((x: number, i: number) => ({ label: ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"][i], value: x }));
  const events = ((dv?.eventos || []) as any[]).slice(-16).reverse();
  const up = (dv?.a_pagar || []) as any[];
  const dy = ((p.dps || []) as number[]).slice(0, 3).map((d) => (isNum(price) && price > 0 ? (d * unit) / price : null));
  const ttmDy = isNum(price) && dv?.ttm?.total ? dv.ttm.total / price : null;
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <StackedColumns
          title="Proventos por ação, por ano da data-com"
          subtitle="B3, valores brutos em base de ações atual. Projeção: payout × lucro."
          data={stack}
          labels={["Dividendos", "JCP", "Projeção"]}
          fmt="num2"
          table={{ columns: ["Ano", "Dividendos", "JCP", "Projeção"], rows: stack.map((c) => [c.label, num(c.a, 4), num(c.b, 4), c.projected == null ? "—" : num(c.projected, 4)]) }}
        />
        <ColumnChart title="Payout" subtitle="Realizado: dividendos pagos na DFC ÷ lucro (CVM)." data={payout} fmt="pct0" table={tbl(payout, "Payout", (v) => pct(v, 0))} />
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="panel p-4 lg:col-span-4">
          <div className="h3">Retorno em dividendos ao preço de agora</div>
          <div className="mt-3 grid grid-cols-2 gap-3">
            <div>
              <div className="label">Últimos 12 meses</div>
              <div className="num text-[20px] font-semibold">{pct(ttmDy, 1)}</div>
              <div className="text-[11.5px] text-muted">{dv?.ttm?.n ?? 0} pagamentos</div>
            </div>
            {["2026E", "2027E", "2028E"].map((y, i) => (
              <div key={y}>
                <div className="label">{y}</div>
                <div className="num text-[20px] font-semibold">{pct(dy[i], 1)}</div>
              </div>
            ))}
          </div>
          <div className="mt-3 border-t border-hairline pt-3 text-[12px] text-ink-2">
            ROE projetado: {((p.roe || []) as number[]).slice(0, 3).map((x) => pct(x, 0)).join(", ")}. Frequência: {num(dv?.freq_3y, 1)} pagamentos por ano. Parcela em JCP: {pct(dv?.jcp_share_3y, 0)}.
          </div>
        </div>
        <div className="space-y-4 lg:col-span-8">
          <CalendarHeatmap
            title="Calendário dos últimos 12 meses"
            subtitle="Yield de cada mês (data-com) sobre o preço de agora"
            cols={months.map((m) => monthYear(m.mes))}
            rows={[calRow]}
            scaleMax={0.03}
            fmt={(v) => pct(v, 2)}
            totalLabel="12 meses"
          />
          <ColumnChart title="Meses em que costuma pagar" subtitle="Fração dos proventos de 2021 a 2025 por mês da data-com" data={season} fmt="pct0" labelLast={false} height={170} />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
        <div className="panel overflow-x-auto p-4 lg:col-span-7">
          <div className="h3">Últimos proventos (B3)</div>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Data-com</th>
                <th>Pagamento</th>
                <th>Tipo</th>
                <th>R$ por ação</th>
                <th>Yield na data-com</th>
              </tr>
            </thead>
            <tbody>
              {events.map((e: any, i: number) => (
                <tr key={i}>
                  <td>{dateBR(e.dc)}</td>
                  <td>{e.pagamento ? dateBR(e.pagamento) : "—"}</td>
                  <td>{e.tipo}</td>
                  <td>{num(e.valor, 4)}</td>
                  <td>{isNum(e.yield_dc) ? pct(e.yield_dc, 2) : "—"}</td>
                </tr>
              ))}
              {events.length === 0 && (
                <tr>
                  <td colSpan={5} className="text-left text-muted">
                    Sem proventos em dinheiro desde 2016.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="space-y-4 lg:col-span-5">
          <div className="panel overflow-x-auto p-4">
            <div className="h3">Aprovados e ainda não pagos</div>
            {up.length ? (
              <table className="data mt-2 text-[12.5px]">
                <thead>
                  <tr>
                    <th>Pagamento</th>
                    <th>Data-com</th>
                    <th>R$ por ação</th>
                    <th>Quem compra hoje</th>
                  </tr>
                </thead>
                <tbody>
                  {up.map((u: any, i: number) => (
                    <tr key={i}>
                      <td>{u.pagamento ? dateBR(u.pagamento) : "a definir"}</td>
                      <td>{u.dc ? dateBR(u.dc) : "—"}</td>
                      <td>{num(u.valor, 4)}</td>
                      <td className={u.da_direito_hoje ? "pos font-medium" : "text-muted"}>{u.da_direito_hoje ? "ainda recebe" : "não recebe"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p className="mt-2 text-[12.5px] text-muted">Nenhum pagamento aprovado a cair.</p>
            )}
          </div>
          <div className="panel p-4 text-[13px] leading-relaxed text-ink-2">
            <div className="h3 text-ink">Política de proventos</div>
            <p className="mt-2">{rs.dividend_policy || "—"}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
