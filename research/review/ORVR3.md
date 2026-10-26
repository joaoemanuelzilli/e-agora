# Revisão independente — ORVR3 (OrizonVR) · 26/10/2026

**Veredito: ajustada** (2 correções pequenas; um ponto metodológico relevante mantido e sinalizado). Original em `research/review/ORVR3.orig.json`.

Preço de referência (foto B3 13h02): R$ 15,58.

| | Antes | Depois |
|---|---|---|
| `other_debt_like` | R$ 30 mi | **R$ 75 mi** |
| `overrides.base.equity_controlling_2025` | — (CVM legado R$ 1.442 mi) | **R$ 4.851,7 mi** (PL combinado de 30/06/26) |
| Valor justo | R$ 5,47 | **R$ 5,42** (−0,9%) |
| DCF / DDM / P/L / EV/EBITDA | 1,96 / 2,46 / 12,53 / 18,45 | 1,89 / 2,46 / 12,53 / 18,38 |
| TIR implícita | 9,6% | **9,6%** |
| TIR 3 anos | 13,9% | **13,9%** |
| ROE 2026E / 2027E / 2028E | 10,7% / 7,6% / 9,0% | **7,0%** / 7,6% / 9,0% |

## Contagem de ações e diluição (ok)
- CVM 30/06/26: 137.324 mil ações (pré-desdobramento). Desdobramento 1:4 em 11/08/26: B3 = 549,30 mi (= 137,324 × 4,00000). O pipeline detecta isso (`b3_vs_cvm` = 4,0).
- Override de 624,9 mi = 549,3 + 75,6 mi dos bônus ORVR11 (75,6 × R$ 13,2325 = R$ 1.000 mi). O tratamento é consistente: os R$ 840 mi (valor presente a 25% de R$ 1.000 mi em ~0,8 ano) entram como ativo não operacional no DCF e no EV/EBITDA, que usam DL anterior à emissão. Os R$ 1.000 mi de `equity_issuance_mn` em 2027 só reduzem a DL projetada (DDM/P/L). Não há dupla contagem.
- O exercício a R$ 13,23 é acretivo ao valor intrínseco (~R$ 4,7 sem bônus). Sem exercício (549,3 mi, sem os R$ 840 mi e sem a emissão), o valor justo seria R$ 5,20. A conclusão não muda. O cenário bear cita "bônus não exercidos", mas só desloca crescimento e margem.

## Achados
1. **(média — mantido) Minoritários de R$ 1.200 mi aplicados igualmente ao DCF e ao EV/EBITDA.** No DCF, o equity consolidado operacional é ~R$ 1.584 mi (EV 3.483 − DL 2.339 − 30 + recebível Ecourbis 470). Deduzir R$ 1.200 mi atribui ~76% dele a quem tem ~23% do lucro. No EV/EBITDA a 9x, porém, os R$ 1.200 mi são pouco (~9% do equity implícito). Como o motor aceita um valor só, o valor "neutro" ponderado pelos pesos (DCF 50%, EV/EBITDA 12,5%) fica entre ~R$ 840 mi (minoritários pró-rata no equity) e ~R$ 1.420 mi (SPEs sem dívida, com a dívida na controladora). Os R$ 1.200 mi estão dentro dessa faixa, por isso não alterei. Efeito: minoritários a R$ 841 mi → valor justo R$ 5,83; a R$ 401 mi (contábil) → R$ 6,27. **Efeito colateral:** o DCF isolado (R$ 1,89) é artefato dessa escolha e não deve ser lido sozinho.
2. **(baixa — corrigido) Parcelamento de impostos fora do debt-like.** A CVM traz R$ 22,9 mi (CP) + R$ 22,6 mi (LP) de parcelamentos, que a especificação manda tratar como debt-like. Só as outorgas (R$ 29,2 mi) estavam incluídas. Novo `other_debt_like` = R$ 75 mi. Efeito no valor justo: −R$ 0,05.
3. **(baixa — corrigido) Perímetro errado no PL-base de 2025.** A receita-base é pró-forma combinada (R$ 3.400 mi), mas o ROE de 2026 usava o PL de 31/12/25 só do legado (R$ 1.442 mi) contra PL de ~R$ 5,0 bi depois da incorporação. Isso inflava o ROE 2026E para 10,7%; o certo é 7,0%. O dashboard usa a média do ROE 2026–28 (9,1% → 7,9%). Valor justo e TIR não mudam.
4. **(média — não verificado) Passivos lançados na conta de dívida e excluídos da DL.** O override de DL (R$ 2.339 mi = dívida 3.785,5 − caixa 1.544,3 + arrendamentos 97,7) confere com a CVM. Os R$ 276 mi excluídos são impostos e contribuições a recolher LP (R$ 257,1 mi) e fornecedores LP (R$ 19,1 mi). Junto com débitos com partes relacionadas LP de R$ 184,3 mi (novos, vindos da Vital), a natureza deles não está clara: podem ser parcelamentos ou mútuos de sócios (debt-like) ou tributos diferidos sobre recebíveis (operacional). Se fossem todos debt-like (+R$ 506 mi), o valor justo cairia para ~R$ 4,96.
5. (baixa) Margem EBITDA de 32% em 2026 (que é o que vale para o stub do 2S26) contra 28,7% no 2T26 pró-forma (−5 p.p. a/a) e ~33,7% no LTM pró-forma. A expansão até 37,5% depende do biometano (7 plantas), do LRCAP e de sinergias. Com margem 2 p.p. menor em todos os anos: valor justo R$ 4,76, TIR 3a 8,5%.
6. (baixa) ROE terminal de 15% contra ROE projetado de 10,8% em 2030 (PL inflado por ágio da incorporação). Com ROE_T de 11%: valor justo R$ 5,37, TIR implícita 8,8%.
7. (baixa) `kd_pre_tax` de 15,5% e custo da DL de 13–15% em 2029–30 abaixo da curva DI (~15,4–15,7% + spread; parte da dívida da Vital é prefixada a >15%). Com os valores da curva: valor justo R$ 5,32, TIR 3a 12,0%.
8. (informativo) P/L LTM (193,8x) e EV/EBITDA LTM (24,3x) da vitrine usam o LTM contábil com 1 mês de Vital e não servem como referência (o dossiê já avisa).

## Outras checagens (ok)
- Receita 2026E de R$ 3.961 mi (+16,5%) contra 2T26 pró-forma anualizado de R$ 3.927 mi. Legado +32% a/a no 2T26, Vital +10,4%.
- Capex de 30% → 12% da receita contra legado de 60% da receita em 2024–25 e 1S26 de R$ 402 mi. Capex terminal (12%) acima do D&A (9,5%): coerente com crescimento.
- IR de 28–30% contra efetivo do legado de 23,7–29,3%. Payout de 0% → 40%, coerente com os prejuízos acumulados de −R$ 720 mi.
- Recebível da Ecourbis (R$ 784 mi, IPCA, 120 parcelas) a R$ 470 mi equivale a desconto de ~14,5% a.a. Razoável para risco Prefeitura de SP; a 25% seria ~R$ 314 mi (−R$ 0,16 no valor justo).

## Sensibilidade (valor justo / TIR implícita / TIR 3a; antes das correções)
| Teste | Valor justo | TIR impl. | TIR 3a |
|---|---|---|---|
| Base original | 5,47 | 9,6% | 13,9% |
| Sem exercício dos bônus | 5,20 | 9,7% | 14,3% |
| Minoritários R$ 841 mi / R$ 401 mi | 5,83 / 6,27 | 9,6% | 13,9% |
| Margem −2 p.p. | 4,76 | 9,2% | 8,5% |
| Debt-like +R$ 506 mi | 4,96 | 9,6% | 13,9% |
| ROE_T 11% | 5,37 | 8,8% | 13,9% |
| Minoritários 30% do lucro | 5,27 | 9,2% | 9,0% |

Conclusão robusta: em nenhum teste a TIR implícita passa de ~10% ou o valor justo se aproxima do preço. A queda é custo de capital e o ativo é "caro" a Ke 25% (ROIC de ~10–13% no ciclo de capex, abaixo do WACC de 21%).

## O que não deu para verificar
- Receita e EBITDA anuais da Vital em 2025 (base pró-forma estimada a partir do 2T25).
- Onde está a dívida (controladora × SPEs com minoritários), que define o valor econômico dos minoritários.
- Natureza dos R$ 257 mi de impostos LP e dos R$ 184 mi de partes relacionadas LP.
- Se os 5,6 mi de bônus (pré-split) entregues à Growth estão dentro dos 75,6 mi do ORVR11 ou são adicionais.
