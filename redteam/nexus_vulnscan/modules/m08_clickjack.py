from lib import common

META = {"id": "M08"}

def run(ctx):
    r = common.http(ctx.url("/"))
    xfo = r["headers"].get("X-Frame-Options", "(ausente)")
    csp = r["headers"].get("Content-Security-Policy", "")
    out = [f"X-Frame-Options: {xfo}", f"CSP frame-ancestors: {'sim' if 'frame-ancestors' in csp else 'não'}"]
    f = []
    if xfo == "DENY":
        f.append(common.achado("info", "Clickjacking mitigado",
                               "X-Frame-Options: DENY", "A aplicação não pode ser embebida em iframes",
                               corrigir=""))
    elif not xfo and "frame-ancestors" not in csp:
        f.append(common.achado("baixo", "Sem protecção anti-clickjacking", "XFO e CSP ausentes",
                               "Botões podem ser sobrepostos em iframe",
                               corrigir="X_FRAME_OPTIONS = 'DENY' ou CSP frame-ancestors 'none'"))
    return common.resultado("\n".join(out), f)