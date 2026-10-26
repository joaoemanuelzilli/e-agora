import fs from "node:fs";
import path from "node:path";
import type { Metadata } from "next";
import { InvestView, type Monitor, type StudyPortfolio } from "@/components/invest/InvestView";
import { getCompany, getOverview } from "@/lib/data";

export const metadata: Metadata = { title: "Investir" };

// Gatilho curto: tira apartes entre parênteses e, se pedido, a justificativa depois de ":" ou " — ".
function clean(s: unknown, dropReason = true): string {
  if (typeof s !== "string") return "";
  let t = s;
  for (let i = 0; i < 3; i++) t = t.replace(/\s*\([^()]*\)/g, "");
  if (dropReason) t = t.split(/:\s| — /)[0];
  return t.replace(/\s+/g, " ").trim().replace(/[.;,]$/, "");
}

export default function Page() {
  const ov = getOverview();
  const monitors: Record<string, Monitor[]> = {};
  for (const t of ov.opportunities) {
    const items = getCompany(t)?.report?.monitor;
    if (!Array.isArray(items)) continue;
    monitors[t] = items
      .map((m: { kpi?: string; threshold?: string; next?: string }) => ({
        kpi: clean(m.kpi),
        threshold: clean(m.threshold),
        next: clean(m.next, false) || undefined,
      }))
      .filter((m: Monitor) => m.kpi && m.threshold);
  }
  const pp = path.join(process.cwd(), "data", "app", "portfolio.json");
  const port: StudyPortfolio | null = fs.existsSync(pp) ? JSON.parse(fs.readFileSync(pp, "utf8")) : null;
  const portfolio = port && port.sleeve?.every((x) => ov.opportunities.includes(x.ticker)) ? port : null;
  return (
    <div className="space-y-6">
      <header>
        <h1 className="h1">Investir</h1>
        <p className="mt-2 max-w-[72ch] text-[15px] text-ink-2">
          Até que preço comprar cada ação para render a meta de retorno, e quantas ações pedir com o valor que você tem. Preço-teto é o menor entre o preço que dá TIR de dono igual ao Ke e o valor justo; acima dele, não compre.
        </p>
      </header>
      <InvestView rows={ov.companies} opps={ov.opportunities} monitors={monitors} portfolio={portfolio} />
    </div>
  );
}
