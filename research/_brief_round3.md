# Briefing da 3ª rodada — ampliação da cobertura (28/10/2026)

Você é analista de ações (buy-side, padrão de fundo) num estudo de valuation pós-eleição. Leia antes, nesta ordem:
`research/_context.md` (o evento e os parâmetros), `docs/model-spec.md` (contrato entre premissas e motor),
`research/_TEMPLATE.json` (formato das premissas) e **dois exemplos prontos e revisados**: `research/TEND3.json` (industrial)
e `research/BBAS3.json` (banco). Para holdings veja `research/SIMH3.json`.

## O que mudou desde 26/10
- 26/10 fechou com Ibovespa −13,9% (176,6 mil). 27/10: 175,7 mil. 28/10 às 15h20: 170,9 mil (−2,7%), SMLL −4,8%.
- Dólar futuro R$ 5,38 (PTAX 28/10 5,342). Curva DI hoje: F27 13,63% · F28 14,46% · F29 14,91% · F31 15,17% · F33 15,25%.
  Selic 13,75%. O CDI implícito a termo para 2027–30 fica em ~14,5–15,5%: **é com ele que se calibra custo de dívida**.
- O valor final do estudo será recalculado pelo motor no **fechamento de 28/10**. Nos textos (`summary`, `thesis`,
  `election_impact`), não escreva valor justo, upside nem TIR (o motor calcula e o site mostra ao vivo); descreva drivers.
  Pode citar o preço de fechamento de 26/10 ou a queda do dia como fato histórico.

## Entregáveis por ticker (só estes arquivos)
1. `research/{TICKER}.json` — premissas completas no formato do template (todas as chaves; arrays de 5 anos 2026–2030).
2. `research/notes/{TICKER}.md` — dossiê de 40–90 linhas: negócio, histórico CVM 5 anos (receita, margem, lucro, ROE, DL/EBITDA),
   último trimestre, guidance, dívida, política de proventos, impacto da eleição, premissas e por quê, riscos, fontes.
3. Rode `EAGORA_SNAPSHOT=1 .venv/bin/python pipeline/model.py {TICKER}` (preço da foto de 26/10 13h02) e leia a saída:
   valor justo por método, TIR de dono, P(valor > preço). Se algo estiver absurdo, o erro quase sempre está na premissa.
Não edite nenhum outro arquivo (nem `_coverage.json`, nem o pipeline, nem dados). Não rode build, git nem servidor.

## Dados disponíveis
- `data/hist/{TICKER}.json`: CVM padronizada (anual 2015–2025, trimestral, LTM, balanço do último trimestre, ações).
  Confira `balance_date` e `ltm_label` (WEGE3, BBDC3 e SAUD3 já têm 3T26).
- `data/market/{TICKER}.json`: preços ajustados, betas, múltiplos históricos (`multiples_history`), proventos B3.
- Cotação ao vivo: `curl -s https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{TICKER}`.
- Pesquisa na web: release do 2T26 (ou 3T26, se já saiu), guidance, fatos relevantes, notícias de 26–28/10. Seja econômico:
  o essencial é o release mais recente, a dívida e a política de proventos.

## Checklist obrigatório (erros que a revisão independente achou na 1ª rodada — não repita)
1. **Custo da dívida** (`cost_of_net_debt`) coerente com a curva DI acima + spread da empresa; não deixe cair para 9–12% em 2030.
   Se a empresa tem caixa líquido, o "custo" vira rendimento do caixa (~CDI × (1 − IR)).
2. **Dívida líquida completa**: arrendamentos (IFRS-16), parcelamentos fiscais, aquisições a pagar, derivativos relevantes,
   dividendos/JCP declarados ainda não pagos, provisões tipo dívida (previdência, desmantelamento, contingências prováveis)
   → `adjustments.other_debt_like`, sem contar duas vezes o que a CVM já pôs na DL.
3. **Minoritários**: `minority_share_ni` coerente com o histórico da CVM (lucro dos não controladores / lucro total) e
   `minority_value` coerente com ele.
4. **`other_financial`** só para itens financeiros de verdade. Custo operacional (ex.: MDR de cartões, juros capitalizados que
   saem no CMV) vai na margem, senão infla o DCF.
5. **Ações**: confira `shares` em `data/hist` com a B3 (cancelamentos e bonificações depois do balanço). Bônus/conversíveis: ou
   ações diluídas + caixa do exercício, ou ações atuais — nunca as duas coisas.
6. **Proventos já com data-com no passado** não são fluxo de quem compra hoje: tire-os do 2026E ou trate como dívida, se ainda não pagos.
7. **Coluna 2026**: o motor usa só a fração do ano depois do balanço-base; a premissa de 2026 deve refletir o run-rate do 2S26,
   não a média de um 1S26 atípico.
8. **Múltiplos-alvo** na base certa (P/L sobre LPA 2027E, EV/EBITDA sobre EBITDA 2027E, mesmo conceito IFRS-16). Justifique
   com o histórico (`multiples_history`) e pares. Lembre que múltiplos de mercado embutem Ke de 11–15%, abaixo dos 25% do estudo.
9. **Commodities** (petróleo, minério, aço, celulose, grãos, alumínio): escreva o deck de preços e câmbio usado (US$ e R$),
   ancorado em curvas futuras/consenso, não em extrapolação. Exportadoras: o real fraco ajuda; diga quanto.
10. **Estatais e reguladas**: risco de intervenção/payout depois da reeleição (Petrobras, Cemig, Copasa, Sanepar, BB Seguridade…)
    entra nas premissas (payout, capex, margem) e no `bear`, não só no texto.
11. **Bancos e seguradoras**: `template: "financial"`, ROE sobre o PL contábil, payout realista, P/VP e P/L alvo.
12. **Holdings** (ITSA4, BRAP4, GOAU4): `template: "holding"`; controlada coberta no estudo → `method: "fair"`; senão `market`
    (ticker listado) ou `fixed` (fechada, com valor justificado). Informe dívida líquida e custo da holding.
13. `confidence` = "alta|média|baixa — motivo". Use "baixa" quando a base contábil for frágil ou o caso depender de um único driver.
14. Antes de entregar, compare o valor justo de cada método: se DCF, DDM e múltiplos divergirem mais de 2×, explique no dossiê
    ou corrija a premissa responsável.

## Resposta final (curta)
Para cada ticker: valor justo e TIR de dono que o motor deu (foto de 26/10), premissas-chave em 1 linha, confiança, e qualquer
dado que você não conseguiu verificar.
