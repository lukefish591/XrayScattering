# X-ray scattering (nested in cardsharpner)

Masters project workspace for **simulated X-ray scattering data models**. This folder is self-contained: poker code in the rest of the repo is unrelated and unused here.

Physics models and experimental pipelines are intentionally not stubbed in. Literature, an intro course, and a maths primer live under `docs/`.

## Setup

Work **from this folder** (`xray-scattering/`), not the repository root.

Python 3.11+ (developed against 3.12).

```bash
cd xray-scattering
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Pinned versions from a working install are in `requirements.lock.txt`:

```bash
python -m pip install -r requirements.lock.txt
python -m pip install -e ".[dev]"
```

Confirm the stack:

```bash
xray-scattering-env
pytest -q
```

Intro course toys (venv on, still in this folder):

```bash
cd course
python 01_kinematics.py
```

Explorations of surfaces and correlation functions: [`explorations/`](explorations/README.md).

Live two-panel toy (surface + simulated detector) in the browser:

```bash
python -m app
# or: panel serve app/main.py --port 5009
```

Opens at http://127.0.0.1:5009 . Everything in the app is **illustrative**, not measured data.

Static in-browser build (Pyodide; for `xray.cardsharpener.com`):

```bash
bash web/build.sh
cd web/dist && python -m http.server 8010
```

Jupyter (optional):

```bash
jupyter lab
```

## Layout

| Path | Purpose |
| --- | --- |
| `src/xray_scattering/` | Installable package: env check plus `sim/` (surface, Born/DWBA toys, invert) |
| `tests/` | Env smoke tests plus surface / Born / invert checks |
| `docs/papers/` | PRB 1988 and Physica A 1996 PDFs |
| `docs/paper-takeaways.md` | Reading notes for both papers |
| `docs/paper-equations.md` | Working equation sheet |
| `docs/intro-course.md` | 8-module intro course |
| `docs/maths/` | Maths primer (9 chapters + numeric checks) |
| `course/` | Course toys (`docs/course/`; run from this symlink) |
| `explorations/` | Illustrative surface / C(R) / scattering diagrams |
| `app/` | Panel browser toy: live surface + simulated lab |
| `web/` | Pyodide convert script, wrangler config, static dist (gitignored) |
| `docs/experiment-questionnaire.md` | Geometry / sample questions before modelling |
| `docs/context/` | Extra experiment notes you add |
| `data/experimental/` | Measured data you provide later (gitignored) |
| `data/simulated/` | Model outputs (gitignored) |

**Math in Markdown:** display equations use `$$...$$` (KaTeX). In-sentence math is HTML/unicode (`<sub>`, `<sup>`, ∣, ∗) so Cursor preview does not treat `_` and `*` as emphasis.

## Next steps

1. Fill `docs/experiment-questionnaire.md` for the actual sample and scans.
2. Drop experimental files under `data/experimental/` and describe them in `docs/context/`.
3. Implement scattering models in `src/xray_scattering/` against those notes and the papers — not against placeholder physics or the course toys.
