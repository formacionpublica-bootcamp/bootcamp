# D10 · Modelos basados en árboles

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Línea B · *Data Scientist* · Semana 11 · Módulo específico de la ruta de Ciencia de Datos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B3-modelos-de-arboles/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

Tras el primer modelo de D9 (regresión lineal), este módulo presenta una familia más potente y
muy usada en la práctica: **árboles de decisión** y **bosques aleatorios**. Se usan con el
**mismo** `fit` / `predict` y la misma disciplina de entrenamiento y prueba, así que el estudiante
ya parte con medio camino andado. El corazón del módulo es ver el **sobreajuste** de forma
tangible (a más profundidad del árbol, más memoriza) y leer la **importancia de variables**.

**Competencia de salida:** entrenar y evaluar un árbol de decisión y un bosque aleatorio para
regresión, diagnosticar el sobreajuste a partir de la profundidad del árbol, y leer la importancia
de las variables.

## Dato real y Fuente

Cantidad de artículos, tamaño del proveedor (`tamano_num`) y monto total en compras públicas de alimentos de **MercadoPúblico / ChileCompra**. Mantenemos este dominio para que puedas comparar de forma justa el desempeño de los modelos basados en árboles y bosques aleatorios con la regresión lineal de D9. La inclusión de la variable `tamano_num` permite que el análisis de importancia de variables tenga sentido.

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
| `compras_ml.csv` | Dataset de compras de alimentos, cantidades y montos. |
| `README.md` | Esta portada. |

## Los 4 ejercicios

1. **Preparar los datos (dos features)** — `X` con cantidad y tamano_num, `y`, y `train_test_split`.
2. **Entrenar y evaluar el árbol** — `DecisionTreeRegressor(max_depth=3)`, `fit`/`predict`, MAE.
3. **Ver el sobreajuste** — árbol sin límite de profundidad: MAE en entrenamiento vs prueba.
4. **Bosque aleatorio e importancias** — `RandomForestRegressor`, MAE en prueba y variable más importante (`feature_importances_`).

## Verificación de calidad

- Solución ejecutada: **4/4 ✅** (árbol max_depth=3 MAE prueba ≈ 85,600.40 CLP; árbol profundo: entrenamiento ≈ 64,198.70 CLP / prueba ≈ 76,018.66 CLP; bosque ≈ 76,057.32 CLP; variable top = cantidad).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0 (analogías, errores típicos, profundidad)?
- [ ] ¿La intuición del árbol (preguntas sí/no) y la visualización ayudan?
- [ ] ¿La curva de sobreajuste (entrenamiento vs prueba) se entiende?
- [ ] ¿Queda clara la idea de bosque (promedio de árboles) e importancia de variables?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: **cómo decide un árbol** (impureza Gini/entropía), **por qué un árbol solo sobreajusta**,
**bagging vs boosting** y los **cuidados al leer la importancia de variables**. Con 4 ejercicios
conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B3-modelos-de-arboles/profundiza.ipynb)

---

*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
