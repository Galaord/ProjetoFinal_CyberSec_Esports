#!/usr/bin/env python3
"""NEXUS ARENA v2 — orquestrador. Cada execução -> linha CSV com achado completo."""

import csv, importlib, os, sys, time, traceback
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from lib import common, config
from lib.common import Ctx, resultado

PESO = {"crit": 25, "alto": 10, "medio": 4, "baixo": 1, "info": 0}
COR = {"crit": "\033[95m", "alto": "\033[91m", "medio": "\033[93m",
       "baixo": "\033[94m", "info": "\033[90m"}
RESET = "\033[0m"

CATALOGO = [
    ("Reconhecimento", [
        ("M01", "m01_reach",  "Alcance do host / ICMP / rota"),
        ("M02", "m02_ports",  "Portas, serviços e versões (nmap)"),
        ("M03", "m03_finger", "Fingerprint da aplicação"),
        ("M04", "m04_tls",    "HTTPS / HSTS / certificado"),
    ]),
    ("Configuração HTTP", [
        ("M05", "m05_headers",   "Cabeçalhos de segurança"),
        ("M06", "m06_cookies",   "Flags de cookie"),
        ("M07", "m07_methods",   "Métodos HTTP"),
        ("M08", "m08_clickjack", "Clickjacking"),
        ("M09", "m09_csrf",      "Protecção CSRF"),
    ]),
    ("Exposição de informação", [
        ("M10", "m10_host",   "Host header / debug / SECRET_KEY"),
        ("M11", "m11_debug",  "Tracebacks e DEBUG (500)"),
        ("M12", "m12_files",  "Ficheiros sensíveis"),
        ("M13", "m13_paths",  "Caminhos Django"),
        ("M14", "m14_admin",  "Painel /admin/"),
        ("M15", "m15_dump",   "Dados sem autenticação"),
        ("M16", "m16_enum",   "Enumeração de contas"),
    ]),
    ("Autenticação", [
        ("M17", "m17_brute",  "Brute force de login"),
        ("M18", "m18_sqlmap", "sqlmap"),
        ("M23", "m23_post",   "Pós-exploração com credenciais"),
    ]),
    ("Dados e stack", [
        ("M19", "m19_mysql", "MySQL / credenciais da BD"),
        ("M20", "m20_xampp", "XAMPP e phpMyAdmin (80/8080)"),
        ("M24", "m24_eol",   "Versões e fim de suporte"),
    ]),
    ("Fecho", [
        ("M21", "m21_nikto",  "Nikto"),
        ("M22", "m22_report", "Relatório consolidado"),
    ]),
]

TODOS = {mid: mod for _, g in CATALOGO for mid, mod, _ in g}


def banner():
    print(r"""
 _   _ ________  ___   _ _____     _    ____  _____ _   _
| \ | |  ___\  \/  |  / /  ___|   / \  |  _ \|  ___| \ | |
|  \| | |__  \  /| | / /| |__    / _ \ | |_) | |__ |  \| |
| . ` |  __| /  \| |/ / |  __|  / ___ \|  _ <|  __|| . ` |
| |\  | |___/ /  \  /  | |___ / /   \ \ |_) | |___| |\  |
|_| \_|_____/_/\_\_/   |_____/_/     \_\____/|_____|_| \_|
        v2 — achados com evidência, impacto e correção
""")


def sessao_nova():
    d = os.path.join(BASE, "resultados",
                     "sessao_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(os.path.join(d, "logs"), exist_ok=True)
    os.makedirs(os.path.join(d, "evidencias"), exist_ok=True)
    p = os.path.join(d, "resultados.csv")
    with open(p, "w", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerow([
            "scan_id", "inicio", "fim", "duracao_s", "modulo", "severidade",
            "alvo", "titulo", "evidencia", "impacto", "exploracao",
            "correcao", "log_bruto", "output"])
    return d, p


def registar(p, linha):
    with open(p, "a", newline="", encoding="utf-8") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerow(linha)


def mostrar(res):
    for a in res.get("achados", []):
        c = COR.get(a["sev"], "")
        print(f"  {c}[{a['sev'].upper()}]{RESET} {a['titulo']}")
        print(f"      evidência: {a['evidencia']}")
        print(f"      impacto  : {a['impacto']}")
        for e in a["explorar"]:
            print(f"      explorar : {e}")
        if a["corrigir"]:
            print(f"      corrigir : {a['corrigir']}")


def executar(mid, modname, ctx, csv_path):
    sid, inicio, t0 = common.novo_id(), common.now(), common.cronometro()
    print(f"\n\033[96m>>> [{mid}] {modname} — {inicio}{RESET}")
    try:
        res = importlib.import_module(f"modules.{modname}").run(ctx) or resultado()
    except KeyboardInterrupt:
        raise
    except Exception:
        res = resultado(traceback.format_exc(),
                        [common.achado("baixo", "Módulo falhou",
                                       traceback.format_exc().splitlines()[-1],
                                       "Resultado deste módulo não é fiável",
                                       corrigir="Ver log do módulo")])

    dur, fim = round(common.cronometro() - t0, 2), common.now()
    out = common.trunc(res.get("output", ""))
    log = ctx.log(mid, res.get("output", ""))

    if out.strip():
        print(out)
    mostrar(res)
    print(f"\033[96m<<< [{mid}] fim {fim} ({dur}s) — severidade máxima: {res['sev']}{RESET}")

    for a in res.get("achados", []) or [{"sev": "info", "titulo": "-", "evidencia": "-",
                                         "impacto": "-", "explorar": [], "corrigir": ""}]:
        registar(csv_path, [
            sid, inicio, fim, dur, mid, a["sev"], ctx.base_url,
            a["titulo"], a["evidencia"], a["impacto"],
            " ; ".join(a["explorar"]), a["corrigir"], log, out])
    return res


def risco(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    score = min(100, sum(PESO.get(l["severidade"], 0) for l in linhas))
    banda = ("CRÍTICO" if score >= 60 else "ALTO" if score >= 35
             else "MÉDIO" if score >= 15 else "BAIXO")
    return score, banda, linhas


def resumo(csv_path):
    score, banda, linhas = risco(csv_path)
    print(f"\n--- RESUMO DA SESSÃO: {score}/100 ({banda}) ---")
    for sev in ("crit", "alto", "medio", "baixo", "info"):
        grupo = [l for l in linhas if l["severidade"] == sev]
        if grupo:
            print(f"\n{COR[sev]}{sev.upper()} ({len(grupo)}){RESET}")
            for l in grupo:
                print(f"  - {l['modulo']} {l['titulo']}")
    print(f"\nCSV: {csv_path}")


def menu():
    print("\n" + "=" * 68)
    for sec, g in CATALOGO:
        print(f"  -- {sec} --")
        for mid, _, d in g:
            print(f"   {mid}  {d}")
    print("=" * 68)
    print("  A) TUDO   S) Resumo/risco   Q) Sair")


def main():
    banner()
    if not common.tcp_open(config.TARGET_IP, config.TARGET_PORT):
        print(f"\033[91m[!] {config.BASE_URL} sem resposta — verifica routing VLAN40->VLAN20\033[0m")

    sess, csv_path = sessao_nova()
    ctx = Ctx(sess)
    print(f"Sessão: {sess}\nAlvo: {config.BASE_URL} (Host: {config.HOST_HEADER})")

    while True:
        menu()
        try:
            op = input("\nOpção > ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            break
        if op in ("Q", "0", ""):
            break
        if op == "S":
            resumo(csv_path); continue
        if op == "A":
            for _, g in CATALOGO:
                for mid, mod, _ in g:
                    if mid != "M22":
                        executar(mid, mod, ctx, csv_path)
            executar("M22", "m22_report", ctx, csv_path)
            continue

        alvos = set()
        for parte in op.replace(" ", "").split(","):
            if "-" in parte:
                a, b = parte.split("-")
                if a.isdigit() and b.isdigit():
                    alvos |= {f"M{i:02d}" for i in range(int(a), int(b) + 1)}
            elif parte.isdigit():
                alvos.add(f"M{int(parte):02d}")
            elif parte in TODOS:
                alvos.add(parte)

        for mid in sorted(alvos):
            if mid in TODOS:
                executar(mid, TODOS[mid], ctx, csv_path)
            else:
                print(f"  ? {mid} inexistente")

    print(f"\nResultados em: {csv_path}")


if __name__ == "__main__":
    main()