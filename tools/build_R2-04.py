"""build_R2-04.py — módulo R2-04 (Fundamentos de Machine Learning).

Rama R2 (Científico de Datos). Rearmado 2026: ancla de la
rama = calidad del aire (PM2.5 diario SINCA). Mismo arco que la versión anterior —
aprendizaje supervisado (X → y), separar un conjunto de prueba, fit/predict, MAE
honesto en prueba, predecir un caso nuevo — ahora como problema real de pronóstico:
el PM2.5 de mañana en Cerro Navia con temperatura, humedad, mes, día de la semana y
el rezago (PM2.5 de ayer). Corte TEMPORAL (entrenar con 2020–2024, probar en 2025) y
un baseline ingenuo («mañana = hoy») que el modelo debe batir.
Profundiza = transferencia con matrícula 2025 (MINEDUC): predecir cursos desde la
matrícula (corte aleatorio, sin tiempo) y la trampa de la fuga de datos.

Uso:  /opt/anaconda3/bin/python tools/build_R2-04.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-04-fundamentos-de-ml")

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
from sklearn.metrics import mean_absolute_error

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "aire_diario.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)

df = pd.read_csv(CSV, parse_dates=["fecha"])
# Estación ancla: Cerro Navia (RM), ordenada por fecha (un día por fila, sin días faltantes).
cn = df[df["estacion"] == "Cerro Navia"].sort_values("fecha").reset_index(drop=True)
print("Cerro Navia:", cn.shape, "| desde", cn["fecha"].min().date(), "hasta", cn["fecha"].max().date())
cn.head()'''

INTRO = '''## ¿Qué es el *machine learning*?

Programar «a la antigua» es **escribir reglas a mano**: *si hace frío y no hay viento, el aire
estará malo*. El *machine learning* lo da vuelta: le mostramos al computador **muchos ejemplos**
con la respuesta conocida y dejamos que **descubra la regla solo**.

> 🧠 **Analogía.** A nadie le enseñaron a reconocer un día de smog con una lista de reglas: viste
> muchos inviernos y aprendiste el patrón. Un modelo hace eso con datos.

### Aprendizaje supervisado
- **Features (`X`):** lo que el modelo usa para predecir — temperatura, humedad, mes, día de la semana y el PM2.5 de ayer.
- **Objetivo (`y`):** lo que queremos predecir — el **PM2.5 del día** en Cerro Navia.

| Tipo | Predice | Ejemplo |
| --- | --- | --- |
| **Regresión** | un **número** | µg/m³ de PM2.5 mañana |
| **Clasificación** | una **categoría** | ¿mañana se supera la norma de 50, sí o no? |

Hoy hacemos **regresión**. La pregunta pública es concreta: si pudieras anticipar el PM2.5 de
mañana, podrías **avisar antes** a la población y a los servicios de salud.'''

EJ = [
 ("## 1. Fabricar las *features* (incluido el rezago)",
  "Un modelo solo puede usar lo que le damos en columnas. La *feature* más valiosa para pronosticar "
  "es, casi siempre, **el valor de ayer** (el *rezago* o *lag*): `shift(1)` corre la columna una fila "
  "hacia abajo. Como `cn` está ordenada por fecha y no le faltan días, la fila anterior es exactamente ayer.",
  "Crea `pm25_ayer`, `mes` y `dia_semana`",
  '''cn["pm25_ayer"] = cn["pm25"].shift(1)
cn["mes"] = cn["fecha"].dt.month
cn["dia_semana"] = cn["fecha"].dt.dayofweek          # 0 = lunes ... 6 = domingo
FEATURES = ["temp_media", "humedad_media", "mes", "dia_semana", "pm25_ayer"]
datos = cn.dropna(subset=FEATURES + ["pm25"])         # solo días completos
print("días con todas las features:", len(datos))
datos[["fecha", "pm25", "pm25_ayer", "mes", "dia_semana"]].head()''',
  '''# TODO: PM2.5 del día anterior -> cn["pm25"].shift(1)
cn["pm25_ayer"] = ...
cn["mes"] = cn["fecha"].dt.month
# TODO: día de la semana (0 = lunes ... 6 = domingo) -> cn["fecha"].dt.dayofweek
cn["dia_semana"] = ...
FEATURES = ["temp_media", "humedad_media", "mes", "dia_semana", "pm25_ayer"]
datos = cn.dropna(subset=FEATURES + ["pm25"])         # solo días completos
print("días con todas las features:", len(datos))''',
  '''assert np.allclose(datos["pm25_ayer"].astype(float), cn["pm25"].shift(1).loc[datos.index])
assert datos["dia_semana"].between(0, 6).all()
assert datos[FEATURES].notna().all().all()''',
  'cn["pm25"].shift(1) trae el valor de la fila anterior; cn["fecha"].dt.dayofweek da 0..6.',
  None),

 ("## 2. La regla de oro: probar con datos que el modelo no vio — y del **futuro**",
  "Si evalúas con los mismos datos con que entrenaste, el modelo puede «memorizar» y parecer perfecto. "
  "Por eso se reserva un **conjunto de prueba**. Pero aquí hay un detalle clave: queremos **pronosticar el "
  "futuro**, así que la prueba debe imitar ese uso. **No barajamos** los días al azar: entrenamos con "
  "**2020–2024** y probamos en **2025**, un año completo que el modelo nunca vio.\n\n"
  "> ⚠️ Barajar una serie de tiempo mete días de 2025 en el entrenamiento y deja que el modelo «vea» "
  "vecinos del futuro: la evaluación ya no mide lo que importa (y puede quedar maquillada). En R2-07 profundizarás la validación temporal.",
  "Corte temporal: entrenamiento antes de 2025, prueba en 2025",
  '''corte = pd.Timestamp("2025-01-01")
train = datos[datos["fecha"] < corte]
test = datos[datos["fecha"] >= corte]
X_train, y_train = train[FEATURES], train["pm25"]
X_test, y_test = test[FEATURES], test["pm25"]
print("entrenamiento:", len(train), "días (2020–2024) | prueba:", len(test), "días (2025)")''',
  '''corte = pd.Timestamp("2025-01-01")
# TODO: train = días ANTES del corte; test = días desde el corte en adelante
train = ...
test = ...
X_train, y_train = train[FEATURES], train["pm25"]
X_test, y_test = test[FEATURES], test["pm25"]
print("entrenamiento:", len(train), "| prueba:", len(test))''',
  '''assert train["fecha"].max() < test["fecha"].min(), "Todo el entrenamiento debe ser anterior a la prueba"
assert len(train) + len(test) == len(datos)
assert (test["fecha"].dt.year == 2025).all()
assert list(X_train.columns) == FEATURES''',
  'train = datos[datos["fecha"] < corte] y test = datos[datos["fecha"] >= corte].',
  None),

 ("## 3. Un *baseline*: la vara que el modelo debe superar",
  "Antes de entrenar nada, define una predicción **ingenua**. Para el aire, la más dura de batir es la "
  "**persistencia**: «mañana será igual que hoy» (predecir con `pm25_ayer`). Si tu modelo no le gana, "
  "no sirve — por sofisticado que sea. La métrica: **MAE** (error absoluto medio), en µg/m³.",
  "MAE del baseline de persistencia (y de «predecir el promedio»)",
  '''pred_base = X_test["pm25_ayer"]
mae_base = mean_absolute_error(y_test, pred_base)
mae_media = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("MAE «mañana = hoy»:", round(mae_base, 2), "µg/m³ | MAE «siempre el promedio»:", round(mae_media, 2))''',
  '''# TODO: la predicción ingenua es la columna pm25_ayer de X_test
pred_base = ...
# TODO: mean_absolute_error(y_test, pred_base)
mae_base = ...
mae_media = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("MAE «mañana = hoy»:", mae_base, "| MAE «siempre el promedio»:", round(mae_media, 2))''',
  '''assert abs(mae_base - mean_absolute_error(y_test, X_test["pm25_ayer"])) < 1e-9
assert mae_base < mae_media, "La persistencia es mucho mejor que predecir siempre el promedio"''',
  'pred_base = X_test["pm25_ayer"] y mae_base = mean_absolute_error(y_test, pred_base).',
  None),

 ("## 4. Entrenar tu primer modelo: `fit` y `predict`",
  "La **regresión lineal** busca la mejor combinación «número × feature» para acercarse a `y`. "
  "En scikit-learn todos los modelos se usan igual:\n\n"
  "```python\nmodelo = LinearRegression()\nmodelo.fit(X_train, y_train)    # 1) APRENDER del pasado\n"
  "y_pred = modelo.predict(X_test)  # 2) PREDECIR días que no vio\n```\n\n"
  "Compara el MAE en prueba con el del baseline, y con el MAE en **entrenamiento**: si el de "
  "entrenamiento fuera mucho menor que el de prueba, sería la alarma de **sobreajuste**.",
  "Entrena, predice 2025 y compara con el baseline",
  '''modelo = LinearRegression()
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)
mae_lr = mean_absolute_error(y_test, y_pred)
mae_lr_train = mean_absolute_error(y_train, modelo.predict(X_train))
print("MAE prueba:", round(mae_lr, 2), "| MAE entrenamiento:", round(mae_lr_train, 2), "| baseline:", round(mae_base, 2))
print("Coeficientes (µg/m³ por unidad de cada feature):")
print(pd.Series(modelo.coef_, index=FEATURES).round(2))''',
  '''# TODO: crea el modelo, entrénalo con (X_train, y_train) y predice sobre X_test
modelo = ...
...
y_pred = ...
mae_lr = mean_absolute_error(y_test, y_pred)
mae_lr_train = mean_absolute_error(y_train, modelo.predict(X_train))
print("MAE prueba:", mae_lr, "| MAE entrenamiento:", mae_lr_train, "| baseline:", mae_base)''',
  '''assert hasattr(modelo, "coef_"), "Falta modelo.fit(X_train, y_train)"
assert abs(mae_lr - mean_absolute_error(y_test, modelo.predict(X_test))) < 1e-9
assert mae_lr < mae_base, "El modelo debería ganarle (por poco) al baseline"''',
  "modelo = LinearRegression(); modelo.fit(X_train, y_train); y_pred = modelo.predict(X_test).",
  guardado(4, '''# (ilustración) 2025: lo real vs lo que predijo el modelo
plt.figure(figsize=(10, 3.8))
plt.plot(test["fecha"], y_test, color="#999999", lw=1, label="real")
plt.plot(test["fecha"], y_pred, color="#4240e5", lw=1.2, label="modelo lineal")
plt.axhline(50, color="#c0392b", ls="--", label="norma 24 h (50 µg/m³)")
plt.ylabel("PM2.5 (µg/m³)"); plt.title("Cerro Navia 2025 — datos que el modelo nunca vio")
plt.legend(); plt.tight_layout(); plt.show()''')),

 ("## 5. Usar el modelo: un día nuevo",
  "Para esto entrenamos modelos: **estimar lo que todavía no ocurre**. scikit-learn pide la entrada "
  "con la **misma forma** que el entrenamiento: una tabla con las mismas columnas, en el mismo orden.",
  "Pronostica un miércoles de julio frío y húmedo",
  '''dia_nuevo = pd.DataFrame([{"temp_media": 7.0, "humedad_media": 85.0, "mes": 7,
                           "dia_semana": 2, "pm25_ayer": 60.0}])[FEATURES]
pm25_estimado = float(modelo.predict(dia_nuevo)[0])
supera_norma = pm25_estimado > 50
print("PM2.5 estimado:", round(pm25_estimado, 1), "µg/m³ | ¿sobre la norma?", supera_norma)''',
  '''dia_nuevo = pd.DataFrame([{"temp_media": 7.0, "humedad_media": 85.0, "mes": 7,
                           "dia_semana": 2, "pm25_ayer": 60.0}])[FEATURES]
# TODO: predice con el modelo y toma el primer valor con [0]
pm25_estimado = ...
# TODO: True si el estimado supera 50 µg/m³
supera_norma = ...
print("PM2.5 estimado:", pm25_estimado, "| ¿sobre la norma?", supera_norma)''',
  '''assert abs(pm25_estimado - float(modelo.predict(dia_nuevo)[0])) < 1e-6
assert supera_norma == (pm25_estimado > 50)''',
  "float(modelo.predict(dia_nuevo)[0]) y supera_norma = pm25_estimado > 50.",
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

1. El modelo usa la **temperatura y la humedad del mismo día** que predice. En la vida real, para
   pronosticar mañana necesitarías el **pronóstico meteorológico** de mañana. ¿Qué le pasaría al
   error si el pronóstico del tiempo también se equivoca?
2. La regresión lineal lee `mes` como un número: para ella, diciembre (12) es «más» que julio (7).
   ¿Tiene sentido? (En R2-05 verás modelos que no tienen ese problema.)'''

CIERRE = '''## Errores típicos

- **Entrenar con los datos de prueba** → `fit` siempre con `X_train`, nunca con `X_test`.
- **Barajar una serie de tiempo** → el modelo «ve el futuro» y la evaluación se infla.
- **No tener baseline** → un MAE de 7 µg/m³ no dice nada si no sabes que «mañana = hoy» ya logra ~7,4.
- **`y` con doble corchete** → el objetivo va con uno (`train["pm25"]`), las features con lista.

## Cierre

- **Supervisado:** features (`X`) → objetivo (`y`); hoy, regresión del PM2.5.
- **Corte temporal:** entrenar con el pasado, probar con el futuro.
- **Baseline primero:** el modelo lineal le gana a la persistencia, pero por poco — y eso es información honesta.
- **`fit` / `predict`:** el patrón es el mismo para todos los modelos que vienen.

> *En R2-05 cambiarás la recta por árboles y bosques — mismo dato, mismo corte, misma vara.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-04", "Fundamentos de Machine Learning", "R2", "Científico de Datos", "10",
                      ["Plantear un problema **supervisado**: features (`X`) y objetivo (`y`).",
                       "Fabricar una *feature* de **rezago** (`shift`).",
                       "Separar entrenamiento y prueba con **corte temporal**.",
                       "Medir un **baseline** ingenuo y entrenar una **regresión lineal** (`fit`/`predict`).",
                       "Evaluar con **MAE** en prueba y **predecir** un caso nuevo."],
                      "entrenar y evaluar con honestidad un primer modelo de regresión que pronostica el PM2.5.",
                      "PM2.5 diario, temperatura y humedad de Cerro Navia 2020–2025 (SINCA, MMA).",
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


# ── Profundización (transferencia: matrícula escolar) ────────────────────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)
mat = pd.read_csv(CSV)    # matrícula 2025 por establecimiento (MINEDUC)
print("establecimientos:", mat.shape)
mat[["nombre", "rural", "mat_total", "mat_hombres", "mat_mujeres", "cursos"]].head()'''

PROF_EJ = [
 ("## 1. Otro problema, el mismo método: ¿cuántos cursos tendrá un colegio?",
  "Planificar dotación docente o infraestructura exige estimar **cursos** a partir de la **matrícula**. "
  "Aquí no hay tiempo de por medio (es una foto de 2025), así que un **corte aleatorio** sí es válido. "
  "Primero, el baseline: predecir siempre el promedio de cursos del entrenamiento.",
  "Divide 70/30 al azar y mide el baseline",
  '''X = mat[["mat_total"]]
y = mat["cursos"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
mae_base = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("entrenamiento:", len(X_train), "| prueba:", len(X_test), "| MAE baseline:", round(mae_base, 2), "cursos")''',
  '''X = mat[["mat_total"]]
y = mat["cursos"]
# TODO: train_test_split(X, y, test_size=0.3, random_state=42)
X_train, X_test, y_train, y_test = ..., ..., ..., ...
# TODO: MAE de predecir siempre y_train.mean()
mae_base = ...
print("MAE baseline:", mae_base)''',
  '''assert len(X_train) + len(X_test) == len(mat)
assert abs(len(X_test) / len(mat) - 0.3) < 0.01
assert abs(mae_base - mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))) < 1e-9''',
  "train_test_split(X, y, test_size=0.3, random_state=42); np.full(len(y_test), y_train.mean()) es la predicción constante."),

 ("## 2. La regresión y su lectura",
  "Entrena la regresión lineal y traduce su coeficiente a lenguaje de gestión: **cursos por cada 100 estudiantes**.",
  "Entrena, evalúa e interpreta el coeficiente",
  '''modelo = LinearRegression().fit(X_train, y_train)
mae_lr = mean_absolute_error(y_test, modelo.predict(X_test))
cursos_por_100 = 100 * modelo.coef_[0]
print("MAE:", round(mae_lr, 2), "cursos | cada 100 estudiantes ≈", round(cursos_por_100, 1), "cursos más")''',
  '''# TODO: entrena LinearRegression con (X_train, y_train)
modelo = ...
mae_lr = mean_absolute_error(y_test, modelo.predict(X_test))
# TODO: 100 * el coeficiente de mat_total (modelo.coef_[0])
cursos_por_100 = ...
print("MAE:", mae_lr, "| cursos por 100 estudiantes:", cursos_por_100)''',
  '''assert mae_lr < mae_base / 2, "El modelo debería reducir el error a menos de la mitad"
assert 1 < cursos_por_100 < 5''',
  "LinearRegression().fit(X_train, y_train); cursos_por_100 = 100 * modelo.coef_[0]."),

 ("## 3. La trampa: un modelo «perfecto» por **fuga de datos**",
  "Ahora predice `mat_total` usando `mat_hombres` y `mat_mujeres`. El resultado será casi perfecto… "
  "porque `mat_total` **es** la suma de ambas. Eso no es predecir: es copiar la respuesta. "
  "Cuando un modelo sale demasiado bueno, sospecha **fuga** (*leakage*): una feature que contiene el objetivo "
  "o que no tendrías al momento de predecir.",
  "Mide el R² del modelo con fuga",
  '''Xf = mat[["mat_hombres", "mat_mujeres"]]
Xf_tr, Xf_te, yf_tr, yf_te = train_test_split(Xf, mat["mat_total"], test_size=0.3, random_state=42)
m_fuga = LinearRegression().fit(Xf_tr, yf_tr)
r2_fuga = r2_score(yf_te, m_fuga.predict(Xf_te))
print("R² con fuga:", round(r2_fuga, 6), "← sospechosamente perfecto")''',
  '''Xf = mat[["mat_hombres", "mat_mujeres"]]
Xf_tr, Xf_te, yf_tr, yf_te = train_test_split(Xf, mat["mat_total"], test_size=0.3, random_state=42)
m_fuga = LinearRegression().fit(Xf_tr, yf_tr)
# TODO: r2_score entre yf_te y las predicciones de m_fuga sobre Xf_te
r2_fuga = ...
print("R² con fuga:", r2_fuga)''',
  '''assert r2_fuga > 0.999, "Con la suma como feature, el R² es prácticamente 1"''',
  "r2_score(yf_te, m_fuga.predict(Xf_te))."),

 ("## 4. El modelo honesto",
  "Si de verdad necesitas estimar la matrícula de un colegio, usa información que **sí tendrías** antes: "
  "cuántos `cursos` tiene y si es `rural`. El R² baja… y eso está bien: ahora es real.",
  "Predice la matrícula sin fuga y compara con su baseline",
  '''Xh = mat[["cursos", "rural"]]
Xh_tr, Xh_te, yh_tr, yh_te = train_test_split(Xh, mat["mat_total"], test_size=0.3, random_state=42)
m_honesto = LinearRegression().fit(Xh_tr, yh_tr)
mae_honesto = mean_absolute_error(yh_te, m_honesto.predict(Xh_te))
mae_base_mat = mean_absolute_error(yh_te, np.full(len(yh_te), yh_tr.mean()))
r2_honesto = r2_score(yh_te, m_honesto.predict(Xh_te))
print("MAE honesto:", round(mae_honesto, 1), "estudiantes | baseline:", round(mae_base_mat, 1), "| R²:", round(r2_honesto, 3))''',
  '''Xh = mat[["cursos", "rural"]]
Xh_tr, Xh_te, yh_tr, yh_te = train_test_split(Xh, mat["mat_total"], test_size=0.3, random_state=42)
# TODO: entrena el modelo honesto y calcula su MAE en prueba
m_honesto = ...
mae_honesto = ...
mae_base_mat = mean_absolute_error(yh_te, np.full(len(yh_te), yh_tr.mean()))
r2_honesto = r2_score(yh_te, m_honesto.predict(Xh_te))
print("MAE honesto:", mae_honesto, "| baseline:", round(mae_base_mat, 1), "| R²:", r2_honesto)''',
  '''assert mae_honesto < mae_base_mat
assert r2_honesto < r2_fuga, "El modelo honesto es peor que el tramposo… y es el único que sirve"''',
  "LinearRegression().fit(Xh_tr, yh_tr) y mean_absolute_error(yh_te, m_honesto.predict(Xh_te))."),
]

PROF_HEADER = '''# R2-04 · Fundamentos de ML — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: el mismo método (baseline → `fit`/`predict` → MAE en prueba) sobre
otro dato del Estado, la **matrícula escolar 2025** (MINEDUC). Dos lecciones nuevas: cuándo **sí** vale
un corte aleatorio (no hay tiempo de por medio) y cómo reconocer la **fuga de datos** cuando un modelo
sale «demasiado bueno».

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md('''## Para llevar

- **Aleatorio o temporal:** depende de cómo se usará el modelo. Foto de un año → aleatorio; pronóstico → temporal.
- **Demasiado bueno para ser cierto** casi siempre es fuga: pregúntate si tendrías esa feature al momento de predecir.

---

*Fin de la profundización de R2-04.*'''))
    nb.cells = cells
    return nb


README = '''# R2-04 · Fundamentos de Machine Learning

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-04-fundamentos-de-ml/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.

Tu primer modelo: **pronosticar el PM2.5 de mañana** en Cerro Navia con temperatura, humedad, mes,
día de la semana y el PM2.5 de ayer (`aire_diario.csv`, SINCA). Aprendizaje supervisado, *feature*
de rezago, **corte temporal** (entrenar 2020–2024, probar 2025), **baseline** «mañana = hoy»,
regresión lineal con `fit`/`predict`, **MAE** honesto y un pronóstico nuevo. La profundización
transfiere el método a la matrícula 2025 (`matricula.csv`): predecir cursos y cazar la **fuga de datos**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: corte aleatorio vs temporal, coeficientes y fuga de datos.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.

*Fuentes: SINCA — Ministerio del Medio Ambiente; MINEDUC — datos abiertos (matrícula 2025).*
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
