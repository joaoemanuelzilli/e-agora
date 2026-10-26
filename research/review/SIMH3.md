# SIMH3 — revisão independente (red team) · 26/10/2026

**Veredito: ajustada.** O SOTP descartava o carrego negativo da holding com um argumento de sinal trocado. Corrigi incluindo o valor presente desse carrego na dívida líquida da holding.

A conclusão do dossiê (opção alavancada em queda de juros, não oportunidade pela meta de 25%) se mantém e fica mais forte. O SOTP também segue enviesado para cima por avaliar JSL e Automob a mercado (ver achado 2).

Preço da foto do estudo: R$ 6,87. O template holding não calcula TIR de dono.

| | Antes | Depois |
|---|---|---|
| DL da holding usada no SOTP | R$ 1.689 mi (1.389 + TRS 300) | **R$ 1.989 mi** (+ carrego 300) |
| NAV justo / NAV a mercado | R$ 4.428 / 6.915 mi | R$ 4.421 / 6.908 mi¹ |
| Valor justo (SOTP) | R$ 4,35 (upside −36,7%) | **R$ 3,82** (upside −44,3%) |
| Desconto do preço ao NAV a mercado | 20,2% | 15,0% |

¹ A diferença de −R$ 7 mi não vem da revisão. AMOB3 não está na foto de preços (`data/market/quotes.json`), então o motor busca a cotação ao vivo a cada rodada (R$ 10,54 às 13h03; ~R$ 10,3 na nova rodada). Isso responde por −R$ 0,01 por ação. O carrego responde por −R$ 0,51.

## Achados

### 1. Carrego negativo da holding descartado com sinal trocado (severidade alta, erro objetivo, corrigido)
- A holding tem dívida bruta de R$ 6.038 mi a 18,8% a.a. (inclui derivativos de hedge na curva de R$ 1.216 mi) e caixa de R$ 4.649 mi rendendo ~CDI.
- O spread é de ~4–4,3 p.p. sobre o caixa, ou ~R$ 190–200 mi por ano de despesa líquida além do que a DL de R$ 1.389 mi "pagaria" sozinha.
- O arquivo original dizia: "a 25% de Ke uma dívida a 18,8% vale abaixo da face — os dois efeitos se compensam".
- Isso só vale se a dívida for descontada a 25% e o caixa não. Descontado a 25%, o caixa (que rende ~CDI) também vale abaixo da face, e perde mais que a dívida. O efeito líquido aumenta o passivo econômico em vez de compensá-lo.
- Cálculo consistente com Ke de 25%, como bullet de 4 anos (o prazo médio da dívida):
  - Dívida: 6.038 × (0,188 × 2,362 + 0,410) = R$ 5.154 mi.
  - Caixa: 4.649 × (0,145 × 2,362 + 0,410) = R$ 3.496 mi.
  - DL econômica: R$ 1.658 mi, ou **+R$ 269 mi** sobre a face.
- Com consumo linear do caixa até meados de 2031 (meta da companhia), o acréscimo fica entre +R$ 272 e +340 mi. Com o carrego perpétuo, entre +R$ 362 e +548 mi.
- Mudança: `sotp.holding_net_debt_mn` de 1.689 → **1.989** (+R$ 300 mi, centro da faixa finita), com a nota corrigida em `adjustments.notes`.
- Impacto: −R$ 0,51 por ação (−12%).

### 2. SOTP mistura valor justo e valor de mercado (severidade média, limitação de método, não alterado)
- Movida e Vamos entram a valor justo (Ke 25%), que fica 52–67% abaixo da tela. JSL e Automob entram a mercado porque não têm modelo próprio.
- JSL sozinha responde por **R$ 1,99 por ação (52% do SOTP justo)**: 67,2% × 285,37 mi ações × R$ 6,05.
- Os fundamentos de JSL são parecidos com os das controladas que o modelo avalia muito abaixo da tela: LL LTM de −R$ 104 mi, DL de R$ 6,18 bi e EBITDA LTM de R$ 1,80 bi (DL/EBITDA 3,4x). A Ke de 25%, o valor justo de JSL provavelmente ficaria bem abaixo do mercado.
- Sensibilidade: JSL 30% abaixo da tela leva o SOTP de R$ 3,82 → 3,23.
- O viés é para cima, então a conclusão (valor justo < preço) fica ainda mais robusta.

### 3. Participação na Movida pode estar superestimada (severidade baixa, não alterado)
- Os 61,07% são de 30/06. Se a Simpar não subscreveu o aumento de set/26 (22,9 mi ações), a participação cai para ~57,8%.
- Impacto: −R$ 0,10 por ação (SOTP de R$ 3,72).
- O dossiê já sinaliza a dúvida, e não verifiquei a subscrição.

### 4. Estimativa do TRS (severidade baixa, não alterado)
- Da data de 30/06 até a foto, a cesta variou assim: SIMH3 7,80 → 6,87 (−12%), MOVI3 9,39 → 8,67 (−8%), VAMO3 2,81 → 2,90 (+3%), JSLG3 5,46 → 6,05 (+11%).
- A queda de "10–15%" da cesta só vale se ela for concentrada em SIMH3. A composição não é divulgada.
- Somando o carrego de ~R$ 31 mi (CDI + 3,63% sobre R$ 526 mi por 4 meses), a MTM provável fica entre −R$ 270 e −300 mi, contra os −300 usados. Diferença ≤ R$ 0,05 por ação.

### 5. Itens verificados e coerentes
- Ações: 583,76 mi (CVM = B3, após o grupamento 2:1 e a emissão de 156,96 mi ações em mai/26).
- Valores justos de 100% de Movida (R$ 4,19 × 423,97 mi) e Vamos (R$ 0,955 × 1.221,7 mi) vêm do motor e não mudaram nesta revisão (ver MOVI3.md e VAMO3.md).
- Automob a R$ ~10,5 × 37,886 mi ações (B3): ~R$ 0,4 bi.
- Não listados conservadores:
  - CS Infra ex-Aratu: R$ 750 mi de equity + DL de R$ 521 mi, ou EV/EBITDA de 8,4x UDM e 6,7x o 2T26 anualizado.
  - Aratu: equity sem earn-out.
  - CS Brasil e Outros: ao PL. BBC: 0,6x o PL.
- Custo de holding: R$ 40 mi × 5 = R$ 200 mi (administrativo da controladora de R$ 25,7 mi no 1S26).
- O TRS fora do balanço é somado à DL. A margem de R$ 183 mi em CDB fica no caixa, sem dupla contagem.

## Sensibilidades (SOTP pós-revisão de R$ 3,82)

| Hipótese | SOTP |
|---|---|
| Movida e Vamos com custo da dívida nos forwards de hoje (valores justos de R$ 3,44 e R$ 0,84) | R$ 3,35 |
| JSL −30% | R$ 3,23 |
| Participação na Movida de 57,8% | R$ 3,72 |
| TRS de −R$ 270 mi | R$ 3,87 |
| Controladas a Ke 20% (dossiê: ~R$ 7,3 antes da correção) | ~R$ 6,8 |

O preço de R$ 6,87 só é justificado com Ke de ~20% nas controladas, sem nenhum dos ajustes negativos.

## Não verificado / pendências para o líder
- Não reli as DFs da Simpar. A DL da holding, o custo de 18,8%, o TRS, as participações e a venda de Aratu foram tomados do dossiê.
- O yield do caixa da holding não foi conferido (usei ~CDI de 14,5%).
- **AMOB3 fora da foto de preços:** o valor da Automob muda a cada execução de `model.py`. Recomendo incluir AMOB3 em `data/market/quotes.json`.
- O dossiê (`research/notes/SIMH3.md`) ainda cita o SOTP de R$ 4,32. Não o editei por estar fora do escopo.
