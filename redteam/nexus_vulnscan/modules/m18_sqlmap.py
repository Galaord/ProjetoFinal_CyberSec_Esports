import os, shutil
from lib import common

META = {"id": "M18"}

def run(ctx):
    out, f = [], []
    if not shutil.which("sqlmap"):
        return common.resultado("sqlmap ausente", [common.achado(
            "info", "sqlmap não instalado", "apt install sqlmap", "", corrigir="")])

    cookie, tok, _ = common.csrf("/login/", ctx)
    base = ["sqlmap", "--batch", "--smart", "--timeout", "12", "--retries", "1",
            "--output-dir", os.path.join(ctx.logdir, "sqlmap")]

    testes = [
        ("GET /torneios/1/", base + ["-u", ctx.url("/torneios/1/*")]),
        ("POST /login/ (nickname)", base + [
            "-u", ctx.url("/login/"),
            "--data", f"csrfmiddlewaretoken={tok or ''}&nickname=admin&password=x",
            "--csrf-token", "csrfmiddlewaretoken",
            "--cookie", f"csrftoken={cookie or ''}",
            "-p", "nickname"]),
    ]

    for nome, cmd in testes:
        ctx.cmd(" ".join(cmd))
        rc, o, _ = common.sh(cmd, timeout=420)
        out.append(f"--- {nome}\n{o[-5000:]}")
        if "is vulnerable" in o:
            f.append(common.achado(
                "alto", f"Injecção SQL em {nome}",
                [l for l in o.splitlines() if "vulnerable" in l][0][:200],
                "Extracção directa da BD por HTTP, sem depender do MySQL exposto.",
                [" ".join(cmd) + " --dbs --dump"],
                "Usar ORM/parametrização (já usado) e validar tipos."))

    if not f:
        f.append(common.achado(
            "info", "Sem injecção SQL detectada",
            "parâmetros testados (path int, nickname POST) não reactivos",
            "Django ORM parametriza; o risco de SQLi aqui é baixo",
            corrigir=""))
    return common.resultado("\n".join(out), f)