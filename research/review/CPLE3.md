# CPLE3 (Copel): revisão independente (red team G11, 26/10/2026)

**Veredito: ok.** Não mudei nenhuma premissa. Elas são coerentes com a CVM e com o release 2T26. As que destoam do histórico erram para o lado conservador, e pouco.

Motor (foto R$ 15,18; 2.970,1 mi ações ON; market cap R$ 45.086 mi, confere): VJ **R$ 2,79**, TIR implícita **8,3%**, TIR 3 anos −17,8%. Métodos: DCF −R$ 1,94 (piso 0), DDM R$ 3,20, múltiplos R$ 7,97.

## Conferido e coerente
- **Receita-base** de R$ 22.486 mi: ROL de R$ 26.117 mi, menos construção de R$ 3.470 mi, menos VNR de R$ 161 mi.
- **EBITDA e equivalência**: o EBITDA recorrente da Copel exclui equivalência (−R$ 125,7 mi no 1S26), VNR (−R$ 308,8 mi) e efeito IFRS da transmissão (release 2T26, tabela de reconciliação). A margem é ex-equivalência e a equivalência entra em `other_financial` (+R$ 220–260 mi; CVM LTM R$ 201 mi). **Não há dupla contagem.**
- **EBITDA 2026E** de R$ 6.674 mi, igual a 2 × o 1S26 recorrente (R$ 3.367 mi, +18,6%). D&A de R$ 1.662 mi contra run-rate de R$ 1.624 mi (2T26 × 4).
- **Custo da DL**: 12,0% × R$ 19.599 mi, ancorado no resultado financeiro recorrente do 1S26 (−R$ 1.142,9 mi; 12,4% a.a.). O custo médio é de 12,92% (91,33% do CDI).
- **DL**: CVM R$ 19.599 mi contra R$ 19.651 mi da companhia. `other_debt_like` de R$ 2.700 mi: pós-emprego R$ 1.491 mi, UBP R$ 382 mi, JCP a pagar R$ 632 mi e derivativos R$ 195 mi. O JCP já declarado não entra no stub do DDM, então não há dupla contagem.
- **Payout de 75%** (política do FR de 15/07/2026). A DL/EBITDA projetada fica em 3,1–3,2x, no topo da banda de 2,6–3,2x. É coerente: o modelo não paga acima do que a banda permite.
- **Capex** de R$ 4,0–4,3 bi/ano, acima do plano de R$ 18 bi em 5 anos (R$ 3,6 bi/ano) mais o LRCAP. Leve viés conservador.
- **Minoritários a 1%** (histórico ~0). Shares e market cap conferem.

## Achados (sem mudança)
| # | Severidade | Achado | Evidência / sensibilidade |
|---|---|---|---|
| 1 | Baixa | IR de 20–22% contra efetiva de 14–18% em FY23–LTM. Com payout de 75% via JCP, o benefício fiscal é grande: −R$ 219,8 mi de tributos no 2T26 só pelo JCP de abril. Mantive porque o tratamento do JCP é um risco legislativo real num 4º mandato. | IR de 17%: VJ 2,89 / TIR 8,6%. |
| 2 | Baixa | Margem plana em 27% de 2027 em diante, apesar da RTP de 23/06/2026 (OPEX regulatório +52,9%, BRR de R$ 19,9 bi). O LL do stub do 2S26 (R$ 1.149 mi) fica abaixo do 1S26 recorrente (R$ 1.284 mi). | Margem de 27,5%: VJ 2,91. Com IR de 17%: VJ 3,01 / TIR 8,8%. |
| 3 | Média | Curva: o custo da DL cai de 12,4% para 11,2% com CDI em queda. | Curva de hoje: VJ 2,63 / TIR 7,8%. |
| 4 | Metodológica | O DCF é negativo (WACC de 20,3% contra ROIC de ~9%) e entra como zero com peso de 50%. O P/L de mercado de 18,9x 2027E contra o alvo de 10x explica a TIR 3 anos negativa. | Sem DCF: VJ 5,59. Tudo otimista (IR 17%, margem 27,5%, 12x / 7,5x, g 5,5%): VJ 3,53 / TIR 9,3%. |

A conclusão é robusta: a TIR de dono fica entre 7,8% e 9,3% em todas as variantes, contra Ke de 25%. A ação é defensiva, mas cara para a meta do usuário.

## Mudanças
Nenhuma. VJ **R$ 2,79** e TIR **8,3%** antes e depois.

## O que não deu para verificar
- O % da dívida em CDI (estimado em 60%).
- O efeito integral da RTP no EBITDA da Copel DIS em 2027.
- O consenso.
- O resultado do 3T26.
