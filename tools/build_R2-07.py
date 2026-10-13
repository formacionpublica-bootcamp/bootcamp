"""build_R2-07.py — genera el módulo R2-07 (Evaluación y validación de modelos).

Rama R2 (Científico de Datos). Métricas honestas con clases desbalanceadas, fuga de
datos, validación cruzada barajada vs **validación temporal** (TimeSeriesSplit: barajar
una serie de tiempo infla el desempeño) y desempeño por grupo (equidad por estación).
Rearmado 2026 (retira compras públicas): ancla = PM2.5 diario SINCA (aire_diario.csv),
clasificando días sobre la norma de 24 h (50 µg/m³, D.S. 12/2011 MMA). Profundiza =
transferencia con matrícula MINEDUC 2025 (matricula.csv): ¿es rural el establecimiento?
— ROC/AUC, umbral, calibración y recall por región. Convención de la casa.

Genera leccion.ipynb, solucion.ipynb, profundiza.ipynb, profundiza_solucion.ipynb, README.md
Uso:  /opt/anaconda3/bin/python tools/build_R2-07.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-07-evaluacion-y-validacion")

RAW = h.REPO_RAW

IMPORTS = """import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, KFold, TimeSeriesSplit
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score"""

PREP = '''# Ordenamos y construimos variables que SÍ se conocen la víspera.
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values(["estacion", "fecha"])
g = df.groupby("estacion")["pm25"]
df["pm25_ayer"] = g.shift(1)                                                  # PM2.5 de ayer
df["pm25_prom7"] = g.transform(lambda s: s.shift(1).rolling(7, min_periods=4).mean())  # promedio de los 7 días previos
df["mes"] = df["fecha"].dt.month
df["dia"] = (df["fecha"] - df["fecha"].min()).dt.days                         # n° de día desde 2020-01-01
# ⚠️ variable con FUGA (para el ejercicio 2): promedio de ayer, HOY y MAÑANA
df["pm25_centrado"] = g.transform(lambda s: s.rolling(3, center=True, min_periods=2).mean())

d = df.dropna(subset=["pm25", "pm25_ayer", "pm25_prom7"]).copy()
d["sobre_norma"] = (d["pm25"] > 50).astype(int)        # norma de 24 h: 50 µg/m³
d = d.sort_values(["fecha", "estacion"]).reset_index(drop=True)   # orden cronológico (clave en el ej. 4)

F = ["pm25_ayer", "pm25_prom7", "mes"]
X, y = d[F], d["sobre_norma"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print("días:", len(d), f"| sobre la norma: {y.mean():.1%} — clases desbalanceadas")'''

# ── (sec_title, sec_body, ej_title, sol, todo, assert, hint, viz_o_None) ─────
EJ = [
 ("## 1. Métricas más allá de la *accuracy*",
  "Ya lo viste en R2-06: con ≈4 % de días sobre la norma, la **exactitud** engaña. Un modelo "
  "evaluado con rigor reporta las cuatro: **accuracy**, **precision** (de las alertas, cuántas "
  "eran ciertas), **recall** (de los días malos, cuántos detectó) y **F1** (el promedio armónico "
  "de precision y recall: solo es alto si **ambas** lo son).",
  "Entrena un modelo limpio y calcula las 4 métricas",
  '''modelo = LogisticRegression(max_iter=1000)
modelo.fit(Xtr, ytr)
pred = modelo.predict(Xte)
metricas = {
    "accuracy":  accuracy_score(yte, pred),
    "precision": precision_score(yte, pred, zero_division=0),
    "recall":    recall_score(yte, pred, zero_division=0),
    "f1":        f1_score(yte, pred, zero_division=0),
}
print({k: round(v, 3) for k, v in metricas.items()})''',
  '''modelo = LogisticRegression(max_iter=1000)
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
assert all(0.0 <= v <= 1.0 for v in metricas.values())
assert abs(metricas["f1"] - f1_score(yte, pred)) < 1e-9
assert metricas["accuracy"] > metricas["f1"] + 0.2, "La accuracy luce mucho mejor que el F1: ahí está el engaño"''',
  "Usa accuracy_score, precision_score, recall_score y f1_score sobre (yte, pred).",
  None),

 ("## 2. Fuga de datos (*data leakage*)",
  "Una **fuga** es usar información que **no tendrías** en el momento de predecir. La columna "
  "`pm25_centrado` parece inocente —«un promedio móvil de 3 días»— pero está **centrado**: "
  "promedia ayer, **hoy** y **mañana**. Contiene la respuesta (el PM2.5 de hoy) y hasta el futuro. "
  "La víspera, cuando la autoridad debe decidir, esa columna **no existe**.\n\n"
  "Compara el F1 del mismo modelo **con** y **sin** la columna con fuga.",
  "Compara el F1 CON fuga vs SIN fuga",
  '''Xtr_f = Xtr.assign(pm25_centrado=d.loc[Xtr.index, "pm25_centrado"])
Xte_f = Xte.assign(pm25_centrado=d.loc[Xte.index, "pm25_centrado"])
m_fuga = LogisticRegression(max_iter=1000).fit(Xtr_f, ytr)
f1_con_fuga = f1_score(yte, m_fuga.predict(Xte_f))
f1_sin_fuga = f1_score(yte, pred)
print(f"F1 CON fuga: {f1_con_fuga:.3f} | F1 SIN fuga: {f1_sin_fuga:.3f}")''',
  '''Xtr_f = Xtr.assign(pm25_centrado=d.loc[Xtr.index, "pm25_centrado"])
Xte_f = Xte.assign(pm25_centrado=d.loc[Xte.index, "pm25_centrado"])
m_fuga = LogisticRegression(max_iter=1000).fit(Xtr_f, ytr)
# TODO: F1 del modelo con fuga (predice sobre Xte_f) y del modelo limpio (pred del ej. 1)
f1_con_fuga = ...
f1_sin_fuga = ...
print("CON fuga:", f1_con_fuga, "| SIN fuga:", f1_sin_fuga)''',
  '''assert abs(f1_sin_fuga - f1_score(yte, pred)) < 1e-9
assert f1_con_fuga > f1_sin_fuga + 0.15, "Con la fuga, el F1 debería dispararse"''',
  "f1_score(yte, m_fuga.predict(Xte_f)) para el con fuga; f1_score(yte, pred) para el limpio.",
  None),

 ("## 3. Validación cruzada (barajada)",
  "Un solo corte entrenamiento/prueba puede salir bueno o malo por suerte. La **validación "
  "cruzada** entrena y evalúa en *k* cortes y promedia. La versión de siempre, `KFold` con "
  "`shuffle=True`, **baraja** las filas antes de cortar.\n\n"
  "Para este ejercicio usamos un modelo más flexible —un **bosque aleatorio** (R2-05)— y le "
  "agregamos una variable tentadora: `dia`, el número de día desde el 1-ene-2020.",
  "5-fold con KFold barajado",
  '''F_dia = F + ["dia"]
bosque = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
cv_barajada = KFold(n_splits=5, shuffle=True, random_state=42)
scores_barajada = cross_val_score(bosque, d[F_dia], y, cv=cv_barajada, scoring="f1")
f1_barajada = scores_barajada.mean()
print("F1 por fold:", scores_barajada.round(3), f"| media: {f1_barajada:.3f}")''',
  '''F_dia = F + ["dia"]
bosque = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
cv_barajada = KFold(n_splits=5, shuffle=True, random_state=42)
# TODO: cross_val_score de bosque sobre (d[F_dia], y) con cv=cv_barajada y scoring="f1"
scores_barajada = ...
f1_barajada = ...
print("F1 por fold:", scores_barajada, "| media:", f1_barajada)''',
  '''assert len(scores_barajada) == 5
assert abs(f1_barajada - np.mean(scores_barajada)) < 1e-9
assert 0.0 <= f1_barajada <= 1.0''',
  "cross_val_score(bosque, d[F_dia], y, cv=cv_barajada, scoring='f1') y luego .mean().",
  None),

 ("## 4. Validación **temporal**: no se puede barajar el tiempo",
  "Al barajar, el modelo entrena con el 14 de julio y el 16 de julio… y se evalúa en el 15. Con "
  "`dia` puede «recordar» el episodio de esa semana: está **mirando el futuro**. En la vida real "
  "el modelo se entrena con el pasado y se usa en días que **todavía no ocurren**.\n\n"
  "`TimeSeriesSplit` respeta el orden: cada fold entrena con lo anterior y evalúa con lo "
  "**siguiente**. (Por eso ordenamos `d` por fecha en la preparación.)",
  "Compara la validación barajada con la temporal",
  '''cv_temporal = TimeSeriesSplit(n_splits=5)
scores_temporal = cross_val_score(bosque, d[F_dia], y, cv=cv_temporal, scoring="f1")
f1_temporal = scores_temporal.mean()
print(f"F1 barajada: {f1_barajada:.3f} | F1 temporal: {f1_temporal:.3f}")''',
  '''cv_temporal = TimeSeriesSplit(n_splits=5)
# TODO: el mismo cross_val_score, ahora con cv=cv_temporal
scores_temporal = ...
f1_temporal = ...
print("F1 barajada:", f1_barajada, "| F1 temporal:", f1_temporal)''',
  '''assert len(scores_temporal) == 5
assert f1_temporal < f1_barajada - 0.1, "Barajar debería inflar el F1 respecto de la validación temporal"''',
  "cross_val_score(bosque, d[F_dia], y, cv=TimeSeriesSplit(n_splits=5), scoring='f1').mean().",
  '''# (ilustración) ¿Barajar SIEMPRE infla? Con variables honestas (sin `dia`) y un modelo simple, casi no.
log = LogisticRegression(max_iter=1000)
b = cross_val_score(log, d[F], y, cv=cv_barajada, scoring="f1").mean()
t = cross_val_score(log, d[F], y, cv=cv_temporal, scoring="f1").mean()
fig, ax = plt.subplots(figsize=(7, 3.5))
x = np.arange(2)
ax.bar(x - 0.18, [f1_barajada, b], 0.36, label="KFold barajado", color="#ff6b35")
ax.bar(x + 0.18, [f1_temporal, t], 0.36, label="TimeSeriesSplit", color="#4240e5")
ax.set_xticks(x, ["Bosque + `dia`", "Logística sin `dia`"])
ax.set_ylim(0, 1); ax.set_ylabel("F1 promedio (5 folds)")
ax.set_title("Barajar una serie de tiempo puede inflar el desempeño")
ax.legend(); plt.tight_layout(); plt.show()
print(f"Logística sin dia → barajada {b:.3f} | temporal {t:.3f}")'''),

 ("## 5. Desempeño por grupo: ¿el modelo sirve igual en todas las estaciones?",
  "Un buen promedio puede esconder un mal desempeño en un grupo. Mide el **recall por "
  "estación** (solo estaciones con al menos 10 días sobre la norma en la prueba): si el modelo "
  "detecta los episodios mucho mejor en unas ciudades que en otras, la población de las demás "
  "queda **menos protegida**. Eso es un problema de **equidad**, no solo técnico.",
  "Recall por estación y su disparidad",
  '''est_te = d.loc[Xte.index, "estacion"]
recall_por_estacion = {}
for e in est_te.unique():
    m = (est_te == e).values
    if yte[m].sum() >= 10:                     # solo grupos con datos suficientes
        recall_por_estacion[e] = recall_score(yte[m], pred[m], zero_division=0)
disparidad = max(recall_por_estacion.values()) - min(recall_por_estacion.values())
print({k: round(v, 2) for k, v in sorted(recall_por_estacion.items(), key=lambda kv: kv[1])})
print(f"Disparidad de recall entre estaciones: {disparidad:.2f}")''',
  '''est_te = d.loc[Xte.index, "estacion"]
recall_por_estacion = {}
for e in est_te.unique():
    m = (est_te == e).values
    if yte[m].sum() >= 10:
        # TODO: guarda el recall de la estación e (yte[m] vs pred[m], zero_division=0)
        recall_por_estacion[e] = ...
# TODO: disparidad = recall máximo - recall mínimo
disparidad = ...
print("Disparidad de recall entre estaciones:", disparidad)''',
  '''assert len(recall_por_estacion) >= 4
assert all(0.0 <= v <= 1.0 for v in recall_por_estacion.values())
assert abs(disparidad - (max(recall_por_estacion.values()) - min(recall_por_estacion.values()))) < 1e-9
assert disparidad > 0.1, "Hay diferencias reales entre estaciones"''',
  "recall_score(yte[m], pred[m], zero_division=0) por estación; disparidad = max(...) - min(...).",
  '''# (ilustración) Recall por estación: ¿el modelo protege parejo?
items = sorted(recall_por_estacion.items(), key=lambda kv: kv[1])
plt.figure(figsize=(6.5, 3.5))
plt.barh([k for k, _ in items], [v for _, v in items], color="#4240e5")
plt.xlim(0, 1); plt.xlabel("Recall (días sobre la norma detectados)")
plt.title("Desempeño por estación"); plt.tight_layout(); plt.show()'''),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Un proveedor te ofrece un modelo de alerta de episodios con **«F1 = 0,9, validado con validación
cruzada»**. Con lo que aprendiste hoy, escribe las **tres preguntas** que le harías antes de
recomendar que el servicio lo adopte. (Pista: ¿qué variables usa y cuándo se conocen? ¿barajó las fechas?
¿cómo le va en *cada* ciudad?)'''

CIERRE = '''## Errores típicos

- **Reportar solo la accuracy** con clases desbalanceadas.
- **Variables que «miran el futuro»**: promedios centrados, totales del mes, datos que se registran después del hecho.
- **Barajar una serie de tiempo** en la validación cruzada: usa `TimeSeriesSplit` (o un corte por fecha).
- **Quedarse con el promedio** sin mirar el desempeño por grupo.

## Cierre

- La **accuracy** sola engaña con clases desbalanceadas: mira precision/recall/F1.
- La **fuga de datos** infla los resultados — desconfía de un modelo «demasiado bueno».
- **Validación cruzada** > un solo split; pero con datos en el tiempo, **validación temporal**.
- El desempeño se audita **por grupo**: un buen promedio puede dejar a una ciudad menos protegida.

> *En R2-08 empaquetarás todo esto —preprocesamiento + modelo— en un **pipeline** reproducible que
> se puede guardar y reutilizar.*

---
*Fuente de datos: Sistema de Información Nacional de Calidad del Aire (SINCA), Ministerio del Medio Ambiente.*'''


def build_leccion(con_solucion):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-07", "Evaluación y validación de modelos", "R2", "Científico de Datos", "12–13",
                      ["Elegir la métrica correcta (precision/recall/F1) cuando las clases están desbalanceadas.",
                       "Detectar y eliminar la **fuga de datos**.",
                       "Distinguir la **validación cruzada barajada** de la **validación temporal** (y por qué importa).",
                       "Auditar el **desempeño por grupo** (estaciones) como una cuestión de equidad."],
                      "evaluar un clasificador con rigor: métricas honestas, sin fuga, con validación "
                      "temporal y auditado por grupo.",
                      "PM2.5 diario 2020–2025 de 14 estaciones SINCA (Ministerio del Medio Ambiente).",
                      n_checks=5),
        h.setup_cell("aire_diario.csv", IMPORTS),
        h.md("### Preparación de datos\n\nObjetivo: anticipar si un día supera la **norma de 24 h "
             "de PM2.5 (50 µg/m³)** con lo que se sabe la víspera."),
        h.code(PREP),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_solucion else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización (opcional): transferencia con matrícula MINEDUC ───────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, roc_curve, recall_score, brier_score_loss

CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/matricula.csv", CSV)
mat = pd.read_csv(CSV)

# Objetivo: ¿el establecimiento es RURAL? (1 = rural) a partir de su tamaño, niveles y dependencia
NUM = ["mat_total", "cursos", "mat_parvularia", "mat_basica", "mat_media_hc", "mat_media_tp", "mat_extranjeros"]
CAT = ["dependencia", "region"]
y = mat["rural"]
X = mat[NUM + CAT]
pre = ColumnTransformer([("num", StandardScaler(), NUM),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), CAT)])
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=2000))]).fit(Xtr, ytr)
proba = modelo.predict_proba(Xte)[:, 1]
print(f"Establecimientos: {{len(mat)}} | rurales: {{y.mean():.1%}} | modelo entrenado.")'''

PROF_EJ = [
 ("## 1. El umbral lo eliges tú: ROC y AUC",
  "Dominio nuevo: los **10.945 establecimientos** con matrícula 2025 (MINEDUC). ¿Se puede "
  "reconocer un establecimiento **rural** solo por su tamaño, sus niveles y su dependencia? "
  "(Sirve, por ejemplo, para detectar registros con la ruralidad mal codificada.)\n\n"
  "El modelo entrega una **probabilidad**; tú fijas el **umbral** que la convierte en decisión. "
  "El **AUC** resume qué tan bien separa las clases considerando **todos** los umbrales "
  "(0,5 = azar, 1 = perfecto).",
  "Calcula el AUC del modelo",
  '''auc = roc_auc_score(yte, proba)
print(f"AUC: {auc:.3f}")
fpr, tpr, _ = roc_curve(yte, proba)
plt.figure(figsize=(4.5, 4))
plt.plot(fpr, tpr, color="#4240e5", label=f"modelo (AUC={auc:.2f})")
plt.plot([0, 1], [0, 1], "--", color="gray", label="azar")
plt.xlabel("Tasa de falsos positivos"); plt.ylabel("Recall (tasa de verdaderos positivos)")
plt.title("Curva ROC — ¿rural?"); plt.legend(); plt.show()''',
  '''# TODO: roc_auc_score sobre (yte, proba)
auc = ...
print("AUC:", auc)''',
  '''assert 0.85 < auc <= 1.0, "El modelo debería separar muy bien (AUC > 0,85)"''',
  "roc_auc_score(yte, proba)."),

 ("## 2. Mover el umbral para subir el recall",
  "Si el objetivo es **no perderse** establecimientos rurales (por ejemplo, para focalizar un "
  "programa de transporte escolar), baja el umbral hasta lograr el recall que la política exige. "
  "El costo: más falsos positivos que revisar a mano.",
  "Encuentra el mayor umbral que logre recall ≥ 0,9",
  '''thr = 0.5
for t in np.linspace(0.5, 0.01, 50):
    if recall_score(yte, (proba >= t).astype(int)) >= 0.9:
        thr = t
        break
rec_thr = recall_score(yte, (proba >= thr).astype(int))
print(f"Recall con umbral 0,5: {recall_score(yte, (proba >= 0.5).astype(int)):.3f}")
print(f"Umbral: {thr:.3f} | recall: {rec_thr:.3f}")''',
  '''thr = 0.5
for t in np.linspace(0.5, 0.01, 50):
    # TODO: si el recall con umbral t alcanza 0.9, fija thr = t y corta el bucle (break)
    ...
rec_thr = recall_score(yte, (proba >= thr).astype(int))
print("Umbral:", thr, "| recall:", rec_thr)''',
  '''assert rec_thr >= 0.9, "Bajando el umbral deberías alcanzar recall >= 0,9"
assert thr < 0.5''',
  "(proba >= t).astype(int) son las predicciones con umbral t; mide su recall_score y corta con break."),

 ("## 3. ¿Son creíbles las probabilidades? Calibración",
  "Si el modelo dice «70 % de probabilidad de ser rural», ¿de cada 10 casos así, ~7 lo son? "
  "El **Brier score** mide el error de las probabilidades (0 = perfectas). "
  "`CalibratedClassifierCV` las reajusta con validación cruzada.",
  "Calibra el modelo y compara el Brier",
  '''brier_base = brier_score_loss(yte, proba)
cal = CalibratedClassifierCV(
    Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=2000))]),
    cv=3, method="isotonic").fit(Xtr, ytr)
brier_cal = brier_score_loss(yte, cal.predict_proba(Xte)[:, 1])
print(f"Brier sin calibrar: {brier_base:.4f} | calibrado: {brier_cal:.4f}")''',
  '''brier_base = brier_score_loss(yte, proba)
cal = CalibratedClassifierCV(
    Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=2000))]),
    cv=3, method="isotonic").fit(Xtr, ytr)
# TODO: brier_score_loss sobre yte y la probabilidad positiva del modelo calibrado
brier_cal = ...
print("Brier sin calibrar:", brier_base, "| calibrado:", brier_cal)''',
  '''assert 0.0 <= brier_cal <= 0.25
assert brier_cal <= brier_base + 0.005, "Calibrar no debería empeorar las probabilidades"''',
  "cal.predict_proba(Xte)[:, 1] son las probabilidades calibradas; pásalas a brier_score_loss(yte, ...)."),

 ("## 4. Recall por región: ¿a quién no ve el modelo?",
  "El mismo chequeo de equidad de la lección, en otro dominio: ¿el modelo reconoce igual de bien "
  "a los establecimientos rurales de todas las regiones?",
  "Recall rural por región y la región peor atendida",
  '''pred = (proba >= 0.5).astype(int)
reg_te = Xte["region"]
recall_region = {}
for r in reg_te.unique():
    m = (reg_te == r).values
    if yte[m].sum() >= 10:
        recall_region[r] = recall_score(yte[m], pred[m])
peor_region = min(recall_region, key=recall_region.get)
print({k: round(v, 2) for k, v in sorted(recall_region.items(), key=lambda kv: kv[1])})
print("Región con menor recall:", peor_region)''',
  '''pred = (proba >= 0.5).astype(int)
reg_te = Xte["region"]
recall_region = {}
for r in reg_te.unique():
    m = (reg_te == r).values
    if yte[m].sum() >= 10:
        # TODO: recall de la región r
        recall_region[r] = ...
# TODO: la región con el menor recall (pista: min con key=recall_region.get)
peor_region = ...
print("Región con menor recall:", peor_region)''',
  '''assert len(recall_region) >= 10
assert recall_region[peor_region] == min(recall_region.values())
assert max(recall_region.values()) - recall_region[peor_region] > 0.3''',
  "recall_score(yte[m], pred[m]) por región; peor_region = min(recall_region, key=recall_region.get)."),
]

PROF_HEADER = '''# R2-07 · Evaluación y validación — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: las herramientas finas de evaluación sobre otro dato del Estado —
la **matrícula escolar 2025** (MINEDUC). Un clasificador que reconoce establecimientos **rurales**:
la **curva ROC/AUC**, el **umbral** que eliges tú según la política, la **calibración** de las
probabilidades y el **recall por región**.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_solucion):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_solucion else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-07.*\n\n"
                      "*Fuente: MINEDUC, Resumen de matrícula por establecimiento 2025 (datos abiertos).*"))
    nb.cells = cells
    return nb


README = '''# R2-07 · Evaluación y validación de modelos

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-07-evaluacion-y-validacion/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Evaluar un modelo con rigor sobre la **calidad del aire** (PM2.5 diario 2020–2025 de 14
estaciones SINCA, `aire_diario.csv`): ¿se supera mañana la norma de 50 µg/m³? Métricas
(precision/recall/F1) con clases desbalanceadas, **fuga de datos** (un promedio «centrado» que
mira el futuro), validación cruzada **barajada vs temporal** (`TimeSeriesSplit`: barajar una serie
de tiempo infla el desempeño) y **desempeño por estación**. La profundización transfiere a la
matrícula 2025 (`matricula.csv`, MINEDUC): ROC/AUC, umbral, calibración y recall por región.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: ROC/AUC, umbral, calibración y equidad por región.
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
