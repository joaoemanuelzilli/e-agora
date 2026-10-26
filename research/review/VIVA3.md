# Revisão independente — VIVA3 (Vivara) · 26/10/2026

**Veredito: ok.** Não achei erro objetivo. Três premissas (capex com direito de uso, capital de giro e IR) ficam no lado favorável do histórico CVM. Cada uma move o valor justo em menos de 5%, e somadas, ~6%. Nenhuma alteração em `research/VIVA3.json`.

Preço de referência (foto B3): R$ 19,47. Resultado do motor, inalterado:
- Valor justo: **R$ 13,31** (DCF 9,79 · DDM 9,59 · múltiplos 24,07).
- TIR implícita: **15,4%**.
- TIR de 3 anos: **30,1%**.

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +10 / 9 / 9 / 8 / 7% | CAGR 3a de 18%; 1S26 +10,1% (R$ 1.428,6 mi); SSS 8% | ok, abaixo do histórico |
| Margem EBITDA (IFRS-16) | 27,8% → 28% | 2021–25: 25,0 / 26,6 / 26,7 / 32,5* / 29,0%; LTM 28,2%. 2S26 implícito: 29,3%, contra 30,3% no 2S25. | ok (*2024 com R$ 94 mi de outras receitas) |
| D&A | 5,0% | 2025: 5,0–5,4%; LTM 4,9% | ok |
| Capex (com direito de uso) | 6,2% → 5,8% | Capex caixa: 8,1% (2023), 5,0% (2024), 2,7% (2025), 3,0% (1S26). Adições + remensurações de arrendamento (roll-forward do passivo): 3,9% / 4,6% / 5,9% / 3,1%. Total: 12,0% / 9,6% / 8,6% / 6,1%. | No limite inferior; ver achado 1 |
| Capital de giro | 55% da receita incremental | (Receb. + estoques − fornecedores)/receita: 69% (2023), 74% (2024), 75% (2025), 77% (LTM). Marginal: 80% em 2024→25 e 91% em 2023→25. | Otimista; ver achado 2 |
| IR | 14% → 18% | Corrente 18,3% (2025) e 19,6% (1S26); pago em caixa 14,3% (2025). O diferido ativo (R$ 626 mi) cresce R$ 115–140 mi/ano e não entra como ativo. | Levemente favorável; ver achado 3 |
| Resultado financeiro | 17% → 14% × DL | Modelo 2026: −137,5. Real: 1S26 anualizado −145; LTM −158. A DL é quase toda arrendamento (707 de 809). | ok |
| Payout | 35% → 55% | 2025: 83% (antecipação de tributação); nada pago no 1S26. A DL projetada cai de 809 para 200. | ok |
| ROIC_T / ROE_T | 17% / 20% | Projetado para 2030: 17,8% / 18,0% | ok (ROE_T de 18%: R$ 13,26, TIR implícita 15,1%) |
| WACC | wd 12%, Kd 15,5% | DL 809 / (809 + valor de mercado pré-eleição 6.356) = 11,3% | ok |
| DL base / debt-like | 809,1 / +39 | 518,3 + 707,4 − 416,7; swap 4131 (36,6) + convênio (2,6) = dívida bruta do release, R$ 557,5 mi | ok |
| Ações | 235,14 mi | 236,20 mi − 1,06 mi em tesouraria | ok |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | R$ 13,31 | 15,4% | 30,1% |
| Capital de giro 75% (intensidade atual) | R$ 12,80 | 15,1% | 28,6% |
| Capex +1 p.p. | R$ 12,99 | 15,2% | 29,2% |
| IR 19% fixo (corrente) | R$ 12,88 | 15,1% | 28,0% |
| Combinado (capital de giro 65% + capex +0,5 p.p. + IR 18–19%) | R$ 12,53 | 14,9% | 26,9% |
| Margem −1 p.p. | R$ 12,54 | 14,8% | 26,6% |
| Margem +1 p.p. | R$ 14,09 | 15,9% | 33,5% |
| Crescimento −2 p.p. | R$ 12,67 | 14,7% | 26,0% |
| Custo da DL 16% fixo | R$ 13,32 | 15,3% | 29,7% |
| P/L-alvo 11x | R$ 13,78 | 15,4% | 38,7% |

A conclusão é robusta: em qualquer caso o valor intrínseco a Ke 25% fica em R$ 12,5–14,1, abaixo do preço. A TIR implícita fica em ~15%. Os ~27–30% da TIR de 3 anos vêm inteiramente da saída a 9,5x P/L em 2029, ou seja, de reversão de múltiplo, não de valor intrínseco. Isso coincide com o dossiê.

## Achados
1. **(média) Capex com direito de uso.** O dossiê diz que as adições de arrendamento são de ~3% da receita, mas o roll-forward do passivo dá 4,6% em 2024 e 5,9% em 2025 (o 1S26 ficou em 3,1%). O investimento líquido projetado (capex − D&A) é de ~1,0–1,2% da receita. Com isso, a intensidade de ativo fixo cai de 31,6% (2025) para ~25% (2030). A tendência de 2023–25 (35% → 31,6%) sustenta a direção, mas não necessariamente o ritmo. Com +1 p.p. de capex, o valor justo vai a R$ 12,99. Não alterado.
2. **(média) Capital de giro marginal de 55%, contra 80–91% no histórico recente.** A premissa supõe sucesso do plano de estoques (582 → ~500 dias), e a NWC/receita cairia de 75% para 68% em 2030. O choque cambial encarece o metal de reposição em R$, o que pesa contra. Com 75%, o valor justo vai a R$ 12,80. Não alterado: é uma premissa de eficiência explícita, com guidance qualitativo.
3. **(baixa) IR de 14–16% em 2026–28**, abaixo do IR corrente de 18–20% (o caixa pago em 2025 foi 14%). Com 19% fixo, o valor justo vai a R$ 12,88.
4. **(informativo, conservador) P/L-alvo.** O P/L de 9,5x é a média de 2024–25 sobre o lucro reportado (alíquota ~0%), mas aqui é aplicado ao LPA tributado a 15%. Equivale a ~11x no conceito histórico; com 11x, o valor justo seria R$ 13,78.

## Mudanças
Nenhuma.

## O que não deu para verificar
- Natureza do IR diferido ativo (lucro intercompany × prejuízo fiscal da varejista) e prazo dos incentivos SUDAM/ZFM.
- Quanto do salto de R$ 95 mi no passivo de arrendamento do 3T25 é loja nova e quanto é remensuração ou renovação.
- Custo e prazo da dívida e posição de antecipação de recebíveis: o salto de +29% a/a nos recebíveis do 2T26 pode ser só fim de antecipação.
- Repasse do metal mais caro em 2027 e o hedge natural do estoque.
