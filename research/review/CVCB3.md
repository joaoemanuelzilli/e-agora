# CVCB3 — revisão independente (red team) · 26/10/2026

**Veredito: ok, sem alteração de premissas.** O tratamento dos recebíveis antecipados não tem dupla contagem e está alinhado à métrica que a própria empresa divulga (DL + antecipação). DL, ações e custo financeiro conferem. Mesmo variando todas as premissas relevantes, o valor justo fica entre R$ 0 e 0,6, contra preço de R$ 1,07: a conclusão de "armadilha" a Ke de 25% é robusta.

**Atenção ao líder.** A "TIR implícita 4,7%" mostrada não é uma TIR. O DDM é negativo a qualquer taxa (LL < 0 até 2030 e proventos zero), e o bisector devolve o piso `g + 0,2 pp`. O correto é exibir **"não definida / negativa"**. A TIR 3a também é indefinida (LPA 2029E < 0).

Preço da foto do estudo: R$ 1,07. Valor justo R$ 0,13. O DCF (−0,77) e o DDM (−0,24) entram como 0. EV/EBITDA 4,5x → R$ 0,51, com peso de 25%.

## O que conferi (ok)
- **DL-base.** R$ 349,9 mi = debêntures R$ 398,2 mi + arrendamentos R$ 142,6 mi − caixa R$ 190,9 mi (CVM 30/06). Sem arrendamentos, dá R$ 207 mi; o release mostra R$ 215 mi.
- **Ações.** 520,80 mi (`b3_vs_cvm` = 1). A amortização extraordinária de R$ 77 mi (09/10) foi paga com caixa e não muda a DL.
- **Recebíveis antecipados (R$ 1.358,2 mi) como `other_debt_like`.** São venda sem regresso, fora do balanço. Não há dupla contagem:
  - o DCF exclui o custo da antecipação do FCFF e desconta o saldo na ponte;
  - o DDM carrega o custo no LL e não desconta o saldo;
  - o EV/EBITDA-alvo foi derivado do EV econômico pré-eleição (mcap 818 + DL 350 + antecipação 1.358 = R$ 2,53 bi / EBITDA aj. R$ 440 mi = 5,7x) e é aplicado na mesma base.
- **Custo financeiro.**
  - O total do motor em 2026E (R$ 319 mi) fica igual ao LTM da CVM (R$ 323 mi).
  - A antecipação custou ~14,6% a.a. no 2T26 (R$ 49,7 mi × 4 / R$ 1.358 mi), ou seja, ≈ CDI. Com os forwards (15,2–16%) e o volume crescendo, ela dá ~R$ 210–220 mi/ano. Somando outros itens, chega-se a −R$ 260–285 mi, coerente com a curva de hoje.
  - A dívida é CDI+3,90%; o custo da DL (17–18%) está ~1–2 pp abaixo do marginal, mas o efeito é imaterial (R$ 5 mi/ano).
- **Margem.** 29–31% no conceito ajustado, contra 29,8% do EBITDA aj. LTM. O 2S26 implícito (−19% a/a no EBITDA ajustado) é duro, mas compatível com o 2T26 (−8%) mais o choque do dólar.
- **Receita.** −3% em 2026 (1S26: −1,8%), depois +2–5%. Entre 2019 e 2025, a receita caiu 2,3% a.a.

## Achados menores (não alterados; nenhum muda a conclusão)
1. **EV/EBITDA-alvo 4,5x, abaixo da regra (4,9x) (baixa, julgamento).**
   - As justificativas são "prejuízo recorrente e covenant". O prejuízo decorre do custo da antecipação, que já entra como dívida na ponte. O covenant está folgado (0,5x contra 2,5x, pelo próprio dossiê).
   - Com 4,9x: justo R$ 0,21. Não alterei por simetria com os prêmios de "qualidade" que outros analistas aplicam à regra (MULT3, IGTI11), também discricionários e pequenos.
2. **IR zero com LAIR < 0 (baixa).** A empresa paga R$ 40–54 mi/ano de IR em controladas lucrativas e na Argentina, mesmo com prejuízo consolidado (LTM −R$ 54 mi). O motor zera o IR, o que deixa o prejuízo projetado ~R$ 45 mi/ano menos negativo. Não afeta o justo (DDM já em zero).
3. **IFRS-16 incompleto no fluxo (baixa).** A D&A de 15,5% inclui a depreciação do direito de uso e os arrendamentos estão na DL, mas o capex de 9% não inclui as adições de direito de uso (+R$ 97 mi no 1T26). O FCFF fica superestimado em ~R$ 40–50 mi/ano. Não afeta o justo (DCF negativo); na ponte do múltiplo, o efeito é −R$ 0,04.
4. **Saldo de antecipação estático.** Cresceu R$ 307 mi a/a. Se crescer mais R$ 300 mi, o justo vai a R$ 0,00.

## Sensibilidade (testes do revisor)
| Teste | Justo | Observação |
|---|---|---|
| Base | 0,13 | |
| EV/EBITDA 4,9x (regra pura) | 0,21 | |
| Margem +2 pp (plano de eficiência de >R$ 80 mi capturado em parte) | 0,19 | LL ainda negativo até 2030 |
| Margem no conceito CVM (~33%) | 0,23 | |
| Bull (margem +3 pp, crescimento +4 pp) | 0,39 | LL positivo só em 2029; TIR implícita ~10% |
| 50% do IR diferido ativo (R$ 260 mi) como ativo | 0,25 | Monetização incerta sem lucro tributável |
| Antecipação +R$ 300 mi | 0,00 | |
| Tratamento alternativo (custo da antecipação no EBITDA, sem dívida extra, 4,1x pela regra) | ~0,35 | Coerente com os R$ 0,33 do dossiê |
| Só o múltiplo (100%) | 0,51 | Teto |

## Não verificado
- Saldo e custo da antecipação vêm do release (fora do balanço, sem nota CVM no hist).
- Composição da diferença entre EBITDA CVM (LTM R$ 474 mi) e ajustado (R$ 440 mi): efeitos cambiais operacionais reclassificados versus não recorrentes.
- Prazo de recuperação dos R$ 520 mi de IR diferido ativo.
