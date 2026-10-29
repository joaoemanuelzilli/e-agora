"use client";
import Link from "next/link";
import { useMemo } from "react";
import { useMarket, useQuotes } from "@/lib/live";
import { num, pct, signClass } from "@/lib/format";

export type Rec = {
  rank: number;
  ticker: string;
  nome: string;
  setor?: string | null;
  preco_ref: number;
  teto: number | null;
  compra_forte: number | null;
  valor_justo: number | null;
  upside: number | null;
  tir_dono: number | null;
  tir_3a: number | null;
  chance_valor_acima: number | null;
  peso_capital: number | null;
  peso_acoes: number | null;
  situacao: string;
  confianca?: string;
  segunda_analise?: { decisao: string; sinal: string; valor_justo?: number } | null;
  tese?: string | null;
};
export type Registro = {
  id: string;
  titulo: string;
  data_ref: string;
  preco_ref: string;
  registrado_em: string;
  ke: number;
  regra?: string;
  benchmarks: { IBOV: number; SMLL: number; CDI_aa: number };
  carteira: { acoes: number; cdi: number; entrada_sugerida?: number | null; acoes_vol_normal?: number | null; retorno_esperado?: number | null; vol?: number | null };
  recomendacoes: Rec[];
  universo: { ticker: string; preco_ref: number; selecionada: boolean }[];
  como_avaliar?: string[];
  aviso?: string;
};

const fin = (x: unknown): x is number => typeof x === "number" && Number.isFinite(x);
const dataBR = (iso: string) => iso.slice(0, 10).split("-").reverse().join("/");
// tons da série 1 para a barra de alocação, do mais escuro ao mais claro
const SHADES = ["#1c5cab", "#2a78d6", "#4b8fe0", "#6aa3e6", "#86b6ef", "#a3c8f3", "#bcd7f6", "#d3e5f9"];

/** Ficha congelada da recomendação: é o que vira imagem. Não usa dado ao vivo. */
export function Ficha({ r }: { r: Registro }) {
  const recs = r.recomendacoes;
  const weighted = recs.filter((x) => fin(x.peso_capital)).sort((a, b) => (b.peso_capital as number) - (a.peso_capital as number));
  const small = weighted.filter((x) => (x.peso_capital as number) < 0.04);
  return (
    <section id={`ficha-${r.id}`} className="mx-auto w-full max-w-[1180px] rounded-lg border border-hairline bg-surface p-4 sm:p-7">
      <header className="flex flex-wrap items-end justify-between gap-4 border-b border-hairline pb-4">
        <div>
          <div className="text-[12.5px] font-medium text-accent-ink">e-agora, registro de recomendação</div>
          <h2 className="mt-1 text-[26px] font-semibold tracking-[-0.015em]">
            {r.titulo}, {dataBR(r.data_ref)}
          </h2>
          <div className="mt-1 text-[13px] text-ink-2">
            {r.preco_ref}. Custo de capital (Ke) de {Math.round(r.ke * 100)}% ao ano. Registrado em {dataBR(r.registrado_em)} para conferir o resultado depois.
          </div>
        </div>
        <div className="grid grid-cols-3 gap-5 text-right">
          <div>
            <div className="label">Ibovespa</div>
            <div className="num text-[17px] font-semibold">{num(r.benchmarks.IBOV, 0)}</div>
          </div>
          <div>
            <div className="label">Small Caps</div>
            <div className="num text-[17px] font-semibold">{num(r.benchmarks.SMLL, 0)}</div>
          </div>
          <div>
            <div className="label">CDI ao ano</div>
            <div className="num text-[17px] font-semibold">{pct(r.benchmarks.CDI_aa, 2)}</div>
          </div>
        </div>
      </header>

      <div className="mt-5">
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <div className="text-[14px] font-semibold">Alocação da carteira-alvo</div>
          <div className="text-[12.5px] text-ink-2">
            {fin(r.carteira.entrada_sugerida)
              ? `Entrada sugerida agora: ${pct(r.carteira.entrada_sugerida, 0)} do capital em ações, subindo até ${pct(r.carteira.acoes_vol_normal ?? r.carteira.acoes, 0)} quando a volatilidade normalizar`
              : ""}
          </div>
        </div>
        <div className="mt-2 flex h-9 w-full overflow-hidden rounded">
          {weighted.map((x, i) => (
            <div
              key={x.ticker}
              className="flex items-center justify-center border-r-2 border-[var(--surface)] text-[11.5px] font-semibold"
              style={{ width: `${(x.peso_capital as number) * 100}%`, background: SHADES[i % SHADES.length], color: i > 3 ? "#0f2a4d" : "#ffffff" }}
              title={`${x.ticker} ${pct(x.peso_capital, 1)}`}
            >
              {(x.peso_capital as number) >= 0.04 ? x.ticker : ""}
            </div>
          ))}
          <div className="flex items-center justify-center text-[11.5px] font-semibold text-ink-2" style={{ width: `${r.carteira.cdi * 100}%`, background: "var(--surface-2)" }}>
            CDI {pct(r.carteira.cdi, 0)}
          </div>
        </div>
        <div className="mt-1 text-[11.5px] text-muted">
          {small.length > 0 && `Fatias menores: ${small.map((x) => `${x.ticker} ${pct(x.peso_capital, 1)}`).join(", ")}. `}
          Pesos: metade pelo máximo Sharpe da TIR de dono, metade por paridade de risco; até 20% por ação e 40% por setor, o resto em CDI.
          {fin(r.carteira.retorno_esperado) ? ` Retorno esperado de ${pct(r.carteira.retorno_esperado, 1)} ao ano, volatilidade de ${pct(r.carteira.vol, 1)}.` : ""}
        </div>
      </div>

      <div className="mt-5 overflow-x-auto">
      <table className="w-full min-w-[860px] border-collapse text-[13px]">
        <thead>
          <tr className="border-b border-hairline text-left text-[11.5px] text-muted">
            <th className="py-2 pr-2 font-medium">#</th>
            <th className="py-2 pr-2 font-medium">Ação</th>
            <th className="py-2 pr-2 text-right font-medium">Preço 28/10</th>
            <th className="py-2 pr-2 text-right font-medium">Preço-teto</th>
            <th className="py-2 pr-2 text-right font-medium">Valor justo</th>
            <th className="py-2 pr-2 text-right font-medium">Upside</th>
            <th className="py-2 pr-2 text-right font-medium">TIR de dono</th>
            <th className="py-2 pr-2 text-right font-medium">Chance de valer mais</th>
            <th className="py-2 pr-2 text-right font-medium">Peso no capital</th>
            <th className="py-2 pr-2 font-medium">Situação</th>
            <th className="py-2 font-medium">2ª análise</th>
          </tr>
        </thead>
        <tbody>
          {recs.map((x) => (
            <tr key={x.ticker} className="border-b border-hairline align-top last:border-b-0">
              <td className="py-2.5 pr-2 font-serif text-[18px] font-medium leading-none text-accent">{x.rank}</td>
              <td className="py-2.5 pr-2">
                <div className="font-semibold">{x.ticker}</div>
                <div className="text-[11.5px] text-muted">{x.nome}</div>
              </td>
              <td className="num py-2.5 pr-2 text-right font-semibold">{num(x.preco_ref)}</td>
              <td className="num py-2.5 pr-2 text-right">{num(x.teto)}</td>
              <td className="num py-2.5 pr-2 text-right">{num(x.valor_justo)}</td>
              <td className={`num py-2.5 pr-2 text-right ${signClass(x.upside)}`}>{pct(x.upside, 0, true)}</td>
              <td className="num py-2.5 pr-2 text-right font-semibold">{pct(x.tir_dono, 1)}</td>
              <td className="num py-2.5 pr-2 text-right">{pct(x.chance_valor_acima, 0)}</td>
              <td className="num py-2.5 pr-2 text-right">{pct(x.peso_capital, 1)}</td>
              <td className={`py-2.5 pr-2 text-[12px] ${x.situacao === "acima do teto" ? "text-ink-2" : "font-medium text-[var(--pos)]"}`}>{x.situacao}</td>
              <td className="py-2.5 text-[12px]">
                {x.segunda_analise ? `${x.segunda_analise.decisao} (${x.segunda_analise.sinal.toLowerCase()})` : <span className="text-muted">não analisada</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>

      <div className="mt-5 grid grid-cols-1 gap-4 border-t border-hairline pt-4 text-[12px] text-ink-2 md:grid-cols-2">
        <div>
          <div className="font-semibold text-ink">Regra de seleção</div>
          <p className="mt-1">{r.regra}</p>
        </div>
        <div>
          <div className="font-semibold text-ink">Como conferir em dezembro</div>
          <p className="mt-1">
            Retorno de cada ação desde o preço de 28/10 mais proventos, carteira com {pct(r.carteira.cdi, 0)} em CDI, contra Ibovespa, Small Caps, CDI e a mediana das{" "}
            {r.universo.length - recs.length} ações cobertas não selecionadas. Ao vivo em e-agora-ivory.vercel.app/registro.
          </p>
        </div>
      </div>
      <div className="mt-3 text-[11px] text-muted">{r.aviso}</div>
    </section>
  );
}

function businessDays(fromIso: string, to: Date) {
  const d = new Date(`${fromIso}T12:00:00-03:00`);
  let n = 0;
  for (;;) {
    d.setDate(d.getDate() + 1);
    if (d > to) break;
    const wd = d.getDay();
    if (wd !== 0 && wd !== 6) n++;
  }
  return n;
}

function Tile({ label, value, note, strong }: { label: string; value: number | null; note?: string; strong?: boolean }) {
  return (
    <div>
      <div className="label">{label}</div>
      <div className={`num ${strong ? "text-[26px]" : "text-[20px]"} font-semibold ${signClass(value)}`}>{pct(value, 1, true)}</div>
      {note && <div className="text-[11.5px] text-muted">{note}</div>}
    </div>
  );
}

/** Desempenho ao vivo desde o preço de referência (retorno de preço, sem proventos). */
export function Desempenho({ r }: { r: Registro }) {
  const tickers = useMemo(() => r.universo.map((u) => u.ticker), [r]);
  const q = useQuotes(tickers, 60000);
  const m = useMarket();
  const ret = (t: string, ref: number) => {
    const p = q.quotes[t]?.price;
    return fin(p) && ref > 0 ? p / ref - 1 : null;
  };
  const recs = r.recomendacoes.map((x) => ({ ...x, now: q.quotes[x.ticker]?.price ?? null, ret: ret(x.ticker, x.preco_ref) }));
  const du = businessDays(r.data_ref, new Date());
  const cdiAcc = Math.pow(1 + r.benchmarks.CDI_aa, du / 252) - 1;
  const ibNow = m?.indices?.IBOV?.price;
  const smNow = m?.indices?.SMLL?.price;
  const ib = fin(ibNow) ? ibNow / r.benchmarks.IBOV - 1 : null;
  const sm = fin(smNow) ? smNow / r.benchmarks.SMLL - 1 : null;
  const have = recs.filter((x) => fin(x.ret));
  const wsum = have.reduce((s, x) => s + (x.peso_capital ?? 0), 0);
  const eqW = wsum > 0 ? have.reduce((s, x) => s + (x.peso_capital ?? 0) * (x.ret as number), 0) / wsum : null;
  const port = eqW !== null ? r.carteira.acoes * eqW + r.carteira.cdi * cdiAcc : null;
  const eqEqual = have.length ? have.reduce((s, x) => s + (x.ret as number), 0) / have.length : null;
  const others = r.universo
    .filter((u) => !u.selecionada)
    .map((u) => ret(u.ticker, u.preco_ref))
    .filter(fin)
    .sort((a, b) => a - b);
  const medOthers = others.length ? others[Math.floor(others.length / 2)] : null;
  const beat = ib !== null ? have.filter((x) => (x.ret as number) > ib).length : null;
  return (
    <section className="space-y-4">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="h2">Desempenho desde {dataBR(r.data_ref)}</h2>
        <span className="text-[12px] text-muted">
          {du} pregões; preços ao vivo{q.asOf ? ` às ${new Date(q.asOf).toLocaleTimeString("pt-BR")}` : ""}; retorno de preço, sem proventos; CDI pelos dias úteis, sem feriados
        </span>
      </div>
      <div className="panel grid grid-cols-2 gap-5 p-5 md:grid-cols-4 xl:grid-cols-7">
        <Tile strong label={`Carteira (${pct(r.carteira.acoes, 0)} ações + CDI)`} value={port} />
        <Tile label="Só as ações, pelos pesos" value={eqW} />
        <Tile label={`Pesos iguais nas ${r.recomendacoes.length}`} value={eqEqual} />
        <Tile label="Ibovespa" value={ib} />
        <Tile label="Small Caps" value={sm} />
        <Tile label="CDI no período" value={cdiAcc} />
        <Tile label="Mediana das não selecionadas" value={medOthers} note={`${others.length} ações`} />
      </div>
      <div className="panel overflow-x-auto">
        <table className="data min-w-[760px] text-[13px]">
          <thead>
            <tr>
              <th className="!text-left">Ação</th>
              <th>Preço 28/10</th>
              <th>Agora</th>
              <th>Retorno</th>
              <th>Contra o Ibovespa</th>
              <th>Preço-teto</th>
              <th>Valor justo</th>
              <th className="!text-left">Agora está</th>
            </tr>
          </thead>
          <tbody>
            {recs.map((x) => (
              <tr key={x.ticker}>
                <td className="text-left">
                  <Link href={`/relatorio/${x.ticker}`} className="font-semibold hover:text-accent">
                    {x.ticker}
                  </Link>
                </td>
                <td>{num(x.preco_ref)}</td>
                <td>{num(x.now)}</td>
                <td className={signClass(x.ret)}>{pct(x.ret, 1, true)}</td>
                <td className={signClass(fin(x.ret) && ib !== null ? (x.ret as number) - ib : null)}>{fin(x.ret) && ib !== null ? pct((x.ret as number) - ib, 1, true) : "—"}</td>
                <td>{num(x.teto)}</td>
                <td>{num(x.valor_justo)}</td>
                <td className="text-left text-[12px] text-ink-2">
                  {fin(x.now) && fin(x.valor_justo) && x.now >= x.valor_justo
                    ? "no valor justo ou acima"
                    : fin(x.now) && fin(x.teto) && x.now <= x.teto
                      ? "na faixa de compra"
                      : fin(x.now)
                        ? "acima do teto"
                        : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {beat !== null && (
        <p className="text-[13px] text-ink-2">
          {beat} de {have.length} recomendações estão à frente do Ibovespa desde {dataBR(r.data_ref)}.
        </p>
      )}
    </section>
  );
}
