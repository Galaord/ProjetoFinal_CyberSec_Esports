from lib import common

META = {"id": "M07"}

def run(ctx):
    out, f = [], []
    for m in ("OPTIONS", "TRACE", "PUT", "DELETE", "PATCH"):
        r = common.http(ctx.url("/"), method=m)
        nota = " (403 = CSRF, não 405)" if r["status"] == 403 else ""
        out.append(f"{m:8} -> {r['status']}{nota}")
        if m == "TRACE" and r["status"] == 200:
            f.append(common.achado(
                "baixo", "TRACE activo",
                "TRACE / -> 200", "Cross-Site Tracing: permite ler cabeçalhos e cookies "
                "via XSS em clientes antigos.",
                ["curl -sX TRACE http://%s/" % ctx.target + ":8000/"],
                "Desactivar TraceEnable no servidor frontal."))
    if not f:
        f.append(common.achado("info", "Métodos sem risco",
                               "PUT/DELETE/PATCH rejeitados com 403",
                               "Superfície de escrita limitada", corrigir=""))
    return common.resultado("\n".join(out), f)