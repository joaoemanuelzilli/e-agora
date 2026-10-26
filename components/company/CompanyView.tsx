"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import Link from "next/link";
import { HBarChart } from "@/components/charts/Bars";
import { LineChart } from "@/components/charts/LineChart";
import { FootballField, IrrMeter } from "@/components/charts/Points";
import { brl, isNum, mult, num, pct, signClass } from "@/lib/format";
import { useKe, useMarket, useQuotes } from "@/lib/live";
import { live, type LiveMetrics } from "@/lib/valuation";
import { Dividends, Financials, Projections } from "./CompanyFin";
import { Sources, Thesis } from "./CompanyText";
import { Quant, Valuation } from "./CompanyVal";

export const SECTIONS = [
  ["resumo", "Resumo"],
  ["queda", "A queda"],
  ["financeiro", "Financeiro"],
  ["projecoes", "Projeções"],
  ["valuation", "Valuation"],
  ["dividendos", "Dividendos"],
  ["quant", "Quant"],
  ["tese", "Tese e riscos"],
  ["fontes", "Fontes"],
] as const;

export function useCompanyLive(doc: any) {
  const row = doc.row;
  const { ke } = useKe();
  const q = useQuotes([row.ticker], 30000);
  const lq = q.quotes[row.ticker];
  const price: number | null = lq?.price ?? row.price_ref;
  const L: LiveMetrics = live(row.engine, price, ke, row.mc_q, row.fair_value);
  return { row, ke, price, L, chg: lq?.chg ?? row.chg_snapshot, ts: lq?.ts ?? null, src: lq?.source ?? null };
}

function Stat({ label, value, sub, cls = "" }: { label: string; value: React.ReactNode; sub?: React.ReactNode; cls?: string }) {
  return (
    <div className="min-w-[112px]">
      <div className="label">{label}</div>
      <div className={`mt-0.5 text-[20px] font-semibold leading-tight tracking-[-0.01em] ${cls}`}>{value}</div>
      {sub && <div className="mt-0.5 text-[11.5px] text-muted">{sub}</div>}
    </div>
  );
}

export function CompanyHeader({ doc, isOpp, report = false }: { doc: any; isOpp: boolean; report?: boolean }) {
  const { row, ke, price, L, chg, ts, src } = useCompanyLive(doc);
  const v = doc.valuation || {};
  const fin = row.template === "financial";
  return (
    <section className="panel p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-baseline gap-3">
            <h1 className="text-[32px] font-semibold leading-none tracking-[-0.02em]">{row.ticker}</h1>
            <span className="text-[16px] text-ink-2">{row.name}</span>
          </div>
          <div className="mt-1.5 text-[12.5px] text-muted">
            {[row.sector?.setor, row.sector?.subsetor, row.sector?.segmento].filter(Boolean).join(" / ")}
          </div>
        </div>
        <div className="text-right">
          <div className="flex items-baseline justify-end gap-3">
            <span className="num text-[30px] font-semibold leading-none">{brl(price)}</span>
            <span className={`num text-[15px] font-medium ${signClass(chg)}`}>{pct(chg, 2, true)}</span>
          </div>
          <div className="mt-1 text-[11.5px] text-muted">
            {ts ? `${src} ${ts.slice(11, 19)}` : "preço de referência do estudo"}
            {row.prev_close ? `, pré-eleição ${brl(row.prev_close)}` : ""}
            {row.price_pre_rally ? `, pré-rali (14/08) ${brl(row.price_pre_rally)}` : ""}
          </div>
        </div>
      </div>
      <div className="mt-5 flex flex-wrap gap-x-8 gap-y-4 border-t border-hairline pt-4">
        <Stat label={`Valor justo (Ke ${Math.round(ke * 100)}%)`} value={brl(L.fair)} sub={row.template === "holding" ? "soma das partes" : "DCF, DDM e múltiplos"} />
        <Stat label="Upside" value={pct(L.upside, 1, true)} cls={signClass(L.upside)} />
        <div className="min-w-[150px]">
          <div className="label">TIR de dono vs Ke</div>
          <div className="mt-1.5 flex items-center gap-2">
            <IrrMeter irr={L.irr} ke={ke} w={92} />
            <span className="num text-[20px] font-semibold leading-tight">{pct(L.irr, 1)}</span>
          </div>
          <div className="mt-0.5 text-[11.5px] text-muted">dividendos + perpetuidade</div>
        </div>
        <Stat label="TIR 3 anos" value={pct(L.irr3, 1)} sub="saída ao P/L alvo em 2028" />
        <Stat label="P(valor > preço)" value={pct(L.prob, 0)} sub="Monte Carlo, 5.000 cenários" />
        <Stat label="DY 2027E" value={pct(L.dy, 1)} />
        <Stat label="P/L 2027E" value={mult(L.pe)} />
        {fin ? <Stat label="P/VP" value={mult(v.pbv_now, 2)} sub={isNum(v.justified_pbv) ? `justo a Ke: ${mult(v.justified_pbv, 2)}` : undefined} /> : <Stat label="EV/EBITDA 2027E" value={mult(v.ev_ebitda_fwd)} />}
      </div>
      {!report && (
        <nav className="no-print mt-5 flex flex-wrap gap-1 border-t border-hairline pt-3 text-[13px]">
          {SECTIONS.map(([id, label]) => (
            <a key={id} href={`#${id}`} className="rounded px-2 py-1 text-ink-2 hover:bg-surface-2 hover:text-ink">
              {label}
            </a>
          ))}
          {isOpp && (
            <Link href={`/relatorio/${row.ticker}`} className="ml-auto rounded bg-accent px-3 py-1 font-medium text-white">
              Abrir relatório
            </Link>
          )}
        </nav>
      )}
    </section>
  );
}

export function SectionTitle({ id, title, sub }: { id: string; title: string; sub?: string }) {
  return (
    <div id={id} className="scroll-mt-[140px] pb-3 pt-2">
      <h2 className="h2">{title}</h2>
      {sub && <p className="mt-1 max-w-[80ch] text-[13px] text-ink-2">{sub}</p>}
    </div>
  );
}

export function football(doc: any, price: number | null, fair: number | null) {
  const v = doc.valuation || {};
  const vals = v.values || {};
  const sens = v.sensitivity?.ke_g as (number | null)[][] | undefined;
  const flat = (sens || []).flat().filter((x): x is number => isNum(x));
  const mc = v.monte_carlo;
  const sc = v.scenarios;
  const d3 = (doc.market?.daily_3y || []) as [string, number][];
  const pre52 = d3.filter((d) => d[0] <= "2026-10-23" && d[0] >= "2025-10-23").map((d) => d[1]);
  const rows = [
    { label: "Valor justo (combinação)", lo: flat.length ? Math.min(...flat) : null, hi: flat.length ? Math.max(...flat) : null, point: fair, note: "Faixa: Ke de 20% a 30% e perpetuidade ±2 p.p." },
    ...(isNum(vals.dcf) ? [{ label: "DCF (FCFF / WACC)", lo: null, hi: null, point: vals.dcf }] : []),
    ...(isNum(vals.ddm) ? [{ label: "DDM (dividendos, Ke)", lo: null, hi: null, point: vals.ddm }] : []),
    ...(isNum(vals.multiples)
      ? [{ label: "Múltiplos-alvo", lo: Math.min(...[vals.pe, vals.ev_ebitda, vals.pbv].filter(isNum)), hi: Math.max(...[vals.pe, vals.ev_ebitda, vals.pbv].filter(isNum)), point: vals.multiples, note: "P/L, EV/EBITDA ou P/VP alvo aplicados a 2027E" }]
      : []),
    ...(isNum(vals.sotp) ? [{ label: "Soma das partes", lo: Math.min(vals.sotp, vals.nav_market ?? vals.sotp), hi: Math.max(vals.sotp, vals.nav_market ?? vals.sotp), point: vals.sotp, note: "Faixa até o NAV a preços de mercado" }] : []),
    ...(mc ? [{ label: "Monte Carlo p10–p90", lo: mc.p10, hi: mc.p90, point: mc.p50 }] : []),
    ...(sc?.bear ? [{ label: "Cenários pessimista–otimista", lo: sc.bear.fair_value, hi: sc.bull?.fair_value, point: fair }] : []),
    ...(isNum(vals.graham) ? [{ label: "Graham", lo: null, hi: null, point: vals.graham, ref: true }] : []),
    ...(isNum(vals.bazin) ? [{ label: "Bazin (DPA/6%)", lo: null, hi: null, point: vals.bazin, ref: true }] : []),
    ...(pre52.length ? [{ label: "Faixa de 52 semanas", lo: Math.min(...pre52), hi: Math.max(...pre52), point: null, ref: true, note: "até a sexta pré-eleição" }] : []),
  ];
  return rows;
}

function Summary({ doc }: { doc: any }) {
  const { price, L, row } = useCompanyLive(doc);
  const rs = doc.research || {};
  const rows = football(doc, price, L.fair);
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <div className="lg:col-span-5">
        <div className="panel h-full p-4">
          <div className="h3">Leitura</div>
          <p className="prose-report mt-2 text-[15px]">{rs.summary || row.summary || "—"}</p>
          {Array.isArray(rs.thesis) && rs.thesis.length > 0 && (
            <ul className="mt-3 space-y-1.5 text-[13.5px] text-ink">
              {rs.thesis.slice(0, 4).map((t: string, i: number) => (
                <li key={i} className="flex gap-2">
                  <span className="mt-[7px] inline-block h-[5px] w-[5px] shrink-0 rounded-full bg-accent" />
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          )}
          {rs.confidence && <div className="mt-3 text-[12px] text-muted">Confiança do analista: {rs.confidence}</div>}
        </div>
      </div>
      <div className="lg:col-span-7">
        <FootballField
          title="Faixas de valor por método"
          subtitle="Por ação ou unit, em R$. Linha cheia: preço ao vivo; tracejada: fechamento pré-eleição."
          rows={rows}
          price={price}
          pre={row.prev_close}
          fmt="num2"
          table={{ columns: ["Método", "Mínimo", "Central", "Máximo"], rows: rows.map((r) => [r.label, num(r.lo), num(r.point), num(r.hi)]) }}
        />
      </div>
    </div>
  );
}

function Drop({ doc }: { doc: any }) {
  const { row, price, chg } = useCompanyLive(doc);
  const m = useMarket(60000);
  const mk = doc.market || {};
  const st = mk.stats || {};
  const t0 = st.today || {};
  const ibLive = m?.indices?.IBOV?.chg;
  const betaD = isNum(st.beta_down_3y) ? st.beta_down_3y : st.beta_2y_daily;
  const obs = isNum(chg) ? chg : t0.chg;
  const expB = isNum(ibLive) && isNum(betaD) ? betaD * ibLive : t0.expected_beta;
  const t = { ...t0, chg: obs, expected_beta: expB, xsec_residual: isNum(obs) && isNum(t0.xsec_predicted) ? obs - t0.xsec_predicted : t0.xsec_residual };
  const d3: [string, number][] = mk.daily_3y || [];
  const ib: [string, number][] = mk.ibov_daily_3y || [];
  const ibMap = new Map(ib.map((d) => [d[0], d[1]]));
  const start = d3.find((d) => ibMap.has(d[0]));
  const base = start ? start[1] : d3[0]?.[1];
  const ibBase = start ? (ibMap.get(start[0]) as number) : ib[0]?.[1];
  const sData: [number, number][] = d3.map((d) => [Date.parse(d[0]), (d[1] / base) * 100]);
  const iData: [number, number][] = ib.filter((d) => !start || d[0] >= start[0]).map((d) => [Date.parse(d[0]), (d[1] / ibBase) * 100]);
  const today = Date.parse("2026-10-26");
  if (isNum(price)) sData.push([today, (price / base) * 100]);
  const ibNow = m?.indices?.IBOV?.price;
  if (isNum(ibNow)) iData.push([today, (ibNow / ibBase) * 100]);
  const items = [
    { label: "Queda observada hoje", value: t.chg ?? row.chg_snapshot ?? 0, highlight: true },
    { label: "Prevista pelo beta de baixa", value: t.expected_beta ?? 0, sub: `beta de baixa ${num(st.beta_down_3y, 2)} × Ibovespa` },
    { label: "Prevista pelos fatores", value: t.xsec_predicted ?? 0, sub: "beta, alavancagem, porte e setor (regressão cross-section, foto do estudo)" },
    { label: "Resíduo (específico)", value: t.xsec_residual ?? 0, sub: "o que os fatores não explicam" },
  ];
  const ev = (mk.crash_events || []) as any[];
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <div className="lg:col-span-7">
        <LineChart
          title={`${row.ticker} contra o Ibovespa, 3 anos (base 100)`}
          subtitle="Preço ajustado por desdobramentos, grupamentos e bonificações (B3). Último ponto ao vivo."
          series={[
            { key: "s", label: row.ticker, color: "var(--series-1)", data: sData, endLabel: true },
            { key: "i", label: "Ibovespa", color: "var(--series-2)", data: iData, width: 1.5 },
          ]}
          vmarks={[
            { x: Date.parse("2026-08-14"), label: "pré-rali" },
            { x: Date.parse("2026-10-05"), label: "1º turno" },
          ]}
          yFmt="num0"
          height={280}
          table={{ columns: ["Data", row.ticker, "Ibovespa"], rows: sData.filter((_, i) => i % 20 === 0).map((d) => [new Date(d[0]).toISOString().slice(0, 10), num(d[1], 1), "—"]) }}
        />
      </div>
      <div className="space-y-4 lg:col-span-5">
        <HBarChart
          title="Quanto da queda foi macro"
          subtitle={`Ao vivo: queda observada e prevista pelo beta (${num(betaD, 2)} × Ibovespa ${pct(isNum(ibLive) ? ibLive : null, 1)}). Resíduo contra os fatores = observado − previsto pela regressão.`}
          items={items}
          fmt="pct1s"
          rowH={34}
          labelWidth={190}
          table={{ columns: ["Componente", "Variação"], rows: items.map((i) => [i.label, pct(i.value, 1, true)]) }}
        />
        <div className="panel grid grid-cols-3 gap-3 p-4 text-[12.5px]">
          <div>
            <div className="label">Beta 2 anos</div>
            <div className="num text-[16px] font-semibold">{num(st.beta_2y_daily, 2)}</div>
          </div>
          <div>
            <div className="label">Volatilidade 1 ano</div>
            <div className="num text-[16px] font-semibold">{pct(st.vol_1y, 0)}</div>
          </div>
          <div>
            <div className="label">Pior queda em 10 anos</div>
            <div className="num text-[16px] font-semibold">{pct(st.max_dd_10y, 0)}</div>
          </div>
          <div>
            <div className="label">Rali até 23/10</div>
            <div className={`num text-[16px] font-semibold ${signClass(st.rally_to_2310)}`}>{pct(st.rally_to_2310, 0, true)}</div>
          </div>
          <div>
            <div className="label">Hoje vs pré-rali</div>
            <div className={`num text-[16px] font-semibold ${signClass(st.now_vs_pre_rally)}`}>{pct(st.now_vs_pre_rally, 0, true)}</div>
          </div>
          <div>
            <div className="label">Retorno 12m pré-eleição</div>
            <div className={`num text-[16px] font-semibold ${signClass(st.ret_12m_pre)}`}>{pct(st.ret_12m_pre, 0, true)}</div>
          </div>
        </div>
      </div>
      {ev.length > 0 && (
        <div className="lg:col-span-12">
          <div className="panel overflow-x-auto p-4">
            <div className="h3">O que aconteceu depois dos outros crashes (dias com Ibovespa −7% ou pior)</div>
            <table className="data mt-2 text-[12.5px]">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Ibovespa no dia</th>
                  <th>{row.ticker} no dia</th>
                  <th>{row.ticker} 3 meses</th>
                  <th>{row.ticker} 12 meses</th>
                  <th>Ibovespa 12 meses</th>
                </tr>
              </thead>
              <tbody>
                {ev.map((e) => (
                  <tr key={e.date}>
                    <td>{e.date.split("-").reverse().join("/")}</td>
                    <td className="neg">{pct(e.ibov, 1)}</td>
                    <td className={signClass(e.stock_d0)}>{pct(e.stock_d0, 1, true)}</td>
                    <td className={signClass(e.f3m)}>{pct(e.f3m, 0, true)}</td>
                    <td className={signClass(e.f12m)}>{pct(e.f12m, 0, true)}</td>
                    <td className={signClass(e.ibov_f12m)}>{pct(e.ibov_f12m, 0, true)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export function CompanyView({ doc, isOpp, notesHtml, reviewHtml }: { doc: any; isOpp: boolean; notesHtml?: string; reviewHtml?: string }) {
  return (
    <div className="space-y-8">
      <CompanyHeader doc={doc} isOpp={isOpp} />
      <div>
        <SectionTitle id="resumo" title="Resumo" />
        <Summary doc={doc} />
      </div>
      <div>
        <SectionTitle id="queda" title="A queda" sub="Decomposição estatística do movimento de hoje e o histórico da ação em crises." />
        <Drop doc={doc} />
      </div>
      <div>
        <SectionTitle id="financeiro" title="Financeiro" sub={`Demonstrações consolidadas da CVM (DFP e ITR), em R$ milhões. Último trimestre: ${doc.profile?.latest_quarter || "—"}.`} />
        <Financials doc={doc} />
      </div>
      <div>
        <SectionTitle id="projecoes" title="Projeções 2026–2030" sub="Premissas da pesquisa setorial, ancoradas no histórico de 5 anos." />
        <Projections doc={doc} />
      </div>
      <div>
        <SectionTitle id="valuation" title="Valuation" sub="Ke de 25% fixado pela meta de retorno. Valores por ação ou unit, salvo indicação." />
        <Valuation doc={doc} />
      </div>
      <div>
        <SectionTitle id="dividendos" title="Dividendos" />
        <Dividends doc={doc} />
      </div>
      <div>
        <SectionTitle id="quant" title="Quant" sub="Fatores comparados às outras 58 empresas da cobertura, sinais de qualidade e de risco de quebra." />
        <Quant doc={doc} />
      </div>
      <div>
        <SectionTitle id="tese" title="Tese e riscos" />
        <Thesis doc={doc} />
      </div>
      <div>
        <SectionTitle id="fontes" title="Fontes e dossiê" />
        <Sources doc={doc} notesHtml={notesHtml} reviewHtml={reviewHtml} />
      </div>
    </div>
  );
}

export { Drop, Summary };
