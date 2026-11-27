import random
from lib import common

META = {"id": "M16"}

def run(ctx):
    out, f = [], []
    nick = "probe%d" % random.randint(100000, 999999)
    mail = nick + "@audit.pt"

    r1 = common.post_form(ctx, "/registo/",
                          {"nickname": nick, "email": mail, "password": "x"}, follow=False)
    out.append(f"criação {nick} -> {r1['status']} (302 = criada)")

    r2 = common.post_form(ctx, "/registo/",
                          {"nickname": nick, "email": "outro%d@audit.pt" % random.randint(1, 9999),
                           "password": "x"}, follow=False)
    out.append(f"nickname duplicado -> {r2['status']} (200 = rejeitado)")

    r3 = common.post_form(ctx, "/registo/",
                          {"nickname": "novo%d" % random.randint(100000, 999999),
                           "email": mail, "password": "x"}, follow=False)
    out.append(f"email duplicado -> {r3['status']} (200 = rejeitado)")

    if r2["status"] == 200 and r3["status"] == 200:
        f.append(common.achado(
            "medio", "Enumeração de contas por nickname e email",
            "nickname existente e email existente devolvem 200 com mensagem própria; "
            "valores novos devolvem 302",
            "Confirma-se se uma conta existe antes de atacar a password. "
            "Nicknames válidos podem ser colhidos em /comunidade/.",
            [f"curl -s -o /dev/null -w '%{{http_code}}' -X POST http://{ctx.target}:8000/registo/ "
             f"-d 'nickname=admin&email=x@x.pt&password=x'"],
            "Aceitar o risco (é o comportamento normal) ou devolver mensagem genérica."))
        out.append(f"conta de teste criada: {nick} / x")
    return common.resultado("\n".join(out), f)