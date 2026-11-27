from lib import common

META = {"id": "M09"}

def run(ctx):
    out, f = [], []
    for caminho, campos in (
        ("/login/", {"nickname": "x", "password": "y"}),
        ("/registo/", {"nickname": "x", "email": "a@x.pt", "password": "y"}),
    ):
        r = common.http(ctx.url(caminho), "POST", data=campos)
        out.append(f"{caminho} POST sem token -> {r['status']}")
        if r["status"] == 403:
            f.append(common.achado("info", f"CSRF activo em {caminho}",
                                   "POST sem csrfmiddlewaretoken devolve 403",
                                   "Formulários protegidos contra submissão cruzada",
                                   corrigir=""))
        elif r["status"] in (200, 302):
            f.append(common.achado("alto", f"CSRF em falta em {caminho}",
                                   "POST sem token aceite", "Acções podem ser forçadas a partir de outro site",
                                   [f"curl -s -X POST http://{ctx.target}:8000{caminho} -d 'nickname=x&password=y'"],
                                   "Garantir {% csrf_token %} e CsrfViewMiddleware."))
    return common.resultado("\n".join(out), f)