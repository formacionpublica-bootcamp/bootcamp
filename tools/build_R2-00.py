"""build_R2-00.py — módulo R2-00 (Fundamentos express: Python + pandas).

Rama R2 (Científico de Datos), entrada cero programación condensada. Del cero a
manipular un DataFrame real: cargar, inspeccionar, filtrar, seleccionar, ordenar
y agregar. Rearmado 2026: ancla de la rama = calidad del
aire (PM2.5 diario SINCA, 14 estaciones, 2020–2025). Profundiza = transferencia
con la matrícula escolar 2025 (MINEDUC). Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-00.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-00-fundamentos-express")

RAW = h.REPO_RAW
IMPORTS = "import pandas as pd\nimport matplotlib.pyplot as plt"

INTRO = '''## El dato: el aire que respiramos, día a día

Cada fila de `df` es **un día en una estación de monitoreo** del Sistema de Información
Nacional de Calidad del Aire (SINCA, Ministerio del Medio Ambiente): la concentración
promedio de **material particulado fino (PM2.5)** en µg/m³ y, en algunas estaciones,
la temperatura y la humedad de ese día.

| columna | qué es |
| --- | --- |
| `fecha` | día de la medición (2020-01-01 a 2025-12-30) |
| `estacion` | estación de monitoreo (14, de Alto Hospicio a Temuco) |
| `pm25` | PM2.5 promedio del día, en µg/m³ |
| `temp_media`, `temp_min`, `temp_max` | temperatura del día (°C) — solo en algunas estaciones |
| `humedad_media` | humedad relativa media (%) — solo en algunas estaciones |

> 🏛️ **¿Por qué importa?** La norma chilena de PM2.5 (D.S. 12/2011 del MMA) fija **50 µg/m³**
> como valor para la concentración de 24 horas. Sobre ese valor, el aire empieza a dañar la
> salud — y en invierno, en ciudades como Temuco o Santiago, se superan esos niveles con
> frecuencia. Con pandas vas a poder responder en segundos cuántos días pasó, dónde y cuándo.'''

EJ = [
 ("## 1. Cargar e inspeccionar un DataFrame",
  "Un **DataFrame** es una tabla. Lo primero: conocer su forma y columnas con `shape`, `columns`, `head`.",
  "Inspecciona la tabla",
  '''n_filas, n_cols = df.shape
columnas = list(df.columns)
print("filas:", n_filas, "| columnas:", columnas)''',
  '''# TODO: n_filas, n_cols a partir de df.shape ; columnas = lista de df.columns
n_filas, n_cols = ...
columnas = ...
print("filas:", n_filas, "| columnas:", columnas)''',
  '''assert n_filas == len(df) and n_cols == df.shape[1]
assert "pm25" in columnas and "estacion" in columnas''',
  "df.shape es (filas, columnas); list(df.columns) da los nombres.",
  None),

 ("## 2. Filtrar filas con una condición",
  "Una **máscara booleana** selecciona filas. Quedémonos con los **días sobre el valor de la norma "
  "diaria** de PM2.5: más de 50 µg/m³.",
  "Filtra los días con PM2.5 sobre 50",
  '''sobre_norma = df[df["pm25"] > 50]
n_sobre_norma = len(sobre_norma)
print("días-estación con PM2.5 > 50:", n_sobre_norma)''',
  '''# TODO: filtra df donde pm25 sea mayor que 50
sobre_norma = ...
n_sobre_norma = len(sobre_norma)
print("días-estación con PM2.5 > 50:", n_sobre_norma)''',
  '''assert (sobre_norma["pm25"] > 50).all()
assert n_sobre_norma == int((df["pm25"] > 50).sum())''',
  "df[df['pm25'] > 50].",
  None),

 ("## 3. Seleccionar columnas y ordenar",
  "Elegir columnas y **ordenar** para ver lo más relevante: los 10 peores días de todo el registro.",
  "Top 10 días con más PM2.5",
  '''top = df.sort_values("pm25", ascending=False).head(10)[["fecha", "estacion", "pm25"]]
print(top)''',
  '''# TODO: ordena df por pm25 de mayor a menor, toma head(10) y las columnas ["fecha", "estacion", "pm25"]
top = ...
print(top)''',
  '''assert list(top.columns) == ["fecha", "estacion", "pm25"]
assert len(top) == 10
assert top["pm25"].is_monotonic_decreasing
assert top["pm25"].iloc[0] == df["pm25"].max()''',
  "df.sort_values('pm25', ascending=False).head(10)[['fecha','estacion','pm25']].",
  None),

 ("## 4. Agregar: una pregunta, una respuesta",
  "**`groupby`** resume por grupo. ¿Cuál es el PM2.5 promedio de cada estación?",
  "PM2.5 promedio por estación",
  '''pm25_estacion = df.groupby("estacion")["pm25"].mean()
print(pm25_estacion.round(1).sort_values(ascending=False))''',
  '''# TODO: agrupa por estacion y calcula la media de pm25
pm25_estacion = ...
print(pm25_estacion.round(1).sort_values(ascending=False))''',
  '''assert len(pm25_estacion) == df["estacion"].nunique()
assert abs(pm25_estacion.max() - df.groupby("estacion")["pm25"].mean().max()) < 1e-9''',
  "df.groupby('estacion')['pm25'].mean().",
  '''# (ilustración) PM2.5 promedio por estación, con la referencia de la norma diaria
g = pm25_estacion.sort_values()
plt.figure(figsize=(7, 5))
plt.barh(g.index, g.values, color="#4240e5")
plt.axvline(50, color="#c0392b", ls="--", label="norma diaria: 50 µg/m³")
plt.xlabel("PM2.5 promedio 2020–2025 (µg/m³)"); plt.title("PM2.5 promedio por estación")
plt.legend(); plt.tight_layout(); plt.show()'''),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige)

El promedio de **todas** las estaciones queda muy por debajo de 50 µg/m³ — y sin embargo
encontraste más de mil días-estación sobre ese valor. ¿Qué le dirías a una jefatura que
concluye «el aire está bien, el promedio es bajo»? ¿Qué número le mostrarías en vez del promedio?'''

CIERRE = '''## Cierre

- Un **DataFrame** se inspecciona con `shape`/`columns`/`head` antes de tocarlo.
- **Máscaras booleanas** filtran filas; `sort_values` ordena; selección con `[[...]]`.
- **`groupby`** responde preguntas agregadas en una línea.
- El promedio esconde los episodios: por eso contar días sobre un umbral es tan informativo.

> *En R2-01 vas a cruzar estas mediciones con la tabla de estaciones (región, comuna, coordenadas)
> y a tomar decisiones de limpieza sobre los faltantes reales de meteorología.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-00", "Fundamentos express: Python + pandas", "R2", "Científico de Datos", "1–2",
                      ["Cargar e **inspeccionar** un DataFrame.",
                       "**Filtrar** filas con máscaras booleanas.",
                       "**Seleccionar** columnas y **ordenar**.",
                       "**Agregar** con `groupby`."],
                      "manipular un DataFrame de datos públicos desde cero, en Colab.",
                      "PM2.5 diario de 14 estaciones del SINCA (Ministerio del Medio Ambiente), 2020–2025: 30.674 días-estación.",
                      n_checks=4),
        h.setup_cell("aire_diario.csv", IMPORTS),
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
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/matricula.csv", CSV)
mat = pd.read_csv(CSV)   # matrícula 2025 por establecimiento (MINEDUC)
print("Datos:", mat.shape)
mat.head(3)'''

PROF_EJ = [
 ("## 1. Filtros combinados",
  "Varias condiciones a la vez con `&` (y) / `|` (o), cada una entre paréntesis. ¿Cuántos "
  "establecimientos **rurales** (`rural == 1`) son **municipales**?",
  "Rurales y municipales",
  '''sel = mat[(mat["rural"] == 1) & (mat["dependencia"] == "Municipal")]
print(len(sel), "establecimientos rurales municipales")''',
  '''# TODO: filtra rural == 1 Y dependencia == "Municipal" (cada condición entre paréntesis, unidas con &)
sel = ...
print(len(sel), "establecimientos rurales municipales")''',
  '''assert (sel["rural"] == 1).all()
assert (sel["dependencia"] == "Municipal").all()
assert len(sel) == int(((mat["rural"] == 1) & (mat["dependencia"] == "Municipal")).sum())''',
  "mat[(mat['rural'] == 1) & (mat['dependencia'] == 'Municipal')]."),

 ("## 2. Conteos rápidos con value_counts",
  "`value_counts` cuenta ocurrencias por categoría: ideal para un primer diagnóstico. "
  "¿Cómo se reparten los establecimientos según su dependencia?",
  "Cuenta establecimientos por dependencia",
  '''conteo = mat["dependencia"].value_counts()
print(conteo)''',
  '''# TODO: value_counts sobre la columna dependencia
conteo = ...
print(conteo)''',
  '''assert conteo.sum() == len(mat)
assert set(conteo.index) == set(mat["dependencia"].unique())''',
  "mat['dependencia'].value_counts()."),

 ("## 3. Crear una columna derivada",
  "El feature engineering empieza aquí: una columna nueva calculada desde otras. "
  "Estudiantes por curso = `mat_total / cursos` (un indicador de tamaño de las salas).",
  "Crea `alumnos_por_curso`",
  '''mat2 = mat.copy()
mat2["alumnos_por_curso"] = mat2["mat_total"] / mat2["cursos"]
print(mat2["alumnos_por_curso"].describe().round(1))''',
  '''mat2 = mat.copy()
# TODO: nueva columna alumnos_por_curso = mat_total / cursos
mat2["alumnos_por_curso"] = ...
print(mat2["alumnos_por_curso"].describe().round(1))''',
  '''assert "alumnos_por_curso" in mat2.columns
assert (mat2["alumnos_por_curso"] > 0).all()
assert abs(mat2["alumnos_por_curso"].sum() - (mat["mat_total"] / mat["cursos"]).sum()) < 1e-6''',
  "mat2['mat_total'] / mat2['cursos']."),
]

PROF_HEADER = '''# R2-00 · Fundamentos express — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas herramientas sobre otro dato del Estado — la
**matrícula escolar 2025** por establecimiento (MINEDUC). **Filtros combinados**,
**`value_counts`** y una primera **columna derivada** (preludio del feature engineering de R2-02).

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-00.*"))
    nb.cells = cells
    return nb


README = '''# R2-00 · Fundamentos express: Python + pandas

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-00-fundamentos-express/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Del cero a manipular un DataFrame real: cargar, inspeccionar, filtrar, seleccionar, ordenar y
agregar con `groupby`. El dato es la **calidad del aire**: PM2.5 diario de 14 estaciones del
SINCA (Ministerio del Medio Ambiente), 2020–2025 (`aire_diario.csv`, 30.674 días-estación). Vas
a contar los días sobre el valor de la norma diaria (50 µg/m³), encontrar los peores días y
comparar estaciones. La profundización transfiere lo mismo a la matrícula escolar 2025 del
MINEDUC (`matricula.csv`, 10.945 establecimientos).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: filtros combinados, `value_counts`, columna derivada (matrícula).
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
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
