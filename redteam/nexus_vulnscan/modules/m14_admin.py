from lib import common

META = {"id": "M14"}

def run(ctx):
    out, f = [], []
    r = common.http(ctx.url("/admin/"), follow=False)
    out.append(f"/admin/ -> {r['status']} {r['headers'].get('Location', '')}")

    if r["status"] in (200, 302):
        f.append(common.achado(
            "medio", "Painel de administração exposto",
            "/admin/ responde " + str(r["status"]),
            "Interface de gestão do Django acessível da VLAN40; alvo de brute force "
            "e de exploits de admin.",
            [f"curl -s http://{ctx.target}:8000/admin/login/"],
            "Restringir /admin/ por IP (Require ip) ou mudar o prefixo."))

    rr = common.post_form(ctx, "/admin/login/",
                          {"username": "admin", "password": "admin", "next": "/admin/"},
                          follow=False)
    out.append(f"POST login admin -> {rr['status']}")
    if rr["status"] == 500:
        f.append(common.achado(
            "alto", "Login do admin quebrado (500)",
            "POST /admin/login/ devolve 500 para qualquer credencial",
            "Nenhuma credencial funciona no admin; a gestão fica dependente da BD.",
            ["curl -s -o /dev/null -w '%{http_code}' -X POST http://%s:8000/admin/login/ -d 'username=a&password=b'" % ctx.target],
            "Definir AUTH_USER_MODEL e criar superuser; ver M11 para o traceback."))
    elif rr["status"] == 302 and "admin/" in rr["headers"].get("Location", ""):
        f.append(common.achado("alto", "admin:admin válido", "302 para /admin/",
                               "Acesso total de gestão", corrigir="Mudar a password."))
    return common.resultado("\n".join(out), f)