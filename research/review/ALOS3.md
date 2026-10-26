# ALOS3 — revisão independente (red team) · 26/10/2026

**Veredito: ajustada.** Há um erro objetivo de contagem de proventos e três incoerências de base: minoritários, IR e a forma como os proventos já declarados entravam no motor. Para manter a neutralidade, refiz os múltiplos-alvo na mesma base em que o motor os aplica, o que puxa o valor para cima. A conclusão do estudo se mantém e fica mais forte: valor justo bem abaixo do preço e TIR de dono longe de 25%. Original em `research/review/ALOS3.orig.json`.

Preço da foto do estudo: R$ 26,87.

| | Antes | Depois |
|---|---|---|
| Valor justo | R$ 14,90 | **R$ 13,07** (−12%) |
| DCF / DDM | 11,08 / 12,53 | 8,78 / 10,56 |
| P/L / EV/EBITDA (perna de 25%) | 24,21 / 25,59 | 21,86 / 26,46 |
| TIR implícita (DDM) | 13,4% | **11,9%** |
| TIR 3 anos (saída a P/L-alvo × LPA 2029E) | 12,3% | **6,8%** |
| LL 2027E ("lucro" do motor) | R$ 1.274 mi | R$ 1.041 mi |
| Proventos 2026 stub / 2027E | R$ 259 mi / R$ 1.210 mi | R$ 290 mi / R$ 989 mi |
| Cenários bear / bull / esperado | 12,90 / 16,50 / 14,72 | 11,16 / 14,61 / 12,90 |
| Monte Carlo p10–p50–p90 · P(valor > preço) | 12,90–14,88–16,95 · 0% | 11,17–13,05–15,03 · 0% |

## Achados

### 1. Faltava uma das cinco parcelas de proventos que já não são do comprador (média, erro objetivo, corrigido)
- A premissa somava 4 parcelas de ~R$ 146 mi (R$ 584 mi). O calendário B3 mostra **5 parcelas** de R$ 0,2919/ação com data-com antes de hoje e pagamento depois do balanço de 30/06:
  - dc 22/06 → pagamento 02/07;
  - dc 23/07 → 04/08;
  - dc 21/08 → 02/09;
  - dc 22/09 → 02/10;
  - dc 22/10 → 04/11.
- Total: 5 × 0,2919 × 500,1 mi = **R$ 730 mi**. A parcela de 22/06 foi a que ficou de fora.
- O balanço confirma: "Dividendos a pagar" de **R$ 438,0 mi** em 30/06 equivale às 3 parcelas aprovadas em 17/06. As outras 2 foram aprovadas em 15/09.
- A premissa também tratava esse caixa só como ajuste estático (`other_debt_like`). Assim, a DL projetada nunca pagava esses R$ 730 mi e o DDM e o P/L recebiam juros sobre um caixa que vai embora entre julho e novembro. Isso inflava o LL em ~R$ 100 mi/ano antes de IR.
- Mudança: `overrides.base.net_debt` passa de R$ 3.680,9 mi para **R$ 4.410,9 mi** (DL CVM + R$ 730 mi).
- Impacto isolado (junto com o achado 4): valor justo 14,90 → 13,97; TIR 13,4% → 12,8%.

### 2. Participação de minoritários contradiz a CVM (média, corrigido)
- `minority_share_ni` era 2%. Na CVM, os minoritários ficaram com R$ 36,4 mi de R$ 592,8 mi de LL no 1S26 (6,1%) e com R$ 17,7 mi no 2T26, já depois de o PL de minoritários cair de R$ 753 mi para R$ 96 mi no 1T26. No LTM, a fatia é 9,3%.
- Um PL contábil de R$ 96 mi não sustenta um lucro de ~R$ 71 mi/ano: seria ROE de 74%.
- Mudança: `minority_share_ni` **0,06** e `minority_value` **R$ 320 mi** (≈ 6% do equity DCF antes de minoritários; antes eram os R$ 96 mi contábeis).
- Sensibilidade com 4% e R$ 220 mi: valor justo 13,31; TIR 12,1%.

### 3. IR de 10% incoerente com a "D&A econômica" (média, corrigido)
- A premissa tira da D&A a amortização da mais-valia da fusão. A D&A cai de ~22% para 8% da receita, de modo que o LAIR do motor fica perto do FFO. Faz sentido.
- O problema é o IR de 10%. Ele foi calibrado no IR efetivo contábil de 6,5–7,1% (2024–25). Esse número é o IR corrente **menos** o crédito de IR diferido gerado pela própria amortização da mais-valia: em 2025, corrente −R$ 195,4 mi e diferido +R$ 123,1 mi.
- O IR corrente, que é o que sai em caixa, foi R$ 199,8 mi (2024), R$ 195,4 mi (2025) e R$ 107,0 mi no 1S26. Isso dá ~7% da receita e **14–16% do LAIR sem PPA** (2025: 195/1.424; 1S26: 107/664).
- Mudança: `tax_rate` 0,10 → **0,15**. O IR de 2027E fica em R$ 195 mi, igual ao corrente de 2025. Antes eram R$ 132 mi.
- O motor usa uma única alíquota para o FCFF e para o LL. Sobre o EBIT, 15% dá R$ 302 mi, entre o IR efetivo (~R$ 213 mi) e o IR desalavancado pleno (~R$ 400 mi).
- Sensibilidade com 12%: valor justo 13,62; TIR 12,2%; TIR 3a 8,8%.

### 4. Derivativos e aquisições a pagar fora da ponte (baixa, corrigido pela spec)
- A premissa deixou os derivativos de fora por "saldo não confirmado". A CVM confirma: derivativos passivos (2.02.02.02.10) de **R$ 180,2 mi** e obrigações por compra de ativos de R$ 2,5 + 15,1 mi.
- A spec manda tratar ambos como dívida. Mudança: `other_debt_like` passa a ser **R$ 197,8 mi** (as parcelas de proventos foram para a DL-base).

### 5. Payout do stub 2026 não reproduzia a intenção declarada (baixa, corrigido)
- A intenção era pagar ao comprador as 2 parcelas restantes: dc 23/11 (R$ 0,2919, já aprovada) e dezembro (guidance de R$ 0,27–0,29). Isso dá ~R$ 290 mi.
- O payout 0,43 rendia R$ 259 mi; depois das correções, renderia R$ 227 mi. Mudança: 0,43 → **0,58**, que dá R$ 290 mi.

### 6. Múltiplos-alvo refeitos na base certa (neutralidade, corrigido para cima)
- **P/L.** O "lucro" do motor é FFO menos a D&A econômica (8% da receita), ou seja, ≈ AFFO, e não o FFO a que o P/FFO de 9,5x se referia. Na mesma regra (+300 bp): AFFO LTM ≈ R$ 1.375 − 232 = R$ 1.143 mi (R$ 2,29/ação). O P/AFFO pré-eleição era 15,4x, o que dá **10,5x**.
- **EV/EBITDA.** O EV de 9,9x omitia itens que a ponte desconta: parcelas declaradas, derivativos e o valor econômico dos minoritários. Com eles, o EV pré-eleição é R$ 22,5 bi, ou 10,5x o EBITDA CVM LTM de R$ 2.141 mi, o que dá **8,0x**.
- Esse ajuste aumenta o valor justo. Sem ele, o justo seria ~R$ 12,5.

## O que verifiquei e está coerente
- **DL.** A dívida está em "outras obrigações" na CVM (R$ 6.871 mi) e o pipeline a captura corretamente. Os arrendamentos (R$ 208,8 mi) entram na DL e a aplicação de longo prazo (R$ 196,7 mi) entra no caixa.
- **Custo da DL** (15,8–16,5%). Com R$ 6,87 bi a CDI+0,57% e caixa de R$ 3,4 bi, os forwards de hoje (CDI ~15,2% em 2027, ~15,8–16% em 2028–30) dão 15,4–16,2% sobre a DL. O 1S26 deu 15,8% efetivo.
- **Ke e WACC.** `kd` 15,2% e `wd` 0,17, igual à proporção de mercado pré-eleição (17,3%).
- **Ações.** 500,10 mi (CVM 30/06; `b3_vs_cvm` = 1).
- **EBITDA 2026E.** R$ 2,175 bi, dentro do guidance de R$ 2,17–2,24 bi.
- **Capex.** R$ 444 mi, no topo do guidance de R$ 350–450 mi.
- **Ganhos de capital** (venda de participações) estão fora da projeção. O modelo não usa valor justo das propriedades.

## Sensibilidade das conclusões (sobre a versão corrigida)
| Teste | Justo | TIR | TIR 3a |
|---|---|---|---|
| ROIC/ROE terminais 15% (em vez de 25%; os contábeis de 2030 são 11–12%, inflados pela mais-valia) | 12,31 | 11,1% | 6,8% |
| Payout 105% / 117% do "lucro" do motor | 13,16 / 13,26 | 11,9% | 6,5% / 6,1% |
| Venda ao KAML11 de R$ 0,8 bi (−NOI ~R$ 76 mi; −DL R$ 640 mi à vista) | 13,74 | 12,2% | 8,6% |

Nenhum cenário plausível aproxima a TIR de 25%: o DCF reverso exige crescimento médio de ~21% a.a.

## Não verificado / limitações
- Cronograma, covenants e indexadores da dívida (release integral não obtido). Não sei se os derivativos têm hedge accounting.
- Composição dos minoritários remanescentes e a operação do 1T26 que reduziu o PL deles em R$ 671 mi (provável desconsolidação de SPE).
- O crescimento de 3% em 2027 sem vendas de ativos parece baixo para IGP-M + 1,5–2 pp. Não alterei por ser julgamento de cenário (choque na classe média).
- Cap rate da tese: com todos os itens da ponte, o EV de hoje é ~R$ 18,4 bi, o que dá cap rate de ~13,1% sobre o NOI anualizado do 2T26, e não 14,4%. A conclusão qualitativa (desconto contra os ~9,5% das transações privadas) não muda.
