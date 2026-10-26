# Revisão independente — VULC3 (Vulcabras) · 26/10/2026

**Veredito: ok.** Não achei erro objetivo. As premissas são coerentes com o CVM. Os desvios vão para os dois lados: IR conservador, e capital de giro e margem do 2S26 levemente otimistas. Nenhuma alteração em `research/VULC3.json`.

Preço de referência (foto B3): R$ 12,49. Saída do motor (inalterada):
- Valor justo **R$ 9,70** (DCF 7,79 · DDM 7,84 · múltiplos 15,41)
- TIR implícita **17,4%**
- TIR 3 anos **28,8%**

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +10 / 9 / 8 / 7 / 6,5% | 1S26 +11,0% (1.771 vs 1.596); CAGR 3a 12% | ok |
| Margem EBITDA | 20,8% → 21,5% | 2023 22,8%; 2024 22,5%; 2025 recorrente 21,4% (CVM 24,8% com créditos); 1S26 20,3%. O 2026 do modelo exige 21,2% no 2S26 (2S25 22,8%). | Levemente otimista em 2026 (insumos petroquímicos + câmbio); ver achado 2 |
| D&A | 3,7% | 2025 3,7%; 1S26 3,8% | ok |
| Capex | 4,8% → 4,7% | 2023 4,9%; 2024 6,7%; 2025 6,8% (expansão); 1S26 4,6%. Arrendamentos irrelevantes (passivo R$ 34 mi). Investimento líquido ~1,1% da receita, com imobilizado/receita ~18%. | ok |
| Capital de giro | 45% da receita incremental | Intensidade (receb. + estoques − fornecedores): 47% (2023), 51% (2024), 51% (2025), 51% (LTM). Marginal: 55% em 2024→25 e 66% em 2023→25. Estoques +19% no 1S26 (835 → 994). | Levemente otimista; ver achado 1 |
| IR | 8% → 14% | ETR 2021–24: 3–8%; 1S26 7,1%; IR pago 3–13%. IR diferido ativo de R$ 378 mi (prejuízos fiscais reconhecidos no 3T25) não entra como ativo. | Conservador; ver achado 3 |
| Resultado financeiro | 15,5% → 13% × DL | Modelo 2026 −94,7; real 1S26 −50,6 (anualizado −101) | ok |
| Payout | 25 / 60 / 75 / 80 / 80% | Proventos suspensos até a dívida zerar (~meados de 2027); 2023–25: 46–137% | ok. DL fica estável em ~0,5–0,6x EBITDA. |
| ROIC_T / ROE_T | 22% / 22% | Projetados para 2030: 19,7% / 21,3% | ROIC_T um pouco acima (−1% se igualado) |
| WACC | wd 8%, Kd 15% | DL 611 / (611 + valor de mercado pré-eleição 5.013) = 10,9% | Imaterial (+1% se 10,9%) |
| DL base / não operacional | 611,1 / +70 | 935,3 + 34,4 − 358,7; coligada a valor contábil (70,1), sem equivalência em `other_financial` | ok, sem dupla contagem |
| Ações | 314,11 mi | CVM 30/06/26 = 314,113 mi (pós-subscrição de dez/25); B3 idem | ok |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | R$ 9,70 | 17,4% | 28,8% |
| Capital de giro 55% | R$ 9,49 | 17,2% | 27,9% |
| Margem 2026 = 1S26 (20,3%) e −0,5 p.p. depois | R$ 9,36 | 17,0% | 26,6% |
| Margem −1 p.p. | R$ 9,01 | 16,6% | 24,4% |
| Margem +1 p.p. | R$ 10,40 | 18,3% | 33,2% |
| IR 7% fixo (histórico) | R$ 10,27 | 18,4% | 33,1% |
| IR → 20% em 2030 | R$ 9,32 | 16,7% | 26,1% |
| Crescimento −2 p.p. | R$ 9,26 | 16,5% | 24,8% |
| wd 10,9% | R$ 9,81 | 17,4% | 28,8% |
| ROIC_T 19,7% | R$ 9,63 | 17,4% | 28,8% |
| Custo da DL 16% fixo | R$ 9,66 | 17,2% | 27,8% |

A conclusão é robusta: o valor intrínseco a Ke 25% fica entre R$ 9,0 e 10,4, abaixo do preço de R$ 12,49, com TIR implícita de 16,5–18,5%. A TIR de 3 anos, de 24–33%, depende da saída a 8x P/L em 2028. Isso é reversão de múltiplo, coerente com o dossiê.

## Achados
1. **(baixa–média) Capital de giro marginal de 45%** contra 55–66% no histórico recente. Os estoques subiram 19% no 1S26 com a nova capacidade. Com 55%, o valor justo seria R$ 9,49. Não alterado.
2. **(baixa–média) Margem de 2026.** Fechar o ano em 20,8% exige 21,2% no 2S26, contra 20,3% no 1S26. Há custo de matéria-prima ainda não repassado (Oriente Médio) e o real caiu 9,5% sobre insumos petroquímicos. Os reajustes de preço desde o fim do 2T26 tornam a premissa plausível. Com 20,3% em 2026 e −0,5 p.p. nos anos seguintes, o valor justo seria R$ 9,36.
3. **(baixa, conservador) IR de 8% a 14%**, acima do ETR histórico de 3–8%. O ativo fiscal diferido de R$ 378 mi não é contado. Com 7% fixo, o valor justo seria R$ 10,27.
4. **(informativo) Dividendo de 2026.** O payout de 25% em 2026 gera ~R$ 67 mi no stub do 2S26, mas a gestão suspendeu proventos até zerar a dívida. Na prática, o mínimo do exercício deve ser pago em 2027. É só um efeito de timing, imaterial.
5. **(informativo) Referências distorcidas pelos não recorrentes de 2025 (R$ 592 mi).** O P/L LTM de 4,2x e a referência de Graham (R$ 23,71) usam o lucro LTM de R$ 930 mi, contra ~R$ 570 mi recorrentes. O motor não lê `overrides.base.ni_2025_recurring`. Nada disso entra no blend, mas o painel mostra esses números.

## Mudanças
Nenhuma.

## O que não deu para verificar
- Vigência dos incentivos SUDENE e ICMS (CE/BA) e renovação do antidumping sobre calçados chineses.
- Custo e prazo da dívida (debêntures de R$ 500 mi de jul/25).
- Repasse de preço no 2S26 (o 3T26 sai nos próximos dias).
