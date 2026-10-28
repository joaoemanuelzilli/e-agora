# TAEE11 — Taesa | dossiê (3ª rodada, 28/10/2026)

**Veredito: renda indexada de boa qualidade, mas com prazo de validade.** A 25% de Ke o fluxo de dividendos fica muito abaixo do preço; a perpetuidade depende da regra de prorrogação de TSN/Novatrans (dez/2030). Confiança média.

## Negócio
- 44 concessões de transmissão: 14 na holding (TSN, Novatrans, ETEO, GTESA, PATESA, Munirah, NTE, STE, ATE, ATE II, ATE III, Sant'Ana, Saíra, Miracema), 11 investidas integrais (Janaúba, São Pedro, Ananaí, Tangará, Juruá etc.) e 19 participações por equivalência (ETAU 75,6%, TBE 49,99%, AIE 50%).
- Controle: Cemig (estatal mineira) e grupo ISA. **Unit = 1 ON + 2 PN**; 1.033,5 mi ações = 344,5 mi units.
- RAP do ciclo 2026/27 (Despacho ANEEL 2.268/2026): R$ 4,56 bi com investidas (R$ 4,29 bi operacional); consolidada ~R$ 3,37 bi, 57% IGP-M (contratos 2000–2006) e 43% IPCA.

## IFRS × regulatório (por que a base é regulatória)
- IFRS (CPC 47/ICPC 01) reconhece receita de construção com margem, remuneração e correção monetária do ativo de contrato: no 2T26, LL IFRS R$ 567,1 mi contra R$ 206,8 mi regulatório; no 6M26, R$ 920,8 mi contra R$ 399,4 mi.
- O regulatório (manual ANEEL, auditado anualmente) registra a RAP faturada e o investimento como imobilizado depreciado: é o mais próximo do caixa e é a base do payout de 100%. Uso overrides.revenue_2025 = R$ 2.513,3 mi.

## Histórico CVM (IFRS) — pouco útil por causa da construção
| | 2021 | 2022 | 2023 | 2024 | 2025 | UDM 2T26 |
|---|---|---|---|---|---|---|
| Receita (R$ mi) | 3.472 | 2.617 | 3.361 | 3.718 | 4.624 | 4.484 |
| Margem EBITDA | 99,6% | 94,3% | 70,0% | 77,7% | 60,5% | 66,8% |
| LL (R$ mi) | 2.214 | 1.449 | 1.368 | 1.694 | 1.580 | 1.625 |
| ROE | 34,8% | 21,9% | 20,7% | 24,9% | 21,7% | 20,7% |
| DL/EBITDA | 1,9x | 2,9x | 3,6x | 3,1x | 3,6x | 3,5x |
- Regulatório 2025: receita R$ 2.513,3 mi (+7,9%), EBITDA R$ 2.104,4 mi (83,7%; +12,5%), LL R$ 1.124,1 mi (+13,4%), proventos R$ 1.124,1 mi (100%).

## 2T26 (release 11/08/2026)
- Receita regulatória R$ 679,2 mi (+9,3%), EBITDA R$ 577,2 mi (85,0%), equivalência R$ 90,8 mi (−14,1%), resultado financeiro −R$ 366,5 mi (+51%: IPCA 1,99% e IGP-M 3,07% no trimestre), LL R$ 206,8 mi (−28,5%). 6M26: LL R$ 399,4 mi (−16,4%).
- Dívida bruta R$ 11.009 mi (IPCA 67,5%, CDI 29,6%, IGP-M 3%; swaps de R$ 1,45 bi IPCA→CDI nas 17ª/18ª emissões → ~43% CDI efetivo); caixa R$ 586 mi; DL R$ 10.422,7 mi; proporcional R$ 13.002 mi = 4,2x EBITDA.
- Projetos: Ananaí, Tangará, Saíra (energizações parciais mar–jul/26), Juruá (jun/28, capex >25% abaixo do ANEEL); reforços com RAP de R$ 66 mi.
- Compra de 100% de 5 transmissoras da Energisa (GO/PA/TO; RAP ~R$ 291 mi; EV R$ 2.293 mi, equity R$ 1.545 mi): CADE ok (jun), AGE ok (14/07), falta ANEEL.

## Proventos
- 100% do lucro regulatório, trimestral, majoritariamente JCP. 1T26 R$ 0,56/unit (pago 26/08); 2T26 R$ 0,60/unit (data-com 14/08, paga 26/11 → tratado como dívida).

## Eleição
- −10% no dia (R$ 44,75 → R$ 40,24), metade do Ibovespa. Canal: taxa de desconto (NTN-B) + CDI a termo encarecendo a dívida da Energisa; risco político concentrado na regra federal das concessões vincendas (ANEEL CP 43/2025; conclusão prevista no 2S26).

## Premissas (research/TAEE11.json) e por quê
- Receita regulatória: 2026 = run-rate do 2S26 (R$ 2,82 bi; novo ciclo + energizações); 2027 +13,5% (Energisa ~R$ 265 mi + rampa de Tangará/Saíra + reajuste); 2028 +5,2% (Juruá, reforços); 2029 +4,5%; 2030 +2,5% (ETEO vence em 2030; perda de 65% da receita).
- Margem 85–85,5% (6M26: 85,4%); D&A regulatória 19,5%; IR efetivo 5–8% (JCP, SUDAM/SUDENE, presumido nas SPEs; 6M26 teve crédito).
- Capex: 2026 inclui o EV da Energisa (R$ 2.293 mi, fechamento suposto no fim de 2026) ÷ 0,504 (fração do ano); depois só Juruá e reforços (R$ 0,15–0,28 bi/ano). Novos leilões não modelados (VPL negativo a 25%).
- Custo da DL 12,3% → 12,9% → 12,6% (IPCA ~4,5–4,8%, CDI a termo 14,6–15,5%, dívida da aquisição). Equivalência regulatória de R$ 360–410 mi em other_financial; investidas a R$ 2,7 bi em non_operating_assets (7x EBITDA proporcional − DL proporcional, −30%).
- Payout 100% (2026) e 95% (2027–30). DL/EBITDA consolidada de 5,3x (2026, sem o EBITDA da Energisa) a 3,5x (2030).
- **Perpetuidade: g 3%, ROIC_T 8%, ROE_T 6%.** ~61% da RAP consolidada vence entre 2030 e 2036 (TSN/Novatrans dez/2030 = R$ 1,09 bi; ETEO 2030; GTESA/PATESA/NTE 2032; Munirah/STE/ATE 2034; ATE II 2035; ATE III 2036), com valor residual de só R$ 3,6 bi. Um fluxo explícito pós-2030 com perda de 65% da receita de cada concessão no vencimento dá TV de FCFF ~R$ 9,7 bi contra R$ 11,2 bi da fórmula com ROIC 12%; ROIC_T 8% reproduz isso. No DDM, ROE_T 6% = reinvestir 50% do lucro para crescer 3% (reposição da RAP vencida). Datas de vencimento por concessão: memória de mercado (contratos de 2000–2006 × 30 anos), não verificadas em fonte primária.
- Múltiplos 8,5x P/L e 6,5x EV/EBITDA regulatórios de 2027E (abaixo de ALUP11: 11x/7x) porque 37% do EBITDA vem de concessões que vencem em 2030 com D&A ~zero.

## Saída do motor (foto 26/10, R$ 40,24/unit; referência)
- VJ R$ 11,50/unit; DDM 11,57, DCF 7,04, P/L 19,90, EV/EBITDA 20,82; TIR implícita 7,7%; TIR 3 anos −8,4%; Monte Carlo p10/p50/p90 8,94/11,42/14,07; P(valor > preço) 0%; bear 10,42 / bull 12,30.
- **Divergência entre métodos (~2,9x)**: os múltiplos embutem o Ke de mercado (11–13%); DCF (WACC 17,5% contra ROIC de ~10–11%) e DDM usam Ke 25%. Não é erro de premissa: é a distância entre o retorno de uma renda regulada (~IPCA+7%) e a meta de 25%.
- Sensibilidades: perpetuidade da Alupar (3,5%/12%/14%) → VJ 13,24, TIR 9,9%; sem a compra da Energisa → VJ 14,68 (a aquisição destrói valor a 25%); múltiplos 10x/8x → 13,43; custo da DL +50 bp → 11,16.

## Riscos
- Regra de prorrogação/relicitação das concessões vincendas e indenização (residual histórico, sem correção).
- Alavancagem e CDI; fechamento e integração da Energisa; queda da equivalência (TBE/AIE com dívida IPCA e concessões antigas vencendo 2030–34).

## Não verificado
- Datas exatas de vencimento por concessão; prazo médio e covenants da dívida; mínimo estatutário de dividendos; data do 3T26; mudanças no bloco de controle.

## Fontes
- Release 2T26: https://investidor10.com.br/acoes/link_comunicado/TAEE3/47455/ (tabelas de RAP, dívida, valor residual e DFC regulatório lidas das páginas 4, 10, 20–22, 34 e 44).
- 4T25: https://investidor10.com.br/acoes/link_comunicado/TAEE3/34372 ; Finance News (18/03/2026).
- Energisa: Cenário Energia (21/05/2026), Agência Infra (15/07/2026); research/ENGI11.json (EV, equity, DL das SPEs).
- CVM padronizado: data/hist/TAEE11.json; mercado: data/market/TAEE11.json.
