"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { ColumnChart, type Col } from "@/components/charts/Bars";
import { LineChart } from "@/components/charts/LineChart";
import { isNum, mn, mult, num, pct } from "@/lib/format";
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
  const dh = (doc.market?.dps_history || []) as any[];
  const p = doc.projections || {};
  const unit = row.per_unit || 1;
  const cols: Col[] = [
    ...dh.filter((d) => d.year >= H0).map((d) => ({ label: String(d.year), value: isNum(d.dps_adj) ? d.dps_adj * unit : null })),
    ...((p.years || []) as number[]).map((y, i) => ({ label: `${String(y).slice(2)}E`, value: isNum(p.dps?.[i]) ? p.dps[i] * unit : null, projected: true })),
  ];
  const payout: Col[] = [
    ...dh.filter((d) => d.year >= H0).map((d) => ({ label: String(d.year), value: isNum(d.payout) && d.payout < 3 ? d.payout : null })),
    ...((p.years || []) as number[]).map((y, i) => ({ label: `${String(y).slice(2)}E`, value: isNum(p.payout?.[i]) ? p.payout[i] : null, projected: true })),
  ];
  const b3 = (doc.market?.dividends_b3 || []) as any[];
  const dy = ((p.dps || []) as number[]).slice(0, 3).map((d) => (isNum(price) && price > 0 ? (d * unit) / price : null));
  const rs = doc.research || {};
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ColumnChart
          title="Dividendos + JCP por ação"
          subtitle="Realizado: caixa pago na DFC ÷ ações (base atual). Projeção: payout × lucro."
          data={cols}
          fmt="num2"
          table={tbl(cols, "R$ por ação", (v) => num(v))}
        />
        <ColumnChart title="Payout" data={payout} fmt="pct0" table={tbl(payout, "Payout", (v) => pct(v, 0))} />
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="panel p-4">
          <div className="h3">Retorno em dividendos ao preço de hoje</div>
          <div className="mt-3 grid grid-cols-3 gap-2">
            {["2026E", "2027E", "2028E"].map((y, i) => (
              <div key={y}>
                <div className="label">{y}</div>
                <div className="num text-[18px] font-semibold">{pct(dy[i], 1)}</div>
              </div>
            ))}
          </div>
          <div className="mt-3 text-[12px] text-muted">ROE projetado: {((p.roe || []) as number[]).slice(0, 3).map((x) => pct(x, 0)).join(", ")}</div>
        </div>
        <div className="panel p-4 text-[13px] leading-relaxed text-ink-2 lg:col-span-2">
          <div className="h3 text-ink">Política de proventos</div>
          <p className="mt-2">{rs.dividend_policy || "—"}</p>
        </div>
      </div>
      {b3.length > 0 && (
        <div className="panel overflow-x-auto p-4">
          <div className="h3">Proventos dos últimos 12 meses (B3)</div>
          <table className="data mt-2 text-[12.5px]">
            <thead>
              <tr>
                <th>Data-com</th>
                <th>Pagamento</th>
                <th>Tipo</th>
                <th>Referência</th>
                <th>R$ por ação</th>
              </tr>
            </thead>
            <tbody>
              {b3.map((d, i) => (
                <tr key={i}>
                  <td>{d.data_com}</td>
                  <td>{d.pagamento || "—"}</td>
                  <td>{d.tipo === "JRS CAP PROPRIO" ? "JCP" : d.tipo === "DIVIDENDO" ? "Dividendo" : d.tipo}</td>
                  <td>{d.ref || "—"}</td>
                  <td>{num(d.valor, 4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
