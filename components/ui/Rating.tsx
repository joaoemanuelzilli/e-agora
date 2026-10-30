import { brl, pct } from "@/lib/format";

const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);

export type Tone = "strong" | "in" | "out" | "none";
export type Call = { tone: Tone; call: string; detail: string; gap: number | null };

/** Recomendação a partir do preço, do preço-teto e do teto de compra forte (Ke + 5 p.p.). */
export function callOf(price: number | null | undefined, ceiling: number | null | undefined, strong?: number | null): Call {
  if (!fin(price) || !fin(ceiling)) return { tone: "none", call: "Sem teto", detail: "sem preço-teto calculável", gap: null };
  if (fin(strong) && price <= strong) return { tone: "strong", call: "Compra forte", detail: "abaixo do teto de compra forte", gap: ceiling / price - 1 };
  if (price <= ceiling) return { tone: "in", call: "Compra", detail: "na faixa de compra", gap: ceiling / price - 1 };
  return { tone: "out", call: "Aguardar", detail: `acima do teto: falta cair ${pct(1 - ceiling / price, 1)}`, gap: ceiling / price - 1 };
}

/** Caixa de recomendação da nota: COMPRA / AGUARDAR, preço-teto e upside até o valor justo. */
export function Rating({ c, ceiling, upside, size = "md", className = "" }: { c: Call; ceiling: number | null | undefined; upside?: number | null; size?: "sm" | "md"; className?: string }) {
  return (
    <div className={`rating ${size === "sm" ? "text-[12px]" : ""} ${className}`} data-tone={c.tone} title={c.detail}>
      <div className="rating-call">{c.call}</div>
      <div className="rating-cell">
        <span>Preço-teto</span>
        <b className="num">{fin(ceiling) ? brl(ceiling) : "—"}</b>
      </div>
      {upside !== undefined && (
        <div className="rating-cell">
          <span>Upside</span>
          <b className={`num ${fin(upside) && upside < 0 ? "neg" : ""}`}>{fin(upside) ? pct(upside, 0, true) : "—"}</b>
        </div>
      )}
    </div>
  );
}

const STATUS_TONE: Record<string, { tone: Tone; call: string }> = {
  "compra forte": { tone: "strong", call: "Compra forte" },
  "na faixa": { tone: "in", call: "Compra" },
  "acima do teto": { tone: "out", call: "Aguardar" },
  "sem preço-teto": { tone: "none", call: "Sem teto" },
};

/** Carimbo compacto (só a recomendação), para tabelas densas. */
export function CallChip({ status, children }: { status: string; children?: React.ReactNode }) {
  const t = STATUS_TONE[status] ?? { tone: "none" as Tone, call: status };
  return (
    <span className="inline-flex flex-wrap items-center gap-x-2 gap-y-0.5">
      <span className="rating" data-tone={t.tone}>
        <span className="rating-call !px-2 !py-[3px] !text-[12px]">{t.call}</span>
      </span>
      {children}
    </span>
  );
}
