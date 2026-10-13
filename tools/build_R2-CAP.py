"""build_R2-CAP.py — Capstone de la rama R2 (Científico de Datos).

Proyecto-plantilla del ciclo ML de punta a punta: enmarcar → features SIN FUGA →
partición temporal → modelo → evaluación contra línea base → ficha de modelo →
brief, con rúbrica (incluye Pertinencia, como R1-CAP) y banco de datasets (propio
del servicio > banco del bootcamp > datos.gob.cl). Rearmado 2026: se retira el
ejemplo anterior; el ejemplo guía es «¿mañana esta estación superará la
norma de PM2.5?» con aire_diario.csv (SINCA, 2020–2025). Convención de la casa.
Profundiza: validación cruzada temporal, desempeño por estación (equidad
territorial) y el trade-off recall/precision con class_weight.

Uso:  /opt/anaconda3/bin/python tools/build_R2-CAP.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-CAP-capstone-modelo")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, precision_score, classification_report

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "aire_diario.csv"          # ← reemplázalo por el dataset de tu organismo
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)

df = pd.read_csv(CSV, parse_dates=["fecha"])
print("Datos cargados:", df.shape, "filas x columnas")
df.head()'''

ENMARCA = '''## 1. Enmarca el problema de modelado

Antes de tocar un modelo, escribe en una frase la **decisión pública** que el modelo va a apoyar
y por qué un modelo aporta algo que una regla simple no. Ejemplo guía:

> *Anticipar, con un día de aviso, los días en que una estación de monitoreo superará la norma
> diaria de PM2.5 (50 µg/m³, D.S. 12/2011 del MMA), para que el equipo de gestión ambiental
> prepare medidas preventivas y avisos a la población — **con revisión humana**.*

Dos preguntas que el capstone debe responder con honestidad: **¿le gana a la regla simple?**
(«si hoy superó la norma, mañana también») y **¿para quién funciona peor?**

**Elige tu dataset** (en este orden de preferencia):

1. **Datos de tu propio organismo** — el capstone vale el doble si responde una pregunta real
   de tu servicio (con los resguardos de datos personales que corresponden).
2. El **banco del bootcamp** (todos reales y ya curados, en `data/` del repositorio):
   `aire_diario.csv` + `aire_nuevos.csv` (PM2.5 diario por estación SINCA, 2020–2025 y 2026) ·
   `sismos.csv` (USGS M≥4,5, 2020–2025) · `matricula.csv` / `establecimientos.csv` (MINEDUC 2025) ·
   `reclamos.csv` (SERNAC, histórico 2011) · `fichas.csv` (trámites ChileAtiende) ·
   `comunas.csv` · `parques.csv`.
3. Cualquier dataset de **datos.gob.cl** (ya sabes usar su API, R1-01).

> Esta plantilla usa `aire_diario.csv` como ejemplo; reemplázalo por el tuyo y adapta cada paso.'''

TABLA_MD = '''### Tabla de modelado (ejemplo ya hecho)

Una fila = **una estación en un día**. Las *features* describen lo que se sabe **hoy**; el
objetivo es lo que pasará **mañana**. Fíjate que la tabla trae, a propósito, dos columnas del
futuro (`pm25_manana` y `episodio_manana`): son la respuesta, y una de ellas es una trampa.'''

TABLA = '''def construir_tabla(df):
    partes = []
    for estacion, d in df.groupby("estacion"):
        d = d.set_index("fecha").sort_index().asfreq("D")      # calendario completo
        d["estacion"] = estacion
        d["pm25_ayer"] = d["pm25"].shift(1)
        d["media_7d"] = d["pm25"].rolling(7, min_periods=5).mean()
        d["mes"] = d.index.month
        d["pm25_manana"] = d["pm25"].shift(-1)                  # ⚠️ el futuro
        partes.append(d.reset_index())
    t = pd.concat(partes, ignore_index=True)
    t = t.dropna(subset=["pm25", "pm25_ayer", "media_7d", "pm25_manana"]).reset_index(drop=True)
    t["episodio_manana"] = (t["pm25_manana"] > 50).astype(int)  # objetivo: 1 si mañana supera la norma
    return t

tabla = construir_tabla(df)
print("filas:", len(tabla), f"| días-estación con episodio mañana: {100 * tabla['episodio_manana'].mean():.1f}%")
tabla[["fecha", "estacion", "pm25", "pm25_ayer", "media_7d", "mes", "pm25_manana", "episodio_manana"]].head(3)'''

EJ = [
 ("## 2. Features sin fuga de datos",
  "El error más caro de la ciencia de datos: entrenar con una variable que **es** la respuesta "
  "o que **viene del futuro**. `pm25_manana` es exactamente lo que queremos predecir: si la "
  "dejas, el modelo saca F1 ≈ 0,99 en la prueba — demasiado bueno para ser verdad — y en "
  "producción no existirá. Elige solo lo que se conoce **hoy**.",
  "Define FEATURES y el objetivo — sin fuga",
  '''FEATURES = ["estacion", "pm25", "pm25_ayer", "media_7d", "mes"]   # NO pm25_manana ni episodio_manana
y = tabla["episodio_manana"]
X = tabla[FEATURES]
print("features:", FEATURES, "| positivos:", f"{100 * y.mean():.1f}%")''',
  '''# TODO: lista de columnas que se conocen HOY (de: estacion, pm25, pm25_ayer, media_7d, mes, pm25_manana)
FEATURES = ...
y = tabla["episodio_manana"]
X = tabla[FEATURES] if isinstance(FEATURES, list) else None
print("features:", FEATURES)''',
  '''assert isinstance(FEATURES, list) and len(FEATURES) >= 3
assert "pm25_manana" not in FEATURES and "episodio_manana" not in FEATURES, "¡fuga! hay una columna del futuro"
assert set(FEATURES) <= set(tabla.columns)''',
  "Usa estacion, pm25, pm25_ayer, media_7d y mes; nunca pm25_manana ni episodio_manana.",
  None),

 ("## 3. Partición temporal",
  "Con datos en el tiempo, la prueba debe estar **después** del entrenamiento: entrena con "
  "2020–2024 y prueba con 2025. Un `train_test_split` al azar mezclaría días vecinos entre "
  "entrenamiento y prueba (el PM2.5 de hoy se parece mucho al de ayer) y daría una idea "
  "optimista de lo que pasará con datos realmente nuevos.",
  "Separa entrenamiento (≤ 2024) y prueba (2025)",
  '''en_prueba = tabla["fecha"] >= "2025-01-01"
Xtr, ytr = X[~en_prueba], y[~en_prueba]
Xte, yte = X[en_prueba], y[en_prueba]
print("entrenamiento:", len(Xtr), "| prueba:", len(Xte), f"| episodios en prueba: {int(yte.sum())}")''',
  '''# TODO: máscara True para las filas de 2025 en adelante
en_prueba = ...
# TODO: separa X e y con la máscara (entrenamiento = ~en_prueba)
Xtr, ytr = ..., ...
Xte, yte = ..., ...''',
  '''_m = tabla["fecha"] >= "2025-01-01"
assert len(Xtr) == int((~_m).sum()) and len(Xte) == int(_m.sum())
assert tabla.loc[Xtr.index, "fecha"].max() < tabla.loc[Xte.index, "fecha"].min(), "la prueba debe ser posterior"''',
  'en_prueba = tabla["fecha"] >= "2025-01-01"; Xtr, ytr = X[~en_prueba], y[~en_prueba]; Xte, yte = X[en_prueba], y[en_prueba].',
  None),

 ("## 4. Entrena el modelo",
  "Un **pipeline** con codificación one-hot de las categóricas (estación y mes) y escalado de las "
  "numéricas, más una **regresión logística**. El pipeline aprende el preprocesamiento solo con "
  "el entrenamiento: sin fuga por la puerta de atrás.",
  "Entrena el pipeline",
  '''pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["estacion", "mes"]),
    ("num", StandardScaler(), ["pm25", "pm25_ayer", "media_7d"]),
])
modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
print("modelo entrenado:", hasattr(modelo, "classes_"))''',
  '''pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["estacion", "mes"]),
    ("num", StandardScaler(), ["pm25", "pm25_ayer", "media_7d"]),
])
# TODO: Pipeline(pre + LogisticRegression(max_iter=1000)) entrenado con Xtr, ytr
modelo = ...
print("modelo entrenado:", hasattr(modelo, "classes_"))''',
  '''assert hasattr(modelo, "predict") and hasattr(modelo, "classes_"), "falta el .fit(Xtr, ytr)"
assert list(modelo.classes_) == [0, 1]''',
  "Pipeline([('pre', pre), ('clf', LogisticRegression(max_iter=1000))]).fit(Xtr, ytr).",
  None),

 ("## 5. Evalúa honestamente: contra la línea base",
  "Los episodios son pocos (≈3% de los días-estación de 2025): la *accuracy* engaña, usa **F1** y "
  "***recall***. Y un modelo no se evalúa solo: se compara con la **regla simple** que ya usaría "
  "cualquiera — «si hoy superó 50, mañana también» (persistencia).",
  "F1 del modelo vs F1 de la persistencia",
  '''pred = modelo.predict(Xte)
f1_modelo = f1_score(yte, pred)
recall_modelo = recall_score(yte, pred)
base = (Xte["pm25"] > 50).astype(int)
f1_base = f1_score(yte, base)
print(f"modelo      → F1 {f1_modelo:.3f} · recall {recall_modelo:.3f} · precision {precision_score(yte, pred):.3f}")
print(f"persistencia → F1 {f1_base:.3f} · recall {recall_score(yte, base):.3f} · precision {precision_score(yte, base):.3f}")''',
  '''pred = modelo.predict(Xte)
# TODO: F1 y recall del modelo en la prueba
f1_modelo = ...
recall_modelo = ...
# TODO: línea base de persistencia: 1 si el pm25 de HOY (Xte["pm25"]) supera 50; y su F1
base = ...
f1_base = ...
print("F1 modelo:", f1_modelo, "| F1 persistencia:", f1_base)''',
  '''_p = modelo.predict(Xte)
assert abs(f1_modelo - f1_score(yte, _p)) < 1e-9 and abs(recall_modelo - recall_score(yte, _p)) < 1e-9
assert abs(f1_base - f1_score(yte, (Xte["pm25"] > 50).astype(int))) < 1e-9''',
  'f1_score(yte, pred), recall_score(yte, pred); base = (Xte["pm25"] > 50).astype(int); f1_score(yte, base).',
  None),
]

MODEL_CARD = '''## 6. Ficha del modelo (*model card*)

Completa esta ficha con **tus** números (los del ejemplo están entre paréntesis). Acompaña al
modelo siempre que lo entregues:

> **Nombre / versión:** _(p. ej. alerta-pm25-manana v1)_
> **Decisión que apoya y usuarios:** _(quién lo usa, para qué; con revisión humana)_
> **Datos:** _(fuente, período, unidad de análisis; ejemplo: SINCA, 14 estaciones, 2020–2025, una fila = estación-día)_
> **Partición:** _(ejemplo: entrena 2020–2024, prueba 2025 — temporal, sin barajar)_
> **Desempeño:** F1 = ___ ; recall = ___ ; **línea base** (persistencia) F1 = ___
> **¿Le gana a la línea base?** _(dilo con el número; en el ejemplo, por muy poco)_
> **Limitaciones y sesgos:** _(¿en qué estaciones/grupos rinde peor? ¿qué datos no usa?)_
> **No usar para:** _(p. ej. decretar episodios de forma automática)_
> **Responsable y monitoreo:** _(quién responde; qué se vigila y cada cuánto — ver R2-09)_'''

BRIEF = '''## 7. Brief para quien decide (una plana)

> **Pregunta:** _(la del paso 1)_
>
> **Resultado (1–2 frases, con el número clave):** _(p. ej. «el modelo detecta X de cada 10 episodios con un día de aviso, casi igual que la regla simple»)_
>
> **Recomendación:** _(¿se usa?, ¿cómo?, ¿qué falta para que aporte más? p. ej. agregar meteorología)_
>
> **Límites y ética:** _(qué NO dice; a quién podría afectar un error; revisión humana)_'''

RUBRICA = '''## Rúbrica de evaluación

| Criterio | Qué se evalúa |
|---|---|
| **Framing** | La decisión pública, el usuario y el objetivo del modelo están bien planteados. |
| **Calidad del dato** | Limpieza, unidad de análisis clara y *features* razonables. |
| **Evaluación honesta** | Sin **fuga de datos**; partición adecuada (temporal si hay fechas); métrica acorde al desbalance; **comparación con una línea base**. |
| **Ficha de modelo** | Documenta datos, desempeño, límites, usos no recomendados y responsable. |
| **Reproducibilidad** | El notebook corre de principio a fin sin pasos manuales. |
| **Comunicación** | El brief es claro, honesto y accionable para alguien no técnico. |
| **Pertinencia** | (Bonus) El dataset es del propio organismo o responde una pregunta real de gestión. |

> **Entregable:** notebook reproducible + modelo entrenado + **ficha de modelo** + **brief** de una plana.'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-CAP", "Capstone — modelo predictivo de punta a punta", "R2", "Científico de Datos", "17–18",
                      ["Plantear un **problema de ML** al servicio de una decisión pública.",
                       "Elegir **features sin fuga** y una **partición temporal** honesta.",
                       "Entrenar un pipeline y **evaluarlo contra una línea base**.",
                       "Documentarlo en una **ficha de modelo** y un **brief** para quien decide."],
                      "ejecutar el ciclo de vida de un modelo de forma responsable, de los datos a la ficha y el brief.",
                      "PM2.5 diario de 14 estaciones SINCA (ejemplo) o el dataset de tu organismo.",
                      n_checks=len(EJ)),
        h.code(SETUP),
        h.md(ENMARCA),
        h.md(TABLA_MD),
        h.code(TABLA),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(MODEL_CARD))
    cells.append(h.md(BRIEF))
    cells.append(h.md(RUBRICA))
    nb.cells = cells
    return nb


PROF_PREP = f'''import os, urllib.request
import numpy as np, pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import f1_score, recall_score, precision_score

CSV = "aire_diario.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)
df = pd.read_csv(CSV, parse_dates=["fecha"])

def construir_tabla(df):
    partes = []
    for estacion, d in df.groupby("estacion"):
        d = d.set_index("fecha").sort_index().asfreq("D")
        d["estacion"] = estacion
        d["pm25_ayer"] = d["pm25"].shift(1)
        d["media_7d"] = d["pm25"].rolling(7, min_periods=5).mean()
        d["mes"] = d.index.month
        d["pm25_manana"] = d["pm25"].shift(-1)
        partes.append(d.reset_index())
    t = pd.concat(partes, ignore_index=True)
    t = t.dropna(subset=["pm25", "pm25_ayer", "media_7d", "pm25_manana"]).reset_index(drop=True)
    t["episodio_manana"] = (t["pm25_manana"] > 50).astype(int)
    return t

tabla = construir_tabla(df).sort_values("fecha").reset_index(drop=True)   # orden temporal
FEATURES = ["estacion", "pm25", "pm25_ayer", "media_7d", "mes"]
en_prueba = tabla["fecha"] >= "2025-01-01"
Xtr, ytr = tabla.loc[~en_prueba, FEATURES], tabla.loc[~en_prueba, "episodio_manana"]
Xte, yte = tabla.loc[en_prueba, FEATURES], tabla.loc[en_prueba, "episodio_manana"]

def nuevo_pipeline(**kw):
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["estacion", "mes"]),
                             ("num", StandardScaler(), ["pm25", "pm25_ayer", "media_7d"])])
    return Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000, **kw))])

print("entrenamiento:", Xtr.shape, "| prueba:", Xte.shape)'''

PROF_EJ = [
 ("## 1. Validación cruzada temporal",
  "Un solo año de prueba puede ser un año raro. `TimeSeriesSplit` hace varias particiones "
  "**respetando el orden**: cada pliegue entrena con el pasado y evalúa en el bloque siguiente. "
  "La dispersión entre pliegues dice cuánto confiar en una sola cifra.",
  "F1 en 5 pliegues temporales",
  '''scores = cross_val_score(nuevo_pipeline(), Xtr, ytr, cv=TimeSeriesSplit(n_splits=5), scoring="f1")
print("F1 por pliegue:", scores.round(3), f"| media {scores.mean():.3f} ± {scores.std():.3f}")''',
  '''# TODO: cross_val_score del pipeline sobre (Xtr, ytr) con TimeSeriesSplit(n_splits=5) y scoring="f1"
scores = ...
print("F1 por pliegue:", scores)''',
  '''assert len(scores) == 5
_s = cross_val_score(nuevo_pipeline(), Xtr, ytr, cv=TimeSeriesSplit(n_splits=5), scoring="f1")
assert np.allclose(scores, _s)''',
  'cross_val_score(nuevo_pipeline(), Xtr, ytr, cv=TimeSeriesSplit(n_splits=5), scoring="f1").'),

 ("## 2. ¿Para quién funciona peor? Recall por estación",
  "Un buen promedio puede esconder estaciones donde el modelo casi no detecta episodios. En "
  "política pública eso es **equidad territorial**: ¿qué comunas quedan peor avisadas? Calcula "
  "el *recall* por estación en 2025, solo para estaciones con al menos 10 episodios.",
  "Recall por estación",
  '''modelo = nuevo_pipeline().fit(Xtr, ytr)
prueba = tabla.loc[en_prueba].assign(pred=modelo.predict(Xte))
con_episodios = prueba.groupby("estacion").filter(lambda d: d["episodio_manana"].sum() >= 10)
recall_estacion = con_episodios.groupby("estacion").apply(
    lambda d: recall_score(d["episodio_manana"], d["pred"]), include_groups=False).sort_values()
estacion_peor = recall_estacion.idxmin()
print(recall_estacion.round(2))
print("Peor avisada:", estacion_peor)''',
  '''modelo = nuevo_pipeline().fit(Xtr, ytr)
prueba = tabla.loc[en_prueba].assign(pred=modelo.predict(Xte))
con_episodios = prueba.groupby("estacion").filter(lambda d: d["episodio_manana"].sum() >= 10)
# TODO: recall por estación en `con_episodios` (groupby + apply con recall_score), ordenado
recall_estacion = ...
estacion_peor = ...     # TODO: la de menor recall
print("Peor avisada:", estacion_peor)''',
  '''_r = {e: recall_score(d["episodio_manana"], d["pred"]) for e, d in con_episodios.groupby("estacion")}
assert len(recall_estacion) == len(_r)
assert estacion_peor == min(_r, key=_r.get)''',
  'con_episodios.groupby("estacion").apply(lambda d: recall_score(d["episodio_manana"], d["pred"]), include_groups=False); .idxmin().'),

 ("## 3. El trade-off: pesar más los episodios",
  "`class_weight=\"balanced\"` le dice al modelo que equivocarse en un episodio (la clase rara) "
  "cuesta más. Sube el *recall*… y baja la *precision* (más falsas alarmas). **¿Cuál conviene?** "
  "No es una pregunta técnica: depende de cuánto cuesta un episodio no avisado frente a una "
  "alarma innecesaria. Mide ambos modelos.",
  "Recall y precision con y sin balanceo",
  '''bal = nuevo_pipeline(class_weight="balanced").fit(Xtr, ytr)
p0, p1 = modelo.predict(Xte), bal.predict(Xte)
comparacion = pd.DataFrame({
    "recall": [recall_score(yte, p0), recall_score(yte, p1)],
    "precision": [precision_score(yte, p0), precision_score(yte, p1)],
    "alertas": [int(p0.sum()), int(p1.sum())],
}, index=["sin balanceo", "balanced"]).round(3)
print(comparacion)''',
  '''# TODO: entrena nuevo_pipeline(class_weight="balanced") con Xtr, ytr
bal = ...
# TODO: tabla con recall, precision y nº de alertas (predicciones = 1) de `modelo` y `bal` en la prueba,
#       con índice ["sin balanceo", "balanced"]
comparacion = ...
print(comparacion)''',
  '''_b = nuevo_pipeline(class_weight="balanced").fit(Xtr, ytr).predict(Xte)
assert abs(float(comparacion.loc["balanced", "recall"]) - recall_score(yte, _b)) < 1e-3
assert float(comparacion.loc["balanced", "recall"]) > float(comparacion.loc["sin balanceo", "recall"])
assert int(comparacion.loc["balanced", "alertas"]) == int(_b.sum())''',
  'bal = nuevo_pipeline(class_weight="balanced").fit(Xtr, ytr); arma un DataFrame con recall_score, precision_score y .sum() de cada predicción.'),
]

PROF_HEADER = '''# R2-CAP · Capstone — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional. Tres refuerzos para que tu capstone resista preguntas difíciles: **validación cruzada
temporal** (¿cuánto varía el desempeño?), **desempeño por estación** (¿a quién le falla?) y el
**trade-off recall/precision** (¿cuántas falsas alarmas aceptamos para no perder episodios?).
Mismo ejemplo de PM2.5; aplícalo a tus datos.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización del capstone R2.*"))
    nb.cells = cells
    return nb


README = '''# R2-CAP · Capstone — modelo predictivo de punta a punta

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-CAP-capstone-modelo/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Proyecto final de la rama R2: enmarcar la decisión → *features* **sin fuga** → partición
**temporal** → modelo → evaluación **contra una línea base** → **ficha de modelo** → **brief**.
La plantilla usa como ejemplo «¿mañana esta estación superará la norma de PM2.5?»
(`aire_diario.csv`, SINCA 2020–2025); lo ideal es usar **datos de tu propio organismo**, o el
banco del bootcamp (`aire_diario`/`aire_nuevos`, `sismos`, `matricula`, `establecimientos`,
`reclamos`, `fichas`, `comunas`, `parques`) o datos.gob.cl.

- `leccion.ipynb` — plantilla con `TODO`; se autoverifica (✅). Incluye **ficha de modelo**, **brief** y **rúbrica** (con criterio de **Pertinencia**).
- `profundiza.ipynb` — opcional 🔬: validación cruzada temporal, recall por estación, trade-off recall/precision.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
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
