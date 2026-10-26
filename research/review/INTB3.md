# Revisão independente — INTB3 (Intelbras) · 26/10/2026

**Veredito: ok** (sem erro objetivo; premissas coerentes com o histórico CVM, em geral conservadoras). Nenhuma alteração em `research/INTB3.json`.

Preço de referência (foto B3 13h02): R$ 14,63. Motor: valor justo **R$ 8,23**, TIR implícita **12,9%**, TIR 3 anos **19,7%** (inalterados).

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +4% / 5,5% / 7% / 7% / 6,5% | CAGR 3a 1,8% (2022–25); 1S26 +4,2% a/a (2.260 vs 2.167) | Coerente; 2028–29 a 7% é o ponto mais otimista, mas é inflação + ganho real modesto |
| Margem EBITDA | 14,0% → 12,7% → 13,2% | 2021–25: 13,1 / 12,6 / 14,6 / 13,5 / 12,1% (média 13,2%); 1S26 14,4% (parte cíclica) | Coerente com a normalização que a própria gestão sinaliza |
| D&A | 2,6–2,8% | 2025 2,6%; LTM 2,6% | ok |
| Capex | 4,5% (2026–27, Manaus) → 3% | 2021–24 2,9–4,2%; 2025 1,4%; 1S26 2,2% | Conservador em 2026 (exige R$ 160 mi no 2S26); capex ≥ D&A na perpetuidade |
| Capital de giro | 30% da receita incremental | (Receb. 1.261 + estoques 1.230 − fornecedores 979)/receita LTM 4.552 ≈ 33% | ok |
| IR efetivo | 5% → 18% | 2019–25 entre −5,6% e +1,9%; LTM 2,7% | Conservador e justificado (fim de incentivos de ICMS até 2032, Lei de TICs, JCP) |
| Resultado financeiro | 13–11,5% sobre caixa líquido + R$ 30 mi | LTM +R$ 99,6 mi; 1S26 anualizado +R$ 106 mi; modelo 2026 +R$ 104 mi | ok em 2026; 2029–30 abaixo da curva DI (~15,4%) — conservador e imaterial |
| Payout | 60% | 2023 32%, 2024 38%, 2025 95% (R$ 300 mi extra) | Coerente com caixa líquido crescente (DL −570 → −1.039) |
| ROIC_T / ROE_T | 16% / 17% | ROIC proj. 2030 15,5%; ROE proj. 2030 14,6% (deprimido pelo caixa) | ROE_T levemente acima do projetado; efeito −R$ 0,04 no valor justo se 15% |
| Ações | 327,2 mi | CVM 30/06/26 = 327,2 mi (tesouraria 0,4 mi) | ok |
| Dívida líquida | −570 (caixa líquido) | 30/06/26: caixa 1.445 − dívida 876 (inclui arrend. 15,5) | ok |
| Risco sacado | R$ 369 mi como debt-like | dentro de fornecedores (979); era R$ 124 mi no 2T25 | Escolha conservadora (o custo não está no resultado projetado); não é dupla contagem |
| LTM | — | `ltm.ni_controlling` agora = 596,2 (o dossiê apontava 284,9); P/L LTM do motor 8,0x está correto | resolvido no pipeline |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
- Base: R$ 8,23 / 12,9% / 19,7%
- IR fixo em 3% para sempre: R$ 8,98 / 14,2% / 27,6%
- IR subindo só até 10%: R$ 8,56 / 13,5% / 23,6%
- Caixa rendendo a curva DI (~15%): R$ 8,30 / 13,2% / 21,6%
- Sem dedução do risco sacado: R$ 8,94 / 12,9% / 19,7%
- Margem 13,5% de 2027 em diante: R$ 8,64 / 13,1% / 21,5%
- Crescimento 4% a.a.: R$ 8,09 / 12,4% / 17,1%

A conclusão (TIR implícita ~12–14%, bem abaixo de Ke 25%; barata em múltiplos, mas não fecha a 25% pelo DDM) é robusta a todas as premissas discutíveis. A TIR de 3 anos é a métrica mais sensível ao IR: só passa de 25% se a alíquota quase zero durar para sempre.

## Achados
1. (baixa) Rendimento do caixa líquido em 2029–30 (12%/11,5%) abaixo da curva DI de hoje (~15,4–15,7%). Conservador; efeito +R$ 0,07 no valor justo. Não alterado.
2. (baixa) ROE terminal 17% acima do ROE projetado de 2030 (14,6%). Efeito −R$ 0,04 se igualado. Não alterado.
3. (informativo) Risco sacado deduzido integralmente (R$ 1,13/ação). Parte (~R$ 124 mi) pode ser estrutural; mantido por conservadorismo, como no dossiê.

## O que não deu para verificar
- 3T26 sai em 28/10/2026 (após a data de avaliação): magnitude e defasagem do repasse cambial.
- Parcela dolarizada do CPV e posição de hedge (a empresa não divulga).
- Prazo e duração dos incentivos fiscais (Lei de TICs, ICMS/SC, SUDAM/Manaus) que mantêm o IR efetivo perto de zero.
