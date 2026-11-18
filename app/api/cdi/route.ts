import { sgsRange } from "@/lib/sources";

export const dynamic = "force-dynamic";

const ISO = /^\d{4}-\d{2}-\d{2}$/;

/** CDI diário realizado (SGS 12, % ao dia) desde `from` até hoje: uma taxa por dia útil. */
export async function GET(req: Request) {
  const from = new URL(req.url).searchParams.get("from") || "";
  if (!ISO.test(from) || Number.isNaN(Date.parse(from))) return Response.json({ error: "from=AAAA-MM-DD" }, { status: 400 });
  const today = new Date().toLocaleDateString("sv-SE", { timeZone: "America/Sao_Paulo" });
  // janela limitada: o acompanhamento começa no registro de 28/10/2026; nada pede mais que ~2 anos de CDI diário
  const minFrom = new Date(Date.now() - 800 * 864e5).toISOString().slice(0, 10);
  if (from < minFrom || from > today) return Response.json({ error: "from fora da faixa permitida" }, { status: 400 });
  const obs = await sgsRange(12, from, today);
  if (!obs) return Response.json({ error: "Banco Central indisponível" }, { status: 502 });
  return Response.json(
    { from, asOf: new Date().toISOString(), days: obs.map((o) => ({ d: o.d, r: o.v / 100 })) },
    { headers: { "Cache-Control": "public, s-maxage=1800, stale-while-revalidate=3600" } },
  );
}
