# Revisão independente — B3SA3 (B3) · 26/10/2026

**Veredito: ok.** Não encontrei erro objetivo. As premissas são coerentes com o histórico da CVM. A conclusão (não é oportunidade com Ke de 25%) se mantém em todas as sensibilidades razoáveis. Não alterei nada.

Preço de referência (foto B3, 13h02): R$ 15,10 (−36%; sexta R$ 23,65).

| | Valor |
|---|---|
| Valor justo | R$ 7,65 (DCF 5,90 · DDM 5,56 · múltiplos 13,23) |
| TIR implícita | 11,4% |
| TIR 3 anos | 7,7% |
| P/L 2027E ao preço | 14,1x |
| Monte Carlo p10–p90 | 6,73–8,63 (P(valor > preço) = 0%) |

## Checagens contra o histórico CVM (ok)
- **Receita bruta × líquida.** A conta 3.01 da B3 é a receita bruta: R$ 11.121,5 mi em 2025, com PIS/Cofins/ISS em 3.02. As margens foram corretamente expressas sobre a bruta.
  - Margem EBITDA (EBIT + D&A) sobre a bruta: 71,7% (2021) → 65,6 / 63,9 / 62,6 / 63,2% (2022–25).
  - LTM 2T26: 63,6% com o ganho da Dimensa e 62,5% sem ele.
  - Premissas de 63% → 61% → 62,5%: coerentes.
- **Receita 2026E +12%.** O 1S26 cresceu +16,3% (6.283 vs 5.403, calculado a partir de FY25 + 1S26 − LTM). Logo, a premissa implica 2S26 +7,9% a/a — conservadora para um semestre que inclui o 3T pré-eleição e volumes de pânico no 4T.
  - A margem 2S26 implícita é de 61,4%, contra 62,9% recorrente no 2T26.
  - 2027 a 0% repete 2022–23 (−1,7% e −1,9% com Selic de 13,75%).
- **D&A e capex.** D&A de 3,1–3,2% da receita vs 2025 de 3,5% (a amortização do PPA da Cetip acabou em 2024). Capex de 2,7–3,0% vs CVM 1,0–1,3% (só imobilizado; o release cita R$ 112 mi no 1S26). Levemente conservador.
- **IR.** 25% em 2026 implica 2S26 a 27,4% (o 1S26 foi de 22,8%, com o benefício do JCP extraordinário). De 2027 em diante, 30% (= 37% estatutário − escudo do JCP), igual ao efetivo LTM de 30,3%. Usar 27% em 2026 muda o valor justo em −R$ 0,01.
- **Resultado financeiro.** 9% sobre o caixa líquido CVM (R$ 4,4 bi) dá +R$ 397 mi, contra +R$ 408 mi LTM. ok.
- **Payout de 90–100% com recompras.** Histórico de (proventos + recompras)/lucro: 100% (2023), 128% (2024), 97% (2025). Como o número de ações fica constante no denominador, o DPS equivale ao "yield total". Coerente.
- **Ajustes debt-like de R$ 3.761 mi.**
  - Garantias recebidas em dinheiro (R$ 2.654,7 mi): correto. O caixa correspondente está nas aplicações que entram na DL da CVM.
  - JCP de 18/06 (R$ 1.106 mi): já ex-direito, então é correto deduzir no DCF. Também não há dupla contagem no EV/EBITDA, porque a DL de 2026E do motor não inclui esse pagamento.
- **Ações.** 4.998,3 mi (CVM 30/06 = total B3, sem cancelamento posterior). ok.
- **ROE.** Contábil projetado de 28–33% vs LTM 29,5% e 2025 25,6%. É inflado em relação ao capital tangível (o ágio de R$ 25,5 bi está dentro do PL), mas é coerente com o histórico.

## Achados
1. **(média — conservadora; não alterei) Explícito × perpetuidade.**
   - No período explícito, capex ≈ D&A: o reinvestimento líquido é ~0 com crescimento de 4–6% a.a.
   - Na perpetuidade, ROIC_T = ROE_T = 30% força reinvestir g/ROIC = 16,7% do lucro.
   - Com 50% (reinvestimento quase nulo, como no explícito): valor justo 7,65 → 7,79 (+2%) e TIR implícita 11,4% → 11,8%.
   - Não alterei: o efeito é pequeno e vai na direção conservadora, e 30% é próximo do ROE contábil projetado.
2. **(média — julgamento) Múltiplos-alvo no p10 de 5 anos.**
   - Histórico de 5 anos: P/L LTM com mediana 15,9x e p10 13,7x; EV/EBITDA com mediana 9,7x e p10 8,1x.
   - Os alvos de 12,5x e 8,5x são defensáveis pelo regime de juros: no fim de 2024, com DI de ~15%, a ação estava a 12,6x.
   - Na mediana, o valor justo iria a 8,33 e a TIR 3 anos de 7,7% para 19,4%. A TIR 3 anos é a métrica mais sensível ao múltiplo de saída; a TIR implícita não muda.
3. **(baixa — motor) Início do stub de 2026.** O stub começa na data-base (30/06), não em 26/10. O DDM conta proventos de jul–out que o comprador de hoje não recebe (~1–2% do valor). É sistêmico do motor e não dá para corrigir via premissas.
4. **(baixa — texto) Narrativa desatualizada.**
   - `summary`, `election_impact`, `thesis` e a nota citam R$ 12,93 (11h55), "−45%", "~12x P/L 2027E", "DY ~8%" e "TIR 12,1% / 12,9%".
   - Na foto final (R$ 15,10), os números são: −36%, P/L 2027E 14,1x, DY 2027E 6,7%, TIR implícita 11,4% e TIR 3 anos 7,7%.
   - Não editei porque não é premissa. O líder deve atualizar.

## Sensibilidade (em memória, sem gravar)
| Teste | Valor justo | TIR implícita | TIR 3a |
|---|---|---|---|
| Base | 7,65 | 11,4% | 7,7% |
| ROIC_T = ROE_T = 50% | 7,79 | 11,8% | 7,7% |
| Múltiplos na mediana de 5 anos (15,9x / 9,7x) | 8,33 | 11,4% | 19,4% |
| Receita 2027 +4% (em vez de 0%) | 7,96 | 11,7% | 10,2% |
| wd = 0 (WACC 25%) | 7,47 | 11,4% | 7,7% |
| Combinado otimista (3 primeiros testes) | 8,81 | 12,1% | 22,1% |
| Bear operacional (2027 −4%, margem 59–61%) | 6,97 | 10,7% | 2,7% |

Mesmo no combinado otimista, o valor justo fica em ~58% do preço e a TIR implícita em ~12%. **A conclusão é robusta.**

## Não verificado
- Guidance formal de 2026 (despesas, capex, payout).
- Recursos próprios da B3 alocados às câmaras: seriam um possível ajuste debt-like adicional, que reduziria o valor.
- Volumes de out/26 (boletins mensais).
- Status regulatório de nova bolsa/clearing.
- % pós-fixado da dívida.
