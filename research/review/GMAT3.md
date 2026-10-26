# Revisão independente — GMAT3 (Grupo Mateus) · G05 · 26/10/2026

**Veredito: ajustada.** Havia um erro objetivo no DCF: o MDR de cartões, um custo operacional, ficava fora do FCFF. Também recalibrei as adições de direito de uso. A conclusão não muda: muito longe de Ke 25%. Valor justo R$ 1,52 → **R$ 1,23**; TIR implícita 13,3% → **13,0%** (preço da foto R$ 3,75); TIR de 3 anos 17,7% → 15,8%.

## Achados

| # | Severidade | Achado | Evidência | Ação |
|---|---|---|---|---|
| 1 | **Alta (erro objetivo, DCF)** | O `other_financial` de −320 a −400 mi/ano era, na prática, o **MDR de cartões**, que o Mateus contabiliza no resultado financeiro. Como o FCFF é pré-financeiro, o DCF omitia um custo operacional recorrente | Release 2T26, tabela "Resultado Financeiro Consolidado": "Despesa c/ % de cartão de crédito e débito (MDR)" de −74,6 (1T26) e −78,1 (2T26), ou 6M26 = −152,7 = **0,79% da RL** (estável: 0,794% e 0,793%). Assaí e a maioria dos pares registram MDR como despesa de vendas, então a margem EBITDA de 6,6–7,2% do Mateus não era comparável. O FCFF ficava inflado em ~R$ 290–350 mi/ano (~27%) | Margem EBITDA reduzida em 0,79 p.p. (pós-MDR) e `other_financial` zerado. O LL praticamente não muda |
| 2 | Média (calibração) | As adições de direito de uso (0,9% da RL embutido no capex) estavam abaixo do observado | ΔPassivo de arrendamento + principal pago (pagamento de arrendamento na DFC − juros de arrendamento): 2024 = 216 + 131 = 347 (**1,08%** da RL); 1S26 = 240 + 92 = 332 (**1,7%**, inflado pela reclassificação de aluguel variável). Em 2025 o número é poluído pela consolidação do Novo Atacarejo | Capex +0,3 p.p. (DU ~1,2%) |
| 3 | Baixa (consistência) | Múltiplo EV/EBITDA | Com o MDR na margem, os 5,0x originais (sobre o EBITDA reportado) equivalem a **5,65x** sobre o EBITDA pós-MDR (5,0 × 2.979 / 2.638). Mantive o julgamento do analista; usar 5,0x pós-MDR (critério igual ao da ASAI3) daria VJ 1,14 | `ev_ebitda` 5,0 → 5,65 (neutro) |
| 4 | Info (ok) | Dívida líquida | O pipeline já captura os arrendamentos: `balance.leases` 4.159 e DL 5.252 = override. A nota "leases = 0" estava desatualizada. O "financiamento por arrendamento" (593,5) está na dívida bruta e é distinto dos passivos IFRS-16, sem dupla contagem. Debt-like: antecipação de recebíveis 360,6 + tributos parcelados 57,9 (ok). Minoritários pelo valor contábil (1.160,6) | Nota atualizada |
| 5 | Info (ok) | Resultado financeiro ex-MDR | 2T26 −169 (anualizado −677), 1S26 −317 (anualizado −633), contra kd 12% × 5.252 = −630. Exposição a CDI pequena (DL ex-arrendamentos 1,1 bi + antecipação 0,36 bi): +100 bp ≈ −R$ 13 mi no LL. Juros de arrendamento de 6M26 = 209 (~10% a.a.) | — |
| 6 | Info (ok) | Crescimento de 2026 (5%) | O 2S26 implícito dá −1,0% a/a (o Novo Atacarejo está nas duas bases). O 1S26 orgânico ≈ −1,5% se o NA tiver ~R$ 1,2 bi/tri, o que é coerente com SSS −8% mais ~25 lojas em 12 meses | — |
| 7 | Info | IR de 8% → 18% | 1S26 efetivo ≈ −3% (crédito de R$ 13,8 mi), com exclusão de subvenção de ICMS. O 2026E de 8% é levemente conservador, porque implica ~16% no 2S26. A rampa até 18% reflete o risco da Lei 14.789/23 e da reforma | Mantido |
| 8 | Info | Exibição | O "EV/EBITDA LTM" do motor usa o EBITDA LTM reportado (pré-MDR) do `data/hist`, enquanto as projeções agora são pós-MDR. Ao comparar, considere ~+14% no múltiplo LTM | — |

## Mudanças em `research/GMAT3.json` (original em `research/review/GMAT3.orig.json`)
- `ebitda_margin`: [6,60; 6,90; 7,10; 7,20; 7,20]% → **[5,81; 6,11; 6,31; 6,41; 6,41]%** (pós-MDR).
- `other_financial`: [−320; −340; −360; −380; −400] → **[0; 0; 0; 0; 0]**.
- `capex_pct_revenue`: [2,8; 3,2; 3,3; 3,3; 3,3]% → **[3,1; 3,5; 3,6; 3,6; 3,6]%**.
- `target_multiples.ev_ebitda`: 5,0 → **5,65**, equivalente sobre a nova base de EBITDA.
- Textos: nota de revisão em `overrides.notes`, `rationale` e `summary` (TIR ~13%).
- Efeito: FCFF 2027E 1.093 → 656. DCF R$ 0,55 → −R$ 0,37 (zerado no blend). DDM 1,35 → 1,29. Múltiplos 3,65 → 3,62. LL 2030E 1.522 → 1.451 (−5%, pelo capex maior).
- **Valor justo de R$ 1,52 → R$ 1,23 (−19%). TIR implícita de 13,3% → 13,0%. TIR de 3 anos de 17,7% → 15,8%.** Monte Carlo: p10–p90 de 0,84 a 1,83, P(valor > preço) = 0%.

## Sensibilidade (nova base, preço R$ 3,75)
| Cenário | VJ | TIR | TIR 3a |
|---|---|---|---|
| Base revisada | 1,23 | 13,0% | 15,8% |
| Margem pós-MDR estável em 6,0% (sem recuperação) | 1,16 | 12,0% | 8,4% |
| Margem pós-MDR de 6,7% em 2029–30 (≈ média 2021–25) | 1,28 | 13,7% | 20,7% |
| IR de 8% fixo (subvenção mantida) | 1,27 | 13,9% | 20,3% |
| IR de 25% desde 2028 (perde a subvenção) | 1,19 | 12,3% | 8,7% |
| Crescimento de 9–10% (expansão volta) | 1,28 | 13,6% | 19,4% |
| ROIC_T e ROE_T de 16% | 1,24 | 13,4% | 15,8% |
| DU de volta a 0,9% | 1,24 | 13,2% | 17,1% |

O DCF é negativo em quase todos os cenários: WACC de 20,5% contra ROIC projetado de ~9–10% pós-MDR. O valor justo vem de 25% DDM e 25% múltiplos. A TIR de dono fica entre 12% e 14% em qualquer variação razoável.

## Não verificado
- A composição das "despesas financeiras" restantes (juros de dívida, antecipação, outras) e o custo/indexador da dívida bruta: o ITR não foi lido.
- O tamanho do Novo Atacarejo (receita e lucro, inclusive a parcela dos minoritários).
- O contexto da reapresentação de estoques/CMV (CPC 23), que afeta a comparabilidade da margem histórica: o 2T25 reapresentado tem margem de 8,8%, contra 8,0% no `data/hist`.
- A margem histórica pós-MDR antes de 2026: assumi o mesmo 0,79% da RL.
