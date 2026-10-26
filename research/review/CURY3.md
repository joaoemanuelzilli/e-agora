# Revisão independente — CURY3 (Cury) · 26/10/2026

**Veredito: ajustada (efeito pequeno).** Corrigi dois itens da ponte de valor:
- os dividendos pós-balanço estavam superestimados em R$ 80 mi;
- os minoritários estavam abaixo da regra da própria nota.

O valor justo vai de R$ 22,74 para R$ 22,80, e a TIR fica igual. A conclusão é robusta: em todos os testes plausíveis, o valor justo fica entre R$ 20,7 e 23,9, abaixo do preço de R$ 26,94, e a TIR fica entre 19,4% e 20,4%, contra Ke de 25%. A melhor operadora do grupo, mas cara a 25%.

| | Valor justo | TIR implícita | TIR 3 anos | P(valor > preço) |
|---|---|---|---|---|
| Analista (preço R$ 26,94, foto 13h02) | R$ 22,74 | 19,5% | 25,9% | 20% |
| Após revisão | **R$ 22,80** | **19,5%** | **25,9%** | 20% |

## O que conferi e está coerente

**Ações e DL.**
- São 308,05 mi de ações (CVM = B3).
- A DL é de −290,6: dívida bruta de 1.343,2 menos caixa de 1.633,7. Não há passivo de cessão no balanço.

**Juros capitalizados (+0,3 p.p.).** Correspondem a R$ 9,5 mi no 1S26 (0,29% da ROL). O efeito é imaterial e o ajuste é neutro no LL.

**WACC = Ke.** Com caixa líquido, o peso de dívida é 0, então a questão do RET e do Kd não se aplica.

**IR.** A alíquota de 11,5% sobre o LAIR (11,4% em 2024–25) dá IR/ROL de 2,6%, igual ao histórico.

**Minoritários de 12%.** O realizado foi 11,6% no LTM e 13,4% no 1S26.

**Margem CVM de 24,0% para 22,5%.** O LTM é 24,3%, o 2T26 ficou em 22,9% e a média de 5 anos é 21,7%. A margem REF é de 43,5%.

**Capital de giro de 0,32.** O CG operacional que calculei (clientes CP+LP + estoques CP+LP + outros − fornecedores − terrenos a pagar − adiantamentos − obrigações/provisões) foi de 0,20x (2023), 0,21x, 0,23x e 0,27x (2T26). O marginal foi de 0,34x (2023→2T26) e 0,39x (2024→2T26). O 0,32 é um pouco leve; com 0,36, o valor seria R$ 22,60.

**Payout de 75–85%.** O FCFE/LL do próprio modelo é de 68–87%, e o histórico vai de 68% a 139%. A DL praticamente não se move (caixa líquido de 0,2x o EBITDA), então o payout é coerente com a geração de caixa.

**Perpetuidade.** O ROIC terminal de 40% e o ROE de 45% são um fade conservador, contra 57–72% no período explícito e ~60% implícitos no capital de giro de 0,32. Com ROIC_T de 60%, o valor seria R$ 23,06.

## Achados

| # | Sev. | Achado | Evidência | Efeito (valor justo / TIR) |
|---|---|---|---|---|
| 1 | média · **corrigido** | `other_debt_like` de 300 contava dividendo já pago antes de 30/06 | O PL controlador variou: 1.381,6 + LL do 1S26 de 572,7 − 1.655,0 = **R$ 299,6 mi** em dividendos no 1S26, o que equivale a 1T26 (0,5194 × 308,05 = 160) + complementar 2025 (0,4545 × 308,05 = 140). A DFC do 1S26 mostra R$ 270 mi pagos, e o balanço de 30/06, R$ 30 mi a pagar. Logo o caixa-base já está líquido de R$ 270 mi, e só restam R$ 30 mi + R$ 190 mi (1S26, ex 14/08, pago 08/09) = **R$ 220 mi**. O analista somou os R$ 140 mi inteiros e abateu os R$ 30 mi | +R$ 0,16 |
| 2 | baixa · **corrigido** | `minority_value` de 850 abaixo da regra da nota | A regra é ~12% × equity 100%. O equity 100% é EV 7.431 + caixa 291 − 220 = 7.501, e 12% disso dá 900 | −R$ 0,10 |
| 3 | média (método, mantido) | Perna de múltiplos 33% acima de DCF e DDM | A perna dá R$ 28,4, contra DCF de 21,4 e DDM de 19,9. O P/L-alvo de 7x contrasta com o P/L de Gordon de ~4,5–5x a Ke de 25% (payout de 85%, g de 5%), que o próprio analista cita. Mantido, porque segue a spec (múltiplos de mercado); é o mesmo ponto do revisor de CYRE3 | P/L 5x e EV/EBITDA 3,9x: R$ 20,71; TIR 3a de 10,1% |
| 4 | baixa (conservador) | Receita de 2026 com +21% implica 2S26 de R$ 3,23 bi, abaixo de 2× o 2T26 (R$ 3,38 bi) | O 1S26 cresceu +29%. A prévia do 3T26 trouxe vendas de +11,4% e VSO de 39,7%, e o REF é de R$ 8,8 bi | +24% em 2026: R$ 23,37 / 19,9% |
| 5 | baixa (conservador) | Kd cai de 13,5% para 11,5%, contra DI1F29–F31 de 15,4–15,7% | A empresa tem caixa líquido, então a queda reduz a receita financeira | Kd plano em 13,5%: R$ 22,82 / 19,6% |
| 6 | info | Margem estável | Mantendo 24,3% até 2030 | R$ 23,89 / 20,4% |

Se o complementar de 2025 não tivesse sido pago (hipótese que o balanço contradiz), o ajuste seria de 330 e o valor justo, R$ 22,58. A faixa é estreita de qualquer forma.

## Mudanças em `research/CURY3.json` (original em `research/review/CURY3.orig.json`)
- **`adjustments.other_debt_like`:** 300 → 220.
- **`adjustments.minority_value`:** 850 → 900.
- Nota explicativa acrescentada em `adjustments.notes`.
- **Efeito:** valor justo de R$ 22,74 para R$ 22,80. TIR implícita (19,5%) e TIR em 3 anos (25,9%) inalteradas.
- O motor foi re-rodado (`EAGORA_SNAPSHOT=1`).

## O que não deu para verificar
- Cronograma efetivo de pagamento do complementar de 2025. A B3 informa 31/12/2026, mas o balanço e a DFC indicam pagamento quase integral no 1S26.
- Participação da Cyrela.
- Custo médio e indexação da dívida (SFH/CRI).
- ITR do 3T26 (só a prévia operacional).
