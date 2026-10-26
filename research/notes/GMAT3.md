# GMAT3 — Grupo Mateus · dossiê G05 · 26/10/2026

**Preço:** R$ 3,54 às 11h55 (−33%; sexta R$ 5,30) · mkt cap ~R$ 8,2 bi · 2.302,3 mi ações · ADTV 3m R$ 30 mi
**Veredito (Ke 25%):** **armadilha (micro antes do macro).** O problema é anterior à eleição: SSS −8%, margem e lucro em queda e reapresentação contábil de estoques. TIR implícita ~13,5% (≈11% pré-eleição). Valor justo do motor R$ 1,5 (DCF R$ 0,6; DDM R$ 1,4; múltiplos R$ 3,7). ROE de só ~9–10% com PL de R$ 11,2 bi.

## Negócio
- Multiformato no Norte/Nordeste: **313 unidades** (234 de varejo alimentar: 144 atacarejos Mix Mateus/Novo Atacarejo, 90 supermercados; 78 Eletro Mateus; 1 farmácia Mix Toureiro Farma), 18 CDs, atacado B2B para ~48 mil clientes/mês (6.993 representantes, 1.861 municípios).
- Aquisição do **Novo Atacarejo** (PE/PB/AL) consolidada desde o 3T25 (não controladores R$ 1.160,6 mi no PL); margem EBITDA da operação de só 5,1% no 2T26 vs 7,5% no resto.
- Controlador: Ilson Mateus.

## 2T26 (release 13/08/2026; IFRS-16)
| Item | 2T26 | a/a |
|---|---|---|
| Receita líquida | R$ 9.852 mi | +12,2% (consolidação); **SSS −8,0%** (1S26 −7,7%) |
| Margem bruta | 23,5% | −0,3 p.p. (+0,6 p.p. t/t) |
| Despesas operacionais | 16,4% da RL | +1,4 p.p. (−1,0 p.p. t/t) |
| EBITDA IFRS-16 | R$ 681,6 mi (6,9%) | −12,1% (8,8% no 2T25) |
| EBITDA pré-IFRS16 | R$ 523,5 mi (5,3%) | −21,1% |
| Lucro líquido controlador | R$ 236,8 mi | **−39,3%** |
| DL ex-arrendamentos / EBITDA pré-IFRS16 | R$ 1.093 mi / 0,51x | +R$ 357 mi t/t (estoques p/ aniversário) |
| Capex | R$ 162 mi | −36,5% ("rigor diante do patamar de juros") |
| Ciclo de caixa | 42 dias | −15 dias a/a; estoques 67 dias |

SSS negativo: consumo fraco/endividamento + redução deliberada do canal **Balcão** nos atacarejos (desde 1T26) — base normaliza a partir do 1T27.
Antecipação de recebíveis de R$ 360,6 mi pelo Novo Mateus em jun/26 (tratada como debt-like).

## Reapresentação contábil e impostos
- **Nota 3.1 do ITR:** "revisou sua política contábil de apuração dos estoques e do CMV" (divulgado no 3T25), reapresentando 2T25/6M25 (estoques, CMV, tributos diferidos); auditoria (Forvis Mazars) sem ressalva. Contexto de mercado/valores do ajuste original não verificados (busca web esgotada).
- IR efetivo baixo: exclusão de subvenções de ICMS (R$ 212,6 mi no 1S26) amparada em liminar/jurisprudência contra a Lei 14.789/23; reversão de provisão inflou o lucro de 2025 (IR +R$ 512 mi; LL 2025 R$ 1.833 mi). Risco judicial + fim dos incentivos de ICMS na reforma (2029–32).

## Histórico (CVM, IFRS-16)
- RL: 12,4 (2020) → 15,9 → 21,8 → 26,8 → 32,1 → 38,4 bi (CAGR 25,4%).
- Margem EBITDA: 7,4% (21), 7,8%, 7,6%, 7,4%, 7,3%. Lucro: 759 → 1.052 → 1.221 → 1.276 → 1.833 mi. ROE médio 15%. Payout de caixa ~0–8% (JCP R$ 339 mi de dez/25 virou aumento de capital).

## ⚠️ Problema de dado (pipeline CVM)
`balance.leases = 0`: o passivo de arrendamento está em **2.01.05.02.05 (R$ 250,9 mi) e 2.02.02.02.03 (R$ 3.908,6 mi)**. DL correta incl. arrendamentos = R$ 1.092,8 + 4.159,4 = **R$ 5.252 mi** (≈2,0x EBITDA LTM) — usado via `overrides.base.net_debt`.

## Dívida
Dívida bruta R$ 2.724 mi (empréstimos 1.285 + debêntures 846 + "financiamento por arrendamento" 594), **R$ 1.530 mi no curto prazo**; indexador/custo não verificados. Exposição líquida a CDI pequena (~R$ 1,45 bi) → +100 bp ≈ −R$ 13 mi no lucro (~1%).

## O que um 4º mandato de Lula muda
Maior exposição do grupo à renda do Norte/Nordeste (Bolsa Família, salário mínimo, isenção de IR) — positivo para volume; crédito caro ao pequeno varejista (B2B) e inflação de alimentos — negativos. Juros pesam pouco no lucro (balanço leve); queda de hoje é beta/fluxo de small cap.

## Premissas do modelo (research/GMAT3.json)
- RL +5% (26) → 7/8/8/7% (histórico de 25% descartado: capex de expansão cortado, SSS negativo).
- Margem EBITDA IFRS-16 6,6% → 7,2% (2029). D&A 1,75%. Capex 2,8–3,3% (caixa + adições de direito de uso ~0,9%). Capital de giro 10% do Δ receita.
- Custo DL incl. arrendamentos 12–12,5% + R$ 320–400 mi/ano de outros encargos (AVP/antecipações). IR 8% → 18%. Payout 25–35%. Minoritários 2% do lucro.
- g 5%, ROIC_T 12%, ROE_T 14%, WACC 20,5% (wd 30%).
- Saídas: LL 0,93 bi (26) → 1,55 bi (30); ROE 8% → 10%; DL/EBITDA 2,0x → 1,5x.

## Fontes
- Release 2T26: https://api.mziq.com/mzfilemanager/v2/d/8ea287f8-ae0a-4b88-b20b-80c1f1b86a1e/759380ab-906c-cfb2-3d52-43e262f436d1?origin=2
- ITR 2T26: https://api.mziq.com/mzfilemanager/v2/d/8ea287f8-ae0a-4b88-b20b-80c1f1b86a1e/bd4a2608-b719-c378-c9e6-048e239d0bab?origin=2
- CVM padronizado: data/hist/GMAT3.json
