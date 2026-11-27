import re
from lib import common

META = {"id": "M03", "sev": "baixo"}

def run(ctx):
    out, f = [], []
    ctx.cmd(f"whatweb {ctx.base_url}")
    rc, o, _ = common.sh(["whatweb", "--color=never", "-a", "3", ctx.base_url], timeout=90)
    out.append(o)
    r = common.http(ctx.url("/"))
    out.append(f"\n[GET /] status={r['status']}")
    for k, v in r["headers"].items():
        out.append(f"  {k}: {v}")
    srv = r["headers"].get("Server", "")
    if srv:
        f.append(f"Server: {srv}")
    if "DisallowedHost" in r["body"]:
        f.append("400 DisallowedHost -> usar Host: localhost")
    if re.search(r"Django", " ".join(r["headers"].values()) + r["body"][:4000], re.I):
        f.append("Stack Django confirmada")
    return common.resultado("\n".join(out), f, "baixo" if f else "info")