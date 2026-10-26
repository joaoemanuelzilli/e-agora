// (5) Rotas do app com `next start` já rodando (tests/run_all.sh sobe e derruba o servidor na porta 3300).
// BASE_URL=http://localhost:3300 node --test tests/app_routes.test.mjs
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { readJSON } from "./_helpers.mjs";

const BASE = process.env.BASE_URL || "http://localhost:3300";
const ov = readJSON("data/app/overview.json");

async function get(path, timeout = 60000) {
  const t0 = Date.now();
  const res = await fetch(BASE + path, { signal: AbortSignal.timeout(timeout), redirect: "manual" });
  const body = await res.text();
  return { status: res.status, type: res.headers.get("content-type") || "", body, ms: Date.now() - t0 };
}

async function page(path, mustContain) {
  const r = await get(path);
  assert.equal(r.status, 200, `${path} respondeu HTTP ${r.status} em ${r.ms} ms`);
  assert.match(r.type, /text\/html/, `${path} content-type ${r.type}`);
  assert.ok(!/Application error|Internal Server Error/i.test(r.body), `${path} contém página de erro`);
  if (mustContain) assert.ok(r.body.includes(mustContain), `${path} não menciona ${mustContain}`);
}

describe("Páginas", () => {
  for (const p of ["/", "/dividendos", "/mercado", "/metodologia"]) test(`GET ${p} → 200`, () => page(p));
  for (const c of ov.companies) test(`GET /empresa/${c.ticker} → 200`, () => page(`/empresa/${c.ticker}`, c.ticker));
  for (const t of ov.opportunities) test(`GET /relatorio/${t} → 200`, () => page(`/relatorio/${t}`, t));
  test("GET /empresa/XXXX3 (fora da cobertura) → 404", async () => {
    const r = await get("/empresa/XXXX3");
    assert.equal(r.status, 404, `HTTP ${r.status}`);
  });
});

describe("APIs ao vivo", () => {
  test("GET /api/quotes?t=RENT3 → JSON válido", async () => {
    const r = await get("/api/quotes?t=RENT3", 90000);
    assert.equal(r.status, 200, `HTTP ${r.status}`);
    assert.match(r.type, /application\/json/, `content-type ${r.type}`);
    const j = JSON.parse(r.body);
    assert.ok(typeof j.asOf === "string" && !Number.isNaN(Date.parse(j.asOf)), `asOf ${j.asOf}`);
    assert.ok(j.quotes && typeof j.quotes === "object" && j.sources && typeof j.sources === "object", `estrutura ${Object.keys(j)}`);
    const q = j.quotes.RENT3;
    if (q) {
      assert.ok(q.price > 0, `preço RENT3 ${q.price}`);
      assert.ok(typeof q.source === "string", `fonte ${q.source}`);
    } else {
      // sem rede: a rota ainda devolve JSON; registra a situação na saída do teste
      console.log("aviso: /api/quotes sem cotação de RENT3 (fontes externas indisponíveis?)");
    }
  });
  test("GET /api/market → JSON válido", async () => {
    const r = await get("/api/market", 90000);
    assert.equal(r.status, 200, `HTTP ${r.status}`);
    assert.match(r.type, /application\/json/, `content-type ${r.type}`);
    const j = JSON.parse(r.body);
    for (const k of ["asOf", "indices", "di", "dollar", "selic", "cdi", "ipca12m", "ptax"]) assert.ok(k in j, `chave ${k} ausente`);
    assert.ok(Array.isArray(j.di) && j.di.length === 6, `curva DI ${JSON.stringify(j.di)}`);
    for (const d of j.di) assert.ok(d.rate === null || (d.rate > 0 && d.rate < 60), `DI ${d.code} ${d.rate}`);
    if (j.selic !== null) assert.ok(j.selic > 0 && j.selic < 0.6, `Selic ${j.selic}`);
    if (j.cdi !== null) assert.ok(j.cdi > 0 && j.cdi < 0.6, `CDI anualizado ${j.cdi}`);
  });
  test("GET /api/quotes sem tickers válidos → JSON vazio (validação de entrada)", async () => {
    const r = await get("/api/quotes?t=../../etc,%3Cscript%3E", 30000);
    assert.equal(r.status, 200, `HTTP ${r.status}`);
    const j = JSON.parse(r.body);
    assert.deepEqual(j.quotes, {}, `quotes ${JSON.stringify(j.quotes)}`);
  });
});
