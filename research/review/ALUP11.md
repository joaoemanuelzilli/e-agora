# ALUP11 (Alupar): revisão independente (red team G11, 26/10/2026)

**Veredito: ok.** Não mudei nenhuma premissa. A base regulatória via overrides está bem construída e é coerente com o release 4T25/2T26. O único ponto relevante é metodológico (o valor dos minoritários), e não muda a TIR de dono.

Motor (foto R$ 31,31/unit): VJ **R$ 9,24/unit**, TIR implícita **10,8%**, TIR 3 anos +13,3%. Métodos: DCF −R$ 3,24 (piso 0), DDM R$ 9,49, múltiplos R$ 27,47. Unit = 1 ON + 2 PN; 988,9 mi ações = 329,6 mi units. ALUP3 R$ 10,50 + 2 × ALUP4 R$ 10,08 = R$ 30,66, perto da unit. Market cap de R$ 10.321 mi confere.

## Conferido e coerente
- **Base regulatória.** O IFRS da transmissão (ICPC 01/CPC 47) infla receita, EBITDA e LL: LL IFRS 2025 de R$ 1.216 mi contra R$ 737,6 mi regulatório. Receita regulatória de R$ 3.545,5 mi, margem de 79,5%; o EBITDA de 2T26 dá 76,6%.
- **DL.** O motor usa DL CVM de R$ 9.523 mi contra R$ 9.499,5 mi da companhia; dívida e caixa são os mesmos nas duas contabilidades. `other_debt_like` de R$ 186 mi: dividendos a pagar mais derivativos.
- **Crescimento contratado.** Receita de +9/+8/+9/+14/+6% segue o cronograma de RAP: TAP R$ 83 mi (2028); TPC R$ 277 mi e TCN R$ 177 mi (2029, daí o +14%); LatAm ~US$ 105 mi. O capex do 2S26 a 2030 (~R$ 8,4 bi) é compatível com a carteira (TAP + TPC + TCN + LatAm US$ 732 mi × R$ 5,49 + Lote 07 × 0,7 ≈ R$ 9,2 bi, parte já gasta).
- **Minoritários a 42% do LL**, igual a 2025 regulatório (541 / 1.279).
- **IR de 12–14%** (lucro presumido nas SPEs), D&A de 15% e custo da DL de 10,8% (6M26 a 11,5% a.a., com IPCA caindo). Exposição líquida a CDI ~nula: CDI ~R$ 3–4 bi contra caixa de R$ 5,4 bi.
- **Perpetuidade conservadora** (g 3,5%; ROIC_T 12% ≈ WACC regulatório), coerente com concessões finitas (as antigas vencem em 2030–35).

## Achados (sem mudança)
| # | Severidade | Achado | Evidência / sensibilidade |
|---|---|---|---|
| 1 | Média (metodológica) | `minority_value` fixo de R$ 4,2 bi nos dois métodos de EV. Os minoritários têm 42% do LL. No DCF a WACC de 17,2%, o equity total é R$ 3.131 mi, e 42% dele seriam R$ 1,3 bi: o valor fixo empurra o DCF para negativo. A 7x EBITDA, o equity total é R$ 12.862 mi, e 42% seriam R$ 5,4 bi: o valor fixo os subestima. Nenhum valor único é coerente com os dois métodos. | Minoritários a R$ 2,26 bi (mesmo múltiplo LL→valor do DDM a Ke 25%): VJ 11,29. A R$ 5,4 bi: VJ 8,79. A TIR implícita não muda (10,8%). |
| 2 | Baixa | Payout de 45–50% do LL regulatório, contra ~38% pago em 2025 (R$ 0,21/unit/tri ≈ R$ 277 mi sobre R$ 737,6 mi). | Payout de ~38%: VJ 9,17 / TIR 10,7%. |
| 3 | Baixa | Receita de 2026 a +9%, com o 1S26 a +13,3% e reajuste da RAP de jul/26. | +11%: VJ 9,57 / TIR 10,9%. Leve viés conservador. |
| 4 | Baixa | O custo da DL cai com o IPCA do Focus pré-choque. A RAP também é IPCA, então o hedge é natural. | Kd sem queda: VJ 9,03 / TIR 10,5%. |
| 5 | Metodológica | DCF negativo com peso de 50%. | Sem DCF: VJ 18,5. Ainda ~40% abaixo do preço. |

A conclusão é robusta: a TIR de dono fica entre 10,5% e 10,9% em todas as variantes. É a melhor relativa do grupo, ainda bem abaixo de 25%.

## Mudanças
Nenhuma. VJ **R$ 9,24** e TIR **10,8%** antes e depois.

## O que não deu para verificar
- As datas de vencimento ativo a ativo das concessões antigas e a regra de renovação ou relicitação.
- O resultado financeiro e a equivalência regulatórios do 1S26 (`other_financial` +R$ 90–110 mi contra equivalência IFRS de R$ 386 mi LTM).
- O consenso.
