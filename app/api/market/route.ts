import { futureCodes, pool, quote, sgs } from "@/lib/sources";
import type { Quote } from "@/lib/types";

export const dynamic = "force-dynamic";

const INDICES = ["IBOV", "SMLL", "IFNC", "IMOB", "ICON", "IEEX"];
const DI = ["DI1F27", "DI1F28", "DI1F29", "DI1F31", "DI1F33", "DI1F35"];

export async function GET() {
  const now = new Date();
  const dol = futureCodes("DOL", now, 2);
  const symbols = [...INDICES, ...DI, ...dol];
  const [res, selic, cdi, ipca, ptax] = await Promise.all([
    pool(symbols, 14, async (s) => [s, await quote(s)] as const),
    sgs(432),
    sgs(12),
    sgs(13522),
    sgs(1),
  ]);
  const q: Record<string, Quote | null> = Object.fromEntries(res);
  // dólar: contrato mais curto com cotação
  const dolKey = dol.find((k) => q[k]) || null;
  const cdiDaily = cdi?.[0] ? Number(cdi[0].valor) / 100 : null;
  return Response.json(
    {
      asOf: new Date().toISOString(),
      indices: Object.fromEntries(INDICES.map((k) => [k, q[k]])),
      di: DI.map((k) => ({ code: k, rate: q[k]?.price ?? null, chg: q[k]?.chg ?? null })),
      dollar: dolKey ? { code: dolKey, price: (q[dolKey] as Quote).price / 1000, chg: (q[dolKey] as Quote).chg } : null,
      selic: selic?.[0] ? Number(selic[0].valor) / 100 : null,
      cdi: cdiDaily !== null ? Math.pow(1 + cdiDaily, 252) - 1 : null,
      ipca12m: ipca?.[0] ? { value: Number(ipca[0].valor) / 100, ref: ipca[0].data } : null,
      ptax: ptax?.[0] ? { value: Number(ptax[0].valor), date: ptax[0].data } : null,
    },
    { headers: { "Cache-Control": "public, s-maxage=30, stale-while-revalidate=90" } },
  );
}
