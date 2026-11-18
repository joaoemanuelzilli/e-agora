# Regra de decisão, confiança e acompanhamento

Versão 2, de 18/11/2026, depois da revisão de 17/11. O registro de 28/10/2026 (`data/registro/2026-10-28.json`) foi
gravado com a versão 1 e não é reescrito.

## O que mudou da versão 1 para a 2

| Tema | Versão 1 (registro de 28/10) | Versão 2 |
|---|---|---|
| Lista | 8 "oportunidades" pela regra abaixo | A mesma regra define a **lista de acompanhamento** |
| Compra | Toda a lista entrava na carteira | Só é **elegível para compra à meta** quem tem TIR de dono ≥ Ke (25%) e preço ≤ preço-teto |
| Data de avaliação | 26/10, com o stub de 2026 inteiro descontado (prazo negativo) | 28/10, com ponte do balanço-base até a data de avaliação |
| Carteira | 8 ações, 60% do capital | Mantida como referência do registro; a carteira das elegíveis sai em `data/app/portfolio.json`, campo `eligible` |

## A regra

**Lista de acompanhamento.** Entram as empresas com:

1. TIR de dono ≥ 20%;
2. chance de o valor justo superar o preço ≥ 45% no Monte Carlo;
3. Altman Z″ fora da zona de risco;
4. confiança nas premissas diferente de "baixa";

ordenadas pelo escore multifator, até 8 nomes.

**Elegível para compra à meta.** Dentro da lista, a ação precisa ter TIR de dono ≥ Ke e preço ≤ preço-teto. O
preço-teto é o menor entre o DDM a Ke (o preço em que a TIR de dono é exatamente Ke) e o valor justo. As outras
continuam em acompanhamento e passam a elegíveis se o preço voltar ao teto.

O site calcula a elegibilidade ao vivo, com o preço e o Ke do momento. O campo `eligible` do `overview.json` guarda a
situação na foto do estudo.

## Por que estes cortes

- **Meta de 25%.** É uma política do investidor, igual para todas as empresas, e não uma estimativa do custo de capital
  de cada uma. Quando entra no WACC, ela não sobe com a alavancagem; isso distorce empresas endividadas e está nas
  limitações do estudo.
- **Corte de 20% na lista.** Dá cinco pontos de folga para o erro das premissas e mantém em observação quem está perto
  da meta. Não autoriza compra: a compra exige os 25%.
- **Corte de 45% na chance.** Um pouco abaixo de 50% para não excluir empresas cuja distribuição simulada é centrada no
  preço; é uma escolha, não um resultado.
- **Oito nomes.** Tamanho escolhido para a vitrine do painel. Com os mesmos cortes passam nove empresas.

A seção 2 de `data/tests/decision_checks.md` mostra quantas empresas passam com outros cortes e outros tamanhos de
lista. O resultado central: com TIR mínima de 25% sobram cinco empresas para qualquer corte de chance entre 35% e 65%.

## Rubrica de confiança

A nota de confiança é julgamento do analista sobre a firmeza das premissas. Os rótulos atuais foram atribuídos na
pesquisa de outubro; a rubrica abaixo documenta os critérios que os textos de justificativa usam, para que novas notas
e revisões sigam a mesma escala. Ela não foi aplicada de forma mecânica às 122 notas existentes.

Parte-se de **média** e ajusta-se um degrau por item (escala: alta, média-alta, média, média-baixa, baixa).

| Critério | Sobe um degrau | Desce um degrau |
|---|---|---|
| Fontes primárias | Release, ITR e prévia do trimestre lidos na fonte | Release do último trimestre não acessado |
| Dado da CVM | Balanço simples, sem ajuste manual | Linha da CVM corrigida à mão ou base contábil refeita (ex.: IFRS 17) |
| Concentração de premissa | Resultado espalhado por vários drivers | Um único driver decide o caso (regulatório, recuperação de margem, benefício fiscal) |
| Histórico do driver | Margem e crescimento estáveis em 2021–2025 | Margem volátil ou em queda recente |
| Dívida | Custo, prazo e hedge conferidos | Custo financeiro efetivo ou composição cambial não divulgados |

"Baixa" tira a empresa da lista. "Média-baixa" e "baixa-média" não tiram, mas devem ser ditas junto da recomendação:
três das oito empresas da lista atual estão nesse degrau.

## Protocolo de acompanhamento

O registro de 28/10 foi gravado em 29/10 com os fechamentos de 28/10. Ele vale como simulação de referência da
carteira-alvo de 60% em ações desde aquele fechamento. Para uma avaliação prospectiva, valem estas regras:

- **Congelamento.** A lista, os pesos e os preços-teto são gravados antes do pregão de execução.
- **Preço de execução.** Fechamento do primeiro pregão depois do congelamento.
- **Custos.** 0,10% por operação (corretagem e emolumentos) mais metade do spread de compra e venda do dia.
- **Entrada.** Começa com cerca de 27% do capital em ações (meio Kelly com volatilidade de crise), na proporção dos pesos, e
  sobe até 60% quando a volatilidade de 21 dias do Ibovespa sair do decil superior da própria história.
- **Ação acima do teto.** Não é comprada. Sua parcela fica em CDI até o preço voltar ao teto.
- **Retorno.** Preço mais proventos com data-com no período; CDI diário realizado (série 12 do Banco Central); dias de
  pregão da B3.
- **Comparativos.** Ibovespa, índice de Small Caps e CDI no mesmo intervalo e na mesma data de cotação. A parcela de
  ações é comparada ao Small Caps; a carteira completa, a uma referência de 60% Small Caps + 40% CDI; a seleção, à
  mediana das empresas não selecionadas. Ibovespa e Small Caps são índices de retorno total.
- **Horizonte.** A tese é de retorno anual. A conferência que vale é a de 12 meses.

## O que os testes sustentam e o que não sustentam

- Os testes automáticos verificam consistência de dados e de cálculo. Não validam margem, tributação, payout nem
  retorno futuro.
- O backtest testa fatores e proxies (preço sobre patrimônio, preço sobre lucro, momentum, qualidade). Não testa a
  estratégia completa, com projeção por empresa, TIR e probabilidade.
- A regressão do dia do choque descreve diferenças entre ações. Não mede a fração causal da queda.
- A comparação de TIR antes e depois mantém as projeções fixas e mede só o efeito do preço.
- Os pesos da carteira, o Sharpe e o Kelly usam a TIR de longo prazo como retorno esperado de um ano. É uma hipótese
  adicional.
