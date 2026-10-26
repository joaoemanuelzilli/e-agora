# MULT3 — revisão independente (red team) · 26/10/2026

**Veredito: ok, sem alteração.** Não encontrei erro objetivo. Premissas, DL, contagem de ações e ajustes conferem com CVM e B3. Os pontos abaixo têm efeitos pequenos e em sentidos opostos. A conclusão do estudo é robusta: em todos os testes, o valor justo fica entre R$ 14,2 e 15,9, contra preço de R$ 27,96, e a TIR implícita entre 13,0% e 14,1%, contra Ke de 25%.

Preço da foto do estudo: R$ 27,96. Valor justo R$ 14,84 (DCF 9,54 · DDM 11,42 · múltiplos 28,84). TIR implícita 13,6%; TIR 3a 17,7%. Saída implícita do DCF: 3,9x EBITDA.

## O que conferi (ok)
- **Ações.** 491,05 mi = 513,16 mi emitidas − 22,12 mi em tesouraria (CVM 30/06; `b3_vs_cvm` = 1).
- **DL.** R$ 4.551 mi = debêntures e empréstimos (2.01.04 + 2.02.01) − caixa e aplicações, igual ao release. Não há CRI/dívida em "outras obrigações", arrendamentos ou obrigações por aquisição remanescentes (zeradas desde 2025). As propriedades estão ao custo, sem ganho de valor justo no lucro.
- **`other_debt_like` R$ 618 mi.** O calendário B3 confirma 4 JCPs com data-com já passada e ainda não pagos:
  - dc 29/12/25 → pagamento 30/12/26;
  - dc 30/03/26 → 31/03/27;
  - dc 30/06/26 → 30/06/27;
  - dc 30/09/26 → 30/09/27.
  - Os três primeiros, líquidos de IRRF, somam ≈ R$ 479 mi de "Dividendos e JCP a pagar" em 30/06, mais os R$ 139 mi aprovados em 25/09. O stub de 2026 (payout 0,22 → R$ 130 mi) equivale ao JCP do 4T26, o único que cabe ao comprador.
- **Margem EBITDA** 73–74,5%. A média de 2023–25 foi 73,3%; o LTM recorrente, sem o crédito de PIS/COFINS de R$ 253 mi, foi 71,6%, com mix imobiliário do 1T26.
- **D&A** 5%, igual a 2025.
- **Capex** 17% → 12% da receita. O stub do 2S26 (R$ 245 mi) é igual ao 1S26 (R$ 216–246 mi, com 2 inaugurações no 2S). Na perpetuidade, o reinvestimento implícito (g/ROIC = 20% do NOPAT) é maior que o de 2030E (13%).
- **Payout** 55–70%. É sustentável: o FCFE de 2027E fica em ~R$ 1,0 bi contra proventos de R$ 728 mi, e a DL/EBITDA cai de 1,9x para 1,1x.
- **WACC.** `wd` 0,20, igual ao mercado pré-eleição (19,8%), e Kd de 15,5%, coerente com CDI+0,63% na curva de hoje.
- **Múltiplos-alvo.** Mesma regra (+300 bp) e mesma base recorrente do LPA do motor:
  - P/L 15,5x → 10,5x;
  - EV/EBITDA 10,9x (11,2x com os R$ 618 mi) → 8,2–8,4x; 8,5x usado.

## Achados (nenhum altera a conclusão)
1. **2026E conservador frente ao 1S26 (baixa, não alterado).**
   - Receita +5% e margem 73% implicam 2S26 com receita −5% e EBITDA −7% a/a.
   - O 1S26 recorrente cresceu +16,5% em receita e +11,7% em EBITDA, com venda imobiliária forte no 1T26 (custo de imóveis de R$ 228 mi). O 4T25 teve margem atípica de 78%.
   - Como a receita imobiliária é volátil, não há evidência firme de erro.
   - Se 2026 crescer 8,5% (1S26 real + 2S25 × 1,06): justo 15,63 (+0,79); TIR 14,0%; TIR 3a 20,3%.
2. **IR de 15% acima do IR caixa (baixa, conservador, não alterado).**
   - IR corrente: R$ 98 mi em 2025 (7,4% do LAIR) e R$ 74 mi no 1S26 (8,5%). O diferido soma ~45% do total e o passivo diferido cresce ~R$ 90 mi/ano (R$ 286 → 529 mi entre 2023 e 2T26).
   - Sem nota explicativa, não dá para saber se ele se reverte (ex.: lucro de incorporação tributado no caixa). O efetivo contábil (14–15%) é a escolha prudente.
   - Com 10%: justo 15,90; TIR 14,1%.
3. **Defasagem de ~12 meses no pagamento do JCP (baixa, não alterado).**
   - O motor desconta os proventos no ano em que são declarados, mas a Multiplan paga ~1 ano depois (ex.: dc 30/03/26 → 31/03/27). Isso infla o DDM.
   - Ao mesmo tempo, o motor não tira da DL os R$ 618 mi que saem até set/27, e superestima a DL futura por pagar os JCPs novos sem defasagem. Os dois efeitos se compensam em parte.
   - Defasando 1 ano, com o caixa retido rendendo ~11% líquido: DDM 11,42 → 10,14 e TIR 13,6% → 13,4%.
   - Levando também os R$ 618 mi para a DL: justo 14,50 e TIR 13,2% só com essa mudança; somando a defasagem, justo ~14,2 e TIR ~13,0%.
   - O motor não modela defasagem; mantive a premissa.
4. **Custo da DL abaixo dos forwards em 2028–30 (baixa, não alterado).**
   - Usado: 13,3 / 13,0 / 12,6%. Os forwards dão CDI de ~15,8–16%. Com o fator empírico de 0,82–0,85× (juros capitalizados nas obras) sobre CDI+0,63%, o custo seria ~14,0–14,1%.
   - Com 12,5 / 13,4 / 14,0 / 14,1 / 14,1%: justo 14,77; TIR 13,4%; TIR 3a 16,6%.
5. **ROIC/ROE terminais de 25% (julgamento).**
   - São defensáveis para aluguel indexado ao IGP-DI, mas ficam acima do ROE contábil de 2030E (20%) e do ROIC de 2030E (17,7%).
   - Com 18%: justo 14,21; TIR 13,0%. A Ke de 25% domina a conclusão: a 40%, o justo só sobe para ~15,4.

## Não verificado
- Composição da receita imobiliária por trimestre e do 4T25.
- Saldo de créditos de PIS/COFINS a compensar (não somado: conservador).
- Natureza do passivo de IR diferido.
- Efeito líquido da reforma tributária (IBS/CBS) sobre a locação a partir de 2027.
