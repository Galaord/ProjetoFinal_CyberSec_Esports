import os, queue, threading
from lib import common

META = {"id": "M13"}
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(ctx):
    palavras = [l.strip() for l in open(os.path.join(BASE, "wordlists", "django_paths.txt"),
                                        encoding="utf-8") if l.strip()]
    fila, achados, lock = queue.Queue(), [], threading.Lock()
    for p in palavras:
        fila.put(p)

    def worker():
        while True:
            try:
                p = fila.get_nowait()
            except queue.Empty:
                return
            r = common.http(ctx.url(p))            # segue 301 -> avalia o destino real
            if r["status"] in (200, 401, 403) and r["status"] != 404:
                with lock:
                    achados.append((r["status"], p, len(r["body"])))
            fila.task_done()

    ts = [threading.Thread(target=worker, daemon=True) for _ in range(12)]
    [t.start() for t in ts]
    [t.join(timeout=150) for t in ts]

    achados.sort()
    out = [f"{s} {n:7}B /{p}" for s, p, n in achados]
    f = []
    publicos = [p for s, p, n in achados if s == 200 and p not in ("", "/")]
    if publicos:
        f.append(common.achado("medio", "Endpoints acessíveis sem sessão",
                               ", ".join("/" + p for p in publicos),
                               "Cada endpoint é superfície de ataque; /teste/ e /comunidade/ "
                               "entregam dados de BD sem login.",
                               [f"curl -s http://{ctx.target}:8000/{p}" for p in publicos[:3]],
                               "Rever o que deve ser público e aplicar @login_required."))
    if not achados:
        f.append(common.achado("info", "Sem caminhos extra", "só as rotas conhecidas", "", corrigir=""))
    return common.resultado("\n".join(out), f)