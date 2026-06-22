# web/ — Sitio de Formación Pública (autohospedado)

Sirve **formacionpublica.cl** desde una Raspberry Pi propia, **sin depender de GitHub Pages**.

## Arquitectura

```
máquina de desarrollo                         Raspberry Pi (server-f1)
─────────────────────                         ────────────────────────
web/build.sh                                  systemd: formacion-publica.service
  ├─ MkDocs (site_url=formacionpublica.cl)      └─ uvicorn app.main:app
  │    → web/public/                                 127.0.0.1:5001
  └─ JupyterLite (notebooks de estudiante           ▲
       + datos, sin soluciones)                     │ Cloudflare Tunnel (server-f1)
       → web/public/lite/                           │
                                                formacionpublica.cl + www
web/deploy.sh  ── rsync public/+app/ ──▶  /home/server-f1/projects/formacion-publica/
```

- La Pi **solo** corre FastAPI+uvicorn sirviendo estáticos ya construidos (no necesita mkdocs ni
  jupyterlite). El build pesado ocurre en la máquina de desarrollo.
- **`/`** → sitio MkDocs · **`/lite/`** → entorno JupyterLite (Python en el navegador, datos incluidos)
  · **`/health`** → healthcheck del túnel.

## Uso

```bash
web/build.sh                 # construye web/public/ (sitio + lite). Crea un venv aislado en web/.buildenv
web/deploy.sh                # build + rsync a la Pi + pip install + restart + verificación
SKIP_BUILD=1 web/deploy.sh   # solo sincroniza el último build
```

Variables: `REMOTE_HOST` (def. `raspi`), `REMOTE_DIR` (def. `/home/server-f1/projects/formacion-publica`),
`SERVICE` (def. `formacion-publica`), `PORT` (def. `5001`).

## Notas

- **Sin dependencia de GitHub para los datos:** los CSV se empaquetan en el build de JupyterLite
  (`/lite/files/<modulo>/<archivo>`), así que los notebooks corren offline en el navegador.
- **Soluciones excluidas:** el build NO publica ningún `*solucion*.ipynb`.
- **scikit-learn en el navegador:** Pyodide trae numpy/pandas/matplotlib; al `import sklearn` se descarga
  el wheel desde el CDN de Pyodide (jsDelivr) la primera vez — es un CDN, **no** GitHub. (Para 100% sin
  red habría que bundlear la distribución Pyodide completa: build más pesado.)
- **Colab sigue disponible:** los botones *Open in Colab* de cada módulo apuntan al repo en GitHub; el
  entorno `/lite/` es la alternativa sin cuenta/sin instalación.
- Artefactos de build (`public/`, `contents/`, `.buildenv/`, `.lite/`) están en `.gitignore`.
