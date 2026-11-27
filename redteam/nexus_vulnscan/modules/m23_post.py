from lib import common

META = {"id": "M23"}

def run(ctx):
    out, f = [], []
    creds = ctx.state.get("creds")
    if not creds:
        ok, _ = common.login(ctx, "admin", "password")
        creds = ("admin", "password") if ok else None

    if not creds:
        return common.resultado("sem credenciais (corre M17)", [common.achado(
            "info", "Sem credenciais para pós-exploração", "M17 não encontrou nada",
            "", corrigir="")])

    user, pw = creds
    ok, r = common.login(ctx, user, pw)
    out.append(f"login {user}:{pw} -> {'OK' if ok else 'falhou'}")

    sess = common.http(ctx.url("/"))
    sid = next((c for c in sess["set_cookie"] if c.startswith("sessionid")), None)
    if sid:
        out.append("sessionid obtido: " + sid.split(";")[0])
        f.append(common.achado(
            "alto", "Sessão capturada em texto limpo",
            sid.split(";")[0] + "  (reutilizável com curl -b)",
            "Quem observar a rede reutiliza a conta sem saber a password. "
            "O cookie pode ser copiado para outro cliente.",
            [f"curl -b 'sessionid=VALOR' http://{ctx.target}:8000/teste/"],
            "SESSION_COOKIE_SECURE + HTTPS."))

    for caminho, nome in (("/teste/", "dados internos"), ("/comunidade/", "listagem")):
        rr = common.http(ctx.url(caminho))
        out.append(f"{caminho} autenticado -> {rr['status']} ({len(rr['body'])}B)")
        if "Online" in rr["body"]:
            f.append(common.achado("info", f"Acesso autenticado a {nome}",
                                   f"{caminho} mostra estado Online", "Área autenticada alcançada",
                                   corrigir=""))

    rr = common.http(ctx.url("/logout/"))
    out.append(f"/logout/ -> {rr['status']} (sessão terminada: {'Sim' if 'Sessão terminada' in rr['body'] else '?'})")
    return common.resultado("\n".join(out), f)