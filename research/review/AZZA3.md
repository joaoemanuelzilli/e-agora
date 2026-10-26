# Revisão independente — AZZA3 (Azzas 2154) · 26/10/2026

**Veredito: ok.** Não achei erro objetivo. As premissas são coerentes com o CVM e, no conjunto, levemente conservadoras. Duas delas são discutíveis e vão em sentidos opostos: o IR perpétuo de 15% e a D&A abaixo da CVM. Nenhuma alteração em `research/AZZA3.json`.

Preço de referência (foto B3): R$ 16,50. No motor, que não mudou:
- valor justo **R$ 6,90** (DCF 5,18 · DDM 5,11 · múltiplos 12,12);
- TIR implícita **12,7%**;
- TIR de 3 anos **13,2%**.

## Checagens contra o histórico CVM
| Item | Premissa | Histórico / evidência | Avaliação |
|---|---|---|---|
| Receita | −5,4% / +4% / +6% / +6% / +6% | 1S26 R$ 5.144 mi (−8,1% a/a). Para fechar o ano, o 2S26 precisa de −3,0% (6.038 vs 6.222 no 2S25). CAGR CVM 5a de 49% é inorgânico. | ok |
| Margem EBITDA ("econômica", −3 p.p.) | 8,8% → 12,5% (CVM equivalente 11,8% → 15,5%) | MDR + AVP de fornecedores = R$ 158 mi no 1S26 (3,07% da receita). CVM 1S26 11,6%; 2025 15,5%; média 5a 15,5%. O 2S26 implícito (12,1% CVM) fica abaixo do 2S25 (13,9%). | Ajuste correto. Não há dupla contagem, porque `other_financial` exclui MDR/AVP. |
| Resultado financeiro | 12,5–13,5% × DL + R$ −90 mi | Modelo: 2026 −444, 2027 −460. Real 1S26 ex-MDR/AVP −214 (anualizado −428). Custo all-in do modelo sobre a DL: 15,7% (2026) → 16,8% (2027) → 16,0% (2030), contra CDI a termo de ~15,2–15,9% (DI1F28–F31). | Coerente com a curva nova. |
| D&A | 5,4% → 5,0% | DFC/DVA: 5,9% (2025), 6,2% LTM, 6,5% no 1S26. A DFC separa a baixa de ativos (R$ 29 mi) da D&A (R$ 697,5 mi = DVA). | Abaixo da CVM, ver achado 2 |
| Capex (com direito de uso) | 4,6% → 5,0% | Capex caixa 3,2% (2025), 2,7% (1S26). Adições de direito de uso observadas ~0,8% da receita: o passivo de arrendamento caiu de 876 para 770 e depois 705, com principal de ~R$ 204 mi/ano. | Conservador no curto prazo; no longo prazo, capex ≈ D&A, coerente. |
| Capital de giro | 25% da receita incremental | (Receb. + estoques − fornecedores)/receita: 26,8% em 2025 e 25,6% no 2T26 | ok |
| IR | 0% → 15% (15% na perpetuidade) | IR diferido ativo de R$ 1.847 mi (~R$ 5,4 bi de base a 34%). IR pago em caixa: R$ 37 mi em 2025. Antes de 2024, o ETR da Arezzo ficava em 10–27%. | Defensável até 2030; generoso na perpetuidade, ver achado 1 |
| Payout | 25% → 45% | Média 5a 27%. 2025: 55% em dividendos + R$ 167 mi de recompra. Nada pago no 1S26. | ok (DL/EBITDA projetada cai de 2,8x para 1,4x) |
| ROIC_T / ROE_T | 14% / 15% | Projetados para 2030: 7,8% / 6,1%, deprimidos por R$ 3,4 bi de intangível da fusão | Marginais acima da média, abaixo do WACC (19,7%) e do Ke: coerente com a tese de "armadilha" |
| WACC | wd 35%, Kd 15% | DL 2.832 / (DL + valor de mercado pré-eleição 5.160) = 35,4% | ok. Kd de 16,5% custaria −R$ 0,19. |
| DL base | R$ 2.832 mi | 3.267,9 + 705,4 − 1.140,9 (CVM 30/06/26) | ok |
| Debt-like / não operacional | +112 / +160 | Aquisições a pagar 89,2 + parcelamentos 22,5; 50% do IR/CSLL a recuperar | ok, ver lacunas |
| Ações | 202,18 mi | 206,49 mi − 4,31 mi em tesouraria | ok |

## Sensibilidade (valor justo / TIR implícita / TIR 3a)
| Caso | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | R$ 6,90 | 12,7% | 13,2% |
| IR 2030 e perpetuidade 24% | R$ 6,12 | 12,0% | 11,5% |
| IR 0 / 10 / 15 / 20 / 24% | R$ 5,85 | 11,9% | 8,1% |
| D&A 6,0% fixa (≈ CVM) | R$ 5,52 | 11,3% | −1,4% |
| Custo da DL +1 p.p. | R$ 6,63 | 12,3% | 9,3% |
| Margem +1 p.p. | R$ 9,96 | 14,6% | 29,8% |
| Margem −1 p.p. | R$ 3,83 | 10,7% | −6,7% |
| ROIC_T = WACC (19,7%) | R$ 7,66 | 12,7% | 13,2% |
| EV/EBITDA-alvo 4x | R$ 6,14 | 12,7% | 13,2% |
| "Bull" combinado (margem +2 p.p. e ROIC_T 20%) | R$ 14,01 | 16,5% | 44,6% |

A margem é o driver dominante: cada 1 p.p. move o valor justo em ±44%. A conclusão é robusta. Mesmo no bull combinado, o valor justo fica abaixo do preço (R$ 16,50) e a TIR implícita bem abaixo de 25%. A TIR de 3 anos é muito volátil, porque depende do LPA de 2029 sobre um lucro fino.

## Achados
1. **(média, viés para cima) IR de 15% na perpetuidade.** O ativo fiscal diferido sustenta alíquota baixa por vários anos. Se ele for amortização fiscal do ágio da fusão (60 meses a partir de ago/24), porém, o benefício acaba por volta de 2029. Com 24% em 2030 e na perpetuidade: R$ 6,12 (−11%) e TIR 12,0%. Não alterei, porque a composição do diferido não está nas fontes lidas e o efeito não muda a conclusão.
2. **(média, viés para cima no lucro contábil) D&A projetada de 5,0–5,4%, contra 5,9–6,5% na CVM.** O dossiê atribui a diferença a baixas dentro da D&A da DVA. Na DFC, porém, a baixa está numa linha própria (R$ 29 mi em 2025) e a D&A da DFC é igual à da DVA. A diferença de ~1 p.p. pode ser amortização de PPA ou de direito de uso. Para o FCFF, D&A ≈ capex de 5% é economicamente defensável e quase não pesa, porque o IR é baixo. No LL (DDM e P/L), a premissa infla o lucro em ~R$ 100 mi/ano antes do IR: com D&A de 6%, R$ 5,52 e TIR 11,3%. Não alterei; o caso é para monitorar.
3. **(baixa) Custo financeiro.** Os 12,5–13,5% sobre a DL parecem baixos frente à curva, mas, somados aos R$ −90 mi de `other_financial`, dão custo all-in de 15,7–16,8% sobre a DL. Isso é coerente com o CDI a termo e com o run-rate do 1S26. Ok.
4. **(baixa, conservador) Adições de direito de uso.** O capex assume ~1,8–2,0% da receita (estado estacionário ≈ depreciação do direito de uso), mas o observado em 2025 e no 1S26 foi ~0,8%, com fechamento de lojas. O efeito é pequeno: capex −0,5 p.p. dá R$ 7,49.
5. **(informativo) Múltiplos × DCF.** O EV/EBITDA de 5x dá R$ 16,89/ação, contra R$ 5,18 do DCF, cujo EV/EBITDA de saída implícito é 2,3x. É a perna que sustenta o blend. A 4x, o valor justo seria R$ 6,14.
6. **(informativo) Lucro de 2026.** O LL do modelo é R$ −64 mi, contra R$ +68 mi reais no 1S26 (IR diferido de +R$ 181 mi). A diferença vem do piso de IR ≥ 0 do motor. Não afeta o valor, porque o dividendo de 2026 é zero, o que é coerente com nada pago no 1S26.

## Mudanças
Nenhuma.

## O que não deu para verificar
- Composição e prazo do IR diferido ativo de R$ 1.847 mi: prejuízo fiscal × ágio × diferenças temporárias.
- A D&A "recorrente" de ~R$ 146 mi/tri citada do release, e se a diferença para a CVM é PPA.
- Provisões para contingências de R$ 622 mi (vindas do PPA da Soma): não foram tratadas como debt-like. Se fossem, −R$ 3,1/ação no DCF, sem mudar o veredito.
- Divisão do "IR/CSLL a recuperar" (R$ 323 mi) dentro de tributos a recuperar (R$ 714 mi).
- Estrutura de capital das duas companhias pós-cisão; MDR e AVP do 2S25.
