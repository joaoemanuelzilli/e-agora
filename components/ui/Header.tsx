"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { useKe, useMarket } from "@/lib/live";

const NAV = [
  { href: "/", label: "Painel" },
  { href: "/investir", label: "Investir" },
  { href: "/dividendos", label: "Dividendos" },
  { href: "/mercado", label: "Mercado" },
  { href: "/metodologia", label: "Metodologia" },
  { href: "/testes", label: "Testes" },
];

function pctTxt(x: number | null | undefined, d = 2) {
  if (x === null || x === undefined || !Number.isFinite(x)) return "—";
  return `${x > 0 ? "+" : ""}${(x * 100).toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d })}%`;
}

function ThemeToggle() {
  const [theme, setTheme] = useState<string>("auto");
  useEffect(() => {
    try {
      setTheme(localStorage.getItem("theme") || "auto");
    } catch {}
  }, []);
  const apply = (t: string) => {
    setTheme(t);
    try {
      if (t === "auto") {
        localStorage.removeItem("theme");
        document.documentElement.removeAttribute("data-theme");
      } else {
        localStorage.setItem("theme", t);
        document.documentElement.setAttribute("data-theme", t);
      }
    } catch {}
  };
  const next = theme === "auto" ? "dark" : theme === "dark" ? "light" : "auto";
  const label = theme === "auto" ? "Tema automático" : theme === "dark" ? "Tema escuro" : "Tema claro";
  return (
    <button type="button" onClick={() => apply(next)} className="rounded border border-hairline px-2 py-1 text-[12px] text-ink-2 hover:bg-surface-2" title="Alternar tema" aria-label={label}>
      {theme === "auto" ? "Auto" : theme === "dark" ? "Escuro" : "Claro"}
    </button>
  );
}

function KeControl() {
  const { ke, setKe } = useKe();
  const opts = [0.2, 0.25, 0.3];
  return (
    <div className="flex items-center gap-1.5" role="group" aria-label="Custo de capital próprio (Ke)">
      <span className="text-[12px] text-muted">Ke</span>
      <div className="flex overflow-hidden rounded border border-hairline">
        {opts.map((o) => (
          <button
            key={o}
            type="button"
            onClick={() => setKe(o)}
            aria-pressed={Math.abs(ke - o) < 1e-9}
            className={`px-2 py-1 text-[12px] num ${Math.abs(ke - o) < 1e-9 ? "bg-accent text-white" : "text-ink-2 hover:bg-surface-2"}`}
          >
            {Math.round(o * 100)}%
          </button>
        ))}
      </div>
    </div>
  );
}

function StripItem({ label, value, chg, invert = false }: { label: string; value: string; chg?: number | null; invert?: boolean }) {
  const cls = chg === null || chg === undefined ? "" : (invert ? -chg : chg) >= 0 ? "pos" : "neg";
  return (
    <div className="flex shrink-0 items-baseline gap-1.5 whitespace-nowrap">
      <span className="text-[12px] text-muted">{label}</span>
      <span className="num text-[13px] font-medium">{value}</span>
      {chg !== undefined && <span className={`num text-[12px] ${cls}`}>{pctTxt(chg)}</span>}
    </div>
  );
}

export type MacroFallback = { selic: number | null; ipca12m: number | null; ibov: number | null; ibovChg: number | null };

function MarketStrip({ fb }: { fb: MacroFallback }) {
  const m = useMarket();
  const ib = m?.indices?.IBOV;
  const di = (code: string) => m?.di?.find((d) => d.code === code);
  const time = m?.asOf ? new Date(m.asOf).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : null;
  const n = (v: number | null | undefined, d = 0) => (v === null || v === undefined ? "—" : v.toLocaleString("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d }));
  const diTxt = (code: string) => {
    const d = di(code);
    return d?.rate ? `${n(d.rate, 2)}%` : "—";
  };
  return (
    <div className="border-b border-hairline bg-surface">
      <div className="mx-auto flex max-w-[1440px] items-center gap-6 overflow-x-auto px-4 py-2 sm:px-6">
        <StripItem label="Ibovespa" value={n(ib?.price ?? fb.ibov, 0)} chg={ib?.chg ?? fb.ibovChg} />
        <StripItem label="Small Caps" value={n(m?.indices?.SMLL?.price, 0)} chg={m?.indices?.SMLL?.chg ?? null} />
        <StripItem label="Financeiro" value={n(m?.indices?.IFNC?.price, 0)} chg={m?.indices?.IFNC?.chg ?? null} />
        <StripItem label="Imobiliário" value={n(m?.indices?.IMOB?.price, 0)} chg={m?.indices?.IMOB?.chg ?? null} />
        <StripItem label="Dólar fut." value={m?.dollar ? `R$ ${n(m.dollar.price, 3)}` : "—"} chg={m?.dollar?.chg ?? null} invert />
        <StripItem label="DI jan/27" value={diTxt("DI1F27")} />
        <StripItem label="DI jan/29" value={diTxt("DI1F29")} />
        <StripItem label="DI jan/31" value={diTxt("DI1F31")} />
        <StripItem label="Selic" value={(m?.selic ?? fb.selic) ? `${n((m?.selic ?? fb.selic)! * 100, 2)}%` : "—"} />
        <StripItem label="IPCA 12m" value={(m?.ipca12m?.value ?? fb.ipca12m) ? `${n((m?.ipca12m?.value ?? fb.ipca12m)! * 100, 2)}%` : "—"} />
        <span className="ml-auto shrink-0 whitespace-nowrap text-[11px] text-muted">
          {time ? `B3 e BCB ao vivo, ${time} (B3 com até 15 min de atraso)` : "Conectando às fontes…"}
        </span>
      </div>
    </div>
  );
}

export function Header({ fallback }: { fallback: MacroFallback }) {
  const path = usePathname();
  const ref = useRef<HTMLElement>(null);
  useEffect(() => {
    // altura real do cabeçalho fixo -> --header-h (cabeçalhos de tabela congelados ficam logo abaixo)
    const el = ref.current;
    if (!el) return;
    const set = () => document.documentElement.style.setProperty("--header-h", `${Math.round(el.getBoundingClientRect().height)}px`);
    set();
    const ro = new ResizeObserver(set);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return (
    <header ref={ref} className="no-print sticky top-0 z-40">
      <div className="border-b border-hairline bg-surface">
        <div className="mx-auto flex max-w-[1440px] flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3 sm:px-6">
          <Link href="/" className="flex items-baseline gap-2 whitespace-nowrap">
            <span className="text-[17px] font-semibold tracking-[-0.01em]">E agora?</span>
            <span className="hidden text-[12px] text-muted lg:inline">Valuation pós-eleição, 26 de outubro de 2026</span>
          </Link>
          <nav className="order-3 flex w-full items-center gap-0.5 overflow-x-auto sm:order-none sm:w-auto sm:gap-1">
            {NAV.map((n) => {
              const active = n.href === "/" ? path === "/" : path.startsWith(n.href);
              return (
                <Link key={n.href} href={n.href} className={`shrink-0 whitespace-nowrap rounded px-1.5 py-1 text-[12.5px] sm:px-2.5 sm:text-[13px] ${active ? "bg-surface-2 font-medium text-ink" : "text-ink-2 hover:text-ink"}`}>
                  {n.label}
                </Link>
              );
            })}
          </nav>
          <div className="ml-auto flex items-center gap-3">
            <KeControl />
            <ThemeToggle />
          </div>
        </div>
      </div>
      <MarketStrip fb={fallback} />
    </header>
  );
}
