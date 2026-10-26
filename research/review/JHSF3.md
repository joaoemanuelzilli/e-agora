# Revisão independente — JHSF3 (JHSF Participações) · 26/10/2026

**Veredito: problema grave, corrigido. A conclusão ("não serve para Ke de 25%") se mantém e fica mais forte. Os números mudam muito.**

Encontrei três erros objetivos, todos verificados no ITR 2T26 (PDF da companhia, 103 páginas):

1. **Receita normalizada de 2026 ~50% acima do que a companhia gera sem o JCDI11.** O estoque que gerava a receita "normal" de 2025 foi vendido ao FII, e seu valor já entra pelos adjustments. Isso é dupla contagem.
2. **Cotas subordinadas do JCDI11 somadas duas vezes:** já estão no caixa CVM.
3. **Arrendamentos IFRS-16 e um terreno a pagar remunerado pelo CDI fora da dívida.** Os dois estavam escondidos em "débitos diversos".

| (preço R$ 11,24, foto 13h02) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 4,83 (−57%) | **R$ 1,70 (−85%)** |
| TIR implícita | 12,3% | **9,0%** |
| TIR 3 anos (saída a 7x P/L) | 2,1% | −24,7% |
| DCF / DDM / P/L / EV-EBITDA | 3,10 / 4,01 / 8,76 / 9,42 | −0,85 (entra como 0) / 2,15 / 5,15 / 4,17 |
| Receita / EBITDA 2026E | 2.376 / 1.105 | 1.601 / 744 |
| Lucro 2027E | 829 | 487 |
| Cenários bear / base / bull | 3,49 / 4,83 / 5,93 | 1,24 / 1,70 / 2,04 |

## Achados

### 1. Grave: receita-base inclui o fluxo do estoque vendido ao FII (corrigido)
**A premissa do analista.** Normalizou 2025 em R$ 1.980 mi, supondo ~R$ 1,5 bi de receita do JCDI11 no 4T25 e ~R$ 0,4 bi no 2T26, e projetou +20% para 2026 (R$ 2.376 mi).

**O que diz o ITR:**
- A nota 1.1.2 mostra R$ 2.467,7 mi de receita da tranche 1 já reconhecida em 30/06/2026. Só no 1S26 houve R$ 693,7 mi de transferências para reconhecimento direto (lotes do Boa Vista Estates).
- A receita LTM sem o JCDI11 é, portanto, 4.053 − 2.468 = **R$ 1.585 mi**.
- Pela nota 18, a venda de imóveis do 1S26 foi R$ 874,1 mi. Tirando o JCDI11, sobram ~R$ 0,07–0,18 bi para clientes finais, contra R$ 350 mi no 1S25.
- As demais receitas brutas somaram R$ 700,5 mi (+10,5% a/a).

O estoque que gerava a receita normal (Boa Vista Village/Estates, Reserva CJ, Surf Club, Santa Helena) agora é do FII. Seu valor entra no modelo pelo caixa recebido, pela tranche 2 e pelo custo a incorrer. Projetar esse fluxo de novo contava o mesmo estoque duas vezes.

Para fechar o 2026E de R$ 2.376 mi, o 2S26 sem JCDI11 precisaria render ~R$ 1,65 bi, contra ~R$ 0,73 bi no 1S26.

**Checagem de lucro.** EBITDA ajustado LTM de 2.153 menos o EBITDA do JCDI11 (2.468 × 57–62%) dá ~R$ 620–740 mi. Depois de R$ 352 mi de resultado financeiro, sobra lucro LTM sem JCDI11 de ~R$ 150–250 mi. O modelo corrigido dá R$ 307 mi em 2026E e R$ 487 mi em 2027E, ou seja, não é punitivo.

**Correção:**
- Base de 1.585 (LTM sem JCDI11) e 2026E de +1% (R$ 1.601 mi).
- Margens e crescimento de 2027–30 do analista foram mantidos.
- Capex e D&A em % foram recalculados para preservar os mesmos R$ absolutos do analista (capex de 618 → 508; D&A de 71 → 118), porque o plano de investimento não depende do estoque vendido.

Isolado, o efeito é de R$ 4,83 → 2,09 no valor justo e de 12,3% → 9,0% na TIR.

O retorno incremental do capex fica coerente com o ROIC terminal de 12% do analista: ~13% antes de IR, contra 19,6% implícitos na versão original.

### 2. Alta: cotas subordinadas do JCDI11 em dupla contagem (corrigido)
- A nota 4 lista "JHSF Capital Desenvolvimento Imobiliário – FII 907.218" dentro de "títulos e valores mobiliários". O total da nota (4.392,4) é exatamente o caixa CVM usado na DL.
- O analista somou mais 50% (R$ 454 mi) em `non_operating_assets`.

**Correção:** `non_operating_assets` de 2.090 → 1.636. As cotas ficam a 100% via DL porque o TRS com empresa do controlador (notas 1.1 e 14) fixa ao CDI o retorno da "parte majoritária" das cotas. Ganho de R$ 26 mi no 1S26.

Efeito: −R$ 0,43.

Se quiser manter o haircut de 50% do analista (ignorando o TRS), seriam mais −R$ 0,08 no valor (DCF já ≤ 0).

### 3. Média: dívida fora da DL (corrigido)
A nota 13 ("débitos diversos") contém dois itens que pela spec são dívida:
- arrendamentos IFRS-16 de R$ 273,4 mi (lojas, restaurantes, hotéis);
- terreno de São Roque a pagar de R$ 137,4 mi, remunerado pelo CDI, com juros anuais e bullet em 10 anos.

O EBITDA ajustado é pré-aluguel, então o passivo de arrendamento entra na dívida. **Correção:** `other_debt_like` de 1.375 → 1.785,8. Efeito: −R$ 0,39 na versão original.

O resto de "débitos diversos" é operacional: obrigações sociais e tributárias de 371, além de fundo de reserva e receita diferida. Os +R$ 537 mi na linha LP da CVM são, sobretudo, R$ 368 mi de adiantamentos de clientes reclassificados para o LP.

### 4. Info: pontos mantidos
- **DCF negativo.** Na versão corrigida, EV de R$ 1,86 bi menos DL e ajustes dá equity DCF de −R$ 0,85/ação, que o blend trunca em 0. A conta de um negócio que reinveste ~R$ 600 mi/ano a ~12% com WACC de 22% é essa. Quem aceita retorno de ativo real ou reciclagem via FIIs a cap rate de mercado chega a outro número, fora do mandato de Ke 25% (o NAV do BBI era de R$ 19,6).
- **Escudo fiscal de 34% (wd 20%, Kd 15%).** Regimes mistos (lucro real nas operações maiores, RET/presumido na incorporação). Sem escudo, o DCF cai mais, mas o valor justo não muda, porque o DCF já é ≤ 0.
- **Custo a incorrer de R$ 1,2 bi (BBI).** É coerente com a nota 28: R$ 1.424 mi a incorrer em unidades vendidas e em estoque, dos quais ~R$ 1,15 bi atribuíveis ao JCDI11.
- **Tranche 2 (R$ 1.744 mi, até 31/12/26).** É condicionada à "formalização do instrumento de venda definitivo e cumprimento da obrigação de performance". Há risco de execução.
- **Outros fundos.** As cotas de outros fundos da JHSF Capital/Fasano (Sardenha 131, Mayfair 107, Northern Trust 209, Malls FII 92 etc.) já estão no caixa CVM a valor contábil. Não são "fora/conservador", como dizia a nota do analista, e parte é ilíquida (desenvolvimento de hotéis).

## Sensibilidades (sobre a versão corrigida)
| Variação | Valor justo | TIR |
|---|---|---|
| Base de 1.650 (se a receita do JCDI na nota 1.1.2 for bruta de RET) | R$ 1,99 | 9,7% |
| Crescimento de 13/12/10/9% em 2027–30 (relançamento da incorporação) | R$ 1,79 | 9,4% |
| Margem +3 p.p. | R$ 1,88 | 9,4% |
| Capex em % original (capex absoluto menor) | R$ 1,87 | 9,6% |
| ROIC/ROE terminais de 15%/16% | R$ 1,73 | 9,3% |

Faixa de R$ 1,6–2,0 e TIR de 9–10%. Nenhuma variação chega perto do preço.

## Mudanças em `research/JHSF3.json` (original em `research/review/JHSF3.orig.json`)
| Campo | Antes | Depois |
|---|---|---|
| `overrides.base.revenue_2025` | 1.980 | 1.585 |
| `projection.revenue_growth` | [0,20; 0,10; 0,10; 0,09; 0,08] | [0,01; 0,10; 0,10; 0,09; 0,08] |
| `projection.capex_pct_revenue` | [0,26; 0,23; 0,20; 0,17; 0,15] | [0,3859; 0,3414; 0,2968; 0,2523; 0,2226] (mesmos R$) |
| `projection.da_pct_revenue` | [0,03; 0,032; 0,034; 0,035; 0,035] | [0,0445; 0,0475; 0,0505; 0,0519; 0,0519] (mesmos R$) |
| `adjustments.non_operating_assets` | 2.090 | 1.636 |
| `adjustments.other_debt_like` | 1.375 | 1.785,8 |

O motor foi re-rodado e `data/model/JHSF3.json` foi atualizado. `data/app` não foi regenerado.

## O que não deu para verificar
- Receita do JCDI11 reconhecida por trimestre (4T25, 1T26, 2T26) e se os valores da nota 1.1.2 são brutos ou líquidos de RET.
- Lançamentos novos fora do FII previstos para 2027+.
- Termos do TRS (fração coberta, prazo, garantias da contraparte).
- Composição de "obrigações sociais e tributárias" (R$ 371 mi), que pode incluir parcelamentos.
