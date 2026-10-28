import Link from "next/link";
import { HBarChart } from "@/components/charts/Bars";
import { Scatter } from "@/components/charts/Points";
import fs from "node:fs";
import path from "node:path";
import { OverviewClient } from "@/components/OverviewClient";
import type { External } from "@/components/opps/OppShowcase";
import { getCompany, getOverview } from "@/lib/data";

const p0 = (v: number) => `${v > 0 ? "+" : ""}${Math.round(v * 100)}%`;

export default function Page() {
  const ov = getOverview();
  const cov = new Set(ov.companies.map((c) => c.ticker));
  const extPath = path.join(process.cwd(), "data", "external", "analise_aprofundada_2810.json");
  const external: External | null = fs.existsSync(extPath) ? JSON.parse(fs.readFileSync(extPath, "utf8")) : null;
  const headlines: Record<string, string> = {};
  for (const t of ov.opportunities) {
    const h = getCompany(t)?.report?.headline;
    if (typeof h === "string") headlines[t] = h;
  }
  const valLabel = (ov as unknown as { valuation_label?: string | null }).valuation_label ?? null;
  const pts = ov.xsec.points;
  const extremes = [...pts].sort((a, b) => a.residual - b.residual);
  const labelSet = new Set([...extremes.slice(0, 6), ...extremes.slice(-4)].map((p) => p.ticker));
  return (
    <div className="space-y-8">
      <OverviewClient rows={ov.companies} opps={ov.opportunities} market={ov.market} xsec={ov.xsec} external={external} headlines={headlines} valLabel={valLabel} reports={ov.reports ?? []} />

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7">
          <Scatter
            title="A queda de hoje foi sistêmica"
            subtitle={`Queda prevista só por fatores (beta de baixa, alavancagem, porte, setor) contra a queda observada, ${ov.xsec.n} ações. R² = ${Math.round(ov.xsec.r2 * 100)}%. Acima da diagonal caiu menos que o previsto.`}
            points={pts.map((p) => ({
              id: p.ticker,
              x: p.predicted,
              y: p.actual,
              highlight: cov.has(p.ticker),
              label: labelSet.has(p.ticker) ? p.ticker : undefined,
              sub: `resíduo ${p0(p.residual)}`,
            }))}
            xFmt="pct0s"
            yFmt="pct0s"
            xLabel="Queda prevista pelos fatores"
            yLabel="Queda observada"
            diagonal
            height={360}
            legend={[
              { label: "Cobertas no estudo", color: "var(--series-1)", kind: "dot" },
              { label: "Demais do universo", color: "var(--deemph)", kind: "dot" },
            ]}
            table={{ columns: ["Ticker", "Prevista", "Observada", "Resíduo"], rows: pts.map((p) => [p.ticker, p0(p.predicted), p0(p.actual), p0(p.residual)]) }}
          />
        </div>
        <div className="lg:col-span-5">
          <HBarChart
            title="Queda mediana por setor"
            subtitle="Universo IBOV + IBrX-100 + SMLL, variação do dia"
            items={ov.sector_stats.map((s) => ({ label: s.setor, value: s.median, sub: `${s.n} ações` }))}
            fmt="pct0s"
            rowH={30}
            table={{ columns: ["Setor", "Mediana", "Ações"], rows: ov.sector_stats.map((s) => [s.setor, p0(s.median), s.n]) }}
          />
          <div className="mt-3 text-right">
            <Link href="/mercado" className="text-[13px] font-medium text-accent hover:underline">
              Ver o estudo de mercado completo
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
