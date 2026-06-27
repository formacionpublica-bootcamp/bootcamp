"""build_R2-01.py — módulo R2-01 (Datos: traer, cruzar y limpiar).

Rama R2 (Científico de Datos). Condensa P3+P4+A2+A3: construir un dataset analítico
limpio — cruzar con merge, agregar con groupby, y limpiar nulos/duplicados/tipos.
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-01-datos-traer-cruzar-limpiar")

IMPORTS = "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt"

EJ = [
 ("## 1. Cruzar tablas con `merge`",
  "Un dataset analítico suele unir varias fuentes. Derivamos una tabla resumen por categoría y la "
  "**cruzamos** de vuelta para enriquecer cada compra con el promedio de su categoría.",
  "Enriquece cada fila con el promedio de su categoría",
  '''resumen = (df.groupby("categoria")["monto_total"].mean()
             .reset_index().rename(columns={"monto_total": "monto_prom_categoria"}))
enriquecido = df.merge(resumen, on="categoria", how="left")
print(enriquecido[["categoria", "monto_total", "monto_prom_categoria"]].head(3))''',
  '''resumen = (df.groupby("categoria")["monto_total"].mean()
             .reset_index().rename(columns={"monto_total": "monto_prom_categoria"}))
# TODO: une df con resumen por la columna "categoria" (how="left")
enriquecido = ...
print(enriquecido[["categoria", "monto_total", "monto_prom_categoria"]].head(3))''',
  '''assert "monto_prom_categoria" in enriquecido.columns
assert len(enriquecido) == len(df)''',
  "df.merge(resumen, on='categoria', how='left').",
  None),

 ("## 2. Limpiar nulos",
  "Los datos reales tienen huecos. Aquí ensuciamos a propósito y luego decidimos: ¿descartar o imputar?",
  "Cuenta y elimina los nulos",
  '''sucio = df.copy()
sucio.loc[sucio.sample(50, random_state=1).index, "monto_total"] = np.nan
n_nulos = int(sucio["monto_total"].isna().sum())
limpio = sucio.dropna(subset=["monto_total"])
print("nulos:", n_nulos, "| filas tras limpiar:", len(limpio))''',
  '''sucio = df.copy()
sucio.loc[sucio.sample(50, random_state=1).index, "monto_total"] = np.nan
# TODO: n_nulos = cuántos NaN hay en monto_total ; limpio = df sin esas filas
n_nulos = ...
limpio = ...
print("nulos:", n_nulos, "| filas tras limpiar:", len(limpio))''',
  '''assert n_nulos == 50
assert int(limpio["monto_total"].isna().sum()) == 0''',
  "sucio['monto_total'].isna().sum() y sucio.dropna(subset=['monto_total']).",
  None),

 ("## 3. Eliminar duplicados",
  "Registros repetidos inflan los conteos. `drop_duplicates` los quita.",
  "Quita las filas duplicadas",
  '''con_dup = pd.concat([df, df.head(10)], ignore_index=True)
sin_dup = con_dup.drop_duplicates()
print("con duplicados:", len(con_dup), "| sin duplicados:", len(sin_dup))''',
  '''con_dup = pd.concat([df, df.head(10)], ignore_index=True)
# TODO: elimina las filas duplicadas de con_dup
sin_dup = ...
print("con duplicados:", len(con_dup), "| sin duplicados:", len(sin_dup))''',
  '''assert len(con_dup) == len(df) + 10
assert len(sin_dup) == len(df.drop_duplicates())''',
  "con_dup.drop_duplicates().",
  None),

 ("## 4. Corregir tipos",
  "Una columna con el tipo correcto ahorra memoria y evita errores. Convertimos el tamaño a categórico.",
  "Convierte tamano_proveedor a category",
  '''df2 = df.copy()
df2["tamano_proveedor"] = df2["tamano_proveedor"].astype("category")
es_category = df2["tamano_proveedor"].dtype.name == "category"
print("es category:", es_category)''',
  '''df2 = df.copy()
# TODO: convierte la columna tamano_proveedor al tipo "category"
df2["tamano_proveedor"] = ...
es_category = df2["tamano_proveedor"].dtype.name == "category"
print("es category:", es_category)''',
  '''assert es_category is True
assert df2["tamano_proveedor"].nunique() == df["tamano_proveedor"].nunique()''',
  "df2['tamano_proveedor'].astype('category').",
  '''# (ilustración) Promedio por categoría que calculamos al cruzar
r = resumen.sort_values("monto_prom_categoria").tail(8)
plt.figure(figsize=(6, 4))
plt.barh(r["categoria"], r["monto_prom_categoria"], color="#4240e5")
plt.xlabel("Monto promedio"); plt.title("Promedio por categoría (tabla cruzada)")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- **`merge`** une tablas por una clave; **`groupby`** las resume.
- Decide entre **descartar** o **imputar** los nulos según el caso.
- **`drop_duplicates`** quita repetidos; los **tipos** correctos evitan errores.
- Con un dataset limpio y cruzado, en R2-02 haremos ingeniería de variables.

> *El 80% del trabajo de datos es dejar el dato listo. Hazlo bien y el modelo lo agradece.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-01", "Datos: traer, cruzar y limpiar", "B", "Data Scientist", "3",
                      ["**Cruzar** tablas con `merge` y resumir con `groupby`.",
                       "Detectar y tratar **nulos**.",
                       "Eliminar **duplicados**.",
                       "Corregir **tipos** de columnas."],
                      "construir un dataset analítico limpio y listo para modelar.",
                      "compras públicas (ChileCompra): monto, categoría, región, tamaño de proveedor.",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Datos cargados arriba. Construyamos un dataset limpio y cruzado."),
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


PROF_PREP = '''import pandas as pd, numpy as np, os, urllib.request
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. inner vs left join",
  "El tipo de join cambia qué filas sobreviven. Con un resumen incompleto, `inner` descarta lo que no cruza.",
  "Compara inner vs left",
  '''resumen = df.groupby("categoria")["monto_total"].mean().reset_index().head(5)  # solo 5 categorías
left = df.merge(resumen, on="categoria", how="left")
inner = df.merge(resumen, on="categoria", how="inner")
print("left:", len(left), "| inner:", len(inner))''',
  '''resumen = df.groupby("categoria")["monto_total"].mean().reset_index().head(5)
# TODO: haz un merge how="left" y otro how="inner" de df con resumen sobre "categoria"
left = ...
inner = ...
print("left:", len(left), "| inner:", len(inner))''',
  '''assert len(left) == len(df)
assert len(inner) <= len(df)''',
  "df.merge(resumen, on='categoria', how='left') y how='inner'."),

 ("## 2. Imputar con la media del grupo",
  "En vez de descartar, a veces conviene **imputar** el nulo con un valor sensato (la media de su grupo).",
  "Imputa monto por la media de la categoría",
  '''sucio = df.copy()
sucio.loc[sucio.sample(40, random_state=2).index, "monto_total"] = np.nan
sucio["monto_total"] = sucio.groupby("categoria")["monto_total"].transform(lambda s: s.fillna(s.mean()))
n_nulos = int(sucio["monto_total"].isna().sum())
print("nulos tras imputar:", n_nulos)''',
  '''sucio = df.copy()
sucio.loc[sucio.sample(40, random_state=2).index, "monto_total"] = np.nan
# TODO: rellena los NaN con la media de monto_total de cada categoria (groupby + transform + fillna)
sucio["monto_total"] = ...
n_nulos = int(sucio["monto_total"].isna().sum())
print("nulos tras imputar:", n_nulos)''',
  '''assert n_nulos == 0''',
  "sucio.groupby('categoria')['monto_total'].transform(lambda s: s.fillna(s.mean()))."),

 ("## 3. Normalizar texto (preludio de record linkage)",
  "Antes de cruzar por nombre, hay que normalizar: mayúsculas y espacios rompen los joins.",
  "Normaliza una columna de texto",
  '''cats = pd.Series(["  Pan ", "PAN", "pan"])
norm = cats.str.strip().str.lower()
n_distintos = norm.nunique()
print(norm.tolist(), "| distintos:", n_distintos)''',
  '''cats = pd.Series(["  Pan ", "PAN", "pan"])
# TODO: quita espacios y pasa a minúsculas (str.strip().str.lower())
norm = ...
n_distintos = norm.nunique()
print(norm.tolist(), "| distintos:", n_distintos)''',
  '''assert n_distintos == 1''',
  "cats.str.strip().str.lower() deja los tres como 'pan'."),
]

PROF_HEADER = '''# R2-01 · Datos: traer, cruzar y limpiar — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Opcional. **inner vs left join**, **imputación** con la media del grupo y **normalización de texto**
(preludio del record linkage de R2/A7). Mismos datos de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-01.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R2-01 · Datos: traer, cruzar y limpiar

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-01-datos-traer-cruzar-limpiar/leccion.ipynb)

Construye un dataset analítico limpio: `merge`/`groupby` para cruzar, y limpieza de nulos,
duplicados y tipos, sobre datos reales de compras públicas (`compras_ml.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: inner/left join, imputación por grupo, normalización de texto.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
