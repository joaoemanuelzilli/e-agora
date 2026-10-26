# ORVR3 — OrizonVR | dossiê G12 (26/10/2026)

**Preço:** R$ 15,72 às 11h54 (−24,6%; sexta R$ 20,84).
**Atenção às ações:**
- 137.324.101 ON na CVM, pré-desdobramento.
- Desdobramento 1:4 em 11/08/2026 → **549,3 mi**.
- Bônus ORVR11 → **+75,6 mi** a R$ 13,2325, exercíveis de mai a set/2027 (~R$ 1,0 bi).
- Total diluído: 624,9 mi.
- Mercado ~R$ 8,6 bi (não diluído).

## Negócio (após incorporar Vital, GBio e Orbis em 11/06/2026)
- Maior plataforma de resíduos da América Latina: 30 ecoparques em 15 estados, 3,9 Mt recebidas no 2T26.
- Cinco segmentos (participação no lucro bruto do 2T26):
  - Destinação final (gate-fee R$ 90,4/t, +3,8% real): 49,9%
  - Gestão integrada (concessões/PPPs, contraprestação fixa indexada: Ecourbis-SP, Ipatinga, Campos, São Luís, Foz etc.): 48,5%
  - Coleta: 0,3%
  - Transição energética (3 plantas de biometano e 3 UTEs; 7 plantas de biometano e a URE Barueri em construção): 2,1%
  - Economia circular: −0,8%
- A contraprestação da Vital foi de 41,2 mi de ações e 5,6 mi de bônus, entregues à Growth (Queiroz Galvão). Novo conselho com Gama FIP.

## 2T26 pró-forma ajustado (ex-ICPC-01 e não recorrentes)
| R$ mi | Legado | Vital | Combinado | Δ a/a |
|---|---|---|---|---|
| Receita | 349,1 | 632,5 | 981,7 | +17,3% |
| EBITDA ajustado | 123,7 | 158,1 | 281,7 (28,7%) | −0,4% |
| Lucro ajustado | 1,5 | 101,5 | 103,1 | −5,9% |

- O contábil consolidado traz só 1 mês da Vital: receita CVM R$ 622,8 mi com construção, lucro controlador de −R$ 11,2 mi.
- EBITDA LTM pró-forma R$ 1.239,5 mi. Dívida líquida R$ 2.241 mi (1,8x), excluindo o recebível da Ecourbis contra a Prefeitura de SP (R$ 784 mi, IPCA, 120 parcelas).
- Biometano: 130 mil m³/dia (Paulínia 58, Jaboatão 58, Metagás 15). Em ago/26, Jaboatão estava acima de 85 mil e Paulínia acima de 100 mil m³/dia.
- LRCAP 2026: 52,7 MW, R$ 79 mi/ano de receita fixa por 10 anos (Paulínia desde ago/26; Jaboatão e João Pessoa em out/28).
- Créditos de carbono: R$ 12,3 mi (348 mil t) no 2T26.
- Minoritários: Ecourbis 36,7%, Recife 30%, Titara/São Luís/Juparanã ~50%. Ficam com ~32% do EBITDA da Vital.

## Histórico (Orizon legado, CVM)
- Receita: 392 / 436 / 626 / 776 / 904 / 1.050 (2020–25), CAGR 21,8%.
- Margem EBITDA: 39% / 31% / 32% / 46% / 47% / 47%.
- Lucro: 20 / −62 / −149 / 40 / 61 / 60. Nunca pagou dividendos; lucros acumulados de −R$ 720 mi.

## Dívida
- Dívida bruta R$ 3.786 mi (debêntures CDI+/IPCA+ da Orizon; a Vital trouxe dívida bancária curta e financiamentos de equipamentos prefixados >15%) e caixa de R$ 1.544 mi.
- **Problema de dados CVM:** a conta 2.02.01 inclui R$ 276 mi de impostos e fornecedores marcados por erro. A dívida líquida da CVM (R$ 2.588 mi) fica superestimada; usei R$ 2.339 mi (empresa + arrendamentos).

## 4º mandato de Lula
- A favor no micro:
  - Combustível do Futuro (mandato de biometano)
  - SBCE (Lei 15.042/2024) e ITMOs
  - fechamento de lixões e PPPs
  - BNDES/Fundo Clima
- Contra:
  - juro real alto num ativo de prazo longo com capex pesado
  - risco de contraparte municipal
- A queda é custo de capital, não fundamento.

## Premissas (research/ORVR3.json)
- Receita-base 2025 pró-forma R$ 3.400 mi. O anual da Vital (~R$ 2,35 bi) é estimado a partir do 2T25 pró-forma.
- Crescimento: 16,5% / 14% / 11% / 9% / 8%.
- Margem EBITDA: 32% → 37,5%.
- Capex: 30% / 22% / 16% / 13% / 12% da receita. D&A 8,5–9,5%.
- Minoritários: 23% do lucro; valor econômico de R$ 1,2 bi (estimativa).
- Ativo não operacional de R$ 1.310 mi: recebível da Ecourbis a valor presente (R$ 470 mi) + valor presente dos bônus (R$ 840 mi).
- WACC 21,3%. g = 5,5%. ROIC terminal 14%.

## Resultado do motor (pipeline/model.py, 26/10/2026, Ke 25%)
- Preço usado: R$ 15,51 | **valor justo R$ 5,47** (-64,7%) | TIR implícita 9,6% | TIR 3a 14,1%
- Métodos: DCF R$ 1,96 · DDM R$ 2,46 · P/L-alvo R$ 12,53 · EV/EBITDA-alvo R$ 18,45 (WACC 21,3%; EV DCF R$ 3.483 mi; TV 60,0% do EV)
- Projeção 2026–30: receita [3961, 4516, 5012, 5463, 5900]; EBITDA [1268, 1558, 1804, 2021, 2213]; lucro controlador [345, 435, 594, 705, 817]
- DL/EBITDA [2.0, 1.1, 0.8, 0.6, 0.3]; ROE ['10,7%', '7,6%', '9,0%', '10,0%', '10,8%']; FCFF [-238, 175, 554, 815, 965]
- Cenários: bear R$ 3,80 · base R$ 5,47 · bull R$ 6,42 · esperado R$ 5,24 | Monte Carlo p10 R$ 3,95 · p50 R$ 5,45 · p90 R$ 7,08 · P(valor>preço) 0,0%
- **Leitura:** bom ativo, mas ROIC de ~10–13% abaixo do WACC de 21% no ciclo de capex. A Ke de 25% destrói o valor do crescimento (DCF ~R$ 2), e a TIR implícita é ~10%. Mesmo após −25%, o preço exige custo de capital de ~12–14%. **Armadilha a Ke 25%** (não é tese de queda macro: o fundamento está ok, o preço é que é alto para essa Ke).

## Fontes
- Release 2T26: https://api.mziq.com/mzfilemanager/v2/d/9267dc34-24be-4623-bcda-2414abcbda9a/257e5556-4090-b46e-67bb-9e3c26c4251b?origin=2
- Release 4T25: https://api.mziq.com/mzfilemanager/v2/d/9267dc34-24be-4623-bcda-2414abcbda9a/5994b0b9-0b0f-fe5f-905a-94ca4ae36b2f?origin=2
- CVM: data/hist/ORVR3.json. **Ações e dívida precisam dos overrides acima.** O P/L LTM (~192x) e o EV/EBITDA LTM (~30x) do motor usam o LTM contábil com só 1 mês de Vital e não servem como referência.
