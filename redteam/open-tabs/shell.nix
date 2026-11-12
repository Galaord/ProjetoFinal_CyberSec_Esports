{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz") {} }:

let
  python = pkgs.python3;
  pythonEnv = python.withPackages (ps: with ps; [
    playwright
    pysocks
    requests
  ]);
in
pkgs.mkShell {
  packages = [
    pythonEnv
    pkgs.playwright-driver.browsers
    pkgs.nodejs
  ];

  env = {
    PLAYWRIGHT_BROWSERS_PATH = "${pkgs.playwright-driver.browsers}";
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD = "1";
    PLAYWRIGHT_NODEJS_PATH = "${pkgs.nodejs}/bin/node";
  };

  shellHook = ''
    echo "python: $(python --version 2>&1)"
    python - <<'EOF'
import importlib.util as u
for m in ("playwright", "socks"):
    print(f"  {m}: {'ok' if u.find_spec(m) else 'MISSING'}")
EOF
  '';
}