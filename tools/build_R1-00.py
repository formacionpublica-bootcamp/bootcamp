"""build_R1-00.py — módulo R1-00 (Fundamentos: Python con datos reales).

Rama R1 (Análisis y Visualización), entrada cero programación. Condensa P1+P2:
variables, listas, comprensiones, diccionarios y bucles, sobre montos reales de
compras públicas. Convención de la casa (ver tools/build_R2-07.py).

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
  "Una **variable** guarda un valor con nombre. Tomemos los montos de compras reales como una lista "
  "y calculemos el total y el promedio sin pandas.",
  "Total y promedio de los montos",
  '''montos = df["monto_total"].tolist()
total = sum(montos)
promedio = total / len(montos)
print("total:", round(total), "| promedio:", round(promedio))''',
  '''montos = df["monto_total"].tolist()
# TODO: total = suma de montos ; promedio = total / cantidad de montos
total = ...
promedio = ...
print("total:", round(total), "| promedio:", round(promedio))''',
  '''assert abs(total - df["monto_total"].sum()) < 1e-6
assert abs(promedio - df["monto_total"].mean()) < 1e-6''',
  "sum(montos) y total / len(montos).",
  None),

 ("## 2. Listas y comprensiones: filtrar",
  "Una **comprensión de lista** filtra en una línea. Contemos las compras caras.",
  "Cuenta los montos sobre $500.000",
  '''caros = [m for m in montos if m > 500_000]
n_caros = len(caros)
print("compras > $500.000:", n_caros)''',
  '''# TODO: lista de montos mayores a 500.000 y su cantidad
caros = ...
n_caros = ...
print("compras > $500.000:", n_caros)''',
  '''assert n_caros == int((df["monto_total"] > 500_000).sum())''',
  "[m for m in montos if m > 500_000] y luego len(...).",
  None),

 ("## 3. Diccionarios y bucles: acumular por clave",
  "Un **diccionario** asocia clave→valor. Con un **bucle** sumamos el gasto por región.",
  "Gasto total por región con un bucle",
  '''gasto_region = {}
for region, monto in zip(df["region_comprador"], df["monto_total"]):
    gasto_region[region] = gasto_region.get(region, 0) + monto
print(len(gasto_region), "regiones")''',
  '''gasto_region = {}
for region, monto in zip(df["region_comprador"], df["monto_total"]):
    # TODO: súmale 'monto' al acumulado de 'region' (usa .get(region, 0))
    ...
print(len(gasto_region), "regiones")''',
  '''assert len(gasto_region) == df["region_comprador"].nunique()
assert abs(sum(gasto_region.values()) - df["monto_total"].sum()) < 1.0''',
  "gasto_region[region] = gasto_region.get(region, 0) + monto.",
  None),

 ("## 4. Condicionales: clasificar en tramos",
  "Con **if/elif/else** dentro de un bucle clasificamos cada compra por tamaño de monto.",
  "Cuenta las compras por tramo",
  '''tramos = {"bajo": 0, "medio": 0, "alto": 0}
for m in montos:
    if m < 100_000:
        tramos["bajo"] += 1
    elif m < 1_000_000:
        tramos["medio"] += 1
    else:
        tramos["alto"] += 1
print(tramos)''',
  '''tramos = {"bajo": 0, "medio": 0, "alto": 0}
for m in montos:
    # TODO: bajo si < 100.000; medio si < 1.000.000; alto en otro caso
    ...
print(tramos)''',
  '''assert sum(tramos.values()) == len(montos)
assert tramos["bajo"] + tramos["medio"] + tramos["alto"] == len(montos)''',
  "if m < 100_000 / elif m < 1_000_000 / else, sumando 1 al tramo correspondiente.",
  '''# (ilustración) Distribución de compras por tramo de monto
plt.figure(figsize=(5, 4))
plt.bar(tramos.keys(), tramos.values(), color="#4240e5")
plt.ylabel("Nº de compras"); plt.title("Compras por tramo de monto")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- **Variables, listas, diccionarios y bucles** son el alfabeto de Python; con ellos ya resumes datos reales.
- Las **comprensiones** filtran y transforman en una línea.
- En el próximo módulo (R1-01) traeremos datos desde archivos y APIs.

> *Python just-in-time: aprendiste la sintaxis resolviendo preguntas sobre compras públicas, no en abstracto.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-00", "Fundamentos: Python con datos reales", "A", "Analista de Datos", "1",
                      ["Usar **variables** y operaciones básicas sobre datos reales.",
                       "Filtrar con **listas y comprensiones**.",
                       "Acumular con **diccionarios** y **bucles**.",
                       "Clasificar con **condicionales**."],
                      "manipular datos públicos con Python puro, desde cero, en Colab.",
                      "montos, regiones y categorías de compras públicas (ChileCompra).",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
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
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
montos = df["monto_total"].tolist()
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Diccionario por comprensión",
  "Agrupar en una línea: gasto por categoría con un dict comprehension.",
  "Gasto por categoría",
  '''cats = df["categoria"].unique()
gasto_cat = {c: df[df["categoria"] == c]["monto_total"].sum() for c in cats}
print(len(gasto_cat), "categorías")''',
  '''cats = df["categoria"].unique()
# TODO: {categoria: suma de monto_total de esa categoria}
gasto_cat = ...
print(len(gasto_cat), "categorías")''',
  '''assert len(gasto_cat) == df["categoria"].nunique()
assert abs(sum(gasto_cat.values()) - df["monto_total"].sum()) < 1.0''',
  "{c: df[df['categoria']==c]['monto_total'].sum() for c in cats}."),

 ("## 2. Funciones: empaquetar un resumen",
  "Una función reutilizable que resume cualquier lista de montos.",
  "Escribe `resumen`",
  '''def resumen(lista):
    return {"n": len(lista), "total": sum(lista), "max": max(lista)}

print(resumen(montos))''',
  '''def resumen(lista):
    # TODO: dict con n (cantidad), total (suma) y max (máximo)
    ...

print(resumen(montos))''',
  '''r = resumen(montos)
assert r["n"] == len(montos)
assert r["max"] == max(montos)''',
  "Devuelve {'n': len(lista), 'total': sum(lista), 'max': max(lista)}."),

 ("## 3. El máximo con una clave",
  "Encontrar la región de mayor gasto: `max` con `key`.",
  "Región con más gasto",
  '''gasto_region = {}
for reg, m in zip(df["region_comprador"], df["monto_total"]):
    gasto_region[reg] = gasto_region.get(reg, 0) + m
top_region = max(gasto_region, key=gasto_region.get)
print("Top:", top_region)''',
  '''gasto_region = {}
for reg, m in zip(df["region_comprador"], df["monto_total"]):
    gasto_region[reg] = gasto_region.get(reg, 0) + m
# TODO: la región con mayor gasto (max con key=gasto_region.get)
top_region = ...
print("Top:", top_region)''',
  '''assert top_region == max(gasto_region, key=gasto_region.get)''',
  "max(gasto_region, key=gasto_region.get) devuelve la clave de mayor valor."),
]

PROF_HEADER = '''# R1-00 · Fundamentos — Profundización (opcional) 🔬

**Formación Pública — Línea A · Analista de Datos · Notebook de profundización**

Opcional. Más Python con datos reales: **dict por comprensión**, **funciones** y `max` con **clave**.
Mismos datos de compras públicas.

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

Entrada cero programación: variables, listas, comprensiones, diccionarios y bucles sobre montos
reales de compras públicas (`compras_ml.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: dict por comprensión, funciones, max con clave.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
