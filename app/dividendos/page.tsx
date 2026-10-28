import type { Metadata } from "next";
import { DividendMap, type DivData } from "@/components/dividends/DividendMap";
import { getDividends, getOverview } from "@/lib/data";

export const metadata: Metadata = { title: "Mapa de dividendos" };

export default function Page() {
  const ov = getOverview();
  const data = getDividends<DivData>();
  return (
    <div className="space-y-6">
      <header>
        <h1 className="h1">Mapa de dividendos</h1>
        <p className="mt-2 max-w-[72ch] text-[15px] text-ink-2">
          Quem paga, quanto, em que meses e o que já está aprovado para cair, em todas as empresas do estudo. Histórico oficial da B3 desde 2016; yields recalculados ao preço ao vivo.
        </p>
      </header>
      <DividendMap rows={ov.companies} data={data} opps={ov.opportunities} />
    </div>
  );
}
