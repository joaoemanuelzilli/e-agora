import { pool, quote } from "@/lib/sources";
import type { Quote } from "@/lib/types";

export const dynamic = "force-dynamic";

const VALID = /^[A-Z0-9]{4,7}$/;

export async function GET(req: Request) {
  const url = new URL(req.url);
  const list = (url.searchParams.get("t") || "")
    .toUpperCase()
    .split(",")
    .map((s) => s.trim())
    .filter((s) => VALID.test(s));
  const tickers = Array.from(new Set(list)).slice(0, 90);
  const res = await pool(tickers, 16, async (t) => [t, await quote(t)] as const);
  const quotes: Record<string, Quote> = {};
  const sources: Record<string, number> = {};
  for (const [t, q] of res) {
    if (q) {
      quotes[t] = q;
      sources[q.source] = (sources[q.source] || 0) + 1;
    }
  }
  return Response.json(
    { asOf: new Date().toISOString(), sources, quotes },
    { headers: { "Cache-Control": "public, s-maxage=15, stale-while-revalidate=45" } },
  );
}
