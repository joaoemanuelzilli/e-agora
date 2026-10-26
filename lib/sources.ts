// Fontes ao vivo (somente servidor). Primária: API oficial da B3 (cotacao.b3.com.br, atraso de até 15 min).
// Reservas: Yahoo Finance (chart v8) e brapi (se BRAPI_TOKEN estiver configurado).
import type { Quote } from "./types";

const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36";

async function getJSON(url: string, ms = 6000): Promise<unknown | null> {
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), ms);
  try {
    const r = await fetch(url, { headers: { "User-Agent": UA, Accept: "application/json" }, signal: ctl.signal, cache: "no-store" });
    if (!r.ok) return null;
    return await r.json();
  } catch {
    return null;
  } finally {
    clearTimeout(t);
  }
}

type B3Resp = {
  BizSts?: { cd?: string };
  Msg?: { dtTm?: string };
  Trad?: { scty?: { SctyQtn?: { curPrc?: number; prcFlcn?: number } } }[];
};

export async function b3Quote(symbol: string): Promise<Quote | null> {
  const d = (await getJSON(`https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/${encodeURIComponent(symbol)}`)) as B3Resp | null;
  if (!d || d.BizSts?.cd !== "OK") return null;
  const q = d.Trad?.[0]?.scty?.SctyQtn;
  if (!q || typeof q.curPrc !== "number") return null;
  const chg = typeof q.prcFlcn === "number" ? q.prcFlcn / 100 : null;
  return {
    price: q.curPrc,
    chg,
    prevClose: chg !== null ? q.curPrc / (1 + chg) : null,
    ts: d.Msg?.dtTm ?? null,
    source: "B3",
  };
}

type YResp = { chart?: { result?: { meta?: { regularMarketPrice?: number; chartPreviousClose?: number; regularMarketTime?: number } }[] } };

export async function yahooQuote(symbol: string): Promise<Quote | null> {
  const ysym = symbol === "IBOV" ? "%5EBVSP" : `${symbol}.SA`;
  const d = (await getJSON(`https://query2.finance.yahoo.com/v8/finance/chart/${ysym}?range=1d&interval=1d`)) as YResp | null;
  const m = d?.chart?.result?.[0]?.meta;
  if (!m || typeof m.regularMarketPrice !== "number") return null;
  const prev = typeof m.chartPreviousClose === "number" ? m.chartPreviousClose : null;
  return {
    price: m.regularMarketPrice,
    chg: prev ? m.regularMarketPrice / prev - 1 : null,
    prevClose: prev,
    ts: m.regularMarketTime ? new Date(m.regularMarketTime * 1000).toISOString() : null,
    source: "Yahoo",
  };
}

type BrapiResp = { results?: { regularMarketPrice?: number; regularMarketPreviousClose?: number; regularMarketTime?: string }[] };

export async function brapiQuote(symbol: string): Promise<Quote | null> {
  const token = process.env.BRAPI_TOKEN;
  if (!token) return null;
  const d = (await getJSON(`https://brapi.dev/api/quote/${encodeURIComponent(symbol)}?token=${encodeURIComponent(token)}`)) as BrapiResp | null;
  const r = d?.results?.[0];
  if (!r || typeof r.regularMarketPrice !== "number") return null;
  const prev = typeof r.regularMarketPreviousClose === "number" ? r.regularMarketPreviousClose : null;
  return { price: r.regularMarketPrice, chg: prev ? r.regularMarketPrice / prev - 1 : null, prevClose: prev, ts: r.regularMarketTime ?? null, source: "brapi" };
}

export async function quote(symbol: string): Promise<Quote | null> {
  return (await b3Quote(symbol)) ?? (await yahooQuote(symbol)) ?? (await brapiQuote(symbol));
}

/** Executa tarefas com limite de concorrência. */
export async function pool<T, R>(items: T[], limit: number, fn: (x: T) => Promise<R>): Promise<R[]> {
  const out: R[] = new Array(items.length);
  let i = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (i < items.length) {
      const k = i++;
      out[k] = await fn(items[k]);
    }
  });
  await Promise.all(workers);
  return out;
}

type SGS = { data: string; valor: string }[];

export async function sgs(code: number, n = 1): Promise<SGS | null> {
  const d = (await getJSON(`https://api.bcb.gov.br/dados/serie/bcdata.sgs.${code}/dados/ultimos/${n}?formato=json`, 8000)) as SGS | null;
  return Array.isArray(d) ? d : null;
}

/** Contratos futuros: código do mês (F=jan … Z=dez). */
const MONTH = "FGHJKMNQUVXZ";
export function futureCodes(prefix: string, from: Date, count: number): string[] {
  const out: string[] = [];
  let y = from.getUTCFullYear();
  let m = from.getUTCMonth() + 1; // próximo mês
  for (let i = 0; i < count; i++) {
    if (m > 11) {
      m -= 12;
      y += 1;
    }
    out.push(`${prefix}${MONTH[m]}${String(y).slice(2)}`);
    m += 1;
  }
  return out;
}
