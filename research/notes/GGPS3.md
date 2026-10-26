# GGPS3 — Grupo GPS | dossiê G12 (26/10/2026)

**Preço:** R$ 10,91 às 11h54 (−33,9%; sexta R$ 16,51; jul–set/26 R$ 11,6–13,1). 752,4 mi de ações → mercado ~R$ 8,2 bi; EV ~R$ 10,6 bi.

## Negócio
- Líder em serviços terceirizados: facilities/limpeza, segurança, logística indoor, utilidades, serviços industriais, alimentação (GRSA, comprada da Compass em 2024), mão de obra temporária e infraestrutura (manutenção de redes).
- 185 mil colaboradores e 4.543 clientes, com baixa concentração e peso industrial relevante.
- Contratos reajustados por dissídio/IPCA, com cláusulas de reequilíbrio por mudança legal.
- Crescimento combina orgânico e M&A (56 aquisições na história).

## 2T26 (release de 12/08/2026)
| R$ mi | 2T26 | 2T25 | Δ |
|---|---|---|---|
| Receita líquida | 4.598 | 4.298 | +7% (orgânico +6%) |
| EBITDA ajustado ex-IFRS16 | 445 (9,7%) | — | +10% |
| EBITDA CVM (EBIT+D&A) | 687,7 | 425,9 | inclui reversão de R$ 247 mi do Sistema S |
| Lucro líquido | 376,7 | 121,7 | ex-Sistema S: R$ 180 mi (+16%) |

- 1S26: caixa operacional R$ 1.082 mi (123% do EBITDA ajustado); dividendos pagos R$ 222 mi.
- Pressões de margem: insumos de alimentação, implantação de contratos de hotelaria marítima e mobilização/desmobilização em manutenção de telefonia e rede elétrica.
- NPS 67% (−8 p.p.).
- Aquisições pendentes de CADE: Grupo SEI, Uniflex e Grupo Aster (R$ 587 mi de receita bruta).

## Histórico (CVM)
- Receita: 4.942 / 6.615 / 9.219 / 10.631 / 14.774 / 17.283 (2020–25), CAGR 28%, majoritariamente inorgânico.
- Margem EBITDA CVM: 11,4% / 11,1% / 12,2% / 13,0% / 11,3% / 10,7%.
- Lucro: 283 / 400 / 517 / 642 / 658 / 684. ROE 18–27%. Payout ~33%.

## Dívida
- Debêntures R$ 5.397 mi + empréstimos R$ 727 mi, majoritariamente CDI+. Caixa R$ 4.017 mi. Duração da carteira: 42 meses.
- Dívida líquida da empresa: R$ 2.349 mi (inclui aquisições a pagar de R$ 180 mi e parcelamentos de R$ 62 mi), 1,3x EBITDA ajustado LTM (era 1,6x). Na CVM, com arrendamentos, R$ 2.142 mi.
- Provisão para contingências e tributos sub judice: R$ 2.092 mi. Do outro lado, depósitos judiciais de R$ 505 mi e ativo indenizatório de R$ 462 mi. Haircut de R$ 500 mi tratado como item debt-like (julgamento).

## Guidance e dividendos
- Orgânico de 8–9% em 2026 (call do 4T25). Alavancagem de conforto ~1,5x.
- Dividendos de ~R$ 0,32/ação em abr/25 e dez/25; bonificação de 10,74% em dez/25. Mínimo estatutário de 25%.

## 4º mandato de Lula — o canal mais específico do grupo
- **PEC da jornada (fim da 6x1):** aprovada no Senado em out/2026 por 75×1, sem mudança de mérito, e aguarda promulgação. Transição: 42h 60 dias após a promulgação e 40h um ano depois.
- Pela GPS: custo até +10% no cenário adverso. Só ~9 mil pessoas (~5%) estão na 6x1, mas a redução de 44h para 40h atinge quase todos.
- Repasse via cláusula de reequilíbrio, o mesmo mecanismo do dissídio. BTG vê renegociação pontual; Safra alerta para resistência de clientes e cortou o EBITDA de 2026 em 3,6%.
- Também pesam salário mínimo com ganho real, encargos e Selic alta encarecendo o M&A.
- **Premissa:** receita +10% e +9% em 2027–28 (repasse aumenta a receita nominal) com margem caindo para 10,0% na transição e voltando a 10,5% em 2030.

## Consenso
Não encontrado com data. A busca web acabou. Numerando estima LPA de R$ 0,88 em 2026.

## Premissas (research/GGPS3.json)
- Crescimento: 7,5% / 10% / 9% / 7,5% / 7%, só orgânico, sem M&A.
- Margem EBITDA: 10,5% / 10,0% / 10,0% / 10,3% / 10,5%.
- Capex 1,6% da receita. Capital de giro: 12% da receita incremental.
- Custo da dívida líquida: 16,5–17,5%, mais −R$ 90 mi/ano de atualizações monetárias de contingências.
- IR 29%. Payout: 40% → 60%.
- WACC 22%. g = 5,5%.

## Resultado do motor (pipeline/model.py, 26/10/2026, Ke 25%)
- Preço usado: R$ 11,54 | **valor justo R$ 7,47** (-35,3%) | TIR implícita 14,9% | TIR 3a 33,1%
- Métodos: DCF R$ 5,19 · DDM R$ 5,16 · P/L-alvo R$ 13,31 · EV/EBITDA-alvo R$ 15,35 (WACC 22,0%; EV DCF R$ 6.875 mi; TV 46,3% do EV)
- Projeção 2026–30: receita [18579, 20437, 22277, 23947, 25624]; EBITDA [1951, 2044, 2228, 2467, 2690]; lucro controlador [772, 834, 1007, 1229, 1443]
- DL/EBITDA [1.0, 0.8, 0.5, 0.3, 0.1]; ROE ['17,8%', '16,8%', '18,5%', '20,6%', '22,1%']; FCFF [1051, 1026, 1134, 1300, 1433]
- Cenários: bear R$ 5,38 · base R$ 7,47 · bull R$ 9,10 · esperado R$ 7,17 | Monte Carlo p10 R$ 5,60 · p50 R$ 7,45 · p90 R$ 9,45 · P(valor>preço) 0,6%
- **Leitura:** a melhor qualidade de balanço entre os 'baratos' (1,3x DL/EBITDA, ~10x P/L 2027E), mas a TIR implícita (~15%) fica abaixo de 25%. A TIR de 3 anos de ~33% depende de reprecificar a 12x P/L. A queda de −34% tem fundamento parcial (jornada de 40h). **Oportunidade apenas tática/condicional ao repasse da jornada.**

## Fontes
- Release 2T26: https://investidor10.com.br/acoes/link_comunicado/GGPS3/47564/
- 6x1 e GPS: https://investnews.com.br/negocios/grupo-gps-impacto-fim-escala-6x1/amp/ · https://euqueroinvestir.com/acoes/fim-da-escala-6x1-pode-elevar-custos-da-gps · https://oespecialista.safra.com.br/analise/gps-impactos-reformas-tributaria-trabalhista/
- Guidance do 4T25: https://monitormercantil.com.br/gps-ggps3-resultado-do-4t25-dinamicas-e-perspectivas/
- Tramitação da PEC: https://www.brasilparalelo.com.br/noticias/quando-o-fim-da-escala-6x1-comeca-a-valer
- Proventos: https://statusinvest.com.br/acoes/ggps3
- CVM: data/hist/GGPS3.json
