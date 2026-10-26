# ECOR3 — EcoRodovias · dossiê (26/10/2026, pós-2º turno)

**Veredito (Ke 25%): armadilha alavancada, não oportunidade.** Valor justo do motor ≈ **R$ 2,15** vs **R$ ~5,0** (−58%). TIR implícita (DDM) **17,9%** < 25%. A queda de 62% no dia é, em sua maior parte, repricing racional de um equity fino sobre ativos longos e dívida indexada. Confiança: média.

## Negócio
- Holding de **11 concessões rodoviárias**: Ecovias Imigrantes, Leste Paulista, Capixaba, Ponte, Norte Minas, Minas Goiás, Cerrado, Rio Minas, Araguaia, Noroeste Paulista, Raposo Castello. Mais Ecoporto Santos (em contrato de transição) e Ecopátio. Controle: grupo italiano ASTM (Gavio).
- Ecovias Sul (Ecosul): contrato **encerrado em 04/03/2026** (EBITDA ajustado de ~R$ 0,48 bi/ano em 2025).
- **Ecovias das Gerais** (BR-251/BR-116 MG, 30 anos): contrato assinado em jun/26, trecho assumido em jul/26, pedágio previsto **até jan/27**. Segundo a companhia, ela "compensará integralmente" a saída da Ecosul.
- Capex contratual a realizar: **R$ 50,9 bi** (base jun/26, sem Gerais). Financiamentos de LP contratados: R$ 18,4 bi, dos quais R$ 10,6 bi ainda a desembolsar (Norte Minas, Minas Goiás, Rio Minas, Araguaia, Noroeste).
- Prazos: as concessões federais recentes são de 30 anos (Gerais até ~2056). **Não verifiquei** o vencimento contrato a contrato, em especial o da Imigrantes (SP), a mais antiga.

## 2T26 (release de 30/07/2026, conferido com a CVM)
| R$ mi | 2T26 | 2T25 | Var. |
|---|---|---|---|
| Receita líquida ajustada (sem construção) | 1.836,6 | 1.818,9 | +1,0% (comparável +9,8%) |
| EBITDA ajustado | 1.348,4 | 1.363,2 | −1,1% (comparável +9,0%) |
| Margem EBITDA ajustada | 73,4% | 74,9% | −1,5 p.p. |
| Resultado financeiro | −804,6 | −614,2 | +31% |
| Lucro do controlador / recorrente | 21,0 / 52,9 | 203,9 / 204,5 | −90% / −74% |
| Capex | 1.547,2 | 1.171,9 | +32% |

- Receita de construção no 2T26: R$ 1.118,7 mi (38% da receita total). Ela distorce as margens, por isso a base do modelo **exclui construção**.
- Tráfego comparável **+3,2%**. Tarifas reajustadas pelo IPCA (4,72%) mais R$ 0,10 cautelar em Imigrantes e Leste Paulista.
- **Dívida bruta** R$ 28.851,5 mi. Caixa R$ 5.371,4 mi. **DL R$ 23.480 mi, 4,1x** o EBITDA ajustado UDM (subholding ECS 3,9x). Fora da DL: R$ 3.342 mi de obrigações com poder concedente e R$ 364 mi de arrendamentos.
- **Indexadores:** 77% IPCA/TLP (R$ 22.253 mi) · 20% CDI/pré (R$ 5.650 mi) · 3% TJLP. Prazo médio de 7,6 anos. Vencimentos: R$ 674 mi no 2S26 e R$ 1.331 mi em 2027 (90% vencem a partir de 2029).
- **Covenant:** DL/EBITDA ajustado de **4,75x**, segundo relatórios de crédito do Santander (ago/24 e ago/25). Não verificado na escritura.

## Histórico (CVM padronizada)
- Receita **sem construção** (DRE 3.01 − DVA 7.01.03): 5.395 → 6.440 → 7.406 (2023–25), CAGR de **17,2%** com as novas concessões.
- EBITDA recorrente sobre receita sem construção: 69,4% / 70,6% / 73,4%. O FY2025 da CVM (5.640) inclui reversão de impairment da Capixaba de +202,7.
- ROE de 2021–25: 34% / 11% / 23% / 29% / 24%. O PL é pequeno, de R$ 4,1 bi. Payout em caixa: 0 / 2% / 10% / 15% / 24%.
- Dividendo de 2025: **R$ 0,3024/ação** (R$ 210 mi), data-com 12/05/2026.

## Premissas (research/ECOR3.json)
- **Receita:** +3% (2026) · +16% (2027, entrada da Gerais e degraus) · +13% · +11% · +10%. CAGR 2025–30 de **10,5%**, abaixo do histórico.
- **Margem EBITDA IFRS:** 73% → 76% em 2030. **D&A:** 19% → 22% da receita.
- **Capex** (sem outorga e sem juros capitalizados): R$ 5,3 bi / 6,3 / 6,5 / 6,3 / 5,8 bi. Em % da receita: 69,5% → 47,5%.
- **Custo da DL:** 15% → 13,5%, em base bruta (inclui ~R$ 0,4–0,6 bi/ano de juros capitalizados). **IR efetivo:** 42% → 35%, porque SPEs pré-operacionais têm prejuízo sem diferido. **Payout:** 25–35%.
- **Perpetuidade:** g = 3,5% com ROIC_T = 16% ≈ WACC. Como as concessões são finitas, o valor residual equivale ao capital investido, sem criação de valor (novos contratos são licitados a ROIC ≈ WACC). Com ROIC = WACC, g não altera o valor.
- **WACC:** 15,9% (D/V 60%, Kd 15%).
- **Itens debt-like:** obrigações com poder concedente, Acordo do Paraná e ANPC, R$ 3.486 mi. Ativo não operacional: indenização do Ecoporto, R$ 352 mi.
- **Múltiplos-alvo:** P/L 6x (p10 de 5 anos 5,7x; mediana 8,7x). EV/EBITDA 5,3x (p10 de 4,7x mais ~0,6x das obrigações com poder concedente).

## Saída do motor (pipeline/model.py)
- **DCF: −R$ 21/ação.** EV de R$ 12,4 bi contra R$ 27,3 bi de dívida e equivalentes. FCFF negativo até 2029 e saída implícita de ~3,0x EBITDA.
- DDM R$ 2,99 · Múltiplos R$ 5,59 · **Justo R$ 2,15** · Bear R$ 0,81 · Bull R$ 3,06 · Monte Carlo p10–p90 R$ 1,0–3,4 (P(valor > preço) ≈ 0).
- **DL/EBITDA:** 4,6x em 2026 · 4,7x · 4,6x · 4,5x · 4,3x em 2030. Fica **colado no covenant de 4,75x** e a DL vai de R$ 24 bi para R$ 40 bi em 2030.
- **Sensibilidade a Ke:** justo R$ 4,8 a Ke 12% (WACC 10,7%) e R$ 2,9 a Ke 16%. O preço atual implica Ke de ~12–18%.

## Eleição: macro vs. micro
- **Macro e alavancagem.** O equity é ~11% do EV. O EV, incluindo obrigações com poder concedente, caiu ~16% (de R$ 36 bi para R$ 31 bi), mas a ação caiu 62%. Juro real mais alto encarece a dívida IPCA e o refinanciamento: cada +200 bp em ~R$ 18 bi a captar ou rolar até 2030 custa ~R$ 0,36 bi/ano.
- **CDI quase neutro:** a dívida CDI/pré é de R$ 5,65 bi e o caixa de R$ 5,37 bi. **IPCA:** cada +100 bp custa ~R$ 223 mi/ano de correção da dívida antes do repasse tarifário.
- **Regulatório.** No 3º mandato, Lula manteve leilões e repactuações via TCU/consenso. Risco moderado de atraso em reequilíbrios: pleitos não contratuais, como o free flow da Imigrantes (R$ 264,7 mi). Contratos estaduais de SP têm outra dinâmica.
- No data/market, o resíduo idiossincrático do dia é de −26% vs. beta e −12% vs. a predição cross-section. Há algum excesso, mas o valor intrínseco a Ke 25% está abaixo do preço.

## Riscos e catalisadores
- **Riscos:** covenant, que pode levar a emissão de ações diluidora; execução simultânea de obras; inflação; tráfego com PIB fraco; Ecoporto; leniência/ANPC.
- **Catalisadores:** resultado do 3T26 (nov/26); início da cobrança na Gerais (jan/27); degraus tarifários de 2027–28; queda da NTN-B.

## Problemas de dados
- Prazos de cada concessão e o covenant não foram verificados nas escrituras.
- A margem e o CAGR sem construção só existem para 2023–25 (a DVA da padronização cobre só os 3 últimos anos fiscais).
- Não há guidance anual de capex: a trajetória de 2027–30 foi estimada a partir do capex contratual a realizar.

## Fontes
- Release 2T26 · Apresentação 2T26 (api.mziq.com, RI EcoRodovias)
- CVM ITR/DFP (data/hist/ECOR3.json)
- B3 proventos
- Santander Research (crédito, covenant)
- ASTM (Rota das Gerais, 01/04/2026)
- Money Times / Investidor10 (2T26)
- data/market/ECOR3.json (múltiplos de 5 anos, betas)
