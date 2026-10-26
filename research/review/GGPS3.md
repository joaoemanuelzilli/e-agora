# Revisão independente — GGPS3 (Grupo GPS) · 26/10/2026

**Veredito: ok** (sem erro objetivo; premissas dentro do histórico pós-GRSA). Nenhuma alteração em `research/GGPS3.json`.

Preço de referência (foto B3 13h02): R$ 12,03. Motor: valor justo **R$ 7,47**, TIR implícita **14,5%**, TIR 3 anos **30,4%** (inalterados).

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | +7,5% / 10% / 9% / 7,5% / 7% (só orgânico) | 1S26 +8,1% a/a (9.082 vs 8.402); guidance orgânico 8–9% | ok; 2027–28 incluem o repasse da jornada de 40h |
| Margem EBITDA (CVM) | 10,5% → 10,0% (2027–28) → 10,5% | 2024 11,3%; 2025 10,7%; LTM ex-Sistema S 10,5% (1.880/17.962); 1S26 ex-evento 9,7% (2S é sazonalmente mais forte: 2S25 11,25%) | ok; 2026 = 1S26 real + 2S26 ≈ 2S25 |
| D&A | 2,2% → 1,8% | 2024 2,7%; 2025 2,4%; LTM 2,2% (R$ 399 mi, estável em R$) | Leve otimismo: a diluição soma ~0,4 p.p. à margem EBIT até 2030 |
| Capex | 1,6% | 2024–25 1,5%; LTM 1,5% | ok |
| Capital de giro | 12% da receita incremental | Capital de giro operacional 30/06/26 ≈ R$ 2,0 bi = 11,3% da receita LTM | ok |
| IR | 29% | 2020–25 28,3–33,2%; LTM 29,8% | ok |
| Resultado financeiro | 16,5–17,5% × DL (15% em 2030) − R$ 90 → 60 mi | 2025 −R$ 465 mi (~19,8% da DL média); 2T26 subjacente ≈ −R$ 141 mi (−40 reportado menos ~R$ 100 mi de reversão de atualização do Sistema S) | ver achado 1 |
| Payout | 40% → 60% | 2023–25 ~33% | Coerente sem M&A (DL/EBITDA cai a 0,1x) |
| ROIC_T / ROE_T | 20% / 22% | projetados 2030: 22,2% / 22,1% | ok |
| Ações | 752,35 mi | CVM 30/06/26 = B3 (bonificação de 10,74% de dez/25 já refletida) | ok |
| DL-base | R$ 2.142 mi (CVM, com arrend. 111) | dívida 6.123 − caixa 4.092 + arrend.; empresa R$ 2.349 mi inclui aquisições a pagar e parcelamentos, que estão em `other_debt_like` | ok, sem dupla contagem |
| Debt-like | R$ 800 mi (300 de itens da DL da empresa + 500 de haircut de contingências) | provisões 2.092 − depósitos 505 − ativo indenizatório 462 = 1.125 líquidos | Julgamento razoável (provisões trabalhistas giram pelo EBITDA) |

## Achados
1. (média) **Custo financeiro provavelmente subestimado em 2028–30.** O motor cobra juros só sobre a DL, mas a GPS carrega dívida bruta de R$ 6,1 bi (CDI+) e caixa de R$ 4,1 bi: o spread sobre a bruta (~1,3% × 6,0 bi ≈ R$ 78 mi) e o PIS/COFINS sobre a receita financeira (~R$ 28 mi) custam ~R$ 100 mi/ano mesmo com DL baixa. Além disso, o custo cai para 15% em 2030, enquanto a curva DI de hoje (F29 15,36%, F31 15,66%) implica CDI a termo ~15,5–16% em 2028–30. Teste com 18% sobre a DL e −R$ 110 mi/ano: valor justo R$ 7,39 (−1%), TIR implícita 14,2%, TIR 3a 28,1%. Não alterado: imaterial para o valor justo e depende de a empresa manter ou não caixa para M&A.
2. (baixa) A diluição do D&A (2,2% → 1,8%) eleva o lucro de 2029–30. Com D&A fixo em 2,2%: valor justo R$ 7,32, TIR 3a 28,2%. Não alterado (amortização de carteira de clientes de aquisições antigas cai de fato).
3. (informativo) Os indicadores de vitrine LTM estão contaminados pelo Sistema S (+R$ 247 mi no EBITDA, +R$ 230 mi no lucro): EV/EBITDA LTM 5,3x e P/L LTM 9,9x, contra ~6,0x e ~13x ex-evento. Não afetam o valor justo (o motor projeta a partir de 30/06/26).
4. (informativo) A TIR de 3 anos (~30%) depende de LPA 2029E de R$ 1,63 (lucro +59% sobre 2026E, por desalavancagem e margem) e da saída a 12x P/L. É a métrica mais frágil da tese.

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
- Base: R$ 7,47 / 14,5% / 30,4%
- Custo da dívida na curva + carrego: R$ 7,39 / 14,2% / 28,1%
- Margem 9,7% em 2027–28 e 10% depois (run-rate do 1S26): R$ 7,01 / 14,0% / 27,6%
- D&A fixo em 2,2%: R$ 7,32 / 14,2% / 28,2%
- Contingências líquidas inteiras (R$ 1.125 mi) como dívida: R$ 6,95 / 14,5% / 30,4%
- Sem haircut de contingências: R$ 7,88 / 14,5% / 30,4%
- ROIC/ROE terminais 16%/18%: R$ 7,21 / 14,0% / 30,4%
- Custo da dívida na curva + D&A 2,2%: R$ 7,25 / 13,9% / 25,8%

A conclusão (TIR implícita ~14%, abaixo de Ke 25%; só "tática" via reprecificação a 12x P/L) se mantém em todos os testes. A TIR de 3 anos cai para ~26% com premissas um pouco mais duras, ainda acima de 25%, mas com pouca folga.

## O que não deu para verificar
- Texto final e data de promulgação da PEC da jornada (42h/40h) e o repasse efetivo nos contratos.
- Composição das provisões (trabalhista × tributária) e o índice de atualização (Selic × IPCA-E), que definem o carrego financeiro real das contingências.
- Aquisições pendentes no CADE (SEI, Uniflex, Aster): não modeladas, nem o caixa reservado para elas.
