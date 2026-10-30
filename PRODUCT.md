# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

O autor do estudo e pessoas próximas (amigos e família que também investem e recebem o link). Pessoas que já investem em ações por conta própria, leem números e querem decidir com base em evidência. Usam o site tanto no desktop quanto no celular, em proporção parecida.

## Product Purpose

"E agora?" é um estudo de valuation das ações brasileiras mais líquidas depois da reeleição de Lula em 26/10/2026, com um painel ao vivo. A tarefa principal ao abrir o site é saber **o que comprar e a que preço**: quais são as oportunidades do dia, o preço-teto de cada uma, se o preço atual está na faixa de compra e quais ordens colocar. Sucesso é a pessoa sair sabendo, em poucos segundos, quais ações estão baratas hoje e qual preço digitar no home broker; e depois conseguir conferir se as recomendações funcionaram.

## Positioning

Não é opinião nem newsletter: cada número sai de um motor de valuation reproduzível (DCF de 3 demonstrações, múltiplos, DDM, TIR de dono contra Ke de 25%, Monte Carlo), com dados oficiais (CVM, B3, Banco Central), uma bateria de testes publicada e um registro congelado das recomendações para ser julgado depois. O leitor pode mudar o Ke e ver os preços-teto recalcularem.

## Operating Context

- Consulta durante o pregão (cotações da B3 com até 15 minutos de atraso) e leitura com calma fora dele.
- Fluxo típico: Painel (oportunidades) → página da empresa ou relatório → Investir (preço-teto, faixa de compra, ordens sugeridas) → home broker do próprio usuário.
- Registro: as recomendações de 28/10/2026 foram congeladas para conferência em dezembro de 2026, contra Ibovespa, Small Caps, CDI e a mediana das não selecionadas.
- O link é repassado por mensagem para pessoas próximas, que abrem no celular.

## Capabilities and Constraints

- Rotas: Painel (`/`), Investir, Registro, Dividendos, Mercado, Metodologia, Testes, página de empresa (`/empresa/[ticker]`) e relatório (`/relatorio/[ticker]`) para 122 empresas.
- Next.js 16 / React 19, páginas estáticas que leem `data/app/*.json`; cotações ao vivo por `/api/quotes` e `/api/market` (B3 e BCB). Deploy na Vercel (`vercel deploy --prod`).
- Controle global de Ke (20%, 25%, 30%) que recalcula valores justos e preços-teto no cliente.
- Tema claro, escuro e automático, com preferência salva.
- Gráficos próprios em SVG (sem biblioteca de gráficos).
- Imagem do registro gerada a partir da própria página (`Ficha`), então essa composição precisa continuar fotografável.
- Idioma: português do Brasil, números no formato brasileiro (vírgula decimal).

## Brand Commitments

- Nome: "E agora?".
- Aviso permanente: estudo quantitativo com finalidade informativa; não é recomendação de investimento.
- Fontes sempre citadas: CVM, B3, Banco Central.
- Tom: direto, sem promessa, sem jargão desnecessário.

## Evidence on Hand

- Dados reais de 122 empresas em `data/app/` (valuation, demonstrações, proventos, Monte Carlo).
- Relatórios escritos em `research/reports/*.json` para as oportunidades.
- Registro congelado em `data/registro/2026-10-28.json` e imagem `public/registro/recomendacoes-2026-10-28.png`.
- Segunda análise externa em `data/external/analise_aprofundada_2810.json`.
- Não existem depoimentos, clientes, histórico de desempenho além do registro, nem logotipo: nada disso deve ser inventado.

## Product Principles

1. O preço de compra vem primeiro: toda tela responde "está barato agora e até quanto pagar".
2. Mostrar o cálculo, não pedir confiança: todo número leva à sua origem e à sua sensibilidade.
3. Densidade com hierarquia: muitos números, mas o que decide a compra se destaca do resto.
4. O registro é sagrado: recomendações passadas não são reescritas, são conferidas.
5. Funciona igual no celular e no desktop; nada importante só aparece com mouse.

## Accessibility & Inclusion

Contraste legível nos dois temas; cor nunca é o único sinal de alta/queda (sinal + ou − sempre presente); tabelas com cabeçalho e primeira coluna congelados no celular.
