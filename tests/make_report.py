"""Gera data/tests/test_report.md e data/tests/test_results.json a partir das saídas JUnit da suíte.

Uso (chamado por tests/run_all.sh):
  python tests/make_report.py --started ISO --pytest-rc N --engine-rc N --build-rc N --routes-rc N
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET  # só lê os JUnit gerados localmente por esta suíte (entrada confiável)
from collections import defaultdict
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data" / "tests"
RAW = OUTDIR / "raw"
COV = {c["ticker"] for c in json.load(open(ROOT / "research" / "_coverage.json"))["coverage"]}

BLOCKS = [
    ("cvm", "Integridade CVM (`data/hist`)", "pytest", "tests.test_cvm_integrity"),
    ("mercado", "Mercado (`data/market`)", "pytest", "tests.test_market_integrity"),
    ("modelo", "Modelo (`data/model`, `data/app`)", "pytest", "tests.test_model_outputs"),
    ("paridade", "Paridade do motor TS × Python", "node", "node_engine.xml"),
    ("app", "App: rotas com `next start`", "node", "node_routes.xml"),
]

# Causas-raiz já diagnosticadas: cada uma aponta o trecho de código (linha achada na hora) e os testes que a evidenciam.
BUGS = [
    {
        "id": "holding-ke", "sev": "alta",
        "title": "Holdings ignoram o Ke no motor TS (valor justo fixo de Ke 25%)",
        "where": [("lib/valuation.ts", 'if (e.template === "holding") return'), ("pipeline/build.py", 'return {"template": "holding", "fair_value"'),
                  ("pipeline/model.py", "cap_cost = hcost / (KE - g)")],
        "tests": [r"fairValue\(e, (20|30)%\) = model\.py"], "tickers_from": "holding",
        "fix": "No `model.py`, `value_holding(..., ke=KE)` deve usar `ke` no custo de holding capitalizado. "
               "No `build.py`, o `engine()` das holdings deve exportar os componentes (ticker, participação, método, valor fixo/de mercado e ações da controlada), "
               "a DL da holding, o custo anual, `g`, `n_sh` e `per_unit`. No `valuation.ts`, `fairValue` da holding passa a ser "
               "Σ fixos/mercado + Σ participação × `fairValue(motor da controlada, ke)` × ações da controlada − DL − custo/(Ke − g), dividido por ações × `per_unit`. "
               "Até lá, o painel deveria travar o Ke em 25% para SIMH3 e CSAN3.",
    },
    {
        "id": "irr3y-eps", "sev": "média",
        "title": "TIR de 3 anos: o TS e o Python divergem quando o LPA 2027E ≤ 0, e o Python devolve TIR sem sentido (−85%)",
        "where": [("lib/valuation.ts", "if (!fin(peVal) || !fin(e.eps[1]) || e.eps[1] <= 0"), ("pipeline/model.py", "if pe_exit and eps[3] > 0:"),
                  ("pipeline/build.py", '"pe_target": None')],
        "tests": [r"irr3y\(e, preço\) = irr_3y", r"test_tir_no_intervalo"],
        "fix": "Alinhar a regra nos dois motores: no `model.py`, trocar por `if pe_exit and eps[1] > 0 and eps[3] > 0:`, a mesma condição do TS; com isso, "
               "MGLU3 fica com `irr_3y = None` e deixa de mostrar −85% (saída a 10x um LPA 2029E de R$ 0,009). Além disso, gravar `out['pe_target'] = tm.get('pe')` no `model.py`, "
               "propagar com `\"pe_target\": m.get(\"pe_target\")` no `engine()` do `build.py` e usar `e.pe_target` no `irr3y` do TS, em vez de `values_share.pe / eps[1]`.",
    },
    {
        "id": "bisect-bound", "sev": "média",
        "title": "A bisseção da TIR devolve o limite do intervalo quando não há raiz",
        "where": [("pipeline/model.py", "if flo < target:"), ("lib/valuation.ts", "if (flo < target) return lo;")],
        "tests": [r"test_tir_nao_fica_presa_no_limite_da_bissecao"],
        "fix": "Quando `fn(lo) < alvo` (o preço supera o valor presente até na menor taxa; por exemplo, lucro terminal negativo) ou `fn(hi) > alvo`, devolver `None`/`null` "
               "nos dois motores e exibir 'n/d'. Hoje CVCB3 aparece com TIR de dono de 4,7% (g + 0,2 p.p.) com DDM negativo, e ainda entra no ranking pelo fator 'valor'.",
    },
    {
        "id": "shares-scale", "sev": "alta",
        "title": "Ações da CVM com escala misturada (unidades × milhares) entre arquivos: a escala é detectada só no último registro",
        "where": [("pipeline/cvm.py", "scale = 1000.0 if 300 < r < 30000 else 1.0"), ("pipeline/market.py", "def shares_at(hh, d, events):")],
        "tests": [r"test_historico_de_acoes_sem_quebra_de_escala", r"test_multiplos_historicos_plausiveis"],
        "fix": "Detectar a escala registro a registro em `cvm.py`: comparar cada `total` com o da B3, ajustado pelos eventos entre as datas, ou com o vizinho, e multiplicar por 1.000 "
               "só os registros em milhares (tesouraria à parte). O efeito chega a `market.py` (`shares_at`): o valor de mercado histórico fica 1.000× menor, "
               "com P/L de 0,01–0,1x e DY de 500%+ nos múltiplos históricos e no `dps_history` de RENT3, BBDC4, TTEN3 e outros. Também afeta o sinal "
               "'Sem emissão de ações' do Piotroski (`build.py`).",
    },
    {
        "id": "month-label", "sev": "baixa",
        "title": "Múltiplos históricos: o mês corrente sai rotulado 2026-10-31 (futuro) antes do ponto ao vivo de 26/10",
        "where": [("pipeline/market.py", 'months = raw["close"].resample("ME").last().dropna()')],
        "tests": [r"test_multiplos_historicos_datas_ordenadas"],
        "fix": "Filtrar `months = months[months.index <= LAST_CLOSE]` (ou rotular pelo último pregão do mês) antes de anexar o ponto ao vivo. Hoje as 141 séries "
               "terminam em …, 2026-09-30, **2026-10-31**, 2026-10-26 (fora de ordem e com o mês duplicado).",
    },
    {
        "id": "restated-zero", "sev": "média",
        "title": "Reapresentação (DFP Y+1, PENÚLTIMO) substitui o ano mesmo quando vem zerada",
        "where": [("pipeline/cvm.py", 'if doc in ("DRE", "DFC_MI", "DVA") and len(tab) >= 0.8 * len(t.get(doc, {})):')],
        "tests": [r"test_sem_anos_ou_trimestres_faltantes", r"test_sinais_receita_positiva"], "msg": r"DRE zerada|FY\d{4}: receita 0\.00",
        "fix": "Só trocar pela versão reapresentada se as contas-chave vierem preenchidas e diferentes de zero, por exemplo "
               "`abs(v(tab, '3.01')) > 0 and abs(v(tab, '3.11') or v(tab, '3.09')) > 0` no DRE. SBSP3 tem o FY2022 todo zerado, o que derruba o 4T22 para receita de −R$ 16,1 bi.",
    },
    {
        "id": "q4-mixed", "sev": "média",
        "title": "4º trimestre derivado mistura bases (FY reapresentado × 9M original; D&A de fontes diferentes)",
        "where": [("pipeline/cvm.py", 'ytd = c["annual"].get(f"FY{y}")')],
        "tests": [r"test_sinais_receita_positiva"], "msg": r"Q4: (receita|D&A) -",
        "fix": "Em `build_quarters`, derivar o 4T de FY e 9M na mesma base: FY original (DFP Y, ÚLTIMO) − 9M do ITR Y, ou os dois reapresentados pelos comparativos "
               "(DFP Y+1 e ITR Y+1, PENÚLTIMO). Para D&A, usar a mesma fonte no ITR e no DFP (DVA 7.04.01 ou o add-back da DFC) e marcar como inválido o 4T negativo de itens "
               "não negativos. Casos: receita negativa no 4T de VAMO3 (23 e 24), NATU3 e SBSP3 (22); D&A negativa no 4T de CEAB3, RAIL3, HAPV3, CYRE3 e NATU3. "
               "Esses trimestres alimentam os gráficos trimestrais e o LTM dos múltiplos históricos (`market.fundamentals_at`).",
    },
    {
        "id": "crash-beta", "sev": "baixa",
        "title": "Beta em dias de crash estimado com só 8 a 15 observações (valores de −1,2 a 4,6 exibidos na página da empresa)",
        "where": [("pipeline/market.py", "if len(cr) >= 8 else"), ("components/company/CompanyVal.tsx", "beta_crash_10y")],
        "tests": [r"test_betas_plausiveis"],
        "fix": "Exigir pelo menos 30 dias de crash, ou encolher a estimativa na direção do `beta_down_3y` (shrinkage de Vasicek/Blume), e ocultar o número na página quando `n_crash_days` < 30.",
    },
    {
        "id": "jump", "sev": "baixa",
        "title": "Salto diário > 35% sem evento societário na série ajustada",
        "where": [("pipeline/market.py", "weird = rets[rets.abs() > 0.35]")],
        "tests": [r"test_sem_saltos_diarios_nao_explicados"],
        "fix": "HAPV3 caiu 42,2% em 13/11/2025. É provavelmente um movimento real (resultado do 3T25), não um erro de ajuste. Convém registrar uma lista de eventos de mercado "
               "explicados no pipeline (ou uma nota em `research/`) para que `price_jumps_unexplained` traga só o que de fato precisa de revisão.",
    },
    {
        "id": "opp-rule", "sev": "processo",
        "title": "Oportunidades publicadas que deixaram de cumprir a regra de seleção com o modelo revisado",
        "where": [("pipeline/build.py", "if reported:")],
        "tests": [r"test_oportunidades_seguem_a_regra_de_selecao"],
        "fix": "O `build.py` congela a lista nas empresas com relatório (decisão de projeto: relatórios datados das 12h55). Com as premissas revisadas, conferir cada caso: "
               "atualizar o relatório e a tese, retirar a empresa da lista ou exibir no app um aviso de que ela não passa mais no filtro (TIR ≥ 20% e P(valor > preço) ≥ 45%).",
    },
    {
        "id": "stale-app", "sev": "processo",
        "title": "`data/app` desatualizado em relação a `data/model` (revisão das premissas em curso)",
        "where": [("pipeline/build.py", "def main():")],
        "tests": [r"test_app_em_dia_com_o_modelo"],
        "fix": "Depois da revisão, rodar `EAGORA_SNAPSHOT=1 python pipeline/model.py --all`, `python pipeline/build.py` e `npx next build`. O painel e a paridade "
               "a 25% usam o `overview.json`; os testes de paridade em Ke 20/30% usam o motor reconstruído do `data/model` atual para não confundir defasagem com bug.",
    },
]


# ordem de impacto no relatório
ORDER = ["holding-ke", "shares-scale", "irr3y-eps", "bisect-bound", "restated-zero", "q4-mixed", "opp-rule",
         "month-label", "crash-beta", "jump", "stale-app"]


def pl(n, one, many):
    return f"{n} {one if n == 1 else many}"


def find_line(rel, needle):
    p = ROOT / rel
    if not p.exists():
        return None
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return i
    return None


def parse_junit(path, kind):
    """-> lista de dicts {block_key, suite, name, status, message}"""
    if not path.exists():
        return None
    root = ET.parse(path).getroot()
    out = []
    for tc in root.iter("testcase"):
        cls = tc.get("classname") or ""
        name = tc.get("name") or ""
        status, msg = "passed", ""
        for child in tc:
            tag = child.tag
            if tag in ("failure", "error"):
                status, msg = "failed", child.get("message") or (child.text or "")
            elif tag == "skipped":
                t = child.get("type") or ""
                msg = child.get("message") or (child.text or "")
                status = "xfailed" if "xfail" in t.lower() else "skipped"
        out.append({"suite": cls, "name": name, "status": status, "message": clean(msg, kind)})
    return out


def clean(msg, kind):
    msg = (msg or "").strip()
    msg = re.sub(r"^(AssertionError|Error \[ERR_TEST_FAILURE\]):\s*", "", msg)
    msg = msg.split("\nassert ")[0].split("\n")[0]
    msg = msg.replace("&quot;", '"')
    return msg[:600]


def ticker_of(name):
    m = re.search(r"\[([A-Z0-9]{4,7})(~fora)?\]", name)
    if m:
        return m.group(1)
    m = re.match(r"(?:GET /(?:empresa|relatorio)/)?([A-Z]{4}[0-9]{1,2})\b", name)
    return m.group(1) if m else None


def check_of(name):
    """Nome do teste sem o parâmetro/ticker (agrupamento)."""
    n = re.sub(r"\[[^\]]*\]$", "", name)
    n = re.sub(r"^[A-Z]{4}[0-9]{1,2}\s+", "", n)
    n = re.sub(r"^GET /(empresa|relatorio)/[A-Z0-9]+", r"GET /\1/{T}", n)
    n = re.sub(r" \[motor reconstruído de data/model: data/app desatualizado\]", "", n)
    return n.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--started", default=datetime.now().isoformat(timespec="seconds"))
    for k in ("pytest-rc", "engine-rc", "build-rc", "routes-rc"):
        ap.add_argument("--" + k, type=int, default=None)
    a = ap.parse_args()
    py = parse_junit(RAW / "pytest.xml", "pytest") or []
    eng = parse_junit(RAW / "node_engine.xml", "node")
    routes = parse_junit(RAW / "node_routes.xml", "node")
    results = {}
    for key, title, kind, src in BLOCKS:
        if kind == "pytest":
            rows = [r for r in py if r["suite"].endswith(src.split(".")[-1])]
        else:
            rows = eng if key == "paridade" else routes
        results[key] = {"title": title, "rows": rows}
    ov = json.load(open(ROOT / "data" / "app" / "overview.json"))
    model_mtime = max(p.stat().st_mtime for p in (ROOT / "data" / "model").glob("*.json"))
    build_log = (RAW / "next_build.log").read_text(errors="replace") if (RAW / "next_build.log").exists() else ""
    m_pages = re.search(r"Generating static pages[^\n]*\((\d+)/(\d+)\)", build_log)
    lines = []
    W = lines.append
    tot = defaultdict(int)
    for key in results:
        for r in results[key]["rows"] or []:
            tot[r["status"]] += 1
    routes_missing = routes is None and a.routes_rc not in (None, 0)  # servidor não subiu / porta ocupada
    n_all = sum(tot.values()) + 1 + (1 if routes_missing else 0)  # + o next build (+ a etapa de rotas, se não rodou)
    n_fail = tot["failed"] + (1 if a.build_rc else 0) + (1 if routes_missing else 0)
    W("# Relatório da suíte de testes automatizados")
    W("")
    W(f"*Execução iniciada em {a.started}; relatório gerado em {datetime.now().isoformat(timespec='seconds')}. "
      f"Base: `data/app/overview.json` de {ov.get('generated_at')}; `data/model` mais recente de {datetime.fromtimestamp(model_mtime).isoformat(timespec='seconds')}. "
      f"Comando: `bash tests/run_all.sh`.*")
    W("")
    W(f"**{n_all} testes: {tot['passed'] + (0 if a.build_rc else 1)} aprovados, {pl(n_fail, 'falha', 'falhas')}, {pl(tot['skipped'], 'pulado', 'pulados')} "
      f"e {pl(tot['xfailed'], 'falha conhecida', 'falhas conhecidas')} (xfail).** "
      "Tolerância da paridade: 0,5% (mais meia unidade da 4ª casa arredondada no `overview.json`).")
    W("")
    fl = [r for key in results for r in (results[key]["rows"] or []) if r["status"] == "failed"]
    f_cov = sum(1 for r in fl if ticker_of(r["name"]) in COV)
    f_out = sum(1 for r in fl if ticker_of(r["name"]) and ticker_of(r["name"]) not in COV)
    W(f"Das {len(fl)} falhas de teste, **{f_cov} são de empresas da cobertura**, {f_out} de outras empresas com dados em `data/hist` ou `data/market` "
      f"e {pl(len(fl) - f_cov - f_out, 'é verificação global', 'são verificações globais')}.")
    par = results["paridade"]["rows"] or []

    def pcount(rx):
        rs = [r for r in par if re.search(rx, r["name"])]
        return f"{sum(1 for r in rs if r['status'] == 'passed')}/{sum(1 for r in rs if r['status'] != 'skipped')}"
    if par:
        W("")
        W(f"**Paridade TS × Python:** `fairValue` a 25% {pcount(r'fairValue[(]e, 25%[)]')}; `irrImplied` {pcount(r'irrImplied[(]e, preço[)]')}; "
          f"`irr3y` {pcount(r'irr3y[(]e, preço[)]')}; upside do painel {pcount(r'upside do painel')}; `fairValue` em Ke 20% {pcount(r'fairValue[(]e, 20%[)]')} "
          f"e em Ke 30% {pcount(r'fairValue[(]e, 30%[)]')} (aprovados/executados).")
    W("")
    W("| Bloco | Testes | Aprovados | Falhas | Pulados | xfail |")
    W("|---|---:|---:|---:|---:|---:|")
    for key, (_, title, _, _) in zip(results, BLOCKS):
        rows = results[key]["rows"]
        if rows is None:
            W(f"| {title} | — | — | não executado | — | — |")
            continue
        c = defaultdict(int)
        for r in rows:
            c[r["status"]] += 1
        W(f"| {title} | {len(rows)} | {c['passed']} | {c['failed']} | {c['skipped']} | {c['xfailed']} |")
    bstat = "passou" if a.build_rc == 0 else ("não executado" if a.build_rc is None else f"**falhou** (código {a.build_rc})")
    pages = f"; {m_pages.group(2)} páginas estáticas geradas" if m_pages else ""
    W(f"| `npx next build` | 1 | {1 if a.build_rc == 0 else 0} | {1 if a.build_rc else 0} | 0 | 0 |")
    W("")
    if routes_missing:
        motivo = (RAW / "node_routes.log").read_text(errors="replace").strip()[:300] if (RAW / "node_routes.log").exists() else ""
        W(f"**Rotas não testadas** (código {a.routes_rc}): {motivo}")
        W("")
    W(f"`next build`: {bstat}{pages}. Rotas: `next start -p 3300` com as 4 páginas gerais, as páginas `/empresa/{{T}}` da cobertura, "
      f"os {len(ov.get('opportunities') or [])} relatórios `/relatorio/{{T}}`, `/api/quotes?t=RENT3` e `/api/market`; o servidor é encerrado ao fim pela porta 3300.")
    W("")
    # ---- bugs
    fails_all = [(key, r) for key in results for r in (results[key]["rows"] or []) if r["status"] == "failed"]
    W("## Bugs e correções sugeridas")
    W("")
    W("Em ordem de impacto. A linha de cada arquivo é localizada na hora a partir do trecho de código. "
      "Os testes **não alteram** nada fora de `tests/` e `data/tests/`.")
    W("")
    used = set()
    i = 0
    for b in sorted(BUGS, key=lambda b: ORDER.index(b["id"]) if b["id"] in ORDER else 99):
        rel = [(k, r) for k, r in fails_all if any(re.search(p, r["name"]) for p in b["tests"])]
        if b["id"] == "holding-ke":
            rel = [(k, r) for k, r in rel if "holding" in r["message"]]
        if b.get("msg"):
            rel = [(k, r) for k, r in rel if re.search(b["msg"], r["message"])]
        rel.sort(key=lambda kr: (ticker_of(kr[1]["name"]) not in COV, kr[1]["name"]))
        if not rel:
            continue
        i += 1
        for k, r in rel:
            used.add((k, r["name"]))
        tks = sorted({ticker_of(r["name"]) or "" for _, r in rel} - {""})
        if not tks:  # teste global: tickers citados na mensagem
            tks = sorted({t for _, r in rel for t in re.findall(r"\b([A-Z]{4}[0-9]{1,2})\b", r["message"])})
        cov_t = [t for t in tks if t in COV]
        locs = []
        for f, needle in b["where"]:
            ln = find_line(f, needle)
            locs.append(f"`{f}:{ln}`" if ln else f"`{f}` (trecho não encontrado; talvez já corrigido)")
        W(f"### {i}. {b['title']} — severidade {b['sev']}")
        W("")
        W(f"- **Onde:** {', '.join(locs)}")
        W(f"- **Evidência:** {pl(len(rel), 'falha', 'falhas')}; empresas: {', '.join(tks[:24])}{' …' if len(tks) > 24 else ''}"
          f"{f' ({len(cov_t)} da cobertura)' if tks else ''}. Exemplo: {rel[0][1]['message'][:420]}")
        W(f"- **Correção:** {b['fix']}")
        W("")
    # ---- failures by check
    W("## Falhas por teste")
    W("")
    by = defaultdict(list)
    for k, r in fails_all:
        by[(k, check_of(r["name"]))].append(r)
    for (k, chk), rs in sorted(by.items(), key=lambda kv: (kv[0][0], -len(kv[1]))):
        tks = [ticker_of(r["name"]) for r in rs]
        cov_n = sum(1 for t in tks if t and t in COV)
        W(f"### {results[k]['title']} · `{chk}` — {len(rs)} falha(s){f', {cov_n} na cobertura' if any(tks) else ''}")
        W("")
        rs_sorted = sorted(rs, key=lambda r: (ticker_of(r["name"]) not in COV, r["name"]))
        for r in rs_sorted[:8]:
            t = ticker_of(r["name"])
            W(f"- {('**' + t + '**') if t in COV else (t or r['name'])}{'' if t in COV or not t else ' (fora da cobertura)'}: {r['message'][:380]}")
        if len(rs) > 8:
            rest = [ticker_of(r["name"]) or r["name"] for r in rs_sorted[8:]]
            W(f"- … e mais {len(rest)}: {', '.join(rest[:60])}{' …' if len(rest) > 60 else ''}")
        W("")
    if not fails_all and not a.build_rc:
        W("Nenhuma falha.")
        W("")
    # ---- xfail / skipped
    xs = [(k, r) for k in results for r in (results[k]["rows"] or []) if r["status"] in ("xfailed", "skipped")]
    if xs:
        W("## Falhas conhecidas (xfail) e testes pulados")
        W("")
        grp = defaultdict(list)
        for k, r in xs:
            grp[(r["status"], r["message"][:200])].append(ticker_of(r["name"]) or r["name"])
        for (st, msg), names in sorted(grp.items()):
            W(f"- {'xfail' if st == 'xfailed' else 'pulado'} ({len(names)}): {', '.join(names[:20])}{' …' if len(names) > 20 else ''} — {msg}")
        W("")
    W("## O que é testado")
    W("")
    W("1. **Paridade TS × Python** (`tests/engine_parity.test.mjs`, motor transpilado em memória com o TypeScript local, sem tocar em `lib/`): "
      "`fairValue`, `irrImplied`, `irr3y` e o upside do painel contra o `overview.json` (Ke 25%, preço = `price_ref`) em todas as empresas da cobertura; `fairValue` em Ke 20% e 30% "
      "contra `pipeline/model.py` recalculado (`tests/pyref.py`, com `EAGORA_SNAPSHOT=1`, controladas das holdings reavaliadas no mesmo Ke). Coerência interna: TIR no preço do DDM "
      "devolve 25%, o valor justo não cresce com o Ke, `probAbove` é monotônica e as probabilidades dos quantis ficam a até 5 p.p. do Monte Carlo.")
    W("2. **CVM** (`tests/test_cvm_integrity.py`, 141 arquivos): ativo = passivo + PL (1%, também na conta 1 × conta 2 brutas), Σ 4 trimestres = LTM (1% + R$ 1 mi), "
      "ações = B3 (`supplement.json`, `totalNumberShares`), histórico de ações sem quebra de escala, DL = bruta − caixa + arrendamentos, receita > 0, D&A ≥ 0, "
      "sem anos ou trimestres faltantes e sem DRE zerada.")
    W("3. **Mercado** (`tests/test_market_integrity.py`): datas ordenadas e sem futuro, preços > 0, saltos diários > 35% só com evento societário, betas em [0; 3] "
      "(beta de crash em [−0,5; 3,5]), múltiplos históricos plausíveis, foto de cotações coerente e proventos ≥ 0 em `dividends.json`.")
    W("4. **Modelo** (`tests/test_model_outputs.py`): valor justo finito, pesos somando 1, TIR em [−50%; 300%] e fora dos limites da bisseção, projeções de 5 anos, "
      "Monte Carlo com p5 ≤ p10 ≤ … ≤ p95 e a base dentro de [p5; p95], DL/EBITDA projetada < 10x (salvo justificativa em `research/`), cenários e sensibilidade coerentes, "
      "`data/app` em dia com `data/model`, `data/model` reproduzível pelas premissas e oportunidades dentro da regra de seleção.")
    W("5. **App** (`tests/app_routes.test.mjs`): `next build`; HTTP 200 e HTML sem página de erro em todas as rotas; ticker fora da cobertura → 404; APIs com JSON válido e campos esperados.")
    W("")
    W("Saídas brutas: `data/tests/raw/` (JUnit e logs do pytest, do node e do Next).")
    (OUTDIR / "test_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"), "started_at": a.started, "overview_generated_at": ov.get("generated_at"),
        "totals": {"tests": n_all, "passed": tot["passed"] + (0 if a.build_rc else 1), "failed": n_fail, "skipped": tot["skipped"], "xfailed": tot["xfailed"]},
        "blocks": {k: {s: sum(1 for r in (v["rows"] or []) if r["status"] == s) for s in ("passed", "failed", "skipped", "xfailed")} for k, v in results.items()},
        "next_build": {"rc": a.build_rc, "pages": m_pages.group(2) if m_pages else None},
        "failures": [{"block": k, "test": r["name"], "message": r["message"]} for k, r in fails_all],
    }
    (OUTDIR / "test_results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"relatório: {OUTDIR / 'test_report.md'} | testes {n_all} | falhas {n_fail}")


if __name__ == "__main__":
    main()
