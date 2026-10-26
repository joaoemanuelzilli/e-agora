# Revisão independente — PGMN3 (Pague Menos) · G05 · 26/10/2026

**Veredito: ajustada.** O custo da dívida de 2028–30 era incoerente com qualquer caminho de juros documentado. O resto está bem montado: AVP fora do EBITDA, adições de direito de uso no capex, DL com recebíveis antecipados e swaps. Valor justo R$ 2,32 → **R$ 2,27**; TIR implícita 20,4% → **19,5%** (preço da foto R$ 2,94); TIR de 3 anos 55,1% → 50,4%. Continua abaixo de Ke 25% pela TIR inteira, mas é a TIR mais alta da cobertura G05.

## Achados

| # | Severidade | Achado | Evidência | Ação |
|---|---|---|---|---|
| 1 | **Média (premissa incoerente)** | `cost_of_net_debt` de 15/14/13,5/13% em 2027–30 implicava CDI de ~9–12% | O resultado financeiro ex-AVP do 1S26 é −262 (−524/ano, 15,5% da DL de 3.374). Parte relevante é fixa: juros de arrendamento de 189 (2025) e 94 (1S26) na DFC 6.01.01.07, ~9,6% sobre 1,9 bi. A exposição a CDI é de só ~1,8 bi (DL ex-arrendamentos 1.468 + recebíveis antecipados 316). Com a DL quase estável no motor (3.374 → 3.142), a trajetória original exigia CDI de ~13,8% (2027), 11,8% (2028), 10,6% (2029) e **9,3% (2030)**: abaixo até do Focus pré-choque e ~6 p.p. abaixo da curva de hoje (forwards de ~15–16%) | Recalibrado com o mesmo caminho de CDI documentado no grupo (ASAI3: 14,5/14/13/12,5%) |
| 2 | Info (ok) | Tratamento do AVP | A margem modelada é ex-AVP: −1,0% da RL, R$ 153 mi LTM. O kd também é ex-AVP, então o lucro não muda e o FCFF não fica superestimado. O problema análogo do MDR no GMAT3 não existe aqui | — |
| 3 | Info (ok) | Adições de direito de uso | ΔArrendamento + principal pago (DFC 6.03.03): 2023 −117 + 281 = 164 (1,5% da RL); 2024 −31 + 281 = 250 (2,0%); 2025 −134 + 305 = 171 (1,15%); 1S26 −51 + 158 = 107 (1,4%). A premissa de ~1,3% é coerente. O capex caixa LTM é de 2,05% | — |
| 4 | Info (ok) | Base, ações e debt-like | DL = 1.581 + 1.906 − 113 = 3.374. Debt-like: recebíveis antecipados 315,7 + swaps passivos 19,5. Ações: 720,15 mi, já pós-aumentos de capital (PL 3.418). Os múltiplos de referência conferem (pré-eleição 11,9x P/L LTM e 4,9x EV/EBITDA) | — |
| 5 | Info | Margem | A premissa ex-AVP de 2026 (8,7%) é levemente conservadora. O 1S26 CVM ficou em 9,5%, +0,6 p.p. a/a, e se o 2S26 repetir o ganho a margem de 2026 dá ~8,9% ex-AVP. A rampa até 9,4% em 2030 é coerente com a tendência (2T26 recorde de 10,2% CVM). É o driver dominante: com margem estável em 8,7%, VJ 1,69 e TIR 16,9% | Mantido |
| 6 | Info | Capital de giro de 15% do Δ receita | O NWC operacional (recebíveis + estoques − fornecedores) é de 18% da RL LTM e 17,4% em 2025. Os 15% incrementais se justificam pela antecipação de recebíveis, tratada como debt-like. Com 18%: VJ 2,15 | Mantido |
| 7 | Info (motor) | A TIR de 3 anos (50%) e a TIR inteira (19,5%) divergem muito | A TIR de 3 anos sai a 8x P/L sobre o LPA 2029E (0,80). O DDM, com ROE_T 16%, g 5% e Ke 25%, equivale a ~3,6x o lucro na perpetuidade. A TIR de 3 anos é uma aposta de re-rating, não de geração de caixa. Com P/L de saída de 6x, a TIR de 3 anos cai para 32,7% | Ressalva |

## Mudanças em `research/PGMN3.json` (original em `research/review/PGMN3.orig.json`)
- `projection.cost_of_net_debt`: [0,150; 0,150; 0,140; 0,135; 0,130] → **[0,150; 0,154; 0,152; 0,148; 0,147]**. Construção: fin_t ≈ 524 + 1,8 bi × (CDI_t − 14,75%), dividido pela DL_{t−1} do motor.
- Efeito: LL 2027–30E de 409/527/615/709 → 397/492/576/658. DDM 2,15 → 2,01; múltiplos 4,65 → 4,58; DCF sem mudança (1,24).
- **Valor justo de R$ 2,32 → R$ 2,27. TIR implícita de 20,4% → 19,5%. TIR de 3 anos de 55,1% → 50,4%.** Monte Carlo: p50 2,25, p10–p90 1,07–3,63, P(valor > preço) = 25%.
- Textos: nota de revisão em `overrides.notes` e `summary` (TIR ~19,5%; ~13,5% pré-eleição).

## Sensibilidade (nova base, preço R$ 2,94)
| Cenário | VJ | TIR | TIR 3a |
|---|---|---|---|
| Base revisada | 2,27 | 19,5% | 50,4% |
| kd com a curva DI (CDI 15,2/15,8/16/16%) | 2,21 | 18,5% | 44,9% |
| kd original do analista | 2,32 | 20,4% | 55,1% |
| Margem ex-AVP +0,2 p.p. | 2,40 | 19,7% | 53,5% |
| Margem ex-AVP estável em 8,7% | 1,69 | 16,9% | 35,9% |
| Crescimento −2 p.p. em 2027–30 (SSS ≈ CMED) | 2,10 | 18,4% | 45,0% |
| IR de 25% desde 2028 (fim dos incentivos) | 2,00 | 18,6% | 43,8% |
| Capital de giro de 18% do Δ receita | 2,15 | 19,2% | 48,7% |

Nem margem de 10% ex-AVP desde 2028 com CDI de ~10% (o kd original) leva a TIR a 25%: fica em 22,7%. Só o bull completo do analista (crescimento +2 p.p., margem +0,6 p.p.) com aquele CDI chega perto, a 24,4%. A conclusão "abaixo da meta, mas o mais perto dela" se mantém.

## Não verificado
- Indexador, custo e cronograma das debêntures (o ITR não foi lido): assumi pós-fixado, com custo efetivo de ~CDI + 0,5–1%, inferido dos juros provisionados (236/ano sobre ~1,66 bi).
- O valor do AVP no 1S26: usei o ~1,0% da RL do analista.
- O cronograma de monetização dos créditos fiscais (ICMS/PIS-COFINS), que não entrou como ativo não operacional e é potencial upside.
