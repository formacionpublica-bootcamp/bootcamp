"""build_R1-CAP.py — Capstone de la rama R1 (Análisis y Visualización).

Proyecto-plantilla (no lección suelta): recorre el ciclo cargar→limpiar→analizar→
visualizar→comunicar, termina en una figura honesta + brief de una plana, con
rúbrica. Rearmado 2026: la plantilla usa matricula.csv (MINEDUC) como ejemplo y
ofrece un banco de datasets curados; lo ideal es que el estudiante use datos de
su propio organismo. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-CAP.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-CAP-capstone-analisis")

IMPORTS = "import pandas as pd\nimport matplotlib.pyplot as plt"

ENMARCA = '''## 1. Enmarca el problema

Antes de tocar el dato, escribe en una frase la **pregunta de gestión** que vas a responder.
Ejemplo guía (matrícula escolar): *¿dónde se concentran los establecimientos rurales chicos,
y qué decisión de apoyo habilita ese hallazgo?*

**Elige tu dataset** (en este orden de preferencia):

1. **Datos de tu propio organismo** — el capstone vale el doble si responde una pregunta real
   de tu servicio.
2. El **banco del bootcamp** (todos reales y ya curados, en `data/` del repositorio):
   `matricula.csv` (matrícula escolar 2025, MINEDUC) · `aire_diario.csv` (PM2.5 diario por
   estación, SINCA) · `sismos.csv` (catálogo USGS 2020–2025) · `fichas.csv` (trámites de
   ChileAtiende) · `reclamos.csv` (reclamos de consumo, SERNAC).
3. Cualquier dataset de **datos.gob.cl** (ya sabes usar su API, R1-01).

> Esta plantilla usa `matricula.csv` como ejemplo; reemplázalo por el tuyo.'''

EJ = [
 ("## 2. Carga y limpia",
  "Construye tu base de trabajo limpia: sin nulos ni duplicados en lo esencial.",
  "Limpia el DataFrame",
  '''df_limpio = df.dropna().drop_duplicates().copy()
n_nulos = int(df_limpio.isna().sum().sum())
print("filas:", len(df_limpio), "| nulos:", n_nulos)''',
  '''# TODO: elimina nulos y duplicados, guarda en df_limpio
df_limpio = ...
n_nulos = int(df_limpio.isna().sum().sum())
print("filas:", len(df_limpio), "| nulos:", n_nulos)''',
  '''assert n_nulos == 0
assert len(df_limpio) <= len(df)''',
  "df.dropna().drop_duplicates().copy().",
  None),

 ("## 3. Analiza",
  "Resume el dato para responder tu pregunta. Una función reutilizable que agrega por una dimensión.",
  "Escribe `resumen_matricula`",
  '''def resumen_matricula(d, por="region"):
    return (d.groupby(por)["mat_total"]
              .agg(["sum", "mean", "count"])
              .sort_values("sum", ascending=False))

tabla = resumen_matricula(df_limpio)
print(tabla.head(3))''',
  '''def resumen_matricula(d, por="region"):
    # TODO: agrupa por 'por' y agrega mat_total con sum, mean y count; ordena por sum desc
    return ...

tabla = resumen_matricula(df_limpio)
print(tabla.head(3))''',
  '''assert "sum" in tabla.columns
assert len(tabla) == df_limpio["region"].nunique()''',
  "d.groupby(por)['mat_total'].agg(['sum','mean','count']).sort_values('sum', ascending=False).",
  None),

 ("## 4. Visualiza (honesto)",
  "Una figura clara y honesta del hallazgo: eje desde 0, título y etiquetas.",
  "Grafica el top 6",
  '''top = tabla.head(6)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(top.index, top["sum"], color="#4240e5")
ax.set_ylim(bottom=0)
ax.set_title("Matrícula por región, 2025 (top 6)"); ax.set_xlabel("Región"); ax.set_ylabel("Estudiantes matriculados")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''top = tabla.head(6)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(top.index, top["sum"], color="#4240e5")
# TODO: eje desde 0, título y etiquetas de ejes
...
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert ax.get_ylim()[0] == 0''',
  "ax.set_ylim(bottom=0); ax.set_title(...); ax.set_xlabel(...); ax.set_ylabel(...).",
  None),
]

COMUNICA = '''## 5. Comunica — brief de una plana

Completa este **brief** (lo que leería quien decide). Es tu entregable principal junto al notebook.

> **Pregunta:** _(la que enmarcaste en el paso 1)_
>
> **Hallazgo (1-2 frases):** _(qué muestran los datos, con el número clave)_
>
> **Recomendación accionable:** _(qué debería hacer el organismo con esto)_
>
> **Límites y ética:** _(qué NO dice este dato; sesgos o cautelas. Ejemplo con matrícula:
> el dato es de abril de 2025 y no captura el movimiento durante el año; «matrícula» no es
> «asistencia».)_'''

RUBRICA = '''## Rúbrica de evaluación

| Criterio | Qué se evalúa |
|---|---|
| **Correctitud del dato** | La limpieza y las agregaciones son correctas y reproducibles. |
| **Claridad visual** | La figura se entiende sola: título, etiquetas, foco en el mensaje. |
| **Honestidad / ética** | Eje desde 0, sin engaños; se declaran límites del dato. |
| **Reproducibilidad** | El notebook corre de principio a fin sin pasos manuales. |
| **Comunicación** | El brief de una plana es claro y accionable. |
| **Pertinencia** | (Bonus) El dataset es del propio organismo o responde una pregunta real de gestión. |

> **Entregable:** notebook reproducible + figura honesta + brief de una plana.'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-CAP", "Capstone — análisis sobre datos de tu organismo", "R1", "Analista de Datos", "11–12",
                      ["Recorrer el ciclo completo: **cargar → limpiar → analizar → visualizar → comunicar**.",
                       "Producir una **figura honesta** y un **brief de una plana**.",
                       "Trabajar sobre **datos de tu propio organismo** (o del banco del bootcamp).",
                       "Entregar un notebook **reproducible**."],
                      "ejecutar un análisis de datos público de punta a punta y comunicarlo con integridad.",
                      "matrícula escolar 2025 (ejemplo) o el dataset de tu organismo.",
                      n_checks=3),
        h.setup_cell("matricula.csv", IMPORTS),
        h.md(ENMARCA),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(COMUNICA))
    cells.append(h.md(RUBRICA))
    nb.cells = cells
    return nb


PROF_PREP = '''import pandas as pd, os, urllib.request
import matplotlib.pyplot as plt
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/matricula.csv", CSV)
df = pd.read_csv(CSV).dropna().drop_duplicates()
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Segunda dimensión de análisis",
  "Un hallazgo robusto se ve desde más de un ángulo. Resume también por dependencia.",
  "Matrícula por dependencia",
  '''por_dependencia = df.groupby("dependencia")["mat_total"].sum().sort_values(ascending=False)
print(por_dependencia.head(3))''',
  '''# TODO: matrícula total por dependencia, ordenada desc
por_dependencia = ...
print(por_dependencia.head(3))''',
  '''assert len(por_dependencia) == df["dependencia"].nunique()''',
  "df.groupby('dependencia')['mat_total'].sum().sort_values(ascending=False)."),

 ("## 2. Exporta la figura para el brief",
  "Guarda la figura como PNG para pegarla en tu informe.",
  "Guarda la figura",
  '''top = df.groupby("region")["mat_total"].sum().sort_values(ascending=False).head(6)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(top.index, top.values, color="#4240e5"); ax.set_ylim(bottom=0)
fig.savefig("figura_matricula_region.png", dpi=120, bbox_inches="tight")
existe = os.path.exists("figura_matricula_region.png")
print("guardada:", existe)''',
  '''top = df.groupby("region")["mat_total"].sum().sort_values(ascending=False).head(6)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(top.index, top.values, color="#4240e5"); ax.set_ylim(bottom=0)
# TODO: guarda la figura como "figura_matricula_region.png"
...
existe = os.path.exists("figura_matricula_region.png")
print("guardada:", existe)''',
  '''assert existe''',
  "fig.savefig('figura_matricula_region.png', dpi=120, bbox_inches='tight')."),
]

PROF_HEADER = '''# R1-CAP · Capstone — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional. Refuerza tu capstone: una **segunda dimensión** de análisis y **exportar** la figura para
pegarla en el brief. Mismos datos de matrícula escolar.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización del capstone R1.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-CAP · Capstone — análisis sobre datos de tu organismo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-CAP-capstone-analisis/leccion.ipynb)

Proyecto final de la rama R1: recorre cargar→limpiar→analizar→visualizar→comunicar, terminando
en una figura honesta + un brief de una plana. La plantilla usa la matrícula escolar 2025
(`matricula.csv`) como ejemplo; lo ideal es usar **datos de tu propio organismo** o el banco
del bootcamp (`matricula`, `aire_diario`, `sismos`, `fichas`, `reclamos`).

- `leccion.ipynb` — plantilla con `TODO`; el notebook se autoverifica (✅).
- Incluye **rúbrica** de evaluación. `profundiza.ipynb` — opcional 🔬.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
