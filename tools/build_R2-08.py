"""build_R2-08.py — módulo R2-08 (Pipelines reproducibles).

Rama R2 (Científico de Datos). Empaquetar preprocesamiento + modelo en un solo objeto:
sklearn Pipeline + ColumnTransformer (imputación de la meteorología faltante, one-hot de
la estación, escalado), validación temporal sin fugas, función de entrenamiento con
semilla (reproducible) y persistencia con joblib (modelo_aire.joblib, lo crea el propio
notebook). Rearmado 2026 (retira compras públicas): ancla = PM2.5 diario SINCA
(aire_diario.csv), regresión del PM2.5 de mañana. Profundiza = transferencia con
matrícula MINEDUC 2025 (matricula.csv): pipeline con variables categóricas y una
categoría nunca vista. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-08.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-08-pipelines-reproducibles")

RAW = h.REPO_RAW

IMPORTS = """import pandas as pd, numpy as np
import matplotlib.pyplot as plt"""

INTRO = '''## El problema que vamos a resolver

Hasta ahora preparabas los datos **a mano** antes de cada modelo: rellenar faltantes, convertir
categorías, escalar… y repetir **exactamente lo mismo** con la prueba y con cada dato nuevo. En
cuanto el proceso crece, algo se rompe o se hace mal. El error más peligroso es la **fuga**
(R2-07): si calculas la mediana o la escala usando **todos** los datos antes de dividir, la prueba
«contamina» al entrenamiento.

Un **pipeline** empaqueta todos los pasos en **un solo objeto** que se entrena (`fit`) y predice
(`predict`) de una vez, siempre en el mismo orden y aprendiendo **solo del entrenamiento**. Ese
objeto se **guarda** en un archivo y se reutiliza mañana, idéntico.

**La tarea:** estimar el PM2.5 de un día en cada estación a partir del PM2.5 del día anterior,
la meteorología del día (temperatura y humedad, que en la práctica vendrían del pronóstico
meteorológico), el mes y **qué estación es**.'''

PREP = '''df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values(["estacion", "fecha"])
df["pm25_ayer"] = df.groupby("estacion")["pm25"].shift(1)
df["mes"] = df["fecha"].dt.month
# R2-01: una humedad de 0 % es imposible → la marcamos como faltante
df.loc[df["humedad_media"] == 0, "humedad_media"] = np.nan

d = df.dropna(subset=["pm25", "pm25_ayer"]).sort_values(["fecha", "estacion"]).reset_index(drop=True)
NUM = ["pm25_ayer", "temp_min", "temp_max", "humedad_media", "mes"]
CAT = ["estacion"]
X, y = d[NUM + CAT], d["pm25"]

# Corte TEMPORAL (R2-07): entrenamos con 2020–2024 y probamos con 2025
es_2025 = d["fecha"].dt.year == 2025
X_train, X_test = X[~es_2025], X[es_2025]
y_train, y_test = y[~es_2025], y[es_2025]
print("train:", X_train.shape, "| test:", X_test.shape)
print("faltantes en X_train (%):")
print((X_train.isna().mean() * 100).round(1))'''

ILUSTRA_NAN = '''# (ilustración) ¿Qué pasa si le pasamos los datos crudos a un modelo?
from sklearn.linear_model import LinearRegression
try:
    LinearRegression().fit(X_train, y_train)
except Exception as e:
    print("💥", type(e).__name__, "—", str(e).splitlines()[0])
print("Dos problemas: hay texto (la estación) y hay NaN (estaciones sin sensor de meteorología).")'''

EJ = [
 ("## 1. El `ColumnTransformer`: un tratamiento para cada tipo de columna",
  "Las columnas necesitan cosas distintas:\n\n"
  "- **Numéricas** (`NUM`): **imputar** los faltantes (con la mediana del entrenamiento) y luego "
  "**escalar** (media 0, desviación 1). Dos pasos en orden → un mini-`Pipeline`.\n"
  "- **Categórica** (`estacion`): **one-hot**, una columna 0/1 por estación. "
  "`handle_unknown=\"ignore\"` evita que falle si mañana aparece una estación nueva.\n\n"
  "El `ColumnTransformer` aplica cada receta a sus columnas y junta el resultado.\n\n"
  "> 🧠 **Analogía.** Es la **oficina de partes**: cada documento que llega se deriva a la "
  "unidad que corresponde (numéricos a una, textos a otra) y todo vuelve en un solo expediente.",
  "Arma el preprocesador",
  '''preprocesador = ColumnTransformer([
    ("num", Pipeline([("imputar", SimpleImputer(strategy="median")),
                      ("escalar", StandardScaler())]), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
])
Xt = preprocesador.fit_transform(X_train)
print("columnas después de preprocesar:", Xt.shape[1], "| NaN restantes:", int(np.isnan(Xt).sum()))''',
  '''# TODO: completa el ColumnTransformer
preprocesador = ColumnTransformer([
    # numéricas: primero SimpleImputer(strategy="median"), luego StandardScaler()
    ("num", Pipeline([("imputar", ...),
                      ("escalar", ...)]), NUM),
    # categórica: OneHotEncoder(handle_unknown="ignore")
    ("cat", ..., CAT),
])
Xt = preprocesador.fit_transform(X_train)
print("columnas después de preprocesar:", Xt.shape[1])''',
  '''assert [n for n, _, _ in preprocesador.transformers] == ["num", "cat"]
Xt_chk = np.asarray(preprocesador.fit_transform(X_train), dtype=float)
assert Xt_chk.shape[1] == len(NUM) + X_train["estacion"].nunique(), "5 numéricas + 1 columna por estación"
assert not np.isnan(Xt_chk).any(), "No deberían quedar NaN: falta el imputador"''',
  "('num', Pipeline([('imputar', SimpleImputer(strategy='median')), ('escalar', StandardScaler())]), NUM) "
  "y ('cat', OneHotEncoder(handle_unknown='ignore'), CAT).",
  None),

 ("## 2. El pipeline completo: preprocesar + modelo en un solo objeto",
  "Ahora encadenamos el preprocesador con el modelo (un bosque aleatorio, R2-05). El pipeline "
  "**se comporta como un modelo cualquiera**: `fit` aprende la mediana, la escala, las "
  "estaciones **y** el bosque, solo con el entrenamiento; `predict` aplica todo igual.\n\n"
  "¿Vale la pena? Compáralo con la **persistencia**, la predicción más ingenua y difícil de "
  "batir en contaminación: «mañana será igual que hoy».",
  "Entrena el pipeline y compáralo con la persistencia",
  '''pipe = Pipeline([
    ("pre", preprocesador),
    ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=20, random_state=42, n_jobs=-1)),
])
pipe.fit(X_train, y_train)
mae_pipe = mean_absolute_error(y_test, pipe.predict(X_test))
mae_persistencia = mean_absolute_error(y_test, X_test["pm25_ayer"])
print(f"MAE pipeline: {mae_pipe:.2f} µg/m³ | MAE «igual que hoy»: {mae_persistencia:.2f} µg/m³")''',
  '''# TODO: Pipeline con dos pasos, en orden: ("pre", preprocesador) y ("modelo", el bosque)
pipe = Pipeline([
    ...,
    ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=20, random_state=42, n_jobs=-1)),
])
# TODO: entrena con (X_train, y_train) y calcula el MAE sobre X_test
...
mae_pipe = ...
# TODO: MAE de la persistencia: predecir y_test con la columna pm25_ayer de X_test
mae_persistencia = ...
print("MAE pipeline:", mae_pipe, "| MAE persistencia:", mae_persistencia)''',
  '''assert [n for n, _ in pipe.steps] == ["pre", "modelo"]
assert abs(mae_persistencia - mean_absolute_error(y_test, X_test["pm25_ayer"])) < 1e-9
assert mae_pipe < mae_persistencia, "El pipeline debería mejorar a «mañana igual que hoy»"''',
  "Pipeline([('pre', preprocesador), ('modelo', ...)]); pipe.fit(X_train, y_train); "
  "mean_absolute_error(y_test, pipe.predict(X_test)) y mean_absolute_error(y_test, X_test['pm25_ayer']).",
  None),

 ("## 3. Validación temporal sin fugas",
  "Al pasar el **pipeline completo** a `cross_val_score`, en **cada** fold el imputador calcula "
  "su mediana y el escalador su media **solo con el entrenamiento de ese fold**: la fuga queda "
  "cerrada por diseño. Y como son datos en el tiempo, usamos `TimeSeriesSplit` (R2-07).",
  "Validación temporal del pipeline (5 folds)",
  '''scores = cross_val_score(pipe, X_train, y_train, cv=TimeSeriesSplit(n_splits=5),
                         scoring="neg_mean_absolute_error")
mae_cv = -scores.mean()
print("MAE por fold:", (-scores).round(2), f"| promedio: {mae_cv:.2f} µg/m³")''',
  '''# TODO: cross_val_score del pipe sobre (X_train, y_train) con cv=TimeSeriesSplit(n_splits=5)
#       y scoring="neg_mean_absolute_error" (sklearn lo entrega NEGATIVO)
scores = ...
mae_cv = ...
print("MAE promedio:", mae_cv)''',
  '''assert len(scores) == 5
assert mae_cv > 0, "Recuerda cambiar el signo: mae_cv = -scores.mean()"
assert abs(mae_cv + np.mean(scores)) < 1e-9''',
  "cross_val_score(pipe, X_train, y_train, cv=TimeSeriesSplit(n_splits=5), "
  "scoring='neg_mean_absolute_error'); mae_cv = -scores.mean().",
  None),

 ("## 4. Reproducible: una función de entrenamiento con semilla",
  "Un resultado que nadie puede repetir no es evidencia. Envuelve **todo** el entrenamiento en "
  "una función que reciba los datos y una **semilla** (`random_state`): con la misma semilla, "
  "el mismo resultado, hoy y en un año, en tu computador o en el de Contraloría.\n\n"
  "Fíjate en que la función **construye el pipeline desde cero** cada vez: no depende de "
  "variables sueltas que alguien pudo modificar más arriba.",
  "Escribe `entrenar()` y comprueba que es reproducible",
  '''def entrenar(X_tr, y_tr, X_te, y_te, semilla=42):
    """Construye, entrena y evalúa el pipeline completo. Devuelve (pipeline, MAE en prueba)."""
    pre = ColumnTransformer([
        ("num", Pipeline([("imputar", SimpleImputer(strategy="median")),
                          ("escalar", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    p = Pipeline([("pre", pre),
                  ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=20,
                                                   random_state=semilla, n_jobs=-1))])
    p.fit(X_tr, y_tr)
    return p, mean_absolute_error(y_te, p.predict(X_te))

_, mae_a = entrenar(X_train, y_train, X_test, y_test, semilla=42)
_, mae_b = entrenar(X_train, y_train, X_test, y_test, semilla=42)
_, mae_otra = entrenar(X_train, y_train, X_test, y_test, semilla=7)
print(f"semilla 42: {mae_a:.4f} | semilla 42 otra vez: {mae_b:.4f} | semilla 7: {mae_otra:.4f}")''',
  '''def entrenar(X_tr, y_tr, X_te, y_te, semilla=42):
    """Construye, entrena y evalúa el pipeline completo. Devuelve (pipeline, MAE en prueba)."""
    pre = ColumnTransformer([
        ("num", Pipeline([("imputar", SimpleImputer(strategy="median")),
                          ("escalar", StandardScaler())]), NUM),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
    ])
    # TODO: usa la semilla recibida como random_state del bosque
    p = Pipeline([("pre", pre),
                  ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=20,
                                                   random_state=..., n_jobs=-1))])
    # TODO: entrena p con (X_tr, y_tr) y devuelve (p, MAE sobre X_te)
    ...

_, mae_a = entrenar(X_train, y_train, X_test, y_test, semilla=42)
_, mae_b = entrenar(X_train, y_train, X_test, y_test, semilla=42)
_, mae_otra = entrenar(X_train, y_train, X_test, y_test, semilla=7)
print("semilla 42:", mae_a, "| otra vez:", mae_b, "| semilla 7:", mae_otra)''',
  '''assert mae_a == mae_b, "Con la misma semilla el MAE debe ser IDÉNTICO"
assert abs(mae_a - mae_pipe) < 1e-9, "Con semilla 42 deberías reproducir el MAE del ejercicio 2"
assert mae_otra > 0''',
  "random_state=semilla; luego p.fit(X_tr, y_tr) y return p, mean_absolute_error(y_te, p.predict(X_te)).",
  None),

 ("## 5. Guardar, recargar y usar el modelo",
  "Entrenar cada vez que se necesita una predicción no tiene sentido. Se entrena **una vez**, se "
  "**guarda** el pipeline completo con `joblib` y se **recarga** donde haga falta (R2-09). Como "
  "el preprocesamiento viaja dentro, el pipeline recargado acepta datos **crudos** — incluso con "
  "la meteorología faltante, que imputa solo.",
  "Guarda `modelo_aire.joblib`, recárgalo y predice dos días nuevos",
  '''joblib.dump(pipe, "modelo_aire.joblib")
pipe_cargado = joblib.load("modelo_aire.joblib")

dias_nuevos = pd.DataFrame({
    "pm25_ayer":     [62.0, 9.0],
    "temp_min":      [-1.5, np.nan],      # Antofagasta no mide meteorología → NaN
    "temp_max":      [14.0, np.nan],
    "humedad_media": [85.0, np.nan],
    "mes":           [6, 6],
    "estacion":      ["Cerro Navia", "Antofagasta"],
})
pred_nuevos = pipe_cargado.predict(dias_nuevos)
print("Archivo:", os.path.getsize("modelo_aire.joblib") // 1024, "KB")
for est, v in zip(dias_nuevos["estacion"], pred_nuevos):
    print(f"{est}: PM2.5 estimado ≈ {v:.1f} µg/m³")''',
  '''# TODO: guarda pipe en "modelo_aire.joblib" con joblib.dump y recárgalo con joblib.load
...
pipe_cargado = ...

dias_nuevos = pd.DataFrame({
    "pm25_ayer":     [62.0, 9.0],
    "temp_min":      [-1.5, np.nan],      # Antofagasta no mide meteorología → NaN
    "temp_max":      [14.0, np.nan],
    "humedad_media": [85.0, np.nan],
    "mes":           [6, 6],
    "estacion":      ["Cerro Navia", "Antofagasta"],
})
# TODO: predice dias_nuevos con el pipeline recargado
pred_nuevos = ...
print(pred_nuevos)''',
  '''assert os.path.exists("modelo_aire.joblib"), "Falta guardar modelo_aire.joblib"
assert len(pred_nuevos) == 2 and not np.isnan(pred_nuevos).any()
assert np.allclose(pred_nuevos, pipe.predict(dias_nuevos)), "El modelo recargado debe predecir igual que el original"
assert pred_nuevos[0] > pred_nuevos[1], "Un día de invierno en Cerro Navia debería verse peor que en Antofagasta"''',
  "joblib.dump(pipe, 'modelo_aire.joblib'); pipe_cargado = joblib.load('modelo_aire.joblib'); "
  "pred_nuevos = pipe_cargado.predict(dias_nuevos).",
  None),
]

IMPORTS_SK = '''import os, joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.metrics import mean_absolute_error'''

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Imagina que dejas el servicio y otra persona hereda `modelo_aire.joblib`. ¿Qué **más** necesita
para confiar en él y volver a entrenarlo? Haz una lista corta. (Pista: la versión de los datos,
la versión de scikit-learn, la función `entrenar()` con su semilla, el MAE de referencia y
**qué hace el modelo con las estaciones que no miden meteorología**.)'''

CIERRE = '''## Errores típicos

- **Preprocesar a mano fuera del pipeline** «por si acaso»: duplicas trabajo y reabres la puerta a la fuga.
- **Ajustar el imputador o el escalador con todos los datos** antes de dividir.
- **Olvidar `handle_unknown="ignore"`**: el modelo se cae el día que aparece una estación nueva.
- **No fijar la semilla**: el resultado cambia en cada ejecución y nadie puede auditarlo.
- **Cargar un `.joblib` de origen desconocido**: `joblib.load` puede ejecutar código; abre solo archivos tuyos o de fuentes confiables.

## Cierre

1. **ColumnTransformer:** cada tipo de columna con su receta (imputar + escalar, one-hot).
2. **Pipeline:** preprocesamiento + modelo en un solo objeto, con `fit`/`predict`.
3. **Sin fugas:** en la validación (temporal) el pipeline aprende solo de cada fold de entrenamiento.
4. **Reproducible:** una función `entrenar()` con semilla da siempre el mismo resultado.
5. **Persistencia:** `modelo_aire.joblib` guarda todo y predice sobre datos crudos.

> *En R2-09 pondrás este modelo a trabajar: una función de predicción, puntuación por lotes y
> validación de entradas.*

---
*Fuente de datos: Sistema de Información Nacional de Calidad del Aire (SINCA), Ministerio del Medio Ambiente.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-08", "Pipelines reproducibles", "R2", "Científico de Datos", "13",
                      ["Tratar cada tipo de columna con un **ColumnTransformer** (imputar, escalar, one-hot).",
                       "Encadenar preprocesamiento + modelo en un **Pipeline**.",
                       "Validar el pipeline **en el tiempo** sin fugas.",
                       "Entrenar de forma **reproducible** (función + semilla) y **guardar/cargar** con joblib."],
                      "empaquetar preprocesamiento y modelo en un pipeline reproducible, validado sin fugas "
                      "y guardado para reutilizarlo.",
                      "PM2.5 y meteorología diarios 2020–2025 de 14 estaciones SINCA (Ministerio del Medio Ambiente).",
                      n_checks=5),
        h.setup_cell("aire_diario.csv", IMPORTS),
        h.md(INTRO),
        h.md("### Preparación"), h.code(PREP), h.code(IMPORTS_SK), h.code(ILUSTRA_NAN),
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


# ── Profundización (opcional): transferencia con matrícula MINEDUC ───────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request, joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/matricula.csv", CSV)
mat = pd.read_csv(CSV)

# Tarea: estimar la matrícula total de un establecimiento a partir de sus cursos,
# si es rural, su dependencia y su región.
NUM = ["cursos", "rural"]
CAT = ["dependencia", "region"]
X_tr, X_te, y_tr, y_te = train_test_split(mat[NUM + CAT], mat["mat_total"],
                                          test_size=0.3, random_state=42)
print("train:", X_tr.shape, "| test:", X_te.shape)
print(mat["dependencia"].value_counts())'''

PROF_EJ = [
 ("## 1. Transferencia: un preprocesador con dos variables categóricas",
  "Dominio nuevo: la **matrícula escolar 2025** (MINEDUC). Ahora hay **dos** categóricas "
  "(`dependencia`, con 5 valores, y `region`, con 16) y dos numéricas. Misma receta: escalar "
  "las numéricas y one-hot a las categóricas.",
  "Arma el ColumnTransformer",
  '''pre = ColumnTransformer([
    ("num", StandardScaler(), NUM),
    ("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
])
n_columnas = pre.fit_transform(X_tr).shape[1]
print("columnas tras preprocesar:", n_columnas)''',
  '''# TODO: StandardScaler para NUM y OneHotEncoder(handle_unknown="ignore") para CAT
pre = ColumnTransformer([
    ("num", ..., NUM),
    ("cat", ..., CAT),
])
n_columnas = pre.fit_transform(X_tr).shape[1]
print("columnas tras preprocesar:", n_columnas)''',
  '''assert n_columnas == len(NUM) + X_tr["dependencia"].nunique() + X_tr["region"].nunique()''',
  "('num', StandardScaler(), NUM) y ('cat', OneHotEncoder(handle_unknown='ignore'), CAT)."),

 ("## 2. Pipeline y línea base",
  "Encadena el preprocesador con un bosque y compáralo con la línea base más simple: predecir "
  "para todos la **mediana** de matrícula del entrenamiento.",
  "Entrena el pipeline y supera a la mediana",
  '''pipe = Pipeline([("pre", pre),
                 ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=5,
                                                  random_state=42, n_jobs=-1))]).fit(X_tr, y_tr)
mae_pipe = mean_absolute_error(y_te, pipe.predict(X_te))
mae_base = mean_absolute_error(y_te, np.full(len(y_te), y_tr.median()))
print(f"MAE pipeline: {mae_pipe:.0f} estudiantes | MAE mediana: {mae_base:.0f} estudiantes")''',
  '''# TODO: Pipeline [("pre", pre), ("modelo", RandomForestRegressor(n_estimators=50, min_samples_leaf=5,
#       random_state=42, n_jobs=-1))] entrenado con (X_tr, y_tr)
pipe = ...
mae_pipe = ...
# TODO: MAE de predecir siempre y_tr.median()
mae_base = ...
print("MAE pipeline:", mae_pipe, "| MAE mediana:", mae_base)''',
  '''assert [n for n, _ in pipe.steps] == ["pre", "modelo"]
assert mae_pipe < 0.6 * mae_base, "El pipeline debería bajar mucho el error de la mediana"''',
  "Pipeline([...]).fit(X_tr, y_tr); mean_absolute_error(y_te, pipe.predict(X_te)); "
  "np.full(len(y_te), y_tr.median()) para la línea base."),

 ("## 3. Guardar, recargar y resistir una categoría nunca vista",
  "Guarda el pipeline como `modelo_matricula.joblib`, recárgalo y predice dos establecimientos "
  "nuevos. El segundo trae una región mal escrita («Region Inventada»): gracias a "
  "`handle_unknown=\"ignore\"` el pipeline **no se cae** (la trata como «ninguna región conocida»). "
  "Ojo: no fallar no es lo mismo que acertar — en producción conviene **validar** las entradas (R2-09).",
  "Persistencia y robustez ante datos nuevos",
  '''joblib.dump(pipe, "modelo_matricula.joblib")
pipe2 = joblib.load("modelo_matricula.joblib")
nuevos = pd.DataFrame({"cursos": [12, 4], "rural": [0, 1],
                       "dependencia": ["Servicio Local de Educación", "Municipal"],
                       "region": ["Metropolitana", "Region Inventada"]})
pred = pipe2.predict(nuevos)
print(pred.round(0))''',
  '''# TODO: guarda pipe en "modelo_matricula.joblib" y recárgalo en pipe2
...
pipe2 = ...
nuevos = pd.DataFrame({"cursos": [12, 4], "rural": [0, 1],
                       "dependencia": ["Servicio Local de Educación", "Municipal"],
                       "region": ["Metropolitana", "Region Inventada"]})
# TODO: predice nuevos con pipe2
pred = ...
print(pred)''',
  '''assert os.path.exists("modelo_matricula.joblib")
assert len(pred) == 2 and (np.asarray(pred) > 0).all()
assert np.allclose(pred, pipe.predict(nuevos))''',
  "joblib.dump(pipe, 'modelo_matricula.joblib'); pipe2 = joblib.load('modelo_matricula.joblib'); "
  "pred = pipe2.predict(nuevos)."),
]

PROF_HEADER = '''# R2-08 · Pipelines reproducibles — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: el mismo pipeline sobre otro dato del Estado — la **matrícula
escolar 2025** (MINEDUC). Dos variables **categóricas** con one-hot, una línea base que superar,
y un pipeline guardado que **no se cae** ante una categoría nunca vista.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-08.*\n\n"
                      "*Fuente: MINEDUC, Resumen de matrícula por establecimiento 2025 (datos abiertos).*"))
    nb.cells = cells
    return nb


README = '''# R2-08 · Pipelines reproducibles

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-08-pipelines-reproducibles/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Empaqueta preprocesamiento + modelo en un solo objeto sobre la **calidad del aire** (PM2.5 y
meteorología diarios 2020–2025 de 14 estaciones SINCA, `aire_diario.csv`): `ColumnTransformer`
(imputar la meteorología que 6 estaciones no miden, escalar, one-hot de la estación) + bosque
aleatorio en un `Pipeline`, validación temporal sin fugas, una función `entrenar()` con semilla
(reproducible) y persistencia con `joblib` (`modelo_aire.joblib`, que crea el propio notebook).
La profundización transfiere a la matrícula 2025 (`matricula.csv`, MINEDUC): pipeline con dos
categóricas y una categoría nunca vista.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: pipeline categórico con matrícula, línea base y `handle_unknown`.
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
