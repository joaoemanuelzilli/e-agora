"""Mapa de dividendos (B3 oficial): histórico completo de proventos em dinheiro por classe + pagamentos anunciados.

Uso: python pipeline/dividends.py <dir_raw_b3>
Lê research/_coverage.json, <dir_raw_b3>/supplement.json (nome de pregão e próximos pagamentos com data),
data/market/quotes.json (foto de preços) e data/model/{TICKER}.json (DPA projetado).
Saída: data/market/dividends.json
"""
import base64
import json
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
TODAY = date(2026, 10, 26)
START_YEAR = 2016
# units: (ações ON, ações PN, rótulo da PN) por unit
UNITS = {"BPAC11": (1, 2, "PNA"), "ENGI11": (1, 4, "PN"), "ALUP11": (1, 2, "PN"), "IGTI11": (1, 2, "PN")}
CLASS_BY_SUFFIX = {"3": ["ON"], "4": ["PN", "PNA"], "5": ["PNA"], "6": ["PNB"]}
TYPE = {"DIVIDENDO": "Dividendo", "JRS CAP PROPRIO": "JCP", "RENDIMENTO": "Rendimento"}


def fnum(s):
    try:
        return float(str(s).replace(".", "").replace(",", "."))
    except Exception:
        return None


def pdate(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except Exception:
        return None


def get_json(url, tries=4):
    for i in range(tries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=40) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def _hist_page(name, page, size=120):
    payload = {"language": "pt-br", "pageNumber": page, "pageSize": size, "tradingName": name}
    url = "https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedCashDividends/" + base64.b64encode(
        json.dumps(payload).encode()).decode()
    return get_json(url)


def history(names):
    """Todas as páginas de GetListedCashDividends. A API ordena por classe e depois por data, então lê tudo.
    O nome de pregão nem sempre é igual ao do suplemento (ex.: 'CURY S/A' x 'CURY S.A.'): tenta variações."""
    for name in names:
        d = _hist_page(name, 1)
        if not d or not (d.get("page") or {}).get("totalRecords"):
            continue
        rows = list(d.get("results") or [])
        for page in range(2, ((d.get("page") or {}).get("totalPages") or 1) + 1):
            dd = _hist_page(name, page)
            if dd:
                rows.extend(dd.get("results") or [])
        return name, rows
    return None, []


def name_variants(sup_name, detail):
    base = (sup_name or "").strip()
    cands = [sup_name, base, base.replace("S/A", "S.A."), base.replace("S.A.", "S/A"), (detail or {}).get("tradingName"),
             ((detail or {}).get("tradingName") or "").replace("S/A", "S.A.")]
    out = []
    for c in cands:
        if c and c not in out:
            out.append(c)
    return out


def class_events(rows, ticker):
    """Eventos por data-com para a classe negociada (units = ON + k × PN)."""
    if ticker in UNITS:
        n_on, n_pn, pn_lab = UNITS[ticker]
        acc = defaultdict(lambda: {"valor": 0.0, "tipos": set(), "aprov": None, "preco": None})
        for r in rows:
            dc = pdate(r.get("lastDatePriorEx"))
            v = fnum(r.get("valueCash"))
            if not dc or v is None:
                continue
            mult = n_on if r.get("typeStock") == "ON" else (n_pn if r.get("typeStock") in (pn_lab, "PN") else 0)
            if not mult:
                continue
            key = (dc, TYPE.get(r.get("corporateAction"), r.get("corporateAction")))
            acc[key]["valor"] += v * mult
            acc[key]["aprov"] = r.get("dateApproval")
        return [{"dc": dc.isoformat(), "tipo": tp, "valor": round(a["valor"], 6), "aprov": a["aprov"], "preco_dc": None, "yield_dc": None}
                for (dc, tp), a in sorted(acc.items())]
    classes = CLASS_BY_SUFFIX.get(ticker[4:], ["ON"])
    present = {r.get("typeStock") for r in rows}
    cls = next((c for c in classes if c in present), None)
    if cls is None:
        return []
    ev = []
    for r in rows:
        if r.get("typeStock") != cls:
            continue
        dc = pdate(r.get("lastDatePriorEx"))
        v = fnum(r.get("valueCash"))
        if not dc or v is None or v <= 0:
            continue
        ev.append({"dc": dc.isoformat(), "tipo": TYPE.get(r.get("corporateAction"), r.get("corporateAction")), "valor": round(v, 6),
                   "aprov": r.get("dateApproval"), "preco_dc": fnum(r.get("closingPricePriorExDate")),
                   "yield_dc": (fnum(r.get("corporateActionPrice")) or 0) / 100 or None})
    return sorted(ev, key=lambda e: e["dc"])


def guess_isin(sup, ticker):
    isins = sorted({e.get("isinCode") for e in (sup or {}).get("cashDividends") or [] if e.get("isinCode")})
    if ticker in UNITS:
        pats = ["CDAM", "UNT"]
    else:
        pats = {"3": ["ACNOR"], "4": ["ACNPR", "ACNPA"], "5": ["ACNPA"], "6": ["ACNPB"]}.get(ticker[4:], ["ACNOR"])
    for p in pats:
        for i in isins:
            if p in i:
                return i
    return None


def supplement_events(sup, isin_by_ticker, ticker):
    """Eventos do suplemento B3 (≈12 meses, com data de pagamento) da classe negociada."""
    isin = isin_by_ticker.get(ticker) or guess_isin(sup, ticker)
    out = []
    for e in (sup or {}).get("cashDividends") or []:
        if isin and e.get("isinCode") != isin:
            continue
        dc, pay = pdate(e.get("lastDatePrior")), pdate(e.get("paymentDate"))
        if pay and pay.year >= 2100:
            pay = None
        v = fnum(e.get("rate"))
        if v is None:
            continue
        out.append({"dc": dc.isoformat() if dc else None, "pagamento": pay.isoformat() if pay else None,
                    "tipo": TYPE.get(e.get("label"), e.get("label")), "valor": v, "ref": e.get("relatedTo"), "aprov": e.get("approvedOn")})
    return out


def attach_payment_dates(ev, sup_ev):
    pool = defaultdict(list)
    for e in sup_ev:
        if e["dc"] and e["pagamento"]:
            pool[(e["dc"], round(e["valor"], 4))].append(e["pagamento"])
    for e in ev:
        k = (e["dc"], round(e["valor"], 4))
        if pool.get(k):
            e["pagamento"] = pool[k].pop(0)


def pay_calendar(sup_ev, price):
    """Caixa por mês de pagamento: 12 meses para trás e 12 para frente (eventos com data de pagamento)."""
    months = []
    y, m = TODAY.year, TODAY.month - 11
    while m <= 0:
        y, m = y - 1, m + 12
    for _ in range(24):
        months.append(f"{y}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    cal = {k: {"valor": 0.0, "eventos": []} for k in months}
    for e in sup_ev:
        if not e["pagamento"]:
            continue
        k = e["pagamento"][:7]
        if k in cal:
            cal[k]["valor"] += e["valor"]
            cal[k]["eventos"].append({"pagamento": e["pagamento"], "dc": e["dc"], "tipo": e["tipo"], "valor": e["valor"]})
    return [{"mes": k, "valor": round(v["valor"], 6), "dy": round(v["valor"] / price, 5) if price and v["valor"] else 0.0, "eventos": v["eventos"]} for k, v in cal.items()]


def upcoming(sup, isin_by_ticker, ticker):
    """Pagamentos anunciados com data de pagamento ≥ hoje (suplemento B3, por ISIN da classe negociada)."""
    isin = isin_by_ticker.get(ticker) or guess_isin(sup, ticker)
    out = []
    for e in (sup or {}).get("cashDividends") or []:
        if isin and e.get("isinCode") != isin:
            continue
        pay = pdate(e.get("paymentDate"))
        dc = pdate(e.get("lastDatePrior"))
        if pay and pay.year >= 2100:  # B3 usa 31/12/9999 para "data a definir"
            out.append({"dc": dc.isoformat() if dc else None, "pagamento": None, "a_definir": True, "tipo": TYPE.get(e.get("label"), e.get("label")),
                        "valor": fnum(e.get("rate")), "ref": e.get("relatedTo"), "aprov": e.get("approvedOn"), "da_direito_hoje": bool(dc and dc >= TODAY)})
            continue
        if pay and pay >= TODAY:
            out.append({"dc": dc.isoformat() if dc else None, "pagamento": pay.isoformat(), "tipo": TYPE.get(e.get("label"), e.get("label")),
                        "valor": fnum(e.get("rate")), "ref": e.get("relatedTo"), "aprov": e.get("approvedOn"),
                        "da_direito_hoje": bool(dc and dc >= TODAY)})
    return sorted(out, key=lambda e: e["pagamento"] or "9999")


def summarize(ev, price, proj_dps):
    by_year = defaultdict(lambda: {"total": 0.0, "div": 0.0, "jcp": 0.0, "n": 0})
    for e in ev:
        y = int(e["dc"][:4])
        if y < START_YEAR:
            continue
        b = by_year[y]
        b["total"] += e["valor"]
        b["n"] += 1
        b["jcp" if e["tipo"] == "JCP" else "div"] += e["valor"]
    d365 = date.fromordinal(TODAY.toordinal() - 365)
    ttm = [e for e in ev if date.fromisoformat(e["dc"]) > d365]
    ttm_total = sum(e["valor"] for e in ttm)
    # mês a mês dos últimos 12 meses (por data-com)
    months = []
    y, m = TODAY.year, TODAY.month
    for _ in range(12):
        months.append(f"{y}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    months = months[::-1]
    by_month = {k: {"valor": 0.0, "eventos": []} for k in months}
    for e in ttm:
        k = e["dc"][:7]
        if k in by_month:
            by_month[k]["valor"] += e["valor"]
            by_month[k]["eventos"].append({"dc": e["dc"], "tipo": e["tipo"], "valor": e["valor"]})
    # sazonalidade 2021–2025: fração do total anual por mês da data-com
    season = [0.0] * 12
    tot5 = 0.0
    for e in ev:
        yy = int(e["dc"][:4])
        if 2021 <= yy <= 2025:
            season[int(e["dc"][5:7]) - 1] += e["valor"]
            tot5 += e["valor"]
    season = [round(x / tot5, 4) if tot5 else 0.0 for x in season]
    yrs3 = [by_year.get(y, {"n": 0, "total": 0.0, "jcp": 0.0}) for y in (2023, 2024, 2025)]
    tot3 = sum(b["total"] for b in yrs3)
    paid_years = [y for y in range(2016, 2026) if by_year.get(y, {}).get("total", 0) > 0]
    return {
        "annual": [{"ano": y, **{k: round(v, 6) if isinstance(v, float) else v for k, v in by_year[y].items()}} for y in sorted(by_year)],
        "ttm": {"total": round(ttm_total, 6), "n": len(ttm), "dy": round(ttm_total / price, 5) if price else None,
                "jcp_share": round(sum(e["valor"] for e in ttm if e["tipo"] == "JCP") / ttm_total, 4) if ttm_total else None},
        "months": [{"mes": k, "valor": round(v["valor"], 6), "dy": round(v["valor"] / price, 5) if price and v["valor"] else 0.0, "eventos": v["eventos"]} for k, v in by_month.items()],
        "season_2021_2025": season,
        "freq_3y": round(sum(b["n"] for b in yrs3) / 3, 1),
        "jcp_share_3y": round(sum(b["jcp"] for b in yrs3) / tot3, 4) if tot3 else None,
        "anos_com_pagamento_10a": len(paid_years),
        "proj_dps": [round(x, 6) if x is not None else None for x in proj_dps],
        "proj_dy": [round(x / price, 5) if price and x is not None else None for x in proj_dps],
        "proj_3y_total_dy": round(sum(x for x in proj_dps[:3] if x is not None) / price, 5) if price and proj_dps else None,
    }


def main(raw_b3):
    raw = Path(raw_b3)
    (raw / "dividends").mkdir(exist_ok=True)
    sup = json.load(open(raw / "supplement.json"))
    cov = json.load(open(ROOT / "research" / "_coverage.json"))["coverage"]
    quotes = json.load(open(ROOT / "data" / "market" / "quotes.json"))
    issuers = sorted({c["ticker"][:4] for c in cov})

    det = json.load(open(raw / "details.json")) if (raw / "details.json").exists() else {}

    def fetch(iss):
        cache = raw / "dividends" / f"{iss}.json"
        if os.environ.get("EAGORA_SNAPSHOT") == "1" and cache.exists():  # rodada da foto: histórico já baixado
            return iss, json.load(open(cache)).get("rows") or []
        s = sup.get(iss) or {}
        used, rows = history(name_variants(s.get("tradingName"), det.get(iss)))
        json.dump({"name": used, "rows": rows}, open(raw / "dividends" / f"{iss}.json", "w"), ensure_ascii=False)
        return iss, rows

    with ThreadPoolExecutor(max_workers=6) as ex:
        hist = dict(ex.map(fetch, issuers))
    # ISIN negociado de cada ticker (último pregão)
    isin_by_ticker = {}
    for c in cov:
        mfile = ROOT / "data" / "market" / f"{c['ticker']}.json"
        if mfile.exists():
            st = json.load(open(mfile))
            isin_by_ticker[c["ticker"]] = st.get("isin")
    out = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "fonte": "B3: proventos em dinheiro (histórico) e suplemento (pagamentos anunciados)",
           "hoje": TODAY.isoformat(), "empresas": []}
    for c in cov:
        tk = c["ticker"]
        price = (quotes.get(tk) or {}).get("price")
        m = {}
        mp = ROOT / "data" / "model" / f"{tk}.json"
        if mp.exists():
            m = json.load(open(mp))
        unit = (m.get("shares") or {}).get("per_unit") or 1
        proj = [x * unit for x in (m.get("dps") or [])][:5] if m.get("dps") else []
        ev = class_events(hist.get(tk[:4]) or [], tk)
        sup_ev = supplement_events(sup.get(tk[:4]), isin_by_ticker, tk)
        if not ev and sup_ev:  # histórico indisponível: usa os 12 meses do suplemento
            ev = [{k: e[k] for k in ("dc", "tipo", "valor", "aprov")} | {"preco_dc": None, "yield_dc": None, "fonte": "suplemento"} for e in sup_ev if e["dc"]]
        attach_payment_dates(ev, sup_ev)
        # base de ações atual: divide proventos antigos pelos desdobramentos/bonificações posteriores à data-com
        mfile = ROOT / "data" / "market" / f"{tk}.json"
        splits = (json.load(open(mfile)).get("stats") or {}).get("split_events") or [] if mfile.exists() else []
        for e in ev:
            f = 1.0
            for sd, mult in splits:
                if sd >= e["dc"]:
                    f *= mult
            if abs(f - 1) > 1e-9:
                e["valor_original"] = e["valor"]
                e["valor"] = round(e["valor"] / f, 6)
                e["ajuste_eventos"] = round(f, 6)
        up = upcoming(sup.get(tk[:4]), isin_by_ticker, tk)
        s = summarize(ev, price, proj)
        s["pay_calendar"] = pay_calendar(sup_ev, price)
        out["empresas"].append({"ticker": tk, "nome": c["name"], "preco_ref": price, "eventos": [e for e in ev if int(e["dc"][:4]) >= START_YEAR],
                                "a_pagar": up, **s})
        print(f"{tk:7s} eventos={len(ev):4d} ttm={s['ttm']['total']:.4f} dy_ttm={s['ttm']['dy']} a_pagar={len(up)} freq={s['freq_3y']}")
    json.dump(out, open(ROOT / "data" / "market" / "dividends.json", "w"), ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main(sys.argv[1])
