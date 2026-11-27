#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

falta=0
for t in nmap whatweb curl nikto sqlmap mysql openssl; do
  command -v "$t" >/dev/null 2>&1 || { echo "[!] em falta: $t"; falta=1; }
done
if ! python3 -c "import sys; sys.exit(0 if sys.version_info>=(3,9) else 1)"; then
  echo "[!] Python 3.9+ necessario"; exit 1
fi
[ "$falta" -eq 1 ] && echo "[i] podes instalar com: sudo apt install nmap whatweb nikto sqlmap default-mysql-client openssl"

python3 nexus_menu.py 