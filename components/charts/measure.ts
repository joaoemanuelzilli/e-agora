/* Medida de texto determinística para rótulos SVG (igual no servidor e no cliente, sem canvas).
   Larguras em em da Libre Franklin 400, medidas no navegador; peso 600+ soma ~3%. */
const W: Record<string, number> = {
  " ": 0.215, ".": 0.21, ",": 0.21, ";": 0.23, ":": 0.21, "-": 0.38, "–": 0.56, "−": 0.56, "+": 0.56, "%": 0.92, "/": 0.34, "(": 0.29, ")": 0.29,
  "×": 0.54, "÷": 0.56, "√": 0.55, "…": 0.75, "≥": 0.55, "≤": 0.55, "=": 0.56, "<": 0.54, ">": 0.54, "·": 0.2, "'": 0.24, '"': 0.41, "&": 0.78, "$": 0.61, "º": 0.41, "ª": 0.4, "Δ": 0.67,
  0: 0.69, 1: 0.47, 2: 0.6, 3: 0.64, 4: 0.65, 5: 0.65, 6: 0.66, 7: 0.6, 8: 0.67, 9: 0.66,
  a: 0.55, b: 0.6, c: 0.54, d: 0.6, e: 0.58, f: 0.38, g: 0.6, h: 0.58, i: 0.24, j: 0.24, k: 0.56, l: 0.24, m: 0.91, n: 0.58, o: 0.6, p: 0.6, q: 0.6, r: 0.38, s: 0.51, t: 0.39, u: 0.58, v: 0.55, w: 0.8, x: 0.54, y: 0.53, z: 0.48,
  A: 0.73, B: 0.7, C: 0.71, D: 0.72, E: 0.63, F: 0.6, G: 0.74, H: 0.74, I: 0.29, J: 0.42, K: 0.7, L: 0.6, M: 0.91, N: 0.76, O: 0.76, P: 0.69, Q: 0.77, R: 0.7, S: 0.64, T: 0.65, U: 0.71, V: 0.71, W: 1.05, X: 0.69, Y: 0.68, Z: 0.63,
};

function em(c: string) {
  const v = W[c];
  if (v !== undefined) return v;
  const base = c.normalize("NFD")[0]; // á → a, Ç → C
  return W[base] ?? 0.6;
}

/** Largura estimada (px) de um texto SVG. */
export function textW(s: string, size = 12, weight = 400) {
  let e = 0;
  for (const c of s) e += em(c);
  return e * size * (weight >= 600 ? 1.03 : 1) * 1.02;
}

/** Corta com reticências até caber em maxW (px). */
export function ellipsize(s: string, maxW: number, size = 12, weight = 400) {
  if (textW(s, size, weight) <= maxW) return s;
  const chars = [...s];
  for (let n = chars.length - 1; n > 0; n--) {
    const t = chars.slice(0, n).join("").trimEnd() + "…";
    if (textW(t, size, weight) <= maxW) return t;
  }
  return "…";
}

/** Quebra por palavras em até maxLines linhas de maxW px. `fits` = coube sem cortar; senão a última linha leva reticências. */
export function wrapText(s: string, maxW: number, size = 12, maxLines = 2, weight = 400): { lines: string[]; fits: boolean } {
  const words = s.split(/\s+/).filter(Boolean);
  const lines: string[] = [];
  let cur = "";
  let i = 0;
  for (; i < words.length; i++) {
    const next = cur ? `${cur} ${words[i]}` : words[i];
    if (textW(next, size, weight) <= maxW) {
      cur = next;
      continue;
    }
    if (cur) {
      lines.push(cur);
      cur = words[i];
    } else {
      cur = words[i]; // palavra sozinha maior que a linha
    }
    if (lines.length === maxLines) break;
  }
  if (lines.length < maxLines && cur) {
    lines.push(cur);
    cur = "";
    i = words.length;
  }
  const rest = i < words.length;
  const tooWide = lines.some((l) => textW(l, size, weight) > maxW);
  if (!rest && !tooWide) return { lines, fits: true };
  const out = lines.slice(0, maxLines);
  const last = [out[out.length - 1], ...(rest ? words.slice(i) : [])].join(" ");
  out[out.length - 1] = ellipsize(last + (rest ? " " : ""), maxW, size, weight);
  for (let k = 0; k < out.length - 1; k++) out[k] = ellipsize(out[k], maxW, size, weight);
  return { lines: out, fits: false };
}

/** Passo entre rótulos de categoria para não encostarem (1 = todos). */
export function labelStride(labels: string[], step: number, size = 11, gap = 6) {
  const mw = Math.max(0, ...labels.map((l) => textW(l, size)));
  return Math.max(1, Math.ceil((mw + gap) / Math.max(1, step)));
}

/** Ticks lineares que cabem na largura: reduz a contagem até os rótulos não encostarem e remove rótulos repetidos. */
export function fitTicks(scale: { ticks: (n: number) => number[]; (v: number): number }, fmt: (v: number) => string, start = 5, size = 11, gap = 10) {
  for (let n = start; n >= 2; n--) {
    const raw = scale.ticks(n);
    const seen = new Set<string>();
    const ts = raw.filter((t) => {
      const k = fmt(t);
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });
    let ok = true;
    for (let k = 1; k < ts.length; k++) {
      const need = (textW(fmt(ts[k - 1]), size) + textW(fmt(ts[k]), size)) / 2 + gap;
      if (scale(ts[k]) - scale(ts[k - 1]) < need) {
        ok = false;
        break;
      }
    }
    if (ok) return ts;
  }
  const t = scale.ticks(2);
  return t.length > 2 ? [t[0], t[t.length - 1]] : t;
}

export type Gap = { x1: number; y0: number; y1: number };
/** Segmentos [y0,y1] de uma linha vertical em x, interrompida onde cruzaria um rótulo (caixas que começam em x=0). */
export function lineSegs(xp: number, y0: number, y1: number, gaps: Gap[]): [number, number][] {
  const out: [number, number][] = [];
  let cur = y0;
  for (const g of [...gaps].sort((a, b) => a.y0 - b.y0)) {
    if (xp > g.x1 || g.y1 <= cur || g.y0 >= y1) continue;
    if (g.y0 > cur) out.push([cur, g.y0]);
    cur = Math.max(cur, g.y1);
  }
  if (cur < y1) out.push([cur, y1]);
  return out;
}

/** Rótulos de um eixo de categorias: todos se couberem; anos de 4 dígitos viram 2 ("2017" → "17", como "26E");
    senão, 1 a cada N, ancorado no último (o mais recente). */
export function categoryLabels(labels: string[], step: number, size = 11): string[] {
  const stride = labelStride(labels, step, size);
  if (stride === 1) return labels;
  const short = labels.map((l) => l.replace(/^(?:19|20)(\d\d)(E?)$/, "$1$2"));
  if (short.some((s, i) => s !== labels[i]) && labelStride(short, step, size, 4) === 1) return short;
  const n = labels.length;
  return labels.map((l, i) => ((n - 1 - i) % stride === 0 ? l : ""));
}
