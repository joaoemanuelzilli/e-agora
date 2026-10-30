import type React from "react";
import type { Metadata, Viewport } from "next";
import { Libre_Franklin } from "next/font/google";
import { Header, type MacroFallback } from "@/components/ui/Header";
import { getOverview } from "@/lib/data";
import { Providers } from "./providers";
import "./globals.css";

const franklin = Libre_Franklin({ variable: "--font-franklin", subsets: ["latin"], weight: ["400", "500", "600", "700"], style: ["normal", "italic"], display: "swap" });

export const metadata: Metadata = {
  title: "E agora? Valuation pós-eleição",
  description: "Estudo de valuation das ações brasileiras mais líquidas depois da reeleição de Lula (26/10/2026): DCF, múltiplos, DDM, TIR de dono, Monte Carlo e evidência estatística, com cotações ao vivo da B3.",
};

export const viewport: Viewport = { themeColor: [{ media: "(prefers-color-scheme: light)", color: "#0b2545" }, { media: "(prefers-color-scheme: dark)", color: "#0d2a4f" }] };

const themeInit = `try{var t=localStorage.getItem("theme");if(t)document.documentElement.setAttribute("data-theme",t)}catch(e){}`;

function macroFallback(): MacroFallback {
  const ov = getOverview();
  const v = (k: string) => {
    const a = ov.macro?.[k];
    return a && a[0] ? Number(a[0].valor) / 100 : null;
  };
  return { selic: v("selic"), ipca12m: v("ipca12m"), ibov: ov.market.ibov_today.price, ibovChg: ov.market.ibov_today.chg };
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const fb = macroFallback();
  return (
    <html lang="pt-BR" className={franklin.variable} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
      </head>
      <body className="min-h-screen">
        <Providers>
          <Header fallback={fb} />
          <main className="mx-auto max-w-[1440px] px-4 pb-16 pt-6 sm:px-6">{children}</main>
          <footer className="no-print border-t border-hairline bg-surface-2">
            <div className="mx-auto grid max-w-[1440px] gap-x-8 gap-y-3 px-4 py-6 text-[12px] leading-relaxed text-muted sm:px-6 md:grid-cols-12">
              <div className="md:col-span-3">
                <div className="text-[13px] font-bold text-ink">E agora? Research</div>
                <div>Valuation pós-eleição, 26 de outubro de 2026</div>
              </div>
              <p className="md:col-span-5">
                Fontes: CVM (DFP/ITR), B3 (cotações, proventos, índices, COTAHIST) e Banco Central (SGS, Focus). Cotações da B3 com até 15 minutos de atraso.
              </p>
              <p className="md:col-span-4">Estudo quantitativo com finalidade informativa; não é recomendação de investimento.</p>
            </div>
          </footer>
        </Providers>
      </body>
    </html>
  );
}
