# EQTL3 (Equatorial): revisão independente (red team G11, 26/10/2026)

**Veredito: ajustada.** Duas premissas eram incoerentes com o histórico CVM e com o preço de mercado; corrigi as duas. Também corrigi um fato desatualizado do dossiê: a renovação de Pará e Maranhão. A conclusão se mantém: holding alavancada, com TIR de dono muito abaixo de 25%.

| | Antes | Depois |
|---|---|---|
| Valor justo (R$/ação) | 5,62 | **5,15** |
| TIR implícita | 7,8% | **7,2%** |
| TIR 3 anos | −26,9% | **−35,5%** |
| LL controlador 2026E / 2030E (R$ mi) | 1.053 / 2.302 | 805 / 1.760 |
| Monte Carlo p10 / p50 / p90 | 3,58 / 5,61 / 7,71 | 3,44 / 5,15 / 6,92 |

Preço da foto: R$ 35,89; 1.255,1 mi ações; market cap R$ 45.045 mi (confere).

## Achados com correção
| # | Severidade | Achado | Evidência | Mudança e impacto |
|---|---|---|---|---|
| 1 | **Alta** | Minoritários a 15% do LL, sem relação com o histórico. | CVM: minoritários de 28,5% / 27,9% / 25,4% / 33,0% do LL em FY22–25, 45,8% no LTM. 1S26: R$ 350 mi (182 + 168), ou 34% do LL ex-ganho do Acordo Gaúcho, ~R$ 700 mi/ano. Com 15%, o modelo dava R$ 186 mi em 2026E e R$ 222 mi em 2027E. Os minoritários (Equatorial Maranhão, PNs da Equatorial Distribuição corrigidas por CDI) não pagam os juros da holding, por isso sua fatia sobe quando o LL consolidado cai. | `minority_share_ni` 0,15 → **0,35**. Isolado: VJ 5,62 → 5,05, TIR 7,8% → 7,2%. Com 35%, 2026–27E ainda ficam abaixo do run-rate (R$ 434 / 519 mi contra ~700); 2030E fica coerente. |
| 2 | Média | Copasa marcada fora do critério usado para a Sabesp. | A Sabesp entrou a mercado × 0,7. A Copasa entrou pelo custo (R$ 5,6 bi) × 0,75 ("queda do setor") × 0,7 = R$ 2,94 bi. Mas os 30% valem a mercado R$ 5,81 bi hoje (113,75 mi × R$ 51,07, já depois de −21% no dia), acima do custo. O −25% era penalidade em dobro. | `non_operating_assets` 12.600 → **13.615**: Sabesp 528,7 mi × R$ 25,80 × 0,7 = 9.548; Copasa × 0,7 = 4.067. Isolado: VJ +0,10. |
| 3 | Média (fato) | O dossiê trata a renovação das concessões do Pará (vencimento em 2028) e do Maranhão (2030) como "principal risco micro do 4º mandato, status não verificado". | O MME assinou os aditivos em 04/05/2026: Pará até 28/07/2058 e Maranhão até 11/08/2060. A Parcela B passou de IGP-M para IPCA em 01/06/2026, e o reajuste do Maranhão de +5,76% saiu em ago/2026. | Nota adicionada em `election_impact`. Sem efeito numérico no caso-base; o cenário bear (30%) está carregado num risco que já não existe. |

## Conferido e coerente
- Receita-base de R$ 40.679 mi: ROL de R$ 52.074 mi, menos construção de R$ 10.706 mi, menos VNR de R$ 689 mi. Transmissão descontinuada e fora da base.
- A margem de 26,5% em 2026E bate com o EBITDA ajustado ex-equivalência do 2T26 (R$ 2.695 mi, +4% a/a).
- O custo da DL de 13,0% × R$ 53.508 mi = R$ 6.956 mi, sem `other_financial`, igual ao resultado financeiro ajustado do 2T26 anualizado (R$ 6.996 mi).
- O D&A de 8,8% bate com o run-rate do 2T26 (R$ 944 mi/tri).
- O capex de 20% bate com o capex da DFC (R$ 8,1 bi LTM).
- A equivalência de Sabesp e Copasa entra só nos métodos de LL (dividendos + ½ do retido), e as participações entram só no DCF e no EV/EBITDA. Não há dupla contagem entre métodos.

## Sem mudança (sensibilidades já com a correção)
- **Curva**: a de hoje (custo da DL ~14,5%) dá VJ 4,54 e TIR 6,4%. A pré-eleição dá 5,66 e 7,6%.
- **Desconto de 30% nas participações**: é julgamento do analista. Sem desconto, VJ 5,73.
- **DCF**: é negativo (−R$ 15,6/ação; WACC de 18,2% contra ROIC projetado de ~8%) e entra como zero com peso de 50%. Sem o DCF, VJ 10,3. Mesmo assim, a ~70% do preço.
- **`minority_value` de R$ 4,0 bi** (contábil R$ 2,6 bi): coerente com ~R$ 700 mi/ano de LL minoritário a Ke de 25%.
- **Alavancagem**: DL/EBITDA ex-equivalência de 4,8x → 4,4x, sem emissão de ações. É um risco de covenant não modelado. Se faltar equity, o viés é para baixo.
- **Coerência cruzada com a SBSP3**: os 15% da Sabesp entram a mercado × 0,7 (R$ 9,55 bi). Pelo valor justo do próprio modelo da SBSP3 a Ke de 25% (R$ 5,36/ação), seriam R$ 2,83 bi. Com isso, o VJ da EQTL3 cai para 4,48; a TIR não muda (7,2%). O efeito fica todo no EV/EBITDA, porque o DCF já é negativo. Não alterei: a marcação a mercado dentro do método de múltiplos é defensável. Mas o "desconto de 30% por coerência com Ke 25%" subestima a distância entre mercado e valor justo.

## O que não deu para verificar
- O % exato da dívida em CDI (o analista estimou 55%).
- Os termos das PNs da Equatorial Distribuição.
- Os dividendos esperados de Sabesp e Copasa.
- O consenso.
