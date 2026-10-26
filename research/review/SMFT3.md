# SMFT3 — revisão independente (red team) · 26/10/2026

**Veredito: ajustada (mudanças pequenas).** O tratamento de IFRS-16 e do capex de expansão está correto. Corrigi duas coisas:
- o P/L-alvo comparava bases diferentes (recorrente × CVM);
- um JCP já fora do alcance do comprador tinha ficado de fora da ponte.

O valor justo quase não muda, porque o DCF é negativo e entra no blend como zero. O que muda é a TIR de 3 anos, que passa a superar a meta, mas de forma frágil (ver sensibilidade). A TIR implícita (DDM), de 13,6%, segue longe de 25%. Original em `research/review/SMFT3.orig.json`.

Preço da foto do estudo: R$ 16,44.

| | Antes | Depois |
|---|---|---|
| Valor justo | R$ 6,65 | **R$ 6,87** (+3%) |
| DCF / DDM | −3,35 (→ 0) / 5,69 | −3,41 (→ 0) / 5,69 |
| P/L / EV/EBITDA (perna de 25%) | 16,89 / 24,94 | 18,72 / 24,88 |
| TIR implícita (DDM) | 13,6% | 13,6% |
| TIR 3 anos (saída a P/L-alvo × LPA 2029E) | 24,1% | **30,0%** (saída de R$ 25,0 → R$ 27,7) |
| Cenários bear / bull / esperado | 4,25 / 9,02 / 6,40 | 4,37 / 9,27 / 6,60 |
| Monte Carlo p10–p50–p90 · P(valor > preço) | 4,52–6,62–10,04 · 0,4% | 4,65–6,84–10,31 · 0,5% |

## Achados

### 1. P/L-alvo derivado numa base e aplicado em outra (média, corrigido para cima)
- O 12x saiu do P/L "recorrente" pré-eleição de 18,6x, calculado sobre o LL recorrente da companhia de R$ 822 mi (+300 bp → 12x).
- O motor aplica esse múltiplo ao LPA **CVM/IFRS-16**: o LL de 2026E é R$ 667 mi, contra R$ 686,5 mi no LTM CVM. Ou seja, o próprio motor está na base CVM.
- A diferença entre as bases é persistente: R$ 48 mi no 2T26 e R$ 136 mi no LTM. Bate com o efeito IFRS-16 (depreciação do direito de uso + juros do arrendamento ≈ R$ 1,50 bi, contra aluguel ≈ R$ 1,26 bi) e, portanto, não é item pontual.
- Na base certa: P/L CVM LTM pré-eleição de 22,3x (R$ 15,29 bi / R$ 686,5 mi) → 4,5% + 3 pp = 7,5% → **13,3x**. Hoje, o P/L CVM LTM está em 14,7x; a saída a 13,3x continua sendo um *de-rating*.
- Impacto: valor justo +R$ 0,22; TIR 3a +5,9 pp.

### 2. JCP de junho fora da ponte (baixa, erro objetivo, corrigido)
- `other_debt_like` só tinha o JCP de dc 03/09 (pago em 30/10, R$ 40 mi).
- O calendário B3 mostra também o de dc 03/06/26 (R$ 0,0652/ação), pago em 31/07, depois do balanço. Ele aparece como R$ 37,3 mi em "Dividendos e JCP a pagar" na CVM em 30/06.
- Mudança: R$ 40 → **R$ 77,3 mi**. O efeito no valor é imaterial: −R$ 0,06 na perna EV/EBITDA, e o DCF já é negativo.

### 3. Proventos de 2025 maiores do que o dossiê indica (informativo, não alterado)
- O JCP declarado em 2025 foi ~R$ 620 mi: 3 × R$ 0,067 mais R$ 0,8417/ação em dez/25, ≈ 97% do LL.
- Cerca de R$ 377 mi foram **reinvestidos em ações** no 1T26: ações emitidas de 597,25 para 616,13 mi; o saldo a pagar caiu de R$ 475,5 para R$ 37,3 mi, com só R$ 148 mi pagos em caixa.
- Os "R$ 188 mi" de 2025 citados no dossiê são o caixa pago. A contagem do motor (613,7 mi) já inclui as ações novas.
- Se a prática (JCP alto com reinvestimento, para aproveitar o escudo fiscal) se repetir, haverá diluição de ~3% a.a., não modelada, e o IR efetivo tende a ficar abaixo dos 20–25% projetados para 2028–30. Os dois efeitos têm sinais opostos.

## O que conferi (ok)
- **IFRS-16 consistente.** O EBITDA exclui aluguel (48% vs 47,9% no LTM) e a DL inclui arrendamentos de R$ 6.529 mi. O capex inclui as **adições de direito de uso**: 50% → 31% da receita, contra 33% de capex físico + 20% de ROU no LTM.
- **Adições de ROU de R$ 1.590 mi em 2025.** O roll-forward do passivo confere: 5.401 + 1.590 + ~600 de juros − 1.219 pagos ≈ 6.274, com câmbio residual.
- **D&A.** Os 24% incluem a depreciação do direito de uso (~10,5% da receita).
- **WACC.** `wd` 0,40, contra 41,6% de mercado pré-eleição com arrendamentos.
- **Custo da DL de 11,7–12%.** Coerente com a curva:
  - Brasil: R$ 4,16 bi a CDI+0,65–1,05% (forward ~15,2–16%);
  - México: TIIE+;
  - arrendamentos: ~10,7% (juros de R$ 540 mi em 2025);
  - caixa: R$ 2,8 bi.
  - Resultado: ~11,6–12,0% sobre a DL de 2026–27E.
- **Ações e DL.** 613,71 mi (`b3_vs_cvm` = 1). DL CVM de R$ 10.876 mi.

## Sensibilidade das conclusões (sobre a versão corrigida)
| Teste | Justo | TIR | TIR 3a |
|---|---|---|---|
| Corrigido | 6,87 | 13,6% | 30,0% |
| P/L 12x (original) | 6,64 | 13,6% | 24,1% |
| Custo da DL 12,4% em todos os anos | 6,65 | 13,0% | 26,0% |
| Capex+ROU de 55% em 2026 (2S26 concentra 70–75% das aberturas) | 6,75 | 13,5% | 28,9% |
| Margem −1 pp | 6,40 | 13,0% | 24,3% |
| Crescimento −2 pp/ano | 6,31 | 12,5% | 21,8% |
| ROIC terminal 25% (DCF ainda −0,61 → 0) | ≈6,9 | 13,6% | 30,0% |

**Leitura.** A TIR 3a de ~22–30% depende só do LPA de 2029E (R$ 2,08) e de uma saída sem re-rating. Isso a torna uma aposta de execução do crescimento (~15% a.a.), não de valor intrínseco. Com Ke de 25%, o DCF é negativo mesmo com ROIC terminal de 25%: a 18,4% de WACC, a perpetuidade sai a 2,0x EBITDA. A TIR de dono pelo DDM fica em 12,5–14%.

## Não verificado / limitações
- Composição exata do "LL recorrente" da companhia: inferi o efeito IFRS-16 pelo tamanho e pela persistência da diferença.
- Efeito do câmbio de hoje sobre a receita das operações fora do Brasil, ~50% das unidades. +5% de receita em 2026 aumentaria o justo em ~R$ 0,6, mas a dívida externa também sobe em R$; não modelado.
- Covenants. Evolve (60%) e Buddha Spa (pós-balanço, pequenas).
- O motor dá peso de 50% a um DCF que vale zero (piso). Essa regra é do motor, não da premissa, mas domina o valor justo desta empresa.
