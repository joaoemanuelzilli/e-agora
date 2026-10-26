# Revisão independente — LREN3 (Lojas Renner) · 26/10/2026

**Veredito: ajustada.** As premissas operacionais estão coerentes com o histórico CVM e, no conjunto, ficam levemente conservadoras frente ao guidance. O erro objetivo está no bridge: dois JCPs foram pagos depois do balanço-base a quem já era acionista e o DCF os creditava a quem compra hoje.

| JCP | Valor | Data-com | Pagamento |
|---|---|---|---|
| 2T26 | R$ 193,0 mi (a pagar em 30/06) | 23/06 | 14/07 |
| 3T26 | R$ 227,5 mi | 22/09 | 14/10 |

Resultado da correção:
- **Valor justo:** R$ 9,06 → **R$ 8,79**.
- **TIR de dono:** inalterada em 20,1%. Ela ainda inclui o JCP do 3T26 no stub de 2026; sem ele, cai para 19,8% (achado 2).

Preço de referência (foto B3): R$ 9,51.

## Mudanças em `research/LREN3.json` (original em `research/review/LREN3.orig.json`)
| Item | Antes | Depois | Por quê |
|---|---|---|---|
| `adjustments.other_debt_like` | 0 | **420,5** | JCP do 2T26 a pagar de 193,0 (BPP 2T26) + JCP do 3T26 de 227,5 (B3: R$ 0,240666 × 945,3 mi) |
| `adjustments.notes`, `thesis[1]`, `key_data` (JCP 2026), `summary` | "JCP de 2026 já declarado em R$ 665 mi" como retorno; VJ ~R$ 9,1 ≈ preço | Ressalva: as 3 parcelas têm data-com até 22/09 e não vão para quem compra hoje; VJ ~R$ 8,8 | Achados 1–3 |

| Métrica (motor, Ke 25%) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 9,06 (upside −4,7%) | **R$ 8,79 (upside −7,6%)** |
| DCF / DDM / múltiplos | 6,62 / 7,40 / 15,61 | 6,18 / 7,40 / 15,39 |
| TIR implícita (dono) | 20,1% | **20,1%** (19,8% sem o JCP do 3T26 no stub) |
| TIR 3 anos (P/L 9x) | 51,6% | 51,6% |
| Monte Carlo P(valor > preço) | 39,5% | 33,8% (p10 6,61 · p50 8,78 · p90 11,14) |
| Cenários bear / bull / esperado | 6,87 / 10,85 / 8,87 | 6,59 / 10,58 / 8,60 |

## Achados
| # | Severidade | Achado | Evidência | Ação / impacto |
|---|---|---|---|---|
| 1 | Média | JCP do 2T26 no caixa da DL-base | BPP 2T26 "Dividendos e JCP a pagar": 193,0 (o bruto seria 0,2293 × 961,3 = 220; o resto é IRRF). B3: data-com 23/06, pago em 14/07 | Incluído. −R$ 0,20/ação no DCF e no EV/EBITDA |
| 2 | Média | JCP do 3T26 creditado ao comprador atual | B3: R$ 0,240666, data-com 22/09, pago em 14/10 (R$ 227,5 mi). O DCF (EV desde 30/06 − DL de 30/06) o contava como valor de quem compra hoje. No EV/EBITDA ele já sai pela DL 2026E (dividendos do stub) | Incluído. DCF −R$ 0,24/ação. A dupla contagem no EV/EBITDA custa ~R$ 0,03 no VJ e foi aceita para corrigir o método de peso 50%. **Resíduo não ajustável nas premissas:** o DDM e a TIR ainda incluem esse JCP no stub de 2026 (sem ele, a TIR fica em 19,8%, abaixo do corte de 20%) |
| 3 | Baixa (texto) | Tese e key_data tratavam o JCP de 2026 já declarado (R$ 665 mi, "~7% do valor de mercado") como retorno | As 3 parcelas têm data-com em 24/03, 23/06 e 22/09. A próxima deve sair em dez/26 | Texto corrigido |
| 4 | Info | Kd do WACC de 14%, abaixo do DI1F31 (15,66%) | O funding da Realize custa 104–107% do CDI | Mantido para consistência com os pares. Com 16,5%: VJ −R$ 0,03 |
| 5 | Info | Ações de 961,3 mi (2T26), contra ~945,3 mi em set/26 após recompras | Base do JCP do 3T26: 227,5 / 0,240666 = 945,3 mi | Coerente, porque o caixa gasto também está no 2T26. Ajustando ações e caixa (−230) juntos: VJ 8,78 / TIR 20,4% |
| 6 | Info | Risco de fim do JCP | Benefício fiscal de R$ 284 mi em 2025 (~19% do lucro) | Mantido (15–20%). Com 30% a partir de 2028: VJ 8,14 / TIR 18,4% |

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita (CVM, inclui a Realize) | +3,5 / +7 / +8 / +8 / +7,5% | 1S26 +1,9% a/a. Para fechar o ano, o 2S26 precisa de +4,9% (8.815 vs 8.404). Guidance de varejo: 4–8% (2026, revisado) e 9–13% (2027–30). CAGR 2019–25 de 8,7%; 3 anos de 6,1% | Conservador frente ao guidance |
| Margem EBITDA IFRS-16 | 19,2 → 20,3% | 2025: 19,5%; LTM: 19,3%; 1S26: 19,5%. O 2S26 implícito (19,0%) fica em linha com o 2S25 (19,1%). A meta oficial implica +3–5 p.p. | ok, conservador |
| D&A | 8,1 → 7,7% | LTM 8,1% (1.296 / 15.972) | ok (capex ≥ D&A) |
| Capex com direito de uso | 9,7 → 9,0% | Guidance de capex caixa: R$ 1.050 mi (6,4%). Principal de arrendamento ≈ 795 − 264 = 531 (3,3%). Capex caixa LTM de 841 (5,3%). O 1S26 gastou só 296, o que exige 754 no 2S26 contra ~525 no stub | ok (pequeno viés de stub) |
| Capital de giro | 20% | Inclui a carteira da Realize (R$ 6,65 bi) | ok |
| Resultado financeiro | 7% × DL | 2026E −96, contra LTM −74 e 1S26 anualizado −110. O caixa de 1.917 supera o funding de 758, e os arrendamentos (2.530) custam ~10,5% fixos. CDI mais alto ajuda | Coerente com a curva |
| IR | 15 → 20% | ETR de 15,0% em 2025 e 12,6% no LTM, com JCP | ok (achado 6) |
| Payout | 80 / 75% (JCP + recompra) | JCP de 50–70% do lucro em 2021–25. Distribuição total de ~120% em 2025 e ~113% no 1S26. No modelo, a DL/EBITDA fica estável em 0,4x | Coberto pelo FCFE |
| ROIC_T / ROE_T | 16% / 17% | Explícito em 2030: 16,1% / 17,6%. Meta oficial de ROIC ~20% | Coerente |
| DL-base | 1.371,0 | Funding da Realize 757,8 + arrendamentos 2.530,2 − caixa 1.917,0 | ok |

## Sensibilidade (já com a correção)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| **Base corrigida** | **R$ 8,79** | **20,1%** | **51,6%** |
| Stub de 2026 sem o JCP do 3T26 | R$ 8,78 | 19,8% | 50,1% |
| Fim do JCP (IR 30% a partir de 2028) | R$ 8,14 | 18,4% | 42,6% |
| Realize: margem −1 p.p. em 2027–28 | R$ 8,33 | 19,8% | 50,2% |
| Receita no guidance (9% em 2027–30) | R$ 9,03 | 20,8% | 54,2% |
| Margem rumo ao guidance (+1,5 p.p. em 2030) | R$ 9,42 | 21,7% | 57,4% |

- **Conclusão mantida:** qualidade a preço razoável, mas abaixo da meta. Nenhum caso testado leva o valor justo acima do preço ou a TIR a 25%.
- **Fora da regra de oportunidade:** LREN3 não cumpre a regra nem antes nem depois da correção. O P(MC) foi de 39,5% para 33,8%, abaixo do corte de 45%.

## O que não deu para verificar
- O valor da IRRF do JCP do 2T26 que saiu de caixa em julho (usei o passivo líquido de 193,0, que é conservador).
- O volume e o preço das recompras de jul–out/26.
- O valor da participação na Vestuá (mantida em zero).
- A exposição cambial do CPV (não divulgada).
