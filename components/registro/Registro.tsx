"use client";
import Link from "next/link";
import { useMemo } from "react";
import { useCdi, useMarket, useQuotes } from "@/lib/live";
import { num, pct, signClass } from "@/lib/format";
import { Rating, callOf } from "@/components/ui/Rating";

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
const SHADES = ["#0b2545", "#163a68", "#1f5fad", "#3f7bc4", "#6696d2", "#8fb2de", "#b5cbe9", "#d3e1f2"];

/** Ficha congelada da recomendação: é o que vira imagem. Não usa dado ao vivo. */
export function Ficha({ r, names = {} }: { r: Registro; names?: Record<string, string> }) {
  const recs = r.recomendacoes;
  const weighted = recs.filter((x) => fin(x.peso_capital)).sort((a, b) => (b.peso_capital as number) - (a.peso_capital as number));
  const small = weighted.filter((x) => (x.peso_capital as number) < 0.04);
  return (
    <section id={`ficha-${r.id}`} className="mx-auto w-full max-w-[1180px] border border-hairline bg-surface">
      <div className="flex items-baseline justify-between gap-3 bg-[var(--navy)] px-4 py-2.5 text-white sm:px-7">
        <span className="text-[15px] font-bold">
          E agora? <span className="font-medium text-[var(--on-navy-2)]">Research</span>
        </span>
        <span className="text-[12px] text-[var(--on-navy-2)]">Registro de recomendação</span>
      </div>
      <div className="p-4 sm:p-7">
      <header className="flex flex-wrap items-end justify-between gap-4 border-b border-hairline pb-4">
        <div>
          <h2 className="text-[26px] font-bold tracking-[-0.015em]">
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
          <div className="text-[14px] font-bold">Alocação da carteira-alvo</div>
          <div className="text-[12.5px] text-ink-2">
            {fin(r.carteira.entrada_sugerida)
              ? `Entrada sugerida agora: ${pct(r.carteira.entrada_sugerida, 0)} do capital em ações, subindo até ${pct(r.carteira.acoes_vol_normal ?? r.carteira.acoes, 0)} quando a volatilidade normalizar`
              : ""}
          </div>
        </div>
        <div className="mt-2 flex h-9 w-full overflow-hidden rounded-[2px]">
          {weighted.map((x, i) => (
            <div
              key={x.ticker}
              className="flex items-center justify-center border-r-2 border-[var(--surface)] text-[12px] font-semibold"
              style={{ width: `${(x.peso_capital as number) * 100}%`, background: SHADES[i % SHADES.length], color: i > 4 ? "#0b2545" : "#ffffff" }}
              title={`${x.ticker} ${pct(x.peso_capital, 1)}`}
            >
              {(x.peso_capital as number) >= 0.04 ? x.ticker : ""}
            </div>
          ))}
          <div className="flex items-center justify-center text-[12px] font-semibold text-ink-2" style={{ width: `${r.carteira.cdi * 100}%`, background: "var(--box)" }}>
            CDI {pct(r.carteira.cdi, 0)}
          </div>
        </div>
        <div className="mt-1 text-[12px] text-muted">
          {small.length > 0 && `Fatias menores: ${small.map((x) => `${x.ticker} ${pct(x.peso_capital, 1)}`).join(", ")}. `}
          Pesos: metade pelo máximo Sharpe da TIR de dono, metade por paridade de risco; até 20% por ação e 40% por setor, o resto em CDI.
          {fin(r.carteira.retorno_esperado) ? ` Retorno esperado de ${pct(r.carteira.retorno_esperado, 1)} ao ano, volatilidade de ${pct(r.carteira.vol, 1)}.` : ""}
        </div>
      </div>

      <div className="mt-5 overflow-x-auto">
      <table className="data min-w-[980px] text-[13px]">
        <thead>
          <tr>
            <th className="!text-left">#</th>
            <th className="!text-left">Ação</th>
            <th>Preço 28/10</th>
            <th>Valor justo</th>
            <th>TIR de dono</th>
            <th>Chance</th>
            <th>Peso</th>
            <th className="!text-left">Recomendação</th>
            <th className="!text-left">2ª análise</th>
          </tr>
        </thead>
        <tbody>
          {recs.map((x) => (
            <tr key={x.ticker}>
              <td className="text-left text-muted">{x.rank}</td>
              <td className="text-left">
                <div className="font-bold">{x.ticker}</div>
                <div className="text-[12px] text-muted">{names[x.ticker] ?? x.nome}</div>
              </td>
              <td className="font-semibold">{num(x.preco_ref)}</td>
              <td>{num(x.valor_justo)}</td>
              <td className="font-semibold">{pct(x.tir_dono, 1)}</td>
              <td>{pct(x.chance_valor_acima, 0)}</td>
              <td>{pct(x.peso_capital, 1)}</td>
              <td className="text-left">
                <Rating size="sm" c={callOf(x.preco_ref, x.teto, x.compra_forte)} ceiling={x.teto} upside={x.upside} />
              </td>
              <td className="text-left text-[12px]">
                {x.segunda_analise ? `${x.segunda_analise.decisao} (${x.segunda_analise.sinal.toLowerCase()})` : <span className="text-muted">não analisada</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>

      <div className="mt-5 grid grid-cols-1 gap-4 border-t border-hairline pt-4 text-[12px] text-ink-2 md:grid-cols-2">
        <div>
          <div className="font-bold text-ink">Regra de seleção</div>
          <p className="mt-1">{r.regra}</p>
        </div>
        <div>
          <div className="font-bold text-ink">Como conferir em dezembro</div>
          <p className="mt-1">
            Retorno de cada ação desde o preço de 28/10 mais proventos, carteira com {pct(r.carteira.cdi, 0)} em CDI, contra Ibovespa, Small Caps, CDI e a mediana das{" "}
            {r.universo.length - recs.length} ações cobertas não selecionadas. Ao vivo em e-agora-ivory.vercel.app/registro.
          </p>
        </div>
      </div>
      <div className="mt-3 text-[12px] text-muted">{r.aviso}</div>
      </div>
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

const spDay = (d: Date) => d.toLocaleDateString("sv-SE", { timeZone: "America/Sao_Paulo" });
/** Dia (AAAA-MM-DD, horário de Brasília) de um carimbo de cotação: a B3 manda horário local sem fuso; Yahoo e brapi, ISO. */
export function quoteDay(ts: string | null | undefined): string | null {
  if (!ts) return null;
  if (/^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}/.test(ts) && !/(Z|[+-]\d{2}:?\d{2})$/.test(ts)) return ts.slice(0, 10);
  const t = Date.parse(ts);
  return Number.isNaN(t) ? null : spDay(new Date(t));
}

function median(a: number[]) {
  if (!a.length) return null;
  const s = [...a].sort((x, y) => x - y);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function Tile({ label, value, note, strong }: { label: string; value: number | null; note?: string; strong?: boolean }) {
  return (
    <div>
      <div className="label">{label}</div>
      <div className={`num ${strong ? "text-[26px]" : "text-[20px]"} font-bold ${signClass(value)}`}>{pct(value, 1, true)}</div>
      {note && <div className="text-[12px] text-muted">{note}</div>}
    </div>
  );
}

/** Proventos por ação com data-com depois da data de referência (R$ por ação). */
export type DivMap = Record<string, { dc: string; valor: number }[]>;
export type TrackOpts = {
  /** CDI diário realizado (uma taxa por dia útil, a partir da data de referência); sem ele, usa a taxa anual do registro. */
  cdiDaily?: { d: string; r: number }[] | null;
  divs?: DivMap | null;
  now?: Date;
};

export type Track = {
  du: number;
  cdiAcc: number;
  /** "realizado" = CDI diário do Banco Central; "estimado" = taxa anual do registro pelos dias de segunda a sexta. */
  cdiMode: "realizado" | "estimado";
  ib: number | null;
  sm: number | null;
  eqW: number | null;
  port: number | null;
  /** referência com a mesma alocação: parcela de ações no Small Caps, o resto em CDI */
  refSmCdi: number | null;
  eqEqual: number | null;
  medOthers: number | null;
  nOthers: number;
  nOthersTotal: number;
  beat: number | null;
  nHave: number;
  /** número de proventos somados aos retornos (data-com depois da referência e até hoje) */
  nDivs: number;
  recs: (Rec & { now: number | null; ret: number | null; divs: number })[];
};

/** Resultado da carteira-alvo desde o preço de referência. Retorno de cada ação = (preço de agora + proventos com
 *  data-com no período) ÷ preço de referência − 1. CDI: taxas diárias realizadas de [referência, hoje), quando informadas. */
export function trackRecord(r: Registro, priceOf: (t: string) => number | null | undefined, ibNow?: number | null, smNow?: number | null, opts: TrackOpts = {}): Track {
  const now = opts.now ?? new Date();
  const today = spDay(now);
  let nDivs = 0;
  const divOf = (t: string) => {
    let s = 0;
    for (const e of opts.divs?.[t] ?? []) {
      if (e.dc > r.data_ref && e.dc <= today && fin(e.valor)) {
        s += e.valor;
        nDivs++;
      }
    }
    return s;
  };
  const ret = (t: string, ref: number, dv = 0) => {
    const p = priceOf(t);
    return fin(p) && ref > 0 ? (p + dv) / ref - 1 : null;
  };
  const recs = r.recomendacoes.map((x) => {
    const dv = divOf(x.ticker);
    return { ...x, now: priceOf(x.ticker) ?? null, divs: dv, ret: ret(x.ticker, x.preco_ref, dv) };
  });
  // a taxa do dia D remunera de D para o dia útil seguinte: do fechamento da referência até hoje entram as taxas de [referência, hoje)
  const rates = (opts.cdiDaily ?? []).filter((x) => x.d >= r.data_ref && x.d < today && fin(x.r));
  const realized = !!opts.cdiDaily && (rates.length > 0 || today <= r.data_ref);
  const du = realized ? rates.length : businessDays(r.data_ref, now);
  const cdiAcc = realized ? rates.reduce((a, x) => a * (1 + x.r), 1) - 1 : Math.pow(1 + r.benchmarks.CDI_aa, du / 252) - 1;
  const ib = fin(ibNow) ? ibNow / r.benchmarks.IBOV - 1 : null;
  const sm = fin(smNow) ? smNow / r.benchmarks.SMLL - 1 : null;
  const have = recs.filter((x) => fin(x.ret));
  const wsum = have.reduce((s, x) => s + (x.peso_capital ?? 0), 0);
  const eqW = wsum > 0 ? have.reduce((s, x) => s + (x.peso_capital ?? 0) * (x.ret as number), 0) / wsum : null;
  const port = eqW !== null ? r.carteira.acoes * eqW + r.carteira.cdi * cdiAcc : null;
  const refSmCdi = sm !== null ? r.carteira.acoes * sm + r.carteira.cdi * cdiAcc : null;
  const eqEqual = have.length ? have.reduce((s, x) => s + (x.ret as number), 0) / have.length : null;
  const rest = r.universo.filter((u) => !u.selecionada);
  const others = rest.map((u) => ret(u.ticker, u.preco_ref, divOf(u.ticker))).filter(fin);
  const beat = ib !== null ? have.filter((x) => (x.ret as number) > ib).length : null;
  return { du, cdiAcc, cdiMode: realized ? "realizado" : "estimado", ib, sm, eqW, port, refSmCdi, eqEqual, medOthers: median(others), nOthers: others.length, nOthersTotal: rest.length, beat, nHave: have.length, nDivs, recs };
}

const diff = (a: number | null, b: number | null) => (a !== null && b !== null ? a - b : null);

/** Desempenho ao vivo da carteira-alvo desde o preço de referência. */
export function Desempenho({ r, divs = null, divsAsOf = null }: { r: Registro; divs?: DivMap | null; divsAsOf?: string | null }) {
  const tickers = useMemo(() => r.universo.map((u) => u.ticker), [r]);
  const q = useQuotes(tickers, 60000);
  const m = useMarket();
  const cdi = useCdi(r.data_ref);
  const ibQ = m?.indices?.IBOV ?? null;
  const smQ = m?.indices?.SMLL ?? null;
  const tr = trackRecord(r, (t) => q.quotes[t]?.price, ibQ?.price, smQ?.price, { cdiDaily: cdi?.days ?? null, divs });
  const { du, cdiAcc, cdiMode, ib, sm, eqW, port, refSmCdi, eqEqual, medOthers, nOthers, nOthersTotal, beat, nHave, nDivs, recs } = tr;
  // mesma data para todas as séries: dia do carimbo de cada cotação usada (ações da lista e os dois índices)
  const days = new Map<string, string[]>();
  const mark = (name: string, ts: string | null | undefined) => {
    const d = quoteDay(ts);
    if (d) days.set(d, [...(days.get(d) ?? []), name]);
  };
  for (const x of r.recomendacoes) if (q.quotes[x.ticker]) mark(x.ticker, q.quotes[x.ticker].ts);
  if (ibQ) mark("Ibovespa", ibQ.ts);
  if (smQ) mark("Small Caps", smQ.ts);
  const mixed = days.size > 1;
  const lastCdi = cdi?.days?.filter((x) => x.d >= r.data_ref).at(-1)?.d ?? null;
  const acoes = pct(r.carteira.acoes, 0);
  return (
    <section className="space-y-4">
      <div className="sec flex flex-wrap items-baseline justify-between gap-3">
        <h2 className="h2">Simulação da carteira-alvo desde {dataBR(r.data_ref)}</h2>
        <span className="text-[12px] text-muted">
          {du} {du === 1 ? "pregão" : "pregões"}; preços ao vivo{q.asOf ? ` às ${new Date(q.asOf).toLocaleTimeString("pt-BR")}` : ""}
        </span>
      </div>
      <p className="max-w-[78ch] text-[13px] text-ink-2">
        Simula {acoes} do capital nas ações, pelos pesos do registro, desde o fechamento de {dataBR(r.data_ref)}, e o resto em CDI. Não é a execução da entrada gradual
        {fin(r.carteira.entrada_sugerida) ? ` de ${pct(r.carteira.entrada_sugerida, 1)}` : ""} sugerida no estudo, nem desconta custos. O registro foi gravado em {dataBR(r.registrado_em)}, com os
        fechamentos de {dataBR(r.data_ref)}: comprar a esses preços já não era possível quando a lista foi congelada.
      </p>
      {mixed && (
        <p role="status" className="border-l-2 border-[var(--neg)] pl-3 text-[13px] text-ink">
          As cotações comparadas não são do mesmo dia:{" "}
          {[...days.entries()]
            .sort((a, b) => a[0].localeCompare(b[0]))
            .map(([d, names]) => `${dataBR(d)}: ${names.join(", ")}`)
            .join("; ")}
          . Compare os retornos só quando todas as séries tiverem a mesma data.
        </p>
      )}
      <div className="panel grid grid-cols-2 gap-5 p-5 md:grid-cols-4">
        <Tile strong label={`Carteira (${acoes} ações + CDI)`} value={port} />
        <Tile label={`Referência: ${acoes} Small Caps + CDI`} value={refSmCdi} note={diff(port, refSmCdi) !== null ? `carteira ${pct(diff(port, refSmCdi), 1, true)} contra a referência` : undefined} />
        <Tile label="Só as ações, pelos pesos" value={eqW} note={diff(eqW, sm) !== null ? `${pct(diff(eqW, sm), 1, true)} contra o Small Caps` : undefined} />
        <Tile label={`Pesos iguais nas ${r.recomendacoes.length}`} value={eqEqual} />
        <Tile label="Small Caps" value={sm} />
        <Tile label="Ibovespa" value={ib} />
        <Tile label="CDI no período" value={cdiAcc} note={cdiMode === "realizado" ? "taxas diárias do Banco Central" : "estimado pela taxa anual do registro"} />
        <Tile label="Mediana das não selecionadas" value={medOthers} note={`${nOthers} de ${nOthersTotal} ações com cotação`} />
      </div>
      <div className="panel overflow-x-auto">
        <table className="data min-w-[820px] text-[13px]">
          <thead>
            <tr>
              <th className="!text-left">Ação</th>
              <th>Preço 28/10</th>
              <th>Agora</th>
              <th>Proventos</th>
              <th>Retorno</th>
              <th>Contra o Ibovespa</th>
              <th>Preço-teto</th>
              <th>Valor justo</th>
              <th className="!text-left">Ao preço de agora</th>
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
                <td>{x.divs > 0 ? num(x.divs) : "—"}</td>
                <td className={signClass(x.ret)}>{pct(x.ret, 1, true)}</td>
                <td className={signClass(fin(x.ret) && ib !== null ? (x.ret as number) - ib : null)}>{fin(x.ret) && ib !== null ? pct((x.ret as number) - ib, 1, true) : "—"}</td>
                <td>{num(x.teto)}</td>
                <td>{num(x.valor_justo)}</td>
                <td className="text-left text-[12px] text-ink-2">
                  {!fin(x.now) || !fin(x.teto) ? "—" : x.now <= x.teto ? `elegível à meta de ${Math.round(r.ke * 100)}%: preço até o teto` : "acompanhamento: acima do teto"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {beat !== null && (
        <p className="text-[13px] text-ink-2">
          {beat} de {nHave} ações da lista estão à frente do Ibovespa desde {dataBR(r.data_ref)}.
        </p>
      )}
      <p className="max-w-[78ch] text-[12px] text-muted">
        {divs
          ? nDivs > 0
            ? `Retorno das ações com ${nDivs} ${nDivs === 1 ? "provento" : "proventos"} de data-com no período`
            : "Retorno de preço: nenhum provento com data-com no período consta na base"
          : "Retorno de preço, sem proventos"}
        {divs && divsAsOf ? ` (proventos da B3 conhecidos até ${dataBR(divsAsOf)}; anúncios posteriores não entram)` : ""}. Ibovespa e Small Caps são índices de retorno total, que já incorporam proventos: sem
        os proventos das ações, a comparação fica desfavorável à carteira.{" "}
        {cdiMode === "realizado"
          ? `CDI: taxas diárias realizadas (Banco Central, SGS 12)${lastCdi ? `, até ${dataBR(lastCdi)}` : ""}.`
          : "CDI: o Banco Central não respondeu; estimado pela taxa anual do registro e pelos dias de segunda a sexta, sem excluir feriados."}{" "}
        O preço-teto e o valor justo da tabela são os congelados no registro, no Ke de {Math.round(r.ke * 100)}%.
      </p>
    </section>
  );
}
