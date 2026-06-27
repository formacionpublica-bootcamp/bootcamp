# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B2 (Fundamentos de ML):
B2/profundiza.ipynb (estudiante) + B2/profundiza_solucion.ipynb (resuelto).

Más teórico que la lección: el *porqué* del aprendizaje automático. Cubre
sesgo-varianza, sobreajuste vs subajuste, validación cruzada (k-fold), el
supuesto i.i.d., el baseline y la curva de aprendizaje. Demos reales con
scikit-learn sobre compras_ml.csv. Todo corre offline."""
import json, os

BASE = "B2-fundamentos-de-ml"

TITULO = """# B2 · Fundamentos de ML — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B2 —donde entrenaste tu primer modelo
(`fit`/`predict`), separaste un conjunto de prueba y mediste el error— aquí vamos al *porqué*: por qué
**ningún modelo es perfecto** (el dilema **sesgo–varianza**), qué distingue al **sobreajuste** del
**subajuste**, por qué un solo train/test **no basta** y aparece la **validación cruzada**, qué supuesto
silencioso (**i.i.d.**) sostiene todo, por qué necesitas un **baseline** antes de festejar, y qué te dice
una **curva de aprendizaje** sobre si conviene juntar más datos.

Menos sintaxis nueva, más **criterio para confiar (o desconfiar) de un modelo**. Los ejercicios del final
son más conceptuales: calculas algo y eliges la **interpretación** correcta.

> Requisito: haber hecho `leccion.ipynb` de B2. Mismo dataset: `compras_ml.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("compras_ml.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B2-fundamentos-de-ml/compras_ml.csv"
        urllib.request.urlretrieve(url, "compras_ml.csv")
    except Exception:
        print("Si estás en Colab, sube compras_ml.csv manualmente.")

df = pd.read_csv("compras_ml.csv")

# Feature principal de la lección (cantidad) + tamano_num como segunda variable para enriquecer las demos.
X = df[["cantidad", "tamano_num"]]
y = df["monto_total"]
print(f"{len(df)} compras públicas | predecimos monto_total desde {list(X.columns)}")
print(f"monto_total: media {y.mean():,.0f} CLP | mediana {y.median():,.0f} CLP (muy sesgado a la derecha)")"""

S1 = """## 1. El dilema central: sesgo vs varianza (por qué ningún modelo es perfecto)

En la lección el modelo "se equivocaba por X pesos" y estaba bien. Aquí está el *porqué* de fondo: el
error de un modelo se puede descomponer en **dos enemigos opuestos** que tiras de un extremo a otro.

- **Sesgo (*bias*):** el error por ser **demasiado simple**. Un modelo rígido (una recta, un árbol muy
  corto) no alcanza a capturar el patrón real: se equivoca **parecido en todas partes**, incluso en los
  datos con los que entrenó. Es el **subajuste**.
- **Varianza:** el error por ser **demasiado flexible**. Un modelo muy complejo se amolda a cada detalle
  —y a cada ruido— de los datos de entrenamiento. Memoriza en vez de aprender, así que **cambia mucho** si
  le tocan otros datos. Es el **sobreajuste**.

> 🧠 **Analogía pública.** Un instructivo de **una sola línea** ("apruebe todo bajo \\$50.000") es de **alto
> sesgo**: simple, pero ignora casos. Un instructivo con **una regla distinta para cada expediente
> histórico** es de **alta varianza**: calza perfecto con el pasado y falla con cualquier caso nuevo. El
> buen instructivo está **en el medio**.

No puedes bajar los dos a cero a la vez: bajar el sesgo (más complejidad) sube la varianza, y viceversa.
El oficio del *data scientist* es encontrar el **punto medio**. Lo vemos subiendo la profundidad de un
árbol y mirando el error de **entrenamiento** y de **prueba** por separado."""

S1_CODE = """from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

profundidades = [1, 2, 3, 5, 8, 12, None]
r2_train, r2_test = [], []
for d in profundidades:
    arbol = DecisionTreeRegressor(max_depth=d, random_state=42).fit(X_train, y_train)
    r2_train.append(arbol.score(X_train, y_train))
    r2_test.append(arbol.score(X_test, y_test))

print(" profundidad | R² entren. | R² prueba")
for d, rtr, rte in zip(profundidades, r2_train, r2_test):
    print(f"   {str(d):>6}    |   {rtr:5.3f}    |   {rte:5.3f}")

eje = [d if d is not None else 15 for d in profundidades]   # 'None' = sin tope; lo ubicamos al final
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(eje, r2_train, "o-", label="R² entrenamiento", color="#0a7e7e")
ax.plot(eje, r2_test, "s--", label="R² prueba", color="crimson")
ax.set_xlabel("Profundidad del árbol (más = más complejo)")
ax.set_ylabel("R² (1 = perfecto)"); ax.set_title("Sesgo (izquierda) vs varianza (derecha)")
ax.legend(); plt.tight_layout(); plt.show()
print("\\nIzquierda: ambos R² bajos = SESGO (subajuste). Derecha: entren. sube pero prueba se estanca")
print("o cae = VARIANZA (sobreajuste). El mejor compromiso está en el medio.")"""

S2 = """## 2. Sobreajuste vs subajuste, en números: la brecha train–test

La sección 1 lo mostró en una curva; afinemos el **diagnóstico** que usarás en la práctica. La señal de
alarma no es "el error es alto" a secas, sino **cómo se compara** el error de entrenamiento con el de
prueba:

- **Subajuste (alto sesgo):** error **alto en ambos** y parecidos. El modelo ni siquiera aprende los datos
  que vio. Solución: darle **más complejidad** (o mejores *features*). Lo que caracteriza al subajuste es la
  **magnitud alta** del error en ambos conjuntos, **no el signo** de la brecha: con datos muy ruidosos (mismas
  *features*, montos muy distintos) un árbol superficial puede dar un error de entrenamiento **levemente mayor**
  que el de prueba, y aun así estar subajustando.
- **Sobreajuste (alta varianza):** error **bajo en entrenamiento** pero **mucho más alto en prueba**. La
  **brecha** entre ambos es la huella del sobreajuste: el modelo memorizó el entrenamiento y no generaliza.
- **Punto justo:** error moderado y **parecido** en ambos. Generaliza.

> ⚠️ Un error de entrenamiento de **0** (R²=1) casi nunca es buena noticia: significa que el modelo se
> aprendió los datos de memoria. La pregunta correcta es siempre: ¿y cómo le va en datos que **no** vio?

Comparemos un árbol **corto** (candidato a subajuste) con uno **sin tope** (candidato a sobreajuste),
mirando el **MAE** (error en pesos, más interpretable que R² para un funcionario)."""

S2_CODE = """from sklearn.metrics import mean_absolute_error

def errores(modelo):
    mae_tr = mean_absolute_error(y_train, modelo.predict(X_train))
    mae_te = mean_absolute_error(y_test, modelo.predict(X_test))
    return mae_tr, mae_te

corto = DecisionTreeRegressor(max_depth=2, random_state=42).fit(X_train, y_train)
profundo = DecisionTreeRegressor(max_depth=None, random_state=42).fit(X_train, y_train)

for nombre, m in [("Árbol corto (depth=2)", corto), ("Árbol sin tope (depth=None)", profundo)]:
    mtr, mte = errores(m)
    brecha = mte - mtr
    print(f"{nombre:<30} MAE entren.={mtr:>9,.0f}  MAE prueba={mte:>9,.0f}  brecha={brecha:>+9,.0f}")

print("\\nEl corto: errores altos y PARECIDOS -> tira a SUBAJUSTE (no captura todo el patrón).")
print("El sin tope: error de entrenamiento mucho menor que el de prueba -> esa BRECHA es SOBREAJUSTE.")
dup = X.duplicated(keep=False).mean() * 100
print(f"\\nNota sobre el signo: en el árbol corto la brecha sale NEGATIVA (prueba algo MENOR que")
print(f"entrenamiento). No es que 'mejore en prueba': en este dataset ~{dup:.0f}% de las filas comparten")
print("features con montos muy distintos, así que el error de entrenamiento queda artificialmente")
print("alto incluso para un modelo simple. Lo que delata al SUBAJUSTE es la MAGNITUD alta en ambos")
print("(diferencia de solo ~4%), no el signo; compárala con la brecha del árbol sin tope (~18%).")"""

S3 = """## 3. Por qué un solo train/test no basta: validación cruzada (k-fold)

La lección reservó **un** conjunto de prueba. Pero ese 30% se eligió **al azar** una vez: ¿y si nos tocó
un test "fácil" (suerte) o "difícil" (mala suerte)? Con un solo corte, tu estimación del error **depende
del sorteo**. Es la misma variabilidad muestral que en estadística: una sola muestra puede engañarte.

La **validación cruzada k-fold** lo resuelve repartiendo la apuesta. Con `k=5`:

1. Parte los datos en **5 bloques** (*folds*) iguales.
2. Entrena con 4 bloques y evalúa en el **que quedó fuera**. Repite **5 veces**, rotando cuál queda fuera.
3. Te quedas con **5 puntajes** → su **promedio** es una estimación más estable, y su **dispersión** te
   dice **cuánto fluctúa** según qué datos tocaron.

> 🧠 **Analogía pública.** No evalúas un programa con **una sola** comuna piloto; lo pruebas en **varias**
> y miras el promedio **y** qué tan disparejos salen los resultados. Una sola comuna puede mentir.

`cross_val_score` hace todo el baile por ti. Lo importante no es solo el promedio: es ver **cuánto saltan**
los 5 puntajes."""

S3_CODE = """from sklearn.model_selection import cross_val_score

arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
puntajes = cross_val_score(arbol, X, y, cv=5, scoring="r2")

print("R² en cada uno de los 5 folds:")
for i, s in enumerate(puntajes, 1):
    print(f"  fold {i}: {s:.3f}")
print(f"\\nPromedio: {puntajes.mean():.3f}   |   Dispersión (std): {puntajes.std():.3f}")
print(f"Rango: de {puntajes.min():.3f} a {puntajes.max():.3f}")
print("\\nUn solo train/test te habría dado UNO de estos números (quizá el más alto o el más bajo).")
print("La validación cruzada promedia los 5 y te muestra cuánto dependía de la suerte del sorteo.")"""

S4 = """## 4. El supuesto silencioso que sostiene todo: i.i.d.

Todo lo anterior —separar test, validación cruzada— asume algo que casi nunca se dice en voz alta: que los
datos son **i.i.d.** (*independientes e idénticamente distribuidos*). En cristiano: que cada fila es una
muestra **del mismo proceso** y el orden **no importa**, así que un trozo cualquiera es **representativo**
del resto.

Cuando ese supuesto **se rompe**, las garantías se caen. Casos típicos en el Estado:

- **Datos con tiempo:** si entrenas con 2020–2022 y evalúas con 2023, el "futuro" puede ser distinto
  (inflación, nuevas leyes). El test ya no es "del mismo proceso".
- **Datos agrupados/ordenados:** si las filas vienen ordenadas por región o por monto, un corte ingenuo
  puede dejar **regiones enteras** fuera del entrenamiento.

Lo dramático es **cuánto** importa. Vamos a hacer trampa a propósito: ordenamos los datos por
`monto_total` y corremos validación cruzada **sin barajar**. Cada fold de prueba será entonces un **rango
de montos que el modelo nunca vio** al entrenar — justo lo que el supuesto i.i.d. prohíbe."""

S4_CODE = """from sklearn.model_selection import KFold

# Ordenamos a propósito por el objetivo: rompemos el i.i.d. (cada fold queda en un rango distinto)
orden = df.sort_values("monto_total").reset_index(drop=True)
X_ord, y_ord = orden[["cantidad", "tamano_num"]], orden["monto_total"]
arbol = DecisionTreeRegressor(max_depth=4, random_state=42)

cv_sin_barajar = cross_val_score(arbol, X_ord, y_ord,
                                 cv=KFold(n_splits=5, shuffle=False), scoring="r2")
cv_barajado   = cross_val_score(arbol, X_ord, y_ord,
                                 cv=KFold(n_splits=5, shuffle=True, random_state=42), scoring="r2")

print("Datos ORDENADOS por monto, SIN barajar (i.i.d. roto):")
print("  R² por fold:", np.round(cv_sin_barajar, 2), " promedio:", round(cv_sin_barajar.mean(), 2))
print("\\nLos MISMOS datos, pero BARAJADOS (i.i.d. restaurado):")
print("  R² por fold:", np.round(cv_barajado, 2), " promedio:", round(cv_barajado.mean(), 2))
print("\\nSin barajar el R² se desploma (incluso negativo: peor que adivinar la media): cada fold")
print("evaluaba montos fuera del rango entrenado. Barajar restaura el supuesto y el modelo funciona.")"""

S5 = """## 5. El baseline: ¿tu modelo aprende algo, o solo aparenta?

Antes de celebrar un MAE, hay una pregunta que casi nadie hace: **¿comparado con qué?** Un error de
"90.000 pesos" no es bueno ni malo en el vacío. Necesitas un **baseline**: el modelo **más tonto posible**,
para medir cuánto aporta el tuyo **por encima** de no pensar.

El baseline clásico en regresión es **predecir siempre la media** del objetivo (ignorando por completo las
*features*). Si tu modelo —que sí mira `cantidad` y `tamano_num`— **no le gana** a "decir la media para
todo", entonces no aprendió nada útil: toda su sofisticación fue decorado.

> 🧠 **Analogía pública.** Antes de afirmar que un programa "redujo los tiempos de espera", compáralo con
> **no hacer nada** (o con el promedio histórico). Si no le gana a la inacción, el programa no sirve, por
> elegante que sea su diseño.

`DummyRegressor(strategy="mean")` es ese tonto de referencia. Comparamos su MAE con el de nuestro árbol."""

S5_CODE = """from sklearn.dummy import DummyRegressor

baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
modelo   = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_train, y_train)

mae_base   = mean_absolute_error(y_test, baseline.predict(X_test))
mae_modelo = mean_absolute_error(y_test, modelo.predict(X_test))
mejora = (mae_base - mae_modelo) / mae_base * 100

print(f"MAE del baseline (predecir siempre la media): {mae_base:>9,.0f} CLP")
print(f"MAE de nuestro árbol (mira las features):     {mae_modelo:>9,.0f} CLP")
print(f"\\nEl árbol reduce el error un {mejora:.0f}% respecto al tonto: SÍ aprendió algo real.")
print("Si esta mejora fuera ~0%, el modelo no aportaría nada sobre adivinar la media.")"""

S6 = """## 6. La curva de aprendizaje: ¿me faltan datos o me falta modelo?

Última pregunta práctica: cuando un modelo no rinde, ¿conviene **conseguir más datos** (caro, lento) o el
problema es **otro**? La **curva de aprendizaje** responde: entrena el modelo con porciones crecientes de
datos (10%, 20%, … 100%) y grafica el error de **entrenamiento** y de **validación** según cuántos datos usó.

Cómo leerla:

- Si la curva de **validación sigue bajando** al final, **más datos ayudarían**: aún no llegaste al techo.
- Si **se aplanó** (las dos curvas convergen y se estancan), **más datos casi no servirán**: el límite ya
  no son los datos, sino el **modelo o las features**. Toca cambiar de modelo o crear mejores variables.
- Una brecha grande y persistente entre ambas curvas vuelve a señalar **sobreajuste**.

> 🧠 **Sentido público.** Equivale a preguntar: "¿levanto más encuestas (más datos) o rediseño el
> instrumento (mejor modelo)?". La curva te dice **dónde** está el cuello de botella antes de gastar plata."""

S6_CODE = """from sklearn.model_selection import learning_curve

arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
tamanos, sc_train, sc_val = learning_curve(
    arbol, X, y, cv=5, scoring="neg_mean_absolute_error",
    train_sizes=np.linspace(0.1, 1.0, 6), shuffle=True, random_state=42)

mae_train = -sc_train.mean(axis=1)   # negamos: scoring devuelve MAE negativo
mae_val   = -sc_val.mean(axis=1)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(tamanos, mae_train, "o-", label="MAE entrenamiento", color="#0a7e7e")
ax.plot(tamanos, mae_val, "s--", label="MAE validación", color="crimson")
ax.set_xlabel("N° de compras usadas para entrenar")
ax.set_ylabel("MAE (CLP, más bajo = mejor)"); ax.set_title("Curva de aprendizaje")
ax.legend(); plt.tight_layout(); plt.show()

caida_final = mae_val[-2] - mae_val[-1]
print(f"MAE de validación con pocos datos: {mae_val[0]:,.0f}  ->  con todos: {mae_val[-1]:,.0f}")
print(f"Caída en el último tramo: {caida_final:,.0f} CLP.")
print("Si la curva de validación ya casi no baja al final, más datos rendirían poco:")
print("el cuello de botella pasa a ser el modelo o las features, no la cantidad de datos.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Festejar un R²=1 (o error 0) en entrenamiento.** Casi siempre es **sobreajuste**: el modelo memorizó. La verdad está en datos que no vio.
- **Confiar en un solo train/test.** Ese sorteo pudo tocar fácil o difícil. Usa **validación cruzada** y mira también su **dispersión**.
- **Olvidar el baseline.** Un MAE "bajo" no dice nada si no le ganas a **predecir la media**. Siempre compara contra el tonto.
- **Ignorar el supuesto i.i.d.** Con datos de **tiempo** o **agrupados**, un corte al azar hace trampa. Respeta el orden temporal / agrupa por bloque.
- **Echarle más datos a un modelo estancado.** Si la **curva de aprendizaje** se aplanó, más datos no ayudan: cambia el modelo o las *features*.
- **Confundir "complejo" con "mejor".** Más profundidad baja el sesgo pero **sube la varianza**. El objetivo es el punto medio, no el modelo más grande."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: en cada uno **calculas algo** y luego eliges la **interpretación
correcta** asignando una letra a `conclusion`. Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 sobreajuste: brecha train-test ----
E1 = """## Ejercicio 01 · Diagnosticar sobreajuste por la brecha
Entrena un `DecisionTreeRegressor(max_depth=None, random_state=42)` con `X_train`/`y_train` (ya creados
en la sección 1) y mide su **R²** en entrenamiento y en prueba.

- Guarda en `r2_tr` el R² en **entrenamiento** (`.score(X_train, y_train)`).
- Guarda en `r2_te` el R² en **prueba** (`.score(X_test, y_test)`).
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** R² alto en entrenamiento y bastante más bajo en prueba: el modelo **sobreajusta** (memorizó, generaliza peor).
  - **B.** Los dos R² son casi iguales: el modelo generaliza perfecto, sin problema alguno.
  - **C.** El R² de prueba es mayor que el de entrenamiento: el modelo mejora en datos nuevos."""
E1_TODO = """from sklearn.tree import DecisionTreeRegressor
arbol_ej = DecisionTreeRegressor(max_depth=None, random_state=42).fit(X_train, y_train)
r2_tr = None        # TODO: arbol_ej.score(X_train, y_train)
r2_te = None        # TODO: arbol_ej.score(X_test, y_test)
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """from sklearn.tree import DecisionTreeRegressor
arbol_ej = DecisionTreeRegressor(max_depth=None, random_state=42).fit(X_train, y_train)
r2_tr = arbol_ej.score(X_train, y_train)
r2_te = arbol_ej.score(X_test, y_test)
conclusion = "A"
"""
E1_CHK = """try:
    from sklearn.tree import DecisionTreeRegressor as _DTR
    _a = _DTR(max_depth=None, random_state=42).fit(X_train, y_train)
    _rtr = _a.score(X_train, y_train)
    _rte = _a.score(X_test, y_test)
    # Derivamos la letra de los números: ¿hay brecha clara a favor del entrenamiento?
    _correcta = "A" if (_rtr - _rte) > 0.05 else "B"
    assert r2_tr is not None and abs(r2_tr - _rtr) < 1e-6, "Revisa r2_tr (.score sobre entrenamiento)."
    assert r2_te is not None and abs(r2_te - _rte) < 1e-6, "Revisa r2_te (.score sobre prueba)."
    assert str(conclusion).strip().upper() == _correcta, "Mira la BRECHA entre los dos R²: ¿qué indica?"
    print(f"✅ Correcto. R² entren.={_rtr:.3f} vs prueba={_rte:.3f}: la brecha ({_rtr-_rte:.3f}) delata sobreajuste.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 validación cruzada: promedio y dispersión ----
E2 = """## Ejercicio 02 · Validación cruzada: promedio y dispersión
Con `cross_val_score`, evalúa un `DecisionTreeRegressor(max_depth=4, random_state=42)` sobre `X`, `y`
con `cv=5` y `scoring="r2"` (igual que en la sección 3).

- Guarda en `media_cv` el **promedio** de los 5 puntajes (`.mean()`).
- Guarda en `disp_cv` su **desviación estándar** (`.std()`).
- Elige en `conclusion` la interpretación correcta:
  - **A.** Como hay 5 puntajes distintos, el modelo está roto y no se puede usar.
  - **B.** El promedio resume el desempeño y la dispersión (pequeña frente al promedio) dice **cuánto fluctúa** según el sorteo: una estimación más confiable que un solo train/test.
  - **C.** La dispersión no aporta nada; solo importa el puntaje más alto de los 5."""
E2_TODO = """from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
_arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
puntajes_ej = cross_val_score(_arbol, X, y, cv=5, scoring="r2")
media_cv = None     # TODO: puntajes_ej.mean()
disp_cv = None      # TODO: puntajes_ej.std()
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
_arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
puntajes_ej = cross_val_score(_arbol, X, y, cv=5, scoring="r2")
media_cv = puntajes_ej.mean()
disp_cv = puntajes_ej.std()
conclusion = "B"
"""
E2_CHK = """try:
    from sklearn.model_selection import cross_val_score as _cvs
    from sklearn.tree import DecisionTreeRegressor as _DTR
    _p = _cvs(_DTR(max_depth=4, random_state=42), X, y, cv=5, scoring="r2")
    _m, _s = _p.mean(), _p.std()
    # Derivamos la letra: la dispersión es chica frente al promedio -> CV da estimación estable y útil (B)
    _correcta = "B" if (_m > 0 and _s < abs(_m)) else "A"
    assert media_cv is not None and abs(media_cv - _m) < 1e-6, "Revisa media_cv (.mean() de los puntajes)."
    assert disp_cv is not None and abs(disp_cv - _s) < 1e-6, "Revisa disp_cv (.std() de los puntajes)."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿qué aportan juntos el promedio Y la dispersión?"
    print(f"✅ Correcto. Promedio={_m:.3f}, dispersión={_s:.3f}: pequeña frente al promedio, estimación confiable.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 i.i.d. ----
E3 = """## Ejercicio 03 · Cuando se rompe el supuesto i.i.d.
Reproduce el experimento de la sección 4 sobre los datos **ordenados por `monto_total`**: corre
`cross_val_score` con `KFold(n_splits=5, shuffle=False)` (sin barajar) y guarda el **promedio** del R².

- Usa `X_ord`, `y_ord` (ya creados en la sección 4) y un `DecisionTreeRegressor(max_depth=4, random_state=42)`.
- Guarda en `media_sin_barajar` el promedio del R² de la validación cruzada **sin barajar**.
- Elige en `conclusion` la lectura correcta:
  - **A.** El promedio sale alto y positivo: ordenar los datos no afecta en nada.
  - **B.** El promedio se desploma (negativo o casi cero): al romper el **i.i.d.**, cada fold evalúa un rango de montos que el modelo nunca vio, así que la evaluación deja de ser válida.
  - **C.** Da exactamente el mismo número que con `shuffle=True`."""
E3_TODO = """from sklearn.model_selection import cross_val_score, KFold
from sklearn.tree import DecisionTreeRegressor
_arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
_cv_sin = cross_val_score(_arbol, X_ord, y_ord, cv=KFold(n_splits=5, shuffle=False), scoring="r2")
media_sin_barajar = None   # TODO: _cv_sin.mean()
conclusion = None          # TODO: "A", "B" o "C"
"""
E3_SOL = """from sklearn.model_selection import cross_val_score, KFold
from sklearn.tree import DecisionTreeRegressor
_arbol = DecisionTreeRegressor(max_depth=4, random_state=42)
_cv_sin = cross_val_score(_arbol, X_ord, y_ord, cv=KFold(n_splits=5, shuffle=False), scoring="r2")
media_sin_barajar = _cv_sin.mean()
conclusion = "B"
"""
E3_CHK = """try:
    from sklearn.model_selection import cross_val_score as _cvs, KFold as _KF
    from sklearn.tree import DecisionTreeRegressor as _DTR
    _cv = _cvs(_DTR(max_depth=4, random_state=42), X_ord, y_ord,
               cv=_KF(n_splits=5, shuffle=False), scoring="r2")
    _m = _cv.mean()
    # Derivamos la letra del signo/magnitud: si el promedio se hunde (<0.2) el i.i.d. está roto -> B
    _correcta = "B" if _m < 0.2 else "A"
    assert media_sin_barajar is not None and abs(media_sin_barajar - _m) < 1e-6, "Revisa media_sin_barajar (.mean())."
    assert str(conclusion).strip().upper() == _correcta, "Pista: mira el signo del promedio. ¿Qué le pasó?"
    print(f"✅ Correcto. Promedio sin barajar = {_m:.2f}: se hundió. Romper el i.i.d. invalida la evaluación.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 baseline ----
E4 = """## Ejercicio 04 · ¿Le gana al baseline?
Compara, en el conjunto de **prueba**, el MAE de un `DummyRegressor(strategy="mean")` (predecir siempre la
media) contra el de un `DecisionTreeRegressor(max_depth=4, random_state=42)`. Ambos entrenados con
`X_train`/`y_train` (sección 1).

- Guarda en `mae_base` el MAE del baseline en prueba.
- Guarda en `mae_modelo` el MAE del árbol en prueba.
- Elige en `conclusion` la lectura correcta:
  - **A.** El árbol tiene un MAE claramente **menor** que el baseline: aprendió algo real de las features, no solo aparenta.
  - **B.** El árbol tiene un MAE **mayor** que el baseline: conviene quedarse con predecir la media.
  - **C.** Ambos MAE son idénticos: el árbol no aporta nada sobre adivinar la media."""
E4_TODO = """from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
_base = DummyRegressor(strategy="mean").fit(X_train, y_train)
_mod = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_train, y_train)
mae_base = None     # TODO: mean_absolute_error(y_test, _base.predict(X_test))
mae_modelo = None   # TODO: mean_absolute_error(y_test, _mod.predict(X_test))
conclusion = None   # TODO: "A", "B" o "C"
"""
E4_SOL = """from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
_base = DummyRegressor(strategy="mean").fit(X_train, y_train)
_mod = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_train, y_train)
mae_base = mean_absolute_error(y_test, _base.predict(X_test))
mae_modelo = mean_absolute_error(y_test, _mod.predict(X_test))
conclusion = "A"
"""
E4_CHK = """try:
    from sklearn.dummy import DummyRegressor as _DR
    from sklearn.tree import DecisionTreeRegressor as _DTR
    from sklearn.metrics import mean_absolute_error as _mae
    _b = _mae(y_test, _DR(strategy="mean").fit(X_train, y_train).predict(X_test))
    _md = _mae(y_test, _DTR(max_depth=4, random_state=42).fit(X_train, y_train).predict(X_test))
    # Derivamos la letra comparando los MAE reales
    _correcta = "A" if _md < _b - 1 else ("B" if _md > _b + 1 else "C")
    assert mae_base is not None and abs(mae_base - _b) < 1e-3, "Revisa mae_base (MAE del DummyRegressor)."
    assert mae_modelo is not None and abs(mae_modelo - _md) < 1e-3, "Revisa mae_modelo (MAE del árbol)."
    assert str(conclusion).strip().upper() == _correcta, "Compara los dos MAE: ¿cuál es menor?"
    print(f"✅ Correcto. Baseline={_b:,.0f} CLP vs árbol={_md:,.0f} CLP: el modelo le gana, aprendió algo real.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo entrenas un modelo: entiendes **por qué ninguno es perfecto** (sesgo vs varianza), cómo
**diagnosticar** sobreajuste y subajuste por la brecha train–test, por qué un solo corte engaña y la
**validación cruzada** estima mejor, qué supuesto (**i.i.d.**) sostiene todo y qué pasa al romperlo, por
qué un resultado no significa nada sin un **baseline**, y cómo una **curva de aprendizaje** te dice si te
faltan **datos** o te falta **modelo**.

La regla de oro que te llevas: **antes de confiar en un modelo, pregunta por la brecha, por el baseline y
por el supuesto.** Eso distingue a quien *entrena* modelos de quien sabe *cuándo creerles* —y en decisiones
públicas, esa diferencia es la que evita gastar plata y reputación en un modelo que solo aparentaba andar.

> **Hacia dónde sigue:** en los módulos siguientes verás modelos más potentes (árboles combinados,
> *boosting*) y clasificación. Toda esta disciplina —train/test honesto, validación cruzada, baseline— se
> aplica **igual**, sin cambios."""


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
