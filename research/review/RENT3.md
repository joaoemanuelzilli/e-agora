# RENT3 — revisão independente (red team) · 26/10/2026

**Veredito: ajustada.** Corrigi um erro objetivo nos múltiplos-alvo. As premissas operacionais (crescimento, margens, capex/D&A, IR, payout, dívida) são coerentes com o histórico CVM. A conclusão do estudo (armadilha pela meta de 25%) se mantém e fica mais nítida: a TIR implícita é 14,7% e a TIR de 3 anos, que antes passava da meta, agora fica abaixo dela.

Preço da foto do estudo: R$ 31,73.

| | Antes | Depois |
|---|---|---|
| Valor justo | R$ 17,50 | **R$ 15,89** (−9%) |
| Múltiplos (perna de 25%) | R$ 40,71 | R$ 34,26 |
| DCF / DDM | R$ 7,02 / 15,26 | inalterados |
| TIR implícita | 14,7% | 14,7% (inalterada, pois vem do DDM) |
| TIR 3 anos (saída a P/L-alvo × LPA 2029E) | 32,2% | **23,3%** |
| Cenários bear / bull / esperado | 10,14 / 22,32 / — | 8,83 / 20,53 / 14,70 |
| Monte Carlo p10–p90 · P(valor > preço) | 10,35–25,96 · 1,9% | 9,02–24,04 · 1,0% |

## Achados

### 1. Múltiplos-alvo comparavam bases diferentes (severidade média, erro objetivo, corrigido)
- A justificativa original dizia: "Alvo 10x 2027E = desconto ao piso recente". Os "~11x / ~13x / ~17x" citados, porém, são P/L sobre o **lucro ajustado de 2025** (LPA R$ 3,10), enquanto o alvo é aplicado ao **LPA de 2027E** (R$ 4,03, 30% maior).
- Na mesma base de 2027E, o P/L foi 8,45x em 12/08 (R$ 34,10), 10,3x em 30/06 (R$ 41,54) e 13,0x em 23/10 (R$ 52,42). Hoje está em 7,9x. Logo, 10x não era desconto ao piso: era o nível de 30/06, cerca de 18% acima do piso de agosto.
- O EV/EBITDA-alvo de 4,7x tinha o mesmo problema: equivale ao nível de 30/06 (4,74x), contra 4,25x em 12/08 e 4,09x hoje.
- Mudança: P/L 10,0x → **8,5x** e EV/EBITDA 4,7x → **4,25x**. É o próprio piso de agosto na base certa, ou seja, a correção mínima, que ainda nem aplica o desconto que a justificativa pretendia. Os dois alvos são consistentes entre si: 8,5 × LL 2027E de R$ 4.455 mi + DL 2026E de R$ 33.593 mi ≈ 4,25 × EBITDA 2027E de R$ 16.805 mi.
- Impacto: valor justo −R$ 1,61 e TIR 3a −8,9 p.p. A TIR 3a depende só do múltiplo de saída: antes, o preço de saída em 2028 era R$ 50,23, contra R$ 42,69 agora.

### 2. Custo da dívida de 2029–30 abaixo da curva de hoje (severidade baixa, não alterado)
- O custo da DL usado é 13,8 / 14,3 / 14,3 / 14,0 / 13,7%. Os forwards implícitos de hoje (DI1F28 14,95%, DI1F29 15,36%, DI1F31 15,66%) dão CDI de ~15,2% em 2027, ~15,9% em 2028 e ~16,0% em 2029–30.
- Para 2026–28 o custo usado é coerente. No LTM, o custo efetivo da DL foi 13,9% (resultado financeiro −R$ 4.665 mi sobre DL média de ~R$ 33,6 bi) com CDI de ~14,5–15%, porque 73% da DL está travada em 12,30% + spread. Nessa estrutura, o CDI forward de 15,2% leva a ~14,0–14,5% em 2027.
- Em 2029–30, porém, o vencimento dos swaps (2027–31) levaria o custo a ~15–16% na curva de hoje.
- Sensibilidade com custo de 13,8 / 14,5 / 14,7 / 15,0 / 15,3%: valor justo R$ 15,89 → 15,62, TIR implícita 14,7% → 14,0%, TIR 3a 23,3% → 20,3%.
- Não alterei porque é a escolha documentada de "curva do meio" (dossiê: LL 2027E de R$ 5,1 bi na curva pré-eleição, R$ 4,46 bi na base e R$ 4,19 bi nos forwards) e o WACC já usa Kd de 15%.

### 3. Margem EBITDA de 2026E um pouco otimista (severidade baixa, não alterado)
- Os 31,8% do ano implicam 31,6% no 2S26, contra 30,8% no 1S26 recorrente (sem o ganho de R$ 282 mi) e 30,5% no 2T26. A margem depende do mix: seminovos, com margem de ~2%, foram 58% da receita no 2T26.
- Com 31,2%, o valor justo cai só R$ 0,08, porque apenas o stub do 2S26 entra.

### 4. Itens verificados e coerentes
- **Crescimento:** +17,5% em 2026 (o 1S26 já fez +22,8%, o que implica +12,6% a/a no 2S26) e 5–7,5% a.a. depois. O orgânico de aluguel foi +8,4% em 2025 e +7,6% no 1S26. O CAGR de 5 anos (32%) não serve de referência por causa da fusão com a Locamerica.
- **Frota (capex líquido × D&A):** capex de 18,8–19,7% contra D&A de 12,2–12,4% da receita. Isso leva o imobilizado de R$ 56,4 bi para ~R$ 72,7 bi em 2030 (+6–7% a.a., em linha com a receita) e a receita/imobilizado de 0,82 para 0,87. No histórico, (Δimobilizado + D&A)/receita foi 21% (2024), 14% (2025) e 24% (LTM).
- **D&A:** o 3T25 (R$ 2.075 mi) inclui o IPI verde. A taxa recorrente é 11,3–11,6% (1T–2T26), e o modelo usa 11,9–12,4% com depreciação por carro em alta. Coerente.
- **Stub de 2026:** o motor aplica 50,4% do capex de 2026E ao 2S26 (R$ 3,7 bi), contra R$ 2,1 bi implícitos se os 15% forem o ano cheio menos os R$ 5,25 bi do 1S26. É conservador e ambíguo, por isso mantive.
- **IR:** 20–22%, contra 20,8% efetivos no 1S26. O JCP (~R$ 2,1–2,5 bi/ano) gera escudo de ~R$ 0,75 bi sobre LAIR de ~R$ 5,7 bi, o que dá ~20–21%. Coerente.
- **Payout:** 55%, contra 61% do lucro ajustado em 2025 e 52% no 1S26. Com ele, a DL/EBITDA cai de 2,15x para 1,9x. Sustentável.
- **DL-base:** R$ 33.753 mi = DL CVM de R$ 34.648 mi (dívida bruta 44.636 + arrendamentos 1.296 − caixa 11.284) − swaps ativos de R$ 895 mi (a dívida em moeda estrangeira está na bruta a valor de mercado). Coerente com a DL de R$ 32.352 mi da companhia.
- **Fornecedores-montadoras:** R$ 10,7 bi, tratados como capital de giro. É defensável, mas é um risco de caixa se o saldo normalizar.
- **Terminal:** ROIC_T de 14% (projetado 13,5% em 2030; a companhia reporta 15,6%) e ROE_T de 16% (projetado 16,7%; ROIC + (ROIC − Kd·(1−t))·D/E ≈ 16,4%). Ambos ficam abaixo do WACC (19,0%) e do Ke (25%), o que implica EV/EBITDA de saída de 2,4x. É a razão estrutural do valor baixo, não um erro.
- **Ações:** 1.104,6 mi em circulação (ON + PN RENT4 conversíveis 1:1). Coerente com a B3.

## Robustez da conclusão
- O valor justo fica abaixo do preço em todo o grid de Ke 20–30% × g 3–7% (de R$ 11,5 a R$ 22,3).
- Com Ke de 15% (no modelo corrigido), o valor justo é R$ 33,2 ≈ preço, ou seja, o mercado precifica ~15% a.a.
- O DCF reverso exige crescimento médio de 19,7% a.a. (base 8,7%).
- O veredito do dossiê se mantém.

## Não verificado / fora do escopo
- Não reli o ITR nem o release. Os números de dívida, swaps, sensibilidade a CDI e cronograma de amortização foram tomados do dossiê.
- A data de vencimento de cada swap também não foi conferida (ela é o que determina o custo em 2029–30).
- O 3T26 sai em 05/11; a depreciação por carro é a principal incerteza.
- **Bug de dados no app (não editado):** a série de múltiplos históricos de RENT3 antes de 3T23 usa a contagem de ações em milhares da CVM (por exemplo, P/L 0,05x e P/VP 0,003x em ago/23). Isso contamina as estatísticas `pe_all`/`pe_5y`/`pbv_5y` mostradas no app. Precisa de correção no pipeline de mercado/build.
- RENT4 não está na foto de preços. O valor de mercado usa o preço de RENT3 para todas as ações, o que é imaterial (conversão 1:1).
