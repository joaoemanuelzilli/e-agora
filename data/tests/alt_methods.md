# Métodos alternativos de valuation e novos pesos (Ke 25%)

*Gerado em 2026-10-28T17:19:53 por `pipeline/tests/alt_methods.py`. Motor `pipeline/model.py` importado sem alterações, premissas lidas de `research/` no momento da execução (os revisores seguem ajustando; rode de novo para atualizar), preços da foto do estudo. Valores por ação/unit, comparáveis ao preço. Dados completos em `data/tests/alt_methods.json`.*

## Resumo

1. **Os métodos intrínsecos alternativos confirmam DCF e DDM.** Mediana por empresa em relação ao DDM: RIM 1,00×, P/L justificado 0,91×, P/VP justificado 1,09×, FCFE 1,18×, pares ajustados ao Ke 1,04×. Em relação ao DCF: APV 1,02× e EVA 1,00×. RIM ≡ DDM e EVA ≡ DCF são identidades quando a perpetuidade é a mesma (erro máximo 1e-14 e 2e-15, relativo). As diferenças vêm só do fade do retorno excedente (RIM em 35 empresas, EVA em 40) e da política de dívida (APV e FCFE).
2. **O viés está nos métodos de mercado.** Na mediana, os múltiplos-alvo do estudo ficam 2,61× o DCF, os pares 2,35× e a mediana histórica de 5 anos 3,73×. Eles embutem Ke de cerca de 13% (P/L-alvo) e 12% (P/L histórico), e o preço de hoje embute uma TIR de dono mediana de 13%: nenhum deles está em 25%. Com 25% de peso, a perna de múltiplos-alvo responde, na mediana, por 50% do valor justo industrial do estudo. Nos bancos, com 50% de peso, responde por 0%.
3. **Onde e por que divergem.** (i) Alavancagem com Ke fixo: 33 das 53 industriais têm DCF ≤ 0 (EV abaixo da dívida, com ROIC < WACC), mas 32 delas têm DDM/FCFE/RIM > 0. Um Ke de 25% que não sobe com a alavancagem viola Modigliani-Miller, e o acionista tem responsabilidade limitada (utilities, concessões, locadoras, MGLU3, ASAI3). (ii) `other_financial` entra no lucro, mas não no FCFF (AZZA3, NATU3, EZTC3, MRVE3, PLPL3, TEND3, AURE3, ENGI11, EQTL3, VALE3, DXCO3, AXIA3, TAEE11): no caso de TEND3/PLPL3/MRVE3, juros capitalizados e custo de cessões inflam o DCF frente ao RIM/FCFE. (iii) Payout baixo: o FCFE supera o DDM em +18% na mediana, porque o caixa retido rende Kd·(1−t) < Ke. (iv) PL com ágio (HAPV3, AZZA3, ALOS3) tira o sentido do P/VP. Detalhes por empresa na tabela de divergências.
4. **Pesos recomendados.** Cada classe usa os métodos coerentes com Ke 25% (tabela abaixo): RIM nos bancos e incorporadoras, APV/DCF mais o lado do acionista em infraestrutura, EVA/APV em locação, e DCF com pares ajustados ao Ke no varejo. Múltiplos de mercado brutos (alvo, pares e histórico) ficam como referência relativa e saem do valor justo.
5. **Efeito.** O valor justo muda -27% na mediana (infraestrutura -61%, shoppings -30%, serviços -30%, bancos -21%, varejo -24%, incorporadoras -14%, locação -14%, cíclicas -14%). O upside mediano das 59 passa de -47% para -62%, e empresas com upside > 0: 14 → 8. Quase toda a queda vem de retirar os múltiplos-alvo: o esquema "estudo sem múltiplos" já dá -64%. O ranking quase não muda (Spearman do escore multifator 0,99; do upside 0,91), porque o upside pesa só 10% do escore e a TIR de dono (30%), a qualidade e a solidez não dependem dos pesos.
6. **As 7 oportunidades.** Com as premissas revisadas de agora, o estudo recalculado mantém 8 das 7 pela regra (VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3, CEAB3, COGN3). Com os pesos propostos, ficam 7: VTRU3 (upside +40%), BEEF3 (upside +64%), SEER3 (upside +22%), MDNE3 (upside +9%), PLPL3 (upside +26%), TEND3 (upside +8%), COGN3 (upside +6%). Saem CEAB3 (P(MC) 37%). Nenhuma empresa nova entra. Os rankings das oportunidades mudam pouco (tabela abaixo).

## Métodos e convenções

| Método | Definição | Bancos | Holdings |
|---|---|---|---|
| RIM/Ohlson | PL_base·(1+Ke)^(−s0) + Σ(LL_t − c_t·PL_{t−1}) a Ke. Se o ROE de 2031 na continuação do estudo (LL₂₀₃₀·(1+g)/PL₂₀₃₀) supera o ROE terminal, ele converge a este em 10 anos (2031–40), reinvestindo g/ROE_T do lucro, com perpetuidade do lucro residual a g. Caso contrário, usa a perpetuidade do estudo | sim | — |
| EVA | CI₀ + Σ(NOPAT_t − c_t·CI_{t−1}) a WACC; CI = PL + DL + minoritários, evolui por capex − D&A + ΔCG; mesmo fade do ROIC ao ROIC terminal; mesma ponte EV → equity do DCF | — | — |
| APV | FCFF e perpetuidade (value driver) a Ku = (1−wd)·Ke + wd·Kd (Harris–Pringle, com wd/Kd do WACC do estudo; Kd ajustado ao RET → custo da DL projetado) + VP a Ku do benefício fiscal da DL projetada (34%, ou a alíquota efetiva se < 20%) | — | — |
| FCFE | LL + D&A − capex − ΔCG + ΔDL, com a DL do balanço-base crescendo com a receita (juros e LL recalculados; caixa líquido constante), a Ke; perpetuidade LL·(1+g)·(1−g/ROE_T)/(Ke−g) | ≡ DDM | — |
| DDM c/ emissões e recompras | DDM do estudo com o fluxo líquido ao acionista (dividendos + recompras − emissões projetadas); ≡ RIM sem fade | ≡ DDM | — |
| P/L justificado | (1 − g/ROE_T)/(Ke − g) × LPA 12m à frente (2T26 + 2027E ponderados) | sim | — |
| P/VP justificado | (ROE_T − g)/(Ke − g) × VPA do balanço-base | sim | — |
| Pares | mediana dos pares da cobertura (grupo ∩ segmento B3 → segmento → subsetor → grupo [moda/consumo, utilities] → 1 par do segmento) de P/L 2027E e EV/EBITDA 2027E atuais (bancos: P/L e P/VP) | sim | — |
| Pares ajustados ao Ke | P/L de cada par × (k_par − g)/(25% − g), com k_par = TIR implícita no preço de hoje (Gordon), mediana × LPA 2027E (bancos: também P/VP) | sim | — |
| Histórico | mediana de 60 meses da própria ação (P/L e EV/EBITDA LTM; bancos P/L e P/VP) × métricas LTM; filtra meses com erro de unidade de ações | sim | P/VP, P/L |
| SOTP | SOTP do estudo recalculado com o valor justo novo das controladas avaliadas pelo motor (MOVI3, VAMO3, RAIL3) | — | sim |

Todos os fluxos seguem o calendário do motor: stub de 2026 após o balanço-base, meio de período e perpetuidade em 31/12/2030. O encargo de capital do RIM e do EVA usa o espaçamento exato entre fluxos. É isso que torna RIM ≡ DDM e EVA ≡ DCF quando a perpetuidade é a mesma.

## Viés sistemático por método

| Método | n | Mediana vs valor justo do estudo | P25 / P75 | Mediana vs DCF | % acima do estudo | Upside mediano vs preço |
|---|---|---|---|---|---|---|
| DCF-FCFF (estudo) | 103 | -44% | -129% / -23% | — | 7% | -75% |
| APV | 103 | -32% | -86% / -19% | +2% | 9% | -68% |
| EVA (fade ROIC) | 103 | -47% | -131% / -23% | -0% | 4% | -76% |
| DDM (estudo) | 117 | -18% | -29% / -4% | +7% | 21% | -59% |
| DDM c/ emissões e recompras | 117 | -18% | -29% / -4% | +4% | 21% | -59% |
| FCFE (DL ∝ receita) | 103 | -3% | -27% / +14% | +32% | 43% | -54% |
| RIM/Ohlson (fade ROE) | 117 | -18% | -30% / -5% | +4% | 20% | -59% |
| P/L justificado | 114 | -27% | -42% / -9% | -5% | 19% | -62% |
| P/VP justificado | 117 | -8% | -34% / +44% | +15% | 44% | -54% |
| Pares ajustados ao Ke 25% | 104 | -16% | -34% / +6% | -1% | 30% | -56% |
| Múltiplos-alvo (estudo) | 117 | +89% | +39% / +165% | +161% | 98% | -1% |
| Pares (mediana) | 106 | +76% | +22% / +229% | +135% | 83% | -2% |
| Histórico 5a (mediana) | 112 | +157% | +53% / +282% | +253% | 94% | +24% |
| SOTP (controladas c/ pesos novos) | 5 | -24% | -25% / -23% | — | 0% | -62% |

O valor justo do estudo já inclui 25% (bancos: 50%) de múltiplos-alvo; por isso os intrínsecos aparecem abaixo dele e próximos do DCF/DDM.

## Onde os métodos divergem mais (e por quê)

Dispersão = desvio-padrão do log dos valores positivos de todos os métodos. Ke implícito no P/L histórico = Ke que torna a mediana de 5 anos do P/L (LTM, Gordon com ROE e g terminais) coerente; TIR hoje = TIR de dono implícita no preço (DDM do estudo).

| # | Empresa | Classe | σ log | Máx/mín | Mercado/intrínseco | Ke impl. P/L hist. | TIR hoje | Causas principais |
|---|---|---|---|---|---|---|---|---|
| 1 | MGLU3 | Varejo e consumo | 1,73 | 106,8× | 21,73× | 6% | 7% | múltiplos de mercado 21,7× a mediana intrínseca (P/L histórico embute Ke ≈ 6%; P/L-alvo embute Ke ≈ 9% vs 25%); EV a WACC 19% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 2 | SMFT3 | Serviços, saúde, educação e tecnologia | 1,47 | 239,3× | 4,47× | 9% | 14% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 67%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 18% abaixo da dívida (ROIC 2030 12%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 4,5× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 11% vs 25%) |
| 3 | EGIE3 | Serviços, saúde, educação e tecnologia | 1,43 | 117,2× | 3,53× | 11% | 10% | APV/DCF = 7,15: dívida projetada (DL/EBITDA 2,8x → 2,1x em 2030) ≠ peso-alvo wd = 40% do WACC; múltiplos de mercado 3,5× a mediana intrínseca (P/L histórico embute Ke ≈ 11%; P/L-alvo embute Ke ≈ 11% vs 25%); EVA/DCF = 0,75: ROIC 2031 (continuação) 12% converge ao ROIC terminal 12% (WACC 18%) em vez de persistir |
| 4 | KLBN11 | Serviços, saúde, educação e tecnologia | 1,33 | 162,0× | 1,68× | 12% | 12% | EV a WACC 15% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; FCFE/DDM = 1,40: payout médio 91% retém caixa que rende Kd·(1−t) < Ke |
| 5 | SBFG3 | Varejo e consumo | 1,27 | 173,9× | 2,08× | 12% | 23% | EV a WACC 19% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,1× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 15% vs 25%); FCFE/DDM = 1,33: payout médio 36% retém caixa que rende Kd·(1−t) < Ke |
| 6 | TUPY3 | Serviços, saúde, educação e tecnologia | 1,21 | 50,5× | 1,87× | 12% | 16% | APV/DCF = 3,87: dívida projetada (DL/EBITDA 2,9x → 1,4x em 2030) ≠ peso-alvo wd = 35% do WACC; valor ≤ 0 em: Histórico 5a (mediana); EVA/DCF = 0,50: ROIC 2031 (continuação) 13% converge ao ROIC terminal 12% (WACC 19%) em vez de persistir |
| 7 | BRAV3 | Serviços, saúde, educação e tecnologia | 1,11 | 32,4× | 3,36× | — | 11% | múltiplos de mercado 3,4× a mediana intrínseca (P/L-alvo embute Ke ≈ 23% vs 25%); FCFE/DDM = 2,22: payout médio 44% retém caixa que rende Kd·(1−t) < Ke; APV/DCF = 2,14: dívida projetada (DL/EBITDA 1,4x → 0,4x em 2030) ≠ peso-alvo wd = 45% do WACC |
| 8 | ENGI11 | Infraestrutura e utilities | 1,05 | 43,8× | 4,88× | 14% | 8% | FCFE/DDM = 0,20: dividendos projetados acima do FCFE (desalavancagem cessa ou dívida financia o payout); múltiplos de mercado 4,9× a mediana intrínseca (P/L histórico embute Ke ≈ 14%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 9 | HAPV3 | Serviços, saúde, educação e tecnologia | 1,05 | 32,1× | 3,03× | — | 29% | múltiplos de mercado 3,0× a mediana intrínseca (P/L-alvo embute Ke ≈ 15% vs 25%); APV/DCF = 1,77: dívida projetada (DL/EBITDA 3,7x → 1,8x em 2030) ≠ peso-alvo wd = 35% do WACC; FCFE/DDM = 1,57: payout médio 22% retém caixa que rende Kd·(1−t) < Ke |
| 10 | CBAV3 | Serviços, saúde, educação e tecnologia | 1,04 | 12,7× | 9,29× | 9% | 6% | múltiplos de mercado 9,3× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 7% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 6%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; FCFE/DDM = 1,44: payout médio 36% retém caixa que rende Kd·(1−t) < Ke |
| 11 | CVCB3 | Serviços, saúde, educação e tecnologia | 1,04 | 11,0× | — | — | — | múltiplos de mercado 6,3× a mediana intrínseca (P/L-alvo embute Ke ≈ 13% vs 25%) |
| 12 | DESK3 | Serviços, saúde, educação e tecnologia | 0,98 | 25,2× | 3,60× | 8% | 10% | múltiplos de mercado 3,6× a mediana intrínseca (P/L histórico embute Ke ≈ 8% vs 25%); APV/DCF = 2,52: dívida projetada (DL/EBITDA 1,8x → 0,9x em 2030) ≠ peso-alvo wd = 40% do WACC; FCFE/DDM = 1,70: payout médio 32% retém caixa que rende Kd·(1−t) < Ke |
| 13 | AURE3 | Infraestrutura e utilities | 0,97 | 13,9× | 6,63× | — | 7% | múltiplos de mercado 6,6× a mediana intrínseca; FCFE/DDM = 5,28: payout médio 25% retém caixa que rende Kd·(1−t) < Ke; EV a WACC 17% abaixo da dívida (ROIC 2030 6%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 14 | RAIL3 | Infraestrutura e utilities | 0,96 | 46,1× | 4,66× | 6% | 10% | múltiplos de mercado 4,7× a mediana intrínseca (P/L histórico embute Ke ≈ 6%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 10%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 15 | SAPR11 | Serviços, saúde, educação e tecnologia | 0,93 | 58,6× | 2,53× | 17% | 13% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 29%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 19% abaixo da dívida (ROIC 2030 10%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,5× a mediana intrínseca (P/L histórico embute Ke ≈ 17%; P/L-alvo embute Ke ≈ 15% vs 25%) |

## Pesos propostos por classe

| Classe | Empresas | Pesos | Justificativa |
|---|---|---|---|
| Bancos | BPAC11, BBAS3, BBDC4, BRSR6, ITUB4, SANB11, BBDC3, ABCB4, PINE4, BBSE3, CXSE3, PSSA3, IRBR3, SAUD3 | RIM/Ohlson (fade ROE) 50%, DDM (estudo) 25%, P/VP justificado 25% | Dívida é matéria-prima (não há FCFF/EV); o valor vem do spread ROE − Ke sobre o capital regulatório. RIM ancora no PL (Basileia) e independe da política de payout; DDM complementa (dividendo limitado pelo capital); P/VP justificado = RIM em estado estacionário. Múltiplos de mercado embutem Ke implícito < 25% e ficam como referência. |
| Incorporadoras | CYRE3, EZTC3, MDNE3, JHSF3, MRVE3, PLPL3, DIRR3, CURY3, TEND3 | RIM/Ohlson (fade ROE) 45%, FCFE (DL ∝ receita) 20%, Pares ajustados ao Ke 25% 15%, DCF-FCFF (estudo) 10%, P/VP justificado 10% | Estoque/terreno e recebíveis SÃO o capital de giro: FCFF oscila com landbank e repasses, e o lucro (POC) mede melhor a criação de valor. RIM sobre o PL (estoque a custo) é o método natural, com P/VP justificado como âncora e FCFE (dívida SFH/cessões no fluxo do acionista); DCF com peso baixo porque o FCFF ignora o other_financial (juros capitalizados, custo de cessões); pares MCMV/média-alta são homogêneos (ajustados ao Ke 25%). |
| Infraestrutura e utilities | ECOR3, MOTV3, RAIL3, AURE3, ENGI11, EQTL3, CPLE3, ALUP11, SBSP3, ORVR3 | APV 40%, DCF-FCFF (estudo) 20%, FCFE (DL ∝ receita) 20%, DDM c/ emissões e recompras 20% | Ativos de vida longa, fluxos previsíveis e alavancagem que muda ao longo da concessão (amortização, ciclos de capex): o APV separa valor operacional (Ku) do benefício fiscal da dívida projetada, sem supor wd constante; DCF-WACC como contraparte; DDM/FCFE (40%) porque, com Ke fixo e ROIC < WACC, o EV fica abaixo da dívida e só o lado do acionista (responsabilidade limitada) dá valor positivo. |
| Shoppings (renda imobiliária) | MULT3, IGTI11, ALOS3 | APV 35%, DCF-FCFF (estudo) 35%, FCFE (DL ∝ receita) 15%, DDM c/ emissões e recompras 15% | NOI estável e alavancagem estrutural (CRI/debêntures) → DCF/APV; PL a custo histórico subavalia as propriedades, então RIM/P/VP ficam fora; DDM/FCFE capturam a distribuição recorrente. |
| Locação (capital intensivo) | RENT3, MOVI3, VAMO3 | EVA (fade ROIC) 30%, APV 25%, DCF-FCFF (estudo) 25%, FCFE (DL ∝ receita) 20% | Valor = (ROIC − WACC) × crescimento da frota: EVA explicita o spread e sua convergência; dívida é estrutural e cíclica (APV); DCF como base; FCFE (estrutura de capital constante) evita penalizar a retenção. |
| Varejo e consumo | MGLU3, SBFG3, CEAB3, LREN3, AZZA3, VIVA3, VULC3, ALPA4, NATU3, ASAI3, GMAT3, PGMN3, RADL3, HYPE3 | DCF-FCFF (estudo) 35%, FCFE (DL ∝ receita) 20%, Pares ajustados ao Ke 25% 25%, P/L justificado 20% | Ciclo curto, margens que revertem à média e arrendamentos IFRS-16: a perpetuidade do DCF é frágil e os pares carregam a leitura do ciclo — mas reescalados ao Ke 25% (Gordon, pela TIR implícita de cada par); P/L justificado mantém o múltiplo coerente com o Ke; FCFE evita penalizar a retenção. |
| Serviços, saúde, educação e tecnologia | SMFT3, CVCB3, YDUQ3, COGN3, ANIM3, HAPV3, RDOR3, B3SA3, TOTS3, INTB3, GGPS3, PETR4, PETR3, PRIO3, BRAV3, RECV3, UGPA3, ENEV3, UNIP6, VALE3, CBAV3, GGBR4, USIM5, SUZB3, KLBN11, SLCE3, WEGE3, EMBJ3, POMO4, RAPT4, TUPY3, LEVE3, DXCO3, AXIA3, CMIG4, EGIE3, CPFE3, ISAE4, TAEE11, CSMG3, SAPR11, ABEV3, MDIA3, GRND3, VIVT3, TIMS3, DESK3, BMOB3, LWSA3, FLRY3, PNVL3, SEER3, VTRU3, RIAA3, AUAU3, TFCO4, JSLG3, MILS3, OPCT3, PRNR3, LOGG3 | DCF-FCFF (estudo) 40%, FCFE (DL ∝ receita) 20%, EVA (fade ROIC) 20%, P/L justificado 20% | Asset-light/crescimento: DCF como base; EVA expõe a convergência do ROIC; FCFE (estrutura de capital constante) e P/L justificado como checagens do lado do acionista. |
| Cíclicas / commodities | VBBR3, BEEF3, TTEN3 | DCF-FCFF (estudo) 45%, FCFE (DL ∝ receita) 30%, DDM c/ emissões e recompras 25% | Lucro cíclico e alavancagem alta: DCF com o ciclo projetado explicitamente; FCFE/DDM do lado do acionista. Múltiplos (históricos ou de pares) não normalizam o ciclo a Ke 25% e o PL é comprimido (BEEF3): ficam como referência. |
| Holdings (SOTP) | SIMH3, CSAN3, BRAP4, GOAU4, ITSA4 | SOTP (controladas c/ pesos novos) 100% | SOTP é o único método coerente; recalculado com o valor justo novo das controladas avaliadas pelo motor. |

Princípios: (1) só entram métodos coerentes com Ke 25%; múltiplos de mercado brutos embutem o Ke implícito do mercado e viram referência; (2) para bancos não existe FCFF/EV; (3) o FCFE substitui o DDM onde o payout é baixo e discricionário; (4) o APV entra onde a alavancagem muda ou difere do wd do WACC. Pesos do estudo, para comparação: industrial DCF 50% / DDM 25% / múltiplos-alvo 25%; bancos DDM 50% / múltiplos 50%; holdings SOTP 100% (EZTC3 com 70/10/20). A agregação é a do motor: média de max(0, valor), renormalizada nos métodos disponíveis.

### Efeito por classe

| Classe | n | Δ mediano do valor justo | Upside mediano estudo | Upside mediano proposto |
|---|---|---|---|---|
| Bancos | 14 | -21% | -31% | -47% |
| Incorporadoras | 9 | -14% | +0% | -13% |
| Infraestrutura e utilities | 10 | -61% | -75% | -89% |
| Shoppings (renda imobiliária) | 3 | -30% | -43% | -60% |
| Locação (capital intensivo) | 3 | -14% | -47% | -65% |
| Varejo e consumo | 14 | -24% | -47% | -61% |
| Serviços, saúde, educação e tecnologia | 61 | -30% | -53% | -69% |
| Cíclicas / commodities | 3 | -14% | -67% | -81% |
| Holdings (SOTP) | 5 | -24% | -50% | -62% |

### Esquemas comparados

| Esquema | Upside mediano | Upside > 0 | Spearman escore vs estudo | Spearman upside vs estudo | Oportunidades pela regra (top 8 por escore) |
|---|---|---|---|---|---|
| Estudo (recalculado agora) | -47% | 14 | 1,00 | 1,00 | BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3 |
| Estudo sem múltiplos-alvo (DCF/DDM renormalizados) | -64% | 8 | 0,99 | 0,94 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3, COGN3 |
| **Proposto por classe** | -62% | 8 | 0,99 | 0,91 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3, COGN3 |
| Proposto sem pares ajustados (só intrínsecos) | -62% | 8 | 0,99 | 0,91 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3, COGN3 |
| Peso igual em todos os métodos (inclui mercado bruto) | -45% | 17 | 0,98 | 0,83 | BEEF3, VTRU3, PLPL3, CEAB3, MDNE3, SEER3, COGN3, TEND3 |

Top 10 do escore multifator: estudo BEEF3, VTRU3, HAPV3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3, ANIM3; proposto BEEF3, VTRU3, PLPL3, HAPV3, MDNE3, SEER3, CEAB3, ANIM3, TEND3, COGN3.

Maiores mudanças no ranking por upside (posições; + = sobe): DESK3 -89, CBAV3 -87, BRAV3 +29, PETR3 +24, JSLG3 +23, ASAI3 +22, PETR4 +22, PNVL3 -22, VBBR3 +21, GMAT3 +21.

## As 7 oportunidades

| Empresa | Preço | Valor justo estudo → proposto | Upside estudo → proposto | Rank escore | Rank upside | P(MC) estudo → proposto | Regra (proposto) |
|---|---|---|---|---|---|---|---|
| VTRU3 | 11,98 | 16,99 → 16,72 | +42% → +40% | 2 → 2 | 2 → 2 | 92% → 91% | passa |
| BEEF3 | 2,87 | 5,44 → 4,69 | +89% → +64% | 1 → 1 | 1 → 1 | 79% → 76% | passa |
| SEER3 | 11,03 | 14,19 → 13,50 | +29% → +22% | 7 → 6 | 4 → 4 | 84% → 78% | passa |
| MDNE3 | 16,86 | 20,19 → 18,45 | +20% → +9% | 5 → 5 | 6 → 5 | 79% → 66% | passa |
| PLPL3 | 4,84 | 6,37 → 6,11 | +32% → +26% | 4 → 3 | 3 → 3 | 82% → 76% | passa |
| TEND3 | 21,22 | 26,81 → 23,01 | +26% → +8% | 8 → 9 | 5 → 6 | 79% → 64% | passa |
| CEAB3 | 6,87 | 6,91 → 5,82 | +1% → -15% | 6 → 7 | 13 → 13 | 50% → 37% | não passa |
| COGN3 | 1,69 | 1,97 → 1,79 | +17% → +6% | 9 → 10 | 7 → 7 | 67% → 58% | passa |

Regra do estudo (build.py): TIR de dono ≥ 20%, P(valor justo > preço) ≥ 45%, Altman fora da zona de risco e confiança diferente de baixa. A TIR, o Altman e a confiança não mudam com os pesos; a probabilidade reescala a amostra do Monte Carlo do motor pelo novo valor justo.

- **VTRU3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 17,57, APV 15,98, EVA (fade ROIC) 17,57, DDM (estudo) 12,98, DDM c/ emissões e recompras 12,98, FCFE (DL ∝ receita) 18,08, RIM/Ohlson (fade ROE) 12,98, P/L justificado 12,83, P/VP justificado 20,16, Pares ajustados ao Ke 25% 15,89, Múltiplos-alvo (estudo) 19,82, Pares (mediana) 15,30, Histórico 5a (mediana) 24,62. Divergências: FCFE/DDM = 1,39: payout médio 40% retém caixa que rende Kd·(1−t) < Ke.
- **BEEF3** (Cíclicas / commodities): DCF-FCFF (estudo) 6,37, APV 8,28, EVA (fade ROIC) 5,16, DDM (estudo) 3,27, DDM c/ emissões e recompras 2,59, FCFE (DL ∝ receita) 3,94, RIM/Ohlson (fade ROE) 2,35, P/L justificado 2,13, P/VP justificado 1,01, Múltiplos-alvo (estudo) 5,75, Histórico 5a (mediana) 6,65. Divergências: FCFF acima do lucro (FCFF/LL 2027–30 = 250%) → DCF ≫ RIM/DDM; múltiplos de mercado 1,9× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 18% vs 25%); DDM do estudo ignora a emissão de ações de R$ 930 mi projetada (dividendo cresce com o capital novo, ações fixas): com ela o DDM seria -21%; o RIM (clean surplus) já a desconta.
- **SEER3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 14,34, APV 12,79, EVA (fade ROIC) 13,35, DDM (estudo) 10,66, DDM c/ emissões e recompras 10,66, FCFE (DL ∝ receita) 15,62, RIM/Ohlson (fade ROE) 10,28, P/L justificado 9,88, P/VP justificado 7,74, Pares ajustados ao Ke 25% 12,79, Múltiplos-alvo (estudo) 17,42, Pares (mediana) 12,89, Histórico 5a (mediana) 23,14. Divergências: FCFE/DDM = 1,46: payout médio 42% retém caixa que rende Kd·(1−t) < Ke.
- **MDNE3** (Incorporadoras): DCF-FCFF (estudo) 16,09, APV 16,33, EVA (fade ROIC) 15,86, DDM (estudo) 19,20, DDM c/ emissões e recompras 19,20, FCFE (DL ∝ receita) 21,67, RIM/Ohlson (fade ROE) 19,15, P/L justificado 18,93, P/VP justificado 16,60, Pares ajustados ao Ke 25% 14,85, Múltiplos-alvo (estudo) 22,22, Pares (mediana) 25,93, Histórico 5a (mediana) 33,73.
- **PLPL3** (Incorporadoras): DCF-FCFF (estudo) 7,58, APV 7,77, EVA (fade ROIC) 6,98, DDM (estudo) 5,75, DDM c/ emissões e recompras 5,75, FCFE (DL ∝ receita) 6,69, RIM/Ohlson (fade ROE) 5,71, P/L justificado 5,53, P/VP justificado 4,70, Pares ajustados ao Ke 25% 6,53, Múltiplos-alvo (estudo) 6,25, Pares (mediana) 8,63, Histórico 5a (mediana) 11,48.
- **TEND3** (Incorporadoras): DCF-FCFF (estudo) 32,83, APV 33,22, EVA (fade ROIC) 30,35, DDM (estudo) 21,71, DDM c/ emissões e recompras 21,71, FCFE (DL ∝ receita) 25,82, RIM/Ohlson (fade ROE) 21,12, P/L justificado 22,30, P/VP justificado 12,56, Pares ajustados ao Ke 25% 25,35, Múltiplos-alvo (estudo) 31,22, Pares (mediana) 32,75, Histórico 5a (mediana) 40,80. Divergências: other_financial (R$ -227 mi/ano, -25% do LL) entra no LL (DDM/RIM/FCFE) mas não no FCFF do DCF.
- **CEAB3** (Varejo e consumo): DCF-FCFF (estudo) 4,30, APV 4,73, EVA (fade ROIC) 4,18, DDM (estudo) 5,75, DDM c/ emissões e recompras 5,75, FCFE (DL ∝ receita) 6,67, RIM/Ohlson (fade ROE) 5,75, P/L justificado 5,62, P/VP justificado 6,34, Pares ajustados ao Ke 25% 7,42, Múltiplos-alvo (estudo) 13,26, Pares (mediana) 10,11, Histórico 5a (mediana) 13,74. Divergências: múltiplos de mercado 2,3× a mediana intrínseca (P/L histórico embute Ke ≈ 14%; P/L-alvo embute Ke ≈ 15% vs 25%).
- **COGN3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 1,74, APV 1,55, EVA (fade ROIC) 1,74, DDM (estudo) 1,65, DDM c/ emissões e recompras 1,65, FCFE (DL ∝ receita) 2,37, RIM/Ohlson (fade ROE) 1,65, P/L justificado 1,36, P/VP justificado 4,46, Pares ajustados ao Ke 25% 2,54, Múltiplos-alvo (estudo) 2,76, Pares (mediana) 2,78, Histórico 5a (mediana) 5,06. Divergências: FCFE/DDM = 1,44: payout médio 50% retém caixa que rende Kd·(1−t) < Ke.

## Para os revisores (achados que afetam o estudo)

- **Múltiplos-alvo incoerentes com Ke 25%**: o P/L-alvo mediano embute Ke de ~13%. Para manter os múltiplos no blend, use os justificados (Gordon a 25%) ou os pares ajustados pela TIR implícita.
- **DCF × `other_financial`**: o FCFF exclui `other_financial`, mas o lucro (DDM/RIM/FCFE) inclui. Onde ele é material (AZZA3 -23% do LL, NATU3 -19% do LL, EZTC3 +25% do LL, MRVE3 -163% do LL, PLPL3 -19% do LL, TEND3 -25% do LL, AURE3 +122% do LL, ENGI11 +18% do LL, EQTL3 +52% do LL, VALE3 -22% do LL, DXCO3 +51% do LL, AXIA3 -71% do LL, TAEE11 +35% do LL), trate o item como ajuste debt-like ou como fluxo operacional, para não inflar (ou deprimir) o DCF.
- **DDM × emissão/recompra projetada**: o DDM do motor desconta só dividendos, com o número de ações fixo; o capital novo aumenta o lucro e o dividendo sem diluir. ORVR3: emissão R$ 1.000 mi, recompra R$ 0 mi → DDM -56% com o fluxo de capital; BEEF3: emissão R$ 930 mi, recompra R$ 0 mi → DDM -21% com o fluxo de capital. Corrija no DDM (fluxo líquido ao acionista) ou ajuste o número de ações.
- **wd do WACC × dívida projetada**: em 33 industriais o DCF dá equity ≤ 0. Com Ke fixo, o wd-alvo precisa ser coerente com a alavancagem a que 25% se refere; senão DCF e DDM medem coisas diferentes (ver APV/DCF e FCFE/DDM no JSON).
- **Série de múltiplos históricos**: . Esses meses têm erro de unidade de ações em `multiples_history` (P/L 0,01, P/VP 0,001), e as medianas de `stats` ficam inválidas.
- **Holdings**: componentes "market" fora da foto de preços (nenhum) forçam cotação ao vivo, que falha de forma intermitente e zera o componente. Aqui o cache foi semeado com o último `data/model` do motor.
- **HAPV3**: o PL de R$ 48 bi é quase todo ágio da fusão e o preço implica P/VP de 0,05×. P/VP e RIM com fade não fazem sentido ali; o fade só corrói retorno excedente.

## Tabela completa (59)

Valores por ação/unit (R$). Rank = escore multifator do build.py recalculado; ↑ = rank por upside. Ordem: rank proposto.

| Empresa | Classe | Preço | DCF | DDM | Múlt. | RIM | EVA | APV | FCFE | P/L j | P/VP j | Pares Ke | Pares | Hist. | Justo estudo | Justo proposto | Upside estudo | Upside proposto | Rank | ↑ Rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BEEF3 | Cíclicas / commodities | 2,87 | 6,37 | 3,27 | 5,75 | 2,35 | 5,16 | 8,28 | 3,94 | 2,13 | 1,01 | — | — | 6,65 | 5,44 | 4,69 | +89% | +64% | 1 → 1 | 1 → 1 |
| VTRU3 | Serviços, saúde, educação e tecnologia | 11,98 | 17,57 | 12,98 | 19,82 | 12,98 | 17,57 | 15,98 | 18,08 | 12,83 | 20,16 | 15,89 | 15,30 | 24,62 | 16,99 | 16,72 | +42% | +40% | 2 → 2 | 2 → 2 |
| PLPL3 | Incorporadoras | 4,84 | 7,58 | 5,75 | 6,25 | 5,71 | 6,98 | 7,77 | 6,69 | 5,53 | 4,70 | 6,53 | 8,63 | 11,48 | 6,37 | 6,11 | +32% | +26% | 4 → 3 | 3 → 3 |
| HAPV3 | Serviços, saúde, educação e tecnologia | 4,21 | 2,52 | 5,57 | 8,67 | 5,57 | 2,52 | 4,46 | 8,78 | 2,78 | 50,58 | 4,13 | 16,92 | 80,90 | 4,82 | 3,82 | +14% | -9% | 3 → 4 | 8 → 9 |
| MDNE3 | Incorporadoras | 16,86 | 16,09 | 19,20 | 22,22 | 19,15 | 15,86 | 16,33 | 21,67 | 18,93 | 16,60 | 14,85 | 25,93 | 33,73 | 20,19 | 18,45 | +20% | +9% | 5 → 5 | 6 → 5 |
| SEER3 | Serviços, saúde, educação e tecnologia | 11,03 | 14,34 | 10,66 | 17,42 | 10,28 | 13,35 | 12,79 | 15,62 | 9,88 | 7,74 | 12,79 | 12,89 | 23,14 | 14,19 | 13,50 | +29% | +22% | 7 → 6 | 4 → 4 |
| CEAB3 | Varejo e consumo | 6,87 | 4,30 | 5,75 | 13,26 | 5,75 | 4,18 | 4,73 | 6,67 | 5,62 | 6,34 | 7,42 | 10,11 | 13,74 | 6,91 | 5,82 | +1% | -15% | 6 → 7 | 13 → 13 |
| ANIM3 | Serviços, saúde, educação e tecnologia | 2,43 | 2,43 | 2,07 | 3,21 | 2,07 | 2,24 | 1,43 | 3,71 | 1,60 | 4,16 | 2,88 | 1,81 | 10,16 | 2,54 | 2,48 | +4% | +2% | 10 → 8 | 10 → 8 |
| TEND3 | Incorporadoras | 21,22 | 32,83 | 21,71 | 31,22 | 21,12 | 30,35 | 33,22 | 25,82 | 22,30 | 12,56 | 25,35 | 32,75 | 40,80 | 26,81 | 23,01 | +26% | +8% | 8 → 9 | 5 → 6 |
| COGN3 | Serviços, saúde, educação e tecnologia | 1,69 | 1,74 | 1,65 | 2,76 | 1,65 | 1,74 | 1,55 | 2,37 | 1,36 | 4,46 | 2,54 | 2,78 | 5,06 | 1,97 | 1,79 | +17% | +6% | 9 → 10 | 7 → 7 |
| SBFG3 | Varejo e consumo | 5,08 | -0,39 | 4,57 | 9,51 | 4,57 | -0,46 | 0,09 | 6,08 | 4,47 | 5,56 | 6,05 | 6,70 | 15,75 | 3,52 | 3,62 | -31% | -29% | 15 → 11 | 38 → 20 |
| MOVI3 | Locação (capital intensivo) | 6,62 | -0,39 | 5,80 | 10,98 | 5,61 | -1,64 | 8,09 | 9,15 | 5,41 | 5,26 | 6,29 | 15,79 | 16,05 | 4,19 | 3,85 | -37% | -42% | 14 → 12 | 46 → 32 |
| POMO4 | Serviços, saúde, educação e tecnologia | 3,89 | 3,63 | 3,23 | 5,34 | 3,23 | 3,59 | 3,60 | 3,65 | 3,15 | 2,90 | 3,53 | 5,37 | 8,06 | 3,96 | 3,53 | +2% | -9% | 12 → 13 | 11 → 10 |
| LEVE3 | Serviços, saúde, educação e tecnologia | 31,17 | 19,08 | 20,86 | 30,92 | 20,86 | 19,05 | 19,01 | 24,50 | 20,64 | 13,89 | — | — | 33,66 | 22,49 | 20,47 | -28% | -34% | 19 → 14 | 34 → 27 |
| SAUD3 | Bancos | 14,64 | — | 6,57 | 13,35 | 6,57 | — | — | — | 6,26 | 5,66 | — | — | — | 9,96 | 6,34 | -32% | -57% | 16 → 15 | 43 → 51 |
| BRAP4 | Holdings (SOTP) | 18,02 | — | — | — | — | — | — | — | — | — | — | — | 14,36 | 3,92 | 2,10 | -78% | -88% | 21 → 16 | 112 → 106 |
| CYRE3 | Incorporadoras | 17,74 | 15,12 | 15,95 | 21,92 | 15,95 | 15,03 | 15,57 | 17,66 | 15,06 | 14,76 | 12,85 | 23,25 | 27,18 | 17,76 | 15,62 | +0% | -12% | 13 → 17 | 14 → 11 |
| PGMN3 | Varejo e consumo | 2,63 | 1,24 | 2,01 | 4,58 | 2,01 | 1,18 | 1,43 | 2,80 | 1,82 | 2,61 | 2,37 | 8,38 | 6,29 | 2,27 | 1,95 | -14% | -26% | 22 → 18 | 22 → 16 |
| LREN3 | Varejo e consumo | 9,31 | 6,18 | 7,40 | 15,39 | 7,34 | 6,14 | 6,45 | 7,46 | 5,76 | 6,47 | 5,80 | 9,09 | 23,05 | 8,79 | 6,26 | -6% | -33% | 11 → 19 | 16 → 25 |
| PINE4 | Bancos | 10,66 | — | 9,34 | 11,49 | 9,33 | — | — | — | 11,29 | 6,02 | 7,56 | 12,82 | 10,56 | 9,45 | 8,50 | -11% | -20% | 20 → 20 | 19 → 14 |
| CURY3 | Incorporadoras | 26,37 | 21,43 | 19,94 | 28,42 | 19,32 | 20,16 | 21,43 | 20,17 | 17,98 | 10,75 | 16,41 | 17,03 | 41,98 | 22,89 | 18,41 | -13% | -30% | 17 → 21 | 21 → 21 |
| BBSE3 | Bancos | 41,40 | — | 23,85 | 32,67 | 23,76 | — | — | — | 21,53 | 17,92 | 13,68 | 33,10 | 38,62 | 28,26 | 22,32 | -32% | -46% | 25 → 22 | 41 → 36 |
| DIRR3 | Incorporadoras | 8,60 | 8,67 | 7,33 | 10,68 | 7,33 | 8,13 | 8,76 | 7,88 | 7,28 | 5,59 | 7,62 | 8,03 | 18,55 | 8,59 | 7,44 | -0% | -13% | 24 → 23 | 15 → 12 |
| PETR4 | Serviços, saúde, educação e tecnologia | 52,73 | 21,35 | 28,46 | 47,25 | 28,46 | 21,07 | 22,40 | 33,25 | 47,27 | 21,32 | 28,25 | 58,53 | 43,40 | 29,60 | 28,86 | -44% | -45% | 29 → 24 | 57 → 35 |
| BBAS3 | Bancos | 16,84 | — | 12,62 | 19,41 | 12,49 | — | — | — | 11,49 | 14,67 | 16,20 | 23,97 | 18,50 | 15,67 | 13,07 | -7% | -22% | 23 → 25 | 17 → 15 |
| YDUQ3 | Serviços, saúde, educação e tecnologia | 8,76 | 6,26 | 6,19 | 9,69 | 6,19 | 6,26 | 6,11 | 8,94 | 2,67 | 8,60 | 3,46 | 6,50 | 12,16 | 7,10 | 6,08 | -19% | -31% | 26 → 26 | 27 → 22 |
| TFCO4 | Serviços, saúde, educação e tecnologia | 10,08 | 4,70 | 4,11 | 13,24 | 4,11 | 4,70 | 4,67 | 4,47 | 4,44 | 3,63 | 4,67 | 9,57 | — | 6,69 | 4,60 | -34% | -54% | 28 → 27 | 44 → 46 |
| PETR3 | Serviços, saúde, educação e tecnologia | 59,12 | 21,35 | 28,46 | 47,25 | 28,46 | 21,07 | 22,40 | 33,25 | 47,27 | 21,32 | 28,26 | 56,94 | 47,30 | 29,60 | 28,86 | -50% | -51% | 33 → 28 | 66 → 42 |
| RIAA3 | Serviços, saúde, educação e tecnologia | 6,33 | 2,63 | 3,80 | 9,63 | 3,80 | 2,63 | 3,16 | 4,51 | 3,76 | 4,84 | 4,92 | 6,56 | — | 4,67 | 3,23 | -26% | -49% | 27 → 29 | 33 → 39 |
| VIVA3 | Varejo e consumo | 17,63 | 9,79 | 9,59 | 24,07 | 9,59 | 9,64 | 9,64 | 11,20 | 9,26 | 10,16 | 10,02 | 20,29 | 36,16 | 13,31 | 10,02 | -24% | -43% | 31 → 30 | 32 → 34 |
| SUZB3 | Serviços, saúde, educação e tecnologia | 48,19 | 6,60 | 18,48 | 27,69 | 18,48 | 6,60 | 9,53 | 32,77 | 17,09 | 20,64 | 33,78 | 77,82 | 44,62 | 14,84 | 13,93 | -69% | -71% | 34 → 31 | 97 → 76 |
| BBDC3 | Bancos | 13,40 | — | 9,95 | 16,68 | 9,83 | — | — | — | 9,08 | 9,60 | 11,12 | 19,33 | 17,29 | 12,37 | 9,80 | -8% | -27% | 30 → 32 | 18 → 17 |
| VULC3 | Varejo e consumo | 11,77 | 7,79 | 7,84 | 15,41 | 7,84 | 7,79 | 7,77 | 8,14 | 7,15 | 7,18 | 7,02 | 18,28 | 20,68 | 9,70 | 7,54 | -18% | -36% | 32 → 33 | 26 → 28 |
| SIMH3 | Holdings (SOTP) | 5,24 | — | — | — | — | — | — | — | — | — | — | — | 17,35 | 2,26 | 1,96 | -57% | -63% | 39 → 34 | 75 → 63 |
| VAMO3 | Locação (capital intensivo) | 2,57 | -0,29 | 1,27 | 2,55 | 1,23 | -0,61 | 1,83 | 1,82 | 1,20 | 1,21 | 1,43 | 1,91 | 9,76 | 0,96 | 0,82 | -63% | -68% | 38 → 35 | 85 → 72 |
| RENT3 | Locação (capital intensivo) | 29,74 | 7,02 | 15,26 | 34,26 | 15,12 | 7,02 | 12,39 | 16,70 | 13,66 | 13,49 | 14,88 | 21,63 | 81,33 | 15,89 | 10,30 | -47% | -65% | 35 → 36 | 61 → 66 |
| ASAI3 | Varejo e consumo | 7,81 | -1,87 | 3,03 | 5,94 | 3,01 | -1,87 | 0,74 | 5,45 | 2,69 | 3,08 | 2,15 | 7,41 | 14,80 | 2,24 | 2,17 | -71% | -72% | 43 → 37 | 101 → 79 |
| ECOR3 | Infraestrutura e utilities | 5,27 | -21,44 | 2,99 | 5,59 | 2,99 | -21,44 | -12,12 | 1,36 | 2,41 | 3,99 | 3,15 | 12,90 | 7,70 | 2,15 | 0,87 | -59% | -83% | 36 → 38 | 80 → 93 |
| BBDC4 | Bancos | 14,71 | — | 9,95 | 16,68 | 9,83 | — | — | — | 9,08 | 9,60 | 8,24 | 10,56 | 19,80 | 12,37 | 9,80 | -16% | -33% | 40 → 39 | 24 → 26 |
| EZTC3 | Incorporadoras | 9,59 | 10,11 | 6,24 | 14,97 | 6,24 | 10,11 | 10,11 | 7,26 | 5,54 | 5,66 | 7,68 | 7,78 | 15,14 | 10,69 | 6,99 | +11% | -27% | 18 → 40 | 9 → 18 |
| ALOS3 | Shoppings (renda imobiliária) | 24,44 | 8,78 | 10,56 | 24,16 | 10,56 | 8,78 | 9,21 | 11,00 | 8,26 | 25,70 | 9,35 | 22,22 | 27,65 | 13,07 | 9,53 | -47% | -61% | 44 → 41 | 60 → 60 |
| INTB3 | Serviços, saúde, educação e tecnologia | 14,36 | 5,97 | 6,02 | 14,98 | 6,02 | 5,97 | 5,97 | 6,67 | 6,06 | 6,06 | — | — | 23,45 | 8,23 | 6,13 | -43% | -57% | 46 → 42 | 55 → 53 |
| BRSR6 | Bancos | 12,94 | — | 9,26 | 13,71 | 9,32 | — | — | — | 8,67 | 9,41 | 14,06 | 20,80 | 17,49 | 10,91 | 9,33 | -16% | -28% | 37 → 43 | 23 → 19 |
| HYPE3 | Varejo e consumo | 21,60 | 7,08 | 9,08 | 19,79 | 9,08 | 7,08 | 6,42 | 12,45 | 8,22 | 10,25 | 10,72 | 17,33 | 37,06 | 10,76 | 9,29 | -50% | -57% | 48 → 44 | 67 → 52 |
| GMAT3 | Varejo e consumo | 3,54 | -0,37 | 1,29 | 3,62 | 1,29 | -0,37 | -0,34 | 1,39 | 1,46 | 2,19 | 2,47 | 4,25 | 8,23 | 1,23 | 1,19 | -65% | -66% | 49 → 45 | 89 → 68 |
| GGPS3 | Serviços, saúde, educação e tecnologia | 10,89 | 5,19 | 5,16 | 14,33 | 5,15 | 4,99 | 5,16 | 6,63 | 4,21 | 5,06 | 5,05 | 12,08 | 24,05 | 7,47 | 5,24 | -31% | -52% | 42 → 46 | 39 → 43 |
| AUAU3 | Serviços, saúde, educação e tecnologia | 3,86 | 1,39 | 1,85 | 5,21 | 1,85 | 1,39 | 1,51 | 2,57 | 1,36 | 2,04 | 1,44 | 2,66 | — | 2,46 | 1,62 | -36% | -58% | 45 → 47 | 45 → 56 |
| AZZA3 | Varejo e consumo | 15,07 | 5,18 | 5,11 | 12,12 | 5,11 | 5,18 | 4,52 | 7,33 | 1,82 | 19,88 | 2,58 | 3,84 | 25,46 | 6,90 | 4,29 | -54% | -72% | 41 → 48 | 72 → 77 |
| MDIA3 | Serviços, saúde, educação e tecnologia | 15,73 | 8,61 | 7,11 | 20,17 | 7,11 | 8,61 | 8,61 | 8,31 | 6,63 | 9,25 | — | — | 28,77 | 11,12 | 8,15 | -29% | -48% | 47 → 49 | 35 → 37 |
| PRIO3 | Serviços, saúde, educação e tecnologia | 72,29 | 47,48 | 43,75 | 65,12 | 42,97 | 45,18 | 46,80 | 57,26 | 50,84 | 23,84 | 29,45 | 61,53 | 55,64 | 50,96 | 49,65 | -30% | -31% | 55 → 50 | 36 → 23 |
| ABEV3 | Serviços, saúde, educação e tecnologia | 15,18 | 7,06 | 6,03 | 14,64 | 6,03 | 6,89 | 7,06 | 6,35 | 4,71 | 5,73 | — | — | 15,99 | 8,70 | 6,41 | -43% | -58% | 51 → 51 | 56 → 54 |
| JSLG3 | Serviços, saúde, educação e tecnologia | 5,62 | -0,49 | 2,20 | 3,94 | 2,05 | -1,27 | 2,59 | 7,01 | 0,76 | 2,07 | 1,28 | 9,57 | 8,39 | 1,53 | 1,55 | -73% | -72% | 58 → 52 | 103 → 80 |
| PSSA3 | Bancos | 46,89 | — | 23,00 | 47,88 | 22,12 | — | — | — | 22,91 | 18,87 | 50,52 | 108,32 | 47,21 | 35,44 | 21,53 | -24% | -54% | 50 → 53 | 31 → 45 |
| ITSA4 | Holdings (SOTP) | 12,91 | — | — | — | — | — | — | — | — | — | — | — | 11,60 | 9,79 | 7,41 | -24% | -43% | 52 → 54 | 29 → 33 |
| ABCB4 | Bancos | 23,05 | — | 13,59 | 20,45 | 14,19 | — | — | — | 13,69 | 13,93 | 18,34 | 30,06 | 22,87 | 16,16 | 13,97 | -30% | -39% | 61 → 55 | 37 → 30 |
| MOTV3 | Infraestrutura e utilities | 14,61 | -1,75 | 5,43 | 15,94 | 5,43 | -1,75 | 0,76 | 5,41 | 4,88 | 6,93 | 6,64 | 11,64 | — | 5,34 | 2,47 | -63% | -83% | 56 → 56 | 86 → 92 |
| MULT3 | Shoppings (renda imobiliária) | 25,84 | 9,54 | 11,42 | 28,84 | 11,42 | 9,54 | 9,30 | 13,81 | 10,57 | 13,76 | 12,44 | 27,17 | 39,93 | 14,84 | 10,38 | -43% | -60% | 57 → 57 | 54 → 57 |
| B3SA3 | Serviços, saúde, educação e tecnologia | 14,66 | 5,90 | 5,56 | 13,23 | 5,47 | 5,65 | 5,94 | 5,66 | 4,53 | 4,68 | — | — | 16,26 | 7,65 | 5,53 | -48% | -62% | 60 → 58 | 64 → 62 |
| RECV3 | Serviços, saúde, educação e tecnologia | 11,14 | 1,68 | 5,81 | 11,22 | 5,81 | 1,68 | 1,61 | 7,39 | 7,69 | 6,47 | 4,97 | 10,58 | 13,11 | 5,10 | 4,02 | -54% | -64% | 64 → 59 | 73 → 64 |
| OPCT3 | Serviços, saúde, educação e tecnologia | 8,92 | 1,23 | 3,28 | 8,67 | 3,19 | 0,83 | 2,33 | 5,61 | 2,96 | 2,97 | 2,04 | 3,77 | 4,81 | 3,60 | 2,37 | -60% | -73% | 62 → 60 | 82 → 82 |
| USIM5 | Serviços, saúde, educação e tecnologia | 5,68 | 2,65 | 2,07 | 6,58 | 2,07 | 2,65 | 2,62 | 2,71 | 2,01 | 3,21 | 2,29 | 8,70 | -1,27 | 3,49 | 2,54 | -39% | -55% | 53 → 61 | 49 → 49 |
| BRAV3 | Serviços, saúde, educação e tecnologia | 18,45 | 0,94 | 6,82 | 17,65 | 6,82 | 0,94 | 2,01 | 15,12 | 18,28 | 14,14 | 10,74 | 22,95 | 30,39 | 6,59 | 7,24 | -64% | -61% | 80 → 62 | 87 → 58 |
| BMOB3 | Serviços, saúde, educação e tecnologia | 24,42 | 12,26 | 11,15 | 24,05 | 11,15 | 12,26 | 12,26 | 10,36 | 8,22 | 11,30 | 11,63 | 31,52 | 23,68 | 14,93 | 11,07 | -39% | -55% | 66 → 63 | 50 → 48 |
| SAPR11 | Serviços, saúde, educação e tecnologia | 32,42 | -2,87 | 11,64 | 29,42 | 11,64 | -2,87 | 1,31 | 9,71 | 14,53 | 16,02 | 18,50 | 77,00 | 19,74 | 10,26 | 4,85 | -68% | -85% | 67 → 64 | 94 → 97 |
| LWSA3 | Serviços, saúde, educação e tecnologia | 3,41 | 2,42 | 1,70 | 4,77 | 1,70 | 2,42 | 2,42 | 1,78 | 1,28 | 4,34 | 1,83 | 5,63 | — | 2,82 | 2,06 | -17% | -39% | 59 → 65 | 25 → 31 |
| CPFE3 | Serviços, saúde, educação e tecnologia | 42,97 | -3,40 | 15,34 | 34,90 | 15,04 | -3,76 | 2,89 | 13,55 | 14,05 | 11,06 | 10,50 | 55,96 | 42,08 | 12,56 | 5,52 | -71% | -87% | 68 → 66 | 98 → 103 |
| TOTS3 | Serviços, saúde, educação e tecnologia | 34,09 | 10,92 | 10,12 | 34,23 | 10,04 | 10,48 | 11,21 | 13,50 | 6,76 | 10,01 | 8,48 | 15,80 | 62,91 | 16,55 | 10,52 | -51% | -69% | 69 → 67 | 69 → 74 |
| GRND3 | Serviços, saúde, educação e tecnologia | 3,65 | 2,65 | 1,90 | 3,85 | 1,90 | 2,65 | 2,65 | 1,85 | 1,51 | 1,65 | 1,86 | 4,13 | 5,42 | 2,76 | 2,26 | -24% | -38% | 70 → 68 | 30 → 29 |
| UNIP6 | Serviços, saúde, educação e tecnologia | 50,61 | 9,57 | 16,54 | 27,47 | 16,05 | 8,44 | 13,54 | 18,06 | 12,01 | 12,32 | — | — | 28,13 | 15,79 | 11,53 | -69% | -77% | 72 → 69 | 95 → 86 |
| KLBN11 | Serviços, saúde, educação e tecnologia | 17,63 | -0,20 | 6,19 | 6,62 | 5,90 | -0,20 | 0,07 | 8,65 | 3,08 | 4,04 | 5,23 | 11,67 | 9,92 | 3,20 | 2,35 | -82% | -87% | 74 → 70 | 116 → 98 |
| RDOR3 | Serviços, saúde, educação e tecnologia | 33,80 | 8,40 | 10,77 | 27,06 | 10,53 | 7,96 | 10,79 | 13,23 | 9,49 | 8,05 | 12,56 | 21,13 | 53,01 | 13,66 | 9,50 | -60% | -72% | 73 → 71 | 81 → 78 |
| PNVL3 | Serviços, saúde, educação e tecnologia | 10,56 | -1,17 | 3,47 | 14,06 | 3,47 | -1,17 | 0,53 | 3,57 | 3,37 | 4,30 | 4,08 | 13,79 | 16,52 | 4,38 | 1,39 | -58% | -87% | 65 → 72 | 78 → 100 |
| RAPT4 | Serviços, saúde, educação e tecnologia | 3,67 | -3,20 | 1,72 | 5,97 | 1,72 | -3,22 | -1,24 | 3,13 | 1,37 | 3,90 | 1,81 | 2,35 | 1,87 | 1,92 | 0,90 | -48% | -75% | 54 → 73 | 63 → 84 |
| JHSF3 | Incorporadoras | 9,50 | -0,85 | 2,15 | 4,66 | 2,15 | -0,85 | -0,61 | 1,81 | 2,11 | 4,53 | 2,74 | 2,49 | 15,29 | 2,62 | 2,20 | -72% | -77% | 78 → 74 | 102 → 85 |
| SMFT3 | Serviços, saúde, educação e tecnologia | 15,99 | -3,41 | 5,69 | 21,80 | 5,69 | -3,41 | 0,12 | 7,67 | 5,02 | 7,36 | — | — | 29,08 | 6,87 | 2,54 | -57% | -84% | 71 → 75 | 76 → 95 |
| ALUP11 | Infraestrutura e utilities | 31,94 | -3,24 | 9,49 | 27,47 | 9,49 | -3,24 | -5,08 | 11,21 | 8,93 | 14,28 | 9,79 | 51,41 | 39,62 | 9,24 | 4,14 | -71% | -87% | 75 → 76 | 99 → 102 |
| VIVT3 | Serviços, saúde, educação e tecnologia | 30,85 | 9,96 | 12,97 | 26,30 | 12,97 | 9,96 | 11,06 | 13,51 | 9,56 | 20,54 | 12,49 | 33,79 | 33,51 | 14,80 | 10,59 | -52% | -66% | 77 → 77 | 70 → 67 |
| ALPA4 | Varejo e consumo | 13,35 | 5,04 | 3,85 | 12,18 | 3,85 | 5,04 | 4,99 | 4,67 | 3,75 | 3,73 | 3,92 | 7,75 | 22,22 | 6,53 | 4,43 | -51% | -67% | 76 → 78 | 68 → 70 |
| RADL3 | Varejo e consumo | 15,67 | 2,07 | 4,52 | 16,96 | 4,50 | 1,98 | 2,92 | 5,18 | 3,95 | 3,96 | 3,88 | 10,14 | 33,22 | 6,41 | 3,52 | -59% | -78% | 79 → 79 | 79 → 87 |
| IGTI11 | Shoppings (renda imobiliária) | 22,70 | 9,45 | 9,01 | 26,51 | 9,01 | 9,45 | 9,36 | 11,03 | 8,56 | 16,66 | 10,02 | 23,96 | 38,13 | 13,60 | 9,59 | -40% | -58% | 81 → 80 | 51 → 55 |
| ITUB4 | Bancos | 39,90 | — | 19,71 | 34,25 | 20,19 | — | — | — | 17,71 | 15,81 | 13,71 | 21,01 | 37,44 | 25,13 | 18,97 | -37% | -52% | 82 → 81 | 47 → 44 |
| SLCE3 | Serviços, saúde, educação e tecnologia | 16,88 | 9,89 | 3,91 | 17,45 | 3,91 | 9,89 | 14,18 | 3,67 | 3,49 | 5,46 | 3,36 | 10,92 | 11,31 | 11,56 | 7,37 | -32% | -56% | 63 → 82 | 40 → 50 |
| WEGE3 | Serviços, saúde, educação e tecnologia | 47,38 | 5,61 | 5,74 | 27,79 | 5,74 | 5,61 | 5,59 | 6,10 | 6,24 | 5,00 | — | — | 50,07 | 11,19 | 5,84 | -76% | -88% | 84 → 83 | 109 → 105 |
| BPAC11 | Bancos | 56,38 | — | 18,90 | 47,97 | 19,54 | — | — | — | 21,06 | 17,22 | 14,22 | 18,23 | 58,91 | 29,59 | 18,80 | -48% | -67% | 83 → 84 | 62 → 69 |
| FLRY3 | Serviços, saúde, educação e tecnologia | 21,67 | 4,99 | 7,56 | 19,85 | 7,41 | 4,79 | 6,36 | 8,95 | 5,38 | 5,98 | 8,00 | 16,47 | 20,10 | 9,35 | 5,82 | -57% | -73% | 85 → 85 | 74 → 81 |
| MILS3 | Serviços, saúde, educação e tecnologia | 15,56 | 4,50 | 5,50 | 14,47 | 5,50 | 4,50 | 5,31 | 6,46 | 5,47 | 5,38 | 7,96 | 18,23 | 19,25 | 7,24 | 5,09 | -53% | -67% | 87 → 86 | 71 → 71 |
| DXCO3 | Serviços, saúde, educação e tecnologia | 4,61 | -0,61 | 1,10 | 3,56 | 1,10 | -0,61 | 0,68 | 1,85 | 0,51 | 2,18 | 0,97 | 5,36 | 4,79 | 1,16 | 0,47 | -75% | -90% | 88 → 87 | 106 → 110 |
| GOAU4 | Holdings (SOTP) | 10,62 | — | — | — | — | — | — | — | — | — | — | — | 6,43 | 5,32 | 4,01 | -50% | -62% | 89 → 88 | 65 → 61 |
| CXSE3 | Bancos | 21,16 | — | 8,87 | 15,99 | 8,76 | — | — | — | 7,08 | 6,72 | 9,27 | 17,45 | 16,39 | 12,43 | 8,28 | -41% | -61% | 92 → 89 | 53 → 59 |
| EGIE3 | Serviços, saúde, educação e tecnologia | 27,30 | 0,31 | 7,57 | 20,54 | 7,57 | 0,23 | 2,24 | 9,77 | 7,50 | 8,34 | 5,61 | 26,67 | 27,37 | 7,18 | 3,63 | -74% | -87% | 93 → 90 | 104 → 99 |
| MRVE3 | Incorporadoras | 4,27 | 4,93 | 1,36 | 4,63 | 1,36 | 4,41 | 6,98 | 1,50 | 0,99 | 3,10 | 1,49 | 1,33 | 25,54 | 2,34 | 1,94 | -45% | -55% | 90 → 91 | 59 → 47 |
| GGBR4 | Serviços, saúde, educação e tecnologia | 23,99 | 6,94 | 7,50 | 18,80 | 7,50 | 6,94 | 7,19 | 9,70 | 7,32 | 7,98 | 6,24 | 14,41 | 9,68 | 10,05 | 7,57 | -58% | -68% | 94 → 92 | 77 → 73 |
| SANB11 | Bancos | 24,33 | — | 12,38 | 22,67 | 12,22 | — | — | — | 10,76 | 13,22 | 15,58 | 23,87 | 29,90 | 16,59 | 12,51 | -32% | -49% | 95 → 93 | 42 → 38 |
| IRBR3 | Bancos | 56,58 | — | 29,10 | 47,39 | 28,87 | — | — | — | 23,43 | 26,26 | 73,75 | 185,18 | 39,17 | 35,09 | 28,28 | -38% | -50% | 96 → 94 | 48 → 40 |
| EMBJ3 | Serviços, saúde, educação e tecnologia | 96,75 | 22,51 | 14,95 | 62,79 | 14,95 | 22,28 | 22,29 | 19,67 | 16,83 | 16,13 | 19,98 | 34,50 | — | 30,69 | 20,76 | -68% | -79% | 98 → 95 | 93 → 88 |
| VBBR3 | Cíclicas / commodities | 30,76 | 1,78 | 8,27 | 15,40 | 8,27 | 1,78 | 3,60 | 10,35 | 7,17 | 14,87 | 4,13 | 5,99 | 40,56 | 6,81 | 5,97 | -78% | -81% | 100 → 96 | 110 → 89 |
| CMIG4 | Serviços, saúde, educação e tecnologia | 10,15 | -3,29 | 3,36 | 6,88 | 3,36 | -3,29 | -1,75 | 1,01 | 4,38 | 5,22 | 4,36 | 17,48 | 7,94 | 2,56 | 1,08 | -75% | -89% | 97 → 97 | 107 → 108 |
| VALE3 | Serviços, saúde, educação e tecnologia | 61,08 | -21,94 | 10,88 | 18,98 | 10,88 | -21,94 | -18,11 | 5,05 | 10,30 | 13,20 | 6,65 | 62,98 | 24,78 | 7,46 | 3,07 | -88% | -95% | 102 → 98 | 121 → 116 |
| EQTL3 | Infraestrutura e utilities | 34,07 | -15,58 | 3,14 | 17,46 | 3,14 | -15,58 | -5,32 | 2,67 | 2,48 | 10,41 | 2,88 | 24,77 | 17,27 | 5,15 | 1,16 | -85% | -97% | 101 → 99 | 118 → 119 |
| UGPA3 | Serviços, saúde, educação e tecnologia | 32,70 | 8,96 | 10,06 | 23,20 | 10,06 | 8,96 | 9,35 | 11,59 | 10,74 | 10,84 | 5,75 | 12,69 | 39,28 | 12,79 | 9,84 | -61% | -70% | 103 → 100 | 84 → 75 |
| TAEE11 | Serviços, saúde, educação e tecnologia | 40,04 | 7,04 | 11,57 | 20,36 | 10,96 | 4,98 | 5,76 | 14,33 | 5,41 | 3,19 | 6,11 | 25,11 | 37,34 | 11,50 | 7,76 | -71% | -81% | 106 → 101 | 100 → 90 |
| ENGI11 | Infraestrutura e utilities | 45,24 | -34,03 | 6,82 | 32,65 | 6,82 | -34,03 | -14,62 | 1,34 | 6,32 | 19,38 | 7,87 | 58,85 | 33,24 | 9,87 | 1,63 | -78% | -96% | 104 → 102 | 111 → 118 |
| CPLE3 | Infraestrutura e utilities | 14,67 | -1,94 | 3,20 | 7,97 | 3,20 | -1,94 | -0,53 | 2,72 | 2,73 | 4,16 | 3,28 | 15,38 | 11,76 | 2,79 | 1,18 | -81% | -92% | 107 → 103 | 115 → 111 |
| CSMG3 | Serviços, saúde, educação e tecnologia | 49,96 | -12,66 | 10,39 | 37,17 | 10,39 | -12,66 | -5,46 | 4,23 | 10,08 | 14,01 | 8,79 | 53,25 | 21,17 | 11,89 | 2,86 | -76% | -94% | 105 → 104 | 108 → 114 |
| LOGG3 | Serviços, saúde, educação e tecnologia | 21,52 | 3,47 | 5,87 | 14,03 | 5,87 | 3,47 | 4,06 | 7,67 | 2,56 | 26,16 | 3,12 | 7,83 | 30,17 | 6,71 | 4,13 | -69% | -81% | 108 → 105 | 96 → 91 |
| NATU3 | Varejo e consumo | 5,02 | 1,98 | 1,72 | 5,54 | 1,72 | 1,98 | 2,26 | 2,81 | 0,90 | 4,58 | 1,24 | 4,65 | — | 2,81 | 1,75 | -44% | -65% | 99 → 106 | 58 → 65 |
| TTEN3 | Cíclicas / commodities | 10,63 | -0,16 | 3,34 | 10,50 | 3,34 | -0,16 | 0,95 | 2,91 | 4,13 | 5,00 | 4,49 | 16,39 | 7,40 | 3,46 | 1,71 | -67% | -84% | 109 → 107 | 92 → 94 |
| PRNR3 | Serviços, saúde, educação e tecnologia | 12,96 | 0,96 | 3,28 | 12,99 | 3,28 | 0,96 | 4,07 | 4,63 | 2,62 | 5,45 | 3,36 | 12,05 | 17,39 | 4,55 | 2,03 | -65% | -84% | 110 → 108 | 88 → 96 |
| ENEV3 | Serviços, saúde, educação e tecnologia | 26,49 | -2,81 | 2,39 | 8,75 | 2,39 | -2,81 | -0,94 | 3,41 | 1,45 | 5,95 | 1,50 | 8,89 | 18,80 | 2,79 | 0,97 | -89% | -96% | 115 → 109 | 122 → 117 |
| CBAV3 | Serviços, saúde, educação e tecnologia | 11,30 | -4,42 | 0,98 | 10,92 | 0,98 | -4,42 | -3,92 | 1,42 | 1,78 | 2,59 | 0,94 | 11,13 | 11,97 | 8,93 | 0,64 | -21% | -94% | 91 → 110 | 28 → 115 |
| ORVR3 | Infraestrutura e utilities | 15,73 | 1,89 | 2,46 | 15,46 | 1,09 | 1,89 | 2,04 | 3,01 | 2,18 | 3,78 | 2,09 | 12,22 | 8,87 | 5,42 | 2,01 | -66% | -87% | 114 → 111 | 90 → 104 |
| RAIL3 | Infraestrutura e utilities | 14,40 | -2,25 | 3,45 | 16,09 | 3,45 | -2,25 | 0,58 | 2,86 | 4,42 | 5,13 | 6,13 | 10,17 | 26,50 | 4,89 | 1,49 | -66% | -90% | 113 → 112 | 91 → 109 |
| TIMS3 | Serviços, saúde, educação e tecnologia | 19,00 | 9,45 | 10,33 | 15,94 | 10,33 | 9,45 | 9,20 | 11,22 | 7,35 | 10,52 | 9,31 | 25,54 | -2,07 | 11,29 | 9,38 | -41% | -51% | 116 → 113 | 52 → 41 |
| CSAN3 | Holdings (SOTP) | 2,37 | — | — | — | — | — | — | — | — | — | — | — | 2,39 | 2,10 | 1,62 | -11% | -32% | 112 → 114 | 20 → 24 |
| TUPY3 | Serviços, saúde, educação e tecnologia | 15,41 | 0,60 | 7,84 | 15,12 | 7,84 | 0,30 | 2,31 | 11,34 | 6,61 | 9,33 | 8,89 | 14,15 | -15,74 | 6,04 | 3,89 | -61% | -75% | 111 → 115 | 83 → 83 |
| SBSP3 | Infraestrutura e utilities | 24,90 | -9,03 | 3,29 | 18,15 | 3,29 | -9,03 | -5,43 | -0,43 | 4,54 | 6,42 | 5,32 | 23,36 | 26,73 | 5,36 | 0,66 | -78% | -97% | 117 → 116 | 113 → 120 |
| MGLU3 | Varejo e consumo | 5,14 | -4,26 | 0,23 | 5,00 | 0,23 | -4,36 | -3,31 | -0,07 | — | 2,16 | — | 4,26 | 24,58 | 1,31 | 0,00 | -75% | -100% | 118 → 117 | 105 → 121 |
| AURE3 | Infraestrutura e utilities | 11,06 | -4,88 | 0,94 | 5,29 | 0,94 | -4,88 | -3,58 | 4,95 | — | 4,87 | — | 6,21 | 13,02 | 1,56 | 1,18 | -86% | -89% | 119 → 118 | 120 → 107 |
| ISAE4 | Serviços, saúde, educação e tecnologia | 25,24 | -6,25 | 4,79 | 15,72 | 4,79 | -6,25 | -4,32 | 1,82 | 5,99 | 6,76 | 6,02 | 21,63 | — | 5,13 | 1,56 | -80% | -94% | 120 → 119 | 114 → 113 |
| DESK3 | Serviços, saúde, educação e tecnologia | 19,32 | 0,77 | 4,13 | 19,46 | 4,13 | 0,77 | 1,94 | 7,01 | 3,35 | 8,00 | 4,72 | 14,06 | 14,87 | 19,46 | 2,54 | +1% | -87% | 86 → 120 | 12 → 101 |
| CVCB3 | Serviços, saúde, educação e tecnologia | 0,88 | -0,77 | -0,24 | 0,51 | -0,24 | -0,89 | -0,94 | -0,22 | — | 0,32 | — | — | 3,48 | 0,13 | 0,00 | -86% | -100% | 121 → 121 | 119 → 122 |
| AXIA3 | Serviços, saúde, educação e tecnologia | 48,18 | -11,15 | 7,54 | 23,56 | 7,54 | -11,15 | -9,58 | 7,74 | 8,48 | 17,01 | 9,63 | 46,10 | — | 7,77 | 3,24 | -84% | -93% | 122 → 122 | 117 → 112 |

Holdings: SOTP do estudo e SOTP recalculado nas colunas "Justo"; "Hist." = P/VP/P/L históricos consolidados (só referência).

## Limitações

- RIM, EVA, APV e FCFE usam as mesmas projeções do estudo: mudam a lente (âncora em PL/CI, fade, estrutura de capital, política de dívida), não os drivers operacionais. Divergências grandes apontam premissas a revisar, não erros de método.
- O APV ignora custos de dificuldade financeira, relevantes para as alavancadas (MGLU3, CVCB3, AZZA3, ECOR3), e trata o benefício fiscal com o risco do ativo (Harris–Pringle).
- O FCFE com estrutura de capital constante supõe rolar e ampliar a dívida na proporção da receita. Para quem precisa desalavancar (covenants), superestima o fluxo do acionista.
- Pares: a cobertura tem só 1 a 4 pares por segmento, e os múltiplos são da foto pós-queda. VBBR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3, SMFT3 e CVCB3 não têm par na cobertura. O ajuste ao Ke usa a TIR implícita de cada par (DDM do estudo) e vale só para múltiplos de equity.
- P(valor > preço) nos esquemas novos reescala a amostra do Monte Carlo do motor, sem refazer as 5.000 simulações; a TIR implícita, o Altman e a confiança não mudam com os pesos.
- Bancos ficam sem FCFF/EVA/APV, e o FCFE coincide com o DDM porque o PL projetado é o capital exigido.
