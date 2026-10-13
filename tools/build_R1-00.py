"""build_R1-00.py — módulo R1-00 (Fundamentos: Python con datos reales).

Rama R1 (Análisis y Visualización), entrada cero programación: variables, listas,
comprensiones, diccionarios y bucles. Rearmado 2026: dataset ancla = matrícula
escolar oficial 2025 por establecimiento (MINEDUC, data/rearmado/matricula.csv).
Convención de la casa (ver tools/build_R2-07.py).

Uso:  /opt/anaconda3/bin/python tools/build_R1-00.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-00-fundamentos")

IMPORTS = "import pandas as pd\nimport matplotlib.pyplot as plt"

EJ = [
 ("## 1. Variables: guardar para reutilizar",
  "Una **variable** guarda un valor con nombre. Cada fila del dataset es un establecimiento "
  "educacional de Chile con su matrícula 2025. Tomemos la matrícula total de cada uno como "
  "una lista y calculemos cuántos estudiantes hay en total y el promedio por establecimiento, "
  "sin pandas.",
  "Total de estudiantes y promedio por establecimiento",
  '''matriculas = df["mat_total"].tolist()
total = sum(matriculas)
promedio = total / len(matriculas)
print("estudiantes en Chile:", total, "| promedio por establecimiento:", round(promedio))''',
  '''matriculas = df["mat_total"].tolist()
# TODO: total = suma de matriculas ; promedio = total / cantidad de establecimientos
total = ...
promedio = ...
print("estudiantes en Chile:", total, "| promedio por establecimiento:", round(promedio))''',
  '''assert total == int(df["mat_total"].sum())
assert abs(promedio - df["mat_total"].mean()) < 1e-6''',
  "sum(matriculas) y total / len(matriculas).",
  None),

 ("## 2. Listas y comprensiones: filtrar",
  "Una **comprensión de lista** filtra en una línea. Contemos los establecimientos grandes.",
  "Cuenta los establecimientos con más de 1.000 estudiantes",
  '''grandes = [m for m in matriculas if m > 1_000]
n_grandes = len(grandes)
print("establecimientos con más de 1.000 estudiantes:", n_grandes)''',
  '''# TODO: lista de matrículas mayores a 1.000 y su cantidad
grandes = ...
n_grandes = ...
print("establecimientos con más de 1.000 estudiantes:", n_grandes)''',
  '''assert n_grandes == int((df["mat_total"] > 1_000).sum())''',
  "[m for m in matriculas if m > 1_000] y luego len(...).",
  None),

 ("## 3. Diccionarios y bucles: acumular por clave",
  "Un **diccionario** asocia clave→valor. Con un **bucle** sumamos los estudiantes por región.",
  "Estudiantes por región con un bucle",
  '''est_region = {}
for region, m in zip(df["region"], df["mat_total"]):
    est_region[region] = est_region.get(region, 0) + m
print(len(est_region), "regiones")''',
  '''est_region = {}
for region, m in zip(df["region"], df["mat_total"]):
    # TODO: súmale 'm' al acumulado de 'region' (usa .get(region, 0))
    ...
print(len(est_region), "regiones")''',
  '''assert len(est_region) == df["region"].nunique()
assert sum(est_region.values()) == int(df["mat_total"].sum())''',
  "est_region[region] = est_region.get(region, 0) + m.",
  None),

 ("## 4. Condicionales: clasificar en tramos",
  "Con **if/elif/else** dentro de un bucle clasificamos cada establecimiento por tamaño.",
  "Cuenta los establecimientos por tramo de tamaño",
  '''tramos = {"chico": 0, "medio": 0, "grande": 0}
for m in matriculas:
    if m < 100:
        tramos["chico"] += 1
    elif m < 500:
        tramos["medio"] += 1
    else:
        tramos["grande"] += 1
print(tramos)''',
  '''tramos = {"chico": 0, "medio": 0, "grande": 0}
for m in matriculas:
    # TODO: chico si < 100 estudiantes; medio si < 500; grande en otro caso
    ...
print(tramos)''',
  '''assert sum(tramos.values()) == len(matriculas)
assert tramos["chico"] == int((df["mat_total"] < 100).sum())''',
  "if m < 100 / elif m < 500 / else, sumando 1 al tramo correspondiente.",
  '''# (ilustración) Establecimientos por tramo de tamaño
plt.figure(figsize=(5, 4))
plt.bar(tramos.keys(), tramos.values(), color="#4240e5")
plt.ylabel("Nº de establecimientos"); plt.title("Establecimientos por tamaño")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- **Variables, listas, diccionarios y bucles** son el alfabeto de Python; con ellos ya resumes datos reales.
- Las **comprensiones** filtran y transforman en una línea.
- En el próximo módulo (R1-01) traeremos datos desde archivos y APIs.

> *Python just-in-time: aprendiste la sintaxis respondiendo preguntas sobre la matrícula escolar de Chile, no en abstracto.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-00", "Fundamentos: Python con datos reales", "R1", "Analista de Datos", "1",
                      ["Usar **variables** y operaciones básicas sobre datos reales.",
                       "Filtrar con **listas y comprensiones**.",
                       "Acumular con **diccionarios** y **bucles**.",
                       "Clasificar con **condicionales**."],
                      "manipular datos públicos con Python puro, desde cero, en Colab.",
                      "matrícula oficial 2025 de los 10.945 establecimientos educacionales de Chile (MINEDUC).",
                      n_checks=4),
        h.setup_cell("matricula.csv", IMPORTS),
        h.md("### Datos cargados arriba. Empecemos por lo básico de Python."),
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
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/matricula.csv", CSV)
df = pd.read_csv(CSV)
matriculas = df["mat_total"].tolist()
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Diccionario por comprensión",
  "Agrupar en una línea: estudiantes por dependencia con un dict comprehension.",
  "Estudiantes por dependencia",
  '''deps = df["dependencia"].unique()
est_dep = {d: df[df["dependencia"] == d]["mat_total"].sum() for d in deps}
print(len(est_dep), "dependencias")''',
  '''deps = df["dependencia"].unique()
# TODO: {dependencia: suma de mat_total de esa dependencia}
est_dep = ...
print(len(est_dep), "dependencias")''',
  '''assert len(est_dep) == df["dependencia"].nunique()
assert sum(est_dep.values()) == int(df["mat_total"].sum())''',
  "{d: df[df['dependencia']==d]['mat_total'].sum() for d in deps}."),

 ("## 2. Funciones: empaquetar un resumen",
  "Una función reutilizable que resume cualquier lista de matrículas.",
  "Escribe `resumen`",
  '''def resumen(lista):
    return {"n": len(lista), "total": sum(lista), "max": max(lista)}

print(resumen(matriculas))''',
  '''def resumen(lista):
    # TODO: dict con n (cantidad), total (suma) y max (máximo)
    ...

print(resumen(matriculas))''',
  '''r = resumen(matriculas)
assert r["n"] == len(matriculas)
assert r["max"] == max(matriculas)''',
  "Devuelve {'n': len(lista), 'total': sum(lista), 'max': max(lista)}."),

 ("## 3. El máximo con una clave",
  "Encontrar la comuna con más estudiantes: `max` con `key`.",
  "Comuna con más estudiantes",
  '''est_comuna = {}
for com, m in zip(df["comuna"], df["mat_total"]):
    est_comuna[com] = est_comuna.get(com, 0) + m
top_comuna = max(est_comuna, key=est_comuna.get)
print("Top:", top_comuna)''',
  '''est_comuna = {}
for com, m in zip(df["comuna"], df["mat_total"]):
    est_comuna[com] = est_comuna.get(com, 0) + m
# TODO: la comuna con más estudiantes (max con key=est_comuna.get)
top_comuna = ...
print("Top:", top_comuna)''',
  '''assert top_comuna == max(est_comuna, key=est_comuna.get)''',
  "max(est_comuna, key=est_comuna.get) devuelve la clave de mayor valor."),
]

PROF_HEADER = '''# R1-00 · Fundamentos — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional. Más Python con datos reales: **dict por comprensión**, **funciones** y `max` con **clave**.
Mismos datos de matrícula escolar.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-00.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-00 · Fundamentos: Python con datos reales

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-00-fundamentos/leccion.ipynb)

Entrada cero programación: variables, listas, comprensiones, diccionarios y bucles sobre la
matrícula escolar oficial 2025 de Chile (`matricula.csv`, MINEDUC — 10.945 establecimientos).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: dict por comprensión, funciones, max con clave.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
