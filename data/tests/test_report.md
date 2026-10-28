# Relatório da suíte de testes automatizados

*Execução iniciada em 2026-10-28T17:19:17-03:00; relatório gerado em 2026-10-28T17:19:34. Base: `data/app/overview.json` de 2026-10-28T17:19:17; `data/model` mais recente de 2026-10-28T17:07:30. Comando: `bash tests/run_all.sh`.*

**4491 testes: 4428 aprovados, 51 falhas, 11 pulados e 1 falha conhecida (xfail).** Tolerância da paridade: 0,5% (mais meia unidade da 4ª casa arredondada no `overview.json`).

Das 51 falhas de teste, **37 são de empresas da cobertura**, 12 de outras empresas com dados em `data/hist` ou `data/market` e 2 são verificações globais.

**Paridade TS × Python:** `fairValue` a 25% 122/122; `irrImplied` 122/122; `irr3y` 122/122; upside do painel 122/122; `fairValue` em Ke 20% 122/122 e em Ke 30% 122/122 (aprovados/executados).

| Bloco | Testes | Aprovados | Falhas | Pulados | xfail |
|---|---:|---:|---:|---:|---:|
| Integridade CVM (`data/hist`) | 988 | 947 | 30 | 10 | 1 |
| Mercado (`data/market`) | 864 | 844 | 20 | 0 | 0 |
| Modelo (`data/model`, `data/app`) | 1416 | 1416 | 0 | 0 | 0 |
| Paridade do motor TS × Python | 1084 | 1082 | 1 | 1 | 0 |
| App: rotas com `next start` | 138 | 138 | 0 | 0 | 0 |
| `npx next build` | 1 | 1 | 0 | 0 | 0 |

`next build`: passou; 140 páginas estáticas geradas. Rotas: `next start -p 3300` com as 4 páginas gerais, as páginas `/empresa/{T}` da cobertura, os 8 relatórios `/relatorio/{T}`, `/api/quotes?t=RENT3` e `/api/market`; o servidor é encerrado ao fim pela porta 3300.

## Bugs e correções sugeridas

Em ordem de impacto. A linha de cada arquivo é localizada na hora a partir do trecho de código. Os testes **não alteram** nada fora de `tests/` e `data/tests/`.

### 1. Ações da CVM com escala misturada (unidades × milhares) entre arquivos: a escala é detectada só no último registro — severidade alta

- **Onde:** `pipeline/cvm.py` (trecho não encontrado; talvez já corrigido), `pipeline/market.py` (trecho não encontrado; talvez já corrigido)
- **Evidência:** 23 falhas; empresas: AUAU3, CASH3, CPLE3, DESK3, GGPS3, GOAU4, IGTI11, INTB3, IRBR3, LAVV3, LWSA3, ORVR3, PETR3, PETR4, PRIO3, SAUD3, SMFT3, SOJA3, VAMO3, VTRU3 (17 da cobertura). Exemplo: 1 problema(s): 2024-12-31→2025-03-31: 3,686,823 → 409,653,901 (×111.1)
- **Correção:** Detectar a escala registro a registro em `cvm.py`: comparar cada `total` com o da B3, ajustado pelos eventos entre as datas, ou com o vizinho, e multiplicar por 1.000 só os registros em milhares (tesouraria à parte). O efeito chega a `market.py` (`shares_at`): o valor de mercado histórico fica 1.000× menor, com P/L de 0,01–0,1x e DY de 500%+ nos múltiplos históricos e no `dps_history` de RENT3, BBDC4, TTEN3 e outros. Também afeta o sinal 'Sem emissão de ações' do Piotroski (`build.py`).

### 2. Reapresentação (DFP Y+1, PENÚLTIMO) substitui o ano mesmo quando vem zerada — severidade média

- **Onde:** `pipeline/cvm.py` (trecho não encontrado; talvez já corrigido)
- **Evidência:** 5 falhas; empresas: BBSE3, BRAP4, CXSE3, TIMS3 (4 da cobertura). Exemplo: 2 problema(s): FY2024: DRE zerada (receita, EBIT e lucro = 0); FY2025: DRE zerada (receita, EBIT e lucro = 0)
- **Correção:** Só trocar pela versão reapresentada se as contas-chave vierem preenchidas e diferentes de zero, por exemplo `abs(v(tab, '3.01')) > 0 and abs(v(tab, '3.11') or v(tab, '3.09')) > 0` no DRE. SBSP3 tem o FY2022 todo zerado, o que derruba o 4T22 para receita de −R$ 16,1 bi.

### 3. Beta em dias de crash estimado com só 8 a 15 observações (valores de −1,2 a 4,6 exibidos na página da empresa) — severidade baixa

- **Onde:** `pipeline/market.py:174`, `components/company/CompanyVal.tsx:367`
- **Evidência:** 1 falha; empresas: . Exemplo: 1 problema(s): sem beta diário de 2 anos
- **Correção:** Exigir pelo menos 30 dias de crash, ou encolher a estimativa na direção do `beta_down_3y` (shrinkage de Vasicek/Blume), e ocultar o número na página quando `n_crash_days` < 30.

### 4. Salto diário > 35% sem evento societário na série ajustada — severidade baixa

- **Onde:** `pipeline/market.py:154`
- **Evidência:** 9 falhas; empresas: BRAP4, CASH3, DASA3, HAPV3, POSI3, PRIO3, QUAL3, RANI3, USIM5 (4 da cobertura). Exemplo: 1 problema(s): 2021-12-17: -58.5% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- **Correção:** HAPV3 caiu 42,2% em 13/11/2025. É provavelmente um movimento real (resultado do 3T25), não um erro de ajuste. Convém registrar uma lista de eventos de mercado explicados no pipeline (ou uma nota em `research/`) para que `price_jumps_unexplained` traga só o que de fato precisa de revisão.

## Falhas por teste

### Integridade CVM (`data/hist`) · `test_historico_de_acoes_sem_quebra_de_escala` — 15 falha(s), 12 na cobertura

- **AUAU3**: 1 problema(s): 2024-12-31→2025-03-31: 3,686,823 → 409,653,901 (×111.1)
- **DESK3**: 1 problema(s): 2020-12-31→2021-12-31: 28,249,338 → 86,992,026 (×3.079)
- **GGPS3**: 1 problema(s): 2020-12-31→2021-12-31: 5,715,416 → 667,490,790 (×116.8)
- **IGTI11**: 1 problema(s): 2020-12-31→2021-12-31: 87,889,000 → 1,126,045,830 (×12.81)
- **INTB3**: 1 problema(s): 2020-12-31→2021-12-31: 28,161,111 → 327,611,110 (×11.63)
- **IRBR3**: 1 problema(s): 2022-09-30→2022-12-31: 2,467,890,332 → 82,263,012 (×0.03333)
- **ORVR3**: 1 problema(s): 2020-12-31→2021-12-31: 5,122,089 → 71,500,000 (×13.96)
- **PRIO3**: 1 problema(s): 2020-12-31→2021-12-31: 144,685,660 → 878,330,845 (×6.071)
- … e mais 7: SAUD3, SMFT3, VAMO3, VTRU3, CASH3, LAVV3, SOJA3

### Integridade CVM (`data/hist`) · `test_soma_4_trimestres_igual_ltm` — 5 falha(s), 4 na cobertura

- **BBSE3**: 2 problema(s): ebit: Σ25Q3+25Q4+26Q1+26Q2 = 4,844.1 × LTM 4,789.3 (+1.1%); ebitda: Σ25Q3+25Q4+26Q1+26Q2 = 4,845.5 × LTM 4,790.7 (+1.1%)
- **BPAC11**: 1 problema(s): revenue: Σ25Q3+25Q4+26Q1+26Q2 = 32,987.8 × LTM 31,200.7 (+5.7%)
- **KLBN11**: 1 problema(s): ni_controlling: Σ25Q3+25Q4+26Q1+26Q2 = 502.9 × LTM 594.5 (-15.4%)
- **SANB11**: 2 problema(s): ni_controlling: Σ25Q3+25Q4+26Q1+26Q2 = 13,840.9 × LTM 15,700.6 (-11.8%); net_income: Σ25Q3+25Q4+26Q1+26Q2 = 14,501.1 × LTM 15,929.6 (-9.0%)
- QUAL3 (fora da cobertura): 3 problema(s): revenue: Σ25Q3+25Q4+26Q1+26Q2 = 1,370.9 × LTM 1,350.8 (+1.5%); ebit: Σ25Q3+25Q4+26Q1+26Q2 = 298.0 × LTM 289.2 (+3.0%); ebitda: Σ25Q3+25Q4+26Q1+26Q2 = 550.2 × LTM 541.4 (+1.6%)

### Integridade CVM (`data/hist`) · `test_sinais_receita_positiva_e_da_nao_negativa` — 4 falha(s), 4 na cobertura

- **BBSE3**: 30 problema(s): FY2015: receita 0.00; FY2016: receita 0.00; FY2017: receita 0.00; FY2018: receita 0.00; FY2019: receita 0.00; FY2020: receita 0.00; FY2021: receita 0.00; FY2022: receita 0.00; FY2023: receita 0.00; FY2024: receita 0.00; FY2025: receita 0.00; 2022Q1: receita 0.00 … (+18)
- **BRAP4**: 30 problema(s): FY2015: receita 0.00; FY2016: receita 0.00; FY2017: receita 0.00; FY2018: receita 0.00; FY2019: receita 0.00; FY2020: receita 0.00; FY2021: receita 0.00; FY2022: receita 0.00; FY2023: receita 0.00; FY2024: receita 0.00; FY2025: receita 0.00; 2022Q1: receita 0.00 … (+18)
- **CXSE3**: 32 problema(s): FY2015: receita 0.00; FY2016: receita 0.00; FY2017: receita 0.00; FY2018: receita 0.00; FY2019: receita 0.00; FY2020: receita 0.00; FY2021: receita 0.00; FY2022: receita 0.00; FY2023: receita 0.00; FY2024: receita 0.00; FY2025: receita 0.00; 2022Q1: receita 0.00 … (+20)
- **TIMS3**: 11 problema(s): FY2024: receita 0.00; FY2025: receita 0.00; 2024Q1: receita 0.00; 2024Q2: receita 0.00; 2024Q3: receita 0.00; 2024Q4: receita 0.00; FY2024: ativo total 0.0; FY2025: ativo total 0.0; 2024Q1: ativo total 0.0; 2024Q2: ativo total 0.0; 2024Q3: ativo total 0.0

### Integridade CVM (`data/hist`) · `test_acoes_coerentes_com_b3` — 3 falha(s), 2 na cobertura

- **EGIE3**: 1 problema(s): B3/CVM (último ITR, escala 1.0) = 1.2399 (eventos B3 posteriores ×1): quantidade da B3 difere >10% da CVM 1,142,298,836
- **OPCT3**: 1 problema(s): B3/CVM (último ITR, escala 1.0) = 2.3730 (eventos B3 posteriores ×1): quantidade da B3 difere >10% da CVM 199,954,942
- LAVV3 (fora da cobertura): 1 problema(s): B3/CVM (último ITR, escala 1.0) = 0.1000 (eventos B3 posteriores ×1): quantidade da B3 difere >10% da CVM 1,954,343,520

### Integridade CVM (`data/hist`) · `test_ativo_igual_passivo_mais_pl` — 2 falha(s), 2 na cobertura

- **AURE3**: 1 problema(s): 2022Q2: ativo 29,391.4 × passivo+PL 26,627.3 (+9.4%)
- **FLRY3**: 1 problema(s): 2022Q3: ativo 6,784.0 × passivo+PL 6,601.4 (+2.7%)

### Integridade CVM (`data/hist`) · `test_sem_anos_ou_trimestres_faltantes` — 1 falha(s), 1 na cobertura

- **TIMS3**: 2 problema(s): FY2024: DRE zerada (receita, EBIT e lucro = 0); FY2025: DRE zerada (receita, EBIT e lucro = 0)

### Mercado (`data/market`) · `test_sem_saltos_diarios_nao_explicados` — 9 falha(s), 4 na cobertura

- **BRAP4**: 1 problema(s): 2021-12-17: -58.5% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- **HAPV3**: 1 problema(s): 2025-11-13: -42.2% (32.69 → 18.89)
- **PRIO3**: 2 problema(s): 2016-03-24: +83.7% (fora da janela de 3 anos, marcado pelo pipeline como não explicado); 2020-03-09: -36.5% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- **USIM5**: 1 problema(s): 2016-03-03: +35.1% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- CASH3 (fora da cobertura): 2 problema(s): 2024-09-03: -35.3% (6.58 → 4.26); 2021-09-10: -81.9% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- DASA3 (fora da cobertura): 1 problema(s): 2019-11-08: +38.5% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- POSI3 (fora da cobertura): 1 problema(s): 2016-08-10: +36.8% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- QUAL3 (fora da cobertura): 1 problema(s): 2019-08-09: +36.6% (fora da janela de 3 anos, marcado pelo pipeline como não explicado)
- … e mais 1: RANI3

### Mercado (`data/market`) · `test_multiplos_historicos_plausiveis` — 8 falha(s), 6 na cobertura

- **CPLE3**: 1 problema(s): valor de mercado 2021-11-30 152,152.4 → 2021-12-31 16,747.7 (×0.11)
- **GOAU4**: 1 problema(s): 6 meses com DY > 50% (ex.: 2022-04-30 50%)
- **IRBR3**: 3 problema(s): valor de mercado 2020-02-29 41,738.3 → 2020-03-31 12,151.2 (×0.291); valor de mercado 2022-11-30 1,841.5 → 2022-12-31 70.4 (×0.0382); valor de mercado 2023-02-28 51.5 → 2023-03-31 1,820.2 (×35.3)
- **LWSA3**: 1 problema(s): valor de mercado 2021-01-31 51,468.3 → 2021-02-28 14,490.9 (×0.282)
- **PETR3**: 1 problema(s): 4 meses com DY > 50% (ex.: 2023-03-31 56%)
- **PETR4**: 1 problema(s): 5 meses com DY > 50% (ex.: 2023-03-31 64%)
- CASH3 (fora da cobertura): 2 problema(s): valor de mercado 2021-08-31 5,143.3 → 2021-09-30 759.9 (×0.148); valor de mercado 2021-11-30 378.0 → 2021-12-31 2,596.3 (×6.87)
- LAVV3 (fora da cobertura): 1 problema(s): valor de mercado 2026-05-31 2,290.5 → 2026-06-30 22,435.9 (×9.8)

### Mercado (`data/market`) · `test_series_com_datas_ordenadas_e_precos_positivos` — 1 falha(s)

- test_series_com_datas_ordenadas_e_precos_positivos[quotes_val~fora]: 1 problema(s): daily_3y com 0 pregões

### Mercado (`data/market`) · `test_betas_plausiveis` — 1 falha(s)

- test_betas_plausiveis[quotes_val~fora]: 1 problema(s): sem beta diário de 2 anos

### Mercado (`data/market`) · `test_proventos_nao_negativos` — 1 falha(s), 1 na cobertura

- **RIAA3**: 1 problema(s): DY TTM 52%

### Paridade do motor TS × Python · `P(valor > preço) do painel (quantis) ≈ Monte Carlo do Python (±5 p.p.)` — 1 falha(s), 1 na cobertura

- **YDUQ3**: YDUQ3 probAbove(mc_q)=0.3613 × prob_mc=0.3092 (quantis vêm de 400 amostras das 5.000)

## Falhas conhecidas (xfail) e testes pulados

- pulado (1): CVCB3 — DDM(25%) por ação = -0.2445 ≤ 0 (lucro terminal negativo): não há preço positivo para a ida e volta
- pulado (10): ABCB4, BBAS3, BBDC3, BBDC4, BPAC11, BRSR6, ITUB3, ITUB4, PINE4, SANB11 — financeira: DL não se aplica
- xfail (1): HAPV3 — IFRS 17 no ITR 2026: 3.01 do 6M26 não é comparável ao DFP 2025; base sobrescrita em research/HAPV3.json (overrides)

## O que é testado

1. **Paridade TS × Python** (`tests/engine_parity.test.mjs`, motor transpilado em memória com o TypeScript local, sem tocar em `lib/`): `fairValue`, `irrImplied`, `irr3y` e o upside do painel contra o `overview.json` (Ke 25%, preço = `price_ref`) em todas as empresas da cobertura; `fairValue` em Ke 20% e 30% contra `pipeline/model.py` recalculado (`tests/pyref.py`, com `EAGORA_SNAPSHOT=1`, controladas das holdings reavaliadas no mesmo Ke). Coerência interna: TIR no preço do DDM devolve 25%, o valor justo não cresce com o Ke, `probAbove` é monotônica e as probabilidades dos quantis ficam a até 5 p.p. do Monte Carlo.
2. **CVM** (`tests/test_cvm_integrity.py`, 141 arquivos): ativo = passivo + PL (1%, também na conta 1 × conta 2 brutas), Σ 4 trimestres = LTM (1% + R$ 1 mi), ações = B3 (`supplement.json`, `totalNumberShares`), histórico de ações sem quebra de escala, DL = bruta − caixa + arrendamentos, receita > 0, D&A ≥ 0, sem anos ou trimestres faltantes e sem DRE zerada.
3. **Mercado** (`tests/test_market_integrity.py`): datas ordenadas e sem futuro, preços > 0, saltos diários > 35% só com evento societário, betas em [0; 3] (beta de crash em [−0,5; 3,5]), múltiplos históricos plausíveis, foto de cotações coerente e proventos ≥ 0 em `dividends.json`.
4. **Modelo** (`tests/test_model_outputs.py`): valor justo finito, pesos somando 1, TIR em [−50%; 300%] e fora dos limites da bisseção, projeções de 5 anos, Monte Carlo com p5 ≤ p10 ≤ … ≤ p95 e a base dentro de [p5; p95], DL/EBITDA projetada < 10x (salvo justificativa em `research/`), cenários e sensibilidade coerentes, `data/app` em dia com `data/model`, `data/model` reproduzível pelas premissas e oportunidades dentro da regra de seleção.
5. **App** (`tests/app_routes.test.mjs`): `next build`; HTTP 200 e HTML sem página de erro em todas as rotas; ticker fora da cobertura → 404; APIs com JSON válido e campos esperados.

Saídas brutas: `data/tests/raw/` (JUnit e logs do pytest, do node e do Next).
