# Robustez do valuation: pesos do blend e premissas (26/10/2026)

Gerado em 2026-10-26T16:40:16 por `pipeline/tests/robustness.py`, com o motor `pipeline/model.py` sem alteração e a foto de preços `data/market/quotes.json`. São 59 empresas (2 holdings por SOTP). Ke base de 25%. Dados para gráfico: `data/tests/robustness.json`.

## Resumo

- **A TIR implícita não depende dos pesos, do Ke nem dos múltiplos.** Ela é a taxa que zera o DDM ao preço de hoje, então só muda com g, margem, crescimento, Kd e Monte Carlo. O ranking por TIR é estável: Spearman mediano de 0,92 (mínimo 0,65) na amostra conjunta de 3.000 combinações.
- **No ranking por upside, a ordem geral resiste aos pesos, mas o topo não.** Nas 66 combinações de pesos, o Spearman mediano é 0,95 (mínimo 0,78), porém só 74% do top 7 por upside se mantém em média. Na amostra conjunta, o Spearman mediano é 0,86 (mínimo 0,44). Causa: na mediana, os múltiplos-alvo valem 2,34× o DDM a Ke 25%, e 19 empresas têm DCF negativo, que o motor trunca em zero sem tirar o peso.
- **Lista robusta por TIR** (top 7 na amostra conjunta): ≥ 80%: MDNE3, PLPL3, TEND3; ≥ 50%: MDNE3, PLPL3, TEND3, HAPV3, DIRR3, BEEF3.
- **Lista robusta por upside** (top 7 na amostra conjunta): ≥ 80%: TEND3; ≥ 50%: TEND3, PLPL3, BEEF3, DIRR3, HAPV3, CEAB3.
- **Núcleo robusto** (top 7 por TIR e por upside em ≥ 50% da amostra conjunta): PLPL3, TEND3, HAPV3, DIRR3, BEEF3. Em todas as grades ao mesmo tempo (≥ 50% em cada uma): TIR MDNE3, PLPL3, TEND3, HAPV3; upside PLPL3, TEND3, BEEF3.
- **As 7 oportunidades atuais (BEEF3, PLPL3, TEND3, MDNE3, COGN3) dependem dos pesos e já das revisões.** Com as premissas revisadas e os pesos atuais, a regra do `build.py` seleciona 5 (BEEF3, PLPL3, TEND3, DIRR3, COGN3); MDNE3 ficou fora pelos filtros de P(MC) ≥ 45% ou TIR ≥ 20%. Nos 66 vetores de pesos (upside, P(MC) e escore recalculados), a regra mantém em média 3,6 das 7 (mínimo 3) e a lista sai idêntica em 0%. Fração de vetores com cada empresa selecionada: BEEF3 100%; PLPL3 100%; TEND3 100%; MDNE3 47% (w_múlt ≥ 0,4; w_DCF ≤ 0,3); COGN3 17% (w_múlt = 0,3; w_DCF = 0,5).
- **Pesos propostos por setor:** o Spearman do upside contra a base fica em 0,94 e o do escore em 0,99. A regra passa a selecionar BEEF3, PLPL3, CEAB3, TEND3, MDNE3, LREN3, COGN3, contra BEEF3, PLPL3, TEND3, DIRR3, COGN3 hoje. O peso dos múltiplos no varejo decide a cauda da lista: varejo DDM 60 / Múlt 20 / DCF 20: BEEF3, PLPL3, TEND3, MDNE3, COGN3; varejo DDM 50 / Múlt 30 / DCF 20 (proposta): BEEF3, PLPL3, CEAB3, TEND3, MDNE3, LREN3, COGN3; varejo DDM 40 / Múlt 40 / DCF 20: BEEF3, CEAB3, PLPL3, LREN3, MDNE3, TEND3, SBFG3.

## Base e reprodução

A base é o motor rodado agora com as premissas atuais. Ele reproduz o `overview.json` (2026-10-26T16:32:54) em valor justo e TIR, exceto em 0 empresas cujas premissas (ou cuja controlada) mudaram depois do build: nenhuma. A P(MC) difere da do app em 10 empresas sem mudança no valor justo (revisão de desvios em `uncertainty`): CYRE3 20,7% → 14,2%, MDNE3 53,9% → 36,5%, MRVE3 11,4% → 32,4%, PLPL3 64,8% → 73,4%, DIRR3 40,5% → 46,3%, CURY3 20,2% → 20,1%, TEND3 73,2% → 86,2%, BBAS3 17,8% → 29,1%, BBDC4 0,1% → 6,6%, BRSR6 1,4% → 7,6%. Com as premissas atuais, a regra de oportunidades seleciona BEEF3, PLPL3, TEND3, DIRR3, COGN3.

Com TIR ≥ 20% e P(MC) a até 5 p.p. do corte de 45%: CEAB3 (43,9%), DIRR3 (46,3%), COGN3 (47,1%), ANIM3 (45,3%), HAPV3 (48,7%). Para essas empresas, a seleção depende de detalhes (sorteios, pesos, revisões).

Top 7 da base por TIR: HAPV3, PLPL3, MDNE3, BEEF3, TEND3, COGN3, DIRR3. Top 7 por upside: BEEF3, TEND3, PLPL3, MDNE3, COGN3, HAPV3, DIRR3.

## Estabilidade do ranking por grade

Spearman de cada combinação contra a base (mediana / mínimo), fração média do top 7 da base que continua no top 7 e número médio de oportunidades atuais que a regra mantém (de 7).

| Grade | Combinações | Spearman TIR | Spearman upside | Spearman escore | Top 7 TIR mantido | Top 7 upside mantido | Oportunidades mantidas |
|---|---:|---|---|---|---:|---:|---:|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | 66 | 1,00 / 1,00 (invariante) | 0,95 / 0,78 | 0,99 / 0,96 | 100% | 74% | 3,6 |
| Ke 20–30% (passo 1 p.p.) | 11 | 1,00 / 1,00 (invariante) | 0,99 / 0,96 | 1,00 / 1,00 | 100% | 84% | 3,8 |
| g terminal −2 a +2 p.p. | 5 | 1,00 / 0,99 | 1,00 / 1,00 | 1,00 / 0,99 | 94% | 91% | 5,0 |
| Múltiplos-alvo −30% a +30% | 7 | 1,00 / 1,00 (invariante) | 0,98 / 0,97 | 1,00 / 1,00 | 100% | 88% | 4,0 |
| Margem EBITDA × crescimento ±2 p.p. | 25 | 0,96 / 0,83 | 0,93 / 0,74 | 0,98 / 0,91 | 79% | 70% | 3,0 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | 3 | 0,90 / 0,90 | 0,98 / 0,97 | 0,97 / 0,97 | 81% | 81% | 3,3 |
| Monte Carlo com desvios ×1,5 | 2000 | 0,76 / 0,45 | 0,72 / 0,26 | — | 48% | 46% | — |
| Amostra conjunta de todas as grades | 3000 | 0,92 / 0,65 | 0,86 / 0,44 | — | 76% | 60% | — |

Na amostra conjunta e no MC ×1,5, o escore e a regra não são recalculados, porque exigiriam um Monte Carlo por combinação. Nas grades determinísticas, P(MC) é recalculada com o Monte Carlo do motor (5.000 sorteios, semente 7).

## Frequência no top 7 e no top 15 por empresa

Frequências na amostra conjunta (C), na grade de pesos (P) e no Monte Carlo ×1,5 (MC). A faixa p5–p95 do valor justo é a da amostra conjunta. A tabela lista as empresas que aparecem no top 15 da base ou em pelo menos 5% das combinações; as demais estão no JSON.

| Empresa | Preço | VJ base | VJ p5–p95 (C) | TIR base (rank) | Upside base (rank) | Top 7 TIR C | Top 15 TIR C | Top 7 TIR MC | Top 7 upside C | Top 15 upside C | Top 7 upside P | Top 7 upside MC | Regra (pesos) |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TEND3 ★ | 22,38 | 26,81 | 19,91–39,25 | 24,4% (5) | 20% (2) | 100% | 100% | 54% | 95% | 100% | 100% | 60% | 100% |
| PLPL3 ★ | 5,70 | 6,37 | 4,40–9,32 | 25,2% (2) | 12% (3) | 100% | 100% | 55% | 75% | 94% | 77% | 50% | 100% |
| MDNE3 ★ | 19,66 | 20,19 | 14,04–25,96 | 24,5% (3) | 3% (4) | 100% | 100% | 53% | 49% | 90% | 38% | 39% | 47% |
| DIRR3 | 8,97 | 8,59 | 6,40–12,28 | 21,4% (7) | -4% (7) | 62% | 100% | 31% | 55% | 95% | 47% | 28% | 23% |
| HAPV3 | 5,00 | 4,82 | 0,36–14,03 | 26,6% (1) | -4% (6) | 72% | 89% | 53% | 54% | 62% | 76% | 45% | 0% |
| BEEF3 ★ | 3,38 | 5,44 | 0,21–11,60 | 24,5% (4) | 61% (1) | 53% | 62% | 52% | 66% | 74% | 100% | 64% | 100% |
| COGN3 ★ | 2,01 | 1,97 | 1,10–3,11 | 21,8% (6) | -2% (5) | 42% | 100% | 36% | 28% | 97% | 77% | 39% | 17% |
| CEAB3 | 7,35 | 6,91 | 2,94–13,73 | 21,1% (9) | -6% (8) | 4% | 100% | 35% | 50% | 85% | 59% | 38% | 58% |
| LREN3 | 9,51 | 8,79 | 5,51–15,61 | 20,1% (12) | -8% (10) | 0% | 100% | 22% | 48% | 97% | 50% | 24% | 50% |
| CYRE3 | 20,13 | 17,76 | 12,65–24,23 | 20,7% (11) | -12% (13) | 41% | 95% | 23% | 14% | 71% | 0% | 16% | 0% |
| PGMN3 | 2,94 | 2,27 | 0,20–5,98 | 19,5% (17) | -23% (18) | 30% | 44% | 24% | 36% | 47% | 21% | 26% | 0% |
| CURY3 | 26,94 | 22,89 | 17,29–31,63 | 19,5% (16) | -15% (14) | 23% | 72% | 23% | 18% | 67% | 0% | 18% | 0% |
| ANIM3 | 2,74 | 2,54 | 0,36–5,22 | 21,4% (8) | -7% (9) | 16% | 80% | 35% | 27% | 50% | 23% | 40% | 0% |
| SBFG3 | 5,88 | 3,52 | 0,83–10,71 | 21,0% (10) | -40% (23) | 33% | 66% | 36% | 21% | 40% | 21% | 23% | 35% |
| BBAS3 | 17,57 | 15,67 | 10,11–21,26 | 20,0% (13) | -11% (11) | 22% | 84% | 21% | 2% | 66% | 0% | 14% | 0% |
| EZTC3 | 12,12 | 10,69 | 6,95–14,83 | 14,6% (25) | -12% (12) | 0% | 7% | 1% | 23% | 60% | 0% | 7% | 0% |
| YDUQ3 | 8,48 | 7,10 | 2,77–12,55 | 20,0% (14) | -16% (15) | 0% | 54% | 32% | 5% | 46% | 0% | 31% | 0% |
| VULC3 | 12,49 | 9,70 | 6,57–15,82 | 17,4% (20) | -22% (17) | 0% | 26% | 6% | 1% | 52% | 0% | 6% | 0% |
| BBDC4 | 15,47 | 12,37 | 8,49–17,31 | 17,9% (19) | -20% (16) | 0% | 40% | 4% | 0% | 37% | 0% | 2% | 0% |
| MOVI3 | 8,67 | 4,19 | 0,17–13,59 | 19,6% (15) | -52% (35) | 0% | 29% | 34% | 6% | 19% | 0% | 29% | 0% |
| BRSR6 | 14,67 | 10,91 | 7,30–15,22 | 17,9% (18) | -26% (19) | 0% | 39% | 12% | 0% | 18% | 0% | 3% | 0% |
| CSAN3 | 2,97 | 2,10 | 1,52–3,48 | — (—) | -29% (20) | — | — | — | 8% | 35% | 0% | 1% | 0% |
| MRVE3 | 4,98 | 2,34 | 0,86–7,04 | 11,8% (42) | -53% (36) | 0% | 0% | 9% | 7% | 28% | 11% | 15% | 0% |
| ECOR3 | 5,45 | 2,15 | 0,00–8,90 | 17,2% (21) | -61% (41) | 0% | 6% | 17% | 7% | 14% | 0% | 1% | 0% |
| VIVA3 | 19,47 | 13,31 | 8,30–23,82 | 15,4% (22) | -32% (21) | 0% | 7% | 0% | 1% | 18% | 0% | 1% | 0% |
| SIMH3 | 6,87 | 3,84 | 0,99–10,27 | — (—) | -44% (25) | — | — | — | 3% | 20% | 0% | 24% | 0% |
| GGPS3 | 12,03 | 7,47 | 3,68–14,85 | 14,5% (26) | -38% (22) | 0% | 0% | 0% | 0% | 6% | 0% | 2% | 0% |

★ = oportunidade atual. A coluna “Regra (pesos)” dá a fração das 66 combinações de pesos em que a regra do app (TIR ≥ 20%, P(MC) ≥ 45%, Altman fora de risco, confiança não baixa, ordem pelo escore) põe a empresa entre as 7.

### Faixa p5–p95 do valor justo por grade (todas as empresas)

| Empresa | Preço | VJ base | Pesos | Ke | g | Múltiplos | Margem × cresc. | Kd | MC ×1,5 | Conjunta |
|---|---:|---:|---|---|---|---|---|---|---|---|
| BEEF3 | 3,38 | 5,44 | 3,78–6,17 | 4,01–7,58 | 5,35–5,47 | 4,64–6,24 | 0,86–10,84 | 4,40–4,94 | 0,37–15,17 | 0,21–11,60 |
| TEND3 | 22,38 | 26,81 | 23,66–32,31 | 23,63–31,85 | 26,71–26,90 | 24,28–29,35 | 22,22–31,61 | 26,71–26,79 | 13,41–49,64 | 19,91–39,25 |
| PLPL3 | 5,70 | 6,37 | 5,91–7,30 | 5,47–7,81 | 6,35–6,38 | 5,84–6,91 | 5,10–7,71 | 6,32–6,35 | 2,89–11,74 | 4,40–9,32 |
| MDNE3 | 19,66 | 20,19 | 16,79–21,53 | 17,80–24,01 | 20,05–20,28 | 18,20–22,18 | 17,94–22,55 | 20,08–20,15 | 11,95–33,97 | 14,04–25,96 |
| COGN3 | 2,01 | 1,97 | 1,68–2,55 | 1,58–2,56 | 1,96–1,98 | 1,70–2,25 | 1,48–2,50 | 1,78–1,89 | 0,66–3,78 | 1,10–3,11 |
| HAPV3 | 5,00 | 4,82 | 3,21–7,97 | 3,21–7,87 | 4,43–5,08 | 3,56–6,08 | 1,26–11,79 | 3,61–4,34 | 0,00–25,16 | 0,36–14,03 |
| DIRR3 | 8,97 | 8,59 | 7,68–10,24 | 7,54–10,26 | 8,50–8,69 | 7,73–9,45 | 7,57–9,66 | 8,56–8,58 | 5,27–13,28 | 6,40–12,28 |
| CEAB3 | 7,35 | 6,91 | 4,77–11,73 | 5,70–8,79 | 6,49–7,20 | 5,78–8,04 | 4,24–9,69 | 6,45–6,70 | 1,58–15,56 | 2,94–13,73 |
| ANIM3 | 2,74 | 2,54 | 2,18–3,04 | 1,28–4,43 | 2,41–2,61 | 1,81–3,27 | 1,11–4,05 | 1,85–2,19 | 0,00–8,36 | 0,36–5,22 |
| LREN3 | 9,51 | 8,79 | 6,58–13,76 | 7,84–10,29 | 8,64–8,90 | 7,69–9,89 | 6,94–10,72 | 8,67–8,75 | 4,95–13,74 | 5,51–15,61 |
| BBAS3 | 17,57 | 15,67 | 12,62–18,05 | 14,08–18,30 | 15,17–16,06 | 13,49–17,86 | 14,13–17,34 | 15,67–15,67 | 11,18–21,42 | 10,11–21,26 |
| EZTC3 | 12,12 | 10,69 | 7,19–13,90 | 10,05–11,70 | 10,34–10,97 | 10,03–11,36 | 10,08–11,33 | 10,69–10,71 | 8,84–13,42 | 6,95–14,83 |
| CYRE3 | 20,13 | 17,76 | 15,39–20,70 | 15,76–20,93 | 17,48–17,95 | 15,93–19,58 | 15,69–19,92 | 17,44–17,68 | 11,70–26,15 | 12,65–24,23 |
| CURY3 | 26,94 | 22,89 | 20,42–26,98 | 20,42–26,87 | 22,51–23,34 | 20,56–25,23 | 20,21–25,72 | 22,90–23,00 | 13,65–37,01 | 17,29–31,63 |
| YDUQ3 | 8,48 | 7,10 | 6,21–9,00 | 5,24–9,90 | 7,01–7,18 | 5,86–8,34 | 4,24–10,14 | 5,88–6,64 | 1,58–17,09 | 2,77–12,55 |
| BBDC4 | 15,47 | 12,37 | 9,95–15,33 | 11,30–14,11 | 12,18–12,52 | 10,65–14,10 | 11,44–13,35 | 12,37–12,37 | 10,13–15,03 | 8,49–17,31 |
| VULC3 | 12,49 | 9,70 | 7,80–13,89 | 8,58–11,50 | 9,68–9,72 | 8,62–10,79 | 8,17–11,31 | 9,58–9,66 | 6,25–13,91 | 6,57–15,82 |
| PGMN3 | 2,94 | 2,27 | 1,49–4,05 | 1,71–3,10 | 2,09–2,39 | 1,78–2,75 | 0,51–4,88 | 1,88–2,08 | 0,57–5,24 | 0,20–5,98 |
| BRSR6 | 14,67 | 10,91 | 9,26–12,82 | 9,87–12,61 | 10,32–11,36 | 9,46–12,35 | 9,70–12,20 | 10,91–10,91 | 7,45–15,10 | 7,30–15,22 |
| CSAN3 | 2,97 | 2,10 | 1,57–3,31 | 2,08–2,12 | 2,08–2,12 | 1,88–2,32 | 2,01–2,19 | 1,99–2,09 | 1,80–2,70 | 1,52–3,48 |
| VIVA3 | 19,47 | 13,31 | 9,66–21,21 | 11,78–15,74 | 13,16–13,41 | 11,58–15,05 | 11,54–15,17 | 13,09–13,23 | 9,35–18,30 | 8,30–23,82 |
| GGPS3 | 12,03 | 7,47 | 5,17–12,50 | 6,51–8,99 | 7,46–7,47 | 6,38–8,56 | 4,70–10,35 | 7,27–7,37 | 4,25–11,54 | 3,68–14,85 |
| SBFG3 | 5,88 | 3,52 | 1,06–8,41 | 3,29–4,95 | 3,43–3,80 | 2,45–4,59 | 1,90–7,12 | 3,09–3,48 | 0,46–12,29 | 0,83–10,71 |
| INTB3 | 14,63 | 8,23 | 5,98–13,19 | 7,57–9,29 | 8,13–8,31 | 7,24–9,22 | 6,66–9,87 | 8,24–8,36 | 5,23–12,31 | 5,26–14,99 |
| SIMH3 | 6,87 | 3,84 | 1,77–7,85 | 3,67–6,45 | 3,75–4,20 | 2,24–5,45 | 2,76–6,63 | 2,61–3,72 | 1,59–13,85 | 0,99–10,27 |
| BPAC11 | 55,32 | 29,59 | 18,90–42,16 | 27,03–33,87 | 29,53–29,62 | 24,66–34,52 | 27,90–31,41 | 29,59–29,59 | 24,46–35,67 | 16,41–46,62 |
| IGTI11 | 25,45 | 13,60 | 9,15–23,09 | 11,84–16,37 | 13,46–13,76 | 11,58–15,63 | 12,16–15,14 | 13,05–13,43 | 10,43–17,35 | 7,73–25,57 |
| HYPE3 | 20,21 | 10,76 | 7,73–17,60 | 9,21–13,14 | 10,26–11,12 | 9,08–12,44 | 8,88–12,74 | 10,04–10,50 | 6,51–15,71 | 6,27–19,82 |
| MULT3 | 27,96 | 14,84 | 10,15–25,31 | 12,73–18,14 | 14,66–15,03 | 12,55–17,12 | 13,19–16,58 | 14,14–14,60 | 11,13–19,30 | 8,48–28,03 |
| B3SA3 | 15,10 | 7,65 | 5,67–11,75 | 7,02–8,64 | 7,58–7,72 | 6,76–8,53 | 7,13–8,19 | 7,63–7,70 | 6,06–9,75 | 5,29–13,05 |
| ALPA4 | 12,99 | 6,53 | 4,24–10,72 | 5,94–7,46 | 6,50–6,54 | 5,70–7,35 | 5,59–7,51 | 6,47–6,51 | 4,08–9,62 | 3,88–11,83 |
| RENT3 | 31,73 | 15,89 | 9,56–30,26 | 12,37–21,26 | 15,05–16,46 | 12,55–19,23 | 10,63–21,47 | 13,55–14,89 | 6,42–33,54 | 5,74–34,48 |
| NATU3 | 5,66 | 2,81 | 1,80–4,82 | 2,29–3,60 | 2,76–2,83 | 2,30–3,31 | 1,31–4,36 | 2,60–2,71 | 0,49–8,01 | 0,95–6,12 |
| ALOS3 | 26,87 | 13,07 | 9,36–21,40 | 11,28–15,84 | 12,94–13,22 | 11,12–15,03 | 11,53–14,71 | 12,41–12,89 | 9,64–17,02 | 7,89–23,81 |
| MOVI3 | 8,67 | 4,19 | 1,29–9,77 | 3,86–8,16 | 4,12–4,73 | 1,96–6,43 | 2,53–8,70 | 2,50–4,03 | 0,00–24,41 | 0,17–13,59 |
| MRVE3 | 4,98 | 2,34 | 2,02–4,83 | 1,87–3,02 | 2,11–2,51 | 2,16–2,52 | 0,91–4,11 | 1,35–2,14 | 0,09–8,42 | 0,86–7,04 |
| TOTS3 | 37,25 | 16,55 | 10,38–29,55 | 14,89–19,18 | 16,49–16,60 | 14,09–19,00 | 14,22–18,99 | 16,16–16,45 | 11,59–22,30 | 9,25–32,84 |
| RADL3 | 15,08 | 6,41 | 2,87–14,41 | 5,54–7,82 | 6,34–6,45 | 5,10–7,72 | 3,36–9,99 | 6,01–6,31 | 3,75–9,87 | 1,64–16,94 |
| AZZA3 | 16,50 | 6,90 | 5,14–10,73 | 5,25–9,42 | 6,48–7,20 | 5,63–8,17 | 3,01–13,46 | 5,76–6,49 | 0,01–26,08 | 1,42–16,65 |
| SMFT3 | 16,44 | 6,87 | 1,82–18,43 | 6,54–8,17 | 6,85–6,88 | 4,75–8,99 | 5,71–8,08 | 5,65–6,75 | 2,91–15,76 | 1,34–19,94 |
| ECOR3 | 5,45 | 2,15 | 0,66–4,98 | 1,97–2,43 | 2,13–2,16 | 0,77–3,93 | 1,38–2,95 | 1,77–2,11 | 0,07–4,61 | 0,00–8,90 |
| RDOR3 | 34,96 | 13,66 | 9,17–23,74 | 11,31–17,36 | 13,55–13,71 | 11,33–15,99 | 10,28–17,21 | 12,70–13,31 | 8,21–20,40 | 6,72–27,17 |
| MOTV3 | 13,85 | 5,34 | 1,60–13,70 | 5,07–6,70 | 5,33–5,35 | 3,75–6,94 | 4,74–5,98 | 4,72–5,28 | 3,70–9,21 | 1,31–15,12 |
| ORVR3 | 15,58 | 5,42 | 2,07–12,84 | 4,75–6,48 | 5,22–5,57 | 4,24–6,60 | 4,54–6,35 | 5,15–5,32 | 3,01–8,72 | 1,70–14,20 |
| VAMO3 | 2,90 | 0,95 | 0,29–2,26 | 0,88–1,76 | 0,93–1,03 | 0,43–1,48 | 0,66–1,67 | 0,55–0,91 | 0,07–4,02 | 0,05–2,99 |
| GMAT3 | 3,75 | 1,23 | 0,37–3,12 | 1,16–1,51 | 1,21–1,25 | 0,88–1,57 | 0,35–2,92 | 1,12–1,22 | 0,54–2,64 | 0,12–4,39 |
| RAIL3 | 15,27 | 4,89 | 1,12–13,48 | 4,72–5,33 | 4,87–4,90 | 3,33–6,45 | 4,25–5,55 | 4,12–4,81 | 2,74–9,16 | 0,85–14,75 |
| TTEN3 | 11,39 | 3,46 | 1,01–8,99 | 3,27–4,65 | 3,41–3,59 | 2,54–4,38 | 1,48–7,52 | 3,17–3,43 | 0,75–10,78 | 0,60–11,73 |
| ALUP11 | 31,31 | 9,24 | 2,77–23,64 | 8,80–13,05 | 9,13–9,32 | 5,91–12,57 | 8,23–10,73 | 8,13–9,13 | 7,01–16,22 | 2,27–26,94 |
| ASAI3 | 8,63 | 2,24 | 0,68–5,28 | 2,07–3,04 | 2,22–2,26 | 1,25–3,24 | 0,01–7,39 | 1,57–2,18 | 0,58–6,01 | 0,00–9,65 |
| JHSF3 | 11,24 | 2,62 | 0,51–4,10 | 2,43–2,96 | 2,55–2,68 | 2,20–3,04 | 2,36–2,90 | 2,29–2,59 | 1,27–4,78 | 0,45–4,50 |
| MGLU3 | 5,85 | 1,31 | 0,07–4,04 | 1,29–1,33 | 1,29–1,33 | 0,14–2,61 | 0,00–2,74 | 1,22–1,30 | 0,00–5,40 | 0,00–6,00 |
| VBBR3 | 32,30 | 6,81 | 3,29–13,81 | 5,54–9,33 | 6,75–6,83 | 5,21–8,41 | 0,00–21,87 | 6,05–6,54 | 1,30–21,06 | 0,00–26,86 |
| ENGI11 | 47,14 | 9,87 | 2,22–27,31 | 9,55–10,38 | 9,79–9,92 | 5,16–14,57 | 6,42–13,43 | 6,93–9,57 | 4,07–17,27 | 0,35–33,92 |
| SBSP3 | 25,80 | 5,36 | 1,07–15,10 | 5,19–5,65 | 5,32–5,39 | 3,66–7,06 | 4,76–5,98 | 4,71–5,29 | 3,76–7,27 | 0,78–16,50 |
| CPLE3 | 15,18 | 2,79 | 0,84–6,94 | 2,67–2,98 | 2,77–2,81 | 1,99–3,60 | 2,24–3,37 | 2,40–2,75 | 1,78–4,12 | 0,65–7,68 |
| AURE3 | 10,29 | 1,56 | 0,30–4,39 | 1,49–1,66 | 1,53–1,57 | 0,27–3,20 | 0,82–2,33 | 1,27–1,53 | 0,00–5,45 | 0,00–7,26 |
| EQTL3 | 35,89 | 5,15 | 1,02–14,52 | 4,99–5,42 | 5,11–5,18 | 2,65–7,65 | 3,42–6,94 | 3,54–4,99 | 2,61–8,85 | 0,22–20,03 |
| CVCB3 | 1,07 | 0,13 | 0,00–0,41 | 0,13–0,13 | 0,13–0,13 | 0,00–0,38 | 0,04–0,22 | 0,12–0,13 | 0,00–1,37 | 0,00–0,90 |

## Lista robusta

Empresas no top 7 em pelo menos 80% ou 50% das combinações de cada grade.

| Grade | TIR ≥ 80% | TIR ≥ 50% | Upside ≥ 80% | Upside ≥ 50% |
|---|---|---|---|---|
| Pesos do blend {DCF, DDM, múltiplos} (passo 0,1) | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | TEND3, BEEF3 | TEND3, BEEF3, PLPL3, COGN3, HAPV3, CEAB3, LREN3 |
| Ke 20–30% (passo 1 p.p.) | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, TEND3, BEEF3, COGN3 | MDNE3, PLPL3, TEND3, BEEF3, COGN3, DIRR3, HAPV3 |
| g terminal −2 a +2 p.p. | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, TEND3, COGN3, HAPV3, BEEF3, DIRR3 | MDNE3, PLPL3, TEND3, COGN3, BEEF3, HAPV3 | MDNE3, PLPL3, TEND3, COGN3, BEEF3, HAPV3, DIRR3 |
| Múltiplos-alvo −30% a +30% | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, DIRR3, TEND3, COGN3, HAPV3, BEEF3 | MDNE3, PLPL3, TEND3, COGN3, BEEF3 | MDNE3, PLPL3, TEND3, COGN3, BEEF3, DIRR3, HAPV3 |
| Margem EBITDA × crescimento ±2 p.p. | MDNE3, PLPL3, TEND3, HAPV3 | MDNE3, PLPL3, TEND3, HAPV3, COGN3, BEEF3, DIRR3 | PLPL3, TEND3 | PLPL3, TEND3, MDNE3, BEEF3, DIRR3, HAPV3 |
| Kd +300 bp (WACC / resultado financeiro / ambos) | MDNE3, PLPL3, DIRR3, TEND3, HAPV3 | MDNE3, PLPL3, DIRR3, TEND3, HAPV3, CYRE3, BBAS3 | LREN3, MDNE3, PLPL3, DIRR3, TEND3, BEEF3 | LREN3, MDNE3, PLPL3, DIRR3, TEND3, BEEF3, COGN3 |
| Monte Carlo com desvios ×1,5 | nenhuma | PLPL3, TEND3, MDNE3, HAPV3, BEEF3 | nenhuma | BEEF3, TEND3, PLPL3 |
| Amostra conjunta de todas as grades | MDNE3, PLPL3, TEND3 | MDNE3, PLPL3, TEND3, HAPV3, DIRR3, BEEF3 | TEND3 | TEND3, PLPL3, BEEF3, DIRR3, HAPV3, CEAB3 |
| Em todas as grades ao mesmo tempo | nenhuma | MDNE3, PLPL3, TEND3, HAPV3 | nenhuma | PLPL3, TEND3, BEEF3 |

## As 7 oportunidades atuais e os pesos

Para cada um dos 66 vetores de pesos, o teste recalcula o upside, a P(valor justo > preço) e o escore e reaplica a regra do `build.py`. A P(MC) sai do mesmo Monte Carlo do motor, com os valores por método guardados em cada sorteio e o blend refeito. A TIR e os demais fatores do escore não dependem dos pesos.

| Empresa | Selecionada (% dos pesos) | Condição (≥ 50% dos vetores) | P(MC) mín–máx | Upside mín–máx | Seleção por w_múlt = 0; 0,1; …; 1 | Seleção por w_DCF = 0; 0,1; …; 1 |
|---|---:|---|---|---|---|---|
| BEEF3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 47%–84% | -3%–88% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| PLPL3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 50%–88% | 1%–33% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| TEND3 ★ | 100% | qualquer w_múlt; qualquer w_DCF | 45%–95% | -3%–47% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% | 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% 100% |
| MDNE3 ★ | 47% | w_múlt ≥ 0,4; w_DCF ≤ 0,3 | 15%–71% | -18%–13% | 9% 10% 22% 38% 57% 83% 100% 100% 100% 100% 100% | 100% 80% 67% 50% 29% 0% 0% 0% 0% 0% 0% |
| COGN3 ★ | 17% | w_múlt = 0,3; w_DCF = 0,5 | 23%–90% | -18%–37% | 0% 0% 11% 75% 43% 17% 0% 0% 0% 0% 0% | 0% 0% 11% 12% 29% 50% 40% 25% 33% 0% 0% |
| CEAB3 | 58% | w_múlt ≥ 0,3; w_DCF ≤ 0,5 | 19%–96% | -41%–80% | 0% 0% 22% 100% 100% 100% 100% 100% 100% 100% 100% | 82% 80% 67% 62% 57% 50% 40% 25% 0% 0% 0% |
| LREN3 | 50% | w_múlt ≥ 0,3; w_DCF ≤ 0,4 | 3%–100% | -35%–62% | 0% 0% 0% 62% 100% 100% 100% 100% 100% 100% 100% | 73% 70% 67% 62% 57% 33% 20% 0% 0% 0% 0% |
| SBFG3 | 35% | w_múlt ≥ 0,5; w_DCF ≤ 0,2 | 5%–83% | -92%–62% | 0% 0% 0% 25% 43% 67% 80% 100% 100% 100% 100% | 73% 70% 56% 38% 0% 0% 0% 0% 0% 0% 0% |
| DIRR3 | 23% | w_múlt entre 0,3 e 0,4; w_DCF entre 0,4 e 0,9, irregular | 18%–83% | -18%–19% | 0% 10% 33% 50% 57% 33% 20% 0% 0% 0% 0% | 0% 0% 0% 12% 57% 50% 60% 50% 33% 50% 0% |

Quantas das 7 atuais a regra mantém, em número de combinações: 3 mantidas: 25, 4 mantidas: 40, 5 mantidas: 1.

Seleção pela regra nas demais grades (fração de combinações em que cada empresa está entre as 7):

- Pesos do blend {DCF, DDM, múltiplos} (passo 0,1): PLPL3 100%, TEND3 100%, BEEF3 100%, CEAB3 58%, LREN3 50%, MDNE3 47%, SBFG3 35%, DIRR3 23%, COGN3 17% (lista idêntica em 0%).
- Ke 20–30% (passo 1 p.p.): TEND3 100%, BEEF3 100%, PLPL3 91%, MDNE3 64%, CEAB3 45%, LREN3 36%, COGN3 27%, CYRE3 18%, DIRR3 18% (lista idêntica em 9%).
- g terminal −2 a +2 p.p.: MDNE3 100%, PLPL3 100%, TEND3 100%, COGN3 100%, BEEF3 100%, CEAB3 40% (lista idêntica em 60%).
- Múltiplos-alvo −30% a +30%: PLPL3 100%, TEND3 100%, BEEF3 100%, MDNE3 71%, CEAB3 43%, LREN3 29%, DIRR3 29%, COGN3 29%, BBAS3 14% (lista idêntica em 14%).
- Margem EBITDA × crescimento ±2 p.p.: TEND3 84%, PLPL3 76%, MDNE3 64%, BEEF3 60%, CEAB3 48%, PGMN3 40%, LREN3 36%, SBFG3 16%, COGN3 16%, DIRR3 4%, YDUQ3 4% (lista idêntica em 4%).
- Kd +300 bp (WACC / resultado financeiro / ambos): MDNE3 100%, PLPL3 100%, TEND3 100%, BEEF3 33% (lista idêntica em 0%).
- Monte Carlo com desvios ×1,5 (P(MC) recalculada com os pesos da base): BEEF3, PLPL3, TEND3, CEAB3, DIRR3, COGN3.

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
| demais | VBBR3, HYPE3, SMFT3, CVCB3, YDUQ3, COGN3, ANIM3, HAPV3, RDOR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3 | DCF 50% / DDM 25% / Múltiplos 25% | Educação, saúde, serviços, tecnologia, proteína, agro, combustíveis e turismo: mantém o padrão da especificação (50/25/25). |

Diagnóstico por setor, com base nos valores da base e na amostra conjunta. A dispersão é (p95 − p5) / p50 de cada método sob Ke, g, múltiplos, margem, crescimento e Kd. Os pesos de mínima dispersão minimizam a dispersão mediana do blend no setor. São só uma checagem, porque payout, capex e capital de giro não são choques da grade e o DDM e o DCF dependem deles.

| Setor | n | DCF < 0 | Múltiplos/DDM (mediana) | DCF/DDM (mediana) | DL/EV mercado | Dispersão DCF | Dispersão DDM | Dispersão múltiplos | Pesos de mínima dispersão |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| bancos | 4 | 0 | 1,61 | — | — | — | 0,77 | 0,68 | DCF 0.0 / DDM 0.6 / Múlt 0.4 |
| utilities | 6 | 6 | 5,16 | -3,85 | 51% | — | 1,85 | 1,43 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| concessoes | 4 | 3 | 3,80 | -0,49 | 50% | 1,93 | 0,95 | 0,99 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| incorporadoras | 9 | 1 | 1,44 | 1,18 | 13% | 0,68 | 0,63 | 0,75 | DCF 0.0 / DDM 0.7 / Múlt 0.3 |
| varejo | 13 | 4 | 2,37 | 0,75 | 38% | 2,11 | 1,38 | 1,40 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| locadoras | 3 | 2 | 2,01 | -0,07 | 78% | 3,47 | 1,89 | 2,51 | DCF 0.0 / DDM 0.9 / Múlt 0.1 |
| shoppings | 3 | 0 | 2,53 | 0,84 | 25% | 1,00 | 0,65 | 0,74 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |
| demais | 15 | 3 | 2,18 | 1,01 | 33% | 1,48 | 1,08 | 1,10 | DCF 0.0 / DDM 0.8 / Múlt 0.2 |

Impacto dos pesos propostos (empresas cujo rank por upside ou cuja seleção muda, além do top 15 de cada lado):

| Empresa | Setor | VJ base → proposto | Δ VJ | Upside base → proposto | Rank upside | P(MC) base → proposta | Rank escore | Regra |
|---|---|---|---:|---|---|---|---|---|
| BEEF3 | demais | 5,44 → 5,44 | 0% | 61% → 61% | 1 → 1 | 74% → 74% | 1 → 1 | mantém |
| TEND3 | incorporadoras | 26,81 → 26,81 | 0% | 20% → 20% | 2 → 2 | 86% → 73% | 4 → 5 | mantém |
| PLPL3 | incorporadoras | 6,37 → 6,37 | 0% | 12% → 12% | 3 → 3 | 73% → 65% | 2 → 2 | mantém |
| CEAB3 | varejo | 6,91 → 7,72 | 12% | -6% → 5% | 8 → 4 | 44% → 55% | 5 → 3 | entra |
| MDNE3 | incorporadoras | 20,19 → 20,19 | 0% | 3% → 3% | 4 → 5 | 36% → 54% | 6 → 6 | entra |
| LREN3 | varejo | 8,79 → 9,55 | 9% | -8% → 0% | 10 → 6 | 34% → 51% | 7 → 7 | entra |
| COGN3 | demais | 1,97 → 1,97 | 0% | -2% → -2% | 5 → 7 | 47% → 47% | 10 → 11 | mantém |
| HAPV3 | demais | 4,82 → 4,82 | 0% | -4% → -4% | 6 → 8 | 49% → 49% | 3 → 4 | — |
| DIRR3 | incorporadoras | 8,59 → 8,59 | 0% | -4% → -4% | 7 → 9 | 46% → 40% | 8 → 10 | sai |
| ANIM3 | demais | 2,54 → 2,54 | 0% | -7% → -7% | 9 → 10 | 45% → 45% | 13 → 14 | — |
| PGMN3 | varejo | 2,27 → 2,63 | 16% | -23% → -11% | 18 → 11 | 25% → 37% | 15 → 13 | — |
| BBAS3 | bancos | 15,67 → 15,67 | 0% | -11% → -11% | 11 → 12 | 29% → 18% | 9 → 15 | — |
| SIMH3 | holdings | 3,84 → 6,06 | 58% | -44% → -12% | 25 → 13 | — → — | 23 → 18 | — |
| CYRE3 | incorporadoras | 17,76 → 17,76 | 0% | -12% → -12% | 13 → 14 | 14% → 21% | 12 → 9 | — |
| SBFG3 | varejo | 3,52 → 5,14 | 46% | -40% → -13% | 23 → 15 | 22% → 39% | 14 → 8 | — |
| CURY3 | incorporadoras | 22,89 → 22,89 | 0% | -15% → -15% | 14 → 16 | 20% → 20% | 11 → 12 | — |
| YDUQ3 | demais | 7,10 → 7,10 | 0% | -16% → -16% | 15 → 18 | 34% → 34% | 16 → 17 | — |
| EZTC3 | incorporadoras | 10,69 → 9,46 | -11% | -12% → -22% | 12 → 21 | 7% → 2% | 19 → 22 | — |

Top 7 por upside: base BEEF3, TEND3, PLPL3, MDNE3, COGN3, HAPV3, DIRR3; proposto BEEF3, TEND3, PLPL3, CEAB3, MDNE3, LREN3, COGN3. Regra de oportunidades: base BEEF3, PLPL3, TEND3, DIRR3, COGN3; proposto BEEF3, PLPL3, CEAB3, TEND3, MDNE3, LREN3, COGN3.

Decomposição, aplicando os pesos propostos a um setor por vez (os demais ficam na base):

| Setor alterado | Δ VJ mediano do setor | Spearman upside vs base | Entram na regra | Saem da regra |
|---|---:|---:|---|---|
| bancos | 0% | 1,00 | nenhuma | nenhuma |
| utilities | 19% | 1,00 | nenhuma | nenhuma |
| concessoes | 32% | 0,98 | nenhuma | nenhuma |
| incorporadoras | 0% | 1,00 | MDNE3 | DIRR3 |
| varejo | 12% | 0,99 | CEAB3, LREN3 | nenhuma |
| locadoras | 73% | 0,97 | nenhuma | nenhuma |
| shoppings | -3% | 1,00 | nenhuma | nenhuma |

Sensibilidade da proposta às escolhas mais discutíveis (os demais setores ficam na proposta):

| Variante | Regra (7) | Top 7 upside | Spearman upside vs base | P(MC): CEAB3 / LREN3 / SBFG3 / DIRR3 / COGN3 |
|---|---|---|---:|---|
| varejo DDM 60 / Múlt 20 / DCF 20 | BEEF3, PLPL3, TEND3, MDNE3, COGN3 | BEEF3, TEND3, PLPL3, MDNE3, COGN3, HAPV3, DIRR3 | 0,94 | 44% / 32% / 31% / 40% / 47% |
| varejo DDM 50 / Múlt 30 / DCF 20 (proposta) | BEEF3, PLPL3, CEAB3, TEND3, MDNE3, LREN3, COGN3 | BEEF3, TEND3, PLPL3, CEAB3, MDNE3, LREN3, COGN3 | 0,94 | 55% / 51% / 39% / 40% / 47% |
| varejo DDM 40 / Múlt 40 / DCF 20 | BEEF3, CEAB3, PLPL3, LREN3, MDNE3, TEND3, SBFG3 | BEEF3, TEND3, CEAB3, PLPL3, LREN3, MDNE3, COGN3 | 0,93 | 64% / 67% / 46% / 40% / 47% |
| incorporadoras no padrão 50/25/25 | BEEF3, PLPL3, TEND3, CEAB3, LREN3, DIRR3, COGN3 | BEEF3, TEND3, PLPL3, CEAB3, LREN3, DIRR3, COGN3 | 0,93 | 55% / 51% / 39% / 46% / 47% |
| demais com DCF 30 / DDM 45 / Múlt 25 | BEEF3, PLPL3, CEAB3, TEND3, MDNE3, LREN3, COGN3 | BEEF3, TEND3, PLPL3, HAPV3, CEAB3, MDNE3, LREN3 | 0,94 | 55% / 51% / 39% / 40% / 45% |

## Achados sobre o motor e limitações

- **DCF negativo entra como zero e mantém o peso** (`max(0, x)` no blend). Isso ocorre em 19 empresas (MOVI3, VAMO3, ECOR3, MOTV3, RAIL3, MGLU3, SBFG3, ASAI3, GMAT3, JHSF3, SMFT3, CVCB3, AURE3, ENGI11, EQTL3, CPLE3, ALUP11, SBSP3, TTEN3): cada 10 p.p. de peso no DCF corta cerca de 10% do valor justo, sem informação nova. Melhor seria tirar o método do blend quando o patrimônio do DCF for negativo, ou trocá-lo pelo DDM.
- **Os múltiplos-alvo não são coerentes com Ke 25%.** Um P/L de 9–12x com g 5% e ROE 17% equivale a um custo de capital próprio de cerca de 11–13%. A P/L justa a Ke 25%, g 5% e ROE 15–20% fica em 3,5–4x. Na mediana, o valor por múltiplos é 2,34× o do DDM. Por isso o peso dos múltiplos é o principal motor do upside, e os pesos propostos limitam os múltiplos a 20–40%.
- **O DCF é o método mais disperso** (tabela de diagnóstico). Com o patrimônio residual EV − DL, um erro pequeno no EV vira um erro grande no valor por ação quando a DL é grande. O peso padrão de 50% no DCF é a maior fonte de fragilidade do valor justo nos setores alavancados.
- **Holding com controlada de valor justo zero:** `value_holding` testa `models[tk].get('fair_value')` pela verdade do valor, então 0,0 vira o valor de mercado da controlada. Isso afeta SIMH3 quando MOVI3 ou VAMO3 chegam a zero, por exemplo com peso 100% no DCF.
- **Kd +300 bp derruba a TIR de BEEF3 e COGN3 para menos de 20%** (BEEF3 24,5% → 19,9%, COGN3 21,8% → 19,9%), e a regra os exclui. O corte de TIR de 20% é uma aresta para empresas alavancadas sob estresse de juros.
- **Choque de ±2 p.p. de margem é desproporcional em negócios de margem fina** (BEEF3 cerca de 8,5%, ASAI3, GMAT3 e VBBR3 com 4–6%): em BEEF3, −2 p.p. levam a TIR de 24,5% a 8,2% e o upside de 61% a -68%. Isso explica boa parte da faixa p5–p95 larga desses nomes na amostra conjunta.
- **Kd +300 bp nos bancos:** o template financeiro não tem custo de dívida, então esses choques não mudam bancos. Margem ±2 p.p. vira ROE ±2 p.p. no template financeiro, que é a convenção do motor.
- Na amostra conjunta e no MC ×1,5, a regra de oportunidades não é recalculada (P(MC) exigiria um Monte Carlo por combinação). No MC ×1,5, os sorteios são independentes entre empresas, o caso conservador para a estabilidade do ranking.

## Como reproduzir

```bash
.venv/bin/python pipeline/tests/robustness.py            # completo
.venv/bin/python pipeline/tests/robustness.py --quick    # rápido (menos sorteios)
```

Parâmetros desta rodada: amostra conjunta de 3.000 combinações, MC ×1,5 com 2.000 sorteios por empresa e P(MC) com 5.000 sorteios. Tempo: 315 s.
