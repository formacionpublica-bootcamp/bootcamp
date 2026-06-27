# D12 · Pipelines reproducibles

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Línea B · *Data Scientist* · Semana 13 · Módulo específico de la ruta de Ciencia de Datos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B5-pipelines-reproducibles/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

Hasta D11 el estudiante hacía el preprocesamiento y el modelo por separado. Este módulo enseña a
hacerlo **bien y de forma reproducible**, con tres herramientas de uso diario: **pipelines** (encadenar
escalado + modelo en un solo objeto), **validación cruzada** (evaluación más honesta que una sola
división) y el **guardado de modelos** con `joblib` (reutilizar sin reentrenar). El hilo conductor
es la **reproducibilidad** y la prevención de la **fuga de información** (*data leakage*).

**Competencia de salida:** encadenar preprocesamiento y modelo en un pipeline de scikit-learn,
evaluarlo con validación cruzada, entender por qué el pipeline evita el *data leakage* al escalar, y
guardar un modelo entrenado para reutilizarlo.

## Dato real y Fuente

Cantidad de artículos, tamaño del proveedor (`tamano_num`) y monto total en compras públicas de alimentos de **MercadoPúblico / ChileCompra**. Se mantiene el dato para **profundizar**: hoy lo central es el método. Se introduce un modelo nuevo, **K-vecinos (KNN)**, que mide distancias y por eso **necesita** escalado — lo que hace que el pipeline sea imprescindible.

**Dataset:** El archivo `compras_ml.csv` ya viene guardado estáticamente en la carpeta del módulo. El notebook lo cargará automáticamente (cuenta con un descargador de respaldo para Google Colab).

## Cómo se usa

1. Abre `leccion.ipynb` con **Open in Colab** (solo necesitas una cuenta de Google).
2. Ejecuta las celdas en orden y completa cada `TODO`.
3. Cada ejercicio termina en una **celda de chequeo** que muestra ✅ o una pista. Logrado cuando las 4 dan ✅.

## Contenido

| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante. |
| `solucion.ipynb` | Soluciones de referencia (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `compras_ml.csv` | Dataset de compras de alimentos, cantidades, montos y proveedores. |
| `README.md` | Esta portada. |

## Los 4 ejercicios

1. **Construir el pipeline** — `Pipeline([("escalador", StandardScaler()), ("modelo", KNeighborsRegressor(3))])`.
2. **Entrenar y evaluar** — `fit`/`predict` del pipeline y MAE en prueba.
3. **Validación cruzada** — `cross_val_score` con `KFold(5)` y MAE promedio.
4. **Guardar y reutilizar** — `joblib.dump`/`load` y predicción de una compra nueva.

## Verificación de calidad

- Solución ejecutada: **4/4 ✅** (KNN pipeline MAE prueba ≈ 74,480.56 CLP; validación cruzada promedio ≈ 90,675.07 CLP; modelo guardado y recargado predice ≈ 243,166.67 CLP).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Nota de diseño

Se optó por utilizar el modelo KNN Regressor como estimador para que el escalado de variables (cantidad y tamano_num) —y por tanto la necesidad del pipeline— sean genuinamente necesarios y visualizables por el estudiante.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0?
- [ ] ¿Queda clara la idea de pipeline (un objeto, mismo `fit`/`predict`) y por qué evita el leakage?
- [ ] ¿Se entiende la validación cruzada como evaluación más honesta?
- [ ] ¿El guardado con joblib y su valor (reutilizar, puente a D13) se entienden?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: el **leakage** por preprocesar antes de separar (ajustar *solo* en train), la separación
**fit/transform**, las **semillas**, el **pipeline como contrato** y la consistencia **train/serve**. Con
4 ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B5-pipelines-reproducibles/profundiza.ipynb)

---

*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
