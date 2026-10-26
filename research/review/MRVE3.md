# Revisão independente — MRVE3 (MRV&CO) · 26/10/2026

**Veredito: ajustada.** Corrigi uma premissa incoerente com a curva de juros de hoje: o custo da dívida líquida caía de 15,5% para 13% até 2030, o que reduzia em até R$ 170 mi/ano os juros sobre ~R$ 6,7 bi de DL. Com o custo mantido em 15,5%, o valor justo vai de R$ 4,06 para R$ 3,96 e a TIR de dono de 13,8% para 11,8%. A conclusão de "armadilha" se fortalece. Nenhum teste plausível leva o valor justo ao preço de R$ 4,98; o máximo foi R$ 4,66. Os itens não verificados (Resia, passivo a descoberto, cessões) são quase todos de viés para baixo.

| | Valor justo | TIR implícita | TIR 3 anos | P(valor > preço) |
|---|---|---|---|---|
| Analista (preço R$ 4,98, foto 13h02) | R$ 4,06 | 13,8% | 5,8% | 34% |
| Após revisão | **R$ 3,96** | **11,8%** | **−5,4%** | 32% |

## O que conferi e está coerente

**Ações.** São 562,83 mi. A CVM traz o número em milhares; a B3 informa 562.835.771.

**DL-base de R$ 5.900 mi (definição da companhia).**
- A DL CVM é de 7.645: dívida bruta de 8.646 menos o caixa CVM de 1.002.
- A definição da companhia soma os derivativos passivos (103,1 + 16,7) e subtrai caixa e TVM de ~2.866. Isso implica TVM de ~1,86 bi dentro de "Outros ativos circulantes" (3.185), coerente com a nota.
- O override é razoável e mais conservador que a DL CVM sem derivativos.

**Resia em ativos não operacionais (R$ 1.802 mi).** São as propriedades para investimento (1.352,9) mais os ativos à venda (1.628,5) menos os passivos associados (1.178,9).
- Esses passivos estão na linha 2.01.07, fora das linhas de empréstimos, então não há dupla contagem com a DL.
- A dívida em moeda estrangeira (929,8 + 914,0) está na DL.

**Juros capitalizados (+3,2 p.p.).** A medida bate com o release do 1T26: margem bruta de 29,4% contra 32,5% no 1T26 e de 29,5% contra 32,9% no 4T25. O ajuste é neutro no LL.

**WACC.**
- O Kd de 0,242 equivale a 16% sem escudo fiscal (RET).
- O peso de dívida de 45% fica abaixo do de mercado (56% pré-eleição; 68% hoje). Isso é conservador: com 60%, o valor seria R$ 4,48.

**IR.** Na FCFF, 17% do EBIT dá ~303, contra RET de ~2% da ROL (242), um viés levemente conservador. No LL, o excesso do RET está em `other_financial`, o que é coerente.

**Operação.**
- Receita de 2026 com +11% (1S26: +15,7%; vendas recorde no 3T26).
- Margem CVM recorrente de 13,5% para 14,5% (2025 recorrente: 13,7%; 1S26: 13,8%).
- Capital de giro de 0,65, entre o bruto (~0,8) e o líquido de cessões.
- Payout zero até 2027, por causa dos prejuízos acumulados de R$ 1.145 mi.

## Achados

| # | Sev. | Achado | Evidência | Efeito (valor justo / TIR) |
|---|---|---|---|---|
| 1 | **média · corrigido** | Kd da projeção caía de 15,5% para 13,0% em 2030 | A curva DI de hoje é plana em ~15,5% (DI1F29 15,36%, DI1F31 15,66%), então a queda supunha cortes de Selic que o mercado não precifica. Com DL de R$ 6,3–7,0 bi, isso subestimava os juros em ~R$ 70/135/170 mi antes de IR em 2028/29/30. A redução de custo pela saída da Resia já está em `other_financial` | LL de 2028–30 de 397/511/612 para 345/400/463. Valor justo −R$ 0,10, TIR −2,0 p.p., TIR 3a de 5,8% para −5,4%. Com Kd = CDI a termo + spread (16–16,5%): R$ 3,88 / 10,8% |
| 2 | alta (método, mantido) | Cessões de R$ 4.706 mi (810 CP + 3.896 LP) fora da DL | O par casado com o pró-soluto exige rolagem perpétua. O saldo cresceu de 2.035 (2023) para 4.706, com custo ~CDI+. A nota do analista é transparente | Como dívida: o DCF fica negativo e o valor justo vai a R$ 0,45 |
| 3 | média (não verificado) | Resia mais negativa no PL que no modelo | Implicitamente, o modelo avalia a Resia em 1.353 + 450 − 1.844 (dívida em US$) = −R$ 41 mi. O PL da Resia era de −US$ 113 mi (≈ −R$ 620 mi; JPMorgan). Há ~R$ 580 mi de passivos da Resia ou de perímetro não explicados | Resia a PL contábil: R$ 3,32 |
| 4 | média (não verificado) | "Passivo a descoberto – participações em investidas" de R$ 665 mi (CP) fora da DL | É a obrigação de cobrir o PL negativo de investidas. Cresce todo ano (483 → 570 → 603 → 665) | Como dívida: R$ 3,22 |
| 5 | média (risco) | Margem | — | Margem CVM em 13,5% plana: R$ 3,29 / 9,6%. Até 15,5%: R$ 4,63 / 13,8% |
| 6 | baixa | Minoritários de 5% do LL subestimam a fatia dos sócios de SPEs quando o LL consolidado é deprimido pela holding | Os sócios ganharam R$ 58/71/98 mi (2019–21) e 53/11/21/0 (2022–25). O modelo dá R$ 1–34 mi em 2026–30. A dedução no DCF a valor contábil (623,5) é razoável | 10% do LL: R$ 3,93 / 11,5% |
| 7 | média (não quantificado) | Equity swap sobre MRVE3 | A ação foi de R$ 8,23 para R$ 4,98 hoje, o que gera perda de MTM. O notional não foi localizado | — |
| 8 | info | DCF de R$ 4,93 contra DDM de R$ 1,36 | O WACC de 20,9% (45% de dívida a 16%) contra Ke de 25% sobre um fluxo ao acionista quase nulo até 2028. O valor justo combinado é puxado pelo DCF | — |

**Teto dos testes plausíveis:** R$ 4,66 (capital de giro líquido de 0,40) e R$ 4,63 (margem de 15,5%). Ambos ficam abaixo do preço, com TIR de 13–14%.

## Mudanças em `research/MRVE3.json` (original em `research/review/MRVE3.orig.json`)
- **`projection.cost_of_net_debt`:** [0,155, 0,155, 0,145, 0,135, 0,13] → [0,155, 0,155, 0,155, 0,155, 0,155], com nota em `wacc.notes`.
- **Efeito:** valor justo de R$ 4,06 para R$ 3,96; TIR implícita de 13,8% para 11,8%; TIR em 3 anos de 5,8% para −5,4%; P(valor > preço) de 34% para 32%.
- O motor foi re-rodado (`EAGORA_SNAPSHOT=1`).

## O que não deu para verificar
- Composição dos ~R$ 1,9 bi de TVM em "outros ativos" e dos passivos associados aos ativos à venda (1.179).
- Natureza do passivo a descoberto.
- Perímetro do PL da Resia e direitos do novo acionista da Resia (perda de R$ 1.046 mi em 2025).
- Notional do equity swap.
- Dívida por indexador e cronograma: as tabelas do release estão em imagem.
- Covenants pós-choque.
