#!/usr/bin/env python3
"""Ejecuta las soluciones de ramas/ y verifica que TODAS las celdas de chequeo den ✅.

Uso:  python tools/run_notebooks.py [--rama R1|R2|R3] [--modulo R2-07] [--timeout 600]

- Se ejecutan `solucion.ipynb` y `profundiza_solucion.ipynb` (las referencias
  completas), NO las lecciones: la lección del estudiante tiene celdas `# TODO`
  con `...` que fallan a propósito.
- Un notebook PASA solo si (1) corre sin errores, (2) imprime al menos un ✅ y
  (3) no imprime ningún ❌. Las celdas de chequeo estilo casa no cortan la
  ejecución con un error: sin la regla (3), un módulo con resultados incorrectos
  pasaría en verde.
- Cada notebook corre en su propia carpeta (datasets con ruta relativa y patrón
  "en vivo o caché"): no se necesita red ni API keys. Los módulos de R3 usan el
  respaldo de preguntar_llm() cuando no hay GEMINI_API_KEY.
- Sale con código 1 si algún notebook falla — pensado para CI.
"""
import argparse, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOMBRES = ("solucion.ipynb", "profundiza_solucion.ipynb")

# Módulos que se saltan y por qué (mantener la razón al día; idealmente vacío).
SKIP: dict[str, str] = {}


def textos_de_salida(nb_path: Path):
    """Concatena el texto de todas las salidas (stdout, resultados y errores)."""
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        for out in cell.get("outputs", []):
            if "text" in out:
                yield "".join(out["text"])
            for v in out.get("data", {}).values():
                if isinstance(v, list):
                    yield "".join(v)
                elif isinstance(v, str):
                    yield v


def ejecutar(nb: Path, timeout: int):
    """Devuelve (ok, n_ok, n_mal, detalle)."""
    # Se ejecuta en una COPIA de la carpeta del módulo: los archivos que crean los
    # notebooks (modelos .joblib, figuras, predicciones) no ensucian el repo.
    with tempfile.TemporaryDirectory() as tmp:
        trabajo = Path(tmp) / nb.parent.name
        shutil.copytree(nb.parent, trabajo)
        salida = Path(tmp) / f"ejecutado_{nb.name}"
        proc = subprocess.run(
            [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
             "--execute", "--output", str(salida), nb.name,
             f"--ExecutePreprocessor.timeout={timeout}"],
            cwd=trabajo, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
            return False, 0, 0, f"error de ejecución:\n{tail}"
        texto = "\n".join(textos_de_salida(salida))
    n_ok, n_mal = texto.count("✅"), texto.count("❌")
    if n_mal:
        lineas = [l for l in texto.splitlines() if "❌" in l or "Pista" in l][:6]
        return False, n_ok, n_mal, "chequeos en ❌:\n" + "\n".join(lineas)
    if n_ok == 0:
        return False, 0, 0, "no se imprimió ningún ✅ (¿faltan celdas de chequeo?)"
    return True, n_ok, 0, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rama", help="solo una rama, p. ej. R1")
    ap.add_argument("--modulo", help="solo un módulo, p. ej. R2-07")
    ap.add_argument("--timeout", type=int, default=600, help="segundos por notebook")
    args = ap.parse_args()

    notebooks = sorted(nb for n in NOMBRES for nb in ROOT.glob(f"ramas/*/R*/{n}"))
    notebooks.sort(key=lambda p: (p.parent.name, p.name))
    if args.rama:
        notebooks = [nb for nb in notebooks if nb.parent.name.startswith(args.rama)]
    if args.modulo:
        notebooks = [nb for nb in notebooks if nb.parent.name.startswith(args.modulo)]
    if not notebooks:
        print("No se encontraron notebooks."); return 1

    failed, skipped, passed, total_ok = [], [], [], 0
    for nb in notebooks:
        etiqueta = f"{nb.parent.name}/{nb.name}"
        if nb.parent.name in SKIP:
            skipped.append(etiqueta)
            print(f"SKIP {etiqueta} ({SKIP[nb.parent.name]})", flush=True)
            continue
        t0 = time.time()
        ok, n_ok, n_mal, detalle = ejecutar(nb, args.timeout)
        dt = time.time() - t0
        if ok:
            passed.append(etiqueta); total_ok += n_ok
            print(f"PASS {etiqueta} · {n_ok} ✅ ({dt:.0f}s)", flush=True)
        else:
            failed.append(etiqueta)
            print(f"FAIL {etiqueta} · {n_ok} ✅ {n_mal} ❌ ({dt:.0f}s)\n--- {detalle}\n---", flush=True)

    print(f"\nResumen: {len(passed)} PASS · {len(failed)} FAIL · {len(skipped)} SKIP "
          f"de {len(notebooks)} notebooks · {total_ok} chequeos en ✅")
    if failed:
        print("Fallaron: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
