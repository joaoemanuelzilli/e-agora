# Revisão independente — DIRR3 (Direcional) · 26/10/2026

**Veredito: ajustada.** Encontrei um erro objetivo. O valor dos minoritários (R$ 1,0 bi) não seguia a regra da própria nota (21% do equity 100%). Corrigido para R$ 1,2 bi, o valor justo cai de R$ 9,08 para **R$ 8,84, abaixo do preço de R$ 8,97**. A TIR de dono não muda (21,4%) e segue abaixo do Ke de 25%. Para o ranking, isso significa que não há margem de segurança em nenhuma das duas métricas. Se a ação permanecer entre as oportunidades, deve ser explicitamente como caso de carry (DY de 7–14%), não de desconto.

| | Valor justo | TIR implícita | TIR 3 anos | P(valor > preço) | Bear / bull |
|---|---|---|---|---|---|
| Analista (preço R$ 8,97, foto 13h02) | R$ 9,08 | 21,4% | 30,3% | 52% | 6,94 / 10,34 |
| Após revisão | **R$ 8,84** | **21,4%** | **30,3%** | 46% | 6,70 / 10,10 |

## O que conferi e está coerente

**Ações.** São 520,0 mi: 520,5 mi emitidas, depois do desdobramento de 1:3 em 08/08/2025, menos 0,5 mi em tesouraria.

**DL CVM de R$ 291 mi.** É a dívida bruta de 3.041,4, que já inclui arrendamentos de 85,3 nas linhas 2.01.04.03/2.02.01.03, menos caixa e aplicações de 2.750,1. A diferença para a DL da companhia (R$ 492 mi) se explica assim: 3.041,4 − 85,3 − (2.750,1 − 295,9) = 501,9. Ou seja, a companhia exclui os arrendamentos e as aplicações de LP (ver achado 3).

**`other_debt_like` de 16.** Corresponde aos dividendos propostos no balanço (16,4). Não há provento declarado depois de 30/06 (B3).

**Juros capitalizados (+2,8 p.p.).**
- A medida bate com o 2T26: EBITDA de 311,5 contra 348 ajustado, ou 2,85% da ROL.
- É neutro no LL. O resultado financeiro de 2026E na base CVM fica em −2, contra −7 no 1S26 e +34 no LTM.

**WACC.** O Kd de 0,227 equivale a 15% sem escudo fiscal (RET). Com peso de dívida de 10%, o WACC fica em 24,0%. Coerente com CDI de ~15% mais spread.

**IR e minoritários.**
- IR de 9,5% sobre o LAIR, o que dá 2,2% da ROL; o histórico foi 2,2–2,3%.
- Minoritários de 21% do LL: 21,5% no LTM e 20,7% no 1S26.

**Crescimento.**
- 2026: os +17% implicam um 2S26 com +10,6% a/a, depois de um 1S26 com +24,8%.
- A margem CVM vai de 25,5% para 24%, contra 26,1% no 1S26 e média de 5 anos de 22,2%.

**Capital de giro de 0,65.** O CG operacional que calculei foi de 0,92x (2023), 0,83x, 0,87x e 0,85x (2T26). Isso inclui os terrenos a pagar por permuta (R$ 5,8 bi) como passivo.
- Marginal 2023→2T26: 0,78x bruto e 0,34x líquido de cessões.
- Marginal 2024→2T26: 0,89x e 0,51x.
- O meio-termo de 0,65 confere com o dossiê.

**Perpetuidade.**
- ROE terminal de 30%, igual ao ROE de 2030E do modelo.
- ROIC terminal de 25%. A intensidade de capital do próprio modelo implica ~36%, então a hipótese é conservadora.

## Achados

| # | Sev. | Achado | Evidência | Efeito (valor justo / TIR) |
|---|---|---|---|---|
| 1 | **média · corrigido** | Minoritários subavaliados | A nota define `minority_value` como "≈21% do LL × equity 100%". O equity 100% do próprio DCF é EV 6.015 − DL 291 − 16 = 5.708, e 21% disso dá 1.199. O valor de 1.000 equivalia a 17,5%. Também é compatível com a referência da Riva: 5% a R$ 151 mi implicam ~R$ 3,0 bi para 100% | R$ 9,08 → R$ 8,84; TIR inalterada |
| 2 | média (método, mantido) | Passivo de cessão de R$ 1.264 mi fora da DL | O tratamento como par casado com os recebíveis pró-soluto cedidos, que ficam no capital de giro, é defensável, e a nota é transparente. Requer que a cessão seja rolada (o saldo foi de 187 em 2023 para 694, 1.197 e 1.264) e que o custo ≈ o rendimento da carteira | Como dívida: R$ 7,32 (−17%) |
| 3 | média (mantido) | Aplicações de LP de R$ 296 mi tratadas como caixa | A companhia as exclui da DL. Elas crescem junto com as cessões (0 → 100 → 230 → 296), o que sugere fundo de reserva ou cota subordinada, ou seja, caixa não livre | Se restritas: R$ 8,48 (−4%) |
| 4 | média (risco) | Receita de 2027 (+10%) exposta ao 3T26 fraco | Vendas líquidas de R$ 1,3 bi, 21% abaixo da Genial, com 8 de 10 lançamentos depois de 15/09. A Riva (média renda) é sensível ao DI | 2027 +4%: R$ 8,32 / 20,3%. Margem caindo à média de 5 anos: R$ 8,18 / 20,2% |
| 5 | baixa (conservador) | Payout de 60–65% em 2027–30, abaixo do FCFE/LL do próprio modelo (65–75%); a recompra aprovada (32 mi ações, 6%) não está no payout, como pede a spec | O caixa líquido chega a R$ 473 mi em 2030 | Payout de 75–80% → R$ 8,92 / 22,0% |
| 6 | baixa (conservador) | Kd cai de 14,5% para 12,5% contra DI1F29–F31 de 15,4–15,7% | A DL é pequena | Kd plano → +R$ 0,003 |
| 7 | info | "Passivos com partes relacionadas" de R$ 213 mi (CP) fora da DL | Natureza não verificada: podem ser mútuos de sócios de SPEs | Como dívida: −R$ 0,26 |

**Leitura:** mesmo somando os achados conservadores (5 e 6), a TIR fica em ~22%. Nenhuma combinação plausível leva a TIR a 25%. O valor justo oscila entre R$ 8,2 e 9,3 nos testes razoáveis, em torno do preço.

## Mudanças em `research/DIRR3.json` (original em `research/review/DIRR3.orig.json`)
- **`adjustments.minority_value`:** 1.000 → 1.200, com nota explicativa.
- **Efeito:**
  - valor justo de R$ 9,08 para R$ 8,84 (−2,6%);
  - TIR implícita (21,4%) e TIR em 3 anos (30,3%) inalteradas, porque são baseadas no LL do controlador;
  - Monte Carlo de 52% para 46%.
- O motor foi re-rodado (`EAGORA_SNAPSHOT=1`).

## O que não deu para verificar
- Natureza das aplicações de LP (R$ 296 mi) e das obrigações com partes relacionadas (R$ 213 mi).
- Custo das cessões contra rendimento do pró-soluto.
- Participação exata da Riza na Riva.
- Execução da recompra.
- Detalhamento da Riva no 3T26.
- Custo médio e prazo da dívida (R$ 3,0 bi).
