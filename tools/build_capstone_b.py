# -*- coding: utf-8 -*-
"""Capstone B (Ciencia de datos): dataset provisto (compras_ml) + scaffold de
proyecto predictivo + ejemplo resuelto + README con rúbrica y model card.
Carpeta: B8-capstone."""
import json, os, shutil

BASE = "B8-capstone"
REPO = "formacionpublica-bootcamp/bootcamp"
os.makedirs(BASE, exist_ok=True)

# 1. Dataset provisto (copia del compras_ml real)
src_csv = os.path.join("data", "compras_ml.csv")
if os.path.exists(src_csv):
    shutil.copy(src_csv, os.path.join(BASE, "compras_ml.csv"))
    print("Dataset copiado a", BASE)
else:
    print("Aviso: falta data/compras_ml.csv; conservo el existente.")

# 2. Celdas
TITULO = """# Capstone B · Predice y explica

**Formación Pública — Capa B · Ciencia de datos aplicada · Proyecto final**

Tu proyecto de cierre de la Capa B: planteas un **problema predictivo**, entrenas un modelo, lo
evalúas **con honestidad** y lo documentas con una **model card**. Integra B1–B7 (features, ML,
árboles, clasificación, pipelines, despliegue, series).

Sigue el **Ciclo Pública** con foco en *Modela*. Al final hay autoevaluación y rúbrica.

**Entregable:** este notebook completo (problema, modelo, evaluación en prueba y model card).
Súbelo a tu GitHub como pieza de portafolio."""

PASO0 = """## Paso 0 · Elige tus datos
- **Opción A (recomendada):** dataset provisto `compras_ml.csv` — compras de alimentos reales de
  ChileCompra con `cantidad`, `tamano_num`, `monto_total`, `categoria`, `tamano_proveedor`,
  `region_comprador`.
- **Opción B:** trae un CSV de tu institución con un objetivo numérico o categórico a predecir."""

CARGA = """import os, urllib.request
import pandas as pd

ARCHIVO = "compras_ml.csv"   # cámbialo por tu archivo si usas la Opción B
if not os.path.exists(ARCHIVO):
    try:
        url = "https://raw.githubusercontent.com/%s/main/B8-capstone/compras_ml.csv"
        urllib.request.urlretrieve(url, ARCHIVO)
    except Exception:
        print("Si estás en Colab, sube el archivo manualmente.")

df = pd.read_csv(ARCHIVO)
print(f"{len(df)} filas, {len(df.columns)} columnas")
df.head()""" % REPO

PASO1 = """## Paso 1 · Plantea el problema predictivo
¿Qué quieres **predecir** y con qué? Define si es **regresión** (un número, ej. `monto_total`) o
**clasificación** (una categoría, ej. `tamano_proveedor`). Buen problema = útil y respondible con
estas variables."""
PASO1_TODO = """**✍️ Tu problema:** _(escríbelo aquí; di qué predices y con qué variables)_"""
PASO1_SOL = """**✍️ Mi problema:** predecir el **monto_total** de una orden (regresión) a partir de la **cantidad** de artículos y el **tamaño del proveedor** (`tamano_num`)."""

PASO2 = """## Paso 2 · Features y objetivo
Separa las **features** (`X`, lo que usas para predecir) del **objetivo** (`y`, lo que predices).
Cuida no incluir en `X` información que "filtre" la respuesta (*leakage*)."""
PASO2_TODO = """# TODO: define X (features) e y (objetivo)
X = None
y = None"""
PASO2_SOL = """X = df[["cantidad", "tamano_num"]]
y = df["monto_total"]
print("X:", list(X.columns), "| y:", y.name)"""

PASO3 = """## Paso 3 · Train / test (con semilla)
Reserva una parte de los datos para **evaluar con honestidad**. La semilla (`random_state`) hace el
resultado reproducible."""
PASO3_TODO = """from sklearn.model_selection import train_test_split
# TODO: divide en entrenamiento y prueba (test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = (None, None, None, None)"""
PASO3_SOL = """from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")"""

PASO4 = """## Paso 4 · Entrena el modelo
Entrena un modelo con los datos de **entrenamiento**. Empieza simple (regresión lineal o un árbol);
lo simple e interpretable suele bastar."""
PASO4_TODO = """from sklearn.linear_model import LinearRegression
# TODO: crea el modelo, entrénalo con X_train, y_train y guárdalo en 'modelo'
modelo = None"""
PASO4_SOL = """from sklearn.linear_model import LinearRegression
modelo = LinearRegression()
modelo.fit(X_train, y_train)
print("Modelo entrenado. Coeficientes:", dict(zip(X.columns, modelo.coef_.round(1))))"""

PASO5 = """## Paso 5 · Evalúa con honestidad (en PRUEBA)
Mide el error en los datos de **prueba** (que el modelo no vio). Para regresión, el MAE (error
absoluto medio) es claro: "en promedio me equivoco en $X"."""
PASO5_TODO = """from sklearn.metrics import mean_absolute_error
# TODO: predice sobre X_test y calcula el MAE contra y_test; guárdalo en 'mae'
mae = None
print("MAE en prueba:", mae)"""
PASO5_SOL = """from sklearn.metrics import mean_absolute_error
pred = modelo.predict(X_test)
mae = mean_absolute_error(y_test, pred)
print(f"MAE en prueba: ${mae:,.0f} CLP")"""

PASO6 = """## Paso 6 · Model card y conclusión
Una *model card* documenta el modelo para que otros lo usen con responsabilidad."""
PASO6_TODO = PASO6 + """

- **Uso previsto:** _(¿para qué sirve y para qué NO?)_
- **Datos:** _(fuente y período)_
- **Variables (features):** _(cuáles)_
- **Desempeño:** _(MAE en prueba)_
- **Límites:** _(¿cuándo falla?)_
- **Riesgos éticos:** _(¿qué decisión NO debería tomarse solo con esto?)_"""
PASO6_SOL = PASO6 + """

- **Uso previsto:** estimar de forma orientativa el monto de una compra de alimentos según cantidad
  y tamaño de proveedor. **No** sirve para aprobar/rechazar compras ni para fiscalizar.
- **Datos:** órdenes de compra de licitaciones de ChileCompra (rubro alimentos), muestra.
- **Variables:** `cantidad`, `tamano_num`.
- **Desempeño:** MAE en prueba ≈ ver Paso 5 (orden de magnitud de cientos de miles de CLP).
- **Límites:** la relación monto≈precio×cantidad lo hace intuitivo pero simple; ignora el tipo de
  producto y precios unitarios muy distintos.
- **Riesgos éticos:** una estimación no es un juicio sobre un organismo o proveedor; usarla como
  control automático sería injusto. Requiere supervisión humana."""

AUTOEVAL = """# Autoevaluación suave — confirma que hiciste cada paso (no califica la calidad del modelo).
hechos = {
    "Definiste X e y": "X" in dir() and X is not None and "y" in dir() and y is not None,
    "Separaste prueba (X_test)": "X_test" in dir() and X_test is not None,
    "Entrenaste un modelo": "modelo" in dir() and modelo is not None,
    "Evaluaste en prueba (mae)": "mae" in dir() and mae is not None,
}
for paso, ok in hechos.items():
    print(("✅ " if ok else "⬜ ") + paso)
print("\\nEvalúate con la rúbrica del README (aprobado: 12/18).")"""

RUBRICA = """## Rúbrica (autoevalúate, 0–3 cada una)
| Criterio | 0–3 |
|---|---|
| Problema predictivo bien planteado | |
| Features y objetivo correctos (sin *leakage*) | |
| Train/test bien hecho (con semilla) | |
| Modelo entrenado | |
| Evaluación honesta (métrica en PRUEBA) | |
| Model card (límites y ética) | |

**Aprobado: 12 de 18.** → Habilita la **certificación: Data Scientist del sector público**
(junto con el Proyecto Final, si tu institución lo pide más extenso)."""


def md(t, cid): return {"cell_type": "markdown", "metadata": {}, "id": cid, "source": t}
def code(t, cid): return {"cell_type": "code", "metadata": {}, "id": cid, "execution_count": None, "outputs": [], "source": t}

def build(resuelto):
    g = lambda sol, todo: sol if resuelto else todo
    cells = [
        md(TITULO, "c00"), md(PASO0, "c01"), code(CARGA, "c02"),
        md(PASO1, "c03"), md(g(PASO1_SOL, PASO1_TODO), "c04"),
        md(PASO2, "c05"), code(g(PASO2_SOL, PASO2_TODO), "c06"),
        md(PASO3, "c07"), code(g(PASO3_SOL, PASO3_TODO), "c08"),
        md(PASO4, "c09"), code(g(PASO4_SOL, PASO4_TODO), "c10"),
        md(PASO5, "c11"), code(g(PASO5_SOL, PASO5_TODO), "c12"),
        md(g(PASO6_SOL, PASO6_TODO), "c13"),
        code(AUTOEVAL, "c14"), md(RUBRICA, "c15"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "proyecto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "ejemplo_resuelto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

README = """# Capstone B · Predice y explica

**Proyecto final de la Capa B (Ciencia de datos aplicada)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/%s/blob/main/B8-capstone/proyecto.ipynb)

## Qué es
Planteas un **problema predictivo**, entrenas un modelo, lo evalúas **con honestidad** (en datos de
prueba) y lo documentas con una **model card**. Integra todo lo de la Capa B.

## Cómo entregar
- **Opción A (recomendada):** dataset provisto `compras_ml.csv` (compras de alimentos reales de ChileCompra).
- **Opción B:** trae un CSV de **tu institución** con un objetivo a predecir.

## Los pasos
1. **Problema** — qué predices (regresión o clasificación) y con qué.
2. **Features y objetivo** — `X` e `y`, sin *leakage*.
3. **Train/test** — con semilla (reproducible).
4. **Modela** — entrena (empieza simple).
5. **Evalúa** — métrica en **prueba** (ej. MAE).
6. **Model card** — uso previsto, datos, límites, riesgos éticos.

## Rúbrica (0–3 c/u · aprobado 12/18)
| Criterio | Qué se evalúa |
|---|---|
| Problema bien planteado | Útil y respondible con los datos. |
| Features y objetivo | Correctos y sin *leakage*. |
| Train/test con semilla | Evaluación reproducible y honesta. |
| Modelo entrenado | Corre y predice. |
| Evaluación en PRUEBA | Mide en datos no vistos. |
| Model card | Documenta límites y ética. |

## Archivos
| Archivo | Para qué |
| --- | --- |
| `proyecto.ipynb` | Scaffold del estudiante (los pasos con TODO). |
| `ejemplo_resuelto.ipynb` | Ejemplo completo de referencia (uso interno / modelo). |
| `compras_ml.csv` | Dataset provisto: compras de alimentos reales de ChileCompra. |
| `README.md` | Esta portada + rúbrica. |

→ Al aprobarlo, junto con el resto de la Capa B, obtienes la **certificación: Data Scientist del
sector público**.

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Dirección ChileCompra (datos-abiertos.chilecompra.cl)
""" % REPO

open(os.path.join(BASE, "README.md"), "w", encoding="utf-8").write(README)
print("Capstone B generado en:", BASE)
print("Archivos:", sorted(os.listdir(BASE)))
