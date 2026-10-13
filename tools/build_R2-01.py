"""build_R2-01.py — módulo R2-01 (Datos: traer, cruzar y limpiar).

Rama R2 (Científico de Datos). Construir un dataset analítico limpio: cruzar con
merge, corregir tipos (fechas), diagnosticar faltantes REALES y tomar decisiones de
limpieza declaradas. Rearmado 2026: ancla = PM2.5 diario
SINCA (aire_diario.csv) × estaciones.csv. Faltantes reales: 7 de 14 estaciones no
miden meteorología; en Las Encinas Temuco los 240 registros de humedad son 0 %
(imposible: sensor defectuoso; 230 tras descartar los días sin PM2.5).
Profundiza = transferencia: matrícula por RBD × directorio MINEDUC (4 huérfanas
reales). Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-01-datos-traer-cruzar-limpiar")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "estaciones.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

df = pd.read_csv("aire_diario.csv")          # mediciones: un día por estación
estaciones = pd.read_csv("estaciones.csv")   # catálogo: dónde está cada estación
print("mediciones:", df.shape, "| estaciones:", estaciones.shape)
df.head(3)'''

INTRO = '''## Dos tablas, un dataset analítico

- `df` — las **mediciones**: un día por estación con su PM2.5 (µg/m³), temperatura y humedad.
- `estaciones` — el **catálogo**: comuna, región y coordenadas de cada una de las 14 estaciones.

Un modelo (y una jefatura) necesita las dos cosas juntas: *«¿cuánto PM2.5 hubo, dónde y
cuándo?»*. En este módulo vas a construir ese **dataset analítico** paso a paso — y en el camino
vas a encontrar problemas **reales**, no inventados: estaciones que nunca midieron temperatura,
días sin dato de PM2.5 y una humedad imposible. Para cada uno vas a tomar (y declarar) una decisión.

> 🧭 **Regla de la casa:** limpiar no es «borrar lo feo». Es **diagnosticar, decidir y dejar
> escrito por qué**.'''

EJ = [
 ("## 1. Cruzar tablas con `merge`",
  "La columna `estacion` existe en ambas tablas: es la **llave**. Con `how=\"left\"` conservas "
  "**todas** las mediciones y les pegas la comuna y la región; si alguna estación no estuviera "
  "en el catálogo, quedaría con región nula (una fila **huérfana**) y la podrías contar.",
  "Enriquece cada medición con su comuna y región",
  '''aire = df.merge(estaciones, on="estacion", how="left")
n_huerfanas = int(aire["region"].isna().sum())
print("filas:", len(aire), "| huérfanas:", n_huerfanas)
print(aire[["fecha", "estacion", "comuna", "region", "pm25"]].head(3))''',
  '''# TODO: une df con estaciones por la llave "estacion" (how="left")
aire = ...
# TODO: cuántas filas quedaron sin región (huérfanas)
n_huerfanas = ...
print("filas:", len(aire), "| huérfanas:", n_huerfanas)''',
  '''assert "region" in aire.columns and "comuna" in aire.columns
assert len(aire) == len(df)
assert n_huerfanas == int(aire["region"].isna().sum())''',
  "df.merge(estaciones, on='estacion', how='left'); las huérfanas con aire['region'].isna().sum().",
  None),

 ("## 2. Corregir tipos: las fechas",
  "`fecha` llegó como **texto** (`object`): pandas no sabe que «2024-07-01» es un día de invierno. "
  "Con `pd.to_datetime` la conviertes en fecha de verdad y puedes extraer el **año** y el **mes** "
  "(`.dt.year`, `.dt.month`) — variables clave para un fenómeno tan estacional como el PM2.5.",
  "Convierte `fecha` a datetime y crea `anio` y `mes`",
  '''aire["fecha"] = pd.to_datetime(aire["fecha"])
aire["anio"] = aire["fecha"].dt.year
aire["mes"] = aire["fecha"].dt.month
print(aire.dtypes[["fecha", "anio", "mes"]])
print("desde", aire["fecha"].min().date(), "hasta", aire["fecha"].max().date())''',
  '''# TODO: convierte la columna fecha con pd.to_datetime
aire["fecha"] = ...
# TODO: extrae el año y el mes con .dt.year y .dt.month
aire["anio"] = ...
aire["mes"] = ...
print(aire.dtypes[["fecha", "anio", "mes"]])''',
  '''assert pd.api.types.is_datetime64_any_dtype(aire["fecha"])
assert set(aire["mes"].unique()) == set(range(1, 13))
assert aire["anio"].min() == 2020 and aire["anio"].max() == 2025''',
  "pd.to_datetime(aire['fecha']); luego aire['fecha'].dt.year y aire['fecha'].dt.month.",
  None),

 ("## 3. Faltantes reales: diagnosticar antes de decidir",
  "Hay dos tipos de huecos muy distintos:\n\n"
  "- **Meteorología:** algunas estaciones **no tienen sensor** de temperatura — su `temp_media` "
  "está vacía el 100 % de los días. Imputar ahí sería **inventar** datos.\n"
  "- **PM2.5:** días sueltos sin medición (mantenimiento, fallas). Para analizar el PM2.5, esas "
  "filas no aportan: se pueden **descartar**, declarándolo.\n\n"
  "Calcula la proporción de nulos de `temp_media` por estación, lista las estaciones **sin** "
  "meteorología y arma `limpio` sin las filas que no tienen PM2.5.",
  "Diagnostica los nulos y descarta los días sin PM2.5",
  '''pct_nulos_temp = aire["temp_media"].isna().groupby(aire["estacion"]).mean()
sin_meteo = sorted(pct_nulos_temp[pct_nulos_temp == 1].index)
n_nulos_pm25 = int(aire["pm25"].isna().sum())
limpio = aire.dropna(subset=["pm25"])
print(pct_nulos_temp.round(2).sort_values(ascending=False))
print("estaciones sin meteorología:", sin_meteo)
print("días sin PM2.5:", n_nulos_pm25, "| filas tras descartar:", len(limpio))''',
  '''# TODO: proporción de nulos de temp_media por estación (isna() + groupby + mean)
pct_nulos_temp = ...
# TODO: lista ordenada de las estaciones con 100 % de nulos (== 1)
sin_meteo = ...
# TODO: cuántos nulos tiene pm25, y limpio = aire sin esas filas (dropna con subset)
n_nulos_pm25 = ...
limpio = ...
print("estaciones sin meteorología:", sin_meteo)
print("días sin PM2.5:", n_nulos_pm25, "| filas tras descartar:", len(limpio))''',
  '''assert abs(pct_nulos_temp.sum() - aire["temp_media"].isna().groupby(aire["estacion"]).mean().sum()) < 1e-9
assert len(sin_meteo) == 7 and "Antofagasta" in sin_meteo
assert n_nulos_pm25 == int(aire["pm25"].isna().sum())
assert int(limpio["pm25"].isna().sum()) == 0 and len(limpio) == len(aire) - n_nulos_pm25''',
  "aire['temp_media'].isna().groupby(aire['estacion']).mean(); sin_meteo = sorted(pct_nulos_temp[pct_nulos_temp == 1].index); aire.dropna(subset=['pm25']).",
  None),

 ("## 4. Decisiones de limpieza: duplicados y valores imposibles",
  "Dos chequeos que todo dataset analítico merece:\n\n"
  "1. **Duplicados de llave:** en esta tabla la combinación `(fecha, estacion)` debería ser única. "
  "Si hubiera repetidos, los promedios quedarían inflados. Cuéntalos con `duplicated(subset=...)`.\n"
  "2. **Valores imposibles:** una humedad relativa media de **0 %** en un día entero no ocurre en "
  "Chile habitado — es un error de registro del sensor. La decisión honesta es convertirla en "
  "**faltante** (`np.nan`), no dejarla como si fuera real. (Spoiler: en una estación **todos** "
  "sus registros de humedad son 0 % — un sensor que nunca midió.)",
  "Cuenta duplicados y anula las humedades imposibles",
  '''n_dup = int(limpio.duplicated(subset=["fecha", "estacion"]).sum())
limpio = limpio.copy()
n_hum_cero = int((limpio["humedad_media"] == 0).sum())
limpio.loc[limpio["humedad_media"] == 0, "humedad_media"] = np.nan
print("duplicados (fecha, estacion):", n_dup)
print("humedades 0 % convertidas en NaN:", n_hum_cero)
print("¿en qué estación?", aire.loc[aire["humedad_media"] == 0, "estacion"].unique())''',
  '''# TODO: cuántas filas repiten la llave (fecha, estacion) -> duplicated(subset=[...]).sum()
n_dup = ...
limpio = limpio.copy()
# TODO: cuántas filas tienen humedad_media == 0
n_hum_cero = ...
# TODO: reemplaza esas humedades por np.nan (usa limpio.loc[condición, "humedad_media"] = np.nan)
...
print("duplicados (fecha, estacion):", n_dup)
print("humedades 0 % convertidas en NaN:", n_hum_cero)''',
  '''assert n_dup == int(limpio.duplicated(subset=["fecha", "estacion"]).sum())
assert n_hum_cero == int((aire.dropna(subset=["pm25"])["humedad_media"] == 0).sum()) and n_hum_cero > 0
assert int((limpio["humedad_media"] == 0).sum()) == 0''',
  "limpio.duplicated(subset=['fecha','estacion']).sum(); (limpio['humedad_media'] == 0).sum(); limpio.loc[limpio['humedad_media'] == 0, 'humedad_media'] = np.nan.",
  '''# (ilustración) El dataset analítico ya responde: PM2.5 promedio por mes y región
tabla = limpio.groupby(["mes", "region"])["pm25"].mean().unstack()
tabla.plot(figsize=(8, 4.5), marker="o")
plt.axhline(50, color="#c0392b", ls="--", lw=1, label="norma diaria (50 µg/m³)")
plt.ylabel("PM2.5 promedio (µg/m³)"); plt.xlabel("mes"); plt.xticks(range(1, 13))
plt.title("El invierno pesa: PM2.5 promedio por mes y región (2020–2025)")
plt.legend(fontsize=7, ncol=2); plt.tight_layout(); plt.show()'''),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Tomaste tres decisiones: **no imputar** la temperatura de 7 estaciones sin sensor, **descartar**
los días sin PM2.5 y **anular** las humedades de 0 %. Escribe en dos líneas la «nota
metodológica» que acompañaría este dataset en un informe: qué hiciste, por qué, y cuántas filas
afectó cada decisión.

> Un dataset sin su nota metodológica es una caja negra. Con ella, es evidencia.'''

CIERRE = '''## Cierre

- **`merge`** une mediciones con su catálogo por una **llave**; `how="left"` deja ver las huérfanas.
- Las **fechas** se convierten con `pd.to_datetime`; de ahí salen año y mes, claves en datos estacionales.
- Los **faltantes** se diagnostican antes de tratarlos: no es lo mismo «no hay sensor» que «falló un día».
- **Duplicados de llave** y **valores imposibles** se revisan siempre — y cada decisión se declara.

> *El 80% del trabajo de datos es dejar el dato listo. En R2-02 vas a fabricar variables
> (features) con SQL sobre este mismo dataset: promedios por mes, el PM2.5 de ayer, medias móviles.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-01", "Datos: traer, cruzar y limpiar", "R2", "Científico de Datos", "3",
                      ["**Cruzar** mediciones con su catálogo usando `merge` (y auditar huérfanas).",
                       "Corregir **tipos**: texto → fecha, y extraer año y mes.",
                       "Diagnosticar **faltantes reales** y decidir: descartar, imputar o dejar.",
                       "Revisar **duplicados de llave** y **valores imposibles**."],
                      "construir un dataset analítico limpio, con sus decisiones de limpieza declaradas.",
                      "PM2.5 y meteorología diaria de 14 estaciones SINCA (2020–2025) × catálogo de estaciones (comuna, región, coordenadas).",
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
for archivo in ["matricula_rbd.csv", "directorio_establecimientos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)
mat = pd.read_csv("matricula_rbd.csv")                  # conteos de estudiantes por RBD
directorio = pd.read_csv("directorio_establecimientos.csv")  # quién es cada RBD
print("matrícula:", mat.shape, "| directorio:", directorio.shape)'''

PROF_EJ = [
 ("## 1. Antes de cruzar: ¿la llave es única? Y después: inner vs left",
  "Si el RBD se repitiera en el directorio, el cruce **multiplicaría** filas. Verifica la "
  "unicidad con `.is_unique` y luego compara cuántas filas sobreviven con `inner` y con `left`.",
  "Verifica la llave y compara inner vs left",
  '''llave_unica = bool(mat["rbd"].is_unique and directorio["rbd"].is_unique)
inner = mat.merge(directorio, on="rbd", how="inner")
left = mat.merge(directorio, on="rbd", how="left")
print("llave única en ambas:", llave_unica, "| inner:", len(inner), "| left:", len(left))''',
  '''# TODO: True si rbd es único en mat Y en directorio (usa .is_unique)
llave_unica = ...
# TODO: merge how="inner" y how="left" de mat con directorio por "rbd"
inner = ...
left = ...
print("llave única en ambas:", llave_unica, "| inner:", len(inner), "| left:", len(left))''',
  '''assert llave_unica == bool(mat["rbd"].is_unique and directorio["rbd"].is_unique)
assert len(left) == len(mat)
assert len(inner) < len(left)''',
  "mat['rbd'].is_unique and directorio['rbd'].is_unique; mat.merge(directorio, on='rbd', how='inner'/'left')."),

 ("## 2. Cazar las huérfanas y medir su peso",
  "Las filas que el `inner` botó en silencio son las que en el `left` quedaron sin región. "
  "¿Cuántas son y **cuántos estudiantes** representan? Ese número decide si importan.",
  "Cuenta huérfanas y sus estudiantes",
  '''huerfanas = left[left["region"].isna()]
n_huerfanas = len(huerfanas)
est_huerfanos = int(huerfanas["mat_total"].sum())
print("huérfanas:", n_huerfanas, "| estudiantes en ellas:", est_huerfanos)
huerfanas''',
  '''# TODO: filas de left sin región, cuántas son y cuántos estudiantes (mat_total) suman
huerfanas = ...
n_huerfanas = ...
est_huerfanos = ...
print("huérfanas:", n_huerfanas, "| estudiantes en ellas:", est_huerfanos)''',
  '''assert n_huerfanas == len(mat) - len(inner)
assert est_huerfanos == int(left.loc[left["region"].isna(), "mat_total"].sum())''',
  "left[left['region'].isna()]; len(...) y ['mat_total'].sum()."),

 ("## 3. Imputar con una categoría explícita (en vez de botar)",
  "Una decisión defendible: no botar las huérfanas, sino **etiquetarlas** como "
  "`\"Sin directorio\"` con `fillna`. Así ningún estudiante desaparece del total y el informe "
  "muestra la categoría a la vista.",
  "Etiqueta las huérfanas y resume por dependencia",
  '''cruce = left.copy()
cruce["dependencia"] = cruce["dependencia"].fillna("Sin directorio")
est_dep = cruce.groupby("dependencia")["mat_total"].sum().sort_values(ascending=False)
print(est_dep)''',
  '''cruce = left.copy()
# TODO: rellena los nulos de dependencia con "Sin directorio"
cruce["dependencia"] = ...
# TODO: estudiantes (mat_total) por dependencia, de mayor a menor
est_dep = ...
print(est_dep)''',
  '''assert "Sin directorio" in est_dep.index
assert int(est_dep.sum()) == int(mat["mat_total"].sum())''',
  "cruce['dependencia'].fillna('Sin directorio'); luego groupby('dependencia')['mat_total'].sum().sort_values(ascending=False)."),
]

PROF_HEADER = '''# R2-01 · Datos: traer, cruzar y limpiar — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: el mismo oficio sobre otro dato del Estado. Cruza los conteos
de **matrícula 2025 por RBD** con el **directorio oficial** de establecimientos (MINEDUC):
verificar que la llave sea única, comparar **inner vs left**, cazar las **filas huérfanas** reales
y decidir qué hacer con ellas sin perder estudiantes del total.

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


README = '''# R2-01 · Datos: traer, cruzar y limpiar

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-01-datos-traer-cruzar-limpiar/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Construye un dataset analítico limpio sobre la **calidad del aire**: cruza el PM2.5 diario de
14 estaciones SINCA 2020–2025 (`aire_diario.csv`, 30.674 filas) con su catálogo
(`estaciones.csv`: comuna, región, coordenadas), convierte las fechas, diagnostica los
**faltantes reales** (7 de 14 estaciones sin sensor meteorológico, 1.030 días sin PM2.5) y toma
decisiones de limpieza declaradas: duplicados de llave y humedades de 0 % imposibles (los 240
registros de humedad de Las Encinas Temuco son 0 %; 230 quedan tras descartar los días sin PM2.5).
La profundización transfiere el cruce a la matrícula 2025 por RBD (`matricula_rbd.csv`) ×
directorio MINEDUC (`directorio_establecimientos.csv`), con 4 huérfanas reales.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: llave única, inner vs left, huérfanas, imputar con categoría explícita.
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
