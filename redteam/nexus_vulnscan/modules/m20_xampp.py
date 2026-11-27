import re
from lib import common, config

META = {"id": "M20"}

CAMINHOS = ["/xampp/", "/dashboard/", "/phpmyadmin/", "/security/", "/applications.html",
            "/img/", "/phpinfo.php", "/server-status", "/webalizer/"]

def run(ctx):
    out, f = [], []
    for porta in config.XAMPP_PORTS:
        if not common.tcp_open(ctx.target, porta):
            out.append(f"porta {porta} fechada")
            continue
        for c in CAMINHOS:
            r = common.http(ctx.xampp(c, porta), host_header=None, follow=False)
            out.append(f"{porta} {r['status']:3} {len(r['body']):6}B {c}")

            if r["status"] == 200 and c == "/dashboard/":
                m = re.search(r"XAMPP[^<]{0,40}", r["body"])
                f.append(common.achado(
                    "medio", f"Dashboard XAMPP acessível na porta {porta}",
                    (m.group(0) if m else "dashboard") + f" -> 200 em /dashboard/",
                    "Confirma a stack e o estado dos serviços; ponto de partida para "
                    "phpMyAdmin, phpinfo e ficheiros do htdocs.",
                    [f"curl -s http://{ctx.target}:{porta}/dashboard/"],
                    "Proteger com auth ou restringir por IP no httpd.conf."))

            if r["status"] == 200 and c == "/applications.html":
                f.append(common.achado(
                    "baixo", f"Lista de aplicações XAMPP exposta (porta {porta})",
                    "/applications.html -> 200",
                    "Inventário das ferramentas instaladas (phpMyAdmin, Webalizer, etc.).",
                    [f"curl -s http://{ctx.target}:{porta}/applications.html"],
                    "Remover páginas de exemplo."))

            if c == "/phpmyadmin/":
                if r["status"] == 403:
                    f.append(common.achado(
                        "medio", f"phpMyAdmin existe mas bloqueado (403) na porta {porta}",
                        "403 Forbidden — barrado por httpd.conf (Require local)",
                        "O bloqueio é por IP de origem: com shell no host, túnel SSH ou "
                        "X-Forwarded-For manipulado, o painel abre e o root sem password dá a BD toda.",
                        [f"curl -sI http://{ctx.target}:{porta}/phpmyadmin/",
                         f"ssh -L 8080:127.0.0.1:{porta} utilizador@{ctx.target}  # abrir localmente"],
                        "Manter o Require local e definir password ao root do MySQL."))
                elif r["status"] == 200:
                    f.append(common.achado(
                        "alto", f"phpMyAdmin aberto na porta {porta}",
                        "formulário de login acessível",
                        "Interface web à BD; com root sem password é dump total pelo browser.",
                        [f"firefox http://{ctx.target}:{porta}/phpmyadmin/  # root / (vazio)"],
                        "Definir password ao root e restringir por IP."))
    return common.resultado("\n".join(out), f)