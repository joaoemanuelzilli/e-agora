# Robustez do valuation: pesos do blend e premissas (foto de 28/10/2026)

Gerado em 2026-11-18T14:31:43 por `pipeline/tests/robustness.py`, com o motor `pipeline/model.py` sem alteração e a foto de preços `data/market/quotes.json`. São 122 empresas (5 holdings por SOTP). Ke base de 25%. Dados para gráfico: `data/tests/robustness.json`.

## Resumo

- **A TIR implícita não depende dos pesos, do Ke nem dos múltiplos.** Ela é a taxa que zera o DDM ao preço de hoje, então só muda com g, margem, crescimento, Kd e Monte Carlo. O ranking por TIR é estável: Spearman mediano de 0,93 (mínimo 0,76) na amostra conjunta de 3.000 combinações.
- **No ranking por upside, a ordem geral resiste aos pesos, mas o topo não.** Nas 66 combinações de pesos, o Spearman mediano é 0,91 (mínimo 0,79), porém só 77% do top 7 por upside se mantém em média. Na amostra conjunta, o Spearman mediano é 0,85 (mínimo 0,53). Causa: na mediana, os múltiplos-alvo valem 2,37× o DDM a Ke 25%, e 35 empresas têm DCF negativo, que o motor trunca em zero sem tirar o peso.
- **Lista robusta por TIR** (top 7 na amostra conjunta): ≥ 80%: MDNE3, PLPL3, TEND3, VTRU3; ≥ 50%: MDNE3, PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3.
- **Lista robusta por upside** (top 7 na amostra conjunta): ≥ 80%: VTRU3, TEND3; ≥ 50%: VTRU3, TEND3, PLPL3, SEER3, BEEF3, HAPV3.
- **Núcleo robusto** (top 7 por TIR e por upside em ≥ 50% da amostra conjunta): PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3. Em todas as grades ao mesmo tempo (≥ 50% em cada uma): TIR nenhuma; upside BEEF3.
- **As 8 oportunidades atuais (VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3, CEAB3, COGN3) dependem dos pesos e já das revisões.** Com as premissas revisadas e os pesos atuais, a regra do `build.py` seleciona 8 (BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3). Nos 66 vetores de pesos (upside, P(MC) e escore recalculados), a regra mantém em média 6,8 das 8 (mínimo 5) e a lista sai idêntica em 20%. Fração de vetores com cada empresa selecionada: VTRU3 100%; BEEF3 100%; SEER3 97% (qualquer w_múlt; qualquer w_DCF); MDNE3 92% (qualquer w_múlt; w_DCF ≤ 0,8); PLPL3 100%; TEND3 74% (w_múlt ≤ 0,6; w_DCF ≥ 0,2); CEAB3 61% (w_múlt ≥ 0,3; w_DCF ≤ 0,5); COGN3 59% (w_múlt entre 0,1 e 0,7, irregular; w_DCF entre 0,0 e 0,9, irregular).
- **Pesos propostos por setor:** o Spearman do upside contra a base fica em 0,92 e o do escore em 0,99. A regra passa a selecionar BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, TEND3, SBFG3, contra BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3 hoje. O peso dos múltiplos no varejo decide a cauda da lista: varejo DDM 60 / Múlt 20 / DCF 20: BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3; varejo DDM 50 / Múlt 30 / DCF 20 (proposta): BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, TEND3, SBFG3; varejo DDM 40 / Múlt 40 / DCF 20: BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, SBFG3, TEND3.

## Base e reprodução

A base é o motor rodado agora com as premissas atuais. Ele reproduz o `overview.json` (2026-11-18T14:19:04) em valor justo e TIR, exceto em 0 empresas cujas premissas (ou cuja controlada) mudaram depois do build: nenhuma. A P(MC) difere da do app em 11 empresas sem mudança no valor justo (revisão de desvios em `uncertainty`): CYRE3 44,0% → 33,1%, MDNE3 76,5% → 61,7%, MRVE3 16,2% → 36,5%, PLPL3 80,2% → 87,0%, DIRR3 45,2% → 49,5%, CURY3 19,2% → 18,5%, TEND3 77,0% → 88,0%, BBAS3 25,0% → 36,7%, BBDC4 0,8% → 15,5%, BRSR6 7,4% → 22,3%, BBDC3 12,9% → 46,5%. Com as premissas atuais, a regra de oportunidades seleciona BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3.

Com TIR ≥ 20% e P(MC) a até 5 p.p. do corte de 45%: CEAB3 (46,5%), DIRR3 (49,5%), ANIM3 (44,6%), POMO4 (47,7%). Para essas empresas, a seleção depende de detalhes (sorteios, pesos, revisões).

Top 7 da base por TIR: HAPV3, PLPL3, MDNE3, BEEF3, VTRU3, TEND3, COGN3. Top 7 por upside: BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3.

## Estabilidade do ranking por grade

Spearman de cada combinação contra a base (mediana / mínimo), fração média do top 7 da base que continua no top 7 e número médio de oportunidades atuais que a regra mantém (de 8).

| Grade | Combinações | Spearman TIR | Spearman upside | Spearman escore | Top 7 TIR mantido | Top 7 upside mantido | Oportunidades mantidas |
|---|---:|---|---|---|---:|---:|---:|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | 66 | 1,00 / 1,00 (invariante) | 0,91 / 0,79 | 0,99 / 0,96 | 100% | 77% | 6,8 |
| Ke 20–30% (passo 1 p.p.) | 11 | 1,00 / 1,00 (invariante) | 0,99 / 0,97 | 1,00 / 1,00 | 100% | 83% | 7,3 |
| g terminal −2 a +2 p.p. | 5 | 1,00 / 0,99 | 1,00 / 1,00 | 1,00 / 0,99 | 100% | 94% | 7,6 |
| Múltiplos-alvo −30% a +30% | 7 | 1,00 / 1,00 (invariante) | 0,99 / 0,96 | 1,00 / 0,99 | 100% | 84% | 7,4 |
| Margem EBITDA × crescimento ±2 p.p. | 25 | 0,97 / 0,86 | 0,96 / 0,85 | 0,98 / 0,91 | 79% | 77% | 6,3 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | 3 | 0,93 / 0,93 | 0,98 / 0,98 | 0,97 / 0,96 | 81% | 86% | 7,0 |
| Monte Carlo com desvios ×1,5 | 2000 | 0,74 / 0,52 | 0,73 / 0,52 | — | 44% | 40% | — |
| Amostra conjunta de todas as grades | 3000 | 0,93 / 0,76 | 0,85 / 0,53 | — | 76% | 64% | — |

Na amostra conjunta e no MC ×1,5, o escore e a regra não são recalculados, porque exigiriam um Monte Carlo por combinação. Nas grades determinísticas, P(MC) é recalculada com o Monte Carlo do motor (5.000 sorteios, semente 7).

## Frequência no top 7 e no top 15 por empresa

Frequências na amostra conjunta (C), na grade de pesos (P) e no Monte Carlo ×1,5 (MC). A faixa p5–p95 do valor justo é a da amostra conjunta. A tabela lista as empresas que aparecem no top 15 da base ou em pelo menos 5% das combinações; as demais estão no JSON.

| Empresa | Preço | VJ base | VJ p5–p95 (C) | TIR base (rank) | Upside base (rank) | Top 7 TIR C | Top 15 TIR C | Top 7 TIR MC | Top 7 upside C | Top 15 upside C | Top 7 upside P | Top 7 upside MC | Regra (pesos) |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| VTRU3 ★ | 11,98 | 16,69 | 11,23–23,25 | 26,3% (5) | 39% (2) | 90% | 100% | 40% | 91% | 100% | 100% | 48% | 100% |
| TEND3 ★ | 21,22 | 26,34 | 19,52–38,63 | 25,0% (6) | 24% (5) | 92% | 100% | 39% | 81% | 97% | 80% | 38% | 74% |
| PLPL3 ★ | 4,84 | 6,25 | 4,30–9,13 | 27,8% (2) | 29% (3) | 100% | 100% | 50% | 76% | 91% | 76% | 41% | 100% |
| MDNE3 ★ | 16,86 | 19,81 | 13,62–25,67 | 27,1% (3) | 17% (6) | 100% | 100% | 46% | 43% | 85% | 33% | 28% | 92% |
| SEER3 ★ | 11,03 | 13,81 | 8,99–19,68 | 24,1% (8) | 25% (4) | 61% | 100% | 25% | 71% | 100% | 82% | 36% | 97% |
| HAPV3 | 4,21 | 4,42 | 0,33–13,87 | 29,3% (1) | 5% (9) | 70% | 84% | 50% | 53% | 61% | 68% | 42% | 0% |
| BEEF3 ★ | 2,87 | 5,04 | 0,11–11,27 | 26,9% (4) | 76% (1) | 53% | 61% | 49% | 63% | 70% | 100% | 59% | 100% |
| COGN3 ★ | 1,69 | 1,89 | 1,02–3,08 | 24,2% (7) | 12% (7) | 30% | 100% | 32% | 20% | 90% | 68% | 30% | 59% |
| PINE4 | 10,66 | 9,34 | 7,49–13,24 | 22,4% (12) | -12% (20) | 29% | 94% | 22% | 4% | 49% | 0% | 3% | 0% |
| CEAB3 ★ | 6,87 | 6,65 | 2,68–13,62 | 21,8% (14) | -3% (14) | 0% | 80% | 24% | 25% | 66% | 32% | 26% | 61% |
| CYRE3 | 17,74 | 17,36 | 12,13–23,98 | 22,3% (13) | -2% (12) | 16% | 97% | 16% | 2% | 56% | 0% | 6% | 0% |
| DIRR3 | 8,60 | 8,41 | 6,18–12,13 | 21,7% (15) | -2% (13) | 8% | 76% | 14% | 14% | 68% | 3% | 10% | 9% |
| PGMN3 | 2,63 | 2,13 | 0,20–5,92 | 20,7% (17) | -19% (26) | 19% | 40% | 16% | 28% | 43% | 11% | 17% | 9% |
| SBFG3 | 5,08 | 3,48 | 0,79–10,51 | 22,7% (11) | -32% (38) | 19% | 57% | 30% | 18% | 36% | 20% | 18% | 42% |
| POMO4 | 3,89 | 3,85 | 2,72–5,68 | 21,1% (16) | -1% (11) | 0% | 68% | 18% | 2% | 77% | 0% | 16% | 0% |
| EZTC3 | 9,59 | 10,69 | 6,80–14,84 | 17,1% (30) | 11% (8) | 0% | 4% | 1% | 36% | 73% | 23% | 6% | 0% |
| ANIM3 | 2,43 | 2,19 | 0,27–5,00 | 22,9% (9) | -10% (18) | 3% | 62% | 25% | 14% | 36% | 0% | 32% | 0% |
| MOVI3 | 6,62 | 4,17 | 0,14–13,32 | 22,9% (10) | -37% (45) | 9% | 40% | 35% | 12% | 24% | 5% | 26% | 0% |
| LREN3 | 9,31 | 8,47 | 5,15–15,49 | 19,8% (19) | -9% (17) | 0% | 9% | 8% | 7% | 57% | 0% | 6% | 0% |
| CSAN3 | 2,37 | 2,10 | 1,51–3,48 | — (—) | -12% (19) | — | — | — | 16% | 46% | 0% | 0% | 0% |
| BBAS3 | 16,84 | 15,50 | 9,89–21,10 | 20,4% (18) | -8% (15) | 0% | 46% | 8% | 0% | 12% | 0% | 2% | 0% |
| BBDC3 | 13,40 | 12,31 | 8,40–17,28 | 19,7% (20) | -8% (16) | 0% | 27% | 3% | 0% | 30% | 0% | 0% | 0% |
| CURY3 | 26,37 | 22,20 | 16,46–31,27 | 19,3% (22) | -16% (21) | 0% | 29% | 9% | 0% | 22% | 0% | 4% | 0% |
| SIMH3 | 5,24 | 2,24 | -1,10–10,53 | — (—) | -57% (74) | — | — | — | 9% | 17% | 0% | 17% | 0% |
| LWSA3 | 3,41 | 2,82 | 1,82–4,69 | 14,7% (43) | -17% (23) | 0% | 0% | 0% | 2% | 22% | 0% | 1% | 0% |
| RAPT4 | 3,67 | 1,92 | 0,23–6,85 | 15,7% (34) | -48% (59) | 0% | 0% | 9% | 5% | 14% | 0% | 16% | 0% |
| ECOR3 | 5,27 | 2,14 | 0,00–8,89 | 17,5% (27) | -59% (78) | 0% | 2% | 8% | 5% | 9% | 0% | 0% | 0% |
| MRVE3 | 4,27 | 2,17 | 0,68–6,66 | 12,9% (66) | -49% (62) | 0% | 0% | 8% | 2% | 16% | 0% | 13% | 0% |
| BRSR6 | 12,94 | 10,68 | 6,99–15,01 | 19,1% (23) | -17% (24) | 0% | 12% | 7% | 0% | 1% | 0% | 1% | 0% |
| YDUQ3 | 8,76 | 6,57 | 2,41–12,27 | 19,4% (21) | -25% (28) | 0% | 3% | 16% | 1% | 6% | 0% | 14% | 0% |
| RIAA3 | 6,33 | 4,52 | 1,55–9,90 | 17,4% (28) | -29% (33) | 0% | 0% | 9% | 0% | 8% | 0% | 12% | 0% |
| BBDC4 | 14,71 | 12,31 | 8,40–17,28 | 18,4% (24) | -16% (22) | 0% | 6% | 1% | 0% | 1% | 0% | 0% | 0% |
| DESK3 | 19,32 | 19,46 | 1,30–19,30 | 10,5% (91) | 1% (10) | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% |

★ = oportunidade atual. A coluna “Regra (pesos)” dá a fração das 66 combinações de pesos em que a regra do app (TIR ≥ 20%, P(MC) ≥ 45%, Altman fora de risco, confiança não baixa, ordem pelo escore) põe a empresa entre as 8.

### Faixa p5–p95 do valor justo por grade (todas as empresas)

| Empresa | Preço | VJ base | Pesos | Ke | g | Múltiplos | Margem × cresc. | Kd | MC ×1,5 | Conjunta |
|---|---:|---:|---|---|---|---|---|---|---|---|
| BEEF3 | 2,87 | 5,04 | 3,70–5,70 | 3,61–7,18 | 4,95–5,08 | 4,24–5,84 | 0,69–10,39 | 3,97–4,52 | 0,35–14,73 | 0,11–11,27 |
| VTRU3 | 11,98 | 16,69 | 13,83–19,10 | 14,05–20,78 | 16,67–16,69 | 15,05–18,33 | 14,33–19,19 | 16,04–16,36 | 8,50–28,01 | 11,23–23,25 |
| PLPL3 | 4,84 | 6,25 | 5,80–7,06 | 5,35–7,69 | 6,23–6,26 | 5,72–6,79 | 5,00–7,57 | 6,20–6,23 | 2,82–11,56 | 4,30–9,13 |
| SEER3 | 11,03 | 13,81 | 11,21–16,59 | 11,68–17,09 | 13,64–13,92 | 12,35–15,28 | 11,49–16,28 | 13,16–13,47 | 6,94–22,77 | 8,99–19,68 |
| TEND3 | 21,22 | 26,34 | 23,24–31,53 | 23,16–31,38 | 26,24–26,43 | 23,80–28,88 | 21,80–31,08 | 26,23–26,32 | 13,06–49,01 | 19,52–38,63 |
| MDNE3 | 16,86 | 19,81 | 16,31–21,43 | 17,42–23,64 | 19,67–19,90 | 17,82–21,80 | 17,59–22,13 | 19,70–19,77 | 11,69–33,46 | 13,62–25,67 |
| COGN3 | 1,69 | 1,89 | 1,60–2,53 | 1,50–2,48 | 1,88–1,89 | 1,61–2,17 | 1,40–2,41 | 1,69–1,80 | 0,59–3,69 | 1,02–3,08 |
| EZTC3 | 9,59 | 10,69 | 7,03–13,90 | 10,05–11,70 | 10,34–10,96 | 10,03–11,35 | 10,09–11,32 | 10,69–10,71 | 8,86–13,38 | 6,80–14,84 |
| HAPV3 | 4,21 | 4,42 | 2,57–7,91 | 3,21–7,48 | 4,04–4,69 | 3,17–5,68 | 1,26–11,39 | 3,13–3,93 | 0,00–24,76 | 0,33–13,87 |
| DESK3 | 19,32 | 19,46 | 1,50–16,28 | 19,46–19,46 | 19,46–19,46 | 10,28–28,63 | 17,54–21,43 | 19,38–19,45 | 18,53–20,43 | 1,30–19,30 |
| POMO4 | 3,89 | 3,85 | 3,22–4,96 | 3,42–4,55 | 3,84–3,86 | 3,50–4,21 | 3,17–4,57 | 3,85–3,85 | 2,02–6,66 | 2,72–5,68 |
| CYRE3 | 17,74 | 17,36 | 14,76–20,59 | 15,35–20,53 | 17,08–17,55 | 15,53–19,18 | 15,33–19,48 | 17,04–17,28 | 11,41–25,66 | 12,13–23,98 |
| DIRR3 | 8,60 | 8,41 | 7,47–10,17 | 7,37–10,09 | 8,33–8,51 | 7,55–9,27 | 7,41–9,47 | 8,38–8,40 | 5,13–13,07 | 6,18–12,13 |
| CEAB3 | 6,87 | 6,65 | 4,43–11,69 | 5,45–8,53 | 6,24–6,95 | 5,52–7,78 | 4,02–9,40 | 6,18–6,44 | 1,57–15,24 | 2,68–13,62 |
| BBAS3 | 16,84 | 15,50 | 12,33–18,00 | 13,91–18,13 | 15,00–15,89 | 13,31–17,69 | 14,00–17,13 | 15,50–15,50 | 11,12–21,13 | 9,89–21,10 |
| BBDC3 | 13,40 | 12,31 | 9,84–15,31 | 11,24–14,04 | 12,11–12,46 | 10,58–14,04 | 11,38–13,28 | 12,31–12,31 | 10,12–14,86 | 8,40–17,28 |
| LREN3 | 9,31 | 8,47 | 6,15–13,68 | 7,53–9,97 | 8,32–8,58 | 7,37–9,57 | 6,69–10,34 | 8,36–8,43 | 4,74–13,30 | 5,15–15,49 |
| ANIM3 | 2,43 | 2,19 | 1,85–2,97 | 1,19–4,08 | 2,06–2,27 | 1,46–2,92 | 0,85–3,70 | 1,45–1,81 | 0,00–8,01 | 0,27–5,00 |
| CSAN3 | 2,37 | 2,10 | 1,56–3,31 | 2,08–2,12 | 2,07–2,12 | 1,88–2,32 | 2,01–2,19 | 1,99–2,09 | 1,79–2,66 | 1,51–3,48 |
| PINE4 | 10,66 | 9,34 | 9,15–11,02 | 8,24–11,14 | 9,33–9,34 | 8,30–10,38 | 8,69–10,03 | 9,34–9,34 | 6,00–13,99 | 7,49–13,24 |
| CURY3 | 26,37 | 22,20 | 19,43–26,76 | 19,72–26,19 | 21,82–22,65 | 19,87–24,54 | 19,58–24,97 | 22,21–22,31 | 13,15–36,11 | 16,46–31,27 |
| BBDC4 | 14,71 | 12,31 | 9,84–15,31 | 11,24–14,04 | 12,11–12,46 | 10,58–14,04 | 11,38–13,28 | 12,31–12,31 | 10,08–14,94 | 8,40–17,28 |
| LWSA3 | 3,41 | 2,82 | 1,93–4,28 | 2,62–3,15 | 2,81–2,83 | 2,53–3,11 | 2,51–3,15 | 2,82–2,86 | 1,94–3,91 | 1,82–4,69 |
| BRSR6 | 12,94 | 10,68 | 8,89–12,75 | 9,64–12,39 | 10,10–11,14 | 9,24–12,13 | 9,52–11,93 | 10,68–10,68 | 7,37–14,73 | 6,99–15,01 |
| VULC3 | 11,77 | 9,55 | 7,60–13,86 | 8,42–11,36 | 9,53–9,57 | 8,47–10,64 | 8,03–11,15 | 9,42–9,51 | 6,13–13,73 | 6,39–15,76 |
| PGMN3 | 2,63 | 2,13 | 1,29–4,04 | 1,57–2,96 | 1,95–2,25 | 1,65–2,61 | 0,51–4,71 | 1,73–1,94 | 0,57–5,08 | 0,20–5,92 |
| CBAV3 | 11,30 | 8,92 | 0,30–8,90 | 8,89–8,97 | 8,90–8,93 | 5,72–12,12 | 6,33–11,58 | 8,25–8,85 | 2,48–17,91 | 0,18–10,09 |
| YDUQ3 | 8,76 | 6,57 | 5,52–8,94 | 4,70–9,37 | 6,48–6,65 | 5,33–7,81 | 3,79–9,53 | 5,37–6,11 | 1,58–16,39 | 2,41–12,27 |
| PSSA3 | 46,89 | 34,93 | 21,97–42,70 | 32,85–38,32 | 34,83–34,99 | 28,46–41,39 | 32,25–37,71 | 34,93–34,93 | 28,46–42,64 | 19,36–47,36 |
| GRND3 | 3,65 | 2,72 | 2,03–3,58 | 2,55–2,97 | 2,69–2,74 | 2,50–2,93 | 2,43–3,02 | 2,72–2,77 | 2,01–3,62 | 1,93–3,92 |
| VIVA3 | 17,63 | 13,03 | 9,34–21,13 | 11,50–15,46 | 12,88–13,13 | 11,29–14,77 | 11,28–14,86 | 12,80–12,95 | 9,12–17,97 | 7,98–23,72 |
| ITSA4 | 12,91 | 9,54 | 7,24–12,29 | 8,85–10,64 | 9,51–9,55 | 8,15–10,92 | 9,06–10,04 | 9,52–9,54 | 8,44–10,76 | 6,49–13,71 |
| RIAA3 | 6,33 | 4,52 | 2,80–8,42 | 3,70–5,79 | 4,22–4,73 | 3,69–5,35 | 2,45–6,69 | 4,15–4,37 | 0,87–10,92 | 1,55–9,90 |
| LEVE3 | 31,17 | 21,70 | 18,60–28,67 | 18,63–26,47 | 21,21–22,27 | 19,32–24,07 | 17,82–25,77 | 21,26–21,49 | 12,53–34,14 | 14,95–33,25 |
| MDIA3 | 15,73 | 10,90 | 7,28–17,76 | 10,01–12,29 | 10,66–11,08 | 9,57–12,23 | 7,81–14,13 | 10,91–10,98 | 5,12–18,49 | 6,04–20,31 |
| ABCB4 | 23,05 | 15,94 | 13,22–19,01 | 14,33–18,58 | 15,54–16,24 | 13,78–18,10 | 14,51–17,47 | 15,94–15,94 | 12,68–19,92 | 10,84–22,05 |
| PRIO3 | 72,29 | 49,53 | 43,40–61,08 | 45,11–55,80 | 49,15–49,79 | 44,35–54,71 | 44,92–54,44 | 48,47–49,00 | 19,68–97,09 | 38,09–69,61 |
| SBFG3 | 5,08 | 3,48 | 1,04–8,38 | 3,25–4,60 | 3,39–3,55 | 2,41–4,55 | 1,87–6,71 | 3,05–3,44 | 0,45–11,84 | 0,79–10,51 |
| SANB11 | 24,33 | 16,50 | 12,24–20,58 | 15,14–18,70 | 16,18–16,74 | 14,03–18,98 | 15,18–17,90 | 16,50–16,50 | 13,22–20,05 | 10,37–23,16 |
| SAUD3 | 14,64 | 9,90 | 6,45–11,97 | 9,31–10,88 | 9,90–9,90 | 8,10–11,70 | 9,30–10,51 | 9,90–9,90 | 8,04–11,83 | 5,71–13,31 |
| GGPS3 | 10,89 | 7,29 | 4,95–12,47 | 6,33–8,82 | 7,29–7,29 | 6,20–8,38 | 4,57–10,14 | 7,09–7,20 | 4,11–11,33 | 3,50–14,80 |
| BBSE3 | 41,40 | 27,57 | 22,46–30,63 | 25,69–30,54 | 27,20–28,00 | 23,16–31,98 | 26,88–28,26 | 27,57–27,57 | 23,09–32,98 | 19,79–34,73 |
| TFCO4 | 10,08 | 6,62 | 4,24–11,50 | 5,84–7,89 | 6,58–6,66 | 5,69–7,55 | 5,60–7,68 | 6,55–6,59 | 3,93–10,43 | 3,68–12,78 |
| SLCE3 | 16,88 | 10,96 | 5,08–15,61 | 9,22–13,52 | 10,88–11,03 | 9,17–12,75 | 8,62–13,42 | 9,50–10,27 | 2,72–31,57 | 3,60–17,10 |
| MOVI3 | 6,62 | 4,17 | 1,27–9,76 | 3,83–7,08 | 4,10–4,22 | 1,94–6,40 | 2,51–7,58 | 2,50–4,00 | 0,00–23,22 | 0,14–13,32 |
| AUAU3 | 3,86 | 2,41 | 1,47–4,52 | 2,09–2,90 | 2,35–2,45 | 2,00–2,82 | 1,59–3,27 | 2,29–2,37 | 0,87–4,37 | 1,07–5,15 |
| ITUB4 | 39,90 | 24,45 | 18,57–31,11 | 22,60–27,41 | 24,41–24,47 | 20,86–28,04 | 23,26–25,68 | 24,45–24,45 | 21,41–27,67 | 16,47–34,78 |
| IRBR3 | 56,58 | 34,55 | 28,19–43,55 | 31,68–39,09 | 33,53–35,33 | 29,79–39,31 | 31,24–38,02 | 34,55–34,55 | 24,99–45,44 | 23,58–49,72 |
| USIM5 | 5,68 | 3,38 | 2,12–5,75 | 3,06–3,87 | 3,04–3,64 | 2,92–3,84 | 2,13–4,68 | 3,37–3,40 | 0,30–9,64 | 1,52–6,74 |
| BMOB3 | 24,42 | 14,47 | 10,90–21,54 | 12,97–16,93 | 14,35–14,60 | 12,86–16,07 | 11,86–17,19 | 14,48–14,60 | 9,66–20,90 | 9,55–24,54 |
| IGTI11 | 22,70 | 13,44 | 9,05–23,03 | 11,67–16,21 | 13,30–13,59 | 11,41–15,46 | 12,00–14,97 | 12,85–13,26 | 10,26–17,19 | 7,55–25,55 |
| CXSE3 | 21,16 | 12,00 | 8,00–14,39 | 11,33–13,07 | 11,92–12,09 | 9,84–14,16 | 11,49–12,51 | 12,00–12,00 | 10,35–13,69 | 7,20–16,01 |
| MULT3 | 25,84 | 14,54 | 9,76–25,27 | 12,43–17,85 | 14,37–14,74 | 12,26–16,82 | 12,91–16,28 | 13,82–14,31 | 10,85–18,99 | 8,12–27,98 |
| TIMS3 | 19,00 | 10,68 | 8,91–14,67 | 9,10–13,05 | 10,51–10,88 | 9,31–12,05 | 9,00–12,46 | 10,00–10,40 | 7,89–14,06 | 7,07–16,77 |
| INTB3 | 14,36 | 8,01 | 5,66–13,12 | 7,34–9,07 | 7,90–8,09 | 7,02–8,99 | 6,48–9,60 | 8,02–8,13 | 5,08–12,00 | 4,97–14,89 |
| ABEV3 | 15,18 | 8,45 | 6,05–13,03 | 7,73–9,58 | 8,40–8,50 | 7,47–9,42 | 7,61–9,33 | 8,46–8,53 | 6,38–11,07 | 5,66–14,50 |
| NATU3 | 5,02 | 2,72 | 1,75–4,79 | 2,20–3,51 | 2,67–2,74 | 2,21–3,22 | 1,21–4,27 | 2,50–2,62 | 0,49–7,92 | 0,85–6,07 |
| PETR4 | 52,73 | 28,04 | 21,51–42,96 | 23,54–34,95 | 26,97–28,80 | 23,91–32,17 | 23,55–32,79 | 26,82–27,42 | 7,94–69,99 | 17,21–48,93 |
| RAPT4 | 3,67 | 1,92 | 0,54–5,08 | 1,83–2,08 | 1,89–1,95 | 0,94–2,90 | 1,03–2,85 | 1,76–1,91 | 0,00–10,50 | 0,23–6,85 |
| BPAC11 | 56,38 | 29,32 | 18,44–42,07 | 26,75–33,60 | 29,25–29,34 | 24,39–34,25 | 27,65–31,11 | 29,32–29,32 | 24,26–35,33 | 15,98–46,51 |
| ALOS3 | 24,44 | 12,58 | 8,70–21,31 | 10,78–15,34 | 12,44–12,73 | 10,62–14,53 | 11,05–14,20 | 11,91–12,39 | 9,18–16,49 | 7,21–23,72 |
| MRVE3 | 4,27 | 2,17 | 1,92–4,45 | 1,70–2,86 | 1,94–2,34 | 1,99–2,35 | 0,70–3,94 | 1,16–1,97 | 0,00–8,26 | 0,68–6,66 |
| B3SA3 | 14,66 | 7,39 | 5,32–11,69 | 6,76–8,38 | 7,33–7,47 | 6,50–8,28 | 6,89–7,93 | 7,37–7,44 | 5,82–9,47 | 4,96–12,95 |
| RENT3 | 29,74 | 14,82 | 8,06–30,09 | 11,54–20,20 | 13,98–15,40 | 11,49–18,16 | 9,88–20,31 | 12,46–13,82 | 6,31–32,24 | 4,95–34,16 |
| GOAU4 | 10,62 | 5,10 | 3,47–8,72 | 4,53–5,99 | 4,76–5,37 | 4,33–5,87 | 3,63–6,65 | 4,99–5,06 | 1,02–12,23 | 2,63–10,01 |
| ALPA4 | 13,35 | 6,40 | 4,08–10,69 | 5,81–7,34 | 6,37–6,42 | 5,58–7,22 | 5,48–7,37 | 6,35–6,38 | 3,99–9,44 | 3,74–11,80 |
| TOTS3 | 34,09 | 16,27 | 10,08–29,47 | 14,61–18,90 | 16,21–16,32 | 13,81–18,72 | 13,97–18,69 | 15,88–16,17 | 11,35–21,97 | 8,94–32,75 |
| HYPE3 | 21,60 | 10,30 | 7,12–17,51 | 8,74–12,69 | 9,80–10,66 | 8,62–11,98 | 8,45–12,25 | 9,56–10,04 | 6,10–15,21 | 5,72–19,68 |
| PETR3 | 59,12 | 28,04 | 21,51–42,96 | 23,54–34,95 | 26,97–28,80 | 23,91–32,17 | 23,55–32,79 | 26,82–27,42 | 8,29–70,50 | 17,21–48,93 |
| VIVT3 | 30,85 | 14,05 | 9,95–23,39 | 12,17–16,94 | 13,86–14,28 | 11,95–16,16 | 11,65–16,61 | 13,39–13,84 | 10,31–18,28 | 8,18–26,29 |
| MILS3 | 15,56 | 6,98 | 4,48–12,60 | 5,96–8,58 | 6,84–7,08 | 5,82–8,14 | 5,96–8,06 | 6,63–6,84 | 3,67–11,59 | 3,69–14,04 |
| AZZA3 | 15,07 | 6,53 | 4,67–10,70 | 4,88–9,06 | 6,11–6,83 | 5,27–7,80 | 2,97–13,04 | 5,32–6,12 | 0,01–25,59 | 1,23–16,54 |
| SMFT3 | 15,99 | 6,85 | 1,80–18,42 | 6,52–7,83 | 6,83–6,86 | 4,73–8,97 | 5,70–8,05 | 5,64–6,73 | 2,90–15,40 | 1,31–19,86 |
| SIMH3 | 5,24 | 2,24 | -0,17–6,91 | 2,02–4,51 | 2,14–2,32 | 0,32–4,22 | 0,83–5,36 | 1,01–2,12 | -0,02–12,28 | -1,10–10,53 |
| RECV3 | 11,14 | 4,73 | 2,24–9,94 | 3,99–5,85 | 4,36–5,01 | 3,70–5,76 | 3,70–5,82 | 4,47–4,63 | 1,75–13,19 | 1,78–11,13 |
| PNVL3 | 10,56 | 4,36 | 1,10–11,84 | 4,18–5,06 | 4,31–4,40 | 3,13–5,59 | 1,75–8,69 | 3,85–4,31 | 2,11–8,39 | 0,43–15,02 |
| FLRY3 | 21,67 | 8,88 | 5,20–17,24 | 7,68–10,74 | 8,66–9,04 | 7,28–10,49 | 6,84–11,02 | 8,34–8,73 | 5,51–12,75 | 4,16–19,26 |
| ECOR3 | 5,27 | 2,14 | 0,66–4,97 | 1,96–2,42 | 2,12–2,15 | 0,76–3,93 | 1,38–2,94 | 1,77–2,10 | 0,07–4,60 | 0,00–8,89 |
| GGBR4 | 23,99 | 9,63 | 6,57–16,44 | 8,53–11,32 | 8,99–10,12 | 8,18–11,08 | 6,86–12,54 | 9,41–9,55 | 1,96–23,05 | 4,98–18,88 |
| RADL3 | 15,67 | 6,23 | 2,64–14,38 | 5,37–7,64 | 6,16–6,28 | 4,93–7,54 | 3,34–9,77 | 5,83–6,13 | 3,70–9,66 | 1,55–16,79 |
| RDOR3 | 33,80 | 13,03 | 8,33–23,64 | 10,69–16,74 | 12,93–13,09 | 10,71–15,36 | 9,72–16,53 | 12,07–12,68 | 7,66–19,71 | 6,01–26,90 |
| OPCT3 | 8,92 | 3,43 | 1,63–7,53 | 2,80–4,87 | 2,98–3,74 | 2,47–4,39 | 2,44–4,76 | 2,66–3,04 | 0,76–11,56 | 0,97–8,62 |
| TUPY3 | 15,41 | 5,80 | 1,85–13,45 | 5,32–8,59 | 5,66–6,23 | 4,14–7,47 | 2,69–12,72 | 5,18–5,69 | 0,00–28,61 | 1,30–18,00 |
| UGPA3 | 32,70 | 12,12 | 8,42–20,39 | 10,68–14,35 | 11,94–12,25 | 10,33–13,92 | 2,48–23,56 | 11,80–11,98 | 5,66–20,41 | 1,59–29,89 |
| VAMO3 | 2,57 | 0,95 | 0,28–2,26 | 0,88–1,51 | 0,92–0,97 | 0,42–1,48 | 0,65–1,42 | 0,54–0,91 | 0,07–3,77 | 0,04–2,95 |
| MOTV3 | 14,61 | 5,34 | 1,60–13,70 | 5,07–6,49 | 5,33–5,34 | 3,74–6,93 | 4,73–5,97 | 4,71–5,27 | 3,70–9,01 | 1,29–15,10 |
| GMAT3 | 3,54 | 1,22 | 0,37–3,12 | 1,15–1,44 | 1,20–1,24 | 0,88–1,57 | 0,35–2,83 | 1,11–1,21 | 0,54–2,56 | 0,12–4,35 |
| ORVR3 | 15,73 | 5,37 | 2,00–12,84 | 4,70–6,43 | 5,17–5,52 | 4,19–6,55 | 4,49–6,30 | 5,08–5,27 | 3,01–8,66 | 1,61–14,20 |
| RAIL3 | 14,40 | 4,86 | 1,09–13,46 | 4,70–5,18 | 4,85–4,87 | 3,30–6,42 | 4,23–5,53 | 4,10–4,79 | 2,72–8,87 | 0,82–14,70 |
| BRAV3 | 18,45 | 6,04 | 1,81–15,26 | 5,76–8,05 | 5,99–6,17 | 3,86–8,23 | 4,98–8,84 | 5,51–5,99 | 0,33–34,48 | 1,60–17,87 |
| PRNR3 | 12,96 | 4,21 | 1,26–10,97 | 3,87–6,47 | 4,09–4,27 | 2,76–5,66 | 2,25–8,16 | 3,41–4,00 | 0,93–17,36 | 0,68–13,50 |
| TTEN3 | 10,63 | 3,45 | 1,00–8,98 | 3,26–4,55 | 3,40–3,50 | 2,53–4,37 | 1,47–7,39 | 3,16–3,42 | 0,74–10,64 | 0,59–11,69 |
| EMBJ3 | 96,75 | 30,42 | 17,12–54,46 | 27,34–35,45 | 30,12–30,61 | 26,10–34,73 | 23,70–37,43 | 30,22–30,34 | 16,41–50,34 | 15,10–60,89 |
| SAPR11 | 32,42 | 10,19 | 3,06–25,52 | 9,59–12,66 | 9,95–10,38 | 7,40–12,98 | 8,92–11,52 | 9,48–10,12 | 6,38–18,87 | 2,61–28,30 |
| LOGG3 | 21,52 | 6,28 | 3,66–12,27 | 5,03–8,08 | 6,09–6,40 | 4,78–7,78 | 4,80–7,84 | 4,62–5,93 | 1,53–14,70 | 2,20–13,17 |
| UNIP6 | 50,61 | 14,75 | 9,95–24,93 | 11,82–19,15 | 14,20–15,14 | 12,10–17,40 | 9,84–19,89 | 13,41–14,31 | 0,00–62,33 | 6,48–29,31 |
| SUZB3 | 48,19 | 13,87 | 7,79–25,25 | 10,50–23,31 | 12,82–15,27 | 9,90–17,84 | 9,30–20,32 | 9,30–11,40 | 0,57–67,98 | 3,55–31,43 |
| ALUP11 | 31,94 | 9,15 | 2,74–23,58 | 8,71–12,27 | 9,05–9,24 | 5,82–12,48 | 8,15–10,21 | 8,06–9,04 | 6,93–15,39 | 2,11–26,82 |
| CPFE3 | 42,97 | 12,31 | 3,69–30,43 | 11,72–14,07 | 12,22–12,39 | 8,82–15,81 | 10,35–14,37 | 11,00–12,18 | 8,45–19,15 | 3,01–33,79 |
| ASAI3 | 7,81 | 2,22 | 0,67–5,27 | 2,05–2,69 | 2,20–2,24 | 1,23–3,21 | 0,01–6,97 | 1,56–2,16 | 0,57–5,61 | 0,00–9,46 |
| JSLG3 | 5,62 | 1,54 | 0,48–3,51 | 1,40–2,79 | 1,50–1,56 | 0,59–2,67 | 0,47–4,98 | 1,47–1,53 | 0,00–10,45 | 0,00–7,64 |
| JHSF3 | 9,50 | 2,59 | 0,51–4,09 | 2,39–2,91 | 2,51–2,64 | 2,17–3,00 | 2,33–2,86 | 2,26–2,55 | 1,25–4,68 | 0,44–4,49 |
| TAEE11 | 40,04 | 10,50 | 6,97–18,30 | 8,15–13,79 | 8,36–12,22 | 8,09–12,91 | 8,15–13,01 | 7,84–9,60 | 6,21–15,71 | 3,61–20,64 |
| MGLU3 | 5,14 | 1,31 | 0,07–4,04 | 1,29–1,33 | 1,29–1,33 | 0,14–2,61 | 0,00–2,58 | 1,22–1,30 | 0,00–4,96 | 0,00–5,92 |
| EGIE3 | 27,30 | 6,93 | 2,08–17,68 | 6,62–9,07 | 6,87–7,01 | 4,82–9,04 | 6,13–8,44 | 6,14–6,85 | 4,97–11,43 | 1,86–19,64 |
| DXCO3 | 4,61 | 1,16 | 0,33–3,04 | 1,10–1,30 | 1,12–1,19 | 0,72–1,60 | 0,78–1,64 | 0,95–1,14 | 0,44–4,06 | 0,21–3,86 |
| CMIG4 | 10,15 | 2,52 | 0,76–6,07 | 2,38–2,74 | 2,49–2,54 | 1,71–3,33 | 1,88–3,19 | 2,17–2,48 | 1,35–3,89 | 0,56–7,04 |
| CSMG3 | 49,96 | 11,83 | 3,21–31,51 | 11,33–12,64 | 11,76–11,88 | 8,36–15,30 | 10,11–13,62 | 10,32–11,68 | 6,96–17,39 | 2,22–34,39 |
| WEGE3 | 47,38 | 11,14 | 5,60–23,36 | 10,19–12,70 | 11,08–11,21 | 9,22–13,06 | 9,59–12,76 | 11,08–11,12 | 7,94–15,19 | 4,94–25,94 |
| ENGI11 | 45,24 | 9,80 | 2,12–27,26 | 9,48–10,31 | 9,72–9,85 | 5,09–14,50 | 6,38–13,33 | 6,90–9,51 | 4,07–17,15 | 0,35–33,86 |
| SBSP3 | 24,90 | 5,33 | 1,03–15,08 | 5,16–5,62 | 5,29–5,37 | 3,63–7,03 | 4,74–5,95 | 4,69–5,27 | 3,73–7,24 | 0,76–16,50 |
| BRAP4 | 18,02 | 3,80 | 1,72–7,83 | 3,78–3,82 | 3,71–3,88 | 2,71–4,89 | 2,84–4,80 | 3,39–3,76 | 0,82–11,85 | 1,42–9,36 |
| VBBR3 | 30,76 | 6,19 | 2,42–13,70 | 5,42–8,71 | 6,13–6,21 | 4,59–7,79 | 0,00–20,79 | 5,44–5,92 | 1,26–20,22 | 0,00–26,30 |
| ISAE4 | 25,24 | 5,01 | 1,37–13,33 | 4,86–5,24 | 4,97–5,05 | 3,06–6,96 | 4,25–5,81 | 3,64–4,88 | 3,31–6,98 | 0,57–14,86 |
| CPLE3 | 14,67 | 2,75 | 0,82–6,90 | 2,62–2,94 | 2,72–2,76 | 1,94–3,55 | 2,20–3,31 | 2,37–2,71 | 1,75–3,93 | 0,61–7,64 |
| KLBN11 | 17,63 | 3,19 | 1,24–6,46 | 2,93–7,11 | 3,19–3,94 | 1,73–4,65 | 2,33–5,86 | 2,34–3,10 | 0,43–17,57 | 0,50–9,50 |
| AXIA3 | 48,18 | 7,69 | 2,21–20,10 | 7,42–8,10 | 7,59–7,76 | 4,66–10,71 | 6,36–9,08 | 6,58–7,58 | 3,14–13,05 | 1,41–23,15 |
| EQTL3 | 34,07 | 5,14 | 1,00–14,51 | 4,97–5,40 | 5,09–5,17 | 2,64–7,63 | 3,42–6,91 | 3,54–4,98 | 2,60–8,83 | 0,22–20,03 |
| CVCB3 | 0,88 | 0,13 | 0,00–0,41 | 0,13–0,13 | 0,13–0,13 | 0,00–0,38 | 0,04–0,22 | 0,12–0,13 | 0,00–1,29 | 0,00–0,90 |
| AURE3 | 11,06 | 1,56 | 0,30–4,39 | 1,49–1,66 | 1,54–1,57 | 0,27–3,20 | 0,82–2,33 | 1,27–1,53 | 0,00–5,15 | 0,00–7,27 |
| VALE3 | 61,08 | 7,18 | 2,18–16,86 | 6,92–7,55 | 7,06–7,27 | 4,55–9,80 | 4,87–9,58 | 6,18–7,08 | 0,00–26,55 | 1,43–20,60 |
| ENEV3 | 26,49 | 2,79 | 0,76–7,42 | 2,64–3,23 | 2,76–2,81 | 1,66–3,91 | 2,14–3,46 | 2,10–2,72 | 1,08–7,29 | 0,43–8,68 |

## Lista robusta

Empresas no top 7 em pelo menos 80% ou 50% das combinações de cada grade.

| Grade | TIR ≥ 80% | TIR ≥ 50% | Upside ≥ 80% | Upside ≥ 50% |
|---|---|---|---|---|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | BEEF3, VTRU3, SEER3, TEND3 | BEEF3, VTRU3, SEER3, TEND3, PLPL3, COGN3, HAPV3 |
| Ke 20–30% (passo 1 p.p.) | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | PLPL3, BEEF3, SEER3, VTRU3, TEND3 | PLPL3, BEEF3, SEER3, VTRU3, TEND3, MDNE3 |
| g terminal −2 a +2 p.p. | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3 | MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3, COGN3 |
| Múltiplos-alvo −30% a +30% | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, VTRU3 | PLPL3, TEND3, BEEF3, SEER3, VTRU3 | PLPL3, TEND3, BEEF3, SEER3, VTRU3, MDNE3 |
| Margem EBITDA × crescimento ±2 p.p. | MDNE3, PLPL3, TEND3, HAPV3, VTRU3 | MDNE3, PLPL3, TEND3, HAPV3, VTRU3, BEEF3 | PLPL3, SEER3, VTRU3, TEND3 | PLPL3, SEER3, VTRU3, TEND3, MDNE3, BEEF3 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | MDNE3, PLPL3, TEND3, HAPV3, VTRU3 | MDNE3, PLPL3, TEND3, HAPV3, VTRU3, PINE4, SEER3 | EZTC3, MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3 | EZTC3, MDNE3, PLPL3, TEND3, BEEF3, SEER3, VTRU3 |
| Monte Carlo com desvios ×1,5 | nenhuma | nenhuma | nenhuma | BEEF3 |
| Amostra conjunta de todas as grades | MDNE3, PLPL3, TEND3, VTRU3 | MDNE3, PLPL3, TEND3, VTRU3, HAPV3, SEER3, BEEF3 | VTRU3, TEND3 | VTRU3, TEND3, PLPL3, SEER3, BEEF3, HAPV3 |
| Em todas as grades ao mesmo tempo | nenhuma | nenhuma | nenhuma | BEEF3 |

## As 8 oportunidades atuais e os pesos

Para cada um dos 66 vetores de pesos, o teste recalcula o upside, a P(valor justo > preço) e o escore e reaplica a regra do `build.py`. A P(MC) sai do mesmo Monte Carlo do motor, com os valores por método guardados em cada sorteio e o blend refeito. A TIR e os demais fatores do escore não dependem dos pesos.

| Empresa | Selecionada (% dos pesos) | Condição (≥ 50% dos vetores) | P(MC) mín–máx | Upside mín–máx | Seleção por w_múlt = 0; 0,1; …; 1 | Seleção por w_DCF = 0; 0,1; …; 1 |
|---|---:|---|---|---|---|---|
| VTRU3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 61%–100% | 8%–65% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| BEEF3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 56%–91% | 12%–100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| PLPL3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 68%–95% | 16%–50% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| SEER3 ★ | 97% | qualquer w_múlt; qualquer w_DCF | 40%–99% | -5%–58% | 82% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 91% 90% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| MDNE3 ★ | 92% | qualquer w_múlt; w_DCF ≤ 0,8 | 34%–89% | -8%–32% | 64% 90% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 75% 67% 0% 0% |
| TEND3 ★ | 74% | w_múlt ≤ 0,6; w_DCF ≥ 0,2 | 49%–96% | 0%–49% | 100% 100% 89% 88% 71% 67% 60% 25% 0% 0% 0% | 18% 40% 78% 100% 100% 100% 100% 100% 100% 100% 100% |
| CEAB3 ★ | 61% | w_múlt ≥ 0,3; w_DCF ≤ 0,5 | 19%–97% | -44%–93% | 0% 0% 44% 100% 100% 100% 100% 100% 100% 100% 100% | 82% 80% 78% 75% 57% 50% 40% 25% 0% 0% 0% |
| COGN3 ★ | 59% | w_múlt entre 0,1 e 0,7, irregular; w_DCF entre 0,0 e 0,9, irregular | 43%–97% | -6%–63% | 0% 100% 89% 75% 86% 67% 40% 50% 33% 0% 0% | 55% 50% 44% 50% 71% 83% 80% 75% 67% 50% 0% |
| SBFG3 | 42% | w_múlt ≥ 0,5; w_DCF ≤ 0,2 | 5%–88% | -91%–87% | 0% 10% 22% 38% 43% 67% 100% 100% 100% 100% 100% | 91% 80% 67% 38% 14% 0% 0% 0% 0% 0% 0% |
| PGMN3 | 9% | w_múlt ≥ 0,8; nenhum w_DCF | 8%–95% | -63%–74% | 0% 0% 0% 0% 0% 0% 0% 25% 67% 100% 100% | 36% 20% 0% 0% 0% 0% 0% 0% 0% 0% 0% |
| DIRR3 | 9% | nenhum w_múlt; w_DCF entre 0,8 e 0,9 | 20%–89% | -17%–24% | 0% 20% 44% 0% 0% 0% 0% 0% 0% 0% 0% | 0% 0% 0% 0% 0% 17% 20% 25% 67% 50% 0% |

Quantas das 8 atuais a regra mantém, em número de combinações: 5 mantidas: 6, 6 mantidas: 12, 7 mantidas: 35.

Seleção pela regra nas demais grades (fração de combinações em que cada empresa está entre as 7):

- Pesos do blend {DCF, DDM, múltiplos} (passo 0,1): PLPL3 100%, BEEF3 100%, VTRU3 100%, SEER3 97%, MDNE3 92%, TEND3 74%, CEAB3 61%, COGN3 59%, SBFG3 42%, PGMN3 9%, DIRR3 9% (lista idêntica em 20%).
- Ke 20–30% (passo 1 p.p.): MDNE3 100%, PLPL3 100%, TEND3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, COGN3 73%, CEAB3 55% (lista idêntica em 55%).
- g terminal −2 a +2 p.p.: MDNE3 100%, PLPL3 100%, TEND3 100%, COGN3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, CEAB3 60%, DIRR3 40% (lista idêntica em 60%).
- Múltiplos-alvo −30% a +30%: MDNE3 100%, PLPL3 100%, TEND3 100%, BEEF3 100%, SEER3 100%, VTRU3 100%, COGN3 86%, CEAB3 57% (lista idêntica em 57%).
- Margem EBITDA × crescimento ±2 p.p.: MDNE3 100%, PLPL3 100%, SEER3 100%, VTRU3 100%, TEND3 72%, BEEF3 68%, CEAB3 52%, PGMN3 40%, COGN3 36%, SBFG3 28%, DIRR3 4% (lista idêntica em 12%).
- Kd +300 bp (WACC / resultado financeiro / ambos): MDNE3 100%, PLPL3 100%, TEND3 100%, COGN3 100%, BEEF3 100%, SEER3 100%, VTRU3 100% (lista idêntica em 0%).
- Monte Carlo com desvios ×1,5 (P(MC) recalculada com os pesos da base): BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3.

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
| bancos | 4 | 0 | 1,63 | — | — | — | 0,79 | 0,68 | DCF 0.0 / DDM 0.6 / Múlt 0.4 |
| utilities | 6 | 6 | 5,32 | -4,23 | 52% | — | 1,89 | 1,43 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| concessoes | 4 | 3 | 3,87 | -0,61 | 50% | 2,07 | 0,96 | 0,99 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| incorporadoras | 9 | 1 | 1,50 | 1,17 | 15% | 0,70 | 0,64 | 0,75 | DCF 0.0 / DDM 0.7 / Múlt 0.3 |
| varejo | 13 | 4 | 2,37 | 0,69 | 39% | 2,35 | 1,38 | 1,40 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| locadoras | 3 | 2 | 2,05 | -0,44 | 80% | 5,13 | 1,89 | 2,51 | DCF 0.0 / DDM 0.9 / Múlt 0.1 |
| shoppings | 3 | 0 | 2,56 | 0,80 | 26% | 1,10 | 0,66 | 0,74 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| demais | 75 | 19 | 2,28 | 0,71 | 33% | 1,24 | 0,85 | 0,94 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |

Impacto dos pesos propostos (empresas cujo rank por upside ou cuja seleção muda, além do top 15 de cada lado):

| Empresa | Setor | VJ base → proposto | Δ VJ | Upside base → proposto | Rank upside | P(MC) base → proposta | Rank escore | Regra |
|---|---|---|---:|---|---|---|---|---|
| BEEF3 | demais | 5,04 → 5,04 | 0% | 76% → 76% | 1 → 1 | 75% → 75% | 1 → 1 | mantém |
| VTRU3 | demais | 16,69 → 16,69 | 0% | 39% → 39% | 2 → 2 | 90% → 90% | 2 → 2 | mantém |
| PLPL3 | incorporadoras | 6,25 → 6,25 | 0% | 29% → 29% | 3 → 3 | 87% → 80% | 3 → 5 | mantém |
| SEER3 | demais | 13,81 → 13,81 | 0% | 25% → 25% | 4 → 4 | 81% → 81% | 6 → 7 | mantém |
| TEND3 | incorporadoras | 26,34 → 26,34 | 0% | 24% → 24% | 5 → 5 | 88% → 77% | 8 → 9 | mantém |
| MDNE3 | incorporadoras | 19,81 → 19,81 | 0% | 17% → 17% | 6 → 6 | 62% → 76% | 7 → 6 | mantém |
| COGN3 | demais | 1,89 → 1,89 | 0% | 12% → 12% | 7 → 7 | 62% → 62% | 9 → 12 | sai |
| MOVI3 | locadoras | 4,17 → 7,29 | 75% | -37% → 10% | 45 → 8 | 29% → 55% | 14 → 8 | — |
| CEAB3 | varejo | 6,65 → 7,55 | 14% | -3% → 10% | 14 → 9 | 47% → 59% | 5 → 4 | mantém |
| HAPV3 | demais | 4,42 → 4,42 | 0% | 5% → 5% | 9 → 10 | 51% → 51% | 4 → 3 | — |
| LREN3 | varejo | 8,47 → 9,26 | 9% | -9% → -1% | 17 → 11 | 31% → 48% | 11 → 11 | — |
| SBFG3 | varejo | 3,48 → 5,05 | 45% | -32% → -1% | 38 → 12 | 25% → 49% | 16 → 10 | entra |
| POMO4 | demais | 3,85 → 3,85 | 0% | -1% → -1% | 11 → 13 | 48% → 48% | 12 → 15 | — |
| BBDC3 | demais | 12,31 → 13,26 | 8% | -8% → -1% | 16 → 14 | 46% → 46% | 25 → 22 | — |
| CYRE3 | incorporadoras | 17,36 → 17,36 | 0% | -2% → -2% | 12 → 15 | 33% → 44% | 21 → 17 | — |
| DIRR3 | incorporadoras | 8,41 → 8,41 | 0% | -2% → -2% | 13 → 16 | 49% → 45% | 24 → 24 | — |
| EZTC3 | incorporadoras | 10,69 → 9,38 | -12% | 11% → -2% | 8 → 17 | 92% → 41% | 15 → 26 | — |
| BBAS3 | bancos | 15,50 → 15,50 | 0% | -8% → -8% | 15 → 21 | 37% → 25% | 17 → 23 | — |
| DESK3 | demais | 19,46 → 6,01 | -69% | 1% → -69% | 10 → 96 | 63% → 0% | 85 → 119 | — |

Top 7 por upside: base BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3; proposto BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3. Regra de oportunidades: base BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, COGN3; proposto BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, TEND3, SBFG3.

Decomposição, aplicando os pesos propostos a um setor por vez (os demais ficam na base):

| Setor alterado | Δ VJ mediano do setor | Spearman upside vs base | Entram na regra | Saem da regra |
|---|---:|---:|---|---|
| bancos | 0% | 1,00 | nenhuma | nenhuma |
| utilities | 18% | 1,00 | nenhuma | nenhuma |
| concessoes | 31% | 0,99 | nenhuma | nenhuma |
| incorporadoras | 0% | 1,00 | nenhuma | nenhuma |
| varejo | 14% | 0,99 | SBFG3 | COGN3 |
| locadoras | 72% | 0,98 | nenhuma | nenhuma |
| shoppings | -3% | 1,00 | nenhuma | nenhuma |

Sensibilidade da proposta às escolhas mais discutíveis (os demais setores ficam na proposta):

| Variante | Regra (7) | Top 7 upside | Spearman upside vs base | P(MC): CEAB3 / LREN3 / SBFG3 / DIRR3 / COGN3 |
|---|---|---|---:|---|
| varejo DDM 60 / Múlt 20 / DCF 20 | BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3 | 0,92 | 48% / 29% / 40% / 45% / 62% |
| varejo DDM 50 / Múlt 30 / DCF 20 (proposta) | BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, TEND3, SBFG3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, MDNE3, COGN3 | 0,92 | 59% / 48% / 49% / 45% / 62% |
| varejo DDM 40 / Múlt 40 / DCF 20 | BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, SBFG3, TEND3 | BEEF3, VTRU3, PLPL3, SEER3, TEND3, CEAB3, MDNE3 | 0,91 | 68% / 66% / 58% / 45% / 62% |
| incorporadoras no padrão 50/25/25 | BEEF3, VTRU3, PLPL3, CEAB3, SEER3, MDNE3, TEND3, SBFG3 | BEEF3, VTRU3, PLPL3, TEND3, SEER3, COGN3, MOVI3 | 0,92 | 59% / 48% / 49% / 49% / 62% |
| demais com DCF 30 / DDM 45 / Múlt 25 | BEEF3, VTRU3, CEAB3, PLPL3, MDNE3, SEER3, TEND3, SBFG3 | BEEF3, VTRU3, PLPL3, TEND3, HAPV3, SEER3, MDNE3 | 0,92 | 59% / 48% / 49% / 45% / 63% |

## Achados sobre o motor e limitações

- **DCF negativo entra como zero e mantém o peso** (`max(0, x)` no blend). Isso ocorre em 35 empresas (MOVI3, VAMO3, ECOR3, MOTV3, RAIL3, MGLU3, SBFG3, ASAI3, GMAT3, JHSF3, SMFT3, CVCB3, AURE3, ENGI11, EQTL3, CPLE3, ALUP11, SBSP3, TTEN3, BRAV3, ENEV3, VALE3, CBAV3, KLBN11, RAPT4, DXCO3, AXIA3, CMIG4, EGIE3, CPFE3, ISAE4, CSMG3, SAPR11, PNVL3, JSLG3): cada 10 p.p. de peso no DCF corta cerca de 10% do valor justo, sem informação nova. Melhor seria tirar o método do blend quando o patrimônio do DCF for negativo, ou trocá-lo pelo DDM.
- **Os múltiplos-alvo não são coerentes com Ke 25%.** Um P/L de 9–12x com g 5% e ROE 17% equivale a um custo de capital próprio de cerca de 11–13%. A P/L justa a Ke 25%, g 5% e ROE 15–20% fica em 3,5–4x. Na mediana, o valor por múltiplos é 2,37× o do DDM. Por isso o peso dos múltiplos é o principal motor do upside, e os pesos propostos limitam os múltiplos a 20–40%.
- **O DCF é o método mais disperso** (tabela de diagnóstico). Com o patrimônio residual EV − DL, um erro pequeno no EV vira um erro grande no valor por ação quando a DL é grande. O peso padrão de 50% no DCF é a maior fonte de fragilidade do valor justo nos setores alavancados.
- **Holding com controlada de valor justo zero:** `value_holding` testa `models[tk].get('fair_value')` pela verdade do valor, então 0,0 vira o valor de mercado da controlada. Isso afeta SIMH3 quando MOVI3 ou VAMO3 chegam a zero, por exemplo com peso 100% no DCF.
- **Choque de ±2 p.p. de margem é desproporcional em negócios de margem fina** (BEEF3 cerca de 8,5%, ASAI3, GMAT3 e VBBR3 com 4–6%): em BEEF3, −2 p.p. levam a TIR de 26,9% a 8,7% e o upside de 76% a -73%. Isso explica boa parte da faixa p5–p95 larga desses nomes na amostra conjunta.
- **Kd +300 bp nos bancos:** o template financeiro não tem custo de dívida, então esses choques não mudam bancos. Margem ±2 p.p. vira ROE ±2 p.p. no template financeiro, que é a convenção do motor.
- Na amostra conjunta e no MC ×1,5, a regra de oportunidades não é recalculada (P(MC) exigiria um Monte Carlo por combinação). No MC ×1,5, os sorteios são independentes entre empresas, o caso conservador para a estabilidade do ranking.

## Como reproduzir

```bash
.venv/bin/python pipeline/tests/robustness.py            # completo
.venv/bin/python pipeline/tests/robustness.py --quick    # rápido (menos sorteios)
```

Parâmetros desta rodada: amostra conjunta de 3.000 combinações, MC ×1,5 com 2.000 sorteios por empresa e P(MC) com 5.000 sorteios. Tempo: 758 s.
