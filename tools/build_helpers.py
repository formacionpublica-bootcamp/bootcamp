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


# Modelo por defecto del curso (revisado oct-2026: gemini-2.5-* quedó restringido a cuentas
# antiguas; 3.5-flash-lite está en la capa gratuita para proyectos nuevos). Cambiarlo AQUÍ
# y re-generar los notebooks; cada estudiante puede sobreescribirlo con GEMINI_MODEL.
GEMINI_MODEL = "gemini-3.5-flash-lite"

GET_LLM_SNIPPET = f'''# ── preguntar_llm(): el LLM (Gemini) detrás de UNA función ─────────────────────
# Cambiar de proveedor o de modelo = cambiar solo esta celda.
# En Colab: 🔑 (Secretos) → agrega GEMINI_API_KEY (gratis en aistudio.google.com).
import os

MODELO = os.environ.get("GEMINI_MODEL", "{GEMINI_MODEL}")

def _clave_gemini():
    try:                                   # Colab: secreto del notebook
        from google.colab import userdata
        return userdata.get("GEMINI_API_KEY")
    except Exception:                      # local: variable de entorno
        return os.environ.get("GEMINI_API_KEY")

def preguntar_llm(prompt, respaldo="[respuesta de respaldo — configura GEMINI_API_KEY para usar el LLM en vivo]"):
    """Envía el prompt a Gemini y devuelve el texto. Sin clave o sin red, devuelve
    `respaldo` para que el notebook siga corriendo (y se pueda verificar en CI)."""
    clave = _clave_gemini()
    if not clave:
        return respaldo
    try:
        from google import genai
        cliente = genai.Client(api_key=clave)
        return cliente.models.generate_content(model=MODELO, contents=prompt).text
    except Exception as e:
        print("⚠️ No se pudo llamar al LLM:", e)
        return respaldo

def get_llm():
    """Compatibilidad: devuelve una función generate(prompt)->str."""
    return preguntar_llm
'''


def write_notebook(nb, path):
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path
