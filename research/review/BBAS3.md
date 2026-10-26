# Revisão independente — BBAS3 (Banco do Brasil) · 26/10/2026

**Veredito: ajustada.** Corrigi uma inconsistência objetiva com o PL já reportado (erro de período). Há um segundo risco relevante — a base do payout e a natureza do lucro "ajustado" — que sinalizo, mas não apliquei, porque não consegui confirmá-lo. Original em `research/review/BBAS3.orig.json`.

Preço de referência (foto B3, 13h02): R$ 17,57 (−28,9%; sexta R$ 24,72).

| | Antes | Depois |
|---|---|---|
| PL controlador FY2025 usado na projeção | 189.208 (CVM) | **180.969** (pró-forma) |
| ROE de abertura 2026 | 8,9% | **9,3%** (LL 2026E mantido em R$ 16,8 bi) |
| PL 2026E | R$ 201,0 bi | **R$ 192,8 bi** |
| LL 2027E / 2030E | R$ 22,1 / 35,4 bi | **R$ 21,2 / 34,0 bi** |
| ROE médio 2027–30 | 10,6 / 12,0 / 13,0 / 13,4% | 10,6 / 12,0 / 13,0 / 13,4% (inalterado) |
| Valor justo | R$ 16,69 | **R$ 16,02** (−4,0%) |
| DDM / P/L / P/VP | 13,14 / 19,36 / 21,12 | 12,62 / 18,57 / 20,26 |
| TIR implícita | 20,6% | **20,0%** |
| TIR 3 anos | 32,0% | **29,3%** |
| Monte Carlo p10–p90 · P(valor > preço) | 13,08–20,48 · 38,5% | 12,55–19,65 · 29,1% |
| Cenários bear / base / bull (esperado) | 13,45 / 16,69 / 19,58 (16,30) | 12,91 / 16,02 / 18,78 (15,64) |

## Achados
1. **(alta — erro objetivo de período) PL-base inconsistente com o 2T26 já arquivado.**
   - **O que o modelo fazia:** o template financeiro projeta o PL a partir do FY2025 (R$ 189.208 mi), somando o lucro **ajustado** retido. Isso levava o PL 2026E a R$ 201,0 bi.
   - **O que a CVM mostra:** o PL controlador **caiu** para R$ 186.079 mi no 2T26 (−R$ 3,1 bi no semestre), apesar de R$ 7,3 bi de lucro ajustado.
   - **De onde vem a diferença:** o LL CVM do 1S26 foi de R$ 4.795 mi (−R$ 2,5 bi vs o ajustado), e o ORA/outros somou ≈ −R$ 5,7 bi. O "vazamento" no semestre foi de R$ 8,2 bi.
   - **Por que importa:** o P/VP-alvo (0,60x) é aplicado sobre o VPA de 2026E, e o LL de 2027+ é ROE × PL. As duas coisas estavam infladas em ~4%.
   - **Correção:** `overrides.base.equity_controlling_2025` = PL 2T26 − lucro ajustado retido do 1S26 (7.300 × 0,7) = R$ 180.969 mi. O ROE 2026 foi recalibrado para manter o LL 2026E do analista. Mesma técnica do PL pró-forma de BBDC4.
   - **Resultado:** o PL 2026E (R$ 192,8 bi) = PL 2T26 + 2S26 retido, e os ROEs médios de 2027–30 ficam idênticos à intenção do analista. É a única mudança.
2. **(média — não verificado, risco de baixa) Base do payout.**
   - A política declarada é "30% do lucro líquido"; as fontes consultadas não dizem se é sobre o ajustado.
   - Indício: o JCP do 1T26 (R$ 400,4 mi antecipados em mar + R$ 465,7 mi em mai = R$ 866 mi) é 25% do ajustado (R$ 3,43 bi). Isso é compatível com 30% sobre o contábil (no 2T26, contábil/ajustado = 3.175/3.900 = 81%).
   - Legalmente, o dividendo sai do lucro contábil.
   - Se o payout incidir sobre o contábil: valor justo 15,76 e TIR implícita 19,6%.
   - Não apliquei: precisa do release "Análise do Desempenho".
3. **(média — julgamento) Lucro "ajustado" × contábil.**
   - CVM (IFRS)/ajustado: 84% (2023), 70% (2024), 66% (2025), 66% (1S26). O gap é crescente.
   - As provisões trabalhistas, fiscais e cíveis da CVM foram de R$ 18,7 bi (2023) para R$ 32,0 bi (2T26).
   - Parte dos "não recorrentes" recorre. Mesmo após a correção, de 2027 em diante o PL cresce pelo ajustado retido.
   - Se o gap de 2T26 (~19%) for estrutural (ROE, payout e P/L em base contábil): valor justo 14,12, TIR implícita 16,0% e TIR 3 anos 25,4%.
   - Não apliquei porque é julgamento, mas a assimetria é para baixo.
4. **(baixa) LL 2026E de R$ 16,8 bi.** Exige 2S26 de R$ 4,75 bi/tri (+22% vs o 2T26 de R$ 3,9 bi), embora fique abaixo do guidance de R$ 18–22 bi. No ritmo do 2T26 (R$ 15,1 bi), o valor justo seria 15,89 — efeito pequeno.
5. **(baixa — não quantificado) Choque de juros de hoje no ORA.** O BB tem R$ 711 bi em ativos a VJORA (2T26). A alta de ~300 bp no DI longo tende a gerar nova perda no ORA, o que reduz o PL e o CET1 (11,27%) e ameaça o payout. A duração da carteira não foi verificada (muito é LFT).
6. **(informativo) ROE terminal e múltiplos.**
   - ROE terminal de 14% vs CVM 2015–25 de 13,6% (IFRS) e ajustado de ~18% em 2021–25. O desconto por intervenção é coerente.
   - P/VP-alvo de 0,60x fica abaixo do p10 de 5 anos (0,66x; mediana 0,77x), justificado por ROE de 10–13%.
   - P/L de 5x sobre o LPA **ajustado** é ligeiramente acima do histórico em base ajustada. O P/L do app é sobre o LL CVM: 4,8x no fim de 2024 ≈ 3,3x ajustado; ~4,4x em 2023; média 2021–24 de ~4,6x. Ainda está dentro da faixa.
7. **(baixa — motor) Cenário bear.** Desloca o ROE em −3 p.p. também em 2026, quando 9 meses já estão praticamente dados. O bear de 2026 fica um pouco severo demais.
8. **(baixa — texto) Narrativa.** Atualizei no JSON os números que mudaram com a correção: `summary` (~4,7x P/L 2027E, TIR ~20%, TIR 3 anos ~29%), `thesis` (R$ 21,2 bi) e `history_check.notes`. O dossiê `notes/BBAS3.md` ainda cita R$ 17,01, valor justo de 16,69, TIR de 20,5% e TIR 3 anos de 31–32%; o líder deve atualizar.

## Sensibilidade (após a correção)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base corrigida | 16,02 | 20,0% | 29,3% |
| Manter o LL original com o PL corrigido (ROE maior) | 16,56 | 20,8% | 32,5% |
| Payout sobre o contábil (×0,814) | 15,76 | 19,6% | 28,7% |
| Base contábil completa (gap de 19% estrutural) | 14,12 | 16,0% | 25,4% |
| ROE_T 12% / 16% | 15,65 / 16,29 | 19,2% / 20,7% | 29,3% |
| Recuperação lenta (ROE 9,3 → 12%; ROE_T 12%) | 14,06 | 17,1% | 18,5% |
| Múltiplos na mediana de 5 anos (0,77x / 5,5x) | 17,92 | 20,0% | 34,7% |
| Múltiplos 0,50x / 4,5x | 14,71 | 20,0% | 23,6% |
| Payout de 40% desde 2027 | 16,17 | 20,2% | 30,1% |
| g 3,5% | 16,29 | 20,5% | 29,3% |

**Conclusão:** a TIR implícita fica entre 16% e 21% em todos os testes, sempre abaixo de 25%. A TIR 3 anos ≥ 25% depende de o ROE normalizar e de o múltiplo de saída voltar a ~5x ajustado. O caso continua sendo "perto do justo, aposta binária", agora com o valor justo um pouco abaixo do preço.

## Não verificado
- Base oficial do payout (ajustado × contábil) e payout de 2026–27.
- Composição dos ajustes de 2T26 (R$ 725 mi) e do gap IFRS × BR GAAP.
- Impacto da curva de hoje no ORA e no CET1.
- Release oficial "Análise do Desempenho" (o analista usou Reuters/Forbes, InfoMoney e BP Money).
- Sensibilidade oficial a juros.

Fontes desta revisão:
- [Mercado & Consumo — BB lucro ajustado R$ 3,9 bi no 2T26](https://mercadoeconsumo.com.br/13/08/2026/mc-capital/banco-do-brasil-tem-lucro-liquido-ajustado-de-r-39-bi-no-2t-alta-de-33/)
- [Trademap — BB 2T26](https://trademap.com.br/noticias/news-8201683)
- [AUVP — payout 30% / JCP 4T25](https://analitica.auvp.com.br/noticias/banco-do-brasil-aprova-r12-bi-em-jcp-com-pagamento-em-marco-de-2026-u)
- [Suno — JCP BB](https://www.suno.com.br/noticias/?p=651692)
- [Money Times — JCP R$ 465,7 mi](https://www.moneytimes.com.br/banco-do-brasil-bbas3-pagara-r-4657-milhoes-em-jcps/)
