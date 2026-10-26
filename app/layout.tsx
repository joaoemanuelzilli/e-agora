import type React from "react";
import type { Metadata, Viewport } from "next";
import { IBM_Plex_Sans, IBM_Plex_Serif } from "next/font/google";
import { Header, type MacroFallback } from "@/components/ui/Header";
import { getOverview } from "@/lib/data";
import { Providers } from "./providers";
import "./globals.css";

const sans = IBM_Plex_Sans({ variable: "--font-plex-sans", subsets: ["latin"], weight: ["400", "500", "600"], display: "swap" });
const serif = IBM_Plex_Serif({ variable: "--font-plex-serif", subsets: ["latin"], weight: ["400", "500"], style: ["normal", "italic"], display: "swap" });

export const metadata: Metadata = {
  title: "E agora? Valuation pós-eleição",
  description: "Estudo de valuation das 59 ações brasileiras que mais caíram após a reeleição de Lula (26/10/2026): DCF, múltiplos, DDM, TIR de dono, Monte Carlo e evidência estatística, com cotações ao vivo da B3.",
};

export const viewport: Viewport = { themeColor: [{ media: "(prefers-color-scheme: light)", color: "#ffffff" }, { media: "(prefers-color-scheme: dark)", color: "#101a2b" }] };

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
    <html lang="pt-BR" className={`${sans.variable} ${serif.variable}`} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
      </head>
      <body className="min-h-screen">
        <Providers>
          <Header fallback={fb} />
          <main className="mx-auto max-w-[1440px] px-4 pb-16 pt-6 sm:px-6">{children}</main>
          <footer className="no-print mx-auto max-w-[1440px] px-4 pb-10 text-[12px] text-muted sm:px-6">
            Fontes: CVM (DFP/ITR), B3 (cotações, proventos, índices, COTAHIST), Banco Central (SGS, Focus). Estudo quantitativo com finalidade informativa; não é recomendação de investimento.
          </footer>
        </Providers>
      </body>
    </html>
  );
}
