// Motor de valuation em TypeScript — espelho de pipeline/model.py (mesmas fórmulas),
// usado para recalcular upside, TIR e valor justo com o preço ao vivo e com outro Ke.
import type { Engine } from "./types";

const TAX_SHIELD = 0.34;
// anos de 26/10/2026 a 31/12/2028 (saída da TIR de 3 anos)
const T_EXIT_3Y = (Date.UTC(2028, 11, 31) - Date.UTC(2026, 9, 26)) / (365.25 * 864e5);

const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);

export function ddmPerShare(e: Engine, ke: number): number | null {
  if (!e.div || !e.taus || !fin(e.g) || !fin(e.roe_T) || !fin(e.ni_last) || !fin(e.n_sh) || !fin(e.tau_T) || !fin(e.f26)) return null;
  const g = e.g;
  const roeT = Math.max(e.roe_T, g + 0.02);
  let pv = 0;
  e.div.forEach((d, i) => {
    const fl = i === 0 ? d * (e.f26 as number) : d;
    pv += fl / Math.pow(1 + ke, (e.taus as number[])[i]);
  });
  if (ke <= g) return null;
  const tv = (e.ni_last * (1 + g) * (1 - g / roeT)) / (ke - g);
  return (pv + tv / Math.pow(1 + ke, e.tau_T)) / e.n_sh;
}

export function waccOf(e: Engine, ke: number): number | null {
  if (!fin(e.wd) || !fin(e.kd)) return null;
  return (1 - e.wd) * ke + e.wd * e.kd * (1 - TAX_SHIELD);
}

export function dcfPerShare(e: Engine, ke: number): number | null {
  if (e.template === "financial" || !e.fcff || !e.taus) return null;
  const wacc = waccOf(e, ke);
  if (!fin(wacc) || !fin(e.g) || !fin(e.roic_T) || !fin(e.nopat_last) || !fin(e.tau_T) || !fin(e.f26) || !fin(e.n_sh)) return null;
  const g = e.g;
  if (wacc <= g) return null;
  const roicT = Math.max(e.roic_T, g + 0.02);
  let pv = 0;
  e.fcff.forEach((x, i) => {
    const fl = i === 0 ? x * (e.f26 as number) : x;
    pv += fl / Math.pow(1 + wacc, (e.taus as number[])[i]);
  });
  const tv = (e.nopat_last * (1 + g) * (1 - g / roicT)) / (wacc - g);
  const ev = pv + tv / Math.pow(1 + wacc, e.tau_T);
  const eq = ev - (e.nd_base ?? 0) - (e.minority_value ?? 0) + (e.eq_bridge_extra ?? 0);
  return eq / e.n_sh;
}

/** Valor justo por unidade negociada (ação ou unit), no Ke informado. */
export function fairValue(e: Engine | null, ke: number): number | null {
  if (!e) return null;
  if (e.template === "holding") return fin(e.fair_value) ? e.fair_value : null;
  const vals: Record<string, number | null> = { ...(e.values_share || {}) };
  vals.ddm = ddmPerShare(e, ke);
  if (e.template !== "financial") vals.dcf = dcfPerShare(e, ke);
  let acc = 0;
  let tot = 0;
  for (const [k, w] of Object.entries(e.weights || {})) {
    const x = vals[k];
    if (fin(x)) {
      acc += w * Math.max(0, x);
      tot += w;
    }
  }
  if (!tot) return null;
  return (acc / tot) * (e.per_unit || 1);
}

function bisect(fn: (r: number) => number, lo: number, hi: number, target: number, it = 70): number | null {
  const flo = fn(lo);
  const fhi = fn(hi);
  if (!fin(flo) || !fin(fhi)) return null;
  if (flo < target) return lo;
  if (fhi > target) return hi;
  for (let i = 0; i < it; i++) {
    const mid = (lo + hi) / 2;
    if (fn(mid) > target) lo = mid;
    else hi = mid;
  }
  return (lo + hi) / 2;
}

/** TIR de dono inteira: taxa que iguala o preço ao valor presente dos dividendos + perpetuidade. */
export function irrImplied(e: Engine | null, price: number | null): number | null {
  if (!e || e.template === "holding" || !fin(price) || !fin(e.g)) return null;
  const pSh = price / (e.per_unit || 1);
  const g = e.g;
  return bisect((r) => (r <= g + 1e-4 ? Infinity : ddmPerShare(e, r) ?? NaN), g + 0.002, 3.0, pSh);
}

/** TIR de 3 anos: dividendos 2026E(stub)–2028E e saída ao P/L alvo × LPA 2029E. */
export function irr3y(e: Engine | null, price: number | null): number | null {
  if (!e || e.template === "holding" || !fin(price) || !e.dps || !e.eps || !e.taus || !fin(e.f26)) return null;
  const peVal = e.values_share?.pe;
  if (!fin(peVal) || !fin(e.eps[1]) || e.eps[1] <= 0 || !fin(e.eps[3]) || e.eps[3] <= 0) return null;
  const peTarget = peVal / e.eps[1];
  const pSh = price / (e.per_unit || 1);
  const dps = e.dps;
  const taus = e.taus;
  const f26 = e.f26;
  const pv = (r: number) => {
    let s = 0;
    for (let i = 0; i < 3; i++) s += (i === 0 ? dps[i] * f26 : dps[i]) / Math.pow(1 + r, taus[i]);
    return s + (peTarget * (e.eps as number[])[3]) / Math.pow(1 + r, T_EXIT_3Y);
  };
  return bisect(pv, -0.9, 5.0, pSh);
}

/** P(valor justo > preço) a partir dos quantis do Monte Carlo (101 pontos, 0..100). */
export function probAbove(q: number[] | null | undefined, price: number | null, scale = 1): number | null {
  if (!q || q.length < 3 || !fin(price)) return null;
  const v = q.map((x) => x * scale);
  if (price <= v[0]) return 1;
  if (price >= v[v.length - 1]) return 0;
  for (let i = 1; i < v.length; i++) {
    if (v[i] >= price) {
      const t = (price - v[i - 1]) / (v[i] - v[i - 1] || 1);
      const pctile = (i - 1 + t) / (v.length - 1);
      return 1 - pctile;
    }
  }
  return 0;
}

export type LiveMetrics = {
  price: number | null;
  fair: number | null;
  upside: number | null;
  irr: number | null;
  irr3: number | null;
  prob: number | null;
  dy: number | null;
  pe: number | null;
};

/** Métricas ao preço vivo e no Ke escolhido. */
export function live(e: Engine | null, price: number | null, ke: number, mcQ?: number[] | null, fairRef?: number | null): LiveMetrics {
  const fair = fairValue(e, ke) ?? fairRef ?? null;
  const upside = fin(fair) && fin(price) && price > 0 ? fair / price - 1 : null;
  const irr = irrImplied(e, price);
  const irr3 = irr3y(e, price);
  const base = fairValue(e, e?.ke_base ?? 0.25);
  const scale = fin(fair) && fin(base) && base > 0 ? fair / base : 1;
  const prob = probAbove(mcQ, price, scale);
  const unit = e?.per_unit || 1;
  const dy = e?.dps && fin(price) && price > 0 ? (e.dps[1] * unit) / price : null;
  const pe = e?.eps && fin(price) && e.eps[1] > 0 ? price / unit / e.eps[1] : null;
  return { price, fair, upside, irr, irr3, prob, dy, pe };
}
