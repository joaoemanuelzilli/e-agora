# Contexto do estudo — 26/10/2026 (segunda-feira)

## O evento
- 2º turno (25/10/2026): **Lula reeleito com 51,79%** × Flávio Bolsonaro 48,21% (TSE, 100% apurado). No 1º turno, Flávio liderou (47,04% × 45,15%), e o mercado precificava vitória dele. Flávio disse que não reconhece o resultado.
- Pregão de 26/10: **circuit breaker** pela 1ª vez desde mar/2020. Snapshot 11h50 (API oficial B3):
  - Ibovespa 169.893 (−17,2%; sexta fechou ~205 mil). SMLL −27,4%, IMOB −29,7%, IFNC −27,5%, ICON −26,7%, IEEX −21,7%.
  - Dólar futuro (DOLX26) R$ 5,49 (+9,5%). PTAX de sexta: 5,0377.
  - Curva DI disparou: DI1F27 13,76% · DI1F28 14,95% · DI1F29 15,36% · DI1F31 15,66% (era ~12,6%) · DI1F33 15,65% · DI1F35 15,58%.
  - Exportadoras subiram: SUZB3 +7,9%, EMBJ3 +7,2%, VALE3 +6,2%, WEGE3 +4,9%.
  - Mediana do universo IBOV+IBrX100+SMLL: −23%. 89 papéis caíram ≥ 20%.
- Tese do usuário: as quedas foram **macro** (prêmio de risco/juros/câmbio), não deterioração dos negócios. O trabalho deve testar isso com honestidade: juros mais altos afetam de fato empresas alavancadas em CDI; intervenção estatal afeta estatais; mas o valor intrínseco de muitos negócios mudou bem menos que o preço.

## Macro (BCB, oficial)
- Selic meta 13,75% (SGS 432). CDI ~13,65% a.a.
- IPCA 12m: 4,58% (set/26).
- Focus (23/10/2026): PIB 2026 1,8% · 2027 1,3% · 2028 1,8% · 2029-30 2,0%. IPCA 2026 5,19% · 2027 4,34% · 2028 3,75% · 2029-30 3,5%. Selic fim 2026 13,25% · 2027 11,75% (anterior ao choque — o mercado agora deve revisar para cima).

## Parâmetros obrigatórios do estudo
- **Ke (custo do capital próprio) = 25% a.a. nominal** — meta de retorno do usuário. Usar em todos os modelos de equity; WACC derivado dele.
- Crescimento na perpetuidade nominal em R$: padrão 5,0% (3,5% IPCA LP + ~1,5% real). Faixa aceitável 3,5%–6,5% conforme setor.
- Projeções: próximas do crescimento histórico de 5 anos da empresa, ajustadas por análise setorial e ganhos de eficiência plausíveis (sem otimismo gratuito).
- Unidades: R$ milhões, nominais.

## Fontes
- Demonstrações padronizadas da CVM (oficial) → `data/hist/{TICKER}.json` (gerado pelo pipeline do líder).
- Cotação ao vivo: `curl -s https://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/{TICKER}` (oficial B3).
- Proventos oficiais B3: endpoint GetListedSupplementCompany (o líder também processa).
- Pesquisa qualitativa: releases de resultados/RI das companhias, apresentações, fatos relevantes, CVM, B3, imprensa financeira de qualidade (Valor, InfoMoney, Brazil Journal, Reuters, Bloomberg Línea, Estadão, Folha, Exame, Money Times, Pipeline).
