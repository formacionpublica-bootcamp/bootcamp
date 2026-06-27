"""build_R2-07.py — genera el módulo R2-07 (Evaluación y validación de modelos).

Módulo NUEVO de la rama R2. Sigue la convención de la casa: encabezado rico,
ejercicios con '### ✍️ Ejercicio N' en celda propia, celdas de chequeo estilo casa
(✅ / ❌+pista, sin cortar), celdas de ilustración con gráficos, y notebook de
profundización opcional. Datos reales: compras_ml.csv (ChileCompra).

Genera leccion.ipynb, solucion.ipynb, profundiza.ipynb, profundiza_solucion.ipynb, README.md
Uso:  /opt/anaconda3/bin/python tools/build_R2-07.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-07-evaluacion-y-validacion")

IMPORTS = """import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, roc_auc_score, brier_score_loss)"""

PREP = '''# Objetivo: predecir si una orden la adjudica un proveedor GRANDE.
y = (df["tamano_proveedor"] == "Grande").astype(int)
NUM = ["cantidad", "monto_total"]
CAT = ["categoria", "region_comprador"]
X = df[NUM + CAT]

pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT)],
                        remainder="passthrough")
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print("Positivos (Grande):", round(100*y.mean(), 1), "% — clase desbalanceada")'''

# ── (sec_title, sec_body, ej_title, sol, todo, assert, hint, viz_o_None) ─────
EJ = [
 ("## 1. Métricas más allá de la *accuracy*",
  "Con clases desbalanceadas la **exactitud** engaña: un modelo que siempre dice «no Grande» "
  "acierta mucho y no sirve. Por eso miramos **precision**, **recall** y **F1**.",
  "Entrena un modelo limpio y calcula las 4 métricas",
  '''modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
modelo.fit(Xtr, ytr)
pred = modelo.predict(Xte)
metricas = {
    "accuracy":  accuracy_score(yte, pred),
    "precision": precision_score(yte, pred, zero_division=0),
    "recall":    recall_score(yte, pred, zero_division=0),
    "f1":        f1_score(yte, pred, zero_division=0),
}
print(metricas)''',
  '''modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
modelo.fit(Xtr, ytr)
pred = modelo.predict(Xte)
# TODO: completa el diccionario con las 4 métricas (usa zero_division=0 donde aplique)
metricas = {
    "accuracy":  ...,
    "precision": ...,
    "recall":    ...,
    "f1":        ...,
}
print(metricas)''',
  '''assert set(metricas) == {"accuracy", "precision", "recall", "f1"}
assert all(0.0 <= v <= 1.0 for v in metricas.values())''',
  "Usa accuracy_score, precision_score, recall_score y f1_score sobre (yte, pred).",
  None),

 ("## 2. Fuga de datos (*data leakage*)",
  "Una **fuga** es usar información que no tendrías al predecir de verdad. Aquí `tamano_num` "
  "**codifica el tamaño del proveedor** → es casi la respuesta. Compara qué pasa al incluirla.",
  "Compara la accuracy CON fuga vs SIN fuga",
  '''Xtr_f = Xtr.assign(tamano_num=df.loc[Xtr.index, "tamano_num"])
Xte_f = Xte.assign(tamano_num=df.loc[Xte.index, "tamano_num"])
pre_f = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT)], remainder="passthrough")
m_fuga = Pipeline([("pre", pre_f), ("clf", DecisionTreeClassifier(random_state=42))]).fit(Xtr_f, ytr)
acc_con_fuga = accuracy_score(yte, m_fuga.predict(Xte_f))
acc_sin_fuga = accuracy_score(yte, modelo.predict(Xte))
print("CON fuga:", round(acc_con_fuga, 3), "| SIN fuga:", round(acc_sin_fuga, 3))''',
  '''Xtr_f = Xtr.assign(tamano_num=df.loc[Xtr.index, "tamano_num"])
Xte_f = Xte.assign(tamano_num=df.loc[Xte.index, "tamano_num"])
pre_f = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT)], remainder="passthrough")
m_fuga = Pipeline([("pre", pre_f), ("clf", DecisionTreeClassifier(random_state=42))]).fit(Xtr_f, ytr)
# TODO: calcula la accuracy CON fuga (sobre Xte_f) y SIN fuga (modelo sobre Xte)
acc_con_fuga = ...
acc_sin_fuga = ...
print("CON fuga:", acc_con_fuga, "| SIN fuga:", acc_sin_fuga)''',
  '''assert acc_con_fuga > 0.99, "Con la fuga la accuracy deberia ser casi perfecta"
assert acc_sin_fuga < acc_con_fuga, "El modelo honesto rinde menos que el que hace trampa"''',
  "tamano_num distingue Grande casi perfecto: acc_con_fuga ~1.0; el modelo limpio rinde menos.",
  None),

 ("## 3. Validación cruzada",
  "Un solo split puede mentir por suerte. La **validación cruzada** entrena y evalúa en varios "
  "cortes y promedia, dando una estimación más confiable.",
  "5-fold cross-validation del modelo limpio",
  '''scores = cross_val_score(modelo, X, y, cv=5, scoring="f1")
print("F1 por fold:", scores.round(3), "| media:", round(scores.mean(), 3))''',
  '''# TODO: usa cross_val_score con cv=5 y scoring="f1" sobre (modelo, X, y)
scores = ...
print("F1 por fold:", scores, "| media:", scores.mean())''',
  '''assert len(scores) == 5
assert 0.0 <= scores.mean() <= 1.0''',
  "cross_val_score(modelo, X, y, cv=5, scoring='f1') devuelve un array de 5 valores.",
  None),

 ("## 4. Calibración",
  "¿Las probabilidades del modelo son creíbles? El **Brier score** las mide (0 = perfectas). "
  "Además se pueden **ver** en una curva de calibración.",
  "Brier score de las probabilidades",
  '''proba = modelo.predict_proba(Xte)[:, 1]
brier = brier_score_loss(yte, proba)
print("Brier score:", round(brier, 4))''',
  '''# TODO: obten la probabilidad de la clase positiva y su brier_score_loss
proba = ...
brier = ...
print("Brier score:", brier)''',
  '''assert 0.0 <= brier <= 1.0''',
  "predict_proba(Xte)[:, 1] da la prob. de la clase positiva; pasala a brier_score_loss(yte, proba).",
  '''# (ilustración) Curva de calibración: ¿la probabilidad predicha coincide con la realidad?
frac_pos, mean_pred = calibration_curve(yte, proba, n_bins=10)
plt.figure(figsize=(5, 4))
plt.plot([0, 1], [0, 1], "--", color="gray", label="perfecta")
plt.plot(mean_pred, frac_pos, "o-", color="#4240e5", label="modelo")
plt.xlabel("Probabilidad predicha"); plt.ylabel("Frecuencia real observada")
plt.title("Curva de calibración"); plt.legend(); plt.show()'''),

 ("## 5. *Fairness* por grupo",
  "Un buen promedio puede esconder un mal desempeño en un grupo. Mide el **recall por región**: "
  "si el modelo detecta proveedores grandes mucho mejor en unas regiones que en otras, hay un sesgo a revisar.",
  "Recall por región y su disparidad",
  '''reg_te = df.loc[Xte.index, "region_comprador"]
recall_por_region = {}
for r in reg_te.unique():
    m = (reg_te == r).values
    if m.sum() >= 20 and yte[m].sum() > 0:      # solo grupos con datos suficientes
        recall_por_region[r] = recall_score(yte[m], pred[m], zero_division=0)
disparidad = max(recall_por_region.values()) - min(recall_por_region.values())
print("Disparidad de recall entre regiones:", round(disparidad, 3))''',
  '''reg_te = df.loc[Xte.index, "region_comprador"]
recall_por_region = {}
for r in reg_te.unique():
    m = (reg_te == r).values
    if m.sum() >= 20 and yte[m].sum() > 0:
        # TODO: guarda el recall del grupo r
        recall_por_region[r] = ...
# TODO: disparidad = recall maximo - recall minimo
disparidad = ...
print("Disparidad de recall entre regiones:", disparidad)''',
  '''assert len(recall_por_region) >= 2
assert disparidad >= 0.0''',
  "recall_score(yte[m], pred[m], zero_division=0) por grupo; disparidad = max(...) - min(...).",
  '''# (ilustración) Recall por región: ¿el modelo es parejo en todo el país?
items = sorted(recall_por_region.items(), key=lambda kv: kv[1])
plt.figure(figsize=(6, 4))
plt.barh([k for k, _ in items], [v for _, v in items], color="#4240e5")
plt.xlabel("Recall (clase Grande)"); plt.title("Fairness: recall por región")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- La **accuracy** sola engaña con clases desbalanceadas: mira precision/recall/F1.
- La **fuga de datos** infla los resultados — desconfía de un modelo "demasiado perfecto".
- **Cross-validation** > un solo split. La **calibración** dice si las probabilidades son creíbles.
- El **fairness** se mide por grupo: un buen promedio puede esconder un mal desempeño en una región.

> *Ética distribuida: evaluar bien es parte de un uso responsable de datos en el Estado.*'''


def build_leccion(con_solucion):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-07", "Evaluación y validación de modelos", "B", "Data Scientist", "12–13",
                      ["Elegir la métrica correcta (precision/recall/F1) cuando las clases están desbalanceadas.",
                       "Detectar y eliminar la **fuga de datos**.",
                       "Validar con **validación cruzada** y leer la **calibración** de las probabilidades.",
                       "Auditar el **fairness** del modelo entre grupos (regiones)."],
                      "evaluar un clasificador con rigor: métricas honestas, sin fuga, validado y auditado por fairness.",
                      "cantidad, monto y tamaño del proveedor de compras públicas de alimentos (ChileCompra).",
                      n_checks=5),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Preparación de datos"), h.code(PREP),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_solucion else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización (opcional) ────────────────────────────────────────────────
PROF_PREP = '''import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, recall_score, brier_score_loss
import os, urllib.request
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
y = (df["tamano_proveedor"] == "Grande").astype(int)
CAT = ["categoria", "region_comprador"]
X = df[["cantidad", "monto_total"] + CAT]
pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT)], remainder="passthrough")
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)
proba = modelo.predict_proba(Xte)[:, 1]
print("Listo: modelo entrenado, proba calculada.")'''

PROF_EJ = [
 ("## 1. El umbral lo eliges tú: ROC y AUC",
  "El modelo da una **probabilidad**; eres tú quien fija el **umbral** que la convierte en decisión. "
  "El **AUC** resume qué tan bien separa las clases en todos los umbrales.",
  "Calcula el AUC del modelo",
  '''auc = roc_auc_score(yte, proba)
print("AUC:", round(auc, 3))''',
  '''# TODO: roc_auc_score sobre (yte, proba)
auc = ...
print("AUC:", auc)''',
  '''assert 0.5 < auc <= 1.0, "Un modelo util separa mejor que el azar (AUC > 0.5)"''',
  "roc_auc_score(yte, proba)."),

 ("## 2. Mover el umbral para subir el recall",
  "Si te importa **no perderte** proveedores grandes (recall), baja el umbral. Tiene un costo "
  "(más falsos positivos), pero a veces el problema público lo justifica.",
  "Encuentra un umbral que logre recall ≥ 0.5",
  '''thr = 0.5
for t in np.linspace(0.5, 0.01, 50):
    if recall_score(yte, (proba >= t).astype(int)) >= 0.5:
        thr = t
        break
rec_thr = recall_score(yte, (proba >= thr).astype(int))
print("Umbral:", round(thr, 3), "| recall:", round(rec_thr, 3))''',
  '''thr = 0.5
for t in np.linspace(0.5, 0.01, 50):
    # TODO: si el recall con umbral t alcanza 0.5, fija thr=t y corta el bucle
    ...
rec_thr = recall_score(yte, (proba >= thr).astype(int))
print("Umbral:", thr, "| recall:", rec_thr)''',
  '''assert rec_thr >= 0.5, "Bajando el umbral deberias alcanzar recall >= 0.5"''',
  "(proba >= t).astype(int) son las predicciones con umbral t; mide su recall_score."),

 ("## 3. Calibrar las probabilidades",
  "`CalibratedClassifierCV` ajusta las probabilidades para que sean más fieles. Compara el Brier.",
  "Calibra el modelo y mide el Brier resultante",
  '''cal = CalibratedClassifierCV(
    Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]),
    cv=3, method="sigmoid").fit(Xtr, ytr)
brier_cal = brier_score_loss(yte, cal.predict_proba(Xte)[:, 1])
print("Brier calibrado:", round(brier_cal, 4))''',
  '''cal = CalibratedClassifierCV(
    Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]),
    cv=3, method="sigmoid").fit(Xtr, ytr)
# TODO: brier_score_loss sobre yte y la prob. positiva del modelo calibrado
brier_cal = ...
print("Brier calibrado:", brier_cal)''',
  '''assert 0.0 <= brier_cal <= 1.0''',
  "cal.predict_proba(Xte)[:, 1] son las probabilidades calibradas; pasalas a brier_score_loss."),
]

PROF_HEADER = '''# R2-07 · Evaluación y validación — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de R2-07, aquí vamos al *porqué* y a las
herramientas finas: la **curva ROC/AUC** y el **umbral** que eliges tú, y la **calibración** de
probabilidades con `CalibratedClassifierCV`. Mismos datos reales de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_solucion):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_solucion else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-07.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    readme = '''# R2-07 · Evaluación y validación de modelos

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-07-evaluacion-y-validacion/leccion.ipynb)

Métricas (precision/recall/F1), **fuga de datos**, validación cruzada, calibración y **fairness**
por grupo, sobre datos reales de compras públicas (`compras_ml.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: ROC/AUC, umbral y calibración.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
'''
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(readme)
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
