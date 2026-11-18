# Checagens da regra de decisão

Gerado em 2026-11-18 sobre a foto de preços de 28/10/2026 (Ke = 25%). Script: `pipeline/tests/decision_checks.py`.

## 1. Lista de acompanhamento e elegíveis para compra

A regra original (TIR ≥ 20%, chance ≥ 45%, Altman fora de risco, confiança diferente de baixa; 8 primeiras pelo escore) define a **lista de acompanhamento**. É **elegível para compra à meta** quem, dentro dela, tem TIR de dono ≥ Ke e preço ≤ preço-teto (o menor entre o DDM a Ke e o valor justo).

| Ação | Preço | Preço-teto | Folga até o teto | TIR de dono | Chance MC | Situação |
|---|---:|---:|---:|---:|---:|---|
| VTRU3 | R$ 11,98 | R$ 12,95 | 8,1% | 26,3% | 90% | elegível à meta |
| BEEF3 | R$ 2,87 | R$ 3,22 | 12,3% | 26,9% | 75% | elegível à meta |
| SEER3 | R$ 11,03 | R$ 10,44 | -5,4% | 24,1% | 81% | acompanhamento (acima do teto) |
| MDNE3 | R$ 16,86 | R$ 18,65 | 10,6% | 27,1% | 76% | elegível à meta |
| PLPL3 | R$ 4,84 | R$ 5,64 | 16,4% | 27,8% | 80% | elegível à meta |
| TEND3 | R$ 21,22 | R$ 21,22 | 0,0% | 25,0% | 77% | elegível à meta |
| CEAB3 | R$ 6,87 | R$ 5,60 | -18,5% | 21,8% | 47% | acompanhamento (acima do teto) |
| COGN3 | R$ 1,69 | R$ 1,62 | -4,4% | 24,2% | 62% | acompanhamento (acima do teto) |

No universo, 6 empresas têm TIR ≥ 25%: HAPV3 (29,3%), PLPL3 (27,8%), MDNE3 (27,1%), BEEF3 (26,9%), VTRU3 (26,3%), TEND3 (25,0%). HAPV3 fica fora da lista por confiança baixa.

## 2. Sensibilidade da regra aos cortes

Quantas empresas passam nos quatro filtros para cada par de cortes (Altman e confiança mantidos; sem limite de tamanho). Entre parênteses, quantas das 8 da lista atual continuam.

| TIR mínima | Chance ≥ 35% | Chance ≥ 45% | Chance ≥ 55% | Chance ≥ 65% |
|---|---:|---:|---:|---:|
| 18% | 10 (8) | 9 (8) | 7 (7) | 6 (6) |
| 20% | 10 (8) | 9 (8) | 7 (7) | 6 (6) |
| 22% | 8 (7) | 7 (7) | 7 (7) | 6 (6) |
| 25% | 5 (5) | 5 (5) | 5 (5) | 5 (5) |

Com os cortes-base (20% e 45%), o tamanho da lista decide quem entra: 5 nomes: VTRU3, BEEF3, SEER3, MDNE3, PLPL3; 6 nomes: VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3; 8 nomes: VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3, CEAB3, COGN3.

## 3. Efeito do preço na TIR (mesmas projeções)

Queda mediana de preço na cobertura entre o fechamento de 23/10 e a foto de 28/10: -25,0%. TIR de dono mediana (116 empresas): 11,1% → 13,3%. Empresas com TIR ≥ 25%: 0 → 6; com TIR ≥ 20%: 2 → 18.

| Ação | TIR ao preço de 23/10 | TIR ao preço de 28/10 |
|---|---:|---:|
| VTRU3 | 18,6% | 26,3% |
| BEEF3 | 21,0% | 26,9% |
| SEER3 | 17,4% | 24,1% |
| MDNE3 | 17,5% | 27,1% |
| PLPL3 | 19,0% | 27,8% |
| TEND3 | 20,4% | 25,0% |
| CEAB3 | 14,0% | 21,8% |
| COGN3 | 16,3% | 24,2% |

É o efeito mecânico do preço com projeções fixas. Não mede quanto os negócios mudaram com juros, câmbio, demanda ou regulação.

## 4. Sensibilidades-chave das selecionadas

Choques aplicados aos cinco anos de projeção, um de cada vez, com o preço da foto. São sensibilidades condicionais, não previsões.

| Ação | TIR base | Margem EBITDA −2 p.p. | Crescimento −2 p.p. | Valor justo base | VJ com margem −2 p.p. |
|---|---:|---:|---:|---:|---:|
| VTRU3 | 26,3% | 24,7% | 24,6% | R$ 16,69 | R$ 15,03 |
| BEEF3 | 26,9% | 8,7% | 23,7% | R$ 5,04 | R$ 0,79 |
| SEER3 | 24,1% | 22,1% | 22,6% | R$ 13,81 | R$ 11,95 |
| MDNE3 | 27,1% | 25,1% | 25,9% | R$ 19,81 | R$ 17,85 |
| PLPL3 | 27,8% | 24,4% | 26,5% | R$ 6,25 | R$ 5,09 |
| TEND3 | 25,0% | 22,1% | 23,5% | R$ 26,34 | R$ 22,37 |
| CEAB3 | 21,7% | 17,8% | 20,3% | R$ 6,65 | R$ 4,21 |
| COGN3 | 24,2% | 21,4% | 22,3% | R$ 1,89 | R$ 1,48 |

**Vitru com IR de 17% nos cinco anos** (base: 4%, 5%, 6%, 8%, 12%; payout de 5%, 15%, 35%, 50%, 60%): valor justo R$ 16,69 → R$ 14,84; TIR 26,3% → 24,6%. A classificação acima de 25% depende do benefício fiscal projetado.

## 5. Ponte da data de avaliação

Antiga: avaliação em 26/10 e stub de 2026 inteiro descontado no meio do stub (prazo negativo de −0,07 ano para balanço de 30/06). Atual: avaliação em 28/10; a parte do stub já decorrida vira ponte de dívida líquida e patrimônio (caixa gerado menos proventos pagos), e só os fluxos posteriores entram no DCF, no DDM e na TIR. Hipótese: fluxos uniformes dentro do stub.

Efeito nas 117 empresas com modelo próprio: valor justo -2,0% na mediana (de -13,6% a 0,0%); TIR de dono -0,09 p.p. na mediana (mínimo -0,73 p.p.). TIR mediana 13,4% → 13,3%; empresas com TIR ≥ 25%: 6 → 6; ≥ 20%: 19 → 18.

| Ação | Valor justo antigo → atual | TIR antiga → atual | 1º prazo de desconto antigo → atual (anos) |
|---|---:|---:|---:|
| VTRU3 | R$ 16,99 → R$ 16,69 | 26,34% → 26,28% | -0,071 → +0,088 |
| BEEF3 | R$ 5,44 → R$ 5,04 | 27,18% → 26,91% | -0,071 → +0,088 |
| SEER3 | R$ 14,19 → R$ 13,81 | 24,42% → 24,08% | -0,071 → +0,088 |
| MDNE3 | R$ 20,19 → R$ 19,81 | 27,79% → 27,05% | -0,071 → +0,088 |
| PLPL3 | R$ 6,37 → R$ 6,25 | 28,30% → 27,81% | -0,071 → +0,088 |
| TEND3 | R$ 26,81 → R$ 26,34 | 25,43% → 25,00% | -0,071 → +0,088 |
| CEAB3 | R$ 6,91 → R$ 6,65 | 22,08% → 21,75% | -0,071 → +0,088 |
| COGN3 | R$ 1,97 → R$ 1,89 | 24,56% → 24,23% | -0,071 → +0,088 |

