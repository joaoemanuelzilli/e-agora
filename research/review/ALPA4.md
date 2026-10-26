# Revisão independente — ALPA4 (Alpargatas) · 26/10/2026

**Veredito: ok.** Não achei erro de valuation. As premissas são coerentes com o CVM e, em geral, conservadoras. Corrigi só o texto de `dividend_policy`, que omitia a restituição de capital em dinheiro de R$ 839 mi de dez/25. Ela não muda o valor, porque já está na dívida líquida-base do 2T26. O original está em `research/review/ALPA4.orig.json`.

Preço de referência (foto B3, PN): R$ 12,99. Motor (inalterado):
- valor justo **R$ 6,53** (DCF 5,04, DDM 3,85, múltiplos 12,18);
- TIR implícita **11,3%**;
- TIR de 3 anos **7,5%**.

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +10,5 / 9 / 7,5 / 7 / 6,5% | 1S26 +11,9% (2.456 vs 2.194). O 2S26 implícito é +9,2%. CAGR 5a 7,8%. | ok |
| Margem EBITDA (CVM) | 21,5% fixa | 1S26 22,1%, ou 22,6% sem a equivalência da Rothy's (−11,6). 2025 18,7% (17,7% sem +46,3). 2S26 implícito 20,9%, contra 20,3% no 2S25. | ok; ligeiramente conservadora frente ao 1S26 |
| D&A | 5,0% | 2025 5,7% (DFC 217 + direito de uso 43,6); 1S26 4,9% | ok |
| Capex (com direito de uso) | 5,7% → 5,4% | Capex caixa 4,9% (2025) e 3,3% (1S26). Adições de direito de uso ~0,4%: o passivo caiu de 190 para 163 e depois 136. Orçamento 2026 R$ 243 mi. | Conservador |
| Capital de giro | 30% da receita incremental | Intensidade 30,5% (2024), 33,0% (2025), 33,4% (LTM). Marginal 56% em 2024→25, puxado por recebíveis +19%. | Levemente otimista; −2% se 40% |
| IR | 13% → 18% | ETR 2025 −1,8%, 1S26 12,6%. IR pago 14% (2025) e 5% (1S26). SUDENE/PB + JCP. | ok |
| Resultado financeiro | 13–13,5% × DL; equivalência 0 → +15 | Modelo 2026 −86,8; real 1S26 anualizado −83. Equivalência 2025 +46,3 e 1S26 −11,6. | ok |
| Rothy's (48,8%) | Não operacional R$ 550 mi (75% do contábil de 744,8) | Receita ~US$ 240 mi/ano, EBITDA US$ 6,5 mi no 2T26 | Razoável. A equivalência fica fora do FCFF; implicitamente vai no EBITDA histórico, mas pequena e de sinal variável. Sem dupla contagem material. |
| Payout | 45% → 55% | 2025: R$ 304 mi em proventos + R$ 839 mi de devolução de capital = 201% do lucro | Conservador (ver achado 2) |
| ROIC_T / ROE_T | 20% / 19% | Projetados para 2030: 18,5% / 18,1% | ok (−1% se igualados) |
| WACC | wd 7%, Kd 14,5% | DL 668 / (668 + ~10,2 bi pré-eleição) ≈ 6% | ok |
| DL base | R$ 667,7 mi | 1.265,9 + 135,5 − 733,7 (CVM 30/06/26) | ok |
| Ações | 679,2 mi | 683,06 mi − 3,86 mi em tesouraria (ON 337,6 + PN 341,6) | ok |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | R$ 6,53 | 11,3% | 7,5% |
| Payout 45 / 70 / 75 / 80 / 80% (≈100% do FCFE) | R$ 6,65 | 11,4% | 7,3% |
| Rothy's a valor contábil (745) | R$ 6,71 | 11,3% | 7,5% |
| Rothy's a R$ 300 mi | R$ 6,30 | 11,3% | 7,5% |
| Margem −1 p.p. | R$ 6,11 | 10,9% | 3,9% |
| Margem +1 p.p. | R$ 6,95 | 11,7% | 11,0% |
| Margem 21% → 20% | R$ 5,92 | 10,7% | 2,2% |
| IR 22% fixo | R$ 6,18 | 10,9% | 4,4% |
| Crescimento −2 p.p. | R$ 6,24 | 10,8% | 4,1% |
| P/L-alvo 13x | R$ 6,78 | 11,3% | 15,7% |
| Capital de giro 40% | R$ 6,40 | 11,2% | 6,8% |

A conclusão "cara para Ke 25%" é robusta. Em todos os casos o valor justo fica entre R$ 5,9 e 7,0, cerca de metade do preço, e a TIR implícita entre ~11% e 12%. Nem um P/L de saída de 13x leva a TIR de 3 anos a 25%.

## Achados
1. **(informativo, omissão factual) Devolução de capital de R$ 839 mi em dez/25.** O capital social caiu de R$ 3.906,9 mi para R$ 3.056,9 mi. A saída está na DFC 2025, linha 6.03.05, rotulada "Venda de Ações em Tesouraria" (−838,99). O dossiê cita só R$ 304 mi de proventos (payout 53%) e atribui a virada da DL (caixa líquido de R$ 229 mi no 3T25 → DL de R$ 828 mi no 4T25) ao JCP e à parcela Ioasys. Na verdade, ela se explica sobretudo por essa devolução. Não há efeito no valor, porque a saída já está na DL-base. Muda a leitura da política de distribuição: o retorno total em 2025 foi de 201% do lucro.
2. **(baixa, conservador) Payout de 45–55% com DL caminhando para caixa líquido de R$ 339 mi em 2030.** O caixa retido rende 12% contra Ke de 25%, e a perpetuidade embute payout de 74% (1 − g/ROE_T). Com ~100% do FCFE (70–80% do lucro), o valor justo vai a R$ 6,65 (+2%). Não alterado.
3. **(baixa) Capital de giro marginal de 30%**, abaixo da intensidade atual de 33% e do marginal de 2025 (56%). Com 40%, o valor justo vai a R$ 6,40.
4. **(informativo) Equivalência da Rothy's.** Ela está no EBIT CVM (conta 3.04.06) e, portanto, no EBITDA histórico. A margem de 21,5% foi calibrada no 1S26, quando a equivalência foi negativa (−11,6). Por isso não há dupla contagem relevante com os +5 a +15 de `other_financial` nem com o ativo não operacional de R$ 550 mi.
5. **(informativo) ALPA3 sem cotação na foto do estudo.** O motor calcula o valor de mercado com o preço da PN para as duas classes. Isso afeta só métricas exibidas (EV, EV/EBITDA), não o valor justo nem a TIR. O valor justo por ação vale para ON e PN; se a ALPA3 negocia com ~25% de desconto, a TIR do detentor de ON é maior.

## Mudanças
- `dividend_policy` (só texto). Antes: "em 2025 pagou R$ 304 mi (CVM)". Depois: em 2025, ~R$ 1,14 bi devolvidos em caixa, sendo R$ 304 mi de dividendos/JCP e R$ 839 mi de restituição de capital ("REST CAP DIN" na B3: R$ 1,254/ação, aprovada em 10/09/2025, paga em 19/12/2025). Isso dá ~200% do lucro e explica a virada da DL.
- Rodei de novo o motor (`EAGORA_SNAPSHOT=1`). Nada mudou: valor justo R$ 6,53, TIR implícita 11,3%, TIR de 3 anos 7,5%.
- `research/notes/ALPA4.md` continua com a omissão. Não editei, porque está fora do escopo de arquivos permitidos.

## O que não deu para verificar
- Passivo de derivativos de R$ 233 mi, tratado como hedge operacional: a perda adicional com o real −9,5% compensa parte do ganho de receita internacional nos próximos 12–18 meses.
- Contratos da Rothy's: opções e obrigações.
- Custo e prazo da dívida.
- Cotação da ALPA3 hoje.
