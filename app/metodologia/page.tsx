import type { Metadata } from "next";
import { getOverview } from "@/lib/data";

export const metadata: Metadata = { title: "Metodologia" };

function Block({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="panel p-5">
      <h2 className="h2">{title}</h2>
      <div className="mt-3 space-y-2 text-[14px] leading-relaxed text-ink-2">{children}</div>
    </section>
  );
}

function F({ children }: { children: React.ReactNode }) {
  return <div className="my-2 rounded border border-hairline bg-surface-2 px-3 py-2 font-serif text-[14.5px] text-ink">{children}</div>;
}

export default function Page() {
  const ov = getOverview();
  return (
    <div className="space-y-6">
      <header>
        <h1 className="h1">Metodologia</h1>
        <p className="mt-2 max-w-[72ch] text-[15px] text-ink-2">Como cada número do painel foi produzido, de onde vêm os dados e quais são os limites do estudo.</p>
      </header>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Block title="Dados e fontes">
          <p>
            <span className="font-medium text-ink">Demonstrações financeiras:</span> base oficial de dados abertos da CVM, DFP 2015–2025 e ITR 2022–2026, consolidadas quando disponíveis, padronizadas por conta. Correções automáticas: escala das ações (milhares × unidades), linhas de dívida fora da conta padrão (CRI, debêntures em outras obrigações), arrendamentos IFRS-16 e lucro do controlador quando a atribuição vem zerada ou com sinal invertido.
          </p>
          <p>
            <span className="font-medium text-ink">Mercado:</span> cotações ao vivo da API oficial da B3 (atraso de até 15 minutos), série histórica COTAHIST 2016–2026, proventos e eventos societários da B3 (desdobramentos, grupamentos, bonificações), histórico diário dos índices desde 1998. Reservas automáticas: Yahoo Finance e brapi.
          </p>
          <p>
            <span className="font-medium text-ink">Macro:</span> Banco Central (SGS: Selic, CDI, IPCA, PTAX; Focus) e curva de DI futuro da B3.
          </p>
          <p>
            <span className="font-medium text-ink">Qualitativo:</span> 32 analistas setoriais (12 na 1ª rodada e 20 na ampliação) leram releases, apresentações e fatos relevantes das companhias e fixaram as premissas de cada uma. Cada dossiê lista as fontes.
          </p>
        </Block>
        <Block title="Cobertura">
          <p>
            1ª rodada (26/10): queda de 20% ou mais no dia e volume médio diário de 3 meses de R$ 20 mi ou mais, no universo Ibovespa, IBrX-100 e Small Caps, na foto das 11h39. Resultado: 59 empresas, revisadas uma a uma por um segundo analista.
          </p>
          <p>
            Ampliação (28/10): todas as demais ações desse universo com volume médio diário de R$ 10 mi ou mais e demonstrações padronizadas na CVM, com premissas feitas sob um checklist com as lições da revisão. Total: {ov.companies.length} empresas. As variações exibidas no painel são ao vivo.
          </p>
          <p>
            <span className="font-medium text-ink">Melhores oportunidades:</span> {(ov as unknown as { opportunity_rule?: string }).opportunity_rule}
          </p>
        </Block>
        <Block title="Projeções (2026–2030)">
          <p>Modelo de três demonstrações por drivers, ancorado no FY2025 da CVM e no balanço do último trimestre. Fluxos de 2026 entram só pela fração do ano após o balanço-base.</p>
          <F>
            Receita<sub>t</sub> = Receita<sub>t−1</sub> × (1 + g<sub>t</sub>); EBITDA = Receita × margem; FCFF = EBIT × (1 − t) + D&amp;A − Capex − ΔCapital de giro
          </F>
          <p>
            Lucro = (EBIT − custo da dívida × dívida líquida) × (1 − alíquota). Dividendos = payout × lucro. Dívida líquida e patrimônio evoluem pelo caixa gerado. Premissas próximas do crescimento de 5 anos, ajustadas por setor e eficiência.
          </p>
          <p>
            Ajustes setoriais: arrendamentos como dívida, com adições de direito de uso no capex (varejo, saúde, educação); frota líquida em locadoras; juros capitalizados no custo de incorporadoras; receita de construção excluída em concessões; bancos modelados por ROE e payout.
          </p>
        </Block>
        <Block title="Custo de capital e perpetuidade">
          <p>Ke = 25% a.a. nominal, a meta de retorno do usuário (o seletor no topo permite testar 20% e 30%).</p>
          <F>WACC = (1 − w<sub>d</sub>) × Ke + w<sub>d</sub> × Kd × (1 − 34%)</F>
          <p>Perpetuidade pelo value driver, que só cria valor se o retorno sobre o capital superar o custo:</p>
          <F>VT = NOPAT<sub>2030</sub> × (1 + g) × (1 − g / ROIC) ÷ (WACC − g)</F>
          <p>g nominal padrão de 5% (3,5% de IPCA de longo prazo do Focus mais 1,5% real), entre 3,5% e 6,5% conforme o setor.</p>
        </Block>
        <Block title="Valor justo">
          <p>
            Combinação ponderada. Industriais: DCF 50%, DDM 25%, múltiplos 25%. Incorporadoras: DDM 50%, P/L-alvo 30%, DCF 20%, porque o fluxo de caixa oscila com terreno, recebíveis e juros capitalizados. Bancos: DDM 60%, P/VP-alvo 40%. Holdings: soma das partes com controladas a valor justo do próprio estudo (recalculada no Ke escolhido) ou a mercado. Valores negativos contam como zero no peso. Os pesos setoriais só mudaram onde as duas baterias de teste concordaram (página Testes).
          </p>
          <F>DDM: VP(dividendos 2026–30, Ke) + Lucro<sub>2030</sub> × (1 + g) × (1 − g / ROE) ÷ (Ke − g)</F>
          <p>Múltiplos-alvo (P/L, EV/EBITDA, P/VP) definidos pelos analistas com base na média de 5 anos e em pares. Graham e Bazin aparecem só como referência.</p>
        </Block>
        <Block title="TIR de dono e retorno em 3 anos">
          <p>
            <span className="font-medium text-ink">TIR de dono (inteira):</span> a taxa que iguala o preço de hoje ao valor presente de todos os dividendos projetados mais a perpetuidade. É o retorno anual de quem compra hoje e fica com a empresa para sempre, comparado ao Ke de 25%.
          </p>
          <p>
            <span className="font-medium text-ink">TIR de 3 anos:</span> compra hoje, recebe os dividendos de 2026 a 2028 e vende no fim de 2028 ao P/L alvo sobre o lucro de 2029. Inclui a volta do múltiplo, por isso é mais alta.
          </p>
          <p>As duas são recalculadas no navegador a cada cotação, com o mesmo motor do estudo.</p>
        </Block>
        <Block title="Probabilidade, cenários e sensibilidade">
          <p>
            Monte Carlo com 5.000 sorteios por empresa: deslocamentos persistentes no crescimento da receita e na margem (correlação 0,5), no capex e na perpetuidade, com desvios definidos pelo analista. P(valor &gt; preço) é a fração dos cenários em que o valor justo supera o preço ao vivo.
          </p>
          <p>Cenários pessimista, base e otimista com probabilidades explícitas. Mapas de sensibilidade de Ke × g e de crescimento × margem. DCF reverso: o crescimento médio de receita que o preço atual embute.</p>
        </Block>
        <Block title="Quant e estatística">
          <p>
            <span className="font-medium text-ink">Decomposição da queda:</span> beta de baixa (dias de queda do Ibovespa, 3 anos) × variação do índice; regressão cross-section das {ov.xsec.n} ações do universo em beta, dívida/EBITDA, porte e dummies de setor, exportadora e estatal (R² = {Math.round(ov.xsec.r2 * 100)}%). O resíduo mede o que a queda teve de específico.
          </p>
          <p>
            <span className="font-medium text-ink">Fatores:</span> escore multifator em z-scores dentro da cobertura: valor (TIR de dono, 25%), qualidade (ROE de 5 anos e Piotroski, 15%), solidez (dívida e Altman Z″ de emergentes, 15%), probabilidade (Monte Carlo, 15%), upside (10%), sobrerreação (resíduo da regressão, 10%) e momentum de 12 meses (10%), pesos revistos pelo backtest de fatores de 2017–2026.
          </p>
          <p>
            <span className="font-medium text-ink">Event study:</span> retornos do Ibovespa 1, 3, 6 e 12 meses após os piores dias desde 1998, após cada eleição presidencial e após quedas de 25% ou mais; histórico de cada ação nos crashes desde 2016. Múltiplos históricos mensais (P/L, P/VP, EV/EBITDA) com média, desvio e z-score do nível atual.
          </p>
        </Block>
        <Block title="Limites">
          <p>
            Preços intradiários de um dia de circuit breaker são voláteis e a liquidez é baixa; os rankings mudam com o preço. O Ke de 25% é exigente: negócios de qualidade com retorno sobre capital moderado aparecem como caros por construção.
          </p>
          <p>
            Parte do consenso de mercado e algumas datas de resultados não puderam ser verificadas na web durante o estudo; os dossiês sinalizam cada lacuna. Holdings e bancos usam métodos próprios, com menos sensibilidades.
          </p>
          <p className="text-ink">Estudo quantitativo com finalidade informativa. Não é recomendação de compra ou venda.</p>
        </Block>
      </div>
    </div>
  );
}
