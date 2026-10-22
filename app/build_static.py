"""Build the static Pyodide Panel app into web/dist.

Usage (from xray-scattering/):

    python -m app.build_static
    # or: bash web/build.sh
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
STAGE = WEB / "stage"
DIST = WEB / "dist"
REQUIREMENTS = ["numpy", "scipy", "matplotlib", "bokeh", "panel"]


def _stage() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    shutil.copy2(WEB / "app.py", STAGE / "app.py")
    shutil.copy2(ROOT / "app" / "main.py", STAGE / "main.py")
    shutil.copy2(ROOT / "app" / "explain.py", STAGE / "explain.py")
    pkg = STAGE / "xray_scattering"
    pkg.mkdir()
    shutil.copy2(ROOT / "src" / "xray_scattering" / "__init__.py", pkg / "__init__.py")
    sim_src = ROOT / "src" / "xray_scattering" / "sim"
    sim_dst = pkg / "sim"
    sim_dst.mkdir()
    for py in sim_src.glob("*.py"):
        shutil.copy2(py, sim_dst / py.name)


def _resource_args() -> list[str]:
    files = [
        STAGE / "main.py",
        STAGE / "explain.py",
        STAGE / "xray_scattering" / "__init__.py",
        *sorted((STAGE / "xray_scattering" / "sim").glob("*.py")),
    ]
    return [str(p) for p in files]


def main() -> int:
    _stage()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    cmd = [
        sys.executable,
        "-m",
        "panel",
        "convert",
        str(STAGE / "app.py"),
        "--to",
        "pyodide-worker",
        "--out",
        str(DIST),
        "--title",
        "X-ray scattering toy",
        "--requirements",
        *REQUIREMENTS,
        "--resources",
        *_resource_args(),
        "--disable-http-patch",
    ]
    print(" ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=str(STAGE))
    app_html = DIST / "app.html"
    if app_html.is_file():
        shutil.copy2(app_html, DIST / "index.html")
    headers = WEB / "_headers"
    if headers.is_file():
        shutil.copy2(headers, DIST / "_headers")
    print(f"Wrote static app to {DIST}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
