import fs from "node:fs";
import path from "node:path";
import type { Metadata } from "next";
import { TestsView } from "@/components/tests/TestsView";
import { mdToSafeHtml } from "@/lib/markdown";

export const metadata: Metadata = { title: "Testes e robustez" };

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyObj = any;

export default function Page() {
  const p = path.join(process.cwd(), "data", "app", "tests.json");
  const t: AnyObj = fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, "utf8")) : null;
  if (!t) return <div className="panel p-6">Os testes ainda não foram gerados.</div>;
  const html: Record<string, string> = {};
  for (const [k, v] of Object.entries(t.md || {})) html[k] = mdToSafeHtml(v as string | null);
  const consensusHtml = (t.consensus_md || []).map((m: string) => mdToSafeHtml(m));
  const review = t.review || [];
  return (
    <div className="space-y-6">
      <header>
        <h1 className="h1">Testes e robustez</h1>
        <p className="mt-2 max-w-[68ch] text-[15px] text-ink-2">
          Revisão independente das 59 avaliações, backtest de fatores desde 2017, o que funcionou depois de outros crashes, sensibilidade a pesos e premissas, métodos alternativos de valuation, carteira com testes de estresse, comparação com o consenso e a suíte automatizada de testes do código.
        </p>
      </header>
      <TestsView data={{ ...t, review, md: undefined, consensus_md: undefined }} html={html} consensusHtml={consensusHtml} />
    </div>
  );
}
