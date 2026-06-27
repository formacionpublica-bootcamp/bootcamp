"""build_R3-00.py — módulo R3-00 (Onramp express + Prueba de Nivel).

Rama R3 (IA Aplicada), puerta de entrada. Python básico + JSON/APIs con patrón
'en vivo o caché' + una PRUEBA DE NIVEL (asserts de corte) que habilita entrada
directa a R3-01. NO llama a un LLM real. Sigue la convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R3-00.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-00-onramp-express-prueba-nivel")

IMPORTS = "import pandas as pd\nimport json, urllib.request"

EJ = [
 ("## 1. Variables, listas y comprensiones",
  "En Python casi todo es **recorrer una colección**. Tomamos los montos reales de compras "
  "públicas como una lista y los resumimos sin pandas.",
  "Resume la lista de montos",
  '''montos = df["monto_total"].tolist()
total = sum(montos)
sobre_un_millon = len([m for m in montos if m > 1_000_000])
print("total:", total, "| órdenes > $1M:", sobre_un_millon)''',
  '''montos = df["monto_total"].tolist()
# TODO: suma de todos los montos
total = ...
# TODO: cuántos montos superan 1.000.000 (usa una comprensión de lista)
sobre_un_millon = ...
print("total:", total, "| órdenes > $1M:", sobre_un_millon)''',
  '''assert abs(total - df["monto_total"].sum()) < 1e-6
assert sobre_un_millon == int((df["monto_total"] > 1_000_000).sum())''',
  "sum(montos) para el total; [m for m in montos if m > 1_000_000] y su len().",
  None),

 ("## 2. Funciones: empaquetar una decisión",
  "Una **función** encapsula una regla reutilizable. Clasifiquemos cada compra por tramo de monto.",
  "Escribe `clasificar`",
  '''def clasificar(monto):
    if monto < 100_000:
        return "bajo"
    elif monto < 1_000_000:
        return "medio"
    return "alto"

print(clasificar(50_000), clasificar(500_000), clasificar(2_000_000))''',
  '''def clasificar(monto):
    # TODO: "bajo" si < 100.000; "medio" si < 1.000.000; "alto" en otro caso
    ...

print(clasificar(50_000), clasificar(500_000), clasificar(2_000_000))''',
  '''assert clasificar(50_000) == "bajo"
assert clasificar(500_000) == "medio"
assert clasificar(2_000_000) == "alto"''',
  "Usa if/elif/else comparando monto contra 100_000 y 1_000_000.",
  None),

 ("## 3. JSON: el idioma de las APIs",
  "Las APIs devuelven **JSON**, que en Python se convierte en diccionarios y listas. "
  "Practiquemos extraer datos de una respuesta típica.",
  "Parsea el JSON y suma los ítems",
  '''texto = '{"orden": 123, "items": [{"nombre": "pan", "monto": 500}, {"nombre": "leche", "monto": 800}]}'
data = json.loads(texto)
monto_items = sum(it["monto"] for it in data["items"])
print("orden:", data["orden"], "| total ítems:", monto_items)''',
  '''texto = '{"orden": 123, "items": [{"nombre": "pan", "monto": 500}, {"nombre": "leche", "monto": 800}]}'
data = json.loads(texto)
# TODO: suma el "monto" de cada item en data["items"]
monto_items = ...
print("orden:", data["orden"], "| total ítems:", monto_items)''',
  '''assert data["orden"] == 123
assert monto_items == 1300''',
  "json.loads(texto) da un dict; recorre data['items'] sumando it['monto'].",
  None),

 ("## 4. En vivo o caché: APIs que no te dejan tirado",
  "Una API real puede fallar (sin red, caída, límite). El patrón **en vivo o caché**: intenta la "
  "llamada y, si falla, usa una copia. Así tu notebook siempre corre.",
  "Escribe `cargar_o_cache`",
  '''def cargar_o_cache(url, fallback):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.load(r)
    except Exception:
        return fallback

datos = cargar_o_cache("http://no-existe.invalid/x.json", {"fuente": "cache", "n": 3})
print(datos)''',
  '''def cargar_o_cache(url, fallback):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.load(r)
    except Exception:
        # TODO: si la llamada falla, devuelve el fallback
        ...

datos = cargar_o_cache("http://no-existe.invalid/x.json", {"fuente": "cache", "n": 3})
print(datos)''',
  '''assert datos["fuente"] == "cache"
assert callable(cargar_o_cache)''',
  "En el except, return fallback. La URL inválida fuerza el camino de caché.",
  None),

 ("## 5. Prueba de Nivel (PN) — ¿puedes saltar directo a R3-01?",
  "Si resuelves esto **sin ayuda**, dominas el prerequisito (Python + colecciones + funciones) y "
  "puedes entrar directo a *Introducción al NLP*. Es el **corte** de entrada por la vía (b).",
  "Resuelve las tres tareas de corte",
  '''def filtra_mayores(lista, umbral):
    return [x for x in lista if x > umbral]

def cuenta_palabras(texto):
    return len(texto.split())

def gasto_por_clave(registros):
    out = {}
    for r in registros:
        out[r["region"]] = out.get(r["region"], 0) + r["monto"]
    return out

print(filtra_mayores([1, 5, 3, 8], 4), cuenta_palabras("compras públicas del estado"),
      gasto_por_clave([{"region": "A", "monto": 100}, {"region": "A", "monto": 50}]))''',
  '''def filtra_mayores(lista, umbral):
    # TODO: devuelve los elementos de lista mayores que umbral
    ...

def cuenta_palabras(texto):
    # TODO: número de palabras en texto
    ...

def gasto_por_clave(registros):
    # TODO: dict {region: suma de monto} recorriendo registros
    ...

print(filtra_mayores([1, 5, 3, 8], 4), cuenta_palabras("compras públicas del estado"),
      gasto_por_clave([{"region": "A", "monto": 100}, {"region": "A", "monto": 50}]))''',
  '''assert filtra_mayores([1, 5, 3, 8], 4) == [5, 8]
assert cuenta_palabras("compras públicas del estado") == 4
assert gasto_por_clave([{"region": "A", "monto": 100}, {"region": "A", "monto": 50}]) == {"A": 150}''',
  "Comprensión con if; texto.split() y su len; acumula en un dict con .get(clave, 0).",
  None),
]

CIERRE = '''## Cierre

- Recorrer colecciones, escribir **funciones** y manejar **JSON** es el 80% de lo que usarás en R3.
- El patrón **en vivo o caché** hace tus notebooks robustos cuando dependes de APIs.
- Si aprobaste la **Prueba de Nivel**, puedes saltar directo a **R3-01 · Introducción al NLP**.

> *En R3 usaremos un LLM (Gemini) detrás de `get_llm()`; aquí solo sentamos las bases de Python y datos.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-00", "Onramp express + Prueba de Nivel", "C", "IA Aplicada", "0–1",
                      ["Manejar variables, listas y **comprensiones** sobre datos reales.",
                       "Escribir **funciones** que encapsulan reglas.",
                       "Leer **JSON** y aplicar el patrón **en vivo o caché** con APIs.",
                       "Aprobar la **Prueba de Nivel** para entrar directo a R3-01."],
                      "tener listo el prerequisito de Python/datos para la rama de IA Aplicada.",
                      "montos de compras públicas reales (ChileCompra) + respuestas tipo API.",
                      n_checks=5),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Cargamos datos reales como base (arriba). Vamos por partes."),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización ───────────────────────────────────────────────────────────
PROF_PREP = '''# Sin dependencias externas: Python puro para afianzar el prerequisito.
print("Listo para profundizar.")'''

PROF_EJ = [
 ("## 1. Diccionarios por comprensión",
  "Agregar con un dict es pan de cada día al preparar datos para un LLM.",
  "Agrupa montos por región con un dict",
  '''regs = [{"region": "A", "monto": 100}, {"region": "B", "monto": 40}, {"region": "A", "monto": 60}]
regiones = {r["region"] for r in regs}
por_region = {x: sum(r["monto"] for r in regs if r["region"] == x) for x in regiones}
print(por_region)''',
  '''regs = [{"region": "A", "monto": 100}, {"region": "B", "monto": 40}, {"region": "A", "monto": 60}]
regiones = {r["region"] for r in regs}
# TODO: dict por comprensión {region: suma de montos de esa region}
por_region = ...
print(por_region)''',
  '''assert por_region == {"A": 160, "B": 40}''',
  "{x: sum(r['monto'] for r in regs if r['region']==x) for x in regiones}."),

 ("## 2. Manejo de errores robusto",
  "Al parsear texto de fuentes reales, los datos vienen sucios. Una función defensiva evita que todo se caiga.",
  "Escribe `a_numero` que nunca lanza error",
  '''def a_numero(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return None

print(a_numero("1234.5"), a_numero("$mil"), a_numero(None))''',
  '''def a_numero(x):
    # TODO: intenta float(x); si falla, devuelve None (sin lanzar error)
    ...

print(a_numero("1234.5"), a_numero("$mil"), a_numero(None))''',
  '''assert a_numero("1234.5") == 1234.5
assert a_numero("$mil") is None
assert a_numero(None) is None''',
  "try: float(x) except (ValueError, TypeError): return None."),

 ("## 3. Preludio de NLP: normalizar texto",
  "Antes de dárselo a un LLM o a un buscador, el texto se **normaliza**. Primer paso del pipeline de R3-01.",
  "Escribe `normaliza`",
  '''def normaliza(texto):
    return texto.strip().lower().split()

print(normaliza("  Compras  PÚBLICAS del Estado  "))''',
  '''def normaliza(texto):
    # TODO: quita espacios extremos, pasa a minúsculas y separa en palabras
    ...

print(normaliza("  Compras  PÚBLICAS del Estado  "))''',
  '''assert normaliza("  Hola  MUNDO ") == ["hola", "mundo"]
assert normaliza("Compras PÚBLICAS") == ["compras", "públicas"]''',
  "texto.strip().lower().split() colapsa espacios y separa en palabras."),
]

PROF_HEADER = '''# R3-00 · Onramp express — Profundización (opcional) 🔬

**Formación Pública — Línea C · IA Aplicada · Notebook de profundización**

Opcional. Afianza el prerequisito con **dicts por comprensión**, **manejo de errores** robusto y
un primer paso de **normalización de texto** (preludio del NLP de R3-01). Python puro, sin dependencias.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R3-00.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R3-00 · Onramp express + Prueba de Nivel

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-00-onramp-express-prueba-nivel/leccion.ipynb)

Puerta de entrada a la rama de IA Aplicada: Python básico + JSON/APIs con patrón **en vivo o caché**
+ **Prueba de Nivel** que habilita el ingreso directo a R3-01.

- `leccion.ipynb` — completa los `TODO`; la PN es el ejercicio de corte.
- `profundiza.ipynb` — opcional 🔬: dicts por comprensión, errores, normalización de texto.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
