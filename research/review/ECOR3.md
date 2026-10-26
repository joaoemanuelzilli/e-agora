# ECOR3 (EcoRodovias): revisão independente

**Veredito: ok.** Não achei erro objetivo nas premissas e não alterei `research/ECOR3.json`.

| | Valor |
|---|---|
| Valor justo (motor) | R$ 2,15 |
| Preço (foto B3) | R$ 5,45 |
| Upside | −61% |
| TIR implícita | 17,2% |
| TIR 3 anos | 13,2% |

A conclusão, valor abaixo do preço a Ke 25%, resiste a todos os testes que fiz.

## Conferências que bateram (CVM × premissas)
- **Receita-base sem construção:** 3.01 de 11.521,1 − DVA 7.01.03 de 4.114,8 = **7.406,3**. Isso é a receita bruta de pedágio da DVA (8.152,0) líquida de ~9% de impostos. Construção tem margem zero, então o EBITDA não muda.
- **EBITDA 2025:** 4.281,7 + 1.358,3 = 5.639,9. Inclui a reversão de impairment de +202,7 (3T25). O recorrente fica em 5.437 (73,4%).
  - 1S26 CVM: 2.691,6 sobre receita sem construção de 3.647,0 = **73,8%**.
  - Premissa 2026: 73%. Coerente.
- **D&A:** o 1T26 tem 549 contra 343 no 2T26, uma baixa pontual ligada ao encerramento da Ecosul em 04/03/2026. O run-rate do 2T26 (343 × 4 = 1.371, ou 18% da receita) sustenta os 19% projetados para 2026.
- **Capex:** a premissa é DFC 6.02.01+6.02.02 sem outorgas. A conta de 2025 é 6.884,5 − 2.268 (Raposo) = 4.616.
  - 1S26: 2.315 − 84 (Gerais) = 2.231.
  - O stub 2S26 do motor é 0,504 × 5.302 = 2.672. Fica em linha com o 2T26 anualizado (1.436 × 2).
  - Juros capitalizados (281/296/286 em 2023–25; 211 no 1S26) não estão no capex de caixa. Por isso o custo da DL é "bruto". Coerente.
- **Custo da DL (15%):** o real do 1S26 foi (1.567,8 × 2 + 210,6 × 2) / DL média de 22.751 = **15,6%**. Isso já inclui ~R$ 0,34 bi/ano de correção das obrigações com o poder concedente. No DDM não há dupla contagem, porque o DDM não deduz `other_debt_like`.
  - Uma checagem bottom-up dá cerca de 13–14% a partir de 2027: 77% da dívida em IPCA + ~7,5%, 20% em CDI + 1%, caixa a CDI.
  - A rampa de 15% → 13,5% é, portanto, levemente conservadora, mas defensável com o DI de hoje.
- **Debt-like 3.486:** BPP de 30/06/2026, obrigações com o poder concedente 156,1 + 3.186,1, leniência 1,6 + 45,5 e ANPC 22,0 + 74,6. Bate. Ativo de indenização do Ecoporto: 352.
- **DL-base:** 28.851,5 + arrendamentos 148,8 + 215,0 − caixa 5.371,4 = 23.844. Bate.
- **Ações e minoritários:** 695,6 mi ações e minoritários de 285. Bate. `minority_share_ni` de 0% é coerente: os minoritários tiveram prejuízo de −19 (2025) e −23 (1S26).
- **Receita 2027 (+16%):** a conta (7.628 − ~110 de Ecosul) × 1,09 + ~650 da Gerais dá ≈ 8.845, contra 8.849 no motor. Coerente com a companhia: Gerais "compensa integralmente" a Ecosul.
- **Múltiplos-alvo:** 5,3x = p10 histórico de 4,7x + ~0,6x das obrigações com o poder concedente (que o motor desconta). P/L 6x ≈ p10 de 5,7x. Coerente com o critério "piso de juros altos".

## Achados

| # | Severidade | Achado | Evidência | Impacto |
|---|---|---|---|---|
| 1 | baixa | IR de 2026 em 42% contra 105% efetivo no 1S26 | 1S26: LAIR 231,9 e IR 243,6. O lucro de 2026 do motor (315) implica 2S26 de ~304, contra 11 no 1S26 | Só afeta o LPA e o dividendo stub de 2026. Com IR de 60% em 2026, o justo fica em R$ 2,13 (−0,02) |
| 2 | baixa | Dossiê diz que "o valor residual equivale ao capital investido", mas não é o que o motor faz | TV de 27,9 bi ≈ 0,56× o capital investido de 2030 (PL 6,2 + DL 39,7 + obrigações 3,5 bi), porque o ROIC contábil de 2030 é 9,6% contra WACC de 15,9% | Só texto. A escolha ROIC_T ≈ WACC é neutra |
| 3 | baixa | Textos desatualizados | `summary` e `key_data` falam em "~R$ 2,5 vs R$ 5,1"; o dossiê fala em "TIR 17,9%" e "queda de 62%". O motor dá R$ 2,15, preço de R$ 5,45, TIR 17,2% e queda de 58,6% (13,15 → 5,45) | Cosmético. Sugiro ao líder atualizar o texto |
| 4 | info | O prazo de cada concessão não foi verificado | A Imigrantes, a mais antiga e a maior geradora, pode vencer bem antes de 2050 | Perpetuidade otimista para esse ativo. Não muda o justo, porque o DCF já é negativo e entra com zero na média |

## Sensibilidade (motor em memória; justo e TIR implícita / TIR 3 anos)

| Cenário | Justo | TIR implícita | TIR 3 anos |
|---|---|---|---|
| Base | 2,15 | 17,2% | 13,2% |
| Múltiplos na mediana de 5 anos (P/L 8,7x; EV/EBITDA 5,9x) | 3,07 | 17,2% | 33,5% |
| Custo da DL −150 bp em todos os anos | 2,74 | 21,5% | 36,5% |
| Capex 2027–30 −15% | 2,32 | 19,7% | 24,4% |
| IR 34% fixo | 2,23 | 17,6% | 15,6% |
| ROIC_T 25% | 2,15 | 17,2% | 13,2% |
| Ke 20% / 15% | 2,47 / 3,11 | 17,2% | 13,2% |

- **DCF:** para ficar positivo, o EV precisaria passar de R$ 27,3 bi. Isso exige uma saída de ~6,0x EBITDA 2030 a WACC 15,9%, contra 3,0x hoje. Não é plausível com esse hurdle.
- **Justo e TIR implícita:** o justo fica abaixo do preço e a TIR implícita abaixo de 25% em todos os casos.
- **TIR 3 anos:** é muito sensível ao múltiplo de saída e ao custo da dívida. É o equity alavancado de 4,3–4,7x DL/EBITDA. Leia como opção sobre juros, não como retorno base.

## Mudanças
Nenhuma. Valor justo R$ 2,15 e TIR 17,2% permanecem.

## O que não deu para verificar
- O vencimento de cada concessão, em especial a Imigrantes.
- O covenant de 4,75x na escritura (vem de relatório do Santander).
- O cronograma anual de capex de 2027–30 (não há guidance). Os R$ 27,6 bi de 2S26–30 cabem nos R$ 50,9 bi contratuais, mas sem abertura por ano.
- A receita de partida da Ecovias das Gerais.
- A natureza e a reversibilidade da "conta reserva – poder concedente" (R$ 1.981 mi), corretamente deixada fora do caixa.
