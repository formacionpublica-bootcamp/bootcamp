"""build_R2-05.py — módulo R2-05 (Modelos basados en árboles).

Rama R2 (Científico de Datos). Rearmado 2026: ancla de la
rama = calidad del aire (PM2.5 diario SINCA). Mismo arco que la versión anterior —
árbol de decisión, sobreajuste según profundidad, bosque aleatorio e importancia de
variables — sobre el MISMO problema de R2-04 (PM2.5 de mañana en Cerro Navia, mismas
features, mismo corte temporal 2020–2024 / 2025) para comparar de forma justa contra
el baseline «mañana = hoy» y la regresión lineal. Cierra pasando de la predicción a
la ALERTA (días sobre la norma de 50 µg/m³).
Profundiza = transferencia con sismos USGS 2020–2025: predecir la profundidad desde
latitud/longitud/magnitud con un árbol interpretable (la subducción aparece sola).

Uso:  /opt/anaconda3/bin/python tools/build_R2-05.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-05-modelos-de-arboles")

RAW = h.REPO_RAW


def guardado(n, src):
    """Celda de ilustración que no se cae si el ejercicio n aún tiene TODO."""
    cuerpo = "\n".join("    " + ln for ln in src.strip("\n").splitlines())
    primera, _, resto = cuerpo.partition("\n")
    return f"""{primera.strip()}
try:
{resto}
except (NameError, TypeError, ValueError, AttributeError):
    print("ℹ️ Completa el ejercicio {n} para ver este gráfico.")"""


SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "aire_diario.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)

df = pd.read_csv(CSV, parse_dates=["fecha"])
cn = df[df["estacion"] == "Cerro Navia"].sort_values("fecha").reset_index(drop=True)

# Las mismas features de R2-04 (ya fabricadas para ti)
cn["pm25_ayer"] = cn["pm25"].shift(1)
cn["mes"] = cn["fecha"].dt.month
cn["dia_semana"] = cn["fecha"].dt.dayofweek
FEATURES = ["temp_media", "humedad_media", "mes", "dia_semana", "pm25_ayer"]
datos = cn.dropna(subset=FEATURES + ["pm25"])
print("Cerro Navia, días completos:", len(datos))'''

INTRO = '''## Por qué el mismo dato (a propósito)

En R2-04 pronosticaste el PM2.5 de Cerro Navia con una **recta**. Hoy usarás **árboles** sobre
**exactamente el mismo problema**: mismas features, mismo corte temporal. Así la comparación es
justa y te concentras en lo nuevo — el modelo — sin distraerte con otro dataset.

| Vara de R2-04 (MAE en 2025) | µg/m³ |
| --- | --- |
| Baseline «mañana = hoy» | ≈ 7,36 |
| Regresión lineal | ≈ 7,09 |

Un **árbol de decisión** predice con una **secuencia de preguntas sí/no**: *¿ayer hubo más de
33,5 µg/m³? → ¿hoy hace menos de 9 °C? → …* hasta una hoja con un valor estimado.

> 🧠 **Analogía.** Es un flujograma de trámite: «si es invierno, pase a la ventanilla A; si además
> ayer hubo episodio, …». Por eso los árboles son de los modelos más fáciles de explicar a una autoridad.'''

EJ = [
 ("## 1. Preparar: el mismo corte temporal, las mismas varas",
  "Repite el corte de R2-04 (entrenar 2020–2024, probar 2025) y recalcula las dos varas: "
  "el baseline de persistencia y la regresión lineal.",
  "Corte temporal y MAE de referencia",
  '''corte = pd.Timestamp("2025-01-01")
train = datos[datos["fecha"] < corte]
test = datos[datos["fecha"] >= corte]
X_train, y_train = train[FEATURES], train["pm25"]
X_test, y_test = test[FEATURES], test["pm25"]
mae_base = mean_absolute_error(y_test, X_test["pm25_ayer"])
mae_lr = mean_absolute_error(y_test, LinearRegression().fit(X_train, y_train).predict(X_test))
print("entrenamiento:", len(train), "| prueba:", len(test))
print("MAE baseline:", round(mae_base, 2), "| MAE regresión lineal:", round(mae_lr, 2))''',
  '''corte = pd.Timestamp("2025-01-01")
# TODO: train = días antes del corte; test = días desde el corte
train = ...
test = ...
X_train, y_train = train[FEATURES], train["pm25"]
X_test, y_test = test[FEATURES], test["pm25"]
mae_base = mean_absolute_error(y_test, X_test["pm25_ayer"])
mae_lr = mean_absolute_error(y_test, LinearRegression().fit(X_train, y_train).predict(X_test))
print("MAE baseline:", round(mae_base, 2), "| MAE regresión lineal:", round(mae_lr, 2))''',
  '''assert train["fecha"].max() < test["fecha"].min()
assert len(train) + len(test) == len(datos)
assert mae_lr < mae_base''',
  'train = datos[datos["fecha"] < corte] y test = datos[datos["fecha"] >= corte] (igual que en R2-04).',
  None),

 ("## 2. Tu primer árbol",
  "El hiperparámetro **`max_depth`** limita cuántas preguntas seguidas puede hacer el árbol. "
  "Empieza con uno chico, `max_depth=3` (8 hojas como máximo), y fija `random_state=42` para que "
  "el resultado sea reproducible.",
  "Entrena un árbol de profundidad 3 y mide su MAE en 2025",
  '''arbol = DecisionTreeRegressor(max_depth=3, random_state=42)
arbol.fit(X_train, y_train)
mae_arbol = mean_absolute_error(y_test, arbol.predict(X_test))
print("MAE árbol (profundidad 3):", round(mae_arbol, 2), "| lineal:", round(mae_lr, 2), "| baseline:", round(mae_base, 2))''',
  '''# TODO: árbol con max_depth=3 y random_state=42, entrenado con (X_train, y_train)
arbol = ...
...
# TODO: MAE en prueba
mae_arbol = ...
print("MAE árbol (profundidad 3):", mae_arbol, "| lineal:", round(mae_lr, 2), "| baseline:", round(mae_base, 2))''',
  '''assert arbol.get_depth() == 3
assert abs(mae_arbol - mean_absolute_error(y_test, arbol.predict(X_test))) < 1e-9''',
  "DecisionTreeRegressor(max_depth=3, random_state=42); .fit(X_train, y_train); mean_absolute_error(y_test, arbol.predict(X_test)).",
  guardado(2, '''# (ilustración) Así «piensa» tu árbol: cada caja es una pregunta; las hojas, el PM2.5 estimado
plt.figure(figsize=(16, 6))
plot_tree(arbol, feature_names=FEATURES, filled=True, rounded=True, fontsize=8, impurity=False)
plt.title("Árbol de profundidad 3 — PM2.5 de Cerro Navia"); plt.show()''')),

 ("## 3. El sobreajuste, ahora visible",
  "Un árbol **sin límite** de profundidad sigue preguntando hasta dejar casi cada día de "
  "entrenamiento en su propia hoja: el error de entrenamiento cae a ~0… y el de prueba se dispara. "
  "Es la firma del **sobreajuste**: memorizar en vez de aprender.",
  "Árbol sin límite: MAE en entrenamiento vs prueba",
  '''arbol_profundo = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)
mae_train = mean_absolute_error(y_train, arbol_profundo.predict(X_train))
mae_test = mean_absolute_error(y_test, arbol_profundo.predict(X_test))
print("profundidad alcanzada:", arbol_profundo.get_depth(), "| hojas:", arbol_profundo.get_n_leaves())
print("MAE entrenamiento:", round(mae_train, 2), "| MAE prueba:", round(mae_test, 2))''',
  '''# TODO: árbol SIN max_depth (solo random_state=42), entrenado con (X_train, y_train)
arbol_profundo = ...
# TODO: MAE en entrenamiento (sobre X_train) y en prueba (sobre X_test)
mae_train = ...
mae_test = ...
print("MAE entrenamiento:", mae_train, "| MAE prueba:", mae_test)''',
  '''assert arbol_profundo.get_depth() > 10, "El árbol no debe tener límite de profundidad"
assert mae_train < 0.5, "Sin límite, el árbol casi memoriza el entrenamiento"
assert mae_test > mae_arbol, "…y en datos nuevos le va peor que al árbol chico"''',
  "DecisionTreeRegressor(random_state=42).fit(X_train, y_train); mide el MAE con predict(X_train) y con predict(X_test).",
  guardado(1, '''# (ilustración) El error según la profundidad: entrenamiento baja siempre; prueba, no
prof = list(range(1, 16))
err_tr, err_te = [], []
for d in prof:
    m = DecisionTreeRegressor(max_depth=d, random_state=42).fit(X_train, y_train)
    err_tr.append(mean_absolute_error(y_train, m.predict(X_train)))
    err_te.append(mean_absolute_error(y_test, m.predict(X_test)))
plt.figure(figsize=(7, 4))
plt.plot(prof, err_tr, "o-", color="#4240e5", label="entrenamiento (memoria)")
plt.plot(prof, err_te, "s-", color="#c0392b", label="prueba 2025 (generalización)")
plt.axhline(mae_base, color="gray", ls=":", label="baseline «mañana = hoy»")
plt.xlabel("max_depth"); plt.ylabel("MAE (µg/m³)"); plt.title("Más profundo no es mejor")
plt.legend(); plt.grid(alpha=0.3); plt.tight_layout(); plt.show()''')),

 ("## 4. Bosque aleatorio e importancia de variables",
  "Un **bosque aleatorio** entrena muchos árboles, cada uno con una muestra distinta de días y de "
  "features, y **promedia** sus predicciones: la sabiduría de la multitud. Con `min_samples_leaf=5` "
  "cada hoja debe tener al menos 5 días, otra forma de frenar la memorización.\n\n"
  "De regalo trae `feature_importances_`: **cuánto pesó cada variable**. A veces saber qué manda "
  "vale más que la predicción misma.",
  "Entrena el bosque, mide su MAE y encuentra la feature más importante",
  '''bosque = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)
bosque.fit(X_train, y_train)
pred_bosque = bosque.predict(X_test)
mae_bosque = mean_absolute_error(y_test, pred_bosque)
importancias = pd.Series(bosque.feature_importances_, index=FEATURES).sort_values(ascending=False)
feature_top = importancias.idxmax()
print("MAE bosque:", round(mae_bosque, 2), "| lineal:", round(mae_lr, 2), "| baseline:", round(mae_base, 2))
print(importancias.round(3))''',
  '''# TODO: RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42), entrenado
bosque = ...
...
pred_bosque = bosque.predict(X_test)
mae_bosque = mean_absolute_error(y_test, pred_bosque)
importancias = pd.Series(bosque.feature_importances_, index=FEATURES).sort_values(ascending=False)
# TODO: nombre de la feature con mayor importancia
feature_top = ...
print("MAE bosque:", mae_bosque, "| feature más importante:", feature_top)''',
  '''assert hasattr(bosque, "estimators_") and len(bosque.estimators_) == 100
assert mae_bosque < mae_lr < mae_base, "El bosque debería superar a la recta y al baseline"
assert feature_top == "pm25_ayer"''',
  "bosque.fit(X_train, y_train); la más importante es importancias.idxmax().",
  guardado(4, '''# (ilustración) ¿Qué variable manda?
plt.figure(figsize=(6, 3.2))
importancias.sort_values().plot.barh(color="#4240e5")
plt.xlabel("importancia (suma 1)"); plt.title("Bosque aleatorio — importancia de variables")
plt.tight_layout(); plt.show()''')),

 ("## 5. De la predicción a la alerta",
  "Una autoridad no necesita el µg/m³ exacto: necesita saber **qué días avisar**. Convierte las "
  "predicciones del bosque en alertas («predice más de 50») y cuéntalas contra los días que "
  "**realmente** superaron la norma en 2025. Compáralo con alertar usando el baseline.",
  "Días detectados y falsas alarmas del bosque",
  '''real = (y_test > 50).values
alerta = pred_bosque > 50
dias_reales = int(real.sum())
detectados = int((alerta & real).sum())
falsas_alarmas = int((alerta & ~real).sum())
alerta_base = (X_test["pm25_ayer"] > 50).values
print("días reales sobre 50:", dias_reales)
print("bosque   → detectados:", detectados, "| falsas alarmas:", falsas_alarmas)
print("baseline → detectados:", int((alerta_base & real).sum()), "| falsas alarmas:", int((alerta_base & ~real).sum()))''',
  '''real = (y_test > 50).values
# TODO: alerta = True donde el bosque predice más de 50
alerta = ...
dias_reales = int(real.sum())
# TODO: detectados = alerta Y real; falsas_alarmas = alerta Y NO real (usa & y ~)
detectados = ...
falsas_alarmas = ...
print("días reales:", dias_reales, "| detectados:", detectados, "| falsas alarmas:", falsas_alarmas)''',
  '''assert dias_reales == int((y_test > 50).sum())
assert detectados == int(((pred_bosque > 50) & (y_test.values > 50)).sum())
assert falsas_alarmas == int(((pred_bosque > 50) & (y_test.values <= 50)).sum())
assert 0 < detectados <= dias_reales''',
  "alerta = pred_bosque > 50; detectados = int((alerta & real).sum()); falsas_alarmas = int((alerta & ~real).sum()).",
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

En el ejercicio 5, el bosque da **menos falsas alarmas** que el baseline, pero se le escapan **más**
días reales sobre la norma. ¿Qué error es más caro para la salud pública: avisar de más o avisar de
menos? ¿Moverías el umbral de alerta por debajo de 50? (En R2-06 y R2-07 esto tiene nombre:
*precision* y *recall*.)'''

CIERRE = '''## Errores típicos

- **No fijar `max_depth`** (ni `min_samples_leaf`) y sorprenderse con el sobreajuste.
- **Elegir la profundidad mirando la prueba** → en rigor, se elige con un conjunto de **validación** aparte (R2-07).
- **Leer la importancia como causalidad** → `pm25_ayer` manda porque el aire persiste, no porque «cause» el de hoy.

## Cierre

- Un **árbol** predice con preguntas sí/no: interpretable, pero inestable y propenso a sobreajustar.
- La **profundidad** controla la complejidad: el error de entrenamiento siempre baja; el de prueba, no.
- El **bosque aleatorio** promedia muchos árboles: aquí supera a la recta y al baseline.
- La **importancia de variables** dice qué manda; la **alerta** convierte el modelo en decisión.

> *En R2-06 pasarás de predecir números a predecir categorías (clasificación) y a agrupar sin etiquetas (clustering).*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-05", "Modelos basados en árboles", "R2", "Científico de Datos", "11",
                      ["Entrenar e **interpretar** un árbol de decisión.",
                       "Ver y controlar el **sobreajuste** con la profundidad.",
                       "Entrenar un **bosque aleatorio** y leer la **importancia de variables**.",
                       "Comparar de forma justa contra el **baseline** y la regresión lineal de R2-04.",
                       "Convertir predicciones en **alertas** sobre la norma de 50 µg/m³."],
                      "entrenar, comparar e interpretar árboles y bosques aleatorios, controlando el sobreajuste.",
                      "PM2.5 diario, temperatura y humedad de Cerro Navia 2020–2025 (SINCA, MMA) — el mismo problema de R2-04.",
                      n_checks=len(EJ)),
        h.code(SETUP),
        h.md(INTRO),
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


# ── Profundización (transferencia: sismos USGS) ──────────────────────────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, export_text
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
CSV = "sismos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)
sis = pd.read_csv(CSV)    # sismos M ≥ 4,5 en Chile 2020–2025 (USGS)
print("sismos:", sis.shape)
sis.head()'''

PROF_EJ = [
 ("## 1. ¿A qué profundidad ocurre un sismo?",
  "Cada fila es un sismo con su ubicación, magnitud y **profundidad** (km). ¿Se puede predecir la "
  "profundidad solo con latitud, longitud y magnitud? Aquí no pronosticamos el futuro sino una "
  "relación física, así que un **corte aleatorio** es razonable (con una advertencia: las réplicas "
  "de un mismo terremoto se parecen entre sí). Primero, el baseline: predecir siempre la profundidad promedio.",
  "Separa 70/30 y mide el baseline",
  '''FEAT = ["latitud", "longitud", "magnitud"]
X = sis[FEAT]
y = sis["profundidad_km"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
mae_base = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("entrenamiento:", len(X_train), "| prueba:", len(X_test), "| MAE baseline:", round(mae_base, 1), "km")''',
  '''FEAT = ["latitud", "longitud", "magnitud"]
X = sis[FEAT]
y = sis["profundidad_km"]
# TODO: train_test_split(X, y, test_size=0.3, random_state=42)
X_train, X_test, y_train, y_test = ..., ..., ..., ...
# TODO: MAE de predecir siempre y_train.mean()
mae_base = ...
print("MAE baseline:", mae_base)''',
  '''assert len(X_train) + len(X_test) == len(sis)
assert abs(len(X_test) / len(sis) - 0.3) < 0.01
assert abs(mae_base - mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))) < 1e-9''',
  "train_test_split(X, y, test_size=0.3, random_state=42); np.full(len(y_test), y_train.mean())."),

 ("## 2. Un árbol que se puede leer",
  "Entrena un árbol de profundidad 3 e **imprime sus reglas** con `export_text`. Fíjate en qué "
  "variable pregunta primero.",
  "Árbol de profundidad 3: MAE y reglas",
  '''arbol = DecisionTreeRegressor(max_depth=3, random_state=42).fit(X_train, y_train)
mae_arbol = mean_absolute_error(y_test, arbol.predict(X_test))
print("MAE árbol:", round(mae_arbol, 1), "km | baseline:", round(mae_base, 1), "km\\n")
print(export_text(arbol, feature_names=FEAT))''',
  '''# TODO: árbol de profundidad 3 (random_state=42) entrenado con (X_train, y_train)
arbol = ...
# TODO: MAE en prueba
mae_arbol = ...
print("MAE árbol:", mae_arbol, "| baseline:", mae_base)
print(export_text(arbol, feature_names=FEAT))''',
  '''assert arbol.get_depth() == 3
assert mae_arbol < mae_base / 2, "El árbol debería reducir el error a menos de la mitad"''',
  "DecisionTreeRegressor(max_depth=3, random_state=42).fit(X_train, y_train)."),

 ("## 3. Sobreajuste, otra vez",
  "Sin límite de profundidad, el árbol memoriza los 1.120 sismos de entrenamiento. Compruébalo.",
  "Árbol sin límite: entrenamiento vs prueba",
  '''arbol_profundo = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)
mae_train = mean_absolute_error(y_train, arbol_profundo.predict(X_train))
mae_test = mean_absolute_error(y_test, arbol_profundo.predict(X_test))
print("MAE entrenamiento:", round(mae_train, 1), "km | MAE prueba:", round(mae_test, 1), "km")''',
  '''# TODO: árbol sin max_depth (random_state=42) y sus MAE de entrenamiento y prueba
arbol_profundo = ...
mae_train = ...
mae_test = ...
print("MAE entrenamiento:", mae_train, "| MAE prueba:", mae_test)''',
  '''assert mae_train < 1, "Sin límite, el error de entrenamiento es casi 0"
assert mae_test > mae_train + 5, "…pero en prueba el error es mucho mayor"''',
  "DecisionTreeRegressor(random_state=42).fit(X_train, y_train); MAE con predict(X_train) y predict(X_test)."),

 ("## 4. El bosque y la física: ¿qué variable manda?",
  "Entrena un bosque aleatorio y mira la importancia de variables. Si la geología tiene razón, una "
  "de las tres debería dominar.",
  "Bosque aleatorio: MAE e importancia",
  '''bosque = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42).fit(X_train, y_train)
mae_bosque = mean_absolute_error(y_test, bosque.predict(X_test))
importancias = pd.Series(bosque.feature_importances_, index=FEAT).sort_values(ascending=False)
feature_top = importancias.idxmax()
print("MAE bosque:", round(mae_bosque, 1), "km | árbol:", round(mae_arbol, 1), "| baseline:", round(mae_base, 1))
print(importancias.round(3))''',
  '''# TODO: RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42), entrenado
bosque = ...
mae_bosque = mean_absolute_error(y_test, bosque.predict(X_test))
importancias = pd.Series(bosque.feature_importances_, index=FEAT).sort_values(ascending=False)
# TODO: la feature más importante
feature_top = ...
print("MAE bosque:", mae_bosque, "| feature más importante:", feature_top)''',
  '''assert mae_bosque < mae_arbol
assert feature_top == "longitud"''',
  "bosque.fit(X_train, y_train) y importancias.idxmax()."),
]

PROF_CIERRE = '''## La subducción, descubierta por un árbol

La **longitud** manda: mientras más al **este** (tierra adentro) ocurre un sismo, más **profundo**
es. Es la huella de la **subducción**: la placa de Nazca se hunde bajo la Sudamericana, inclinada
hacia el este, y los sismos siguen esa placa. El árbol no sabe geología — la encontró en los datos.
La magnitud casi no aporta: un sismo grande puede ser superficial o profundo.'''

PROF_VIZ = '''# (ilustración) Profundidad según longitud: la placa que se hunde hacia el este
try:
    plt.figure(figsize=(7, 4))
    plt.scatter(sis["longitud"], sis["profundidad_km"], s=8, alpha=0.4, color="#4240e5")
    plt.gca().invert_yaxis()
    plt.xlabel("longitud (° — más a la derecha = más al este)"); plt.ylabel("profundidad (km)")
    plt.title("Sismos M ≥ 4,5 en Chile 2020–2025"); plt.tight_layout(); plt.show()
except Exception:
    print("ℹ️ Ejecuta la celda de preparación primero.")'''

PROF_HEADER = '''# R2-05 · Modelos basados en árboles — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: árboles, sobreajuste e importancia de variables sobre otro dato
público, el catálogo de **sismos M ≥ 4,5 en Chile 2020–2025** del Servicio Geológico de EE.UU. (USGS).
¿Se puede predecir la **profundidad** de un sismo con su ubicación y magnitud? Un árbol de 3 preguntas
te va a mostrar algo que los geólogos ya saben.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md(PROF_CIERRE))
    cells.append(h.code(PROF_VIZ))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-05.*"))
    nb.cells = cells
    return nb


README = '''# R2-05 · Modelos basados en árboles

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-05-modelos-de-arboles/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.

**Árboles de decisión** y **bosques aleatorios** sobre el mismo problema de R2-04 — el PM2.5 de mañana
en Cerro Navia (`aire_diario.csv`, SINCA), con el mismo corte temporal — para comparar de forma justa
contra el baseline y la regresión lineal. Sobreajuste según la profundidad, **importancia de variables**
y el paso de la predicción a la **alerta** sobre la norma de 50 µg/m³. La profundización transfiere los
árboles a los sismos de Chile (`sismos.csv`, USGS): predecir la profundidad y descubrir la subducción.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: un árbol interpretable sobre sismos M ≥ 4,5 (2020–2025).
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.

*Fuentes: SINCA — Ministerio del Medio Ambiente; USGS — catálogo sísmico FDSN.*
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
