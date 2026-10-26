# Revisão independente — BRSR6 (Banrisul PNB) · 26/10/2026

**Veredito: ok.** Não há erro objetivo. ROE, payout, PL-base e múltiplos são coerentes com 10 anos de CVM. A conclusão (armadilha de valor para Ke de 25%) é robusta. Não alterei nada.

Preço de referência (foto B3, 13h02): PNB R$ 14,67 (−19,2%; sexta R$ 18,16).

| | Valor |
|---|---|
| Valor justo | R$ 11,49 (DDM 9,26 · P/L 14,04 · P/VP 13,38) |
| TIR implícita | 17,9% |
| TIR 3 anos | 18,9% |
| P/VP justo (Gordon, ROE_T 11,5%) | 0,33x vs 0,51x hoje (PL 2T26 R$ 11.844 mi) |
| P/L 2027E ao preço | 4,7x |

## Checagens (ok)
- **Lucro 2026E de R$ 1.158 mi** (ROE de 10,1% × PL FY25 de 11.462). O CVM do 1S26 é de R$ 557,8 mi, então a premissa implica 2S26 de R$ 600 mi.
  - O ritmo subjacente é de ~R$ 265–280 mi/tri: o 2T26 teve reversão de provisões de R$ 101,5 mi e o 1T26, despesa de R$ 98,9 mi.
  - O 4T é sistematicamente o trimestre mais forte (EBT do 4T: 373 / 489 / 268 / 674 em 2022–25). Logo, 2S26 de ~600 é plausível.
  - Com 2S26 de 520, o valor seria 11,42. Imaterial.
- **PL projetado × reportado.** O modelo implica PL de meio de ano de 11.796 vs 11.844 na CVM do 2T26. Bate (o problema de BBAS3 não ocorre aqui).
- **Trajetória de ROE.** Médio de 9,8% → 11,6% (2030), com terminal de 11,5%. Comparações:
  - CVM 2015–25: 13,6 / 11,0 / 15,5 / 12,3 / 16,7 / 7,7 / 12,5 / 9,0 / 10,4 / 7,2 / 15,7% (média de 12,0%);
  - CVM 2021–24: média de 9,8%;
  - 2025: inflado pelo 4T25 (R$ 718 mi).

  Neutro: entre a média recente e a de 10 anos.
- **Payout de 40%.** Histórico de caixa de 34–56% (média de ~40%). Coerente; o controlador (RS em Regime de Recuperação Fiscal) depende de proventos.
- **Ações.** 408,97 mi (205,06 ON + 203,91 PN), total da B3 = CVM, sem tesouraria. ok.
- **Múltiplos.** P/L 4,5x e P/VP 0,45x, entre o p10 (3,7x / 0,43x) e a mediana de 5 anos (5,2x / 0,49x). Coerentes entre si: 0,45 / ROE de ~10% ≈ 4,5x.

## Achados
1. **(baixa) TIR 3 anos sensível ao múltiplo de saída.** Fica em 9,6% no p10 de 5 anos e em 26,4% na mediana. Com ROE parado em 10%, cai a 11,1%. O caso de 3 anos depende de re-rating e de o ROE subir para 12%.
2. **(baixa — motor/dados) Market cap.** `listed_classes` inclui BRSR3, mas a foto (`quotes.json`) não tem BRSR3. O motor caiu no fallback (PNB × todas as ações = R$ 6,0 bi) e a nota descreve outro cálculo (ON a preço da ON = ~R$ 6,7 bi). Não afeta o valuation, que no template financeiro não usa o market cap.
3. **(baixa — texto) Narrativa.** Cita PNB R$ 14,29, −21%, TIR implícita de 18,0% e TIR 3 anos de 19,6%. Na foto final: R$ 14,67, −19,2%, 17,9% e 18,9%. Diferenças pequenas.
4. **(informativo) Opcionalidade de privatização.** Corretamente fora do caso-base. O resultado da eleição para governador do RS (25/10) segue não verificado, mas mexe só no bull, não no base.

## Sensibilidade (em memória)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | 11,49 | 17,9% | 18,9% |
| LL 2026E de R$ 1.080 mi (ritmo subjacente) | 11,42 | 17,8% | 18,5% |
| ROE_T 10% / 13% | 11,20 / 11,71 | 16,9% / 18,6% | 18,9% |
| ROE plano em 10% (inclusive terminal) | 10,43 | 15,1% | 11,1% |
| ROE 12,5% (nível de 2021, inclusive terminal) | 12,09 | 19,1% | 24,2% |
| Payout 50% / 30% | 11,83 / 11,13 | 18,5% / 17,4% | 20,1% / 17,7% |
| Múltiplos na mediana de 5 anos (5,2x / 0,49x) | 12,33 | 17,9% | 26,4% |
| Múltiplos no p10 de 5 anos (3,7x / 0,43x) | 10,71 | 17,9% | 9,6% |

A TIR implícita fica entre 15% e 19% em todos os testes, abaixo de 25%. **A conclusão é robusta.**

## Não verificado
- Release oficial do 2T26.
- Basileia/CET1.
- Política estatutária de dividendos e direitos da PNB (prioridade, tag-along ou +10% — o motor trata ON e PN como iguais).
- Natureza do 4T25 (R$ 718 mi).
- Resultado da eleição estadual do RS.
- Liquidez: ADTV de ~R$ 31 mi.
