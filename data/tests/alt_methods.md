# Métodos alternativos de valuation e novos pesos (Ke 25%)

*Gerado em 2026-10-26T16:35:01 por `pipeline/tests/alt_methods.py`. Motor `pipeline/model.py` importado sem alterações, premissas lidas de `research/` no momento da execução (os revisores seguem ajustando; rode de novo para atualizar), preços da foto do estudo. Valores por ação/unit, comparáveis ao preço. Dados completos em `data/tests/alt_methods.json`.*

## Resumo

1. **Os métodos intrínsecos alternativos confirmam DCF e DDM.** Mediana por empresa em relação ao DDM: RIM 1,00×, P/L justificado 0,91×, P/VP justificado 1,18×, FCFE 1,17×, pares ajustados ao Ke 1,09×. Em relação ao DCF: APV 1,01× e EVA 0,99×. RIM ≡ DDM e EVA ≡ DCF são identidades quando a perpetuidade é a mesma (erro máximo 1e-14 e 2e-15, relativo). As diferenças vêm só do fade do retorno excedente (RIM em 17 empresas, EVA em 23) e da política de dívida (APV e FCFE).
2. **O viés está nos métodos de mercado.** Na mediana, os múltiplos-alvo do estudo ficam 2,47× o DCF, os pares 2,17× e a mediana histórica de 5 anos 3,82×. Eles embutem Ke de cerca de 13% (P/L-alvo) e 11% (P/L histórico), e o preço de hoje embute uma TIR de dono mediana de 14%: nenhum deles está em 25%. Com 25% de peso, a perna de múltiplos-alvo responde, na mediana, por 49% do valor justo industrial do estudo. Nos bancos, com 50% de peso, responde por 0%.
3. **Onde e por que divergem.** (i) Alavancagem com Ke fixo: 19 das 53 industriais têm DCF ≤ 0 (EV abaixo da dívida, com ROIC < WACC), mas 18 delas têm DDM/FCFE/RIM > 0. Um Ke de 25% que não sobe com a alavancagem viola Modigliani-Miller, e o acionista tem responsabilidade limitada (utilities, concessões, locadoras, MGLU3, ASAI3). (ii) `other_financial` entra no lucro, mas não no FCFF (AZZA3, NATU3, EZTC3, MRVE3, PLPL3, TEND3, AURE3, ENGI11, EQTL3): no caso de TEND3/PLPL3/MRVE3, juros capitalizados e custo de cessões inflam o DCF frente ao RIM/FCFE. (iii) Payout baixo: o FCFE supera o DDM em +17% na mediana, porque o caixa retido rende Kd·(1−t) < Ke. (iv) PL com ágio (HAPV3, AZZA3, ALOS3) tira o sentido do P/VP. Detalhes por empresa na tabela de divergências.
4. **Pesos recomendados.** Cada classe usa os métodos coerentes com Ke 25% (tabela abaixo): RIM nos bancos e incorporadoras, APV/DCF mais o lado do acionista em infraestrutura, EVA/APV em locação, e DCF com pares ajustados ao Ke no varejo. Múltiplos de mercado brutos (alvo, pares e histórico) ficam como referência relativa e saem do valor justo.
5. **Efeito.** O valor justo muda -24% na mediana (infraestrutura -61%, shoppings -30%, serviços -28%, bancos -19%, varejo -19%, incorporadoras -14%, locação -14%, cíclicas -14%). O upside mediano das 59 passa de -49% para -63%, e empresas com upside > 0: 4 → 3. Quase toda a queda vem de retirar os múltiplos-alvo: o esquema "estudo sem múltiplos" já dá -65%. O ranking quase não muda (Spearman do escore multifator 1,00; do upside 0,97), porque o upside pesa só 10% do escore e a TIR de dono (30%), a qualidade e a solidez não dependem dos pesos.
6. **As 7 oportunidades.** Com as premissas revisadas de agora, o estudo recalculado mantém 5 das 7 pela regra (BEEF3, PLPL3, TEND3, MDNE3, COGN3). Com os pesos propostos, ficam 3: BEEF3 (upside +39%), PLPL3 (upside +7%), TEND3 (upside +3%). Saem MDNE3 (P(MC) 40%), COGN3 (P(MC) 36%). Nenhuma empresa nova entra. Os rankings das oportunidades mudam pouco (tabela abaixo).

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
| DCF-FCFF (estudo) | 53 | -38% | -132% / -23% | — | 9% | -67% |
| APV | 53 | -31% | -88% / -20% | +1% | 13% | -63% |
| EVA (fade ROIC) | 53 | -39% | -135% / -23% | -1% | 6% | -67% |
| DDM (estudo) | 57 | -19% | -31% / -10% | -1% | 19% | -59% |
| DDM c/ emissões e recompras | 57 | -19% | -31% / -10% | -1% | 19% | -59% |
| FCFE (DL ∝ receita) | 53 | -7% | -26% / +13% | +26% | 40% | -52% |
| RIM/Ohlson (fade ROE) | 57 | -19% | -31% / -10% | -1% | 19% | -59% |
| P/L justificado | 54 | -26% | -38% / -13% | -9% | 15% | -61% |
| P/VP justificado | 57 | +7% | -26% / +63% | +4% | 53% | -51% |
| Pares ajustados ao Ke 25% | 46 | -4% | -28% / +12% | +5% | 43% | -50% |
| Múltiplos-alvo (estudo) | 57 | +94% | +59% / +170% | +147% | 98% | +3% |
| Pares (mediana) | 48 | +85% | +25% / +252% | +117% | 81% | -7% |
| Histórico 5a (mediana) | 56 | +236% | +108% / +363% | +282% | 100% | +70% |
| SOTP (controladas c/ pesos novos) | 2 | -15% | -19% / -12% | — | 0% | -47% |

O valor justo do estudo já inclui 25% (bancos: 50%) de múltiplos-alvo; por isso os intrínsecos aparecem abaixo dele e próximos do DCF/DDM.

## Onde os métodos divergem mais (e por quê)

Dispersão = desvio-padrão do log dos valores positivos de todos os métodos. Ke implícito no P/L histórico = Ke que torna a mediana de 5 anos do P/L (LTM, Gordon com ROE e g terminais) coerente; TIR hoje = TIR de dono implícita no preço (DDM do estudo).

| # | Empresa | Classe | σ log | Máx/mín | Mercado/intrínseco | Ke impl. P/L hist. | TIR hoje | Causas principais |
|---|---|---|---|---|---|---|---|---|
| 1 | MGLU3 | Varejo e consumo | 1,74 | 106,8× | 21,73× | 6% | 6% | múltiplos de mercado 21,7× a mediana intrínseca (P/L histórico embute Ke ≈ 6%; P/L-alvo embute Ke ≈ 9% vs 25%); EV a WACC 19% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 2 | SMFT3 | Serviços, saúde, educação e tecnologia | 1,47 | 239,3× | 4,47× | 9% | 14% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 67%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 18% abaixo da dívida (ROIC 2030 12%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 4,5× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 11% vs 25%) |
| 3 | SBFG3 | Varejo e consumo | 1,27 | 173,9× | 2,08× | 12% | 21% | EV a WACC 19% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,1× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 15% vs 25%); FCFE/DDM = 1,33: payout médio 36% retém caixa que rende Kd·(1−t) < Ke |
| 4 | ENGI11 | Infraestrutura e utilities | 1,06 | 45,0× | 4,88× | 14% | 8% | FCFE/DDM = 0,20: dividendos projetados acima do FCFE (desalavancagem cessa ou dívida financia o payout); múltiplos de mercado 4,9× a mediana intrínseca (P/L histórico embute Ke ≈ 14%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 9%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 5 | HAPV3 | Serviços, saúde, educação e tecnologia | 1,05 | 32,1× | 3,44× | — | 27% | múltiplos de mercado 3,4× a mediana intrínseca (P/L-alvo embute Ke ≈ 15% vs 25%); APV/DCF = 1,77: dívida projetada (DL/EBITDA 3,7x → 1,8x em 2030) ≠ peso-alvo wd = 35% do WACC; FCFE/DDM = 1,57: payout médio 22% retém caixa que rende Kd·(1−t) < Ke |
| 6 | CVCB3 | Serviços, saúde, educação e tecnologia | 1,04 | 11,0× | — | — | — | múltiplos de mercado 6,3× a mediana intrínseca (P/L-alvo embute Ke ≈ 13% vs 25%) |
| 7 | AURE3 | Infraestrutura e utilities | 0,97 | 13,9× | 6,85× | — | 7% | múltiplos de mercado 6,8× a mediana intrínseca; FCFE/DDM = 5,28: payout médio 25% retém caixa que rende Kd·(1−t) < Ke; EV a WACC 17% abaixo da dívida (ROIC 2030 6%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 8 | RAIL3 | Infraestrutura e utilities | 0,96 | 46,1× | 4,66× | 6% | 10% | múltiplos de mercado 4,7× a mediana intrínseca (P/L histórico embute Ke ≈ 6%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 10%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 9 | VBBR3 | Cíclicas / commodities | 0,89 | 22,7× | 3,38× | 15% | 10% | múltiplos de mercado 3,4× a mediana intrínseca (P/L histórico embute Ke ≈ 15%; P/L-alvo embute Ke ≈ 15% vs 25%); APV/DCF = 2,02: dívida projetada (DL/EBITDA 2,3x → 1,7x em 2030) ≠ peso-alvo wd = 27% do WACC |
| 10 | MRVE3 | Incorporadoras | 0,89 | 25,7× | 3,07× | — | 12% | other_financial (R$ -696 mi/ano, -163% do LL) entra no LL (DDM/RIM/FCFE) mas não no FCFF do DCF; FCFF acima do lucro (FCFF/LL 2027–30 = 376%) → DCF ≫ RIM/DDM; múltiplos de mercado 3,1× a mediana intrínseca (P/L-alvo embute Ke ≈ 15% vs 25%) |
| 11 | EQTL3 | Infraestrutura e utilities | 0,88 | 10,1× | 5,56× | 9% | 7% | múltiplos de mercado 5,6× a mediana intrínseca (P/L histórico embute Ke ≈ 9%; P/L-alvo embute Ke ≈ 11% vs 25%); EV a WACC 18% abaixo da dívida (ROIC 2030 8%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada |
| 12 | SBSP3 | Infraestrutura e utilities | 0,86 | 8,6× | 8,13× | 10% | 8% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = -41%: capex/ΔCG) → DCF ≪ métodos de lucro; múltiplos de mercado 8,1× a mediana intrínseca (P/L histórico embute Ke ≈ 10%; P/L-alvo embute Ke ≈ 11% vs 25%); DCF dependente da perpetuidade (TV = 218% do EV: fluxos explícitos negativos) |
| 13 | ORVR3 | Infraestrutura e utilities | 0,84 | 14,2× | 6,61× | — | 10% | múltiplos de mercado 6,6× a mediana intrínseca (P/L-alvo embute Ke ≈ 9% vs 25%); DDM do estudo ignora a emissão de ações de R$ 1.000 mi projetada (dividendo cresce com o capital novo, ações fixas): com ela o DDM seria -56%; o RIM (clean surplus) já a desconta |
| 14 | RADL3 | Varejo e consumo | 0,77 | 16,8× | 4,29× | 7% | 12% | múltiplos de mercado 4,3× a mediana intrínseca (P/L histórico embute Ke ≈ 7%; P/L-alvo embute Ke ≈ 11% vs 25%); APV/DCF = 1,41: dívida projetada (DL/EBITDA 1,6x → 1,2x em 2030) ≠ peso-alvo wd = 18% do WACC |
| 15 | MOTV3 | Infraestrutura e utilities | 0,76 | 20,9× | 2,65× | — | 13% | FCFF baixo frente ao lucro (FCFF/LL 2027–30 = 64%: capex/ΔCG) → DCF ≪ métodos de lucro; EV a WACC 18% abaixo da dívida (ROIC 2030 11%): DCF/APV ≤ 0, mas DDM/FCFE/RIM > 0 — Ke fixo não sobe com a alavancagem (MM) e o acionista tem responsabilidade limitada; múltiplos de mercado 2,6× a mediana intrínseca (P/L-alvo embute Ke ≈ 13% vs 25%) |

## Pesos propostos por classe

| Classe | Empresas | Pesos | Justificativa |
|---|---|---|---|
| Bancos | BPAC11, BBAS3, BBDC4, BRSR6 | RIM/Ohlson (fade ROE) 50%, DDM (estudo) 25%, P/VP justificado 25% | Dívida é matéria-prima (não há FCFF/EV); o valor vem do spread ROE − Ke sobre o capital regulatório. RIM ancora no PL (Basileia) e independe da política de payout; DDM complementa (dividendo limitado pelo capital); P/VP justificado = RIM em estado estacionário. Múltiplos de mercado embutem Ke implícito < 25% e ficam como referência. |
| Incorporadoras | CYRE3, EZTC3, MDNE3, JHSF3, MRVE3, PLPL3, DIRR3, CURY3, TEND3 | RIM/Ohlson (fade ROE) 45%, FCFE (DL ∝ receita) 20%, Pares ajustados ao Ke 25% 15%, DCF-FCFF (estudo) 10%, P/VP justificado 10% | Estoque/terreno e recebíveis SÃO o capital de giro: FCFF oscila com landbank e repasses, e o lucro (POC) mede melhor a criação de valor. RIM sobre o PL (estoque a custo) é o método natural, com P/VP justificado como âncora e FCFE (dívida SFH/cessões no fluxo do acionista); DCF com peso baixo porque o FCFF ignora o other_financial (juros capitalizados, custo de cessões); pares MCMV/média-alta são homogêneos (ajustados ao Ke 25%). |
| Infraestrutura e utilities | ECOR3, MOTV3, RAIL3, AURE3, ENGI11, EQTL3, CPLE3, ALUP11, SBSP3, ORVR3 | APV 40%, DCF-FCFF (estudo) 20%, FCFE (DL ∝ receita) 20%, DDM c/ emissões e recompras 20% | Ativos de vida longa, fluxos previsíveis e alavancagem que muda ao longo da concessão (amortização, ciclos de capex): o APV separa valor operacional (Ku) do benefício fiscal da dívida projetada, sem supor wd constante; DCF-WACC como contraparte; DDM/FCFE (40%) porque, com Ke fixo e ROIC < WACC, o EV fica abaixo da dívida e só o lado do acionista (responsabilidade limitada) dá valor positivo. |
| Shoppings (renda imobiliária) | MULT3, IGTI11, ALOS3 | APV 35%, DCF-FCFF (estudo) 35%, FCFE (DL ∝ receita) 15%, DDM c/ emissões e recompras 15% | NOI estável e alavancagem estrutural (CRI/debêntures) → DCF/APV; PL a custo histórico subavalia as propriedades, então RIM/P/VP ficam fora; DDM/FCFE capturam a distribuição recorrente. |
| Locação (capital intensivo) | RENT3, MOVI3, VAMO3 | EVA (fade ROIC) 30%, APV 25%, DCF-FCFF (estudo) 25%, FCFE (DL ∝ receita) 20% | Valor = (ROIC − WACC) × crescimento da frota: EVA explicita o spread e sua convergência; dívida é estrutural e cíclica (APV); DCF como base; FCFE (estrutura de capital constante) evita penalizar a retenção. |
| Varejo e consumo | MGLU3, SBFG3, CEAB3, LREN3, AZZA3, VIVA3, VULC3, ALPA4, NATU3, ASAI3, GMAT3, PGMN3, RADL3, HYPE3 | DCF-FCFF (estudo) 35%, FCFE (DL ∝ receita) 20%, Pares ajustados ao Ke 25% 25%, P/L justificado 20% | Ciclo curto, margens que revertem à média e arrendamentos IFRS-16: a perpetuidade do DCF é frágil e os pares carregam a leitura do ciclo — mas reescalados ao Ke 25% (Gordon, pela TIR implícita de cada par); P/L justificado mantém o múltiplo coerente com o Ke; FCFE evita penalizar a retenção. |
| Serviços, saúde, educação e tecnologia | SMFT3, CVCB3, YDUQ3, COGN3, ANIM3, HAPV3, RDOR3, B3SA3, TOTS3, INTB3, GGPS3 | DCF-FCFF (estudo) 40%, FCFE (DL ∝ receita) 20%, EVA (fade ROIC) 20%, P/L justificado 20% | Asset-light/crescimento: DCF como base; EVA expõe a convergência do ROIC; FCFE (estrutura de capital constante) e P/L justificado como checagens do lado do acionista. |
| Cíclicas / commodities | VBBR3, BEEF3, TTEN3 | DCF-FCFF (estudo) 45%, FCFE (DL ∝ receita) 30%, DDM c/ emissões e recompras 25% | Lucro cíclico e alavancagem alta: DCF com o ciclo projetado explicitamente; FCFE/DDM do lado do acionista. Múltiplos (históricos ou de pares) não normalizam o ciclo a Ke 25% e o PL é comprimido (BEEF3): ficam como referência. |
| Holdings (SOTP) | SIMH3, CSAN3 | SOTP (controladas c/ pesos novos) 100% | SOTP é o único método coerente; recalculado com o valor justo novo das controladas avaliadas pelo motor. |

Princípios: (1) só entram métodos coerentes com Ke 25%; múltiplos de mercado brutos embutem o Ke implícito do mercado e viram referência; (2) para bancos não existe FCFF/EV; (3) o FCFE substitui o DDM onde o payout é baixo e discricionário; (4) o APV entra onde a alavancagem muda ou difere do wd do WACC. Pesos do estudo, para comparação: industrial DCF 50% / DDM 25% / múltiplos-alvo 25%; bancos DDM 50% / múltiplos 50%; holdings SOTP 100% (EZTC3 com 70/10/20). A agregação é a do motor: média de max(0, valor), renormalizada nos métodos disponíveis.

### Efeito por classe

| Classe | n | Δ mediano do valor justo | Upside mediano estudo | Upside mediano proposto |
|---|---|---|---|---|
| Bancos | 4 | -19% | -23% | -37% |
| Incorporadoras | 9 | -14% | -12% | -22% |
| Infraestrutura e utilities | 10 | -61% | -75% | -89% |
| Shoppings (renda imobiliária) | 3 | -30% | -47% | -63% |
| Locação (capital intensivo) | 3 | -14% | -52% | -68% |
| Varejo e consumo | 14 | -19% | -48% | -60% |
| Serviços, saúde, educação e tecnologia | 11 | -28% | -44% | -58% |
| Cíclicas / commodities | 3 | -14% | -70% | -82% |
| Holdings (SOTP) | 2 | -15% | -37% | -47% |

### Esquemas comparados

| Esquema | Upside mediano | Upside > 0 | Spearman escore vs estudo | Spearman upside vs estudo | Oportunidades pela regra (top 8 por escore) |
|---|---|---|---|---|---|
| Estudo (recalculado agora) | -49% | 4 | 1,00 | 1,00 | BEEF3, PLPL3, TEND3, MDNE3, COGN3 |
| Estudo sem múltiplos-alvo (DCF/DDM renormalizados) | -65% | 3 | 1,00 | 0,97 | BEEF3, PLPL3, TEND3 |
| **Proposto por classe** | -63% | 3 | 1,00 | 0,97 | BEEF3, PLPL3, TEND3 |
| Proposto sem pares ajustados (só intrínsecos) | -63% | 3 | 1,00 | 0,97 | BEEF3, PLPL3, TEND3 |
| Peso igual em todos os métodos (inclui mercado bruto) | -38% | 10 | 0,99 | 0,89 | BEEF3, PLPL3, CEAB3, MDNE3, TEND3, LREN3, COGN3 |

Top 10 do escore multifator: estudo BEEF3, PLPL3, HAPV3, TEND3, MDNE3, CEAB3, LREN3, CYRE3, DIRR3, COGN3; proposto BEEF3, PLPL3, HAPV3, CEAB3, MDNE3, TEND3, ANIM3, COGN3, LREN3, SBFG3.

Maiores mudanças no ranking por upside (posições; + = sobe): MOVI3 +10, GMAT3 +10, VBBR3 +8, ASAI3 +8, EZTC3 -8, MRVE3 +8, SMFT3 -8, BPAC11 -8, VAMO3 +7, JHSF3 +7.

## As 7 oportunidades

| Empresa | Preço | Valor justo estudo → proposto | Upside estudo → proposto | Rank escore | Rank upside | P(MC) estudo → proposto | Regra (proposto) |
|---|---|---|---|---|---|---|---|
| BEEF3 | 3,38 | 5,44 → 4,69 | +61% → +39% | 1 → 1 | 1 → 1 | 74% → 67% | passa |
| PLPL3 | 5,70 | 6,37 → 6,11 | +12% → +7% | 2 → 2 | 3 → 2 | 65% → 61% | passa |
| TEND3 | 22,38 | 26,81 → 23,01 | +20% → +3% | 4 → 6 | 2 → 3 | 73% → 55% | passa |
| MDNE3 | 19,66 | 20,19 → 18,46 | +3% → -6% | 5 → 5 | 4 → 4 | 54% → 40% | não passa |
| COGN3 | 2,01 | 1,97 → 1,79 | -2% → -11% | 10 → 8 | 5 → 7 | 47% → 36% | não passa |

Regra do estudo (build.py): TIR de dono ≥ 20%, P(valor justo > preço) ≥ 45%, Altman fora da zona de risco e confiança diferente de baixa. A TIR, o Altman e a confiança não mudam com os pesos; a probabilidade reescala a amostra do Monte Carlo do motor pelo novo valor justo.

- **BEEF3** (Cíclicas / commodities): DCF-FCFF (estudo) 6,37, APV 8,28, EVA (fade ROIC) 5,16, DDM (estudo) 3,27, DDM c/ emissões e recompras 2,59, FCFE (DL ∝ receita) 3,94, RIM/Ohlson (fade ROE) 2,35, P/L justificado 2,13, P/VP justificado 1,01, Múltiplos-alvo (estudo) 5,75, Histórico 5a (mediana) 6,65. Divergências: FCFF acima do lucro (FCFF/LL 2027–30 = 250%) → DCF ≫ RIM/DDM; múltiplos de mercado 1,9× a mediana intrínseca (P/L histórico embute Ke ≈ 12%; P/L-alvo embute Ke ≈ 18% vs 25%); DDM do estudo ignora a emissão de ações de R$ 930 mi projetada (dividendo cresce com o capital novo, ações fixas): com ela o DDM seria -21%; o RIM (clean surplus) já a desconta.
- **PLPL3** (Incorporadoras): DCF-FCFF (estudo) 7,58, APV 7,77, EVA (fade ROIC) 6,98, DDM (estudo) 5,75, DDM c/ emissões e recompras 5,75, FCFE (DL ∝ receita) 6,69, RIM/Ohlson (fade ROE) 5,71, P/L justificado 5,53, P/VP justificado 4,70, Pares ajustados ao Ke 25% 6,53, Múltiplos-alvo (estudo) 6,25, Pares (mediana) 8,97, Histórico 5a (mediana) 11,48.
- **TEND3** (Incorporadoras): DCF-FCFF (estudo) 32,83, APV 33,22, EVA (fade ROIC) 30,35, DDM (estudo) 21,71, DDM c/ emissões e recompras 21,71, FCFE (DL ∝ receita) 25,82, RIM/Ohlson (fade ROE) 21,12, P/L justificado 22,30, P/VP justificado 12,56, Pares ajustados ao Ke 25% 25,35, Múltiplos-alvo (estudo) 31,22, Pares (mediana) 33,94, Histórico 5a (mediana) 40,80. Divergências: other_financial (R$ -227 mi/ano, -25% do LL) entra no LL (DDM/RIM/FCFE) mas não no FCFF do DCF.
- **MDNE3** (Incorporadoras): DCF-FCFF (estudo) 16,09, APV 16,33, EVA (fade ROIC) 15,86, DDM (estudo) 19,20, DDM c/ emissões e recompras 19,20, FCFE (DL ∝ receita) 21,67, RIM/Ohlson (fade ROE) 19,15, P/L justificado 18,93, P/VP justificado 16,60, Pares ajustados ao Ke 25% 14,90, Múltiplos-alvo (estudo) 22,22, Pares (mediana) 33,04, Histórico 5a (mediana) 33,73.
- **COGN3** (Serviços, saúde, educação e tecnologia): DCF-FCFF (estudo) 1,74, APV 1,55, EVA (fade ROIC) 1,74, DDM (estudo) 1,65, DDM c/ emissões e recompras 1,65, FCFE (DL ∝ receita) 2,37, RIM/Ohlson (fade ROE) 1,65, P/L justificado 1,36, P/VP justificado 4,46, Pares ajustados ao Ke 25% 2,56, Múltiplos-alvo (estudo) 2,76, Pares (mediana) 2,82, Histórico 5a (mediana) 5,06. Divergências: FCFE/DDM = 1,44: payout médio 50% retém caixa que rende Kd·(1−t) < Ke.

## Para os revisores (achados que afetam o estudo)

- **Múltiplos-alvo incoerentes com Ke 25%**: o P/L-alvo mediano embute Ke de ~13%. Para manter os múltiplos no blend, use os justificados (Gordon a 25%) ou os pares ajustados pela TIR implícita.
- **DCF × `other_financial`**: o FCFF exclui `other_financial`, mas o lucro (DDM/RIM/FCFE) inclui. Onde ele é material (AZZA3 -23% do LL, NATU3 -19% do LL, EZTC3 +25% do LL, MRVE3 -163% do LL, PLPL3 -19% do LL, TEND3 -25% do LL, AURE3 +122% do LL, ENGI11 +18% do LL, EQTL3 +52% do LL), trate o item como ajuste debt-like ou como fluxo operacional, para não inflar (ou deprimir) o DCF.
- **DDM × emissão/recompra projetada**: o DDM do motor desconta só dividendos, com o número de ações fixo; o capital novo aumenta o lucro e o dividendo sem diluir. ORVR3: emissão R$ 1.000 mi, recompra R$ 0 mi → DDM -56% com o fluxo de capital; BEEF3: emissão R$ 930 mi, recompra R$ 0 mi → DDM -21% com o fluxo de capital. Corrija no DDM (fluxo líquido ao acionista) ou ajuste o número de ações.
- **wd do WACC × dívida projetada**: em 19 industriais o DCF dá equity ≤ 0. Com Ke fixo, o wd-alvo precisa ser coerente com a alavancagem a que 25% se refere; senão DCF e DDM medem coisas diferentes (ver APV/DCF e FCFE/DDM no JSON).
- **Série de múltiplos históricos**: BRSR6 (50 meses descartados). Esses meses têm erro de unidade de ações em `multiples_history` (P/L 0,01, P/VP 0,001), e as medianas de `stats` ficam inválidas.
- **Holdings**: componentes "market" fora da foto de preços (nenhum) forçam cotação ao vivo, que falha de forma intermitente e zera o componente. Aqui o cache foi semeado com o último `data/model` do motor.
- **HAPV3**: o PL de R$ 48 bi é quase todo ágio da fusão e o preço implica P/VP de 0,05×. P/VP e RIM com fade não fazem sentido ali; o fade só corrói retorno excedente.

## Tabela completa (59)

Valores por ação/unit (R$). Rank = escore multifator do build.py recalculado; ↑ = rank por upside. Ordem: rank proposto.

| Empresa | Classe | Preço | DCF | DDM | Múlt. | RIM | EVA | APV | FCFE | P/L j | P/VP j | Pares Ke | Pares | Hist. | Justo estudo | Justo proposto | Upside estudo | Upside proposto | Rank | ↑ Rank |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BEEF3 | Cíclicas / commodities | 3,38 | 6,37 | 3,27 | 5,75 | 2,35 | 5,16 | 8,28 | 3,94 | 2,13 | 1,01 | — | — | 6,65 | 5,44 | 4,69 | +61% | +39% | 1 → 1 | 1 → 1 |
| PLPL3 | Incorporadoras | 5,70 | 7,58 | 5,75 | 6,25 | 5,71 | 6,98 | 7,77 | 6,69 | 5,53 | 4,70 | 6,53 | 8,97 | 11,48 | 6,37 | 6,11 | +12% | +7% | 2 → 2 | 3 → 2 |
| HAPV3 | Serviços, saúde, educação e tecnologia | 5,00 | 2,52 | 5,57 | 8,67 | 5,57 | 2,52 | 4,46 | 8,78 | 2,78 | 50,58 | 4,25 | 19,20 | 80,90 | 4,82 | 3,82 | -4% | -24% | 3 → 3 | 6 → 11 |
| CEAB3 | Varejo e consumo | 7,35 | 4,30 | 5,75 | 13,26 | 5,75 | 4,18 | 4,73 | 6,67 | 5,62 | 6,34 | 11,05 | 20,29 | 13,74 | 6,91 | 6,73 | -6% | -8% | 6 → 4 | 8 → 5 |
| MDNE3 | Incorporadoras | 19,66 | 16,09 | 19,20 | 22,22 | 19,15 | 15,86 | 16,33 | 21,67 | 18,93 | 16,60 | 14,90 | 33,04 | 33,73 | 20,19 | 18,46 | +3% | -6% | 5 → 5 | 4 → 4 |
| TEND3 | Incorporadoras | 22,38 | 32,83 | 21,71 | 31,22 | 21,12 | 30,35 | 33,22 | 25,82 | 22,30 | 12,56 | 25,35 | 33,94 | 40,80 | 26,81 | 23,01 | +20% | +3% | 4 → 6 | 2 → 3 |
| ANIM3 | Serviços, saúde, educação e tecnologia | 2,74 | 2,43 | 2,07 | 3,21 | 2,07 | 2,24 | 1,43 | 3,71 | 1,60 | 4,16 | 2,89 | 2,09 | 10,16 | 2,54 | 2,48 | -7% | -9% | 12 → 7 | 9 → 6 |
| COGN3 | Serviços, saúde, educação e tecnologia | 2,01 | 1,74 | 1,65 | 2,76 | 1,65 | 1,74 | 1,55 | 2,37 | 1,36 | 4,46 | 2,56 | 2,82 | 5,06 | 1,97 | 1,79 | -2% | -11% | 10 → 8 | 5 → 7 |
| LREN3 | Varejo e consumo | 9,51 | 6,18 | 7,40 | 15,39 | 7,34 | 6,14 | 6,45 | 7,46 | 5,76 | 6,47 | 10,00 | 17,01 | 23,05 | 8,79 | 7,31 | -8% | -23% | 7 → 9 | 10 → 10 |
| SBFG3 | Varejo e consumo | 5,88 | -0,39 | 4,57 | 9,51 | 4,57 | -0,46 | 0,09 | 6,08 | 4,47 | 5,56 | 6,03 | 7,07 | 15,75 | 3,52 | 3,62 | -40% | -38% | 14 → 10 | 23 → 18 |
| CYRE3 | Incorporadoras | 20,13 | 15,12 | 15,95 | 21,92 | 15,95 | 15,03 | 15,57 | 17,66 | 15,06 | 14,76 | 12,90 | 30,26 | 27,18 | 17,76 | 15,63 | -12% | -22% | 8 → 11 | 13 → 9 |
| DIRR3 | Incorporadoras | 8,97 | 8,67 | 7,33 | 10,68 | 7,33 | 8,13 | 8,76 | 7,88 | 7,28 | 5,59 | 7,69 | 8,43 | 18,55 | 8,59 | 7,45 | -4% | -17% | 9 → 12 | 7 → 8 |
| CURY3 | Incorporadoras | 26,94 | 21,43 | 19,94 | 28,42 | 19,32 | 20,16 | 21,43 | 20,17 | 17,98 | 10,75 | 16,60 | 17,84 | 41,98 | 22,89 | 18,44 | -15% | -32% | 11 → 13 | 14 → 14 |
| PGMN3 | Varejo e consumo | 2,94 | 1,24 | 2,01 | 4,58 | 2,01 | 1,18 | 1,43 | 2,80 | 1,82 | 2,61 | 2,37 | 7,95 | 6,29 | 2,27 | 1,95 | -23% | -34% | 15 → 14 | 18 → 15 |
| YDUQ3 | Serviços, saúde, educação e tecnologia | 8,48 | 6,26 | 6,19 | 9,69 | 6,19 | 6,26 | 6,11 | 8,94 | 2,67 | 8,60 | 3,55 | 7,35 | 12,16 | 7,10 | 6,08 | -16% | -28% | 16 → 15 | 15 → 13 |
| BBAS3 | Bancos | 17,57 | — | 12,62 | 19,41 | 12,49 | — | — | — | 11,49 | 14,67 | 16,21 | 25,21 | 18,50 | 15,67 | 13,07 | -11% | -26% | 13 → 16 | 11 → 12 |
| MOVI3 | Locação (capital intensivo) | 8,67 | -0,39 | 5,80 | 10,98 | 5,61 | -1,64 | 8,09 | 9,15 | 5,41 | 5,26 | 6,36 | 17,31 | 16,05 | 4,19 | 3,85 | -52% | -56% | 17 → 17 | 35 → 25 |
| VULC3 | Varejo e consumo | 12,49 | 7,79 | 7,84 | 15,41 | 7,84 | 7,79 | 7,77 | 8,14 | 7,15 | 7,18 | 7,53 | 17,74 | 20,68 | 9,70 | 7,67 | -22% | -39% | 18 → 18 | 17 → 19 |
| INTB3 | Serviços, saúde, educação e tecnologia | 14,63 | 5,97 | 6,02 | 14,98 | 6,02 | 5,97 | 5,97 | 6,67 | 6,06 | 6,06 | — | — | 22,77 | 8,23 | 6,13 | -44% | -58% | 20 → 19 | 24 → 27 |
| VIVA3 | Varejo e consumo | 19,47 | 9,79 | 9,59 | 24,07 | 9,59 | 9,64 | 9,64 | 11,20 | 9,26 | 10,16 | 10,13 | 23,53 | 36,16 | 13,31 | 10,05 | -32% | -48% | 21 → 20 | 21 → 22 |
| SIMH3 | Holdings (SOTP) | 6,87 | — | — | — | — | — | — | — | — | — | — | — | 17,35 | 3,84 | 3,54 | -44% | -49% | 22 → 21 | 25 → 23 |
| BBDC4 | Bancos | 15,47 | — | 9,95 | 16,68 | 9,83 | — | — | — | 9,08 | 9,60 | 8,28 | 11,02 | 19,80 | 12,37 | 9,80 | -20% | -37% | 23 → 22 | 16 → 17 |
| EZTC3 | Incorporadoras | 12,12 | 10,11 | 6,24 | 14,97 | 6,24 | 10,11 | 10,11 | 7,26 | 5,54 | 5,66 | 7,64 | 8,72 | 15,14 | 10,69 | 6,99 | -12% | -42% | 19 → 23 | 12 → 20 |
| GGPS3 | Serviços, saúde, educação e tecnologia | 12,03 | 5,19 | 5,16 | 14,33 | 5,15 | 4,99 | 5,16 | 6,63 | 4,21 | 5,06 | — | — | 23,46 | 7,47 | 5,24 | -38% | -56% | 24 → 24 | 22 → 26 |
| B3SA3 | Serviços, saúde, educação e tecnologia | 15,10 | 5,90 | 5,56 | 13,23 | 5,47 | 5,65 | 5,94 | 5,66 | 4,53 | 4,68 | — | — | 16,26 | 7,65 | 5,53 | -49% | -63% | 25 → 25 | 30 → 31 |
| HYPE3 | Varejo e consumo | 20,21 | 7,08 | 9,08 | 19,79 | 9,08 | 7,08 | 6,42 | 12,45 | 8,22 | 10,25 | 10,78 | 17,28 | 37,06 | 10,76 | 9,31 | -47% | -54% | 26 → 26 | 28 → 24 |
| VAMO3 | Locação (capital intensivo) | 2,90 | -0,29 | 1,27 | 2,55 | 1,23 | -0,61 | 1,83 | 1,82 | 1,20 | 1,21 | 1,48 | 2,30 | 9,76 | 0,96 | 0,82 | -67% | -72% | 28 → 27 | 45 → 38 |
| BRSR6 | Bancos | 14,67 | — | 9,26 | 13,71 | 9,32 | — | — | — | 8,67 | 9,41 | 14,07 | 21,88 | — | 10,91 | 9,33 | -26% | -36% | 27 → 28 | 19 → 16 |
| RENT3 | Locação (capital intensivo) | 31,73 | 7,02 | 15,26 | 34,26 | 15,12 | 7,02 | 12,39 | 16,70 | 13,66 | 13,49 | 15,49 | 24,57 | 81,33 | 15,89 | 10,30 | -50% | -68% | 29 → 29 | 32 → 35 |
| GMAT3 | Varejo e consumo | 3,75 | -0,37 | 1,29 | 3,62 | 1,29 | -0,37 | -0,34 | 1,39 | 1,46 | 2,19 | 2,51 | 4,63 | 7,82 | 1,23 | 1,20 | -67% | -68% | 32 → 30 | 46 → 36 |
| ECOR3 | Infraestrutura e utilities | 5,45 | -21,44 | 2,99 | 5,59 | 2,99 | -21,44 | -12,12 | 1,36 | 2,41 | 3,99 | 2,63 | 13,34 | 7,70 | 2,15 | 0,87 | -61% | -84% | 30 → 31 | 41 → 47 |
| RDOR3 | Serviços, saúde, educação e tecnologia | 34,96 | 8,40 | 10,77 | 27,06 | 10,53 | 7,96 | 10,79 | 13,23 | 9,49 | 8,05 | 14,83 | 13,04 | 53,01 | 13,66 | 9,50 | -61% | -73% | 33 → 32 | 42 → 40 |
| MULT3 | Shoppings (renda imobiliária) | 27,96 | 9,54 | 11,42 | 28,84 | 11,42 | 9,54 | 9,30 | 13,81 | 10,57 | 13,76 | 12,47 | 30,18 | 39,93 | 14,84 | 10,38 | -47% | -63% | 34 → 33 | 29 → 30 |
| AZZA3 | Varejo e consumo | 16,50 | 5,18 | 5,11 | 12,12 | 5,11 | 5,18 | 4,52 | 7,33 | 1,82 | 19,88 | 2,87 | 3,17 | 25,46 | 6,90 | 4,36 | -58% | -74% | 31 → 34 | 39 → 41 |
| ALOS3 | Shoppings (renda imobiliária) | 26,87 | 8,78 | 10,56 | 24,16 | 10,56 | 8,78 | 9,21 | 11,00 | 8,26 | 25,70 | 9,42 | 24,54 | 27,65 | 13,07 | 9,53 | -51% | -65% | 35 → 35 | 34 → 32 |
| ASAI3 | Varejo e consumo | 8,63 | -1,87 | 3,03 | 5,94 | 3,01 | -1,87 | 0,74 | 5,45 | 2,69 | 3,08 | 2,17 | 8,00 | 14,80 | 2,24 | 2,17 | -74% | -75% | 40 → 36 | 50 → 42 |
| ALPA4 | Varejo e consumo | 12,99 | 5,04 | 3,85 | 12,18 | 3,85 | 5,04 | 4,99 | 4,67 | 3,75 | 3,73 | 4,19 | 7,76 | 22,22 | 6,53 | 4,50 | -50% | -65% | 37 → 37 | 31 → 33 |
| RADL3 | Varejo e consumo | 15,08 | 2,07 | 4,52 | 16,96 | 4,50 | 1,98 | 2,92 | 5,18 | 3,95 | 3,96 | 3,91 | 9,98 | 33,22 | 6,41 | 3,53 | -58% | -77% | 36 → 38 | 38 → 43 |
| MOTV3 | Infraestrutura e utilities | 13,85 | -1,75 | 5,43 | 15,94 | 5,43 | -1,75 | 0,76 | 5,41 | 4,88 | 6,93 | 5,39 | 12,85 | — | 5,34 | 2,47 | -61% | -82% | 38 → 39 | 43 → 46 |
| BPAC11 | Bancos | 55,32 | — | 18,90 | 47,97 | 19,54 | — | — | — | 21,06 | 17,22 | 14,30 | 19,02 | 58,91 | 29,59 | 18,80 | -47% | -66% | 41 → 40 | 26 → 34 |
| SMFT3 | Serviços, saúde, educação e tecnologia | 16,44 | -3,41 | 5,69 | 21,80 | 5,69 | -3,41 | 0,12 | 7,67 | 5,02 | 7,36 | — | — | 29,08 | 6,87 | 2,54 | -58% | -85% | 39 → 41 | 40 → 48 |
| TOTS3 | Serviços, saúde, educação e tecnologia | 37,25 | 10,92 | 10,12 | 34,23 | 10,04 | 10,48 | 11,21 | 13,50 | 6,76 | 10,01 | — | — | 62,91 | 16,55 | 10,52 | -56% | -72% | 42 → 42 | 37 → 39 |
| IGTI11 | Shoppings (renda imobiliária) | 25,45 | 9,45 | 9,01 | 26,51 | 9,01 | 9,45 | 9,36 | 11,03 | 8,56 | 16,66 | 10,01 | 26,08 | 38,13 | 13,60 | 9,59 | -47% | -62% | 43 → 43 | 27 → 29 |
| ALUP11 | Infraestrutura e utilities | 31,31 | -3,24 | 9,49 | 27,47 | 9,49 | -3,24 | -5,08 | 11,21 | 8,93 | 14,28 | 9,80 | 53,24 | 39,62 | 9,24 | 4,14 | -70% | -87% | 44 → 44 | 49 → 50 |
| JHSF3 | Incorporadoras | 11,24 | -0,85 | 2,15 | 4,66 | 2,15 | -0,85 | -0,61 | 1,81 | 2,11 | 4,53 | 2,73 | 2,97 | 15,29 | 2,62 | 2,19 | -77% | -80% | 46 → 45 | 51 → 44 |
| NATU3 | Varejo e consumo | 5,66 | 1,98 | 1,72 | 5,54 | 1,72 | 1,98 | 2,26 | 2,81 | 0,90 | 4,58 | 1,24 | 5,01 | — | 2,81 | 1,75 | -50% | -69% | 45 → 46 | 33 → 37 |
| VBBR3 | Cíclicas / commodities | 32,30 | 1,78 | 8,27 | 15,40 | 8,27 | 1,78 | 3,60 | 10,35 | 7,17 | 14,87 | — | — | 40,56 | 6,81 | 5,97 | -79% | -82% | 47 → 47 | 53 → 45 |
| ENGI11 | Infraestrutura e utilities | 47,14 | -34,03 | 6,82 | 32,65 | 6,82 | -34,03 | -14,62 | 1,34 | 6,32 | 19,38 | 7,85 | 60,46 | 33,24 | 9,87 | 1,63 | -79% | -97% | 48 → 48 | 54 → 55 |
| CPLE3 | Infraestrutura e utilities | 15,18 | -1,94 | 3,20 | 7,97 | 3,20 | -1,94 | -0,53 | 2,72 | 2,73 | 4,16 | 3,27 | 15,85 | 11,76 | 2,79 | 1,18 | -82% | -92% | 52 → 49 | 56 → 54 |
| SBSP3 | Infraestrutura e utilities | 25,80 | -9,03 | 3,29 | 18,15 | 3,29 | -9,03 | -5,43 | -0,43 | 4,54 | 6,42 | 5,36 | 28,27 | 26,73 | 5,36 | 0,66 | -79% | -97% | 50 → 50 | 55 → 57 |
| MGLU3 | Varejo e consumo | 5,85 | -4,26 | 0,23 | 5,00 | 0,23 | -4,36 | -3,31 | -0,07 | — | 2,16 | — | 4,71 | 24,58 | 1,31 | 0,00 | -78% | -100% | 49 → 51 | 52 → 58 |
| MRVE3 | Incorporadoras | 4,98 | 4,93 | 1,36 | 4,63 | 1,36 | 4,41 | 6,98 | 1,50 | 0,99 | 3,10 | 1,51 | 1,63 | 25,54 | 2,34 | 1,94 | -53% | -61% | 51 → 52 | 36 → 28 |
| RAIL3 | Infraestrutura e utilities | 15,27 | -2,25 | 3,45 | 16,09 | 3,45 | -2,25 | 0,58 | 2,86 | 4,42 | 5,13 | 5,87 | 10,52 | 26,50 | 4,89 | 1,49 | -68% | -90% | 53 → 53 | 47 → 53 |
| ORVR3 | Infraestrutura e utilities | 15,58 | 1,89 | 2,46 | 15,46 | 1,09 | 1,89 | 2,04 | 3,01 | 2,18 | 3,78 | 2,10 | 13,51 | 9,19 | 5,42 | 2,01 | -65% | -87% | 54 → 54 | 44 → 51 |
| EQTL3 | Infraestrutura e utilities | 35,89 | -15,58 | 3,14 | 17,46 | 3,14 | -15,58 | -5,32 | 2,67 | 2,48 | 10,41 | 2,89 | 24,95 | 17,27 | 5,15 | 1,16 | -86% | -97% | 55 → 55 | 58 → 56 |
| TTEN3 | Cíclicas / commodities | 11,39 | -0,16 | 3,34 | 10,50 | 3,34 | -0,16 | 0,95 | 2,91 | 4,13 | 5,00 | — | — | 7,31 | 3,46 | 1,71 | -70% | -85% | 56 → 56 | 48 → 49 |
| AURE3 | Infraestrutura e utilities | 10,29 | -4,88 | 0,94 | 5,29 | 0,94 | -4,88 | -3,58 | 4,95 | — | 4,87 | — | 6,42 | 13,02 | 1,56 | 1,18 | -85% | -89% | 57 → 57 | 57 → 52 |
| CVCB3 | Serviços, saúde, educação e tecnologia | 1,07 | -0,77 | -0,24 | 0,51 | -0,24 | -0,89 | -0,94 | -0,22 | — | 0,32 | — | — | 3,48 | 0,13 | 0,00 | -88% | -100% | 58 → 58 | 59 → 59 |
| CSAN3 | Holdings (SOTP) | 2,97 | — | — | — | — | — | — | — | — | — | — | — | 2,39 | 2,10 | 1,62 | -29% | -45% | 59 → 59 | 20 → 21 |

Holdings: SOTP do estudo e SOTP recalculado nas colunas "Justo"; "Hist." = P/VP/P/L históricos consolidados (só referência).

## Limitações

- RIM, EVA, APV e FCFE usam as mesmas projeções do estudo: mudam a lente (âncora em PL/CI, fade, estrutura de capital, política de dívida), não os drivers operacionais. Divergências grandes apontam premissas a revisar, não erros de método.
- O APV ignora custos de dificuldade financeira, relevantes para as alavancadas (MGLU3, CVCB3, AZZA3, ECOR3), e trata o benefício fiscal com o risco do ativo (Harris–Pringle).
- O FCFE com estrutura de capital constante supõe rolar e ampliar a dívida na proporção da receita. Para quem precisa desalavancar (covenants), superestima o fluxo do acionista.
- Pares: a cobertura tem só 1 a 4 pares por segmento, e os múltiplos são da foto pós-queda. VBBR3, B3SA3, TOTS3, INTB3, GGPS3, BEEF3, TTEN3, SMFT3 e CVCB3 não têm par na cobertura. O ajuste ao Ke usa a TIR implícita de cada par (DDM do estudo) e vale só para múltiplos de equity.
- P(valor > preço) nos esquemas novos reescala a amostra do Monte Carlo do motor, sem refazer as 5.000 simulações; a TIR implícita, o Altman e a confiança não mudam com os pesos.
- Bancos ficam sem FCFF/EVA/APV, e o FCFE coincide com o DDM porque o PL projetado é o capital exigido.
