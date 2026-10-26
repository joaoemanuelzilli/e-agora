# Revisão independente — BEEF3 (Minerva) · 26/10/2026

**Veredito: ajustada.** A trajetória de custo da dívida líquida contrariava a curva DI de hoje; foi corrigida. Com isso, **a TIR implícita cai de 26,3% para 24,5%, abaixo (por pouco) da Ke de 25%.** O valor justo segue bem acima do preço, mas a afirmação "única do grupo com TIR acima de 25%" deixa de ser robusta: a TIR fica na faixa de ~23–27% conforme premissas razoáveis. Original em `research/review/BEEF3.orig.json`.

Preço de referência (foto B3 13h02): R$ 3,38.

| | Antes | Depois |
|---|---|---|
| `cost_of_net_debt` 2026–30 | 21 / 20,5 / 20 / 19 / 18% | **21 / 21 / 21 / 20,5 / 20%** |
| Valor justo | R$ 5,57 | **R$ 5,44** (−2,3%) |
| DCF / DDM / P/L / EV/EBITDA | 6,37 / 3,66 / 3,70 / 8,09 | 6,37 / 3,27 / 3,41 / 8,09 |
| **TIR implícita** | 26,3% | **24,5%** |
| **TIR 3 anos** | 57,9% | **50,2%** |
| Lucro controlador 2027E / 2029E | 726 / 1.612 | 669 / 1.448 |
| LPA 2029E (base da saída da TIR 3a) | R$ 1,368 | R$ 1,230 |
| Cenários bear / base / bull (esperado) | 2,12 / 5,57 / 8,54 (5,13) | 1,97 / 5,44 / 8,41 (4,99) |
| Monte Carlo p10 / p50 / p90; P(valor > preço) | 1,87 / 5,52 / 10,01; 76,7% | 1,85 / 5,38 / 9,88; 73,6% |

## Achados
1. **(alta — corrigido) Custo da dívida líquida caindo de 21% para 18% sem respaldo na curva.** No 1S26, o resultado financeiro contábil foi −R$ 1.523 mi: 1T26 −766 e 2T26 −757 sobre DL média de R$ 13,3–14,1 bi, ou seja, **~22–23% a.a.** (variação cambial e hedge se compensaram: +251/−243 e −35/+82). Isso com CDI médio de ~14,6%. A curva de hoje (F27 13,76%, F28 14,95%, F29 15,36%, F31 15,66%) implica CDI a termo de ~15,2–16% em 2027–30, *acima* do 1S26. Ela encarece os R$ 8,9 bi de dívida em reais (majoritariamente pós-fixada) e o carrego do hedge cambial. A queda para 18% só faria sentido com Selic em queda (o Focus pré-choque) ou com forte redução da dívida bruta, e não há sinal disso: a dívida bruta foi de R$ 27,8 bi (dez/25) para R$ 29,3 bi (jun/26), com Notas 2036 novas. Correção: 21% até 2028 e 20,5%/20% em 2029–30, com algum crédito a recompras de bonds. É ainda generoso frente ao run-rate contábil de 22–23%. Com a curva "cheia" (21,5–22%), a TIR implícita seria 22,7% e o valor justo R$ 5,27.
2. **(média — mantido, julgamento) Kd do WACC de 13% está no limite inferior.** O custo médio sobre a dívida bruta é ~10,7% em juros + ~1,75% em hedge/taxas (R$ 514 mi LTM) = ~12,5%, mas o custo marginal subiu com a curva (+~300 bp na parcela em reais) e com o spread de high yield. Uma estimativa coerente com hedge de ≥50% da exposição fica em ~14–15%. Com Kd de 15%: WACC 17,4% e valor justo R$ 5,03. A TIR implícita (DDM) não muda.
3. **(média — informativo) O DCF (50% do peso) é o método mais favorável, e o benefício fiscal é otimista para quem quase não paga IR.** O WACC aplica 34% de benefício fiscal à dívida (regra do motor), mas a Minerva registra crédito de IR há anos (2023 +54, 2025 +150, LTM +166; IR corrente de só R$ 26–113 mi/ano). Em compensação, o FCFF cobra 15–22% de IR sobre o EBIT (~R$ 0,6–1,1 bi/ano), muito acima do IR pago, então os efeitos se compensam em boa parte. Sem benefício fiscal no WACC: valor justo R$ 4,21. É o maior risco de método da tese. Nota: o DCF (R$ 6,37) fica no dobro do DDM (R$ 3,27) porque não enxerga o carrego negativo de manter R$ 14,9 bi de caixa (~4–5% em US$) contra dívida bruta de R$ 29,3 bi.
4. **(baixa — mantido) Múltiplos-alvo inconsistentes entre si.** 4,8x EV/EBITDA 2027E implica ~12x P/L 2027E (EV 23.794 − DL 14.381 − 603 = equity de R$ 8,8 bi ex-bônus, sobre lucro de R$ 726 mi), contra P/L-alvo de 6x. Além disso, 4,8x fica acima do que os preços-alvo publicados implicam (~4,2x) e da faixa pós-Marfrig (3,8–4,2x). Com 4,2x: valor justo R$ 5,12.
5. **(ok) Bônus de subscrição.** 187,0 mi de bônus × R$ 4,975 = R$ 930 mi. Bate com a emissão de 2025 (386,8 mi de ações a R$ 5,17, 1 bônus para cada 2 = 193,4 mi; 6,4 mi já exercidos, o que bate com 994,13 → 1.000,54 mi de ações). Diluição total (1.178,1 mi) com PV de R$ 720 mi no DCF/EV-EBITDA e R$ 930 mi em 2027 na DL projetada: consistente, sem dupla contagem. Como o valor justo (~R$ 5,4) fica perto do strike, o método é razoável: sem bônus, o valor seria R$ 5,92/ação e a TIR 25,6%.
6. **(ok) Ações e DL.** 991,14 mi em circulação (CVM 30/06: 1.000,54 − 9,40 em tesouraria = B3). DL de R$ 14.449 mi = dívida 29.298 (ME 20.389; MN 8.908) − caixa e aplicações 14.935 + arrendamentos 87. Confere com o release (R$ 14.363 mi ex-arrendamentos).
7. **(não verificado — risco relevante) "Outras contas a pagar" de R$ 5.254 mi no passivo circulante** (9% da receita; R$ 1,8 bi em 2023, salto de +R$ 2,7 bi em 2024 com a Marfrig). A variação passa pelo caixa operacional e acompanha a receita, o que sugere adiantamento de clientes (operacional). Se houver derivativos passivos ou obrigações de aquisição ali dentro, a DL estaria subestimada: cada R$ 1 bi equivale a ~R$ 0,53/ação no valor justo.
8. **(informativo) Efeitos não modelados, em direções opostas.** (a) Capital de giro: o 1S26 consumiu R$ 2,0 bi (fornecedores −R$ 1,0 bi), e historicamente o 2º semestre gera muito mais caixa (CFO 2S25 R$ 4,3 bi contra 1S25 R$ 0,4 bi). Se R$ 1 bi voltar no 2S26: valor justo R$ 6,20, TIR 26,6%. (b) Câmbio a R$ 5,49: a parcela não hedgeada da dívida em US$ eleva a DL (~+R$ 0,5 bi), enquanto o EBITDA dolarizado sobe. Teste conjunto: valor justo R$ 5,38, TIR 24,3%.

## Checagens contra o histórico CVM (ok)
- Margem EBITDA 2021–25: 8,8 / 9,2 / 9,5 / 9,1 / 8,8%; 1S26 8,5%; LTM 8,6%. Premissa 8,2–8,8%: abaixo da média, coerente com o ciclo do gado e a salvaguarda chinesa. **É a premissa de maior alavanca:** margem 8,0–8,2% → valor justo R$ 4,43, TIR 21,0%; média de 9,1% → R$ 6,57, TIR 27,2%.
- D&A 1,8% (LTM 1,78%); capex 2,0–2,1% (LTM 2,0%); capital de giro de 10% da receita incremental, conservador (capital de giro comercial ~4,5% da receita).
- IR 15% → 22% sobre o LAIR contra efetivo negativo nos últimos anos: conservador para o lucro.
- Payout 25/25/35/50/50%: a DL/EBITDA projetada fecha 2028 em 2,44x (≤2,5x dispararia 50% já em 2028; efeito +R$ 0,02). Minoritários 5% do lucro (2025 4,5%; 1S26 13%).
- ROIC_T 15% e ROE_T 20%, abaixo dos projetados para 2030 (20,5% e 32,7%, com PL pequeno): conservador.

## Sensibilidade (após a correção)
| Teste | Valor justo | TIR impl. | TIR 3a |
|---|---|---|---|
| Base corrigida | 5,44 | 24,5% | 50,2% |
| Custo da DL na curva cheia (21,5–22%) | 5,27* | 22,7%* | 43,3%* |
| Kd do WACC 15% | 5,03 | 24,5% | 50,2% |
| Sem benefício fiscal no WACC | 4,21 | 24,5% | 50,2% |
| EV/EBITDA-alvo 4,2x | 5,12 | 24,5% | 50,2% |
| Margem 8,0–8,2% | 4,43 | 21,0% | 32,8% |
| Margem 9,1% (média de 5 anos) | 6,57 | 27,2% | 62,7% |
| Capital de giro devolve R$ 1 bi no 2S26 | 6,20 | 26,6% | 60,9% |
| Sem bônus (991 mi de ações) | 5,92 | 25,6% | 54,8% |
| P/L de saída 8x | 5,58 | 24,5% | 70,4% |
\* calculado sobre a premissa original nos demais itens.

**Leitura:** o valor justo fica acima do preço em quase todos os testes (o bear é R$ 1,97), mas a TIR implícita fica em torno da Ke, de ~21% a ~27%. A TIR de 3 anos é alta (33–70%) porque supõe que o lucro triplica até 2029 e reprecifica a 6x: é uma opção alavancada em margem e juros, não uma TIR "de dono" folgadamente acima de 25%. Recomendo descrever BEEF3 como "TIR ≈ Ke, com assimetria positiva no valor e risco alto", e não como "acima da Ke".

## O que não deu para verificar
- Composição de "Outras contas a pagar" (R$ 5,25 bi) e posição de derivativos (MTM) em 30/06/26.
- Moeda do caixa (quanto dos R$ 14,9 bi está em US$) e notional/estrutura do hedge; PTAX de 30/06/26 contra R$ 5,49 de hoje.
- Cronograma de amortização por moeda e se a empresa vai usar caixa para reduzir a dívida bruta.
- Resultado do 3T26 (início de nov/2026).
