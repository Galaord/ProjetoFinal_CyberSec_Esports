import re
from lib import common

META = {"id": "M15"}

def run(ctx):
    out, f = [], []
    r = common.http(ctx.url("/teste/"))
    out.append(f"/teste/ -> {r['status']} ({len(r['body'])}B)")

    if r["status"] == 200 and "Tabela de Equipas" in r["body"]:
        ctx.evidencia("M15_teste_dump.html", r["body"])
        linhas = re.findall(r"<tr>(.*?)</tr>", r["body"], re.S)
        dados = []
        for l in linhas:
            cels = [re.sub("<[^>]+>", "", c).strip() for c in re.findall(r"<td>(.*?)</td>", l, re.S)]
            if cels:
                dados.append(" | ".join(cels))
        out.append(f"linhas: {len(dados)}")
        out += ["  " + d for d in dados]

        f.append(common.achado(
            "alto", "/teste/ despeja a base de dados sem login",
            f"{len(dados)} registos de equipas (id, nome, tag, país, V/D) legíveis por visitante",
            "Reconhecimento gratuito: nomes reais de equipas e histórico competitivo. "
            "É o mesmo ORM que alimenta a app, logo confirma tabelas e colunas.",
            ["curl -s http://%s:8000/teste/ | grep -o '<td>[^<]*</td>'" % ctx.target],
            "Colocar /teste/ atrás de login ou desactivar em produção."))

    r2 = common.http(ctx.url("/comunidade/"))
    if r2["status"] == 200:
        emails = set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", r2["body"]))
        out.append(f"/comunidade/ -> 200, emails: {len(emails)}")
        f.append(common.achado(
            "medio", "/comunidade/ expõe jogadores e equipas sem login",
            "nicknames, elo e tags de todas as equipas visíveis",
            "Lista pronta para brute force (nicknames válidos) e para engenharia social.",
            ["curl -s http://%s:8000/comunidade/ | grep -o '<td><strong>[^<]*'" % ctx.target],
            "Aceitável, mas documentar o que é público."))
    return common.resultado("\n".join(out), f)