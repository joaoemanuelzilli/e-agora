# Revisão independente — TOTS3 (TOTVS) · 26/10/2026

**Veredito: ajustada** (1 erro objetivo de contagem de ações; demais premissas coerentes). Original em `research/review/TOTS3.orig.json`.

Preço de referência (foto B3 13h02): R$ 37,25.

| | Antes | Depois |
|---|---|---|
| Ações em circulação (mi) | 554,07 | **573,20** |
| Valor justo | R$ 17,12 | **R$ 16,55** (−3,3%) |
| DCF / DDM / P/L / EV/EBITDA | 11,29 / 10,47 / 30,53 / 40,29 | 10,92 / 10,12 / 29,52 / 38,95 |
| TIR implícita | 11,3% | **11,1%** |
| TIR 3 anos | 17,4% | **15,5%** |
| P/L 2027E ao preço | 20,7x | 21,5x |
| Monte Carlo p10–p90 | 14,27–20,13 | 13,79–19,45 |

## Achados
1. **(alta — erro objetivo) Contagem de ações.** O pipeline calcula ações = total B3 (579,40 mi, já após o cancelamento de 20 mi de ações em tesouraria em 04/08/2026) × (1 − tesouraria/total da CVM em 30/06 = 26,21/599,40 = 4,37%) = 554,07 mi. Isso conta o cancelamento duas vezes: as 20 mi canceladas saíram da tesouraria, então as ações em circulação continuam 573,20 mi (CVM 30/06: 599,40 − 26,21; o dossiê e o `key_data` também usam 573,2 mi). Corrigido com `overrides.base.shares_outstanding_mn = 573,195`. DL e PL-base também são de 30/06, então a data fica consistente. **Alerta ao líder:** o mesmo viés atinge qualquer ticker que tenha cancelado ações em tesouraria depois do último balanço arquivado (`shares.b3_vs_cvm` < 1 sem desdobramento/grupamento).
2. (baixa) Os múltiplos-alvo são inconsistentes entre si: 11x EV/EBITDA 2027E implica ~22,4x P/L 2027E (EV 24.816 − DL 2026E 2.710 − 66 + 287 = 22.327 / LL 995), contra P/L-alvo de 17x. O método EV/EBITDA (R$ 38,95) fica 32% acima do P/L (R$ 29,52). Parte da diferença é legítima (D&A de 6,4% da receita inclui amortização de PPA da Linx). Não alterado: é julgamento, pesa 12,5% e não muda a conclusão.
3. (baixa) Receita 2027 de +12,5% sobre 2026 reportado (Linx por ~10 meses) equivale a ~+9,8% pró-forma (2026 PF ≈ 7.624 + ~190 de jan–fev de Linx), abaixo do ARR (+14%) e do pró-forma do 2T26 (+13,3%). Conservador, coerente com PMEs sob Selic alta. Não alterado (+1,5 p.p./ano → valor justo R$ 17,10).
4. (informativo) Custo da dívida líquida em 2029–30 (14%/13%) abaixo da curva DI (~15,4–15,7%), mas a DL de 2029–30 é pequena (869/156): efeito imaterial.

## Checagens contra o histórico CVM (ok)
- Margem EBITDA (EBIT+D&A) 2020–25: 23,0 / 24,6 / 23,1 / 22,1 / 23,7 / 25,4%; 1S26 25,8%. Premissa 25,6% → 28% em 2030 (+0,6 p.p./ano, ritmo de 2024–25): plausível, levemente otimista.
- D&A 6,5% → 5,8% vs 2T26 6,6%, LTM 6,2%. Capex 3,5% vs LTM 3,5% (2025 2,8%). D&A > capex por PPA e direito de uso (IFRS-16); a perpetuidade usa NOPAT × (1 − g/ROIC), então não capitaliza esse diferencial.
- IR 20% → 24% vs efetivo 2025 19,2%, LTM 16,7%: conservador (embute risco de fim do JCP).
- Resultado financeiro 2026E −R$ 466 mi (15,5% × DL 3.007) vs 2T26 anualizado −R$ 504 mi: coerente.
- Payout (inclui recompras) 50% → 75% vs histórico de caixa ~40% + recompras (2024: 116% do lucro; LTM ~110%); com FCF > lucro, a DL zera em 2030. Coerente.
- ROIC_T 22% / ROE_T 26% vs projetados em 2030: 26,1% / 26,7%. ok.
- DL-base R$ 3.007 mi (debêntures 4.743 + arrendamentos 284 − caixa 2.020) confere com a CVM de 30/06/26. Techfin a valor contábil (R$ 287 mi) e obrigações de aquisição líquidas (R$ 66 mi): ok.
- Receita-base pró-forma de R$ 6.900 mi (5.772 CVM ex-Dimensa + Linx ~1.135) bate com o pró-forma do 2T26.

## Sensibilidade (após a correção)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | 16,55 | 11,1% | 15,5% |
| Crescimento +1,5 p.p./ano | 17,10 | 11,4% | 17,9% |
| Margem 30% em 2030 | 17,47 | 11,6% | 19,6% |
| g 6,5% | 16,58 | 11,8% | 15,5% |
| IR fixo 20% | 16,98 | 11,4% | 17,6% |
| ROIC/ROE terminais 30% | 16,88 | 11,3% | 15,5% |
| P/L de saída 25x | 18,28 | 11,1% | 37,1% |
| Tudo otimista junto (exceto múltiplo) | 19,10 | 13,1% | 24,3% |

A conclusão (qualidade alta, mas não é oportunidade a Ke 25%) é robusta: nenhum conjunto plausível de premissas operacionais leva a TIR implícita perto de 25%. Só a TIR de 3 anos com saída a P/L ≥ ~25x passa da meta, e isso é aposta em múltiplo, não em fundamento.

## O que não deu para verificar
- Recompras executadas entre 04/08 e 26/10/2026 no novo programa (até 30 mi de ações); qualquer recompra reduziria ações e caixa juntos (efeito pequeno por ação).
- Receita trimestral exata da Linx antes da aquisição (base pró-forma estimada a partir do crescimento pró-forma divulgado).
- Resultado do 3T26 (início de nov/2026).
