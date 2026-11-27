# NEXUS ARENA — Auditoria de vulnerabilidades

Kali `192.168.40.11` (VLAN40) -> alvo `192.168.20.13:8000` (VLAN20).

## Pré-requisitos

1. Routing entre VLANs garantido no firewall/L3:
   - `ip route get 192.168.20.13` deve indicar o gateway correcto
   - `ping -c3 192.168.20.13` e `nc -zv 192.168.20.13 8000`
2. Ferramentas: `sudo apt install nmap whatweb nikto sqlmap default-mysql-client openssl`
3. **ALLOWED_HOSTS vazio + DEBUG=True**: o Django só aceita `localhost`,
   por isso todos os pedidos enviam `Host: localhost`. Para testar pelo IP real,
   põe `HOST_HEADER = None` em `lib/config.py`.
ip route get 192.168.20.13 && ping -c3 192.168.20.13 && nc -zv 192.168.20.13 8000
## Execução

```bash
chmod +x run.sh && ./run.sh