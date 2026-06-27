"""build_R3-CAP.py — Capstone de la rama R3 (IA Aplicada).

Proyecto-plantilla de IA generativa SIN red y SIN LLM real: get_llm() en modo caché
(determinista), un mini-pipeline tipo RAG (recuperar + responder) sobre un corpus de
normativa de compras, ficha de uso responsable y rúbrica. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R3-CAP.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-CAP-capstone-ia-aplicada")

CORPUS_CELL = '''# Corpus de ejemplo (normativa de compras públicas). En tu proyecto, reemplázalo por
# los documentos de tu organismo. Sin red y sin LLM real: todo es verificable offline.
CORPUS = [
    "Las licitaciones publicas se rigen por la ley de compras y se publican en MercadoPublico.",
    "El convenio marco permite comprar a proveedores preacordados sin hacer una licitacion.",
    "El trato directo es excepcional y requiere una justificacion formal documentada.",
    "Los proveedores del Estado se clasifican por tamano: micro, pequena, mediana y grande.",
]

def get_llm():
    """Modo CACHE (determinista): NO llama a Gemini ni a la red. Para usar el LLM en vivo,
    define GEMINI_API_KEY y reemplaza esta función por la real (ver R3-00 / R3-02)."""
    def generar(prompt):
        return "Respuesta (modo cache, sin LLM real) basada en el contexto: " + prompt.strip()[:160]
    return generar

print("Corpus:", len(CORPUS), "documentos | get_llm en modo cache")'''

EJ = [
 ("## 1. Recuperación (la R de RAG)",
  "Un RAG primero **recupera** el documento más relevante. Versión simple: el de mayor solapamiento "
  "de palabras con la pregunta.",
  "Escribe `recuperar`",
  '''def recuperar(pregunta, corpus=CORPUS):
    palabras = set(pregunta.lower().split())
    return max(corpus, key=lambda d: len(palabras & set(d.lower().split())))

doc = recuperar("¿que es el convenio marco?")
print(doc)''',
  '''def recuperar(pregunta, corpus=CORPUS):
    palabras = set(pregunta.lower().split())
    # TODO: devuelve el documento del corpus con mayor solapamiento de palabras
    return ...

doc = recuperar("¿que es el convenio marco?")
print(doc)''',
  '''assert recuperar("¿que es el convenio marco?") in CORPUS
assert "convenio" in recuperar("¿que es el convenio marco?").lower()''',
  "max(corpus, key=lambda d: len(palabras & set(d.lower().split()))).",
  None),

 ("## 2. El LLM en modo caché (determinista)",
  "Para que el notebook sea **verificable sin red**, `get_llm()` devuelve respuestas deterministas. "
  "Mismo prompt → misma salida.",
  "Comprueba que el LLM-caché es determinista",
  '''llm = get_llm()
a = llm("pregunta de prueba")
b = llm("pregunta de prueba")
es_determinista = (a == b)
print("determinista:", es_determinista, "| tipo:", type(a).__name__)''',
  '''llm = get_llm()
# TODO: llama dos veces con el mismo prompt y compara
a = ...
b = ...
es_determinista = (a == b)
print("determinista:", es_determinista, "| tipo:", type(a).__name__)''',
  '''assert es_determinista
assert isinstance(a, str) and len(a) > 0''',
  "llm('mismo prompt') dos veces; deben ser iguales.",
  None),

 ("## 3. Responder con contexto (RAG completo)",
  "Une las piezas: **recuperar** el documento y pasárselo al **LLM** como contexto para responder.",
  "Escribe `responder`",
  '''def responder(pregunta, llm):
    doc = recuperar(pregunta)
    prompt = f"Contexto: '{doc}'. Pregunta: {pregunta}"
    return llm(prompt)

respuesta = responder("¿cuando se usa el trato directo?", get_llm())
print(respuesta)''',
  '''def responder(pregunta, llm):
    doc = recuperar(pregunta)
    # TODO: arma un prompt con el doc como contexto y la pregunta, y pásalo al llm
    prompt = ...
    return llm(prompt)

respuesta = responder("¿cuando se usa el trato directo?", get_llm())
print(respuesta)''',
  '''resp = responder("¿cuando se usa el trato directo?", get_llm())
assert isinstance(resp, str) and len(resp) > 0
assert "trato directo" in recuperar("¿cuando se usa el trato directo?").lower()''',
  "prompt = f\"Contexto: '{doc}'. Pregunta: {pregunta}\" y return llm(prompt).",
  None),
]

FICHA = '''## 4. Ficha de uso responsable

Toda solución de IA en el Estado debe acompañarse de esta ficha:

> **Uso previsto:** _(qué pregunta responde, para quién)_
> **Costo:** usar proveedor con **capa gratuita** (Gemini) + patrón en vivo o caché; estimar tokens por consulta.
> **Privacidad:** los datos de compras son **públicos**; NO enviar datos personales/sensibles a un LLM externo.
> **Verificabilidad (groundedness):** la respuesta **cita** el documento recuperado; sin fuente, no se publica.
> **Supervisión humana:** un funcionario revisa antes de cualquier decisión; el LLM **no decide**.'''

RUBRICA = '''## Rúbrica de evaluación

| Criterio | Qué se evalúa |
|---|---|
| **Utilidad pública** | Resuelve una pregunta real de gestión. |
| **Groundedness / citas** | La respuesta se apoya en un documento recuperado y citable. |
| **Costo / privacidad** | Usa capa gratuita; no expone datos sensibles. |
| **Reproducibilidad** | Corre sin red (modo caché) de principio a fin. |
| **Uso responsable** | Incluye la ficha y declara la supervisión humana. |

> **Entregable:** notebook reproducible (modo caché) + ficha de uso responsable + demo del RAG.'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-CAP", "Capstone — proyecto integrador de IA aplicada", "C", "IA Aplicada", "6–7",
                      ["Construir un mini **RAG**: recuperar + responder con contexto.",
                       "Trabajar con un **LLM en modo caché** (verificable sin red).",
                       "Documentar el **uso responsable** (costo, privacidad, groundedness).",
                       "Entregar un proyecto **reproducible**."],
                      "integrar recuperación y generación para responder preguntas públicas con citas y criterio.",
                      "normativa de compras públicas (corpus de ejemplo); reemplazable por el de tu organismo.",
                      n_checks=3),
        h.code(CORPUS_CELL),
        h.md("### El corpus y `get_llm()` (modo caché) están listos arriba. Armemos el RAG."),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(FICHA))
    cells.append(h.md(RUBRICA))
    nb.cells = cells
    return nb


PROF_PREP = '''# Sin red ni LLM real: corpus de ejemplo y utilidades de recuperación.
CORPUS = [
    "Las licitaciones publicas se rigen por la ley de compras y se publican en MercadoPublico.",
    "El convenio marco permite comprar a proveedores preacordados sin hacer una licitacion.",
    "El trato directo es excepcional y requiere una justificacion formal documentada.",
    "Los proveedores del Estado se clasifican por tamano: micro, pequena, mediana y grande.",
]
def score(pregunta, doc):
    return len(set(pregunta.lower().split()) & set(doc.lower().split()))
print("Listo:", len(CORPUS), "documentos")'''

PROF_EJ = [
 ("## 1. Medir la relevancia",
  "Para confiar en la recuperación, mide el **solapamiento** (score) entre pregunta y documento.",
  "Usa `score` para el mejor documento",
  '''pregunta = "convenio marco proveedores"
mejor = max(CORPUS, key=lambda d: score(pregunta, d))
s = score(pregunta, mejor)
print("mejor doc score:", s)''',
  '''pregunta = "convenio marco proveedores"
# TODO: elige el documento de mayor score y calcula ese score
mejor = ...
s = score(pregunta, mejor)
print("mejor doc score:", s)''',
  '''assert s >= 1
assert "convenio" in mejor.lower()''',
  "max(CORPUS, key=lambda d: score(pregunta, d)) y score(pregunta, mejor)."),

 ("## 2. Citar la fuente",
  "Sin cita no hay groundedness. Devuelve la respuesta **junto al índice y texto** de la fuente.",
  "Escribe `responder_con_cita`",
  '''def responder_con_cita(pregunta, corpus=CORPUS):
    idx = max(range(len(corpus)), key=lambda i: score(pregunta, corpus[i]))
    return {"fuente_idx": idx, "fuente": corpus[idx]}

r = responder_con_cita("trato directo justificacion")
print(r)''',
  '''def responder_con_cita(pregunta, corpus=CORPUS):
    # TODO: idx del documento de mayor score; devuelve dict con fuente_idx y fuente
    idx = ...
    return {"fuente_idx": idx, "fuente": corpus[idx]}

r = responder_con_cita("trato directo justificacion")
print(r)''',
  '''assert r["fuente"] in CORPUS
assert "trato directo" in r["fuente"].lower()''',
  "idx = max(range(len(corpus)), key=lambda i: score(pregunta, corpus[i]))."),

 ("## 3. No alucinar: fallback sin match",
  "Si nada es relevante, es más honesto **no responder** que inventar. Umbral mínimo de score.",
  "Escribe `recuperar_robusto`",
  '''def recuperar_robusto(pregunta, corpus=CORPUS, umbral=1):
    mejor = max(corpus, key=lambda d: score(pregunta, d))
    return mejor if score(pregunta, mejor) >= umbral else None

print(recuperar_robusto("xyzzy qwerty zzz"))''',
  '''def recuperar_robusto(pregunta, corpus=CORPUS, umbral=1):
    mejor = max(corpus, key=lambda d: score(pregunta, d))
    # TODO: devuelve 'mejor' solo si su score alcanza el umbral; si no, None
    return ...

print(recuperar_robusto("xyzzy qwerty zzz"))''',
  '''assert recuperar_robusto("xyzzy qwerty zzz") is None
assert recuperar_robusto("convenio marco") in CORPUS''',
  "return mejor if score(pregunta, mejor) >= umbral else None."),
]

PROF_HEADER = '''# R3-CAP · Capstone — Profundización (opcional) 🔬

**Formación Pública — Línea C · IA Aplicada · Notebook de profundización**

Opcional. Hacia un RAG confiable: **medir la relevancia**, **citar la fuente** y **no alucinar**
(fallback con umbral). Sin red ni LLM real.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización del capstone R3.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R3-CAP · Capstone — proyecto integrador de IA aplicada

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-CAP-capstone-ia-aplicada/leccion.ipynb)

Proyecto final de la rama R3: un mini-**RAG** (recuperar + responder con contexto) sobre normativa
de compras, con `get_llm()` en **modo caché** (verificable sin red), ficha de **uso responsable** y rúbrica.

- `leccion.ipynb` — plantilla con `TODO`; se autoverifica (✅). Para el LLM en vivo, ver R3-00/R3-02.
- `profundiza.ipynb` — opcional 🔬: medir relevancia, citar la fuente, fallback sin alucinar.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
