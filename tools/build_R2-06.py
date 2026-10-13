"""build_R2-06.py — módulo R2-06 (Clasificación y clustering).

Rama R2 (Científico de Datos). Los dos grandes tipos de aprendizaje: clasificación
supervisada (con clases desbalanceadas, matriz de confusión y precisión/recall) y
clustering no supervisado (K-Means con escalado). Rearmado 2026 (retira compras
públicas): ancla = PM2.5 diario SINCA (aire_diario.csv). Clasificación: ¿el día
supera la norma de 24 h (50 µg/m³, D.S. 12/2011 MMA)? Clustering: perfil mensual
de PM2.5 de las 14 estaciones, estandarizado. Profundiza = transferencia: reclamos
SERNAC 2011 (reclamos.csv, dato histórico) — clasificación tabular con one-hot.
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-06.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-06-clasificacion-y-clustering")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "estaciones.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

df = pd.read_csv("aire_diario.csv", parse_dates=["fecha"])   # PM2.5 diario por estación
estaciones = pd.read_csv("estaciones.csv")                    # comuna y región de cada estación
print("mediciones:", df.shape, "| estaciones:", estaciones.shape)
df.head(3)'''

INTRO = '''## Dos preguntas, dos tipos de aprendizaje

- **Supervisado (clasificación):** *«Tengo seis años de días ya etiquetados: sé cuáles superaron
  la norma de PM2.5. ¿Puede un modelo aprender a anticipar si **mañana** la superará?»*
  Hay una respuesta correcta (`y`) con la que aprender.
- **No supervisado (clustering):** *«Tengo 14 estaciones con su contaminación mes a mes, pero
  nadie las ha clasificado. ¿Se agrupan solas en **tipos de ciudad** según cuándo se ensucia
  su aire?»* No hay respuesta correcta: el algoritmo busca parecidos.

> 📏 **La norma.** La norma primaria de calidad del aire para PM2.5 en 24 horas es
> **50 µg/m³** (D.S. 12/2011 del Ministerio del Medio Ambiente). Un día «sobre la norma» es
> un día en que la población respiró aire que la ley considera dañino para la salud.'''

PREP = '''# Preparación: ordenamos por estación y fecha y construimos las variables.
df = df.sort_values(["estacion", "fecha"])
# lo que SÍ sabemos la víspera: el PM2.5 de ayer en la misma estación
df["pm25_ayer"] = df.groupby("estacion")["pm25"].shift(1)
df["mes"] = df["fecha"].dt.month
df["invierno"] = df["mes"].isin([5, 6, 7, 8]).astype(int)   # mayo a agosto
# solo días con el dato de hoy y el de ayer
d = df.dropna(subset=["pm25", "pm25_ayer"]).copy()
d["sobre_norma"] = (d["pm25"] > 50).astype(int)              # 1 = día sobre la norma
print("días utilizables:", len(d), "| días sobre la norma:", int(d["sobre_norma"].sum()))'''

EJ = [
 ("## 1. Clasificación: predecir una categoría",
  "Es el mismo flujo de R2-04 y R2-05 —separar prueba, `fit`, `predict`— con un cambio: el "
  "objetivo `y` ahora es una **categoría** (0 = día bajo la norma, 1 = día sobre la norma).\n\n"
  "Antes de modelar, mira **cuántos** positivos hay. Si son pocos, las clases están "
  "**desbalanceadas** y conviene dividir con `stratify=y`, para que entrenamiento y prueba "
  "tengan la **misma proporción** de días sobre la norma.\n\n"
  "> 🧠 **Analogía.** No estimas *cuántos* µg/m³ habrá (eso sería regresión): decides si el día "
  "cae en la pila «normal» o en la pila «sobre la norma».",
  "Prepara X, y y una división estratificada",
  '''X = d[["pm25_ayer", "invierno"]]
y = d["sobre_norma"]
tasa_positivos = y.mean()
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)
print(f"Días sobre la norma: {tasa_positivos:.1%} del total")
print("train:", len(X_train), f"({y_train.mean():.2%} positivos)",
      "| test:", len(X_test), f"({y_test.mean():.2%} positivos)")''',
  '''# TODO: X con las columnas "pm25_ayer" e "invierno"; y con "sobre_norma"
X = ...
y = ...
# TODO: proporción de días sobre la norma (el promedio de una columna 0/1)
tasa_positivos = ...
# TODO: divide con test_size=0.3, random_state=42 y stratify=y
X_train, X_test, y_train, y_test = ...
print("tasa de positivos:", tasa_positivos)''',
  '''assert list(X_train.columns) == ["pm25_ayer", "invierno"], "X debe tener pm25_ayer e invierno, en ese orden"
assert 0.02 < tasa_positivos < 0.08, "La tasa de días sobre la norma debería rondar el 4 %"
assert abs(len(X_test) - 0.3 * len(X)) <= 1, "Usa test_size=0.3"
assert abs(y_train.mean() - y_test.mean()) < 0.002, "Falta stratify=y: las proporciones no calzan"''',
  "X = d[['pm25_ayer', 'invierno']], y = d['sobre_norma'], tasa = y.mean() y "
  "train_test_split(X, y, test_size=0.3, random_state=42, stratify=y).",
  None),

 ("## 2. La trampa de la exactitud",
  "La **exactitud** (*accuracy*) es el % de días bien clasificados. Suena bien, pero con clases "
  "desbalanceadas **engaña**: un «modelo» que **siempre** dice «hoy no se supera la norma» acierta "
  "en todos los días normales… y nunca avisa de un día malo. Entrena una **regresión logística** "
  "(el clasificador lineal clásico) y compárala con ese modelo tonto.",
  "Entrena el clasificador y compáralo con el modelo que siempre dice «no»",
  '''modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)
exactitud = accuracy_score(y_test, y_pred)
exactitud_tonta = (y_test == 0).mean()      # acierta todos los días normales y ninguno malo
print(f"Exactitud del modelo:        {exactitud:.3f}")
print(f"Exactitud de «siempre no»:   {exactitud_tonta:.3f}")''',
  '''modelo = LogisticRegression(max_iter=1000)
# TODO: entrena con (X_train, y_train) y predice sobre X_test
...
y_pred = ...
# TODO: exactitud del modelo y la del modelo que siempre predice 0
exactitud = ...
exactitud_tonta = ...
print("modelo:", exactitud, "| siempre no:", exactitud_tonta)''',
  '''ref = LogisticRegression(max_iter=1000).fit(X_train, y_train)
assert abs(float(exactitud) - accuracy_score(y_test, ref.predict(X_test))) < 0.005
assert abs(float(exactitud_tonta) - (y_test == 0).mean()) < 1e-9
assert exactitud_tonta > 0.9, "El modelo tonto también supera el 90 %: ahí está la trampa"''',
  "modelo.fit(X_train, y_train); y_pred = modelo.predict(X_test); accuracy_score(y_test, y_pred) "
  "y (y_test == 0).mean() para el modelo que siempre dice 0.",
  None),

 ("## 3. La matriz de confusión: ¿en qué se equivoca?",
  "La exactitud resume todo en un número; la **matriz de confusión** separa los aciertos y los "
  "**dos tipos de error**:\n\n"
  "| | predice «normal» | predice «sobre la norma» |\n"
  "|---|---|---|\n"
  "| **real: normal** | verdadero negativo (TN) | **falsa alarma** (FP) |\n"
  "| **real: sobre la norma** | **día malo que se escapó** (FN) | verdadero positivo (TP) |\n\n"
  "Con `confusion_matrix(y_test, y_pred).ravel()` obtienes los cuatro números en el orden "
  "`tn, fp, fn, tp`.",
  "Cuenta los aciertos y los dos tipos de error",
  '''cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()
print(cm)
print(f"Días malos detectados: {tp} | días malos que se escaparon: {fn} | falsas alarmas: {fp}")''',
  '''# TODO: matriz de confusión entre lo real (y_test) y lo predicho (y_pred)
cm = ...
# TODO: desarma la matriz en sus 4 números (en este orden: tn, fp, fn, tp)
tn, fp, fn, tp = ...
print(cm)''',
  '''assert tn + fp + fn + tp == len(y_test)
assert tp + fn == int(y_test.sum()), "tp + fn deben sumar todos los días realmente sobre la norma"
assert fn > 0, "Con este modelo se escapan días malos (fn > 0)"''',
  "cm = confusion_matrix(y_test, y_pred) y tn, fp, fn, tp = cm.ravel().",
  '''# (ilustración) La matriz de confusión dibujada
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, display_labels=["normal", "sobre la norma"], cmap="Blues")
plt.title("¿Supera mañana la norma? — conjunto de prueba")
plt.show()'''),

 ("## 4. Precisión, recall y el error más caro",
  "Dos métricas miran **solo** a la clase que importa (el día sobre la norma):\n\n"
  "- **Precisión** = de los días que el modelo **alertó**, ¿cuántos eran realmente malos? (pocas falsas alarmas)\n"
  "- **Recall** (sensibilidad) = de los días **realmente** malos, ¿cuántos detectó? (pocos días que se escapan)\n\n"
  "Para la **autoridad sanitaria** los errores no cuestan lo mismo. Un día malo que se escapa (FN) "
  "es población —niñas, niños, personas mayores, enfermos respiratorios— expuesta **sin aviso ni "
  "medidas**. Una falsa alarma (FP) es una restricción innecesaria (calefacción a leña, actividad "
  "física escolar) con costo económico y de credibilidad. Si el FN es más caro, conviene "
  "**subir el recall** aunque baje la precisión.\n\n"
  "Una forma de lograrlo: `class_weight=\"balanced\"` le dice al modelo que equivocarse con la "
  "clase rara pesa más.",
  "Compara precisión y recall del modelo normal y del modelo balanceado",
  '''precision_base = precision_score(y_test, y_pred)
recall_base = recall_score(y_test, y_pred)

modelo_bal = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
y_pred_bal = modelo_bal.predict(X_test)
precision_bal = precision_score(y_test, y_pred_bal)
recall_bal = recall_score(y_test, y_pred_bal)
print(f"Normal:     precisión {precision_base:.2f} | recall {recall_base:.2f}")
print(f"Balanceado: precisión {precision_bal:.2f} | recall {recall_bal:.2f}")''',
  '''# TODO: precisión y recall del modelo normal (y_test vs y_pred)
precision_base = ...
recall_base = ...

# TODO: entrena el mismo modelo con class_weight="balanced" y predice X_test
modelo_bal = ...
y_pred_bal = ...
precision_bal = ...
recall_bal = ...
print("normal:", precision_base, recall_base, "| balanceado:", precision_bal, recall_bal)''',
  '''assert abs(float(precision_base) - precision_score(y_test, y_pred)) < 1e-9
assert abs(float(recall_base) - recall_score(y_test, y_pred)) < 1e-9
assert recall_bal > recall_base + 0.2, "El modelo balanceado debería detectar muchos más días malos"
assert precision_bal < precision_base, "…a cambio de más falsas alarmas (menor precisión)"''',
  "precision_score / recall_score sobre (y_test, y_pred); luego "
  "LogisticRegression(max_iter=1000, class_weight='balanced').fit(X_train, y_train).",
  '''# (ilustración) El intercambio, en días concretos del conjunto de prueba
for nombre, pred in [("normal", y_pred), ("balanceado", y_pred_bal)]:
    _, fp_, fn_, _ = confusion_matrix(y_test, pred).ravel()
    print(f"{nombre:>10}: {fn_:>4} días malos se escapan | {fp_:>4} falsas alarmas")'''),

 ("## 5. Clustering: descubrir grupos sin etiquetas",
  "Cambiamos de mundo. Ahora **no** hay una respuesta correcta. Resumimos cada estación en su "
  "**perfil**: el PM2.5 promedio de cada mes (una fila por estación, 12 columnas). Le pedimos a "
  "**K-Means** que forme **3 grupos** de estaciones parecidas.\n\n"
  "K-Means mide **distancias**, así que primero **estandarizamos** con `StandardScaler` (cada mes "
  "queda con media 0 y desviación 1): así ningún mes domina solo por tener números más grandes.\n\n"
  "> 🧠 **Analogía.** Te pasan 14 fichas de ciudades sin clasificar y las separas en pilas "
  "según cómo se ve su año de contaminación. Nadie te dijo qué pilas hacer.",
  "Arma el perfil mensual y agrupa las estaciones con K-Means",
  '''perfil = df.pivot_table(index="estacion", columns="mes", values="pm25", aggfunc="mean")
Z = StandardScaler().fit_transform(perfil)
km = KMeans(n_clusters=3, random_state=42, n_init=10)
grupos = pd.Series(km.fit_predict(Z), index=perfil.index, name="cluster")
print(perfil.shape)
print(grupos.sort_values())''',
  '''# TODO: tabla estación × mes con el PM2.5 promedio (pivot_table con aggfunc="mean")
perfil = ...
# TODO: estandariza el perfil con StandardScaler().fit_transform(...)
Z = ...
km = KMeans(n_clusters=3, random_state=42, n_init=10)
# TODO: etiqueta de cluster de cada estación (km.fit_predict(Z)), como Serie con índice = estación
grupos = ...
print(grupos)''',
  '''assert perfil.shape == (14, 12), "El perfil debe tener 14 estaciones (filas) y 12 meses (columnas)"
assert abs(float(np.mean(Z))) < 1e-6, "Z debe estar estandarizado (media 0)"
assert len(grupos) == 14 and grupos.nunique() == 3''',
  "perfil = df.pivot_table(index='estacion', columns='mes', values='pm25', aggfunc='mean'); "
  "Z = StandardScaler().fit_transform(perfil); grupos = pd.Series(km.fit_predict(Z), index=perfil.index).",
  '''# (ilustración) Cada línea es una estación, coloreada por su cluster
colores = ["#4240e5", "#ff6b35", "#2a9d8f"]
fig, ax = plt.subplots(figsize=(8, 4.5))
for est, fila in perfil.iterrows():
    ax.plot(fila.index, fila.values, color=colores[grupos[est]], alpha=0.8)
ax.axhline(50, ls="--", color="gray", lw=1)
ax.set_xticks(range(1, 13))
ax.set_xlabel("Mes"); ax.set_ylabel("PM2.5 promedio (µg/m³)")
ax.set_title("Perfil mensual de PM2.5 por estación, coloreado por cluster")
plt.tight_layout(); plt.show()'''),

 ("## 6. Interpretar los grupos",
  "Un cluster no trae nombre: **tú** se lo pones mirando su perfil promedio y quiénes lo integran. "
  "Calcula el perfil promedio de cada grupo, identifica el grupo con el **invierno más severo** "
  "(mayor PM2.5 en junio) y lista sus estaciones. Luego cruza con `estaciones` para ver dónde están.",
  "Ponle nombre al grupo del invierno más severo",
  '''perfil_grupo = perfil.groupby(grupos).mean()
cluster_invierno = perfil_grupo[6].idxmax()
estaciones_invierno = list(grupos[grupos == cluster_invierno].index)
print(perfil_grupo.round(1))
print("Grupo de invierno más severo:", estaciones_invierno)
tabla = estaciones.merge(grupos.reset_index(), on="estacion")[["estacion", "comuna", "region", "cluster"]]
print(tabla.sort_values("cluster").to_string(index=False))''',
  '''# TODO: perfil promedio de cada grupo (agrupa perfil por grupos y promedia)
perfil_grupo = ...
# TODO: el cluster con mayor PM2.5 en junio (columna 6) — usa idxmax()
cluster_invierno = ...
# TODO: lista de estaciones que pertenecen a ese cluster
estaciones_invierno = ...
print("Grupo de invierno más severo:", estaciones_invierno)''',
  '''assert perfil_grupo.shape == (3, 12)
assert "Las Encinas Temuco" in estaciones_invierno and "Nielol" in estaciones_invierno
assert "Antofagasta" not in estaciones_invierno''',
  "perfil.groupby(grupos).mean(); perfil_grupo[6].idxmax(); "
  "list(grupos[grupos == cluster_invierno].index).",
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

1. Con el modelo balanceado se escapan muchos menos días malos, pero suben las falsas alarmas.
   Si fueras la **SEREMI de Salud**, ¿con cuál te quedarías y cómo se lo explicarías a la
   ciudadanía que tuvo que apagar su estufa un día que al final no superó la norma?
2. El clustering separó a Temuco del resto, sin que nadie le dijera nada de leña ni de latitud.
   ¿Qué **política** distinta pediría cada grupo? ¿Qué le falta al algoritmo para saber *por qué*
   se parecen?

> Un modelo te da números; la decisión sobre **qué error tolerar** es pública y se declara.'''

CIERRE = '''## Errores típicos

- **Celebrar un 96 % de exactitud** con clases desbalanceadas: compárala siempre con el modelo «siempre no».
- **Olvidar `stratify=y`**: con 4 % de positivos, un corte al azar puede dejar la prueba casi sin días malos.
- **No escalar antes de K-Means**: la variable con números más grandes decide sola los grupos.
- **Creer que el cluster es «la verdad»**: es una agrupación útil, no una categoría oficial; cambia con *k* y con las variables.

## Cierre

1. **Clasificación** (supervisada): mismo `fit`/`predict`, pero la exactitud engaña con clases
   desbalanceadas → mira la **matriz de confusión**, la **precisión** y el **recall**.
2. **Qué error es más caro** es una decisión de política pública: `class_weight="balanced"` sube el recall a costa de la precisión.
3. **Clustering** (no supervisado): K-Means sobre perfiles **estandarizados** descubre grupos que tú interpretas.

> *En R2-07 aprenderás a evaluar con rigor: fuga de datos, validación cruzada y por qué con datos
> en el tiempo **no** se puede barajar.*

---
*Fuente de datos: Sistema de Información Nacional de Calidad del Aire (SINCA), Ministerio del Medio Ambiente.*'''

IMPORTS_CELL = '''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-06", "Clasificación y clustering", "R2", "Científico de Datos", "12",
                      ["Entrenar un **clasificador** y desconfiar de la exactitud con clases desbalanceadas.",
                       "Leer la **matriz de confusión** y distinguir los dos tipos de error.",
                       "Usar **precisión y recall** para decidir qué error es más caro.",
                       "Agrupar con **K-Means** (con escalado) e **interpretar** los clusters."],
                      "entrenar y evaluar un clasificador con clases desbalanceadas, y aplicar clustering "
                      "con K-Means distinguiendo cuándo un problema es supervisado y cuándo no.",
                      "PM2.5 diario 2020–2025 de 14 estaciones SINCA (Ministerio del Medio Ambiente).",
                      n_checks=6),
        h.code(SETUP),
        h.md(INTRO),
        h.md("### Preparación"), h.code(PREP), h.code(IMPORTS_CELL),
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


# ── Profundización (opcional): transferencia con reclamos SERNAC ─────────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, classification_report

CSV = "reclamos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/reclamos.csv", CSV)
rec = pd.read_csv(CSV)
print("reclamos:", rec.shape)
print(rec["resultado"].value_counts())'''

PROF_EJ = [
 ("## 1. Transferencia: ¿el proveedor acogerá el reclamo?",
  "Dominio nuevo: **reclamos de consumidores ante el SERNAC** (muestra de 20.000 reclamos de "
  "**2011** — un dato histórico: el SERNAC no publica una base abierta más reciente con este "
  "detalle). Todas las variables son **categorías** (mercado, motivo legal…), no números.\n\n"
  "Objetivo binario: `acoge = 1` si el resultado fue «PROVEEDOR ACOGE». Primero, la vara mínima: "
  "la exactitud de predecir siempre la clase más frecuente.\n\n"
  "Un modelo no entiende texto: hay que convertir cada categoría en columnas 0/1. Eso es el "
  "**one-hot encoding** (`OneHotEncoder`): una columna por cada valor posible.",
  "Objetivo, línea base y codificación one-hot",
  '''rec["acoge"] = (rec["resultado"] == "PROVEEDOR ACOGE").astype(int)
CAT = ["mercado", "motivo_legal"]
X_tr, X_te, y_tr, y_te = train_test_split(rec[CAT], rec["acoge"], test_size=0.3,
                                          random_state=42, stratify=rec["acoge"])
linea_base = max(y_te.mean(), 1 - y_te.mean())
enc = OneHotEncoder(handle_unknown="ignore").fit(X_tr)
n_columnas = enc.transform(X_tr).shape[1]
print(f"Acoge: {rec['acoge'].mean():.1%} | línea base: {linea_base:.3f} | columnas one-hot: {n_columnas}")''',
  '''rec["acoge"] = (rec["resultado"] == "PROVEEDOR ACOGE").astype(int)
CAT = ["mercado", "motivo_legal"]
X_tr, X_te, y_tr, y_te = train_test_split(rec[CAT], rec["acoge"], test_size=0.3,
                                          random_state=42, stratify=rec["acoge"])
# TODO: exactitud de predecir siempre la clase más frecuente en y_te
linea_base = ...
# TODO: ajusta un OneHotEncoder(handle_unknown="ignore") sobre X_tr
enc = ...
# TODO: cuántas columnas 0/1 genera (shape[1] de enc.transform(X_tr))
n_columnas = ...
print("línea base:", linea_base, "| columnas:", n_columnas)''',
  '''assert 0.5 < linea_base < 0.55
assert n_columnas == X_tr["mercado"].nunique() + X_tr["motivo_legal"].nunique(), \\
    "One-hot crea una columna por cada valor distinto de cada variable"''',
  "linea_base = max(y_te.mean(), 1 - y_te.mean()); enc = OneHotEncoder(handle_unknown='ignore').fit(X_tr); "
  "enc.transform(X_tr).shape[1]."),

 ("## 2. Clasificar con variables categóricas",
  "Con las categorías ya convertidas en números, el flujo es el de siempre. ¿Supera el modelo "
  "a la línea base? ¿Por cuánto?",
  "Entrena una regresión logística sobre el one-hot",
  '''clf = LogisticRegression(max_iter=2000).fit(enc.transform(X_tr), y_tr)
pred = clf.predict(enc.transform(X_te))
exactitud = accuracy_score(y_te, pred)
print(f"Exactitud: {exactitud:.3f} vs línea base {linea_base:.3f}")''',
  '''# TODO: entrena LogisticRegression(max_iter=2000) con enc.transform(X_tr), y_tr
clf = ...
# TODO: predice sobre enc.transform(X_te) y mide la exactitud
pred = ...
exactitud = ...
print("exactitud:", exactitud)''',
  '''assert exactitud > linea_base + 0.05, "El modelo debería superar claramente a la línea base"''',
  "clf = LogisticRegression(max_iter=2000).fit(enc.transform(X_tr), y_tr); "
  "pred = clf.predict(enc.transform(X_te)); accuracy_score(y_te, pred)."),

 ("## 3. Siete resultados: el desbalance vuelve",
  "El resultado real tiene **7 categorías**, algunas muy raras (p. ej. «antecedentes insuficientes»). "
  "Con un clasificador multiclase, la exactitud puede verse aceptable mientras las clases raras "
  "**nunca** se predicen. El **recall macro** (el promedio simple del recall de cada clase) lo delata.",
  "Exactitud vs recall macro en el problema de 7 clases",
  '''CAT3 = ["mercado", "categoria_mercado", "motivo_legal"]
X_tr3, X_te3, y_tr3, y_te3 = train_test_split(rec[CAT3], rec["resultado"], test_size=0.3,
                                              random_state=42, stratify=rec["resultado"])
enc3 = OneHotEncoder(handle_unknown="ignore").fit(X_tr3)
clf3 = LogisticRegression(max_iter=3000).fit(enc3.transform(X_tr3), y_tr3)
pred3 = clf3.predict(enc3.transform(X_te3))
exactitud3 = accuracy_score(y_te3, pred3)
recall_macro = recall_score(y_te3, pred3, average="macro", zero_division=0)
print(f"Exactitud: {exactitud3:.2f} | recall macro: {recall_macro:.2f}")
print(classification_report(y_te3, pred3, zero_division=0))''',
  '''CAT3 = ["mercado", "categoria_mercado", "motivo_legal"]
X_tr3, X_te3, y_tr3, y_te3 = train_test_split(rec[CAT3], rec["resultado"], test_size=0.3,
                                              random_state=42, stratify=rec["resultado"])
enc3 = OneHotEncoder(handle_unknown="ignore").fit(X_tr3)
clf3 = LogisticRegression(max_iter=3000).fit(enc3.transform(X_tr3), y_tr3)
pred3 = clf3.predict(enc3.transform(X_te3))
# TODO: exactitud y recall macro (recall_score con average="macro", zero_division=0)
exactitud3 = ...
recall_macro = ...
print("exactitud:", exactitud3, "| recall macro:", recall_macro)''',
  '''assert recall_macro < exactitud3 - 0.1, "El recall macro debería quedar muy por debajo de la exactitud"''',
  "accuracy_score(y_te3, pred3) y recall_score(y_te3, pred3, average='macro', zero_division=0)."),
]

PROF_HEADER = '''# R2-06 · Clasificación y clustering — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: clasificación con datos **puramente categóricos** — reclamos de
consumidores ante el **SERNAC** (muestra de 20.000 reclamos de 2011, dato histórico). Vas a
convertir categorías en números con **one-hot**, superar una **línea base** y ver cómo el
**desbalance** reaparece cuando el problema tiene 7 clases.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-06.*\n\n"
                      "*Fuente: SERNAC, reclamos de consumidores 2011 (muestra de 20.000; dato histórico).*"))
    nb.cells = cells
    return nb


README = '''# R2-06 · Clasificación y clustering

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-06-clasificacion-y-clustering/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Los dos grandes tipos de aprendizaje sobre la **calidad del aire** (PM2.5 diario 2020–2025 de 14
estaciones SINCA, `aire_diario.csv` + `estaciones.csv`). **Clasificación:** ¿mañana se supera
la norma de 50 µg/m³? — clases desbalanceadas (≈4 % de días sobre la norma), la trampa de la
exactitud, matriz de confusión, precisión vs recall y qué error es más caro para la autoridad
sanitaria. **Clustering:** K-Means sobre el perfil mensual estandarizado de cada estación, que
separa solo a Temuco, a las estaciones del centro y a las del norte/costa. La profundización
transfiere la clasificación a reclamos SERNAC 2011 (`reclamos.csv`, dato histórico) con one-hot.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: one-hot, línea base y desbalance multiclase con reclamos.
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
