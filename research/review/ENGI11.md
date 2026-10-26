# ENGI11 (Energisa): revisão independente (red team G11, 26/10/2026)

**Veredito: ajustada.** Corrigi uma dupla contagem objetiva na venda da transmissão para a Taesa. A conclusão não muda: com Ke de 25% e dívida ~100% CDI, o equity vale muito menos que o preço.

| | Antes | Depois |
|---|---|---|
| Valor justo (R$/unit) | 11,24 | **9,87** |
| TIR implícita | 8,6% | **8,1%** |
| TIR 3 anos | −14,9% | **−21,5%** |
| LL controlador 2030E (R$ mi) | 1.550 | 1.316 |
| DL/EBITDA 2030E | 4,0x | 4,2x |
| Monte Carlo p10 / p50 / p90 | 7,66 / 11,22 / 14,88 | 6,36 / 9,86 / 13,45 |

Preço da foto: R$ 47,14/unit. Unit = 1 ON + 4 PN; 2.515,3 mi ações = 503,1 mi units equivalentes. O market cap de R$ 23.715 mi confere.

## Achado principal (grave no método, moderado no valor): venda da transmissão contada duas vezes
Os fatos: Taesa compra 5 concessões. EV R$ 2.293 mi; equity ~R$ 1.545 mi; dívida líquida das SPEs R$ 748 mi; RAP ~R$ 291 mi, cerca de 27% da RAP do segmento. A operação depende de Aneel e Cade (Fato Relevante de 21/05/2026; release 2T26).

1. **DL-base.** O analista usou DL CVM de R$ 32.879 mi menos R$ 2,1 bi, lendo os "0,2x" do release como redução futura de R$ 2,1 bi. Só que, no 2T26, as SPEs já estavam como mantidas para venda (IFRS 5): ativos de R$ 3.021 mi (1.01.08.01) e passivos de R$ 1.313 mi (2.01.07.01), fora das contas 2.01.04 e 2.02.01. A DL da companhia (R$ 32.530 mi) reconcilia com a dívida CVM + derivativos − créditos setoriais (R$ 2.859 mi), sem a dívida das SPEs. Os "0,2x" são o efeito total (2.293 / EBITDA covenants 10.664 = 0,215x), e a parte da dívida das SPEs já saiu na reclassificação. No fechamento entra só o equity. DL-base: **32.879 − 1.545 = R$ 31.334 mi**, antes 30.779 (+R$ 555 mi).
2. **EBITDA dos ativos vendidos continuava na base.** A receita e o EBITDA "ajustados" do release incluem a transmissão regulatória inteira. O caixa da venda abatia a DL e, ao mesmo tempo, o EBITDA de ~R$ 210 mi/ano (74% da RAP; EBITDA regulatório do segmento de R$ 334 mi no 6M26 para RAP de R$ 450 mi) seguia projetado. Correção: `revenue_2025` 29.384,6 → **29.129,6** (ROL ~R$ 255 mi). Margem de [27,0; 28,0; 28,5; 29,0; 29,0]% para **[26,53; 27,56; 28,08; 28,61; 28,62]%**. O EBITDA removido é de R$ 219 → 257 mi, corrigido por IPCA. capex% e D&A% foram reescalonados para manter os valores em R$, porque os ativos estão operacionais e o D&A societário deles é ~0.

Impacto isolado: só a DL leva o VJ a 10,87; só o EBITDA, a 10,14; as duas juntas, a 9,87. A venda a ~10,9x EV/EBITDA cria valor contra o múltiplo-alvo de 6,5x, mas o modelo não pode ficar com o caixa e com o EBITDA.

## Outros achados (sem mudança)
| # | Severidade | Achado | Evidência / sensibilidade (já com a correção) |
|---|---|---|---|
| 2 | Média | Minoritários a 22% do LL. Depois da compra da EPM, os minoritários caíram para R$ 91 mi no 2T26 (−61%). Mas o Itaú entrou com 9,98% da Denerge (R$ 1,4 bi, 29/06/2026), e o PL de minoritários subiu de R$ 1.986 para R$ 3.485 mi. Com o lucro consolidado deprimido por juros da holding, a fatia dos minoritários tende a ficar acima do peso contábil deles (15%). | Minoritários a 28%: VJ 9,53 / TIR 7,9%. Não alterei porque os direitos econômicos da PN Denerge não foram verificados. |
| 3 | Média | Custo da DL de CDI + 1,2 p.p., com CDI de 13,9% → 14,5% → 13,0%: "metade do choque". A calibração bate com o resultado financeiro recorrente do 1S26 (~R$ 4,5 bi/ano). | Curva de hoje (CDI ~15–15,4%): VJ 8,77 / TIR 6,6%. Curva pré-eleição: 11,16 / 8,6%. |
| 4 | Baixa | `other_financial` de +R$ 250–290 mi não está documentado. A equivalência explica ~R$ 150 mi/ano (1S26: 78; ela fica fora do EBITDA ajustado). O resto (~R$ 100 mi) pode ser receita moratória já embutida na calibração do custo. | other_financial de 150–190: VJ ≈ 9,6 / TIR ≈ 7,9%. |
| 5 | Baixa (motor) | O stub do DDM começa em 30/06, então o dividendo de R$ 251,5 mi pago em 24/08 conta como recebível para quem compra hoje (R$ 0,50/unit). O DCF já o desconta em `other_debt_like`. | ~−R$ 0,13/unit no VJ. Afeta todo o universo, não corrigi aqui. |
| 6 | Metodológica | DCF negativo (−R$ 34/unit): WACC de 18,4% contra ROIC projetado de ~9% e retorno regulatório de ~12% nominal. Todo capex destrói valor a esse WACC. O DCF entra como zero com peso de 50%. | Sem DCF (DDM/múltiplos 50/50): VJ 19,7. Múltiplos no topo (13x / 7,5x): 12,6. Nada se aproxima de R$ 47. |
| 7 | Ok | Receita +6,5–7% (2025: +7,4%; 1S26: +6%; reajustes do 2S26 de +7,9% a +9,6%). Margem 2026 coerente com o 1S26 (26,9%). Capex de 22% → 18% (2025: 22,6%). IR de 22–25% (SUDAM/SUDENE). Payout de 50% contra o mínimo de 25% (payout de 25%: 9,51). Retorno incremental EBITDA/capital de ~17%, compatível com a lógica de BRR. | — |

## O que não deu para verificar
- O direito econômico da PN Denerge do Itaú: dividendo prioritário ou proporcional, e preço da call.
- A data de fechamento e a correção pelo CDI do preço da venda à Taesa. Somariam ~R$ 50–130 mi ao caixa.
- Os prazos de ETO, EMR, ESS, ERO e EAC.
- O consenso.
- O resultado do 3T26.
