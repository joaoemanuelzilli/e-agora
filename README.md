# E agora? Valuation pós-eleição (26/10/2026)

Estudo de valuation das 59 ações brasileiras líquidas que caíram 20% ou mais no pregão seguinte à reeleição de Lula, com painel ao vivo.

- **Painel:** preço de hoje contra valor justo, TIR de dono contra Ke de 25%, ranking multifator e as melhores oportunidades.
- **Empresa (59 páginas):** histórico CVM 2015–2025, projeções 2026–2030, DCF, DDM, múltiplos, sensibilidades, cenários, Monte Carlo, múltiplos históricos, dividendos, fatores quant, tese, riscos e dossiê.
- **Relatórios:** nota detalhada para cada oportunidade selecionada, com motivos, embasamento estatístico, riscos e gatilhos.
- **Mercado:** event study de crashes e eleições desde 1998, regressão cross-section da queda, curva DI ao vivo.

## Dados

| Fonte | Uso |
|---|---|
| CVM (dados abertos DFP/ITR) | Demonstrações padronizadas, ações, dividendos pagos |
| B3 (cotacao.b3.com.br, listados, COTAHIST) | Cotações ao vivo, histórico diário, proventos, eventos, índices, DI futuro |
| Banco Central (SGS, Focus) | Selic, CDI, IPCA, PTAX, expectativas |
| Releases e RI das companhias | Premissas e contexto qualitativo (ver `research/notes/`) |

As cotações do painel são buscadas a cada 30 segundos em `/api/quotes` (B3 primeiro; Yahoo e brapi como reserva, esta com `BRAPI_TOKEN` opcional) e os indicadores em `/api/market`. Todo o valuation dependente de preço (upside, TIR, probabilidade) é recalculado no navegador com o mesmo motor do estudo (`lib/valuation.ts`, espelho de `pipeline/model.py`).

## Estrutura

```
pipeline/   Python: coleta (B3, CVM), padronização, mercado/quant, motor de valuation, montagem do app
research/   Premissas por empresa (JSON), dossiês (notes/) e relatórios das oportunidades (reports/)
data/       hist (CVM), market (B3), model (valuation), app (dados consumidos pelo site)
docs/       Especificação do modelo
app/        Next.js (páginas e rotas de API ao vivo)
components/ Gráficos SVG e seções das páginas
lib/        Motor TS, formatação, fontes ao vivo
```

## Rodar

```bash
# app
npm install
npm run dev

# pipeline (Python 3.12)
uv venv .venv && uv pip install --python .venv/bin/python pandas numpy scipy requests
python pipeline/fetch_universe.py <dir_b3> <universe.json>
python pipeline/cvm.py <dir_cvm> <fca_vm.csv> <universe.json> research/_coverage.json <out_hist> <supplement.json>
python pipeline/market.py <cotahist.csv.gz> <dir_b3> <universe.json>
EAGORA_SNAPSHOT=1 python pipeline/model.py --all
python pipeline/build.py
```

Ke = 25% a.a. (meta do estudo). Estudo quantitativo com finalidade informativa; não é recomendação de investimento.
