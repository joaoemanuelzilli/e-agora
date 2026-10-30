"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import Link from "next/link";
import { Dividends, Financials, Projections } from "@/components/company/CompanyFin";
import { Sources } from "@/components/company/CompanyText";
import { CompanyHeader, Drop, SectionTitle, Summary } from "@/components/company/CompanyView";
import { Quant, Valuation } from "@/components/company/CompanyVal";

type Reason = { title: string; body: string; metric?: { label: string; value: string } };
type StatItem = { title: string; body: string; stat?: string };
type Risk = { title: string; body: string; mitigant?: string };
type Mon = { kpi: string; threshold: string; next?: string };

function ReasonPoint({ r }: { r: Reason }) {
  return (
    <div className="border-t border-hairline pt-3">
      <p className="max-w-[68ch] text-[14px] leading-relaxed text-ink-2">
        <b className="font-bold text-ink">{r.title}.</b> {r.body}
      </p>
      {r.metric && (
        <p className="mt-1.5 text-[12.5px] text-muted">
          {r.metric.label}: <b className="num font-bold text-ink">{r.metric.value}</b>
        </p>
      )}
    </div>
  );
}

function StatCard({ s }: { s: StatItem }) {
  return (
    <div className="border-t border-hairline pt-3">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4">
        <div className="h3">{s.title}</div>
        {s.stat && <div className="num text-[13px] font-semibold text-accent-ink">{s.stat}</div>}
      </div>
      <p className="mt-1 text-[13.5px] leading-relaxed text-ink-2">{s.body}</p>
    </div>
  );
}

export function ReportView({ doc, notesHtml, rank, total, rule, dropped }: { doc: any; notesHtml?: string; rank: number; total: number; rule: string; dropped?: string[] }) {
  const rp = doc.report || {};
  const row = doc.row;
  const reasons = (rp.reasons || []) as Reason[];
  const stats = (rp.statistics || []) as StatItem[];
  const risks = (rp.risks || []) as Risk[];
  const mon = (rp.monitor || []) as Mon[];
  const cats = (rp.catalysts || []) as { date: string; event: string }[];
  return (
    <article className="space-y-8">
      <div className="no-print flex items-center justify-between gap-3 text-[12.5px]">
        <Link href="/" className="text-ink-2 hover:text-ink">
          Painel
        </Link>
        <div className="flex items-center gap-3">
          <Link href={`/empresa/${row.ticker}`} className="link">
            Análise completa da empresa
          </Link>
          <button type="button" onClick={() => window.print()} className="btn btn-secondary !py-1">
            Imprimir ou salvar PDF
          </button>
        </div>
      </div>

      <CompanyHeader doc={doc} isOpp report />

      <header className="space-y-4">
        {dropped && (
          <div className="keybox px-4 py-3 text-[13.5px] text-ink-2">
            <span className="font-semibold text-ink">Saiu da seleção na revisão independente de 26/10.</span> Motivo: {dropped.join("; ")}. O relatório segue publicado como registro da tese.
          </div>
        )}
        <h1
          className={`max-w-[40ch] font-bold tracking-[-0.02em] ${(rp.headline || "").length > 140 ? "text-[24px] leading-[1.22]" : (rp.headline || "").length > 90 ? "text-[28px] leading-[1.18]" : "text-[34px] leading-[1.12]"}`}
        >
          {rp.headline || `${row.ticker}: ${row.name}`}
        </h1>
        {rp.verdict && <p className="prose-report text-[17px]">{rp.verdict}</p>}
        <p className="text-[12.5px] text-muted">
          {dropped ? "Relatório de 26 de outubro de 2026, fora da seleção atual" : rank > 0 ? `Relatório de oportunidade ${rank} de ${total}` : "Relatório de 26 de outubro de 2026, fora da seleção atual"}
          . Texto escrito com os preços de 26/10 (13h02); os números do quadro acima são ao vivo.
        </p>
      </header>

      {reasons.length > 0 && (
        <section>
          <SectionTitle id="motivos" title={dropped ? "A tese, e o que ainda vale nela" : "Por que está entre as melhores"} />
          <div className="grid grid-cols-1 gap-x-10 gap-y-4 md:grid-cols-2">
            {reasons.map((r, i) => (
              <ReasonPoint key={i} r={r} />
            ))}
          </div>
        </section>
      )}

      <section>
        <SectionTitle id="valor" title="Quanto vale" sub="Cada método de valuation, a faixa de sensibilidade e onde o preço está." />
        <Summary doc={doc} />
      </section>

      <section>
        <SectionTitle id="estatistica" title="Embasamento estatístico" sub="O que os dados dizem sobre a queda, o preço relativo e a probabilidade de a tese funcionar." />
        {stats.length > 0 && (
          <div className="panel mb-4 grid grid-cols-1 gap-x-8 gap-y-4 p-5 lg:grid-cols-2">
            {stats.map((s, i) => (
              <StatCard key={i} s={s} />
            ))}
          </div>
        )}
        <Drop doc={doc} />
      </section>

      <section>
        <SectionTitle id="valuation" title="Valuation em detalhe" sub="DCF, sensibilidades, cenários, Monte Carlo e múltiplos históricos." />
        <Valuation doc={doc} />
      </section>

      <section>
        <SectionTitle id="fundamentos" title="Fundamentos" sub={`Histórico oficial da CVM e projeções do estudo. Último trimestre: ${doc.profile?.latest_quarter || "—"}.`} />
        <Financials doc={doc} />
      </section>

      <section>
        <SectionTitle id="projecoes" title="Projeções e premissas" />
        <Projections doc={doc} />
      </section>

      <section>
        <SectionTitle id="dividendos" title="Dividendos e retorno ao acionista" />
        <Dividends doc={doc} />
      </section>

      <section>
        <SectionTitle id="quant" title="Fatores quantitativos" />
        <Quant doc={doc} />
      </section>

      {(risks.length > 0 || mon.length > 0) && (
        <section>
          <SectionTitle id="riscos" title="Riscos e o que invalida a tese" />
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
            <div className="panel p-4">
              <div className="h3 mb-3">Riscos</div>
              <div className="space-y-3">
                {risks.map((r, i) => (
                  <div key={i} className="border-b border-hairline pb-3 last:border-b-0 last:pb-0">
                    <div className="text-[13.5px] font-semibold">{r.title}</div>
                    <p className="mt-0.5 text-[13px] leading-relaxed text-ink-2">{r.body}</p>
                    {r.mitigant && (
                      <p className="mt-1 text-[12.5px] text-ink-2">
                        <span className="font-medium text-ink">Mitigante: </span>
                        {r.mitigant}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
            <div className="space-y-4">
              {mon.length > 0 && (
                <div className="panel overflow-x-auto p-4">
                  <div className="h3 mb-2">O que acompanhar</div>
                  <table className="data text-[12.5px]">
                    <thead>
                      <tr>
                        <th>Indicador</th>
                        <th className="!text-left">Gatilho que invalida</th>
                        <th>Próximo dado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {mon.map((m, i) => (
                        <tr key={i}>
                          <td className="whitespace-normal">{m.kpi}</td>
                          <td className="whitespace-normal text-left text-ink-2">{m.threshold}</td>
                          <td className="whitespace-normal text-muted">{m.next || "—"}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              {cats.length > 0 && (
                <div className="panel p-4">
                  <div className="h3 mb-2">Catalisadores</div>
                  <ul className="space-y-1.5 text-[13px]">
                    {cats.map((c, i) => (
                      <li key={i} className="flex gap-3">
                        <span className="num w-[92px] shrink-0 text-muted">{c.date}</span>
                        <span>{c.event}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {rp.bottom_line && (
        <section className="panel rounded-none border-t-2 border-t-[var(--rule)] p-5">
          <div className="h3">Conclusão</div>
          <p className="prose-report mt-2 text-[16px]">{rp.bottom_line}</p>
        </section>
      )}

      <section>
        <SectionTitle id="fontes" title="Fontes, método e dossiê" sub={`Critério de seleção: ${rule}`} />
        <Sources doc={doc} notesHtml={notesHtml} />
      </section>
    </article>
  );
}
