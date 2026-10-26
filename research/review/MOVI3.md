# MOVI3 — revisão independente (red team) · 26/10/2026

**Veredito: ok, sem alterações.** Não achei erro objetivo. A dívida líquida econômica, a contagem de ações, o PL ajustado, a base do custo da dívida e os múltiplos-alvo são coerentes entre si e com a CVM.

O valor, porém, é frágil. O lucro de 2027–30 depende de duas premissas favoráveis: margem EBITDA no recorde e CDI caindo para ~13% até 2030 (a curva de hoje está em ~16%). Isso afeta sobretudo a TIR de 3 anos (39,6%), que não resiste a nenhuma das duas sensibilidades. A conclusão do estudo (valor justo < preço; TIR implícita < 25%) é robusta.

Preço da foto do estudo: R$ 8,67. Valores atuais (inalterados):
- Valor justo R$ 4,19 (DCF −0,39, que conta como 0 na média; DDM 5,80; múltiplos 10,98).
- TIR implícita 19,6%; TIR 3a 39,6%.
- Ke 20% → R$ 8,71; Ke 15% → R$ 16,31.

## Achados

### 1. CDI implícito no custo da dívida fica bem abaixo da curva de hoje (severidade média, não alterado)
- O custo da DL econômica usado é 17,1 / 17,5 / 17,0 / 16,5 / 16,0%. Pela regra "CDI + ~3 p.p." do próprio arquivo, isso equivale a CDI de 14,1 / 14,5 / 14,0 / 13,5 / 13,0%.
- Os forwards de hoje (DI1F28 14,95%, DI1F29 15,36%, DI1F31 15,66%) dão ~15,2% em 2027, ~15,9% em 2028 e ~16,0% em 2029–30. A diferença chega a 3 p.p. em 2030, e ~90% da dívida é pós-fixada.
- O spread de ~3 p.p. bate com o histórico: resultado financeiro LTM de −R$ 3.159 mi sobre DL econômica média de ~R$ 18,4 bi = 17,2%, com CDI de ~14,6%, ou seja, CDI + ~2,6 p.p.
- Sensibilidade com custo de 17,1 / 18,2 / 18,9 / 19,0 / 19,0%:
  - LL 2027–30: 703 / 876 / 1.066 / 1.271 → 603 / 590 / 651 / 730.
  - ROE de 2030: 19,0% → 12,4%.
  - Valor justo R$ 4,19 → 3,44; TIR implícita 19,6% → 14,5%; **TIR 3a 39,6% → 11,3%**.
- Não alterei porque a trajetória "curva do meio" (custo caindo até 2030 a partir do pico de 2027–28) é a convenção de praticamente todas as 53 premissas industriais do estudo. Mudar só aqui quebraria a comparabilidade. Recomendo ao líder decidir de forma global e, no mínimo, mostrar a TIR 3a também com os forwards.

### 2. Margem EBITDA no recorde por todo o horizonte (severidade média, não alterado)
- O modelo usa 43,5% em 2026 (o que implica 43,9% no 2S26) e 44% em 2027–30. O histórico CVM é 38,8% em 2025, 41,6% no LTM, 43,1% no 1S26 e 44,8% no 2T26 (recorde).
- A margem EBIT implícita de 26% fica acima de todo o histórico, exceto o 2T26 (27,0%): 22,2% em 2025, 24,3% no LTM e 25,6% no 1S26.
- O 2T26 foi ajudado pelo mix: seminovos caíram 18% a/a. A desmobilização prevista para depois de julho tende a devolver parte disso.
- A tendência de alta de tarifa (RAC +6,8%, GTF +11,5% a/a) sustenta parte da margem, então a premissa é otimista, não incoerente.
- Sensibilidade com margem de 43,0% em 2027–30: LL 2027 de 703 → 580; valor justo R$ 4,19 → 3,60; TIR implícita 19,6% → 18,0%; TIR 3a 39,6% → 29,1%.
- Com 42,5%: valor justo R$ 3,28; TIR implícita 17,0%; TIR 3a 23,3%. A alavancagem operacional e financeira faz −1,5 p.p. de margem custar −26% do lucro.

### 3. ROE terminal de 16% fica entre duas bases inconsistentes (severidade baixa, não alterado)
- Com os parâmetros terminais do próprio DCF (ROIC_T 12,5%, Kd 16,5% pré-IR, IR 25%), o ROE implícito seria ~12,9%.
- Com o ano de 2030 projetado (ROIC 13,7%, Kd 16%), o ROE seria ~18,5%.
- Com ROE_T de 14%, o valor justo cai só R$ 0,06, então é imaterial.

### 4. Itens verificados e coerentes
- **DL-base de R$ 19.150 mi:**
  - Base CVM: R$ 16.320 mi (dívida bruta 23.800 − caixa 7.479, que inclui CLN de R$ 4,0 bi espelhado na dívida) + derivativos passivos 1.220 + cessão de recebíveis 1.562 − aumento de capital de set/26 152 = R$ 18.950 mi.
  - Base da companhia: 17.221 + arrendamentos 756 + 1.562 − 152 = R$ 19.387 mi.
  - O ponto médio é razoável: ±R$ 120 mi ≈ ±R$ 0,28 por ação na perna de múltiplos. Fornecedores-montadoras (~R$ 5,0 bi) tratados como capital de giro, como em RENT3.
- **Ações:** 423,97 mi (B3 425,09 − tesouraria 1,12), contra 423,90 mi no hist. A CVM ainda mostra 401,04 mi. **PL:** 3.902 + 152 = R$ 4.054 mi. Coerentes com o aumento de set/26 (22,93 mi ações a R$ 6,65).
- **Crescimento:** +4% em 2026 (o 1S26 fez +4,1% e o 2S26 implícito é +3,9%) e 5–6% depois. O CAGR de 5 anos (29%) inclui aquisições.
- **D&A:** 17,8–18%, contra 17,3% no LTM e 17,8% no 2T26.
- **Capex líquido:** 24–25% contra D&A de 18% leva a imobilizado +4,5–5% a.a., coerente com receita +5–6%. Em 2026 (15%), o motor aplica 50,4% do ano ao 2S26 (R$ 1,15 bi, abaixo do D&A de R$ 1,37 bi), o que é coerente com o guidance de frota média de 2026 ≤ 2025. Como o DCF é negativo, o efeito no valor justo é nulo.
- **IR:** 22–25%, contra 22,2% efetivos no 1S26.
- **Payout:** 25% (mínimo estatutário). Com ele, a DL/EBITDA cai de 2,82x para 2,45x.
- **Stub do 2S26:** resultado financeiro de 0,504 × R$ 3.275 mi = R$ 1.650 mi, contra 2 × R$ 846 mi do 2T26. LL do stub de R$ 255 mi, contra ~R$ 285 mi do guidance do 3T26 + tendência.
- **Múltiplos-alvo:**
  - P/L 6,5x e EV/EBITDA 3,3x sobre 2027E, consistentes entre si: 3,3 × 7.117 − DL 2026E de 18.744 implica P/L de 6,75x.
  - A justificativa ("abaixo do pré-choque") é verdadeira: em 23/10 eram 11,3x e 3,8x; hoje são 5,2x e 3,21x; em 12/08, 4,15x e 3,10x.
  - Atenção: com a alavancagem de ~5x DL/valor de mercado, cada 0,1x de EV/EBITDA vale ~R$ 1,7 por ação na perna EV/EBITDA, ou ~R$ 0,2 no valor justo final.
- **Terminal:** g 5%, ROIC_T 12,5% contra WACC 16,5%. O EV fica ≈ DL e o DCF ≈ 0. É consequência estrutural de Ke 25% com Kd de 16,5%, não erro.

## Robustez da conclusão
- O valor justo fica abaixo do preço com Ke ≥ 20%. Só com Ke ≈ 20% o valor justo encosta no preço da foto (R$ 8,71 contra R$ 8,67).
- A TIR implícita fica entre 14,5% (forwards) e 19,6% (base), sempre abaixo de 25%.
- A TIR 3a "acima da meta" depende ao mesmo tempo de margem ≥ 43%, CDI caindo e P/L de saída de 6,5x. Não deve ser lida como sinal de oportunidade.

## Não verificado
- Não reli o release nem o ITR. A dívida, o CLN, os derivativos, a cessão e a exposição ao CDI (R$ 14,0 bi) foram tomados do dossiê.
- O limite de covenant não é divulgado (dossiê).
- O 3T26 sai amanhã (27/10). O guidance de R$ 130–150 mi é consistente com o stub do modelo.
