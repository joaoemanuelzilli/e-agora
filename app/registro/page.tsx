import fs from "node:fs";
import path from "node:path";
import type { Metadata } from "next";
import { Desempenho, Ficha, type Registro } from "@/components/registro/Registro";

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

export default function Page() {
  const list = registros();
  return (
    <div className="space-y-8">
      <header>
        <h1 className="h1">Registro de recomendações</h1>
        <p className="mt-2 max-w-[72ch] text-[15px] text-ink-2">
          Cada recomendação fica congelada com os preços do dia em que foi feita, para medir depois se foi uma boa decisão: retorno das ações escolhidas e da carteira contra Ibovespa, Small Caps, CDI e as ações que ficaram de fora.
        </p>
      </header>
      {list.length === 0 && <div className="panel p-6 text-ink-2">Nenhum registro ainda.</div>}
      {list.map((r) => {
        const png = `/registro/recomendacoes-${r.id}.png`;
        const hasPng = fs.existsSync(path.join(process.cwd(), "public", png));
        return (
          <div key={r.id} className="space-y-6">
            <Ficha r={r} />
            {hasPng && (
              <div className="text-right text-[13px]">
                <a href={png} download className="font-medium text-accent hover:underline">
                  Baixar a imagem deste registro
                </a>
              </div>
            )}
            <Desempenho r={r} />
          </div>
        );
      })}
    </div>
  );
}
