import re
from lib import common

META = {"id": "M10"}

def run(ctx):
    out, f = [], []
    r = common.http(ctx.url("/"), host_header="evil.attacker.com", follow=False)
    out.append(f"Host: evil.attacker.com -> {r['status']}")

    if r["status"] == 400:
        pagina = r["body"]
        caminho = ctx.evidencia("M10_disallowedhost.html", pagina)
        out.append(f"página de debug guardada: {caminho}")

        m = re.search(r"SECRET_KEY\s*[=:]\s*['\"]?([\w\-+#!^()@$%&*=.]{30,})", pagina)
        if m:
            chave = m.group(1)
            out.append(f"SECRET_KEY EXTRAÍDA: {chave}")
            f.append(common.achado(
                "alto", "SECRET_KEY exposta numa página de erro",
                f"SECRET_KEY = {chave[:18]}… ({len(chave)} chars) obtida do 400 de DisallowedHost",
                "Com a chave e DEBUG=True assina-se tokens: links de reset de password, "
                "dados em signed cookies e mensagens. Permite forjar identidade onde o token é assinado.",
                ["curl -s -H 'Host: evil.attacker.com' http://%s:8000/ | grep -o 'SECRET_KEY[^<]*'" % ctx.target,
                 "python3 -c \"from django.core import signing; print(signing.dumps({'uid':1}, key='CHAVE'))\""],
                "DEBUG=False em produção e SECRET_KEY fora do repositório (variável de ambiente)."))

        if "DEBUG = True" in pagina or "DEBUG" in pagina and "True" in pagina:
            f.append(common.achado(
                "alto", "DEBUG=True em produção",
                "Página de erro 400 expõe settings, ALLOWED_HOSTS e traceback",
                "Cada erro entrega caminhos internos, queries SQL e variáveis locais "
                "— mapa completo da aplicação para quem ataca.",
                ["curl -s -H 'Host: x.tld' http://%s:8000/ | head -50" % ctx.target],
                "DEBUG = False; servir erros estáticos."))
    else:
        f.append(common.achado("info", "Host header validado",
                               f"host desconhecido -> {r['status']}", "Sem host injection", corrigir=""))

    r2 = common.http(ctx.url("/"), extra_headers={"X-Forwarded-Host": "evil.attacker.com"})
    out.append(f"X-Forwarded-Host -> {r2['status']}")
    if r2["status"] == 200:
        f.append(common.achado("baixo", "X-Forwarded-Host aceite",
                               "cabeçalho aceite sem validação",
                               "Se houver cache/CDN, permite envenenar links absolutos.",
                               corrigir="USE_X_FORWARDED_HOST = True só atrás de proxy de confiança."))
    return common.resultado("\n".join(out), f)