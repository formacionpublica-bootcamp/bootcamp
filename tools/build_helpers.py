"""build_helpers.py — utilidades compartidas para generar notebooks (Fase 2).

Los notebooks del bootcamp se GENERAN con nbformat (no se escriben a mano).
Este módulo concentra las piezas comunes: celda de preparación del entorno con el
patrón "en vivo o caché", celdas de chequeo con assert + pista amable, y el snippet
get_llm() (Gemini) que usarán los módulos de R3.

Ejecutar los build_*.py con:  /opt/anaconda3/bin/python tools/build_R2-07.py
"""
import nbformat as nbf

REPO_RAW = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data"


def new_notebook():
    return nbf.v4.new_notebook(metadata={"language_info": {"name": "python"}})


def md(text):
    """Celda markdown."""
    return nbf.v4.new_markdown_cell(text.strip("\n"))


def code(src):
    """Celda de código."""
    return nbf.v4.new_code_cell(src.strip("\n"))


def setup_cell(csv_name, imports="import pandas as pd"):
    """Primera celda: carga el CSV local o lo baja de GitHub (en vivo o caché)."""
    src = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
{imports}

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "{csv_name}"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{REPO_RAW}/{csv_name}", CSV)

df = pd.read_csv(CSV)
print("Datos cargados:", df.shape, "filas x columnas")
df.head()'''
    return code(src)


def header_cell(code_id, titulo, linea, rol, semana, lograr, competencia, dato_real, n_checks):
    """Encabezado rico de lección, al estilo de los módulos existentes."""
    goals = "\n".join(f"{i}. {g}" for i, g in enumerate(lograr, 1))
    text = f'''# {code_id} · {titulo} — Lección

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Línea {linea} · *{rol}* · Semana {semana} · Se ejecuta en Google Colab.

> 🚀 **Cómo se trabaja:** lee, ejecuta cada celda con **▶︎** (o `Shift`+`Enter`) y completa los `TODO`. Cada ejercicio termina en una **celda de chequeo** que muestra ✅ si está bien o una pista si todavía no.

---

## ¿Qué vas a lograr?

{goals}

**Competencia de salida:** {competencia}

**Dato real:** {dato_real}

**Entregable:** que las **{n_checks} celdas de chequeo** muestren ✅.'''
    return md(text)


def exercise_md(n, titulo, cuerpo=""):
    """Celda markdown propia para cada ejercicio: '### ✍️ Ejercicio N — ...'."""
    txt = f"### ✍️ Ejercicio {n} — {titulo}"
    if cuerpo:
        txt += "\n\n" + cuerpo.strip("\n")
    return md(txt)


def check_cell(n, assert_block, hint):
    """Celda de chequeo · Ejercicio n — estilo casa: imprime ✅ / ❌+pista, sin cortar la ejecución."""
    indented = "\n".join("    " + ln for ln in assert_block.strip("\n").splitlines())
    src = f'''# ── Celda de chequeo · Ejercicio {n} ──────────────────────────────────────────
try:
{indented}
    print("✅ Ejercicio {n}: ¡correcto!")
except Exception as e:
    print("❌ Aún no. Revisa tu respuesta y vuelve a intentarlo.")
    print("   Pista:", {hint!r})
    print("   Detalle:", e)'''
    return code(src)


GET_LLM_SNIPPET = '''# ── get_llm(): proveedor de LLM (Gemini) detrás de una abstracción ────────────
# Decisión congelada: Gemini API (capa gratuita sin tarjeta). Cambiar de proveedor
# = cambiar solo esta función. Para agentes con baja latencia se puede usar Groq.
import os

def get_llm():
    """Devuelve una función generate(prompt)->str. En vivo si hay GEMINI_API_KEY,
    si no, cae a una respuesta cacheada para que el notebook sea verificable sin red."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return lambda prompt: model.generate_content(prompt).text
    # Fallback cacheado (sin red): respuesta de ejemplo para que los assert corran.
    return lambda prompt: "[respuesta cacheada de ejemplo — define GEMINI_API_KEY para usar el LLM en vivo]"
'''


def write_notebook(nb, path):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path
