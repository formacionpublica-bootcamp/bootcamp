"""build_R2-CAP.py — Capstone de la rama R2 (Científico de Datos).

Proyecto-plantilla del ciclo ML: datos→features→modelo→evaluación SIN FUGA→model card,
sobre datos del organismo (ejemplo: compras_ml.csv). Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-CAP.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-CAP-capstone-modelo")

IMPORTS = """import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, classification_report"""

ENMARCA = '''## 1. Enmarca el problema de modelado

Define en una frase la **decisión pública** que el modelo va a apoyar y por qué un modelo aporta
(¿priorizar fiscalización? ¿anticipar demanda?). Ejemplo guía: *predecir si una orden la adjudicará
un proveedor grande, para entender la concentración del mercado.*

> Usamos `compras_ml.csv` como ejemplo; reemplázalo por los datos de tu organismo.
> **Objetivo (ejemplo):** clasificar si el proveedor es **Grande**.'''

EJ = [
 ("## 2. Features sin fuga de datos",
  "El error más caro: incluir una variable que **es** la respuesta. Aquí `tamano_num` codifica el "
  "tamaño del proveedor (el target) → **queda fuera**. Selecciona features honestas.",
  "Define X, y y la partición — sin fuga",
  '''FEATURES = ["cantidad", "monto_total", "categoria", "region_comprador"]   # NO tamano_num (fuga)
y = (df["tamano_proveedor"] == "Grande").astype(int)
X = df[FEATURES]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print("train:", Xtr.shape, "| positivos:", round(100 * y.mean(), 1), "%")''',
  '''# TODO: define FEATURES sin incluir tamano_num ni tamano_proveedor
FEATURES = ...
y = (df["tamano_proveedor"] == "Grande").astype(int)
X = df[FEATURES]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print("train:", Xtr.shape, "| positivos:", round(100 * y.mean(), 1), "%")''',
  '''assert "tamano_num" not in FEATURES
assert "tamano_proveedor" not in FEATURES''',
  "Usa cantidad, monto_total, categoria y region_comprador; nunca tamano_num/tamano_proveedor.",
  None),

 ("## 3. Entrena el modelo",
  "Un pipeline con one-hot de las categóricas + un clasificador. El pipeline evita fugas en el preprocesamiento.",
  "Entrena un pipeline",
  '''pre = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), ["categoria", "region_comprador"])],
    remainder="passthrough")
modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
print("modelo entrenado:", hasattr(modelo, "predict"))''',
  '''pre = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), ["categoria", "region_comprador"])],
    remainder="passthrough")
# TODO: arma un Pipeline(pre + LogisticRegression(max_iter=1000)) y entrénalo con Xtr, ytr
modelo = ...
print("modelo entrenado:", hasattr(modelo, "predict"))''',
  '''assert hasattr(modelo, "predict")''',
  "Pipeline([('pre', pre), ('clf', LogisticRegression(max_iter=1000))]).fit(Xtr, ytr).",
  None),

 ("## 4. Evalúa honestamente",
  "Mide en el conjunto de **prueba** con una métrica adecuada al desbalance (F1).",
  "Calcula el F1 en test",
  '''pred = modelo.predict(Xte)
f1 = f1_score(yte, pred, zero_division=0)
print("F1 (test):", round(f1, 3))
print(classification_report(yte, pred, zero_division=0))''',
  '''pred = modelo.predict(Xte)
# TODO: f1_score sobre (yte, pred) con zero_division=0
f1 = ...
print("F1 (test):", round(f1, 3))''',
  '''assert 0.0 <= f1 <= 1.0''',
  "f1_score(yte, pred, zero_division=0).",
  None),
]

MODEL_CARD = '''## 5. Model card (ficha del modelo)

Completa esta ficha — acompaña al modelo cuando lo entregas:

> **Nombre / versión:** _(p.ej. clasificador-proveedor-grande v1)_
> **Objetivo y uso previsto:** _(qué decide, quién lo usa)_
> **Datos de entrenamiento:** compras públicas (ChileCompra); features: cantidad, monto, categoría, región.
> **Métrica y desempeño:** F1 = _(valor)_ en test; clase positiva ≈ _(%)_.
> **Limitaciones y sesgos:** _(grupos donde rinde peor; qué NO predice)_
> **Riesgos / uso responsable:** _(no usar para decisiones punitivas automáticas; revisión humana)_'''

RUBRICA = '''## Rúbrica de evaluación

| Criterio | Qué se evalúa |
|---|---|
| **Framing** | El problema y el uso del modelo están bien planteados. |
| **Calidad del dato** | Limpieza y features razonables. |
| **Evaluación honesta** | Sin **fuga de datos**; métrica adecuada al desbalance; mide en test. |
| **Model card** | Documenta datos, desempeño, límites y uso responsable. |
| **Reproducibilidad** | El notebook corre de principio a fin. |

> **Entregable:** notebook reproducible + modelo entrenado + **model card** + informe de validación.'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-CAP", "Capstone — modelo predictivo sobre datos de tu organismo", "B", "Data Scientist", "17–18",
                      ["Plantear un **problema de ML** público y su uso.",
                       "Elegir **features sin fuga de datos**.",
                       "Entrenar y **evaluar honestamente** un modelo.",
                       "Documentarlo en una **model card**."],
                      "ejecutar el ciclo de vida de un modelo de forma responsable, de datos a model card.",
                      "compras públicas (ejemplo) o el dataset de tu organismo.",
                      n_checks=3),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md(ENMARCA),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(MODEL_CARD))
    cells.append(h.md(RUBRICA))
    nb.cells = cells
    return nb


PROF_PREP = '''import pandas as pd, numpy as np, os, urllib.request
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
FEATURES = ["cantidad", "monto_total", "categoria", "region_comprador"]
y = (df["tamano_proveedor"] == "Grande").astype(int)
X = df[FEATURES]
pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["categoria", "region_comprador"])], remainder="passthrough")
print("Listo:", X.shape)'''

PROF_EJ = [
 ("## 1. Validación cruzada",
  "Un solo split puede engañar. Valida con 5-fold para una estimación robusta del F1.",
  "5-fold CV del pipeline",
  '''pipe = Pipeline([("pre", pre), ("clf", DecisionTreeClassifier(random_state=42, max_depth=6))])
scores = cross_val_score(pipe, X, y, cv=5, scoring="f1")
print("F1 por fold:", scores.round(3), "| media:", round(scores.mean(), 3))''',
  '''pipe = Pipeline([("pre", pre), ("clf", DecisionTreeClassifier(random_state=42, max_depth=6))])
# TODO: cross_val_score(pipe, X, y, cv=5, scoring="f1")
scores = ...
print("F1 por fold:", scores.round(3), "| media:", round(scores.mean(), 3))''',
  '''assert len(scores) == 5
assert 0.0 <= scores.mean() <= 1.0''',
  "cross_val_score(pipe, X, y, cv=5, scoring='f1')."),

 ("## 2. Importancia de variables",
  "¿Qué variables pesan más? Un árbol expone `feature_importances_`.",
  "Suma de importancias",
  '''pipe = Pipeline([("pre", pre), ("clf", DecisionTreeClassifier(random_state=42, max_depth=6))]).fit(X, y)
importancias = pipe.named_steps["clf"].feature_importances_
suma = float(importancias.sum())
print("nº features:", len(importancias), "| suma importancias:", round(suma, 3))''',
  '''pipe = Pipeline([("pre", pre), ("clf", DecisionTreeClassifier(random_state=42, max_depth=6))]).fit(X, y)
# TODO: toma feature_importances_ del clasificador y su suma
importancias = ...
suma = float(importancias.sum())
print("nº features:", len(importancias), "| suma importancias:", round(suma, 3))''',
  '''assert abs(suma - 1.0) < 1e-6''',
  "pipe.named_steps['clf'].feature_importances_ suma 1."),
]

PROF_HEADER = '''# R2-CAP · Capstone — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Opcional. Refuerza la evaluación del capstone con **validación cruzada** e **importancia de variables**.
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
    cells.append(h.md("---\n\n*Fin de la profundización del capstone R2.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R2-CAP · Capstone — modelo predictivo sobre datos de tu organismo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-CAP-capstone-modelo/leccion.ipynb)

Proyecto final de la rama R2: ciclo ML datos→features→modelo→evaluación **sin fuga**→**model card**,
sobre datos del propio organismo (ejemplo: `compras_ml.csv`).

- `leccion.ipynb` — plantilla con `TODO`; se autoverifica (✅). Incluye **model card** y **rúbrica**.
- `profundiza.ipynb` — opcional 🔬: validación cruzada, importancia de variables.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
