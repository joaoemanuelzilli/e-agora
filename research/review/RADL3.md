# Revisão independente — RADL3 (RD Saúde) · G05 · 26/10/2026

**Veredito: ajustada.** O modelo é cuidadoso: base ex-4Bio, AVP fora do EBITDA, margem sobre base ajustada, dívida com recebíveis descontados, recebível da 4Bio e proventos declarados. Um único ponto foi recalibrado: as adições de direito de uso estavam abaixo do histórico CVM. Valor justo R$ 6,84 → **R$ 6,41**; TIR implícita 12,3% → **12,1%** (preço da foto R$ 15,08); TIR de 3 anos 23,9% → 21,9%. A conclusão (qualidade alta, mas não rende 25%) fica mais firme.

## Achados

| # | Severidade | Achado | Evidência | Ação |
|---|---|---|---|---|
| 1 | **Média (calibração vs CVM)** | As adições de direito de uso (~2,4% da RL embutido no capex) estavam ~0,7–1,2 p.p. abaixo do histórico | ΔPassivo de arrendamento + principal pago (DFC 6.03.05; os juros vêm à parte, em 6.01.03.03, e o pagamento total de ~R$ 1,40 bi bate com a reclassificação de aluguel de R$ 359,8 mi/tri do release): 2023 = 197 + 823 = 1.019 (**3,0%**); 2024 = 488 + 859 = 1.346 (**3,5%**); 2025 = 542 + 921 = 1.463 (**3,3%**; 3,6% ex-4Bio); 1S26 = 174 + 490 = 664 (**3,1%**, subestimado pela baixa dos arrendamentos da 4Bio). O ROU tem depreciação de R$ 255 mi/tri e cresce ~10% a.a. Com 2,4%, o ROIC incremental implícito ficava em ~34% | Capex +0,7 p.p. (DU 3,1%, o piso da faixa) |
| 2 | Info (ok) | Base de receita ex-4Bio (41,0 bi) | O 1S26 CVM (21.631, já com a 4Bio em descontinuadas: 3.10 = +19,96) contra o 1S25 ex-4Bio (20.882 − 1.535 = 19.347) dá +11,8%. Os +10,4% de 2026 implicam 2S26 de +9,1% a/a (o 2T26 fez +9,8%) | — |
| 3 | Info (ok) | Margem ex-AVP de 11,15% em 2026 | O CVM do 1S26 (10,9%) inclui ~R$ 195 mi de não recorrentes no 1T26: EBITDA aj. pré-IFRS16 de 820,8 + aluguel ~352 contra 978 CVM. Ajustado ≈ 11,8% com AVP, ou ~11,2% ex-AVP (AVP de 65,5 no 2T26 = 0,59% da RL). A premissa é coerente | — |
| 4 | Info (ok) | Custo da dívida | O 1S26 ex-AVP anualizado dá −1.052 (13,25% da DL de 7.940), contra 13,2% em 2026. A trajetória de 13,4% → 12,0% implica CDI de ~15% (2027) caindo a ~11% (2030), próxima do caminho do grupo. A exposição a CDI é baixa (~R$ 2,9 bi): na curva DI, VJ −0,04 e TIR −0,3 p.p. O recebível da 4Bio (716, CDI) só rendeu 2 meses no 1S26, o que deixa o kd de 2027 levemente conservador (~R$ 40 mi) | Mantido |
| 5 | Info (ok) | Itens debt-like e ativos não operacionais | other_debt_like 1.106 = recebíveis descontados 808,9 + opções 16,6 − antecipações a fornecedores 25,7 + JCP/dividendos declarados e já ex 306,1 (correto: não pertencem a quem compra hoje). Ativos não operacionais 776 = recebível da 4Bio 716,4 + 50% do DIFAL. Bate com a "dívida líquida ajustada" do release (2.999,6) | — |
| 5b | Baixa (imaterial, mantido) | Os proventos declarados a pagar (306) estão só em `other_debt_like`, então o desembolso não entra na trajetória da DL nem no custo financeiro do DDM. É o mesmo ponto corrigido no HYPE3, onde o valor era 984 | Movê-los para a DL dá VJ 6,36 (−0,05) e TIR 12,0% (−0,1 p.p.) | Não alterado (imaterial) |
| 6 | Info | IR, payout, ações | IR de 19–21% contra 19,1% recorrente no 1S26 (release). Payout de 45–50% contra 40–50% histórico. Ações: 1.748,5 mi | — |
| 7 | Info (metodologia) | Os múltiplos-alvo estão acima do preço | 15x P/L e 7x EV/EBITDA 2027E ex-AVP contra 14,6x e ~6x hoje. O método de múltiplos (17,0) fica acima do preço, enquanto DCF (2,1) e DDM (4,5) a Ke 25% ficam muito abaixo. O VJ (6,4) é uma média de métodos que divergem em 8x. A perpetuidade do DDM (g 5,5%, ROE_T 24%, Ke 25%) vale ~4,2x o LL de 2030 | Ressalva |

## Mudanças em `research/RADL3.json` (original em `research/review/RADL3.orig.json`)
- `projection.capex_pct_revenue`: [5,5; 5,5; 5,4; 5,3; 5,2]% → **[6,2; 6,2; 6,1; 6,0; 5,9]%**.
- Efeito: FCFF 2027E 1.557 → 1.199; DL 2030E 7.537 → 9.542 (mais arrendamentos); LL 2030E 3.058 → 2.921. DCF 2,79 → 2,07; DDM 4,70 → 4,52; múltiplos 17,08 → 16,96.
- **Valor justo de R$ 6,84 → R$ 6,41 (−6%). TIR implícita de 12,3% → 12,1%. TIR de 3 anos de 23,9% → 21,9%.** Monte Carlo: p10–p90 de 4,86 a 8,05, P(valor > preço) = 0%.
- Textos: nota de revisão em `overrides.notes` e `summary` (≈10,5% pré-eleição).

## Sensibilidade (nova base, preço R$ 15,08)
| Cenário | VJ | TIR | TIR 3a |
|---|---|---|---|
| Base revisada | 6,41 | 12,1% | 21,9% |
| Capex original (DU 2,4%) | 6,84 | 12,3% | 23,9% |
| kd na curva DI | 6,37 | 11,8% | 19,9% |
| Margem ex-AVP estável em 11,15% | 5,87 | 11,4% | 16,4% |
| Margem ex-AVP de 12,2% em 2030 | 6,81 | 12,6% | 25,8% |
| Crescimento −2 p.p. em 2027–30 | 6,13 | 11,6% | 18,3% |
| ROIC_T 22% e ROE_T 30% | 6,67 | 12,4% | 21,9% |
| Múltiplos pré-eleição (20x / 9x) | 7,88 | 12,1% | 38,5% |
| Payout de 70% em 2027–30 | 6,54 | 12,1% | 21,4% |

A TIR inteira fica entre 11% e 13% em qualquer variação. A meta de 25% só aparece na TIR de 3 anos, e só com re-rating (P/L de saída ≥ ~16–20x).

## Não verificado
- As receitas da 4Bio no 2S25 (o analista estimou ~R$ 1,7 bi) e o valor dos arrendamentos da 4Bio baixados no 2T26.
- O custo marginal de novos arrendamentos e o efeito do fim do ICMS-ST de SP sobre o capital de giro de 2027.
- O 3T26, que ainda não estava disponível.
