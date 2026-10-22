# Static in-browser app (Pyodide)

Converts the Panel toy to **pyodide-worker** HTML so it runs entirely in the visitor’s browser (numpy / scipy / matplotlib / bokeh / panel from the Pyodide CDN). No Python process on the server after the files are uploaded.

Intended public URL: **https://xray.cardsharpener.com** (subdomain of `PUBLIC_BASE_URL` in `site/wrangler.jsonc`). This folder is a **separate** Cloudflare project named `xray-scattering`. It must not share the cardsharpner Worker, Stripe secrets, or LICENSES KV.

## Packages loaded in the browser

- numpy
- scipy
- matplotlib
- bokeh
- panel

(Pyodide itself is fetched from `cdn.jsdelivr.net/pyodide/v0.29.3/`. Panel/Bokeh wheels come from the usual Panel CDN.)

## Build

From `xray-scattering/` with the venv on:

```bash
bash web/build.sh
# or: python -m app.build_static
```

Output: `web/dist/` (`index.html`, `app.html`, `app.js` worker, `app.resources.zip`). That directory is gitignored — rebuild before deploy.

Preview locally:

```bash
cd web/dist
python -m http.server 8010
```

Open http://127.0.0.1:8010/ . First load downloads Pyodide + scipy (tens of MB); later loads cache.

### Size and speed (measured 22 Oct 2026 on this VM)

Origin files in `web/dist/` (gitignored): ~1.0 MB uncompressed (`index.html` 930 KB, `app.js` 3 KB, `app.resources.zip` 75 KB); gzip of those ~0.46 MB. Do not commit `dist/`.

First visit also pulls Pyodide 0.29.3, numpy/scipy/matplotlib (and deps), plus Panel/Bokeh wheels and `bokeh-mathjax` from CDN. Order of magnitude:

- Download (CDN file bytes): ~45–50 MB (scipy wheel ~13 MB, matplotlib ~6.7 MB, numpy ~3.1 MB, `pyodide.asm.wasm` ~8.6 MB, stdlib zip ~2.4 MB, Panel/Bokeh/MathJax JS+wheels ~8 MB, plus origin HTML).
- Unpacked in the browser: ~120 MB (scipy unzip ~46 MB, matplotlib ~16 MB, numpy ~11 MB, OpenBLAS ~6.5 MB, stdlib ~9 MB, wasm ~8.6 MB, rest of the stack).

In-app **Update** line at default N=96: **0.58 s** on first Python refresh after WASM was up; **2.07 s** after moving σ (5→7 Å). Native `python -m app` is ~**0.3 s** at the same N. Cold first load in Chrome on this VM (navigation to plots visible) was **~99 s** (13:31:14–13:32:53).

## Deploy (you run this; the agent does not)

Need a Cloudflare account that can create a **new** Worker/assets project. Do not edit `site/wrangler.jsonc`.

1. Build: `cd xray-scattering && bash web/build.sh`
2. From `xray-scattering/web/`:

   ```bash
   npx wrangler deploy
   ```

   First time, Wrangler creates project `xray-scattering`. Confirm it is **not** `cardsharpner`.
3. Cloudflare dashboard → Workers & Pages → **xray-scattering** → Settings → Domains & Routes → **Custom domain** → `xray.cardsharpener.com`.
4. DNS: CNAME `xray` → the workers.dev / pages target Cloudflare shows (proxied). Apex `cardsharpener.com` stays on the existing site Worker.
5. Optional: in the same custom-domain UI, wait until the certificate is issued.

### Headers / WASM

`dist/_headers` (copied from `web/_headers`) sets `Content-Type: application/wasm` and long cache on `*.wasm` / `*.js` / `*.zip`. Cloudflare static assets honour `_headers`. Pyodide wasm is usually loaded from jsDelivr, not from this bucket; the rule is there if you later vendor it.

If a future **compiled / threaded** Pyodide build needs `SharedArrayBuffer`, add:

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

That can break third-party scripts without CORP; the current convert does **not** require it.

SPA: `not_found_handling` is `single-page-application` so unknown paths serve `index.html`. The worker script `app.js` and `app.resources.zip` must stay at the same origin and path prefix as `index.html`.

## Limits versus `python -m app`

- First visit waits for Pyodide + scipy.
- Slider updates are slower; N is capped at 96 in the WASM build.
- No local filesystem; session JSON stays in the page.
- MathJax is loaded with Bokeh/Panel from CDN (not `inline=True`).
