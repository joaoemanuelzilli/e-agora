# Carteiras pós-choque — 26/10/2026

Gerado por `pipeline/tests/portfolio.py` em 2026-10-28T17:09:12 (dados: `data/app/overview.json`, preços B3 ajustados 2016–2026, câmbio BCB). Ibovespa -14,6% no dia, dólar 9,2%, CDI 13,65%, DI longo ~15,5%. Limites: 20% por ação e 40% por setor B3. Estudo quantitativo com finalidade informativa; não é recomendação de investimento.

## Resumo

- **Carteira recomendada (alvo):** BEEF3 20 · MDNE3 10 · PLPL3 9 · VTRU3 8 · TEND3 4 · COGN3 3 · SEER3 3 · CEAB3 3 (% do capital) + **40% em CDI**. São as 8 oportunidades do estudo, com pesos de 50% máximo Sharpe (TIR − CDI) e 50% paridade de risco. 7 das 8 são Consumo Cíclico, então o limite de 40% por setor só permite investir 60%; o resto fica no CDI.
- **Tamanho (Kelly fracionado):** meio Kelly dá 28% do capital em ações no regime de choque (3 meses de volatilidade de crise) e 43%–60% no regime normal. Sugestão: entrar com ~28% e subir até 60% quando a volatilidade normalizar.
- **Risco ex-ante (carteira-alvo):** vol 19,5% a.a., beta 0,86 (beta de baixa 0,95), retorno esperado 21,5% a.a. (7,8% acima do CDI), Sharpe 0,40. VaR 95% de 1 mês: 7,5% (normal) e 24,2% no regime de crise; CVaR 12,1% no histórico 2016–2026 e 29,7% na crise. N efetivo 5,2; BEEF3 responde por 32% do risco.
- **Estresses (carteira-alvo):** Ibovespa −20% → -19,0% pelo beta de baixa, ou -31,8% repetindo a reação de hoje; DI +300 bp → -10,4%; dólar +20% → -5,3% no canal cambial puro e -19,7% com o co-movimento histórico da bolsa. Na reversão (Ibovespa +30%), 25,5%. No pregão de hoje a carteira teria rendido -23,2%; o beta de baixa previa -13,9%.
- **Monte Carlo 1 ano (deriva = TIR):** no regime normal, mediana 19,9%, p5 -16,7%, P(perda) 19% e P(abaixo do CDI) 39%. Com 3 meses de choque, mediana 20,6%, p5 -29,9%, P(perda) 26% e drawdown mediano -17,0%.
- **Alternativa totalmente diversificável:** o máximo Sharpe do universo de 59 (BEEF3 20 · BBAS3 19 · MDNE3 12 · PLPL3 11 · PINE4 10 · HAPV3 10 · VTRU3 9 · LEVE3 6 … (+1)) tem Sharpe 0,44, mas inclui nomes fora das oportunidades (BBAS3, HAPV3, BRSR6). Dimensionado a meio Kelly (85% em ações), fica com risco parecido (vol 22,1%, Ibovespa −20% → -21,9%).
- **Histórico de crashes:** em 2017-05-18, as mais caídas subiram 25,9% em 3m (mediana 18,7%; 89% acima do índice), contra 11,4% do Ibovespa. Em 12m, a mediana delas foi 21,4%, contra 28,1% do índice, e a das mais baratas por P/L 37,0%. Depois da compra, o drawdown chegou a -21,1%; em 2020-03-16, as mais caídas subiram 44,5% em 3m (mediana 39,1%; 57% acima do índice), contra 34,3% do Ibovespa. Em 12m, a mediana delas foi 64,0%, contra 59,1% do índice, e a das mais baratas por P/L 44,3%. Depois da compra, o drawdown chegou a -19,3%. A reversão das mais caídas é forte e ampla nos primeiros 3–6 meses (correlação de ranking entre a queda e o retorno de 3m: -0,32 e -0,45), mas em 12 meses a vantagem da ação mediana diminui ou some. O P/L baixo, isolado, bateu o índice em 2017 e perdeu em 2020. Nos 16 episódios de queda diária ≤ −5% do Ibovespa desde 1998, comprar no 1º dia rendeu mediana de 9,3% em 12m (69% positivos). Em 2020, comprar em 26/02 rendeu 6,6%, contra 59,1% comprando em 16/03. O risco de entrar cedo justifica a entrada escalonada.

## Carteira recomendada

**Recomendada · 8 oportunidades (50% máx. Sharpe TIR + 50% paridade de risco), setor B3 ≤ 40%, excedente em CDI**

| Ação | % capital | % das ações | Setor / subsetor | TIR | Upside | Contrib. risco | Beta baixa | DI +300 | Dólar +20% puro |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| BEEF3 | 20,0% | 33,3% | Consumo não Cíclico / Alimentos Processados | 27,2% | 89,5% | 32,4% | 1,10 | -22,3% | 1,3% |
| MDNE3 | 10,5% | 17,5% | Consumo Cíclico / Construção Civil | 27,8% | 19,7% | 18,0% | 1,92 | -10,9% | -14,9% |
| PLPL3 | 8,5% | 14,2% | Consumo Cíclico / Construção Civil | 28,3% | 31,7% | 15,4% | 1,72 | -13,8% | -14,8% |
| VTRU3 | 8,1% | 13,5% | Consumo Cíclico / Diversos | 26,3% | 41,8% | 12,7% | 1,59 | -18,0% | -16,8% |
| TEND3 | 4,3% | 7,2% | Consumo Cíclico / Construção Civil | 25,4% | 26,4% | 6,9% | 1,90 | -14,7% | -15,5% |
| COGN3 | 3,0% | 5,0% | Consumo Cíclico / Diversos | 24,6% | 16,7% | 4,7% | 1,84 | -18,1% | -12,2% |
| SEER3 | 2,9% | 4,9% | Consumo Cíclico / Diversos | 24,4% | 28,6% | 4,9% | 2,32 | -16,6% | -6,9% |
| CEAB3 | 2,7% | 4,5% | Consumo Cíclico / Comércio | 22,1% | 0,5% | 5,0% | 1,82 | -18,3% | -6,9% |
| CDI | 40,0% | — | caixa | 13,65% | — | 0% | 0 | 0% | 0% |

Dimensionamento por Kelly (fração da carteira-alvo; exposição resultante em ações):

| Regime | Kelly cheio | Meio Kelly | Ações / capital |
|---|---:|---:|---:|
| analitico | 2,06 | 1,03 | 60% |
| normal_bootstrap | 1,44 | 0,72 | 43% |
| choque_3m | 0,92 | 0,46 | 28% |
| crise_ano | 0,55 | 0,28 | 17% |

Regra: começar no meio Kelly do regime de choque e subir até o meio Kelly normal/analítico (teto = parcela investida da carteira-alvo) quando a vol. 21d do Ibovespa sair do decil superior.

## Carteiras testadas

`op7_b3` = 8 oportunidades com setor B3 ≤ 40% (máximo investível 60%, resto em CDI); `op7_sub` = 8 oportunidades com subsetor B3 ≤ 40% (incorporação ≤ 40%, 100% investido); `u59` = universo de 59 com setor B3 ≤ 40%.

| Carteira | Pesos (% do capital) |
|---|---|
| op7_b3_ew | BEEF3 20 · COGN3 6 · MDNE3 6 · TEND3 6 · SEER3 6 · VTRU3 6 · CEAB3 6 · PLPL3 6 + CDI 40 |
| op7_b3_iv | BEEF3 20 · MDNE3 7 · TEND3 6 · VTRU3 6 · PLPL3 6 · COGN3 6 · SEER3 5 · CEAB3 5 + CDI 40 |
| op7_b3_rp | BEEF3 20 · TEND3 6 · SEER3 6 · PLPL3 6 · VTRU3 6 · COGN3 6 · MDNE3 6 · CEAB3 5 + CDI 40 |
| op7_b3_mv | BEEF3 20 · VTRU3 10 · MDNE3 9 · TEND3 8 · COGN3 5 · PLPL3 5 · SEER3 3 + CDI 40 |
| op7_b3_ms_tir | BEEF3 20 · MDNE3 15 · PLPL3 11 · VTRU3 10 · TEND3 3 · COGN3 0 + CDI 40 |
| op7_b3_ms_up | VTRU3 20 · BEEF3 20 · PLPL3 9 · TEND3 7 · SEER3 4 + CDI 40 |
| op7_sub_ew | CEAB3 12 · MDNE3 12 · PLPL3 12 · TEND3 12 · COGN3 12 · BEEF3 12 · SEER3 12 · VTRU3 12 |
| op7_sub_iv | BEEF3 14 · MDNE3 14 · TEND3 13 · VTRU3 13 · PLPL3 13 · COGN3 12 · SEER3 11 · CEAB3 11 |
| op7_sub_rp | BEEF3 18 · VTRU3 13 · MDNE3 13 · TEND3 12 · PLPL3 12 · COGN3 12 · SEER3 11 · CEAB3 10 |
| op7_sub_mv | BEEF3 20 · VTRU3 20 · MDNE3 18 · TEND3 13 · COGN3 12 · PLPL3 9 · SEER3 6 · CEAB3 2 |
| op7_sub_ms_tir | MDNE3 20 · BEEF3 20 · VTRU3 20 · PLPL3 18 · COGN3 13 · SEER3 7 · TEND3 2 |
| op7_sub_ms_up | VTRU3 20 · BEEF3 20 · PLPL3 20 · SEER3 18 · TEND3 16 · MDNE3 4 · COGN3 2 |
| u59_ew | RENT3 1 · MOVI3 1 · VAMO3 1 · SIMH3 1 · ECOR3 1 · MOTV3 1 · RAIL3 1 · CSAN3 1 … (+114) |
| u59_iv | TAEE11 1 · BBSE3 1 · ALUP11 1 · KLBN11 1 · ISAE4 1 · CPFE3 1 · EGIE3 1 · ITUB4 1 … (+114) |
| u59_rp | SUZB3 2 · PETR4 2 · PETR3 2 · BBSE3 2 · SLCE3 2 · PRIO3 2 · KLBN11 2 · VALE3 1 … (+114) |
| u59_mv | PETR4 11 · TAEE11 11 · BBSE3 11 · SUZB3 10 · SLCE3 8 · ABEV3 6 · VALE3 6 · ALUP11 5 … (+15) |
| u59_ms_tir | BEEF3 20 · BBAS3 19 · MDNE3 12 · PLPL3 11 · PINE4 10 · HAPV3 10 · VTRU3 9 · LEVE3 6 … (+1) |
| u59_ms_up | BEEF3 20 · VTRU3 20 · POMO4 14 · PLPL3 13 · HAPV3 9 · DESK3 8 · BBAS3 8 · SEER3 4 … (+1) |
| rec_op7_core | BEEF3 20 · MDNE3 10 · PLPL3 9 · VTRU3 8 · TEND3 4 · COGN3 3 · SEER3 3 · CEAB3 3 + CDI 40 |
| alt_u59_halfkelly | BEEF3 17 · BBAS3 16 · MDNE3 10 · PLPL3 10 · PINE4 8 · HAPV3 8 · VTRU3 7 · LEVE3 5 … (+1) + CDI 15 |

| Carteira | Invest. | Nomes | Vol | Beta | Beta baixa | E[exc.] TIR | Sharpe TIR | Sharpe upside | VaR95 1m normal | VaR95 1m crise | CVaR95 1m hist. | CVaR95 1m crise | N efetivo | Máx. contrib. risco |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | 60% | 8 | 19,7% | 0,89 | 0,97 | 7,5% | 0,38 | 0,39 | 7,6% | 24,1% | 12,2% | 29,4% | 5,7 | 32% |
| op7_b3_iv | 60% | 8 | 19,6% | 0,88 | 0,97 | 7,5% | 0,38 | 0,39 | 7,6% | 24,2% | 12,1% | 29,6% | 5,7 | 32% |
| op7_b3_rp | 60% | 8 | 19,7% | 0,88 | 0,97 | 7,5% | 0,38 | 0,39 | 7,6% | 24,0% | 12,2% | 29,4% | 5,7 | 32% |
| op7_b3_mv | 60% | 7 | 19,3% | 0,85 | 0,95 | 7,8% | 0,40 | 0,42 | 7,4% | 23,8% | 11,8% | 29,2% | 5,1 | 32% |
| op7_b3_ms_tir | 60% | 6 | 19,8% | 0,84 | 0,93 | 8,2% | 0,41 | 0,42 | 7,6% | 24,3% | 12,2% | 30,7% | 4,1 | 31% |
| op7_b3_ms_up | 60% | 5 | 20,1% | 0,81 | 0,92 | 7,8% | 0,39 | 0,45 | 7,8% | 22,5% | 11,9% | 27,5% | 3,8 | 39% |
| op7_sub_ew | 100% | 8 | 34,7% | 1,61 | 1,78 | 12,1% | 0,35 | 0,27 | 14,3% | 41,9% | 22,4% | 49,4% | 8,0 | 15% |
| op7_sub_iv | 100% | 8 | 34,3% | 1,60 | 1,76 | 12,2% | 0,36 | 0,28 | 14,1% | 41,7% | 22,1% | 49,2% | 7,9 | 14% |
| op7_sub_rp | 100% | 8 | 33,8% | 1,57 | 1,73 | 12,3% | 0,36 | 0,30 | 13,9% | 40,8% | 21,6% | 48,4% | 7,8 | 13% |
| op7_sub_mv | 100% | 8 | 33,0% | 1,51 | 1,68 | 12,8% | 0,39 | 0,35 | 13,5% | 40,0% | 21,1% | 48,6% | 6,4 | 21% |
| op7_sub_ms_tir | 100% | 7 | 33,4% | 1,51 | 1,67 | 13,1% | 0,39 | 0,35 | 13,6% | 40,6% | 21,5% | 48,8% | 5,7 | 21% |
| op7_sub_ms_up | 100% | 7 | 34,1% | 1,47 | 1,72 | 12,8% | 0,37 | 0,36 | 14,0% | 38,0% | 21,0% | 44,9% | 5,5 | 22% |
| u59_ew | 100% | 122 | 20,9% | 1,21 | 1,21 | 0,8% | 0,04 | -0,93 | 8,7% | 32,0% | 15,3% | 39,7% | 122,0 | 2% |
| u59_iv | 100% | 122 | 18,9% | 1,11 | 1,12 | 0,1% | 0,01 | -1,11 | 7,8% | 30,3% | 14,2% | 37,7% | 112,7 | 1% |
| u59_rp | 100% | 122 | 17,5% | 1,03 | 1,05 | -0,0% | -0,00 | -1,20 | 7,2% | 29,9% | 13,7% | 37,6% | 101,8 | 1% |
| u59_mv | 100% | 23 | 11,8% | 0,60 | 0,64 | -1,7% | -0,14 | -2,03 | 4,6% | 22,4% | 10,0% | 29,3% | 13,8 | 11% |
| u59_ms_tir | 100% | 9 | 25,9% | 1,27 | 1,29 | 11,4% | 0,44 | 0,26 | 10,2% | 35,2% | 17,5% | 44,0% | 7,4 | 22% |
| u59_ms_up | 100% | 9 | 28,3% | 1,30 | 1,38 | 10,8% | 0,38 | 0,33 | 11,4% | 34,2% | 18,6% | 42,6% | 7,1 | 25% |
| rec_op7_core | 60% | 8 | 19,5% | 0,86 | 0,95 | 7,8% | 0,40 | 0,41 | 7,5% | 24,2% | 12,1% | 29,7% | 5,2 | 32% |
| alt_u59_halfkelly | 85% | 9 | 22,1% | 1,08 | 1,10 | 9,7% | 0,44 | 0,26 | 8,5% | 30,2% | 15,0% | 38,3% | 7,4 | 22% |

Exposição setorial (setor B3, % do capital):

| Carteira | Setores |
|---|---|
| op7_b3_ew | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_iv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_rp | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_mv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_ms_tir | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_sub_ew | Consumo Cíclico 88 · Consumo não Cíclico 12 |
| op7_sub_iv | Consumo Cíclico 86 · Consumo não Cíclico 14 |
| op7_sub_rp | Consumo Cíclico 82 · Consumo não Cíclico 18 |
| op7_sub_mv | Consumo Cíclico 80 · Consumo não Cíclico 20 |
| op7_sub_ms_tir | Consumo Cíclico 80 · Consumo não Cíclico 20 |
| op7_sub_ms_up | Consumo Cíclico 80 · Consumo não Cíclico 20 |
| u59_ew | Consumo Cíclico 26 · Financeiro 16 · Utilidade Pública 13 · Bens Industriais 10 · Materiais Básicos 8 · Petróleo. Gás e Biocombustíveis 7 · Consumo não Cíclico 7 · Saúde 7 · Tecnologia da Informação 3 · Comunicações 2 |
| u59_iv | Consumo Cíclico 20 · Financeiro 19 · Utilidade Pública 17 · Bens Industriais 9 · Materiais Básicos 9 · Petróleo. Gás e Biocombustíveis 7 · Consumo não Cíclico 6 · Saúde 6 · Tecnologia da Informação 3 · Comunicações 3 |
| u59_rp | Consumo Cíclico 17 · Financeiro 17 · Utilidade Pública 15 · Materiais Básicos 12 · Petróleo. Gás e Biocombustíveis 10 · Bens Industriais 9 · Consumo não Cíclico 7 · Saúde 6 · Comunicações 3 · Tecnologia da Informação 3 |
| u59_mv | Utilidade Pública 21 · Financeiro 18 · Materiais Básicos 18 · Consumo não Cíclico 16 · Petróleo. Gás e Biocombustíveis 14 · Bens Industriais 5 · Consumo Cíclico 5 · Comunicações 4 |
| u59_ms_tir | Consumo Cíclico 38 · Financeiro 29 · Consumo não Cíclico 20 · Saúde 10 · Bens Industriais 3 |
| u59_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 · Bens Industriais 14 · Saúde 9 · Comunicações 8 · Financeiro 8 |
| rec_op7_core | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| alt_u59_halfkelly | Consumo Cíclico 32 · Financeiro 25 · Consumo não Cíclico 17 · Saúde 8 · Bens Industriais 3 |

## Estresses (choque instantâneo, % do capital)

| Carteira | Ibov −20% (beta baixa) | Ibov −20% (reação de hoje) | DI +300 bp | Dólar +20% puro | Dólar +20% c/ co-mov. | Ibov +30% (beta alta) |
|---|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | -19,4% | -31,7% | -10,8% | -4,8% | -19,8% | 25,9% |
| op7_b3_iv | -19,3% | -31,6% | -10,7% | -4,9% | -19,8% | 25,8% |
| op7_b3_rp | -19,4% | -31,6% | -10,8% | -4,8% | -19,8% | 25,8% |
| op7_b3_mv | -19,0% | -30,8% | -10,5% | -5,6% | -19,5% | 24,5% |
| op7_b3_ms_tir | -18,6% | -32,1% | -10,0% | -5,9% | -19,6% | 25,3% |
| op7_b3_ms_up | -18,4% | -30,5% | -11,0% | -5,8% | -18,6% | 23,6% |
| op7_sub_ew | -35,5% | -55,3% | -16,6% | -10,8% | -36,4% | 46,5% |
| op7_sub_iv | -35,1% | -54,9% | -16,6% | -10,8% | -36,1% | 46,0% |
| op7_sub_rp | -34,6% | -54,5% | -16,9% | -10,4% | -35,5% | 45,3% |
| op7_sub_mv | -33,6% | -53,4% | -16,7% | -11,1% | -34,9% | 43,1% |
| op7_sub_ms_tir | -33,4% | -55,8% | -16,6% | -11,1% | -35,5% | 44,5% |
| op7_sub_ms_up | -34,4% | -51,1% | -17,0% | -10,6% | -33,3% | 41,7% |
| u59_ew | -24,2% | -35,7% | -22,8% | -6,4% | -27,3% | 35,7% |
| u59_iv | -22,4% | -31,3% | -22,3% | -5,3% | -24,7% | 32,6% |
| u59_rp | -20,9% | -27,4% | -22,1% | -3,7% | -22,2% | 29,9% |
| u59_mv | -12,7% | -7,6% | -20,0% | 2,1% | -9,9% | 16,8% |
| u59_ms_tir | -25,7% | -50,2% | -18,6% | -5,7% | -27,0% | 39,0% |
| u59_ms_up | -27,6% | -45,1% | -19,5% | -7,7% | -27,7% | 38,8% |
| rec_op7_core | -19,0% | -31,8% | -10,4% | -5,3% | -19,7% | 25,5% |
| alt_u59_halfkelly | -21,9% | -42,8% | -15,8% | -4,8% | -23,0% | 33,2% |
| Ibovespa (referência) | −20,0% | −20,0% | — | — | -18,3% | +30,0% |

A coluna "reação de hoje" usa a razão entre a queda de cada ação e a do Ibovespa em 26/10. Como o universo foi escolhido justamente por ter caído ≥ 20%, essa razão superestima o beta. Ainda assim, ela mostra que em choques políticos os nomes domésticos se movem perto do dobro do índice.

## Monte Carlo de 1 ano (bootstrap estacionário, 10 mil trajetórias)

Regimes: `normal_hist` = dias de 2016–2026 com a média histórica; `normal_tir` = mesmos dias com a média de cada ação trocada pela TIR de dono; `choque_tir` = 3 meses sorteados dos dias de crise e 9 meses normais; `crise_tir` = o ano todo em dias de crise (vol 21d do Ibovespa ≥ 28,1%: 267 dias, em 2016, 2017, 2018, 2020, 2021, 2022 e out/2026); `crise_hist` = dias de crise com a média que tiveram.

| Carteira | Regime | Média | p5 | p25 | p50 | p75 | p95 | P(perda) | P(< CDI) | DD mediano | P(DD > 25%) | Kelly cheio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rec_op7_core | normal_hist | 16,9% | -19,8% | 0,6% | 15,5% | 31,5% | 58,9% | 24% | 47% | -14,3% | 14% | 0,67 |
| rec_op7_core | normal_tir | 21,4% | -16,7% | 4,5% | 19,9% | 36,5% | 65,0% | 19% | 39% | -13,7% | 12% | 1,44 |
| rec_op7_core | choque_tir | 22,7% | -29,9% | -0,9% | 20,6% | 44,0% | 81,9% | 26% | 41% | -17,0% | 33% | 0,92 |
| rec_op7_core | crise_tir | 27,0% | -50,6% | -14,0% | 19,6% | 58,9% | 129,9% | 36% | 46% | -38,4% | 71% | 0,55 |
| rec_op7_core | crise_hist | 30,1% | -49,4% | -11,8% | 22,5% | 62,8% | 135,5% | 34% | 44% | -38,1% | 71% | 0,66 |
| alt_u59_halfkelly | normal_hist | 17,4% | -27,7% | -3,0% | 14,9% | 34,9% | 70,9% | 29% | 48% | -18,0% | 24% | 0,49 |
| alt_u59_halfkelly | normal_tir | 23,5% | -24,0% | 2,1% | 20,9% | 41,9% | 79,8% | 23% | 40% | -16,9% | 20% | 1,17 |
| alt_u59_halfkelly | choque_tir | 25,4% | -40,2% | -6,6% | 21,3% | 52,0% | 105,2% | 31% | 43% | -22,0% | 43% | 0,73 |
| alt_u59_halfkelly | crise_tir | 31,6% | -62,0% | -23,7% | 15,3% | 69,0% | 176,9% | 41% | 49% | -48,2% | 78% | 0,44 |
| alt_u59_halfkelly | crise_hist | 36,4% | -60,7% | -20,9% | 19,5% | 75,2% | 186,9% | 38% | 47% | -47,8% | 77% | 0,54 |
| op7_b3_ms_tir | normal_hist | 17,4% | -20,1% | 0,8% | 16,0% | 32,1% | 60,2% | 24% | 46% | -14,6% | 14% | 0,74 |
| op7_b3_ms_tir | normal_tir | 21,6% | -17,2% | 4,5% | 20,2% | 36,8% | 66,0% | 19% | 39% | -13,8% | 13% | 1,42 |
| op7_b3_ms_tir | choque_tir | 23,0% | -31,1% | -1,3% | 21,0% | 45,1% | 83,4% | 26% | 41% | -17,4% | 34% | 0,90 |
| op7_b3_ms_tir | crise_tir | 27,4% | -51,7% | -14,5% | 19,1% | 59,7% | 134,7% | 36% | 46% | -39,1% | 72% | 0,54 |
| op7_b3_ms_tir | crise_hist | 28,3% | -51,4% | -13,9% | 19,9% | 60,8% | 136,3% | 35% | 45% | -39,0% | 72% | 0,57 |
| op7_sub_ms_tir | normal_hist | 20,2% | -42,6% | -10,8% | 13,8% | 44,7% | 103,3% | 36% | 50% | -26,9% | 57% | 0,41 |
| op7_sub_ms_tir | normal_tir | 27,2% | -39,2% | -5,5% | 20,5% | 53,2% | 115,2% | 30% | 44% | -25,6% | 52% | 0,80 |
| op7_sub_ms_tir | choque_tir | 31,9% | -55,8% | -16,8% | 21,0% | 68,5% | 156,9% | 37% | 45% | -31,5% | 65% | 0,57 |
| op7_sub_ms_tir | crise_tir | 49,0% | -77,8% | -40,2% | 10,9% | 93,6% | 300,2% | 45% | 51% | -59,7% | 86% | 0,39 |
| op7_sub_ms_tir | crise_hist | 66,1% | -75,2% | -33,3% | 23,7% | 115,8% | 345,9% | 40% | 46% | -58,9% | 84% | 0,56 |
| u59_ms_tir | normal_hist | 18,1% | -33,8% | -6,2% | 14,4% | 38,2% | 82,6% | 32% | 49% | -21,5% | 37% | 0,42 |
| u59_ms_tir | normal_tir | 25,3% | -29,8% | -0,5% | 21,4% | 46,7% | 93,7% | 26% | 41% | -20,1% | 31% | 1,01 |
| u59_ms_tir | choque_tir | 28,1% | -47,6% | -10,8% | 21,6% | 58,6% | 125,7% | 33% | 44% | -26,0% | 52% | 0,65 |
| u59_ms_tir | crise_tir | 36,9% | -69,8% | -30,7% | 13,1% | 78,0% | 219,1% | 43% | 50% | -54,7% | 82% | 0,40 |
| u59_ms_tir | crise_hist | 42,7% | -68,5% | -27,8% | 17,9% | 85,5% | 232,7% | 41% | 48% | -54,2% | 81% | 0,49 |
| u59_rp | normal_hist | 20,4% | -22,3% | 2,1% | 18,6% | 36,7% | 68,9% | 22% | 42% | -15,0% | 16% | 1,04 |
| u59_rp | normal_tir | 13,4% | -26,8% | -3,8% | 11,7% | 28,8% | 59,1% | 31% | 53% | -16,4% | 19% | 0,00 |
| u59_rp | choque_tir | 15,2% | -42,7% | -13,0% | 12,6% | 39,2% | 81,9% | 37% | 51% | -22,6% | 44% | 0,11 |
| u59_rp | crise_tir | 21,7% | -65,5% | -30,1% | 6,0% | 55,9% | 158,4% | 46% | 55% | -47,7% | 80% | 0,20 |
| u59_rp | crise_hist | 41,9% | -59,8% | -18,4% | 23,6% | 81,7% | 201,2% | 36% | 45% | -46,2% | 78% | 0,64 |
| u59_mv | normal_hist | 17,8% | -13,0% | 4,9% | 16,7% | 29,8% | 51,3% | 17% | 43% | -11,2% | 9% | 1,23 |
| u59_mv | normal_tir | 11,7% | -17,5% | -0,5% | 10,7% | 23,1% | 43,5% | 26% | 57% | -12,3% | 10% | 0,00 |
| u59_mv | choque_tir | 12,9% | -32,0% | -7,9% | 11,7% | 30,7% | 60,7% | 34% | 53% | -16,5% | 32% | 0,00 |
| u59_mv | crise_tir | 18,4% | -53,7% | -21,6% | 7,9% | 45,3% | 118,4% | 44% | 55% | -37,9% | 72% | 0,16 |
| u59_mv | crise_hist | 27,3% | -50,1% | -15,7% | 16,0% | 56,3% | 134,8% | 37% | 48% | -36,7% | 71% | 0,49 |

## Backtest ilustrativo: comprar no crash

Regra: tickers de data/market com histórico na data, ADTV 3m ≥ R$ 10 mi (viés de sobrevivência: lista atual). Retornos: retornos de preço + DY 12m na data × prazo (aprox.). Cestas com pesos iguais, compradas no fechamento do dia do choque. "Mais caídas" = terço com maior queda desde a data de referência; "mais baratas" = terço com maior L/P (P/L do fim do mês anterior levado ao preço do choque); "caídas e baratas" = quintil superior da soma dos dois rankings.

### 2017-05-18 — Joesley Day (delação JBS/Temer)

Universo de 53 ações. O Ibovespa caiu -8,8% entre 2017-05-17 e o fechamento do choque (-8,8% no dia) e depois subiu 11,4% em 3m, 19,2% em 6m e 28,1% em 12m.

| Cesta | N | Queda média | P/L mediano | 3m | 6m | 12m | Mediana 12m | Excesso 12m | % > Ibov 12m | DD máx. 12m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| todas | 53 | -9,5% | 14,6 | 15,8% | 21,9% | 29,2% | 16,9% | 1,1% | 40% | -11,3% |
| mais_caidas | 18 | -15,2% | 14,0 | 25,9% | 31,2% | 45,9% | 21,4% | 17,8% | 44% | -16,9% |
| menos_caidas | 18 | -3,4% | 17,2 | 11,4% | 18,3% | 19,3% | 14,3% | -8,8% | 33% | -8,1% |
| mais_baratas | 12 | -7,9% | 10,2 | 14,1% | 19,0% | 35,9% | 37,0% | 7,8% | 67% | -10,8% |
| caidas_e_baratas | 7 | -13,6% | 11,0 | 15,3% | 19,5% | 20,5% | 15,4% | -7,6% | 43% | -21,1% |

Correlação de ranking (Spearman) entre a queda e o retorno seguinte: 3m -0,32, 6m -0,11, 12m -0,18 (negativo = as mais caídas sobem mais). Entre o L/P e o retorno: 3m -0,00, 12m 0,24.

### 2020-03-16 — Covid-19 (circuit breakers de março)

Universo de 89 ações. O Ibovespa caiu -37,4% entre 2020-02-21 e o fechamento do choque (-13,9% no dia) e depois subiu 34,3% em 3m, 40,9% em 6m e 59,1% em 12m.

| Cesta | N | Queda média | P/L mediano | 3m | 6m | 12m | Mediana 12m | Excesso 12m | % > Ibov 12m | DD máx. 12m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| todas | 89 | -38,5% | 11,5 | 31,1% | 43,2% | 58,8% | 37,2% | -0,4% | 33% | -15,8% |
| mais_caidas | 30 | -50,6% | 10,3 | 44,5% | 65,4% | 91,8% | 64,0% | 32,6% | 53% | -17,5% |
| menos_caidas | 30 | -27,0% | 11,8 | 20,9% | 24,3% | 38,9% | 18,8% | -20,2% | 20% | -13,1% |
| mais_baratas | 22 | -37,4% | 7,8 | 28,7% | 32,4% | 63,1% | 44,3% | 4,0% | 36% | -18,0% |
| caidas_e_baratas | 13 | -50,3% | 6,8 | 40,5% | 44,9% | 93,2% | 50,7% | 34,0% | 46% | -19,3% |

Correlação de ranking (Spearman) entre a queda e o retorno seguinte: 3m -0,45, 6m -0,41, 12m -0,22 (negativo = as mais caídas sobem mais). Entre o L/P e o retorno: 3m -0,06, 12m 0,05.

### Ibovespa após quedas diárias ≤ −5% (episódios com ≥ 60 dias de intervalo, desde 1998)

| Data | Queda no dia | 3m | 6m | 12m |
|---|---:|---:|---:|---:|
| 1998-01-09 | -5,6% | 34,6% | 19,6% | -19,1% |
| 1998-04-27 | -5,7% | -6,7% | -37,9% | 7,5% |
| 2000-01-04 | -6,4% | 5,4% | 9,4% | 7,1% |
| 2000-04-13 | -5,0% | 8,9% | -0,7% | -11,6% |
| 2001-03-22 | -5,3% | 4,4% | -25,9% | -5,8% |
| 2001-09-11 | -9,2% | 25,3% | 30,1% | -12,2% |
| 2002-06-20 | -5,1% | -12,9% | -0,7% | 19,4% |
| 2002-09-27 | -5,3% | 29,3% | 36,2% | 93,8% |
| 2004-01-29 | -6,1% | -12,0% | 0,3% | 11,1% |
| 2004-05-10 | -5,5% | 20,8% | 31,9% | 38,5% |
| 2007-02-27 | -6,6% | 19,9% | 19,7% | 43,4% |
| 2008-01-21 | -6,6% | 20,2% | 6,5% | -28,3% |
| 2008-09-15 | -7,6% | -18,7% | -16,4% | 25,8% |
| 2011-08-04 | -5,7% | 11,1% | 23,5% | 11,6% |
| 2017-05-18 | -8,8% | 11,4% | 19,2% | 28,1% |
| 2020-02-26 | -7,0% | -17,8% | -4,8% | 6,6% |
| **mediana** | | **10,0%** (69% > 0) | **8,0%** (62% > 0) | **9,3%** (69% > 0) |

## Sensibilidades por ação

★ = oportunidade. Duration = queda do DDM com +3 p.p. na taxa ÷ 3 p.p. Lucro DI = efeito do canal de lucro sobre o preço.

| Ação | Setor | Vol | Beta | Beta baixa | Beta alta | Hoje | TIR − CDI | Upside a.a. 3a | Ibov −20% | DI +300 | Lucro DI | Duration (anos) | Beta câmbio puro | Dólar +20% puro |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RENT3 | Consumo Cíclico | 40,8% | 1,73 | 1,58 | 1,93 | -43,3% | 1,7% | -18,9% | -31,5% | -23,5% | -1,2% | 7,5 | -0,84 | -16,7% |
| MOVI3 | Consumo Cíclico | 64,7% | 2,53 | 2,35 | 2,84 | -64,5% | 9,4% | -14,1% | -46,9% | -33,6% | -18,9% | 6,1 | -1,65 | -33,0% |
| VAMO3 | Consumo Cíclico | 59,1% | 2,31 | 1,71 | 2,73 | -59,9% | 2,7% | -28,1% | -34,2% | -33,7% | -11,6% | 8,3 | 0,29 | 5,8% |
| SIMH3 | Financeiro | 60,5% | 2,49 | 2,07 | 2,60 | -68,5% | — | -24,4% | -41,4% | -42,1% | -26,6% | 7,0 | -0,65 | -13,0% |
| ECOR3 | Bens Industriais | 48,2% | 2,12 | 2,34 | 2,23 | -59,9% | 3,9% | -25,9% | -46,8% | -22,7% | -0,3% | 7,5 | -0,86 | -17,2% |
| MOTV3 | Bens Industriais | 26,6% | 1,22 | 1,44 | 1,17 | -27,7% | -0,9% | -28,5% | -28,8% | -25,5% | -3,3% | 7,6 | -0,39 | -7,8% |
| RAIL3 | Bens Industriais | 31,2% | 1,16 | 0,99 | 1,22 | -22,7% | -3,8% | -30,2% | -19,8% | -24,9% | -2,8% | 7,6 | -0,25 | -5,0% |
| CSAN3 | Petróleo. Gás e Biocombustíveis | 44,6% | 1,97 | 1,75 | 2,18 | -54,4% | — | -3,9% | -34,9% | -24,2% | -3,9% | 7,0 | -0,54 | -10,9% |
| VBBR3 | Petróleo. Gás e Biocombustíveis | 29,0% | 1,02 | 1,14 | 0,74 | -14,1% | -3,3% | -39,5% | -22,9% | -23,9% | -2,1% | 7,4 | 0,00 | 0,0% |
| MGLU3 | Consumo Cíclico | 69,7% | 2,63 | 1,93 | 3,03 | -59,5% | -7,1% | -36,6% | -38,5% | -35,8% | -10,1% | 9,6 | -0,29 | -5,9% |
| SBFG3 | Consumo Cíclico | 51,3% | 2,00 | 1,85 | 2,20 | -55,3% | 9,6% | -11,5% | -37,1% | -19,4% | -4,4% | 5,2 | -0,65 | -13,0% |
| CEAB3 ★ | Consumo Cíclico | 58,3% | 2,02 | 1,82 | 2,15 | -50,4% | 8,4% | 0,2% | -36,4% | -18,3% | -2,0% | 5,6 | -0,35 | -6,9% |
| LREN3 | Consumo Cíclico | 42,9% | 1,75 | 1,68 | 1,62 | -36,1% | 6,8% | -1,9% | -33,6% | -14,3% | 0,5% | 4,9 | -0,78 | -15,6% |
| AZZA3 | Consumo Cíclico | 48,4% | 1,57 | 1,59 | 1,52 | -40,9% | -0,3% | -22,9% | -31,8% | -29,5% | -4,2% | 8,8 | -0,95 | -19,1% |
| VIVA3 | Consumo Cíclico | 38,1% | 1,33 | 1,22 | 1,23 | -34,8% | 2,7% | -8,9% | -24,3% | -22,6% | -0,3% | 7,4 | -0,27 | -5,4% |
| VULC3 | Consumo Cíclico | 32,5% | 1,01 | 1,11 | 0,96 | -26,3% | 4,6% | -6,2% | -22,2% | -18,9% | -0,8% | 6,1 | -0,49 | -9,9% |
| ALPA4 | Consumo Cíclico | 40,3% | 1,22 | 1,36 | 0,75 | -21,2% | -2,5% | -21,2% | -27,2% | -23,5% | -0,3% | 7,8 | -0,46 | -9,1% |
| NATU3 | Consumo não Cíclico | 46,9% | 1,14 | 1,30 | 1,08 | -36,5% | -0,2% | -17,6% | -26,0% | -28,7% | -2,8% | 8,9 | -0,42 | -8,4% |
| ASAI3 | Consumo não Cíclico | 46,4% | 1,81 | 1,79 | 2,12 | -43,4% | 0,5% | -34,0% | -35,8% | -30,2% | -5,7% | 8,7 | -0,44 | -8,8% |
| GMAT3 | Consumo não Cíclico | 36,9% | 1,28 | 1,10 | 1,30 | -33,2% | -0,2% | -29,7% | -22,1% | -25,8% | -0,8% | 8,4 | -0,26 | -5,2% |
| PGMN3 | Saúde | 47,8% | 1,80 | 1,93 | 1,88 | -51,6% | 7,3% | -4,8% | -38,6% | -22,6% | -5,0% | 6,2 | -0,25 | -4,9% |
| RADL3 | Saúde | 36,5% | 1,13 | 1,08 | 1,06 | -22,7% | -1,8% | -25,8% | -21,6% | -25,6% | -0,5% | 8,4 | -0,36 | -7,2% |
| HYPE3 | Saúde | 32,9% | 1,02 | 0,97 | 0,89 | -20,7% | -0,3% | -20,7% | -19,5% | -23,8% | -1,9% | 7,4 | -0,46 | -9,1% |
| CYRE3 | Consumo Cíclico | 38,4% | 1,68 | 1,84 | 1,72 | -50,1% | 9,2% | 0,0% | -36,7% | -15,0% | -1,5% | 4,6 | -0,60 | -12,0% |
| EZTC3 | Consumo Cíclico | 41,7% | 1,56 | 1,69 | 1,69 | -50,7% | 3,8% | 3,7% | -33,9% | -16,7% | 1,4% | 5,9 | -0,46 | -9,3% |
| MDNE3 ★ | Consumo Cíclico | 45,7% | 1,69 | 1,92 | 1,60 | -44,3% | 14,1% | 6,2% | -38,3% | -10,9% | 0,6% | 3,8 | -0,74 | -14,9% |
| JHSF3 | Consumo Cíclico | 37,1% | 1,37 | 1,28 | 1,02 | -31,6% | -4,0% | -34,9% | -25,5% | -25,1% | -3,1% | 7,6 | -0,47 | -9,4% |
| MRVE3 | Consumo Cíclico | 50,8% | 1,83 | 1,85 | 1,90 | -48,1% | -0,8% | -18,2% | -37,1% | -35,1% | -12,1% | 8,7 | -0,73 | -14,5% |
| PLPL3 ★ | Consumo Cíclico | 50,6% | 1,60 | 1,72 | 1,82 | -42,8% | 14,7% | 9,6% | -34,5% | -13,8% | -1,1% | 4,3 | -0,74 | -14,8% |
| DIRR3 | Consumo Cíclico | 36,9% | 1,36 | 1,63 | 1,10 | -25,6% | 8,5% | -0,0% | -32,6% | -15,5% | -0,4% | 5,1 | -0,87 | -17,4% |
| CURY3 | Consumo Cíclico | 36,2% | 1,25 | 1,39 | 1,05 | -18,9% | 6,2% | -4,6% | -27,9% | -15,8% | 0,1% | 5,3 | -0,58 | -11,5% |
| TEND3 ★ | Consumo Cíclico | 50,3% | 1,60 | 1,90 | 1,24 | -25,2% | 11,8% | 8,1% | -38,0% | -14,7% | -1,1% | 4,6 | -0,78 | -15,5% |
| MULT3 | Financeiro | 26,0% | 1,20 | 1,30 | 1,17 | -31,1% | 0,6% | -16,9% | -26,0% | -24,9% | -1,9% | 7,8 | -0,51 | -10,1% |
| IGTI11 | Financeiro | 27,7% | 1,28 | 1,40 | 1,24 | -29,5% | -0,0% | -15,7% | -28,0% | -25,2% | -1,5% | 8,0 | -0,47 | -9,4% |
| ALOS3 | Financeiro | 24,5% | 1,17 | 1,30 | 1,11 | -30,4% | -0,9% | -18,8% | -25,9% | -21,2% | -1,6% | 6,6 | -0,50 | -10,1% |
| SMFT3 | Consumo Cíclico | 36,2% | 1,46 | 1,17 | 1,63 | -35,8% | 0,1% | -24,5% | -23,3% | -27,7% | -1,1% | 9,0 | -1,20 | -24,1% |
| CVCB3 | Consumo Cíclico | 65,9% | 1,81 | 1,85 | 1,85 | -43,9% | — | -47,5% | -36,9% | -37,7% | -21,1% | 7,0 | -1,57 | -31,5% |
| YDUQ3 | Consumo Cíclico | 50,6% | 1,73 | 1,60 | 1,55 | -37,6% | 5,9% | -6,8% | -32,0% | -24,2% | -6,8% | 6,2 | -1,10 | -22,1% |
| COGN3 ★ | Consumo Cíclico | 51,4% | 1,85 | 1,84 | 1,81 | -45,5% | 10,9% | 5,3% | -36,7% | -18,1% | -3,8% | 4,9 | -0,61 | -12,2% |
| ANIM3 | Consumo Cíclico | 68,6% | 2,48 | 2,67 | 2,46 | -51,8% | 9,2% | 1,4% | -53,3% | -33,6% | -17,0% | 6,6 | -1,14 | -22,8% |
| HAPV3 | Saúde | 61,1% | 1,84 | 1,29 | 1,96 | -52,3% | 15,6% | 4,6% | -25,8% | -24,8% | -10,6% | 5,3 | -0,21 | -4,2% |
| RDOR3 | Saúde | 31,7% | 1,26 | 1,08 | 1,27 | -22,7% | -1,4% | -26,1% | -21,7% | -25,8% | -1,5% | 8,2 | -0,27 | -5,3% |
| B3SA3 | Financeiro | 35,4% | 1,71 | 1,50 | 2,10 | -38,0% | -2,0% | -19,5% | -30,1% | -19,6% | 0,2% | 6,6 | -0,51 | -10,1% |
| BPAC11 | Financeiro | 32,9% | 1,57 | 1,63 | 1,72 | -29,4% | -0,5% | -19,3% | -32,6% | -26,2% | 0,0% | 8,7 | -0,74 | -14,8% |
| BBAS3 | Financeiro | 26,3% | 1,06 | 1,15 | 1,12 | -31,9% | 7,0% | -2,4% | -23,0% | -18,5% | 0,0% | 6,2 | 0,01 | 0,2% |
| BBDC4 | Financeiro | 28,9% | 1,27 | 1,19 | 1,49 | -27,8% | 4,9% | -5,6% | -23,7% | -18,2% | 0,0% | 6,1 | -0,24 | -4,8% |
| BRSR6 | Financeiro | 28,5% | 0,95 | 1,08 | 0,92 | -28,7% | 5,9% | -5,5% | -21,6% | -17,9% | 0,0% | 6,0 | -0,15 | -3,1% |
| AURE3 | Utilidade Pública | 29,7% | 1,08 | 1,14 | 1,17 | -27,4% | -7,0% | -48,0% | -22,7% | -28,2% | -2,0% | 8,9 | -0,15 | -3,0% |
| ENGI11 | Utilidade Pública | 27,2% | 1,32 | 1,19 | 1,45 | -31,9% | -5,4% | -39,8% | -23,7% | -28,7% | -7,4% | 7,7 | -0,64 | -12,8% |
| EQTL3 | Utilidade Pública | 25,0% | 1,18 | 1,10 | 1,28 | -30,3% | -6,4% | -46,7% | -21,9% | -27,0% | -3,0% | 8,2 | -0,63 | -12,5% |
| CPLE3 | Utilidade Pública | 23,3% | 0,98 | 1,08 | 0,85 | -15,4% | -5,2% | -42,5% | -21,6% | -20,6% | -1,2% | 6,5 | 0,01 | 0,3% |
| ALUP11 | Utilidade Pública | 20,6% | 0,78 | 0,81 | 0,84 | -17,4% | -3,0% | -33,9% | -16,2% | -21,7% | 0,3% | 7,3 | -0,34 | -6,8% |
| SBSP3 | Utilidade Pública | 26,2% | 1,07 | 1,14 | 1,13 | -22,1% | -5,3% | -40,1% | -22,8% | -26,3% | -1,5% | 8,4 | -0,24 | -4,8% |
| TOTS3 | Tecnologia da Informação | 33,9% | 0,98 | 0,98 | 0,75 | -23,1% | -2,0% | -21,4% | -19,7% | -24,6% | -0,6% | 8,0 | -0,39 | -7,8% |
| INTB3 | Tecnologia da Informação | 38,1% | 1,17 | 1,07 | 1,25 | -27,2% | -0,6% | -16,9% | -21,3% | -20,8% | 0,8% | 7,1 | -0,84 | -16,8% |
| GGPS3 | Bens Industriais | 32,3% | 1,26 | 1,19 | 1,54 | -34,0% | 1,8% | -11,8% | -23,8% | -25,9% | -1,1% | 8,3 | -0,72 | -14,4% |
| ORVR3 | Utilidade Pública | 28,7% | 1,08 | 1,28 | 1,17 | -24,5% | -4,1% | -29,9% | -25,6% | -27,7% | -0,7% | 9,1 | -0,72 | -14,3% |
| BEEF3 ★ | Consumo não Cíclico | 44,4% | 1,04 | 1,10 | 1,08 | -32,8% | 13,5% | 23,7% | -22,1% | -22,3% | -8,8% | 4,9 | 0,07 | 1,3% |
| TTEN3 | Consumo não Cíclico | 38,3% | 0,94 | 0,95 | 0,85 | -24,8% | -1,0% | -31,2% | -19,0% | -28,1% | -2,9% | 8,7 | -0,73 | -14,6% |
| PETR4 | Petróleo. Gás e Biocombustíveis | 26,8% | 0,62 | 0,66 | 0,60 | -10,1% | 1,4% | -17,5% | -13,3% | -20,2% | 0,2% | 6,8 | 0,59 | 11,8% |
| PETR3 | Petróleo. Gás e Biocombustíveis | 29,1% | 0,65 | 0,65 | 0,59 | -9,4% | 0,2% | -20,6% | -12,9% | -20,2% | 0,2% | 6,8 | 0,63 | 12,5% |
| PRIO3 | Petróleo. Gás e Biocombustíveis | 33,3% | 0,54 | 0,53 | 0,36 | -2,0% | 0,2% | -11,0% | -10,6% | -14,3% | 0,0% | 4,8 | 0,34 | 6,7% |
| BRAV3 | Petróleo. Gás e Biocombustíveis | 44,4% | 0,80 | 0,87 | 0,49 | -14,9% | -2,2% | -29,1% | -17,5% | -22,4% | -3,0% | 6,7 | 1,21 | 24,1% |
| RECV3 | Petróleo. Gás e Biocombustíveis | 36,5% | 0,92 | 0,86 | 0,70 | -13,0% | 0,0% | -22,9% | -17,2% | -16,3% | 2,2% | 6,0 | 0,07 | 1,5% |
| UGPA3 | Petróleo. Gás e Biocombustíveis | 31,7% | 1,10 | 1,35 | 0,81 | -15,2% | -3,1% | -26,9% | -27,0% | -21,4% | -1,0% | 6,9 | 0,16 | 3,2% |
| ENEV3 | Utilidade Pública | 30,0% | 1,08 | 1,06 | 0,92 | -15,9% | -6,5% | -52,8% | -21,2% | -26,2% | -0,3% | 8,7 | -0,39 | -7,8% |
| UNIP6 | Materiais Básicos | 30,8% | 0,77 | 0,73 | 0,73 | -14,2% | -2,9% | -32,2% | -14,6% | -21,4% | -1,2% | 6,8 | -0,19 | -3,7% |
| VALE3 | Materiais Básicos | 25,1% | 0,76 | 0,79 | 0,75 | -1,3% | -7,9% | -50,4% | -15,7% | -12,4% | -0,1% | 4,1 | 0,39 | 7,8% |
| BRAP4 | Materiais Básicos | 25,4% | 0,86 | 0,84 | 0,98 | -5,2% | — | -39,8% | -16,8% | -20,8% | 0,4% | 7,0 | 0,32 | 6,3% |
| CBAV3 | Materiais Básicos | 48,7% | 0,92 | 0,86 | 0,67 | 0,5% | -7,7% | -7,5% | -17,3% | -19,8% | 1,8% | 7,1 | 0,67 | 13,5% |
| GGBR4 | Materiais Básicos | 29,0% | 0,85 | 0,87 | 0,72 | -4,9% | -3,3% | -25,2% | -17,5% | -20,1% | -0,4% | 6,6 | 0,23 | 4,7% |
| GOAU4 | Materiais Básicos | 29,0% | 0,92 | 0,90 | 0,86 | -6,8% | — | -20,6% | -17,9% | -21,4% | -0,4% | 7,0 | 0,26 | 5,3% |
| USIM5 | Materiais Básicos | 43,8% | 1,08 | 1,08 | 0,76 | -14,3% | -1,8% | -15,0% | -21,6% | -21,0% | 0,1% | 7,0 | -0,05 | -1,0% |
| SUZB3 | Materiais Básicos | 26,1% | 0,28 | 0,28 | 0,35 | 11,9% | -0,7% | -32,5% | -5,6% | -23,0% | -0,2% | 7,6 | 0,43 | 8,5% |
| KLBN11 | Materiais Básicos | 21,4% | 0,56 | 0,54 | 0,55 | -3,2% | -2,1% | -43,4% | -10,7% | -20,7% | 0,5% | 7,0 | 0,21 | 4,1% |
| SLCE3 | Consumo não Cíclico | 25,0% | 0,44 | 0,26 | 0,32 | -3,5% | -4,2% | -11,9% | -5,3% | -25,0% | -4,4% | 7,2 | -0,21 | -4,3% |
| WEGE3 | Bens Industriais | 29,3% | 0,65 | 0,47 | 0,57 | 10,9% | -5,5% | -38,2% | -9,4% | -24,5% | 0,0% | 8,2 | 0,37 | 7,3% |
| EMBJ3 | Bens Industriais | 39,8% | 0,56 | 1,33 | 0,18 | 9,5% | -4,5% | -31,8% | -26,5% | -25,9% | 0,0% | 8,6 | 0,85 | 17,0% |
| POMO4 | Bens Industriais | 40,0% | 1,05 | 1,21 | 1,14 | -18,4% | 8,0% | 0,6% | -24,1% | -16,1% | -0,7% | 5,2 | -0,59 | -11,9% |
| RAPT4 | Bens Industriais | 39,2% | 1,37 | 1,21 | 1,38 | -54,5% | 2,0% | -19,4% | -24,2% | -36,7% | -15,1% | 8,5 | -0,81 | -16,2% |
| TUPY3 | Bens Industriais | 34,7% | 0,96 | 0,90 | 1,11 | -24,5% | 2,3% | -26,8% | -18,0% | -24,3% | -1,6% | 7,7 | -0,22 | -4,4% |
| LEVE3 | Consumo Cíclico | 27,5% | 0,61 | 0,70 | 0,57 | -17,4% | 4,4% | -10,3% | -13,9% | -17,4% | 0,4% | 5,9 | 0,12 | 2,3% |
| DXCO3 | Materiais Básicos | 37,1% | 1,38 | 1,07 | 1,41 | -43,6% | -3,3% | -36,8% | -21,5% | -28,9% | -5,7% | 8,2 | -1,13 | -22,6% |
| ITUB4 | Financeiro | 23,3% | 1,10 | 1,15 | 1,17 | -17,4% | 0,5% | -14,3% | -23,0% | -20,6% | 0,0% | 6,9 | -0,17 | -3,3% |
| ITSA4 | Financeiro | 23,6% | 1,17 | 1,16 | 1,25 | -15,7% | — | -8,8% | -23,1% | -21,2% | -0,1% | 7,0 | -0,19 | -3,8% |
| SANB11 | Financeiro | 26,6% | 1,00 | 1,20 | 0,82 | -11,6% | 1,7% | -12,0% | -23,9% | -22,7% | 0,0% | 7,6 | -0,06 | -1,1% |
| BBDC3 | Financeiro | 26,8% | 1,22 | 1,16 | 1,46 | -25,8% | 6,2% | -2,6% | -23,2% | -16,8% | 0,0% | 5,6 | -0,25 | -5,1% |
| ABCB4 | Financeiro | 25,5% | 0,90 | 0,95 | 0,98 | -21,8% | 3,7% | -11,2% | -18,9% | -19,2% | 2,6% | 7,1 | -0,01 | -0,1% |
| PINE4 | Financeiro | 42,0% | 1,02 | 0,77 | 0,98 | -35,2% | 9,1% | -3,9% | -15,3% | -22,0% | -7,5% | 5,2 | -0,19 | -3,7% |
| BBSE3 | Financeiro | 20,4% | 0,50 | 0,56 | 0,43 | -5,2% | 2,1% | -12,0% | -11,1% | -19,2% | 0,8% | 6,6 | 0,00 | 0,0% |
| CXSE3 | Financeiro | 23,4% | 0,58 | 0,78 | 0,47 | -1,2% | -1,0% | -16,2% | -15,6% | -19,8% | 0,9% | 6,8 | 0,18 | 3,5% |
| PSSA3 | Financeiro | 24,0% | 0,67 | 0,87 | 0,64 | -9,1% | 1,3% | -8,9% | -17,4% | -21,3% | 1,9% | 7,6 | -0,44 | -8,8% |
| IRBR3 | Financeiro | 44,3% | 1,06 | 1,38 | 0,75 | -16,4% | 1,1% | -14,7% | -27,7% | -18,2% | 3,4% | 7,0 | 0,27 | 5,4% |
| SAUD3 | Saúde | 33,5% | 1,14 | 0,68 | 1,18 | -11,5% | 0,7% | -12,0% | -13,6% | -22,8% | 1,2% | 7,9 | 0,07 | 1,3% |
| AXIA3 | Utilidade Pública | 27,6% | 1,29 | 1,42 | 1,11 | -16,9% | -6,9% | -45,6% | -28,4% | -19,2% | -1,3% | 6,1 | 0,12 | 2,3% |
| CMIG4 | Utilidade Pública | 25,1% | 0,88 | 0,84 | 0,85 | -13,0% | -2,5% | -36,8% | -16,8% | -22,0% | -1,0% | 7,1 | 0,07 | 1,4% |
| EGIE3 | Utilidade Pública | 22,5% | 0,75 | 0,74 | 0,74 | -11,3% | -3,9% | -35,9% | -14,7% | -21,1% | -0,9% | 6,8 | -0,11 | -2,2% |
| CPFE3 | Utilidade Pública | 22,1% | 0,75 | 0,75 | 0,69 | -13,7% | -2,5% | -33,6% | -15,0% | -21,6% | -2,1% | 6,6 | -0,16 | -3,2% |
| ISAE4 | Utilidade Pública | 21,9% | 0,85 | 0,89 | 0,72 | -10,9% | -7,3% | -41,2% | -17,7% | -17,5% | -1,5% | 5,4 | 0,03 | 0,6% |
| TAEE11 | Utilidade Pública | 18,2% | 0,71 | 0,72 | 0,69 | -10,5% | -6,0% | -34,0% | -14,5% | -16,8% | -1,9% | 5,1 | -0,00 | -0,0% |
| CSMG3 | Utilidade Pública | 30,7% | 0,76 | 0,90 | 0,92 | -22,6% | -4,1% | -38,0% | -18,0% | -23,9% | -0,4% | 7,9 | -0,12 | -2,5% |
| SAPR11 | Utilidade Pública | 28,7% | 0,81 | 0,81 | 0,90 | -22,7% | -0,6% | -31,8% | -16,2% | -23,7% | 1,3% | 8,2 | -0,15 | -3,0% |
| ABEV3 | Consumo não Cíclico | 23,4% | 0,66 | 0,65 | 0,56 | -9,0% | -1,8% | -16,9% | -12,9% | -19,6% | 0,0% | 6,5 | -0,01 | -0,2% |
| MDIA3 | Consumo não Cíclico | 33,7% | 0,80 | 0,78 | 1,01 | -17,7% | -0,3% | -10,9% | -15,6% | -20,2% | 0,5% | 6,9 | -0,32 | -6,4% |
| GRND3 | Consumo Cíclico | 30,5% | 0,80 | 0,86 | 0,70 | -21,8% | -0,1% | -8,9% | -17,3% | -16,8% | 1,0% | 5,9 | -0,21 | -4,1% |
| VIVT3 | Comunicações | 24,5% | 0,73 | 0,85 | 0,72 | -4,9% | -1,7% | -21,7% | -16,9% | -19,0% | -0,4% | 6,2 | -0,41 | -8,2% |
| TIMS3 | Comunicações | 27,1% | 0,72 | 0,79 | 0,57 | -0,5% | 0,7% | -15,9% | -15,9% | -18,8% | -0,4% | 6,2 | -0,26 | -5,2% |
| DESK3 | Comunicações | 46,6% | 0,92 | 1,01 | 0,62 | 0,4% | -3,1% | 0,2% | -20,1% | -28,8% | -3,5% | 8,7 | 0,06 | 1,2% |
| BMOB3 | Tecnologia da Informação | 32,3% | 1,13 | 1,27 | 1,00 | -27,9% | 0,4% | -15,1% | -25,3% | -21,9% | 0,6% | 7,5 | -0,14 | -2,8% |
| LWSA3 | Tecnologia da Informação | 48,2% | 1,55 | 1,49 | 1,48 | -36,1% | 1,0% | -6,1% | -29,7% | -22,0% | -0,3% | 7,2 | -0,82 | -16,3% |
| FLRY3 | Saúde | 27,8% | 0,95 | 1,08 | 0,87 | -22,2% | -2,3% | -24,4% | -21,7% | -21,3% | -0,9% | 6,9 | -0,24 | -4,8% |
| PNVL3 | Saúde | 30,8% | 1,21 | 1,40 | 1,30 | -32,5% | -1,0% | -25,4% | -28,1% | -26,1% | -1,0% | 8,5 | -0,68 | -13,6% |
| SEER3 ★ | Consumo Cíclico | 58,1% | 1,70 | 2,32 | 1,38 | -39,6% | 10,8% | 8,8% | -46,5% | -16,6% | -1,6% | 5,1 | -0,34 | -6,9% |
| VTRU3 ★ | Consumo Cíclico | 50,5% | 1,40 | 1,59 | 1,32 | -42,3% | 12,7% | 12,3% | -31,8% | -18,0% | -3,4% | 5,1 | -0,84 | -16,8% |
| RIAA3 | Consumo Cíclico | 44,8% | 1,72 | 1,32 | 1,73 | -45,2% | 3,9% | -9,6% | -26,4% | -22,8% | -2,4% | 7,0 | -1,68 | -33,6% |
| AUAU3 | Consumo Cíclico | 38,8% | 0,98 | 0,35 | 0,95 | -26,9% | 1,1% | -14,0% | -7,0% | -22,4% | 0,4% | 7,6 | -0,85 | -17,1% |
| TFCO4 | Consumo Cíclico | 32,3% | 1,25 | 1,29 | 1,34 | -31,2% | 0,7% | -12,8% | -25,8% | -25,8% | -0,4% | 8,5 | -0,63 | -12,6% |
| JSLG3 | Bens Industriais | 55,4% | 2,03 | 2,11 | 2,25 | -54,7% | 1,2% | -35,1% | -42,3% | -35,0% | -10,1% | 9,2 | 0,04 | 0,9% |
| MILS3 | Bens Industriais | 27,9% | 0,91 | 0,85 | 0,78 | -4,3% | -1,3% | -22,5% | -17,1% | -24,3% | -1,5% | 7,7 | -0,32 | -6,4% |
| OPCT3 | Petróleo. Gás e Biocombustíveis | 36,9% | 0,95 | 1,07 | 0,95 | -12,2% | -0,6% | -26,1% | -21,5% | -25,4% | -1,8% | 8,0 | -0,86 | -17,1% |
| PRNR3 | Bens Industriais | 33,9% | 1,04 | 1,14 | 0,99 | -37,7% | -2,3% | -29,5% | -22,8% | -30,1% | -5,3% | 8,7 | -0,17 | -3,4% |
| LOGG3 | Financeiro | 34,1% | 1,02 | 1,01 | 1,11 | -29,9% | -4,9% | -32,2% | -20,2% | -19,6% | -3,1% | 5,7 | -0,50 | -9,9% |

## Método e ressalvas

- Covariância: 2023-10-25 a 2026-10-23 (diário), 748 observações diárias, Ledoit-Wolf com alvo de correlação constante (intensidade 0,101, correlação média 0,320), anualizada × 252. Vol 3a do Ibovespa: 16,0%.
- Otimização: SLSQP, long-only, 20% por ação e 40% por setor. Pesos iguais e inverso da volatilidade são projetados no conjunto viável. A paridade de risco minimiza o desvio das contribuições de risco em relação a 1/N, com limites. Máximo Sharpe usa várias partidas; holdings sem TIR (SIMH3, CSAN3) ficam de fora da versão TIR.
- Retorno esperado = TIR de dono − CDI (alternativa: (1+upside)^(1/3) − 1).
- Betas de 3 anos diários; beta de baixa/alta = OLS só nos dias de queda/alta do Ibovespa.
- DI +300 bp = (1 + canal de lucro) × (1 + canal de duration) − 1. Lucro: valor presente de 3 anos de 3 × sensibilidade do lucro por 100 bp de CDI (research/{T}.json) ÷ valor de mercado; bancos sem dado = 0. Duration: DDM do motor (mesmos fluxos da TIR de dono) reprecificado a r + 3 p.p., r = max(TIR, DI longo 15,5%).
- Dólar +20%: 'puro' = beta cambial semanal (3a) com Ibovespa constante; 'comov' = beta univariado (inclui a queda típica da bolsa quando o dólar sobe).
- Monte Carlo: bootstrap estacionário (bloco médio 21 d) de retornos diários 2016–2026; 'crise' sorteia só dias com vol. 21d do Ibovespa no decil superior; 'tir' troca a média histórica de cada ação pela TIR de dono.
- Ausências de histórico (ex.: MOTV3 entre CCRO3 e MOTV3) preenchidas com beta × Ibovespa + resíduo sorteado.
- A TIR de dono é a taxa implícita no preço sob as projeções do estudo (horizonte longo), não uma previsão de 12 meses. O Sharpe ex-ante herda os erros dessas projeções; por isso a recomendação mistura máximo Sharpe com paridade de risco e não usa o máximo Sharpe puro.
- Backtest: só 2 eventos, preços sem reinvestimento de proventos (DY aproximado; valores fora de 0–15% descartados) e P/L histórico com erros de unidade em alguns tickers (P/L fora de 1–60 descartado). Há viés de sobrevivência, porque o universo é a lista atual. É ilustrativo, não estatisticamente conclusivo.
- Estresses são lineares e instantâneos, sem efeitos de segunda ordem (liquidez, chamadas de margem, rebaixamentos).
