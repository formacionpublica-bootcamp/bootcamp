#!/usr/bin/env python3
"""Ejecuta todos los solucion.ipynb de ramas/ y reporta cuáles fallan.

Uso:  python tools/run_notebooks.py [--rama R1|R2|R3] [--timeout 600]

- Se ejecuta `solucion.ipynb` (la referencia completa) y NO `leccion.ipynb`: la
  lección del estudiante tiene celdas `# TODO` con `...` que fallan a propósito.
  Si la solución corre verde, el módulo está sano.
- Cada notebook se ejecuta con `jupyter nbconvert --execute` en su propia carpeta
  (los datasets se cargan con ruta relativa y patrón "en vivo o caché", así que
  no se necesita red ni API keys).
- SKIP: módulos que no pueden correr desatendidos (p. ej. dashboards Gradio con
  `launch()`, que bloquean). Se listan igual en el resumen, como SKIP.
- Sale con código 1 si algún notebook falla — pensado para CI.
"""
import argparse, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Módulos que se saltan y por qué (mantener la razón al día):
SKIP = {
    "R1-09-dashboards-ligeros": "Gradio launch() bloquea en ejecución desatendida",
}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rama", help="solo una rama, p.ej. R1")
    ap.add_argument("--timeout", type=int, default=600, help="segundos por notebook")
    args = ap.parse_args()

    notebooks = sorted(ROOT.glob("ramas/*/R*/solucion.ipynb"))
    if args.rama:
        notebooks = [nb for nb in notebooks if nb.parent.name.startswith(args.rama)]
    if not notebooks:
        print("No se encontraron notebooks."); return 1

    failed, skipped, passed = [], [], []
    for nb in notebooks:
        mod = nb.parent.name
        if mod in SKIP:
            skipped.append(mod)
            print(f"SKIP {mod} ({SKIP[mod]})", flush=True)
            continue
        t0 = time.time()
        proc = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
             "--execute", "--stdout", nb.name,
             f"--ExecutePreprocessor.timeout={args.timeout}"],
            cwd=nb.parent, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        dt = time.time() - t0
        if proc.returncode == 0:
            passed.append(mod)
            print(f"PASS {mod} ({dt:.0f}s)", flush=True)
        else:
            failed.append(mod)
            tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
            print(f"FAIL {mod} ({dt:.0f}s)\n--- stderr (últimas líneas) ---\n{tail}\n---", flush=True)

    print(f"\nResumen: {len(passed)} PASS · {len(failed)} FAIL · {len(skipped)} SKIP de {len(notebooks)}")
    if failed:
        print("Fallaron: " + ", ".join(failed))
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
