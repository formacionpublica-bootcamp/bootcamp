# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B4 (clasificación y clustering):
B4/profundiza.ipynb (estudiante) + B4/profundiza_solucion.ipynb (resuelto).

Más teórico que la lección: el *porqué*. Cubre la TRAMPA DE LA EXACTITUD con clases
desbalanceadas, precisión/recall/F1, matriz de confusión, ROC/AUC y el umbral, y los
supuestos de K-Means (escalado, elección de k, clusters como construcción)."""
import json, os

BASE = "B4-clasificacion-y-clustering"

TITULO = """# B4 · Clasificación y clustering — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B4 —donde *entrenaste* un clasificador y
agrupaste compras con K-Means— aquí vamos al *porqué*: por qué la **exactitud (*accuracy*) miente**
cuando las clases están desbalanceadas (un modelo "todo negativo" puede acertar el 90% y ser **inútil**),
qué miden de verdad la **precisión**, el **recall** y el **F1**, cómo leer la **matriz de confusión**, qué
es el **umbral** y la curva **ROC/AUC**, y qué **supuestos esconde K-Means** (por qué necesita **escalado**,
por qué asume grupos "esféricos", cómo elegir **k** y por qué los clusters **no son la verdad**).

Menos botones de scikit-learn, más **criterio de evaluación**. Los ejercicios del final son más
conceptuales: calculas un número y eliges la **interpretación correcta**.

> Requisito: haber hecho `leccion.ipynb` de B4. Mismo dataset: `compras_ml.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("compras_ml.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B4-clasificacion-y-clustering/compras_ml.csv"
        urllib.request.urlretrieve(url, "compras_ml.csv")
    except Exception:
        print("Si estás en Colab, sube compras_ml.csv manualmente.")

df = pd.read_csv("compras_ml.csv")

# Construimos una etiqueta BINARIA DESBALANCEADA para todo el cuaderno:
# "compra de alto monto" = top ~10% del monto_total (el caso 'raro' que querríamos detectar).
UMBRAL = df["monto_total"].quantile(0.90)
df["alto_monto"] = (df["monto_total"] >= UMBRAL).astype(int)

prevalencia = df["alto_monto"].mean()
print(f"{len(df)} compras cargadas.")
print(f"Etiqueta 'alto_monto' (top 10% de monto, umbral = ${UMBRAL:,.0f}):")
print(f"  positivos (alto monto): {int(df['alto_monto'].sum())}  ->  {prevalencia:.1%} del total")
print(f"  negativos (resto):      {int((df['alto_monto']==0).sum())}")
print("Clases MUY desbalanceadas: solo 1 de cada 10 compras es 'alto monto'. Eso lo cambia todo.")"""

S1 = """## 1. La trampa de la exactitud: un modelo "todo negativo" que acierta el 90%

En la lección mediste el modelo con la **exactitud** (*accuracy*): el porcentaje de aciertos. Es la
métrica más intuitiva… y la más **engañosa** cuando una clase es rara.

Nuestra etiqueta `alto_monto` está **desbalanceada**: solo el ~10% de las compras son de alto monto.
Imagina el clasificador más tonto posible: **uno que dice "NO es alto monto" para absolutamente todo**.
Nunca detecta una sola compra grande… pero como el 90% de las compras *efectivamente* no lo son, **acierta
el 90% de las veces**. Una exactitud del 90% que, para el problema que importa (encontrar las compras
grandes), es **completamente inútil**.

> 🧠 **Analogía pública.** Un detector de fraude que dice "no hay fraude" en todos los casos tendrá
> "exactitud" altísima (el fraude es raro) y no servirá para nada. La pregunta no es *"¿cuántas veces
> acierta?"*, sino *"¿encuentra lo que estamos buscando?"*.

Comparemos ese modelo-trampa contra la realidad de la etiqueta."""

S1_CODE = """from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split

# Features honestas: NO usamos monto_total (sería hacer trampa: la etiqueta SALE del monto).
# Usamos 'cantidad' y 'tamano_num' para deducir si la compra es de alto monto.
X = df[["cantidad", "tamano_num"]]
y = df["alto_monto"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# El "modelo trampa": predice SIEMPRE la clase mayoritaria (0 = no alto monto)
trampa = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
pred_trampa = trampa.predict(X_te)

acc_trampa = accuracy_score(y_te, pred_trampa)
rec_trampa = recall_score(y_te, pred_trampa, zero_division=0)
print(f"Modelo 'todo negativo':")
print(f"  Exactitud (accuracy): {acc_trampa:.1%}   <- ¡parece buenísimo!")
print(f"  Recall de 'alto monto': {rec_trampa:.1%}   <- detecta CERO compras grandes")
print("\\nMisma exactitud del 90%, utilidad nula. La exactitud sola te mintió.")"""

S2 = """## 2. Precisión, recall y F1: las preguntas que la exactitud no responde

Para no caer en la trampa, separamos el acierto en **dos preguntas distintas** sobre la clase que nos
importa (las compras de alto monto):

- **Recall** (sensibilidad) — *"de todas las compras grandes que existen, ¿cuántas pillé?"*
  `recall = verdaderos positivos / (verdaderos positivos + FALSOS NEGATIVOS)`.
  Un recall bajo significa que se te **escapan** casos reales (compras grandes sin detectar).
- **Precisión** — *"de todas las que marqué como grandes, ¿cuántas lo eran de verdad?"*
  `precisión = verdaderos positivos / (verdaderos positivos + FALSOS POSITIVOS)`.
  Una precisión baja significa que das **muchas falsas alarmas**.

Hay una **tensión** entre ambas: si marcas todo como "grande" tienes recall perfecto pero precisión
pésima; si marcas casi nada, lo poco que marcas acierta (precisión alta) pero se te escapa casi todo
(recall bajo). El **F1** las resume en un solo número (su media armónica), que solo es alto cuando
**ambas** lo son.

> 🧠 **En el Estado importa cuál priorizas.** En un tamizaje de salud prefieres **recall** alto (mejor
> una falsa alarma que dejar pasar un caso). En una acusación de fraude prefieres **precisión** alta
> (no acusar a un inocente). La métrica correcta **depende del costo de cada error**."""

S2_CODE = """from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_score, f1_score

# Un clasificador REAL (un árbol) sobre las mismas features honestas
clf = DecisionTreeClassifier(max_depth=4, random_state=42).fit(X_tr, y_tr)
pred = clf.predict(X_te)

acc  = accuracy_score(y_te, pred)
prec = precision_score(y_te, pred, zero_division=0)
rec  = recall_score(y_te, pred, zero_division=0)
f1   = f1_score(y_te, pred, zero_division=0)

print(f"Clasificador real (árbol) sobre 'alto monto':")
print(f"  Exactitud : {acc:.1%}")
print(f"  Precisión : {prec:.1%}   (de las que marcó grandes, cuántas lo eran)")
print(f"  Recall    : {rec:.1%}   (de las grandes reales, cuántas pilló)")
print(f"  F1        : {f1:.1%}")
print(f"\\nFíjate: exactitud {acc:.1%}, pero el RECALL es {rec:.1%}: se le escapa el {1-rec:.0%} de las")
print("compras grandes. La exactitud sola jamás te habría mostrado eso.")"""

S3 = """## 3. La matriz de confusión: ver *en qué* se equivoca

La matriz de confusión abre el acierto en sus cuatro piezas y es la base de todas las métricas
anteriores. Para un problema binario (positivo = "alto monto"):

|                       | Predijo NEGATIVO        | Predijo POSITIVO        |
|-----------------------|-------------------------|-------------------------|
| **Real NEGATIVO**     | VN (verdadero negativo) | FP (falso positivo)     |
| **Real POSITIVO**     | FN (falso negativo)     | VP (verdadero positivo) |

Los dos errores **no cuestan lo mismo**:

- **Falso negativo (FN):** una compra grande que el modelo dejó pasar como normal. En auditoría, **el
  caso que se te escapó**.
- **Falso positivo (FP):** una compra normal que el modelo marcó como grande. Una **falsa alarma** que
  gasta tiempo de revisión.

La matriz te muestra **cuántos de cada uno** cometes, no solo "cuánto acierta". Veámosla en números."""

S3_CODE = """from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_te, pred, labels=[0, 1])
vn, fp, fn, vp = cm.ravel()
print("Matriz de confusión (clase positiva = 'alto monto'):")
print(f"  Verdaderos negativos (VN): {vn:4d}   |  Falsos positivos (FP): {fp:4d}")
print(f"  Falsos  negativos   (FN): {fn:4d}   |  Verdaderos positivos (VP): {vp:4d}")
print(f"\\nLas {fn} compras grandes que cayeron en FN son las que se te ESCAPARON:")
print("ese es justo el error que la exactitud del modelo escondía.")

fig, ax = plt.subplots(figsize=(5, 4))
ConfusionMatrixDisplay(cm, display_labels=["normal", "alto monto"]).plot(ax=ax, cmap="Blues", colorbar=False)
ax.set_title("Matriz de confusión — detectar compras de alto monto")
plt.tight_layout(); plt.show()"""

S4 = """## 4. El umbral y la curva ROC/AUC: la decisión que tomas tú, no el modelo

Un clasificador no escupe "sí/no" directamente: por dentro estima una **probabilidad** (p. ej. "esta
compra tiene 0,73 de ser de alto monto"). El "sí/no" aparece al comparar esa probabilidad con un
**umbral**, que **por defecto es 0,5** — pero ese 0,5 **lo eliges tú**, no es sagrado:

- **Bajar el umbral** (p. ej. a 0,3): marcas más compras como "grandes" → **sube el recall** (pillas más)
  pero **baja la precisión** (más falsas alarmas).
- **Subir el umbral** (p. ej. a 0,7): marcas menos → **sube la precisión** pero **baja el recall**.

La **curva ROC** recorre *todos* los umbrales posibles y dibuja, para cada uno, cuántos positivos pillas
frente a cuántas falsas alarmas das. El **AUC** (área bajo esa curva) resume en un número la capacidad
del modelo de **separar** las dos clases, **sin depender de un umbral**:

- **AUC = 0,5** → el modelo no distingue nada (como tirar una moneda).
- **AUC = 1,0** → separación perfecta.

Por eso el AUC es una métrica honesta para datos desbalanceados: no se deja engañar por la clase
mayoritaria como sí lo hace la exactitud."""

S4_CODE = """from sklearn.metrics import roc_curve, roc_auc_score

# Probabilidades de la clase positiva (no el sí/no)
proba = clf.predict_proba(X_te)[:, 1]
auc = roc_auc_score(y_te, proba)
fpr, tpr, _ = roc_curve(y_te, proba)

print(f"AUC del clasificador: {auc:.3f}")
print("(0.5 = moneda al aire; 1.0 = separación perfecta)")

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.plot(fpr, tpr, color="#0a7e7e", lw=2, label=f"Clasificador (AUC = {auc:.2f})")
ax.plot([0, 1], [0, 1], "--", color="gray", label="Moneda al aire (AUC = 0.50)")
ax.set_xlabel("Tasa de falsas alarmas (FPR)")
ax.set_ylabel("Recall / Tasa de detección (TPR)")
ax.set_title("Curva ROC — separar 'alto monto' del resto")
ax.legend(loc="lower right"); plt.tight_layout(); plt.show()"""

S5 = """## 5. K-Means tiene letra chica: por qué SIN escalar el monto manda solo

K-Means agrupa por **distancia**: pone cada compra cerca del centro de grupo más próximo. Pero la
distancia se calcula sumando las diferencias de **todas** las columnas, y aquí está la trampa: nuestras
columnas viven en **escalas distintísimas**. `cantidad` va de 0 a ~500; `monto_total` llega a **millones**.

Cuando mezclas escalas tan dispares, la columna de números grandes **domina** la distancia: una diferencia
de \\$1.000.000 en monto aplasta cualquier diferencia en cantidad. Resultado: **sin escalar, K-Means agrupa
principalmente por monto, aplastando la señal de la cantidad** (los grupos quedan definidos casi por completo
por el monto). Por eso la lección insistió en `StandardScaler`
(deja todas las columnas con media 0 y desviación 1, así pesan **parejo**).

Otros supuestos que K-Means da por sentado (y conviene tener presentes):
- Asume grupos **"esféricos"** y de **tamaño parecido**; con formas alargadas o densidades muy distintas
  los parte mal.
- **k lo eliges tú**: el algoritmo no descubre "cuántos grupos hay de verdad" (sección 6).

Veamos el efecto del escalado comparando los centros de los grupos con y sin escalar."""

S5_CODE = """from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

Xc = df[["cantidad", "monto_total"]].copy()

# (a) SIN escalar
km_raw = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Xc)
df["cluster_raw"] = km_raw.labels_

# (b) CON escalado (lo correcto)
Xs = StandardScaler().fit_transform(Xc)
km_esc = KMeans(n_clusters=3, random_state=42, n_init=10).fit(Xs)
df["cluster_esc"] = km_esc.labels_

print("Centros de cada grupo SIN escalar (mira cómo cambia el monto entre grupos, no la cantidad):")
print(df.groupby("cluster_raw")[["cantidad", "monto_total"]].mean().round(0).to_string())
print("\\nCON escalado (los grupos ya distinguen también por cantidad):")
print(df.groupby("cluster_esc")[["cantidad", "monto_total"]].mean().round(0).to_string())

fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharex=True, sharey=True)
axes[0].scatter(df["cantidad"], df["monto_total"], c=df["cluster_raw"], cmap="viridis", s=10, alpha=0.4)
axes[0].set_title("SIN escalar: el monto manda solo")
axes[1].scatter(df["cantidad"], df["monto_total"], c=df["cluster_esc"], cmap="viridis", s=10, alpha=0.4)
axes[1].set_title("CON StandardScaler: grupos más sensatos")
for a in axes:
    a.set_xlabel("Cantidad"); a.set_ylabel("Monto total (CLP)")
plt.tight_layout(); plt.show()"""

S6 = """## 6. ¿Cuántos grupos? El codo, la silueta, y por qué los clusters NO son "la verdad"

K-Means te obliga a elegir **k** (cuántos grupos). ¿Cómo escoger sin que sea pura intuición? Dos guías:

- **Codo (*elbow*):** entrenas con varios k y mides la **inercia** (qué tan apretados quedan los grupos:
  la suma de distancias de cada punto a su centro). La inercia **siempre baja** al subir k (con k = n° de
  filas sería 0). Se busca el "**codo**": el punto donde añadir otro grupo ya **casi no mejora**.
- **Silueta:** para cada punto mide qué tan bien encaja en su grupo frente al grupo vecino. Va de **−1 a 1**
  (más alto = mejor separación). Se prefiere el k con **silueta más alta**.

Pero la idea más importante de toda la sección es esta: **los clusters no son una verdad que estaba ahí
esperando ser descubierta — son una construcción**. Cambias el k, las features o el escalado y obtienes
**grupos distintos**, todos igual de "válidos" matemáticamente. K-Means **siempre** te entrega grupos,
incluso en datos sin ninguna estructura real.

> 🧠 **Cuidado en lo público.** "El algoritmo encontró 3 perfiles de beneficiarios" no es un hallazgo
> objetivo: es el resultado de **tus** decisiones (k, variables, escala). Los clusters son una **hipótesis
> de trabajo** para explorar, no una etiqueta oficial sobre las personas."""

S6_CODE = """from sklearn.metrics import silhouette_score

# Submuestra fija (silhouette es caro) para reproducibilidad
rng = np.random.default_rng(42)
idx = rng.choice(len(Xs), size=2000, replace=False)

inercias, siluetas, ks = [], [], range(2, 7)
for k in ks:
    kmk = KMeans(n_clusters=k, random_state=42, n_init=10).fit(Xs)
    inercias.append(kmk.inertia_)
    siluetas.append(silhouette_score(Xs[idx], kmk.labels_[idx]))

print("k  | inercia (baja siempre) | silueta (más alta = mejor)")
for k, ine, sil in zip(ks, inercias, siluetas):
    print(f"{k}  | {ine:14,.0f}       | {sil:.3f}")

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].plot(list(ks), inercias, "o-", color="#0a7e7e"); axes[0].set_title("Codo: inercia vs k")
axes[0].set_xlabel("k"); axes[0].set_ylabel("Inercia")
axes[1].plot(list(ks), siluetas, "o-", color="crimson"); axes[1].set_title("Silueta vs k")
axes[1].set_xlabel("k"); axes[1].set_ylabel("Silueta")
plt.tight_layout(); plt.show()
print("\\nNo hay un 'k verdadero': estas curvas SUGIEREN, no dictan. El criterio del analista decide.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Reportar solo la exactitud con clases desbalanceadas.** Un modelo "todo negativo" puede dar 90% y ser inútil. Mira **recall**, **precisión** y la **matriz de confusión**.
- **Olvidar que recall y precisión están en tensión.** Subir uno suele bajar el otro; elige según **el costo de cada error** en tu contexto.
- **Creer que el umbral 0,5 es obligatorio.** Es una decisión tuya: muévelo para favorecer recall (no perderte casos) o precisión (no dar falsas alarmas).
- **Correr K-Means sin escalar.** La variable de mayor escala (aquí el monto) domina la distancia y arruina los grupos. **Escala siempre** (`StandardScaler`).
- **Buscar el k "verdadero".** No existe: el codo y la silueta **sugieren**, no dictan. K-Means siempre entrega grupos, incluso en datos sin estructura.
- **Tratar los clusters como una etiqueta oficial.** Son una **construcción** que depende de tus decisiones (k, features, escala): úsalos para explorar, no para clasificar personas."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: en cada uno **calculas un número** y luego eliges la **interpretación
correcta** asignando una letra (`"A"`, `"B"` o `"C"`). Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 trampa de la exactitud ----
E1 = """## Ejercicio 01 · La trampa de la exactitud
Reutiliza `y_te` (las etiquetas reales del conjunto de prueba, ya creado en la sección 1).

- Guarda en `acc_todo_neg` la **exactitud** de un modelo que predice **0 (no alto monto) para TODO**.
  Pista: si predices 0 a todos, aciertas en todos los que realmente son 0 → `(y_te == 0).mean()`.
- Guarda en `recall_todo_neg` el **recall** de ese modelo sobre la clase positiva (los 'alto monto').
  Pista: si nunca predices 1, no pillas ninguno → es `0.0`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** Como la exactitud es alta (~90%), el modelo "todo negativo" es un buen detector de compras grandes.
  - **B.** La exactitud es alta **pero** el recall es 0: el modelo no detecta ni una compra grande. La exactitud, sola, engaña con clases desbalanceadas.
  - **C.** Exactitud y recall siempre coinciden, así que da igual cuál mires."""
E1_TODO = """acc_todo_neg = None      # TODO: exactitud de predecir 0 a todos -> (y_te == 0).mean()
recall_todo_neg = None   # TODO: recall del modelo 'todo negativo' sobre la clase 1 (es 0.0)
conclusion = None        # TODO: "A", "B" o "C"
"""
E1_SOL = """acc_todo_neg = (y_te == 0).mean()
recall_todo_neg = 0.0
conclusion = "B"
"""
E1_CHK = """try:
    _acc = (y_te == 0).mean()
    _rec = 0.0
    _correcta = "B" if (_acc > 0.8 and _rec == 0.0) else "A"
    assert acc_todo_neg is not None and abs(acc_todo_neg - _acc) < 0.01, f"acc_todo_neg debería ser ~{_acc:.2f}"
    assert recall_todo_neg is not None and abs(recall_todo_neg - _rec) < 1e-9, "recall_todo_neg debería ser 0.0"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿alta exactitud con recall 0 es un buen detector?"
    print(f"✅ Correcto. Exactitud {_acc:.1%} con recall 0: acierta mucho y NO detecta nada. Esa es la trampa.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 recall del clasificador real ----
E2 = """## Ejercicio 02 · Recall: lo que se te escapa
Usa el clasificador real `clf` y sus predicciones `pred` sobre `X_te` (creados en la sección 2).

- Guarda en `recall_real` el **recall** del clasificador sobre la clase 'alto monto' (clase 1).
  Pista: `recall_score(y_te, pred, zero_division=0)`.
- Guarda en `acc_real` su **exactitud**: `accuracy_score(y_te, pred)`.
- Elige en `conclusion` la interpretación correcta:
  - **A.** Como la exactitud supera el 90%, el modelo encuentra casi todas las compras grandes.
  - **B.** A pesar de la exactitud alta, el recall es cercano al 50%: se le **escapa** alrededor de la mitad de las compras grandes reales. Exactitud ≠ detección.
  - **C.** Un recall de ~0,5 significa que el modelo se equivoca en la mitad de TODAS las predicciones."""
E2_TODO = """recall_real = None   # TODO: recall_score(y_te, pred, zero_division=0)
acc_real = None      # TODO: accuracy_score(y_te, pred)
conclusion = None    # TODO: "A", "B" o "C"
"""
E2_SOL = """recall_real = recall_score(y_te, pred, zero_division=0)
acc_real = accuracy_score(y_te, pred)
conclusion = "B"
"""
E2_CHK = """try:
    _rec = recall_score(y_te, pred, zero_division=0)
    _acc = accuracy_score(y_te, pred)
    # Alta exactitud pero recall claramente por debajo: la exactitud no refleja la detección
    _correcta = "B" if (_acc > 0.8 and _rec < 0.8) else "A"
    assert recall_real is not None and abs(recall_real - _rec) < 0.01, f"recall_real debería ser ~{_rec:.2f}"
    assert acc_real is not None and abs(acc_real - _acc) < 0.01, f"acc_real debería ser ~{_acc:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa qué dice el recall vs la exactitud"
    print(f"✅ Correcto. Exactitud {_acc:.1%} pero recall {_rec:.1%}: se escapa ~la mitad de las compras grandes.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 matriz de confusión: falsos negativos ----
E3 = """## Ejercicio 03 · Falsos negativos en la matriz de confusión
Usa la matriz de confusión de `clf` sobre el conjunto de prueba.

- Calcula `cm = confusion_matrix(y_te, pred, labels=[0, 1])` y desempácala:
  `vn, fp, fn, vp = cm.ravel()`.
- Guarda en `falsos_negativos` el valor `fn` (compras de alto monto que el modelo dejó pasar como normales).
- Guarda en `verdaderos_positivos` el valor `vp` (compras de alto monto correctamente detectadas).
- Elige en `conclusion` la lectura correcta:
  - **A.** Los falsos negativos son falsas alarmas inofensivas: dan lo mismo.
  - **B.** Cada falso negativo es una compra grande que **se escapó** sin revisión; en una auditoría es justo el error que más cuesta.
  - **C.** Si hay falsos negativos, la matriz de confusión está mal calculada."""
E3_TODO = """cm = None                  # TODO: confusion_matrix(y_te, pred, labels=[0, 1])
falsos_negativos = None    # TODO: el valor fn de cm.ravel()
verdaderos_positivos = None  # TODO: el valor vp de cm.ravel()
conclusion = None          # TODO: "A", "B" o "C"
"""
E3_SOL = """cm = confusion_matrix(y_te, pred, labels=[0, 1])
vn, fp, fn, vp = cm.ravel()
falsos_negativos = fn
verdaderos_positivos = vp
conclusion = "B"
"""
E3_CHK = """try:
    _cm = confusion_matrix(y_te, pred, labels=[0, 1])
    _vn, _fp, _fn, _vp = _cm.ravel()
    # Un falso negativo es, por definición, un positivo real que se predijo negativo:
    # un caso que se escapó. Esa lectura (B) no depende de los números.
    _correcta = "B"
    assert falsos_negativos is not None and int(falsos_negativos) == int(_fn), f"falsos_negativos debería ser {_fn}"
    assert verdaderos_positivos is not None and int(verdaderos_positivos) == int(_vp), f"verdaderos_positivos debería ser {_vp}"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿qué es un falso negativo en una auditoría?"
    print(f"✅ Correcto. {int(_fn)} falsos negativos: {int(_fn)} compras grandes que se escaparon sin revisar.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 K-Means y escalado (calcula la dominancia del monto) ----
E4 = """## Ejercicio 04 · Por qué K-Means necesita escalado
Sin escalar, la distancia de K-Means la domina la variable de mayor rango. Compáralos sobre `df`:

- Guarda en `rango_cantidad` el rango de `cantidad`: `df["cantidad"].max() - df["cantidad"].min()`.
- Guarda en `rango_monto` el rango de `monto_total`: `df["monto_total"].max() - df["monto_total"].min()`.
- Guarda en `veces` cuántas veces más grande es el rango del monto que el de la cantidad:
  `rango_monto / rango_cantidad`.
- Elige en `conclusion` la interpretación correcta:
  - **A.** Como ambos rangos son parecidos, escalar da exactamente lo mismo.
  - **B.** El rango del monto es **miles de veces** mayor que el de la cantidad: sin escalar, el monto domina la distancia y K-Means agrupa casi solo por monto. Por eso hay que **escalar** antes.
  - **C.** El monto tiene mayor rango, así que conviene dejarlo sin escalar para que "pese más"."""
E4_TODO = """rango_cantidad = None   # TODO: max - min de df["cantidad"]
rango_monto = None      # TODO: max - min de df["monto_total"]
veces = None            # TODO: rango_monto / rango_cantidad
conclusion = None       # TODO: "A", "B" o "C"
"""
E4_SOL = """rango_cantidad = df["cantidad"].max() - df["cantidad"].min()
rango_monto = df["monto_total"].max() - df["monto_total"].min()
veces = rango_monto / rango_cantidad
conclusion = "B"
"""
E4_CHK = """try:
    _rc = df["cantidad"].max() - df["cantidad"].min()
    _rm = df["monto_total"].max() - df["monto_total"].min()
    _veces = _rm / _rc
    _correcta = "B" if _veces > 100 else "A"
    assert rango_cantidad is not None and abs(rango_cantidad - _rc) < 1, "Revisa rango_cantidad"
    assert rango_monto is not None and abs(rango_monto - _rm) < 1, "Revisa rango_monto"
    assert veces is not None and abs(veces - _veces) < 1, f"veces debería ser ~{_veces:.0f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa qué pasa cuando una variable tiene rango muchísimo mayor"
    print(f"✅ Correcto. El monto tiene un rango ~{_veces:,.0f}× mayor: sin escalar domina la distancia. Por eso se escala.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo entrenas y agrupas: entiendes **por qué la exactitud engaña** con clases desbalanceadas, qué
miden de verdad **precisión, recall y F1**, cómo leer una **matriz de confusión** (y por qué un **falso
negativo** puede ser el error más caro), qué decisión tomas al mover el **umbral** y qué resume el **AUC**.
Y en clustering: por qué K-Means **necesita escalado**, qué **supuestos** esconde, cómo orientarte con el
**codo** y la **silueta**, y por qué los clusters son una **construcción**, no una verdad.

La regla de oro que te llevas: **ninguna métrica habla sola.** Antes de confiar en un modelo, pregunta por
la clase rara, por el tipo de error que más cuesta y por las decisiones (umbral, escala, k) que hay detrás
del resultado. Eso distingue a quien *usa* un modelo de quien *se deja convencer* por él."""


def md(t, cid): return {"cell_type": "markdown", "metadata": {}, "id": cid, "source": t}
def code(t, cid): return {"cell_type": "code", "metadata": {}, "id": cid, "execution_count": None, "outputs": [], "source": t}

def build(resuelto):
    g = lambda sol, todo: sol if resuelto else todo
    cells = [
        md(TITULO, "p00"), code(CARGA, "p01"),
        md(S1, "p02"), code(S1_CODE, "p03"),
        md(S2, "p04"), code(S2_CODE, "p05"),
        md(S3, "p06"), code(S3_CODE, "p07"),
        md(S4, "p08"), code(S4_CODE, "p09"),
        md(S5, "p10"), code(S5_CODE, "p11"),
        md(S6, "p12"), code(S6_CODE, "p13"),
        md(ERRORES, "p14"), md(EJ_HEADER, "p15"),
        md(E1, "p16"), code(g(E1_SOL, E1_TODO), "p17"), code(E1_CHK, "p18"),
        md(E2, "p19"), code(g(E2_SOL, E2_TODO), "p20"), code(E2_CHK, "p21"),
        md(E3, "p22"), code(g(E3_SOL, E3_TODO), "p23"), code(E3_CHK, "p24"),
        md(E4, "p25"), code(g(E4_SOL, E4_TODO), "p26"), code(E4_CHK, "p27"),
        md(CIERRE, "p28"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "profundiza.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "profundiza_solucion.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Generados: profundiza.ipynb y profundiza_solucion.ipynb en", BASE)
