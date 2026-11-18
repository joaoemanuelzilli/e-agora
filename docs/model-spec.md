# Especificação do modelo de valuation (contrato entre pesquisa e motor)

O motor (`pipeline/model.py`) lê `research/{TICKER}.json` (premissas) + `data/hist/{TICKER}.json` (CVM)
e gera projeções, valuation, TIR e Monte Carlo. As premissas são **drivers**; o motor calcula as linhas.

## Convenções
- R$ milhões nominais. Ano-base contábil: FY2025 (real). Projeção explícita: 2026E–2030E. Perpetuidade a partir de 2031.
- Data de avaliação: 2026-10-28, a mesma da foto de preços. Balanço-base: último trimestre arquivado na CVM
  (2T26 = 2026-06-30, ou 3T26 se já saiu). Desconto em meio de período.
- **Ponte até a data de avaliação** (revisão de 17/11/2026). O stub de 2026 (balanço-base → 31/12) é dividido em dois:
  a parte já decorrida até a data de avaliação não é fluxo futuro do comprador. O caixa gerado nesse intervalo, líquido de
  juros, impostos e proventos pagos, ajusta a dívida líquida (`nd_val`) e o patrimônio (`eq_val`) pela mesma identidade de
  caixa da projeção; só a parte posterior (`f_fwd`) entra no DCF, no DDM e na TIR, descontada no meio do período restante.
  Hipótese: fluxos uniformes dentro do stub. A convenção anterior descontava o stub inteiro com prazo negativo
  (−0,07 ano para balanço de 30/06) e contava para o comprador proventos de antes da compra; o efeito medido está em
  `data/tests/decision_checks.md`, seção 5.
- **Ke = 25%**. Kd = custo marginal da dívida pré-IR (ex.: CDI + spread). IR estatutário 34% para o benefício fiscal da dívida.
- **EBITDA = EBIT (conta CVM 3.05) + D&A (DVA 7.04.01)** → base IFRS-16 (depreciação de direito de uso dentro do D&A).
- **Dívida líquida (DL) = empréstimos/financiamentos/debêntures (2.01.04 + 2.02.01) + passivo de arrendamento IFRS-16
  − caixa (1.01.01) − aplicações financeiras (CP + LP)**. Itens "debt-like" extras (aquisições a pagar, parcelamentos fiscais,
  derivativos relevantes) → `adjustments.other_debt_like`. Ativos não operacionais (participações não consolidadas,
  créditos fiscais monetizáveis, imóveis não operacionais) → `adjustments.non_operating_assets`.
- Receita = receita líquida (3.01). Lucro = lucro atribuído aos controladores (3.11.01).

## Template `industrial` (padrão)
Para t = 2026…2030 (arrays de 5 posições nas premissas):
```
Receita_t   = Receita_{t-1} × (1 + revenue_growth_t)          (Receita_2025 = FY2025 CVM, ou overrides.base.revenue_2025)
EBITDA_t    = Receita_t × ebitda_margin_t
D&A_t       = Receita_t × da_pct_revenue_t
EBIT_t      = EBITDA_t − D&A_t
ResFin_t    = −cost_of_net_debt_t × DL_{t-1} + other_financial_t (R$ mi; equivalência patrimonial pode entrar aqui)
LAIR_t      = EBIT_t + ResFin_t
IR_t        = max(0, LAIR_t) × tax_rate_t                      (alíquota efetiva; JCP reduz)
LL_t        = LAIR_t − IR_t ; LL_controlador_t = LL_t × (1 − minority_share_ni)
Capex_t     = Receita_t × capex_pct_revenue_t                  (investimento LÍQUIDO; ver notas setoriais)
ΔCG_t       = nwc_pct_revenue × (Receita_t − Receita_{t-1})
FCFF_t      = EBIT_t × (1 − tax_rate_t) + D&A_t − Capex_t − ΔCG_t
Div_t       = LL_controlador_t × payout_t   (recompras: inclua no payout; buyback_mn só afeta DL e PL, não o DDM)
DL_t        = DL_{t-1} − (EBITDA_t − IR_t + ResFin_t − Capex_t − ΔCG_t) + Div_t + buyback_mn_t − equity_issuance_mn_t
PL_t        = PL_{t-1} + LL_controlador_t − Div_t − buyback_mn_t + equity_issuance_mn_t
ROE_t       = LL_controlador_t / média(PL) ; ROIC_t = EBIT_t(1−t) / média(PL + DL)
```
- WACC = we·Ke + wd·Kd·(1−34%), com `wacc.target_debt_weight` (wd). Se omitido: DL/(DL + valor de mercado pré-eleição), limitado a [0; 0,6].
- Perpetuidade FCFF (value driver): `TV = NOPAT_2030 × (1+g) × (1 − g/ROIC_T) / (WACC − g)`, com `terminal.roic`.
- Equity DCF = EV − DL_base − minoritários (valor contábil, ou `adjustments.minority_value`) + non_operating_assets − other_debt_like.
- DDM/FCFE: Σ Div_t descontado a Ke + `TV_eq = LL_2030 × (1+g) × (1 − g/ROE_T) / (Ke − g)` com `terminal.roe`.

### Notas setoriais (industrial)
- **Locadoras (RENT3, MOVI3, VAMO3)**: receita CVM inclui venda de seminovos e o custo inclui o valor contábil dos carros
  vendidos (não caixa). Logo `capex_pct_revenue` = (compra bruta de frota − valor contábil dos carros vendidos + outros capex) / receita
  total, i.e., crescimento líquido de frota + depreciação. D&A = depreciação de frota + outros.
- **Incorporadoras**: terreno/estoque e recebíveis são capital de giro → `nwc_pct_revenue` alto (tipicamente 0,6–1,5); capex baixo.
- **Concessões/utilities**: investimento em ativo de contrato/intangível de concessão entra em `capex_pct_revenue`, mesmo que a DFC
  o classifique como operacional. Receita de construção (ICPC 01/IFRS 15) pode ser excluída: use `overrides.base.revenue_2025`
  e explique em `overrides.notes`.
- **Varejo**: arrendamentos são dívida (DL inclui IFRS-16); margem EBITDA no conceito IFRS-16.

## Template `financial` (bancos)
```
LL_t  = ROE_t × PL_{t-1}  (ou LL_{t-1} × (1+ni_growth_t) se informado)
Div_t = LL_t × payout_t ;  PL_t = PL_{t-1} + LL_t − Div_t
```
Valor = DDM (Ke) com `TV_eq = LL_2030 (1+g)(1 − g/ROE_T)/(Ke − g)`; P/VP justo = (ROE_T − g)/(Ke − g); múltiplos alvo.

## Template `holding` (SOTP)
Lista `sotp.components[]`: `{name, ticker|null, stake, method: "fair"|"market"|"fixed", value_mn}`.
- `fair`: usa o valor justo do motor para o ticker coberto (participação × equity value justo).
- `market`: participação × valor de mercado ao vivo do ticker.
- `fixed`: `value_mn` (100% da empresa) justificado nas premissas.
Valor = Σ componentes − dívida líquida da holding − custo de holding capitalizado (`sotp.holding_cost_mn / (Ke − g)`).

## Métodos e pesos (valor justo final)
| Template | DCF-FCFF | DDM/FCFE | Múltiplos | Notas |
|---|---|---|---|---|
| industrial | 50% | 25% | 25% | múltiplos = média de P/L alvo×LPA 2027E e EV/EBITDA alvo×EBITDA 2027E |
| financial | — | 50% | 50% | múltiplos = média de P/L alvo e P/VP alvo; P/VP justo (Gordon) entra no DDM como checagem |
| bancos (`_BANKS` e premissas com `valuation_weights`) | — | 60% | 40% | só P/VP alvo; vale para 10 das 14 financeiras da cobertura |
| incorporadoras (`_HOMEBUILDERS`) | 20% | 50% | 30% | só P/L alvo: o caixa oscila com terrenos e recebíveis |
| holding | SOTP 100% | — | — | desconto de holding mostrado |
Referências (não entram no blend): Graham (√22,5·LPA·VPA), Bazin (DPA/6%), DCF reverso (crescimento implícito no preço).
Pesos podem ser sobrescritos via `valuation_weights` com justificativa.

## TIR de dono
- **TIR implícita (inteira)**: taxa r que iguala o preço de hoje ao valor presente de todos os dividendos projetados + perpetuidade
  (equity value driver). Comparada com Ke 25%. Só entram dividendos posteriores à data de avaliação.
- **Preço-teto**: o menor entre o DDM a Ke (preço em que a TIR de dono = Ke) e o valor justo. É o critério de compra
  da regra v2 (`docs/regra-de-decisao.md`); o valor justo do blend mistura métodos que embutem retornos diferentes.
- **TIR 3 anos**: compra hoje, recebe os dividendos posteriores à data de avaliação (stub restante de 2026E até 2028E) e vende ao fim de 2028 ao múltiplo alvo P/L × LPA 2029E.
- Retorno 3 anos de ROE: ROE projetado 2026E–2028E e dividend yield sobre o preço atual.

## Cenários e Monte Carlo
- `scenarios.bear` / `scenarios.bull`: deslocamentos aditivos nos drivers (`revenue_growth_shift`, `ebitda_margin_shift`,
  `terminal_g_shift`, `capex_pct_shift`) e `probability` (base = 1 − bear − bull).
- `uncertainty` (desvios-padrão anuais) para 5.000 simulações: `revenue_growth_sd`, `ebitda_margin_sd`, `terminal_g_sd`,
  `capex_pct_sd`; correlação crescimento×margem fixa em 0,5.
