// Paridade do motor TS (lib/valuation.ts) com o Python (pipeline/model.py) — docs/model-spec.md.
// node --test tests/engine_parity.test.mjs
import { describe, test } from "node:test";
import assert from "node:assert/strict";
import { close, fin, fmt, loadTs, pyReference, readJSON } from "./_helpers.mjs";

const V = await loadTs("lib/valuation.ts");
const ov = readJSON("data/app/overview.json");
const REF = pyReference([0.2, 0.25, 0.3]);
const ENG_MODEL = REF._engines_from_model || {};

const pct = (a, b) => (fin(a) && fin(b) && b !== 0 ? `${(((a - b) / Math.abs(b)) * 100).toFixed(3)}%` : "n/d");
const why3y = (e) => {
  if (!e?.eps) return "";
  const hints = [];
  if (!(e.eps[1] > 0)) hints.push(`LPA 2027E = ${fmt(e.eps[1])} ≤ 0: o TS reconstrói o P/L alvo como values_share.pe / eps[1] e exige eps[1] > 0; o Python só exige P/L alvo e LPA 2029E > 0`);
  if (!fin(e.values_share?.pe)) hints.push("values_share.pe ausente no motor (engine.pe_target = null)");
  return hints.length ? ` — ${hints.join("; ")}` : "";
};

describe("Paridade TS × Python gravado (overview.json, Ke 25%, preço = price_ref)", () => {
  for (const c of ov.companies) {
    const e = c.engine;
    test(`${c.ticker} fairValue(e, 25%) = fair_value`, () => {
      const ts = V.fairValue(e, 0.25);
      assert.ok(close(ts, c.fair_value), `${c.ticker} [${c.template}] fairValue TS=${fmt(ts)} × Python=${fmt(c.fair_value)} (dif. ${pct(ts, c.fair_value)}; tolerância 0,5%)`);
    });
    test(`${c.ticker} irrImplied(e, preço) = irr_implied`, () => {
      const ts = V.irrImplied(e, c.price_ref);
      assert.ok(close(ts, c.irr_implied), `${c.ticker} irrImplied TS=${fmt(ts)} × Python=${fmt(c.irr_implied)} (preço ${c.price_ref}; dif. ${pct(ts, c.irr_implied)})`);
    });
    test(`${c.ticker} irr3y(e, preço) = irr_3y`, () => {
      const ts = V.irr3y(e, c.price_ref);
      assert.ok(close(ts, c.irr_3y), `${c.ticker} irr3y TS=${fmt(ts)} × Python=${fmt(c.irr_3y)} (preço ${c.price_ref})${why3y(e)}`);
    });
    test(`${c.ticker} upside do painel (live) = upside`, () => {
      const m = V.live(e, c.price_ref, 0.25, c.mc_q, c.fair_value);
      assert.ok(close(m.upside, c.upside), `${c.ticker} upside TS=${fmt(m.upside)} × Python=${fmt(c.upside)}`);
    });
  }
});

/** Diferença entre dois motores (números com tolerância relativa 1e-6); devolve o primeiro campo divergente. */
function engineDiff(a, b, path = "engine") {
  if (fin(a) && fin(b)) return Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(b)) ? null : `${path}: ${a} × ${b}`;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return `${path}: tamanhos diferentes`;
    for (let i = 0; i < a.length; i++) {
      const d = engineDiff(a[i], b[i], `${path}[${i}]`);
      if (d) return d;
    }
    return null;
  }
  if (a && b && typeof a === "object" && typeof b === "object") {
    for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
      const d = engineDiff(a[k] ?? null, b[k] ?? null, `${path}.${k}`);
      if (d) return d;
    }
    return null;
  }
  return (a ?? null) === (b ?? null) ? null : `${path}: ${a} × ${b}`;
}

describe("Paridade TS × Python recalculado com model.py (Ke 20% e 30%)", () => {
  for (const ke of [0.2, 0.3]) {
    for (const c of ov.companies) {
      const py = REF[String(ke)]?.[c.ticker] || {};
      const py25 = REF["0.25"]?.[c.ticker] || {};
      const stored = readJSON(`data/model/${c.ticker}.json`);
      // 1) data/model precisa ser reproduzível pelas premissas atuais (senão a revisão ainda não rodou o model.py)
      const modelStale = !py25.error && ["fair_value", "irr_implied", "irr_3y"].some((k) => !close(py25[k], stored[k] ?? null));
      // 2) motor do app × motor reconstruído do data/model atual (data/app desatualizado → usa o reconstruído)
      const rebuilt = ENG_MODEL[c.ticker];
      const appStale = rebuilt ? engineDiff(c.engine, rebuilt) : null;
      const e = appStale ? rebuilt : c.engine;
      const tag = appStale ? " [motor reconstruído de data/model: data/app desatualizado]" : "";
      const skip = modelStale ? "data/model desatualizado em relação a research/hist (ver test_modelo_reproduzivel_a_partir_das_premissas)" : false;
      test(`${c.ticker} fairValue(e, ${ke * 100}%) = model.py${tag}`, { skip }, () => {
        assert.ok(!py.error, `${c.ticker} erro no lado Python: ${py.error}`);
        const ts = V.fairValue(e, ke);
        const extra =
          c.template === "holding"
            ? ` — holding: o TS devolve o valor fixo de Ke 25% (${fmt(e.fair_value)}) para qualquer Ke; no Python o SOTP muda com Ke (controladas "fair" e custo de holding / (Ke − g))`
            : "";
        assert.ok(close(ts, py.fair_value), `${c.ticker} [${c.template}] Ke ${ke * 100}%: TS=${fmt(ts)} × Python=${fmt(py.fair_value)} (dif. ${pct(ts, py.fair_value)})${extra}${appStale ? ` [${appStale}]` : ""}`);
      });
    }
  }
});

describe("Coerência interna do motor TS", () => {
  for (const c of ov.companies) {
    const e = c.engine;
    if (!e || e.template === "holding") continue;
    const ddm25 = V.ddmPerShare(e, 0.25);
    const skip = fin(ddm25) && ddm25 > 0 ? false : `DDM(25%) por ação = ${fmt(ddm25)} ≤ 0 (lucro terminal negativo): não há preço positivo para a ida e volta`;
    test(`${c.ticker} TIR implícita no preço = DDM(25%) devolve 25%`, { skip }, () => {
      const p = ddm25;
      const r = V.irrImplied(e, p * (e.per_unit || 1));
      assert.ok(fin(r) && Math.abs(r - 0.25) < 1e-4, `${c.ticker} irrImplied(DDM a 25%) = ${fmt(r, 6)} (esperado 0,25)`);
    });
    test(`${c.ticker} valor justo não cresce com o Ke (20% ≥ 25% ≥ 30%)`, () => {
      const [a, b, d] = [0.2, 0.25, 0.3].map((k) => V.fairValue(e, k));
      assert.ok(fin(a) && fin(b) && fin(d) && a >= b - 1e-9 && b >= d - 1e-9, `${c.ticker} fairValue: Ke20 ${fmt(a)} | Ke25 ${fmt(b)} | Ke30 ${fmt(d)}`);
    });
  }
  test("probAbove: monotônica no preço e 50% na mediana dos quantis", () => {
    for (const c of ov.companies) {
      const q = c.mc_q;
      if (!q) continue;
      const ps = [0.5, 0.8, 1, 1.25, 2].map((k) => V.probAbove(q, q[50] * k));
      for (let i = 1; i < ps.length; i++) assert.ok(ps[i] <= ps[i - 1] + 1e-12, `${c.ticker} probAbove não monotônica: ${ps.map((x) => fmt(x)).join(", ")}`);
      assert.ok(Math.abs(V.probAbove(q, q[50]) - 0.5) <= 0.011, `${c.ticker} probAbove(mediana) = ${fmt(V.probAbove(q, q[50]))}`);
    }
  });
  for (const c of ov.companies) {
    if (!c.mc_q || !fin(c.prob_mc)) continue;
    test(`${c.ticker} P(valor > preço) do painel (quantis) ≈ Monte Carlo do Python (±5 p.p.)`, () => {
      const p = V.probAbove(c.mc_q, c.price_ref);
      assert.ok(fin(p) && Math.abs(p - c.prob_mc) <= 0.05, `${c.ticker} probAbove(mc_q)=${fmt(p)} × prob_mc=${fmt(c.prob_mc)} (quantis vêm de 400 amostras das 5.000)`);
    });
  }
});
