// Utilitários compartilhados pelos testes node --test (não é um arquivo de teste).
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const PYTHON = process.env.PYTHON || path.join(ROOT, ".venv", "bin", "python");

export const readJSON = (rel) => JSON.parse(fs.readFileSync(path.join(ROOT, rel), "utf8"));

/**
 * Carrega um módulo TypeScript de lib/ sem alterá-lo: transpila em memória com o TypeScript local
 * (devDependency) e, na falta dele, com `npx --yes esbuild`. Só serve para módulos sem imports de valor
 * (lib/valuation.ts importa apenas tipos).
 */
export async function loadTs(rel) {
  const file = path.join(ROOT, rel);
  const src = fs.readFileSync(file, "utf8");
  let js;
  try {
    const ts = createRequire(path.join(ROOT, "package.json"))("typescript");
    js = ts.transpileModule(src, {
      compilerOptions: { module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 },
      fileName: path.basename(file),
    }).outputText;
  } catch {
    js = execFileSync("npx", ["--yes", "esbuild@0.24.0", file, "--format=esm", "--platform=node", "--log-level=error"], {
      cwd: ROOT,
      encoding: "utf8",
    });
  }
  return import("data:text/javascript;base64," + Buffer.from(js).toString("base64"));
}

/** Roda tests/pyref.py (lado Python, pipeline/model.py) nos Ke pedidos. */
export function pyReference(kes) {
  const out = execFileSync(PYTHON, ["-I", "-W", "ignore", path.join(ROOT, "tests", "pyref.py"), ...kes.map(String)], {
    cwd: ROOT,
    encoding: "utf8",
    maxBuffer: 256 * 1024 * 1024,
    env: { ...process.env, EAGORA_SNAPSHOT: "1", PYTHONDONTWRITEBYTECODE: "1" },
  });
  return JSON.parse(out);
}

export const fin = (x) => typeof x === "number" && Number.isFinite(x);

/** Igualdade com tolerância relativa (0,5%) + meia unidade da 4ª casa (arredondamento do overview.json). */
export function close(a, b, rel = 0.005, abs = 5e-5) {
  if (a === null || a === undefined || b === null || b === undefined) return (a ?? null) === (b ?? null);
  if (!fin(a) || !fin(b)) return false;
  return Math.abs(a - b) <= rel * Math.abs(b) + abs;
}

export const fmt = (x, d = 4) => (x === null || x === undefined ? "null" : fin(x) ? x.toFixed(d) : String(x));
