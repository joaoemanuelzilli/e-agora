"""Demonstrações oficiais da CVM (DFP anual + ITR trimestral) -> séries padronizadas por empresa.

Uso: python pipeline/cvm.py <dir_raw_cvm> <universe_json> <coverage_json> <out_dir>

Saída: <out_dir>/{TICKER}.json com séries anuais (FY2015..), trimestrais (2022Q1..), LTM, balanço mais recente,
indicadores e linhas brutas das demonstrações. Valores em R$ milhões.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

DOCS = ["DRE", "BPA", "BPP", "DFC_MI", "DFC_MD", "DVA"]
USECOLS = ["CNPJ_CIA", "DT_REFER", "VERSAO", "ESCALA_MOEDA", "ORDEM_EXERC", "DT_INI_EXERC", "DT_FIM_EXERC",
           "CD_CONTA", "DS_CONTA", "VL_CONTA"]
EXTRA_CNPJ = {"BPAC11": "30.306.294/0001-45"}  # BTG Pactual (unit não listada no FCA com esse código)
UNITS = {"ENGI11": 5, "IGTI11": 4.0638, "ALUP11": 3, "BPAC11": 3, "SAPR11": 5, "TAEE11": 3, "KLBN11": 5, "SANB11": 2, "BRBI11": 3}


def norm(s):
    return (s or "").lower()


def read_zip_csv(zpath, name, cnpjs):
    with zipfile.ZipFile(zpath) as z:
        if name not in z.namelist():
            return None
        with z.open(name) as fh:
            df = pd.read_csv(fh, sep=";", encoding="latin1", dtype=str, usecols=lambda c: c in USECOLS or c.startswith("QT_"))
    return df[df.CNPJ_CIA.isin(cnpjs)].copy()


def load_all(raw, cnpjs):
    """Retorna dict (kind, doc, basis) -> DataFrame concatenado de todos os anos."""
    out = {}
    for kind, years in (("dfp", range(2015, 2026)), ("itr", range(2022, 2027))):
        for y in years:
            zp = Path(raw) / f"{kind}_cia_aberta_{y}.zip"
            if not zp.exists():
                continue
            for doc in DOCS:
                for basis in ("con", "ind"):
                    df = read_zip_csv(zp, f"{kind}_cia_aberta_{doc}_{basis}_{y}.csv", cnpjs)
                    if df is not None and len(df):
                        out.setdefault((kind, doc, basis), []).append(df)
            cc = read_zip_csv(zp, f"{kind}_cia_aberta_composicao_capital_{y}.csv", cnpjs)
            if cc is not None and len(cc):
                out.setdefault((kind, "CAP", "-"), []).append(cc)
            print(kind, y, flush=True)
    for k in out:
        df = pd.concat(out[k], ignore_index=True)
        if "VL_CONTA" in df:
            df["VL"] = pd.to_numeric(df["VL_CONTA"], errors="coerce")
            scale = np.where(df["ESCALA_MOEDA"].str.upper().str.startswith("MIL"), 1e-3, 1e-6)
            df["VL"] = df["VL"] * scale
        df["VERSAO"] = pd.to_numeric(df["VERSAO"], errors="coerce")
        out[k] = df
    return out


def latest_version(df):
    mx = df.groupby(["CNPJ_CIA", "DT_REFER"])["VERSAO"].transform("max")
    return df[df["VERSAO"] == mx]


# ---------------------------------------------------------------- extração padronizada
def tab_from(df):
    """DataFrame de um período -> dict code -> (desc, value)."""
    return {r.CD_CONTA: (r.DS_CONTA, r.VL) for r in df.itertuples()}


def v(tab, code):
    x = tab.get(code)
    return float(x[1]) if x and pd.notna(x[1]) else np.nan


def top_matches(tab, prefix, pattern, sign=None, exclude=None):
    """Soma contas sob `prefix` cuja descrição casa com `pattern`, sem contar duas vezes (pega o ancestral mais alto)."""
    rx = re.compile(pattern, re.I)
    ex = re.compile(exclude, re.I) if exclude else None
    hits = []
    for code, (desc, val) in tab.items():
        if not code.startswith(prefix + ".") or pd.isna(val):
            continue
        if rx.search(desc or "") and not (ex and ex.search(desc or "")):
            hits.append(code)
    hits.sort(key=lambda c: c.count("."))
    chosen = []
    for c in hits:
        if not any(c.startswith(p + ".") for p in chosen):
            chosen.append(c)
    tot = 0.0
    for c in chosen:
        val = float(tab[c][1])
        if sign == "neg" and val > 0:
            continue
        if sign == "pos" and val < 0:
            continue
        tot += val
    return tot if chosen else np.nan


def sum_outside(tab, roots, pattern, exclude, skip):
    rx, ex = re.compile(pattern, re.I), re.compile(exclude, re.I)
    hits = [c for c, (d, val) in tab.items()
            if any(c.startswith(r + ".") for r in roots) and not any(c == k or c.startswith(k + ".") for k in skip)
            and rx.search(d or "") and not ex.search(d or "") and pd.notna(val)]
    hits.sort(key=lambda c: c.count("."))
    chosen = []
    for c in hits:
        if not any(c.startswith(q + ".") for q in chosen):
            chosen.append(c)
    return float(sum(float(tab[c][1]) for c in chosen)) if chosen else 0.0


def find_level(tab, level, pattern, prefix="", last=True):
    rx = re.compile(pattern, re.I)
    cands = [c for c, (d, _) in tab.items() if c.count(".") == level and c.startswith(prefix) and rx.search(d or "")]
    if not cands:
        return None
    cands.sort(key=lambda c: [int(x) for x in c.split(".")])
    return cands[-1] if last else cands[0]


def fin_type(dre):
    d = norm(dre.get("3.01", ("", 0))[0])
    if "intermedia" in d:
        return "bank"
    if any(w in d for w in ("prêmio", "premio", "seguro", "resseguro")):
        return "insurer"
    return None


def extract_flows(dre, dfc, dva, ftype):
    o = {}
    ni_code = find_level(dre, 1, r"(lucro|preju[íi]zo|resultado l[íi]quido).*(per[íi]odo|exerc[íi]cio)") or "3.11"
    o["net_income"] = v(dre, ni_code)
    ctrl = find_level(dre, 2, r"controlador", prefix=ni_code + ".", last=False)
    mino = find_level(dre, 2, r"n[ãa]o controlador", prefix=ni_code + ".")
    o["ni_controlling"] = v(dre, ctrl) if ctrl and "não" not in norm(dre[ctrl][0]) and "nao" not in norm(dre[ctrl][0]) else np.nan
    if np.isnan(o["ni_controlling"]):
        o["ni_controlling"] = o["net_income"] - (v(dre, mino) if mino else 0.0)
    o["ni_minority"] = v(dre, mino) if mino else 0.0
    if np.isnan(o["ni_minority"]):
        o["ni_minority"] = 0.0
    ni, ct, mn = o["net_income"], o["ni_controlling"], o["ni_minority"]
    if not np.isnan(ni):
        tol = 0.02 * abs(ni) + 0.5
        if np.isnan(ct):
            o["ni_controlling"] = ni - mn
        elif abs(ct) < 1e-6 and abs(mn) < 1e-6 and abs(ni) > 0.5:  # atribuição zerada na base CVM
            o["ni_controlling"] = ni
        elif abs(ct + mn - ni) <= tol:
            pass
        elif abs(ct - mn - ni) <= tol:  # sinal do minoritário invertido
            o["ni_minority"] = -mn
        elif abs(mn) <= tol:  # minoritário desprezível: controlador = total (ex.: INTB3 2T26 com 0,15)
            o["ni_controlling"] = ni - mn
        elif abs(ct) < 1e-6:
            o["ni_controlling"] = ni - mn
    o["revenue"] = v(dre, "3.01")
    if ftype is None:
        o.update(cogs=v(dre, "3.02"), gross_profit=v(dre, "3.03"), opex=v(dre, "3.04"), ebit=v(dre, "3.05"),
                 fin_result=v(dre, "3.06"), fin_income=v(dre, "3.06.01"), fin_expense=v(dre, "3.06.02"),
                 ebt=v(dre, "3.07"), taxes=v(dre, "3.08"), ni_discontinued=v(dre, "3.10"))
        o["selling"] = top_matches(dre, "3.04", r"vendas|comerciais")
        o["g_and_a"] = top_matches(dre, "3.04", r"gerais e administrativas|administrativas")
        o["equity_income"] = top_matches(dre, "3.04", r"equival[êe]ncia patrimonial")
        da = top_matches(dva, "7", r"deprecia[çc][ãa]o|amortiza[çc][ãa]o|exaust") if dva else np.nan
        if np.isnan(da) or da == 0:
            da = -top_matches(dfc, "6.01", r"deprecia[çc][ãa]o|amortiza[çc][ãa]o", exclude=r"custo|empr|juros|ágio de")
        o["d_and_a"] = abs(da) if not np.isnan(da) else np.nan
        o["ebitda"] = o["ebit"] + (o["d_and_a"] if not np.isnan(o["d_and_a"]) else 0.0)
    else:
        ebt = find_level(dre, 1, r"resultado antes dos tributos|antes do imposto|antes dos impostos")
        tx = find_level(dre, 1, r"imposto de renda e contribui")
        o.update(ebt=v(dre, ebt) if ebt else np.nan, taxes=v(dre, tx) if tx else np.nan,
                 fin_interm_expense=v(dre, "3.02"), gross_fin_interm=v(dre, "3.03"))
    if dfc:
        o["cfo"], o["cfi"], o["cff"] = v(dfc, "6.01"), v(dfc, "6.02"), v(dfc, "6.03")
        o["capex"] = top_matches(dfc, "6.02", r"imobilizad|intang[íi]vel|ativo fixo|ativos? de contrato|infraestrutura|obras|propriedades? para investimento|bens de uso|frota|ve[íi]culo|carro",
                                 sign="neg", exclude=r"venda|aliena|baixa|recebimento|resgate|aplica|alien")
        o["fleet_capex_cfo"] = top_matches(dfc, "6.01", r"(aquisi|compra|adi[çc]).*(carro|ve[íi]culo|frota|caminh|m[áa]quina|equipamento)", sign="neg")
        o["dividends_paid"] = top_matches(dfc, "6.03", r"dividend|juros sobre (o )?capital|jcp|provento|remunera[çc][ãa]o (aos|dos) acionistas|distribui[çc][ãa]o de (lucros|resultados)", sign="neg")
        o["buybacks"] = top_matches(dfc, "6.03", r"tesouraria|recompra", sign="neg", exclude=r"deb[êe]nture|d[íi]vida|empr[ée]stimo|bond|notas?|cr[ée]dito|t[íi]tulo")
        o["lease_paid"] = top_matches(dfc, "6.03", r"arrendamento|aluguel|direito de uso", sign="neg")
        o["interest_paid"] = top_matches(dfc, "6", r"juros pagos|pagamento de juros|juros sobre empr|juros de empr|juros de deb|juros sobre deb", sign="neg", exclude=r"capital pr[óo]prio")
        o["debt_raised"] = top_matches(dfc, "6.03", r"capta|emiss[ãa]o de deb|ingresso|obten|contrata|empr[ée]stimos e financiamentos obtidos", sign="pos", exclude=r"a[çc][õo]es|capital")
        o["debt_repaid"] = top_matches(dfc, "6.03", r"(pagamento|amortiza|liquida).*(empr[ée]st|financ|deb[êe]nt|d[íi]vida|principal|nota)", sign="neg", exclude=r"juros|arrendamento")
    return o


def extract_bs(bpa, bpp, ftype):
    o = {"total_assets": v(bpa, "1")}
    eq = find_level(bpp, 1, r"patrim[ôo]nio l[íi]quido") or "2.03"
    o["equity"] = v(bpp, eq)
    mino = find_level(bpp, 2, r"n[ãa]o controlador", prefix=eq + ".")
    o["minority"] = v(bpp, mino) if mino else 0.0
    o["equity_controlling"] = o["equity"] - (o["minority"] if not np.isnan(o["minority"]) else 0.0)
    if ftype is None:
        o.update(current_assets=v(bpa, "1.01"), cash=v(bpa, "1.01.01"), st_investments=v(bpa, "1.01.02"),
                 receivables=v(bpa, "1.01.03"), inventories=v(bpa, "1.01.04"), noncurrent_assets=v(bpa, "1.02"),
                 investments=v(bpa, "1.02.02"), ppe=v(bpa, "1.02.03"), intangible=v(bpa, "1.02.04"),
                 current_liab=v(bpp, "2.01"), noncurrent_liab=v(bpp, "2.02"),
                 st_debt=v(bpp, "2.01.04"), lt_debt=v(bpp, "2.02.01"))
        lt_inv = top_matches(bpa, "1.02.01", r"aplica[çc][õo]es financeiras|t[íi]tulos e valores mobili")
        o["lt_investments"] = 0.0 if np.isnan(lt_inv) else lt_inv
        if np.isnan(o["st_investments"]):
            o["st_investments"] = 0.0
        lease = sum_outside(bpp, ("2.01", "2.02"), r"arrendamento|arredamento|direito de uso|leasing", r"receb|ativo", ("2.01.04", "2.02.01"))
        extra = sum_outside(bpp, ("2.01", "2.02"),
                            r"empr[ée]stimo|financiamento|deb[êe]nture|\bcri\b|certificados? de receb|c[ée]dulas? de cr[ée]dito|notas? comerc|notas? promiss|bonds|senior notes|t[íi]tulos? a pagar",
                            r"arrendamento|leasing|direito de uso|fornecedor|deriv|parcelamento|dividend|tribut|imposto|adiantamento|receita|provis|partes relacionadas|juros sobre capital",
                            ("2.01.04", "2.02.01"))
        o["leases"] = lease
        o["debt_other_lines"] = extra
        o["gross_debt"] = np.nansum([o["st_debt"], o["lt_debt"]]) + extra
        o["cash_total"] = np.nansum([o["cash"], o["st_investments"], o["lt_investments"]])
        o["net_debt_ex_leases"] = o["gross_debt"] - o["cash_total"]
        o["net_debt"] = o["net_debt_ex_leases"] + lease
        o["retained"] = np.nansum([top_matches(bpp, eq, r"reservas de lucro"), top_matches(bpp, eq, r"lucros.*acumulados|preju[íi]zos acumulados")])
    return o


# ---------------------------------------------------------------- montagem por empresa
def period_tables(store, kind, cnpj, dt, basis, ordem="ÚLTIMO", dt_ini=None):
    res = {}
    for doc in DOCS:
        df = store.get((kind, doc, basis))
        if df is None:
            continue
        sub = df[(df.CNPJ_CIA == cnpj) & (df.DT_REFER == dt) & (df.ORDEM_EXERC == ordem)]
        if dt_ini is not None and "DT_INI_EXERC" in sub and doc in ("DRE",) and sub["DT_INI_EXERC"].notna().any():
            sub = sub[sub.DT_INI_EXERC == dt_ini]
        if len(sub):
            res[doc] = tab_from(sub)
    if "DFC_MI" not in res and "DFC_MD" in res:
        res["DFC_MI"] = res["DFC_MD"]
    return res


def choose_basis(store, kind, cnpj, dt):
    df = store.get((kind, "DRE", "con"))
    if df is not None and ((df.CNPJ_CIA == cnpj) & (df.DT_REFER == dt)).any():
        return "con"
    return "ind"


def flows_bs(t, ftype):
    f = extract_flows(t.get("DRE", {}), t.get("DFC_MI", {}), t.get("DVA", {}), ftype)
    b = extract_bs(t.get("BPA", {}), t.get("BPP", {}), ftype) if "BPA" in t else {}
    return f, b


def _filled(doc, tab):
    """Reapresentação útil: DRE com receita e resultado diferentes de zero; DFC/DVA com algum valor não nulo."""
    if not tab:
        return False
    if doc == "DRE":
        rev = v(tab, "3.01")
        res = [x for x in (v(tab, "3.11"), v(tab, "3.09"), v(tab, "3.05")) if not np.isnan(x)]
        return not np.isnan(rev) and abs(rev) > 0 and any(abs(x) > 0 for x in res)
    return any(pd.notna(x[1]) and abs(float(x[1])) > 0 for x in tab.values())


def company(store, cnpj, ticker):
    out = {"annual": {}, "annual_orig": {}, "q_ytd": {}, "q_3m": {}, "bs_q": {}, "raw_src": {}}
    ftype = None
    # anual: DFP Y (ÚLTIMO) com preferência pela reapresentação na DFP Y+1 (PENÚLTIMO)
    dfp_dre = store.get(("dfp", "DRE", "con"))
    for y in range(2015, 2026):
        dt = f"{y}-12-31"
        dt_next = f"{y+1}-12-31"
        basis = choose_basis(store, "dfp", cnpj, dt)
        t = period_tables(store, "dfp", cnpj, dt, basis)
        if not t:
            continue
        t_orig = dict(t)
        if y < 2025:
            t2 = period_tables(store, "dfp", cnpj, dt_next, choose_basis(store, "dfp", cnpj, dt_next), ordem="PENÚLTIMO")
            for doc, tab in t2.items():
                if doc in ("DRE", "DFC_MI", "DVA") and len(tab) >= 0.8 * len(t.get(doc, {})) and _filled(doc, tab):
                    t[doc] = tab
        ftype = fin_type(t.get("DRE", {})) or ftype
        f, b = flows_bs(t, ftype)
        out["annual"][f"FY{y}"] = {**f, **b, "basis": basis}
        f0, _ = flows_bs(t_orig, ftype) if t_orig is not t else (f, b)
        out["annual_orig"][f"FY{y}"] = f0  # mesma base do ITR do ano, para derivar o 4T
        out["raw_src"][f"FY{y}"] = t
    # trimestral (ITR): DRE 3 meses e YTD; DFC/DVA YTD; balanço
    itr = store.get(("itr", "DRE", "con"))
    dts = set()
    for basis in ("con", "ind"):
        df = store.get(("itr", "DRE", basis))
        if df is not None:
            dts |= set(df[df.CNPJ_CIA == cnpj].DT_REFER.unique())
    for dt in sorted(dts):
        y, m = int(dt[:4]), int(dt[5:7])
        q = {3: 1, 6: 2, 9: 3}.get(m)
        if not q:
            continue
        basis = choose_basis(store, "itr", cnpj, dt)
        qstart = f"{y}-{(q-1)*3+1:02d}-01"
        t_ytd = period_tables(store, "itr", cnpj, dt, basis, dt_ini=f"{y}-01-01")
        t_3m = period_tables(store, "itr", cnpj, dt, basis, dt_ini=qstart)
        ftype = fin_type(t_ytd.get("DRE", {})) or ftype
        fy, by = flows_bs(t_ytd, ftype)
        f3, _ = flows_bs({"DRE": t_3m.get("DRE", {})}, ftype)
        key = f"{y}Q{q}"
        out["q_ytd"][key] = fy
        out["q_3m"][key] = f3
        out["bs_q"][key] = {**by, "date": dt}
        out["raw_src"][key] = t_ytd
    out["ftype"] = ftype
    return out


FLOW_KEYS = ["revenue", "cogs", "gross_profit", "opex", "selling", "g_and_a", "equity_income", "ebit", "d_and_a", "ebitda",
             "fin_result", "fin_income", "fin_expense", "ebt", "taxes", "ni_discontinued", "net_income", "ni_controlling", "ni_minority",
             "cfo", "cfi", "cff", "capex", "fleet_capex_cfo", "dividends_paid", "buybacks", "lease_paid", "interest_paid",
             "debt_raised", "debt_repaid", "fin_interm_expense", "gross_fin_interm"]
BS_KEYS = ["total_assets", "current_assets", "cash", "st_investments", "lt_investments", "cash_total", "receivables", "inventories",
           "noncurrent_assets", "investments", "ppe", "intangible", "current_liab", "noncurrent_liab", "st_debt", "lt_debt", "debt_other_lines",
           "gross_debt", "leases", "net_debt_ex_leases", "net_debt", "equity", "minority", "equity_controlling", "retained"]


def r2(x):
    if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
        return None
    return round(float(x), 2)


def build_quarters(c):
    """Fluxos trimestrais (3m) e LTM. DRE: 3m direto (Q1–Q3), Q4 = FY − 9M. DFC/DVA: diferenças de YTD."""
    quarters = {}
    years = sorted({int(k[:4]) for k in c["q_ytd"]} | {int(k[2:]) for k in c["annual"]})
    for y in years:
        prev_ytd = None
        for q in (1, 2, 3, 4):
            key = f"{y}Q{q}"
            if q < 4:
                ytd = c["q_ytd"].get(key)
                if ytd is None:
                    prev_ytd = None
                    continue
            else:
                ytd = (c.get("annual_orig") or {}).get(f"FY{y}") or c["annual"].get(f"FY{y}")
                if ytd is None or prev_ytd is None or f"{y}Q3" not in c["q_ytd"]:
                    continue
            row = {}
            for k in FLOW_KEYS:
                a = ytd.get(k, np.nan)
                b = prev_ytd.get(k, np.nan) if prev_ytd else 0.0
                row[k] = a - (b if b is not None and not np.isnan(b) else 0.0) if a is not None and not np.isnan(a) else np.nan
            if q < 4 and key in c["q_3m"]:  # DRE 3m oficial quando disponível
                for k in ("revenue", "ebit", "net_income", "ni_controlling", "ebt", "taxes", "fin_result", "cogs", "gross_profit"):
                    val = c["q_3m"][key].get(k)
                    if val is not None and not np.isnan(val):
                        row[k] = val
                if not np.isnan(row.get("ebit", np.nan)) and not np.isnan(row.get("d_and_a", np.nan)):
                    row["ebitda"] = row["ebit"] + row["d_and_a"]
            # D&A (sempre ≥ 0) e receita de não financeira negativas no trimestre derivado = bases misturadas: lacuna
            if row.get("d_and_a") is not None and not np.isnan(row["d_and_a"]) and row["d_and_a"] < -0.5:
                row["d_and_a"] = np.nan
                row["ebitda"] = np.nan
            if c.get("ftype") is None and row.get("revenue") is not None and not np.isnan(row["revenue"]) and row["revenue"] < -0.5:
                for k in FLOW_KEYS:
                    row[k] = np.nan
            quarters[key] = row
            prev_ytd = ytd
    return quarters


def ltm(c):
    if not c["q_ytd"]:
        return None, None
    last = sorted(c["q_ytd"], key=lambda k: (int(k[:4]), int(k[-1])))[-1]
    y, q = int(last[:4]), int(last[-1])
    fy_prev = c["annual"].get(f"FY{y-1}")
    ytd_prev = c["q_ytd"].get(f"{y-1}Q{q}")
    ytd = c["q_ytd"][last]
    fy_last = c["annual"].get(f"FY{y}")
    if fy_last is not None and q == 4:
        return last, {k: fy_last.get(k) for k in FLOW_KEYS}
    if fy_prev is None or ytd_prev is None:
        return last, None
    out = {}
    for k in FLOW_KEYS:
        a, b, d = ytd.get(k, np.nan), fy_prev.get(k, np.nan), ytd_prev.get(k, np.nan)
        out[k] = a + b - d if not any(x is None or np.isnan(x) for x in (a, b, d)) else np.nan
    return last, out


def raw_lines(c, keys, max_level=4):
    docs = {}
    for doc in ("DRE", "BPA", "BPP", "DFC_MI", "DVA"):
        codes = {}
        for k in keys:
            t = c["raw_src"].get(k, {}).get(doc, {})
            for code, (desc, val) in t.items():
                if code.count(".") <= max_level - 1 or doc in ("DFC_MI", "BPP") and code.count(".") <= max_level:
                    codes.setdefault(code, {"desc": desc})[k] = r2(val)
        rows = sorted(codes.items(), key=lambda kv: [int(x) if x.isdigit() else 0 for x in kv[0].split(".")])
        docs[doc] = {"periods": keys, "rows": [[code, d["desc"]] + [d.get(k) for k in keys] for code, d in rows]}
    return docs


def ratios(a, prev=None):
    o = {}
    rev = a.get("revenue")
    def div(x, y):
        return x / y if x is not None and y not in (None, 0) and not np.isnan(x) and not np.isnan(y) else np.nan
    o["gross_margin"] = div(a.get("gross_profit", np.nan), rev)
    o["ebitda_margin"] = div(a.get("ebitda", np.nan), rev)
    o["ebit_margin"] = div(a.get("ebit", np.nan), rev)
    o["net_margin"] = div(a.get("ni_controlling", np.nan), rev)
    eq_avg = a.get("equity_controlling")
    if prev and prev.get("equity_controlling") is not None and not np.isnan(prev.get("equity_controlling", np.nan)):
        eq_avg = (a.get("equity_controlling", np.nan) + prev["equity_controlling"]) / 2
    o["roe"] = div(a.get("ni_controlling", np.nan), eq_avg)
    if a.get("net_debt") is not None and not np.isnan(a.get("net_debt", np.nan)):
        o["nd_ebitda"] = div(a["net_debt"], a.get("ebitda", np.nan))
        ic = a.get("equity", np.nan) + a["net_debt"]
        o["roic"] = div(a.get("ebit", np.nan) * (1 - 0.34), ic)
    o["payout"] = div(-a.get("dividends_paid", np.nan) if a.get("dividends_paid") is not None else np.nan, a.get("ni_controlling", np.nan))
    return {k: (round(float(x), 4) if x is not None and not np.isnan(x) and not np.isinf(x) else None) for k, x in o.items()}


def main(raw, fca_csv, universe_json, coverage_json, out_dir, supplement_json=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    uni = json.load(open(universe_json))["rows"]
    cov = {r["ticker"] for r in json.load(open(coverage_json))["coverage"]}
    fca = pd.read_csv(fca_csv, sep=";", dtype=str)
    supp = json.load(open(supplement_json)) if supplement_json else {}
    cad = pd.read_csv(Path(raw) / "cad_cia_aberta.csv", sep=";", encoding="latin1", dtype=str)
    cad = cad.sort_values("DT_REG").drop_duplicates("CNPJ_CIA", keep="last").set_index("CNPJ_CIA")
    t2c = dict(zip(fca.Codigo_Negociacao, fca.CNPJ_Companhia))
    t2c.update(EXTRA_CNPJ)
    tickers = [r["ticker"] for r in uni]
    tickers = [t for t in tickers if t in cov] + [t for t in tickers if t not in cov]  # cobertura primeiro
    cnpjs = sorted({t2c[t] for t in tickers if t in t2c})
    cache = out_dir.parent / "_cvm_store.pkl"
    if cache.exists():
        store = pd.read_pickle(cache)
    else:
        store = load_all(raw, set(cnpjs))
        for k in list(store):
            if k[1] != "CAP":
                store[k] = latest_version(store[k])
        pd.to_pickle(store, cache)
    by_cnpj = {}
    for k, df in store.items():
        if k[1] == "CAP":
            continue
        for cn, g in df.groupby("CNPJ_CIA"):
            by_cnpj.setdefault(cn, {})[k] = g
    print("grouped", len(by_cnpj), flush=True)
    cap = store.get(("itr", "CAP", "-"))
    capd = store.get(("dfp", "CAP", "-"))
    caps = pd.concat([x for x in (cap, capd) if x is not None], ignore_index=True)
    for c_ in ["QT_ACAO_ORDIN_CAP_INTEGR", "QT_ACAO_PREF_CAP_INTEGR", "QT_ACAO_TOTAL_CAP_INTEGR", "QT_ACAO_ORDIN_TESOURO", "QT_ACAO_PREF_TESOURO", "QT_ACAO_TOTAL_TESOURO"]:
        caps[c_] = pd.to_numeric(caps[c_], errors="coerce")
    summary = []
    for tk in tickers:
        cnpj = t2c.get(tk)
        if not cnpj:
            print("sem CNPJ:", tk)
            continue
        c = company(by_cnpj.get(cnpj, {}), cnpj, tk)
        if not c["annual"]:
            print("sem dados:", tk)
            continue
        quarters = build_quarters(c)
        last_q, ltm_flows = ltm(c)
        years = sorted(c["annual"], key=lambda k: int(k[2:]))
        # balanço mais recente
        bs_latest = c["bs_q"].get(last_q) if last_q and int(last_q[:4]) > int(years[-1][2:]) else None
        if bs_latest is None:
            bs_latest = {k: c["annual"][years[-1]].get(k) for k in BS_KEYS}
            bs_latest["date"] = f"{years[-1][2:]}-12-31"
        # ações
        cs = caps[caps.CNPJ_CIA == cnpj].sort_values(["DT_REFER", "VERSAO"])
        raw_sh = []
        nz = lambda x: 0.0 if x is None or np.isnan(x) else float(x)
        for dt, g in cs.groupby("DT_REFER"):
            r = g.iloc[-1]
            tot = r.QT_ACAO_TOTAL_CAP_INTEGR
            if tot and not np.isnan(tot):
                raw_sh.append({"date": dt, "tot": float(tot), "tes": nz(r.QT_ACAO_TOTAL_TESOURO),
                               "on": nz(r.QT_ACAO_ORDIN_CAP_INTEGR), "on_t": nz(r.QT_ACAO_ORDIN_TESOURO),
                               "pn": nz(r.QT_ACAO_PREF_CAP_INTEGR), "pn_t": nz(r.QT_ACAO_PREF_TESOURO)})
        # ações: total corrente oficial da B3 × (1 − fração em tesouraria da CVM); escala da CVM (unidades × milhares)
        # decidida registro a registro: o último contra a B3, os anteriores contra o vizinho seguinte já corrigido
        sp = (supp or {}).get(tk[:4]) or {}
        b3_total = float(str(sp.get("totalNumberShares", "0")).replace(".", "") or 0)
        b3_on = float(str(sp.get("numberCommonShares", "0")).replace(".", "") or 0)
        b3_pn = float(str(sp.get("numberPreferredShares", "0")).replace(".", "") or 0)
        shares_hist = [None] * len(raw_sh)
        nxt = b3_total or None
        near = lambda a, b: bool(a and b) and abs(a / b - 1) < 0.05
        for i in range(len(raw_sh) - 1, -1, -1):
            rr = raw_sh[i]
            s_i = 1.0
            if nxt and rr["tot"]:
                q = nxt / rr["tot"]
                s_i = 1000.0 if 300 < q < 30000 else (0.001 if 1 / 30000 < q < 1 / 300 else 1.0)
                if s_i == 1.0 and not (0.5 < q < 2) and i > 0 and i < len(raw_sh) - 1:
                    # registro isolado fora da escala dos vizinhos (ex.: BRSR6 set/25, GMAT3 jun/22): se o anterior,
                    # na mesma escala, bate com o seguinte, o do meio é erro de preenchimento e repete o seguinte
                    prev = raw_sh[i - 1]["tot"]
                    if any(near(prev * k, nxt) for k in (1.0, 1000.0, 0.001)):
                        nx = shares_hist[i + 1]
                        shares_hist[i] = {**nx, "date": rr["date"], "repaired": True}
                        continue
            t_s = s_i
            if s_i == 1000.0 and rr["tot"] and rr["tes"] / rr["tot"] > 0.25:  # tesouraria em unidades com total em milhares (ex.: TEND3)
                t_s = 1.0
            tot, tes = rr["tot"] * s_i, rr["tes"] * t_s
            shares_hist[i] = {"date": rr["date"], "total": tot, "treasury": tes, "outstanding": tot - tes,
                              "on": rr["on"] * s_i - rr["on_t"] * t_s, "pn": rr["pn"] * s_i - rr["pn_t"] * t_s, "cvm_scale": s_i}
            nxt = tot
        scale = shares_hist[-1]["cvm_scale"] if shares_hist else 1.0
        if shares_hist and b3_total:
            last = shares_hist[-1]
            tr = last["treasury"] / last["total"] if last["total"] else 0.0
            ratio = b3_total / last["total"] if last["total"] else 1.0
            if abs(ratio - 1) < 0.05:
                # emissão/cancelamento depois do balanço: o cancelamento sai da tesouraria (não contar duas vezes)
                tes_now = max(0.0, last["treasury"] - max(0.0, last["total"] - b3_total))
                out_now = b3_total - tes_now
                tr_now = tes_now / b3_total
            else:  # desdobramento, grupamento ou bonificação: a tesouraria acompanha a proporção
                tr_now = tr
                out_now = b3_total * (1 - tr)
            shares_now = {"date": "B3 atual", "source": "B3 (ações emitidas) − tesouraria CVM " + last["date"] + " (líquida de cancelamentos posteriores)",
                          "total": b3_total, "treasury_ratio": tr_now, "outstanding": out_now,
                          "on": b3_on * (1 - tr_now), "pn": b3_pn * (1 - tr_now), "cvm_scale": scale,
                          "cvm_outstanding": last["outstanding"], "b3_vs_cvm": ratio}
        else:
            shares_now = shares_hist[-1] if shares_hist else None
        info = cad.loc[cnpj] if cnpj in cad.index else None
        annual = {}
        prev = None
        for y in years:
            a = {k: r2(c["annual"][y].get(k)) for k in FLOW_KEYS + BS_KEYS}
            a["ratios"] = ratios({k: (x if x is not None else np.nan) for k, x in a.items()}, prev)
            annual[y] = a
            prev = {k: (x if x is not None else np.nan) for k, x in a.items()}
        ltm_d = None
        if ltm_flows:
            ltm_d = {k: r2(ltm_flows.get(k)) for k in FLOW_KEYS}
            merged = {**{k: (x if x is not None else np.nan) for k, x in ltm_d.items()}, **{k: (bs_latest.get(k) if bs_latest.get(k) is not None else np.nan) for k in BS_KEYS}}
            ltm_d["ratios"] = ratios(merged, {k: (annual[years[-1]].get(k) if annual[years[-1]].get(k) is not None else np.nan) for k in BS_KEYS})
        qlabel = lambda k: f"{k[-1]}T{k[2:4]}"
        rev = [annual[y].get("revenue") for y in years]
        def cagr(series, n=5):
            s = [x for x in series if x is not None]
            if len(series) > n and series[-1] and series[-1 - n] and series[-1] > 0 and series[-1 - n] > 0:
                return round((series[-1] / series[-1 - n]) ** (1 / n) - 1, 4)
            return None
        doc = {
            "ticker": tk, "cnpj": cnpj, "in_coverage": tk in cov,
            "cvm_code": info.CD_CVM if info is not None else None,
            "name": info.DENOM_COMERC if info is not None and isinstance(info.DENOM_COMERC, str) else (info.DENOM_SOCIAL if info is not None else tk),
            "sector_cvm": info.SETOR_ATIV if info is not None else None,
            "fin_type": c["ftype"], "is_financial": c["ftype"] is not None,
            "shares_per_unit": UNITS.get(tk, 1),
            "basis_latest": c["annual"][years[-1]].get("basis"),
            "latest_quarter": last_q, "latest_quarter_label": qlabel(last_q) if last_q else None,
            "balance_date": bs_latest.get("date"),
            "units": "R$ milhões",
            "shares": shares_now,
            "shares_history": shares_hist,
            "annual": annual,
            "quarterly": {k: {kk: r2(vv) for kk, vv in q.items()} for k, q in sorted(quarters.items(), key=lambda kv: (int(kv[0][:4]), int(kv[0][-1])))},
            "balance_quarterly": {k: {kk: (r2(vv) if kk != "date" else vv) for kk, vv in b.items()} for k, b in c["bs_q"].items()},
            "ltm": ltm_d, "ltm_label": f"LTM {qlabel(last_q)}" if last_q and ltm_d else None,
            "balance": {k: (r2(bs_latest.get(k)) if k != "date" else bs_latest.get(k)) for k in BS_KEYS + ["date"]},
            "growth": {"revenue_cagr_5y": cagr(rev), "revenue_cagr_3y": cagr(rev, 3),
                       "ni_cagr_5y": cagr([annual[y].get("ni_controlling") for y in years]),
                       "ebitda_cagr_5y": cagr([annual[y].get("ebitda") for y in years])},
        }
        raw_keys = list(years[-3:]) + ([last_q] if last_q and int(last_q[:4]) > int(years[-1][2:]) else [])
        doc["raw"] = raw_lines(c, raw_keys)
        json.dump(doc, open(out_dir / f"{tk}.json", "w"), ensure_ascii=False)
        print("ok", tk, flush=True)
        summary.append((tk, doc["fin_type"], last_q, annual[years[-1]].get("revenue"), annual[years[-1]].get("ni_controlling"), doc["balance"].get("net_debt")))
    for s in summary:
        if s[0] in cov:
            print(*s)


if __name__ == "__main__":
    main(*sys.argv[1:7])
