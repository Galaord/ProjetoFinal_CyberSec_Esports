import shutil
from lib import common

META = {"id": "M21"}

def run(ctx):
    if not shutil.which("nikto"):
        return common.resultado("nikto ausente", [common.achado(
            "info", "nikto não instalado", "apt install nikto", "", corrigir="")])

    # sem -vhost/-ask (quebram a ligação na 2.6.1); o IP já é aceite pelo ALLOWED_HOSTS
    cmd = ["nikto", "-h", ctx.base_url, "-nointeractive", "-nolookup",
           "-maxtime", "150s", "-Tuning", "123b"]
    ctx.cmd(" ".join(cmd))
    rc, out, _ = common.sh(cmd, timeout=260)

    if "Unable to connect" in out:
        return common.resultado(out, [common.achado(
            "baixo", "nikto não conseguiu ligar",
            "ver log; testar com 'nikto -h http://IP:8000/ -nolookup'",
            "Cobertura de checks genéricos em falta", corrigir="")])

    itens = [l.strip() for l in out.splitlines()
             if l.strip().startswith("+") and not l.startswith("+ Target")
             and "Server:" not in l and "root page" not in l]
    f = []
    if itens:
        f.append(common.achado(
            "medio", f"{len(itens)} observações do nikto",
            itens[0][:200] + (" …" if len(itens) > 1 else ""),
            "Configuração do servidor com detalhes reveladores (ver output completo).",
            [f"nikto -h {ctx.base_url} -Tuning 123b"],
            "Rever cada linha do output e fechar o que não for necessário."))
    return common.resultado(out, f)