import re
from lib import common, config

META = {"id": "M24"}

def run(ctx):
    out, f = [], []
    alvos = {}

    for porta in config.XAMPP_PORTS:
        r = common.http(f"http://{ctx.target}:{porta}/", host_header=None, follow=False)
        srv = r["headers"].get("Server", "")
        if srv:
            alvos[porta] = srv
            out.append(f"porta {porta}: {srv}")

    r = common.http(ctx.url("/"))
    alvos["django"] = r["headers"].get("Server", "") + " | " + r["headers"].get("X-Powered-By", "")
    out.append("aplicação: " + alvos["django"])

    for chave, motivo in config.EOL.items():
        for onde, valor in alvos.items():
            if chave.split()[0].lower() in valor.lower():
                f.append(common.achado(
                    "medio", f"{chave} fora de suporte",
                    f"{motivo} — detectado em {onde}: {valor[:90]}",
                    "Sem patches de segurança novos; CVEs recentes ficam por corrigir.",
                    [f"searchsploit '{chave}'"],
                    f"Actualizar {chave.split()[0]}."))
    if not f:
        f.append(common.achado("info", "Versões sem EOL conhecido", str(alvos), "", corrigir=""))
    return common.resultado("\n".join(out), f)