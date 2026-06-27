# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B3 (modelos de árboles):
B3/profundiza.ipynb (estudiante) + B3/profundiza_solucion.ipynb (resuelto).

Más teórico que la lección: explica el *porqué* (cómo decide un árbol por impureza,
por qué solo sobreajusta, bagging vs boosting, y las trampas de la importancia de
variables). Demos de código real sobre compras_ml.csv. Corre offline con
pandas/numpy/scikit-learn/matplotlib."""
import json, os

BASE = "B3-modelos-de-arboles"

TITULO = """# B3 · Modelos de árboles — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B3 —donde entrenaste árboles y un bosque
aleatorio— aquí vamos al *porqué*, no al *cómo*: **cómo decide** un árbol por dentro (la idea de
**impureza**: cuán "mezclado" está un nodo y por qué la mejor pregunta es la que más lo ordena), por
qué un árbol suelto **solo sabe sobreajustar** (memoriza si lo dejas crecer), la diferencia de fondo
entre **bagging** (promediar muchos árboles independientes) y **boosting** (corregir errores uno tras
otro), y las **trampas de la importancia de variables** —una cifra que en el sector público se usa para
justificar decisiones, y que engaña con facilidad.

Menos código nuevo, más **modelo mental**. Todo corre **offline** con scikit-learn; los ejercicios del
final son más conceptuales y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de B3. Mismo dataset: `compras_ml.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("compras_ml.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B3-modelos-de-arboles/compras_ml.csv"
        urllib.request.urlretrieve(url, "compras_ml.csv")
    except Exception:
        print("Si estás en Colab, sube compras_ml.csv manualmente.")

df = pd.read_csv("compras_ml.csv")

# Para razonar sobre IMPUREZA necesitamos una pregunta de SÍ/NO (clasificación).
# Inventamos una etiqueta clara: ¿la compra es "cara"? = monto por encima de la mediana.
# Queda balanceada ~50/50 a propósito, para que la impureza se vea nítida.
df["caro"] = (df["monto_total"] > df["monto_total"].median()).astype(int)

print(f"{len(df)} compras cargadas | columnas: {list(df.columns)}")
print(f"Etiqueta 'caro' (monto > mediana): {df['caro'].mean():.0%} de las compras son 'caras'.")"""

# ───────────────────────── Sección 1 ─────────────────────────
S1 = """## 1. Cómo decide un árbol: la idea de impureza (Gini)

En la lección, un árbol predecía con una **secuencia de preguntas sí/no**. Pero ¿*cómo* elige cada
pregunta? La respuesta es una sola idea, y es preciosa: el árbol busca **ordenar**.

Imagina un nodo del árbol como una **caja con compras adentro**, cada una con una etiqueta (acá:
"cara" o "barata"). Un nodo está **mezclado** si tiene de las dos, y está **puro** si dentro hay puras
"caras" (o puras "baratas"). La **impureza de Gini** pone número a ese "cuán mezclado":

$$\\text{Gini} = 1 - \\sum_k p_k^2$$

donde $p_k$ es la proporción de cada etiqueta en el nodo. Intuición sin fórmula:

- Nodo **puro** (todo de una clase) → Gini = **0**. No hay nada que decidir, ya sabes la respuesta.
- Nodo **lo más mezclado posible** (mitad y mitad, dos clases) → Gini = **0,5**, el máximo. Es pura duda.
- Para dos clases, el Gini cae siempre en el **rango cerrado [0, 0,5]**: 0 si el nodo es puro, **0,5
  exacto** si está justo mitad y mitad, y cualquier valor intermedio en el resto de los casos. (Por eso
  más abajo la **raíz**, casi mitad y mitad por construcción, imprime Gini = 0,500.)

> 🧠 **Analogía pública.** Es la "incertidumbre" de una ventanilla. Si a una mesa solo llegan trámites
> de un tipo, sabes exactamente qué hacer (impureza 0). Si llega mitad licitaciones y mitad tratos
> directos revueltos, cada caso es una moneda al aire (impureza máxima). El árbol arma preguntas para
> que a cada mesa lleguen casos lo más **parecidos** posible.

La **entropía** es otra medida de lo mismo (mezcla); Gini es la que usa scikit-learn por defecto porque
es más rápida y, en la práctica, dan árboles casi idénticos. Calculemos Gini **a mano** de un nodo real."""

S1_CODE = """def gini(serie):
    \"\"\"Impureza de Gini de una columna de etiquetas 0/1 (o cualquier categoría).\"\"\"
    if len(serie) == 0:
        return 0.0
    props = serie.value_counts(normalize=True)   # proporción de cada clase
    return 1 - (props ** 2).sum()

# Nodo RAÍZ: todas las compras juntas (la caja sin abrir)
g_raiz = gini(df["caro"])
print(f"Gini de la raíz (todas las compras): {g_raiz:.3f}   <- cerca de 0,5: muy mezclado")

# Un NODO cualquiera: las compras de pocos artículos (cantidad <= 10)
nodo = df[df["cantidad"] <= 10]["caro"]
g_nodo = gini(nodo)
print(f"\\nNodo 'cantidad <= 10':  n={len(nodo)}  |  {nodo.mean():.0%} caras  |  Gini = {g_nodo:.3f}")
print("Bajó de 0,50 a ~0,35: este grupo está MENOS mezclado (la mayoría son baratas).")
print("Un Gini de 0 sería un nodo puro; 0,5 el más revuelto. 0,35 = parcialmente ordenado.")"""

# ───────────────────────── Sección 2 ─────────────────────────
S2 = """## 2. La mejor división es la que más reduce la impureza

Ya tenemos la regla de oro del árbol: **probar muchas preguntas posibles y quedarse con la que deja los
dos grupos resultantes lo más puros posible.** Eso se mide con la **reducción de impureza**:

$$\\text{reducción} = \\text{Gini(padre)} - \\big[\\,w_{izq}\\cdot\\text{Gini(izq)} + w_{der}\\cdot\\text{Gini(der)}\\,\\big]$$

donde $w$ es el **peso** (la fracción de datos que cae a cada lado). Es decir: la impureza del nodo
padre, menos el **promedio ponderado** de la impureza de los dos hijos. Mientras más baje, mejor la
pregunta. El árbol hace esto en **cada** nodo, de forma **codiciosa** (*greedy*): elige la mejor pregunta
del momento, sin mirar el futuro.

> 🧠 **Analogía pública.** Es diseñar el formulario de admisión perfecto. ¿Qué primera pregunta separa
> mejor a quienes califican de quienes no? La que, al responderla, deje cada montón lo más **homogéneo**
> posible, para no tener que seguir preguntando. El árbol prueba todas y se queda con la campeona.

Comparemos dos preguntas candidatas sobre nuestros datos y veamos **cuál ordena más**."""

S2_CODE = """def gini_split(df_, columna, umbral):
    \"\"\"Gini ponderado de los dos hijos al dividir por 'columna <= umbral'.\"\"\"
    izq = df_[df_[columna] <= umbral]["caro"]
    der = df_[df_[columna] >  umbral]["caro"]
    n = len(df_)
    w_izq, w_der = len(izq) / n, len(der) / n
    return w_izq * gini(izq) + w_der * gini(der)

g_padre = gini(df["caro"])

# Candidata A: ¿cantidad <= 10?     Candidata B: ¿tamano_num <= 2 (Micro/Pequeña)?
g_A = gini_split(df, "cantidad", 10)
g_B = gini_split(df, "tamano_num", 2)
red_A = g_padre - g_A
red_B = g_padre - g_B

print(f"Gini del padre: {g_padre:.3f}\\n")
print(f"A) dividir por 'cantidad <= 10'      -> hijos: {g_A:.3f}  | reducción: {red_A:.3f}")
print(f"B) dividir por 'tamano_num <= 2'     -> hijos: {g_B:.3f}  | reducción: {red_B:.3f}")
mejor = "A (cantidad)" if red_A > red_B else "B (tamano_num)"
print(f"\\nGana {mejor}: reduce MÁS la impureza, así que es la pregunta que el árbol elegiría primero.")"""

# ───────────────────────── Sección 3 ─────────────────────────
S3 = """## 3. Por qué un árbol, solo, únicamente sabe sobreajustar

Aquí está la debilidad de fondo del árbol individual, y conviene entenderla bien. Su regla —dividir
hasta dejar los nodos puros— **no tiene freno natural**. Si lo dejas crecer sin límite, seguirá haciendo
preguntas cada vez más específicas hasta aislar **cada compra rara en su propia hojita**. En ese punto
la impureza de entrenamiento llega a **cero**: el árbol no aprendió el patrón, se **memorizó la lista**.

> 🧠 **Analogía pública.** Es el funcionario que, en vez de aprender el *criterio* de una norma, se
> aprende de memoria la resolución de **cada expediente pasado**. Con los casos viejos es perfecto. Pero
> llega un caso nuevo —que no está en su lista— y no sabe qué hacer, porque nunca entendió la regla.

Por eso un árbol suelto es **inestable** y casi siempre sobreajusta: cambias unos pocos datos y el árbol
cambia entero. Su error de **entrenamiento** baja y baja con la profundidad… mientras el de **prueba**
(los datos nuevos, los que importan) primero baja y luego **sube**. Esa brecha que se abre es la firma
del sobreajuste. Vamos a *verla* dejando crecer un árbol sin límite."""

S3_CODE = """from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Le damos MUCHAS columnas (one-hot de categoría y región) para que tenga dónde memorizar
X = pd.get_dummies(df[["cantidad", "tamano_num", "categoria", "region_comprador"]], drop_first=False)
y = df["monto_total"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=42)

# Árbol SIN límite de profundidad: crece hasta memorizar
arbol = DecisionTreeRegressor(random_state=42).fit(X_tr, y_tr)
mae_train = mean_absolute_error(y_tr, arbol.predict(X_tr))
mae_test  = mean_absolute_error(y_te, arbol.predict(X_te))

print(f"Profundidad a la que creció el árbol: {arbol.get_depth()}  ({arbol.get_n_leaves()} hojas)")
print(f"MAE en ENTRENAMIENTO (datos vistos):  {mae_train:,.0f} CLP")
print(f"MAE en PRUEBA       (datos nuevos):   {mae_test:,.0f} CLP")
print(f"\\nEl error de prueba es {mae_test/mae_train:.1f}× el de entrenamiento: esa brecha = sobreajuste.")
print("El árbol no entendió el patrón, se memorizó las compras de entrenamiento.")"""

# ───────────────────────── Sección 4 ─────────────────────────
S4 = """## 4. La cura: muchos árboles. Bagging vs Boosting

Si un árbol solo es inestable y memorión, la idea genial es **no usar uno, sino un comité de muchos** (un
*ensemble*). Hay dos filosofías para armar ese comité, y conviene distinguirlas porque resuelven
problemas distintos:

**Bagging (lo que hace el Random Forest de la lección).** Entrena **muchos árboles independientes**, cada
uno sobre una **muestra al azar** de los datos (y mirando solo algunas columnas al azar en cada
división). Luego **promedia** sus predicciones. La gracia: cada árbol se equivoca distinto, y al promediar,
los errores **se cancelan**. Baja la varianza y la inestabilidad.

> 🧠 **Analogía: la sabiduría de la multitud.** En vez de una comisión revisora de **una** persona
> (que puede tener un mal día), juntas **muchas** opiniones **independientes** y promedias. El promedio
> es más estable y suele acertar más que cualquier voto individual.

**Boosting (XGBoost, LightGBM…).** Entrena árboles **uno tras otro, en secuencia**: cada árbol nuevo se
concentra en **corregir los errores** que dejó el anterior. No son independientes; cada uno arregla lo
que el comité aún hace mal.

> 🧠 **Analogía: la cadena de revisores.** El primer revisor hace una pasada; el segundo se enfoca **solo
> en lo que el primero falló**; el tercero, en lo que aún queda mal… El equipo afina el resultado paso a
> paso.

La diferencia clave: **bagging promedia errores independientes** (reduce *varianza*, es robusto y difícil
de arruinar); **boosting corrige errores secuencialmente** (suele dar más precisión, pero es más sensible
y puede sobreajustar si te pasas de árboles). Veamos al bagging (Random Forest) **arreglando** el árbol
memorión de la sección anterior.

> ⚠️ **Lee los números con cuidado.** En *este* dataset el bagging arregla sobre todo la **brecha**
> entrenamiento–prueba (el sobreajuste), no tanto el error de prueba en sí: el MAE de prueba apenas
> baja. Es porque el monto tiene mucha **varianza irreducible** —ruido que ningún modelo puede predecir
> con estas columnas—. Lo que el bosque sí hace siempre es **estabilizar** y dejar de memorizar; en
> datasets más complejos, además, baja el MAE de prueba de forma clara."""

S4_CODE = """from sklearn.ensemble import RandomForestRegressor

# Mismo split; comparamos el árbol suelto contra un bosque (bagging de 100 árboles)
bosque = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_tr, y_tr)
mae_bosque_train = mean_absolute_error(y_tr, bosque.predict(X_tr))
mae_bosque_test  = mean_absolute_error(y_te, bosque.predict(X_te))

print("                         MAE entrenamiento     MAE prueba")
print(f"Árbol suelto (memorión)   {mae_train:>10,.0f}        {mae_test:>10,.0f}")
print(f"Bosque (bagging, 100)     {mae_bosque_train:>10,.0f}        {mae_bosque_test:>10,.0f}")
print()
gap_arbol  = mae_test - mae_train
gap_bosque = mae_bosque_test - mae_bosque_train
print(f"\\nBrecha (prueba - entrenamiento):  árbol suelto {gap_arbol:,.0f}  ->  bosque {gap_bosque:,.0f} CLP")
print("El árbol suelto tiene un entrenamiento casi perfecto y una brecha enorme (memorizó).")
print("El bosque tiene una brecha MUCHO menor: cada árbol memoriza distinto y al promediar")
print("esos errores se cancelan. Es más honesto y más estable. Esa es la magia del bagging.")
print("\\nOJO con los números: aquí el MAE de PRUEBA casi no cambió (este dataset tiene mucha")
print("varianza irreducible: el monto no se deja predecir del todo con estas columnas). Lo que")
print("SÍ se redujo fue la BRECHA (el sobreajuste). En datasets más complejos el bagging")
print("además baja el MAE de prueba; aquí su aporte visible es estabilizar, no adivinar mejor.")"""

# ───────────────────────── Sección 5 ─────────────────────────
S5 = """## 5. La trampa: la "importancia de variables" engaña

El Random Forest regala un número irresistible: `feature_importances_`, "cuánto pesó cada variable". En
el sector público es tentador leerlo como *"esto es lo que más influye, ataquemos esto"*. **Cuidado.** Esa
cifra mide cuánto **usó** el modelo cada columna para dividir, y eso se distorsiona de tres formas:

1. **Sesgo hacia la alta cardinalidad.** Las variables con **muchos valores distintos** (montos, IDs,
   fechas, un número continuo cualquiera) ofrecen **muchísimos cortes posibles**, así que el árbol las
   usa más y **parecen** importantes… aunque sean **puro ruido**. Lo demostraremos abajo: meteremos una
   columna **totalmente aleatoria** y veremos cómo el modelo le asigna una importancia alta.
2. **Variables correlacionadas se reparten el crédito.** Si dos columnas dicen casi lo mismo, el bosque
   reparte la importancia entre ambas, y cada una se ve **menos** importante de lo que realmente es (o
   una se "roba" todo el crédito por azar).
3. **Importancia ≠ causalidad.** Que una variable sea útil para *predecir* **no** significa que *cause* el
   resultado, ni que moverla cambie nada. Predecir y explicar son cosas distintas.

> 🧠 **Analogía pública.** El termómetro es un excelente **predictor** de fiebre, pero romperlo no te
> baja la fiebre. Una variable puede "pesar" mucho en el modelo y ser solo un **síntoma**, no una palanca.

Hagamos el experimento del ruido: si una columna inventada al azar saca importancia alta, ya sabes que
esta cifra **no se lee sola**."""

S5_CODE = """from sklearn.ensemble import RandomForestRegressor

rng = np.random.default_rng(7)
df_exp = df.copy()
df_exp["ruido_aleatorio"] = rng.normal(size=len(df_exp))   # columna SIN relación con el monto

X_exp = df_exp[["cantidad", "tamano_num", "ruido_aleatorio"]]
rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_exp, df_exp["monto_total"])
imp = pd.Series(rf.feature_importances_, index=X_exp.columns).sort_values(ascending=False)

print("Importancia de variables (incluye una columna de RUIDO puro):")
for var, val in imp.items():
    print(f"  {var:>16}: {val:.1%}")

print(f"\\n'ruido_aleatorio' no tiene NINGUNA relación con el monto, pero saca {imp['ruido_aleatorio']:.0%}.")
print("¿Por qué? Es un número continuo (alta cardinalidad): ofrece infinitos cortes y el árbol lo usa.")

fig, ax = plt.subplots(figsize=(7, 3.2))
colores = ["#0a7e7e" if v != "ruido_aleatorio" else "crimson" for v in imp.index]
ax.barh(imp.index[::-1], imp.values[::-1], color=colores[::-1])
ax.set_title("Importancia de variables (en rojo: ruido puro que 'parece' importante)")
ax.set_xlabel("Importancia"); plt.tight_layout(); plt.show()"""

# ───────────────────────── Errores ─────────────────────────
ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Creer que un árbol más profundo es "mejor".** Sin límite, solo memoriza: error de entrenamiento 0 y prueba pésima. Controla la complejidad (`max_depth`, o usa un bosque).
- **Confiar en un solo árbol para decisiones.** Es inestable: cambian unos datos y cambia entero. Para robustez, usa un *ensemble* (bagging/boosting).
- **Confundir bagging con boosting.** *Bagging* promedia árboles **independientes** (reduce varianza, robusto); *boosting* corrige errores **en secuencia** (más preciso, más delicado).
- **Leer `feature_importances_` como verdad.** Está **sesgada hacia variables de alta cardinalidad** (montos, IDs) y reparte mal el crédito entre variables **correlacionadas**.
- **Saltar de "importante" a "causa".** La importancia mide utilidad para **predecir**, no **causalidad**. El termómetro predice la fiebre; romperlo no la cura.
- **No fijar `random_state`.** Árboles y bosques usan azar; sin semilla, tus resultados no son reproducibles."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan algo, **todos** piden **elegir la interpretación
correcta**. Completa cada `TODO` y ejecuta la celda de chequeo."""

# ───────────────────────── E1: Gini de un nodo ─────────────────────────
E1 = """## Ejercicio 01 · Calcular la impureza de un nodo
Usa la función `gini` (definida en la sección 1) sobre la etiqueta `caro` de un **nodo concreto**: las
compras de proveedores **chicos**, `tamano_num <= 2` (Micro o Pequeña).

- Guarda en `g_nodo` la impureza de Gini de ese grupo: `gini(df[df["tamano_num"] <= 2]["caro"])`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** `g_nodo` es 0: el nodo es **puro**, todas las compras son de la misma clase.
  - **B.** `g_nodo` está en el **rango (0, 0,5]**: el nodo sigue **mezclado**, no es puro; el árbol
    querría seguir dividiéndolo para ordenarlo más.
  - **C.** `g_nodo` es mayor que 0,5: imposible para dos clases, hay un error."""
E1_TODO = """g_nodo = None        # TODO: gini de la etiqueta 'caro' del nodo tamano_num <= 2
conclusion = None    # TODO: "A", "B" o "C"
"""
E1_SOL = """g_nodo = gini(df[df["tamano_num"] <= 2]["caro"])
conclusion = "B"
"""
E1_CHK = """try:
    _g = gini(df[df["tamano_num"] <= 2]["caro"])
    # Derivamos la letra correcta desde el número, sin hardcodear:
    if _g <= 1e-9:
        _correcta = "A"
    elif _g > 0.5 + 1e-9:
        _correcta = "C"
    else:
        _correcta = "B"
    assert g_nodo is not None and abs(g_nodo - _g) < 1e-6, f"g_nodo debería ser ~{_g:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿este nodo es puro (0), mezclado (0-0,5) o imposible (>0,5)?"
    print(f"✅ Correcto. Gini = {_g:.3f}: el nodo está mezclado (en el rango (0, 0,5]), no es puro.")
    print("   Por eso el árbol seguiría buscando preguntas para ordenarlo más.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ───────────────────────── E2: mejor split ─────────────────────────
E2 = """## Ejercicio 02 · ¿Cuál pregunta divide mejor?
El árbol elige la pregunta que **más reduce la impureza**. Compara dos candidatas usando `gini_split`
(sección 2) y la impureza del padre `gini(df["caro"])`:

- Candidata A: `gini_split(df, "cantidad", 10)`  → guárdala en `gini_A`.
- Candidata B: `gini_split(df, "tamano_num", 2)` → guárdala en `gini_B`.

Recuerda: **menor** Gini de los hijos = **mayor** reducción = mejor pregunta.

Elige en `conclusion` la interpretación correcta:
- **A.** Gana la candidata **A** (`cantidad <= 10`): deja los hijos menos mezclados, reduce más la impureza.
- **B.** Gana la candidata **B** (`tamano_num <= 2`): deja los hijos menos mezclados.
- **C.** Da exactamente lo mismo: las dos preguntas dividen igual de bien."""
E2_TODO = """gini_A = None        # TODO: gini_split(df, "cantidad", 10)
gini_B = None        # TODO: gini_split(df, "tamano_num", 2)
conclusion = None    # TODO: "A", "B" o "C"
"""
E2_SOL = """gini_A = gini_split(df, "cantidad", 10)
gini_B = gini_split(df, "tamano_num", 2)
conclusion = "A"
"""
E2_CHK = """try:
    _gA = gini_split(df, "cantidad", 10)
    _gB = gini_split(df, "tamano_num", 2)
    # La mejor es la de MENOR gini de hijos. Derivamos la letra desde los números:
    if abs(_gA - _gB) < 1e-9:
        _correcta = "C"
    elif _gA < _gB:
        _correcta = "A"
    else:
        _correcta = "B"
    assert gini_A is not None and abs(gini_A - _gA) < 1e-6, f"gini_A debería ser ~{_gA:.3f}"
    assert gini_B is not None and abs(gini_B - _gB) < 1e-6, f"gini_B debería ser ~{_gB:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa cuál deja los hijos MENOS mezclados (menor Gini)."
    print(f"✅ Correcto. Gini hijos A={_gA:.3f} vs B={_gB:.3f}: gana la {_correcta}, reduce más la impureza.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ───────────────────────── E3: sobreajuste ─────────────────────────
E3 = """## Ejercicio 03 · Medir el sobreajuste de un árbol suelto
Reusa el árbol sin límite ya entrenado en la sección 3 (`arbol`, `X_tr`, `X_te`, `y_tr`, `y_te`).

- Guarda en `mae_train` el MAE en **entrenamiento** y en `mae_test` el MAE en **prueba**.
  Pista: `mean_absolute_error(y_tr, arbol.predict(X_tr))` y lo mismo con el set de prueba.
- Guarda en `brecha` el cociente `mae_test / mae_train`.

Elige en `conclusion` la lectura correcta:
- **A.** `mae_train` ≈ `mae_test`: el árbol generaliza perfecto, no hay sobreajuste.
- **B.** `mae_test` es **bastante mayor** que `mae_train` (brecha > 1,5): el árbol **memorizó** el
  entrenamiento y generaliza peor. Eso es sobreajuste.
- **C.** `mae_train` es mayor que `mae_test`: el árbol predice mejor lo que nunca vio."""
E3_TODO = """mae_train = None     # TODO: MAE en entrenamiento (y_tr vs arbol.predict(X_tr))
mae_test = None      # TODO: MAE en prueba (y_te vs arbol.predict(X_te))
brecha = None        # TODO: mae_test / mae_train
conclusion = None    # TODO: "A", "B" o "C"
"""
E3_SOL = """mae_train = mean_absolute_error(y_tr, arbol.predict(X_tr))
mae_test = mean_absolute_error(y_te, arbol.predict(X_te))
brecha = mae_test / mae_train
conclusion = "B"
"""
E3_CHK = """try:
    _mtr = mean_absolute_error(y_tr, arbol.predict(X_tr))
    _mte = mean_absolute_error(y_te, arbol.predict(X_te))
    _br = _mte / _mtr
    # Derivamos la letra desde la brecha real:
    if _mtr > _mte:
        _correcta = "C"
    elif _br > 1.5:
        _correcta = "B"
    else:
        _correcta = "A"
    assert mae_train is not None and abs(mae_train - _mtr) < 1.0, f"mae_train debería ser ~{_mtr:,.0f}"
    assert mae_test is not None and abs(mae_test - _mte) < 1.0, f"mae_test debería ser ~{_mte:,.0f}"
    assert brecha is not None and abs(brecha - _br) < 1e-3, f"brecha debería ser ~{_br:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿el error de prueba es mucho mayor que el de entrenamiento?"
    print(f"✅ Correcto. Entrenamiento {_mtr:,.0f} vs prueba {_mte:,.0f} CLP (brecha {_br:.1f}×): puro sobreajuste.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ───────────────────────── E4: importancia / causalidad ─────────────────────────
E4 = """## Ejercicio 04 · La trampa de la importancia de variables (conceptual)
Vuelve al experimento de la sección 5: metimos `ruido_aleatorio`, una columna **inventada al azar y sin
ninguna relación** con el monto. Aun así, el Random Forest le dio una importancia **alta**, comparable a
la de variables reales.

- Calcula en `imp_ruido` la importancia que el modelo le dio a `ruido_aleatorio`. Reusa `rf` y `X_exp`
  de la sección 5; pista: `pd.Series(rf.feature_importances_, index=X_exp.columns)["ruido_aleatorio"]`.
- Elige en `conclusion` la lectura correcta:
  - **A.** Si `ruido_aleatorio` saca importancia alta, entonces **causa** el monto y hay que vigilarlo.
  - **B.** Una variable de **alta cardinalidad** (un número continuo) ofrece muchos cortes y **parece**
    importante aunque sea ruido. La importancia mide utilidad para *predecir*, **no causalidad**: no se
    lee sola.
  - **C.** El modelo está mal entrenado: una columna de ruido **nunca** debería recibir importancia.

*(Opcional, no se corrige): en `reflexion` escribe qué harías antes de afirmar que una variable "importante" debe ser el foco de una política.)*"""
E4_TODO = """imp_ruido = None     # TODO: importancia de 'ruido_aleatorio' (rf.feature_importances_)
conclusion = None    # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """imp_ruido = pd.Series(rf.feature_importances_, index=X_exp.columns)["ruido_aleatorio"]
conclusion = "B"
reflexion = "Buscaría evidencia causal (no solo predictiva), revisaría correlaciones entre variables y validaría con datos nuevos antes de fijar una política."
"""
E4_CHK = """try:
    _imp = pd.Series(rf.feature_importances_, index=X_exp.columns)["ruido_aleatorio"]
    assert imp_ruido is not None and abs(imp_ruido - _imp) < 1e-6, f"imp_ruido debería ser ~{_imp:.3f}"
    # 'B' es la respuesta conceptualmente correcta independientemente del valor exacto de imp_ruido
    # (la alta cardinalidad SIEMPRE sesga la importancia MDI). El assert de abajo solo confirma que
    # este experimento concreto reprodujo el fenómeno con una importancia visible, no condiciona la letra.
    assert _imp > 0.05, "El experimento debería dar importancia no trivial al ruido."
    assert str(conclusion).strip().upper() == "B", "Pista: que prediga bien no significa que cause; ojo con la alta cardinalidad."
    print(f"✅ Correcto. El ruido sacó {_imp:.0%} de importancia siendo azar puro: la cifra NO se lee sola.")
    print("   Importancia = utilidad para predecir, sesgada por cardinalidad. No implica causalidad.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *entrenas* árboles: entiendes **cómo deciden** (buscan la pregunta que más reduce la
**impureza**), por qué un árbol suelto **solo sabe memorizar**, la diferencia entre **bagging** (promediar
árboles independientes) y **boosting** (corregir errores en secuencia), y por qué la **importancia de
variables** —tan tentadora en el Estado— **engaña** con la alta cardinalidad, las variables correlacionadas
y la confusión entre predecir y causar.

La regla de oro que te llevas: **un modelo que predice bien no es un modelo que explica.** Antes de
convertir una "variable importante" en una política, pregunta por la cardinalidad, por las correlaciones
y, sobre todo, por la **causa**. Eso distingue a quien *usa* los árboles de quien *se deja engañar* por
ellos."""


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
        md(ERRORES, "p12"), md(EJ_HEADER, "p13"),
        md(E1, "p14"), code(g(E1_SOL, E1_TODO), "p15"), code(E1_CHK, "p16"),
        md(E2, "p17"), code(g(E2_SOL, E2_TODO), "p18"), code(E2_CHK, "p19"),
        md(E3, "p20"), code(g(E3_SOL, E3_TODO), "p21"), code(E3_CHK, "p22"),
        md(E4, "p23"), code(g(E4_SOL, E4_TODO), "p24"), code(E4_CHK, "p25"),
        md(CIERRE, "p26"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "profundiza.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "profundiza_solucion.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Generados: profundiza.ipynb y profundiza_solucion.ipynb en", BASE)
