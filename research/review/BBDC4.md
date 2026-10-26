# Revisão independente — BBDC4 (Bradesco PN) · 26/10/2026

**Veredito: ok.** Não há erro objetivo nas premissas. O PL pró-forma do aumento de capital, a contagem de ações e o ROE batem com a CVM do 3T26. Há uma limitação do motor (o +10% de dividendo da PN), que quantifico abaixo e não forcei via override. Não alterei nada.

Preço de referência (foto B3, 13h02): PN R$ 15,47 (−24,1%) · ON R$ 14,29 (−20,9%).

| | Valor |
|---|---|
| Valor justo (por ação média ON/PN) | R$ 13,31 (DDM 9,95 · P/L 17,35 · P/VP 16,01) |
| TIR implícita | 17,9% |
| TIR 3 anos | 26,2% |
| P/VP justo (Gordon, ROE_T 16%) | 0,55x; P/VP de mercado ≈ 0,85x (market cap ON+PN R$ 166,3 bi / PL 3T26 R$ 195,0 bi) |
| P/L 2027E ao preço | 5,8x |

## Checagens (ok)
- **Data-base.** 3T26 (30/09/2026), já arquivado na CVM. O stub de 2026 é de 0,252 ano.
- **PL pró-forma.** R$ 188.135 mi = CVM FY25 de 178.415 + 9.720 integralizados (capital social de 93.770 → 103.490 na CVM de 30/09).
  - O PL 2026E do modelo (198,8 bi) bate com o PL do 3T26 (195,0 bi) + 4T retido (~3–4 bi).
  - Sem o pró-forma, com as mesmas ações, o valor cairia para 12,67, o que confirma que o override é necessário e está correto.
- **Ações.** O total da B3 (11.196,9 mi) = CVM 10.592,0 + o máximo da emissão (302,9 mi ON + 302,0 mi PN). Em circulação: 11.174,3 mi.
  - Se só 97,2% tiverem sido emitidos (R$ 9,72 de R$ 10 bi), o valor iria a 13,33. Imaterial.
  - Não há o problema de cancelamento duplo visto em outros tickers: a tesouraria é de 0,2%.
- **Lucro.** ROE 2026 de 14,95% × 188.135 = R$ 28,1 bi (recorrente: 6.811 + 7.050 + 7.109 + 4TE 7.150).
  - O CVM 9M26 é de R$ 19.648 mi (vs 20.970 recorrente; o gap está todo no 1T26).
  - Recalibrando para a base CVM (R$ 26,8 bi), o valor iria a 13,27. Imaterial.
- **ROE.** Abertura de 15 → 16,5% (médio de 14,6 → 16,0%) e terminal de 16%. Comparações:
  - ROAE recorrente: 14,8% (2025), 16,2% (2T26), 15,6% (3T26; 16,1% ex-aumento de capital);
  - CVM 2021–25: média de 12,5%;
  - pico de 2015–19: 18–20%.

  É levemente otimista para um ciclo de crédito em piora (PDD +24% a/a, NPL 90 de 4,6%), mas 2027 fica plano (14,6%) e a subida é gradual. Aceitável.
- **Payout de 60–62%.** Histórico bruto de 52–79% (2025: 62%). O CET1 pró-forma de 13,6% sustenta o payout. ROE de 16% × retenção de 40% = 6,4% de crescimento do PL, compatível com carteira de +6–8%.
- **Múltiplos.** P/L 6,5x e P/VP 0,90x = ~10% abaixo da série oficial do RAEF (P/L recorrente de 6,7–7,4x; P/VP de 1,0–1,1x). Coerentes entre si (0,9 / ROE 14,6% ≈ 6,2x).

## Achados
1. **(média — limitação do motor; não alterei) A PN recebe dividendos 10% maiores que a ON.** Isso está no estatuto e no próprio `dividend_policy`.
   - O motor divide o valor do equity igualmente por ação, mas o preço usado é o da PN.
   - Em ações PN-equivalentes (PN + ON/1,1 = 10.665,7 mi; fator de 1,048):
     - valor justo da PN: R$ 13,95 (+4,8%);
     - TIR implícita: 18,5%;
     - TIR 3 anos: 29,3%;
     - valor justo da ON: ~R$ 12,68.
   - Não apliquei por override de ações porque distorceria o market cap e a contagem de ações exibidos (−4,5%). **Sugestão ao líder:** um fator de classe no motor, ou exibir o ajuste. A conclusão não muda: 18,5% < 25%.
2. **(média) A TIR 3 anos é sensível.** Vai de 22,7% (ROE parado em 15%) a 31,7% (saída nos múltiplos médios do RAEF). Ler como faixa.
3. **(baixa — dados do app, não premissa) Histórico de múltiplos quebrado.** `data/app/companies/BBDC4.json` → `market.multiples_history` traz market cap de centenas de R$ mi antes de 2024 (P/L de 0,01x, P/VP de 0,001x, DY de 20–70x). As estatísticas de 5 anos (mediana de P/L 0,01x) estão contaminadas.
   - Provável erro de escala ou de ações no módulo de mercado.
   - As premissas não usam essa série (usam o RAEF oficial), mas o app exibe dados errados. **Alerta ao líder.**
4. **(baixa — motor) Início do stub.** Começa em 30/09, então o efeito é pequeno aqui. Os JCP de R$ 6,5 bi antecipados para 15/09 já saíram antes da data-base, sem dupla contagem.
5. **(baixa — texto) Narrativa desatualizada.**
   - A nota cita PN R$ 14,67, "−28%" e "P/VP ~0,83–0,85x".
   - Na foto final, a PN está a R$ 15,47 (−24%) e o P/VP do motor é 0,886x (preço da PN sobre todas as ações; com ON+PN a preço de mercado, ~0,85x).
   - A TIR implícita (~18%) e a TIR 3 anos (26%) estão em linha.

## Sensibilidade (em memória)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | 13,31 | 17,9% | 26,2% |
| PN-equivalente (+10% de dividendo) | 13,95 | 18,5% | 29,3% |
| ROE_T 14% / 18% | 13,15 / 13,44 | 17,3% / 18,3% | 26,2% |
| ROE plano em 15% (inclusive terminal) | 12,91 | 16,6% | 22,7% |
| Múltiplos na média do RAEF (7,2x / 1,0x) | 14,23 | 17,9% | 31,7% |
| Payout 50% / 70% | 13,08 / 13,54 | 17,6% / 18,1% | 26,0% / 26,4% |
| PL sem pró-forma (erro hipotético) | 12,67 | 17,3% | 23,1% |
| LL 2026E em base CVM (R$ 26,8 bi) | 13,27 | 17,8% | 26,0% |

A TIR implícita fica entre 16,6% e 18,5%: **não bate 25% na perpetuidade em nenhum teste.** O melhor caso continua sendo o horizonte de 3 anos, com re-rating.

## Não verificado
- Status do guidance no 3T26.
- PL gerencial do 3T26.
- Preço de subscrição e quantidade final de ações emitidas.
- Aprovação do efeito Bradsaúde no capital.
- Execução da nova recompra (3,55% ON / ~1% PN), que não está no payout e seria um pequeno upside.
