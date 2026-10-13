"""build_R1-03.py — módulo R1-03 (Cruzar y resumir tablas).

Rama R1 (Análisis y Visualización). El superpoder de pandas: merge (llave, inner
vs left, la fila huérfana) y groupby para responder la pregunta real. Rearmado
2026 (reemplaza al legacy M3B de órdenes/organismos): cruza los conteos de
matrícula por RBD con el directorio oficial de establecimientos — con 4 filas
huérfanas REALES (RBD con matrícula pero sin estado «funcionando»). Profundiza =
transferencia: matrícula por comuna × población comunal. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-03-cruzar-y-resumir-tablas")

RAW = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data"

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["matricula_rbd.csv", "directorio_establecimientos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

df_matricula = pd.read_csv("matricula_rbd.csv")          # conteos de estudiantes por RBD
df_directorio = pd.read_csv("directorio_establecimientos.csv")  # quién es cada RBD
print("matrícula:", df_matricula.shape, "| directorio:", df_directorio.shape)
df_matricula.head(3)'''

INTRO = '''## ¿Por qué dos tablas? La llave que las une

El MINEDUC no guarda el nombre, la comuna y la dependencia del establecimiento **en cada
registro de matrícula**: eso duplicaría la misma información miles de veces. En su lugar,
cada establecimiento tiene un código único — el **RBD** (Rol Base de Datos) — y hay dos tablas:

- `df_matricula`: **cuántos** estudiantes tiene cada RBD (la medida).
- `df_directorio`: **quién es** cada RBD — nombre, dependencia, región, comuna (el catálogo).

Para responder «¿qué región tiene más estudiantes?» necesitas las dos. El **cruce** (`merge`)
es el BUSCARV profesional: le pega a cada fila de matrícula los atributos de su establecimiento.

> Dato real: las dos tablas NO calzan perfecto — hay 4 RBD que reportan matrícula pero no
> figuran «funcionando» en el directorio oficial. Los vas a cazar en el ejercicio 3.'''

EJ = [
 ("## 1. Encontrar la llave",
  "Antes de cruzar hay que identificar la **llave**: la columna que existe en ambas tablas "
  "y significa lo mismo. Mira `df_matricula.columns` y `df_directorio.columns`.",
  "Identifica la llave y el tamaño de cada tabla",
  '''llave = "rbd"
n_matricula = len(df_matricula)
n_directorio = len(df_directorio)
print("llave:", llave, "| matrícula:", n_matricula, "| directorio:", n_directorio)''',
  '''# TODO: nombre de la columna que está en AMBAS tablas (entre comillas)
llave = ...
# TODO: filas de cada tabla
n_matricula = ...
n_directorio = ...
print("llave:", llave, "| matrícula:", n_matricula, "| directorio:", n_directorio)''',
  '''assert llave in df_matricula.columns and llave in df_directorio.columns
assert n_matricula == len(df_matricula)
assert n_directorio == len(df_directorio)''',
  "Compara las listas de columnas: la común es 'rbd'. len(...) para los tamaños.",
  None),

 ("## 2. El primer cruce: `pd.merge`",
  "`pd.merge(izquierda, derecha, on=llave)` pega las columnas de la derecha a cada fila de la "
  "izquierda cuando la llave coincide. Cruza matrícula con directorio.",
  "Cruza las dos tablas",
  '''df_cruce = pd.merge(df_matricula, df_directorio, on="rbd")
n_cruce = len(df_cruce)
print("filas del cruce:", n_cruce, "| columnas:", list(df_cruce.columns))''',
  '''# TODO: cruza df_matricula con df_directorio por la llave "rbd"
df_cruce = ...
n_cruce = ...
print("filas del cruce:", n_cruce)''',
  '''assert "region" in df_cruce.columns and "mat_total" in df_cruce.columns
assert n_cruce == len(pd.merge(df_matricula, df_directorio, on="rbd"))''',
  'pd.merge(df_matricula, df_directorio, on="rbd") y len(...).',
  None),

 ("## 3. Inner vs left: cazar la fila huérfana",
  'El cruce anterior (inner, el modo por defecto) **botó** los RBD que no están en el '
  'directorio. Con `how="left"` conservas TODAS las filas de matrícula; las que no '
  'encontraron pareja quedan con la región **nula** — y las puedes contar.',
  "Encuentra los establecimientos huérfanos",
  '''df_left = pd.merge(df_matricula, df_directorio, on="rbd", how="left")
n_huerfanas = int(df_left["region"].isna().sum())
print("filas totales:", len(df_left), "| huérfanas (sin directorio):", n_huerfanas)
df_left[df_left["region"].isna()]''',
  '''# TODO: cruce que conserva TODAS las filas de matrícula (how="left")
df_left = ...
# TODO: cuántas quedaron sin datos de directorio (region nula)
n_huerfanas = ...
print("filas totales:", len(df_left), "| huérfanas (sin directorio):", n_huerfanas)''',
  '''assert len(df_left) == len(df_matricula)
assert n_huerfanas == int(df_left["region"].isna().sum())
assert n_huerfanas > 0''',
  'pd.merge(..., how="left") y df_left["region"].isna().sum().',
  None),

 ("## 4. La pregunta real: ¿qué región concentra los estudiantes?",
  "Cruzar es el medio; el fin es **responder algo**. Ahora que cada conteo tiene su región, "
  "`groupby` responde la pregunta de gestión.",
  "Estudiantes por región y la región líder",
  '''est_por_region = df_cruce.groupby("region")["mat_total"].sum().sort_values(ascending=False)
region_top = est_por_region.idxmax()
print(est_por_region.head())
print("región con más estudiantes:", region_top)''',
  '''# TODO: estudiantes (mat_total) por región, de mayor a menor
est_por_region = ...
# TODO: nombre de la región con más estudiantes
region_top = ...
print("región con más estudiantes:", region_top)''',
  '''assert len(est_por_region) == df_cruce["region"].nunique()
assert region_top == est_por_region.idxmax()''',
  'groupby("region")["mat_total"].sum().sort_values(ascending=False); el líder es .idxmax().',
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Los 4 RBD huérfanos que cazaste en el ejercicio 3 reportan estudiantes pero no figuran
«funcionando» en el registro oficial. En una o dos frases: ¿qué harías con esas filas en un
informe — las botas, las incluyes, las reportas aparte? ¿A quién le preguntarías por qué existen?

> Esa pregunta — qué hacer con los datos que no calzan — es el trabajo real del analista.'''

CIERRE = '''## Errores típicos al cruzar

- **`KeyError` en la llave** → no se llama igual en ambas tablas; usa `left_on=`/`right_on=` si difieren.
- **El cruce tiene MÁS filas que las tablas** → la llave está repetida en alguna tabla (relación 1-a-muchos).
- **Todo quedó nulo** → cruzaste por la columna equivocada o los tipos difieren (texto vs número).

## Cierre

- La **llave** conecta la medida con el catálogo; el **RBD** es la cédula de identidad de cada escuela.
- `inner` bota lo que no calza; `left` lo conserva como **nulo** — y contarlos es auditar.
- El cruce es el medio: la pregunta de gestión se responde con **groupby** después de cruzar.

> *En R1-04 aprenderás a limpiar datos sucios — porque las llaves que no calzan y los valores
> imposibles son el pan de cada día.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-03", "Cruzar y resumir tablas", "R1", "Analista de Datos", "4",
                      ["Identificar la **llave** que une dos tablas.",
                       "Cruzar con **pd.merge** y entender qué produce.",
                       "Distinguir **inner vs left** y cazar filas huérfanas.",
                       "Responder la pregunta real con **groupby** tras el cruce."],
                      "cruzar tablas del Estado con criterio: el BUSCARV profesional, con auditoría de lo que no calza.",
                      "matrícula 2025 por RBD × directorio oficial de establecimientos (MINEDUC) — con 4 huérfanas reales.",
                      n_checks=4),
        h.code(SETUP),
        h.md(INTRO),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


PROF_PREP = f'''import pandas as pd, os, urllib.request
for archivo in ["matricula.csv", "comunas.csv", "parques.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)
mat = pd.read_csv("matricula.csv")
comunas = pd.read_csv("comunas.csv")     # población de las 30 comunas más grandes
parques = pd.read_csv("parques.csv")     # parques nacionales de Chile
print("matrícula:", mat.shape, "| comunas:", comunas.shape, "| parques:", parques.shape)'''

PROF_EJ = [
 ("## 1. Transferencia: matrícula × población comunal",
  "Cruza los estudiantes por comuna con la **población** de las 30 comunas más grandes "
  "(dos fuentes distintas unidas por el nombre de la comuna).",
  "Construye la tabla comunal cruzada",
  '''est_comuna = mat.groupby("comuna")["mat_total"].sum().reset_index()
cruce = pd.merge(est_comuna, comunas, on="comuna")
print("comunas cruzadas:", len(cruce))
print(cruce.head(3))''',
  '''est_comuna = mat.groupby("comuna")["mat_total"].sum().reset_index()
# TODO: cruza est_comuna con comunas por la columna "comuna"
cruce = ...
print("comunas cruzadas:", len(cruce))''',
  '''assert "poblacion" in cruce.columns and "mat_total" in cruce.columns
assert len(cruce) <= len(comunas)''',
  'pd.merge(est_comuna, comunas, on="comuna").'),

 ("## 2. El indicador que ninguna tabla tiene sola",
  "Estudiantes por cada 1.000 habitantes: solo existe DESPUÉS del cruce. ¿Qué comuna es la "
  "más «escolar» en proporción a su gente?",
  "Calcula la tasa y encuentra la comuna líder",
  '''cruce["tasa"] = 1000 * cruce["mat_total"] / cruce["poblacion"]
comuna_top = cruce.loc[cruce["tasa"].idxmax(), "comuna"]
print(cruce.sort_values("tasa", ascending=False).head(3)[["comuna", "tasa"]])
print("líder:", comuna_top)''',
  '''# TODO: tasa = 1000 * estudiantes / población, y la comuna con mayor tasa
cruce["tasa"] = ...
comuna_top = ...
print("líder:", comuna_top)''',
  '''assert cruce["tasa"].max() > 0
assert comuna_top == cruce.loc[cruce["tasa"].idxmax(), "comuna"]''',
  '1000 * cruce["mat_total"] / cruce["poblacion"]; el líder con idxmax + loc.'),

 ("## 3. Resumir sin cruzar: los parques por región",
  "El groupby también responde solo. ¿Qué región concentra más superficie de parques nacionales?",
  "Superficie de parques por región",
  '''sup_region = parques.groupby("region")["superficie_ha"].sum().sort_values(ascending=False)
print(sup_region.head())''',
  '''# TODO: superficie total (superficie_ha) por región, de mayor a menor
sup_region = ...
print(sup_region.head())''',
  '''assert len(sup_region) == parques["region"].nunique()
assert list(sup_region.values) == sorted(sup_region.values, reverse=True)''',
  'parques.groupby("region")["superficie_ha"].sum().sort_values(ascending=False).'),
]

PROF_HEADER = '''# R1-03 · Cruzar y resumir — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: cruza la matrícula por comuna con la **población comunal**
para construir un indicador que ninguna tabla tiene sola (estudiantes por 1.000 habitantes),
y resume los **parques nacionales** por región.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-03.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-03 · Cruzar y resumir tablas

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-03-cruzar-y-resumir-tablas/leccion.ipynb)

El superpoder de pandas: **merge** (llave, inner vs left, filas huérfanas) y **groupby** para
la pregunta real. Cruza la matrícula 2025 por RBD (`matricula_rbd.csv`) con el directorio
oficial (`directorio_establecimientos.csv`) — con 4 huérfanas reales que cazar. La
profundización cruza matrícula comunal con población (`comunas.csv`) y resume `parques.csv`.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: estudiantes por 1.000 habitantes, parques por región.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
