# Revisão independente — CEAB3 (C&A Modas) · 26/10/2026

**Veredito: ajustada.** As premissas operacionais estão bem calibradas. O analista corrigiu a D&A de direito de uso que a DVA lança fora de 7.04.01. Mas havia um erro objetivo de período:
- O JCP do exercício 2025 (R$ 139,8 mi a pagar em 30/06/26) estava no caixa da DL-base.
- Esse JCP foi pago em 31/08/26 a quem era acionista em 23/12/25. O analista viu o item e não o ajustou, e o relatório ainda o apresenta como retorno de "7,1% do preço".

Resultado da correção:
- **Valor justo:** R$ 7,20 → **R$ 6,91**.
- **TIR de dono:** inalterada em 21,1%.
- **P(valor > preço) no Monte Carlo:** 47,6% → **43,9%**, abaixo do corte de 45% da regra de oportunidades.

Preço de referência (foto B3): R$ 7,35.

## Mudanças em `research/CEAB3.json` (original em `research/review/CEAB3.orig.json`)
| Item | Antes | Depois | Por quê |
|---|---|---|---|
| `adjustments.other_debt_like` | 0 | **139,8** | "Dividendos e JCP a pagar" do BPP 2T26. Data-com 23/12/2025, pagamento 31/08/2026 (B3) |
| `adjustments.notes`, `thesis[2]`, `dividend_policy`, `catalysts`, `summary` | "JCP de 2025 equivale a ~7% do preço"; "a pagar, data a confirmar"; catalisador "pagamento do JCP de 2025"; VJ ~R$ 7,2 | Texto corrigido (já pago; não é do comprador de hoje); VJ ~R$ 6,9 | Achado 1 |

| Métrica (motor, Ke 25%) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 7,20 (upside −2,1%) | **R$ 6,91 (upside −6,1%)** |
| DCF / DDM / múltiplos | 4,77 / 5,75 / 13,50 | 4,30 / 5,75 / 13,26 |
| TIR implícita (dono) | 21,1% | **21,1%** |
| TIR 3 anos (P/L 7x) | 52,8% | 52,8% |
| Monte Carlo P(valor > preço) | 47,6% | **43,9%** (p10 3,15 · p50 6,89 · p90 11,07) |
| Cenários bear / bull / esperado | 3,59 / 9,69 / 6,61 | 3,30 / 9,40 / 6,32 |

## Achados
| # | Severidade | Achado | Evidência | Ação / impacto |
|---|---|---|---|---|
| 1 | **Média–alta** | JCP de 2025 contado como valor para quem compra hoje | B3: JCP de R$ 0,5216/ação, data-com 23/12/2025, pago em 31/08/2026. BPP 2T26: "Dividendos e JCP a pagar" de 139,8, dentro do caixa de 782 da DL-base. O relatório diz que o JCP "já equivale a 7,1% do preço" e a tese diz "~7% do preço". | Incluído em debt-like. −R$ 0,47/ação no DCF e no EV/EBITDA; VJ −R$ 0,29 |
| 2 | **Alta (consequência)** | CEAB3 deixa de cumprir a regra de oportunidade: P(MC) de 43,9% < 45% | O build congela a lista nas empresas com relatório, então CEAB3 continua listada. O relatório `reports/CEAB3.json` ficou desatualizado: cita VJ R$ 7,20 (−2%), P(MC) de 47%, esperado de R$ 6,61 e o JCP como 7,1% do preço | **Recomendo ao líder rever a seleção ou o relatório** (não editei). A TIR de 21,1% segue ≥ 20% |
| 3 | Média | A seleção é frágil mesmo após a correção | P(MC) com premissas razoáveis: ROIC_T de 18% → 51,0%; Kd de 16,5% → 42,2%; capex do 2S26 no guidance → 41,1%; margem −1 p.p. de 2027 em diante (câmbio) → 30,0%, com TIR de 19,3% | Informativo |
| 4 | Baixa | Capex de 2026 no stub abaixo do guidance | O guidance é de R$ 680 mi em caixa, e o 1S26 gastou só 247, o que exige 433 no 2S26. O stub do motor põe ~340 em caixa (+~180 de direito de uso) | Mantido. Com o guidance: VJ 6,68 / TIR 20,9% |
| 5 | Baixa | Kd do WACC de 14,5% abaixo do DI1F31 (15,66%) | A 4ª emissão saiu a CDI+0,8–1,0%, o que dá um marginal de ~16,5% | Mantido para consistência com os pares. Com 16,5%: VJ −R$ 0,14 |
| 6 | Info (a favor) | ROIC_T de 13% conservador frente ao RONIC explícito | Em 2030, o reinvestimento de 410 sobre NOPAT de 973 sustenta crescimento de 7,5%, o que implica RONIC de ~18%. A meta da empresa é ROIC > 18% nos projetos novos | Mantido. Com 18%: VJ R$ 7,45 / P(MC) 51% |
| 7 | Info (dados) | EBITDA LTM do pipeline sem a depreciação de direito de uso (DVA 7.04.02 em 2023–25) | O `ev_ebitda_ltm` do app mostra 3,1x; o correto é ~2,4x (EBITDA LTM corrigido de ~1.705). A série histórica de EV/EBITDA de 2023–26 também está inflada | Não afeta o valuation. É problema do pipeline, que não editei |

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +2,6 / +6,5 / +8 / +8 / +7,5% | 1S26 +0,9% (fim da telefonia). Para fechar o ano, o 2S26 precisa de +4,1%. CAGR 2019–25 de 7,1%; 3 anos de 8,9%; 15–20 lojas/ano | ok |
| Margem EBITDA IFRS-16 recorrente | 19,5 → 20,5% | Ajustada: 19,7% (2025), 19,6% (LTM), 20,9% no 2T26 (a reportada de 24,1% inclui ~81 de PIS/COFINS). O CVM corrigido de 2025 é 22,1%, com o ganho Bradescard | ok. O câmbio em 2027 é o risco (achado 3) |
| D&A | 9,0 → 8,8% | 2025: 344,6 (7.04.01) + 375,7 (7.04.02) = 720 (9,0%) | ok |
| Capex com direito de uso | 12,8 → 11,5% | Guidance de capex caixa: 8,3% em 2026 e 7–8% em 2027–30. Principal de arrendamento ≈ 545,5 − ~185 de juros = ~360 (4,5%). O passivo de arrendamento ficou estável em 1,78–1,83 bi | ok (achado 4) |
| Capital de giro | 15% | Ciclo de caixa +19 dias no 2T26 | ok |
| Resultado financeiro | 12–12,5% × DL e −60 de AVP | 2026E −293, contra LTM −286 e 1S26 anualizado −266. Na curva de hoje, o custo misto fica em ~11,8% (dívida de 949 a ~16,6%, arrendamentos de 1.776 a ~10,4%, caixa de 782 a CDI) | Coerente, levemente conservador |
| IR | 15 → 24% | ETR de 19,2% em 2025 e 17,1% no LTM, com JCP. Sem JCP (30% no terminal): VJ −R$ 0,44 | ok |
| Payout | 30 → 45% | JCP de 23% (2024) e 27% (2025) do lucro. Com o payout do modelo, a DL fica estável em ~1,95–1,99 bi | ok |
| ROIC_T / ROE_T | 13% / 15% | Explícito: 12,6–13,4% / 12,4–14,3%. Contra WACC de 20,4% e Ke de 25% | Coerente e conservador (achado 6) |
| DL-base | 1.943,6 | Dívida 949,4 + arrendamentos 1.776,2 − caixa 782,0 (CVM 30/06/26) | ok. Risco sacado de 281,6 tratado como capital de giro |
| Ações | 300,0 mi | B3 308,25 mi × (1 − 2,67% em tesouraria no 2T26). O RI mostra 12,18 mi em tesouraria depois do balanço (≈ 296,1 mi em circulação) | Coerente com o caixa do 2T26. Ajustar ações e caixa juntos dá efeito < R$ 0,10 |

## Sensibilidade (já com a correção)
| Caso | Valor justo | TIR implícita | P(MC) |
|---|---|---|---|
| **Base corrigida** | **R$ 6,91** | **21,1%** | **43,9%** |
| Original (sem o JCP no bridge) | R$ 7,20 | 21,1% | 47,6% |
| Kd de 16,5% | R$ 6,77 | 21,1% | 42,2% |
| Capex do 2S26 no guidance | R$ 6,68 | 20,9% | 41,1% |
| Margem −1 p.p. de 2027 em diante | R$ 5,76 | 19,3% | 30,0% |
| ROIC_T de 18% | R$ 7,45 | 21,1% | 51,0% |

**A tese de "TIR de dono de ~21%" sobrevive.** O que muda é o resto do argumento:
- o valor justo não fica mais "≈ preço": está ~6% abaixo;
- o critério estatístico da seleção (P ≥ 45%) depende de premissas favoráveis (ROIC_T acima de 13%).

## O que não deu para verificar
- Se a fração de IRRF do JCP (R$ 158 mi brutos contra 139,8 a pagar) também saiu de caixa depois de 30/06. Usei o passivo contábil, que é o número conservador.
- Recompras depois do 2T26 e preço médio.
- Composição de "Outros ativos não circulantes" (632, em queda), que pode conter créditos fiscais monetizáveis. Não somei.
- Repasse de câmbio no 3T26 (resultado em início de nov/26).
