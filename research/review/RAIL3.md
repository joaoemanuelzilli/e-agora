# RAIL3 (Rumo): revisão independente

**Veredito: ajustada.** Corrigi duas premissas incoerentes, que puxam em direções opostas:
- **Custo da dívida:** contrariava a curva DI de hoje.
- **IR:** a alíquota sobre lucro reportado era aplicada a um EBT ajustado.

O valor justo praticamente não muda: **R$ 4,89 → R$ 4,89** contra preço de R$ 15,27 (−68%). A TIR de dono cai: implícita **10,3% → 9,6%**; 3 anos **4,6% → −0,2%**.

Original salvo em `research/review/RAIL3.orig.json`.

## Conferências que bateram
- **DL-base 26.191** (CVM 30/06/2026): dívida 22.910 + arrendamentos/concessões 8.736 − caixa 5.456.
  - Os 8.736 se dividem em IFRS-16 de 4.469 e passivos em litígio/parcelados de 4.268 (Malha Oeste 2.976 · Paulista 867 · outras concessões 425).
  - O release diz 17.303 na definição "ampla", que exclui esses passivos. Coerente.
- **Ajustes do balanço:**
  - `other_debt_like` 481: derivativos 271 + dividendos de 2025 a pagar em 30/11/2026, que pertencem à base acionária de 28/04/2026.
  - Ativos não operacionais: TVM e caixa restrito somam 428.
  - Ações: 1.855,8 mi (B3 = CVM).
- **EBITDA ajustado:**
  - 2025: EBIT 4.579,7 + D&A 2.213,3 + impairment 1.227,9 = 8.021 (57,9%).
  - 1S26: ~57% (2T26: 2.267 sobre 3.940 = 57,5%).
  - Premissa 2026 de 56,5%: coerente. O capex inclui o investimento recorrente da Malha Sul, que é baixado a impairment, então não há dupla contagem.
- **Capex:**
  - 1S26: 3.371. O stub 2S26 é 0,504 × 6.001 = 3.024, coerente com o "2S26 abaixo do 1S26" do release.
  - 2027–28: R$ 4,9–5,0 bi, contra R$ 4,7 bi do Itaú BBA.
- **Minoritários:** 1,5%, em linha com 18/865 em 2025 e 8,5/617,5 no 1S26.
- **Múltiplo-alvo:** EV/EBITDA ajustado de 6,5x contra 6,7x hoje e 7,5x pré-eleição (54,7 bi ÷ 8.118 LTM). Coerente.

## Achados

| # | Severidade | Achado | Evidência |
|---|---|---|---|
| 1 | média | **Custo da DL abaixo da curva DI de hoje.** A trajetória 12 / 12,5 / 12 / 11,5 / 11% implica CDI de ~12,7% em 2030 | Dívida ~102% do CDI. Os termos da curva de hoje dão CDI de 15,2% (2027), 15,9% (2028) e 16,0% (2029–30): F28 14,95%, F29 15,36%, F31 15,66%. No 1S26 o custo foi −1.610,6 × 2 ÷ DL média de 25.491 = **12,6%**, com CDI de ~14,5%. Com estrutura (22,9 × 1,02 − 5,5) × CDI + 8,7 bi a ~10% − ~0,27 bi calibrado no 1S26, o CDI de 15,0% (2027) e 15,5% (2028–30) dá **12,6% e 12,9%** |
| 2 | média | **IR alto demais para o EBT ajustado.** 36 / 33 / 31 / 30 / 29% sobre um EBT que soma de volta o impairment da Malha Sul | Alíquota efetiva sobre o EBT ajustado: 21,5% (2023), 26,7% (2024), 24,8% (2025) e **29,5% (1S26: 398,9 ÷ (1.016,4 + 336,5))**. Os 36% misturavam bases |
| 3 | baixa | ROE_T de 18% contra ROE projetado de 11,7–14,8% | O payout terminal implícito é 75%. Com ROE_T = 14%, o justo cai para R$ 4,84 e a TIR para 9,2%. Não alterei: é uma escolha de RONIC, mas fica acima da própria projeção |
| 4 | baixa | 50% do passivo da Malha Oeste (1.488) entra como ativo | É julgamento (release: "sem expectativa de desembolso"; o 5º aditivo prevê compensação). Sem esse ajuste, o justo cai para R$ 4,79 |
| 5 | baixa | Novos arrendamentos e remensurações (~R$ 0,4 bi/ano) não estão modelados na DL | Os arrendamentos subiram 7.753 → 8.133 em 2025 com pagamentos de 828. O D&A inclui a amortização do direito de uso, mas o capex é só caixa. O efeito é pequeno: ~R$ 0,1 bi/ano de juros a mais em 2030 |
| 6 | info | O Kd do WACC (14,5%) fica abaixo do marginal (~15,8% = 102% de um CDI a termo de ~15,5%) | Não muda o justo, porque o DCF já é negativo e entra com zero |

## Mudanças em `research/RAIL3.json`

| Premissa | Antes | Depois |
|---|---|---|
| `cost_of_net_debt` | 12,0 / 12,5 / 12,0 / 11,5 / 11,0% | 12,0 / 12,6 / 12,9 / 12,9 / 12,9% |
| `tax_rate` | 36 / 33 / 31 / 30 / 29% | 29% fixo |

| Resultado | Antes | Depois |
|---|---|---|
| Valor justo | R$ 4,888 | R$ 4,887 |
| DDM | 3,86 | 3,45 |
| P/L-alvo × LPA 2027 | 13,87 | 14,62 |
| EV/EBITDA | 17,52 | 17,57 |
| DCF | −2,58 | −2,25 |
| TIR implícita | 10,3% | **9,6%** |
| TIR 3 anos | 4,6% | **−0,2%** (LPA 2029 cai 10%, de 1,30 para 1,17, com o juro maior) |
| Lucro 2027 / 2030 | 2.145 / 2.726 | 2.261 / 2.322 |
| Monte Carlo p10–p90 | 3,74–6,16 | 3,71–6,32 |
| P(valor > preço) | 0% | 0% |

A CSAN3 usa este valor justo. A mudança de −R$ 0,001/ação é imaterial para o SOTP.

## Sensibilidade (premissas novas)

| Cenário | Justo | TIR implícita | TIR 3 anos |
|---|---|---|---|
| Base | 4,89 | 9,6% | −0,2% |
| Custo da DL original | 5,02 | 10,4% | 5,8% |
| EV/EBITDA-alvo 7,5x (pré-eleição) | 5,50 | 9,6% | — |
| Ke 20% | 5,54 | — | — |
| Ke 15% | 8,69 | — | — |
| Ke 12% | 12,07 | — | — |

- A conclusão (preço muito acima do valor a Ke 25%; TIR abaixo de 25%) não depende de nenhuma das premissas revistas.
- Mesmo a Ke 12%, o justo fica abaixo do preço.

## O que não deu para verificar
- Ato formal de prorrogação da Malha Sul. O modelo assume saída no início de 2029. A saída em mar/2027 tiraria ~R$ 2 bi de receita, mas pouco FCF: margem de ~40% contra ~R$ 0,7 bi/ano de capex.
- Prazo do benefício SUDAM da Malha Norte (sustenta os 29%).
- Indexador e taxa dos passivos de arrendamento e concessão.
- Juros capitalizados da Ferrovia do MT após a entrega da 1ª fase.
