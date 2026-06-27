"""materializar_ramas.py — crea ramas/Rx/ y copia los notebooks 'Reusar'.

Las 3 ramas son INDEPENDIENTES: un mismo módulo fuente puede copiarse a varias ramas.
Solo materializa los módulos de estado 'Reusar' (single-source, copia tal cual).
Los módulos Refactor / 🆕 Nuevo / fundamentos condensados los generan los build_*.py.

Uso:  python3 tools/materializar_ramas.py        (la copia es idempotente)
"""
import os, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BRANCH_DIR = {
    "R1": "ramas/R1-analisis-visualizacion",
    "R2": "ramas/R2-cientifico-de-datos",
    "R3": "ramas/R3-ia-aplicada",
}

# (código destino, rama, carpeta fuente, nombre carpeta destino)
REUSE_MAP = [
    # R1 · Análisis y Visualización
    ("R1-02", "R1", "A1-exploracion-con-pandas",   "R1-02-exploracion-con-pandas"),
    ("R1-03", "R1", "A2-cruzar-y-resumir-tablas",  "R1-03-cruzar-y-resumir-tablas"),
    ("R1-04", "R1", "A3-limpieza-de-datos",        "R1-04-limpieza-de-datos"),
    ("R1-05", "R1", "A4-sql-fundamentos",          "R1-05-sql-para-analisis"),
    ("R1-06", "R1", "A5-estadistica-descriptiva",  "R1-06-estadistica-descriptiva"),
    # R2 · Científico de Datos
    ("R2-02", "R2", "B1-sql-para-features",        "R2-02-sql-para-features"),
    ("R2-04", "R2", "B2-fundamentos-de-ml",        "R2-04-fundamentos-de-ml"),
    ("R2-05", "R2", "B3-modelos-de-arboles",       "R2-05-modelos-de-arboles"),
    ("R2-06", "R2", "B4-clasificacion-y-clustering","R2-06-clasificacion-y-clustering"),
    ("R2-08", "R2", "B5-pipelines-reproducibles",  "R2-08-pipelines-reproducibles"),
    ("R2-09", "R2", "B6-despliegue-de-modelos",    "R2-09-despliegue-de-modelos"),
    ("R2-10", "R2", "B7-series-temporales",        "R2-10-series-temporales"),
    # R3 · IA Aplicada
    ("R3-01", "R3", "C1-introduccion-al-nlp",      "R3-01-introduccion-al-nlp"),
    ("R3-02", "R3", "A7-ia-generativa-y-llms",     "R3-02-ia-generativa-y-llms"),
    ("R3-03", "R3", "C2-rag",                      "R3-03-rag"),
    ("R3-04", "R3", "C3-agentes",                  "R3-04-agentes"),
]

COPY_NAMES = ("leccion.ipynb", "solucion.ipynb", "README.md")


def main():
    # estructura base
    for d in BRANCH_DIR.values():
        os.makedirs(os.path.join(ROOT, d, "sample_projects"), exist_ok=True)

    copied, missing = 0, []
    for code, branch, src, dest in REUSE_MAP:
        src_dir = os.path.join(ROOT, src)
        dest_dir = os.path.join(ROOT, BRANCH_DIR[branch], dest)
        if not os.path.isdir(src_dir):
            missing.append((code, src))
            continue
        os.makedirs(dest_dir, exist_ok=True)
        for name in COPY_NAMES:
            sp = os.path.join(src_dir, name)
            if os.path.exists(sp):
                shutil.copy2(sp, os.path.join(dest_dir, name))
        # copiar también los CSV locales que la lección use como caché
        for f in os.listdir(src_dir):
            if f.endswith(".csv"):
                shutil.copy2(os.path.join(src_dir, f), os.path.join(dest_dir, f))
        copied += 1
        print(f"  {code:6} ← {src}  →  {dest}")

    print(f"\nMaterializados {copied}/{len(REUSE_MAP)} módulos Reusar.")
    if missing:
        print("⚠️  Fuentes no encontradas:", missing)


if __name__ == "__main__":
    main()
