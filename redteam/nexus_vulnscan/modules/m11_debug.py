import re
from lib import common

META = {"id": "M11"}

def run(ctx):
    out, f = [], []

    # /admin/login/ devolve 500 -> página de debug completa
    r = common.post_form(ctx, "/admin/login/",
                         {"username": "audit", "password": "audit", "next": "/admin/"},
                         follow=False)
    out.append(f"POST /admin/login/ -> {r['status']} ({len(r['body'])}B)")

    if r["status"] == 500:
        pag = r["body"]
        ctx.evidencia("M11_traceback_admin.html", pag)
        exc = re.search(r"<title>(.*?)</title>", pag, re.S)
        tipo = re.search(r"(django\.[\w.]+(?:Error|Exception)|[\w]+Error)", pag)
        sql = re.findall(r"(SELECT .{0,160})", pag)
        out.append("excepção: " + (tipo.group(1) if tipo else "?"))
        out.append("título: " + (exc.group(1).strip()[:200] if exc else "?"))

        f.append(common.achado(
            "alto", "Painel /admin/ rebenta com 500 no login",
            f"POST /admin/login/ -> 500; excepção {tipo.group(1) if tipo else 'não identificada'}; "
            f"traceback completo guardado em evidencias/M11_traceback_admin.html",
            "O admin está inutilizável (não há gestão de utilizadores/torneios pelo Django admin) "
            "e cada tentativa devolve stack trace com SQL e variáveis locais.",
            ["curl -s -X POST http://%s:8000/admin/login/ -d 'username=a&password=b' | head -80" % ctx.target],
            "Causa provável: AUTH_USER_MODEL não definido e 'Utilizador' não herda AbstractBaseUser, "
            "logo authenticate() falha. Definir AUTH_USER_MODEL='core.Utilizador' + criar superuser, "
            "ou usar django.contrib.auth.models.User."))

        if sql:
            out.append("SQL visível no traceback: " + sql[0])
            f.append(common.achado(
                "medio", "Queries SQL expostas no erro",
                sql[0][:160], "Revela esquema de tabelas e colunas reais.",
                corrigir="DEBUG=False e logging de SQL desligado em produção."))

    for p in ("/torneios/999999999999999999999/", "/torneios/abc/"):
        rr = common.http(ctx.url(p))
        out.append(f"{p} -> {rr['status']}")

    r2 = common.post_form(ctx, "/registo/", {
        "nickname": "A" * 300, "email": "overflow@audit.pt", "password": "x"}, follow=False)
    out.append(f"registo com nickname de 300 chars (max_length=50) -> {r2['status']}")
    if r2["status"] in (200, 302):
        f.append(common.achado(
            "baixo", "Sem validação de tamanho no registo",
            "nickname de 300 caracteres (limite 50) é aceite sem erro",
            "Dados truncados/desalinhados na BD; layout quebra em listagens.",
            ["curl -s -X POST http://%s:8000/registo/ -d \"nickname=$(python3 -c 'print(\"A\"*300)')\" -d 'email=a@a.pt' -d 'password=x'" % ctx.target],
            "Validar com forms.Form/ModelForm (max_length) em vez de request.POST directo."))

    if not f:
        f.append(common.achado("info", "Sem exposição de debug", "sem 500 nem traceback",
                               "Erros contidos", corrigir=""))
    return common.resultado("\n".join(out), f)