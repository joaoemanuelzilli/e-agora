# Revisão independente — PLPL3 (Plano & Plano) · 26/10/2026

**Veredito: ajustada.** Corrigi dois pontos objetivos, ambos de efeito pequeno e para baixo: o IR do RET em 2026–28 e o valor dos minoritários. A conclusão do estudo se mantém, mas no fio da navalha. A TIR de dono fica em 25,2%, praticamente igual ao Ke, e o resultado depende de a margem se recuperar. Se a margem ficar no nível do 1S26, o valor justo cai abaixo do preço.

| | Valor justo | TIR implícita | TIR 3 anos | P(valor > preço) | Bear / bull |
|---|---|---|---|---|---|
| Analista (preço R$ 5,70, foto 13h02) | R$ 6,94 | 25,4% | 38,3% | 77% | 4,71 / 8,75 |
| Após revisão | **R$ 6,79** | **25,2%** | **37,5%** | 73% | 4,56 / 8,60 |

## O que conferi e está coerente

**Ações.** São 202,95 mi: 203,90 mi emitidas (B3) × (1 − 0,47% em tesouraria).

**DL-base de R$ 182,8 mi.** É a dívida bruta de 1.047,5 mais arrendamentos de 19,6, menos o caixa de 884,3.
- Os CRIs (79,2 + 670,5 = 749,7) estão nas linhas 2.01.04.03/2.02.01.03, que a CVM chama de "Financiamento por arrendamento". Já estão na dívida bruta.
- Os arrendamentos reais são o "Direito de uso a pagar" (2,5 + 17,2). Não há dupla contagem.

**`other_debt_like` de 100.** É o dividendo de R$ 0,4928/ação: aprovado em 22/12/25, ex em 29/12/25, pago em 01/07/26. Ele está em "Dividendos e JCP a pagar" (100,0) no balanço de 30/06, então o caixa-base ainda o contém.

**Juros capitalizados (+2,0 p.p.).**
- A medida bate com o 2T26: margem bruta de 27,7% na CVM contra 29,7% ajustada.
- O ajuste é neutro no LL. O resultado financeiro de 2026E na base CVM fica em −26,5, contra −14,7 no LTM, coerente com a DL maior.
- A troca do EV/EBITDA-alvo de 3,5x para 3,0x preserva o valor da perna: R$ 6,18 com a regra antiga, R$ 6,08 com a nova.

**WACC.** O Kd de 0,235 equivale a 15,5% sem escudo fiscal (RET). Com peso de dívida de 15%, o WACC fica em 23,6%. Não há dupla contagem com o ajuste de juros capitalizados: a dívida que os gera (CRI/SFH) está na DL.

**Crescimento.**
- 2026: os +10% implicam um 2S26 com +3,6% a/a, depois de um 1S26 com +18,7%. É conservador.
- 2027–30: 5–6% a.a., contra CAGR de 29,5% em 2020–25. Coerente com o corte de lançamentos.

**Margem EBITDA (base CVM).** O modelo vai de 12% para 14,5%. O 1S26 ficou em 11,2% e a média de 5 anos é 15,5%. A recuperação é parcial e fica abaixo do histórico.

**Minoritários de 13% do LL.** O realizado foi 12,0% (2024), 14,4% (2025), 12,9% (LTM) e 15,9% (1S26).

**Perpetuidade.**
- ROE terminal de 22%, abaixo do Ke, o que dá P/VP justo de 0,85x.
- ROIC terminal de 18%. A intensidade de capital do próprio modelo implica ~22%, então a hipótese é levemente conservadora.

## Achados

| # | Sev. | Achado | Evidência | Efeito (valor justo / TIR) |
|---|---|---|---|---|
| 1 | média · **corrigido** | IR subestimado em 2026–27 | O IR do RET incide sobre a receita. IR/ROL foi de 2,3% (2023), 2,2% (2024), 2,6% (2025), 2,8% (1T26) e 3,0% (2T26). No 1S26, a alíquota sobre o LAIR foi de 30%. O modelo aplicava 19% sobre um LAIR deprimido, o que dava só 2,0% da ROL em 2026 e 2,2% em 2027 | O LL de 2026E cai de 269 para 250 e o de 2027E de 311 para 298. −R$ 0,06 / −0,2 p.p. |
| 2 | baixa · **corrigido** | `minority_value` de 200 fora da regra da própria nota | A regra é 13% × equity 100%. Pelo DCF, o equity 100% é EV 2.052 − DL 183 − 100 = 1.769, o que dá 13% de 230 | −R$ 0,09 / 0 |
| 3 | **alta (risco, não erro)** | A tese depende da margem | A margem bruta ajustada caiu 4,8 p.p. a/a no 2T26 e o 3T26 não foi verificado. O REF de 37,5% contra 29,7% é uma diferença atípica | Margem CVM em 12→13%, sem recuperação: R$ 5,97 / 23,1%. Margem no nível do 1S26 (~11,5–12%): R$ 5,46 / 21,7%, abaixo do preço |
| 4 | média (mantido) | Capital de giro de 0,60 é otimista diante da tendência | O CG operacional que calculei (clientes + estoques CP/LP + outros − fornecedores − terrenos a pagar − adiantamentos − obrigações/provisões) foi de 0,33x (2023), 0,33x (2024), 0,45x (2025) e 0,51x (2T26). O marginal 2023→2T26 foi de 0,77x bruto e 0,56x líquido de cessões; o de 2024→2T26, de 1,01x e 0,70x | 0,74 → R$ 6,49 / 24,8% |
| 5 | média (método, mantido) | Cessões de R$ 304 mi (238,7 CP + 65,2 LP) fora da DL | É defensável como par casado: os recebíveis cedidos ficam no ativo, dentro do capital de giro, que o DCF nunca libera. Tirar só o passivo puniria duas vezes. Mas isso exige que a cessão seja rolada e que o custo ≈ o rendimento do pró-soluto, e nenhuma das duas coisas foi verificada | Como dívida: R$ 5,86 / 25,2% |
| 6 | baixa | Derivativos passivos de R$ 27,8 mi (2,2 + 25,6) fora da DL | A DFC do 1S26 mostra MTM de swap de −40,5. Natureza e objeto do hedge não verificados | Como dívida: −R$ 0,09 |
| 7 | baixa (conservador) | Kd cai de 14,5% para 12,5%, com o DI1F29–F31 em 15,4–15,7% | A DL é pequena e vira caixa em 2028 | Kd plano em 14,5% → +R$ 0,004 |
| 8 | baixa (conservador) | Payout de 45–50% em 2028–30, abaixo do FCFE/LL do próprio modelo (64–73%) | O caixa líquido chega a R$ 273 mi em 2030. O DDM avalia esse caixa só pelo rendimento (~13%) a Ke de 25%. Mantido: após a queima de caixa, política conservadora é plausível | Payout de 60–70% em 2028+ → R$ 6,91 / 26,7% |

Nota de motor, que vale para todo o estudo: o `other_debt_like` não entra na DL da projeção. O dividendo de 100 pago em 01/07 continua rendendo juros no lucro, ~R$ 12 mi/ano antes de IR (3–4% do LL de 2026–27). Não alterei.

## Mudanças em `research/PLPL3.json` (original em `research/review/PLPL3.orig.json`)
- **`adjustments.minority_value`:** 200 → 230.
- **`projection.other_financial`:** [−72,2, −75,8, −80,4, −85,2, −89,4] → [−98,6, −93,9, −85,4, −85,2, −89,4].
  - Isso leva o IR total a 2,6% da ROL em 2026–28. Usei `other_financial`, e não `tax_rate`, para não inflar o IR da FCFF: 19% × EBIT ≈ 2,5% da ROL, já próximo do RET.
- **Efeito total:** valor justo de R$ 6,94 para R$ 6,79; TIR implícita de 25,4% para 25,2%; TIR em 3 anos de 38,3% para 37,5%; P(valor > preço) de 77% para 73%.
- O motor foi re-rodado (`EAGORA_SNAPSHOT=1`).

## O que não deu para verificar
- Prévia e resultado do 3T26, o teste decisivo da margem.
- Indexador e prazo dos CRIs (R$ 750 mi) e covenants.
- Custo das cessões contra rendimento do pró-soluto cedido, e se a cessão será rolada.
- Objeto dos derivativos.
- Aplicações com restrição (citadas na DFC) e se parte do caixa é restrita.
- Composição acionária: participação da Cyrela.
