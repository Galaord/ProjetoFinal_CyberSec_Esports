import csv, os, html
from lib import common

META = {"id": "M22"}

PESO = {"crit": 25, "alto": 10, "medio": 4, "baixo": 1, "info": 0}
ORDEM = ["crit", "alto", "medio", "baixo", "info"]

def run(ctx):
    csv_path = os.path.join(ctx.sess_dir, "resultados.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))

    score = min(100, sum(PESO.get(l["severidade"], 0) for l in linhas))
    banda = ("CRÍTICO" if score >= 60 else "ALTO" if score >= 35
             else "MÉDIO" if score >= 15 else "BAIXO")

    md = [f"# Auditoria NEXUS ARENA — risco {score}/100 ({banda})", "",
          f"Alvo: {ctx.base_url}", f"Sessão: {ctx.sess_dir}", ""]
    plano = []
    for sev in ORDEM:
        grupo = [l for l in linhas if l["severidade"] == sev]
        if not grupo:
            continue
        md += [f"## {sev.upper()} ({len(grupo)})", ""]
        for l in grupo:
            md += [f"### {l['modulo']} — {l['titulo']}",
                   f"- **Evidência:** {l['evidencia']}",
                   f"- **Impacto:** {l['impacto']}"]
            if l["exploracao"] and l["exploracao"] != "-":
                md.append("- **Explorar:**")
                for e in l["exploracao"].split(" ; "):
                    if e.strip():
                        md.append(f"  ```\n  {e}\n  ```")
            if l["correcao"] and l["correcao"] != "-":
                md.append(f"- **Correção:** {l['correcao']}")
            md.append("")
            if sev in ("crit", "alto") and l["correcao"] not in ("", "-"):
                plano.append(f"{len(plano)+1}. [{sev.upper()}] {l['titulo']} → {l['correcao']}")

    if plano:
        md += ["## Plano por prioridade", ""] + plano + [""]

    with open(os.path.join(ctx.sess_dir, "relatorio.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    linhas_html = []
    for sev in ORDEM:
        for l in [x for x in linhas if x["severidade"] == sev]:
            linhas_html.append(
                f"<article class='{sev}'><h3><span>{sev.upper()}</span> {html.escape(l['modulo'])} — "
                f"{html.escape(l['titulo'])}</h3><p><b>Evidência:</b> {html.escape(l['evidencia'])}</p>"
                f"<p><b>Impacto:</b> {html.escape(l['impacto'])}</p>"
                f"<pre>{html.escape(l['exploracao'])}</pre>"
                f"<p><b>Correção:</b> {html.escape(l['correcao'])}</p></article>")
    doc = f"""<!doctype html><meta charset="utf-8"><title>Auditoria NEXUS ARENA</title>
<style>body{{font-family:system-ui;background:#0b1020;color:#e8edf7;max-width:900px;margin:auto;padding:30px}}
h1{{font-size:26px}}h3{{margin:0 0 8px;font-size:16px}}article{{border-left:5px solid #556;background:#151c33;
padding:14px 16px;margin:14px 0;border-radius:8px}}article.crit{{border-color:#e5484d}}article.alto{{border-color:#f76b15}}
article.medio{{border-color:#f5b800}}article.baixo{{border-color:#3e9bff}}article.info{{border-color:#667}}
span{{font-size:11px;letter-spacing:1px;opacity:.8}}pre{{background:#0b1020;padding:8px;border-radius:6px;overflow-x:auto;font-size:12px}}
.risco{{font-size:20px;font-weight:800;color:#f76b15}}</style>
<h1>Auditoria NEXUS ARENA</h1><p class="risco">Risco {score}/100 — {banda}</p>
<p>Alvo: {ctx.base_url}</p>{''.join(linhas_html)}"""
    with open(os.path.join(ctx.sess_dir, "relatorio.html"), "w", encoding="utf-8") as f:
        f.write(doc)

    resumo = [f"Risco: {score}/100 ({banda})"]
    for sev in ORDEM:
        n = len([l for l in linhas if l["severidade"] == sev])
        if n:
            resumo.append(f"{sev}: {n}")
    with open(os.path.join(ctx.sess_dir, "resumo.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(resumo + ["", *plano]))

    f_out = [common.achado("info", f"Relatório gerado — risco {score}/100 ({banda})",
                           f"{len(linhas)} achados; {os.path.join(ctx.sess_dir, 'relatorio.html')}",
                           "Abrir o HTML para leitura, o CSV para dados",
                           corrigir="")]
    return common.resultado("\n".join(md[:60]), f_out)