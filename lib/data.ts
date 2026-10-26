import "server-only";
import fs from "node:fs";
import path from "node:path";
import type { Overview } from "./types";

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
