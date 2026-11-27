from lib import common, config

META = {"id": "M01", "sev": "info"}

def run(ctx):
    out, f = [], []
    ctx.cmd(f"ping -c 3 {ctx.target}")
    rc, o, _ = common.sh(["ping", "-c", "3", "-W", "2", ctx.target], timeout=20)
    out.append(o)
    if rc == 0:
        f.append("Host responde a ICMP")
        rc2, o2, _ = common.sh(["ping", "-c", "1", "-W", "2", ctx.target], timeout=8)
        out.append(o2)
    else:
        f.append("Sem ICMP (pode estar filtrado)")
    rc3, o3, _ = common.sh(["ip", "route", "get", ctx.target], timeout=8)
    out.append("\n[rota]\n" + o3)
    return common.resultado("\n".join(out), f, "info")