# Revisão independente — ASAI3 (Assaí) · G05 · 26/10/2026

**Veredito: ajustada.** O custo da dívida líquida estava mal calibrado e há correções de texto. A conclusão não muda: o papel não entrega Ke de 25% e a fragilidade fica maior. Valor justo R$ 2,48 → **R$ 2,24**; TIR de dono (implícita) 14,2% → **13,4%** ao preço da foto (R$ 8,63); TIR de 3 anos 14,0% → 7,9%.

## Achados

| # | Severidade | Achado | Evidência | Ação |
|---|---|---|---|---|
| 1 | **Média (erro objetivo)** | `cost_of_net_debt` de 2026 (13,0%) anualizava só o 2T26, um trimestre com receita financeira pontual, e contradiz o 1S26 já realizado | 13,0% × DL 22.520 = −2.928 = 4 × o 2T26 (−732). O release do 2T26 mostra "Outras receitas e atualizações monetárias" de +125 (contra +15 no 1T26 e +57 no 2T25), dos quais **~R$ 70 mi são atualização monetária de créditos tributários**. A receita financeira CVM foi de 172 contra 74 no 1T26. O 1S26 CVM já soma −1.602; para fechar o ano em −2.928, o 2S26 teria de ser −663/tri, contra −802/tri recorrente no 2T26 | Recalibrado |
| 2 | Média (coerência) | Mesmo com o CDI do próprio analista (14,5/14/13/12,5%), o kd de 2027–30 ficava ~1,1 p.p. baixo | Recorrente do 1S26 (release, pré-IFRS16 + arrendamentos): encargos da dívida −1.183, arrendamentos −617 (~11,6% a.a.), antecipação −40, caixa +98, outras ex-pontual +70 ⇒ **−3,34 bi/ano = 15,2% da DL** com CDI de ~14,75%. Parte fixa ≈ 1,5 bi (arrendamentos + spreads); exposição a CDI ≈ 12,4 bi (DL ex-arrendamentos líquida de derivativos + recebíveis descontados), caindo com a desalavancagem do motor. Resultado: 14,7/14,4/13,8/13,5% contra 13,6/13,4/12,8/12,4%. Histórico do custo efetivo sobre a DL incluindo arrendamentos: 15,3% (2023), 13,9% (2024), 15,9% (2025) | Recalibrado |
| 3 | Média (premissa de juízo, mantida) | O caminho de CDI do analista fica abaixo da curva DI de hoje em 2028–30 | Forwards implícitos (DI1F27 13,76% · F28 14,95% · F29 15,36% · F31 15,66%): ~15,2% (2027), ~15,8% (2028), ~16% (2029–30). O analista usa 14,5/14/13/12,5%, entre o Focus pré-choque e a curva, e documenta a escolha | Mantido. Sensibilidade abaixo |
| 4 | Baixa (erro de texto) | A justificativa dos múltiplos tinha conta errada | Pré-eleição: 13,80 × 1.339 mi = R$ 18,5 bi, o que dá ~19x o LL LTM de 965 (o texto dizia ~13x). EV de 18,5 + 22,5 = R$ 41 bi sobre EBITDA LTM de 6,21 bi dá ~6,6x (o texto dizia ~5,7x). O resumo dizia "~8x P/L 2027E" a R$ 8,23: o motor dá ~10x antes da revisão e ~12x depois | Texto corrigido. Os múltiplos-alvo (8x / 5x) foram mantidos e ficam ainda mais conservadores do que o texto sugeria |
| 5 | Baixa (mantido) | A DL-base é a do 2T26, um pico sazonal | DL 2T26 22.520 contra 20.923 no 4T25 e média de 4 trimestres de 21.948. O ΔCG do motor não reverte a sazonalidade do 2S (fornecedores −1.623 no 1S26) | Mantido (convenção do motor). Com a média: VJ +0,14, TIR +0,3 p.p. |
| 6 | Info (ok) | O capex inclui as adições de direito de uso | ΔArrendamento + principal pago (DFC 6.03.09): 1.086 (2023, 1,6% da RL), 749 (1,0%), 1.159 (2025, 1,5%) e 398 no 1S26 (1,05%). A premissa de ~1,4% é coerente. O capex caixa de 2026 (~0,9%, R$ 0,7 bi) bate com o guidance. O MDR de cartões não está no resultado financeiro da Assaí (não há essa linha no release), então o problema do GMAT3 não se repete aqui | — |
| 7 | Info (ok) | Margem, D&A, IR, payout e ações | Margem do 1S26 sem créditos de PIS/COFINS ≈ 7,5–7,6%; o 2S26 implícito sem créditos ≈ 7,7% contra 7,8% no 2S25 ex-impairment. A margem de 7,8–8,0% em 2027–30 é levemente otimista, mas plausível. D&A de 2,4% contra 2,45% no 1S26. IR de 25–27% contra 27% efetivo no 1S26. Payout de 25–40% (mínimo estatutário de 25%). Ações: 1.339,3 mi (B3 líquido de tesouraria) | — |
| 8 | Info | Dívida, itens debt-like e o DCF negativo | DL = 16.282 + 10.711 − 4.473 = 22.520 (ok). Recebíveis descontados (1.123) e convênio (959) entram como debt-like, por juízo conservador; sem o convênio, VJ +0,09. Derivativos (533) entram como ativo, corretamente. O DCF dá −1,87/ação: o EV a WACC de 17,4% (R$ 21,6 bi, 3,4x o EBITDA 27E) fica abaixo de DL + debt-like (24,1 bi). O motor zera métodos negativos sem redistribuir o peso, então o VJ fica = 25% DDM + 25% múltiplos | — |
| 9 | Info (pipeline) | `data/hist`: os juros de arrendamento estão contados em dois campos | `lease_paid` 2025 (1.471) = principal 325 + juros 1.146 (DFC 6.03.09 + 6.03.10). `interest_paid` (3.338) = juros de empréstimos 2.192 + os mesmos 1.146 | Não afeta o motor. Afeta qualquer métrica que some os dois campos |

## Mudanças em `research/ASAI3.json` (original em `research/review/ASAI3.orig.json`)
- `projection.cost_of_net_debt`: [0,130; 0,136; 0,134; 0,128; 0,124] → **[0,143; 0,147; 0,144; 0,138; 0,135]**. Resultado financeiro: 2026E −2.928 → −3.220 (o 2S26 implícito passa a ser −809/tri, contra −802 recorrente no 2T26); 2030E −2.542 → −2.831.
- Efeito: LL 2026–30E de 1.633/1.094/1.402/1.789/2.085 → 1.414/907/1.222/1.600/1.874. DDM 3,40 → 3,03; múltiplos 6,53 → 5,94; DCF sem mudança (−1,87).
- **Valor justo de R$ 2,48 → R$ 2,24 (−10%). TIR implícita de 14,2% → 13,4% (13,7% a R$ 8,23; 10,5% no preço pré-eleição). TIR de 3 anos de 14,0% → 7,9%.** Monte Carlo: p50 2,24, p10–p90 1,28–3,71, P(valor > preço) = 0%.
- Textos: `target_multiples.rationale` (19x / 6,6x), `summary` (~12x P/L 27E; TIR ~13,5%) e uma nota de revisão em `overrides.notes`.

## Sensibilidade (nova base, preço R$ 8,63)
| Cenário | VJ | TIR | TIR 3a |
|---|---|---|---|
| Base revisada | 2,24 | 13,4% | 7,9% |
| kd original do analista | 2,48 | 14,2% | 14,0% |
| CDI na curva DI (15,2/15,8/16/16%) | 2,08 | 12,1% | −1,2% |
| Margem 2027–30 de 7,6% (sem créditos, nível do 1S26) | 1,95 | 12,1% | −1,7% |
| Margem de 8,2% (créditos recorrentes permanecem) | 2,48 | 14,0% | 12,7% |
| DL-base pela média de 4 trimestres | 2,38 | 13,7% | 10,2% |
| ROIC_T 18% e ROE_T 22% | 2,28 | 13,8% | 7,9% |
| wd 57% e Kd 13,5% (WACC 15,8%) | 2,29 | 13,4% | 7,9% |
| Múltiplos-alvo de 12x P/L e 6,5x EV/EBITDA | 3,48 | 13,4% | 29,4% |

Nenhuma variação razoável leva a TIR implícita perto de 25%. A TIR de 3 anos é dominada pelo P/L de saída: só supera Ke se o mercado voltar a pagar ~12x em 2028.

## Não verificado
- Indexadores, prazos e cronograma da dívida (as notas do ITR não foram lidas). Supus a dívida toda em CDI depois dos derivativos e os arrendamentos a taxa contratual fixa.
- O efeito da CBS (2027) sobre os créditos recorrentes (~R$ 110 mi/tri) e o resultado do 3T26.
