# Revisão independente — BPAC11 (BTG Pactual, unit) · 26/10/2026

**Veredito: ok.** Não há erro objetivo. Unit, ações, PL-base, ROE e payout batem com a CVM e com o dossiê. A conclusão (franquia de qualidade, mas cara para Ke de 25%) é robusta. Não alterei nada.

Preço de referência (foto B3, 13h02): R$ 55,32/unit (−30,7%; sexta R$ 79,82).

| | Valor |
|---|---|
| Valor justo | R$ 33,44/unit (DDM 18,90 · P/L 50,31 · P/VP 45,63) |
| TIR implícita | 13,3% |
| TIR 3 anos | 12,4% |
| P/VP justo (Gordon, ROE_T 21%) | 0,80x vs 2,57x hoje (PL CVM 2T26) |
| P/L 2027E ao preço | 9,9x |

## Checagens (ok)
- **Unit e ações.** `shares_per_unit` = 3 (1 ON + 2 PNA). São 11.587,65 mi de ações ex-tesouraria = 3.862,6 mi de units equivalentes. O total da B3 é igual ao da CVM (sem cancelamento posterior) e o market cap de R$ 213,7 bi está correto. O aumento de +164 mi ações em dez/25 (incorporação do Pan) já está no PL de FY2025.
- **Lucro e ROE de 2026.** O ROE de abertura de 27,6% × PL FY25 de R$ 73.353 mi dá R$ 20.245 mi (ajustado). Isso implica 2S26 de R$ 10,3 bi, +3,5% s/s sobre o 1S26 ajustado (R$ 9,95 bi), ou seja, o 2T26 repetido. O ROE médio de 25,1% bate com o 1S26 anualizado (CVM 24,8% / ajustado 25,4% sobre o PL médio da CVM).
- **Ajustado × contábil.** A CVM do 1S26 mostra R$ 9.690 mi contra R$ 9.950 mi ajustados (gap de 2,7%, amortização de ágio). Recalibrar sobre a base CVM muda o valor justo em −0,4% (33,44 → 33,29). Imaterial.
- **PL projetado × reportado.** O modelo implica PL de meio de ano ≈ 73.353 + 9.950 × 0,73 = 80.617. A CVM do 2T26 mostra 83.133 antes do dividendo semestral do 1S (~R$ 2,7 bi, declarado em ago); depois dele, ~80,4 bi. Bate (diferença de −0,2%). O PL 2026E de 88,1 bi é coerente.
- **Trajetória de ROE.** Médio de 25,1% → 21,3% em 2030, com terminal de 21%. Comparações:
  - CVM 2021–25: 19,9 / 16,8 / 20,6 / 19,2 / 24,1% (média de 20,1%);
  - LTM: 23,6%;
  - ROAE gerencial: 26,7%.

  A queda de ROE com o PL crescendo ~18% a.a. (retenção de 73%) é internamente coerente: capital excedente rende ~CDI. Neutra.
- **Payout de 27–30%.** Histórico de 25–29%. Basileia 16,0% e CET1 11,6%: sem restrição.
- **Múltiplos.**
  - P/L 9x × LPA 2027E = R$ 50,31/unit. P/VP 2,0x × VPA 2026E = R$ 45,63/unit.
  - São coerentes entre si: 9x × ROE de ~22,5% ≈ 2,0x.
  - Ficam no piso da faixa histórica. Histórico de 5 anos: P/L LTM com mediana 13,7x e p10 11,3x; P/VP com mediana 2,46x e p10 2,05x; fundo de dez/24 em 9,4x LTM.
  - 9x forward ≈ 10,3–10,8x LTM, entre o fundo de 2024 e o p10. Conservador, mas dentro do observado e justificado pelo regime de juros.

## Achados
1. **(média — julgamento) Peso dos múltiplos de mercado.** O DDM a Ke de 25% (R$ 18,90) fica muito longe dos múltiplos de mercado (R$ 47,97, que embutem Ke de ~14%). O blend 50/50 é o método do estudo, mas a "verdade" para a meta do usuário é o DDM/TIR implícita (13,3% vs 25%). Mesmo com múltiplos na mediana de 5 anos, o valor justo fica em R$ 42,63 (< preço).
2. **(média) A TIR 3 anos é a métrica mais frágil.** Ela vai de 12,4% a 35,6% conforme o P/L de saída (9x → 13,7x) e cai para 5,9% se o ROE ficar 2 p.p. abaixo. Deve ser lida como faixa, não como ponto.
3. **(baixa — motor) Início do stub de 2026.** Começa em 30/06, não em 26/10 (sistêmico, efeito pequeno).
4. **(baixa — texto) Narrativa desatualizada.**
   - A nota e `election_impact` citam R$ 51,40, −36%, "~2,4x PL e ~9x lucro 2027E" e "TIR 13,6% / 15,1%".
   - Na foto final (R$ 55,32), os números são: −30,7%, 2,57x PL CVM, 9,9x lucro 2027E, TIR implícita 13,3% e TIR 3 anos 12,4%.
   - Não editei (não é premissa).

## Sensibilidade (em memória)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | 33,44 | 13,3% | 12,4% |
| ROE_T 18% / 24% | 33,09 / 33,69 | 12,9% / 13,5% | 12,4% |
| ROE −2 p.p. em todo o horizonte (ROE_T 19%) | 30,77 | 12,2% | 5,9% |
| Lucro na base CVM (−2,7% no 1S26) | 33,29 | 13,2% | 12,1% |
| Múltiplos no p10 de 5 anos (11,3x / 2,05x) | 36,93 | 13,3% | 24,4% |
| Múltiplos na mediana de 5 anos (13,7x / 2,46x) | 42,63 | 13,3% | 35,6% |
| Payout de 50% a partir de 2027 | 34,14 | 12,9% | 9,9% |
| g 6,5% | 33,39 | 13,9% | 12,4% |

A TIR implícita fica entre 12% e 14% em todos os testes, muito abaixo de 25%. **A conclusão "não é oportunidade pelo critério do usuário" é robusta.**

## Não verificado
- Resultado do 3T26 (sai em 10/11) e efeito da volatilidade de out/26 em S&T.
- Consenso pós-eleição.
- Sensibilidade oficial a juros.
- Valor por unit dos dividendos semestrais.
- Composição dos minoritários (R$ 6,8 bi de PL; LL LTM de R$ 793 mi — o motor usa só o controlador, corretamente).
