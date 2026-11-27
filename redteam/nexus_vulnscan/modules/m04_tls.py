from lib import common, config

META = {"id": "M04", "sev": "baixo"}

def run(ctx):
    out, f = [], []
    for porta in (443, 8443):
        if common.tcp_open(ctx.target, porta):
            f.append(f"TLS aberto na porta {porta}")
            url = f"https://{ctx.target}:{porta}/"
            ctx.cmd(f"openssl s_client -connect {ctx.target}:{porta}")
            rc, o, _ = common.sh(
                ["openssl", "s_client", "-connect", f"{ctx.target}:{porta}",
                 "-servername", ctx.target], timeout=20)
            out.append(o[:4000])
    r = common.http(ctx.url("/"), follow=False)
    out.append(f"[GET / sem seguir] status={r['status']} Location={r['headers'].get('Location')}")
    if r["status"] != 301 and r["status"] != 302:
        f.append("Sem redirect para HTTPS (tráfego em claro)")
    else:
        loc = r["headers"].get("Location", "")
        if loc.startswith("http://"):
            f.append("Redirect fraco: continua em http://")
    r2 = common.http(ctx.url("/"), host_header="__cfg__", follow=False)
    out.append(f"[HSTS] Strict-Transport-Security: {r2['headers'].get('Strict-Transport-Security')}")
    if not r2["headers"].get("Strict-Transport-Security"):
        f.append("HSTS ausente")
    return common.resultado("\n".join(out), f, "baixo")