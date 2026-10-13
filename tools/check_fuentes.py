#!/usr/bin/env python3
"""Revisa que las fuentes de datos del curso sigan vivas y avisa si hay datos más nuevos.

Uso:  python tools/check_fuentes.py

- Cada fuente de tools/make_datasets.py debe responder (si una cae, el pipeline
  no se puede regenerar y hay que buscar respaldo).
- MINEDUC publica la matrícula oficial de un año hacia fines de ese año: si ya
  existe el archivo del año siguiente al que usa el curso, toca actualizar.
- Sale con código 1 si hay algo que hacer (fuente caída o dato nuevo) — pensado
  para un workflow mensual que avise por correo de GitHub.
"""
import datetime as dt
import re
import sys

import requests

UA = {"User-Agent": "formacionpublica-bootcamp/1.0 (verificador de fuentes)"}
ANIO_MATRICULA_CURSO = 2025   # mantener al día con tools/make_datasets.py

FUENTES = {
    "MINEDUC (matrícula)": "https://datosabiertos.mineduc.cl/resumen-de-matricula-por-establecimiento-educacional/",
    "SINCA (aire)": "https://sinca.mma.gob.cl/",
    "ChileAtiende (fichas)": "https://www.chileatiende.gob.cl/temas",
    "datos.gob.cl (SERNAC)": "https://datos.gob.cl/api/3/action/package_search?q=reclamos%20sernac&rows=1",
    "USGS (sismos)": "https://earthquake.usgs.gov/fdsnws/event/1/version",
}


def main() -> int:
    pendientes = []
    for nombre, url in FUENTES.items():
        try:
            r = requests.get(url, headers=UA, timeout=60)
            estado = "OK" if r.ok else f"HTTP {r.status_code}"
        except requests.RequestException as e:
            r, estado = None, f"sin respuesta ({type(e).__name__})"
        print(f"{'✅' if estado == 'OK' else '❌'} {nombre}: {estado}")
        if estado != "OK":
            pendientes.append(f"fuente caída: {nombre}")
        if nombre.startswith("MINEDUC") and r is not None and r.ok:
            anios = sorted({int(a) for a in re.findall(r"Resumen_Matricula_EE_(\d{4})", r.text)})
            if anios:
                print(f"   años publicados: {anios[0]}–{anios[-1]} (el curso usa {ANIO_MATRICULA_CURSO})")
                if anios[-1] > ANIO_MATRICULA_CURSO:
                    pendientes.append(f"MINEDUC publicó la matrícula {anios[-1]}: actualizar URL_MATRICULA")

    hoy = dt.date.today()
    print(f"\nRevisado el {hoy.isoformat()}.")
    if pendientes:
        print("Acciones pendientes:\n- " + "\n- ".join(pendientes))
        return 1
    print("Sin acciones pendientes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
