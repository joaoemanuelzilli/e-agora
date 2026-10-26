# Revisão independente — SBFG3 (Grupo SBF) · 26/10/2026

**Veredito: ajustada.** O bridge do equity tinha dois erros objetivos, os dois no sentido de inflar o valor:
- R$ 341,3 mi de parcelamentos de tributos ficaram de fora. A spec manda tratá-los como debt-like.
- R$ 125,0 mi de dividendos a pagar, já entregues a acionistas anteriores, estavam no caixa da DL-base.

Também corrigi um erro de texto: a "recompra de R$ 353 mi no 1S26" não existiu.

Resultado da correção:
- **Valor justo:** R$ 4,59 → **R$ 3,52** (−23%).
- **TIR de dono:** inalterada em 21,0%, porque vem do DDM e o bridge não entra nela.

Preço de referência (foto B3): R$ 5,88.

## Mudanças em `research/SBFG3.json` (original em `research/review/SBFG3.orig.json`)
| Item | Antes | Depois | Por quê |
|---|---|---|---|
| `adjustments.other_debt_like` | 0 | **466,3** | Parcelamento de tributos de 341,3 (BPP 2T26: CP 85,5 + LP 255,8) mais dividendos a pagar de 125,0 (data-com 24/04/26, pagos em 05/08/26) |
| `adjustments.notes`, `dividend_policy`, `history_check.notes`, `summary` | "recompras de R$ 353 mi (1S26)"; "risco sacado não divulgado"; VJ ~R$ 4,6 | Texto corrigido; VJ ~R$ 3,5 | Ver achados 3 e 4 |

| Métrica (motor, Ke 25%) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 4,59 (upside −22,0%) | **R$ 3,52 (upside −40,1%)** |
| DCF / DDM / múltiplos | 1,63 / 4,57 / 10,52 | −0,39 (entra com 0 no blend) / 4,57 / 9,51 |
| TIR implícita (dono) | 21,0% | **21,0%** |
| TIR 3 anos (P/L 6x) | 47,8% | 47,8% |
| Monte Carlo P(valor > preço) | 34,6% | 22,0% (p10 1,66 · p50 3,56 · p90 7,71) |
| Cenários bear / bull / esperado | 1,83 / 7,70 / 4,38 | 1,58 / 6,43 / 3,52 |

## Achados
| # | Severidade | Achado | Evidência | Ação / impacto |
|---|---|---|---|---|
| 1 | **Alta** | Parcelamento de tributos fora do bridge | Linhas 2.01.03.01.02 (85,5) e 2.02.02.02.04 (255,8) do BPP 2T26. O saldo subiu: 96 (2023) → 242 (2024) → 245 (2025) → 341 (2T26). O salto de 2024 coincide com a queda da provisão fiscal de 574 para 154, o que sugere transação tributária (inferência). É passivo financeiro com o governo (Selic). | Incluído. −R$ 1,48/ação no DCF e no EV/EBITDA |
| 2 | Média | Dividendo de 2025 (R$ 0,5429/ação = R$ 125 mi), pago depois do balanço-base | B3: data-com 24/04/2026, pagamento 05/08/2026. O BPP 2T26 tem "Dividendos e JCP a pagar" de 125,0. O caixa de 30/06 (429) o incluía, mas quem compra hoje não o recebe. | Incluído. −R$ 0,54/ação |
| 3 | Média (fato) | "Recompras de R$ 353 mi no 1S26" (JSON e dossiê) não aconteceram | A DFC CVM do 1S26 tem buybacks de 0. A tesouraria no PL foi de −153,1 (4T25) para 0 com o cancelamento de 13,89 mi ações em mai/26, e a quantidade em tesouraria ficou estável em 14,29 mi do 3T25 ao 1T26. O PL subiu 116 no 2T26. O número vem de linha desalinhada da DFC do ITR 2026: no mesmo bloco, "Pagamento baseado em ações +598" é, na verdade, a captação da SBFC15. As recompras reais somam R$ 153 mi (2024–25). | Texto do JSON corrigido. **O dossiê `notes/SBFG3.md` ainda traz o número** (não editei) |
| 4 | Baixa | Risco sacado "não divulgado" | O BPP 2T26 traz "Risco sacado" de 62,7 dentro de fornecedores (84,3 no 4T25) | Mantido como capital de giro, como nos pares. Como dívida: −R$ 0,03 no VJ |
| 5 | Info | Contagem de ações correta (230,66 mi), mas o histórico CVM tem erro | Nos ITR/DFP de 4T24 e 3T25–1T26, o campo "total" já vem líquido de tesouraria: 240.408.980 + 3.604.000 = 244.012.980, que é o total do 1T25; e 244.555.330 − 13.891.336 = 230.663.994. Por isso o `data/hist` mostra 215,98 mi ações em circulação no 3T25–1T26, quando o certo é 230,27 mi. | A base do modelo usa B3 com tesouraria zero no 2T26 e está certa. Os múltiplos históricos desses trimestres podem sair ~6% baixos. É problema do pipeline, que não editei |
| 6 | Info | DL normalizada (−R$ 314 mi de recebíveis da Copa) | A DL subiu 513 no 1S26, contra 256 no 1S25. A empresa estima ~0,4x de alavancagem. Ainda não dá para conferir: o 3T26 sai em 09/11. | Mantida. Sem ela: VJ 3,12 / TIR 19,8% |
| 7 | Info | Alíquota de 20% na perpetuidade | O ETR de 2022–24 ficou em 2–11%, com benefício em 2025 e no LTM, e há IR diferido ativo de 873. Isso sustenta 0–20% até 2030. Mas a reforma tributária extingue o ICMS (e o incentivo da Fisia) até 2033, então 20% perpétuo é generoso. | Mantida. Com 30% no terminal: VJ 3,41 / TIR 19,4% |
| 8 | Info | Kd do WACC de 15,5%, contra DI1F31 de 15,66% + spread de 1,0–2,1% | — | Sem efeito no VJ, porque o DCF já é negativo. Mantido, como nos pares |

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +12 / +4 / +7 / +7,5 / +7% | O 1S26 foi de 4.004 (+18,7% a/a, Copa). Para fechar o ano, o 2S26 precisa de +6,8% (4.661 vs 4.365). CAGR 2021–25 de 10,9%; 3 anos de 7,3% | ok |
| Margem EBITDA IFRS-16 | 14,0 → 13,3 → 14,0% | 2025: 12,9%; LTM: 13,65%; 1S26: 15,0%. O 2S26 implícito (13,1%) fica acima do 2S25 (12,4%). Média 2021–25 de 13,5% | ok, sem ganho estrutural |
| D&A | 5,8% | LTM 5,8% (484 / 8.369); 2T26 anualizado de ~500 | ok |
| Capex com direito de uso | 7,2 → 7,1% | Capex caixa: 3,6–3,7% (2023–24), 5,4% (2025), 6,0% (LTM). Amortização do direito de uso: 226,7 (2,9%). Nos níveis de 2025/LTM o total daria 8,3–8,9% | Leve no curto prazo. Com 8,3%: VJ 3,42 |
| Capital de giro | 18% da receita incremental | (Recebíveis + estoques − fornecedores) / receita: 31% (2025) e 34% (2T26) | Abaixo da média. Com 25%: VJ 3,46 |
| Resultado financeiro | 12,5–13% × DL | 2026E −307, contra LTM −290 e 1S26 anualizado −332. Na curva de hoje (dívida de 1.614 a CDI+1,0–2,1%, arrendamentos de 1.587 a ~7,8%, caixa a CDI), o custo misto fica em ~11,5–12% | ok, levemente conservador |
| IR | 0 → 20% | Ver achado 7 | Defensável até 2030 |
| Payout | 30 → 40% | Média de ~22% do lucro do ano anterior; 38% em 2026, mais R$ 126 mi de recompras em 2025. A DL/EBITDA projetada cai de 2,0x para 1,5x | ok |
| ROIC_T / ROE_T | 11% / 13% | Explícito: 10,3–12,6% / 9,3–12,6%. Contra WACC de 19,1% e Ke de 25%, crescer destrói valor | Coerente (ROE_T ~1 p.p. acima do que ROIC 11% + alavancagem dão) |
| DL-base (CVM) | 2.771,3 → override 2.457,3 | Dívida 1.613,9 + arrendamentos 1.586,7 (lançados em "empréstimos") − caixa 429,3 | Bate com o release. Override no achado 6 |
| Ações | 230,66 mi | B3 230.663.994; tesouraria zero no 2T26 | ok (achado 5) |

## Sensibilidade (já com a correção)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| **Base corrigida** | **R$ 3,52** | **21,0%** | **47,8%** |
| Sem normalização da Copa | R$ 3,12 | 19,8% | 41,0% |
| Alíquota 0 → 30% (terminal 30%) | R$ 3,41 | 19,4% | 42,0% |
| Capex 8,3% → 7,5% | R$ 3,42 | 20,3% | 44,5% |
| Capital de giro de 25% | R$ 3,46 | 20,6% | 46,2% |
| Margem +1 p.p. | R$ 5,07 | 24,1% | 64,1% |
| EV/EBITDA alvo 5,5x | R$ 4,17 | 21,0% | 47,8% |

- **Robustez da conclusão:** o valor justo fica abaixo do preço (R$ 5,88) em todos os casos testados; o maior é R$ 5,07, com margem +1 p.p.
- **TIR de dono:** fica entre 19% e 24%, abaixo do Ke de 25%.
- **Divergência entre métodos:** o DCF dá ~0 e o DDM, R$ 4,57. Isso vem do WACC (40% de dívida barata) contra o Ke fixo de 25%, e não de premissa.

## O que não deu para verificar
- Taxa e prazo do parcelamento. A dedução usa o valor contábil; como é corrigido pela Selic, não deve haver desconto relevante.
- Conversão dos recebíveis da Copa em caixa (3T26 em 09/11/26).
- Execução do novo programa de recompra depois de 31/08/26.
- Valor justo dos derivativos hoje.
- Nota explicativa de arrendamentos: as adições de direito de uso foram aproximadas pela amortização, sem o roll-forward.
