# Backtest de fatores — ações brasileiras, painel mensal point-in-time 2017-01 a 2026-09

Gerado por `pipeline/tests/factor_backtest.py` em 2026-11-18T14:26:09. Dados completos (ICs mensais, spreads, séries dos compostos, bootstrap) em `data/tests/factor_backtest.json`. 117 meses de formação (2017-01 a 2026-09), média de 102 ações por mês (mín. 53, máx. 142). IC = correlação de Spearman entre o fator (orientado no sinal esperado) e o retorno total futuro; t com erros de Newey-West (defasagens = horizonte + 2).

## Conclusões

1. **Funcionaram (t ≥ 2 em algum horizonte e IC 12m positivo dentro e fora da amostra):** E/P (IC 12m 0.113, t 2.31); B/P (IC 12m 0.152, t 3.55); EBITDA/EV (IC 12m 0.099, t 2.03); Momentum 12-1 (IC 12m 0.073, t 1.95). O sinal mais robusto é **valor**: barato por lucro, patrimônio e EBITDA paga em todos os horizontes, cresce com o horizonte e se mantém em 2023–2026.
2. **Positivos mas fracos (IC > 0 em 3+ horizontes e t entre 1 e 2):** DY 12m (IC 1m 0.025, t 1.29); ROE (IC 1m 0.024, t 1.35); ROIC (IC 1m 0.022, t 1.13); Piotroski F (IC 1m 0.027, t 1.85); Dív. líq./EBITDA (IC 1m 0.026, t 1.82); Volatilidade 1a (IC 1m 0.039, t 1.59); Beta 2a (IC 1m 0.013, t 0.50).
3. **Sem efeito ou contrários:** Margem bruta (IC 1m -0.001, t -0.04); Altman Z″ (EM) (IC 1m 0.004, t 0.31); Tamanho (log mcap) (IC 1m -0.005, t -0.31).
4. **Proxies dos blocos sem histórico do painel não funcionaram em meses normais.** Upside até o múltiplo histórico da própria ação: IC 1m -0.021 (t -1.14), 6m -0.063 (t -2.62): ações baratas contra o próprio passado continuam caindo. Sobrerreação (comprar quem caiu mais que o beta prevê no mês): IC 1m -0.039 (t -3.13), 12m -0.057 (t -3.94). O retorno residual tem continuação, não reversão. Só nos meses de crise o sinal vira: IC 1m 0.042 em 9 meses, amostra pequena demais para concluir.
5. **Fora da amostra, pesos otimizados não batem regras simples.** O máximo IC-IR estimado em 2017–2022 (blocos) teve excesso sobre o universo de +12.2% a.a. dentro da amostra e -0.1% a.a. fora dela. Pesos iguais por bloco ficaram em +2.9% e os pesos atuais do painel renormalizados em +4.7% (IC 12m fora da amostra 0.118). A regra recomendada, estimada só com 2017–2022, entregou +3.3% (IC 1m 0.064, IC 12m 0.223). Com 46 meses fora da amostra, nenhuma dessas diferenças é estatisticamente distinguível. A escolha tem de ser por robustez, não pelo melhor número.
6. **Regime de crise** (formação após Ibovespa ≤ −10% em 3 meses; 9 meses: 2018-05, 2018-06, 2020-03, 2020-04, 2020-05, 2021-09, 2021-10, 2021-11, 2022-06; quatro episódios independentes). Valor (B/P, EBITDA/EV) e momentum ficam mais fortes. Baixo risco **inverte**: as ações de beta e volatilidade altas lideram a recuperação. IC 3m em crise: B/P 0.152; Momentum 12-1 0.137; Piotroski F 0.083; EBITDA/EV 0.065; ... Margem bruta -0.052; Volatilidade 1a -0.153; Beta 2a -0.201.

## Pesos recomendados

A regra dá a cada fator peso proporcional ao seu IC-IR positivo, na média dos horizontes de 1, 3 e 12 meses. Fatores de IC-IR médio ≤ 0 ficam com zero. São 13 candidatos: tamanho fica fora porque é o fator mais contaminado pelo viés de sobrevivência. A regra não inverte a covariância dos ICs nem usa corte duro. Fora da amostra, esquemas simples como este generalizaram tão bem ou melhor que o máximo IC-IR, que concentrou peso em momentum e perdeu força em 2023–2026. Os números são medianas de 1000 reamostragens em blocos de 12 meses da amostra inteira (95 meses com os três horizontes). O intervalo é o de 90% (p5–p95), e o peso recomendado é a mediana normalizada e arredondada para 5%. A mesma regra estimada só com 2017–2022 está na tabela de compostos, com o resultado fora da amostra.

| Bloco | Peso recomendado | Mediana bootstrap | IC 90% | P(peso > 1%) | Estimativa pontual |
|---|---:|---:|---:|---:|---:|
| Valor | **40%** | 39% | 23% – 56% | 1.00 | 39% |
| Qualidade | **20%** | 20% | 4% – 30% | 0.97 | 20% |
| Solidez | **10%** | 12% | 4% – 19% | 0.98 | 13% |
| Momentum 12-1 | **10%** | 10% | 5% – 22% | 1.00 | 10% |
| Baixo risco | **20%** | 18% | 12% – 28% | 1.00 | 19% |

Por fator (mediana [p5–p95], P(peso > 1%)): E/P 11% [4%–15%], 0.97; B/P 12% [6%–27%], 1.00; EBITDA/EV 9% [3%–14%], 0.98; DY 12m 7% [0%–11%], 0.86; ROE 6% [0%–9%], 0.88; ROIC 7% [0%–10%], 0.94; Margem bruta 0% [0%–8%], 0.35; Piotroski F 6% [0%–10%], 0.88; Altman Z″ (EM) 3% [0%–8%], 0.69; Dív. líq./EBITDA 9% [4%–13%], 0.98; Momentum 12-1 10% [5%–22%], 1.00; Volatilidade 1a 11% [8%–15%], 1.00; Beta 2a 7% [2%–14%], 0.98. Os demais ficam com peso zero na maioria das reamostragens.

Tradução para o painel (hoje valor 30%, qualidade 20%, solidez 15%, upside 10%, sobrerreação 10%, probabilidade 15%):

- **Valor** deve ser o maior bloco: 40% recomendado, intervalo 23%–56%. Upside (DCF) e probabilidade (Monte Carlo) derivam do mesmo valor justo e, na prática, são valor de novo. Sem histórico para testá-los, o prudente é tratá-los como parte do bloco valor, sem somar peso.
- **Qualidade** 20% e **solidez** 10%. Os sinais que sobrevivem são ROE, Piotroski e dívida líquida/EBITDA, todos fracos (t de 1 a 2). Margem bruta e Altman Z″ têm IC ≈ 0 e podem sair dos blocos.
- **Momentum** 10% e **baixo risco** 20% não existem no painel e entram pela evidência. O momentum perdeu força fora da amostra no horizonte de 1m, mas segue positivo em 12m. Os dois estão inflados pelo viés de sobrevivência, e baixo risco inverte em crises.
- **Sobrerreação**: o proxy mensal tem IC negativo significativo, e com os proxies no otimizador o bootstrap dá peso mediano 0% a ela e 0% ao upside histórico. A recomendação é 0% a 5% fora de crises.
- **Em crise**, os pesos de referência (IC-IR 3m nos 9 meses de crise, blocos) são valor 29%, qualidade 0%, solidez 10%, momentum 49%, baixo risco 0%, tamanho 12%. Indicam mais valor e momentum e zero em baixo risco, mas vêm de quatro episódios e não servem como estimativa.

## IC por fator e horizonte (amostra inteira)

IC médio, com o t de Newey-West entre parênteses. IC-IR = média/dp do IC mensal. Q5−Q1 = carteira long-short mensal, igualmente ponderada, do quintil mais atrativo menos o menos atrativo (retorno total, anualizado ×12).

| Fator (sinal) | 1m | 3m | 6m | 12m | IC-IR 1m | % meses IC>0 (1m) | Q5−Q1 a.a. | Sharpe Q5−Q1 | Q5−Q1 12m a.a. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E/P (+) | 0.036 (1.9) | 0.062 (2.0) | 0.073 (1.7) | 0.113 (2.3) | 0.21 | 59% | +10.1% | 0.54 | +8.7% |
| B/P (+) | 0.027 (1.5) | 0.044 (1.6) | 0.082 (2.4) | 0.152 (3.6) | 0.15 | 56% | +14.3% | 0.79 | +17.6% |
| EBITDA/EV (+) | 0.026 (1.4) | 0.047 (1.8) | 0.057 (1.6) | 0.099 (2.0) | 0.14 | 55% | +16.2% | 0.80 | +8.2% |
| DY 12m (+) | 0.025 (1.3) | 0.037 (1.2) | 0.039 (0.8) | 0.061 (1.0) | 0.15 | 55% | +3.0% | 0.16 | -0.4% |
| ROE (+) | 0.024 (1.4) | 0.037 (1.6) | 0.028 (0.9) | 0.012 (0.3) | 0.14 | 56% | +5.8% | 0.30 | +0.6% |
| ROIC (+) | 0.022 (1.1) | 0.038 (1.4) | 0.025 (0.7) | 0.009 (0.2) | 0.12 | 56% | +3.4% | 0.16 | -0.0% |
| Margem bruta (+) | -0.001 (-0.0) | -0.010 (-0.5) | -0.019 (-0.7) | -0.031 (-0.7) | -0.00 | 52% | -4.3% | -0.27 | -6.4% |
| Piotroski F (+) | 0.027 (1.8) | 0.034 (1.5) | 0.032 (1.0) | 0.037 (0.7) | 0.18 | 58% | +5.9% | 0.38 | +3.1% |
| Altman Z″ (EM) (+) | 0.004 (0.3) | 0.006 (0.3) | 0.007 (0.2) | -0.012 (-0.3) | 0.03 | 51% | -4.3% | -0.28 | -5.9% |
| Dív. líq./EBITDA (−) | 0.026 (1.8) | 0.037 (1.7) | 0.040 (1.3) | 0.043 (1.1) | 0.17 | 56% | +6.5% | 0.42 | +4.4% |
| Momentum 12-1 (+) | 0.037 (2.0) | 0.060 (2.5) | 0.085 (3.2) | 0.073 (1.9) | 0.17 | 59% | +7.8% | 0.35 | +6.7% |
| Volatilidade 1a (−) | 0.039 (1.6) | 0.071 (2.2) | 0.081 (1.7) | 0.081 (1.3) | 0.15 | 57% | -0.2% | -0.01 | -1.6% |
| Beta 2a (−) | 0.013 (0.5) | 0.037 (1.0) | 0.039 (0.8) | 0.037 (0.6) | 0.05 | 50% | -5.1% | -0.19 | -1.2% |
| Tamanho (log mcap) (−) | -0.005 (-0.3) | -0.012 (-0.5) | -0.008 (-0.3) | 0.002 (0.1) | -0.03 | 49% | +8.9% | 0.47 | +7.2% |
| Upside p/ múltiplo histórico (proxy) (+) | -0.021 (-1.1) | -0.043 (-1.8) | -0.063 (-2.6) | -0.045 (-1.6) | -0.12 | 48% | -1.4% | -0.07 | -6.0% |
| Reversão 1m residual (proxy sobrerreação) (+) | -0.039 (-3.1) | -0.036 (-2.6) | -0.051 (-3.3) | -0.057 (-3.9) | -0.27 | 38% | -12.2% | -0.82 | -6.5% |
| ln(1+upside hist)/vol (proxy probabilidade) (+) | -0.017 (-1.0) | -0.033 (-1.4) | -0.051 (-2.3) | -0.027 (-1.1) | -0.11 | 48% | -2.7% | -0.16 | -5.8% |

## Estabilidade: dentro × fora da amostra e crise × normal

| Fator | IC 1m 2017–22 | IC 1m 2023–26 | IC 12m 2017–22 | IC 12m 2023–26 | IC 3m crise | IC 3m normal | % crise IC>0 (3m) |
|---|---:|---:|---:|---:|---:|---:|---:|
| E/P | 0.016 | 0.066 | 0.061 | 0.171 | 0.033 | 0.065 | 56% |
| B/P | 0.021 | 0.036 | 0.168 | 0.114 | 0.152 | 0.034 | 89% |
| EBITDA/EV | 0.028 | 0.022 | 0.088 | 0.086 | 0.065 | 0.046 | 67% |
| DY 12m | 0.010 | 0.048 | -0.008 | 0.132 | 0.034 | 0.038 | 44% |
| ROE | 0.015 | 0.037 | -0.032 | 0.071 | -0.034 | 0.043 | 33% |
| ROIC | 0.024 | 0.018 | -0.042 | 0.054 | -0.024 | 0.043 | 33% |
| Margem bruta | -0.014 | 0.021 | -0.071 | 0.060 | -0.052 | -0.007 | 22% |
| Piotroski F | 0.019 | 0.037 | -0.060 | 0.132 | 0.083 | 0.029 | 89% |
| Altman Z″ (EM) | -0.001 | 0.012 | -0.083 | 0.055 | 0.043 | 0.003 | 67% |
| Dív. líq./EBITDA | 0.026 | 0.025 | -0.019 | 0.116 | 0.022 | 0.039 | 67% |
| Momentum 12-1 | 0.057 | 0.006 | 0.025 | 0.112 | 0.137 | 0.054 | 78% |
| Volatilidade 1a | 0.025 | 0.060 | -0.011 | 0.197 | -0.153 | 0.091 | 33% |
| Beta 2a | 0.005 | 0.025 | -0.012 | 0.106 | -0.201 | 0.057 | 33% |
| Tamanho (log mcap) | -0.003 | -0.009 | 0.022 | -0.030 | 0.033 | -0.016 | 56% |
| Upside p/ múltiplo histórico (proxy) | -0.038 | 0.000 | -0.007 | -0.081 | -0.044 | -0.043 | 56% |
| Reversão 1m residual (proxy sobrerreação) | -0.046 | -0.029 | -0.067 | -0.038 | -0.011 | -0.038 | 56% |

## Decaimento do sinal

IC médio entre o fator em t e o retorno do mês t+k → t+k+1. Mede por quanto tempo uma leitura do fator continua informativa.

| Fator | k=0 | k=1 | k=2 | k=3 | k=6 | k=9 | k=11 |
|---|---:|---:|---:|---:|---:|---:|---:|
| E/P | 0.036 | 0.033 | 0.030 | 0.024 | 0.030 | 0.035 | 0.048 |
| B/P | 0.027 | 0.025 | 0.033 | 0.037 | 0.042 | 0.047 | 0.053 |
| EBITDA/EV | 0.026 | 0.026 | 0.020 | 0.009 | 0.018 | 0.022 | 0.033 |
| DY 12m | 0.025 | 0.022 | 0.016 | 0.012 | 0.016 | 0.015 | 0.021 |
| ROE | 0.024 | 0.019 | 0.013 | 0.004 | 0.001 | -0.001 | 0.011 |
| ROIC | 0.022 | 0.022 | 0.010 | -0.004 | -0.006 | -0.006 | -0.002 |
| Margem bruta | -0.001 | 0.001 | -0.007 | -0.012 | -0.009 | -0.010 | -0.014 |
| Piotroski F | 0.027 | 0.020 | 0.008 | -0.000 | 0.010 | 0.007 | 0.004 |
| Altman Z″ (EM) | 0.004 | 0.002 | 0.003 | -0.003 | -0.000 | -0.009 | -0.012 |
| Dív. líq./EBITDA | 0.026 | 0.025 | 0.015 | 0.009 | 0.014 | 0.005 | 0.005 |
| Momentum 12-1 | 0.037 | 0.031 | 0.039 | 0.046 | 0.022 | 0.001 | 0.012 |
| Volatilidade 1a | 0.039 | 0.043 | 0.038 | 0.035 | 0.032 | 0.037 | 0.033 |
| Beta 2a | 0.013 | 0.015 | 0.012 | 0.008 | 0.010 | 0.015 | 0.014 |
| Tamanho (log mcap) | -0.005 | -0.003 | -0.001 | -0.002 | -0.002 | -0.004 | -0.006 |
| Upside p/ múltiplo histórico (proxy) | -0.021 | -0.027 | -0.021 | -0.023 | -0.014 | -0.004 | 0.009 |
| Reversão 1m residual (proxy sobrerreação) | -0.039 | -0.019 | -0.006 | 0.002 | -0.034 | -0.054 | 0.038 |

## Compostos: dentro (2017–2022) e fora da amostra (2023–2026)

Carteira = quintil superior do escore, igualmente ponderada, rebalanceamento mensal, retorno total, sem custos. Sharpe do quintil superior sobre o CDI; Sharpe da long-short sem taxa livre. Excesso = quintil superior menos a média igualmente ponderada do universo (t Newey-West). No mesmo período, o universo igualmente ponderado rendeu 13.9% a.a. em 2017–2022 e 16.5% a.a. em 2023–2026. O Ibovespa (sem proventos) rendeu 9.3% e 17.7%.

| Composto | Período | Q5 a.a. | Vol | Sharpe | Máx. DD | Excesso a.a. (t) | L/S a.a. | Sharpe L/S | IC 1m (t) | IC 12m | Giro/mês |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | 2017–22 | 17.7% | 25% | 0.60 | -37% | +3.2% (0.8) | -1.4% | 0.02 | -0.007 (-0.3) | -0.023 | 28% |
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | 2023–26 | 16.8% | 21% | 0.46 | -19% | -0.1% (-0.0) | +3.7% | 0.40 | 0.029 (1.6) | 0.073 | 28% |
| Pesos atuais do painel (proxies p/ upside, sobrerreação, probabilidade) | crise | 71.2% | 30% | 1.85 | -10% | +10.8% (1.2) | +15.1% | 0.94 | 0.040 (0.5) | 0.016 | 28% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | 2017–22 | 21.5% | 25% | 0.73 | -37% | +6.2% (1.2) | +5.6% | 0.37 | 0.008 (0.3) | -0.015 | 17% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | 2023–26 | 22.5% | 20% | 0.70 | -13% | +4.7% (1.4) | +10.3% | 0.85 | 0.041 (2.0) | 0.118 | 17% |
| Pesos atuais do painel renormalizados (valor, upside, qualidade, solidez) | crise | 83.4% | 29% | 2.18 | -8% | +17.6% (1.4) | +19.3% | 1.08 | 0.028 (0.4) | 0.033 | 17% |
| Pesos iguais (14 fatores) | 2017–22 | 17.5% | 23% | 0.64 | -37% | +2.3% (0.6) | +8.0% | 0.50 | 0.031 (1.2) | 0.013 | 13% |
| Pesos iguais (14 fatores) | 2023–26 | 20.6% | 19% | 0.67 | -14% | +2.9% (0.7) | +6.0% | 0.40 | 0.060 (2.3) | 0.204 | 13% |
| Pesos iguais (14 fatores) | crise | 52.9% | 25% | 1.72 | -9% | -2.2% (-0.2) | -0.5% | 0.06 | 0.009 (0.1) | 0.043 | 13% |
| Pesos iguais (6 blocos) | 2017–22 | 20.1% | 23% | 0.72 | -38% | +4.7% (1.3) | +11.8% | 0.70 | 0.037 (1.6) | 0.025 | 15% |
| Pesos iguais (6 blocos) | 2023–26 | 20.5% | 19% | 0.64 | -15% | +2.9% (0.7) | +1.9% | 0.20 | 0.047 (1.9) | 0.179 | 15% |
| Pesos iguais (6 blocos) | crise | 61.7% | 28% | 1.76 | -9% | +4.2% (0.3) | +0.8% | 0.13 | 0.012 (0.2) | 0.047 | 15% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | 2017–22 | 25.0% | 25% | 0.85 | -40% | +9.3% (2.4) | +19.9% | 1.06 | 0.051 (2.1) | 0.040 | 19% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | 2023–26 | 22.8% | 19% | 0.76 | -13% | +4.7% (0.9) | +5.8% | 0.38 | 0.054 (2.0) | 0.210 | 19% |
| Pesos ∝ IC-IR 1m positivo (2017–2022) | crise | 73.3% | 27% | 2.06 | -8% | +11.3% (2.5) | +25.9% | 1.60 | 0.051 (1.0) | 0.088 | 19% |
| Máx. IC-IR, 14 fatores (2017–2022) | 2017–22 | 30.1% | 24% | 1.03 | -38% | +13.1% (3.6) | +29.5% | 1.47 | 0.063 (2.8) | 0.048 | 19% |
| Máx. IC-IR, 14 fatores (2017–2022) | 2023–26 | 16.8% | 19% | 0.50 | -16% | -0.4% (-0.1) | -5.1% | -0.10 | 0.036 (1.3) | 0.174 | 19% |
| Máx. IC-IR, 14 fatores (2017–2022) | crise | 79.5% | 27% | 2.20 | -8% | +15.0% (1.6) | +33.2% | 1.80 | 0.038 (0.7) | 0.093 | 19% |
| Máx. IC-IR, 6 blocos (2017–2022) | 2017–22 | 28.1% | 26% | 0.92 | -42% | +12.2% (3.0) | +25.5% | 1.28 | 0.064 (3.0) | 0.089 | 23% |
| Máx. IC-IR, 6 blocos (2017–2022) | 2023–26 | 16.9% | 20% | 0.47 | -18% | -0.1% (-0.0) | +0.4% | 0.12 | 0.040 (1.6) | 0.191 | 23% |
| Máx. IC-IR, 6 blocos (2017–2022) | crise | 64.7% | 25% | 2.01 | -8% | +5.5% (0.8) | +24.2% | 1.63 | 0.062 (1.8) | 0.111 | 23% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | 2017–22 | 26.4% | 26% | 0.89 | -42% | +10.6% (2.3) | +22.9% | 1.16 | 0.066 (2.8) | 0.086 | 23% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | 2023–26 | 18.3% | 20% | 0.54 | -17% | +1.1% (0.2) | -1.5% | 0.06 | 0.041 (1.4) | 0.198 | 23% |
| Máx. IC-IR, 6 blocos + upside hist. + reversão 1m (2017–2022) | crise | 57.7% | 22% | 2.03 | -8% | +0.5% (0.1) | +8.7% | 0.70 | 0.038 (1.2) | 0.082 | 23% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | 2017–22 | 20.2% | 22% | 0.76 | -36% | +4.5% (1.0) | +11.1% | 0.62 | 0.045 (1.6) | 0.072 | 16% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | 2023–26 | 21.6% | 16% | 0.80 | -9% | +3.3% (0.6) | +2.8% | 0.24 | 0.064 (2.0) | 0.223 | 16% |
| Regra recomendada (peso ∝ IC-IR positivo médio 1/3/12m, 13 fatores, sem tamanho), estimada em 2017–2022 | crise | 55.1% | 21% | 2.05 | -7% | -1.5% (-0.1) | -6.5% | -0.23 | 0.004 (0.1) | 0.072 | 16% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | 2017–22 | 28.2% | 28% | 0.88 | -44% | +12.8% (3.4) | +22.6% | 1.22 | 0.050 (2.8) | 0.085 | 22% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | 2023–26 | 16.2% | 21% | 0.43 | -18% | -0.4% (-0.1) | +2.2% | 0.21 | 0.030 (1.3) | 0.157 | 22% |
| Pesos de crise (IC-IR 3m nos meses de crise, amostra inteira — referência) | crise | 89.9% | 31% | 2.15 | -9% | +21.8% (4.2) | +55.9% | 2.93 | 0.082 (2.3) | 0.122 | 22% |

Pesos estimados em 2017–2022 (usados fora da amostra):

- `otim_fatores_2017_2022`: mom_12_1 23%, nd_ebitda 19%, vol_1y 14%, roic 12%, size 11%, ebitda_ev 9%, bp 6%, beta_2y 3%, roe 2%
- `otim_blocos_2017_2022`: momentum 46%, valor 31%, baixo_risco 10%, solidez 8%, tamanho 5%
- `otim_blocos_proxies_2017_2022`: momentum 50%, valor 25%, baixo_risco 21%, tamanho 4%
- `icir_simples_2017_2022`: mom_12_1 20%, nd_ebitda 13%, ebitda_ev 11%, roic 10%, piotroski 10%, bp 8%, vol_1y 8%, ep 7%, roe 7%, dy 5%, beta_2y 2%
- `crise_blocos`: momentum 49%, valor 29%, tamanho 12%, solidez 10%
- `recomendado_regra_2017_2022`: bp 16%, mom_12_1 14%, vol_1y 12%, beta_2y 12%, ebitda_ev 12%, roic 10%, nd_ebitda 9%, ep 8%, roe 5%, dy 3%

Bootstrap no nível dos 14 fatores, amostra inteira, IC-IR 1m, agregado por grupo (mediana [p5–p95]): valor 37% [15%–62%]; qualidade 18% [0%–38%]; solidez 9% [0%–30%]; momentum 15% [5%–33%]; baixo_risco 11% [3%–23%]; tamanho 6% [0%–15%].

## Método

- **Preços**: COTAHIST oficial da B3 (lote padrão, à vista), série por ISIN (cobre troca de código), corte na última lacuna > 45 dias. Os ajustes usam `split_events`/`adjust` de `pipeline/market.py` sobre o suplemento B3, mais o histórico do Yahoo (o suplemento só guarda o evento mais recente de cada tipo por ISIN; sem isso faltariam, por exemplo, as bonificações anuais do Bradesco 2015–2021) e a detecção de razões redondas. Restituição de capital em ações (BRAP4, 12/2021) recebe ajuste neutro. **Retorno total**: proventos em dinheiro da B3 (histórico por evento), na classe negociada (units: linha UNT ou composição), reinvestidos no ex-dia.
- **Fundamentos**: DFP 2015–2025 e ITR 2016–2026 brutos da CVM, extraídos com as funções de `pipeline/cvm.py`. Usa o arquivo original de cada período, sem a reapresentação do ano seguinte, e a última versão entregue daquele período. O LTM sai da aritmética dos acumulados (YTD + exercício anterior − YTD de um ano antes), que funciona para exercícios fora de dezembro (CAML3, SMTO3). **Disponibilidade**: cada demonstração entra no painel na data em que a versão usada foi recebida pela CVM (DT_RECEB), e o LTM só quando as três peças já tinham sido entregues; a defasagem fixa de 45 dias (ITR) e 90 dias (DFP) fica só como reserva quando não há data de entrega. Os arquivos da CVM guardam apenas a última versão de cada período: uma reapresentação entra, portanto, com atraso (na data da reapresentação), nunca antes. Os dados ficam velhos demais (descartados) após 18 meses.
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

