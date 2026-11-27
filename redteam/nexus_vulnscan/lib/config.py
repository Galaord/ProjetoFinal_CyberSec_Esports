"""Alvos e parâmetros. Ajusta antes de correr."""

TARGET_IP   = "192.168.20.13"
TARGET_PORT = 8000
BASE_URL    = f"http://{TARGET_IP}:{TARGET_PORT}"

XAMPP_PORTS = [80, 8080]
MYSQL_HOST  = TARGET_IP
MYSQL_PORT  = 3306
DB_NAME     = "bd_torneios"

# pares testados por ordem; o 1130 (host não autorizado) é o esperado aqui
DB_USERS = [("root", ""), ("root", "root"), ("root", "password"), ("root", "xampp"),
            ("nexus", ""), ("nexus", "nexus"), ("admin", ""), ("django", "")]

KALI_IP     = "192.168.40.11"
HOST_HEADER = "localhost"     # ALLOWED_HOSTS restrito; None para usar o IP

USER_AGENT  = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) NexusAudit/2.0"
PORTS_TOP   = "21,22,25,80,443,3306,8000,8080,8443,33060"
HTTP_TIMEOUT = 12
MAX_OUTPUT   = 50000
BRUTE_LIMIT  = 60

# fim de suporte (para o módulo de versões)
EOL = {
    "PHP 8.2":     "suporte de segurança terminou em 2025-12-08",
    "MariaDB 10.3": "fim de vida em 2023-05-23",
    "WSGIServer":  "runserver — servidor de desenvolvimento, não de produção",
}