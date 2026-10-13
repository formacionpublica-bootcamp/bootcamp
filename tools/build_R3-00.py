"""build_R3-00.py — módulo R3-00 (Onramp express + Prueba de Nivel).

Rama R3 (IA Aplicada), puerta de entrada. Python + JSON express sobre el ANCLA de
la rama: las fichas de trámites de ChileAtiende (fichas.csv). Strings, listas,
diccionarios, funciones, el JSON de una ficha, el patrón «en vivo o caché» y una
PRUEBA DE NIVEL que habilita la entrada directa a R3-01. NO llama a un LLM.
Rearmado 2026 (nueva versión sobre fichas). Profundiza =
transferencia: calidad del aire (SINCA) convertida en una respuesta tipo API (JSON).

Uso:  /opt/anaconda3/bin/python tools/build_R3-00.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-00-onramp-express-prueba-nivel")

RAW = h.REPO_RAW
IMPORTS = "import pandas as pd\nimport json"

INTRO = '''## El dato de toda la rama: las fichas de ChileAtiende

Cada fila de `df` es una **ficha de trámite** publicada en ChileAtiende: 245 fichas reales,
de 64 instituciones y 18 temas (bonos, salud, vivienda, jubilación…). La columna `texto`
trae la ficha completa, tal como la lee la ciudadanía.

En toda la rama R3 trabajaremos sobre estas fichas: en R3-01 las **clasificarás** por tema,
en R3-02 un **LLM** las resumirá en lenguaje claro, y más adelante construirás un asistente
que **responde preguntas** citándolas. Aquí, primero, el Python mínimo para manipularlas.

> Ejecuta la celda de abajo para ver la ficha con la que trabajaremos en los primeros ejercicios.'''

FICHA = '''# Una ficha concreta: el Bono de Invierno (id 39484)
ficha = df[df["id"] == 39484].iloc[0]
print(ficha["titulo"], "·", ficha["institucion"], "·", ficha["tema"])
print(ficha["url"])
print()
print(ficha["texto"][:400], "...")'''

EJ = [
 ("## 1. Strings: el texto es una cadena de caracteres",
  "Un texto en Python es un **string** (`str`). Tiene métodos para pasarlo a mayúsculas "
  "(`.upper()`), partirlo en palabras (`.split()`) o en líneas (`.split(\"\\n\")`), y el "
  "operador `in` responde «¿aparece esto dentro?». Así se empieza a «leer» una ficha con código.",
  "Explora el texto de la ficha",
  '''titulo = ficha["titulo"]
texto = ficha["texto"]
titulo_mayus = titulo.upper()
n_palabras = len(texto.split())
primera_linea = texto.split("\\n")[0]
menciona_ips = "IPS" in texto
print(titulo_mayus, "|", n_palabras, "palabras | ¿menciona al IPS?", menciona_ips)
print("Primera línea:", primera_linea)''',
  '''titulo = ficha["titulo"]
texto = ficha["texto"]
# TODO: el título en MAYÚSCULAS
titulo_mayus = ...
# TODO: cuántas palabras tiene el texto (parte por espacios y cuenta)
n_palabras = ...
# TODO: la primera línea del texto (parte por "\\n" y toma el elemento 0)
primera_linea = ...
# TODO: ¿aparece "IPS" dentro del texto? (True / False)
menciona_ips = ...
print(titulo_mayus, "|", n_palabras, "palabras | ¿menciona al IPS?", menciona_ips)
print("Primera línea:", primera_linea)''',
  '''assert titulo_mayus == "BONO DE INVIERNO"
assert n_palabras == ficha["n_palabras"], "debe coincidir con la columna n_palabras"
assert primera_linea.startswith("Es un beneficio no postulable")
assert isinstance(menciona_ips, bool) and menciona_ips == ("IPS" in texto)''',
  'titulo.upper(); len(texto.split()); texto.split("\\n")[0]; "IPS" in texto.',
  None),

 ("## 2. Listas y comprensiones: recorrer las 245 fichas",
  "Una **lista** guarda muchos valores en orden. Una **comprensión de lista** crea una lista "
  "nueva filtrando otra, en una línea que se lee casi en castellano: "
  "`[t for t in titulos if \"certificado\" in t.lower()]` = «cada título t, si contiene "
  "“certificado”».",
  "Filtra y resume con listas",
  '''titulos = df["titulo"].tolist()
palabras = df["n_palabras"].tolist()
con_certificado = [t for t in titulos if "certificado" in t.lower()]
n_extensas = len([p for p in palabras if p > 1000])
promedio = sum(palabras) / len(palabras)
print(len(con_certificado), "títulos con 'certificado' | fichas > 1.000 palabras:", n_extensas,
      "| promedio:", round(promedio))
print(con_certificado[:3])''',
  '''titulos = df["titulo"].tolist()
palabras = df["n_palabras"].tolist()
# TODO: títulos que contienen "certificado" (sin importar mayúsculas: usa t.lower())
con_certificado = ...
# TODO: cuántas fichas tienen MÁS de 1000 palabras
n_extensas = ...
# TODO: promedio de palabras por ficha (sum / len)
promedio = ...
print("fichas > 1.000 palabras:", n_extensas, "| promedio:", promedio)''',
  '''assert len(con_certificado) == int(df["titulo"].str.lower().str.contains("certificado").sum())
assert n_extensas == int((df["n_palabras"] > 1000).sum())
assert abs(promedio - df["n_palabras"].mean()) < 1e-9''',
  "[t for t in titulos if 'certificado' in t.lower()]; len([p for p in palabras if p > 1000]); sum(palabras)/len(palabras).",
  None),

 ("## 3. Diccionarios: contar por categoría",
  "Un **diccionario** (`dict`) guarda pares **clave → valor**, como una ficha: "
  "`{\"salud\": 15, \"vivienda\": 15}`. El patrón clásico para contar es "
  "`conteo[clave] = conteo.get(clave, 0) + 1`: «súmale uno a lo que había (o a 0 si no había nada)».",
  "Cuenta las fichas por tema con un dict",
  '''conteo = {}
for tema in df["tema"]:
    conteo[tema] = conteo.get(tema, 0) + 1
tema_top = max(conteo, key=conteo.get)
print(len(conteo), "temas | el primero con más fichas:", tema_top, "→", conteo[tema_top])''',
  '''conteo = {}
for tema in df["tema"]:
    # TODO: suma 1 al conteo de este tema (usa conteo.get(tema, 0))
    ...
# TODO: el tema con más fichas: max(conteo, key=conteo.get)
tema_top = ...
print("tema con más fichas:", tema_top)''',
  '''assert conteo == df["tema"].value_counts().to_dict()
assert conteo[tema_top] == max(conteo.values())''',
  "Dentro del for: conteo[tema] = conteo.get(tema, 0) + 1. Luego max(conteo, key=conteo.get).",
  None),

 ("## 4. Funciones: empaquetar una regla",
  "Una **función** encapsula una regla para reutilizarla. Clasifiquemos cada ficha por su "
  "**extensión**: una ficha extensa es más difícil de leer — y, en R3-02, más cara de enviarle a un LLM.",
  "Escribe `extension`",
  '''def extension(n_palabras):
    if n_palabras < 300:
        return "breve"
    elif n_palabras < 700:
        return "media"
    return "extensa"

df["extension"] = df["n_palabras"].apply(extension)
print(extension(150), extension(435), extension(765))
print(df["extension"].value_counts())''',
  '''def extension(n_palabras):
    # TODO: "breve" si < 300; "media" si < 700; "extensa" en otro caso
    ...

df["extension"] = df["n_palabras"].apply(extension)
print(extension(150), extension(435), extension(765))
print(df["extension"].value_counts())''',
  '''assert extension(150) == "breve" and extension(435) == "media" and extension(765) == "extensa"
assert extension(300) == "media" and extension(700) == "extensa"
assert int((df["extension"] == "breve").sum()) == int((df["n_palabras"] < 300).sum())''',
  "if n_palabras < 300: return 'breve' / elif n_palabras < 700: return 'media' / return 'extensa'.",
  None),

 ("## 5. JSON: la ficha como la entregaría una API",
  "Las APIs — incluida la del LLM que usarás en R3-02 — hablan **JSON**: texto con llaves y "
  "corchetes que en Python se vuelve `dict` y `list`. `json.dumps` convierte un dict en texto "
  "JSON y `json.loads` hace el camino de vuelta.\n\n"
  "> ⚠️ Gotcha real: los números que salen de pandas son de tipo `numpy.int64`, y `json.dumps` "
  "**no los acepta**. Por eso se envuelven en `int(...)`.",
  "Arma el JSON de la ficha y recupéralo",
  '''registro = {
    "id": int(ficha["id"]),
    "titulo": ficha["titulo"],
    "institucion": ficha["institucion"],
    "n_palabras": int(ficha["n_palabras"]),
    "primeras_lineas": ficha["texto"].split("\\n")[:2],
}
texto_json = json.dumps(registro, ensure_ascii=False, indent=2)
recuperado = json.loads(texto_json)
print(texto_json)''',
  '''registro = {
    "id": int(ficha["id"]),
    "titulo": ficha["titulo"],
    "institucion": ...,   # TODO: la institución de la ficha
    "n_palabras": ...,    # TODO: n_palabras envuelto en int(...)
    "primeras_lineas": ficha["texto"].split("\\n")[:2],
}
# TODO: convierte registro a texto JSON (json.dumps, con ensure_ascii=False e indent=2)
texto_json = ...
# TODO: y de vuelta a dict (json.loads)
recuperado = ...
print(texto_json)''',
  '''assert isinstance(texto_json, str) and texto_json.strip().startswith("{")
assert recuperado == registro
assert set(registro) == {"id", "titulo", "institucion", "n_palabras", "primeras_lineas"}
assert recuperado["n_palabras"] == 765 and len(recuperado["primeras_lineas"]) == 2''',
  'Dentro del dict: "institucion": ficha["institucion"], "n_palabras": int(ficha["n_palabras"]). Luego json.dumps(...) y json.loads(texto_json).',
  None),

 ("## 6. En vivo o caché: APIs que no te dejan tirado",
  "Una API real puede fallar (sin red, caída, límite de uso). El patrón **en vivo o caché**: "
  "intenta la llamada y, si falla, usa una copia. Es exactamente lo que hará `preguntar_llm()` "
  "en R3-02: si no hay clave o red, devuelve una respuesta de respaldo y el notebook sigue.",
  "Escribe `cargar_o_cache`",
  '''import urllib.request

def cargar_o_cache(url, respaldo):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.load(r)
    except Exception:
        return respaldo

datos = cargar_o_cache("http://no-existe.invalid/ficha.json", registro)
print(datos["titulo"], "(desde el respaldo)")''',
  '''import urllib.request

def cargar_o_cache(url, respaldo):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            return json.load(r)
    except Exception:
        # TODO: si la llamada falla, devuelve el respaldo
        ...

datos = cargar_o_cache("http://no-existe.invalid/ficha.json", registro)
print(datos)''',
  '''assert datos == registro
assert cargar_o_cache("http://no-existe.invalid/x.json", {"fuente": "cache"}) == {"fuente": "cache"}''',
  "En el except: return respaldo. La URL inválida fuerza el camino del respaldo.",
  None),

 ("## 7. Prueba de Nivel (PN) — ¿puedes saltar directo a R3-01?",
  "Si resuelves esto **sin ayuda**, dominas el prerequisito (colecciones + funciones + dicts) y "
  "puedes entrar directo a *Introducción al NLP*. Es el **corte** de entrada por la vía (b).",
  "Resuelve las tres tareas de corte",
  '''def filtra_mayores(lista, umbral):
    return [x for x in lista if x > umbral]

def cuenta_palabras(texto):
    return len(texto.split())

def conteo_por_clave(registros, clave):
    out = {}
    for r in registros:
        out[r[clave]] = out.get(r[clave], 0) + 1
    return out

print(filtra_mayores([150, 435, 765], 400), cuenta_palabras("Bono de Invierno"),
      conteo_por_clave([{"tema": "salud"}, {"tema": "salud"}, {"tema": "vivienda"}], "tema"))''',
  '''def filtra_mayores(lista, umbral):
    # TODO: devuelve los elementos de lista mayores que umbral
    ...

def cuenta_palabras(texto):
    # TODO: número de palabras en texto
    ...

def conteo_por_clave(registros, clave):
    # TODO: dict {valor de r[clave]: cuántas veces aparece} recorriendo registros
    ...

print(filtra_mayores([150, 435, 765], 400), cuenta_palabras("Bono de Invierno"),
      conteo_por_clave([{"tema": "salud"}, {"tema": "salud"}, {"tema": "vivienda"}], "tema"))''',
  '''assert filtra_mayores([150, 435, 765], 400) == [435, 765]
assert cuenta_palabras("Bono de Invierno") == 3
assert conteo_por_clave([{"tema": "salud"}, {"tema": "salud"}, {"tema": "vivienda"}], "tema") == {"salud": 2, "vivienda": 1}
assert conteo_por_clave(df.to_dict("records"), "institucion") == df["institucion"].value_counts().to_dict()''',
  "Comprensión con if; texto.split() y su len; acumula en un dict con out.get(r[clave], 0) + 1.",
  None),
]

CIERRE = '''## Cierre

- Un texto es un **string**: `.split()`, `.upper()`, `in` y `.split("\\n")` ya permiten «leer» una ficha con código.
- **Listas**, **comprensiones** y **diccionarios** resumen 245 fichas sin pandas — y son exactamente las estructuras que viajan en un JSON.
- `json.dumps` / `json.loads` traducen entre Python y el idioma de las APIs (ojo con `numpy.int64`: envuélvelo en `int`).
- El patrón **en vivo o caché** hace tus notebooks robustos cuando dependes de un servicio externo.
- Si aprobaste la **Prueba de Nivel**, puedes saltar directo a **R3-01 · Introducción al NLP**.

> *En R3-01 convertirás el texto de estas mismas fichas en números (frecuencias, TF-IDF) para
> que un modelo aprenda a reconocer el tema de cada una.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-00", "Onramp express + Prueba de Nivel", "R3", "Especialista en IA Aplicada", "0–1",
                      ["Manipular **strings**: partir un texto en palabras y líneas, buscar dentro.",
                       "Recorrer colecciones con **listas**, **comprensiones** y **diccionarios**.",
                       "Escribir **funciones** que encapsulan una regla.",
                       "Convertir una ficha a **JSON** (y de vuelta) y aplicar el patrón **en vivo o caché**.",
                       "Aprobar la **Prueba de Nivel** para entrar directo a R3-01."],
                      "tener listo el prerequisito de Python y JSON para la rama de IA Aplicada.",
                      "245 fichas de trámites de ChileAtiende con su texto completo (18 temas, 64 instituciones).",
                      n_checks=len(EJ)),
        h.setup_cell("fichas.csv", IMPORTS),
        h.md(INTRO),
        h.code(FICHA),
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


# ── Profundización (transferencia: calidad del aire → JSON tipo API) ─────────
PROF_PREP = f'''import os, json, urllib.request
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "estaciones.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

aire = pd.read_csv("aire_diario.csv")          # PM2,5 diario por estación (SINCA, 2020-2025)
estaciones = pd.read_csv("estaciones.csv")     # dónde está cada estación
print("aire:", aire.shape, "| estaciones:", estaciones.shape)
aire.head(3)'''

PROF_EJ = [
 ("## 1. De tabla a lista de dicts (y un dict por comprensión)",
  "`df.to_dict(\"records\")` convierte una tabla en una **lista de diccionarios** — exactamente "
  "la forma de un JSON. Con un **dict por comprensión** armas un «buscador» estación → región.",
  "Construye el buscador `region_de`",
  '''registros = estaciones.to_dict("records")
region_de = {r["estacion"]: r["region"] for r in registros}
print(len(region_de), "estaciones |", region_de["Nielol"])''',
  '''registros = estaciones.to_dict("records")
# TODO: dict por comprensión {estacion: region} recorriendo registros
region_de = ...
print(region_de)''',
  '''assert isinstance(registros, list) and isinstance(registros[0], dict)
assert len(region_de) == len(estaciones)
assert region_de["Nielol"] == "Región de La Araucanía"''',
  "{r['estacion']: r['region'] for r in registros}."),

 ("## 2. Números que llegan sucios",
  "Las respuestas de las APIs traen números como texto (`\"16.0\"`), vacíos o marcas como "
  "`\"s/d\"` (sin dato). Una función **defensiva** nunca se cae: devuelve `None` cuando no hay "
  "número. Ojo: `float(\"nan\")` NO lanza error — el truco es que `NaN` no es igual a sí mismo.",
  "Escribe `a_numero`",
  '''def a_numero(x):
    try:
        v = float(x)
    except (ValueError, TypeError):
        return None
    if v != v:          # NaN es el único valor distinto de sí mismo
        return None
    return v

print(a_numero("16.0"), a_numero("s/d"), a_numero(None), a_numero(aire["pm25"].iloc[0]))''',
  '''def a_numero(x):
    # TODO: intenta float(x); si lanza ValueError o TypeError, devuelve None
    ...
    # TODO: si el resultado es NaN (v != v), devuelve None; si no, el número

print(a_numero("16.0"), a_numero("s/d"), a_numero(None), a_numero(aire["pm25"].iloc[0]))''',
  '''assert a_numero("16.0") == 16.0
assert a_numero("s/d") is None and a_numero(None) is None
assert a_numero(float("nan")) is None
assert sum(a_numero(x) is None for x in aire["pm25"]) == int(aire["pm25"].isna().sum())''',
  "try: v = float(x) / except (ValueError, TypeError): return None / if v != v: return None / return v."),

 ("## 3. Tu propia respuesta «tipo API»",
  "Empaqueta el resumen de una estación en un mes como un dict listo para `json.dumps`: "
  "solo tipos nativos de Python (`int`, `float`, `str`). Como umbral usamos **50 µg/m³**, el "
  "valor de la norma diaria chilena de PM2,5.",
  "Escribe `resumen_estacion`",
  '''def resumen_estacion(aire, estacion, mes):
    serie = aire[(aire["estacion"] == estacion) & (aire["fecha"].str.startswith(mes))]["pm25"]
    return {
        "estacion": estacion,
        "region": region_de[estacion],
        "mes": mes,
        "dias_con_dato": int(serie.count()),
        "pm25_promedio": round(float(serie.mean()), 1),
        "dias_sobre_50": int((serie > 50).sum()),
    }

r = resumen_estacion(aire, "Las Encinas Temuco", "2024-06")
print(json.dumps(r, ensure_ascii=False, indent=2))''',
  '''def resumen_estacion(aire, estacion, mes):
    serie = aire[(aire["estacion"] == estacion) & (aire["fecha"].str.startswith(mes))]["pm25"]
    return {
        "estacion": estacion,
        "region": region_de[estacion],
        "mes": mes,
        # TODO: días con dato (serie.count(), envuelto en int)
        "dias_con_dato": ...,
        # TODO: promedio de PM2,5 redondeado a 1 decimal (round(float(...), 1))
        "pm25_promedio": ...,
        # TODO: días sobre 50 µg/m³ (envuelto en int)
        "dias_sobre_50": ...,
    }

r = resumen_estacion(aire, "Las Encinas Temuco", "2024-06")
print(r)''',
  '''assert json.loads(json.dumps(r)) == r
assert r["dias_con_dato"] == 30 and isinstance(r["dias_con_dato"], int)
_s = aire[(aire["estacion"] == "Las Encinas Temuco") & (aire["fecha"].str.startswith("2024-06"))]["pm25"]
assert r["pm25_promedio"] == round(float(_s.mean()), 1)
assert r["dias_sobre_50"] == int((_s > 50).sum())''',
  "int(serie.count()), round(float(serie.mean()), 1), int((serie > 50).sum())."),

 ("## 4. Leer un JSON anidado",
  "Las APIs suelen responder con un sobre: metadatos arriba y una **lista de resultados** "
  "adentro. Lee la respuesta y encuentra la estación con el peor promedio de junio 2024.",
  "Encuentra la peor estación en la respuesta",
  '''respuesta = json.dumps({"fuente": "SINCA", "resultados": [
    resumen_estacion(aire, e, "2024-06") for e in ["Las Encinas Temuco", "Nielol", "Cerro Navia"]]})
datos = json.loads(respuesta)
peor = max(datos["resultados"], key=lambda x: x["pm25_promedio"])["estacion"]
print("estación con peor promedio:", peor)''',
  '''respuesta = json.dumps({"fuente": "SINCA", "resultados": [
    resumen_estacion(aire, e, "2024-06") for e in ["Las Encinas Temuco", "Nielol", "Cerro Navia"]]})
# TODO: convierte la respuesta (texto) a dict
datos = ...
# TODO: el nombre de la estación con mayor "pm25_promedio" dentro de datos["resultados"]
peor = ...
print("estación con peor promedio:", peor)''',
  '''assert isinstance(datos, dict) and len(datos["resultados"]) == 3
assert peor == max(datos["resultados"], key=lambda x: x["pm25_promedio"])["estacion"]
assert peor == "Cerro Navia"''',
  'datos = json.loads(respuesta); max(datos["resultados"], key=lambda x: x["pm25_promedio"])["estacion"].'),
]

PROF_HEADER = '''# R3-00 · Onramp express — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional y de **transferencia**: lo mismo de la lección (dicts, funciones, JSON), pero con otro
dato real — la **calidad del aire** diaria (PM2,5) de 14 estaciones del SINCA, 2020-2025. Vas a
convertir una tabla en una **respuesta tipo API** y a leer un JSON anidado.

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


README = '''# R3-00 · Onramp express + Prueba de Nivel

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-00-onramp-express-prueba-nivel/leccion.ipynb)

Puerta de entrada a la rama de IA Aplicada: Python + JSON express sobre las **245 fichas de
trámites de ChileAtiende** (`fichas.csv`), el dato ancla de toda la rama — strings, listas,
diccionarios, funciones, el JSON de una ficha y el patrón **en vivo o caché** — más una
**Prueba de Nivel** que habilita el ingreso directo a R3-01. La profundización transfiere lo
aprendido a la calidad del aire (`aire_diario.csv` + `estaciones.csv`, SINCA).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅). El ejercicio 7 es la PN.
- `profundiza.ipynb` — opcional 🔬: de tabla a respuesta tipo API (JSON) con datos del aire.

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.
'''


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(README)
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
