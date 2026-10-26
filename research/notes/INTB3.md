# INTB3 — Intelbras | dossiê G12 (26/10/2026)

**Preço:** R$ 13,45 às 11h54 (−31,8%; sexta R$ 19,72). 327,2 mi de ações → mercado ~R$ 4,4 bi. Caixa líquido de R$ 570 mi; risco sacado de R$ 369 mi.

## Negócio
- Fabricante nacional (São José/SC; expansão em Manaus) de três linhas, com mix de receita do 2T26:
  - Segurança eletrônica (CFTV, alarmes, controle de acesso): 60%
  - TIC (redes empresariais, cabeamento, comunicação): 25%
  - Energia (nobreaks, carregadores veiculares, solar): 15%
- Vende via distribuidores, instaladores e varejo, com foco em PMEs e consumo.
- Produção local com componentes majoritariamente importados (Ásia).
- Usa incentivos de produção local (Lei de TICs/PPB, ICMS).

## 2T26 (release de 28/07/2026)
| R$ mi | 2T26 | 1T26 | 2T25 |
|---|---|---|---|
| Receita líquida | 1.149,0 | 1.110,6 | 1.246,4 |
| Margem bruta | 33,1% | 30,7% | 29,3% |
| EBITDA | 168,9 (14,7%) | 156,3 (14,1%) | 154,4 (12,4%) |
| Lucro líquido | 158,3 | 153,1 | 136,3 |
| ROIC pré-IR LTM | 18,8% | 17,7% | 13,6% |

- A queda a/a é base de comparação: o 2T25 teve faturamento represado pela migração de ERP. O 1S26 cresceu +4,2%.
- A margem bruta subiu pela precificação a custo de reposição. A própria gestão diz que essa parcela é cíclica e vai normalizar.
- Por segmento: Energia −13,5% (saída deliberada de solar de baixa margem); TIC +7% (antidumping de cabos ópticos desde dez/25, com a fábrica no limite).
- Caixa operacional de R$ 318 mi no trimestre. Dívida bruta de R$ 860 mi (BNDES 325, FINEP 146, debêntures 359, bancos 30).

## Histórico (CVM)
- Receita: 2.134 / 3.087 / 4.233 / 4.104 / 4.756 / 4.460 (2020–25). CAGR 5 anos de 15,9%, mas CAGR 3 anos de só 1,8%.
- Margem EBITDA: 19,2% / 13,1% / 12,6% / 14,6% / 13,5% / 12,1%.
- Lucro: 328 / 364 / 480 / 544 / 529 / 483. ROE de 25% (2021) a 16% (2025).
- Alíquota efetiva de IR próxima de zero (incentivos/JCP).

## Câmbio — o ponto-chave
- CPV ~67% da receita, majoritariamente dolarizado. Um dólar +9,5% sustentado sobe o custo em ~4–5% da receita antes de repasse (estimativa própria; a empresa não divulga a % dolarizada).
- Mitigantes:
  - precificação a custo de reposição, com o estoque a custo antigo amortecendo por ~1–2 trimestres;
  - hedge (variação cambial líquida de só −R$ 6 mi/trimestre);
  - histórico de repasse em 2020–21 e 2024.
- O risco é de **volume**: demanda de PMEs e consumo com Selic alta e PIB de ~1,3% em 2027.

## Guidance e dividendos
- Sem guidance. Investimentos em Manaus em 2026–27.
- Dividendos: R$ 93,5 mi (R$ 0,2856/ação) pagos em 14/08/2026. Em 2025 foram R$ 460 mi (95% do lucro, com R$ 300 mi extraordinários).
- **3T26 sai em 28/10/2026** (após o fechamento).

## 4º mandato de Lula
- A favor: conteúdo local (Nova Indústria Brasil, antidumping, Zona Franca).
- Contra: reforma tributária encerra incentivos de ICMS até 2032; risco de fim do JCP; demanda.
- Juros: neutros no lucro (caixa líquido).
- A queda de −32% parece exagerada para o canal de juros, mas é coerente com o risco cambial no curto prazo.

## Premissas (research/INTB3.json)
- Crescimento: 4% / 5,5% / 7% / 7% / 6,5%.
- Margem EBITDA: 14,0% / 12,7% / 13,0% / 13,2% / 13,2%.
- Capex: 4,5% em 2026–27 (Manaus), depois 3%. Capital de giro: 30% da receita incremental.
- IR: 5% → 18%. Payout 60%.
- WACC 25% (sem dívida). g = 5%. Risco sacado tratado como item debt-like.

## Resultado do motor (pipeline/model.py, 26/10/2026, Ke 25%)
- Preço usado: R$ 14,25 | **valor justo R$ 8,23** (-42,2%) | TIR implícita 13,1% | TIR 3a 21,3%
- Métodos: DCF R$ 5,97 · DDM R$ 6,02 · P/L-alvo R$ 16,92 · EV/EBITDA-alvo R$ 13,04 (WACC 25,0%; EV DCF R$ 1.774 mi; TV 40,7% do EV)
- Projeção 2026–30: receita [4639, 4894, 5237, 5603, 5967]; EBITDA [649, 622, 681, 740, 788]; lucro controlador [600, 554, 573, 600, 618]
- DL/EBITDA [-1.0, -1.1, -1.2, -1.2, -1.3]; ROE ['18,7%', '15,7%', '15,2%', '15,0%', '14,6%']; FCFF [361, 286, 357, 374, 388]
- Cenários: bear R$ 6,52 · base R$ 8,23 · bull R$ 9,25 · esperado R$ 7,92 | Monte Carlo p10 R$ 6,51 · p50 R$ 8,22 · p90 R$ 10,15 · P(valor>preço) 0,0%
- **Leitura:** barata em múltiplos (~8x P/L 2027E, caixa líquido, DY ~7–8%), mas a TIR implícita (~13%) não chega a 25%. O lucro está inflado por IR quase zero e margem cíclica, e a receita está estagnada. **Neutra/armadilha leve:** o 3T26 (28/10) mostra se o câmbio vai ser repassado sem perda de volume.

## Fontes
- Release 2T26: https://api.mziq.com/mzfilemanager/v2/d/660c9d23-3bb0-4bd4-9707-c9fe5ad308b4/94c5df34-3998-9f71-9d8c-7160ca6df70e?origin=2
- Release 4T25: https://api.mziq.com/mzfilemanager/v2/d/660c9d23-3bb0-4bd4-9707-c9fe5ad308b4/b803062b-5c59-d8f2-643f-e472fd3106c4?origin=2
- RI (agenda do 3T26): https://ri.intelbras.com.br/
- CVM: data/hist/INTB3.json. **Problema de dados:** `ltm.ni_controlling` = 284,9, quando a soma dos trimestres dá ~597. O P/L LTM do motor (~15–16x) está errado; o correto é ~7,4x.
