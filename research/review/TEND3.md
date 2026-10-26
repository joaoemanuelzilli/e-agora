# Revisão independente — TEND3 (Tenda) · 26/10/2026

**Veredito: ok.** Não encontrei erro objetivo que justifique alterar as premissas. Há vieses nos dois sentidos, de tamanho parecido, e eles se compensam:
- **margem otimista:** 18,5% CVM sustentados por três anos, o maior nível da história da empresa;
- **perpetuidade e payout conservadores:** ROIC terminal abaixo do WACC e caixa acumulando até R$ 0,8 bi.

A TIR de dono de 24,5% fica no limite do Ke. O valor justo (R$ 29,6) tem folga sobre o preço (R$ 22,38) em quase todos os testes. Só a quebra de margem derruba a tese, e é ela que o investidor deve monitorar.

| | Valor justo | TIR implícita | TIR 3 anos | P(valor > preço) |
|---|---|---|---|---|
| Analista (preço R$ 22,38, foto 13h02) | R$ 29,65 | 24,5% | 42,9% | 86% |
| Após revisão (sem alteração) | R$ 29,65 | 24,5% | 42,9% | 86% |

## O que conferi e está coerente

**Ações.** São 122,51 mi. O override está certo: a CVM traz o total em milhares e a tesouraria em unidades. A base B3 padronizada (122,51 mi) e o dividendo (R$ 78 mi ÷ R$ 0,6363) confirmam o número.

**DL-base de R$ 339 mi.** É a dívida bruta de 1.168,7 (debêntures de 895) mais arrendamentos de 35,9, menos caixa e aplicações de 865,4.

**`other_debt_like` de 78.** É o dividendo do 1S26, aprovado em 07/08 e com pagamento em 30/12/26, posterior ao balanço. Os R$ 100 mi do 3T25 foram pagos em 07/01/2026, antes da data-base. Os dividendos a pagar em 30/06 eram de R$ 0,2 mi.

**Juros capitalizados (+1,6 p.p.).**
- A medida bate com o 2T26: margem bruta de 35,7% na CVM contra 37,3% ajustada.
- É neutro no LL. O resultado financeiro de 2026E na base CVM (−181) bate com o 2T26 sem swap anualizado (≈ −180).

**WACC.** O Kd de 0,235 equivale a 15,5% sem escudo fiscal (RET); o peso de dívida é de 15%.

**Guidance 2026 (04/08).**
- O LL de 2026E do modelo (R$ 618 mi) está dentro do guidance de R$ 600–660 mi.
- O EBITDA consolidado de 1.023 (base ex-juros, com a Alea) equivale a ~1,08–1,10 bi no segmento Tenda. Fica no piso do guidance de R$ 1,1–1,2 bi.

**Crescimento.** Os +22% de 2026 implicam um 2S26 com +13% a/a, depois de um 1S26 com +33%. Em 2027–30, a projeção é de 10% a 6% a.a.

**IR.** A alíquota de 9–10% sobre o LAIR dá 1,2–1,5% da ROL; o 1S26 ficou em 1,35% (RET de 1% nas Faixas 1–2).

**Minoritários de 0%.** É conservador: na Alea, os minoritários absorvem prejuízo (−R$ 24 mi no LTM).

**Capital de giro de 0,35.** É conservador. O CG operacional que calculei foi de 0,45x (2023–25) e 0,40x (2T26). O marginal foi de 0,29–0,33x bruto e 0,18–0,28x líquido de cessões.

## Achados

| # | Sev. | Achado | Evidência | Efeito (valor justo / TIR) |
|---|---|---|---|---|
| 1 | **alta (risco, não erro)** | Margem no topo histórico por três anos | A margem CVM projetada é de 18,5% em 2026–28. O 1S26 ficou em 18,5%, o LTM em 16,4% e 2025 em 14,1%. O melhor nível antes da crise foi 16,5% (2019); em 2022, −10,8%. Distratos +55% t/t no 3T26, INCC de mão de obra em 7,6% e câmbio +9,5% | Margem de 16,5/15,5%: R$ 25,51 / 21,5%. Volta ao nível de 2025 até 2030: R$ 25,65 / 21,0% |
| 2 | média (conservador) | Payout de 50–60% em 2028–30, contra FCFE/LL do próprio modelo de 83–88% | A DL zera em 2027 e o caixa líquido chega a R$ 795 mi (0,6x o EBITDA) em 2030. O DDM avalia esse caixa só pelo rendimento (~13%) a Ke de 25%, o que deprime a TIR. Mantido: é política, e a empresa saiu de crise há pouco | Payout de 60–75% em 2028+: R$ 29,92 / 25,4%. De 70–80%: R$ 30,09 / 26,0% |
| 3 | baixa (conservador) | ROIC terminal de 20%, abaixo do WACC de 23,6%; ROE terminal = Ke | No período explícito, o ROIC é de 43–48%; a intensidade de capital implica ~59%. O histórico ex-crise é de 12–25%. É defensável dado o histórico | ROE_T 30% e ROIC_T 25%: R$ 30,21 / 24,8% |
| 4 | média (incerto) | Equity swap sobre TEND3 não modelado | Pelo ganho do 2T26 (R$ 17,8 mi com a ação +17%), a exposição comprada é de ~3,3–5 mi de ações. De 30/06 (R$ 36,55) até hoje (R$ 22,38), a perda de MTM é de ~R$ 47–72 mi. Mas o MTM em 30/06 (provável ativo, depois de +49% no 1S26) também está fora da DL, então o efeito líquido tem sinal incerto. Não ajustei | Se −R$ 50 mi líquidos: −R$ 0,26 |
| 5 | média (método, mantido) | Cessões de R$ 515 mi (105 CP + 409 LP, estes em "passivos sobre ativos à venda") fora da DL | Par casado com o pró-soluto cedido. O saldo caiu de 603 para 515 no 1S26 (a cessão não está sendo rolada), e o run-off funciona como amortização de dívida. Por outro lado, o capital de giro de 0,35 é bruto, conservador no fluxo | Como dívida: R$ 27,02 / 24,5% |
| 6 | baixa (conservador) | Kd cai de 15% para 13%, contra DI1F29–F31 de 15,4–15,7% | A empresa passa a ter caixa líquido em 2028 | Kd plano em 15% → R$ 29,69 / 24,6% |
| 7 | info | Capex (1,2%) abaixo do D&A (1,6%) | Efeito de ~R$ 20 mi/ano. O capex de 2025 (2,9%) inclui a fábrica da Alea | Irrelevante |

**Leitura:** a combinação "neutra" (Kd plano + payout de 60–75% em 2028+) dá ~R$ 29,9 e TIR de ~25,5%. A combinação com margem mais baixa (16,5/15,5%) dá ~R$ 25,5 e TIR de ~21,5%, ainda acima do preço. O valor justo só cai abaixo de R$ 22,4 com margem CVM de volta a 14,5–15,5% já em 2027 e crescimento de 5% a.a. (R$ 22,24, com TIR de 18,8%). O cenário bear do analista vale R$ 20,5.

## Mudanças
Nenhuma. `research/TEND3.json` não foi alterado e o motor não foi re-rodado.

## O que não deu para verificar
- Notional, preço de entrada e liquidação do equity swap.
- Detalhe do resultado da Alea no 2T26.
- Política de rolagem das cessões e se os fundos de reserva das cessões (−R$ 41 mi na DFC do 1S26) estão dentro do caixa de R$ 865 mi.
- Covenants e cronograma da dívida.
- Resultado do 3T26 (só a prévia operacional).
