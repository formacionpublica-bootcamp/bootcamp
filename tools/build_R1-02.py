"""build_R1-02.py — módulo R1-02 (Exploración con pandas).

Rama R1 (Análisis y Visualización). Primer contacto con pandas: inspeccionar,
seleccionar columnas, filtrar filas, contar por categoría y estadísticos rápidos.
Rearmado 2026 (reemplaza al legacy M3): lección sobre matrícula escolar 2025
(MINEDUC); profundiza = transferencia con los establecimientos del Servicio
Médico Legal (`establecimientos.csv`, dataset que se conserva del curso previo).
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-02.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-02-exploracion-con-pandas")

IMPORTS = "import pandas as pd"

EJ = [
 ("## 1. Auditoría visual: ¿qué tengo entre manos?",
  "**pandas** organiza los datos en un **DataFrame**: la planilla Excel en memoria. Antes de "
  "calcular nada, inspecciona: ¿cuántas filas?, ¿qué columnas? `df.shape`, `df.columns` y "
  "`df.head()` son tu primer vistazo a cualquier dataset nuevo.",
  "Inspecciona la tabla",
  '''n_establecimientos = len(df)
columnas = list(df.columns)
print("establecimientos:", n_establecimientos)
print("columnas:", columnas)''',
  '''# TODO: cuántas filas tiene df (len) y la lista de nombres de columna
n_establecimientos = ...
columnas = ...
print("establecimientos:", n_establecimientos)
print("columnas:", columnas)''',
  '''assert n_establecimientos == len(df)
assert "mat_total" in columnas and "region" in columnas''',
  "len(df) y list(df.columns).",
  None),

 ("## 2. Seleccionar columnas: mostrar solo lo que importa",
  'En Excel ocultas columnas para enfocarte; en pandas **seleccionas**: una columna con '
  '`df["col"]`, varias con una lista doble corchete `df[["a", "b"]]`.',
  "Crea una vista con nombre, comuna y matrícula",
  '''vista = df[["nombre", "comuna", "mat_total"]]
print(vista.head())''',
  '''# TODO: selecciona solo las columnas nombre, comuna y mat_total
vista = ...
print(vista.head())''',
  '''assert list(vista.columns) == ["nombre", "comuna", "mat_total"]
assert len(vista) == len(df)''',
  'df[["nombre", "comuna", "mat_total"]] — ojo con el doble corchete.',
  None),

 ("## 3. Filtrar filas: el botón de filtro de Excel",
  'Para quedarte con las filas que cumplen una condición: `df[df["col"] == valor]`. '
  'La expresión interior produce una columna de verdaderos/falsos que selecciona las filas.',
  "Filtra los establecimientos del Maule",
  '''maule = df[df["region"] == "Maule"]
n_maule = len(maule)
print("establecimientos en el Maule:", n_maule)
maule[["nombre", "comuna", "mat_total"]].head()''',
  '''# TODO: filtra las filas cuya region sea "Maule" y cuenta cuántas son
maule = ...
n_maule = ...
print("establecimientos en el Maule:", n_maule)''',
  '''assert n_maule == int((df["region"] == "Maule").sum())
assert set(maule["region"].unique()) == {"Maule"}''',
  'df[df["region"] == "Maule"] y len(...).',
  None),

 ("## 4. Contar por categoría: la tabla dinámica exprés",
  "`value_counts()` cuenta cuántas filas hay de cada categoría, ordenado de mayor a menor. "
  "Es la tabla dinámica más rápida del oeste.",
  "Cuenta establecimientos por dependencia",
  '''por_dependencia = df["dependencia"].value_counts()
n_municipales = int(por_dependencia["Municipal"])
print(por_dependencia)''',
  '''# TODO: conteo por dependencia con value_counts, y extrae el valor de "Municipal"
por_dependencia = ...
n_municipales = ...
print(por_dependencia)''',
  '''assert por_dependencia.sum() == len(df)
assert n_municipales == int((df["dependencia"] == "Municipal").sum())''',
  'df["dependencia"].value_counts() y luego por_dependencia["Municipal"].',
  None),

 ("## 5. Estadísticos rápidos: el pie de página de Excel",
  "Sobre una columna numérica: `.mean()`, `.max()`, `.min()`. Y `.idxmax()` te dice **qué fila** "
  "tiene el máximo — con `.loc` recuperas su nombre.",
  "Estadísticos de la matrícula",
  '''promedio = df["mat_total"].mean()
maximo = int(df["mat_total"].max())
mas_grande = df.loc[df["mat_total"].idxmax(), "nombre"]
print("promedio:", round(promedio, 1), "| máximo:", maximo, "|", mas_grande)''',
  '''# TODO: promedio y máximo de mat_total, y el nombre del establecimiento más grande
promedio = ...
maximo = ...
mas_grande = df.loc[df["mat_total"].idxmax(), "nombre"]
print("promedio:", round(promedio, 1), "| máximo:", maximo, "|", mas_grande)''',
  '''assert abs(promedio - df["mat_total"].mean()) < 1e-6
assert maximo == int(df["mat_total"].max())''',
  'df["mat_total"].mean() y int(df["mat_total"].max()).',
  None),
]

CIERRE = '''## Errores típicos al empezar

- `KeyError`: seleccionaste una columna que no existe. Revisa mayúsculas, tildes y espacios — `df.columns` es tu amigo.
- `SyntaxError` en filtros: el doble corchete `df[[...]]` es para listas de columnas; el filtro lleva la condición adentro: `df[df["col"] == valor]`.
- Confundir `df["col"]` (una columna, tipo Serie) con `df[["col"]]` (una tabla de una columna).

## Cierre

- **Inspecciona** antes de calcular: `shape`, `columns`, `head`.
- **Selecciona** columnas, **filtra** filas, **cuenta** con `value_counts`, **resume** con `mean/max/min`.
- Con estas cinco operaciones ya puedes explorar cualquier dataset del Estado.

> *En R1-03 aprenderás el superpoder de pandas: cruzar dos tablas (el BUSCARV profesional).*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-02", "Exploración con pandas", "R1", "Analista de Datos", "3",
                      ["**Inspeccionar** un DataFrame: filas, columnas, primeros registros.",
                       "**Seleccionar** columnas y **filtrar** filas.",
                       "**Contar por categoría** con value_counts.",
                       "Calcular **estadísticos rápidos** de una columna."],
                      "explorar cualquier dataset público con pandas, como una planilla con superpoderes.",
                      "matrícula oficial 2025 de los 10.945 establecimientos educacionales de Chile (MINEDUC).",
                      n_checks=5),
        h.setup_cell("matricula.csv", IMPORTS),
        h.md("### Datos cargados arriba. Cada fila es un establecimiento educacional de Chile."),
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


PROF_PREP = '''import pandas as pd, os, urllib.request
CSV = "establecimientos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/establecimientos.csv", CSV)
sml = pd.read_csv(CSV)
print("Establecimientos del Servicio Médico Legal:", sml.shape)'''

PROF_EJ = [
 ("## 1. Transferencia: otro dataset, mismas herramientas",
  "Ahora los datos son los **establecimientos del Servicio Médico Legal** a lo largo de Chile "
  "(datos.gob.cl). Mismas cinco operaciones, dominio nuevo: si puedes explorar esto sin ayuda, "
  "la técnica ya es tuya.",
  "Cuenta los SML por región",
  '''por_region = sml["region"].value_counts()
n_maule = int(por_region["Maule"])
print(por_region.head())
print("SML en el Maule:", n_maule)''',
  '''# TODO: conteo de SML por región y cuántos hay en el "Maule"
por_region = ...
n_maule = ...
print("SML en el Maule:", n_maule)''',
  '''assert por_region.sum() == len(sml)
assert n_maule == int((sml["region"] == "Maule").sum())''',
  'sml["region"].value_counts() y por_region["Maule"].'),

 ("## 2. Estadísticos de una columna: la geografía del país",
  "La latitud dice dónde está cada establecimiento: máxima = más al norte, mínima = más al sur.",
  "Estadísticos de la latitud",
  '''lat_promedio = sml["latitud"].mean()
lat_norte = sml["latitud"].max()
lat_sur = sml["latitud"].min()
print("promedio:", round(lat_promedio, 2), "| más al norte:", lat_norte, "| más al sur:", lat_sur)''',
  '''# TODO: promedio, máximo (más al norte) y mínimo (más al sur) de la latitud
lat_promedio = ...
lat_norte = ...
lat_sur = ...
print("promedio:", round(lat_promedio, 2), "| más al norte:", lat_norte, "| más al sur:", lat_sur)''',
  '''assert abs(lat_promedio - sml["latitud"].mean()) < 1e-6
assert lat_norte == sml["latitud"].max()
assert lat_sur == sml["latitud"].min()''',
  '.mean(), .max() y .min() sobre sml["latitud"].'),

 ("## 3. Una función de consulta reutilizable",
  "Empaqueta el filtro en una función: recibe la región y devuelve cuántos establecimientos hay.",
  "Escribe `cuantos_en`",
  '''def cuantos_en(d, region):
    return len(d[d["region"] == region])

print("Maule:", cuantos_en(sml, "Maule"), "| Metropolitana:", cuantos_en(sml, "Metropolitana"))''',
  '''def cuantos_en(d, region):
    # TODO: filtra d por la región indicada y devuelve la cantidad de filas
    ...

print("Maule:", cuantos_en(sml, "Maule"), "| Metropolitana:", cuantos_en(sml, "Metropolitana"))''',
  '''assert cuantos_en(sml, "Maule") == int((sml["region"] == "Maule").sum())
assert cuantos_en(sml, "Metropolitana") == int((sml["region"] == "Metropolitana").sum())''',
  'return len(d[d["region"] == region]).'),
]

PROF_HEADER = '''# R1-02 · Exploración con pandas — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas cinco operaciones de la lección, ahora sobre los
**establecimientos del Servicio Médico Legal** (datos.gob.cl). `value_counts`, estadísticos
y una función de consulta reutilizable.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-02.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-02 · Exploración con pandas

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-02-exploracion-con-pandas/leccion.ipynb)

Primer contacto con pandas: inspeccionar, seleccionar, filtrar, contar por categoría y
estadísticos rápidos, sobre la matrícula escolar oficial 2025 (`matricula.csv`, MINEDUC).
La profundización transfiere las mismas operaciones a los establecimientos del Servicio
Médico Legal (`establecimientos.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: transferencia con los SML de Chile.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
