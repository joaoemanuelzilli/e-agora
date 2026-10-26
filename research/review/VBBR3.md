# VBBR3 (Vibra): revisão independente

**Veredito: ajustada.** Corrigi dois erros objetivos, ambos para baixo:
- **Dupla contagem no stub de 2026:** a janela de crise do 1S26 era contada de novo no 2S26.
- **Passivos debt-like omitidos:** previdência/saúde e desmantelamento não estavam descontados.

| | Antes | Depois |
|---|---|---|
| Valor justo | R$ 8,47 | **R$ 6,81** |
| Upside vs. preço de R$ 32,30 | −73,8% | −78,9% |
| TIR implícita | 10,3% | **10,0%** |
| TIR 3 anos | −15,5% | **−17,5%** |

Original em `research/review/VBBR3.orig.json`.

## Achados

| # | Severidade | Achado | Evidência | Impacto isolado |
|---|---|---|---|---|
| 1 | **alta (erro objetivo: período/dupla contagem)** | A margem de 2026 (5,2%) é a média do ano: 1S26 real mais 2S26 a 3,5%. Mas o motor usa **f26 × coluna 2026** para o stub do 2S26, e o balanço-base de 30/06 já embute o caixa do 1S26 (a DL caiu de 19.569 para 16.142) | 1S26 CVM: EBITDA 7.143 sobre receita de 105.303 (6,8%). A premissa dá 10.618 ≈ 7.143 + 3,5% × 98.898. O stub ficava em 0,504 × 10.618 = **5.351** de EBITDA no 2S26, contra os ~3.461 pretendidos. Isso significa ~R$ 1,9 bi de EBITDA (~1,4 bi após IR) contados duas vezes no FCFF e na DL de 2026 | Justo de 8,47 para 7,53 |
| 2 | média (erro objetivo: debt-like omitido) | A DL e `other_debt_like` não incluem o passivo de **plano de pensão e saúde** (Petros/AMS, 1.238) nem a **provisão para desmantelamento** (861, nova no 2T26) | BPP 2T26, contas 2.02.04.02.04 e 2.02.04.02.05. São saídas de caixa futuras fora do EBITDA. Usei o valor após IR: (1.238 + 861) × 0,66 = **1.385** | Justo de 8,47 para 7,75 |
| 3 | baixa | O custo da DL (14,5% → 12%) não segue a curva DI (CDI a termo de 15,2–16%): é conservador em 2026–27 e otimista em 2029–30 | 1S26: −1.211 × 2 ÷ DL média de 18.373 = 13,2% com CDI de ~14,5% (0,91× CDI). Com 0,91× a curva, a trajetória seria 12,5 / 13,7 / 14,1 / 14,1 / 14,1% | Neutro: justo +0,01. **Não alterei** |
| 4 | baixa | ROE_T de 20% contra ROE projetado de 9–12% | O payout terminal implícito é 77,5%. Fica acima da própria projeção, que tem a base de ativos da Comerc | Não alterei. É uma escolha de RONIC; vale o mesmo comentário feito para RAIL3/MOTV3 |
| 5 | info | Derivativos passivos de 5,5 bi fora da DL | Surgiram em dez/25 junto com +6,2 bi em "outros ativos" (energia da Comerc). A contrapartida provável é ativa, mas não foi confirmada | Se o líquido for passivo, o justo cai mais |
| 6 | info | Textos desatualizados ("~R$ 8–9 vs R$ 31") | Hoje o justo é R$ 6,81 e o preço R$ 32,30 | Cosmético |

## Mudanças em `research/VBBR3.json`

| Premissa | Antes | Depois | Motivo |
|---|---|---|---|
| `revenue_growth` 2026 / 2027 | +8,0% / −4,0% | **+4,61% / −0,89%** | Coluna 2026 = 2 × 98.898 (o próprio 2S26 implícito na premissa original). A receita de 2027 fica igual à original (196.031) |
| `ebitda_margin` 2026 | 5,2% | **3,5%** | É a margem do próprio dossiê para o 2S26. 2027–30 seguem em 3,4% |
| `payout` 2026 | 35% | **73,6%** | Sobre o lucro anualizado do 2S26 (2.454), mantém o dividendo do stub em ~R$ 910 mi (~R$ 0,76/ação, JCP do 4T26), igual ao original |
| `other_debt_like` | 2.365 | **3.750** | + 1.385 de pensão/saúde e desmantelamento, após IR |

| Resultado | Antes | Depois |
|---|---|---|
| DDM | 8,63 | 8,27 |
| DCF | 4,17 | 1,78 |
| P/L × LPA 2027 | 14,80 | 13,97 |
| EV/EBITDA | 19,01 | 16,82 |
| DL fim de 2026 | 14.768 | 16.001 |
| Lucro 2027 | 2.361 | 2.229 |
| Bear / bull | 4,19 / 14,05 | 3,73 / 12,35 |
| Monte Carlo p10–p90 | 3,59–14,94 | 3,15–13,22 |
| P(valor > preço) | 0% | 0% |

**Efeito colateral de exibição:** a coluna "2026E" do app passa a mostrar o 2S26 anualizado (EBITDA 6.923; lucro 2.454; DL/EBITDA 2,3x). Isso fica abaixo do exercício contábil, que deve fechar perto de ~10,6 bi de EBITDA e ~5,2 bi de lucro. Está explicado em `overrides.notes`. É a forma de cumprir a convenção do motor (fluxos de 2026E × fração após o balanço-base) quando o 1S e o 2S diferem muito.

## Sensibilidade (premissas novas)

| Cenário | Justo | TIR implícita | TIR 3 anos |
|---|---|---|---|
| Base | 6,81 | 10,0% | −17,5% |
| Margem 2027–30 de 4,0% em vez de 3,4% (crise mais longa ou formalização) | 10,82 | 11,8% | −5,0% |
| Ke 15% | 15,0 | — | — |
| Ke 12% | 21,2 | — | — |

A conclusão (preço muito acima do valor a Ke 25%) independe dos achados. O preço de R$ 32,30 só se justifica com margem de crise persistente e Ke bem abaixo de 12%.

## O que não deu para verificar
- O release oficial do 2T26.
- A margem real do 3T26: a normalização para 3,5% no 2S26 é do analista e é a premissa mais sensível.
- A natureza dos derivativos de 5,5 bi e da reclassificação de ~7 bi de "tributos diferidos" para "outros ativos não circulantes" no 1S26.
- O valor do JCP do 4T26.
- O prazo e os covenants da dívida.
