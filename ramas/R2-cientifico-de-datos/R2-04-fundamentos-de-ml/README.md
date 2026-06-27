# D9 · Fundamentos de Machine Learning

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Línea B · *Data Scientist* · Semana 10 · Módulo específico de la ruta de Ciencia de Datos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B2-fundamentos-de-ml/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

El primer modelo de *machine learning* del bootcamp. Tras aprender a fabricar *features* (D8),
el estudiante entrena un modelo que **aprende un patrón de ejemplos y predice casos nuevos**. El
foco no es el algoritmo (es simple), sino los **hábitos correctos**: separar un conjunto de
prueba, entrenar, evaluar con honestidad y entender el **sobreajuste**.

**Competencia de salida:** plantear un problema de aprendizaje supervisado (*features* y
objetivo), dividir en entrenamiento y prueba, entrenar un modelo de regresión con scikit-learn,
evaluarlo de forma honesta en datos que no vio, y usarlo para predecir un caso nuevo.

## Dato real y Fuente

Cantidad de artículos y monto total en compras públicas reales de alimentos de **MercadoPúblico / ChileCompra**. La relación cantidad → monto_total es clara e intuitiva: ideal para que un primer modelo "se vea funcionar". El modelo aprende que cada unidad adicional aumenta el costo en aproximadamente **2,538 CLP**, con un error medio en prueba de **~104,359 CLP**.

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
| `compras_ml.csv` | Dataset de compras de alimentos y montos. |
| `README.md` | Esta portada. |

## Los 4 ejercicios

1. **Separar `X`, `y` y reservar la prueba** — *features* vs objetivo y `train_test_split`.
2. **Crear, entrenar y predecir** — `LinearRegression`, `fit` y `predict`.
3. **Calcular el error en prueba** — MAE con `mean_absolute_error`; entrenamiento vs prueba.
4. **Predecir una cantidad nueva** — usar el modelo para estimar el costo de 100 artículos.

## Verificación de calidad

- Solución ejecutada: **4/4 ✅** (coef ≈ 2538.27 CLP/unidad; MAE prueba ≈ 104,359.65 CLP).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0 (profundidad, analogías, errores típicos)?
- [ ] ¿Quedan claros aprendizaje supervisado, train/test y sobreajuste para alguien sin ML previo?
- [ ] ¿La evaluación honesta (MAE en prueba) y la idea de generalización se entienden?
- [ ] ¿El uso del dato real (ChileCompra) y el cambio de dominio se justifican bien?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: la descomposición **sesgo-varianza**, **sobreajuste vs subajuste**, **por qué train/test
y la validación cruzada**, el supuesto **i.i.d.**, el valor de un **baseline** y la **curva de
aprendizaje**. Con 4 ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B2-fundamentos-de-ml/profundiza.ipynb)

---

*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
