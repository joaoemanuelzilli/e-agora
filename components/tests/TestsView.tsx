"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import Link from "next/link";
import { useState, type ReactNode } from "react";
import { HBarChart } from "@/components/charts/Bars";
import { num, pct, signClass } from "@/lib/format";
import { AltCharts, ConsensusChart, CrashCharts, FactorCharts, PortfolioCharts, RobustCharts, SuiteTiles } from "./TestCharts";

export function Md({ html, collapsed = true }: { html?: string; collapsed?: boolean }) {
  const [open, setOpen] = useState(!collapsed);
  if (!html) return null;
  return (
    <div className="panel p-4">
      <div className="flex items-center justify-between">
        <div className="h3">Relatório completo da bateria</div>
        <button type="button" onClick={() => setOpen((v) => !v)} className="no-print rounded border border-hairline px-2 py-0.5 text-[12px] text-ink-2 hover:bg-surface-2">
          {open ? "Recolher" : "Expandir"}
        </button>
      </div>
      <div className={`dossier mt-3 ${open ? "" : "max-h-[220px] overflow-hidden [mask-image:linear-gradient(to_bottom,black_65%,transparent)]"}`} dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}

export function Section({ id, title, sub, children }: { id: string; title: string; sub?: string; children: ReactNode }) {
  return (
    <section id={id} className="scroll-mt-[140px] space-y-4">
      <div>
        <h2 className="h2">{title}</h2>
        {sub && <p className="mt-1 max-w-[80ch] text-[13px] text-ink-2">{sub}</p>}
      </div>
      {children}
    </section>
  );
}

function Review({ rows }: { rows: any[] }) {
  const reviewed = rows.filter((r) => r.has_review);
  const changed = rows.filter((r) => r.changed);
  const deltas = changed
    .filter((r) => r.before.irr !== null && r.after.irr !== null && Math.abs(r.after.irr - r.before.irr) >= 0.0005)
    .map((r) => ({ label: r.ticker, value: r.after.irr - r.before.irr, sub: `TIR ${pct(r.before.irr, 1)} → ${pct(r.after.irr, 1)}` }))
    .sort((a, b) => a.value - b.value);
  return (
    <div className="space-y-4">
      <div className="panel grid grid-cols-2 gap-4 p-5 md:grid-cols-4">
        <div>
          <div className="label">Empresas revisadas</div>
          <div className="text-[26px] font-semibold">
            {reviewed.length} de {rows.length}
          </div>
        </div>
        <div>
          <div className="label">Premissas corrigidas</div>
          <div className="text-[26px] font-semibold">{changed.length}</div>
        </div>
        <div>
          <div className="label">TIR subiu</div>
          <div className="text-[26px] font-semibold">{deltas.filter((d) => d.value > 0.0005).length}</div>
        </div>
        <div>
          <div className="label">TIR caiu</div>
          <div className="text-[26px] font-semibold">{deltas.filter((d) => d.value < -0.0005).length}</div>
        </div>
      </div>
      {deltas.length > 0 && (
        <HBarChart
          title="Efeito das correções na TIR de dono"
          subtitle="Pontos percentuais, depois da revisão menos antes"
          items={deltas.map((d) => ({ ...d, value: d.value * 100 }))}
          fmt={(v: number) => `${v > 0 ? "+" : ""}${v.toLocaleString("pt-BR", { maximumFractionDigits: 1 })} p.p.`}
          rowH={22}
          labelWidth={70}
        />
      )}
      <div className="panel sticky-host">
        <div className="freeze-wrap">
          <table className="data freeze min-w-[900px] text-[12.5px]">
            <thead>
              <tr>
                <th className="freeze-col">Empresa</th>
                <th className="!text-left">Veredito do revisor</th>
                <th>Valor justo antes</th>
                <th>depois</th>
                <th>TIR antes</th>
                <th>depois</th>
                <th>Ranking antes</th>
                <th>depois</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.ticker}>
                  <td className="freeze-col">
                    <Link href={`/empresa/${r.ticker}`} className="font-semibold hover:text-accent">
                      {r.ticker}
                    </Link>
                    {r.changed && <span className="ml-1.5 rounded px-1 text-[10.5px] text-accent-ink" style={{ background: "var(--accent-soft)" }}>ajustada</span>}
                  </td>
                  <td className="max-w-[360px] whitespace-normal text-left text-ink-2">{r.verdict || (r.has_review ? "revisada" : "em revisão")}</td>
                  <td>{num(r.before.fair)}</td>
                  <td className={signClass((r.after.fair ?? 0) - (r.before.fair ?? 0))}>{num(r.after.fair)}</td>
                  <td>{pct(r.before.irr, 1)}</td>
                  <td className={signClass((r.after.irr ?? 0) - (r.before.irr ?? 0))}>{pct(r.after.irr, 1)}</td>
                  <td>{r.before.rank ?? "—"}</td>
                  <td>{r.after.rank ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function Decisions({ data }: { data: any }) {
  const rv = (data.review || []) as any[];
  const changed = rv.filter((r) => r.changed).length;
  const dropped = (data.dropped || []) as { ticker: string; reasons: string[] }[];
  const items: [string, string][] = [
    ["Premissas", `${changed} das ${rv.length} avaliações tiveram premissas corrigidas pela revisão independente; a conclusão de quem bate o Ke de 25% quase não mudou.`],
    ["Pesos do valuation", "Incorporadoras passaram a DDM 50%, P/L-alvo 30% e DCF 20%; bancos a DDM 60% e P/VP 40%. Nos demais setores as duas baterias discordaram e o padrão 50/25/25 ficou."],
    ["Escore multifator", "Momentum de 12 meses entrou com 10%; valor e qualidade cederam 5 p.p. cada. Pesos otimizados não se sustentaram fora da amostra."],
    ["Seleção", `${(data.opportunities || []).join(", ")}.${dropped.length ? ` Saíram ${dropped.map((d) => d.ticker).join(" e ")}: chance de o valor justo superar o preço abaixo de 45%.` : ""}`],
    ["Código e dados", "Corrigidos: escala das ações da CVM, ano reapresentado zerado, 4º trimestre com bases misturadas, TIR sem raiz, holdings fora do Ke escolhido e preços das controladas fixados na foto das 13h02."],
    ["Ampliação (28/10)", "63 empresas novas (todas as do universo com liquidez de R$ 10 mi/dia ou mais), feitas por 20 analistas sob um checklist com as lições da revisão, sem segunda revisão independente. A busca na web esgotou no meio do trabalho, então parte dos dados ficou só com documentos oficiais; cada dossiê lista o que não foi verificado."],
  ];
  return (
    <div className="panel divide-y divide-hairline">
      {items.map(([k, v]) => (
        <div key={k} className="grid grid-cols-1 gap-1 px-4 py-3 sm:grid-cols-[180px_1fr] sm:gap-4">
          <div className="text-[13px] font-semibold text-ink">{k}</div>
          <div className="text-[13.5px] text-ink-2">{v}</div>
        </div>
      ))}
    </div>
  );
}

export function TestsView({ data, html, consensusHtml }: { data: any; html: Record<string, string>; consensusHtml: string[] }) {
  return (
    <div className="space-y-10">
      <nav className="no-print flex flex-wrap gap-1 text-[13px]">
        {[
          ["decisoes", "O que mudou"],
          ["revisao", "Revisão independente"],
          ["fatores", "Backtest de fatores"],
          ["crashes", "Depois de crashes"],
          ["robustez", "Robustez a pesos"],
          ["metodos", "Métodos alternativos"],
          ["carteira", "Carteira e estresse"],
          ["consenso", "Consenso"],
          ["suite", "Testes do código"],
        ].map(([id, l]) => (
          <a key={id} href={`#${id}`} className="rounded border border-hairline px-2.5 py-1 text-ink-2 hover:bg-surface-2 hover:text-ink">
            {l}
          </a>
        ))}
      </nav>
      <Section id="decisoes" title="O que mudou no estudo por causa dos testes">
        <Decisions data={data} />
      </Section>
      <Section id="revisao" title="Revisão independente das 59 avaliações" sub="Um segundo analista por setor auditou premissas, contas e coerência com o histórico da CVM, corrigindo erros nos dois sentidos.">
        <Review rows={data.review || []} />
      </Section>
      <Section id="fatores" title="Backtest de fatores (2017–2026)" sub="Quais características previram retorno nas ações brasileiras, mês a mês, e que pesos funcionam fora da amostra.">
        <FactorCharts f={data.factor} />
        <Md html={html.factor_backtest} />
      </Section>
      <Section id="crashes" title="O que funcionou depois de outros crashes" sub="Joesley Day, Covid, eleição de 2022 e outros dias de queda forte: que tipo de ação se recuperou mais.">
        <CrashCharts c={data.crash} />
        <Md html={html.crash_study} />
      </Section>
      <Section id="robustez" title="Robustez a pesos e premissas" sub="Quanto o ranking e as oportunidades mudam com os pesos do valuation, o Ke, a perpetuidade, os múltiplos, a margem e o custo da dívida.">
        <RobustCharts rb={data.robust} />
        <Md html={html.robustness} />
      </Section>
      <Section id="metodos" title="Métodos alternativos de valuation" sub="Lucro residual, EVA, APV, FCFE e múltiplos justificados contra os métodos do estudo.">
        <AltCharts a={data.alt} />
        <Md html={html.alt_methods} />
      </Section>
      <Section id="carteira" title="Carteira e testes de estresse" sub="Como dimensionar as posições e o que acontece em cenários de juros, câmbio e bolsa.">
        <PortfolioCharts p={data.portfolio} />
        <Md html={html.portfolio} />
      </Section>
      <Section id="consenso" title="Comparação com o consenso de mercado" sub="Preços-alvo dos bancos contra o valor justo final do estudo, que usa Ke de 25%.">
        <ConsensusChart rows={data.consensus || []} />
        {consensusHtml.map((h, i) => (
          <Md key={i} html={h} />
        ))}
      </Section>
      <Section id="suite" title="Testes automatizados do código" sub="Paridade do motor TypeScript com o Python, integridade dos dados da CVM e da B3, saídas do modelo e rotas do site.">
        <SuiteTiles s={data.suite} />
        <Md html={html.test_report} />
      </Section>
    </div>
  );
}
