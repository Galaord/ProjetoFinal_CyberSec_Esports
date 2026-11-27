from lib import common

META = {"id": "M05", "sev": "medio"}

CHECKS = {
    "Strict-Transport-Security": "HSTS ausente",
    "Content-Security-Policy": "CSP ausente (XSS sem defesa em profundidade)",
    "X-Content-Type-Options": "X-Content-Type-Options ausente (MIME sniffing)",
    "Referrer-Policy": "Referrer-Policy ausente (fuga de URL)",
    "Permissions-Policy": "Permissions-Policy ausente",
    "X-Frame-Options": "X-Frame-Options ausente (clickjacking)",
}

def run(ctx):
    r = common.http(ctx.url("/"))
    out = [f"status={r['status']}"]
    for k, v in r["headers"].items():
        out.append(f"  {k}: {v}")
    f = [msg for h, msg in CHECKS.items() if h not in r["headers"]]
    sev = "medio" if len(f) >= 3 else ("baixo" if f else "info")
    return common.resultado("\n".join(out), f, sev)