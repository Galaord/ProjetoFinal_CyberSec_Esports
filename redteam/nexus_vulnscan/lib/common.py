import csv, os, re, socket, ssl, subprocess, time, uuid
import http.cookiejar
from datetime import datetime
from urllib import request, parse, error

from . import config

_SSL = ssl.create_default_context()
_SSL.check_hostname = False
_SSL.verify_mode = ssl.CERT_NONE

CJ = http.cookiejar.CookieJar()
_OPENER = request.build_opener(request.HTTPCookieProcessor(CJ),
                               request.HTTPSHandler(context=_SSL))

class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None

_OPENER_NOREDIR = request.build_opener(request.HTTPCookieProcessor(CJ),
                                       request.HTTPSHandler(context=_SSL),
                                       _NoRedirect())


def now():
    return datetime.now().astimezone().isoformat(timespec="seconds")

def novo_id():
    return uuid.uuid4().hex[:8]

def cronometro():
    return time.perf_counter()


def sh(cmd, timeout=300, cwd=None):
    t0 = time.perf_counter()
    try:
        p = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=cwd,
                           capture_output=True, text=True, timeout=timeout)
        out = p.stdout or ""
        if p.stderr:
            out += "\n[stderr]\n" + p.stderr
        return p.returncode, out, round(time.perf_counter() - t0, 2)
    except subprocess.TimeoutExpired as e:
        so = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        return 124, f"[TIMEOUT {timeout}s]\n{so}", round(time.perf_counter() - t0, 2)
    except FileNotFoundError:
        nome = cmd[0] if isinstance(cmd, list) else cmd.split()[0]
        return 127, f"[ferramenta ausente: {nome}]", 0.0
    except Exception as e:
        return 1, f"[erro: {e}]", 0.0


def tcp_open(host, port, timeout=4):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def http(url, method="GET", data=None, extra_headers=None,
         timeout=None, follow=True, host_header="__cfg__"):
    hdrs = {"User-Agent": config.USER_AGENT}
    hh = config.HOST_HEADER if host_header == "__cfg__" else host_header
    if hh:
        hdrs["Host"] = hh
    if extra_headers:
        hdrs.update(extra_headers)

    body = None
    if data is not None:
        body = parse.urlencode(data).encode()
        hdrs.setdefault("Content-Type", "application/x-www-form-urlencoded")

    req = request.Request(url, data=body, headers=hdrs, method=method)
    opener = _OPENER if follow else _OPENER_NOREDIR
    t0 = time.perf_counter()
    try:
        with opener.open(req, timeout=timeout or config.HTTP_TIMEOUT) as r:
            raw = r.read(600_000)
            return {"status": r.status, "headers": dict(r.headers),
                    "set_cookie": r.headers.get_all("Set-Cookie") or [],
                    "body": raw.decode("utf-8", "replace"), "url": r.geturl(),
                    "elapsed": round(time.perf_counter() - t0, 3), "error": None}
    except error.HTTPError as e:
        raw = e.read(600_000) or b""
        return {"status": e.code, "headers": dict(e.headers or {}),
                "set_cookie": (e.headers.get_all("Set-Cookie") if e.headers else []) or [],
                "body": raw.decode("utf-8", "replace"), "url": url,
                "elapsed": round(time.perf_counter() - t0, 3), "error": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": 0, "headers": {}, "set_cookie": [], "body": "",
                "url": url, "elapsed": round(time.perf_counter() - t0, 3), "error": str(e)}


def csrf(url_path, ctx):
    r = http(ctx.url(url_path))
    m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r["body"])
    tok = m.group(1) if m else None
    cookie = next((c.value for c in CJ if c.name == "csrftoken"), None)
    return cookie, tok, r


def post_form(ctx, url_path, fields, referer_path=None, follow=True):
    cookie, tok, _ = csrf(url_path, ctx)
    data = dict(fields)
    if tok:
        data["csrfmiddlewaretoken"] = tok
    hdrs = {}
    if cookie:
        hdrs["X-CSRFToken"] = cookie
    if referer_path:
        hdrs["Referer"] = ctx.url(referer_path)
    return http(ctx.url(url_path), "POST", data=data,
                extra_headers=hdrs, follow=follow)


def login(ctx, user, pw):
    """True se 302 (sucesso). False se 200 (credenciais erradas) ou 403."""
    r = post_form(ctx, "/login/", {"nickname": user, "password": pw}, follow=False)
    return r["status"] == 302, r


def trunc(s):
    if s is None:
        return ""
    return s if len(s) <= config.MAX_OUTPUT else s[:config.MAX_OUTPUT] + "\n[...TRUNCADO...]"


def snippet(text, needle, largura=120):
    i = text.lower().find(needle.lower())
    if i < 0:
        return ""
    return text[max(0, i - largura):i + largura].replace("\n", " ")


def achado(sev, titulo, evidencia, impacto, explorar=None, corrigir=""):
    return {"sev": sev, "titulo": titulo, "evidencia": evidencia,
            "impacto": impacto,
            "explorar": explorar if isinstance(explorar, list) else ([explorar] if explorar else []),
            "corrigir": corrigir}


class Ctx:
    def __init__(self, sess_dir):
        self.base_url = config.BASE_URL
        self.target = config.TARGET_IP
        self.host_header = config.HOST_HEADER
        self.timeout = config.HTTP_TIMEOUT
        self.sess_dir = sess_dir
        self.logdir = os.path.join(sess_dir, "logs")
        self.evidir = os.path.join(sess_dir, "evidencias")
        self.state = {}
        self.cmds = []
        os.makedirs(self.logdir, exist_ok=True)
        os.makedirs(self.evidir, exist_ok=True)

    def url(self, path=""):
        return self.base_url.rstrip("/") + "/" + path.lstrip("/")

    def xampp(self, path="", porta=None):
        return f"http://{self.target}:{porta or config.XAMPP_PORTS[0]}/{path.lstrip('/')}"

    def cmd(self, c):
        self.cmds.append(c if isinstance(c, str) else " ".join(map(str, c)))

    def log(self, mid, texto):
        p = os.path.join(self.logdir, f"{mid}_{int(time.time())}.log")
        with open(p, "w", encoding="utf-8") as f:
            f.write(texto)
        return p

    def evidencia(self, nome, conteudo):
        p = os.path.join(self.evidir, nome)
        with open(p, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return p


def resultado(output="", achados=None, sev=None):
    achados = achados or []
    if sev is None:
        ordem = {"crit": 4, "alto": 3, "medio": 2, "baixo": 1, "info": 0}
        sev = max((a["sev"] for a in achados), key=lambda s: ordem.get(s, 0), default="info")
    return {"output": output, "achados": achados, "sev": sev}