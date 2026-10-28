"use client";
import { createContext, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import type { Quote } from "./types";

type QuotesState = { quotes: Record<string, Quote>; asOf: string | null; loading: boolean; error: boolean };

function useVisibleInterval(fn: () => void, ms: number) {
  const ref = useRef(fn);
  ref.current = fn;
  useEffect(() => {
    let id: ReturnType<typeof setInterval> | null = null;
    const start = () => {
      ref.current();
      id = setInterval(() => ref.current(), ms);
    };
    const stop = () => id && clearInterval(id);
    const onVis = () => (document.hidden ? stop() : start());
    start();
    document.addEventListener("visibilitychange", onVis);
    return () => {
      stop();
      document.removeEventListener("visibilitychange", onVis);
    };
  }, [ms]);
}

/** Cotações ao vivo (API oficial da B3 via /api/quotes), atualizadas a cada `ms`. */
export function useQuotes(tickers: string[], ms = 30000): QuotesState {
  const key = useMemo(() => Array.from(new Set(tickers)).sort().join(","), [tickers]);
  const [st, setSt] = useState<QuotesState>({ quotes: {}, asOf: null, loading: true, error: false });
  useVisibleInterval(() => {
    if (!key) return;
    // a rota atende até 90 tickers por chamada: divide em lotes de 60 e junta as respostas
    const all = key.split(",");
    const chunks: string[][] = [];
    for (let i = 0; i < all.length; i += 60) chunks.push(all.slice(i, i + 60));
    Promise.allSettled(chunks.map((c) => fetch(`/api/quotes?t=${c.join(",")}`).then((r) => (r.ok ? r.json() : Promise.reject(r.status)))))
      .then((res) => {
        const ok = res.filter((x): x is PromiseFulfilledResult<{ quotes?: Record<string, Quote>; asOf: string }> => x.status === "fulfilled").map((x) => x.value);
        if (!ok.length) return setSt((s) => ({ ...s, loading: false, error: true }));
        setSt({ quotes: Object.assign({}, ...ok.map((d) => d.quotes || {})), asOf: ok[0].asOf, loading: false, error: ok.length < chunks.length });
      })
      .catch(() => setSt((s) => ({ ...s, loading: false, error: true })));
  }, ms);
  return st;
}

export type MarketLive = {
  asOf: string;
  indices: Record<string, Quote | null>;
  di: { code: string; rate: number | null; chg: number | null }[];
  dollar: { code: string; price: number; chg: number | null } | null;
  selic: number | null;
  cdi: number | null;
  ipca12m: { value: number; ref: string } | null;
  ptax: { value: number; date: string } | null;
};

export function useMarket(ms = 45000): MarketLive | null {
  const [st, setSt] = useState<MarketLive | null>(null);
  useVisibleInterval(() => {
    fetch("/api/market")
      .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
      .then((d) => setSt(d))
      .catch(() => {});
  }, ms);
  return st;
}

/* Ke global (meta do usuário = 25%), ajustável e lembrado no navegador. */
type KeCtx = { ke: number; setKe: (k: number) => void };
const Ctx = createContext<KeCtx>({ ke: 0.25, setKe: () => {} });

export function KeProvider({ children }: { children: ReactNode }) {
  const [ke, setKeState] = useState(0.25);
  useEffect(() => {
    try {
      const v = Number(localStorage.getItem("ke"));
      if (v >= 0.1 && v <= 0.4) setKeState(v);
    } catch {}
  }, []);
  const setKe = (k: number) => {
    setKeState(k);
    try {
      localStorage.setItem("ke", String(k));
    } catch {}
  };
  return <Ctx.Provider value={{ ke, setKe }}>{children}</Ctx.Provider>;
}
export const useKe = () => useContext(Ctx);
