import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { Overview } from "./types";
import { cleanName } from "./format";

const APP = path.join(process.cwd(), "data", "app");

let _overview: Overview | null = null;
export function getOverview(): Overview {
  if (!_overview) _overview = JSON.parse(fs.readFileSync(path.join(APP, "overview.json"), "utf8")) as Overview;
  return _overview;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Company = any;

export function getCompany(ticker: string): Company | null {
  const p = path.join(APP, "companies", `${ticker.toUpperCase()}.json`);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

export function tickers(): string[] {
  return getOverview().companies.map((c) => c.ticker);
}

let _div: unknown = null;
export function getDividends<T>(): T {
  if (!_div) _div = JSON.parse(fs.readFileSync(path.join(APP, "dividends.json"), "utf8"));
  return _div as T;
}

/** Registros congelados de recomendação (data/registro/*.json), do mais novo ao mais antigo. */
export function getRegistros<T>(): T[] {
  const dir = path.join(process.cwd(), "data", "registro");
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".json") && !f.startsWith("_"))
    .sort()
    .reverse()
    .map((f) => JSON.parse(fs.readFileSync(path.join(dir, f), "utf8")) as T);
}

/** Nome legível da companhia (research/{T}.json), sem "S.A." e sufixos societários: "Vitru Educação", "Plano & Plano". */
let _names: Record<string, string> | null = null;
export function displayNames(): Record<string, string> {
  if (_names) return _names;
  const out: Record<string, string> = {};
  for (const t of tickers()) {
    const p = path.join(process.cwd(), "research", `${t}.json`);
    if (!fs.existsSync(p)) continue;
    const n = cleanName(JSON.parse(fs.readFileSync(p, "utf8"))?.name);
    if (n) out[t] = n;
  }
  _names = out;
  return out;
}
