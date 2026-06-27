# D11 · Clasificación y clustering

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Línea B · *Data Scientist* · Semana 12 · Módulo específico de la ruta de Ciencia de Datos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B4-clasificacion-y-clustering/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

Dos saltos sobre lo aprendido en D9–D10. Primero, de predecir **números** (regresión) a predecir
**categorías**: la **clasificación** supervisada, con el mismo `fit`/`predict` y evaluada con
exactitud y matriz de confusión. Segundo, el mundo **sin etiquetas**: el **clustering** (K-Means),
donde el modelo **descubre grupos** por sí solo.

**Competencia de salida:** entrenar y evaluar un clasificador (exactitud y matriz de confusión), y
aplicar *clustering* con K-Means (incluido el escalado de variables), distinguiendo cuándo un
problema es supervisado y cuándo no.

## Dato real y Fuente

Cantidad de artículos, tamaño del proveedor (`tamano_proveedor`) y monto total en compras públicas de alimentos de **MercadoPúblico / ChileCompra**. La tarea de clasificación consiste en predecir el tamaño del proveedor (Micro, Pequeña, Mediana, Grande) a partir de la cantidad y monto total. El clustering agrupa las compras sin conocer estas etiquetas de antemano.

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

1. **Preparar la clasificación** — `X` (cantidad y monto_total), `y` (tamano_proveedor) y `train_test_split` con `stratify`.
2. **Entrenar y medir la exactitud** — `DecisionTreeClassifier`, `accuracy_score`.
3. **Agrupar con K-Means** — `StandardScaler` + `KMeans(3)`, etiquetas de cluster.
4. **¿Coinciden grupos y tamaños de proveedor?** — `pd.crosstab` entre tamano_proveedor y cluster, e interpretación.

## Verificación de calidad

- Solución ejecutada: **4/4 ✅** (clasificador exactitud en prueba ≈ 0.81; el clustering separa adecuadamente los perfiles de compra; la tabla cruzada demuestra que no se superponen perfectamente, lo cual es una valiosa lección didáctica).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0 (analogías, errores típicos, profundidad)?
- [ ] ¿Queda clara la diferencia entre supervisado (clasificación) y no supervisado (clustering)?
- [ ] ¿Se entienden exactitud, matriz de confusión y la necesidad de escalar antes de K-Means?
- [ ] ¿La discusión de que el clustering no calza exacto con las etiquetas reales es comprensible?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: la **trampa de la exactitud** con clases desbalanceadas, **precisión/recall/F1 y la
matriz de confusión**, **ROC/AUC y el umbral**, y los **supuestos de k-means** (escalado, forma, elegir
*k*, y que los clusters no son "la verdad"). Con 4 ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B4-clasificacion-y-clustering/profundiza.ipynb)

---

*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
