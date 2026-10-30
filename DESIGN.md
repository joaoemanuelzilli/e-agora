---
name: E agora?
description: Nota de research de ações brasileiras pós-eleição; cada empresa é uma nota encabeçada pela caixa de recomendação.
colors:
  navy: "#0b2545"
  navy-2: "#163a68"
  on-navy: "#ffffff"
  on-navy-2: "#b9c6d8"
  rule: "#0b2545"
  accent: "#1d4f91"
  accent-soft: "rgba(29, 79, 145, 0.1)"
  page: "#ffffff"
  surface: "#ffffff"
  surface-2: "#f1f4f8"
  box: "#e9edf2"
  ink: "#101828"
  ink-2: "#3d4a5c"
  muted: "#5f6b7c"
  hairline: "#d5dce5"
  grid: "#e6eaf0"
  axis: "#b8c2cf"
  pos: "#1b7f4c"
  neg: "#b42318"
  buy: "#1b7f4c"
  buy-strong: "#126339"
  buy-soft: "#e6f2eb"
  wait: "#8a5a0b"
  wait-soft: "#fbf1df"
  wait-line: "#e2c68f"
  series-1: "#1f5fad"
  series-2: "#d9682b"
  series-3: "#1a9e77"
  fill-1: "#0b2545"
  proj: "#8fb2de"
  deemph: "#b9c1cc"
  div-neg: "#d9534f"
  div-mid: "#eef0f2"
typography:
  display:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "28px"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.018em"
  ticker:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  report-headline:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "34px"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.008em"
  title:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1.375
  title-sm:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.3
  figure:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.01em"
    fontFeature: "\"tnum\" 1, \"lnum\" 1"
  prose:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.68
  lead:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "14.5px"
    fontWeight: 400
    lineHeight: 1.625
  body:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"lnum\" 1"
  table:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.5
    fontFeature: "\"tnum\" 1, \"lnum\" 1"
  button:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.5
  label:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.5
  table-head:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.25
  rating-call:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.06em"
  chart-tick:
    fontFamily: "Libre Franklin, Helvetica Neue, Arial, sans-serif"
    fontSize: "11px"
    fontWeight: 400
    fontFeature: "\"tnum\" 1, \"lnum\" 1"
rounded:
  none: "0px"
  sm: "2px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "16px"
  xl: "20px"
  gutter: "24px"
  section: "32px"
  section-lg: "40px"
components:
  masthead:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.on-navy}"
    height: "56px"
    padding: "0 24px"
  masthead-nav-link:
    textColor: "{colors.on-navy-2}"
    typography: "{typography.button}"
    padding: "0 10px"
  masthead-nav-link-active:
    textColor: "{colors.on-navy}"
    typography: "{typography.button}"
  market-strip:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    padding: "6px 24px"
  button-primary:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.on-navy}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "7px 14px"
  button-primary-hover:
    backgroundColor: "{colors.navy-2}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "7px 14px"
  link:
    textColor: "{colors.accent}"
    typography: "{typography.button}"
  segmented-option:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-2}"
    typography: "{typography.button}"
    rounded: "{rounded.sm}"
    padding: "4px 12px"
  segmented-option-selected:
    backgroundColor: "{colors.navy}"
    textColor: "{colors.on-navy}"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "16px"
  panel-ruled:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.none}"
    padding: "20px"
  keybox:
    backgroundColor: "{colors.box}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "12px 16px 16px"
  exhibit:
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "10px 0 0"
  rating-call-strong:
    backgroundColor: "{colors.buy-strong}"
    textColor: "{colors.on-navy}"
    typography: "{typography.rating-call}"
    padding: "6px 10px"
  rating-call-buy:
    backgroundColor: "{colors.buy}"
    textColor: "{colors.on-navy}"
    typography: "{typography.rating-call}"
    padding: "6px 10px"
  rating-call-wait:
    backgroundColor: "{colors.wait-soft}"
    textColor: "{colors.wait}"
    typography: "{typography.rating-call}"
    padding: "6px 10px"
  rating-call-none:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.muted}"
    typography: "{typography.rating-call}"
    padding: "6px 10px"
  rating-cell:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "5px 10px"
  table-header:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.ink-2}"
    typography: "{typography.table-head}"
    padding: "7px 10px"
  table-cell:
    textColor: "{colors.ink}"
    typography: "{typography.table}"
    padding: "7px 10px"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "6px 12px"
  select:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: "4px 28px 4px 10px"
  tooltip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "8px 10px"
  footer:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.muted}"
    typography: "{typography.label}"
    padding: "24px"
---

# Design System: E agora?

## Overview

**Creative North Star: "A Nota de Research"**

O e-agora se apresenta como uma publicação de equity research de banco brasileiro, não como um painel de fintech. Cada empresa é uma nota encabeçada pela caixa de recomendação (COMPRA ou AGUARDAR, preço-teto, upside); o Painel é a nota de top picks do mês; Investir, Registro, Dividendos, Mercado, Metodologia e Testes são os anexos da mesma publicação. A barra marinho no topo é o cabeçalho do papel timbrado; abaixo dela tudo é papel branco, fios finos, quadros cinza-claros e números tabulares.

A densidade é a de uma nota impressa: tabelas com cabeçalho em faixa cinza, listas de dados-chave com rótulo à esquerda e valor à direita, gráficos tratados como "exibições" numeradas pela fonte embaixo. A hierarquia vem do peso e do fio marinho de 2px que abre cada seção, não de cartões, sombras ou cor de fundo. Uma família só (Libre Franklin) faz títulos, texto e números. A cor é quase toda neutra; marinho é o único cromado, verde e âmbar falam só da recomendação, verde e vermelho só da variação.

O mundo recusa explicitamente o painel de fintech em cartões brancos com azul e blocos de KPI. A confiança vem de mostrar o método e as fontes como no rodapé de um research (CVM, B3, Banco Central), não de decoração.

**Key Characteristics:**
- Barra marinho #0b2545 de 56px com a marca em texto ("E agora?" + "Research"), navegação, Ke segmentado e tema; faixa de mercado cinza logo abaixo.
- Papel branco, fios de 1px #d5dce5, quadros de dados-chave em cinza #e9edf2.
- Seções, exibições e quadros que abrem seção levam um fio marinho de 2px no topo; nada mais leva.
- A caixa de recomendação (carimbo + Preço-teto + Upside) é o elemento-assinatura e aparece em toda decisão de compra.
- Libre Franklin 400/500/600/700 em tudo, números tabulares e com sinal explícito, formato pt-BR.
- Plano: a única sombra do sistema é a do tooltip.
- Tema claro e escuro com a mesma estrutura; o escuro é marinho profundo, não preto.

## Colors

Paleta de papel e tinta com um único cromado marinho; verde e âmbar reservados à recomendação, verde e vermelho à variação, e três séries de gráfico validadas para os dois temas.

### Primary
- **Marinho de Cabeçalho** (`navy`): a barra do topo, o botão primário, a opção selecionada de todo controle segmentado, a seleção de texto e o preenchimento de barras de alocação (`fill-1`). É o único tom "de marca"; não existe gradiente nem segundo azul de chrome.
- **Marinho de Hover** (`navy-2`): só o hover do botão primário e de controles marinhos.
- **Fio Marinho** (`rule`): o fio de 2px que abre seções, exibições e quadros que abrem a própria seção, o fio de 1px no topo do cabeçalho de tabela e o topo do tooltip. No claro é igual a `navy`; no escuro clareia para #5b8fd1 para continuar visível.
- **Texto sobre Marinho** (`on-navy` / `on-navy-2`): branco para a marca, o link ativo e o texto de botões; azul-acinzentado #b9c6d8 para navegação ociosa, "Research", rótulo "Ke" e contagens dentro de opções selecionadas.

### Secondary
- **Azul de Link** (`accent`): links (`.link`, peso 600), hover do ticker, foco (`:focus-visible` 2px) e borda de input em foco. `accent-soft` (10% de opacidade) só como faixa de destaque dentro de gráficos. Nunca preenche botão nem barra.

### Tertiary
- **Verde de Compra** (`buy`, `buy-strong`, `buy-soft`): preenchimento do carimbo COMPRA (#1b7f4c) e COMPRA FORTE (#126339), com texto branco; `buy-soft` só em fundos de apoio à recomendação.
- **Âmbar de Espera** (`wait`, `wait-soft`, `wait-line`): o carimbo AGUARDAR é sempre suave: texto #8a5a0b sobre #fbf1df, borda #e2c68f.
- **Alta e Queda** (`pos` #1b7f4c / `neg` #b42318): cor de variações de preço e de retorno, sempre junto do sinal + ou −.
- **Séries de gráfico** (`series-1` azul #1f5fad, `series-2` laranja #d9682b, `series-3` verde #1a9e77): nessa ordem fixa, validadas pelo validador de paleta do dataviz contra #ffffff (claro) e #0f1c30 (escuro). `proj` (#8fb2de) para projeções e faixas de sensibilidade, `deemph` (#b9c1cc) para o universo não destacado, `div-neg`/`div-mid` para escalas divergentes (mapas de calor, calendário).

### Neutral
- **Papel** (`page`, `surface` #ffffff): fundo da página, dos painéis, das exibições e das células da caixa de recomendação.
- **Faixa Cinza** (`surface-2` #f1f4f8): faixa de mercado, cabeçalho de tabela, rodapé, hover de linha e de controles ociosos, carimbo "Sem teto".
- **Quadro de Dados** (`box` #e9edf2): o cinza da nota para dados-chave e para faixas de resumo (Investir, aviso de relatório).
- **Tinta** (`ink` #101828): texto principal e números decisivos. **Tinta Secundária** (`ink-2` #3d4a5c): texto de apoio, rótulos de linha, teses, linhas em AGUARDAR. **Cinza de Nota** (`muted` #5f6b7c): rótulos de 12px, notas, linhas de fonte.
- **Fio Fino** (`hairline` #d5dce5): bordas de painel, divisórias de lista, bordas de controles. **Grade** (`grid` #e6eaf0): linhas entre células de tabela e linhas de grade de gráfico. **Eixo** (`axis` #b8c2cf): eixos, barra de rolagem e a parte CDI da barra de alocação.

### Tema escuro

Mesmos nomes de token, redefinidos em `prefers-color-scheme: dark` e em `[data-theme="dark"]`:

| Token | Escuro | Nota |
|---|---|---|
| page / surface / surface-2 / box | #0a1424 / #0f1c30 / #13233b / #172a45 | escala de marinho, nunca preto |
| ink / ink-2 / muted | #e8edf5 / #b0bccd / #97a8c0 | |
| hairline / grid / axis | #24354f / #1b2b43 / #34465f | |
| navy / navy-2 / on-navy-2 | #0d2a4f / #173c6c / #a9b9cf | barra continua marinho |
| rule / fill-1 | #5b8fd1 / #4a8fe0 | o fio clareia para ser visto |
| accent | #7fb0ea | |
| pos / neg | #4cc38a / #f07a70 | |
| buy / buy-strong | #1e7a49 / #17663c | escuros o bastante para texto branco |
| wait / wait-soft / wait-line | #e7b45a / âmbar 12% / #7a5a22 | continua suave |
| series-1 / 2 / 3 | #4a8fe0 / #d66a30 / #20a27c | validadas contra #0f1c30 |
| proj / deemph | #24508c / #45546b | |

### Named Rules
**A Regra do Marinho Único.** O marinho é o único cromado: barra, botão primário, opção selecionada, seleção de texto. Nenhum outro azul preenche superfícies; o azul de link fica no texto e no foco.

**A Regra da Espera Mansa.** AGUARDAR é âmbar suave (texto `wait` sobre `wait-soft`, borda `wait-line`), nunca preenchido sólido e nunca vermelho. Esperar não é vender.

**A Regra do Sinal.** Cor nunca é o único sinal de alta ou queda: toda variação leva + ou − impresso; `pos`/`neg` apenas reforçam.

## Typography

**Display Font:** Libre Franklin (com Helvetica Neue, Arial, sans-serif)
**Body Font:** Libre Franklin
**Label/Mono Font:** nenhuma; números usam Libre Franklin com `tabular-nums lining-nums`

**Character:** Uma grotesca americana de jornal financeiro, carregada via `next/font` nos pesos 400, 500, 600 e 700 (com itálico). Títulos em 700 com tracking levemente negativo; o resto em 400–600. A voz é a de uma nota de banco: firme, compacta, sem display decorativo.

### Hierarchy
- **Report headline** (700, 34px → 28px → 24px conforme o comprimento, 1,12–1,22, −0,02em, máx. 40ch): a manchete da tese no relatório.
- **Ticker** (700, 32px, 1, −0,02em): o ticker no cabeçalho da empresa; o preço ao lado em 700/30px tabular.
- **Display** (700, 28px, 1,15, −0,018em): o título de cada página (`.h1`): "Top picks pós-eleição", "Investir", "Registro de recomendações".
- **Headline** (700, 18px, 1,25, −0,008em): títulos de seção (`.h2`), sempre logo abaixo do fio marinho.
- **Title** (700, 15px, ~1,375): título de exibição (gráfico) e títulos do quadro de dados-chave. **Title-sm** (700, 14px, 1,3): título dentro de painel (`.h3`).
- **Figure** (700, 20px, −0,01em, tabular): números-chave em linha no cabeçalho da empresa.
- **Prose** (400, 15px, 1,68, máx. 70ch): texto corrido de relatório e resumo (`.prose-report`); o veredito do relatório sobe para 17px.
- **Lead** (400, 14,5px, ~1,625, `ink-2`, máx. 68ch): o parágrafo de abertura de página.
- **Body** (400, 14px, 1,5): base do `body`, com algarismos lining.
- **Table** (400, 13,5px, tabular): corpo das tabelas principais; tabelas secundárias e o modo Tabela das exibições usam 12–13px. Linhas de metadado (publicação, setor, pesos) ficam em 12,5–13px `muted`.
- **Button** (600, 13px): botões, navegação e controles segmentados (estes também em 12px).
- **Label** (400, 12px, `muted`): rótulos de campo e de dado, notas, linhas de fonte, legendas, tooltip.
- **Table head** (600, 12px, `ink-2`): cabeçalho de tabela; sub-rótulo de coluna em 500 `muted`.
- **Rating call** (700, 12px, maiúsculas, +0,06em): o carimbo da recomendação. É o único texto em maiúsculas do sistema.
- **Chart tick** (400, 11px, tabular, SVG): rótulos de eixo e de ponto dentro de gráficos.

### Named Rules
**A Regra da Família Única.** Libre Franklin faz tudo: título, texto, número, gráfico (`.chart text`). Sem serifada de display, sem monoespaçada.

**A Regra do Piso de 12px.** Nenhum texto HTML abaixo de 12px. A única exceção é o texto SVG de gráfico, com piso de 11px, medido por `components/charts/measure.ts` (larguras em em da Libre Franklin, determinístico no servidor e no cliente) e cortado com reticências ou quebrado em vez de encolhido.

**A Regra dos Números Tabulares.** Toda coluna de número, a caixa de recomendação, a faixa de mercado e o texto de gráfico usam `tabular-nums lining-nums`, em formato brasileiro (vírgula decimal, R$, 13,64%).

## Layout

Coluna central de no máximo 1440px, com margem lateral de 16px no celular e 24px a partir de 640px; o conteúdo começa 24px abaixo do cabeçalho fixo e termina com 64px antes do rodapé. O cabeçalho (barra de 56px + faixa de mercado) é fixo, e sua altura real é publicada em `--header-h` para que cabeçalhos de tabela congelados parem logo abaixo dele.

A grade é de 12 colunas a partir de 1024px. O Painel abre com 9 colunas para a nota (título, linha de publicação, botões, parágrafo de abertura, tabela de top picks) e 3 colunas para o quadro de dados-chave, com 32px entre colunas e 24px entre linhas; pares de exibições dividem 7 + 5. O rodapé repete a grade em 3 / 5 / 4 (marca, fontes, aviso).

Ritmo vertical: 40px entre os blocos do Painel, 32px entre seções nas demais páginas, 16px dentro de seções; espaçamentos internos na escala 4 / 8 / 12 / 16 / 20 / 24. Painéis de lista e tabela usam 16px de respiro; painéis de formulário e o cabeçalho da empresa, 20px. Células de tabela 7px × 10px; linhas de dados-chave 6px na vertical.

Abaixo de 768px, a tabela de top picks vira lista empilhada: ticker em 16px bold, tese em 13px, a caixa de recomendação em largura total e uma mini-grade de 4 dados de 12px. A navegação desce para uma segunda linha da barra e rola na horizontal; a palavra "Research" some abaixo de 420px. Tabelas largas, abaixo de 1280px, rolam por dentro (`max-height` 78vh) com cabeçalho e primeira coluna congelados; a partir de 1280px a página rola e só o cabeçalho fica preso sob a barra.

### Named Rules
**A Regra da Nota, Não do Cartão.** Dados vivem em linhas: tabelas, listas `dl` com rótulo à esquerda e valor à direita separados por fio fino, e a linha de números-chave do cabeçalho da empresa. Não se monta grade de cartões de KPI.

## Elevation & Depth

O sistema é plano como papel. A profundidade vem de tom e de fio: página branca, faixas `surface-2` (mercado, cabeçalho de tabela, rodapé, hover), quadro `box` para dados-chave, fios de 1px `hairline` e o fio marinho de 2px que marca aberturas. No escuro a mesma escada sobe em marinhos (#0a1424 → #0f1c30 → #13233b → #172a45).

### Shadow Vocabulary
- **Nota flutuante** (`box-shadow: 0 6px 18px rgba(10, 20, 36, 0.14)`): exclusiva do tooltip de gráfico, que flutua sobre a exibição.
- **Fio de cabeçalho congelado** (`box-shadow: inset 0 -1px 0 var(--hairline)`): não é elevação; substitui a borda inferior do cabeçalho de tabela fixo, que o `border-collapse` perderia.

### Named Rules
**A Regra do Papel Plano.** Painéis, botões, quadros, a caixa de recomendação e a barra não têm sombra. Só o tooltip flutua.

## Shapes

Estrutura em ângulo reto, controles com canto de 2px, círculos só como marca de dado. Painéis, exibições, aberturas de seção, o cabeçalho da empresa e o quadro de dados-chave quando abre coluna (com fio marinho) têm canto 0. Botões, inputs, selects, controles segmentados, a caixa de recomendação, o tooltip, o quadro cinza solto e o anel de foco têm 2px. Círculos aparecem apenas em pontos de dispersão, marcadores de legenda, os marcadores de 5px das listas de texto da empresa e o selo de 16px de aprovado/reprovado nos testes de valuation. Bordas são sempre de 1px (`hairline`, `grid`); o fio de 2px é marinho (aberturas) ou branco (link ativo na barra). A barra de alocação usa 1px de canto e 2px de vão entre as partes.

### Named Rules
**A Regra dos 2px.** Nada passa de 2px de raio: sem pílulas, sem cartões arredondados. O círculo é reservado a pontos de dado.

**A Regra do Fio Marinho.** O fio marinho de 2px marca apenas uma abertura: o título de seção (`.sec`), a exibição (gráfico), o painel que abre a própria seção sem título acima (`.panel-ruled`), o quadro de dados-chave e o cabeçalho da empresa. Um painel que fica sob um título de seção mantém só o fio fino; nunca se empilham dois fios marinhos.

## Components

### Barra (Navigation)
Cabeçalho de papel timbrado, fixo no topo.
- **Barra:** `navy`, 56px de altura, largura total; conteúdo alinhado à coluna de 1440px.
- **Marca:** só texto, sem logotipo: "E agora?" em 700/18px branco (−0,015em) e "Research" em 500/14px `on-navy-2`, na mesma linha de base.
- **Links:** 13px, ociosos em 500 `on-navy-2`, hover branco; o ativo em 600 branco com fio branco de 2px colado à base da barra (`aria-current="page"`).
- **Ke:** controle segmentado sobre marinho (borda branca a 25%, raio 2px, opções 20% / 25% / 30% em 600/12px tabular); a selecionada é branca com texto marinho. Ao lado, o botão de tema (Auto → Escuro → Claro), contornado com borda branca a 25% que sobe para 60% no hover.
- **Faixa de mercado:** banda `surface-2` com fio fino embaixo; cada item é rótulo 12px `muted` + valor 600/13px tabular + variação 12px com sinal e `pos`/`neg`. Rola na horizontal com 48px de esmaecimento na borda direita e termina com a hora da fonte ("B3 e BCB ao vivo, … (B3 com até 15 min de atraso)").
- **Celular:** a navegação vai para uma segunda linha e rola; o rótulo do tema encurta para "Auto".

### Caixa de recomendação (Signature)
O carimbo da nota; toda decisão de compra passa por ele.
- **Forma:** grade em linha de colunas, borda de 1px, raio 2px, fundo `surface`, números tabulares.
- **Carimbo:** 700/12px em maiúsculas, +0,06em, 6px × 10px, centralizado. Tons: **Compra forte** (`buy-strong` sólido, texto branco, borda `buy-strong`; preço abaixo do teto a Ke + 5 p.p.), **Compra** (`buy` sólido, texto branco, borda `buy`), **Aguardar** (`wait-soft`, texto `wait`, borda `wait-line`), **Sem teto** (`surface-2`, texto `muted`, borda `hairline`).
- **Células:** "Preço-teto" e "Upside", cada uma com rótulo 12px `muted` sobre valor 700/14px `ink`, 5px × 10px, separadas por fio fino à esquerda. Upside negativo leva `neg` e o sinal.
- **Variantes:** em tabela, colunas fixas de 6,6rem / 6rem / 4,4rem para que os carimbos se alinhem em coluna; no celular, largura total em `auto 1fr 1fr`. O `title` traz o detalhe ("acima do teto: falta cair 3,2%"). Quando a recomendação mudou de lado desde o registro, uma nota 12px `muted` embaixo: "era Compra em 28/10".
- **Carimbo compacto (CallChip):** só o carimbo, 3px × 8px, 12px, para tabelas densas, seguido de texto de apoio opcional.

### Buttons
- **Shape:** canto de 2px; 7px × 14px; 600/13px; transição de fundo, borda e cor em 150ms ease-out.
- **Primary:** fundo `navy`, texto `on-navy`, borda `navy`; hover `navy-2`; desabilitado a 40% de opacidade. Uma ação principal por contexto ("Ver ordens sugeridas", "Abrir relatório").
- **Secondary:** fundo `surface`, texto `ink`, fio `hairline`; hover escurece a borda para `ink-2`.
- **Link:** texto `accent` 600, sublinhado de 1px com afastamento de 3px no hover.
- **Navegação interna da empresa:** âncoras 500/13px `ink-2`, 4px × 8px, raio 2px, hover com fundo `surface-2`.
- **Foco:** contorno de 2px `accent` com afastamento de 2px em todo elemento focável.

### Controles segmentados e opções (Chips)
- **Style:** grupo com fio `hairline` e raio 2px; opções em 600/12–13px, ociosas em `ink-2` com hover `surface-2`; contagens tabulares em `muted`.
- **State:** a selecionada é `navy` com texto branco (contagem em `on-navy-2`), sinalizada por `aria-pressed`. Opções com descrição (Investir, "Como dividir") são blocos com borda e raio 2px: rótulo 600/13px e nota 12px; selecionadas viram marinho.

### Painéis e quadros (Cards / Containers)
- **Painel:** fundo `surface`, fio `hairline` de 1px, canto 0, sem sombra; 16px (listas, tabelas) ou 20px (formulários) de respiro. Tabelas dentro rolam na horizontal.
- **Painel que abre seção (`panel-ruled`):** o mesmo painel com o topo trocado por fio marinho de 2px; usado quando não há título de seção acima (Investir, tabelas completas).
- **Quadro de dados-chave (`keybox`):** fundo `box`, raio 2px. Como coluna lateral do Painel, ganha canto 0, fio marinho de 2px no topo e 12px / 16px / 16px de respiro; títulos 700/15px; linhas com rótulo 13px `ink-2` à esquerda, valor 700/13,5px tabular à direita, nota 12px `muted` sob o rótulo e fio fino entre linhas. Solto, serve de faixa de resumo (12px × 16px, texto 13,5–14px `ink-2` com números em `ink` bold).
- **Cabeçalho da empresa:** painel com fio marinho; ticker, nome (500/17px `ink-2`), setor (12,5px `muted`), preço 30px com variação assinada, caixa de recomendação à direita; abaixo de um fio fino, a linha de números-chave (rótulo 12px, valor 700/20px, nota 12px).

### Abertura de seção
Fio marinho de 2px, 10px de respiro e o título `.h2` (700/18px); à direita, opcionalmente, um link ou nota 12–13px. O conteúdo abaixo não leva outro fio marinho.

### Exibição (gráfico)
- **Moldura:** `figure` sem caixa nem fundo, aberta por fio marinho de 2px e 10px de respiro.
- **Legenda de cima:** título 700/15px; subtítulo 12px `muted` até 76ch; à direita, o botão "Tabela" / "Gráfico" (contornado, raio 2px, 600/12px), que troca o gráfico pelo seu gêmeo acessível em tabela.
- **Legenda de séries:** 12px `ink-2`, só com 2 ou mais séries; marcadores de linha 14×2px (pontilhado para pré-eleição), retângulo 10px de raio 2px, ponto 8px, anel 9px.
- **Marcas:** grade `grid`, eixos `axis`, séries na ordem `series-1` / `series-2` / `series-3`; destaque em `series-1` com o resto em `deemph`; faixas em `proj`.
- **Fonte:** linha 12px `muted` no pé, por padrão "Fonte: CVM, B3 e Banco Central; cálculos do e-agora."
- **Tooltip:** `surface`, fio `hairline`, topo marinho de 2px, raio 2px, 8px × 10px, 12px, com a única sombra do sistema; linhas com amostra da série, rótulo `ink-2` e valor 600 tabular.

### Tabelas de dados
- **Cabeçalho:** faixa `surface-2`, fio marinho de 1px no topo e `hairline` embaixo, 600/12px `ink-2`, alinhado à direita (primeira coluna à esquerda), 7px × 10px, sem quebra.
- **Corpo:** 7px × 10px, fio `grid` entre linhas, números à direita e tabulares; hover de linha `surface-2`. Célula de ação: ticker 700 `ink` (hover `accent` sublinhado), nome e setor 12px `muted` embaixo. Linhas em AGUARDAR esmaecem para `ink-2`.
- **Congelada (`freeze`):** cabeçalho e primeira coluna fixos; o fio inferior do cabeçalho vem do `inset` de 1px.

### Inputs / Fields
- **Style:** fio `hairline` de 1px, raio 2px, fundo `surface`, texto tabular; o campo de valor principal em 600/22px com "R$" de 18px `muted` fora do campo.
- **Focus:** borda `accent` mais o contorno de foco global.
- **Select:** sem aparência nativa, seta desenhada em `ink-2`, 13px, 4px / 28px / 4px / 10px, hover escurece a borda. Checkbox, rádio e range usam `fill-1` como cor de destaque.

### Rodapé
Banda `surface-2` com fio fino no topo, 12px `muted`: "E agora? Research" em 700/13px `ink` com a data do estudo, as fontes (CVM, B3, Banco Central e o atraso de 15 minutos) e o aviso permanente de que não é recomendação de investimento.

## Do's and Don'ts

### Do:
- **Faça** cada seção abrir com fio marinho de 2px + título 700/18px; quando o painel abre a própria seção sem título acima, ele leva o fio (`panel-ruled`).
- **Faça** toda recomendação passar pela caixa de recomendação (carimbo + Preço-teto + Upside); em tabelas densas, use o carimbo compacto.
- **Faça** dados-chave como lista de linhas: rótulo 13px `ink-2` à esquerda, valor 700 tabular à direita, nota 12px `muted`, fio fino entre linhas.
- **Faça** todo gráfico como exibição: fio marinho, título 15px, subtítulo 12px, alternância Gráfico/Tabela e linha de fonte no pé.
- **Faça** as séries na ordem fixa `series-1` azul, `series-2` laranja, `series-3` verde; destaque um grupo em `series-1` e deixe o resto em `deemph`.
- **Faça** toda variação com sinal impresso (+1,2% / −3,5%) e `pos`/`neg` só como reforço.
- **Faça** números em `tabular-nums lining-nums` e formato pt-BR (vírgula decimal, R$).
- **Faça** tabelas largas com cabeçalho e primeira coluna congelados abaixo de 1280px, e listas empilhadas no lugar de tabelas abaixo de 768px.
- **Faça** novos tokens de cor entrarem nos três blocos (claro, `prefers-color-scheme: dark` e `[data-theme="dark"]`) e as séries novas passarem pelo validador de paleta contra #ffffff e #0f1c30.

### Don't:
- **Não** monte grades de cartões de KPI nem blocos de números-herói; o fintech em cartões brancos com azul é o anti-mundo deste site.
- **Não** coloque fio marinho em painel que já está sob um título de seção, nem empilhe dois fios marinhos.
- **Não** pinte AGUARDAR de âmbar sólido nem de vermelho; ele fica âmbar suave (`wait` sobre `wait-soft`).
- **Não** use cor como único sinal de alta ou queda.
- **Não** use texto HTML abaixo de 12px, nem texto SVG de gráfico abaixo de 11px.
- **Não** use sombra em painel, quadro, botão ou caixa de recomendação; só o tooltip flutua.
- **Não** arredonde além de 2px nem use pílulas; círculo só em ponto de dado.
- **Não** introduza outra família tipográfica, display serifado ou fonte monoespaçada para números.
- **Não** use texto em maiúsculas com tracking como sobretítulo; as maiúsculas pertencem só ao carimbo da recomendação.
- **Não** preencha superfícies com o azul de link nem crie um segundo cromado (gradientes, azul vibrante); o marinho é o único.
- **Não** desenhe logotipo; a marca é o texto "E agora?" + "Research" na barra.
