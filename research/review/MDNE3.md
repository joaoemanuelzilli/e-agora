# Revisão independente — MDNE3 (Moura Dubeux) · 26/10/2026

**Veredito: ajustada. A conclusão muda de "passa raspando" para "fica raspando abaixo" do hurdle.**

O modelo projetava geração de caixa no 2S26 que contradiz a prévia oficial do 3T26. Também aplicava escudo fiscal de 34% na dívida de uma empresa no presumido/RET. Corrigidos os dois pontos, o valor justo fica abaixo do preço e a TIR em 24,5%, contra Ke de 25%.

A tese do relatório ("única do grupo que supera o Ke") deixa de valer na base. Ainda está dentro do ruído, então a ação merece ser acompanhada, não chamada de oportunidade.

| (preço R$ 19,66, foto 13h02) | Antes | Depois |
|---|---|---|
| Valor justo | R$ 20,64 (+5,0%) | **R$ 18,40 (−6,4%)** |
| TIR implícita | 25,6% | **24,5%** |
| TIR 3 anos (saída a 5x P/L) | 42,2% | 38,2% |
| DCF / DDM / P/L / EV-EBITDA | 19,04 / 20,20 / 26,13 / 22,43 | 16,09 / 19,20 / 24,56 / 19,88 |
| P(valor > preço), Monte Carlo | 59,3% | 36,5% |
| Cenários bear / base / bull (esperado) | 16,23 / 20,64 / 23,61 (19,91) | 14,08 / 18,40 / 21,31 (17,69) |

## Achados

### 1. Alta: o caixa do 2S26 contradiz a prévia do 3T26 (corrigido)
**O que o motor projetava.** Fluxo pré-dividendos de +R$ 166,4 mi no 2S26, ou +R$ 83,2 mi por trimestre:
- EBITDA 665 − IR 84 + resultado financeiro 57 − capex 53 − ΔCG 255;
- vezes a fração do ano após o balanço-base, f26 = 0,504.

Isso levaria a DL de 56 para −16 no fim de 2026.

**O que a companhia reportou.** A prévia oficial de 08/10/2026 (p. 8), que conferi no PDF: "No 3T26, o consumo de caixa, excluindo dividendos e recompra de ações, foi de R$ 170 milhões". Sem os R$ 97 mi do terreno em Salvador, R$ 73 mi.

**O histórico recente vai na mesma direção:**
- 3T25: −65;
- 2T26: +27, só por causa da cessão de R$ 153 mi; sem ela, −126;
- CFO CVM no 1S26: −183.

O CG está crescendo bem acima de 0,9x a receita. Pelas minhas contas, o CG/receita foi de 0,90x (2024), 0,91x (2025) e 1,03x (LTM 2T26). O motivo é que o fee de terreno é reconhecido na constituição do condomínio e recebido ao longo da obra.

**Correção.** DL-base de 56,4 → 309,6, somando o desvio de −170 − 83,2 = −R$ 253,2 mi. O 4T26 continua como projetado (+R$ 83 mi), o que é generoso diante do histórico. A correção desloca a trajetória de DL e reduz o resultado financeiro em ~R$ 35 mi/ano antes de IR.

Impacto, isolado:
- valor justo de R$ 20,64 → 18,65;
- TIR de 25,6% → 24,5%.

Mesmo sem o terreno de Salvador (desvio de R$ 156 mi), o valor seria R$ 19,16 e a TIR 24,9%.

### 2. Média: escudo fiscal incoerente com o regime (corrigido)
O motor aplica (1 − 34%) ao Kd. A MD paga 12% sobre o LAIR (11,1% no 1S26; ~2,9% da receita), padrão de presumido/RET, regime em que os juros não reduzem o imposto.

Os pares do mesmo estudo (DIRR3, PLPL3, TEND3) já informam Kd/0,66. Aqui, `kd_pre_tax` passou de 0,15 para 0,2273, e o WACC de 23,5% para 24,0%.

Impacto isolado: valor justo −R$ 0,25. A TIR não muda.

### 3. Média: cessão de recebíveis fora da dívida (mantido, sensibilidade)
- Os R$ 146,9 mi ficam fora da DL, como a própria MD e os pares do estudo fazem. Os recebíveis cedidos, porém, seguem no ativo, o que indica risco retido.
- Como dívida, o valor cairia mais R$ 1,15, para R$ 17,25, e a TIR para 23,9%.

### 4. Média: ROE terminal de 20% acima do ciclo (mantido, sensibilidade)
- O ROE de 20% é igual ao do próprio modelo em 2027–30 (19,5–20%). Porém fica acima da média de 2021–25 (~15%) e depende da margem EBITDA CVM de ~21% (de 14,8% na média de 5 anos e 19,6% em 2025).
- Com ROE_T de 17,5% e ROIC de 16%: R$ 18,06 / 24,0%.

### 5. Baixa: outros itens (mantidos)
- IR de 12%: a média 2021–25 foi 14,7%. A 14% → R$ 17,92 / 24,0%.
- Kd na curva (14,5–15%): efeito desprezível, R$ 18,41.

### 6. Info: o que conferi e está coerente
- **Ações:** 103,71 mi (B3 × (1 − 0,48% de tesouraria)). O dividendo de R$ 4,16/ação × 84,5 mi pré-follow-on dá R$ 351,7 mi, que confere.
- **`other_debt_like` de 252:**
  - Bate com o balanço: "Dividendos a pagar" CP de 200,0 + LP de 51,7, rotulado "permutas"; no FY25 era 151,7, e a diferença é o pagamento de 100 no 1T26.
  - Bate também com as parcelas da B3: 2 × 0,5918 em 14/07/26 e 0,5918 + 0,5918 + 0,6116 em 2027.
  - O comprador de hoje não recebe essas parcelas. Não há dupla contagem com o "consumo ex-dividendos" do 3T26.
- **Juros capitalizados:** +1,7 p.p. contra 1,6 p.p. no release do 2T26.
- **`other_financial` de 65:** coerente com o resultado financeiro anualizado do 1S26 (112) menos juros capitalizados (45).
- **D&A e capex:** D&A de 0,7% e capex de 2,0%, iguais ao LTM.
- **Múltiplos-alvo:** P/L de 5,0x e EV/EBITDA de 4,5x, abaixo do p25 histórico (5,49x e 5,46x, conferidos em `data/market`).
- **Receita de 2026 com +12%:** exige um 2S26 de +2% a/a. É plausível, porque as adesões do 9M26 caíram só −1,9% (a queda de −43,5% é do 3T26).

**Sensibilidades combinadas sobre a versão corrigida:**
- margem 2027–30 −1,5 p.p. → R$ 16,94 / 23,3%;
- receita de 2027 −12% → R$ 17,75 / 23,7%;
- CG marginal de 1,05x → R$ 18,12 / 24,4%.

Para a TIR voltar a ≥ 25% seria preciso ROE ou margem acima da base. Os riscos documentados (adesões, distratos de 8,3%, consumo de caixa) apontam para o outro lado.

## Mudanças em `research/MDNE3.json` (original em `research/review/MDNE3.orig.json`)
| Campo | Antes | Depois | Efeito isolado no valor justo / TIR |
|---|---|---|---|
| `overrides.base.net_debt` | 56,4 | 309,6 | −1,99 / −1,1 p.p. |
| `wacc.kd_pre_tax` | 0,15 | 0,2273 | −0,25 / 0 |
| Conjunto | 20,64 / 25,6% | **18,40 / 24,5%** | |

O motor foi re-rodado (`EAGORA_SNAPSHOT=1 pipeline/model.py MDNE3`), e `data/model/MDNE3.json` foi atualizado. **`data/app/companies/MDNE3.json` e `research/reports/MDNE3.json` não foram regenerados**: continuam com R$ 20,64 / 25,6%. O relatório da oportunidade precisa ser revisto pelo líder.

## O que não deu para verificar
- Geração de caixa do 4T26 e resultado do 3T26 (sai em meados de novembro).
- Se a cessão tem coobrigação.
- Quanto do fee de terreno de 2027 já está contratado (adesões do 4T26).
- Prazo médio dos R$ 1,49 bi de recebíveis de terreno.
