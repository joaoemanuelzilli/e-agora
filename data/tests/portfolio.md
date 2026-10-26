# Carteiras pós-choque — 26/10/2026

Gerado por `pipeline/tests/portfolio.py` em 2026-10-26T16:37:19 (dados: `data/app/overview.json`, preços B3 ajustados 2016–2026, câmbio BCB). Ibovespa -14,6% no dia, dólar 9,2%, CDI 13,65%, DI longo ~15,5%. Limites: 20% por ação e 40% por setor B3. Estudo quantitativo com finalidade informativa; não é recomendação de investimento.

## Resumo

- **Carteira recomendada (alvo):** BEEF3 20 · MDNE3 13 · PLPL3 11 · TEND3 10 · COGN3 5 (% do capital) + **40% em CDI**. São as 5 oportunidades do estudo, com pesos de 50% máximo Sharpe (TIR − CDI) e 50% paridade de risco. 4 das 5 são Consumo Cíclico, então o limite de 40% por setor só permite investir 60%; o resto fica no CDI.
- **Tamanho (Kelly fracionado):** meio Kelly dá 23% do capital em ações no regime de choque (3 meses de volatilidade de crise) e 36%–46% no regime normal. Sugestão: entrar com ~23% e subir até 46% quando a volatilidade normalizar.
- **Risco ex-ante (carteira-alvo):** vol 20,5% a.a., beta 0,87 (beta de baixa 0,96), retorno esperado 20,1% a.a. (6,4% acima do CDI), Sharpe 0,31. VaR 95% de 1 mês: 8,0% (normal) e 26,4% no regime de crise; CVaR 12,1% no histórico 2016–2026 e 31,6% na crise. N efetivo 4,3; BEEF3 responde por 31% do risco.
- **Estresses (carteira-alvo):** Ibovespa −20% → -19,2% pelo beta de baixa, ou -22,6% repetindo a reação de hoje; DI +300 bp → -10,6%; dólar +20% → -5,6% no canal cambial puro e -19,7% com o co-movimento histórico da bolsa. Na reversão (Ibovespa +30%), 25,6%. No pregão de hoje a carteira teria rendido -16,5%; o beta de baixa previa -14,0%.
- **Monte Carlo 1 ano (deriva = TIR):** no regime normal, mediana 18,5%, p5 -18,2%, P(perda) 21% e P(abaixo do CDI) 42%. Com 3 meses de choque, mediana 20,1%, p5 -32,1%, P(perda) 27% e drawdown mediano -18,6%.
- **Alternativa totalmente diversificável:** o máximo Sharpe do universo de 59 (BBAS3 20 · BEEF3 20 · HAPV3 16 · PLPL3 14 · MDNE3 14 · TEND3 9 · BRSR6 4 · DIRR3 3) tem Sharpe 0,34, mas inclui nomes fora das oportunidades (BBAS3, HAPV3, BRSR6). Dimensionado a meio Kelly (57% em ações), fica com risco parecido (vol 16,9%, Ibovespa −20% → -16,4%).
- **Histórico de crashes:** em 2017-05-18, as mais caídas subiram 25,9% em 3m (mediana 18,7%; 89% acima do índice), contra 11,4% do Ibovespa. Em 12m, a mediana delas foi 21,4%, contra 28,1% do índice, e a das mais baratas por P/L 33,7%. Depois da compra, o drawdown chegou a -21,4%; em 2020-03-16, as mais caídas subiram 44,5% em 3m (mediana 39,1%; 57% acima do índice), contra 34,3% do Ibovespa. Em 12m, a mediana delas foi 64,0%, contra 59,1% do índice, e a das mais baratas por P/L 46,5%. Depois da compra, o drawdown chegou a -19,3%. A reversão das mais caídas é forte e ampla nos primeiros 3–6 meses (correlação de ranking entre a queda e o retorno de 3m: -0,32 e -0,45), mas em 12 meses a vantagem da ação mediana diminui ou some. O P/L baixo, isolado, bateu o índice em 2017 e perdeu em 2020. Nos 16 episódios de queda diária ≤ −5% do Ibovespa desde 1998, comprar no 1º dia rendeu mediana de 9,3% em 12m (69% positivos). Em 2020, comprar em 26/02 rendeu 6,6%, contra 59,1% comprando em 16/03. O risco de entrar cedo justifica a entrada escalonada.

## Carteira recomendada

**Recomendada · 5 oportunidades (50% máx. Sharpe TIR + 50% paridade de risco), setor B3 ≤ 40%, excedente em CDI**

| Ação | % capital | % das ações | Setor / subsetor | TIR | Upside | Contrib. risco | Beta baixa | DI +300 | Dólar +20% puro |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|
| BEEF3 | 20,0% | 33,3% | Consumo não Cíclico / Alimentos Processados | 24,5% | 60,9% | 30,6% | 1,10 | -22,9% | 1,3% |
| MDNE3 | 13,3% | 22,2% | Consumo Cíclico / Construção Civil | 24,5% | 2,7% | 22,8% | 1,92 | -12,8% | -14,9% |
| PLPL3 | 11,3% | 18,8% | Consumo Cíclico / Construção Civil | 25,2% | 11,8% | 20,7% | 1,72 | -15,4% | -14,8% |
| TEND3 | 10,3% | 17,2% | Consumo Cíclico / Construção Civil | 24,4% | 19,8% | 18,1% | 1,90 | -15,3% | -15,5% |
| COGN3 | 5,1% | 8,6% | Consumo Cíclico / Diversos | 21,8% | -1,9% | 7,9% | 1,84 | -19,6% | -12,2% |
| CDI | 40,0% | — | caixa | 13,65% | — | 0% | 0 | 0% | 0% |

Dimensionamento por Kelly (fração da carteira-alvo; exposição resultante em ações):

| Regime | Kelly cheio | Meio Kelly | Ações / capital |
|---|---:|---:|---:|
| analitico | 1,54 | 0,77 | 46% |
| normal_bootstrap | 1,21 | 0,60 | 36% |
| choque_3m | 0,75 | 0,38 | 23% |
| crise_ano | 0,54 | 0,27 | 16% |

Regra: começar no meio Kelly do regime de choque e subir até o meio Kelly normal/analítico (teto = parcela investida da carteira-alvo) quando a vol. 21d do Ibovespa sair do decil superior.

## Carteiras testadas

`op7_b3` = 5 oportunidades com setor B3 ≤ 40% (máximo investível 60%, resto em CDI); `op7_sub` = 5 oportunidades com subsetor B3 ≤ 40% (incorporação ≤ 40%, 100% investido); `u59` = universo de 59 com setor B3 ≤ 40%.

| Carteira | Pesos (% do capital) |
|---|---|
| op7_b3_ew | BEEF3 20 · COGN3 10 · MDNE3 10 · PLPL3 10 · TEND3 10 + CDI 40 |
| op7_b3_iv | BEEF3 20 · MDNE3 11 · TEND3 10 · PLPL3 10 · COGN3 10 + CDI 40 |
| op7_b3_rp | BEEF3 20 · MDNE3 10 · TEND3 10 · COGN3 10 · PLPL3 10 + CDI 40 |
| op7_b3_mv | BEEF3 20 · MDNE3 13 · COGN3 10 · TEND3 9 · PLPL3 8 + CDI 40 |
| op7_b3_ms_tir | BEEF3 20 · MDNE3 16 · PLPL3 13 · TEND3 11 · COGN3 0 + CDI 40 |
| op7_b3_ms_up | TEND3 20 · BEEF3 20 · PLPL3 18 · MDNE3 2 + CDI 40 |
| op7_sub_ew | COGN3 20 · BEEF3 20 · TEND3 13 · MDNE3 13 · PLPL3 13 + CDI 20 |
| op7_sub_iv | COGN3 20 · BEEF3 20 · MDNE3 14 · TEND3 13 · PLPL3 13 + CDI 20 |
| op7_sub_rp | BEEF3 20 · COGN3 20 · MDNE3 14 · TEND3 13 · PLPL3 13 + CDI 20 |
| op7_sub_mv | COGN3 20 · BEEF3 20 · MDNE3 18 · TEND3 12 · PLPL3 10 + CDI 20 |
| op7_sub_ms_tir | COGN3 20 · BEEF3 20 · MDNE3 16 · PLPL3 13 · TEND3 10 + CDI 20 |
| op7_sub_ms_up | TEND3 20 · COGN3 20 · BEEF3 20 · PLPL3 20 + CDI 20 |
| u59_ew | TTEN3 2 · SIMH3 2 · ECOR3 2 · MOTV3 2 · RAIL3 2 · CSAN3 2 · VBBR3 2 · NATU3 2 … (+51) |
| u59_iv | ALUP11 3 · CPLE3 3 · ALOS3 3 · EQTL3 3 · MULT3 2 · SBSP3 2 · BBAS3 2 · MOTV3 2 … (+51) |
| u59_rp | ALUP11 3 · BBAS3 3 · CPLE3 3 · BRSR6 3 · VBBR3 2 · SBSP3 2 · AURE3 2 · HYPE3 2 … (+51) |
| u59_mv | ALUP11 20 · BBAS3 16 · CPLE3 14 · VBBR3 11 · BRSR6 10 · SBSP3 6 · HYPE3 4 · ALOS3 4 … (+7) |
| u59_ms_tir | BBAS3 20 · BEEF3 20 · HAPV3 16 · PLPL3 14 · MDNE3 14 · TEND3 9 · BRSR6 4 · DIRR3 3 |
| u59_ms_up | PLPL3 20 · TEND3 20 · BEEF3 20 · BBAS3 20 · HAPV3 20 |
| rec_op7_core | BEEF3 20 · MDNE3 13 · PLPL3 11 · TEND3 10 · COGN3 5 + CDI 40 |
| alt_u59_halfkelly | BBAS3 11 · BEEF3 11 · HAPV3 9 · PLPL3 8 · MDNE3 8 · TEND3 5 · BRSR6 2 · DIRR3 2 + CDI 43 |

| Carteira | Invest. | Nomes | Vol | Beta | Beta baixa | E[exc.] TIR | Sharpe TIR | Sharpe upside | VaR95 1m normal | VaR95 1m crise | CVaR95 1m hist. | CVaR95 1m crise | N efetivo | Máx. contrib. risco |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | 60% | 5 | 20,4% | 0,88 | 0,96 | 6,3% | 0,31 | 0,22 | 8,0% | 25,9% | 12,2% | 31,4% | 4,5 | 31% |
| op7_b3_iv | 60% | 5 | 20,4% | 0,88 | 0,96 | 6,3% | 0,31 | 0,22 | 8,0% | 26,0% | 12,2% | 31,5% | 4,5 | 31% |
| op7_b3_rp | 60% | 5 | 20,4% | 0,88 | 0,96 | 6,3% | 0,31 | 0,22 | 8,0% | 25,9% | 12,2% | 31,4% | 4,5 | 31% |
| op7_b3_mv | 60% | 5 | 20,3% | 0,88 | 0,96 | 6,3% | 0,31 | 0,21 | 8,0% | 26,6% | 12,3% | 32,1% | 4,4 | 31% |
| op7_b3_ms_tir | 60% | 5 | 20,8% | 0,86 | 0,96 | 6,6% | 0,32 | 0,23 | 8,2% | 27,0% | 12,2% | 32,1% | 3,8 | 30% |
| op7_b3_ms_up | 60% | 4 | 21,8% | 0,85 | 0,95 | 6,6% | 0,30 | 0,25 | 8,6% | 24,5% | 12,1% | 29,8% | 3,2 | 37% |
| op7_sub_ew | 80% | 5 | 27,7% | 1,23 | 1,33 | 8,2% | 0,30 | 0,17 | 11,3% | 35,2% | 17,0% | 41,9% | 4,8 | 28% |
| op7_sub_iv | 80% | 5 | 27,7% | 1,23 | 1,33 | 8,2% | 0,30 | 0,17 | 11,3% | 35,4% | 17,1% | 42,1% | 4,8 | 29% |
| op7_sub_rp | 80% | 5 | 27,7% | 1,23 | 1,33 | 8,2% | 0,30 | 0,17 | 11,3% | 35,3% | 17,0% | 42,0% | 4,8 | 28% |
| op7_sub_mv | 80% | 5 | 27,6% | 1,24 | 1,33 | 8,2% | 0,30 | 0,17 | 11,3% | 36,1% | 17,2% | 42,9% | 4,7 | 29% |
| op7_sub_ms_tir | 80% | 5 | 27,7% | 1,23 | 1,33 | 8,2% | 0,30 | 0,17 | 11,3% | 35,8% | 17,2% | 42,5% | 4,7 | 29% |
| op7_sub_ms_up | 80% | 4 | 28,6% | 1,22 | 1,31 | 8,2% | 0,29 | 0,19 | 11,7% | 32,7% | 16,8% | 39,6% | 4,0 | 28% |
| u59_ew | 100% | 59 | 26,9% | 1,48 | 1,45 | 1,3% | 0,05 | -0,73 | 11,5% | 35,2% | 17,6% | 43,3% | 58,9 | 3% |
| u59_iv | 100% | 59 | 24,9% | 1,38 | 1,38 | 0,7% | 0,03 | -0,84 | 10,6% | 35,0% | 16,6% | 42,0% | 54,3 | 2% |
| u59_rp | 100% | 59 | 24,7% | 1,37 | 1,36 | 0,8% | 0,03 | -0,84 | 10,5% | 34,8% | 16,4% | 41,6% | 54,1 | 2% |
| u59_mv | 100% | 15 | 17,9% | 0,98 | 1,05 | -0,6% | -0,03 | -1,43 | 7,4% | 30,8% | 13,8% | 37,2% | 8,4 | 17% |
| u59_ms_tir | 100% | 8 | 29,5% | 1,39 | 1,43 | 10,0% | 0,34 | 0,11 | 12,0% | 37,9% | 18,5% | 44,5% | 6,5 | 22% |
| u59_ms_up | 100% | 5 | 31,7% | 1,43 | 1,43 | 10,5% | 0,33 | 0,14 | 13,0% | 36,2% | 18,6% | 42,3% | 5,0 | 27% |
| rec_op7_core | 60% | 5 | 20,5% | 0,87 | 0,96 | 6,4% | 0,31 | 0,22 | 8,0% | 26,4% | 12,1% | 31,6% | 4,3 | 31% |
| alt_u59_halfkelly | 57% | 8 | 16,9% | 0,80 | 0,82 | 5,7% | 0,34 | 0,11 | 6,4% | 22,8% | 10,5% | 27,2% | 6,5 | 22% |

Exposição setorial (setor B3, % do capital):

| Carteira | Setores |
|---|---|
| op7_b3_ew | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_iv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_rp | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_mv | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_ms_tir | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_b3_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| op7_sub_ew | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| op7_sub_iv | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| op7_sub_rp | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| op7_sub_mv | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| op7_sub_ms_tir | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| op7_sub_ms_up | Consumo Cíclico 60 · Consumo não Cíclico 20 |
| u59_ew | Consumo Cíclico 40 · Financeiro 16 · Utilidade Pública 12 · Consumo não Cíclico 9 · Saúde 9 · Bens Industriais 7 · Petróleo. Gás e Biocombustíveis 4 · Tecnologia da Informação 4 |
| u59_iv | Consumo Cíclico 34 · Financeiro 19 · Utilidade Pública 17 · Saúde 8 · Bens Industriais 8 · Consumo não Cíclico 7 · Petróleo. Gás e Biocombustíveis 4 · Tecnologia da Informação 3 |
| u59_rp | Consumo Cíclico 33 · Financeiro 18 · Utilidade Pública 17 · Consumo não Cíclico 9 · Saúde 9 · Bens Industriais 7 · Tecnologia da Informação 4 · Petróleo. Gás e Biocombustíveis 4 |
| u59_mv | Utilidade Pública 40 · Financeiro 32 · Petróleo. Gás e Biocombustíveis 11 · Saúde 6 · Tecnologia da Informação 4 · Consumo Cíclico 4 · Consumo não Cíclico 3 · Bens Industriais 1 |
| u59_ms_tir | Consumo Cíclico 40 · Financeiro 24 · Consumo não Cíclico 20 · Saúde 16 |
| u59_ms_up | Consumo Cíclico 40 · Consumo não Cíclico 20 · Financeiro 20 · Saúde 20 |
| rec_op7_core | Consumo Cíclico 40 · Consumo não Cíclico 20 |
| alt_u59_halfkelly | Consumo Cíclico 23 · Financeiro 14 · Consumo não Cíclico 11 · Saúde 9 |

## Estresses (choque instantâneo, % do capital)

| Carteira | Ibov −20% (beta baixa) | Ibov −20% (reação de hoje) | DI +300 bp | Dólar +20% puro | Dólar +20% c/ co-mov. | Ibov +30% (beta alta) |
|---|---:|---:|---:|---:|---:|---:|
| op7_b3_ew | -19,2% | -22,7% | -10,9% | -5,5% | -19,9% | 25,9% |
| op7_b3_iv | -19,2% | -22,7% | -10,9% | -5,5% | -19,9% | 25,9% |
| op7_b3_rp | -19,2% | -22,7% | -10,9% | -5,5% | -19,9% | 25,9% |
| op7_b3_mv | -19,3% | -22,9% | -10,8% | -5,5% | -20,1% | 25,8% |
| op7_b3_ms_tir | -19,2% | -22,5% | -10,3% | -5,7% | -19,4% | 25,4% |
| op7_b3_ms_up | -19,0% | -20,5% | -10,7% | -5,8% | -18,2% | 24,7% |
| op7_sub_ew | -26,5% | -31,6% | -14,3% | -8,2% | -28,0% | 36,0% |
| op7_sub_iv | -26,6% | -31,7% | -14,3% | -8,2% | -28,1% | 36,0% |
| op7_sub_rp | -26,5% | -31,6% | -14,3% | -8,2% | -28,0% | 36,0% |
| op7_sub_mv | -26,7% | -31,9% | -14,2% | -8,2% | -28,3% | 35,9% |
| op7_sub_ms_tir | -26,5% | -32,1% | -14,2% | -8,2% | -28,3% | 36,3% |
| op7_sub_ms_up | -26,3% | -30,1% | -14,6% | -8,2% | -27,1% | 35,7% |
| u59_ew | -29,1% | -42,7% | -24,3% | -10,6% | -34,5% | 45,1% |
| u59_iv | -27,6% | -39,8% | -23,9% | -10,0% | -32,4% | 42,0% |
| u59_rp | -27,3% | -39,2% | -23,9% | -9,8% | -31,9% | 41,3% |
| u59_mv | -20,9% | -26,4% | -21,7% | -3,9% | -21,4% | 28,0% |
| u59_ms_tir | -28,6% | -40,6% | -19,0% | -6,6% | -29,2% | 42,3% |
| u59_ms_up | -28,7% | -40,2% | -19,5% | -6,6% | -28,3% | 43,3% |
| rec_op7_core | -19,2% | -22,6% | -10,6% | -5,6% | -19,7% | 25,6% |
| alt_u59_halfkelly | -16,4% | -23,3% | -10,9% | -3,8% | -16,7% | 24,3% |
| Ibovespa (referência) | −20,0% | −20,0% | — | — | -18,3% | +30,0% |

A coluna "reação de hoje" usa a razão entre a queda de cada ação e a do Ibovespa em 26/10. Como o universo foi escolhido justamente por ter caído ≥ 20%, essa razão superestima o beta. Ainda assim, ela mostra que em choques políticos os nomes domésticos se movem perto do dobro do índice.

## Monte Carlo de 1 ano (bootstrap estacionário, 10 mil trajetórias)

Regimes: `normal_hist` = dias de 2016–2026 com a média histórica; `normal_tir` = mesmos dias com a média de cada ação trocada pela TIR de dono; `choque_tir` = 3 meses sorteados dos dias de crise e 9 meses normais; `crise_tir` = o ano todo em dias de crise (vol 21d do Ibovespa ≥ 28,1%: 267 dias, em 2016, 2017, 2018, 2020, 2021, 2022 e out/2026); `crise_hist` = dias de crise com a média que tiveram.

| Carteira | Regime | Média | p5 | p25 | p50 | p75 | p95 | P(perda) | P(< CDI) | DD mediano | P(DD > 25%) | Kelly cheio |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rec_op7_core | normal_hist | 20,7% | -17,9% | 3,1% | 18,8% | 36,0% | 65,6% | 21% | 41% | -14,6% | 14% | 1,26 |
| rec_op7_core | normal_tir | 20,4% | -18,2% | 2,9% | 18,5% | 35,6% | 65,1% | 21% | 42% | -14,7% | 14% | 1,21 |
| rec_op7_core | choque_tir | 21,4% | -32,1% | -2,3% | 20,1% | 43,1% | 80,0% | 27% | 42% | -18,6% | 36% | 0,75 |
| rec_op7_core | crise_tir | 27,4% | -53,4% | -14,1% | 20,0% | 61,5% | 129,9% | 35% | 46% | -38,6% | 72% | 0,54 |
| rec_op7_core | crise_hist | 25,5% | -54,1% | -15,4% | 18,3% | 59,2% | 126,5% | 36% | 47% | -38,7% | 72% | 0,48 |
| alt_u59_halfkelly | normal_hist | 18,2% | -14,6% | 2,9% | 16,5% | 31,4% | 57,1% | 20% | 45% | -12,8% | 10% | 1,10 |
| alt_u59_halfkelly | normal_tir | 19,5% | -13,6% | 4,1% | 17,8% | 32,9% | 58,9% | 19% | 42% | -12,5% | 9% | 1,39 |
| alt_u59_halfkelly | choque_tir | 20,2% | -26,8% | -0,5% | 18,7% | 38,6% | 71,5% | 26% | 43% | -16,3% | 31% | 0,81 |
| alt_u59_halfkelly | crise_tir | 24,7% | -47,5% | -10,7% | 18,1% | 52,2% | 111,6% | 34% | 46% | -33,6% | 68% | 0,53 |
| alt_u59_halfkelly | crise_hist | 25,0% | -47,4% | -10,5% | 18,4% | 52,5% | 112,1% | 34% | 46% | -33,6% | 68% | 0,54 |
| op7_b3_ms_tir | normal_hist | 22,3% | -17,4% | 4,5% | 20,3% | 38,0% | 68,5% | 19% | 39% | -14,6% | 14% | 1,41 |
| op7_b3_ms_tir | normal_tir | 20,4% | -18,6% | 2,9% | 18,5% | 36,0% | 66,0% | 21% | 42% | -15,0% | 14% | 1,20 |
| op7_b3_ms_tir | choque_tir | 21,6% | -33,3% | -2,5% | 20,4% | 43,6% | 81,4% | 27% | 42% | -18,9% | 37% | 0,74 |
| op7_b3_ms_tir | crise_tir | 28,3% | -55,1% | -14,8% | 20,6% | 63,5% | 134,8% | 35% | 45% | -39,0% | 73% | 0,54 |
| op7_b3_ms_tir | crise_hist | 20,8% | -57,7% | -19,8% | 13,5% | 53,9% | 121,0% | 40% | 50% | -39,3% | 73% | 0,28 |
| op7_sub_ms_tir | normal_hist | 21,7% | -31,3% | -3,9% | 17,1% | 42,8% | 89,4% | 30% | 46% | -21,5% | 36% | 0,75 |
| op7_sub_ms_tir | normal_tir | 22,7% | -30,7% | -3,1% | 18,1% | 44,0% | 90,9% | 29% | 45% | -21,3% | 35% | 0,82 |
| op7_sub_ms_tir | choque_tir | 24,8% | -46,8% | -11,3% | 19,8% | 53,8% | 115,3% | 34% | 45% | -26,3% | 54% | 0,56 |
| op7_sub_ms_tir | crise_tir | 36,3% | -68,6% | -27,3% | 15,9% | 79,4% | 200,4% | 41% | 49% | -50,3% | 80% | 0,44 |
| op7_sub_ms_tir | crise_hist | 43,3% | -66,9% | -23,5% | 21,8% | 88,6% | 215,8% | 39% | 46% | -49,7% | 80% | 0,55 |
| u59_ms_tir | normal_hist | 21,9% | -33,4% | -6,5% | 16,5% | 43,8% | 96,3% | 32% | 47% | -23,7% | 45% | 0,66 |
| u59_ms_tir | normal_tir | 24,3% | -32,0% | -4,7% | 18,8% | 46,7% | 100,2% | 30% | 45% | -23,1% | 43% | 0,83 |
| u59_ms_tir | choque_tir | 26,7% | -50,1% | -13,3% | 19,1% | 56,5% | 127,4% | 35% | 46% | -29,2% | 61% | 0,54 |
| u59_ms_tir | crise_tir | 41,4% | -73,3% | -31,8% | 13,0% | 79,1% | 219,1% | 43% | 50% | -53,1% | 84% | 0,39 |
| u59_ms_tir | crise_hist | 42,0% | -73,2% | -31,5% | 13,5% | 79,8% | 220,4% | 43% | 50% | -53,0% | 84% | 0,40 |
| u59_rp | normal_hist | 21,7% | -28,0% | -2,4% | 17,7% | 41,6% | 83,6% | 28% | 45% | -19,7% | 30% | 0,83 |
| u59_rp | normal_tir | 14,8% | -32,0% | -7,9% | 11,1% | 33,7% | 73,3% | 35% | 53% | -21,1% | 35% | 0,13 |
| u59_rp | choque_tir | 16,8% | -48,9% | -17,4% | 11,1% | 42,6% | 100,9% | 40% | 52% | -27,8% | 57% | 0,16 |
| u59_rp | crise_tir | 28,1% | -71,9% | -35,8% | 4,0% | 65,7% | 196,0% | 47% | 55% | -51,3% | 85% | 0,24 |
| u59_rp | crise_hist | 52,0% | -66,7% | -23,8% | 23,4% | 96,6% | 250,9% | 38% | 45% | -49,4% | 83% | 0,60 |
| u59_mv | normal_hist | 21,4% | -22,7% | 0,8% | 18,7% | 38,7% | 74,8% | 24% | 43% | -16,3% | 19% | 1,05 |
| u59_mv | normal_tir | 13,4% | -27,8% | -5,8% | 10,9% | 29,6% | 63,4% | 33% | 54% | -17,8% | 24% | 0,00 |
| u59_mv | choque_tir | 15,6% | -44,8% | -15,2% | 10,3% | 38,5% | 88,9% | 39% | 54% | -25,1% | 50% | 0,10 |
| u59_mv | crise_tir | 30,0% | -67,9% | -33,0% | 4,0% | 57,6% | 170,3% | 48% | 56% | -47,1% | 84% | 0,22 |
| u59_mv | crise_hist | 42,0% | -64,8% | -26,7% | 13,7% | 72,2% | 195,3% | 42% | 50% | -46,2% | 83% | 0,43 |

## Backtest ilustrativo: comprar no crash

Regra: tickers de data/market com histórico na data, ADTV 3m ≥ R$ 10 mi (viés de sobrevivência: lista atual). Retornos: retornos de preço + DY 12m na data × prazo (aprox.). Cestas com pesos iguais, compradas no fechamento do dia do choque. "Mais caídas" = terço com maior queda desde a data de referência; "mais baratas" = terço com maior L/P (P/L do fim do mês anterior levado ao preço do choque); "caídas e baratas" = quintil superior da soma dos dois rankings.

### 2017-05-18 — Joesley Day (delação JBS/Temer)

Universo de 53 ações. O Ibovespa caiu -8,8% entre 2017-05-17 e o fechamento do choque (-8,8% no dia) e depois subiu 11,4% em 3m, 19,2% em 6m e 28,1% em 12m.

| Cesta | N | Queda média | P/L mediano | 3m | 6m | 12m | Mediana 12m | Excesso 12m | % > Ibov 12m | DD máx. 12m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| todas | 53 | -9,5% | 15,1 | 15,7% | 21,8% | 29,1% | 16,9% | 1,0% | 40% | -11,3% |
| mais_caidas | 18 | -15,2% | 14,6 | 25,9% | 31,0% | 45,7% | 21,4% | 17,6% | 44% | -16,9% |
| menos_caidas | 18 | -3,4% | 17,2 | 11,4% | 18,3% | 19,3% | 14,3% | -8,8% | 33% | -8,1% |
| mais_baratas | 12 | -7,3% | 10,4 | 13,8% | 19,2% | 33,2% | 33,7% | 5,2% | 58% | -10,5% |
| caidas_e_baratas | 7 | -12,4% | 12,6 | 13,9% | 20,2% | 19,4% | 15,4% | -8,7% | 43% | -21,4% |

Correlação de ranking (Spearman) entre a queda e o retorno seguinte: 3m -0,32, 6m -0,10, 12m -0,18 (negativo = as mais caídas sobem mais). Entre o L/P e o retorno: 3m -0,06, 12m 0,21.

### 2020-03-16 — Covid-19 (circuit breakers de março)

Universo de 89 ações. O Ibovespa caiu -37,4% entre 2020-02-21 e o fechamento do choque (-13,9% no dia) e depois subiu 34,3% em 3m, 40,9% em 6m e 59,1% em 12m.

| Cesta | N | Queda média | P/L mediano | 3m | 6m | 12m | Mediana 12m | Excesso 12m | % > Ibov 12m | DD máx. 12m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| todas | 89 | -38,5% | 11,5 | 31,1% | 43,2% | 58,7% | 37,2% | -0,4% | 33% | -15,8% |
| mais_caidas | 30 | -50,6% | 10,3 | 44,5% | 65,4% | 91,8% | 64,0% | 32,6% | 53% | -17,5% |
| menos_caidas | 30 | -27,0% | 12,7 | 20,9% | 24,2% | 38,8% | 18,8% | -20,4% | 20% | -13,1% |
| mais_baratas | 21 | -37,8% | 7,8 | 29,5% | 34,2% | 66,4% | 46,5% | 7,3% | 38% | -17,6% |
| caidas_e_baratas | 13 | -50,3% | 6,8 | 40,5% | 44,9% | 93,2% | 50,7% | 34,0% | 46% | -19,3% |

Correlação de ranking (Spearman) entre a queda e o retorno seguinte: 3m -0,45, 6m -0,41, 12m -0,22 (negativo = as mais caídas sobem mais). Entre o L/P e o retorno: 3m -0,03, 12m 0,09.

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
| RENT3 | Consumo Cíclico | 40,8% | 1,73 | 1,58 | 1,93 | -39,5% | 1,0% | -20,6% | -31,5% | -23,4% | -1,1% | 7,5 | -0,84 | -16,7% |
| MOVI3 | Consumo Cíclico | 64,7% | 2,53 | 2,35 | 2,84 | -53,6% | 6,0% | -21,5% | -46,9% | -33,2% | -15,2% | 7,1 | -1,65 | -33,0% |
| VAMO3 | Consumo Cíclico | 59,1% | 2,31 | 1,71 | 2,73 | -54,8% | 1,6% | -30,9% | -34,2% | -34,0% | -10,4% | 8,8 | 0,29 | 5,8% |
| SIMH3 | Financeiro | 60,5% | 2,49 | 2,07 | 2,60 | -58,7% | — | -17,6% | -41,4% | -38,2% | -20,3% | 7,5 | -0,65 | -13,0% |
| ECOR3 | Bens Industriais | 48,2% | 2,12 | 2,34 | 2,23 | -58,6% | 3,6% | -26,7% | -46,8% | -23,1% | -0,3% | 7,6 | -0,86 | -17,2% |
| MOTV3 | Bens Industriais | 26,6% | 1,22 | 1,44 | 1,17 | -31,4% | -0,5% | -27,2% | -28,8% | -25,6% | -3,5% | 7,6 | -0,39 | -7,8% |
| RAIL3 | Bens Industriais | 31,2% | 1,16 | 0,99 | 1,22 | -18,0% | -4,1% | -31,6% | -19,8% | -24,8% | -2,6% | 7,6 | -0,25 | -5,0% |
| CSAN3 | Petróleo. Gás e Biocombustíveis | 44,6% | 1,97 | 1,75 | 2,18 | -42,9% | — | -10,9% | -34,9% | -24,8% | -3,1% | 7,5 | -0,54 | -10,9% |
| VBBR3 | Petróleo. Gás e Biocombustíveis | 29,0% | 1,02 | 1,14 | 0,74 | -9,8% | -3,6% | -40,5% | -22,9% | -23,9% | -2,0% | 7,4 | 0,00 | 0,0% |
| MGLU3 | Consumo Cíclico | 69,7% | 2,63 | 1,93 | 3,03 | -53,9% | -7,3% | -39,3% | -38,5% | -35,0% | -8,8% | 9,6 | -0,29 | -5,9% |
| SBFG3 | Consumo Cíclico | 51,3% | 2,00 | 1,85 | 2,20 | -48,2% | 7,3% | -15,7% | -37,1% | -20,8% | -3,9% | 5,9 | -0,65 | -13,0% |
| CEAB3 | Consumo Cíclico | 58,3% | 2,02 | 1,82 | 2,15 | -46,9% | 7,4% | -2,1% | -36,4% | -19,1% | -1,9% | 5,8 | -0,35 | -6,9% |
| LREN3 | Consumo Cíclico | 42,9% | 1,75 | 1,68 | 1,62 | -34,8% | 6,5% | -2,6% | -33,6% | -14,6% | 0,5% | 5,0 | -0,78 | -15,6% |
| AZZA3 | Consumo Cíclico | 48,4% | 1,57 | 1,59 | 1,52 | -35,3% | -1,0% | -25,2% | -31,8% | -29,2% | -3,9% | 8,8 | -0,95 | -19,1% |
| VIVA3 | Consumo Cíclico | 38,1% | 1,33 | 1,22 | 1,23 | -28,0% | 1,7% | -11,9% | -24,3% | -23,9% | -0,3% | 7,9 | -0,27 | -5,4% |
| VULC3 | Consumo Cíclico | 32,5% | 1,01 | 1,11 | 0,96 | -21,7% | 3,8% | -8,1% | -22,2% | -19,8% | -0,8% | 6,4 | -0,49 | -9,9% |
| ALPA4 | Consumo Cíclico | 40,3% | 1,22 | 1,36 | 0,75 | -23,3% | -2,4% | -20,5% | -27,2% | -23,5% | -0,3% | 7,8 | -0,46 | -9,1% |
| NATU3 | Consumo não Cíclico | 46,9% | 1,14 | 1,30 | 1,08 | -28,4% | -1,0% | -20,9% | -26,0% | -28,4% | -2,5% | 8,9 | -0,42 | -8,4% |
| ASAI3 | Consumo não Cíclico | 46,4% | 1,81 | 1,79 | 2,12 | -37,5% | -0,2% | -36,2% | -35,8% | -29,8% | -5,2% | 8,7 | -0,44 | -8,8% |
| GMAT3 | Consumo não Cíclico | 36,9% | 1,28 | 1,10 | 1,30 | -29,2% | -0,6% | -31,1% | -22,1% | -25,8% | -0,7% | 8,4 | -0,26 | -5,2% |
| PGMN3 | Saúde | 47,8% | 1,80 | 1,93 | 1,88 | -45,9% | 5,9% | -8,3% | -38,6% | -23,6% | -4,6% | 6,6 | -0,25 | -4,9% |
| RADL3 | Saúde | 36,5% | 1,13 | 1,08 | 1,06 | -25,6% | -1,6% | -24,8% | -21,6% | -25,6% | -0,5% | 8,4 | -0,36 | -7,2% |
| HYPE3 | Saúde | 32,9% | 1,02 | 0,97 | 0,89 | -25,8% | 0,3% | -19,0% | -19,5% | -23,9% | -2,0% | 7,4 | -0,46 | -9,1% |
| CYRE3 | Consumo Cíclico | 38,4% | 1,68 | 1,84 | 1,72 | -43,4% | 7,0% | -4,1% | -36,7% | -16,6% | -1,4% | 5,2 | -0,60 | -12,0% |
| EZTC3 | Consumo Cíclico | 41,7% | 1,56 | 1,69 | 1,69 | -37,7% | 1,0% | -4,1% | -33,9% | -19,7% | 1,2% | 6,9 | -0,46 | -9,3% |
| MDNE3 ★ | Consumo Cíclico | 45,7% | 1,69 | 1,92 | 1,60 | -35,1% | 10,9% | 0,9% | -38,3% | -12,8% | 0,6% | 4,4 | -0,74 | -14,9% |
| JHSF3 | Consumo Cíclico | 37,1% | 1,37 | 1,28 | 1,02 | -19,1% | -4,7% | -38,4% | -25,5% | -24,7% | -2,6% | 7,6 | -0,47 | -9,4% |
| MRVE3 | Consumo Cíclico | 50,8% | 1,83 | 1,85 | 1,90 | -39,5% | -1,8% | -22,3% | -37,1% | -33,8% | -10,4% | 8,7 | -0,73 | -14,5% |
| PLPL3 ★ | Consumo Cíclico | 50,6% | 1,60 | 1,72 | 1,82 | -32,6% | 11,5% | 3,8% | -34,5% | -15,4% | -1,0% | 4,8 | -0,74 | -14,8% |
| DIRR3 | Consumo Cíclico | 36,9% | 1,36 | 1,63 | 1,10 | -22,4% | 7,8% | -1,4% | -32,6% | -16,1% | -0,4% | 5,3 | -0,87 | -17,4% |
| CURY3 | Consumo Cíclico | 36,2% | 1,25 | 1,39 | 1,05 | -17,1% | 5,9% | -5,3% | -27,9% | -16,2% | 0,1% | 5,4 | -0,58 | -11,5% |
| TEND3 ★ | Consumo Cíclico | 50,3% | 1,60 | 1,90 | 1,24 | -21,1% | 10,8% | 6,2% | -38,0% | -15,3% | -1,0% | 4,8 | -0,78 | -15,5% |
| MULT3 | Financeiro | 26,0% | 1,20 | 1,30 | 1,17 | -25,5% | -0,0% | -19,0% | -26,0% | -24,8% | -1,7% | 7,8 | -0,51 | -10,1% |
| IGTI11 | Financeiro | 27,7% | 1,28 | 1,40 | 1,24 | -21,0% | -0,9% | -18,8% | -28,0% | -25,0% | -1,4% | 8,0 | -0,47 | -9,4% |
| ALOS3 | Financeiro | 24,5% | 1,17 | 1,30 | 1,11 | -23,5% | -1,7% | -21,4% | -25,9% | -21,1% | -1,5% | 6,6 | -0,50 | -10,1% |
| SMFT3 | Consumo Cíclico | 36,2% | 1,46 | 1,17 | 1,63 | -34,0% | -0,1% | -25,2% | -23,3% | -27,7% | -1,1% | 9,0 | -1,20 | -24,1% |
| CVCB3 | Consumo Cíclico | 65,9% | 1,81 | 1,85 | 1,85 | -31,8% | — | -50,9% | -36,9% | -35,9% | -17,3% | 7,5 | -1,57 | -31,5% |
| YDUQ3 | Consumo Cíclico | 50,6% | 1,73 | 1,60 | 1,55 | -39,6% | 6,4% | -5,8% | -32,0% | -23,9% | -7,0% | 6,1 | -1,10 | -22,1% |
| COGN3 ★ | Consumo Cíclico | 51,4% | 1,85 | 1,84 | 1,81 | -35,2% | 8,1% | -0,6% | -36,7% | -19,6% | -3,4% | 5,6 | -0,61 | -12,2% |
| ANIM3 | Consumo Cíclico | 68,6% | 2,48 | 2,67 | 2,46 | -45,6% | 7,7% | -2,6% | -53,3% | -33,3% | -15,4% | 7,0 | -1,14 | -22,8% |
| HAPV3 | Saúde | 61,1% | 1,84 | 1,29 | 1,96 | -43,4% | 12,9% | -1,2% | -25,8% | -24,9% | -9,2% | 5,8 | -0,21 | -4,2% |
| RDOR3 | Saúde | 31,7% | 1,26 | 1,08 | 1,27 | -20,1% | -1,6% | -26,9% | -21,7% | -25,8% | -1,5% | 8,2 | -0,27 | -5,3% |
| B3SA3 | Financeiro | 35,4% | 1,71 | 1,50 | 2,10 | -36,2% | -2,2% | -20,3% | -30,1% | -19,6% | 0,2% | 6,6 | -0,51 | -10,1% |
| BPAC11 | Financeiro | 32,9% | 1,57 | 1,63 | 1,72 | -30,7% | -0,4% | -18,8% | -32,6% | -26,2% | 0,0% | 8,7 | -0,74 | -14,8% |
| BBAS3 | Financeiro | 26,3% | 1,06 | 1,15 | 1,12 | -28,9% | 6,4% | -3,7% | -23,0% | -19,0% | 0,0% | 6,3 | 0,01 | 0,2% |
| BBDC4 | Financeiro | 28,9% | 1,27 | 1,19 | 1,49 | -24,1% | 4,2% | -7,2% | -23,7% | -19,0% | 0,0% | 6,3 | -0,24 | -4,8% |
| BRSR6 | Financeiro | 28,5% | 0,95 | 1,08 | 0,92 | -19,2% | 4,3% | -9,4% | -21,6% | -19,8% | 0,0% | 6,6 | -0,15 | -3,1% |
| AURE3 | Utilidade Pública | 29,7% | 1,08 | 1,14 | 1,17 | -32,5% | -6,8% | -46,7% | -22,7% | -28,3% | -2,1% | 8,9 | -0,15 | -3,0% |
| ENGI11 | Utilidade Pública | 27,2% | 1,32 | 1,19 | 1,45 | -29,1% | -5,6% | -40,6% | -23,7% | -28,5% | -7,1% | 7,7 | -0,64 | -12,8% |
| EQTL3 | Utilidade Pública | 25,0% | 1,18 | 1,10 | 1,28 | -26,6% | -6,5% | -47,6% | -21,9% | -26,9% | -2,9% | 8,2 | -0,63 | -12,5% |
| CPLE3 | Utilidade Pública | 23,3% | 0,98 | 1,08 | 0,85 | -12,5% | -5,3% | -43,1% | -21,6% | -20,5% | -1,1% | 6,5 | 0,01 | 0,3% |
| ALUP11 | Utilidade Pública | 20,6% | 0,78 | 0,81 | 0,84 | -19,1% | -2,9% | -33,4% | -16,2% | -21,6% | 0,3% | 7,3 | -0,34 | -6,8% |
| SBSP3 | Utilidade Pública | 26,2% | 1,07 | 1,14 | 1,13 | -19,3% | -5,4% | -40,8% | -22,8% | -26,3% | -1,5% | 8,4 | -0,24 | -4,8% |
| TOTS3 | Tecnologia da Informação | 33,9% | 0,98 | 0,98 | 0,75 | -16,0% | -2,5% | -23,7% | -19,7% | -24,6% | -0,5% | 8,0 | -0,39 | -7,8% |
| INTB3 | Tecnologia da Informação | 38,1% | 1,17 | 1,07 | 1,25 | -25,8% | -0,8% | -17,4% | -21,3% | -20,8% | 0,8% | 7,1 | -0,84 | -16,8% |
| GGPS3 | Bens Industriais | 32,3% | 1,26 | 1,19 | 1,54 | -27,1% | 0,9% | -14,7% | -23,8% | -25,8% | -1,0% | 8,3 | -0,72 | -14,4% |
| ORVR3 | Utilidade Pública | 28,7% | 1,08 | 1,28 | 1,17 | -25,2% | -4,1% | -29,7% | -25,6% | -27,7% | -0,7% | 9,1 | -0,72 | -14,3% |
| BEEF3 ★ | Consumo não Cíclico | 44,4% | 1,04 | 1,10 | 1,08 | -20,8% | 10,8% | 17,2% | -22,1% | -22,9% | -7,8% | 5,5 | 0,07 | 1,3% |
| TTEN3 | Consumo não Cíclico | 38,3% | 0,94 | 0,95 | 0,85 | -19,4% | -1,5% | -32,8% | -19,0% | -28,0% | -2,7% | 8,7 | -0,73 | -14,6% |

## Método e ressalvas

- Covariância: 2023-10-25 a 2026-10-23 (diário), 748 observações diárias, Ledoit-Wolf com alvo de correlação constante (intensidade 0,193, correlação média 0,444), anualizada × 252. Vol 3a do Ibovespa: 16,0%.
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
