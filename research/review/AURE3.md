# AURE3 (Auren Energia): revisão independente (red team G11, 26/10/2026)

**Veredito: ok.** Não mudei nenhuma premissa. A conclusão (valor justo muito abaixo do preço com Ke de 25%) se sustenta em todas as variantes plausíveis que testei.

Motor (foto B3 a R$ 10,29): VJ **R$ 1,56**, TIR implícita **6,9%**, sem TIR de 3 anos (P/L-alvo nulo, justificado). Métodos: DCF −R$ 4,88 (piso 0 no blend, peso 50%), DDM R$ 0,94, EV/EBITDA R$ 5,29.

## O que conferi e bate
- **Ações**: a base CVM já corrige a escala (cvm_scale 1000; 1.044,6 mi em circulação). O override `shares_outstanding_mn` = 1.044,635 é redundante, mas inócuo. Market cap: R$ 10,29 × 1.044,6 = R$ 10.749 mi, igual ao do motor. A nota "base em milhares" está desatualizada.
- **Dívida líquida**: o motor usa a DL CVM de R$ 20.015 mi, com R$ 163 mi de arrendamentos (2.01.04.03 + 2.02.01.03). Somando os derivativos (R$ 159 mi) e tirando as contas-reserva (R$ 1.101 mi), chega-se a R$ 19.073 mi. A DL da companhia é R$ 18.907,5 mi, que mais os arrendamentos dá R$ 19.070 mi. Não há dupla contagem: os derivativos não estão em 2.01.04/2.02.01.
- **Participações e equivalência**: as participações entram a valor contábil (R$ 2.043 mi) em `non_operating_assets`, e a equivalência (R$ 230–270 mi) em `other_financial`. Esta segunda linha não entra no FCFF, então não há dupla contagem no DCF, e a margem EBITDA é ex-dividendos. A coerência vale nos três métodos. A equivalência é menor que os dividendos recebidos (R$ 383 mi em 2025), o que é conservador.
- **Base 2026**: o LAIR 2026E (−R$ 794 mi) bate com o LAIR LTM (−R$ 775 mi). Resultado financeiro mais equivalência: 2026E −R$ 2.212 mi contra LTM −R$ 2.149 mi. D&A: R$ 1.891 mi contra R$ 1.875 mi.
- **Custo da DL** (12,2%): o LTM é coerente (R$ 2.442 mi contra R$ 2.379 mi). O mix é 67% IPCA e 21% CDI, e o caixa rende CDI. Ou seja, o CDI pesa pouco: +100 bp ≈ −R$ 35 mi.
- **Capex** de 3–5% da receita (R$ 420–675 mi): Cajuína 3 está em 83%, sem expansão nova. É compatível com manutenção de 7,5 GW.

## Achados
| # | Severidade | Achado | Evidência / impacto |
|---|---|---|---|
| 1 | Média | O custo da DL cai de 12,2% para 10,9% em 2030, ancorado no IPCA Focus de antes do choque. Com a curva de hoje (DI1F29 15,4%, IPCA esperado subindo), a queda é otimista. | Kd plano em 12,2%: VJ 1,48 / TIR 5,9%. Kd ~12,5%: 1,49 / 6,0%. Base: 1,56 / 6,9%. Mantive a base porque a parcela IPCA é casada com contratos IPCA e o próprio dossiê traz essa sensibilidade (1,52 / 6,4%). |
| 2 | Média (não verificável) | O prazo das concessões do complexo Tietê (ex-AES; vencimento original em 2029, mais a extensão do GSF) não foi confirmado. A perpetuidade com g de 3,5% sobre GF hídrica constante pode superestimar o valor. | Se as concessões acabarem por volta de 2032, o valor cai ainda mais. O viés da conclusão é para baixo, então ela fica mais robusta, não menos. |
| 3 | Baixa | O IR é zero em ano de prejuízo (o motor usa max(0, LAIR)). A companhia pagou R$ 255 mi no LTM com LAIR negativo, porque a tributação é por entidade. Mas o 1S26 teve crédito líquido de R$ 51 mi. | Vazamento de IR de R$ 150 mi/ano em 2026–27: VJ 1,53 / TIR 6,7%. |
| 4 | Baixa | Minoritários a 5% do LL absorvem prejuízo. No histórico, os minoritários lucram mesmo com o consolidado no vermelho (R$ 106 mi em 2025, R$ 60 mi no LTM). | Minoritários a 10%: VJ 1,54 / TIR 6,7%. |
| 5 | Metodológica | O DCF fica negativo (EV R$ 15,0 bi contra direitos de R$ 20,1 bi) e entra no blend como zero com peso de 50%. O WACC é 16,6% e o EV/EBITDA de saída implícito, 2,3x. | Tirando o DCF e renormalizando: VJ ≈ R$ 3,1. Continua ~70% abaixo do preço. |
| 6 | Baixa | O D&A inclui a amortização da mais-valia da AES, que não é caixa nem precisa ser reposta. Isso deprime o NOPAT terminal e o LL. | D&A ex-PPA (−3 p.p.) com wd 0,56: VJ 1,70 / TIR 8,4%. |
| 7 | Baixa | O dividendo de 2028E (R$ 14 mi) só existe se o prejuízo acumulado (−R$ 1.032 mi no 1S26) for absorvido antes. | Imaterial. |

## Sensibilidade (motor em memória, preço da foto)
| Variante | VJ (R$) | TIR implícita |
|---|---|---|
| Base | 1,56 | 6,9% |
| Margem 27,2% desde 2027 (FY25 ex-dividendos) | 1,88 | 7,4% |
| EV/EBITDA-alvo 8x | 2,43 | 6,9% |
| Tudo otimista (wd 0,56; D&A ex-PPA; margem 27,2%; 8x; g 4,5%; ROIC_T 13%) | 2,92 | 9,3% |
| Capex 4,5–5% | 1,53 | 6,6% |

A conclusão é robusta. Nenhuma combinação razoável leva o valor justo para perto de R$ 10, nem a TIR para perto de 25%. O preço implica Ke de mercado de ~13–14%: EV/EBITDA 2027E pré-eleição de ~9,9x, e de 8,8x hoje.

## Mudanças
Nenhuma. VJ **R$ 1,56** e TIR **6,9%** antes e depois.

## O que não deu para verificar
- O prazo final das concessões do complexo Tietê e de Porto Primavera.
- A regra de curtailment pós-nov/2025.
- A curva forward de energia de 2029–30.
- O consenso de mercado.
- O EBITDA ajustado do 3T26 (resultado ainda não saiu).
