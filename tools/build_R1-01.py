"""build_R1-01.py — módulo R1-01 (Traer el dato: archivos, JSON y APIs).

Rama R1 (Análisis y Visualización). Funciones, lectura de archivos, JSON y APIs
con patrón 'en vivo o caché'. Rearmado 2026: dataset ancla = matrícula escolar
2025 (MINEDUC); el profundiza consulta la API CKAN de datos.gob.cl en vivo.
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-01-traer-el-dato")

IMPORTS = "import pandas as pd\nimport json, urllib.request, os\nimport matplotlib.pyplot as plt"

EJ = [
 ("## 1. Funciones para cargar datos",
  "Una **función** encapsula la carga para reutilizarla. Empezamos por leer un CSV con pandas.",
  "Escribe `cargar_csv`",
  '''def cargar_csv(ruta):
    return pd.read_csv(ruta)

datos = cargar_csv("matricula.csv")
print("Cargado:", datos.shape)''',
  '''def cargar_csv(ruta):
    # TODO: lee el CSV en 'ruta' con pandas y devuélvelo
    ...

datos = cargar_csv("matricula.csv")
print("Cargado:", datos.shape)''',
  '''assert cargar_csv("matricula.csv").shape == df.shape''',
  "pd.read_csv(ruta) y return.",
  None),

 ("## 2. JSON: el formato de las APIs",
  "Las APIs responden **JSON**. Con `json.loads` se convierte en diccionarios y listas que recorres.",
  "Parsea una respuesta y suma las matrículas",
  '''respuesta = '{"results": [{"comuna": "Arica", "matricula": 512}, {"comuna": "Putre", "matricula": 48}]}'
data = json.loads(respuesta)
matriculas = [r["matricula"] for r in data["results"]]
total = sum(matriculas)
print("registros:", len(data["results"]), "| total:", total)''',
  '''respuesta = '{"results": [{"comuna": "Arica", "matricula": 512}, {"comuna": "Putre", "matricula": 48}]}'
data = json.loads(respuesta)
# TODO: lista de matrículas de data["results"] y su suma
matriculas = ...
total = ...
print("registros:", len(data["results"]), "| total:", total)''',
  '''assert len(data["results"]) == 2
assert total == 560''',
  "json.loads(respuesta); luego [r['matricula'] for r in data['results']] y sum(...).",
  None),

 ("## 3. En vivo o caché: APIs que no fallan",
  "Una fuente remota puede caerse. El patrón **en vivo o caché**: intenta la fuente remota y, si falla, "
  "usa la copia local. Tu análisis siempre corre.",
  "Escribe `cargar_o_cache`",
  '''def cargar_o_cache(url, ruta_local):
    try:
        return pd.read_csv(url)
    except Exception:
        return pd.read_csv(ruta_local)

d = cargar_o_cache("http://no-existe.invalid/x.csv", "matricula.csv")
print("filas cargadas:", len(d))''',
  '''def cargar_o_cache(url, ruta_local):
    try:
        return pd.read_csv(url)
    except Exception:
        # TODO: si la fuente remota falla, lee el archivo local
        ...

d = cargar_o_cache("http://no-existe.invalid/x.csv", "matricula.csv")
print("filas cargadas:", len(d))''',
  '''assert len(d) == len(df)
assert callable(cargar_o_cache)''',
  "En el except: return pd.read_csv(ruta_local). La URL inválida fuerza el camino de caché.",
  None),

 ("## 4. Guardar el resultado",
  "Tras traer y resumir, **persistes** el resultado en un archivo para compartirlo o reutilizarlo.",
  "Guarda un resumen por región",
  '''resumen = df.groupby("region")["mat_total"].sum().reset_index()
resumen.to_csv("resumen_regiones.csv", index=False)
existe = os.path.exists("resumen_regiones.csv")
print("guardado:", existe, "| filas:", len(resumen))''',
  '''resumen = df.groupby("region")["mat_total"].sum().reset_index()
# TODO: guarda 'resumen' como CSV "resumen_regiones.csv" sin el índice
...
existe = os.path.exists("resumen_regiones.csv")
print("guardado:", existe, "| filas:", len(resumen))''',
  '''assert existe is True
assert pd.read_csv("resumen_regiones.csv").shape[0] == df["region"].nunique()''',
  "resumen.to_csv('resumen_regiones.csv', index=False).",
  '''# (ilustración) El resumen que acabamos de guardar
r = resumen.sort_values("mat_total").tail(8)
plt.figure(figsize=(6, 4))
plt.barh(r["region"], r["mat_total"], color="#4240e5")
plt.xlabel("Estudiantes matriculados"); plt.title("Matrícula por región (top 8)")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- Encapsula la carga en **funciones** reutilizables.
- Las APIs hablan **JSON**: `json.loads` lo vuelve diccionarios y listas.
- El patrón **en vivo o caché** hace tu trabajo robusto ante caídas de red.
- **Guarda** tus resultados para compartirlos y reutilizarlos.

> *Con el dato ya en casa, en R1-02 empezamos a explorarlo con pandas.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-01", "Traer el dato: archivos, JSON y APIs", "R1", "Analista de Datos", "2",
                      ["Escribir **funciones** que cargan datos.",
                       "Leer **JSON** de una respuesta tipo API.",
                       "Aplicar el patrón **en vivo o caché** ante fallos de red.",
                       "**Guardar** resultados en archivos."],
                      "traer datos públicos desde archivos y APIs de forma robusta.",
                      "matrícula escolar oficial 2025 (MINEDUC) en CSV + respuestas JSON tipo API.",
                      n_checks=4),
        h.setup_cell("matricula.csv", IMPORTS),
        h.md("### Datos base cargados arriba. Aprendamos a traerlos de varias fuentes."),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


PROF_PREP = '''import pandas as pd, json, os, urllib.request
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/matricula.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. JSON anidado",
  "Las respuestas reales anidan listas dentro de objetos. Practica navegarlas.",
  "Extrae los niveles anidados",
  '''payload = '{"rbd": 1, "niveles": [{"nivel": "parvularia", "matricula": 45}, {"nivel": "basica", "matricula": 320}, {"nivel": "media", "matricula": 210}]}'
data = json.loads(payload)
niveles = [n["nivel"] for n in data["niveles"]]
print(niveles)''',
  '''payload = '{"rbd": 1, "niveles": [{"nivel": "parvularia", "matricula": 45}, {"nivel": "basica", "matricula": 320}, {"nivel": "media", "matricula": 210}]}'
data = json.loads(payload)
# TODO: lista con el "nivel" de cada elemento en data["niveles"]
niveles = ...
print(niveles)''',
  '''assert niveles == ["parvularia", "basica", "media"]''',
  "[n['nivel'] for n in data['niveles']]."),

 ("## 2. Carga robusta con descarga y caché en disco",
  "El patrón completo: si no está en disco, descarga; si la descarga falla, avisa sin romper.",
  "Escribe `asegurar_csv`",
  '''def asegurar_csv(ruta, url):
    if os.path.exists(ruta):
        return "local"
    try:
        urllib.request.urlretrieve(url, ruta)
        return "descargado"
    except Exception:
        return "sin_datos"

estado = asegurar_csv("matricula.csv", "http://no-existe.invalid/x.csv")
print(estado)''',
  '''def asegurar_csv(ruta, url):
    if os.path.exists(ruta):
        return "local"
    try:
        urllib.request.urlretrieve(url, ruta)
        return "descargado"
    except Exception:
        # TODO: si falla la descarga, devuelve "sin_datos"
        ...

estado = asegurar_csv("matricula.csv", "http://no-existe.invalid/x.csv")
print(estado)''',
  '''assert estado == "local"''',
  "El archivo ya existe localmente, así que debe devolver 'local'."),

 ("## 3. Normalizar tipos al cargar",
  "Los datos vienen sucios: a veces los números llegan como texto. Conviértelos con seguridad.",
  "Escribe `a_float`",
  '''def a_float(x):
    try:
        return float(str(x).replace("$", "").replace(".", "").replace(",", "."))
    except ValueError:
        return None

print(a_float("1.234,50"), a_float("$2000"), a_float("N/A"))''',
  '''def a_float(x):
    try:
        return float(str(x).replace("$", "").replace(".", "").replace(",", "."))
    except ValueError:
        # TODO: si no se puede convertir, devuelve None
        ...

print(a_float("1.234,50"), a_float("$2000"), a_float("N/A"))''',
  '''assert a_float("1.234,50") == 1234.50
assert a_float("N/A") is None''',
  "En el except ValueError: return None."),

 ("## 4. Una API estatal de verdad: datos.gob.cl",
  "El portal de datos abiertos del Estado tiene una **API real** (CKAN). Consultémosla en vivo, "
  "con caché de respaldo por si no hay red: el mismo patrón de la lección, contra una API que existe.",
  "Consulta cuántos datasets de matrícula hay en datos.gob.cl",
  '''URL = "https://datos.gob.cl/api/3/action/package_search?q=matricula&rows=3"
CACHE = '{"success": true, "result": {"count": 42, "results": [{"title": "Matrícula (caché)"}]}}'

def consultar_api(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return json.loads(CACHE)

data = consultar_api(URL)
n_datasets = data["result"]["count"]
print("datasets sobre matrícula en datos.gob.cl:", n_datasets)
for res in data["result"]["results"]:
    print(" -", res["title"])''',
  '''URL = "https://datos.gob.cl/api/3/action/package_search?q=matricula&rows=3"
CACHE = '{"success": true, "result": {"count": 42, "results": [{"title": "Matrícula (caché)"}]}}'

def consultar_api(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return json.loads(CACHE)

data = consultar_api(URL)
# TODO: el número total de datasets está en data["result"]["count"]
n_datasets = ...
print("datasets sobre matrícula en datos.gob.cl:", n_datasets)''',
  '''assert data["success"] is True
assert isinstance(n_datasets, int) and n_datasets > 0''',
  "data['result']['count'] — navega el JSON igual que en el ejercicio 1."),
]

PROF_HEADER = '''# R1-01 · Traer el dato — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional. **JSON anidado**, carga robusta con **descarga + caché en disco**, **normalización de
tipos** y una consulta **en vivo a la API de datos.gob.cl**. Mismos datos de matrícula escolar.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-01.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-01 · Traer el dato: archivos, JSON y APIs

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-01-traer-el-dato/leccion.ipynb)

Funciones de carga, **JSON**, patrón **en vivo o caché** y guardado de resultados, sobre la
matrícula escolar oficial 2025 (`matricula.csv`, MINEDUC). El profundiza consulta en vivo la
API CKAN de datos.gob.cl.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: JSON anidado, descarga+caché, tipos, API de datos.gob.cl.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
