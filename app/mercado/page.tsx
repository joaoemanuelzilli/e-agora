import type { Metadata } from "next";
import { MarketView } from "@/components/market/MarketView";
import { getOverview } from "@/lib/data";

export const metadata: Metadata = { title: "Mercado: o choque em perspectiva" };

export default function Page() {
  const ov = getOverview();
  const m = ov.market;
  const f12 = m.crash_forward_stats.f12m;
  return (
    <div className="space-y-6">
      <header>
        <h1 className="h1">O choque em perspectiva</h1>
        <p className="mt-2 max-w-[68ch] text-[15px] text-ink-2">
          O Ibovespa fechou a sexta em {m.ibov_today.prev_close.toLocaleString("pt-BR", { maximumFractionDigits: 0 })} pontos, perto da máxima histórica, depois de subir desde {m.ibov_today.pre_rally ? `${m.ibov_today.pre_rally.toLocaleString("pt-BR", { maximumFractionDigits: 0 })} pontos em 14/08` : "agosto"} com a expectativa de vitória de Flávio Bolsonaro. Hoje devolveu o rali inteiro em um pregão. Desde 1998, depois de dias de queda de 5% ou mais, a mediana do índice em 12 meses foi de {Math.round((f12.median ?? 0) * 100)}% de alta, com alta em {Math.round((f12.pct_pos ?? 0) * 100)}% das vezes.
        </p>
      </header>
      <MarketView market={m} xsec={ov.xsec} sectors={ov.sectors} />
    </div>
  );
}
