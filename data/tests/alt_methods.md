# Métodos alternativos de valuation e novos pesos (Ke 25%)

*Gerado em 2026-11-18T14:19:06 por `pipeline/tests/alt_methods.py`. Motor `pipeline/model.py` importado sem alterações, premissas lidas de `research/` no momento da execução (os revisores seguem ajustando; rode de novo para atualizar), preços da foto do estudo. Valores por ação/unit, comparáveis ao preço. Dados completos em `data/tests/alt_methods.json`.*

## Resumo

1. **Os métodos intrínsecos alternativos confirmam DCF e DDM.** Mediana por empresa em relação ao DDM: RIM 1,00×, P/L justificado 0,95×, P/VP justificado 1,13×, FCFE 1,17×, pares ajustados ao Ke 1,07×. Em relação ao DCF: APV 1,01× e EVA 1,00×. RIM ≡ DDM e EVA ≡ DCF são identidades quando a perpetuidade é a mesma (erro máximo 7e-15 e 1e-15, relativo). As diferenças vêm só do fade do retorno excedente (RIM em 35 empresas, EVA em 40) e da política de dívida (APV e FCFE).
2. **O viés está nos métodos de mercado.** Na mediana, os múltiplos-alvo do estudo ficam 2,78× o DCF, os pares 2,52× e a mediana histórica de 5 anos 3,86×. Eles embutem Ke de cerca de 13% (P/L-alvo) e 12% (P/L histórico), e o preço de hoje embute uma TIR de dono mediana de 13%: nenhum deles está em 25%. Com 25% de peso, a perna de múltiplos-alvo responde, na mediana, por 52% do valor justo industrial do estudo. Nos bancos, com 50% de peso, responde por 0%.
3. **Onde e por que divergem.** (i) Alavancagem com Ke fixo: 35 das 53 industriais têm DCF ≤ 0 (EV abaixo da dívida, com ROIC < WACC), mas 34 delas têm DDM/FCFE/RIM > 0. Um Ke de 25% que não sobe com a alavancagem viola Modigliani-Miller, e o acionista tem responsabilidade limitada (utilities, concessões, locadoras, MGLU3, ASAI3). (ii) `other_financial` entra no lucro, mas não no FCFF (AZZA3, NATU3, EZTC3, MRVE3, PLPL3, TEND3, AURE3, ENGI11, EQTL3, VALE3, DXCO3, AXIA3, TAEE11): no caso de TEND3/PLPL3/MRVE3, juros capitalizados e custo de cessões inflam o DCF frente ao RIM/FCFE. (iii) Payout baixo: o FCFE supera o DDM em +17% na mediana, porque o caixa retido rende Kd·(1−t) < Ke. (iv) PL com ágio (HAPV3, AZZA3, ALOS3) tira o sentido do P/VP. Detalhes por empresa na tabela de divergências.
4. **Pesos recomendados.** Cada classe usa os métodos coerentes com Ke 25% (tabela abaixo): RIM nos bancos e incorporadoras, APV/DCF mais o lado do acionista em infraestrutura, EVA/APV em locação, e DCF com pares ajustados ao Ke no varejo. Múltiplos de mercado brutos (alvo, pares e histórico) ficam como referência relativa e saem do valor justo.
5. **Efeito.** O valor justo muda -29% na mediana (infraestrutura -61%, shoppings -31%, serviços -31%, bancos -22%, varejo -24%, incorporadoras -14%, locação -29%, cíclicas -16%). O upside mediano da cobertura passa de -49% para -66%, e empresas com upside > 0: 10 → 6. Quase toda a queda vem de retirar os múltiplos-alvo: o esquema "estudo sem múltiplos" já dá -67%. O ranking quase não muda (Spearman do escore multifator 0,99; do upside 0,90), porque o upside pesa só 10% do escore e a TIR de dono (30%), a qualidade e a solidez não dependem dos pesos.
6. **As 8 oportunidades.** Com as premissas de agora, o estudo recalculado mantém 8 das 8 pela regra (VTRU3, BEEF3, SEER3, MDNE3, PLPL3, TEND3, CEAB3, COGN3). Com os pesos propostos, ficam 7: VTRU3 (upside +35%), BEEF3 (upside +50%), SEER3 (upside +17%), MDNE3 (upside +6%), PLPL3 (upside +23%), TEND3 (upside +6%), COGN3 (upside -1%). Saem CEAB3 (P(MC) 32%). Nenhuma empresa nova entra. Os rankings das oportunidades mudam pouco (tabela abaixo).

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
| DCF-FCFF (estudo) | 103 | -48% | -140% / -24% | — | 5% | -77% |
| APV | 103 | -36% | -96% / -23% | +1% | 7% | -73% |
| EVA (fade ROIC) | 103 | -50% | -140% / -27% | -0% | 4% | -77% |
| DDM (estudo) | 117 | -19% | -31% / -5% | +13% | 20% | -61% |
| DDM c/ emissões e recompras | 117 | -19% | -31% / -5% | +11% | 20% | -61% |
| FCFE (DL ∝ receita) | 103 | -3% | -26% / +23% | +32% | 45% | -55% |
| RIM/Ohlson (fade ROE) | 117 | -19% | -31% / -5% | +11% | 19% | -61% |
| P/L justificado | 114 | -26% | -39% / -8% | -0% | 20% | -62% |
| P/VP justificado | 117 | -5% | -32% / +49% | +21% | 44% | -54% |
| Pares ajustados ao Ke 25% | 104 | -13% | -33% / +6% | +7% | 32% | -57% |
| Múltiplos-alvo (estudo) | 117 | +96% | +46% / +169% | +178% | 98% | -1% |
| Pares (mediana) | 106 | +82% | +26% / +234% | +152% | 85% | -3% |
| Histórico 5a (mediana) | 112 | +166% | +56% / +298% | +267% | 96% | +24% |
| SOTP (controladas c/ pesos novos) | 5 | -27% | -39% / -26% | — | 0% | -65% |

O valor justo do estudo já inclui 25% (bancos: 50%) de múltiplos-alvo; por isso os intrínsecos aparecem abaixo dele e próximos do DCF/DDM.

## Onde os métodos divergem mais (e por quê)

Dispersão = desvio-padrão do log dos valores positivos de todos os métodos. Ke implícito no P/L histórico = Ke que torna a mediana de 5 anos do P/L (LTM, Gordon com ROE e g terminais) coerente; TIR hoje = TIR de dono implícita no preço (DDM do estudo).

| # | Empresa | Classe | σ log | Máx/mín | Mercado/intrínseco | Ke impl. P/L hist. | TIR hoje | Causas principais |
|---|---|---|---|---|---|---|---|---|
| 1 | MGLU3 | Varejo e consumo | 1,77 | 148,4× | 21,71× | 6% | 7% | múltiplos de mercado 21,7× a mediana intrínseca (P/L histórico embute Ke ≈ 6%; P/L-alvo embute Ke ≈ 9% vs 25%); EV a WACC 19% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 2 | TUPY3 | Serviços, saúde, educação e tecnologia | 1,33 | 125,6× | 1,85× | 12% | 16% | APV/DCF = 13,32: dívida projetada (DL/EBITDA 2,9x → 1,4x em 2030) ≠ peso-alvo wd = 35% do WACC; valor ≤ 0 em: EVA (fade ROIC), Histórico 5a (mediana); múltiplos de mercado 1,9× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 15% vs 25%) |
| 3 | DESK3 | Serviços, saúde, educação e tecnologia | 1,32 | 74,4× | 3,65× | 8% | 10% | APV/DCF = 4,65: dívida projetada (DL/EBITDA 1,8x → 0,9x em 2030) ≠ peso-alvo wd = 40% do WACC; múltiplos de mercado 3,6× a mediana intrínseca (P/L histórico embute Ke ≈ 8% vs 25%); FCFE/DDM = 1,68: payout médio 32% retém caixa que rende Kd·(1−t) < Ke |
| 4 | PNVL3 | Serviços, saúde, educação e tecnologia | 1,24 | 124,0× | 4,16× | 9% | 13% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 46%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 20% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 4,2× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 11% vs 25%) |
| 5 | SAPR11 | Serviços, saúde, educação e tecnologia | 1,21 | 184,4× | 2,59× | 17% | 13% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 29%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 19% abaixo da dívida (ROIC 2030 10%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,6× a mediana intrínseca (P/L histórico embute Ke ≈ 17%; P/L-alvo embute Ke ≈ 15% vs 25%) |
| 6 | PRNR3 | Serviços, saúde, educação e tecnologia | 1,18 | 58,2× | 4,01× | 9% | 11% | APV/DCF = 10,45: dívida projetada (DL/EBITDA 2,4x → 1,6x em 2030) ≠ peso-alvo wd = 35% do WACC; múltiplos de mercado 4,0× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 10% vs 25%); FCFE/DDM = 1,55: payout médio 32% retém caixa que rende Kd·(1−t) < Ke |
| 7 | MOTV3 | Infraestrutura e utilities | 1,18 | 95,9× | 2,58× | — | 13% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 64%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 18% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,6× a mediana intrínseca (P/L-alvo embute Ke ≈ 13% vs 25%) |
| 8 | HAPV3 | Serviços, saúde, educação e tecnologia | 1,13 | 46,9× | 3,03× | — | 29% | múltiplos de mercado 3,0× a mediana intrínseca (P/L-alvo embute Ke ≈ 15% vs 25%); APV/DCF = 2,04: dívida projetada (DL/EBITDA 3,7x → 1,8x em 2030) ≠ peso-alvo wd = 35% do WACC; FCFE/DDM = 1,59: payout médio 22% retém caixa que rende Kd·(1−t) < Ke |
| 9 | BRAV3 | Serviços, saúde, educação e tecnologia | 1,10 | 72,2× | 3,63× | — | 11% | EV a WACC 18% abaixo da dívida (ROIC 2030 7%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 3,6× a mediana intrínseca (P/L-alvo embute Ke ≈ 23% vs 25%); FCFE/DDM = 1,94: payout médio 44% retém caixa que rende Kd·(1−t) < Ke |
| 10 | VBBR3 | Cíclicas / commodities | 1,07 | 50,8× | 1,98× | 15% | 10% | APV/DCF = 2,99: dívida projetada (DL/EBITDA 2,3x → 1,7x em 2030) ≠ peso-alvo wd = 27% do WACC; múltiplos de mercado 2,0× a mediana intrínseca (P/L histórico embute Ke ≈ 15%; P/L-alvo embute Ke ≈ 15% vs 25%) |
| 11 | CBAV3 | Serviços, saúde, educação e tecnologia | 1,07 | 13,0× | 10,26× | 9% | 6% | múltiplos de mercado 10,3× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 7% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 6%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; FCFE/DDM = 1,38: payout médio 36% retém caixa que rende Kd·(1−t) < Ke |
| 12 | CPFE3 | Serviços, saúde, educação e tecnologia | 1,07 | 72,0× | 3,00× | 14% | 11% | EV a WACC 19% abaixo da dívida (ROIC 2030 12%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 3,0× a mediana intrínseca (P/L histórico embute Ke ≈ 14%; P/L-alvo embute Ke ≈ 13% vs 25%) |
| 13 | SBSP3 | Infraestrutura e utilities | 1,04 | 34,8× | 7,27× | 10% | 8% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = -41%: capex/ΔCG) → DCF ≪ métodos de lucro; múltiplos de mercado 7,3× a mediana intrínseca (P/L histórico embute Ke ≈ 10%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 20% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 14 | CVCB3 | Serviços, saúde, educação e tecnologia | 1,04 | 11,0× | — | — | — | múltiplos de mercado 6,3× a mediana intrínseca (P/L-alvo embute Ke ≈ 13% vs 25%) |
| 15 | AURE3 | Infraestrutura e utilities | 0,98 | 13,9× | 7,15× | — | 7% | múltiplos de mercado 7,1× a mediana intrínseca; FCFE/DDM = 5,15: payout médio 25% retém caixa que rende Kd·(1−t) < Ke; EV a WACC 17% abaixo da dívida (ROIC 2030 6%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |

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
| Bancos | 14 | -22% | -32% | -49% |
| Incorporadoras | 9 | -14% | -2% | -16% |
| Infraestrutura e utilities | 10 | -61% | -75% | -90% |
| Shoppings (renda imobiliária) | 3 | -31% | -44% | -62% |
| Locação (capital intensivo) | 3 | -29% | -50% | -71% |
| Varejo e consumo | 14 | -24% | -49% | -63% |
| Serviços, saúde, educação e tecnologia | 61 | -31% | -55% | -71% |
| Cíclicas / commodities | 3 | -16% | -68% | -83% |
| Holdings (SOTP) | 5 | -27% | -52% | -65% |

### Esquemas comparados

| Esquema | Upside mediano | Upside > 0 | Spearman escore vs estudo | Spearman upside vs estudo | Oportunidades pela regra (top 8 por escore) |
|---|---|---|---|---|---|
| Estudo (recalculado agora) | -49% | 10 | 1,00 | 1,00 | BEEF3, VTRU3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3 |
| Estudo sem múltiplos-alvo (DCF/DDM renormalizados) | -67% | 7 | 0,99 | 0,94 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3 |
| **Proposto por classe** | -66% | 6 | 0,99 | 0,90 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3, COGN3 |
| Proposto sem pares ajustados (só intrínsecos) | -65% | 6 | 0,99 | 0,91 | BEEF3, VTRU3, PLPL3, MDNE3, SEER3, TEND3, COGN3 |
| Peso igual em todos os métodos (inclui mercado bruto) | -46% | 15 | 0,97 | 0,82 | BEEF3, VTRU3, PLPL3, CEAB3, MDNE3, SEER3, COGN3, TEND3 |

Top 10 do escore multifator: estudo BEEF3, VTRU3, HAPV3, PLPL3, MDNE3, CEAB3, SEER3, TEND3, COGN3, ANIM3; proposto BEEF3, VTRU3, PLPL3, HAPV3, MDNE3, SEER3, CEAB3, TEND3, ANIM3, COGN3.

Maiores mudanças no ranking por upside (posições; + = sobe): DESK3 -96, CBAV3 -88, BRAV3 +28, PETR3 +27, ASAI3 +26, GMAT3 +24, RAPT4 -24, JSLG3 +24, PETR4 +22, SUZB3 +22.

## As 8 oportunidades

| Empresa | Preço | Valor justo estudo → proposto | Upside estudo → proposto | Rank escore | Rank upside | P(MC) estudo → proposto | Regra (proposto) |
|---|---|---|---|---|---|---|---|
| VTRU3 | 11,98 | 16,69 → 16,19 | +39% → +35% | 2 → 2 | 2 → 2 | 90% → 88% | passa |
| BEEF3 | 2,87 | 5,04 → 4,31 | +76% → +50% | 1 → 1 | 1 → 1 | 75% → 71% | passa |
| SEER3 | 11,03 | 13,81 → 12,95 | +25% → +17% | 7 → 6 | 4 → 4 | 81% → 75% | passa |
| MDNE3 | 16,86 | 19,81 → 17,94 | +17% → +6% | 5 → 5 | 6 → 5 | 76% → 62% | passa |
| PLPL3 | 4,84 | 6,25 → 5,97 | +29% → +23% | 4 → 3 | 3 → 3 | 80% → 76% | passa |
| TEND3 | 21,22 | 26,34 → 22,39 | +24% → +6% | 8 → 8 | 5 → 6 | 77% → 59% | passa |
| CEAB3 | 6,87 | 6,65 → 5,56 | -3% → -19% | 6 → 7 | 14 → 12 | 47% → 32% | não passa |
| COGN3 | 1,69 | 1,89 → 1,68 | +12% → -1% | 9 → 10 | 7 → 7 | 62% → 50% | passa |

Regra do estudo (build.py): TIR de dono ≥ 20%, P(valor justo > preço) ≥ 45%, Altman fora da zona de risco e confiança diferente de baixa. A TIR, o Altman e a confiança não mudam com os pesos; a probabilidade reescala a amostra do Monte Carlo do motor pelo novo valor justo.

- **VTRU3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 17,00, APV 15,38, EVA (fade ROIC) 17,00, DDM (estudo) 12,95, DDM c/ emissões e recompras 12,95, FCFE (DL ∝ receita) 17,09, RIM/Ohlson (fade ROE) 12,95, P/L justificado 12,84, P/VP justificado 20,16, Pares ajustados ao Ke 25% 15,77, Múltiplos-alvo (estudo) 19,82, Pares (mediana) 15,61, Histórico 5a (mediana) 24,62. Divergências: FCFE/DDM = 1,32: payout médio 40% retém caixa que rende Kd·(1−t) < Ke.
- **BEEF3** (Cíclicas / commodities): DCF-FCFF (estudo) 5,60, APV 7,38, EVA (fade ROIC) 4,38, DDM (estudo) 3,22, DDM c/ emissões e recompras 2,54, FCFE (DL ∝ receita) 3,86, RIM/Ohlson (fade ROE) 2,30, P/L justificado 2,13, P/VP justificado 1,01, Múltiplos-alvo (estudo) 5,75, Histórico 5a (mediana) 6,65. Divergências: FCFF acima do lucro (FCFF/LL 2027–30 = 250%) → DCF ≫ RIM/DDM; múltiplos de mercado 1,9× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 18% vs 25%); DDM do estudo ignora a emissão de ações de R$ 930 mi projetada (dividendo cresce com o capital novo, ações fixas): com ela o DDM seria -21%; o RIM (clean surplus) já a desconta.
- **SEER3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 13,70, APV 12,13, EVA (fade ROIC) 12,71, DDM (estudo) 10,44, DDM c/ emissões e recompras 10,44, FCFE (DL ∝ receita) 14,75, RIM/Ohlson (fade ROE) 10,06, P/L justificado 9,89, P/VP justificado 7,74, Pares ajustados ao Ke 25% 12,70, Múltiplos-alvo (estudo) 17,42, Pares (mediana) 13,07, Histórico 5a (mediana) 23,14. Divergências: FCFE/DDM = 1,41: payout médio 42% retém caixa que rende Kd·(1−t) < Ke.
- **MDNE3** (Incorporadoras): DCF-FCFF (estudo) 15,59, APV 15,80, EVA (fade ROIC) 15,36, DDM (estudo) 18,65, DDM c/ emissões e recompras 18,65, FCFE (DL ∝ receita) 20,71, RIM/Ohlson (fade ROE) 18,59, P/L justificado 18,91, P/VP justificado 16,60, Pares ajustados ao Ke 25% 14,75, Múltiplos-alvo (estudo) 22,22, Pares (mediana) 25,70, Histórico 5a (mediana) 33,73.
- **PLPL3** (Incorporadoras): DCF-FCFF (estudo) 7,28, APV 7,45, EVA (fade ROIC) 6,67, DDM (estudo) 5,64, DDM c/ emissões e recompras 5,64, FCFE (DL ∝ receita) 6,56, RIM/Ohlson (fade ROE) 5,59, P/L justificado 5,53, P/VP justificado 4,70, Pares ajustados ao Ke 25% 6,33, Múltiplos-alvo (estudo) 6,25, Pares (mediana) 8,69, Histórico 5a (mediana) 11,48.
- **TEND3** (Incorporadoras): DCF-FCFF (estudo) 31,68, APV 32,06, EVA (fade ROIC) 29,20, DDM (estudo) 21,22, DDM c/ emissões e recompras 21,22, FCFE (DL ∝ receita) 24,96, RIM/Ohlson (fade ROE) 20,63, P/L justificado 22,32, P/VP justificado 12,56, Pares ajustados ao Ke 25% 24,59, Múltiplos-alvo (estudo) 31,22, Pares (mediana) 33,10, Histórico 5a (mediana) 40,80. Divergências: other_financial (R$ -227 mi/ano, -25% do LL) entra no LL (DDM/RIM/FCFE) mas não no FCFF do DCF.
- **CEAB3** (Varejo e consumo): DCF-FCFF (estudo) 3,87, APV 4,26, EVA (fade ROIC) 3,75, DDM (estudo) 5,60, DDM c/ emissões e recompras 5,60, FCFE (DL ∝ receita) 6,52, RIM/Ohlson (fade ROE) 5,60, P/L justificado 5,63, P/VP justificado 6,34, Pares ajustados ao Ke 25% 7,09, Múltiplos-alvo (estudo) 13,26, Pares (mediana) 10,13, Histórico 5a (mediana) 13,74. Divergências: múltiplos de mercado 2,4× a mediana intrínseca (P/L histórico embute Ke ≈ 14%; P/L-alvo embute Ke ≈ 15% vs 25%).
- **COGN3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 1,59, APV 1,39, EVA (fade ROIC) 1,59, DDM (estudo) 1,62, DDM c/ emissões e recompras 1,62, FCFE (DL ∝ receita) 2,27, RIM/Ohlson (fade ROE) 1,62, P/L justificado 1,36, P/VP justificado 4,46, Pares ajustados ao Ke 25% 2,52, Múltiplos-alvo (estudo) 2,76, Pares (mediana) 2,78, Histórico 5a (mediana) 5,06. Divergências: FCFE/DDM = 1,40: payout médio 50% retém caixa que rende Kd·(1−t) < Ke.

## Para os revisores (achados que afetam o estudo)

- **Múltiplos-alvo incoerentes com Ke 25%**: o P/L-alvo mediano embute Ke de ~13%. Para manter os múltiplos no blend, use os justificados (Gordon a 25%) ou os pares ajustados pela TIR implícita.
- **DCF × `other_financial`**: o FCFF exclui `other_financial`, mas o lucro (DDM/RIM/FCFE) inclui. Onde ele é material (AZZA3 -23% do LL, NATU3 -19% do LL, EZTC3 +25% do LL, MRVE3 -163% do LL, PLPL3 -19% do LL, TEND3 -25% do LL, AURE3 +122% do LL, ENGI11 +18% do LL, EQTL3 +52% do LL, VALE3 -22% do LL, DXCO3 +51% do LL, AXIA3 -71% do LL, TAEE11 +35% do LL), trate o item como ajuste debt-like ou como fluxo operacional, para não inflar (ou deprimir) o DCF.
- **DDM × emissão/recompra projetada**: o DDM do motor desconta só dividendos, com o número de ações fixo; o capital novo aumenta o lucro e o dividendo sem diluir. ORVR3: emissão R$ 1.000 mi, recompra R$ 0 mi → DDM -56% com o fluxo de capital; BEEF3: emissão R$ 930 mi, recompra R$ 0 mi → DDM -21% com o fluxo de capital. Corrija no DDM (fluxo líquido ao acionista) ou ajuste o número de ações.
- **wd do WACC × dívida projetada**: em 35 industriais o DCF dá equity ≤ 0. Com Ke fixo, o wd-alvo precisa ser coerente com a alavancagem a que 25% se refere; senão DCF e DDM medem coisas diferentes (ver APV/DCF e FCFE/DDM no JSON).
- **Série de múltiplos históricos**: . Esses meses têm erro de unidade de ações em `multiples_history` (P/L 0,01, P/VP 0,001), e as medianas de `stats` ficam inválidas.
- **Holdings**: componentes "market" fora da foto de preços (nenhum) forçam cotação ao vivo, que falha de forma intermitente e zera o componente. Aqui o cache foi semeado com o último `data/model` do motor.
- **HAPV3**: o PL de R$ 48 bi é quase todo ágio da fusão e o preço implica P/VP de 0,05×. P/VP e RIM com fade não fazem sentido ali; o fade só corrói retorno excedente.

## Tabela completa

Valores por ação/unit (R$). Rank = escore multifator do build.py recalculado; ↑ = rank por upside. Ordem: rank proposto.

| Empresa | Classe | Preço | DCF | DDM | Múlt. | RIM | EVA | APV | FCFE | P/L j | P/VP j | Pares Ke | Pares | Hist. | Justo estudo | Justo proposto | Upside estudo | Upside proposto | Rank | ↑ Rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BEEF3 | Cíclicas / commodities | 2,87 | 5,60 | 3,22 | 5,75 | 2,30 | 4,38 | 7,38 | 3,86 | 2,13 | 1,01 | — | — | 6,65 | 5,04 | 4,31 | +76% | +50% | 1 → 1 | 1 → 1 |
| VTRU3 | Serviços, saúde, educação e tecnologia | 11,98 | 17,00 | 12,95 | 19,82 | 12,95 | 17,00 | 15,38 | 17,09 | 12,84 | 20,16 | 15,77 | 15,61 | 24,62 | 16,69 | 16,19 | +39% | +35% | 2 → 2 | 2 → 2 |
| PLPL3 | Incorporadoras | 4,84 | 7,28 | 5,64 | 6,25 | 5,59 | 6,67 | 7,45 | 6,56 | 5,53 | 4,70 | 6,33 | 8,69 | 11,48 | 6,25 | 5,97 | +29% | +23% | 4 → 3 | 3 → 3 |
| HAPV3 | Serviços, saúde, educação e tecnologia | 4,21 | 1,73 | 5,58 | 8,67 | 5,58 | 1,73 | 3,52 | 8,86 | 2,78 | 50,58 | 4,07 | 16,91 | 80,90 | 4,42 | 3,37 | +5% | -20% | 3 → 4 | 9 → 13 |
| MDNE3 | Incorporadoras | 16,86 | 15,59 | 18,65 | 22,22 | 18,59 | 15,36 | 15,80 | 20,71 | 18,91 | 16,60 | 14,75 | 25,70 | 33,73 | 19,81 | 17,94 | +17% | +6% | 5 → 5 | 6 → 5 |
| SEER3 | Serviços, saúde, educação e tecnologia | 11,03 | 13,70 | 10,44 | 17,42 | 10,06 | 12,71 | 12,13 | 14,75 | 9,89 | 7,74 | 12,70 | 13,07 | 23,14 | 13,81 | 12,95 | +25% | +17% | 7 → 6 | 4 → 4 |
| CEAB3 | Varejo e consumo | 6,87 | 3,87 | 5,60 | 13,26 | 5,60 | 3,75 | 4,26 | 6,52 | 5,63 | 6,34 | 7,09 | 10,13 | 13,74 | 6,65 | 5,56 | -3% | -19% | 6 → 7 | 14 → 12 |
| TEND3 | Incorporadoras | 21,22 | 31,68 | 21,22 | 31,22 | 20,63 | 29,20 | 32,06 | 24,96 | 22,32 | 12,56 | 24,59 | 33,10 | 40,80 | 26,34 | 22,39 | +24% | +6% | 8 → 8 | 5 → 6 |
| ANIM3 | Serviços, saúde, educação e tecnologia | 2,43 | 1,74 | 2,07 | 3,21 | 2,07 | 1,54 | 0,70 | 3,57 | 1,61 | 4,16 | 2,84 | 1,82 | 10,16 | 2,19 | 2,04 | -10% | -16% | 10 → 9 | 18 → 11 |
| COGN3 | Serviços, saúde, educação e tecnologia | 1,69 | 1,59 | 1,62 | 2,76 | 1,62 | 1,59 | 1,39 | 2,27 | 1,36 | 4,46 | 2,52 | 2,78 | 5,06 | 1,89 | 1,68 | +12% | -1% | 9 → 10 | 7 → 7 |
| SBFG3 | Varejo e consumo | 5,08 | -1,01 | 4,40 | 9,51 | 4,40 | -1,07 | -0,52 | 5,92 | 4,47 | 5,56 | 5,77 | 6,77 | 15,75 | 3,48 | 3,52 | -32% | -31% | 17 → 11 | 38 → 20 |
| POMO4 | Serviços, saúde, educação e tecnologia | 3,89 | 3,49 | 3,09 | 5,34 | 3,09 | 3,46 | 3,47 | 3,45 | 3,15 | 2,90 | 3,53 | 5,37 | 8,06 | 3,85 | 3,41 | -1% | -12% | 12 → 12 | 11 → 8 |
| SAUD3 | Bancos | 14,64 | — | 6,45 | 13,35 | 6,44 | — | — | — | 6,26 | 5,66 | — | — | — | 9,90 | 6,25 | -32% | -57% | 15 → 13 | 40 → 49 |
| MOVI3 | Locação (capital intensivo) | 6,62 | -2,50 | 5,70 | 10,98 | 5,51 | -3,75 | 5,09 | 8,41 | 5,42 | 5,26 | 6,19 | 16,22 | 16,05 | 4,17 | 2,96 | -37% | -55% | 14 → 14 | 45 → 46 |
| LEVE3 | Serviços, saúde, educação e tecnologia | 31,17 | 17,99 | 19,89 | 30,92 | 19,89 | 17,95 | 17,86 | 23,02 | 20,65 | 13,89 | — | — | 33,66 | 21,70 | 19,52 | -30% | -37% | 20 → 15 | 34 → 26 |
| BRAP4 | Holdings (SOTP) | 18,02 | — | — | — | — | — | — | — | — | — | — | — | 14,36 | 3,80 | 2,07 | -79% | -89% | 21 → 16 | 112 → 105 |
| CYRE3 | Incorporadoras | 17,74 | 14,45 | 15,42 | 21,92 | 15,42 | 14,35 | 14,88 | 16,67 | 15,06 | 14,76 | 12,76 | 23,05 | 27,18 | 17,36 | 15,11 | -2% | -15% | 13 → 17 | 12 → 9 |
| PGMN3 | Varejo e consumo | 2,63 | 0,98 | 1,97 | 4,58 | 1,97 | 0,92 | 1,16 | 2,76 | 1,82 | 2,61 | 2,34 | 8,37 | 6,29 | 2,13 | 1,85 | -19% | -30% | 22 → 18 | 26 → 18 |
| PINE4 | Bancos | 10,66 | — | 9,15 | 11,49 | 9,13 | — | — | — | 11,29 | 6,02 | 7,43 | 12,82 | 10,56 | 9,34 | 8,36 | -12% | -22% | 19 → 19 | 20 → 14 |
| LREN3 | Varejo e consumo | 9,31 | 5,75 | 6,99 | 15,39 | 6,93 | 5,71 | 6,02 | 7,08 | 5,76 | 6,47 | 5,76 | 9,00 | 23,05 | 8,47 | 6,02 | -9% | -35% | 11 → 20 | 17 → 25 |
| CURY3 | Incorporadoras | 26,37 | 20,31 | 19,01 | 28,42 | 18,39 | 19,03 | 20,31 | 19,28 | 17,99 | 10,75 | 16,05 | 16,90 | 41,98 | 22,20 | 17,65 | -16% | -33% | 18 → 21 | 21 → 22 |
| BBSE3 | Bancos | 41,40 | — | 22,46 | 32,67 | 22,38 | — | — | — | 21,53 | 17,92 | 13,24 | 33,10 | 38,62 | 27,57 | 21,29 | -33% | -49% | 25 → 22 | 42 → 34 |
| DIRR3 | Incorporadoras | 8,60 | 8,31 | 7,12 | 10,68 | 7,12 | 7,76 | 8,40 | 7,57 | 7,28 | 5,59 | 7,40 | 8,14 | 18,55 | 8,41 | 7,22 | -2% | -16% | 24 → 23 | 13 → 10 |
| BBAS3 | Bancos | 16,84 | — | 12,33 | 19,41 | 12,21 | — | — | — | 11,51 | 14,67 | 16,09 | 23,97 | 18,50 | 15,50 | 12,85 | -8% | -24% | 23 → 24 | 15 → 15 |
| PETR4 | Serviços, saúde, educação e tecnologia | 52,73 | 19,07 | 26,77 | 47,25 | 26,77 | 18,79 | 19,86 | 30,02 | 47,24 | 21,32 | 27,28 | 58,73 | 43,40 | 28,04 | 26,84 | -47% | -49% | 29 → 25 | 58 → 36 |
| TFCO4 | Serviços, saúde, educação e tecnologia | 10,08 | 4,59 | 4,07 | 13,24 | 4,07 | 4,59 | 4,55 | 4,40 | 4,45 | 3,63 | 4,61 | 9,49 | — | 6,62 | 4,52 | -34% | -55% | 28 → 26 | 43 → 45 |
| YDUQ3 | Serviços, saúde, educação e tecnologia | 8,76 | 5,26 | 6,06 | 9,69 | 6,06 | 5,26 | 5,02 | 8,52 | 2,68 | 8,60 | 3,43 | 6,46 | 12,16 | 6,57 | 5,40 | -25% | -38% | 27 → 27 | 28 → 28 |
| PETR3 | Serviços, saúde, educação e tecnologia | 59,12 | 19,07 | 26,77 | 47,25 | 26,77 | 18,79 | 19,86 | 30,02 | 47,24 | 21,32 | 27,24 | 57,13 | 47,30 | 28,04 | 26,84 | -53% | -55% | 33 → 28 | 69 → 42 |
| RIAA3 | Serviços, saúde, educação e tecnologia | 6,33 | 2,35 | 3,75 | 9,63 | 3,75 | 2,35 | 2,84 | 4,29 | 3,76 | 4,84 | 4,70 | 6,66 | — | 4,52 | 3,02 | -29% | -52% | 26 → 29 | 33 → 39 |
| VIVA3 | Varejo e consumo | 17,63 | 9,36 | 9,33 | 24,07 | 9,33 | 9,20 | 9,18 | 10,74 | 9,26 | 10,16 | 9,95 | 20,25 | 36,16 | 13,03 | 9,77 | -26% | -45% | 31 → 30 | 31 → 32 |
| SUZB3 | Serviços, saúde, educação e tecnologia | 48,19 | 4,97 | 17,84 | 27,69 | 17,84 | 4,97 | 7,40 | 31,75 | 17,10 | 20,64 | 33,71 | 78,02 | 44,62 | 13,87 | 12,75 | -71% | -74% | 34 → 31 | 97 → 75 |
| BBDC3 | Bancos | 13,40 | — | 9,84 | 16,68 | 9,72 | — | — | — | 9,08 | 9,60 | 10,86 | 19,33 | 17,29 | 12,31 | 9,72 | -8% | -27% | 30 → 32 | 16 → 16 |
| VULC3 | Varejo e consumo | 11,77 | 7,55 | 7,71 | 15,41 | 7,71 | 7,55 | 7,52 | 7,80 | 7,16 | 7,18 | 6,90 | 18,24 | 20,68 | 9,55 | 7,36 | -19% | -37% | 32 → 33 | 25 → 27 |
| ECOR3 | Infraestrutura e utilities | 5,27 | -22,42 | 2,96 | 5,59 | 2,96 | -22,42 | -13,69 | 3,09 | 2,42 | 3,99 | 3,14 | 12,45 | 7,70 | 2,14 | 1,21 | -59% | -77% | 35 → 34 | 78 → 85 |
| BBDC4 | Bancos | 14,71 | — | 9,84 | 16,68 | 9,72 | — | — | — | 9,08 | 9,60 | 8,12 | 10,56 | 19,80 | 12,31 | 9,72 | -16% | -34% | 37 → 35 | 22 → 23 |
| ASAI3 | Varejo e consumo | 7,81 | -2,56 | 2,95 | 5,94 | 2,92 | -2,56 | -0,22 | 5,08 | 2,68 | 3,08 | 2,14 | 7,56 | 14,80 | 2,22 | 2,09 | -72% | -73% | 42 → 36 | 100 → 74 |
| RENT3 | Locação (capital intensivo) | 29,74 | 5,23 | 14,58 | 34,26 | 14,44 | 5,23 | 10,12 | 15,93 | 13,67 | 13,49 | 14,75 | 21,67 | 81,33 | 14,82 | 8,59 | -50% | -71% | 36 → 37 | 64 → 72 |
| VAMO3 | Locação (capital intensivo) | 2,57 | -0,78 | 1,24 | 2,55 | 1,20 | -1,09 | 1,14 | 1,92 | 1,21 | 1,21 | 1,41 | 1,82 | 9,76 | 0,95 | 0,67 | -63% | -74% | 39 → 38 | 85 → 79 |
| EZTC3 | Incorporadoras | 9,59 | 10,13 | 6,06 | 14,97 | 6,06 | 10,13 | 10,13 | 6,81 | 5,54 | 5,66 | 7,45 | 7,87 | 15,14 | 10,69 | 6,78 | +11% | -29% | 16 → 39 | 8 → 17 |
| SIMH3 | Holdings (SOTP) | 5,24 | — | — | — | — | — | — | — | — | — | — | — | 17,35 | 2,24 | 1,36 | -57% | -74% | 38 → 40 | 74 → 80 |
| ALOS3 | Shoppings (renda imobiliária) | 24,44 | 7,98 | 10,18 | 24,16 | 10,18 | 7,98 | 8,34 | 10,47 | 8,26 | 25,70 | 9,33 | 22,10 | 27,65 | 12,58 | 8,81 | -49% | -64% | 45 → 41 | 61 → 58 |
| GMAT3 | Varejo e consumo | 3,54 | -0,49 | 1,26 | 3,62 | 1,26 | -0,49 | -0,47 | 1,37 | 1,46 | 2,19 | 2,45 | 4,21 | 8,23 | 1,22 | 1,18 | -66% | -67% | 49 → 42 | 87 → 63 |
| BRSR6 | Bancos | 12,94 | — | 8,89 | 13,71 | 8,94 | — | — | — | 8,68 | 9,41 | 13,96 | 20,80 | 17,49 | 10,68 | 9,05 | -17% | -30% | 41 → 43 | 24 → 19 |
| INTB3 | Serviços, saúde, educação e tecnologia | 14,36 | 5,70 | 5,65 | 14,98 | 5,65 | 5,70 | 5,70 | 6,20 | 6,06 | 6,06 | — | — | 23,45 | 8,01 | 5,87 | -44% | -59% | 46 → 44 | 55 → 52 |
| HYPE3 | Varejo e consumo | 21,60 | 6,35 | 8,71 | 19,79 | 8,71 | 6,35 | 5,68 | 11,86 | 8,21 | 10,25 | 10,61 | 17,45 | 37,06 | 10,30 | 8,89 | -52% | -59% | 48 → 45 | 68 → 51 |
| GGPS3 | Serviços, saúde, educação e tecnologia | 10,89 | 4,91 | 5,03 | 14,33 | 5,01 | 4,71 | 4,82 | 6,31 | 4,21 | 5,06 | 5,02 | 12,23 | 24,05 | 7,29 | 5,01 | -33% | -54% | 43 → 46 | 41 → 40 |
| AUAU3 | Serviços, saúde, educação e tecnologia | 3,86 | 1,30 | 1,82 | 5,21 | 1,82 | 1,30 | 1,40 | 2,44 | 1,36 | 2,04 | 1,43 | 2,71 | — | 2,41 | 1,54 | -38% | -60% | 44 → 47 | 46 → 56 |
| AZZA3 | Varejo e consumo | 15,07 | 4,45 | 5,12 | 12,12 | 5,12 | 4,45 | 3,78 | 7,02 | 1,84 | 19,88 | 2,56 | 3,86 | 25,46 | 6,53 | 3,97 | -57% | -74% | 40 → 48 | 72 → 76 |
| MDIA3 | Serviços, saúde, educação e tecnologia | 15,73 | 8,32 | 6,77 | 20,17 | 6,77 | 8,32 | 8,32 | 7,78 | 6,63 | 9,25 | — | — | 28,77 | 10,90 | 7,87 | -31% | -50% | 47 → 49 | 35 → 37 |
| ABEV3 | Serviços, saúde, educação e tecnologia | 15,18 | 6,72 | 5,72 | 14,64 | 5,72 | 6,55 | 6,72 | 5,93 | 4,71 | 5,73 | — | — | 15,99 | 8,45 | 6,13 | -44% | -60% | 51 → 50 | 56 → 55 |
| PSSA3 | Bancos | 46,89 | — | 21,97 | 47,88 | 21,12 | — | — | — | 22,92 | 18,87 | 48,68 | 108,32 | 47,21 | 34,93 | 20,77 | -26% | -56% | 50 → 51 | 29 → 47 |
| PRIO3 | Serviços, saúde, educação e tecnologia | 72,29 | 45,26 | 42,50 | 65,12 | 41,72 | 42,96 | 44,42 | 51,09 | 50,86 | 23,84 | 28,60 | 63,09 | 55,64 | 49,53 | 47,08 | -31% | -35% | 56 → 52 | 37 → 24 |
| JSLG3 | Serviços, saúde, educação e tecnologia | 5,62 | -1,60 | 2,20 | 3,94 | 2,06 | -2,38 | 1,48 | 6,62 | 0,76 | 2,07 | 1,28 | 10,10 | 8,39 | 1,54 | 1,48 | -73% | -74% | 60 → 53 | 101 → 77 |
| ITSA4 | Holdings (SOTP) | 12,91 | — | — | — | — | — | — | — | — | — | — | — | 11,60 | 9,54 | 7,08 | -26% | -45% | 52 → 54 | 32 → 33 |
| ABCB4 | Bancos | 23,05 | — | 13,22 | 20,45 | 13,79 | — | — | — | 13,70 | 13,93 | 17,97 | 30,06 | 22,87 | 15,94 | 13,68 | -31% | -41% | 59 → 55 | 36 → 31 |
| MOTV3 | Infraestrutura e utilities | 14,61 | -2,14 | 5,40 | 15,94 | 5,40 | -2,14 | 0,17 | 5,85 | 4,89 | 6,93 | 6,61 | 11,89 | — | 5,34 | 2,32 | -63% | -84% | 55 → 56 | 86 → 95 |
| MULT3 | Shoppings (renda imobiliária) | 25,84 | 9,04 | 11,25 | 28,84 | 11,25 | 9,04 | 8,73 | 13,26 | 10,57 | 13,76 | 12,35 | 27,21 | 39,93 | 14,54 | 9,90 | -44% | -62% | 57 → 57 | 53 → 57 |
| B3SA3 | Serviços, saúde, educação e tecnologia | 14,66 | 5,56 | 5,21 | 13,23 | 5,12 | 5,31 | 5,60 | 5,26 | 4,53 | 4,68 | — | — | 16,26 | 7,39 | 5,25 | -50% | -64% | 61 → 58 | 63 → 60 |
| OPCT3 | Serviços, saúde, educação e tecnologia | 8,92 | 0,91 | 3,22 | 8,67 | 3,13 | 0,52 | 1,89 | 5,70 | 2,96 | 2,97 | 1,96 | 3,63 | 4,81 | 3,43 | 2,20 | -62% | -75% | 62 → 59 | 82 → 81 |
| USIM5 | Serviços, saúde, educação e tecnologia | 5,68 | 2,49 | 1,95 | 6,58 | 1,95 | 2,49 | 2,46 | 2,45 | 2,02 | 3,21 | 2,25 | 8,81 | -1,27 | 3,38 | 2,39 | -41% | -58% | 54 → 60 | 49 → 50 |
| RECV3 | Serviços, saúde, educação e tecnologia | 11,14 | 1,17 | 5,37 | 11,22 | 5,37 | 1,17 | 1,08 | 6,80 | 7,69 | 6,47 | 4,83 | 10,50 | 13,11 | 4,73 | 3,60 | -58% | -68% | 65 → 61 | 75 → 66 |
| LWSA3 | Serviços, saúde, educação e tecnologia | 3,41 | 2,41 | 1,69 | 4,77 | 1,69 | 2,41 | 2,41 | 1,69 | 1,28 | 4,34 | 1,81 | 5,67 | — | 2,82 | 2,04 | -17% | -40% | 58 → 62 | 23 → 30 |
| SAPR11 | Serviços, saúde, educação e tecnologia | 32,42 | -3,54 | 11,34 | 29,42 | 11,34 | -3,54 | 0,42 | 10,40 | 14,53 | 16,02 | 18,42 | 78,11 | 19,74 | 10,19 | 4,99 | -69% | -85% | 66 → 63 | 94 → 96 |
| BMOB3 | Serviços, saúde, educação e tecnologia | 24,42 | 11,63 | 10,55 | 24,05 | 10,55 | 11,63 | 11,63 | 10,06 | 8,23 | 11,30 | 11,58 | 31,15 | 23,68 | 14,47 | 10,64 | -41% | -56% | 68 → 64 | 50 → 48 |
| TOTS3 | Serviços, saúde, educação e tecnologia | 34,09 | 10,47 | 9,90 | 34,23 | 9,82 | 10,03 | 10,66 | 12,93 | 6,77 | 10,01 | 8,36 | 15,94 | 62,91 | 16,27 | 10,13 | -52% | -70% | 67 → 65 | 67 → 70 |
| CPFE3 | Serviços, saúde, educação e tecnologia | 42,97 | -5,12 | 14,36 | 34,90 | 14,06 | -5,48 | 0,77 | 13,57 | 14,05 | 11,06 | 10,34 | 55,25 | 42,08 | 12,31 | 5,52 | -71% | -87% | 69 → 66 | 99 → 101 |
| KLBN11 | Serviços, saúde, educação e tecnologia | 17,63 | -0,36 | 6,14 | 6,62 | 5,84 | -0,36 | -0,13 | 8,63 | 3,09 | 4,04 | 5,21 | 11,61 | 9,92 | 3,19 | 2,34 | -82% | -87% | 74 → 67 | 116 → 98 |
| RAPT4 | Serviços, saúde, educação e tecnologia | 3,67 | -3,66 | 1,72 | 5,97 | 1,72 | -3,70 | -1,93 | 2,97 | 1,37 | 3,90 | 1,78 | 2,44 | 1,87 | 1,92 | 0,87 | -48% | -76% | 53 → 68 | 59 → 83 |
| GRND3 | Serviços, saúde, educação e tecnologia | 3,65 | 2,59 | 1,82 | 3,85 | 1,82 | 2,59 | 2,59 | 1,71 | 1,51 | 1,65 | 1,85 | 4,14 | 5,42 | 2,72 | 2,20 | -26% | -40% | 71 → 69 | 30 → 29 |
| PNVL3 | Serviços, saúde, educação e tecnologia | 10,56 | -1,51 | 3,38 | 14,06 | 3,38 | -1,51 | 0,13 | 3,74 | 3,37 | 4,30 | 4,02 | 13,72 | 16,52 | 4,36 | 1,42 | -59% | -87% | 64 → 70 | 76 → 97 |
| BRAV3 | Serviços, saúde, educação e tecnologia | 18,45 | -0,27 | 6,52 | 17,65 | 6,52 | -0,27 | 0,42 | 12,66 | 18,26 | 14,14 | 10,37 | 23,66 | 30,39 | 6,04 | 6,18 | -67% | -66% | 81 → 71 | 90 → 62 |
| UNIP6 | Serviços, saúde, educação e tecnologia | 50,61 | 7,90 | 15,72 | 27,47 | 15,24 | 6,77 | 11,52 | 17,47 | 11,99 | 12,32 | — | — | 28,13 | 14,75 | 10,41 | -71% | -79% | 73 → 72 | 96 → 89 |
| RDOR3 | Serviços, saúde, educação e tecnologia | 33,80 | 7,38 | 10,33 | 27,06 | 10,08 | 6,94 | 9,52 | 12,85 | 9,49 | 8,05 | 12,45 | 21,13 | 53,01 | 13,03 | 8,81 | -61% | -74% | 72 → 73 | 81 → 78 |
| JHSF3 | Incorporadoras | 9,50 | -1,05 | 2,08 | 4,66 | 2,08 | -1,05 | -0,83 | 1,94 | 2,12 | 4,53 | 2,66 | 2,37 | 15,29 | 2,59 | 2,18 | -73% | -77% | 77 → 74 | 102 → 86 |
| SMFT3 | Serviços, saúde, educação e tecnologia | 15,99 | -4,04 | 5,60 | 21,80 | 5,60 | -4,04 | -0,63 | 8,57 | 5,02 | 7,36 | — | — | 29,08 | 6,85 | 2,72 | -57% | -83% | 70 → 75 | 73 → 94 |
| ALUP11 | Infraestrutura e utilities | 31,94 | -4,64 | 9,14 | 27,47 | 9,14 | -4,64 | -6,61 | 11,47 | 8,93 | 14,28 | 9,73 | 51,42 | 39,62 | 9,15 | 4,12 | -71% | -87% | 75 → 76 | 98 → 100 |
| ALPA4 | Varejo e consumo | 13,35 | 4,86 | 3,71 | 12,18 | 3,71 | 4,86 | 4,81 | 4,44 | 3,75 | 3,73 | 3,84 | 7,72 | 22,22 | 6,40 | 4,30 | -52% | -68% | 76 → 77 | 66 → 67 |
| VIVT3 | Serviços, saúde, educação e tecnologia | 30,85 | 8,87 | 12,19 | 26,30 | 12,19 | 8,87 | 9,90 | 12,73 | 9,56 | 20,54 | 12,27 | 33,72 | 33,51 | 14,05 | 9,78 | -54% | -68% | 79 → 78 | 70 → 68 |
| RADL3 | Varejo e consumo | 15,67 | 1,79 | 4,40 | 16,96 | 4,37 | 1,69 | 2,60 | 5,13 | 3,96 | 3,96 | 3,82 | 10,06 | 33,22 | 6,23 | 3,40 | -60% | -78% | 78 → 79 | 80 → 87 |
| IGTI11 | Shoppings (renda imobiliária) | 22,70 | 9,11 | 9,03 | 26,51 | 9,03 | 9,11 | 8,96 | 10,63 | 8,57 | 16,66 | 9,91 | 24,04 | 38,13 | 13,44 | 9,27 | -41% | -59% | 80 → 80 | 51 → 53 |
| ITUB4 | Bancos | 39,90 | — | 18,57 | 34,25 | 19,03 | — | — | — | 17,71 | 15,81 | 13,56 | 21,01 | 37,44 | 24,45 | 18,11 | -39% | -55% | 84 → 81 | 47 → 43 |
| SLCE3 | Serviços, saúde, educação e tecnologia | 16,88 | 8,93 | 3,66 | 17,45 | 3,66 | 8,93 | 12,90 | 3,96 | 3,50 | 5,46 | 3,35 | 11,23 | 11,31 | 10,96 | 6,85 | -35% | -59% | 63 → 82 | 44 → 54 |
| WEGE3 | Serviços, saúde, educação e tecnologia | 47,38 | 5,55 | 5,68 | 27,79 | 5,68 | 5,55 | 5,53 | 6,04 | 6,24 | 5,00 | — | — | 50,07 | 11,14 | 5,79 | -76% | -88% | 85 → 83 | 109 → 103 |
| BPAC11 | Bancos | 56,38 | — | 18,44 | 47,97 | 19,06 | — | — | — | 21,06 | 17,22 | 14,02 | 18,23 | 58,91 | 29,32 | 18,44 | -48% | -67% | 82 → 84 | 60 → 65 |
| FLRY3 | Serviços, saúde, educação e tecnologia | 21,67 | 4,28 | 7,12 | 19,85 | 6,96 | 4,08 | 5,54 | 8,56 | 5,39 | 5,98 | 7,96 | 16,47 | 20,10 | 8,88 | 5,32 | -59% | -75% | 86 → 85 | 77 → 82 |
| MILS3 | Serviços, saúde, educação e tecnologia | 15,56 | 4,10 | 5,27 | 14,47 | 5,27 | 4,10 | 4,81 | 6,16 | 5,47 | 5,38 | 7,91 | 18,29 | 19,25 | 6,98 | 4,78 | -55% | -69% | 87 → 86 | 71 → 69 |
| DXCO3 | Serviços, saúde, educação e tecnologia | 4,61 | -0,85 | 1,09 | 3,56 | 1,09 | -0,85 | 0,32 | 1,83 | 0,51 | 2,18 | 0,97 | 5,36 | 4,79 | 1,16 | 0,47 | -75% | -90% | 88 → 87 | 106 → 109 |
| MRVE3 | Incorporadoras | 4,27 | 4,08 | 1,36 | 4,63 | 1,36 | 3,57 | 6,04 | 1,94 | 1,00 | 3,10 | 1,46 | 1,03 | 25,54 | 2,17 | 1,94 | -49% | -55% | 91 → 88 | 62 → 44 |
| GOAU4 | Holdings (SOTP) | 10,62 | — | — | — | — | — | — | — | — | — | — | — | 6,43 | 5,10 | 3,73 | -52% | -65% | 90 → 89 | 65 → 61 |
| EGIE3 | Serviços, saúde, educação e tecnologia | 27,30 | -0,67 | 7,17 | 20,54 | 7,17 | -0,75 | 1,03 | 9,17 | 7,50 | 8,34 | 5,52 | 26,85 | 27,37 | 6,93 | 3,33 | -75% | -88% | 93 → 90 | 105 → 104 |
| CXSE3 | Bancos | 21,16 | — | 8,00 | 15,99 | 7,89 | — | — | — | 7,08 | 6,72 | 9,00 | 17,45 | 16,39 | 12,00 | 7,62 | -43% | -64% | 92 → 91 | 52 → 59 |
| GGBR4 | Serviços, saúde, educação e tecnologia | 23,99 | 6,33 | 7,07 | 18,80 | 7,07 | 6,33 | 6,52 | 8,98 | 7,31 | 7,98 | 6,11 | 13,85 | 9,68 | 9,63 | 7,05 | -60% | -71% | 94 → 92 | 79 → 71 |
| SANB11 | Bancos | 24,33 | — | 12,24 | 22,67 | 12,08 | — | — | — | 10,76 | 13,22 | 15,31 | 23,87 | 29,90 | 16,50 | 12,40 | -32% | -49% | 95 → 93 | 39 → 35 |
| IRBR3 | Bancos | 56,58 | — | 28,19 | 47,39 | 27,97 | — | — | — | 23,45 | 26,26 | 70,70 | 185,18 | 39,17 | 34,55 | 27,60 | -39% | -51% | 96 → 94 | 48 → 38 |
| EMBJ3 | Serviços, saúde, educação e tecnologia | 96,75 | 22,07 | 14,73 | 62,79 | 14,73 | 21,82 | 21,82 | 18,73 | 16,84 | 16,13 | 19,99 | 34,74 | — | 30,42 | 20,31 | -69% | -79% | 97 → 95 | 93 → 88 |
| VBBR3 | Cíclicas / commodities | 30,76 | 0,80 | 7,76 | 15,40 | 7,76 | 0,80 | 2,39 | 9,77 | 7,17 | 14,87 | 3,96 | 5,94 | 40,56 | 6,19 | 5,23 | -80% | -83% | 100 → 96 | 113 → 93 |
| CMIG4 | Serviços, saúde, educação e tecnologia | 10,15 | -3,75 | 3,20 | 6,88 | 3,20 | -3,75 | -2,25 | 1,16 | 4,37 | 5,22 | 4,30 | 17,27 | 7,94 | 2,52 | 1,11 | -75% | -89% | 99 → 97 | 107 → 107 |
| VALE3 | Serviços, saúde, educação e tecnologia | 61,08 | -23,80 | 9,72 | 18,98 | 9,72 | -23,80 | -20,15 | 4,72 | 10,29 | 13,20 | 6,65 | 62,34 | 24,78 | 7,18 | 3,00 | -88% | -95% | 102 → 98 | 121 → 116 |
| EQTL3 | Infraestrutura e utilities | 34,07 | -16,96 | 3,08 | 17,46 | 3,08 | -16,96 | -7,32 | 3,34 | 2,48 | 10,41 | 2,87 | 24,73 | 17,27 | 5,14 | 1,28 | -85% | -96% | 101 → 99 | 118 → 119 |
| UGPA3 | Serviços, saúde, educação e tecnologia | 32,70 | 8,00 | 9,31 | 23,20 | 9,31 | 8,00 | 8,29 | 10,60 | 10,71 | 10,84 | 5,59 | 12,62 | 39,28 | 12,12 | 9,06 | -63% | -72% | 103 → 100 | 84 → 73 |
| TAEE11 | Serviços, saúde, educação e tecnologia | 40,04 | 5,46 | 10,71 | 20,36 | 10,09 | 3,41 | 4,13 | 18,02 | 5,41 | 3,19 | 6,01 | 22,99 | 37,34 | 10,50 | 7,55 | -74% | -81% | 106 → 101 | 103 → 90 |
| ENGI11 | Infraestrutura e utilities | 45,24 | -36,65 | 6,53 | 32,65 | 6,53 | -36,65 | -18,29 | 3,22 | 6,33 | 19,38 | 7,79 | 58,45 | 33,24 | 9,80 | 1,95 | -78% | -96% | 104 → 102 | 110 → 117 |
| CSMG3 | Serviços, saúde, educação e tecnologia | 49,96 | -13,51 | 10,14 | 37,17 | 10,14 | -13,51 | -6,47 | 5,61 | 10,08 | 14,01 | 8,76 | 53,82 | 21,17 | 11,83 | 3,14 | -76% | -94% | 105 → 103 | 108 → 114 |
| CPLE3 | Infraestrutura e utilities | 14,67 | -2,32 | 3,01 | 7,97 | 3,01 | -2,32 | -1,00 | 2,77 | 2,73 | 4,16 | 3,24 | 15,39 | 11,76 | 2,75 | 1,16 | -81% | -92% | 107 → 104 | 115 → 111 |
| NATU3 | Varejo e consumo | 5,02 | 1,80 | 1,72 | 5,54 | 1,72 | 1,80 | 2,00 | 2,65 | 0,91 | 4,58 | 1,22 | 4,69 | — | 2,72 | 1,65 | -46% | -67% | 98 → 105 | 57 → 64 |
| LOGG3 | Serviços, saúde, educação e tecnologia | 21,52 | 2,73 | 5,61 | 14,03 | 5,61 | 2,73 | 3,24 | 9,05 | 2,56 | 26,16 | 3,13 | 6,98 | 30,17 | 6,28 | 3,96 | -71% | -82% | 108 → 106 | 95 → 91 |
| TTEN3 | Cíclicas / commodities | 10,63 | -0,35 | 3,29 | 10,50 | 3,29 | -0,35 | 0,72 | 3,43 | 4,14 | 5,00 | 4,43 | 16,24 | 7,40 | 3,45 | 1,85 | -68% | -83% | 109 → 107 | 92 → 92 |
| PRNR3 | Serviços, saúde, educação e tecnologia | 12,96 | 0,30 | 3,24 | 12,99 | 3,24 | 0,30 | 3,12 | 5,03 | 2,63 | 5,45 | 3,32 | 11,62 | 17,39 | 4,21 | 1,71 | -68% | -87% | 110 → 108 | 91 → 99 |
| ENEV3 | Serviços, saúde, educação e tecnologia | 26,49 | -3,19 | 2,40 | 8,75 | 2,40 | -3,19 | -1,41 | 3,92 | 1,45 | 5,95 | 1,47 | 8,76 | 18,80 | 2,79 | 1,07 | -89% | -96% | 115 → 109 | 122 → 118 |
| CBAV3 | Serviços, saúde, educação e tecnologia | 11,30 | -4,58 | 0,92 | 10,92 | 0,92 | -4,58 | -4,13 | 1,28 | 1,78 | 2,59 | 0,94 | 11,27 | 11,97 | 8,92 | 0,61 | -21% | -95% | 89 → 110 | 27 → 115 |
| ORVR3 | Infraestrutura e utilities | 15,73 | 1,78 | 2,46 | 15,46 | 1,09 | 1,78 | 1,87 | 3,21 | 2,18 | 3,78 | 2,08 | 12,30 | 8,87 | 5,37 | 1,96 | -66% | -88% | 114 → 111 | 88 → 102 |
| RAIL3 | Infraestrutura e utilities | 14,40 | -2,74 | 3,36 | 16,09 | 3,36 | -2,74 | -0,10 | 3,17 | 4,42 | 5,13 | 6,10 | 10,42 | 26,50 | 4,86 | 1,31 | -66% | -91% | 113 → 112 | 89 → 110 |
| CSAN3 | Holdings (SOTP) | 2,37 | — | — | — | — | — | — | — | — | — | — | — | 2,39 | 2,10 | 1,59 | -12% | -33% | 112 → 113 | 19 → 21 |
| TUPY3 | Serviços, saúde, educação e tecnologia | 15,41 | 0,12 | 7,85 | 15,12 | 7,85 | -0,18 | 1,60 | 11,12 | 6,64 | 9,33 | 8,74 | 14,01 | -15,74 | 5,80 | 3,60 | -62% | -77% | 111 → 114 | 83 → 84 |
| TIMS3 | Serviços, saúde, educação e tecnologia | 19,00 | 8,53 | 9,71 | 15,94 | 9,71 | 8,53 | 8,24 | 10,53 | 7,35 | 10,52 | 9,18 | 25,55 | -2,07 | 10,68 | 8,69 | -44% | -54% | 116 → 115 | 54 → 41 |
| SBSP3 | Infraestrutura e utilities | 24,90 | -9,41 | 3,18 | 18,15 | 3,18 | -9,41 | -5,94 | 0,77 | 4,54 | 6,42 | 5,29 | 23,09 | 26,73 | 5,33 | 0,79 | -79% | -97% | 117 → 116 | 111 → 120 |
| MGLU3 | Varejo e consumo | 5,14 | -5,15 | 0,23 | 5,00 | 0,23 | -5,24 | -4,20 | 0,17 | — | 2,16 | — | 4,05 | 24,58 | 1,31 | 0,06 | -75% | -99% | 118 → 117 | 104 → 121 |
| AURE3 | Infraestrutura e utilities | 11,06 | -5,52 | 0,94 | 5,29 | 0,94 | -5,52 | -4,21 | 4,83 | — | 4,87 | — | 6,70 | 13,02 | 1,56 | 1,15 | -86% | -90% | 119 → 118 | 120 → 108 |
| ISAE4 | Serviços, saúde, educação e tecnologia | 25,24 | -7,53 | 4,33 | 15,72 | 4,33 | -7,53 | -5,75 | 2,86 | 5,99 | 6,76 | 5,94 | 20,96 | — | 5,01 | 1,77 | -80% | -93% | 120 → 119 | 114 → 112 |
| DESK3 | Serviços, saúde, educação e tecnologia | 19,32 | 0,26 | 4,08 | 19,46 | 4,08 | 0,26 | 1,21 | 6,85 | 3,35 | 8,00 | 4,57 | 14,10 | 14,87 | 19,46 | 2,20 | +1% | -89% | 83 → 120 | 10 → 106 |
| CVCB3 | Serviços, saúde, educação e tecnologia | 0,88 | -0,94 | -0,24 | 0,51 | -0,24 | -1,06 | -1,12 | -0,20 | — | 0,32 | — | — | 3,48 | 0,13 | 0,00 | -86% | -100% | 121 → 121 | 119 → 122 |
| AXIA3 | Serviços, saúde, educação e tecnologia | 48,18 | -12,95 | 7,19 | 23,56 | 7,19 | -12,95 | -11,49 | 7,63 | 8,49 | 17,01 | 9,50 | 45,80 | — | 7,69 | 3,22 | -84% | -93% | 122 → 122 | 117 → 113 |

Holdings: SOTP do estudo e SOTP recalculado nas colunas "Justo"; "Hist." = P/VP/P/L históricos consolidados (só referência).

## Limitações

- RIM, EVA, APV e FCFE usam as mesmas projeções do estudo: mudam a lente (âncora em PL/CI, fade, estrutura de capital, política de dívida), não os drivers operacionais. Divergências grandes apontam premissas a revisar, não erros de método.
- O APV ignora custos de dificuldade financeira, relevantes para as alavancadas (MGLU3, CVCB3, AZZA3, ECOR3), e trata o benefício fiscal com o risco do ativo (Harris–Pringle).
- O FCFE com estrutura de capital constante supõe rolar e ampliar a dívida na proporção da receita. Para quem precisa desalavancar (covenants), superestima o fluxo do acionista.
- Pares: a cobertura tem só 1 a 4 pares por segmento, e os múltiplos são da foto pós-queda. VBBR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3, SMFT3 e CVCB3 não têm par na cobertura. O ajuste ao Ke usa a TIR implícita de cada par (DDM do estudo) e vale só para múltiplos de equity.
- P(valor > preço) nos esquemas novos reescala a amostra do Monte Carlo do motor, sem refazer as 5.000 simulações; a TIR implícita, o Altman e a confiança não mudam com os pesos.
- Bancos ficam sem FCFF/EVA/APV, e o FCFE coincide com o DDM porque o PL projetado é o capital exigido.
