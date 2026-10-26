# IGTI11 — revisão independente (red team) · 26/10/2026

**Veredito: ok, sem alteração.** A contagem econômica da unit (`shares_per_unit` 4,0638) está correta, e a DL e os ajustes conferem. Não há erro objetivo. Os pontos em aberto (capex, custo financeiro, "demais obrigações") puxam o valor um pouco para baixo, mas não mudam a conclusão. Em todos os testes, o valor justo fica entre R$ 12,8 e 13,6 por unit, contra preço de R$ 25,45, e a TIR implícita entre 11,8% e 12,7%.

Preço da foto do estudo: R$ 25,45/unit. Valor justo R$ 13,60 (DCF 9,45 · DDM 9,01 · múltiplos 26,51). TIR implícita 12,7%; TIR 3a 19,4%.

## Unit e `shares_per_unit` = 4,0638 (conferido)
- A unit tem 1 ON + 2 PN, mas cada PN recebe 3× o provento da ON. Logo, 1 unit = 7 ON-equivalentes.
- **Unidades-equivalentes**: (ON 769,40 + 3 × PN 435,17)/7 = 296,7 mi; tirando ~0,3 mi em tesouraria, **296,4 mi**.
- **Ações por unit** = 1.204,57 mi ações CVM / 296,41 mi = **4,0638**.
- Três checagens independentes com dados B3 confirmam:
  - 2025: proventos pagos de R$ 199,74 mi (DFC) ÷ R$ 0,6752/unit (0,1685 + 0,5067) = **295,8 mi units**.
  - 2026: 4 parcelas de R$ 0,1685–0,1690/unit × 296,4 mi = R$ 50 mi cada, igual ao anúncio de R$ 200 mi.
  - Market cap do motor: 25,45/4,0638 × 1.204,57 = R$ 7.544 mi = 25,45 × 296,4.
- Com 3 ações por unit, a contagem errada sugerida pelo hist, o justo cairia para R$ 10,04 (−26%) e a TIR 3a para 3,5%.

## O que conferi (ok)
- **DL.** R$ 2.138,6 mi = dívida R$ 4.436,7 mi − caixa e aplicações R$ 2.298,1 mi (CVM 30/06, igual ao release). Não há arrendamentos nem dívida em "outras obrigações" (o "Financiamento por arrendamento" de R$ 931,6 mi em 2024 é debênture mal rotulada e já está na dívida bruta). Minoritários: R$ 0,2 mi.
- **`other_debt_like` R$ 100 mi.** Parcelas dc 15/07 (paga em 29/07) e dc 15/10 (paga em 29/10). É o próprio saldo de "Dividendos a pagar" de R$ 101,4 mi em 30/06. O stub de 2026 é 0, correto, porque os proventos de 2027 serão anunciados em ~dez/26.
- **Margem.** 74,5% em 2026E, coerente com a sazonalidade: 1S26 recorrente de 72,9% (1T26 sem o ganho de ~R$ 141 mi do XPML11: 72,0%; 2T26: 73,8%) e 2S25 de 75,3%. O caminho até 76% em 2029–30 é otimismo modesto.
- **Receita.** O stub do 2S26 (R$ 783 mi) é igual ao 2S25 (R$ 781 mi), já com as vendas de fatias ao XPML11. É conservador.
- **IR** de 15%, igual ao efetivo de 2023–25 (14–15%). **D&A** de 9%, igual ao LTM (9,4%).
- **Múltiplos.** Mesma regra (+300 bp) e base recorrente:
  - P/L 18x → 12x;
  - EV/EBITDA 9,9x (10,0x com os R$ 100 mi) → 7,6–7,7x; 8,0x usado ("prêmio de qualidade").
- **WACC.** `wd` 0,18, igual ao mercado pré-eleição (18,3%).

## Achados (nenhum altera a conclusão; não alterados)
1. **Capex 22% → 14% da receita pode ser baixo (média, não verificável).**
   - O pipeline não captura o capex da Iguatemi entre 2022 e 2025 (campo nulo). Na DFC bruta, "Aquisições de ativo não circulante" foi R$ 340 mi em 2024 (27,5% da receita) e R$ 305 mi no 1S26; tirando os R$ 75,6 mi da compra do Pátio Paulista, sobra ~31% orgânico. Entre 2016 e 2021, a média ficou em ~21%.
   - Não há explicação no dossiê para a queda a 14%.
   - Com 30% → 18%: justo 12,88; TIR 12,4%; TIR 3a 16,9%.
2. **Custo da DL (baixa).**
   - O efetivo do 1S26 foi ~16,8% da DL (≈1,15–1,2× o CDI, porque a dívida bruta é 2× a DL). Com os forwards de hoje (CDI de 15,2–16%), o mesmo fator daria ~18–19%; usado: 16–17%.
   - Com 16,8 / 18,2 / 19,0 / 19,2 / 19,2%: justo 13,40; TIR 12,4%.
3. **"Demais obrigações" de R$ 346 mi fora da ponte (baixa, não verificável).**
   - O saldo (2.01.05.02.09 + 2.02.02.02.13) saltou de R$ 45 mi (2023) para R$ 440 mi (2024), na época das compras de participações; pode ser preço de aquisição a pagar.
   - Em sentido contrário, há R$ 269 mi de "Outras contas a receber" (parcelas de vendas de ativos), também fora da ponte.
   - Tratando os dois: justo 13,44. Só a obrigação: 12,87.
4. **Proventos de 2027E de R$ 292 mi (45% do LL), contra R$ 200 mi fixos em 2024–26 (julgamento).** A empresa pode preferir recompras com a unit a 0,4x NAV. O efeito no DDM é pequeno.
5. **ROIC/ROE terminais de 25%, contra 14,9% contábeis em 2030E (julgamento).** O PL foi inflado pela reestruturação de 2021. Com 15%: justo 12,77; TIR 11,8%.
6. **Proventos declarados (R$ 100 mi) ficam no ajuste estático e não entram na DL projetada.** O efeito é imaterial (justo 13,48; TIR 12,6% se levados à DL).

## Não verificado
- Capex orgânico de 2025–26 e composição de "demais obrigações" (sem release/notas).
- Classificação das cotas de XPML11 recebidas (R$ 191,7 mi): provavelmente em aplicações financeiras, portanto já dentro do caixa e da DL. Se estiverem fora, o justo sobe ~R$ 0,4.
- NOI LTM exato (a tese usa o 2T26 anualizado).
