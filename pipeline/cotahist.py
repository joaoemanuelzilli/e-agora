"""Série histórica oficial da B3 (COTAHIST) -> CSV diário por ticker (mercado à vista, lote padrão).

Uso: python pipeline/cotahist.py <dir_zips> <saida_csv_gz> [ano_ini] [ano_fim]
Preços NÃO ajustados (ajuste por proventos/eventos é feito em etapa posterior).
"""
import gzip
import io
import sys
import zipfile
from pathlib import Path


def parse_zip(path, out):
    n = 0
    with zipfile.ZipFile(path) as z:
        name = z.namelist()[0]
        with z.open(name) as fh:
            for raw in io.TextIOWrapper(fh, encoding="latin1"):
                if raw[0:2] != "01" or raw[24:27] != "010" or raw[10:12] not in ("02", "96"):
                    continue
                if raw[10:12] == "96":  # fracionário: ignora
                    continue
                tk = raw[12:24].strip()
                d = raw[2:10]
                f = lambda a, b: int(raw[a:b]) / 100.0
                out.write(
                    f"{d[0:4]}-{d[4:6]}-{d[6:8]},{tk},{f(56,69)},{f(69,82)},{f(82,95)},{f(108,121)},{f(95,108)},"
                    f"{int(raw[147:152])},{int(raw[152:170])},{f(170,188)},{int(raw[210:217])},{raw[230:242].strip()}\n"
                )
                n += 1
    return n


def main(zdir, out_path, y0=2016, y1=2026):
    with gzip.open(out_path, "wt") as out:
        out.write("date,ticker,open,high,low,close,avg,trades,qty,volume,fatcot,isin\n")
        for y in range(int(y0), int(y1) + 1):
            p = Path(zdir) / f"COTAHIST_A{y}.ZIP"
            if p.exists():
                print(y, parse_zip(p, out), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
