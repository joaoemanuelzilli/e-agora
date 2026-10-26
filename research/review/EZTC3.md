# Revisão independente — EZTC3 (EZTEC) · 26/10/2026

**Veredito: ok.** Não encontrei erro objetivo. Há premissas puxando para os dois lados: o EV/EBITDA-alvo é generoso, o crescimento de 2026 é otimista e a queda de juros reduz o lucro de uma empresa com caixa líquido. A conclusão se sustenta em todos os testes: valor justo entre R$ 10,3 e 11,3, abaixo do preço de R$ 12,12, e TIR de 14–15,5%, contra Ke de 25%.

| | Valor justo | TIR implícita | TIR 3 anos |
|---|---|---|---|
| Analista (preço R$ 12,12, foto 13h02) | R$ 10,69 | 14,6% | 22,3% |
| Após revisão (sem alteração) | R$ 10,69 | 14,6% | 22,3% |

## O que conferi e está coerente

**Ações e balanço.**
- São 277,36 mi de ações, com tesouraria zerada no 2T26 (linha de −45,2 cancelada) e bonificação de ~27%: o capital foi de 2.889 para 4.301.
- A DL é −1,4 (caixa 1.793,6 contra dívida 1.792,2). O PL do controlador é 5.232.
- Os recebíveis CP+LP somam 390,5 + 1.268,8 = 1.659,3, o que confere com o dossiê.

**Juros capitalizados (+2 p.p.).**
- Os R$ 14,8 mi do 1S26 equivalem a 2,1% da receita.
- `other_financial` de 202 em 2026 = resultado financeiro anualizado do 1S26 (118 × 2 = 236) − ~33 de juros capitalizados.
- O lucro de 2026E (528) fica em linha com o LTM (531).

**Margem, IR e minoritários.**
- Margem na base CVM de 23,5–24%: a média 2021–25 foi 25,9% e o 1S26, 21,9%.
- IR de 9%: a média 2021–25 foi 8,5% e o LTM, 8,8%.
- Minoritários de 3%: 2,4% em 2025 e 3,3% no LTM.

**Capital de giro marginal de 1,0x.** O CG que calculei (recebíveis CP+LP + estoques CP+LP − "outros" CP e LP) foi:
- 4.078 (2023), 4.550 (2024), 4.585 (2025) e 4.587 (2T26), entre 2,9x e 3,8x a receita;
- marginal de 0,99x em 2023→24 e de 1,43x em 2023→2T26, este último inflado pela obra do Esther.

**Ativos não operacionais.**
- Esther: NOI de 111 a cap rate de 10% = 1.110. Descontando 75 de tributos e 125 de custo a incorrer, e trazendo 1 ano a 15%, chega a ≈ 791. A dívida da EZ INC (575) está na DL e o aluguel ficou fora da receita, então não há dupla contagem.
- Carteira: 90% × 756. Os juros ficam só no resultado financeiro, fora do FCFF.

**Ajustes de dividendo.** O `other_debt_like` de 26 corresponde ao dividendo do 2T26 (data-com 13/08), posterior ao balanço-base.

**Pesos 70/10/20.** A justificativa procede: o DDM não enxerga o Esther, cujo aluguel foi excluído do lucro. Com os pesos padrão 50/25/25, o valor seria R$ 10,36.

## Achados (nenhum exige correção)

| # | Sev. | Achado | Evidência | Sensibilidade (valor justo / TIR) |
|---|---|---|---|---|
| 1 | média | EV/EBITDA-alvo de 6,0x é a mediana dos pares, e sobre EBITDA ajustado (+2 p.p.), ≈ 6,5x na base CVM | No CYRE3 o mesmo estudo usa o p25 (4,6x ajustado ≈ 5,1x CVM) pelo "regime de juros mais alto". O EV/EBITDA operacional histórico da EZTEC, tirando ~R$ 1,5 bi de ativos não operacionais, é ~4–5x | 4,7x → R$ 10,47 |
| 2 | média | Receita de 2026 com +10% exige 2S26 de ~R$ 949 mi (+29% a/a), quando o 1S26 caiu −8% e o 2T26 −16% | Apoio: o CEO fala em "~R$ 500 mi/trimestre" e os lançamentos foram de R$ 2,36 bi em 2025 e R$ 2,42 bi no 9M26. Contra: VSO de 12,9% no 3T26 | +1% em 2026 → R$ 10,40 / 14,1% |
| 3 | baixa (conservador) | Kd cai de 14% para 11,5% e `other_financial` de 202 para 153, com o DI1F29–F31 em 15,4–15,7% | Com caixa líquido crescente (DL de −606 em 2030), a queda de juros reduz o lucro | Kd de 14,5% e OF estável em 202 → R$ 10,77 / 15,5% |
| 4 | baixa | Capex abaixo do D&A em 2028–30 (1,0% contra 1,5%) | Em 2021–25, capex ≈ D&A ≈ 1,4% da receita; no 1S26, o capex foi de 4% | Capex = D&A → R$ 10,65 |
| 5 | info | ROIC terminal de 11% contra ROIC do modelo de 8,2% em 2030 | O denominador inclui os ativos não operacionais. O ROIC operacional ex-ativos fica em ~12%, e o marginal no período explícito em ~22% | ROIC_T de 8% → R$ 10,27 |
| 6 | info | A TIR implícita (via DDM) não inclui a monetização do Esther nem da carteira | Somando R$ 1,2/ação em 2027 (Esther líquido da dívida da EZ INC): 15,6%. Somando R$ 3,6/ação (Esther + carteira, teto): 18,4% | Continua abaixo de 25% |
| 7 | info | Cap rate do Esther | Cap rate de 8% (sell-side pré-choque) → R$ 11,32; de 11% → R$ 10,43 | — |

- **Outras sensibilidades:** margem −1,5 p.p. → R$ 10,25 / 14,1%; capital de giro de 1,4x → R$ 10,25.
- Nenhuma combinação plausível leva o valor justo ao preço.

## Mudanças
Nenhuma. `research/EZTC3.json` não foi alterado e o motor não foi re-rodado.

## O que não deu para verificar
- Custo a incorrer do Esther (premissa de R$ 125 mi) e cap rate de mercado pós-choque para lajes AAA com contrato atípico.
- Composição exata do estoque LP (terrenos contra custo do Esther).
- Locação do Air Brooklin.
- Juros da EZ INC que vão ao resultado após a entrega do Esther. É provável que expliquem parte da queda de `other_financial`, mas isso não está documentado.
