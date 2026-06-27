"""build_R2-00.py — módulo R2-00 (Fundamentos express: Python + pandas).

Rama R2 (Científico de Datos), entrada cero programación condensada. Une P1+P2+A1:
del cero a manipular un DataFrame de compras públicas (cargar, inspeccionar, filtrar,
seleccionar, ordenar, agregar). Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-00.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-00-fundamentos-express")

IMPORTS = "import pandas as pd\nimport matplotlib.pyplot as plt"

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
  '''assert n_filas == len(df)
assert "monto_total" in columnas''',
  "df.shape es (filas, columnas); list(df.columns) da los nombres.",
  None),

 ("## 2. Filtrar filas con una condición",
  "Una **máscara booleana** selecciona filas. Quedémonos con las compras a proveedores grandes.",
  "Filtra los proveedores Grande",
  '''grandes = df[df["tamano_proveedor"] == "Grande"]
n_grandes = len(grandes)
print("compras a proveedores Grande:", n_grandes)''',
  '''# TODO: filtra df donde tamano_proveedor sea "Grande"
grandes = ...
n_grandes = len(grandes)
print("compras a proveedores Grande:", n_grandes)''',
  '''assert (grandes["tamano_proveedor"] == "Grande").all()
assert n_grandes == int((df["tamano_proveedor"] == "Grande").sum())''',
  "df[df['tamano_proveedor'] == 'Grande'].",
  None),

 ("## 3. Seleccionar columnas y ordenar",
  "Elegir columnas y **ordenar** para ver lo más relevante: las compras de mayor monto.",
  "Top 10 compras por monto",
  '''top = df.sort_values("monto_total", ascending=False).head(10)[["categoria", "monto_total"]]
print(top)''',
  '''# TODO: ordena df por monto_total desc, toma head(10) y las columnas ["categoria", "monto_total"]
top = ...
print(top)''',
  '''assert list(top.columns) == ["categoria", "monto_total"]
assert top["monto_total"].is_monotonic_decreasing''',
  "df.sort_values('monto_total', ascending=False).head(10)[['categoria','monto_total']].",
  None),

 ("## 4. Agregar: una pregunta, una respuesta",
  "**`groupby`** resume por grupo. ¿Cuál es el monto promedio por categoría?",
  "Monto promedio por categoría",
  '''gasto_categoria = df.groupby("categoria")["monto_total"].mean()
print(gasto_categoria.round(0))''',
  '''# TODO: agrupa por categoria y calcula la media de monto_total
gasto_categoria = ...
print(gasto_categoria.round(0))''',
  '''assert len(gasto_categoria) == df["categoria"].nunique()
assert gasto_categoria.min() >= 0''',
  "df.groupby('categoria')['monto_total'].mean().",
  '''# (ilustración) Monto promedio por categoría (top 8)
g = gasto_categoria.sort_values().tail(8)
plt.figure(figsize=(6, 4))
plt.barh(g.index, g.values, color="#4240e5")
plt.xlabel("Monto promedio"); plt.title("Promedio por categoría (top 8)")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- Un **DataFrame** se inspecciona con `shape`/`columns`/`head` antes de tocarlo.
- **Máscaras booleanas** filtran filas; `sort_values` ordena; selección con `[[...]]`.
- **`groupby`** responde preguntas agregadas en una línea.
- Con esto ya estás listo para la ingeniería de variables de R2-02.

> *Python y pandas just-in-time: lo aprendiste resolviendo preguntas sobre compras públicas reales.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-00", "Fundamentos express: Python + pandas", "B", "Data Scientist", "1–2",
                      ["Cargar e **inspeccionar** un DataFrame.",
                       "**Filtrar** filas con máscaras booleanas.",
                       "**Seleccionar** columnas y **ordenar**.",
                       "**Agregar** con `groupby`."],
                      "manipular un DataFrame de datos públicos desde cero, en Colab.",
                      "compras públicas (ChileCompra): monto, categoría, región, tamaño de proveedor.",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Datos cargados arriba. A manipular el DataFrame."),
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
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Filtros combinados",
  "Varias condiciones a la vez con `&` (y) / `|` (o), cada una entre paréntesis.",
  "Grandes con monto alto",
  '''sel = df[(df["tamano_proveedor"] == "Grande") & (df["monto_total"] > 1_000_000)]
print(len(sel), "filas")''',
  '''# TODO: filtra Grande Y monto_total > 1.000.000 (cada condición entre paréntesis, unidas con &)
sel = ...
print(len(sel), "filas")''',
  '''assert (sel["tamano_proveedor"] == "Grande").all()
assert (sel["monto_total"] > 1_000_000).all()''',
  "df[(df['tamano_proveedor']=='Grande') & (df['monto_total']>1_000_000)]."),

 ("## 2. Conteos rápidos con value_counts",
  "`value_counts` cuenta ocurrencias por categoría: ideal para un primer diagnóstico.",
  "Cuenta compras por tamaño de proveedor",
  '''conteo = df["tamano_proveedor"].value_counts()
print(conteo)''',
  '''# TODO: value_counts sobre la columna tamano_proveedor
conteo = ...
print(conteo)''',
  '''assert conteo.sum() == len(df)
assert set(conteo.index) == set(df["tamano_proveedor"].unique())''',
  "df['tamano_proveedor'].value_counts()."),

 ("## 3. Crear una columna derivada",
  "El feature engineering empieza aquí: una columna nueva calculada desde otras.",
  "Crea `monto_por_unidad`",
  '''df2 = df.copy()
df2["monto_por_unidad"] = df2["monto_total"] / df2["cantidad"]
print(df2["monto_por_unidad"].describe().round(1))''',
  '''df2 = df.copy()
# TODO: nueva columna monto_por_unidad = monto_total / cantidad
df2["monto_por_unidad"] = ...
print(df2["monto_por_unidad"].describe().round(1))''',
  '''assert "monto_por_unidad" in df2.columns
assert (df2["monto_por_unidad"] >= 0).all()''',
  "df2['monto_total'] / df2['cantidad']."),
]

PROF_HEADER = '''# R2-00 · Fundamentos express — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Opcional. **Filtros combinados**, **`value_counts`** y una primera **columna derivada** (preludio del
feature engineering de R2-02). Mismos datos de compras públicas.

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


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R2-00 · Fundamentos express: Python + pandas

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-00-fundamentos-express/leccion.ipynb)

Del cero a manipular un DataFrame de compras públicas: cargar, inspeccionar, filtrar, seleccionar,
ordenar y agregar con `groupby`.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: filtros combinados, value_counts, columna derivada.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
