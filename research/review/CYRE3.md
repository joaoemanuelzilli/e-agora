# Revisão independente — CYRE3 (Cyrela) · 26/10/2026

**Veredito: ajustada, com mudança pequena.** Não há erro de dados.

- **Única correção:** o escudo fiscal de 34% no WACC é incoerente com o RET. Alinhei ao critério já usado no estudo para DIRR3, PLPL3, TEND3 e MDNE3.
- **Demais premissas:** batem com o histórico CVM. Os pontos discutíveis vão para os dois lados e quase se anulam.
- **Conclusão mantida:** valor justo abaixo do preço e TIR de ~20%, contra Ke de 25%.

| (preço R$ 20,13, foto 13h02) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 17,41 (−13,5%) | **R$ 17,03 (−15,4%)** |
| TIR implícita | 20,7% | 20,7% |
| TIR 3 anos | 26,6% | 26,6% |
| DCF / DDM / P/L / EV-EBITDA | 15,88 / 15,95 / 22,53 / 21,31 | 15,12 / 15,95 / 22,53 / 21,31 |
| WACC | 22,7% | 23,4% |
| P(valor > preço), Monte Carlo | 17,8% | 14,2% |

## Mudança em `research/CYRE3.json` (original em `research/review/CYRE3.orig.json`)
**`wacc.kd_pre_tax`: 0,145 → 0,22**, ou seja, 14,5%/0,66, Kd sem benefício fiscal. Motivos:
- As SPEs estão no RET: o IR corrente é ~2,1% da receita e a alíquota efetiva do modelo é 8%.
- A holding concentra G&A (R$ 525 mi) e juros, e provavelmente opera com prejuízo fiscal.
- Na margem, os juros não reduzem o imposto. O motor aplica (1 − 34%) fixo.

Efeito: valor justo −R$ 0,38. A TIR não muda, porque vem do DDM. O motor foi re-rodado e `data/model/CYRE3.json` foi atualizado. `data/app` não foi regenerado.

## O que conferi e está coerente

**Ações.** São 435,76 mi ex-tesouraria; B3/CVM = 1,000. A divisão ON/PN do motor (369,0/66,7) difere um pouco da do dossiê (366,3/69,4). O efeito é nulo: a CYRE4 não está na foto, e o market cap usa o preço da ON.

**DL e PL.**
- DL = 1.161 (CVM) + 887 de AVJORA = 2.048.
- PL = 11.168 − 878 de ORA = 10.290. No FY25: 10.227 − 704 = 9.523.
- No BPA: VJORA = 1.401,9 + 3.494,2 = 4.896; caixa de tesouraria = 7.712 − 4.896 = 2.816.
- A carteira CashMe entra a custo na DL e o funding (2.813) na dívida bruta. Não há dupla contagem.

**AVJORA.** Os R$ 450 mi (~50% do AVJORA) são coerentes com uma marcação de −R$ 260 a 510 mi: +150 a 300 bp de juro × duration de ~3,5 anos sobre R$ 4,9 bi.

**Capital de giro de 0,95x.** O CG operacional (recebíveis CP+LP + estoques CP+LP − "outros" CP − "outras provisões" LP) foi:
- 1,02x (2023), 0,92x (2024), 1,00x (2025) e 0,98x (2T26);
- marginal de 0,97x em 2023→25.

**Margem com juros capitalizados.**
- Base recorrente CVM: (2.458 − 279 de ganhos em investimentos)/9.423 = 23,1% no FY25; ≈ 21,8% no 1S26.
- O ajuste de +2,5 p.p. fica entre a DFC 2025 ("encargos capitalizados" de 178, ou 1,9 p.p.) e o release do 2T26 (2,9 p.p.).
- O lucro fica neutro: resultado financeiro do modelo de 2026 + juros capitalizados ≈ +213, contra LTM CVM de +229.

**Minoritários de 15%.** Foram 16,2% em 2025, 15,1% no LTM e 14,8% no 1S26.

**Payout.** O payout de 40→70% fica abaixo do sustentável (1 − g/ROE = 71%). A DL cai de 2.048 para 648 em 2030. O DDM (15,95) ≈ DCF antes do ajuste (15,88).

**Múltiplos citados.** Batem com `data/market`:
- P/L de 5 anos: mediana 6,06, p25 5,29;
- P/VP: 0,98 / 0,89;
- EV/EBITDA: 5,64 / 5,10.

**Coligadas.** A equivalência está dentro do EBIT 3.05, sem dupla contagem com `non_operating_assets`.

## Achados mantidos (sensibilidades sobre a versão ajustada, aprox.)
| # | Sev. | Achado | Evidência | Sensibilidade |
|---|---|---|---|---|
| 1 | média (método) | P/L-alvo de 5,3x e EV/EBITDA de 4,6x (p25 histórico) não batem com Ke de 25% | Com ROE de 17,5%, o Gordon dá P/VP de 0,625x e P/L ≈ 3,6x, e o próprio analista usa esse Gordon para o P/VP. A perna de múltiplos (R$ 21,9) fica ~40% acima do DCF/DDM. A TIR de 3 anos depende da saída a 5,3x | Múltiplos de Gordon: valor ≈ R$ 15,2 e TIR 3a ≈ 9%. Mantido: segue a spec |
| 2 | baixa/média | Caixa do 2S26 otimista | O motor gera +R$ 704 mi pré-dividendos no 2S26, contra +R$ 406 mi reportados no 1S26 inteiro. A prévia do 3T26 não traz caixa. O ΔCG/Δreceita da DFC foi de 0,92–1,56x em 2023–1S26 | CG de 1,10x: −R$ 0,3 |
| 3 | baixa | IR de 8% abaixo da média de 2021–25 (9,5%) | 1S26: 10,8%. Em 2025, 5,8% (corrente: 7,8%) | IR de 9,5%: −R$ 0,35 / TIR −0,3 p.p. |
| 4 | baixa | ROE terminal de 17,5% acima do ROE do modelo em 2029–30 (16,7–16,9%) | Média CVM de 2021–25: 15,3%; de 10 anos: ~10% | ROE_T 16,5% / ROIC 15,5%: −R$ 0,12 |
| 5 | baixa | Kd cai de 13,5% para 11%, com DI1F29–F31 em 15,4–15,7% | Efeito mínimo, porque a DL é pequena | −R$ 0,06 |
| 6 | baixa (conservador) | Coligadas subavaliadas | Valem ~R$ 1,5 bi implícitos no modelo, contra ~R$ 2,0 bi pelos valores justos do estudo (CURY3 22,74; PLPL3 6,94) e pela Lavvi a mercado | +R$ 500 mi: +R$ 0,7 |
| 7 | info | Capex líquido baixo | Capex de 2,2% contra D&A de 2,0% (líquido de 0,2% da receita). O histórico teve ~1,5 p.p. de capex líquido; no 1S26, D&A de 2,7% e capex de 3,7% | Capex 3%: −R$ 0,37 |

Nenhuma variação plausível leva o valor ao preço nem a TIR a 25%. A 20% de Ke, o valor chega perto do preço.

## O que não deu para verificar
- REF, landbank e distratos do 2T26.
- Participações exatas na Lavvi e na Cury (inferidas da equivalência).
- AVJORA da CashMe depois do choque.
- Geração de caixa do 3T26.
- Natureza dos +R$ 480 mi de imobilizado em 2025.
- Receita atípica do 4T25 (R$ 3,2 bi, +52% t/t) na base de 2026.
- Rótulos da DFC 2026Q2, que parecem deslocados; não usei esses números.
