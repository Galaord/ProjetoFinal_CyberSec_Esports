from lib import common

META = {"id": "M12"}

ALVOS = ["/settings.py", "/nexus_arena/settings.py", "/core/views.py", "/manage.py",
         "/.env", "/.git/HEAD", "/db.sqlite3", "/bd_torneios.sql", "/backup.sql",
         "/requirements.txt", "/robots.txt", "/static/admin/css/base.css", "/media/"]

def run(ctx):
    out, f, hits = [], [], []
    for a in ALVOS:
        r = common.http(ctx.url(a), follow=False)
        out.append(f"{r['status']:3} {len(r['body']):7}B {a}")
        if r["status"] == 200 and len(r["body"]) > 30:
            hits.append(a)
            if "SECRET_KEY" in r["body"]:
                f.append(common.achado("crit", "Código-fonte de settings.py servido",
                                       f"{a} -> 200 com SECRET_KEY",
                                       "Configuração completa (BD, chave, apps) exposta por HTTP.",
                                       [f"curl -s http://{ctx.target}:8000{a}"],
                                       "Servir só /static/ e usar whitenoise/nginx para estáticos."))
    if not hits:
        f.append(common.achado("info", "Sem ficheiros de código expostos",
                               "todos os alvos testados devolvem 404",
                               "Bom — a raiz do projecto não está montada",
                               corrigir=""))
    return common.resultado("\n".join(out), f)