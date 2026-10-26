# TTEN3 — 3tentos | dossiê G12 (26/10/2026)

**Preço:** R$ 11,32 às 11h54 (−19,9%; sexta R$ 14,14). 500,4 mi de ações → mercado ~R$ 5,7 bi. Free float 22,6% (família Dumoncel).

## Negócio
- Ecossistema agro em três segmentos:
  - Insumos: 81 lojas (59 RS, 14 MT, 3 GO, 2 PA, 2 MG, 1 TO); fertilizantes 71% da receita do segmento.
  - Grãos: originação de soja, milho e trigo.
  - Indústria: esmagamento de soja em Cruz Alta/RS e Vera/MT; biodiesel em Ijuí/RS e Vera/MT; **etanol de milho em Porto Alegre do Norte/MT**, operando desde mai/26 e na capacidade nominal de 2.800 t/dia desde ago/26.
- Também tem a TentosCap, com carteira de crédito de R$ 424,5 mi (+78%).
- Plano anunciado: 2ª planta de etanol em Redenção/PA e novas lojas em PA, TO, GO e MG.

## 2T26 (release de 13/08/2026)
| R$ mi | 2T26 | 2T25 | 6M26 | 6M25 |
|---|---|---|---|---|
| Receita líquida | 4.700,4 | 3.562,9 | 8.907,3 | 7.062,0 |
| EBITDA CVM | 204,6 | 330,2 | 343,3 | 494,9 |
| EBITDA aj. c/ hedge | 78,7 (1,7%) | 220,5 (6,2%) | 472,9 (5,3%) | 419,1 (5,9%) |
| Lucro líquido | 205,9 | 330,8 | 291,1 | 523,3 |
| Lucro ajustado (ex-AVJ) | 14,4 | 104,5 | 245,3 | 214,1 |

- A indústria comprimiu: margem bruta ajustada de 12,2% contra 21,7%. Causas: rentabilidade do biodiesel (B16), farelo −12%, custo de insumos com a guerra e suspensão de PIS/COFINS.
- Insumos (+25%) e grãos (+76%) fortes.
- Dívida líquida R$ 3.576 mi (pico sazonal de estoque de soja), **3,05x o EBITDA ajustado ex-TentosCap, com waiver de covenant para 2T26–4T26**.

## Histórico (CVM)
- Receita: 3.112 / 5.339 / 6.886 / 8.999 / 12.826 / 16.424 (2020–25), CAGR 39,5%.
- EBITDA ajustado c/ hedge: R$ 1.002 mi em 2024 (7,8%) e R$ 1.025 mi em 2025 (6,2%). O EBITDA CVM oscila com AVJ e hedge.
- Lucro CVM: 246 / 430 / 571 / 575 / 759 / 816. ROE 19–29%.
- Payout de caixa de 6–12%, porque a reserva de incentivos fiscais reduz a base.
- Capex: R$ 1,7 bi em 2025, recorde.

## Juros, câmbio e crédito
- Dívida bruta R$ 5,1 bi, majoritariamente de curto prazo (R$ 2,16 bi), em capital de giro, crédito rural e CRA. Custo não detalhado no release.
- Dólar alto: eleva o preço de grãos em R$ e o custo de fertilizantes. Líquido levemente positivo via renda do produtor.
- Selic alta: pressiona o crédito ao produtor e a equalização do Plano Safra, num momento de recuperações judiciais no agro em 2025–26.

## 4º mandato de Lula
- A favor: mandato de biodiesel (B15→B20 pela Lei do Combustível do Futuro) e apoio ao etanol de milho.
- Contra:
  - intervenção em preço de combustíveis (a suspensão de PIS/COFINS afetou o 2T26)
  - custo fiscal do Plano Safra com juros altos
  - possível tributação de LCA/agro
- A queda de −20% (a menor do grupo) é coerente com o beta.

## Premissas (research/TTEN3.json)
- Dívida líquida normalizada em R$ 2.700 mi, contra R$ 3.749 mi no pico da CVM; a média de 4 trimestres é R$ 2.463 mi.
- Crescimento: 18% / 12% / 8% / 7% / 6,5%.
- Margem EBITDA (ajustada c/ hedge): 5,6% → 6,7%.
- Capex: 5,2% → 2,2%. Capital de giro: 15% da receita incremental.
- Custo da dívida: 14% (+R$ 100 mi/ano de AVP). IR: 18% → 22%. Payout: 15% → 35%.
- WACC 20,4%. g = 5%.

## Resultado do motor (pipeline/model.py, 26/10/2026, Ke 25%)
- Preço usado: R$ 11,35 | **valor justo R$ 3,46** (-69,5%) | TIR implícita 12,2% | TIR 3a 6,1%
- Métodos: DCF R$ -0,16 · DDM R$ 3,34 · P/L-alvo R$ 10,34 · EV/EBITDA-alvo R$ 10,67 (WACC 20,4%; EV DCF R$ 2.624 mi; TV 84,6% do EV)
- Projeção 2026–30: receita [19380, 21706, 23442, 25083, 26713]; EBITDA [1085, 1411, 1547, 1681, 1790]; lucro controlador [503, 647, 682, 763, 835]
- DL/EBITDA [2.9, 2.6, 2.6, 2.4, 2.2]; ROE ['10,2%', '11,8%', '11,4%', '11,7%', '11,8%']; FCFF [-526, -133, 213, 518, 634]
- Cenários: bear R$ 2,02 · base R$ 3,46 · bull R$ 5,23 · esperado R$ 3,38 | Monte Carlo p10 R$ 1,88 · p50 R$ 3,54 · p90 R$ 6,80 · P(valor>preço) 0,4%
- **Leitura:** crescimento real (30 trimestres seguidos) e o etanol podem melhorar a margem, mas a 25% de Ke o ciclo de capex e o capital de giro (FCFF negativo em 2026–27) e o ROIC de ~13% derrubam o DCF. TIR implícita ~12%; alavancagem com waiver. **Não é oportunidade a 25%.** A queda de −20% é a mais 'justa' do grupo.

## Fontes
- Release 2T26: https://api.mziq.com/mzfilemanager/v2/d/050fef26-7d75-4607-8a2b-bd8cd509d0c7/d4b27ac0-b355-9310-603c-1efb1a0c3307?origin=2
- Release 4T25: https://api.mziq.com/mzfilemanager/v2/d/050fef26-7d75-4607-8a2b-bd8cd509d0c7/4ee6b235-6f1c-f92f-0cc3-66ef9a599b2e?origin=2
- CVM: data/hist/TTEN3.json. O EV/EBITDA LTM do motor (~19x) usa o EBITDA CVM sem hedge (R$ 507 mi). No conceito ajustado da empresa é ~8,6x.
