# Carteiras pós-choque — 26/10/2026

Gerado por `pipeline/tests/portfolio.py` em 2026-11-18T14:20:06 (dados: `data/app/overview.json`, preços B3 ajustados 2016–2026, câmbio BCB). Ibovespa -14,6% no dia, dólar 9,2%, CDI 13,65%, DI longo ~15,5%. Limites: 20% por ação e 40% por setor B3. Estudo quantitativo com finalidade informativa; não é recomendação de investimento.

## Resumo

- **Carteira recomendada (alvo):** BEEF3 20 · MDNE3 10 · VTRU3 9 · PLPL3 9 · TEND3 4 · COGN3 3 · SEER3 3 · CEAB3 3 (% do capital) + **40% em CDI**. São as 8 oportunidades do estudo, com pesos de 50% máximo Sharpe (TIR − CDI) e 50% paridade de risco. 7 das 8 são Consumo Cíclico, então o limite de 40% por setor só permite investir 60%; o resto fica no CDI.
- **Tamanho (Kelly fracionado):** meio Kelly dá 27% do capital em ações no regime de choque (3 meses de volatilidade de crise) e 43%–60% no regime normal. Sugestão: entrar com ~27% e subir até 60% quando a volatilidade normalizar.
- **Risco ex-ante (carteira-alvo):** vol 19,5% a.a., beta 0,86 (beta de baixa 0,95), retorno esperado 21,3% a.a. (7,6% acima do CDI), Sharpe 0,39. VaR 95% de 1 mês: 7,5% (normal) e 24,0% no regime de crise; CVaR 12,0% no histórico 2016–2026 e 29,7% na crise. N efetivo 5,2; BEEF3 responde por 32% do risco.
- **Estresses (carteira-alvo):** Ibovespa −20% → -19,0% pelo beta de baixa, ou -31,8% repetindo a reação de hoje; DI +300 bp → -10,7%; dólar +20% → -5,3% no canal cambial puro e -19,7% com o co-movimento histórico da bolsa. Na reversão (Ibovespa +30%), 25,5%. No pregão de hoje a carteira teria rendido -23,2%; o beta de baixa previa -13,9%.
- **Monte Carlo 1 ano (deriva = TIR):** no regime normal, mediana 19,7%, p5 -16,7%, P(perda) 19% e P(abaixo do CDI) 40%. Com 3 meses de choque, mediana 20,4%, p5 -29,9%, P(perda) 26% e drawdown mediano -17,0%.
- **Alternativa totalmente diversificável:** o máximo Sharpe do universo de 122 (BEEF3 20 · BBAS3 20 · PLPL3 12 · MDNE3 11 · HAPV3 11 · PINE4 10 · VTRU3 10 · LEVE3 4 … (+1)) tem Sharpe 0,43, mas inclui nomes fora das oportunidades (BBAS3, HAPV3, BRSR6). Dimensionado a meio Kelly (82% em ações), fica com risco parecido (vol 21,5%, Ibovespa −20% → -21,1%).
- **Histórico de crashes:** em 2017-05-18, as mais caídas subiram 25,9% em 3m (mediana 18,7%; 89% acima do índice), contra 11,4% do Ibovespa. Em 12m, a mediana delas foi 21,4%, contra 28,1% do índice, e a das mais baratas por P/L 37,0%. Depois da compra, o drawdown chegou a -21,1%; em 2020-03-16, as mais caídas subiram 44,5% em 3m (mediana 39,1%; 57% acima do índice), contra 34,3% do Ibovespa. Em 12m, a mediana delas foi 64,0%, contra 59,1% do índice, e a das mais baratas por P/L 44,3%. Depois da compra, o drawdown chegou a -19,3%. A reversão das mais caídas é forte e ampla nos primeiros 3–6 meses (correlação de ranking entre a queda e o retorno de 3m: -0,32 e -0,45), mas em 12 meses a vantagem da ação mediana diminui ou some. O P/L baixo, isolado, bateu o índice em 2017 e perdeu em 2020. Nos 16 episódios de queda diária ≤ −5% do Ibovespa desde 1998, comprar no 1º dia rendeu mediana de 9,3% em 12m (69% positivos). Em 2020, comprar em 26/02 rendeu 6,6%, contra 59,1% comprando em 16/03. O risco de entrar cedo justifica a entrada escalonada.

## Carteira recomendada

**Recomendada · 8 oportunidades (50% máx. Sharpe TIR + 50% paridade de risco), setor B3 ≤ 40%, excedente em CDI**

| Ação | % capital | % das ações | Setor / subsetor | TIR | Upside | Contrib. risco | Beta baixa | DI +300 | Dólar +20% puro |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| BEEF3 | 20,0% | 33,3% | Consumo não Cíclico / Alimentos Processados | 26,9% | 75,6% | 32,4% | 1,10 | -22,7% | 1,3% |
| MDNE3 | 9,9% | 16,4% | Consumo Cíclico / Construção Civil | 27,1% | 17,5% | 16,8% | 1,92 | -11,7% | -14,9% |
| VTRU3 | 8,6% | 14,3% | Consumo Cíclico / Diversos | 26,3% | 39,3% | 13,7% | 1,59 | -18,1% | -16,8% |
| PLPL3 | 8,5% | 14,2% | Consumo Cíclico / Construção Civil | 27,8% | 29,2% | 15,5% | 1,72 | -14,3% | -14,8% |
| TEND3 | 4,4% | 7,3% | Consumo Cíclico / Construção Civil | 25,0% | 24,1% | 7,0% | 1,90 | -15,3% | -15,5% |
| COGN3 | 3,0% | 5,0% | Consumo Cíclico / Diversos | 24,2% | 11,8% | 4,8% | 1,84 | -18,6% | -12,2% |
| SEER3 | 2,9% | 4,9% | Consumo Cíclico / Diversos | 24,1% | 25,2% | 4,9% | 2,32 | -17,2% | -6,9% |
| CEAB3 | 2,7% | 4,5% | Consumo Cíclico / Comércio | 21,8% | -3,2% | 5,0% | 1,82 | -19,0% | -6,9% |
| CDI | 40,0% | — | caixa | 13,65% | — | 0% | 0 | 0% | 0% |

Dimensionamento por Kelly (fração da carteira-alvo; exposição resultante em ações):

| Regime | Kelly cheio | Meio Kelly | Ações / capital |
|---|---:|---:|---:|
| analitico | 2,00 | 1,00 | 60% |
| normal_bootstrap | 1,42 | 0,71 | 43% |
| choque_3m | 0,90 | 0,45 | 27% |
| crise_ano | 0,55 | 0,28 | 17% |

Regra: começar no meio Kelly do regime de choque e subir até o meio Kelly normal/analítico (teto = parcela investida da carteira-alvo) quando a vol. 21d do Ibovespa sair do decil superior.

## Carteiras testadas

`op7_b3` = 8 oportunidades com setor B3 ≤ 40% (máximo investível 60%, resto em CDI); `op7_sub` = 8 oportunidades com subsetor B3 ≤ 40% (incorporação ≤ 40%, 100% investido); `u59` = universo da cobertura com setor B3 ≤ 40%.

| Carteira | Pesos (% do capital) |
|---|---|
| op7_b3_ew | BEEF3 20 · COGN3 6 · MDNE3 6 · TEND3 6 · SEER3 6 · VTRU3 6 · CEAB3 6 · PLPL3 6 + CDI 40 |
| op7_b3_iv | BEEF3 20 · MDNE3 7 · TEND3 6 · VTRU3 6 · PLPL3 6 · COGN3 6 · SEER3 5 · CEAB3 5 + CDI 40 |
| op7_b3_rp | BEEF3 20 · TEND3 6 · SEER3 6 · PLPL3 6 · VTRU3 6 · COGN3 6 · MDNE3 6 · CEAB3 5 + CDI 40 |
| op7_b3_mv | BEEF3 20 · VTRU3 10 · MDNE3 9 · TEND3 8 · COGN3 5 · PLPL3 5 · SEER3 3 + CDI 40 |
| op7_b3_ms_tir | BEEF3 20 · MDNE3 14 · VTRU3 11 · PLPL3 11 · TEND3 3 · COGN3 0 + CDI 40 |
| op7_b3_ms_up | VTRU3 20 · BEEF3 20 · PLPL3 10 · TEND3 7 · SEER3 4 + CDI 40 |
| op7_sub_ew | CEAB3 12 · MDNE3 12 · PLPL3 12 · TEND3 12 · COGN3 12 · BEEF3 12 · SEER3 12 · VTRU3 12 |
| op7_sub_iv | BEEF3 14 · MDNE3 14 · TEND3 13 · VTRU3 13 · PLPL3 13 · COGN3 12 · SEER3 11 · CEAB3 11 |
| op7_sub_rp | BEEF3 18 · VTRU3 13 · MDNE3 13 · TEND3 12 · PLPL3 12 · COGN3 12 · SEER3 11 · CEAB3 10 |
| op7_sub_mv | BEEF3 20 · VTRU3 20 · MDNE3 18 · TEND3 13 · COGN3 12 · PLPL3 9 · SEER3 6 · CEAB3 2 |
| op7_sub_ms_tir | VTRU3 20 · MDNE3 20 · BEEF3 20 · PLPL3 18 · COGN3 13 · SEER3 7 · TEND3 2 |
| op7_sub_ms_up | PLPL3 20 · BEEF3 20 · SEER3 20 · VTRU3 20 · TEND3 18 · MDNE3 2 |
| u59_ew | RENT3 1 · MOVI3 1 · VAMO3 1 · SIMH3 1 · ECOR3 1 · MOTV3 1 · RAIL3 1 · CSAN3 1 … (+114) |
| u59_iv | TAEE11 1 · BBSE3 1 · ALUP11 1 · KLBN11 1 · ISAE4 1 · CPFE3 1 · EGIE3 1 · ITUB4 1 … (+114) |
| u59_rp | SUZB3 2 · PETR4 2 · PETR3 2 · BBSE3 2 · SLCE3 2 · PRIO3 2 · KLBN11 2 · VALE3 1 … (+114) |
| u59_mv | PETR4 11 · TAEE11 11 · BBSE3 11 · SUZB3 10 · SLCE3 8 · ABEV3 6 · VALE3 6 · ALUP11 5 … (+15) |
| u59_ms_tir | BEEF3 20 · BBAS3 20 · PLPL3 12 · MDNE3 11 · HAPV3 11 · PINE4 10 · VTRU3 10 · LEVE3 4 … (+1) |
| u59_ms_up | VTRU3 20 · BEEF3 20 · POMO4 14 · PLPL3 13 · DESK3 12 · BBAS3 10 · HAPV3 4 · TEND3 3 … (+1) |
| el_b3_ew | BEEF3 20 · TEND3 10 · MDNE3 10 · PLPL3 10 · VTRU3 10 + CDI 40 |
| el_b3_iv | BEEF3 20 · MDNE3 11 · TEND3 10 · VTRU3 10 · PLPL3 10 + CDI 40 |
| el_b3_rp | BEEF3 20 · VTRU3 10 · MDNE3 10 · TEND3 10 · PLPL3 10 + CDI 40 |
| el_b3_mv | BEEF3 20 · VTRU3 13 · MDNE3 12 · TEND3 9 · PLPL3 6 + CDI 40 |
| el_b3_ms_tir | BEEF3 20 · MDNE3 14 · VTRU3 12 · PLPL3 11 · TEND3 3 + CDI 40 |
| el_b3_ms_up | BEEF3 20 · VTRU3 20 · PLPL3 11 · TEND3 9 · MDNE3 0 + CDI 40 |
| rec_op7_core | BEEF3 20 · MDNE3 10 · VTRU3 9 · PLPL3 9 · TEND3 4 · COGN3 3 · SEER3 3 · CEAB3 3 + CDI 40 |
| rec_elig_core | BEEF3 20 · MDNE3 12 · VTRU3 11 · PLPL3 10 · TEND3 6 + CDI 40 |
| alt_u59_halfkelly | BEEF3 16 · BBAS3 16 · PLPL3 10 · MDNE3 9 · HAPV3 9 · PINE4 8 · VTRU3 8 · LEVE3 3 … (+1) + CDI 18 |

| Carteira | Invest. | Nomes | Vol | Beta | Beta baixa | E[exc.] TIR | Sharpe TIR | Sharpe upside | VaR95 1m normal | VaR95 1m crise | CVaR95 1m hist. | CVaR95 1m crise | N efetivo | Máx. contrib. risco |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | 60% | 8 | 19,7% | 0,89 | 0,97 | 7,3% | 0,37 | 0,34 | 7,6% | 24,1% | 12,2% | 29,5% | 5,7 | 32% |
| op7_b3_iv | 60% | 8 | 19,6% | 0,88 | 0,97 | 7,3% | 0,37 | 0,34 | 7,6% | 24,2% | 12,1% | 29,6% | 5,7 | 32% |
| op7_b3_rp | 60% | 8 | 19,7% | 0,88 | 0,97 | 7,3% | 0,37 | 0,34 | 7,6% | 24,0% | 12,2% | 29,4% | 5,7 | 32% |
| op7_b3_mv | 60% | 7 | 19,3% | 0,85 | 0,95 | 7,6% | 0,39 | 0,38 | 7,4% | 23,8% | 11,8% | 29,3% | 5,1 | 32% |
| op7_b3_ms_tir | 60% | 6 | 19,8% | 0,84 | 0,93 | 7,9% | 0,40 | 0,38 | 7,6% | 24,3% | 12,1% | 30,4% | 4,1 | 31% |
| op7_b3_ms_up | 60% | 5 | 20,1% | 0,81 | 0,92 | 7,7% | 0,38 | 0,40 | 7,8% | 22,5% | 11,9% | 27,6% | 3,8 | 39% |
| op7_sub_ew | 100% | 8 | 34,7% | 1,61 | 1,78 | 11,7% | 0,34 | 0,23 | 14,4% | 41,9% | 22,4% | 49,4% | 8,0 | 15% |
| op7_sub_iv | 100% | 8 | 34,3% | 1,60 | 1,76 | 11,9% | 0,35 | 0,25 | 14,1% | 41,8% | 22,1% | 49,2% | 7,9 | 14% |
| op7_sub_rp | 100% | 8 | 33,8% | 1,57 | 1,73 | 11,9% | 0,35 | 0,27 | 13,9% | 40,8% | 21,6% | 48,4% | 7,8 | 13% |
| op7_sub_mv | 100% | 8 | 33,0% | 1,51 | 1,68 | 12,4% | 0,38 | 0,31 | 13,5% | 40,0% | 21,1% | 48,6% | 6,4 | 21% |
| op7_sub_ms_tir | 100% | 7 | 33,4% | 1,51 | 1,67 | 12,7% | 0,38 | 0,31 | 13,7% | 40,6% | 21,5% | 49,1% | 5,7 | 21% |
| op7_sub_ms_up | 100% | 6 | 34,3% | 1,47 | 1,73 | 12,4% | 0,36 | 0,33 | 14,1% | 37,5% | 21,1% | 44,5% | 5,2 | 24% |
| u59_ew | 100% | 122 | 20,9% | 1,21 | 1,21 | 0,7% | 0,03 | -0,96 | 8,7% | 32,0% | 15,3% | 39,7% | 122,0 | 2% |
| u59_iv | 100% | 122 | 18,9% | 1,11 | 1,12 | -0,0% | -0,00 | -1,15 | 7,8% | 30,3% | 14,2% | 37,7% | 112,7 | 1% |
| u59_rp | 100% | 122 | 17,5% | 1,03 | 1,05 | -0,2% | -0,01 | -1,25 | 7,2% | 29,9% | 13,7% | 37,6% | 101,8 | 1% |
| u59_mv | 100% | 23 | 11,8% | 0,60 | 0,64 | -1,9% | -0,16 | -2,11 | 4,6% | 22,4% | 10,0% | 29,4% | 13,8 | 11% |
| u59_ms_tir | 100% | 9 | 26,3% | 1,28 | 1,29 | 11,3% | 0,43 | 0,22 | 10,4% | 35,3% | 17,7% | 43,8% | 7,2 | 21% |
| u59_ms_up | 100% | 9 | 27,6% | 1,24 | 1,36 | 9,7% | 0,35 | 0,29 | 11,2% | 34,7% | 18,6% | 43,4% | 6,8 | 26% |
| el_b3_ew | 60% | 5 | 19,7% | 0,84 | 0,93 | 7,8% | 0,40 | 0,38 | 7,6% | 23,9% | 11,7% | 29,2% | 4,5 | 31% |
| el_b3_iv | 60% | 5 | 19,7% | 0,84 | 0,94 | 7,8% | 0,40 | 0,38 | 7,5% | 24,1% | 11,7% | 29,4% | 4,5 | 31% |
| el_b3_rp | 60% | 5 | 19,6% | 0,84 | 0,93 | 7,8% | 0,40 | 0,38 | 7,5% | 23,8% | 11,7% | 29,1% | 4,5 | 31% |
| el_b3_mv | 60% | 5 | 19,6% | 0,83 | 0,93 | 7,8% | 0,40 | 0,38 | 7,5% | 23,8% | 11,7% | 29,6% | 4,4 | 31% |
| el_b3_ms_tir | 60% | 5 | 19,8% | 0,84 | 0,93 | 8,0% | 0,40 | 0,38 | 7,6% | 24,3% | 12,1% | 30,4% | 4,1 | 31% |
| el_b3_ms_up | 60% | 5 | 20,2% | 0,81 | 0,90 | 7,8% | 0,38 | 0,40 | 7,8% | 22,6% | 11,9% | 27,8% | 3,6 | 38% |
| rec_op7_core | 60% | 8 | 19,5% | 0,86 | 0,95 | 7,6% | 0,39 | 0,36 | 7,5% | 24,0% | 12,0% | 29,7% | 5,2 | 32% |
| rec_elig_core | 60% | 5 | 19,7% | 0,84 | 0,93 | 7,9% | 0,40 | 0,38 | 7,5% | 23,7% | 11,8% | 29,8% | 4,4 | 31% |
| alt_u59_halfkelly | 82% | 9 | 21,5% | 1,05 | 1,05 | 9,2% | 0,43 | 0,22 | 8,3% | 29,2% | 14,5% | 36,7% | 7,2 | 21% |

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
| u59_ms_tir | Consumo Cíclico 37 · Financeiro 30 · Consumo não Cíclico 20 · Saúde 11 · Bens Industriais 2 |
| u59_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 · Bens Industriais 14 · Comunicações 12 · Financeiro 10 · Saúde 4 |
| el_b3_ew | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| el_b3_iv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| el_b3_rp | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| el_b3_mv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| el_b3_ms_tir | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| el_b3_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| rec_op7_core | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| rec_elig_core | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| alt_u59_halfkelly | Consumo Cíclico 30 · Financeiro 25 · Consumo não Cíclico 16 · Saúde 9 · Bens Industriais 2 |

## Estresses (choque instantâneo, % do capital)

| Carteira | Ibov −20% (beta baixa) | Ibov −20% (reação de hoje) | DI +300 bp | Dólar +20% puro | Dólar +20% c/ co-mov. | Ibov +30% (beta alta) |
|---|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | -19,4% | -31,7% | -11,1% | -4,8% | -19,8% | 25,9% |
| op7_b3_iv | -19,3% | -31,6% | -11,0% | -4,9% | -19,8% | 25,8% |
| op7_b3_rp | -19,4% | -31,6% | -11,1% | -4,8% | -19,8% | 25,8% |
| op7_b3_mv | -19,0% | -30,8% | -10,8% | -5,6% | -19,5% | 24,5% |
| op7_b3_ms_tir | -18,6% | -32,0% | -10,4% | -5,9% | -19,5% | 25,2% |
| op7_b3_ms_up | -18,3% | -30,5% | -11,2% | -5,8% | -18,6% | 23,6% |
| op7_sub_ew | -35,5% | -55,3% | -17,1% | -10,8% | -36,4% | 46,5% |
| op7_sub_iv | -35,1% | -54,9% | -17,1% | -10,8% | -36,1% | 46,0% |
| op7_sub_rp | -34,6% | -54,5% | -17,4% | -10,4% | -35,5% | 45,3% |
| op7_sub_mv | -33,6% | -53,4% | -17,2% | -11,1% | -34,9% | 43,1% |
| op7_sub_ms_tir | -33,4% | -55,9% | -17,0% | -11,1% | -35,5% | 44,5% |
| op7_sub_ms_up | -34,6% | -50,7% | -17,5% | -10,5% | -33,0% | 41,3% |
| u59_ew | -24,2% | -35,7% | -23,3% | -6,4% | -27,3% | 35,7% |
| u59_iv | -22,4% | -31,3% | -22,8% | -5,3% | -24,7% | 32,6% |
| u59_rp | -20,9% | -27,4% | -22,6% | -3,7% | -22,2% | 29,9% |
| u59_mv | -12,7% | -7,6% | -20,7% | 2,1% | -9,9% | 16,8% |
| u59_ms_tir | -25,9% | -51,2% | -19,2% | -5,7% | -27,3% | 39,6% |
| u59_ms_up | -27,3% | -41,9% | -20,0% | -7,4% | -26,4% | 36,9% |
| el_b3_ew | -18,7% | -30,2% | -10,5% | -5,9% | -19,0% | 24,4% |
| el_b3_iv | -18,7% | -30,2% | -10,5% | -5,9% | -19,1% | 24,5% |
| el_b3_rp | -18,7% | -30,2% | -10,5% | -5,9% | -19,0% | 24,4% |
| el_b3_mv | -18,6% | -30,4% | -10,5% | -6,0% | -19,1% | 24,1% |
| el_b3_ms_tir | -18,5% | -32,0% | -10,4% | -5,9% | -19,5% | 25,2% |
| el_b3_ms_up | -18,0% | -30,2% | -11,1% | -6,1% | -18,5% | 23,8% |
| rec_op7_core | -19,0% | -31,8% | -10,7% | -5,3% | -19,7% | 25,5% |
| rec_elig_core | -18,6% | -31,1% | -10,4% | -5,9% | -19,3% | 24,8% |
| alt_u59_halfkelly | -21,1% | -41,8% | -15,7% | -4,7% | -22,3% | 32,3% |
| Ibovespa (referência) | −20,0% | −20,0% | — | — | -18,3% | +30,0% |

A coluna "reação de hoje" usa a razão entre a queda de cada ação e a do Ibovespa em 26/10. Como o universo foi escolhido justamente por ter caído ≥ 20%, essa razão superestima o beta. Ainda assim, ela mostra que em choques políticos os nomes domésticos se movem perto do dobro do índice.

## Monte Carlo de 1 ano (bootstrap estacionário, 10 mil trajetórias)

Regimes: `normal_hist` = dias de 2016–2026 com a média histórica; `normal_tir` = mesmos dias com a média de cada ação trocada pela TIR de dono; `choque_tir` = 3 meses sorteados dos dias de crise e 9 meses normais; `crise_tir` = o ano todo em dias de crise (vol 21d do Ibovespa ≥ 28,1%: 267 dias, em 2016, 2017, 2018, 2020, 2021, 2022 e out/2026); `crise_hist` = dias de crise com a média que tiveram.

| Carteira | Regime | Média | p5 | p25 | p50 | p75 | p95 | P(perda) | P(< CDI) | DD mediano | P(DD > 25%) | Kelly cheio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rec_op7_core | normal_hist | 16,7% | -19,8% | 0,5% | 15,3% | 31,2% | 58,6% | 24% | 48% | -14,3% | 14% | 0,64 |
| rec_op7_core | normal_tir | 21,2% | -16,7% | 4,3% | 19,7% | 36,2% | 64,6% | 19% | 40% | -13,7% | 12% | 1,42 |
| rec_op7_core | choque_tir | 22,5% | -29,9% | -1,0% | 20,4% | 43,7% | 81,1% | 26% | 41% | -17,0% | 33% | 0,90 |
| rec_op7_core | crise_tir | 26,6% | -50,4% | -13,9% | 19,3% | 58,4% | 128,9% | 36% | 46% | -38,3% | 71% | 0,55 |
| rec_op7_core | crise_hist | 31,0% | -48,7% | -10,9% | 23,4% | 63,8% | 136,7% | 33% | 43% | -38,0% | 71% | 0,70 |
| alt_u59_halfkelly | normal_hist | 16,8% | -26,6% | -2,9% | 14,5% | 33,7% | 68,6% | 29% | 49% | -17,6% | 23% | 0,45 |
| alt_u59_halfkelly | normal_tir | 22,9% | -22,8% | 2,1% | 20,4% | 40,7% | 77,3% | 22% | 40% | -16,4% | 19% | 1,18 |
| alt_u59_halfkelly | choque_tir | 24,7% | -38,4% | -5,9% | 20,7% | 50,3% | 101,6% | 30% | 43% | -21,3% | 42% | 0,74 |
| alt_u59_halfkelly | crise_tir | 30,4% | -60,1% | -22,4% | 15,3% | 66,0% | 166,7% | 40% | 49% | -46,4% | 77% | 0,44 |
| alt_u59_halfkelly | crise_hist | 38,5% | -57,6% | -17,6% | 22,4% | 76,1% | 183,0% | 36% | 45% | -45,8% | 77% | 0,63 |
| op7_b3_ms_tir | normal_hist | 17,0% | -20,3% | 0,6% | 15,7% | 31,7% | 59,7% | 24% | 47% | -14,6% | 14% | 0,68 |
| op7_b3_ms_tir | normal_tir | 21,4% | -17,4% | 4,3% | 20,0% | 36,6% | 65,6% | 20% | 40% | -13,8% | 13% | 1,40 |
| op7_b3_ms_tir | choque_tir | 22,7% | -31,1% | -1,4% | 20,5% | 44,4% | 82,9% | 26% | 42% | -17,4% | 34% | 0,89 |
| op7_b3_ms_tir | crise_tir | 26,9% | -50,9% | -14,3% | 18,8% | 58,9% | 132,8% | 36% | 46% | -38,8% | 72% | 0,54 |
| op7_b3_ms_tir | crise_hist | 30,0% | -49,7% | -12,3% | 21,7% | 62,8% | 138,5% | 34% | 44% | -38,7% | 72% | 0,64 |
| op7_sub_ms_tir | normal_hist | 20,2% | -42,6% | -10,8% | 13,8% | 44,7% | 103,3% | 36% | 50% | -27,0% | 57% | 0,41 |
| op7_sub_ms_tir | normal_tir | 26,9% | -39,4% | -5,8% | 20,2% | 52,8% | 114,7% | 30% | 44% | -25,7% | 53% | 0,79 |
| op7_sub_ms_tir | choque_tir | 31,5% | -55,9% | -17,0% | 20,7% | 68,0% | 156,3% | 37% | 46% | -31,5% | 65% | 0,56 |
| op7_sub_ms_tir | crise_tir | 48,6% | -77,8% | -40,4% | 10,6% | 93,1% | 299,0% | 46% | 51% | -59,7% | 86% | 0,39 |
| op7_sub_ms_tir | crise_hist | 66,2% | -75,2% | -33,3% | 23,7% | 116,0% | 346,2% | 40% | 46% | -58,9% | 84% | 0,56 |
| u59_ms_tir | normal_hist | 17,7% | -34,5% | -7,1% | 13,8% | 37,9% | 83,1% | 33% | 50% | -22,0% | 39% | 0,37 |
| u59_ms_tir | normal_tir | 25,2% | -30,3% | -1,1% | 21,0% | 46,7% | 94,8% | 26% | 41% | -20,5% | 33% | 0,99 |
| u59_ms_tir | choque_tir | 28,0% | -47,8% | -11,3% | 21,0% | 58,4% | 127,1% | 33% | 44% | -26,5% | 53% | 0,63 |
| u59_ms_tir | crise_tir | 36,9% | -69,9% | -31,3% | 12,2% | 76,8% | 218,6% | 43% | 51% | -54,4% | 82% | 0,39 |
| u59_ms_tir | crise_hist | 47,3% | -67,6% | -26,0% | 20,7% | 90,2% | 242,7% | 40% | 46% | -53,9% | 81% | 0,55 |
| u59_rp | normal_hist | 20,4% | -22,3% | 2,1% | 18,6% | 36,7% | 68,9% | 22% | 42% | -15,0% | 16% | 1,04 |
| u59_rp | normal_tir | 13,3% | -26,9% | -3,9% | 11,6% | 28,6% | 58,9% | 31% | 54% | -16,4% | 19% | 0,00 |
| u59_rp | choque_tir | 15,1% | -42,8% | -13,1% | 12,4% | 39,1% | 81,7% | 38% | 51% | -22,7% | 44% | 0,10 |
| u59_rp | crise_tir | 21,6% | -65,6% | -30,2% | 5,9% | 55,7% | 158,1% | 46% | 55% | -47,7% | 80% | 0,19 |
| u59_rp | crise_hist | 41,9% | -59,8% | -18,4% | 23,6% | 81,7% | 201,2% | 36% | 45% | -46,2% | 78% | 0,64 |
| u59_mv | normal_hist | 17,8% | -13,0% | 4,9% | 16,7% | 29,8% | 51,3% | 17% | 43% | -11,2% | 9% | 1,23 |
| u59_mv | normal_tir | 11,5% | -17,7% | -0,7% | 10,5% | 22,9% | 43,3% | 26% | 57% | -12,3% | 10% | 0,00 |
| u59_mv | choque_tir | 12,7% | -32,1% | -8,0% | 11,5% | 30,5% | 60,4% | 35% | 53% | -16,6% | 32% | 0,00 |
| u59_mv | crise_tir | 18,2% | -53,7% | -21,7% | 7,7% | 45,1% | 118,1% | 44% | 55% | -37,9% | 72% | 0,15 |
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
| RENT3 | Consumo Cíclico | 40,8% | 1,73 | 1,58 | 1,93 | -43,3% | 1,5% | -20,7% | -31,5% | -24,0% | -1,2% | 7,7 | -0,84 | -16,7% |
| MOVI3 | Consumo Cíclico | 64,7% | 2,53 | 2,35 | 2,84 | -64,5% | 9,2% | -14,3% | -46,9% | -34,0% | -19,0% | 6,2 | -1,65 | -33,0% |
| VAMO3 | Consumo Cíclico | 59,1% | 2,31 | 1,71 | 2,73 | -59,9% | 2,6% | -28,3% | -34,2% | -34,1% | -11,6% | 8,5 | 0,29 | 5,8% |
| SIMH3 | Financeiro | 60,5% | 2,49 | 2,07 | 2,60 | -68,5% | — | -24,6% | -41,4% | -42,6% | -26,6% | 7,3 | -0,65 | -13,0% |
| ECOR3 | Bens Industriais | 48,2% | 2,12 | 2,34 | 2,23 | -59,9% | 3,9% | -26,0% | -46,8% | -22,9% | -0,3% | 7,6 | -0,86 | -17,2% |
| MOTV3 | Bens Industriais | 26,6% | 1,22 | 1,44 | 1,17 | -27,7% | -1,0% | -28,5% | -28,8% | -25,5% | -3,3% | 7,7 | -0,39 | -7,8% |
| RAIL3 | Bens Industriais | 31,2% | 1,16 | 0,99 | 1,22 | -22,7% | -3,8% | -30,4% | -19,8% | -25,2% | -2,8% | 7,7 | -0,25 | -5,0% |
| CSAN3 | Petróleo. Gás e Biocombustíveis | 44,6% | 1,97 | 1,75 | 2,18 | -54,4% | — | -4,0% | -34,9% | -24,8% | -3,9% | 7,3 | -0,54 | -10,9% |
| VBBR3 | Petróleo. Gás e Biocombustíveis | 29,0% | 1,02 | 1,14 | 0,74 | -14,1% | -3,4% | -41,4% | -22,9% | -24,7% | -2,1% | 7,7 | 0,00 | 0,0% |
| MGLU3 | Consumo Cíclico | 69,7% | 2,63 | 1,93 | 3,03 | -59,5% | -7,1% | -36,6% | -38,5% | -35,8% | -10,1% | 9,5 | -0,29 | -5,9% |
| SBFG3 | Consumo Cíclico | 51,3% | 2,00 | 1,85 | 2,20 | -55,3% | 9,0% | -11,9% | -37,1% | -20,4% | -4,5% | 5,6 | -0,65 | -13,0% |
| CEAB3 ★ | Consumo Cíclico | 58,3% | 2,02 | 1,82 | 2,15 | -50,4% | 8,1% | -1,1% | -36,4% | -19,0% | -2,0% | 5,8 | -0,35 | -6,9% |
| LREN3 | Consumo Cíclico | 42,9% | 1,75 | 1,68 | 1,62 | -36,1% | 6,1% | -3,1% | -33,6% | -15,6% | 0,5% | 5,4 | -0,78 | -15,6% |
| AZZA3 | Consumo Cíclico | 48,4% | 1,57 | 1,59 | 1,52 | -40,9% | -0,3% | -24,3% | -31,8% | -29,5% | -4,2% | 8,8 | -0,95 | -19,1% |
| VIVA3 | Consumo Cíclico | 38,1% | 1,33 | 1,22 | 1,23 | -34,8% | 2,6% | -9,6% | -24,3% | -23,1% | -0,3% | 7,6 | -0,27 | -5,4% |
| VULC3 | Consumo Cíclico | 32,5% | 1,01 | 1,11 | 0,96 | -26,3% | 4,4% | -6,7% | -22,2% | -19,3% | -0,8% | 6,2 | -0,49 | -9,9% |
| ALPA4 | Consumo Cíclico | 40,3% | 1,22 | 1,36 | 0,75 | -21,2% | -2,6% | -21,7% | -27,2% | -24,0% | -0,3% | 7,9 | -0,46 | -9,1% |
| NATU3 | Consumo não Cíclico | 46,9% | 1,14 | 1,30 | 1,08 | -36,5% | -0,2% | -18,5% | -26,0% | -28,7% | -2,8% | 8,9 | -0,42 | -8,4% |
| ASAI3 | Consumo não Cíclico | 46,4% | 1,81 | 1,79 | 2,12 | -43,4% | 0,4% | -34,2% | -35,8% | -30,5% | -5,7% | 8,8 | -0,44 | -8,8% |
| GMAT3 | Consumo não Cíclico | 36,9% | 1,28 | 1,10 | 1,30 | -33,2% | -0,3% | -29,9% | -22,1% | -26,1% | -0,8% | 8,5 | -0,26 | -5,2% |
| PGMN3 | Saúde | 47,8% | 1,80 | 1,93 | 1,88 | -51,6% | 7,1% | -6,8% | -38,6% | -23,1% | -5,0% | 6,3 | -0,25 | -4,9% |
| RADL3 | Saúde | 36,5% | 1,13 | 1,08 | 1,06 | -22,7% | -1,9% | -26,4% | -21,6% | -26,0% | -0,5% | 8,5 | -0,36 | -7,2% |
| HYPE3 | Saúde | 32,9% | 1,02 | 0,97 | 0,89 | -20,7% | -0,4% | -21,9% | -19,5% | -24,3% | -1,9% | 7,6 | -0,46 | -9,1% |
| CYRE3 | Consumo Cíclico | 38,4% | 1,68 | 1,84 | 1,72 | -50,1% | 8,7% | -0,7% | -36,7% | -15,8% | -1,5% | 4,8 | -0,60 | -12,0% |
| EZTC3 | Consumo Cíclico | 41,7% | 1,56 | 1,69 | 1,69 | -50,7% | 3,5% | 3,7% | -33,9% | -17,4% | 1,4% | 6,2 | -0,46 | -9,3% |
| MDNE3 ★ | Consumo Cíclico | 45,7% | 1,69 | 1,92 | 1,60 | -44,3% | 13,4% | 5,5% | -38,3% | -11,7% | 0,6% | 4,1 | -0,74 | -14,9% |
| JHSF3 | Consumo Cíclico | 37,1% | 1,37 | 1,28 | 1,02 | -31,6% | -4,0% | -35,2% | -25,5% | -25,5% | -3,1% | 7,7 | -0,47 | -9,4% |
| MRVE3 | Consumo Cíclico | 50,8% | 1,83 | 1,85 | 1,90 | -48,1% | -0,8% | -20,2% | -37,1% | -35,1% | -12,1% | 8,7 | -0,73 | -14,5% |
| PLPL3 ★ | Consumo Cíclico | 50,6% | 1,60 | 1,72 | 1,82 | -42,8% | 14,2% | 8,9% | -34,5% | -14,3% | -1,1% | 4,5 | -0,74 | -14,8% |
| DIRR3 | Consumo Cíclico | 36,9% | 1,36 | 1,63 | 1,10 | -25,6% | 8,1% | -0,7% | -32,6% | -16,3% | -0,4% | 5,3 | -0,87 | -17,4% |
| CURY3 | Consumo Cíclico | 36,2% | 1,25 | 1,39 | 1,05 | -18,9% | 5,7% | -5,6% | -27,9% | -17,0% | 0,2% | 5,7 | -0,58 | -11,5% |
| TEND3 ★ | Consumo Cíclico | 50,3% | 1,60 | 1,90 | 1,24 | -25,2% | 11,4% | 7,5% | -38,0% | -15,3% | -1,1% | 4,8 | -0,78 | -15,5% |
| MULT3 | Financeiro | 26,0% | 1,20 | 1,30 | 1,17 | -31,1% | 0,6% | -17,4% | -26,0% | -25,1% | -1,9% | 7,9 | -0,51 | -10,1% |
| IGTI11 | Financeiro | 27,7% | 1,28 | 1,40 | 1,24 | -29,5% | -0,0% | -16,0% | -28,0% | -25,2% | -1,5% | 8,0 | -0,47 | -9,4% |
| ALOS3 | Financeiro | 24,5% | 1,17 | 1,30 | 1,11 | -30,4% | -1,1% | -19,9% | -25,9% | -21,6% | -1,6% | 6,8 | -0,50 | -10,1% |
| SMFT3 | Consumo Cíclico | 36,2% | 1,46 | 1,17 | 1,63 | -35,8% | 0,1% | -24,6% | -23,3% | -27,9% | -1,1% | 9,0 | -1,20 | -24,1% |
| CVCB3 | Consumo Cíclico | 65,9% | 1,81 | 1,85 | 1,85 | -43,9% | — | -47,5% | -36,9% | -38,3% | -21,1% | 7,3 | -1,57 | -31,5% |
| YDUQ3 | Consumo Cíclico | 50,6% | 1,73 | 1,60 | 1,55 | -37,6% | 5,8% | -9,2% | -32,0% | -24,6% | -6,8% | 6,4 | -1,10 | -22,1% |
| COGN3 ★ | Consumo Cíclico | 51,4% | 1,85 | 1,84 | 1,81 | -45,5% | 10,6% | 3,8% | -36,7% | -18,6% | -3,9% | 5,1 | -0,61 | -12,2% |
| ANIM3 | Consumo Cíclico | 68,6% | 2,48 | 2,67 | 2,46 | -51,8% | 9,2% | -3,4% | -53,3% | -33,5% | -17,0% | 6,6 | -1,14 | -22,8% |
| HAPV3 | Saúde | 61,1% | 1,84 | 1,29 | 1,96 | -52,3% | 15,7% | 1,7% | -25,8% | -24,8% | -10,6% | 5,3 | -0,21 | -4,2% |
| RDOR3 | Saúde | 31,7% | 1,26 | 1,08 | 1,27 | -22,7% | -1,5% | -27,2% | -21,7% | -26,3% | -1,5% | 8,4 | -0,27 | -5,3% |
| B3SA3 | Financeiro | 35,4% | 1,71 | 1,50 | 2,10 | -38,0% | -2,2% | -20,4% | -30,1% | -20,3% | 0,2% | 6,8 | -0,51 | -10,1% |
| BPAC11 | Financeiro | 32,9% | 1,57 | 1,63 | 1,72 | -29,4% | -0,6% | -19,6% | -32,6% | -26,5% | 0,0% | 8,8 | -0,74 | -14,8% |
| BBAS3 | Financeiro | 26,3% | 1,06 | 1,15 | 1,12 | -31,9% | 6,7% | -2,7% | -23,0% | -19,0% | 0,0% | 6,3 | 0,01 | 0,2% |
| BBDC4 | Financeiro | 28,9% | 1,27 | 1,19 | 1,49 | -27,8% | 4,8% | -5,8% | -23,7% | -18,5% | 0,0% | 6,2 | -0,24 | -4,8% |
| BRSR6 | Financeiro | 28,5% | 0,95 | 1,08 | 0,92 | -28,7% | 5,5% | -6,2% | -21,6% | -18,8% | 0,0% | 6,3 | -0,15 | -3,1% |
| AURE3 | Utilidade Pública | 29,7% | 1,08 | 1,14 | 1,17 | -27,4% | -7,0% | -48,0% | -22,7% | -28,1% | -2,0% | 8,9 | -0,15 | -3,0% |
| ENGI11 | Utilidade Pública | 27,2% | 1,32 | 1,19 | 1,45 | -31,9% | -5,5% | -40,0% | -23,7% | -29,2% | -7,4% | 7,8 | -0,64 | -12,8% |
| EQTL3 | Utilidade Pública | 25,0% | 1,18 | 1,10 | 1,28 | -30,3% | -6,4% | -46,8% | -21,9% | -27,2% | -3,0% | 8,3 | -0,63 | -12,5% |
| CPLE3 | Utilidade Pública | 23,3% | 0,98 | 1,08 | 0,85 | -15,4% | -5,2% | -42,8% | -21,6% | -21,3% | -1,2% | 6,8 | 0,01 | 0,3% |
| ALUP11 | Utilidade Pública | 20,6% | 0,78 | 0,81 | 0,84 | -17,4% | -3,1% | -34,1% | -16,2% | -22,1% | 0,3% | 7,4 | -0,34 | -6,8% |
| SBSP3 | Utilidade Pública | 26,2% | 1,07 | 1,14 | 1,13 | -22,1% | -5,4% | -40,2% | -22,8% | -26,7% | -1,5% | 8,5 | -0,24 | -4,8% |
| TOTS3 | Tecnologia da Informação | 33,9% | 0,98 | 0,98 | 0,75 | -23,1% | -2,0% | -21,9% | -19,7% | -24,9% | -0,6% | 8,1 | -0,39 | -7,8% |
| INTB3 | Tecnologia da Informação | 38,1% | 1,17 | 1,07 | 1,25 | -27,2% | -0,8% | -17,7% | -21,3% | -21,5% | 0,8% | 7,4 | -0,84 | -16,8% |
| GGPS3 | Bens Industriais | 32,3% | 1,26 | 1,19 | 1,54 | -34,0% | 1,7% | -12,5% | -23,8% | -26,2% | -1,1% | 8,4 | -0,72 | -14,4% |
| ORVR3 | Utilidade Pública | 28,7% | 1,08 | 1,28 | 1,17 | -24,5% | -4,1% | -30,1% | -25,6% | -27,6% | -0,7% | 9,1 | -0,72 | -14,3% |
| BEEF3 ★ | Consumo não Cíclico | 44,4% | 1,04 | 1,10 | 1,08 | -32,8% | 13,3% | 20,7% | -22,1% | -22,7% | -8,9% | 5,1 | 0,07 | 1,3% |
| TTEN3 | Consumo não Cíclico | 38,3% | 0,94 | 0,95 | 0,85 | -24,8% | -1,1% | -31,3% | -19,0% | -28,3% | -2,9% | 8,7 | -0,73 | -14,6% |
| PETR4 | Petróleo. Gás e Biocombustíveis | 26,8% | 0,62 | 0,66 | 0,60 | -10,1% | 1,1% | -19,0% | -13,3% | -20,9% | 0,2% | 7,0 | 0,59 | 11,8% |
| PETR3 | Petróleo. Gás e Biocombustíveis | 29,1% | 0,65 | 0,65 | 0,59 | -9,4% | -0,0% | -22,0% | -12,9% | -20,9% | 0,2% | 7,0 | 0,63 | 12,5% |
| PRIO3 | Petróleo. Gás e Biocombustíveis | 33,3% | 0,54 | 0,53 | 0,36 | -2,0% | -0,1% | -11,8% | -10,6% | -14,6% | 0,0% | 4,9 | 0,34 | 6,7% |
| BRAV3 | Petróleo. Gás e Biocombustíveis | 44,4% | 0,80 | 0,87 | 0,49 | -14,9% | -2,3% | -31,1% | -17,5% | -22,9% | -3,0% | 6,8 | 1,21 | 24,1% |
| RECV3 | Petróleo. Gás e Biocombustíveis | 36,5% | 0,92 | 0,86 | 0,70 | -13,0% | -0,4% | -24,8% | -17,2% | -17,2% | 2,2% | 6,3 | 0,07 | 1,5% |
| UGPA3 | Petróleo. Gás e Biocombustíveis | 31,7% | 1,10 | 1,35 | 0,81 | -15,2% | -3,3% | -28,2% | -27,0% | -22,3% | -1,0% | 7,2 | 0,16 | 3,2% |
| ENEV3 | Utilidade Pública | 30,0% | 1,08 | 1,06 | 0,92 | -15,9% | -6,5% | -52,8% | -21,2% | -26,2% | -0,3% | 8,7 | -0,39 | -7,8% |
| UNIP6 | Materiais Básicos | 30,8% | 0,77 | 0,73 | 0,73 | -14,2% | -3,0% | -33,7% | -14,6% | -22,0% | -1,2% | 7,0 | -0,19 | -3,7% |
| VALE3 | Materiais Básicos | 25,1% | 0,76 | 0,79 | 0,75 | -1,3% | -8,0% | -51,0% | -15,7% | -13,4% | -0,1% | 4,5 | 0,39 | 7,8% |
| BRAP4 | Materiais Básicos | 25,4% | 0,86 | 0,84 | 0,98 | -5,2% | — | -40,5% | -16,8% | -21,5% | 0,4% | 7,3 | 0,32 | 6,3% |
| CBAV3 | Materiais Básicos | 48,7% | 0,92 | 0,86 | 0,67 | 0,5% | -7,7% | -7,6% | -17,3% | -20,6% | 1,8% | 7,3 | 0,67 | 13,5% |
| GGBR4 | Materiais Básicos | 29,0% | 0,85 | 0,87 | 0,72 | -4,9% | -3,5% | -26,2% | -17,5% | -20,7% | -0,4% | 6,8 | 0,23 | 4,7% |
| GOAU4 | Materiais Básicos | 29,0% | 0,92 | 0,90 | 0,86 | -6,8% | — | -21,7% | -17,9% | -22,1% | -0,4% | 7,3 | 0,26 | 5,3% |
| USIM5 | Materiais Básicos | 43,8% | 1,08 | 1,08 | 0,76 | -14,3% | -2,0% | -15,9% | -21,6% | -21,7% | 0,1% | 7,3 | -0,05 | -1,0% |
| SUZB3 | Materiais Básicos | 26,1% | 0,28 | 0,28 | 0,35 | 11,9% | -0,8% | -34,0% | -5,6% | -23,4% | -0,2% | 7,8 | 0,43 | 8,5% |
| KLBN11 | Materiais Básicos | 21,4% | 0,56 | 0,54 | 0,55 | -3,2% | -2,1% | -43,4% | -10,7% | -20,8% | 0,5% | 7,1 | 0,21 | 4,1% |
| SLCE3 | Consumo não Cíclico | 25,0% | 0,44 | 0,26 | 0,32 | -3,5% | -4,3% | -13,4% | -5,3% | -25,7% | -4,4% | 7,4 | -0,21 | -4,3% |
| WEGE3 | Bens Industriais | 29,3% | 0,65 | 0,47 | 0,57 | 10,9% | -5,5% | -38,3% | -9,4% | -24,6% | 0,0% | 8,2 | 0,37 | 7,3% |
| EMBJ3 | Bens Industriais | 39,8% | 0,56 | 1,33 | 0,18 | 9,5% | -4,5% | -32,0% | -26,5% | -26,0% | 0,0% | 8,7 | 0,85 | 17,0% |
| POMO4 | Bens Industriais | 40,0% | 1,05 | 1,21 | 1,14 | -18,4% | 7,5% | -0,3% | -24,1% | -17,2% | -0,7% | 5,5 | -0,59 | -11,9% |
| RAPT4 | Bens Industriais | 39,2% | 1,37 | 1,21 | 1,38 | -54,5% | 2,0% | -19,4% | -24,2% | -36,7% | -15,1% | 8,5 | -0,81 | -16,2% |
| TUPY3 | Bens Industriais | 34,7% | 0,96 | 0,90 | 1,11 | -24,5% | 2,3% | -27,8% | -18,0% | -24,3% | -1,6% | 7,7 | -0,22 | -4,4% |
| LEVE3 | Consumo Cíclico | 27,5% | 0,61 | 0,70 | 0,57 | -17,4% | 4,0% | -11,4% | -13,9% | -18,5% | 0,4% | 6,3 | 0,12 | 2,3% |
| DXCO3 | Materiais Básicos | 37,1% | 1,38 | 1,07 | 1,41 | -43,6% | -3,3% | -36,8% | -21,5% | -29,0% | -5,7% | 8,2 | -1,13 | -22,6% |
| ITUB4 | Financeiro | 23,3% | 1,10 | 1,15 | 1,17 | -17,4% | 0,2% | -15,1% | -23,0% | -21,2% | 0,0% | 7,1 | -0,17 | -3,3% |
| ITSA4 | Financeiro | 23,6% | 1,17 | 1,16 | 1,25 | -15,7% | — | -9,6% | -23,1% | -21,8% | -0,1% | 7,3 | -0,19 | -3,8% |
| SANB11 | Financeiro | 26,6% | 1,00 | 1,20 | 0,82 | -11,6% | 1,6% | -12,1% | -23,9% | -22,8% | 0,0% | 7,6 | -0,06 | -1,1% |
| BBDC3 | Financeiro | 26,8% | 1,22 | 1,16 | 1,46 | -25,8% | 6,1% | -2,8% | -23,2% | -17,1% | 0,0% | 5,7 | -0,25 | -5,1% |
| ABCB4 | Financeiro | 25,5% | 0,90 | 0,95 | 0,98 | -21,8% | 3,5% | -11,6% | -18,9% | -19,8% | 2,6% | 7,3 | -0,01 | -0,1% |
| PINE4 | Financeiro | 42,0% | 1,02 | 0,77 | 0,98 | -35,2% | 8,8% | -4,3% | -15,3% | -22,5% | -7,5% | 5,4 | -0,19 | -3,7% |
| BBSE3 | Financeiro | 20,4% | 0,50 | 0,56 | 0,43 | -5,2% | 1,7% | -12,7% | -11,1% | -20,2% | 0,8% | 6,9 | 0,00 | 0,0% |
| CXSE3 | Financeiro | 23,4% | 0,58 | 0,78 | 0,47 | -1,2% | -1,3% | -17,2% | -15,6% | -21,1% | 0,9% | 7,3 | 0,18 | 3,5% |
| PSSA3 | Financeiro | 24,0% | 0,67 | 0,87 | 0,64 | -9,1% | 1,1% | -9,4% | -17,4% | -21,8% | 1,9% | 7,8 | -0,44 | -8,8% |
| IRBR3 | Financeiro | 44,3% | 1,06 | 1,38 | 0,75 | -16,4% | 0,9% | -15,2% | -27,7% | -18,6% | 3,4% | 7,1 | 0,27 | 5,4% |
| SAUD3 | Saúde | 33,5% | 1,14 | 0,68 | 1,18 | -11,5% | 0,7% | -12,2% | -13,6% | -23,0% | 1,2% | 8,0 | 0,07 | 1,3% |
| AXIA3 | Utilidade Pública | 27,6% | 1,29 | 1,42 | 1,11 | -16,9% | -6,9% | -45,8% | -28,4% | -19,8% | -1,3% | 6,2 | 0,12 | 2,3% |
| CMIG4 | Utilidade Pública | 25,1% | 0,88 | 0,84 | 0,85 | -13,0% | -2,6% | -37,1% | -16,8% | -22,5% | -1,0% | 7,3 | 0,07 | 1,4% |
| EGIE3 | Utilidade Pública | 22,5% | 0,75 | 0,74 | 0,74 | -11,3% | -4,0% | -36,7% | -14,7% | -21,7% | -0,9% | 7,0 | -0,11 | -2,2% |
| CPFE3 | Utilidade Pública | 22,1% | 0,75 | 0,75 | 0,69 | -13,7% | -2,6% | -34,1% | -15,0% | -22,3% | -2,1% | 6,9 | -0,16 | -3,2% |
| ISAE4 | Utilidade Pública | 21,9% | 0,85 | 0,89 | 0,72 | -10,9% | -7,4% | -41,7% | -17,7% | -18,6% | -1,4% | 5,8 | 0,03 | 0,6% |
| TAEE11 | Utilidade Pública | 18,2% | 0,71 | 0,72 | 0,69 | -10,5% | -6,1% | -36,0% | -14,5% | -17,6% | -1,9% | 5,3 | -0,00 | -0,0% |
| CSMG3 | Utilidade Pública | 30,7% | 0,76 | 0,90 | 0,92 | -22,6% | -4,1% | -38,1% | -18,0% | -24,2% | -0,4% | 7,9 | -0,12 | -2,5% |
| SAPR11 | Utilidade Pública | 28,7% | 0,81 | 0,81 | 0,90 | -22,7% | -0,6% | -32,0% | -16,2% | -24,0% | 1,3% | 8,3 | -0,15 | -3,0% |
| ABEV3 | Consumo não Cíclico | 23,4% | 0,66 | 0,65 | 0,56 | -9,0% | -1,9% | -17,7% | -12,9% | -20,2% | 0,0% | 6,7 | -0,01 | -0,2% |
| MDIA3 | Consumo não Cíclico | 33,7% | 0,80 | 0,78 | 1,01 | -17,7% | -0,5% | -11,5% | -15,6% | -20,7% | 0,5% | 7,0 | -0,32 | -6,4% |
| GRND3 | Consumo Cíclico | 30,5% | 0,80 | 0,86 | 0,70 | -21,8% | -0,4% | -9,4% | -17,3% | -17,3% | 1,0% | 6,0 | -0,21 | -4,1% |
| VIVT3 | Comunicações | 24,5% | 0,73 | 0,85 | 0,72 | -4,9% | -1,9% | -23,1% | -16,9% | -19,7% | -0,4% | 6,5 | -0,41 | -8,2% |
| TIMS3 | Comunicações | 27,1% | 0,72 | 0,79 | 0,57 | -0,5% | 0,4% | -17,5% | -15,9% | -19,5% | -0,4% | 6,4 | -0,26 | -5,2% |
| DESK3 | Comunicações | 46,6% | 0,92 | 1,01 | 0,62 | 0,4% | -3,2% | 0,2% | -20,1% | -28,9% | -3,5% | 8,8 | 0,06 | 1,2% |
| BMOB3 | Tecnologia da Informação | 32,3% | 1,13 | 1,27 | 1,00 | -27,9% | 0,2% | -16,0% | -25,3% | -22,6% | 0,6% | 7,7 | -0,14 | -2,8% |
| LWSA3 | Tecnologia da Informação | 48,2% | 1,55 | 1,49 | 1,48 | -36,1% | 1,0% | -6,1% | -29,7% | -22,1% | -0,3% | 7,3 | -0,82 | -16,3% |
| FLRY3 | Saúde | 27,8% | 0,95 | 1,08 | 0,87 | -22,2% | -2,4% | -25,7% | -21,7% | -22,0% | -0,9% | 7,1 | -0,24 | -4,8% |
| PNVL3 | Saúde | 30,8% | 1,21 | 1,40 | 1,30 | -32,5% | -1,0% | -25,5% | -28,1% | -26,4% | -1,0% | 8,6 | -0,68 | -13,6% |
| SEER3 ★ | Consumo Cíclico | 58,1% | 1,70 | 2,32 | 1,38 | -39,6% | 10,4% | 7,8% | -46,5% | -17,2% | -1,6% | 5,3 | -0,34 | -6,9% |
| VTRU3 ★ | Consumo Cíclico | 50,5% | 1,40 | 1,59 | 1,32 | -42,3% | 12,6% | 11,7% | -31,8% | -18,1% | -3,4% | 5,1 | -0,84 | -16,8% |
| RIAA3 | Consumo Cíclico | 44,8% | 1,72 | 1,32 | 1,73 | -45,2% | 3,8% | -10,6% | -26,4% | -23,1% | -2,4% | 7,1 | -1,68 | -33,6% |
| AUAU3 | Consumo Cíclico | 38,8% | 0,98 | 0,35 | 0,95 | -26,9% | 1,0% | -14,5% | -7,0% | -22,6% | 0,4% | 7,6 | -0,85 | -17,1% |
| TFCO4 | Consumo Cíclico | 32,3% | 1,25 | 1,29 | 1,34 | -31,2% | 0,7% | -13,1% | -25,8% | -25,9% | -0,4% | 8,5 | -0,63 | -12,6% |
| JSLG3 | Bens Industriais | 55,4% | 2,03 | 2,11 | 2,25 | -54,7% | 1,2% | -35,1% | -42,3% | -34,9% | -10,1% | 9,2 | 0,04 | 0,9% |
| MILS3 | Bens Industriais | 27,9% | 0,91 | 0,85 | 0,78 | -4,3% | -1,4% | -23,4% | -17,1% | -24,8% | -1,5% | 7,9 | -0,32 | -6,4% |
| OPCT3 | Petróleo. Gás e Biocombustíveis | 36,9% | 0,95 | 1,07 | 0,95 | -12,2% | -0,7% | -27,3% | -21,5% | -25,6% | -1,8% | 8,1 | -0,86 | -17,1% |
| PRNR3 | Bens Industriais | 33,9% | 1,04 | 1,14 | 0,99 | -37,7% | -2,3% | -31,3% | -22,8% | -30,2% | -5,3% | 8,8 | -0,17 | -3,4% |
| LOGG3 | Financeiro | 34,1% | 1,02 | 1,01 | 1,11 | -29,9% | -4,9% | -33,7% | -20,2% | -20,0% | -3,1% | 5,8 | -0,50 | -9,9% |

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
