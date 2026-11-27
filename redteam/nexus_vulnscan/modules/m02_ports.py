from lib import common, config

META = {"id": "M02"}

def run(ctx):
    out, f = [], []
    cmd = ["nmap", "-sT", "-Pn", "-n", "-p", config.PORTS_TOP, "--open",
           "-sV", "--version-light", "-T4", "--host-timeout", "240s", ctx.target]
    ctx.cmd(" ".join(cmd))
    rc, o, _ = common.sh(cmd, timeout=300)
    out.append(o)

    abertas = [l.split("/")[0] for l in o.splitlines() if "/tcp" in l and " open " in l]
    out.append(f"\nportas abertas: {abertas}")

    if "3306" in abertas:
        f.append(common.achado(
            "alto", "MySQL/MariaDB exposto à rede",
            "3306/tcp aberto a partir da VLAN40",
            "Superfície de ataque directa à base de dados; se a autenticação ceder, "
            "dá acesso a todas as tabelas (incluindo passwords em texto limpo).",
            [f"nc -zv {ctx.target} 3306",
             f"mysql -h {ctx.target} -u root --connect-timeout=5"],
            "Ligar o MariaDB a 127.0.0.1 no my.ini e expor só via app, ou filtrar 3306 por ACL."))

    for p in ("80", "8080"):
        if p in abertas:
            f.append(common.achado(
                "medio", f"Stack XAMPP exposta na porta {p}",
                f"{p}/tcp a servir Apache 2.4.58 (Win64) PHP 8.2.12",
                "Acesso directo ao Apache/PHP fora da aplicação Django: painel XAMPP, "
                "phpMyAdmin e ficheiros do directório htdocs.",
                [f"curl -s http://{ctx.target}:{p}/dashboard/"],
                "Publicar só a porta da aplicação e restringir o Apache com Require ip."))

    if "8000" in abertas:
        f.append(common.achado(
            "medio", "Django em runserver",
            "8000/tcp com WSGIServer CPython (servidor de desenvolvimento)",
            "runserver é mono-processo, sem hardening de estáticos e reinicia com o código.",
            [f"curl -sI http://{ctx.target}:8000/"],
            "Passar a gunicorn/waitress atrás de IIS ou nginx."))

    if not f:
        f.append(common.achado("info", "Sem serviços de risco", str(abertas),
                               "Superfície reduzida", corrigir=""))
    return common.resultado("\n".join(out), f)