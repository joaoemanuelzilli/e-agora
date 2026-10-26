# Backtest de fatores — ações brasileiras, painel mensal point-in-time 2017-01 a 2026-09

Gerado por `pipeline/tests/factor_backtest.py` em 2026-10-26T16:33:51. Dados completos (ICs mensais, spreads, séries dos compostos, bootstrap) em `data/tests/factor_backtest.json`. 117 meses de formação (2017-01 a 2026-09), média de 102 ações por mês (mín. 53, máx. 142). IC = correlação de Spearman entre o fator (orientado no sinal esperado) e o retorno total futuro; t com erros de Newey-West (defasagens = horizonte + 2).

## Conclusões

1. **Funcionaram (t ≥ 2 em algum horizonte e IC 12m positivo dentro e fora da amostra):** E/P (IC 12m 0.119, t 2.43); B/P (IC 12m 0.150, t 3.59); EBITDA/EV (IC 12m 0.108, t 2.26); Momentum 12-1 (IC 12m 0.073, t 1.95). O sinal mais robusto é **valor**: barato por lucro, patrimônio e EBITDA paga em todos os horizontes, cresce com o horizonte e se mantém em 2023–2026.
2. **Positivos mas fracos (IC > 0 em 3+ horizontes e t entre 1 e 2):** DY 12m (IC 1m 0.025, t 1.29); ROE (IC 1m 0.024, t 1.30); ROIC (IC 1m 0.022, t 1.09); Piotroski F (IC 1m 0.027, t 1.87); Dív. líq./EBITDA (IC 1m 0.027, t 1.81); Volatilidade 1a (IC 1m 0.039, t 1.59); Beta 2a (IC 1m 0.013, t 0.50).
3. **Sem efeito ou contrários:** Margem bruta (IC 1m 0.003, t 0.18); Altman Z″ (EM) (IC 1m 0.004, t 0.31); Tamanho (log mcap) (IC 1m -0.005, t -0.31).
4. **Proxies dos blocos sem histórico do painel não funcionaram em meses normais.** Upside até o múltiplo histórico da própria ação: IC 1m -0.023 (t -1.26), 6m -0.064 (t -2.68): ações baratas contra o próprio passado continuam caindo. Sobrerreação (comprar quem caiu mais que o beta prevê no mês): IC 1m -0.039 (t -3.13), 12m -0.057 (t -3.94). O retorno residual tem continuação, não reversão. Só nos meses de crise o sinal vira: IC 1m 0.042 em 9 meses, amostra pequena demais para concluir.
5. **Fora da amostra, pesos otimizados não batem regras simples.** O máximo IC-IR estimado em 2017–2022 (blocos) teve excesso sobre o universo de +10.8% a.a. dentro da amostra e +0.8% a.a. fora dela. Pesos iguais por bloco ficaram em +2.9% e os pesos atuais do painel renormalizados em +4.4% (IC 12m fora da amostra 0.121). A regra recomendada, estimada só com 2017–2022, entregou +4.6% (IC 1m 0.061, IC 12m 0.221). Com 46 meses fora da amostra, nenhuma dessas diferenças é estatisticamente distinguível. A escolha tem de ser por robustez, não pelo melhor número.
6. **Regime de crise** (formação após Ibovespa ≤ −10% em 3 meses; 9 meses: 2018-05, 2018-06, 2020-03, 2020-04, 2020-05, 2021-09, 2021-10, 2021-11, 2022-06; quatro episódios independentes). Valor (B/P, EBITDA/EV) e momentum ficam mais fortes. Baixo risco **inverte**: as ações de beta e volatilidade altas lideram a recuperação. IC 3m em crise: B/P 0.164; Momentum 12-1 0.137; EBITDA/EV 0.084; Piotroski F 0.078; ... Margem bruta -0.051; Volatilidade 1a -0.153; Beta 2a -0.201.

## Pesos recomendados

A regra dá a cada fator peso proporcional ao seu IC-IR positivo, na média dos horizontes de 1, 3 e 12 meses. Fatores de IC-IR médio ≤ 0 ficam com zero. São 13 candidatos: tamanho fica fora porque é o fator mais contaminado pelo viés de sobrevivência. A regra não inverte a covariância dos ICs nem usa corte duro. Fora da amostra, esquemas simples como este generalizaram tão bem ou melhor que o máximo IC-IR, que concentrou peso em momentum e perdeu força em 2023–2026. Os números são medianas de 1000 reamostragens em blocos de 12 meses da amostra inteira (93 meses com os três horizontes). O intervalo é o de 90% (p5–p95), e o peso recomendado é a mediana normalizada e arredondada para 5%. A mesma regra estimada só com 2017–2022 está na tabela de compostos, com o resultado fora da amostra.

| Bloco | Peso recomendado | Mediana bootstrap | IC 90% | P(peso > 1%) | Estimativa pontual |
|---|---:|---:|---:|---:|---:|
| Valor | **38%** | 38% | 22% – 54% | 1.00 | 39% |
| Qualidade | **19%** | 21% | 5% – 32% | 0.98 | 21% |
| Solidez | **14%** | 12% | 5% – 19% | 0.99 | 13% |
| Momentum 12-1 | **10%** | 9% | 6% – 22% | 1.00 | 10% |
| Baixo risco | **19%** | 18% | 12% – 27% | 1.00 | 18% |

Por fator (mediana [p5–p95], P(peso > 1%)): E/P 11% [5%–14%], 0.98; B/P 11% [6%–24%], 1.00; EBITDA/EV 9% [4%–15%], 0.99; DY 12m 7% [0%–11%], 0.85; ROE 6% [0%–9%], 0.90; ROIC 7% [1%–10%], 0.95; Margem bruta 0% [0%–9%], 0.43; Piotroski F 7% [0%–11%], 0.91; Altman Z″ (EM) 3% [0%–7%], 0.71; Dív. líq./EBITDA 9% [5%–14%], 0.99; Momentum 12-1 9% [6%–22%], 1.00; Volatilidade 1a 11% [8%–14%], 1.00; Beta 2a 7% [3%–15%], 0.98. Os demais ficam com peso zero na maioria das reamostragens.

Tradução para o painel (hoje valor 30%, qualidade 20%, solidez 15%, upside 10%, sobrerreação 10%, probabilidade 15%):

- **Valor** deve ser o maior bloco: 38% recomendado, intervalo 22%–54%. Upside (DCF) e probabilidade (Monte Carlo) derivam do mesmo valor justo e, na prática, são valor de novo. Sem histórico para testá-los, o prudente é tratá-los como parte do bloco valor, sem somar peso.
- **Qualidade** 19% e **solidez** 14%. Os sinais que sobrevivem são ROE, Piotroski e dívida líquida/EBITDA, todos fracos (t de 1 a 2). Margem bruta e Altman Z″ têm IC ≈ 0 e podem sair dos blocos.
- **Momentum** 10% e **baixo risco** 19% não existem no painel e entram pela evidência. O momentum perdeu força fora da amostra no horizonte de 1m, mas segue positivo em 12m. Os dois estão inflados pelo viés de sobrevivência, e baixo risco inverte em crises.
- **Sobrerreação**: o proxy mensal tem IC negativo significativo, e com os proxies no otimizador o bootstrap dá peso mediano 0% a ela e 0% ao upside histórico. A recomendação é 0% a 5% fora de crises.
- **Em crise**, os pesos de referência (IC-IR 3m nos 9 meses de crise, blocos) são valor 31%, qualidade 0%, solidez 11%, momentum 47%, baixo risco 0%, tamanho 11%. Indicam mais valor e momentum e zero em baixo risco, mas vêm de quatro episódios e não servem como estimativa.

## IC por fator e horizonte (amostra inteira)

IC médio, com o t de Newey-West entre parênteses. IC-IR = média/dp do IC mensal. Q5−Q1 = carteira long-short mensal, igualmente ponderada, do quintil mais atrativo menos o menos atrativo (retorno total, anualizado ×12).

| Fator (sinal) | 1m | 3m | 6m | 12m | IC-IR 1m | % meses IC>0 (1m) | Q5−Q1 a.a. | Sharpe Q5−Q1 | Q5−Q1 12m a.a. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E/P (+) | 0.037 (2.0) | 0.067 (2.2) | 0.079 (1.9) | 0.119 (2.4) | 0.22 | 61% | +11.3% | 0.59 | +8.9% |
| B/P (+) | 0.028 (1.6) | 0.043 (1.6) | 0.082 (2.5) | 0.150 (3.6) | 0.16 | 56% | +13.6% | 0.74 | +16.0% |
| EBITDA/EV (+) | 0.029 (1.6) | 0.050 (2.0) | 0.064 (1.9) | 0.108 (2.3) | 0.16 | 55% | +17.0% | 0.84 | +10.6% |
| DY 12m (+) | 0.025 (1.3) | 0.037 (1.2) | 0.039 (0.8) | 0.061 (1.0) | 0.15 | 55% | +3.0% | 0.16 | -0.4% |
| ROE (+) | 0.024 (1.3) | 0.038 (1.6) | 0.032 (1.0) | 0.017 (0.4) | 0.13 | 57% | +5.9% | 0.29 | +0.8% |
| ROIC (+) | 0.022 (1.1) | 0.040 (1.4) | 0.028 (0.8) | 0.013 (0.3) | 0.12 | 56% | +5.3% | 0.25 | +2.9% |
| Margem bruta (+) | 0.003 (0.2) | -0.005 (-0.3) | -0.014 (-0.5) | -0.027 (-0.7) | 0.02 | 52% | -2.8% | -0.19 | -5.8% |
| Piotroski F (+) | 0.027 (1.9) | 0.036 (1.7) | 0.038 (1.2) | 0.046 (0.9) | 0.18 | 58% | +7.9% | 0.53 | +4.8% |
| Altman Z″ (EM) (+) | 0.004 (0.3) | 0.006 (0.3) | 0.005 (0.2) | -0.015 (-0.3) | 0.03 | 50% | -6.0% | -0.38 | -7.6% |
| Dív. líq./EBITDA (−) | 0.027 (1.8) | 0.042 (1.9) | 0.044 (1.4) | 0.043 (1.2) | 0.18 | 56% | +7.3% | 0.48 | +5.5% |
| Momentum 12-1 (+) | 0.037 (2.0) | 0.060 (2.5) | 0.085 (3.2) | 0.073 (1.9) | 0.17 | 59% | +7.8% | 0.35 | +6.7% |
| Volatilidade 1a (−) | 0.039 (1.6) | 0.071 (2.2) | 0.081 (1.7) | 0.081 (1.3) | 0.15 | 57% | -0.2% | -0.01 | -1.6% |
| Beta 2a (−) | 0.013 (0.5) | 0.037 (1.0) | 0.039 (0.8) | 0.037 (0.6) | 0.05 | 50% | -5.1% | -0.19 | -1.2% |
| Tamanho (log mcap) (−) | -0.005 (-0.3) | -0.012 (-0.5) | -0.008 (-0.3) | 0.002 (0.1) | -0.03 | 49% | +8.9% | 0.47 | +7.2% |
| Upside p/ múltiplo histórico (proxy) (+) | -0.023 (-1.3) | -0.042 (-1.7) | -0.064 (-2.7) | -0.049 (-2.3) | -0.13 | 49% | -3.0% | -0.15 | -7.0% |
| Reversão 1m residual (proxy sobrerreação) (+) | -0.039 (-3.1) | -0.036 (-2.6) | -0.051 (-3.3) | -0.057 (-3.9) | -0.27 | 38% | -12.2% | -0.82 | -6.5% |
| ln(1+upside hist)/vol (proxy probabilidade) (+) | -0.019 (-1.1) | -0.033 (-1.4) | -0.052 (-2.3) | -0.030 (-1.6) | -0.12 | 50% | -3.9% | -0.24 | -6.6% |

## Estabilidade: dentro × fora da amostra e crise × normal

| Fator | IC 1m 2017–22 | IC 1m 2023–26 | IC 12m 2017–22 | IC 12m 2023–26 | IC 3m crise | IC 3m normal | % crise IC>0 (3m) |
|---|---:|---:|---:|---:|---:|---:|---:|
| E/P | 0.020 | 0.064 | 0.067 | 0.181 | 0.035 | 0.069 | 44% |
| B/P | 0.024 | 0.036 | 0.168 | 0.108 | 0.164 | 0.033 | 89% |
| EBITDA/EV | 0.036 | 0.019 | 0.104 | 0.086 | 0.084 | 0.047 | 67% |
| DY 12m | 0.010 | 0.048 | -0.008 | 0.132 | 0.034 | 0.038 | 44% |
| ROE | 0.016 | 0.037 | -0.033 | 0.086 | -0.045 | 0.045 | 33% |
| ROIC | 0.024 | 0.018 | -0.040 | 0.061 | -0.032 | 0.046 | 33% |
| Margem bruta | -0.010 | 0.022 | -0.068 | 0.064 | -0.051 | -0.002 | 22% |
| Piotroski F | 0.020 | 0.036 | -0.044 | 0.132 | 0.078 | 0.032 | 89% |
| Altman Z″ (EM) | 0.000 | 0.010 | -0.088 | 0.057 | 0.039 | 0.003 | 56% |
| Dív. líq./EBITDA | 0.029 | 0.023 | -0.014 | 0.112 | 0.031 | 0.043 | 67% |
| Momentum 12-1 | 0.057 | 0.006 | 0.025 | 0.112 | 0.137 | 0.054 | 78% |
| Volatilidade 1a | 0.025 | 0.060 | -0.011 | 0.197 | -0.153 | 0.091 | 33% |
| Beta 2a | 0.005 | 0.025 | -0.012 | 0.106 | -0.201 | 0.057 | 33% |
| Tamanho (log mcap) | -0.003 | -0.009 | 0.022 | -0.030 | 0.033 | -0.016 | 56% |
| Upside p/ múltiplo histórico (proxy) | -0.040 | -0.002 | -0.016 | -0.076 | -0.024 | -0.044 | 56% |
| Reversão 1m residual (proxy sobrerreação) | -0.046 | -0.029 | -0.067 | -0.038 | -0.011 | -0.038 | 56% |

## Decaimento do sinal

IC médio entre o fator em t e o retorno do mês t+k → t+k+1. Mede por quanto tempo uma leitura do fator continua informativa.

| Fator | k=0 | k=1 | k=2 | k=3 | k=6 | k=9 | k=11 |
|---|---:|---:|---:|---:|---:|---:|---:|
| E/P | 0.037 | 0.036 | 0.030 | 0.024 | 0.035 | 0.037 | 0.051 |
| B/P | 0.028 | 0.026 | 0.031 | 0.036 | 0.042 | 0.046 | 0.049 |
| EBITDA/EV | 0.029 | 0.029 | 0.020 | 0.011 | 0.024 | 0.025 | 0.033 |
| DY 12m | 0.025 | 0.022 | 0.016 | 0.012 | 0.016 | 0.015 | 0.021 |
| ROE | 0.024 | 0.020 | 0.011 | 0.005 | 0.007 | 0.002 | 0.015 |
| ROIC | 0.022 | 0.021 | 0.010 | -0.002 | -0.001 | -0.004 | 0.001 |
| Margem bruta | 0.003 | 0.003 | -0.005 | -0.011 | -0.009 | -0.011 | -0.013 |
| Piotroski F | 0.027 | 0.019 | 0.005 | 0.007 | 0.017 | 0.012 | 0.008 |
| Altman Z″ (EM) | 0.004 | 0.001 | 0.001 | -0.004 | 0.001 | -0.010 | -0.013 |
| Dív. líq./EBITDA | 0.027 | 0.028 | 0.018 | 0.012 | 0.017 | 0.004 | 0.003 |
| Momentum 12-1 | 0.037 | 0.031 | 0.039 | 0.046 | 0.022 | 0.001 | 0.012 |
| Volatilidade 1a | 0.039 | 0.043 | 0.038 | 0.035 | 0.032 | 0.037 | 0.033 |
| Beta 2a | 0.013 | 0.015 | 0.012 | 0.008 | 0.010 | 0.015 | 0.014 |
| Tamanho (log mcap) | -0.005 | -0.003 | -0.001 | -0.002 | -0.002 | -0.004 | -0.006 |
| Upside p/ múltiplo histórico (proxy) | -0.023 | -0.022 | -0.025 | -0.029 | -0.016 | -0.010 | 0.012 |
| Reversão 1m residual (proxy sobrerreação) | -0.039 | -0.019 | -0.006 | 0.002 | -0.034 | -0.054 | 0.038 |

## Compostos: dentro (2017–2022) e fora da amostra (2023–2026)

Carteira = quintil superior do escore, igualmente ponderada, rebalanceamento mensal, retorno total, sem custos. Sharpe do quintil superior sobre o CDI; Sharpe da long-short sem taxa livre. Excesso = quintil superior menos a média igualmente ponderada do universo (t Newey-West). No mesmo período, o universo igualmente ponderado rendeu 13.9% a.a. em 2017–2022 e 16.5% a.a. em 2023–2026. O Ibovespa (sem proventos) rendeu 9.3% e 17.7%.

| Composto | Período | Q5 a.a. | Vol | Sharpe | Máx. DD | Excesso a.a. (t) | L/S a.a. | Sharpe L/S | IC 1m (t) | IC 12m | Giro/mês |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | 2017–22 | 18.5% | 25% | 0.63 | -38% | +3.9% (1.0) | +3.3% | 0.26 | -0.001 (-0.0) | -0.017 | 28% |
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | 2023–26 | 16.7% | 21% | 0.45 | -20% | -0.1% (-0.0) | +3.2% | 0.35 | 0.029 (1.6) | 0.078 | 28% |
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | crise | 61.6% | 29% | 1.69 | -10% | +4.6% (0.4) | +16.8% | 1.06 | 0.034 (0.5) | 0.021 | 28% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | 2017–22 | 22.5% | 25% | 0.77 | -37% | +7.0% (1.6) | +12.2% | 0.70 | 0.012 (0.5) | -0.007 | 18% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | 2023–26 | 22.2% | 20% | 0.69 | -13% | +4.4% (1.1) | +8.7% | 0.71 | 0.040 (2.0) | 0.121 | 18% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | crise | 73.4% | 28% | 2.04 | -8% | +11.6% (0.8) | +17.0% | 1.09 | 0.020 (0.3) | 0.037 | 18% |
| Pesos iguais (14 fatores) | 2017–22 | 18.1% | 23% | 0.66 | -36% | +2.8% (0.7) | +11.0% | 0.65 | 0.034 (1.3) | 0.017 | 14% |
| Pesos iguais (14 fatores) | 2023–26 | 21.0% | 19% | 0.69 | -14% | +3.1% (0.7) | +3.1% | 0.25 | 0.059 (2.2) | 0.203 | 14% |
| Pesos iguais (14 fatores) | crise | 53.5% | 25% | 1.69 | -9% | -1.6% (-0.2) | +2.3% | 0.21 | 0.006 (0.1) | 0.047 | 14% |
| Pesos iguais (6 blocos) | 2017–22 | 19.6% | 24% | 0.70 | -38% | +4.4% (1.2) | +11.8% | 0.70 | 0.040 (1.7) | 0.029 | 16% |
| Pesos iguais (6 blocos) | 2023–26 | 20.6% | 19% | 0.65 | -15% | +2.9% (0.8) | +1.7% | 0.19 | 0.048 (1.9) | 0.184 | 16% |
| Pesos iguais (6 blocos) | crise | 63.0% | 28% | 1.77 | -9% | +5.2% (0.4) | +6.6% | 0.41 | 0.009 (0.1) | 0.051 | 16% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | 2017–22 | 25.8% | 25% | 0.89 | -39% | +9.8% (2.3) | +22.4% | 1.18 | 0.054 (2.2) | 0.060 | 19% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | 2023–26 | 21.7% | 18% | 0.72 | -16% | +3.7% (0.8) | +4.1% | 0.30 | 0.053 (2.0) | 0.213 | 19% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | crise | 77.8% | 26% | 2.28 | -8% | +13.7% (2.2) | +30.6% | 1.94 | 0.056 (1.1) | 0.115 | 19% |
| Máx. IC-IR, 14 fatores (2017–2022) | 2017–22 | 31.8% | 26% | 1.05 | -41% | +14.9% (3.8) | +30.4% | 1.50 | 0.068 (3.2) | 0.053 | 21% |
| Máx. IC-IR, 14 fatores (2017–2022) | 2023–26 | 19.9% | 19% | 0.62 | -17% | +2.4% (0.5) | -4.2% | -0.06 | 0.038 (1.4) | 0.185 | 21% |
| Máx. IC-IR, 14 fatores (2017–2022) | crise | 74.2% | 28% | 2.04 | -9% | +12.0% (1.9) | +36.1% | 2.40 | 0.056 (1.3) | 0.114 | 21% |
| Máx. IC-IR, 6 blocos (2017–2022) | 2017–22 | 26.3% | 27% | 0.86 | -43% | +10.8% (2.5) | +27.2% | 1.43 | 0.064 (2.9) | 0.099 | 22% |
| Máx. IC-IR, 6 blocos (2017–2022) | 2023–26 | 18.0% | 20% | 0.52 | -19% | +0.8% (0.2) | +0.8% | 0.14 | 0.044 (1.8) | 0.200 | 22% |
| Máx. IC-IR, 6 blocos (2017–2022) | crise | 61.8% | 27% | 1.84 | -10% | +4.1% (0.5) | +30.6% | 2.03 | 0.070 (1.9) | 0.142 | 22% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | 2017–22 | 26.3% | 26% | 0.88 | -43% | +10.7% (2.3) | +21.7% | 1.10 | 0.067 (3.0) | 0.098 | 23% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | 2023–26 | 19.2% | 20% | 0.57 | -17% | +1.8% (0.4) | +0.3% | 0.13 | 0.041 (1.5) | 0.197 | 23% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | crise | 55.5% | 23% | 1.87 | -9% | -0.7% (-0.1) | +12.4% | 0.98 | 0.050 (1.6) | 0.110 | 23% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | 2017–22 | 20.6% | 22% | 0.77 | -35% | +4.8% (1.0) | +14.0% | 0.75 | 0.048 (1.8) | 0.079 | 16% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | 2023–26 | 23.2% | 16% | 0.86 | -9% | +4.6% (0.9) | +4.9% | 0.33 | 0.061 (2.0) | 0.221 | 16% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | crise | 51.3% | 21% | 1.95 | -7% | -4.1% (-0.4) | -7.4% | -0.26 | 0.013 (0.2) | 0.090 | 16% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | 2017–22 | 26.7% | 28% | 0.84 | -46% | +11.7% (3.0) | +22.9% | 1.24 | 0.053 (2.9) | 0.092 | 21% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | 2023–26 | 17.7% | 21% | 0.50 | -17% | +0.8% (0.2) | +3.0% | 0.25 | 0.032 (1.4) | 0.165 | 21% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | crise | 84.1% | 29% | 2.14 | -9% | +18.2% (3.9) | +49.9% | 3.67 | 0.084 (2.3) | 0.138 | 21% |

Pesos estimados em 2017–2022 (usados fora da amostra):

- `otim_fatores_2017_2022`: mom_12_1 26%, nd_ebitda 23%, vol_1y 13%, ebitda_ev 10%, bp 9%, roic 9%, size 7%, beta_2y 2%, roe 1%
- `otim_blocos_2017_2022`: momentum 42%, valor 37%, baixo_risco 8%, solidez 8%, tamanho 5%
- `otim_blocos_proxies_2017_2022`: momentum 48%, valor 28%, baixo_risco 17%, tamanho 7%
- `icir_simples_2017_2022`: mom_12_1 19%, nd_ebitda 14%, ebitda_ev 13%, piotroski 9%, roic 9%, bp 9%, ep 8%, vol_1y 7%, roe 6%, dy 4%, beta_2y 1%
- `crise_blocos`: momentum 47%, valor 31%, tamanho 11%, solidez 11%
- `recomendado_regra_2017_2022`: bp 16%, mom_12_1 15%, ebitda_ev 14%, vol_1y 12%, beta_2y 11%, nd_ebitda 10%, ep 9%, roic 8%, roe 5%, dy 2%

Bootstrap no nível dos 14 fatores, amostra inteira, IC-IR 1m, agregado por grupo (mediana [p5–p95]): valor 38% [16%–58%]; qualidade 18% [1%–37%]; solidez 10% [0%–28%]; momentum 15% [5%–28%]; baixo_risco 10% [4%–22%]; tamanho 5% [0%–13%].

## Método

- **Preços**: COTAHIST oficial da B3 (lote padrão, à vista), série por ISIN (cobre troca de código), corte na última lacuna > 45 dias. Os ajustes usam `split_events`/`adjust` de `pipeline/market.py` sobre o suplemento B3, mais o histórico do Yahoo (o suplemento só guarda o evento mais recente de cada tipo por ISIN; sem isso faltariam, por exemplo, as bonificações anuais do Bradesco 2015–2021) e a detecção de razões redondas. Restituição de capital em ações (BRAP4, 12/2021) recebe ajuste neutro. **Retorno total**: proventos em dinheiro da B3 (histórico por evento), na classe negociada (units: linha UNT ou composição), reinvestidos no ex-dia.
- **Fundamentos**: DFP 2015–2025 e ITR 2016–2026 brutos da CVM, extraídos com as funções de `pipeline/cvm.py`. Usa o arquivo original de cada período, sem a reapresentação do ano seguinte, e a última versão entregue daquele período. O LTM sai da aritmética dos acumulados (YTD + exercício anterior − YTD de um ano antes), que funciona para exercícios fora de dezembro (CAML3, SMTO3). Defasagem de 45 dias para ITR e 90 dias para DFP. Os dados ficam velhos demais (descartados) após 18 meses.
- **Ações em circulação**: composição do capital da CVM (2020+), com escala corrigida registro a registro contra a contagem atual da B3 retroprojetada pelos eventos. Antes de 2020, retroprojeção pelos eventos, corrigida por emissões e recompras grandes (> 15%) inferidas do lucro por ação básico (BEEF3, CYRE3, DASA3, ENEV3, EQTL3, GOAU4, JHSF3, LOGG3, MILS3, MOVI3, MYPK3, POMO3, POMO4, SUZB3, TOTS3, VULC3).
- **Universo**: os 147 tickers de data/market/quotes.json (universo líquido atual, sem as entradas 'extra') filtrados por ADTV 3m >= R$ 5 mi na data; 1 classe por emissor (maior ADTV). Formação no último pregão do mês. Ações com último negócio há mais de 7 dias são excluídas.
- **Fatores**: E/P = lucro LTM dos controladores / valor de mercado. B/P = PL dos controladores / valor de mercado. EBITDA/EV, com EV = valor de mercado + dívida líquida (com arrendamentos) + minoritários. DY = proventos com data-com nos últimos 12 meses / preço. ROE sobre PL médio. ROIC = EBIT×(1−34%)/(PL + dívida líquida). Margem bruta LTM. Piotroski F com os 9 sinais LTM contra LTM de um ano antes (como `pipeline/build.py`). Altman Z″ mercados emergentes = 3,25 + 6,56·X1 + 3,26·X2 + 6,72·X3 + 1,05·X4. Dívida líquida/EBITDA (EBITDA ≤ 0 com dívida = pior). Momentum 12-1. Volatilidade de 252 pregões. Beta diário de 504 pregões contra o Ibovespa. Log do valor de mercado. Bancos, seguradoras, B3 e Itaúsa ficam fora dos fatores de EBITDA, ROIC, margem, Piotroski, Altman e alavancagem.
- **Compostos**: z-score transversal winsorizado (2,5%/97,5%, corte ±3). O escore pondera os z disponíveis e renormaliza os pesos por ação, como o escore do painel. Proxies do painel: valor = média z(E/P, EBITDA/EV, DY), no lugar da TIR implícita. Upside = desconto dos múltiplos (E/P, B/P, EBITDA/EV) contra a mediana de 60 meses da própria ação. Qualidade = ROE médio de 5 exercícios + (Piotroski − 4,5)/9. Solidez = −dív. líq./EBITDA + Altman/3, como no painel. Sobrerreação = −(retorno do mês − beta × Ibovespa). Probabilidade = ln(1 + upside)/volatilidade.

## Vieses e limitações

- **Sobrevivência e seleção**: o universo são as ações líquidas de out/2026. Empresas que quebraram, foram compradas ou perderam liquidez em 2017–2026 não entram. Pior: uma small cap de 2017 só está aqui se sobreviveu e cresceu, o que infla retornos passados de small caps e de ações com momentum. Os números de tamanho, momentum e baixo risco devem ser lidos com desconto. O nível de retorno do universo (a.a.) é otimista. Diferenças entre fatores e ICs sofrem menos, mas também sofrem.
- **Poucos anos**: 117 meses, cerca de 9 anos e um único ciclo de juros. Fora da amostra são 46 meses. Crise são 9 meses de quatro episódios. Com IC-IR mensal de ~0,15–0,25, t ≈ 2 exige ~100 meses: quase todos os fatores estão no limiar da significância, e os intervalos dos pesos são largos.
- **Universo pequeno**: 53 a 142 nomes por mês, quintis de 10 a 28 ações. Os spreads Q5−Q1 são ruidosos e não descontam custos. O giro mensal do quintil superior aparece na tabela.
- **Dados**: a última versão de cada ITR/DFP pode conter correções feitas depois da data de corte (viés pequeno). Ações antes de 2020 são estimadas. Proventos e eventos dependem de B3/Yahoo. O mês 2026-10 é parcial (até 23/10). O retorno do Ibovespa é só de preço. Upside DCF, probabilidade Monte Carlo e sobrerreação do dia da eleição não têm histórico e foram testados só por proxies.
- **Múltiplas comparações**: 14 fatores × 4 horizontes. Alguns t ≈ 2 surgem por acaso. Pesos de crise são ilustrativos.

