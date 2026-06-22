# -*- coding: utf-8 -*-
"""Formación Pública — servidor estático.

Sirve el sitio (build de MkDocs) en `/` y el entorno JupyterLite en `/lite/`,
ambos desde la carpeta `public/` (artefactos pre-construidos por build.sh).
Mantiene `/health` para el monitoreo del túnel Cloudflare.

Diseño: la Raspberry Pi NO necesita mkdocs ni jupyterlite; solo FastAPI+uvicorn
sirviendo archivos estáticos ya construidos. El build ocurre en la máquina de
desarrollo y se sincroniza `public/` por rsync.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE = Path(__file__).resolve().parent.parent
PUBLIC = BASE / "public"

app = FastAPI(title="Formación Pública", docs_url=None, redoc_url=None)


@app.get("/health")
def health():
    """Healthcheck del túnel/monitor. Responde a GET y HEAD."""
    return {"status": "ok", "service": "formacion-publica"}


# El sitio estático se monta al final, en "/", para que /health tenga prioridad.
# StaticFiles maneja GET y HEAD (resuelve el 405 del placeholder) y sirve
# index.html en cada directorio (html=True). JupyterLite vive en public/lite/.
if PUBLIC.is_dir() and any(PUBLIC.iterdir()):
    app.mount("/", StaticFiles(directory=str(PUBLIC), html=True), name="site")
else:
    # Fallback honesto si aún no se ha sincronizado el build.
    @app.get("/", response_class=HTMLResponse)
    def placeholder():
        return (
            "<!doctype html><html lang='es'><meta charset='utf-8'>"
            "<title>Formación Pública</title>"
            "<body style='font-family:system-ui;max-width:40rem;margin:4rem auto;padding:0 1rem'>"
            "<h1>Formación Pública</h1>"
            "<p>El sitio se está desplegando. Vuelve en unos minutos.</p>"
            "</body></html>"
        )

    @app.exception_handler(404)
    def _nf(_req, _exc):
        return JSONResponse({"detail": "not found"}, status_code=404)
