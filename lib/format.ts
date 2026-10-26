const nf = (d: number) => new Intl.NumberFormat("pt-BR", { minimumFractionDigits: d, maximumFractionDigits: d });
const cache = new Map<number, Intl.NumberFormat>();
function fmtN(d: number) {
  let f = cache.get(d);
  if (!f) {
    f = nf(d);
    cache.set(d, f);
  }
  return f;
}

export const isNum = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);

/** Número com casas fixas, em pt-BR. */
export function num(x: number | null | undefined, d = 2): string {
  return isNum(x) ? fmtN(d).format(x) : "—";
}

/** Percentual a partir de fração (0,25 → 25,0%). */
export function pct(x: number | null | undefined, d = 1, signed = false): string {
  if (!isNum(x)) return "—";
  const s = fmtN(d).format(x * 100);
  return `${signed && x > 0 ? "+" : ""}${s}%`;
}

/** Preço em reais. */
export function brl(x: number | null | undefined, d = 2): string {
  return isNum(x) ? `R$ ${fmtN(d).format(x)}` : "—";
}

/** Valores em R$ milhões, compactos (bi quando ≥ 1.000). */
export function mn(x: number | null | undefined): string {
  if (!isNum(x)) return "—";
  const a = Math.abs(x);
  if (a >= 1000) return `${fmtN(a >= 100000 ? 0 : 1).format(x / 1000)} bi`;
  return `${fmtN(0).format(x)} mi`;
}

/** Múltiplo (8,4x). */
export function mult(x: number | null | undefined, d = 1): string {
  return isNum(x) ? `${fmtN(d).format(x)}x` : "—";
}

export function signClass(x: number | null | undefined): string {
  if (!isNum(x) || Math.abs(x) < 1e-9) return "";
  return x > 0 ? "pos" : "neg";
}

export function dateBR(iso: string): string {
  const [y, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${y}`;
}

const MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
export function monthYear(iso: string): string {
  const [y, m] = iso.split("-");
  return `${MESES[Number(m) - 1]}/${y.slice(2)}`;
}
