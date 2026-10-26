# CSAN3 (Cosan, holding SOTP): revisão independente

**Veredito: ajustada.** Achei um erro objetivo de período: o componente Compass usava a cotação de outra hora.

| | Antes | Depois |
|---|---|---|
| Valor justo | R$ 2,157 | **R$ 2,100** |
| Upside vs. preço de R$ 2,97 | −27,4% | −29,3% |
| NAV a mercado por ação | 3,62 | 3,57 |
| Desconto sobre o NAV a mercado | 18,0% | 16,7% |

O motor não calcula TIR de dono para holdings. Original em `research/review/CSAN3.orig.json`.

## Achado principal: Compass precificada fora da foto do estudo

| # | Severidade | Achado | Evidência |
|---|---|---|---|
| 1 | média (erro objetivo) | Compass entrava como `market` com PASS3 **ao vivo** e CSAN3 da foto de 13:02 | PASS3 não está em `data/market/quotes.json` (foto de 13:02:40). Com `EAGORA_SNAPSHOT=1`, `live_quote` cai na API ao vivo. O valor publicado usou ~R$ 20,84 (≈15:17; 14.883,7 ÷ 714,19). Às 13:02 a PASS3 estava a **R$ 20,43** (B3 DailyFluctuationHistory). Uma nova rodada às 16:07 usaria R$ 19,72 e daria SOTP de R$ 2,00. O resultado mudava conforme a hora em que se rodava o pipeline |

**Correção:** Compass passou para `fixed` com 14.590,9 = R$ 20,43 × 714,19 mi ações (100%), mantendo a participação de 76,18%. O efeito é −R$ 223 mi de NAV, ou −R$ 0,057 por ação. A justificativa foi registrada em `sotp.notes`.

A revisão da RAIL3 (custo da dívida e IR) mudou o justo da Rumo em −R$ 0,001 (Rumo 100%: 9.072 → 9.069). É imaterial aqui.

## Conferências que bateram
- **Ações:** 3.944,4 mi em circulação (CVM 30/06 = B3).
- **DL da holding:** 9.919 + 2.621 + 3.871 + 74 − 7.268 = 9.217, mais o TRS de 3.014 = **12.231**. Bate.
- **Custo de holding:** 180 ÷ (25% − 5%) = 900, coerente com o G&A de 42 no 2T26.
- **Participação na Rumo:** 30%, coerente com a equivalência do 2T26 (156 ÷ 516 = 30,2%). O TRS entra como dívida e as ações sob TRS dentro dos 30%, sem dupla contagem se o TRS estiver contabilizado como financiamento (ver "não verificado").
- **Prefs da Cosan Dez:** valor contábil de 3.871, não o resgate de 4.019. É correto se o contábil for o valor presente do resgate.
- **Raízen = 0:** coerente. A participação de 44% de ~R$ 3,6 bi vale menos que as prefs do Itaú na Cosan Nove (R$ 2.660 mi).

## Achados menores (sem alteração)

| # | Severidade | Achado | Impacto no justo |
|---|---|---|---|
| 2 | baixa | O desconto de 20% sobre o laudo da Radar também incide sobre os R$ 586 mi que entram em caixa até 30/10. A venda de 12% por R$ 1,85 bi implica 85% do laudo para os 100% | Com 85% do laudo nos 88% restantes + 586 em caixa: **+R$ 0,075** |
| 3 | baixa | DL da holding de 30/06: há ~4 meses de carrego negativo até hoje (ICSD 0,2x; juros líquidos de 2.186 contra dividendos de 961 no LTM) | ~−R$ 0,4 bi, ou **−R$ 0,10** (depende de dividendos recebidos no 2S26) |
| 4 | baixa | Método inconsistente entre componentes: Rumo a valor justo (Ke 25%), Compass a mercado e Moove a ~6x lucro/4–5x EBITDA | Se a Compass também fosse a Ke 25%, o SOTP cairia (Compass −30% → **R$ 1,26**). A assimetria favorece o valor |
| 5 | baixa | Textos desatualizados ("R$ ~2,7–2,8", "desconto ~25%", "R$ 2,13–2,2") | Foto de hoje: R$ 2,97, desconto de 16,7%, justo de R$ 2,10. Cosmético |

## Sensibilidade (justo por ação; preço R$ 2,97)

| Cenário | Justo |
|---|---|
| Base revisada | 2,10 |
| Rumo a mercado (R$ 15,27) | 3,57 |
| Rumo a Ke 15% (R$ 8,69) | 2,64 |
| Rumo a Ke 12% (R$ 12,07) | 3,12 |
| Compass −30% | 1,26 |
| Moove a R$ 2,2 bi (3x EBITDA − DL) | 1,78 |
| Radar a 85% do laudo + caixa | 2,18 |
| Carrego negativo até hoje | 2,00 |

A conclusão (SOTP abaixo do preço a Ke 25%) depende de valorizar a Rumo a Ke 25%:
- Com a Rumo a mercado, o justo vai a R$ 3,57, acima do preço.
- A Ke de ~12% para a Rumo, o justo empata com o preço.

A "sobrerreação relativa" do dossiê (ação −43% contra NAV a mercado ~−24%) é real. Mas, no critério do estudo, não vira oportunidade.

## O que não deu para verificar
- Se as ~160 mi de ações da Rumo sob TRS (≈ 3.014 ÷ ~R$ 19, ou ~8,5% da Rumo) estão dentro ou fora dos 30% de equivalência. Se estiverem fora, a participação econômica seria ~38,5% e o justo subiria ~R$ 0,20.
- Se as prefs da Cosan Nove têm recurso contra a Cosan S.A.
- Valor da Moove (sem transação nem preço). O LTM foi inferido de 6M26/6M25; o 2T26 tem EBITDA de 475, possivelmente inflado pela crise de lubrificantes.
- Caixa da holding e dividendos recebidos após 30/06.
