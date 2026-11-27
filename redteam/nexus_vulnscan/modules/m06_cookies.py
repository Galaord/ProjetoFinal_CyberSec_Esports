from lib import common

META = {"id": "M06"}

def run(ctx):
    out, f = [], []
    for caminho in ("/", "/login/", "/registo/"):
        r = common.http(ctx.url(caminho))
        for c in r["set_cookie"]:
            out.append(f"{caminho}  {c}")

    r = common.http(ctx.url("/login/"))
    csrf = next((c for c in r["set_cookie"] if c.startswith("csrftoken")), "")
    if csrf:
        if "secure" not in csrf.lower():
            f.append(common.achado(
                "medio", "Cookie csrftoken sem Secure",
                "Set-Cookie: " + csrf.split(";")[0] + " … SameSite=Lax (sem Secure)",
                "Em HTTP simples o token viaja em claro e pode ser lido numa rede "
                "partilhada. HttpOnly no csrftoken é omitido de propósito (JS usa-o).",
                ["tcpdump -i eth0 -A 'tcp port 8000' | grep -i csrftoken"],
                "SESSION_COOKIE_SECURE = True e CSRF_COOKIE_SECURE = True (exige HTTPS)."))
        if "samesite" not in csrf.lower():
            f.append(common.achado("baixo", "Cookie sem SameSite",
                                   csrf.split(";")[0], "CSRF cross-site facilitado",
                                   corrigir="CSRF_COOKIE_SAMESITE = 'Lax'"))

    ok, _ = common.login(ctx, "admin", "password")
    if ok:
        s = next((c for c in common.http(ctx.url("/")).get("set_cookie", [])
                  if c.startswith("sessionid")), "")
        r2 = common.http(ctx.url("/teste/"))
        out.append(f"[sessão autenticada] sessionid: {s.split(';')[0] if s else '(não reenviado)'}")
        if s and "httponly" not in s.lower():
            f.append(common.achado("alto", "sessionid sem HttpOnly",
                                   s.split(";")[0], "Roubo de sessão via XSS",
                                   corrigir="SESSION_COOKIE_HTTPONLY = True (já é o default; verificar)"))
        if s and "secure" not in s.lower():
            f.append(common.achado("alto", "sessionid sem Secure",
                                   "sessionid transmitido em HTTP",
                                   "Sniffing da rede entrega a conta sem brute force.",
                                   ["tcpdump -i eth0 -A 'tcp port 8000' | grep -i sessionid"],
                                   "SESSION_COOKIE_SECURE = True + HTTPS."))
        out.append(f"confirmação autenticada /teste/: {'Online' if 'Online' in r2['body'] else '?'}")
    return common.resultado("\n".join(out), f)