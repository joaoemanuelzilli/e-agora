# Revisão independente — NATU3 (Natura) · 26/10/2026

**Veredito: ok.** Não achei erro objetivo. As premissas são coerentes com o CVM, que tem perímetro não comparável. O tratamento de dívida (FIDC e hedges como debt-like) está correto e sem dupla contagem. Nenhuma alteração em `research/NATU3.json`.

Preço de referência (foto B3): R$ 5,66. Resultado do motor (inalterado):
- Valor justo **R$ 2,81** (DCF 1,98 · DDM 1,72 · múltiplos 5,54).
- TIR implícita **12,6%**.
- TIR de 3 anos **18,4%**.

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | −4,5% / +6 / 5,5 / 5 / 5% | 1S26 CVM 9.915,5 vs 10.434,4 (−5,0%). 2S26 implícito: −4,1% sobre o 2S25 (11.389). | ok |
| Margem EBITDA (CVM) | 10,8% → 13,5% | 2025: 10,2% (recorrente 14,1%). 1S26: 9,8% (2T26: 12,0%; 13,2% ex-ICMS-ST). LTM: 8,8%. 2S26 implícito: 11,7%, contra 8,0% no 2S25. | Exigente para o 2S26 (ver achado 1). 2030 abaixo do recorrente de 2025. |
| D&A | 4,3% → 4,0% | 2025: 3,7%. 1S26: 4,5% (pós-incorporação da holding, intangível de R$ 10 bi) | Levemente baixa; −4% se 4,5% |
| Capex (com direito de uso) | 2,5% → 3,3% | Capex caixa 1,7% (2025) e 0,9% (1S26). Adições de direito de uso ~0,5%; passivo 683 → 594 → 495. | Conservador frente ao atual (contido) |
| Capital de giro | 15% da receita incremental | (Receb. + estoques − fornecedores)/receita: 13,3% (2025), 14,5% (LTM) | ok |
| IR | 34% → 30% | ETR CVM 2–4% (2024–25, continuadas). IR pago ~R$ 190 mi (2025) e R$ 156 mi (1S26), ~20% do EBIT | Conservador; +2% se 30% fixo |
| Resultado financeiro | 20–21% → 18% × DL + R$ −250 → −220 mi | Modelo 2026: −1.124. CVM: 2025 −867; LTM −1.384; 1S26 −826 (−351 ex-variação cambial). Juros + carry dos hedges ~R$ 207 mi/tri. | Coerente com a curva DI nova |
| Debt-like | 1.260 = FIDC 723 + derivativos 537 | Os bonds estão a câmbio spot na dívida bruta; bond + hedge = custo travado em R$. O custo do FIDC fica em `other_financial`. | Correto, sem dupla contagem |
| Payout | 0% → 40% | DL/EBITDA (companhia) de 2,06x, contra meta de 1,0–1,5x | ok |
| ROIC_T / ROE_T | 18% / 15% | Projetados para 2030: 10,3% / 8,6% (PL com R$ 10 bi de intangível) | Marginais acima da média, abaixo do WACC (20,8%) e do Ke. Coerente. |
| WACC | wd 30%, Kd 16,5% | DL 4.370 / (4.370 + valor de mercado pré-eleição 10.856) = 28,7% | ok |
| DL base | R$ 4.369,6 mi | 6.263,2 + 495,0 − 2.388,7 (CVM 30/06/26) | ok |
| Ações | 1.374,2 mi | CVM 1.374,235 mi; B3 idem | ok |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | R$ 2,81 | 12,6% | 18,4% |
| Margem −1 p.p. | R$ 2,11 | 11,3% | 5,8% |
| Margem +1 p.p. | R$ 3,51 | 13,9% | 29,6% |
| Margem até 15% em 2030 (bull) | R$ 3,41 | 14,2% | 30,7% |
| Margem 2026 = 1S26 (9,8%) | R$ 2,76 | 12,6% | 17,7% |
| Custo da DL sem queda (21% de 2027 em diante) | R$ 2,79 | 12,3% | 15,8% |
| IR 30% fixo | R$ 2,87 | 12,7% | 19,5% |
| Sem derivativos como debt-like (só FIDC) | R$ 3,05 | 12,6% | 18,4% |
| ROIC_T 15% | R$ 2,70 | 12,6% | 18,4% |
| Capex 2,2% fixo | R$ 3,08 | 13,1% | 21,6% |
| D&A 4,5% fixa | R$ 2,70 | 12,3% | 14,2% |
| Crescimento −2 p.p. | R$ 2,51 | 11,8% | 12,0% |

A conclusão de "armadilha" é robusta. Em todos os casos o valor justo fica entre R$ 2,1 e 3,5 (contra preço de R$ 5,66) e a TIR implícita entre 11% e 14%. A margem domina: cada 1 p.p. move o valor justo em ±25%. A TIR de 3 anos só passa de 25% com margem 1 p.p. acima do caso-base em todos os anos.

## Achados
1. **(média) Recuperação da margem no 2S26.** O caso-base exige 11,7% no 2S26, contra 9,8% no 1S26 e 8,0% no 2S25. Dois fatores sustentam a premissa: o fim do ICMS-ST na venda direta em SP desde 01/07, que vale ~+1,2 p.p., e a meta revisada da companhia de expandir a margem reportada sobre os 10,2% de 2025. Ela depende, porém, de o Brasil parar de cair (−14,8% no 2T26). Se 2026 ficar em 9,8%, o efeito no valor é pequeno (−2%), porque o que importa é a trajetória de 2027–30.
2. **(baixa) Custo da DL caindo de 21% para 18%.** A queda implica economia marginal de ~22,6% por real desalavancado. O custo realista é ~17% (CDI a termo de ~15,5% + 1,5%), e o caixa de R$ 2,4 bi rende só ~3,6%. Com o custo fixo em 21%: R$ 2,79 e TIR de 3 anos de 15,8%. Não alterado: o impacto no valor justo é imaterial.
3. **(baixa, conservador) IR de 30–34% sobre o EBIT** no FCFF, contra IR pago de ~20% do EBIT. Com 30% fixo, o valor sobe 2%.
4. **(informativo) Lucro de 2026.** O LL do ano inteiro no motor (+R$ 152 mi) implicaria +R$ 562 mi só no 2S26, porque o 1S26 real foi −R$ 409 mi. O motor projeta o ano por drivers. Só o stub entra no valor, e o dividendo de 2026 é zero, então não há efeito; mas o LPA/ROE de 2026 exibidos ficam otimistas.
5. **(informativo) Classificação do FIDC e dos hedges.** Tratar FIDC e hedges como dívida é julgamento correto do analista; a companhia os exclui. Excluir só os derivativos daria R$ 3,05 (+9%).

## Mudanças
Nenhuma.

## O que não deu para verificar
- Natureza da perda cambial de −R$ 475 mi no 1S26 (recorrente ou não) e a data exata de liquidação dos hedges.
- Contingências remanescentes da Avon International/API e indenizações do Chapter 11.
- Lucro recorrente oficial de 2025, covenants e consenso.
- Quanto dos fornecedores (R$ 4,3 bi) é risco sacado.
