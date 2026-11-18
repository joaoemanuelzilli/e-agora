import fs from "node:fs";
import path from "node:path";
import type { Metadata } from "next";
import { Desempenho, Ficha, type DivMap, type Registro } from "@/components/registro/Registro";
import { displayNames, getDividends } from "@/lib/data";

export const metadata: Metadata = { title: "Registro de recomendações" };

function registros(): Registro[] {
  const dir = path.join(process.cwd(), "data", "registro");
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json") && !f.startsWith("_"))
    .sort()
    .reverse()
    .map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")) as Registro);
}

type DivFile = { gerado_em?: string; empresas?: { ticker: string; eventos?: { dc?: string; valor?: number }[]; a_pagar?: { dc?: string; valor?: number }[] }[] };

/** Proventos com data-com depois da data de referência, por ação (eventos da B3 e pagamentos anunciados, sem repetir a mesma data-com). */
function proventosDesde(ref: string): { divs: DivMap | null; asOf: string | null } {
  let f: DivFile;
  try {
    f = getDividends<DivFile>();
  } catch {
    return { divs: null, asOf: null };
  }
  if (!Array.isArray(f?.empresas)) return { divs: null, asOf: null };
  const divs: DivMap = {};
  for (const e of f.empresas) {
    const seen = new Set<string>();
    for (const ev of [...(e.eventos ?? []), ...(e.a_pagar ?? [])]) {
      if (typeof ev.dc !== "string" || typeof ev.valor !== "number" || ev.dc <= ref) continue;
      const k = `${ev.dc}|${ev.valor.toFixed(4)}`;
      if (seen.has(k)) continue;
      seen.add(k);
      (divs[e.ticker] ??= []).push({ dc: ev.dc, valor: ev.valor });
    }
  }
  return { divs, asOf: typeof f.gerado_em === "string" ? f.gerado_em.slice(0, 10) : null };
}

export default function Page() {
  const list = registros();
  return (
    <div className="space-y-8">
      <header>
        <h1 className="h1">Registro de recomendações</h1>
        <p className="mt-2 max-w-[68ch] text-[15px] text-ink-2">
          Cada lista fica congelada com os preços de referência e a regra do dia, para medir depois se foi uma boa decisão: retorno das ações escolhidas e da carteira-alvo contra Ibovespa, Small Caps, CDI, uma referência com a mesma parcela em ações e as ações que ficaram de fora.
        </p>
      </header>
      {list.length === 0 && <div className="panel p-6 text-ink-2">Nenhum registro ainda.</div>}
      {list.map((r) => {
        const png = `/registro/recomendacoes-${r.id}.png`;
        const hasPng = fs.existsSync(path.join(process.cwd(), "public", png));
        const pv = proventosDesde(r.data_ref);
        return (
          <div key={r.id} className="space-y-6">
            <Ficha r={r} names={displayNames()} />
            {hasPng && (
              <div className="text-right text-[13px]">
                <a href={png} download className="link">
                  Baixar a imagem deste registro
                </a>
              </div>
            )}
            <Desempenho r={r} divs={pv.divs} divsAsOf={pv.asOf} />
          </div>
        );
      })}
    </div>
  );
}
