# VAMO3 — revisão independente (red team) · 26/10/2026

**Veredito: ok, sem alterações.** Não achei erro objetivo com efeito material. A DL econômica, as ações, o crescimento e a margem ancorados no guidance, o D&A, o IR e o payout batem com a CVM e com o dossiê.

A conclusão (armadilha pela meta de 25%) é robusta. O valor justo fica abaixo do preço até com Ke de 20%, e a TIR implícita fica em 12,8–15,3%. Assim como em MOVI3, a TIR de 3 anos (20,6%) depende do CDI cair até 2030.

Preço da foto do estudo: R$ 2,90. Valores atuais (inalterados):
- Valor justo R$ 0,96 (DCF −0,29, que conta como 0 na média; DDM 1,27; múltiplos 2,55).
- TIR implícita 15,3%; TIR 3a 20,6%.
- Ke 20% → R$ 1,89; Ke 15% → R$ 3,62.

## Achados

### 1. Custo da dívida assume CDI em queda até 2030 (severidade média, não alterado)
- O custo usado é 17,2 / 17,5 / 17,1 / 16,7 / 16,3%. Ele bate com o histórico recente: 0,504 × R$ 2.179 mi para o stub, contra o resultado financeiro de −R$ 547 mi/tri no 2T26 e de −R$ 2.243 mi no LTM.
- Com ~70% da dívida pós-fixada, os forwards de hoje (CDI ~15,2% em 2027, ~15,9% em 2028 e ~16,0% em 2029–30) somariam +0,5 / +1,3 / +1,6 / +1,9 p.p. ao custo de 2027–30.
- Efeito dessa sensibilidade:
  - LL 2027–30: 472 / 584 / 706 / 835 → 423 / 450 / 523 / 599.
  - Valor justo R$ 0,96 → 0,84; TIR implícita 15,3% → 12,8%; **TIR 3a 20,6% → 5,1%**.
- Não alterei porque é a convenção de "curva do meio" do estudo inteiro (ver MOVI3.md). Recomendo ao líder decidir de forma global.

### 2. Justificativa dos múltiplos-alvo não fecha internamente (severidade baixa, imaterial, não alterado)
- O texto diz que EV/EBITDA de 3,8x "implica P/L ~7–8x". Na verdade, 3,8 × EBITDA 2027E de 4.161 − DL 2026E de 12.881 = R$ 2.931 mi, o que dá P/L de **6,2x** sobre o LL de R$ 472 mi.
- Com o P/L de 7x, o EV/EBITDA equivalente é 3,89x.
- Uniformizar em qualquer das duas pontas move o valor justo em ±R$ 0,04.
- Os níveis estão ancorados corretamente no piso pré-rali e no preço de hoje. Na mesma base de 2027E:

  | Data | P/L 2027E | EV/EBITDA 2027E |
  |---|---|---|
  | 12/08 | 7,19x | 3,86x |
  | Hoje (R$ 2,90) | 7,5x | 3,90x |
  | 23/10 | 16,6x | 4,93x |

  Logo, os alvos ficam levemente abaixo da tela. Não há o erro de base visto em RENT3.

### 3. ROE terminal de 14% fica entre duas bases (severidade baixa, não alterado)
- Com os parâmetros terminais do DCF (ROIC_T 12%, Kd 16,5% pré-IR, IR 25%), o ROE implícito é ~11,0%, porque o spread contra a dívida é negativo.
- Com o ano de 2030 projetado (ROIC 13,3%, Kd 16,3%), seria ~16,1%.
- Com ROE_T de 12,5%, o valor justo vai a R$ 0,94 e a TIR implícita a 14,8%.

### 4. Itens verificados e coerentes
- **DL-base de R$ 12.666 mi:** DL CVM de R$ 11.271 mi (dívida bruta 15.678 com arrendamentos de direito de uso de R$ 84 mi, menos caixa de 4.407) + derivativos líquidos de 375 + cessão de 912 + aquisições a pagar de 109.
  - Cessão conferida nas linhas CVM 2.01.05.02.04 (487) e 2.02.04.02.04 (425).
  - Derivativos coerentes com a DL de covenant de R$ 11.561 mi, que exclui arrendamentos.
- **Ações:** 1.221,74 mi, já com os 155,8 mi do aumento de mai/26 a R$ 3,85, que está no balanço do 2T26 (PL de 2.605 → 3.298).
- **2026E:**
  - Receita +10,9%: o 1S26 fez +16%, e o 2S26 implícito é +6,2% a/a, ou +2,3% acima de 2× o 2T26.
  - Margem de 60,7% = EBITDA de R$ 3.875 mi, ponto médio do guidance de R$ 3,75–4,0 bi. O 2S26 implícito (R$ 1.952 mi) bate com 2× o 2T26 (R$ 1.944 mi).
- **2027–30:** margem de 61,5%, contra 62,1% no 2T26 e 60,9% no LTM. A margem EBIT implícita de 42,5% compara com 43,2% no 2T26, 41,8% no 1S26 e 42,7% no LTM. D&A de 19%, contra 18,9% no 2T26.
- **Capex líquido de 29–30% × D&A de 19%:** leva o imobilizado a +4,5–5% a.a. Com giro de 2,5x (imobilizado/receita), crescer 5,5% exige ~32% de capex, então os 30% são coerentes com receita +5–6%.
  - Divergência a notar: a CVM mostra (Δimobilizado + D&A) de só 14,5% da receita no LTM (imobilizado de 16.042 → 15.813). Já o release cita "implantado R$ 2,02 bi − valor contábil vendido R$ 0,81 bi" no 1S26, ou 38% da receita.
  - Não consegui reconciliar a diferença (~R$ 0,8 bi) só com a CVM: não há "ativos não correntes a venda", e os estoques são de R$ 107 mi.
  - Se o investimento líquido real for menor, a DL cresce menos. Isso é viés conservador, mas aí o crescimento de 5–6% também fica menos sustentado.
- **IR:** 22–25%, contra 22,8% no 1S26 e 24% em 2025. **Payout:** 25% (mínimo). Com ele, a DL/EBITDA econômica cai de 3,32x para 2,88x; o covenant (≤ 3,75x, na métrica da companhia) é atendido.
- **Terminal:** ROIC_T de 12% contra WACC de 16,5%, o que dá EV de R$ 12,3 bi < DL. Resultado estrutural de Ke 25% com Kd de 16,5%, não erro.

## Robustez da conclusão
- O valor justo fica abaixo do preço em todo o grid de Ke ≥ 20%. Só com Ke de ~17% ele iguala a tela.
- A TIR implícita fica entre 12,8% (forwards) e 15,3% (base).
- A TIR 3a de 20,6% já está abaixo da meta na base e cai para ~5% com os forwards.

## Não verificado
- Não reli o release nem a DF.
- A sensibilidade ao CDI (~70% pós-fixado) é estimativa do dossiê; a nota do ITR não fecha com a DL.
- O cronograma de amortização está em imagem.
- O histórico CVM até 2024 inclui as concessionárias (pré-cisão para a Automob) e não serve para médias de 5 anos.
- A data do 3T26 não está confirmada.
