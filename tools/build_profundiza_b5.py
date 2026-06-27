# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B5 (pipelines reproducibles):
B5/profundiza.ipynb (estudiante) + B5/profundiza_solucion.ipynb (resuelto).

El cuaderno va al *porqué* de los pipelines: qué es el LEAKAGE y por qué es tan
peligroso, la separación FIT/TRANSFORM, el pipeline como CONTRATO, las SEMILLAS,
la consistencia TRAIN/SERVE y el VERSIONADO. Demos con sklearn Pipeline +
ColumnTransformer sobre el dataset real del módulo (compras_ml.csv)."""
import json, os

BASE = "B5-pipelines-reproducibles"

TITULO = """# B5 · Pipelines reproducibles — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B5 —donde *armaste* un `Pipeline` que
escalaba y entrenaba en un solo objeto— aquí vamos al *porqué*: qué es de verdad la **fuga de
información** (*data leakage*) y por qué tu modelo puede mentirte sin que te des cuenta, por qué el
escalado debe hacer **fit solo en entrenamiento** (la regla FIT/TRANSFORM), por qué un pipeline es un
**contrato** que evita olvidos, qué garantizan las **semillas**, por qué la transformación al **servir**
debe ser idéntica a la del **entrenamiento**, y qué rol juega el **versionado**.

Menos sintaxis nueva, más **disciplina de reproducibilidad**. Vamos a *medir numéricamente* la diferencia
entre hacerlo mal (con fuga) y hacerlo bien (con pipeline). Los ejercicios del final son más conceptuales
y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de B5. Mismo dataset: `compras_ml.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.metrics import mean_absolute_error

if not os.path.exists("compras_ml.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B5-pipelines-reproducibles/compras_ml.csv"
        urllib.request.urlretrieve(url, "compras_ml.csv")
    except Exception:
        print("Si estás en Colab, sube compras_ml.csv manualmente.")

df = pd.read_csv("compras_ml.csv")
X = df[["cantidad", "tamano_num"]]
y = df["monto_total"]
print(f"{len(df)} compras públicas cargadas | columnas: {list(df.columns)}")"""

S1 = """## 1. Qué es de verdad el *data leakage* (y por qué te miente)

En la lección lo nombramos: **fuga de información**. Aquí el *porqué*. La idea central de todo modelo es
estimar cómo se comportará con **datos que nunca ha visto**. Para eso reservamos un conjunto de **prueba**
(*test*) que el modelo **no toca** durante el entrenamiento, y lo usamos como un examen sorpresa.

El **leakage** ocurre cuando, sin darte cuenta, información del conjunto de prueba **se filtra** al
entrenamiento. El caso más común y silencioso: **preprocesar antes de separar**. Si calculas la media y
la desviación para escalar usando **todos** los datos (entrenamiento + prueba) y *después* separas, esos
estadísticos ya "vieron" la prueba. El examen dejó de ser sorpresa: el modelo recibe una pista del futuro.

**Analogía del sector público.** Es como diseñar la prueba de selección de un concurso usando también las
respuestas de los postulantes que vas a evaluar: el puntaje saldrá brillante, pero **no mide** quién
rendirá bien en el trabajo real. Tu métrica queda **optimista y falsa**.

Veámoslo con el dato real: escalamos de las dos formas y comparamos el error en la prueba."""

S1_CODE = """# DOS formas de escalar antes de un KNN. La diferencia es CUÁNDO calculamos media/desviación.

# (A) MAL: fit del escalador sobre TODO X (train+test) y RECIÉN ahí separamos -> leakage
escalador_todo = StandardScaler().fit(X)
X_todo = pd.DataFrame(escalador_todo.transform(X), columns=X.columns)
Xtr_m, Xte_m, ytr_m, yte_m = train_test_split(X_todo, y, test_size=0.3, random_state=42)
mae_leak = mean_absolute_error(yte_m, KNeighborsRegressor(3).fit(Xtr_m, ytr_m).predict(Xte_m))

# (B) BIEN: separar PRIMERO; fit del escalador SOLO en train; transform en ambos
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42)
escalador_train = StandardScaler().fit(Xtr)                 # estadísticos SOLO de train
mae_ok = mean_absolute_error(
    yte, KNeighborsRegressor(3).fit(escalador_train.transform(Xtr), ytr).predict(escalador_train.transform(Xte)))

print(f"MAE con leakage (escalar TODO antes de separar): {mae_leak:,.2f} CLP")
print(f"MAE honesto   (fit del escalador solo en train): {mae_ok:,.2f} CLP")

# ¿Por qué la brecha entre los dos MAE es tan chica? NO porque escalar dé igual.
# (De hecho escalar SÍ mueve mucho a un KNN: comparémoslo sin escalar.)
mae_sin_escalar = mean_absolute_error(yte, KNeighborsRegressor(3).fit(Xtr, ytr).predict(Xte))
media_train_cant = escalador_train.mean_[0]      # media que usó el fit honesto (solo train)
media_todo_cant  = escalador_todo.mean_[0]       # media que usó el fit con fuga (todo el dataset)
print(f"\\n(Para contraste) MAE de KNN SIN escalar:          {mae_sin_escalar:,.2f} CLP")
print(f"  -> escalar mueve el MAE en {abs(mae_sin_escalar - mae_ok):,.0f} CLP: el escalado SÍ importa, y mucho.")
print(f"  -> el leakage solo lo mueve {abs(mae_leak - mae_ok):,.0f} CLP.")
print(f"\\nLa brecha del leakage es pequeña porque con {len(df):,} filas y split 70/30,")
print(f"la media de train ({media_train_cant:.2f}) y la del total ({media_todo_cant:.2f}) difieren apenas")
print(f"{abs(media_train_cant - media_todo_cant):.2f} unidades: los estadísticos del escalador con y sin fuga casi coinciden.")
print("Con POCOS datos, el mismo experimento mostraría una diferencia mayor.")
print("El HÁBITO es el problema: en la sección 6 verás un caso donde el leakage es CATASTRÓFICO.")"""

S2 = """## 2. La regla de oro: FIT solo en train, TRANSFORM en ambos

Toda transformación que **aprende** algo de los datos (un escalador aprende media y desviación; un
imputador aprende con qué valor rellenar; un codificador aprende qué categorías existen) tiene dos
momentos distintos:

- **`fit`** → *aprender* los parámetros (ej: la media de cada columna). Se hace **solo con el
  entrenamiento**. Es el único conjunto del que el modelo tiene "permitido" mirar.
- **`transform`** → *aplicar* lo aprendido. Se hace en **ambos** conjuntos (train y test), pero usando
  **los parámetros aprendidos solo en train**.

La regla completa cabe en una frase: **`fit` solo en train; `transform` en todos**. Si haces `fit` con la
prueba incluida, ya filtraste información. Por eso `scikit-learn` separa a propósito estos dos métodos:
no es burocracia, es la barrera que impide la fuga.

Lo bonito es que **un `Pipeline` hace esto solo, siempre**: cuando llamas a `pipe.fit(X_train)`, internamente
hace `fit` de cada paso con train; cuando llamas a `pipe.predict(X_test)`, hace `transform` con lo aprendido.
Nunca se equivoca de conjunto. Comprobémoslo mirando *qué media guardó* el escalador."""

S2_CODE = """# El escalador que entrenamos SOLO con train: ¿qué media memorizó?
media_que_guardo = escalador_train.mean_[0]          # parámetro aprendido por el fit
media_de_train   = Xtr["cantidad"].mean()            # media real del train
media_de_todo    = X["cantidad"].mean()              # media de TODO el dataset

print(f"Media que guardó el escalador (columna 'cantidad'): {media_que_guardo:.4f}")
print(f"Media real de SOLO el train:                        {media_de_train:.4f}")
print(f"Media de TODO el dataset (train+test):              {media_de_todo:.4f}")
print()
print(f"¿El escalador usó la media de train?  {np.isclose(media_que_guardo, media_de_train)}")
print(f"¿Usó la media de TODO (leakage)?      {np.isclose(media_que_guardo, media_de_todo)}")
print("\\nEl fit miró SOLO el train: por eso su media coincide con la de train, no con la del total.")"""

S3 = """## 3. El pipeline como CONTRATO (no como atajo)

Mucha gente ve el `Pipeline` como una comodidad para escribir menos líneas. Es mucho más: es un
**contrato** que *garantiza* tres cosas que a mano se olvidan justo el día equivocado:

1. **El orden siempre es el mismo.** Escalar → modelar, nunca al revés, ni hoy ni en seis meses.
2. **El `fit`/`transform` se hace bien por construcción.** Imposible escalar la prueba con sus propios
   estadísticos: el pipeline lo prohíbe.
3. **Lo que entrenaste es exactamente lo que sirves.** El objeto que guardas contiene *todos* los pasos.

Y con un **`ColumnTransformer`** el contrato cubre **columnas distintas con tratos distintos**: las
**numéricas** (`cantidad`, `tamano_num`) se escalan; las **categóricas** (`categoria`,
`tamano_proveedor`, `region_comprador`) se convierten a columnas 0/1 con *one-hot*. Todo dentro del mismo
objeto, sin pasos sueltos que se puedan olvidar.

**Analogía del sector público.** No es un *post-it* con instrucciones (que se despega y cada quien
interpreta a su manera): es un **procedimiento firmado y plastificado**, idéntico para todos, todas las
veces. Esa es la diferencia entre "reproducible" y "salió bien esta vez"."""

S3_CODE = """num = ["cantidad", "tamano_num"]
cat = ["categoria", "tamano_proveedor", "region_comprador"]
Xc, yc = df[num + cat], df["monto_total"]

# El ColumnTransformer da un trato DISTINTO a cada tipo de columna, dentro de un solo contrato
pre = ColumnTransformer([
    ("numericas",   StandardScaler(),                      num),
    ("categoricas", OneHotEncoder(handle_unknown="ignore"), cat),
])
pipe_ct = Pipeline([("preparacion", pre), ("modelo", Ridge(alpha=1.0))])

cv = KFold(n_splits=5, shuffle=True, random_state=42)
mae_ct = -cross_val_score(pipe_ct, Xc, yc, cv=cv, scoring="neg_mean_absolute_error").mean()
pipe_ct.fit(Xc, yc)
n_cols = pipe_ct.named_steps["preparacion"].transform(Xc[:1]).shape[1]

print(f"Un SOLO objeto escala 2 numéricas y codifica 3 categóricas -> {n_cols} columnas internas.")
print(f"MAE (validación cruzada, Ridge sobre num+categóricas): {mae_ct:,.2f} CLP")
print("\\nEscala, codifica, modela: todo encadenado en un contrato. Nada suelto que olvidar.")"""

S4 = """## 4. Semillas: por qué el azar tiene que ser *el mismo* azar

Separar en train/test, barajar para validación cruzada, inicializar ciertos modelos… todos usan
**azar**. Si el azar cambia cada vez que ejecutas, tus resultados también, y entonces **nadie puede
reproducir tu número** —ni tú mismo la semana siguiente, ni la auditoría dentro de un año.

La **semilla** (`random_state`) fija ese azar. No lo elimina: lo vuelve **repetible**. Con la misma
semilla, `train_test_split` deja **exactamente las mismas filas** en la prueba, siempre. Con una semilla
distinta, deja otras. Esto es lo que separa un resultado **reproducible** de uno **anecdótico**.

**Analogía del sector público.** Es como el **sorteo de un orden de revisión** de expedientes: si se hace
con una semilla registrada, cualquiera puede repetir el sorteo y verificar que no hubo trampa. Sin semilla,
"confía en mí" es todo lo que tienes — y en el Estado eso no basta.

Comprobémoslo: misma semilla ⇒ mismas filas en la prueba; semilla distinta ⇒ filas distintas."""

S4_CODE = """idx = np.arange(len(df))
# Dos separaciones con la MISMA semilla y una con OTRA. Miramos qué filas caen en la prueba (test).
_, test_42a = train_test_split(idx, test_size=0.3, random_state=42)
_, test_42b = train_test_split(idx, test_size=0.3, random_state=42)
_, test_7   = train_test_split(idx, test_size=0.3, random_state=7)

iguales_misma   = np.array_equal(test_42a, test_42b)
iguales_distinta = np.array_equal(test_42a, test_7)

print(f"Primeras filas de prueba con semilla 42: {list(test_42a[:5])}")
print(f"Primeras filas de prueba con semilla 42: {list(test_42b[:5])}  (otra vez)")
print(f"Primeras filas de prueba con semilla 7 : {list(test_7[:5])}")
print()
print(f"¿Semilla 42 == semilla 42?  {iguales_misma}   (misma semilla => MISMO split, reproducible)")
print(f"¿Semilla 42 == semilla 7?   {iguales_distinta}   (otra semilla => OTRO split)")"""

S5 = """## 5. TRAIN = SERVE: la transformación al servir debe ser idéntica

Un modelo no sirve de nada guardado en un cajón: en algún momento llega un **caso nuevo** (una compra
recién ingresada) y hay que **predecir en producción** (*serve*). Aquí aparece el error más caro de
todos: **transformar el caso nuevo de forma distinta a como entrenaste**.

Si al entrenar escalaste con la media de train, pero al servir escalas con… nada, o con otra media, o se
te olvida codificar una categórica, el modelo recibe números en otra escala y predice cualquier cosa —sin
avisar, sin error visible. A esto se le llama **train/serve skew** (desajuste entre entrenamiento y
servicio), y es invisible justamente porque "no se rompe": solo da malas predicciones.

La solución es la misma de todo el cuaderno: **servir el pipeline completo**. El mismo objeto que escala y
codifica al entrenar, escala y codifica al servir, con los **mismos parámetros aprendidos**. Por eso se
**versiona y se guarda con `joblib`** el pipeline entero (no solo el modelo): así garantizas que la
transformación de hoy es bit a bit la de mañana. Sirvamos una compra nueva — incluso con una región que el
modelo **nunca vio**."""

S5_CODE = """# Compra nueva que llega "en producción". El MISMO pipeline la transforma como entrenó.
compra_nueva = pd.DataFrame({
    "cantidad": [100], "tamano_num": [2],
    "categoria": ["Productos de panadería"],
    "tamano_proveedor": ["Micro"],
    "region_comprador": ["Region de Los Rios"],
})
pred = pipe_ct.predict(compra_nueva)[0]
print(f"Predicción al servir (pipeline completo): {pred:,.0f} CLP")

# Caso límite: una región que NO estaba en el entrenamiento. handle_unknown='ignore' evita el crash.
compra_rara = compra_nueva.copy()
compra_rara["region_comprador"] = ["Region Que No Existe"]
pred_rara = pipe_ct.predict(compra_rara)[0]
print(f"Predicción con región nunca vista:        {pred_rara:,.0f} CLP  (no se cae: el contrato la maneja)")
print("\\nLa clave: al servir se aplicó EXACTAMENTE la misma preparación que al entrenar.")
print("Por eso se versiona y guarda el PIPELINE entero (joblib), no solo el modelo suelto.")"""

S6 = """## 6. Cuando el leakage es catastrófico: la prueba de fuego

En la sección 1 la fuga casi no movió el error. No te confíes: ahí el leakage tuvo efecto mínimo porque el
dataset es grande (~7.400 filas) y los estadísticos de train casi igualan los del total, **no** porque el
escalado no importe (de hecho escalar mueve mucho a un KNN). El leakage se vuelve **catastrófico** cuando
el paso que filtra información **usa la variable objetivo** (`y`) — por ejemplo, **seleccionar las
variables más correlacionadas con `y`** mirando *todos* los datos antes de validar.

Para verlo sin lugar a dudas montamos el experimento clásico: un objetivo que es **ruido puro** y cientos
de variables que también son **ruido puro**. **La verdad es que no hay nada que predecir**, así que
cualquier evaluación honesta debe dar un R² de aproximadamente **cero o negativo**.

- **Con leakage**: elegimos las 20 variables "más correlacionadas con `y`" usando **todo** el dataset, y
  *luego* validamos. Por azar, algunas de esas variables-ruido parecen predictivas → R² **falsamente alto**.
- **Sin leakage**: metemos la selección **dentro del pipeline**, así se re-hace en cada partición usando
  solo su train → el espejismo se desvanece y el R² cae a su valor honesto (≈0 o negativo).

Esta es la demostración de por qué el pipeline no es opcional: **te protege de engañarte a ti mismo**."""

S6_CODE = """from sklearn.feature_selection import SelectKBest, f_regression

# Mundo de ruido puro: y no depende de NADA. Cualquier R2 honesto debe ser ~0 o negativo.
rng = np.random.default_rng(0)
n_obs, n_vars = 200, 1000
X_ruido = rng.standard_normal((n_obs, n_vars))
y_ruido = rng.standard_normal(n_obs)              # objetivo independiente de las variables
cv6 = KFold(n_splits=5, shuffle=True, random_state=42)

# (A) CON LEAKAGE: seleccionar las 20 "mejores" mirando TODO, y recién después validar
selector = SelectKBest(f_regression, k=20).fit(X_ruido, y_ruido)   # ¡miró y_ruido completo!
X_elegidas = selector.transform(X_ruido)
r2_con_leak = cross_val_score(LinearRegression(), X_elegidas, y_ruido, cv=cv6, scoring="r2").mean()

# (B) SIN LEAKAGE: la selección vive DENTRO del pipeline (se re-hace por partición, solo con su train)
pipe_honesto = Pipeline([("seleccion", SelectKBest(f_regression, k=20)), ("modelo", LinearRegression())])
r2_honesto = cross_val_score(pipe_honesto, X_ruido, y_ruido, cv=cv6, scoring="r2").mean()

print(f"R² CON leakage (selección sobre TODO):       {r2_con_leak:+.3f}   <- ¡espejismo, parece que predice!")
print(f"R² SIN leakage (selección dentro del pipe):  {r2_honesto:+.3f}   <- la verdad: no hay señal")

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.bar(["Con leakage\\n(fuera del pipe)", "Sin leakage\\n(dentro del pipe)"],
       [r2_con_leak, r2_honesto], color=["#c0392b", "#0a7e7e"])
ax.axhline(0, color="gray", lw=1)
ax.set_ylabel("R² (validación cruzada)")
ax.set_title("El mismo dato, dos formas de validar: el leakage INVENTA señal")
plt.tight_layout(); plt.show()

print("\\nMisma data, misma métrica: solo cambió DÓNDE se hizo la selección. El leakage te miente.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Preprocesar antes de separar** (escalar/imputar/seleccionar con estadísticos de *todo* el dataset). Es la fuga más silenciosa: separa **primero**.
- **Hacer `fit` del escalador con train + test.** El `fit` mira **solo** el train; el `transform` se aplica a ambos.
- **Seleccionar variables por su correlación con `y` usando todos los datos.** Es leakage **catastrófico**: la selección va **dentro** del pipeline.
- **Confiar en una métrica sin semilla.** Sin `random_state` el número es **anecdótico**, no reproducible.
- **Servir solo el modelo y olvidar la preparación.** Guarda y versiona el **pipeline completo**: train y serve deben transformar **idéntico**.
- **Creer que el pipeline es solo para escribir menos.** Es un **contrato** que evita el olvido que te arruina la métrica."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan algo, **todos** piden **elegir la interpretación
correcta**. Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 leakage infla la métrica ----
E1 = """## Ejercicio 01 · El leakage infla la métrica
Reusa el experimento de ruido puro de la sección 6 (`X_ruido`, `y_ruido`, `cv6`). Recuerda: **no hay
nada que predecir**, así que la evaluación honesta debe dar un R² ≈ 0 o negativo.

- Guarda en `r2_con_leak` el R² **seleccionando las 20 mejores variables sobre TODO** `X_ruido` y luego
  validando con `LinearRegression` (leakage).
- Guarda en `r2_honesto` el R² con la **selección dentro de un `Pipeline`** (sin leakage).
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** Ambos R² son parecidos: dónde se hace la selección no cambia nada.
  - **B.** El R² con leakage es claramente **mayor**: la fuga **inventa** señal donde no la hay y tu
    métrica queda falsamente buena.
  - **C.** El R² honesto es mayor: meter la selección en el pipeline mejora el modelo real.

Pista: usa `SelectKBest(f_regression, k=20)` y `cross_val_score(..., cv=cv6, scoring="r2").mean()`."""
E1_TODO = """from sklearn.feature_selection import SelectKBest, f_regression
# (X_ruido, y_ruido, cv6 vienen de la sección 6)
r2_con_leak = None   # TODO: seleccionar 20 mejores sobre TODO X_ruido, luego cross_val_score con LinearRegression
r2_honesto = None    # TODO: selección DENTRO de un Pipeline, luego cross_val_score
conclusion = None    # TODO: "A", "B" o "C"
"""
E1_SOL = """from sklearn.feature_selection import SelectKBest, f_regression
_sel = SelectKBest(f_regression, k=20).fit(X_ruido, y_ruido)
r2_con_leak = cross_val_score(LinearRegression(), _sel.transform(X_ruido), y_ruido, cv=cv6, scoring="r2").mean()
_pipe = Pipeline([("seleccion", SelectKBest(f_regression, k=20)), ("modelo", LinearRegression())])
r2_honesto = cross_val_score(_pipe, X_ruido, y_ruido, cv=cv6, scoring="r2").mean()
conclusion = "B"
"""
E1_CHK = """try:
    from sklearn.feature_selection import SelectKBest, f_regression
    _s = SelectKBest(f_regression, k=20).fit(X_ruido, y_ruido)
    _leak = cross_val_score(LinearRegression(), _s.transform(X_ruido), y_ruido, cv=cv6, scoring="r2").mean()
    _p = Pipeline([("seleccion", SelectKBest(f_regression, k=20)), ("modelo", LinearRegression())])
    _hon = cross_val_score(_p, X_ruido, y_ruido, cv=cv6, scoring="r2").mean()
    _correcta = "B" if _leak > _hon else "A"
    assert r2_con_leak is not None and abs(r2_con_leak - _leak) < 1e-6, f"r2_con_leak debería ser ~{_leak:.3f}"
    assert r2_honesto is not None and abs(r2_honesto - _hon) < 1e-6, f"r2_honesto debería ser ~{_hon:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿qué R² es más alto, el que vio la prueba o el honesto?"
    print(f"✅ Correcto. Con leakage R²={_leak:+.3f} (espejismo); honesto R²={_hon:+.3f}. La fuga infla la métrica.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 semilla determinismo ----
E2 = """## Ejercicio 02 · Reproducibilidad con la semilla
Trabaja con `idx = np.arange(len(df))`.

- Separa con `train_test_split(idx, test_size=0.3, random_state=42)` y guarda en `test_a` el segundo
  resultado (las filas de **prueba**). Hazlo otra vez igual y guárdalo en `test_b`.
- Separa con `random_state=7` y guarda las filas de prueba en `test_c`.
- Guarda en `iguales_misma` el booleano `np.array_equal(test_a, test_b)` y en `iguales_distinta` el
  booleano `np.array_equal(test_a, test_c)`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** El `random_state` no influye: las tres separaciones dan las mismas filas.
  - **B.** Misma semilla ⇒ **mismo** split (reproducible); semilla distinta ⇒ **otro** split. Por eso se
    fija `random_state` para que el resultado sea repetible.
  - **C.** Cada ejecución da filas distintas aunque repitas la semilla: el azar nunca se puede fijar.

Pista: el segundo elemento de `train_test_split` es el conjunto de prueba."""
E2_TODO = """idx = np.arange(len(df))
test_a = None           # TODO: prueba con random_state=42
test_b = None           # TODO: prueba con random_state=42 (otra vez)
test_c = None           # TODO: prueba con random_state=7
iguales_misma = None    # TODO: np.array_equal(test_a, test_b)
iguales_distinta = None # TODO: np.array_equal(test_a, test_c)
conclusion = None       # TODO: "A", "B" o "C"
"""
E2_SOL = """idx = np.arange(len(df))
test_a = train_test_split(idx, test_size=0.3, random_state=42)[1]
test_b = train_test_split(idx, test_size=0.3, random_state=42)[1]
test_c = train_test_split(idx, test_size=0.3, random_state=7)[1]
iguales_misma = np.array_equal(test_a, test_b)
iguales_distinta = np.array_equal(test_a, test_c)
conclusion = "B"
"""
E2_CHK = """try:
    _idx = np.arange(len(df))
    _a = train_test_split(_idx, test_size=0.3, random_state=42)[1]
    _b = train_test_split(_idx, test_size=0.3, random_state=42)[1]   # repetir con la MISMA semilla
    _c = train_test_split(_idx, test_size=0.3, random_state=7)[1]
    _im = bool(np.array_equal(_a, _b))           # misma semilla => True (dos splits independientes)
    _id = bool(np.array_equal(_a, _c))           # distinta semilla => False
    _correcta = "B" if (_im and not _id) else "A"
    assert iguales_misma is not None and bool(iguales_misma) == _im, "Revisa iguales_misma (misma semilla)."
    assert iguales_distinta is not None and bool(iguales_distinta) == _id, "Revisa iguales_distinta (otra semilla)."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿qué garantiza repetir la misma semilla?"
    print(f"✅ Correcto. Misma semilla => mismo split ({_im}); semilla distinta => otro split ({_id}). Reproducible.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 fit solo en train ----
E3 = """## Ejercicio 03 · `fit` solo en train (sin fuga)
Separa con `train_test_split(X, y, test_size=0.3, random_state=42)` en `Xtr3, Xte3, ytr3, yte3` y entrena
un `StandardScaler` **solo con `Xtr3`** (guárdalo en `sc3`).

- Guarda en `media_scaler` la media que aprendió para la columna `cantidad` (`sc3.mean_[0]`).
- Guarda en `media_train` la media real de `Xtr3["cantidad"]` y en `media_todo` la de `X["cantidad"]`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** La media del escalador coincide con la de **todo** el dataset: hizo `fit` con train + test.
  - **B.** La media del escalador coincide con la de **solo el train**: el `fit` miró únicamente el
    entrenamiento, sin filtrar la prueba.
  - **C.** No se puede saber con qué datos hizo `fit` el escalador."""
E3_TODO = """Xtr3 = Xte3 = ytr3 = yte3 = None   # TODO: train_test_split(X, y, test_size=0.3, random_state=42)
sc3 = None              # TODO: StandardScaler().fit(Xtr3)
media_scaler = None     # TODO: sc3.mean_[0]
media_train = None      # TODO: media real de Xtr3["cantidad"]
media_todo = None       # TODO: media de X["cantidad"]
conclusion = None       # TODO: "A", "B" o "C"
"""
E3_SOL = """Xtr3, Xte3, ytr3, yte3 = train_test_split(X, y, test_size=0.3, random_state=42)
sc3 = StandardScaler().fit(Xtr3)
media_scaler = sc3.mean_[0]
media_train = Xtr3["cantidad"].mean()
media_todo = X["cantidad"].mean()
conclusion = "B"
"""
E3_CHK = """try:
    _Xtr, _Xte, _ytr, _yte = train_test_split(X, y, test_size=0.3, random_state=42)
    _sc = StandardScaler().fit(_Xtr)
    _ms = _sc.mean_[0]
    _mt = _Xtr["cantidad"].mean()
    _mtodo = X["cantidad"].mean()
    _correcta = "B" if np.isclose(_ms, _mt) and not np.isclose(_ms, _mtodo) else "A"
    assert media_scaler is not None and abs(media_scaler - _ms) < 1e-6, "Revisa media_scaler (sc3.mean_[0])."
    assert media_train is not None and abs(media_train - _mt) < 1e-6, "Revisa media_train."
    assert media_todo is not None and abs(media_todo - _mtodo) < 1e-6, "Revisa media_todo."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿con qué media coincide la del escalador?"
    print(f"✅ Correcto. media_scaler={_ms:.2f} = media_train={_mt:.2f} (no la de todo={_mtodo:.2f}): fit solo en train.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 train/serve consistencia (conceptual) ----
E4 = """## Ejercicio 04 · Consistencia train/serve y versionado (conceptual)
Un equipo entrena un pipeline (escalado + one-hot + modelo) y obtiene buen error en validación. Al
llevarlo a producción, **guardan solo el modelo** (no el pipeline) y, al servir cada compra nueva, la
pasan **sin escalar ni codificar**. En producción las predicciones salen disparatadas, aunque "no se
rompe" nada.

Elige en `conclusion` (letra) la lectura correcta:
- **A.** El modelo se "echó a perder" al guardarlo; hay que reentrenar con más datos.
- **B.** Es **train/serve skew**: al servir hay que aplicar **exactamente** la misma preparación que al
  entrenar. La solución es **versionar y servir el pipeline completo** (con `joblib`), no el modelo suelto.
- **C.** Da lo mismo cómo se sirva: si el error de validación fue bueno, producción también lo será.

*(Opcional, no se corrige): en `reflexion` escribe qué guardarías y versionarías para que train y serve
sean idénticos.)*"""
E4_TODO = """conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """conclusion = "B"
reflexion = "Guardaría y versionaría el PIPELINE completo con joblib (preprocesamiento + modelo), más la versión de las librerías, para que la transformación al servir sea idéntica a la del entrenamiento."
"""
E4_CHK = """try:
    assert conclusion is not None, "Aún no elegiste una letra en 'conclusion'."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿qué pasa si al servir NO aplicas la misma preparación que al entrenar?"
    print("✅ Correcto. Train y serve deben transformar idéntico: por eso se versiona y sirve el PIPELINE completo.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir conclusion:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *armas* un pipeline: entiendes **por qué** existe. Sabes qué es el **leakage** y que puede ser
**catastrófico**, dominas la regla **`fit` solo en train / `transform` en ambos**, ves el pipeline como un
**contrato** que evita el olvido, fijas **semillas** para que tus números sean **reproducibles**, y
cuidas la consistencia **train/serve** versionando el pipeline completo.

La regla de oro que te llevas: **separa antes de preparar, y sirve exactamente lo que entrenaste.** Eso
distingue una métrica honesta de un espejismo — y en decisiones públicas, esa diferencia importa.

> **Hacia dónde sigue:** en **B6 · Despliegue** tomarás este pipeline versionado y lo expondrás en una API
> para que cualquier sistema de compras del Estado prediga en tiempo real, con la misma transformación de
> siempre."""


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
