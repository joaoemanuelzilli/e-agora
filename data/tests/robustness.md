# Robustez do valuation: pesos do blend e premissas (26/10/2026)

Gerado em 2026-10-28T17:19:06 por `pipeline/tests/robustness.py`, com o motor `pipeline/model.py` sem alteração e a foto de preços `data/market/quotes.json`. São 122 empresas (5 holdings por SOTP). Ke base de 25%. Dados para gráfico: `data/tests/robustness.json`.

## Resumo

- **A TIR implícita não depende dos pesos, do Ke nem dos múltiplos.** Ela é a taxa que zera o DDM ao preço de hoje, então só muda com g, margem, crescimento, Kd e Monte Carlo. O ranking por TIR é estável: Spearman mediano de 0,93 (mínimo 0,76) na amostra conjunta de 3.000 combinações.
- **No ranking por upside, a ordem geral resiste aos pesos, mas o topo não.** Nas 66 combinações de pesos, o Spearman mediano é 0,91 (mínimo 0,78), porém só 78% do top 7 por upside se mantém em média. Na amostra conjunta, o Spearman mediano é 0,85 (mínimo 0,53). Causa: na mediana, os múltiplos-alvo valem 2,30× o DDM a Ke 25%, e 33 empresas têm DCF negativo, que o motor trunca em zero sem tirar o peso.
- **Lista robusta por TIR** (top 7 na amostra conjunta): ≥ 80%: MDNE3, PLPL3, TEND3, VTRU3; ≥ 50%: MDNE3, PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3.
- **Lista robusta por upside** (top 7 na amostra conjunta): ≥ 80%: VTRU3, TEND3; ≥ 50%: VTRU3, TEND3, PLPL3, SEER3, BEEF3, HAPV3.
- **Núcleo robusto** (top 7 por TIR e por upside em ≥ 50% da amostra conjunta): PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3. Em todas as grades ao mesmo tempo (≥ 50% em cada uma): TIR PLPL3; upside BEEF3.
- **As 7 oportunidades atuais (VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3, CEAB3, COGN3) dependem dos pesos e já das revisões.** Com as premissas revisadas e os pesos atuais, a regra do `build.py` seleciona 7 (BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3). Nos 66 vetores de pesos (upside, P(MC) e escore recalculados), a regra mantém em média 6,3 das 7 (mínimo 5) e a lista sai idêntica em 0%. Fração de vetores com cada empresa selecionada: VTRU3 100%; BEEF3 100%; SEER3 85% (w_múlt entre 0,0 e 1,0, irregular; w_DCF ≥ 0,1); MDNE3 95% (qualquer w_múlt; w_DCF ≤ 0,9); PLPL3 97% (w_múlt ≤ 0,9; qualquer w_DCF); TEND3 56% (w_múlt ≤ 0,3; w_DCF ≥ 0,3); CEAB3 62% (w_múlt ≥ 0,2; w_DCF ≤ 0,5); COGN3 36% (w_múlt ≤ 0,1; w_DCF ≥ 0,5).
- **Pesos propostos por setor:** o Spearman do upside contra a base fica em 0,93 e o do escore em 0,99. A regra passa a selecionar BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3, contra BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3 hoje. O peso dos múltiplos no varejo decide a cauda da lista: varejo DDM 60 / Múlt 20 / DCF 20: BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3; varejo DDM 50 / Múlt 30 / DCF 20 (proposta): BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3; varejo DDM 40 / Múlt 40 / DCF 20: BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3.

## Base e reprodução

A base é o motor rodado agora com as premissas atuais. Ele reproduz o `overview.json` (2026-10-28T17:08:17) em valor justo e TIR, exceto em 0 empresas cujas premissas (ou cuja controlada) mudaram depois do build: nenhuma. A P(MC) difere da do app em 11 empresas sem mudança no valor justo (revisão de desvios em `uncertainty`): CYRE3 49,4% → 39,3%, MDNE3 79,4% → 65,0%, MRVE3 18,1% → 43,7%, PLPL3 82,3% → 89,4%, DIRR3 49,3% → 54,4%, CURY3 23,2% → 22,9%, TEND3 79,1% → 90,4%, BBAS3 28,7% → 38,7%, BBDC4 1,1% → 16,4%, BRSR6 10,2% → 25,5%, BBDC3 14,8% → 47,6%. Com as premissas atuais, a regra de oportunidades seleciona BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3.

Top 7 da base por TIR: HAPV3, PLPL3, MDNE3, BEEF3, VTRU3, TEND3, COGN3. Top 7 por upside: BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3.

## Estabilidade do ranking por grade

Spearman de cada combinação contra a base (mediana / mínimo), fração média do top 7 da base que continua no top 7 e número médio de oportunidades atuais que a regra mantém (de 7).

| Grade | Combinações | Spearman TIR | Spearman upside | Spearman escore | Top 7 TIR mantido | Top 7 upside mantido | Oportunidades mantidas |
|---|---:|---|---|---|---:|---:|---:|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | 66 | 1,00 / 1,00 (invariante) | 0,91 / 0,78 | 0,99 / 0,96 | 100% | 78% | 6,3 |
| Ke 20–30% (passo 1 p.p.) | 11 | 1,00 / 1,00 (invariante) | 0,99 / 0,96 | 1,00 / 1,00 | 100% | 83% | 6,7 |
| g terminal −2 a +2 p.p. | 5 | 1,00 / 0,99 | 1,00 / 1,00 | 1,00 / 0,99 | 100% | 94% | 7,0 |
| Múltiplos-alvo −30% a +30% | 7 | 1,00 / 1,00 (invariante) | 0,99 / 0,96 | 1,00 / 0,99 | 100% | 86% | 6,9 |
| Margem EBITDA × crescimento ±2 p.p. | 25 | 0,97 / 0,87 | 0,95 / 0,85 | 0,98 / 0,91 | 79% | 78% | 5,9 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | 3 | 0,93 / 0,93 | 0,99 / 0,98 | 0,97 / 0,96 | 81% | 90% | 7,0 |
| Monte Carlo com desvios ×1,5 | 2000 | 0,74 / 0,52 | 0,73 / 0,52 | — | 43% | 39% | — |
| Amostra conjunta de todas as grades | 3000 | 0,93 / 0,76 | 0,85 / 0,53 | — | 76% | 63% | — |

Na amostra conjunta e no MC ×1,5, o escore e a regra não são recalculados, porque exigiriam um Monte Carlo por combinação. Nas grades determinísticas, P(MC) é recalculada com o Monte Carlo do motor (5.000 sorteios, semente 7).

## Frequência no top 7 e no top 15 por empresa

Frequências na amostra conjunta (C), na grade de pesos (P) e no Monte Carlo ×1,5 (MC). A faixa p5–p95 do valor justo é a da amostra conjunta. A tabela lista as empresas que aparecem no top 15 da base ou em pelo menos 5% das combinações; as demais estão no JSON.

| Empresa | Preço | VJ base | VJ p5–p95 (C) | TIR base (rank) | Upside base (rank) | Top 7 TIR C | Top 15 TIR C | Top 7 TIR MC | Top 7 upside C | Top 15 upside C | Top 7 upside P | Top 7 upside MC | Regra (pesos) |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TEND3 ★ | 21,22 | 26,81 | 19,91–39,25 | 25,4% (6) | 26% (5) | 96% | 100% | 39% | 81% | 97% | 80% | 36% | 56% |
| VTRU3 ★ | 11,98 | 16,99 | 11,40–23,41 | 26,3% (5) | 42% (2) | 84% | 100% | 37% | 89% | 100% | 100% | 47% | 100% |
| PLPL3 ★ | 4,84 | 6,37 | 4,40–9,32 | 28,3% (2) | 32% (3) | 100% | 100% | 50% | 76% | 91% | 74% | 40% | 97% |
| MDNE3 ★ | 16,86 | 20,19 | 14,04–25,96 | 27,8% (3) | 20% (6) | 100% | 100% | 47% | 41% | 84% | 32% | 27% | 95% |
| SEER3 ★ | 11,03 | 14,19 | 9,28–19,91 | 24,4% (8) | 29% (4) | 60% | 100% | 26% | 69% | 100% | 82% | 35% | 85% |
| HAPV3 | 4,21 | 4,82 | 0,36–14,03 | 29,3% (1) | 14% (8) | 69% | 82% | 49% | 53% | 62% | 74% | 42% | 0% |
| BEEF3 ★ | 2,87 | 5,44 | 0,21–11,60 | 27,2% (4) | 89% (1) | 53% | 59% | 48% | 66% | 73% | 100% | 61% | 100% |
| COGN3 ★ | 1,69 | 1,97 | 1,10–3,11 | 24,6% (7) | 17% (7) | 29% | 100% | 31% | 22% | 93% | 76% | 31% | 36% |
| PINE4 | 10,66 | 9,45 | 7,67–13,37 | 22,7% (13) | -11% (19) | 28% | 92% | 21% | 4% | 45% | 0% | 3% | 0% |
| CYRE3 | 17,74 | 17,76 | 12,65–24,23 | 22,9% (11) | 0% (14) | 20% | 99% | 17% | 3% | 54% | 0% | 6% | 0% |
| CEAB3 ★ | 6,87 | 6,91 | 2,94–13,73 | 22,1% (15) | 1% (13) | 0% | 81% | 24% | 25% | 67% | 30% | 26% | 62% |
| DIRR3 | 8,60 | 8,59 | 6,40–12,28 | 22,1% (14) | -0% (15) | 8% | 77% | 15% | 12% | 67% | 0% | 8% | 3% |
| SBFG3 | 5,08 | 3,52 | 0,83–10,71 | 23,2% (9) | -31% (38) | 26% | 57% | 31% | 19% | 37% | 20% | 19% | 26% |
| PGMN3 | 2,63 | 2,27 | 0,20–5,98 | 20,9% (17) | -14% (22) | 19% | 40% | 16% | 28% | 43% | 11% | 18% | 0% |
| POMO4 | 3,89 | 3,96 | 2,83–5,74 | 21,7% (16) | 2% (11) | 0% | 78% | 20% | 2% | 77% | 0% | 15% | 0% |
| EZTC3 | 9,59 | 10,69 | 6,95–14,83 | 17,4% (29) | 12% (9) | 0% | 4% | 1% | 32% | 70% | 14% | 4% | 0% |
| ANIM3 | 2,43 | 2,54 | 0,36–5,22 | 22,9% (12) | 4% (10) | 1% | 54% | 24% | 19% | 42% | 0% | 35% | 0% |
| MOVI3 | 6,62 | 4,19 | 0,17–13,59 | 23,1% (10) | -37% (46) | 8% | 38% | 34% | 13% | 26% | 3% | 29% | 0% |
| LREN3 | 9,31 | 8,79 | 5,51–15,61 | 20,5% (19) | -6% (16) | 0% | 19% | 10% | 8% | 62% | 0% | 6% | 38% |
| CSAN3 | 2,37 | 2,10 | 1,52–3,48 | — (—) | -11% (20) | — | — | — | 13% | 42% | 0% | 0% | 0% |
| CURY3 | 26,37 | 22,89 | 17,29–31,63 | 19,9% (20) | -13% (21) | 0% | 33% | 10% | 0% | 24% | 0% | 4% | 0% |
| BBAS3 | 16,84 | 15,67 | 10,11–21,26 | 20,6% (18) | -7% (17) | 0% | 43% | 8% | 0% | 8% | 0% | 2% | 0% |
| BBDC3 | 13,40 | 12,37 | 8,49–17,31 | 19,8% (21) | -8% (18) | 0% | 22% | 2% | 0% | 22% | 0% | 0% | 0% |
| SIMH3 | 5,24 | 2,26 | -1,08–10,81 | — (—) | -57% (75) | — | — | — | 10% | 18% | 0% | 19% | 0% |
| MRVE3 | 4,27 | 2,34 | 0,86–7,04 | 12,8% (68) | -45% (59) | 0% | 0% | 7% | 5% | 24% | 5% | 13% | 0% |
| RAPT4 | 3,67 | 1,92 | 0,24–6,85 | 15,7% (35) | -48% (63) | 0% | 0% | 9% | 5% | 14% | 0% | 16% | 0% |
| LWSA3 | 3,41 | 2,82 | 1,82–4,70 | 14,7% (44) | -17% (25) | 0% | 0% | 0% | 1% | 17% | 0% | 1% | 0% |
| ECOR3 | 5,27 | 2,15 | 0,00–8,90 | 17,6% (27) | -59% (80) | 0% | 2% | 8% | 5% | 9% | 0% | 0% | 0% |
| BRSR6 | 12,94 | 10,91 | 7,30–15,22 | 19,5% (23) | -16% (23) | 0% | 12% | 8% | 0% | 1% | 0% | 1% | 0% |
| YDUQ3 | 8,76 | 7,10 | 2,77–12,55 | 19,6% (22) | -19% (27) | 0% | 3% | 16% | 1% | 8% | 0% | 15% | 0% |
| RIAA3 | 6,33 | 4,67 | 1,68–9,97 | 17,5% (28) | -26% (33) | 0% | 0% | 8% | 0% | 8% | 0% | 11% | 0% |
| DESK3 | 19,32 | 19,46 | 1,43–19,34 | 10,5% (92) | 1% (12) | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |

★ = oportunidade atual. A coluna “Regra (pesos)” dá a fração das 66 combinações de pesos em que a regra do app (TIR ≥ 20%, P(MC) ≥ 45%, Altman fora de risco, confiança não baixa, ordem pelo escore) põe a empresa entre as 7.

### Faixa p5–p95 do valor justo por grade (todas as empresas)

| Empresa | Preço | VJ base | Pesos | Ke | g | Múltiplos | Margem × cresc. | Kd | MC ×1,5 | Conjunta |
|---|---:|---:|---|---|---|---|---|---|---|---|
| BEEF3 | 2,87 | 5,44 | 3,78–6,17 | 4,01–7,58 | 5,35–5,47 | 4,64–6,24 | 0,86–10,84 | 4,40–4,94 | 0,37–15,17 | 0,21–11,60 |
| VTRU3 | 11,98 | 16,99 | 13,96–19,15 | 14,35–21,07 | 16,96–16,99 | 15,35–18,63 | 14,62–19,49 | 16,38–16,68 | 8,79–28,31 | 11,40–23,41 |
| PLPL3 | 4,84 | 6,37 | 5,91–7,30 | 5,47–7,81 | 6,35–6,38 | 5,84–6,91 | 5,10–7,71 | 6,32–6,35 | 2,89–11,74 | 4,40–9,32 |
| SEER3 | 11,03 | 14,19 | 11,48–16,68 | 12,06–17,46 | 14,01–14,30 | 12,73–15,66 | 11,84–16,69 | 13,56–13,87 | 7,23–23,24 | 9,28–19,91 |
| TEND3 | 21,22 | 26,81 | 23,66–32,31 | 23,63–31,85 | 26,71–26,90 | 24,28–29,35 | 22,22–31,61 | 26,71–26,79 | 13,41–49,64 | 19,91–39,25 |
| MDNE3 | 16,86 | 20,19 | 16,79–21,53 | 17,80–24,01 | 20,05–20,28 | 18,20–22,18 | 17,94–22,55 | 20,08–20,15 | 11,95–33,97 | 14,04–25,96 |
| COGN3 | 1,69 | 1,97 | 1,68–2,55 | 1,58–2,56 | 1,96–1,98 | 1,70–2,25 | 1,48–2,50 | 1,78–1,89 | 0,66–3,78 | 1,10–3,11 |
| HAPV3 | 4,21 | 4,82 | 3,21–7,97 | 3,21–7,87 | 4,43–5,08 | 3,56–6,08 | 1,26–11,79 | 3,61–4,34 | 0,00–25,16 | 0,36–14,03 |
| EZTC3 | 9,59 | 10,69 | 7,19–13,90 | 10,05–11,70 | 10,34–10,97 | 10,03–11,36 | 10,08–11,33 | 10,69–10,71 | 8,84–13,42 | 6,95–14,83 |
| ANIM3 | 2,43 | 2,54 | 2,18–3,04 | 1,28–4,43 | 2,41–2,61 | 1,81–3,27 | 1,11–4,05 | 1,85–2,19 | 0,00–8,36 | 0,36–5,22 |
| POMO4 | 3,89 | 3,96 | 3,36–4,99 | 3,52–4,65 | 3,95–3,96 | 3,60–4,31 | 3,26–4,69 | 3,95–3,96 | 2,08–6,80 | 2,83–5,74 |
| DESK3 | 19,32 | 19,46 | 1,86–16,31 | 19,46–19,46 | 19,46–19,46 | 10,28–28,63 | 17,54–21,43 | 19,38–19,45 | 18,53–20,43 | 1,43–19,34 |
| CEAB3 | 6,87 | 6,91 | 4,77–11,73 | 5,70–8,79 | 6,49–7,20 | 5,78–8,04 | 4,24–9,69 | 6,45–6,70 | 1,58–15,56 | 2,94–13,73 |
| CYRE3 | 17,74 | 17,76 | 15,39–20,70 | 15,76–20,93 | 17,48–17,95 | 15,93–19,58 | 15,69–19,92 | 17,44–17,68 | 11,70–26,15 | 12,65–24,23 |
| DIRR3 | 8,60 | 8,59 | 7,68–10,24 | 7,54–10,26 | 8,50–8,69 | 7,73–9,45 | 7,57–9,66 | 8,56–8,58 | 5,27–13,28 | 6,40–12,28 |
| LREN3 | 9,31 | 8,79 | 6,58–13,76 | 7,84–10,29 | 8,64–8,90 | 7,69–9,89 | 6,94–10,72 | 8,67–8,75 | 4,95–13,74 | 5,51–15,61 |
| BBAS3 | 16,84 | 15,67 | 12,62–18,05 | 14,08–18,30 | 15,17–16,06 | 13,49–17,86 | 14,13–17,34 | 15,67–15,67 | 11,18–21,42 | 10,11–21,26 |
| BBDC3 | 13,40 | 12,37 | 9,95–15,33 | 11,30–14,11 | 12,18–12,52 | 10,65–14,10 | 11,44–13,35 | 12,37–12,37 | 10,17–14,95 | 8,49–17,31 |
| PINE4 | 10,66 | 9,45 | 9,34–11,06 | 8,35–11,26 | 9,45–9,45 | 8,41–10,49 | 8,80–10,15 | 9,45–9,45 | 6,08–14,13 | 7,67–13,37 |
| CSAN3 | 2,37 | 2,10 | 1,57–3,31 | 2,08–2,12 | 2,08–2,12 | 1,88–2,32 | 2,01–2,19 | 1,99–2,09 | 1,80–2,70 | 1,52–3,48 |
| CURY3 | 26,37 | 22,89 | 20,42–26,98 | 20,42–26,87 | 22,51–23,34 | 20,56–25,23 | 20,21–25,72 | 22,90–23,00 | 13,65–37,01 | 17,29–31,63 |
| PGMN3 | 2,63 | 2,27 | 1,49–4,05 | 1,71–3,10 | 2,09–2,39 | 1,78–2,75 | 0,51–4,88 | 1,88–2,08 | 0,57–5,24 | 0,20–5,98 |
| BRSR6 | 12,94 | 10,91 | 9,26–12,82 | 9,87–12,61 | 10,32–11,36 | 9,46–12,35 | 9,70–12,20 | 10,91–10,91 | 7,45–15,10 | 7,30–15,22 |
| BBDC4 | 14,71 | 12,37 | 9,95–15,33 | 11,30–14,11 | 12,18–12,52 | 10,65–14,10 | 11,44–13,35 | 12,37–12,37 | 10,13–15,03 | 8,49–17,31 |
| LWSA3 | 3,41 | 2,82 | 1,93–4,28 | 2,62–3,15 | 2,82–2,83 | 2,53–3,12 | 2,51–3,15 | 2,83–2,86 | 1,95–3,92 | 1,82–4,70 |
| VULC3 | 11,77 | 9,70 | 7,80–13,89 | 8,58–11,50 | 9,68–9,72 | 8,62–10,79 | 8,17–11,31 | 9,58–9,66 | 6,25–13,91 | 6,57–15,82 |
| YDUQ3 | 8,76 | 7,10 | 6,21–9,00 | 5,24–9,90 | 7,01–7,18 | 5,86–8,34 | 4,24–10,14 | 5,88–6,64 | 1,58–17,09 | 2,77–12,55 |
| CBAV3 | 11,30 | 8,93 | 0,32–8,91 | 8,90–8,98 | 8,91–8,94 | 5,74–12,13 | 6,34–11,60 | 8,26–8,86 | 2,48–17,93 | 0,20–10,10 |
| ITSA4 | 12,91 | 9,79 | 7,66–12,37 | 9,11–10,90 | 9,76–9,81 | 8,41–11,18 | 9,29–10,32 | 9,77–9,79 | 8,64–11,07 | 6,87–13,83 |
| GRND3 | 3,65 | 2,76 | 2,11–3,59 | 2,60–3,01 | 2,73–2,79 | 2,55–2,98 | 2,47–3,07 | 2,77–2,81 | 2,04–3,69 | 2,00–3,95 |
| PSSA3 | 46,89 | 35,44 | 23,00–42,91 | 33,36–38,83 | 35,34–35,50 | 28,98–41,91 | 32,72–38,27 | 35,44–35,44 | 28,87–43,27 | 20,32–47,70 |
| VIVA3 | 17,63 | 13,31 | 9,66–21,21 | 11,78–15,74 | 13,16–13,41 | 11,58–15,05 | 11,54–15,17 | 13,09–13,23 | 9,35–18,30 | 8,30–23,82 |
| RIAA3 | 6,33 | 4,67 | 3,01–8,43 | 3,85–5,94 | 4,38–4,89 | 3,84–5,51 | 2,59–6,86 | 4,32–4,53 | 0,87–11,10 | 1,68–9,97 |
| LEVE3 | 31,17 | 22,49 | 19,66–28,87 | 19,43–27,25 | 22,00–23,06 | 20,11–24,87 | 18,51–26,66 | 22,05–22,28 | 13,17–35,15 | 15,79–33,77 |
| MDIA3 | 15,73 | 11,12 | 7,59–17,82 | 10,24–12,51 | 10,88–11,31 | 9,79–12,45 | 7,97–14,42 | 11,13–11,21 | 5,23–18,85 | 6,27–20,38 |
| PRIO3 | 72,29 | 50,96 | 44,96–61,50 | 46,55–57,21 | 50,58–51,22 | 45,78–56,14 | 46,30–55,90 | 49,96–50,43 | 20,95–98,93 | 39,49–70,20 |
| ABCB4 | 23,05 | 16,16 | 13,59–19,08 | 14,55–18,80 | 15,77–16,46 | 14,00–18,33 | 14,70–17,72 | 16,16–16,16 | 12,83–20,22 | 11,16–22,26 |
| SBFG3 | 5,08 | 3,52 | 1,06–8,41 | 3,29–4,95 | 3,43–3,80 | 2,45–4,59 | 1,90–7,12 | 3,09–3,48 | 0,46–12,29 | 0,83–10,71 |
| GGPS3 | 10,89 | 7,47 | 5,17–12,50 | 6,51–8,99 | 7,46–7,47 | 6,38–8,56 | 4,70–10,35 | 7,27–7,37 | 4,25–11,54 | 3,68–14,85 |
| SLCE3 | 16,88 | 11,56 | 5,37–15,78 | 9,82–14,12 | 11,48–11,63 | 9,77–13,35 | 9,17–14,07 | 10,11–10,87 | 2,74–32,56 | 3,85–17,34 |
| BBSE3 | 41,40 | 28,26 | 23,85–30,91 | 26,39–31,23 | 27,90–28,69 | 23,85–32,67 | 27,56–28,98 | 28,26–28,26 | 23,66–33,81 | 21,04–35,25 |
| SANB11 | 24,33 | 16,59 | 12,38–20,61 | 15,23–18,78 | 16,27–16,83 | 14,11–19,06 | 15,25–17,99 | 16,59–16,59 | 13,28–20,16 | 10,49–23,18 |
| SAUD3 | 14,64 | 9,96 | 6,57–12,00 | 9,37–10,94 | 9,96–9,96 | 8,16–11,77 | 9,36–10,58 | 9,96–9,96 | 8,08–11,91 | 5,83–13,35 |
| TFCO4 | 10,08 | 6,69 | 4,30–11,52 | 5,91–7,95 | 6,65–6,73 | 5,76–7,62 | 5,67–7,75 | 6,62–6,65 | 3,98–10,52 | 3,76–12,80 |
| AUAU3 | 3,86 | 2,46 | 1,54–4,52 | 2,14–2,95 | 2,40–2,50 | 2,05–2,87 | 1,63–3,33 | 2,35–2,42 | 0,88–4,43 | 1,13–5,18 |
| MOVI3 | 6,62 | 4,19 | 1,29–9,77 | 3,86–8,16 | 4,12–4,73 | 1,96–6,43 | 2,53–8,70 | 2,50–4,03 | 0,00–24,41 | 0,17–13,59 |
| ITUB4 | 39,90 | 25,13 | 19,71–31,34 | 23,28–28,09 | 25,09–25,15 | 21,54–28,73 | 23,88–26,42 | 25,13–25,13 | 21,94–28,51 | 17,52–35,12 |
| IRBR3 | 56,58 | 35,09 | 29,10–43,73 | 32,23–39,63 | 34,08–35,87 | 30,33–39,85 | 31,68–38,67 | 35,09–35,09 | 25,23–46,28 | 24,30–49,92 |
| USIM5 | 5,68 | 3,49 | 2,26–5,78 | 3,17–3,99 | 3,15–3,76 | 3,03–3,95 | 2,21–4,83 | 3,49–3,51 | 0,30–9,93 | 1,62–6,81 |
| BMOB3 | 24,42 | 14,93 | 11,51–21,67 | 13,44–17,39 | 14,81–15,06 | 13,33–16,53 | 12,23–17,74 | 14,94–15,07 | 9,99–21,48 | 10,04–24,75 |
| IGTI11 | 22,70 | 13,60 | 9,15–23,09 | 11,84–16,37 | 13,46–13,76 | 11,58–15,63 | 12,16–15,14 | 13,05–13,43 | 10,43–17,35 | 7,73–25,57 |
| TIMS3 | 19,00 | 11,29 | 9,73–14,80 | 9,72–13,65 | 11,12–11,49 | 9,92–12,66 | 9,56–13,13 | 10,60–11,01 | 8,44–14,74 | 7,69–16,99 |
| CXSE3 | 21,16 | 12,43 | 8,87–14,57 | 11,77–13,51 | 12,36–12,52 | 10,27–14,59 | 11,90–12,97 | 12,43–12,43 | 10,69–14,21 | 8,03–16,29 |
| MULT3 | 25,84 | 14,84 | 10,15–25,31 | 12,73–18,14 | 14,66–15,03 | 12,55–17,12 | 13,19–16,58 | 14,14–14,60 | 11,13–19,30 | 8,48–28,03 |
| INTB3 | 14,36 | 8,23 | 5,98–13,19 | 7,57–9,29 | 8,13–8,31 | 7,24–9,22 | 6,66–9,87 | 8,24–8,36 | 5,23–12,31 | 5,26–14,99 |
| ABEV3 | 15,18 | 8,70 | 6,37–13,09 | 7,98–9,82 | 8,65–8,75 | 7,72–9,67 | 7,84–9,60 | 8,71–8,78 | 6,59–11,36 | 5,99–14,57 |
| PETR4 | 52,73 | 29,60 | 23,59–43,31 | 25,11–36,50 | 28,54–30,36 | 25,47–33,73 | 25,04–34,42 | 28,42–29,02 | 8,24–71,97 | 19,12–49,62 |
| NATU3 | 5,02 | 2,81 | 1,80–4,82 | 2,29–3,60 | 2,76–2,83 | 2,30–3,31 | 1,31–4,36 | 2,60–2,71 | 0,49–8,01 | 0,95–6,12 |
| MRVE3 | 4,27 | 2,34 | 2,02–4,83 | 1,87–3,02 | 2,11–2,51 | 2,16–2,52 | 0,91–4,11 | 1,35–2,14 | 0,09–8,42 | 0,86–7,04 |
| ALOS3 | 24,44 | 13,07 | 9,36–21,40 | 11,28–15,84 | 12,94–13,22 | 11,12–15,03 | 11,53–14,71 | 12,41–12,89 | 9,64–17,02 | 7,89–23,81 |
| RENT3 | 29,74 | 15,89 | 9,56–30,26 | 12,37–21,26 | 15,05–16,46 | 12,55–19,23 | 10,63–21,47 | 13,55–14,89 | 6,42–33,54 | 5,74–34,48 |
| BPAC11 | 56,38 | 29,59 | 18,90–42,16 | 27,03–33,87 | 29,53–29,62 | 24,66–34,52 | 27,90–31,41 | 29,59–29,59 | 24,46–35,67 | 16,41–46,62 |
| RAPT4 | 3,67 | 1,92 | 0,54–5,08 | 1,83–2,08 | 1,89–1,95 | 0,94–2,90 | 1,03–2,92 | 1,76–1,91 | 0,00–10,73 | 0,24–6,85 |
| B3SA3 | 14,66 | 7,65 | 5,67–11,75 | 7,02–8,64 | 7,58–7,72 | 6,76–8,53 | 7,13–8,19 | 7,63–7,70 | 6,06–9,75 | 5,29–13,05 |
| GOAU4 | 10,62 | 5,32 | 3,77–8,77 | 4,75–6,21 | 4,98–5,59 | 4,55–6,09 | 3,82–6,90 | 5,21–5,28 | 1,08–12,57 | 2,89–10,11 |
| PETR3 | 59,12 | 29,60 | 23,59–43,31 | 25,11–36,50 | 28,54–30,36 | 25,47–33,73 | 25,04–34,42 | 28,42–29,02 | 8,57–72,39 | 19,12–49,62 |
| HYPE3 | 21,60 | 10,76 | 7,73–17,60 | 9,21–13,14 | 10,26–11,12 | 9,08–12,44 | 8,88–12,74 | 10,04–10,50 | 6,51–15,71 | 6,27–19,82 |
| ALPA4 | 13,35 | 6,53 | 4,24–10,72 | 5,94–7,46 | 6,50–6,54 | 5,70–7,35 | 5,59–7,51 | 6,47–6,51 | 4,08–9,62 | 3,88–11,83 |
| TOTS3 | 34,09 | 16,55 | 10,38–29,55 | 14,89–19,18 | 16,49–16,60 | 14,09–19,00 | 14,22–18,99 | 16,16–16,45 | 11,59–22,30 | 9,25–32,84 |
| VIVT3 | 30,85 | 14,80 | 10,94–23,56 | 12,92–17,68 | 14,60–15,03 | 12,69–16,91 | 12,31–17,44 | 14,12–14,58 | 10,96–19,13 | 8,99–26,53 |
| MILS3 | 15,56 | 7,24 | 4,83–12,65 | 6,22–8,84 | 7,11–7,34 | 6,09–8,40 | 6,21–8,34 | 6,90–7,10 | 3,89–11,90 | 4,01–14,14 |
| AZZA3 | 15,07 | 6,90 | 5,14–10,73 | 5,25–9,42 | 6,48–7,20 | 5,63–8,17 | 3,01–13,46 | 5,76–6,49 | 0,01–26,08 | 1,42–16,65 |
| RECV3 | 11,14 | 5,10 | 2,71–10,03 | 4,35–6,22 | 4,72–5,38 | 4,07–6,13 | 4,04–6,22 | 4,84–5,00 | 1,81–13,70 | 2,14–11,23 |
| FLRY3 | 21,67 | 9,35 | 5,83–17,33 | 8,15–11,21 | 9,13–9,51 | 7,74–10,96 | 7,23–11,55 | 8,79–9,20 | 5,89–13,29 | 4,70–19,41 |
| SIMH3 | 5,24 | 2,26 | -0,16–6,91 | 2,04–5,46 | 2,15–2,65 | 0,34–4,24 | 0,84–6,35 | 1,01–2,13 | 0,00–13,24 | -1,08–10,81 |
| SMFT3 | 15,99 | 6,87 | 1,82–18,43 | 6,54–8,17 | 6,85–6,88 | 4,75–8,99 | 5,71–8,08 | 5,65–6,75 | 2,91–15,76 | 1,34–19,94 |
| GGBR4 | 23,99 | 10,05 | 7,13–16,53 | 8,95–11,74 | 9,41–10,54 | 8,60–11,50 | 7,21–13,02 | 9,83–9,97 | 2,06–23,68 | 5,46–19,05 |
| PNVL3 | 10,56 | 4,38 | 1,13–11,86 | 4,20–5,25 | 4,33–4,42 | 3,15–5,62 | 1,76–8,94 | 3,86–4,33 | 2,12–8,62 | 0,45–15,07 |
| RADL3 | 15,67 | 6,41 | 2,87–14,41 | 5,54–7,82 | 6,34–6,45 | 5,10–7,72 | 3,36–9,99 | 6,01–6,31 | 3,75–9,87 | 1,64–16,94 |
| ECOR3 | 5,27 | 2,15 | 0,66–4,98 | 1,97–2,43 | 2,13–2,16 | 0,77–3,93 | 1,38–2,95 | 1,77–2,11 | 0,07–4,61 | 0,00–8,90 |
| RDOR3 | 33,80 | 13,66 | 9,17–23,74 | 11,31–17,36 | 13,55–13,71 | 11,33–15,99 | 10,28–17,21 | 12,70–13,31 | 8,21–20,40 | 6,72–27,17 |
| OPCT3 | 8,92 | 3,60 | 1,88–7,55 | 2,82–5,04 | 3,15–3,91 | 2,65–4,56 | 2,45–4,94 | 2,86–3,22 | 0,77–11,78 | 1,08–8,67 |
| TUPY3 | 15,41 | 6,04 | 2,23–13,49 | 5,32–8,82 | 5,67–6,47 | 4,37–7,71 | 2,69–12,95 | 5,21–5,71 | 0,00–28,84 | 1,30–18,12 |
| UGPA3 | 32,70 | 12,79 | 9,31–20,54 | 11,35–15,01 | 12,61–12,92 | 11,00–14,59 | 2,57–24,52 | 12,47–12,65 | 6,17–21,27 | 1,76–30,41 |
| VAMO3 | 2,57 | 0,95 | 0,29–2,26 | 0,88–1,76 | 0,93–1,03 | 0,43–1,48 | 0,66–1,67 | 0,55–0,91 | 0,07–4,02 | 0,05–2,99 |
| MOTV3 | 14,61 | 5,34 | 1,60–13,70 | 5,07–6,70 | 5,33–5,35 | 3,75–6,94 | 4,74–5,98 | 4,72–5,28 | 3,70–9,21 | 1,31–15,12 |
| BRAV3 | 18,45 | 6,59 | 2,63–15,34 | 5,84–8,73 | 6,21–6,85 | 4,40–8,77 | 5,05–9,54 | 5,62–6,11 | 0,33–35,32 | 1,89–18,04 |
| PRNR3 | 12,96 | 4,55 | 1,72–10,99 | 3,88–6,81 | 4,43–4,62 | 3,10–6,00 | 2,26–8,54 | 3,56–4,16 | 0,93–17,78 | 0,74–13,59 |
| GMAT3 | 3,54 | 1,23 | 0,37–3,12 | 1,16–1,51 | 1,21–1,25 | 0,88–1,57 | 0,35–2,92 | 1,12–1,22 | 0,54–2,64 | 0,12–4,39 |
| ORVR3 | 15,73 | 5,42 | 2,07–12,84 | 4,75–6,48 | 5,22–5,57 | 4,24–6,60 | 4,54–6,35 | 5,15–5,32 | 3,01–8,72 | 1,70–14,20 |
| RAIL3 | 14,40 | 4,89 | 1,12–13,48 | 4,72–5,33 | 4,87–4,90 | 3,33–6,45 | 4,25–5,55 | 4,12–4,81 | 2,74–9,16 | 0,85–14,75 |
| TTEN3 | 10,63 | 3,46 | 1,01–8,99 | 3,27–4,65 | 3,41–3,59 | 2,54–4,38 | 1,48–7,52 | 3,17–3,43 | 0,75–10,78 | 0,60–11,73 |
| EMBJ3 | 96,75 | 30,69 | 17,41–54,54 | 27,63–35,72 | 30,40–30,89 | 26,38–35,00 | 23,93–37,75 | 30,50–30,62 | 16,62–50,67 | 15,36–60,91 |
| SAPR11 | 32,42 | 10,26 | 3,08–25,57 | 9,67–13,07 | 10,02–10,45 | 7,47–13,05 | 8,99–11,79 | 9,55–10,19 | 6,44–19,32 | 2,80–28,37 |
| UNIP6 | 50,61 | 15,79 | 11,43–25,11 | 12,87–20,18 | 15,24–16,18 | 13,14–18,44 | 10,75–21,06 | 14,46–15,35 | 0,00–63,86 | 7,70–29,58 |
| LOGG3 | 21,52 | 6,71 | 4,25–12,34 | 5,46–8,51 | 6,53–6,84 | 5,21–8,21 | 5,22–8,29 | 5,02–6,36 | 1,55–15,27 | 2,66–13,34 |
| SUZB3 | 48,19 | 14,84 | 9,21–25,42 | 10,66–24,28 | 13,80–16,24 | 10,87–18,81 | 9,43–21,37 | 10,15–12,45 | 0,61–69,29 | 3,95–31,90 |
| CPFE3 | 42,97 | 12,56 | 3,77–30,60 | 11,97–15,18 | 12,46–12,63 | 9,06–16,05 | 10,57–15,11 | 11,21–12,42 | 8,64–20,43 | 3,23–34,05 |
| ALUP11 | 31,94 | 9,24 | 2,77–23,64 | 8,80–13,05 | 9,13–9,32 | 5,91–12,57 | 8,23–10,73 | 8,13–9,13 | 7,01–16,22 | 2,27–26,94 |
| TAEE11 | 40,04 | 11,50 | 8,38–18,49 | 9,15–14,80 | 9,36–13,22 | 9,09–13,92 | 9,11–14,05 | 8,77–10,59 | 7,00–16,77 | 4,54–21,04 |
| ASAI3 | 7,81 | 2,24 | 0,68–5,28 | 2,07–3,04 | 2,22–2,26 | 1,25–3,24 | 0,01–7,39 | 1,57–2,18 | 0,58–6,01 | 0,00–9,65 |
| JHSF3 | 9,50 | 2,62 | 0,51–4,10 | 2,43–2,96 | 2,55–2,68 | 2,20–3,04 | 2,36–2,90 | 2,29–2,59 | 1,27–4,78 | 0,45–4,50 |
| JSLG3 | 5,62 | 1,53 | 0,48–3,51 | 1,40–3,34 | 1,50–1,64 | 0,59–2,67 | 0,47–5,58 | 1,47–1,53 | 0,00–11,06 | 0,00–7,75 |
| EGIE3 | 27,30 | 7,18 | 2,37–17,76 | 6,71–9,66 | 6,96–7,57 | 5,07–9,29 | 6,23–9,05 | 6,24–6,96 | 5,05–12,06 | 2,05–19,80 |
| MGLU3 | 5,14 | 1,31 | 0,07–4,04 | 1,29–1,33 | 1,29–1,33 | 0,14–2,61 | 0,00–2,74 | 1,22–1,30 | 0,00–5,40 | 0,00–6,00 |
| DXCO3 | 4,61 | 1,16 | 0,34–3,04 | 1,10–1,40 | 1,12–1,20 | 0,72–1,60 | 0,78–1,78 | 0,95–1,14 | 0,44–4,20 | 0,22–3,87 |
| CMIG4 | 10,15 | 2,56 | 0,77–6,09 | 2,42–2,78 | 2,53–2,58 | 1,75–3,37 | 1,91–3,23 | 2,20–2,52 | 1,38–4,03 | 0,59–7,07 |
| CSMG3 | 49,96 | 11,89 | 3,27–31,56 | 11,39–12,70 | 11,82–11,94 | 8,42–15,36 | 10,17–13,69 | 10,37–11,74 | 7,00–17,54 | 2,25–34,43 |
| WEGE3 | 47,38 | 11,19 | 5,65–23,37 | 10,24–12,75 | 11,12–11,26 | 9,27–13,11 | 9,63–12,81 | 11,12–11,17 | 7,97–15,24 | 4,99–25,97 |
| VBBR3 | 30,76 | 6,81 | 3,29–13,81 | 5,54–9,33 | 6,75–6,83 | 5,21–8,41 | 0,00–21,87 | 6,05–6,54 | 1,30–21,06 | 0,00–26,86 |
| ENGI11 | 45,24 | 9,87 | 2,22–27,31 | 9,55–10,38 | 9,79–9,92 | 5,16–14,57 | 6,42–13,43 | 6,93–9,57 | 4,07–17,27 | 0,35–33,92 |
| BRAP4 | 18,02 | 3,92 | 1,81–7,86 | 3,90–3,94 | 3,83–4,00 | 2,83–5,01 | 2,94–4,94 | 3,50–3,88 | 0,82–12,66 | 1,47–9,47 |
| SBSP3 | 24,90 | 5,36 | 1,07–15,10 | 5,19–5,65 | 5,32–5,39 | 3,66–7,06 | 4,76–5,98 | 4,71–5,29 | 3,76–7,27 | 0,78–16,50 |
| ISAE4 | 25,24 | 5,13 | 1,47–13,41 | 4,98–5,36 | 5,08–5,16 | 3,18–7,07 | 4,36–5,93 | 3,71–4,98 | 3,42–7,15 | 0,66–14,86 |
| CPLE3 | 14,67 | 2,79 | 0,84–6,94 | 2,67–2,98 | 2,77–2,81 | 1,99–3,60 | 2,24–3,37 | 2,40–2,75 | 1,78–4,12 | 0,65–7,68 |
| KLBN11 | 17,63 | 3,20 | 1,25–6,48 | 2,94–7,20 | 3,21–4,04 | 1,74–4,66 | 2,34–5,97 | 2,34–3,12 | 0,43–17,71 | 0,51–9,56 |
| AXIA3 | 48,18 | 7,77 | 2,29–20,17 | 7,51–8,19 | 7,68–7,85 | 4,75–10,80 | 6,44–9,18 | 6,65–7,66 | 3,19–13,65 | 1,49–23,20 |
| EQTL3 | 34,07 | 5,15 | 1,02–14,52 | 4,99–5,42 | 5,11–5,18 | 2,65–7,65 | 3,42–6,94 | 3,54–4,99 | 2,61–8,85 | 0,22–20,03 |
| CVCB3 | 0,88 | 0,13 | 0,00–0,41 | 0,13–0,13 | 0,13–0,13 | 0,00–0,38 | 0,04–0,22 | 0,12–0,13 | 0,00–1,37 | 0,00–0,90 |
| AURE3 | 11,06 | 1,56 | 0,30–4,39 | 1,49–1,66 | 1,53–1,57 | 0,27–3,20 | 0,82–2,33 | 1,27–1,53 | 0,00–5,45 | 0,00–7,26 |
| VALE3 | 61,08 | 7,46 | 2,38–16,95 | 7,21–7,83 | 7,35–7,55 | 4,84–10,09 | 5,10–9,92 | 6,44–7,36 | 0,00–28,49 | 1,58–20,84 |
| ENEV3 | 26,49 | 2,79 | 0,76–7,42 | 2,64–3,38 | 2,76–2,80 | 1,66–3,91 | 2,14–3,46 | 2,10–2,72 | 1,08–7,48 | 0,44–8,70 |

## Lista robusta

Empresas no top 7 em pelo menos 80% ou 50% das combinações de cada grade.

| Grade | TIR ≥ 80% | TIR ≥ 50% | Upside ≥ 80% | Upside ≥ 50% |
|---|---|---|---|---|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | BEEF3, VTRU3, SEER3, TEND3 | BEEF3, VTRU3, SEER3, TEND3, COGN3, PLPL3, HAPV3 |
| Ke 20–30% (passo 1 p.p.) | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | PLPL3, BEEF3, SEER3, VTRU3, TEND3 | PLPL3, BEEF3, SEER3, VTRU3, TEND3, MDNE3 |
| g terminal −2 a +2 p.p. | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3, COGN3 |
| Múltiplos-alvo −30% a +30% | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | PLPL3, TEND3, BEEF3, SEER3, VTRU3 | PLPL3, TEND3, BEEF3, SEER3, VTRU3, MDNE3 |
| Margem EBITDA × crescimento ±2 p.p. | MDNE3, PLPL3, TEND3, HAPV3, VTRU3 | MDNE3, PLPL3, TEND3, HAPV3, VTRU3, BEEF3 | PLPL3, SEER3, VTRU3, TEND3 | PLPL3, SEER3, VTRU3, TEND3, BEEF3, MDNE3 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | MDNE3, PLPL3, TEND3, HAPV3, VTRU3 | MDNE3, PLPL3, TEND3, HAPV3, VTRU3, PINE4, SEER3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3, EZTC3 |
| Monte Carlo com desvios ×1,5 | nenhuma | PLPL3 | nenhuma | BEEF3 |
| Amostra conjunta de todas as grades | MDNE3, PLPL3, TEND3, VTRU3 | MDNE3, PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3 | VTRU3, TEND3 | VTRU3, TEND3, PLPL3, SEER3, BEEF3, HAPV3 |
| Em todas as grades ao mesmo tempo | nenhuma | PLPL3 | nenhuma | BEEF3 |

## As 7 oportunidades atuais e os pesos

Para cada um dos 66 vetores de pesos, o teste recalcula o upside, a P(valor justo > preço) e o escore e reaplica a regra do `build.py`. A P(MC) sai do mesmo Monte Carlo do motor, com os valores por método guardados em cada sorteio e o blend refeito. A TIR e os demais fatores do escore não dependem dos pesos.

| Empresa | Selecionada (% dos pesos) | Condição (≥ 50% dos vetores) | P(MC) mín–máx | Upside mín–máx | Seleção por w_múlt = 0; 0,1; …; 1 | Seleção por w_DCF = 0; 0,1; …; 1 |
|---|---:|---|---|---|---|---|
| VTRU3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 62%–100% | 8%–65% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| BEEF3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 57%–91% | 14%–122% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| PLPL3 ★ | 97% | w_múlt ≤ 0,9; qualquer w_DCF | 70%–96% | 19%–57% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 50% 0% | 82% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| MDNE3 ★ | 95% | qualquer w_múlt; w_DCF ≤ 0,9 | 40%–89% | -5%–32% | 82% 100% 100% 100% 100% 100% 100% 100% 67% 100% 100% | 100% 100% 89% 100% 100% 100% 100% 100% 100% 50% 0% |
| SEER3 ★ | 85% | w_múlt entre 0,0 e 1,0, irregular; w_DCF ≥ 0,1 | 43%–99% | -3%–58% | 91% 100% 100% 100% 86% 83% 60% 50% 33% 50% 100% | 45% 60% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| CEAB3 ★ | 62% | w_múlt ≥ 0,2; w_DCF ≤ 0,5 | 23%–97% | -37%–93% | 0% 0% 56% 100% 100% 100% 100% 100% 100% 100% 100% | 82% 80% 78% 75% 71% 50% 40% 25% 0% 0% 0% |
| TEND3 ★ | 56% | w_múlt ≤ 0,3; w_DCF ≥ 0,3 | 52%–97% | 2%–55% | 100% 100% 78% 75% 43% 0% 0% 0% 0% 0% 0% | 18% 20% 44% 50% 71% 83% 100% 100% 100% 100% 100% |
| COGN3 ★ | 36% | w_múlt ≤ 0,1; w_DCF ≥ 0,5 | 46%–97% | -2%–63% | 100% 90% 44% 0% 0% 0% 0% 0% 0% 0% 0% | 9% 20% 22% 25% 29% 50% 60% 75% 100% 100% 100% |
| LREN3 | 38% | w_múlt ≥ 0,4; w_DCF ≤ 0,3 | 4%–100% | -34%–65% | 0% 0% 0% 0% 57% 100% 100% 100% 100% 100% 100% | 64% 60% 56% 50% 29% 17% 0% 0% 0% 0% 0% |
| SBFG3 | 26% | w_múlt ≥ 0,7; w_DCF ≤ 0,1 | 8%–88% | -91%–87% | 0% 10% 22% 25% 14% 17% 40% 50% 100% 100% 100% | 91% 60% 11% 0% 0% 0% 0% 0% 0% 0% 0% |
| DIRR3 | 3% | nenhum w_múlt; w_DCF ≥ 0,9 | 24%–89% | -15%–24% | 18% 0% 0% 0% 0% 0% 0% 0% 0% 0% 0% | 0% 0% 0% 0% 0% 0% 0% 0% 0% 50% 100% |

Quantas das 7 atuais a regra mantém, em número de combinações: 5 mantidas: 12, 6 mantidas: 21, 7 mantidas: 33.

Seleção pela regra nas demais grades (fração de combinações em que cada empresa está entre as 7):

- Pesos do blend {DCF, DDM, múltiplos} (passo 0,1): BEEF3 100%, VTRU3 100%, PLPL3 97%, MDNE3 95%, SEER3 85%, CEAB3 62%, TEND3 56%, LREN3 38%, COGN3 36%, SBFG3 26%, DIRR3 3% (lista idêntica em 0%).
- Ke 20–30% (passo 1 p.p.): MDNE3 100%, PLPL3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, TEND3 82%, CEAB3 64%, COGN3 27%, LREN3 9% (lista idêntica em 0%).
- g terminal −2 a +2 p.p.: MDNE3 100%, PLPL3 100%, TEND3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, CEAB3 80%, COGN3 20% (lista idêntica em 0%).
- Múltiplos-alvo −30% a +30%: MDNE3 100%, PLPL3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, TEND3 86%, CEAB3 57%, COGN3 43%, LREN3 14% (lista idêntica em 0%).
- Margem EBITDA × crescimento ±2 p.p.: PLPL3 100%, VTRU3 100%, MDNE3 96%, SEER3 80%, BEEF3 68%, CEAB3 56%, TEND3 56%, PGMN3 40%, COGN3 32%, SBFG3 20%, LREN3 4% (lista idêntica em 0%).
- Kd +300 bp (WACC / resultado financeiro / ambos): MDNE3 100%, PLPL3 100%, TEND3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, CEAB3 67%, COGN3 33% (lista idêntica em 0%).
- Monte Carlo com desvios ×1,5 (P(MC) recalculada com os pesos da base): BEEF3, VTRU3, PLPL3, CEAB3, MDNE3, SEER3, TEND3, COGN3.

## Pesos propostos por setor

| Setor | Empresas | Pesos | Justificativa |
|---|---|---|---|
| bancos | BBAS3, BBDC4, BRSR6, BPAC11 | DDM 60% / P/VP 40% | Valor de banco = ROE contra Ke sobre o PL. O DDM já é o fluxo do acionista (dividendo limitado pelo capital regulatório) e sua perpetuidade é o P/VP de Gordon (ROE−g)/(Ke−g); o P/VP-alvo é a âncora de mercado. O P/L sai: é redundante com o DDM (ambos lucro) e distorcido pelo ciclo de provisões e pelo JCP. |
| utilities | ALUP11, AURE3, CPLE3, ENGI11, EQTL3, SBSP3 | DDM 80% / Múltiplos 20% | Retorno regulado e payout por política. Com DL de cerca de 50% do EV, o patrimônio do DCF (EV − DL) é a diferença de dois números grandes e sai negativo a Ke 25% nas 6 empresas: o motor trunca em zero e mantém o peso, então o DCF vira só um corte. O DCF fica como checagem (ROIC < WACC). O DDM desconta direto o fluxo do acionista após o serviço da dívida e foi o método menos disperso do setor. |
| concessoes | ECOR3, MOTV3, RAIL3, ORVR3 | DDM 80% / Múltiplos 20% | Concessões rodoviárias, ferroviárias e ambientais com alavancagem de projeto de cerca de 50% do EV. O retorno do acionista é o dividendo após a dívida, e o DCF dá patrimônio residual negativo em ECOR3, MOTV3 e RAIL3. Os múltiplos ficam com 20% como âncora de mercado. |
| incorporadoras | CURY3, CYRE3, DIRR3, EZTC3, JHSF3, MDNE3, MRVE3, PLPL3, TEND3 | DDM 50% / P/L 30% / DCF 20% | P/VP-ROE: no motor, a perpetuidade do DDM é PL×(ROE−g)/(Ke−g), o mesmo que P/VP justo × VPA. O P/L é o múltiplo de mercado do setor. EV/EBITDA sai porque há juros capitalizados no custo e a DL inclui financiamento à produção (capital de giro). O FCFF oscila com terreno e recebíveis (nwc de 0,6–1,5× a receita), daí só 20% de DCF. |
| varejo | CEAB3, LREN3, SBFG3, MGLU3, ASAI3, GMAT3, PGMN3, RADL3, AZZA3, ALPA4, VIVA3, VULC3, NATU3 | DDM 50% / Múltiplos 30% / DCF 20% | Muitos comparáveis listados e ciclo de margem e de giro: os múltiplos (P/L e EV/EBITDA IFRS-16) sobem para 30% (o padrão é 25%). Não vão além porque embutem custo de capital de cerca de 12%, e a 40% sozinhos põem LREN3 e SBFG3 na lista (ver sensibilidade). O DCF cai para 20%: o arrendamento IFRS-16 entra na DL (cerca de 40% do EV) e o DCF é o método mais disperso do setor. O DDM, coerente com o Ke 25%, fica com 50%. |
| locadoras | RENT3, MOVI3, VAMO3 | DDM 70% / Múltiplos 30% | O capex de frota é sobretudo crescimento e a DL passa de 70% do EV: o FCFF é negativo no horizonte explícito e o patrimônio do DCF fica ≤ 0 (MOVI3, VAMO3), daí DCF fora do blend. O dividendo reflete a geração depois da frota. O mercado precifica por P/L e EV/EBITDA, que ficam com 30%. |
| shoppings | ALOS3, IGTI11, MULT3 | DDM 50% / DCF 30% / Múltiplos 20% | Ativos reais de vida longa, payout alto e alavancagem moderada (DL de cerca de 25% do EV). DCF e DDM convergem no nível (diferença de 5–16%), mas o DDM é menos disperso (0,65 contra 1,00), daí 50/30. Os múltiplos-alvo (P/L de 9,5–12x) valem 2,5× o DDM porque embutem custo de capital muito abaixo de 25%; ficam com 20%. |
| demais | VBBR3, HYPE3, SMFT3, CVCB3, YDUQ3, COGN3, ANIM3, HAPV3, RDOR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3, PETR4, PETR3, PRIO3, BRAV3, RECV3, UGPA3, ENEV3, UNIP6, VALE3, CBAV3, GGBR4, USIM5, SUZB3, KLBN11, SLCE3, WEGE3, EMBJ3, POMO4, RAPT4, TUPY3, LEVE3, DXCO3, ITUB4, SANB11, BBDC3, ABCB4, PINE4, BBSE3, CXSE3, PSSA3, IRBR3, SAUD3, AXIA3, CMIG4, EGIE3, CPFE3, ISAE4, TAEE11, CSMG3, SAPR11, ABEV3, MDIA3, GRND3, VIVT3, TIMS3, DESK3, BMOB3, LWSA3, FLRY3, PNVL3, SEER3, VTRU3, RIAA3, AUAU3, TFCO4, JSLG3, MILS3, OPCT3, PRNR3, LOGG3 | DCF 50% / DDM 25% / Múltiplos 25% | Educação, saúde, serviços, tecnologia, proteína, agro, combustíveis e turismo: mantém o padrão da especificação (50/25/25). |

Diagnóstico por setor, com base nos valores da base e na amostra conjunta. A dispersão é (p95 − p5) / p50 de cada método sob Ke, g, múltiplos, margem, crescimento e Kd. Os pesos de mínima dispersão minimizam a dispersão mediana do blend no setor. São só uma checagem, porque payout, capex e capital de giro não são choques da grade e o DDM e o DCF dependem deles.

| Setor | n | DCF < 0 | Múltiplos/DDM (mediana) | DCF/DDM (mediana) | DL/EV mercado | Dispersão DCF | Dispersão DDM | Dispersão múltiplos | Pesos de mínima dispersão |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| bancos | 4 | 0 | 1,61 | — | — | — | 0,77 | 0,68 | DCF 0.0 / DDM 0.6 / Múlt 0.4 |
| utilities | 6 | 6 | 5,16 | -3,85 | 52% | — | 1,85 | 1,43 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| concessoes | 4 | 3 | 3,80 | -0,49 | 50% | 1,93 | 0,95 | 0,99 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| incorporadoras | 9 | 1 | 1,44 | 1,18 | 15% | 0,68 | 0,63 | 0,75 | DCF 0.0 / DDM 0.7 / Múlt 0.3 |
| varejo | 13 | 4 | 2,37 | 0,75 | 39% | 2,11 | 1,38 | 1,40 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| locadoras | 3 | 2 | 2,01 | -0,07 | 80% | 3,47 | 1,89 | 2,51 | DCF 0.0 / DDM 0.9 / Múlt 0.1 |
| shoppings | 3 | 0 | 2,53 | 0,84 | 26% | 1,00 | 0,65 | 0,74 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| demais | 75 | 17 | 2,18 | 0,75 | 33% | 1,17 | 0,82 | 0,94 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |

Impacto dos pesos propostos (empresas cujo rank por upside ou cuja seleção muda, além do top 15 de cada lado):

| Empresa | Setor | VJ base → proposto | Δ VJ | Upside base → proposto | Rank upside | P(MC) base → proposta | Rank escore | Regra |
|---|---|---|---:|---|---|---|---|---|
| BEEF3 | demais | 5,44 → 5,44 | 0% | 89% → 89% | 1 → 1 | 79% → 79% | 1 → 1 | mantém |
| VTRU3 | demais | 16,99 → 16,99 | 0% | 42% → 42% | 2 → 2 | 92% → 92% | 2 → 2 | mantém |
| PLPL3 | incorporadoras | 6,37 → 6,37 | 0% | 32% → 32% | 3 → 3 | 89% → 82% | 3 → 5 | mantém |
| SEER3 | demais | 14,19 → 14,19 | 0% | 29% → 29% | 4 → 4 | 84% → 84% | 6 → 7 | mantém |
| TEND3 | incorporadoras | 26,81 → 26,81 | 0% | 26% → 26% | 5 → 5 | 90% → 79% | 8 → 10 | sai |
| MDNE3 | incorporadoras | 20,19 → 20,19 | 0% | 20% → 20% | 6 → 6 | 65% → 79% | 7 → 6 | mantém |
| COGN3 | demais | 1,97 → 1,97 | 0% | 17% → 17% | 7 → 7 | 67% → 67% | 9 → 12 | — |
| HAPV3 | demais | 4,82 → 4,82 | 0% | 14% → 14% | 8 → 8 | 53% → 53% | 4 → 3 | — |
| CEAB3 | varejo | 6,91 → 7,72 | 12% | 1% → 12% | 13 → 9 | 50% → 61% | 5 → 4 | mantém |
| MOVI3 | locadoras | 4,19 → 7,35 | 75% | -37% → 11% | 46 → 10 | 35% → 56% | 13 → 8 | — |
| ANIM3 | demais | 2,54 → 2,54 | 0% | 4% → 4% | 10 → 11 | 51% → 51% | 10 → 13 | — |
| LREN3 | varejo | 8,79 → 9,55 | 9% | -6% → 3% | 16 → 12 | 38% → 55% | 11 → 9 | entra |
| POMO4 | demais | 3,96 → 3,96 | 0% | 2% → 2% | 11 → 13 | 52% → 52% | 12 → 15 | — |
| SBFG3 | varejo | 3,52 → 5,14 | 46% | -31% → 1% | 38 → 14 | 29% → 51% | 15 → 11 | — |
| CYRE3 | incorporadoras | 17,76 → 17,76 | 0% | 0% → 0% | 14 → 15 | 39% → 49% | 18 → 16 | — |
| DIRR3 | incorporadoras | 8,59 → 8,59 | 0% | -0% → -0% | 15 → 17 | 54% → 49% | 24 → 24 | — |
| EZTC3 | incorporadoras | 10,69 → 9,46 | -11% | 12% → -1% | 9 → 19 | 91% → 45% | 17 → 27 | — |
| DESK3 | demais | 19,46 → 6,28 | -68% | 1% → -67% | 12 → 92 | 63% → 0% | 87 → 119 | — |

Top 7 por upside: base BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3; proposto BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3. Regra de oportunidades: base BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3; proposto BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3.

Decomposição, aplicando os pesos propostos a um setor por vez (os demais ficam na base):

| Setor alterado | Δ VJ mediano do setor | Spearman upside vs base | Entram na regra | Saem da regra |
|---|---:|---:|---|---|
| bancos | 0% | 1,00 | nenhuma | nenhuma |
| utilities | 19% | 1,00 | nenhuma | nenhuma |
| concessoes | 32% | 0,99 | nenhuma | nenhuma |
| incorporadoras | 0% | 1,00 | nenhuma | nenhuma |
| varejo | 12% | 0,99 | nenhuma | nenhuma |
| locadoras | 73% | 0,98 | nenhuma | nenhuma |
| shoppings | -3% | 1,00 | nenhuma | nenhuma |

Sensibilidade da proposta às escolhas mais discutíveis (os demais setores ficam na proposta):

| Variante | Regra (7) | Top 7 upside | Spearman upside vs base | P(MC): CEAB3 / LREN3 / SBFG3 / DIRR3 / COGN3 |
|---|---|---|---:|---|
| varejo DDM 60 / Múlt 20 / DCF 20 | BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3 | 0,93 | 51% / 37% / 42% / 49% / 67% |
| varejo DDM 50 / Múlt 30 / DCF 20 (proposta) | BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3 | 0,93 | 61% / 55% / 51% / 49% / 67% |
| varejo DDM 40 / Múlt 40 / DCF 20 | BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, LREN3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, CEAB3, MDNE3 | 0,92 | 70% / 71% / 59% / 49% / 67% |
| incorporadoras no padrão 50/25/25 | BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3 | BEEF3, VTRU3, PLPL3, TEND3, SEER3, COGN3, HAPV3 | 0,92 | 61% / 55% / 51% / 54% / 67% |
| demais com DCF 30 / DDM 45 / Múlt 25 | BEEF3, VTRU3, PLPL3, CEAB3, MDNE3, SEER3, TEND3 | BEEF3, VTRU3, PLPL3, HAPV3, TEND3, SEER3, MDNE3 | 0,92 | 61% / 55% / 51% / 49% / 68% |

## Achados sobre o motor e limitações

- **DCF negativo entra como zero e mantém o peso** (`max(0, x)` no blend). Isso ocorre em 33 empresas (MOVI3, VAMO3, ECOR3, MOTV3, RAIL3, MGLU3, SBFG3, ASAI3, GMAT3, JHSF3, SMFT3, CVCB3, AURE3, ENGI11, EQTL3, CPLE3, ALUP11, SBSP3, TTEN3, ENEV3, VALE3, CBAV3, KLBN11, RAPT4, DXCO3, AXIA3, CMIG4, CPFE3, ISAE4, CSMG3, SAPR11, PNVL3, JSLG3): cada 10 p.p. de peso no DCF corta cerca de 10% do valor justo, sem informação nova. Melhor seria tirar o método do blend quando o patrimônio do DCF for negativo, ou trocá-lo pelo DDM.
- **Os múltiplos-alvo não são coerentes com Ke 25%.** Um P/L de 9–12x com g 5% e ROE 17% equivale a um custo de capital próprio de cerca de 11–13%. A P/L justa a Ke 25%, g 5% e ROE 15–20% fica em 3,5–4x. Na mediana, o valor por múltiplos é 2,30× o do DDM. Por isso o peso dos múltiplos é o principal motor do upside, e os pesos propostos limitam os múltiplos a 20–40%.
- **O DCF é o método mais disperso** (tabela de diagnóstico). Com o patrimônio residual EV − DL, um erro pequeno no EV vira um erro grande no valor por ação quando a DL é grande. O peso padrão de 50% no DCF é a maior fonte de fragilidade do valor justo nos setores alavancados.
- **Holding com controlada de valor justo zero:** `value_holding` testa `models[tk].get('fair_value')` pela verdade do valor, então 0,0 vira o valor de mercado da controlada. Isso afeta SIMH3 quando MOVI3 ou VAMO3 chegam a zero, por exemplo com peso 100% no DCF.
- **Choque de ±2 p.p. de margem é desproporcional em negócios de margem fina** (BEEF3 cerca de 8,5%, ASAI3, GMAT3 e VBBR3 com 4–6%): em BEEF3, −2 p.p. levam a TIR de 27,2% a 8,6% e o upside de 89% a -62%. Isso explica boa parte da faixa p5–p95 larga desses nomes na amostra conjunta.
- **Kd +300 bp nos bancos:** o template financeiro não tem custo de dívida, então esses choques não mudam bancos. Margem ±2 p.p. vira ROE ±2 p.p. no template financeiro, que é a convenção do motor.
- Na amostra conjunta e no MC ×1,5, a regra de oportunidades não é recalculada (P(MC) exigiria um Monte Carlo por combinação). No MC ×1,5, os sorteios são independentes entre empresas, o caso conservador para a estabilidade do ranking.

## Como reproduzir

```bash
.venv/bin/python pipeline/tests/robustness.py            # completo
.venv/bin/python pipeline/tests/robustness.py --quick    # rápido (menos sorteios)
```

Parâmetros desta rodada: amostra conjunta de 3.000 combinações, MC ×1,5 com 2.000 sorteios por empresa e P(MC) com 5.000 sorteios. Tempo: 639 s.
