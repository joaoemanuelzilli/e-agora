# Revisão independente — MGLU3 (Magazine Luiza) · 26/10/2026

**Veredito: ok, sem alteração.** Não achei erro objetivo.
- **O que confere:** DL-base, ações, capex com direito de uso, alíquota, bridge (recebíveis cedidos como debt-like, com o custo em `other_financial`, sem dupla contagem) e ativos fiscais a 50%.
- **Viés otimista nos juros de 2028–30:** a premissa de juros embute queda do CDI que a curva de hoje não sustenta.
- **Por que não alterei:** corrigir esse viés só reforça a conclusão de "armadilha". Também levaria a TIR para um piso artificial do motor (achado 1).

| | Valor |
|---|---|
| Preço de referência (foto B3) | R$ 5,85 |
| Valor justo (motor, inalterado) | **R$ 1,31** (DCF −4,26, que entra com 0 no blend · DDM 0,23 · EV/EBITDA 5,00) |
| TIR implícita | **6,4%** |
| P(valor > preço) no Monte Carlo | 0,5% |

## Achados
| # | Severidade | Achado | Evidência | Ação / impacto |
|---|---|---|---|---|
| 1 | Média (viés otimista) | Custo financeiro de 2028–30 cai com a DL subindo | O `cost_of_net_debt` vai de 13,6% a 12,5% e a antecipação (`other_financial`) de −1.350 a −1.100, implícito CDI de ~12,5–13% em 2029–30. Curva de hoje: forwards de ~15,2% (2027), 15,85% (2028) e ~16% (2029–30). Refazendo de baixo para cima (arrendamentos de 3.566 a ~10% fixos, dívida a CDI+1,5%, caixa a CDI), o kd na curva fica em 13,3 / 13,7 / 14,3 / 14,5 / 14,6% e a antecipação (R$ 5,8 bi cedidos + Cartão Luiza, ~R$ 1,4 bi/ano a ~14,5%) em −1.350 a −1.545. O dossiê diz que a curva "mantém o custo em ~R$ 2,2–2,3 bi/ano", mas o modelo tem a DL crescendo de 6,75 para 8,48 bi com o resultado financeiro caindo para −2,15 bi | **Mantido.** Com CDI plano em ~14,5%: VJ 1,25, LL 2030 de −217 (não volta ao lucro até 2030). Na curva: VJ 1,25, LL 2030 de −481. Nos dois casos o motor mostra TIR de 5,2%, mas esse número é o limite inferior da bisseção (g + 0,2 p.p.), não uma TIR real |
| 2 | Baixa | A TIR de 3 anos de −85% é artefato | LPA 2029E de R$ 0,009 × P/L 10x dá saída a R$ 0,09 | Sugiro ao líder ocultar a métrica quando o LPA de saída ≈ 0 (motor; não editei) |
| 3 | Baixa (julgamento) | Risco sacado ("fornecedores convênio") de R$ 2.572,6 mi tratado como capital de giro | BPP 2T26 (era 3.356 no 4T25) | Mantido, como nos pares. Como dívida: VJ R$ 0,48 |
| 4 | Info | Evidência da queima de caixa | O dossiê diz "DL CVM subindo R$ 0,4 bi em 12 meses", mas a DL CVM caiu de 7.612 (2T25) para 6.750 (2T26). O indicador neutro à antecipação, DL − recebíveis, piorou +723 (1.871 → 2.594), e do 4T24 ao 4T25 a piora foi de +767 | A tese de queima de ~R$ 0,5–0,7 bi/ano se sustenta. Só o número citado está impreciso |
| 5 | Info | O valor justo depende do EV/EBITDA | O DCF é negativo e entra com 0 (peso 50%), então VJ = 25% × DDM + 25% × EV/EBITDA. O alvo de 4,5x fica ≈ no múltiplo de hoje na mesma definição (4,6–4,9x) | Com 5,5x: VJ R$ 2,38. Com ROIC_T = WACC: DCF −1,91 (ainda 0 no blend) |
| 6 | Info | Kd do WACC de 16%, contra DI1F31 de 15,66% + spread de 1,25–1,75% | — | Sem efeito: o DCF é negativo com qualquer kd |

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +1% (2026), +5% a.a. | 1S26 de 18.105 (−2,3% a/a). Para fechar o ano, o 2S26 precisa de +4,0% (20.985 vs 20.180), com a Casas Bahia em RJ. CAGR de 5,8% em 5 anos e 1,2% em 3 | ok |
| Margem EBITDA CVM (inclui equivalência da Luizacred) | 8,0 → 8,4% | 2025: 8,3%; LTM: 8,1%; 1S26: 7,5%; 2S25: 8,7%. O 2S26 implícito é 8,4%. Fica acima do melhor ano ajustado | Generoso, como o próprio analista reconhece |
| D&A | 3,4 → 3,3% | LTM 3,4% (1.308) | ok |
| Capex com direito de uso | 3,5 → 3,4% | Capex caixa de 892 (2,3%) + principal de arrendamento de ~461 (1,2%). Arrendamentos estáveis em 3,5–3,7 bi desde 2022, ou seja, adições ≈ principal | ok |
| Capital de giro | 10% | Plausível. Os recebíveis cedidos estão fora do balanço e foram tratados como dívida | ok |
| Resultado financeiro | Ver achado 1 | 2026E −2.248, contra LTM −2.202 e 2T26 anualizado −2.289 | 2026 ok; 2028–30 otimista |
| IR | 10 → 28% | O LAIR LTM é negativo (−393). O motor não registra crédito de IR, ao contrário do contábil | ok (convenção) |
| Payout | 0 / 25% | Dividendos de 0 (2023–24), 225 (2025) e 63 (2026, pagos em 08/05, antes do balanço-base) | ok. Não há dividendos a pagar no 2T26 |
| ROIC_T / ROE_T | 9% / 8% | ROIC explícito de 9,0–9,2%. O ROE de 2030 é 1,9%, abaixo do ROE_T de 8%, mas isso é imaterial (DDM de R$ 0,23) | ok |
| DL-base | 6.749,9 | Dívida 4.946,1 + arrendamentos 3.566,1 − caixa 1.762,2 (CVM 30/06/26) | ok |
| Debt-like / não operacional | +5.766,4 / +1.700 | Recebíveis cedidos (ITR), 50% dos tributos a recuperar (3.454). O IR diferido (3.993) entra pela alíquota baixa | ok, sem dupla contagem |
| Ações | 775,66 mi | Grupamento de 10:1 (mai/24) e bonificação de 5% (dez/25); B3 com tesouraria de 0,04% | ok |

## Sensibilidade (motor, em memória)
| Caso | Valor justo | TIR implícita |
|---|---|---|
| **Base** | **R$ 1,31** | **6,4%** |
| Juros planos (CDI ~14,5%) | R$ 1,25 | n/d (piso de 5,2%) |
| Juros na curva DI | R$ 1,25 | n/d (piso de 5,2%) |
| Risco sacado como dívida | R$ 0,48 | 6,4% |
| Margem +1 p.p. em todos os anos | R$ 1,32 | 9,2% |
| EV/EBITDA alvo de 5,5x | R$ 2,38 | 6,4% |

**Conclusão: "armadilha a Ke 25%" robusta.**
- O DCF reverso exige crescimento de ~32% a.a. para justificar R$ 5,85.
- Nenhum caso testado passa de R$ 2,4 de valor justo ou de 10% de TIR.

## O que não deu para verificar
- O saldo da antecipação do Cartão Luiza junto à Luizacred, que não é divulgado. O analista não o somou, então o bridge fica otimista.
- Os limites de covenants.
- A captura efetiva de vendas da Casas Bahia (3T26 em 09/11/26).
