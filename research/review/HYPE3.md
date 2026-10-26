# Revisão independente — HYPE3 (Hypera) · G05 · 26/10/2026

**Veredito: ajustada.** Duas correções na estrutura financeira, em sentidos opostos e que quase se anulam: (1) os JCP declarados a pagar (R$ 984 mi) passaram para a DL-base; (2) o custo da dívida foi recalibrado ao custo efetivo observado na CVM, que estava ~3 p.p. abaixo do modelado. Valor justo R$ 10,63 → **R$ 10,76**; TIR implícita 13,7% → **14,0%** (preço da foto R$ 20,21); TIR de 3 anos 22,7% → 24,5%. A conclusão não muda: barata em múltiplos (8,2x P/L 27E), mas ROE de ~12% não sustenta Ke 25%.

## Achados

| # | Severidade | Achado | Evidência | Ação |
|---|---|---|---|---|
| 1 | **Média (erro objetivo, DDM/LL)** | Os JCP/dividendos declarados e já ex (983,9) entravam só como `other_debt_like`. Isso acertava a ponte do DCF e dos múltiplos, mas o caixa que sai nos próximos meses não entrava na trajetória da DL do motor, e o LL/DDM omitia ~R$ 110–140 mi/ano de custo financeiro | BPP 2.01.05.02.01 = 983,89 em 30/06/26 (760,9 no 4T25; só 147 pagos no 1S26). Isolado, o ajuste reduz o VJ de 10,63 para 10,27 e a TIR de 13,7% para 13,2% | `net_debt` 6.887 e `other_debt_like` 457. A soma DL + debt-like não muda (7.344) |
| 2 | **Média (premissa incoerente com a CVM, conservadora)** | `cost_of_net_debt` de 13,5–14% mais `other_financial` de −60 a −80 dava custo total de ~15% da DL (~CDI + 0,5 p.p.). O custo efetivo observado é **~CDI − 2,8 p.p.** | Resultado financeiro / DL média por trimestre: 1T25 10,2% (CDI ~13,2%), 2T25 11,2% (~14,6%), 3T25 12,3% (~14,9%), 4T25 12,1% (~14,9%), 1T26 ~12,1% (~14,9%, ajustado pela entrada do aumento de capital no fim do tri), 2T26 11,6% (~14,5%). O DVA "Juros" (1.099,7) ≈ despesa financeira da DRE (1.102), e os juros pagos (1.147) também: não há juros capitalizados que expliquem a diferença. Provável fonte: dívida subsidiada (TJLP/TR/FCO) e IPCA. Com a premissa original, o resultado financeiro de 2026 (−857) implicava um 2S26 de −227/tri, contra −177 no 2T26 com DL menor | Recalibrado: CDI do grupo (14,5/14/13/12,5%) − 2,5 p.p. (margem conservadora ante os −2,8 p.p. observados), com `other_financial` mantido e o JCP financiado a ~CDI ⇒ kd [10,2; 11,4; 10,8; 9,6; 8,9]%. 2026 = 1S26 real −403 + 2S26 ≈ −762 |
| 3 | Info (ok) | Base e crescimento | RL 2025 de 7.699 (deprimida pelo destocking do 1T25). Os +18,6% de 2026 implicam 2S26 de +7,0% a/a, coerente com sell-out de +7,6–8,8%. Ações: 704,0 mi (pós-aumento de R$ 1,5 bi). DL = 7.482 − 1.578,5 (sem arrendamentos relevantes no BP) | — |
| 4 | Info (ok) | Margem | 1S26 = 30,8%; 2S26 implícito = 32,0% (2S25: 33,7%); 2027 = 30,0% (efeito do câmbio sobre o IFA, defasado por ~194 dias de estoque). É o driver mais incerto: −2 p.p. dá VJ 9,36 | Mantido |
| 5 | Info (ok) | IR de 0% → 18% | 1S26 efetivo −8,7% (benefício de 67, com JCP e subvenções). Os prejuízos fiscais (base de R$ 5,67 bi) e o JCP recorrente (~R$ 0,7–1,0 bi/ano, escudo de ~34%) sustentam alíquota baixa; a rampa reflete o fim das subvenções. IR de 25% desde 2028 dá VJ 9,71 e TIR 13,1% | Mantido |
| 6 | Info | ROE_T de 15% contra ROE projetado de ~12,5–12,9% | A base de intangíveis (R$ 12,2 bi, Takeda) deprime o ROE contábil. Os 15% em capital incremental são plausíveis. Com 12,5%: VJ 10,65 e TIR 13,3% | Mantido |
| 7 | Info (exibição) | O EV/EBITDA LTM exibido subiu (7,1x → 7,4x) | Efeito de o JCP estar agora na DL-base: o EV "hoje" do motor soma a DL, não o debt-like. Fica mais correto, mas não é estritamente comparável com papéis que mantêm proventos declarados fora da DL (ex.: RADL3, 306 mi, imaterial) | — |

## Mudanças em `research/HYPE3.json` (original em `research/review/HYPE3.orig.json`)
- `overrides.base.net_debt`: (CVM 5.903,5) → **6.887**; `adjustments.other_debt_like`: 1.441 → **457**.
- `projection.cost_of_net_debt`: [13,5; 14,0; 13,5; 13,0; 12,5]% → **[10,2; 11,4; 10,8; 9,6; 8,9]%**. São taxas efetivas sobre a DL, não custo marginal; o Kd do WACC continua em 15%.
- Textos: notas de revisão em `overrides.notes` e `adjustments.notes`.
- Efeito: resultado financeiro 2026–30E de −857/−863/−776/−691/−605 → −762/−824/−736/−618/−534. LL de 1.663/1.692/1.947/2.145/2.236 → 1.758/1.730/1.985/2.209/2.294. DL 2030E 3.643 → 4.516. DCF sem mudança (7,08); DDM 8,84 → 9,08; múltiplos 19,53 → 19,79.
- **Valor justo de R$ 10,63 → R$ 10,76 (+1%). TIR implícita de 13,7% → 14,0%. TIR de 3 anos de 22,7% → 24,5%.** Monte Carlo: p10–p90 de 8,43 a 13,16, P(valor > preço) = 0%.

## Sensibilidade (nova base, preço R$ 20,21)
| Cenário | VJ | TIR | TIR 3a |
|---|---|---|---|
| Base revisada | 10,76 | 14,0% | 24,5% |
| kd original do analista (com o JCP na DL) | 10,27 | 13,2% | 18,8% |
| kd efetivo com a curva DI (15,2/15,8/16/16%) | 10,55 | 13,4% | 20,4% |
| Margem −2 p.p. (câmbio sem repasse) | 9,36 | 13,1% | 18,4% |
| Margem de 33% desde 2028 (nível do 2S25) | 11,84 | 14,8% | 30,2% |
| IR de 25% desde 2028 | 9,71 | 13,1% | 15,3% |
| IR de 8% fixo | 11,29 | 14,8% | 26,6% |
| ROE_T 12,5% | 10,65 | 13,3% | 24,5% |
| Capital de giro de 30% do Δ receita | 10,64 | 13,9% | 24,2% |

A TIR inteira fica entre 13% e 15% em todos os cenários. A TIR de 3 anos passa de 25% só com margem de volta a ~33% e saída a 9x P/L.

## Não verificado
- A composição exata da dívida que explica o custo efetivo abaixo do CDI (o ITR não foi lido): saldos e taxas da dívida subsidiada e IPCA, swaps e a parcela efetivamente pós-fixada (a sensibilidade do ITR sugere ~R$ 5,9 bi). Se a dívida barata amortizar, o custo efetivo sobe na direção da premissa original.
- O cronograma de pagamento dos R$ 984 mi de JCP.
- A participação do CPV em dólar, o CMED máximo de 2026 e os desdobramentos da proposta da EMS.
