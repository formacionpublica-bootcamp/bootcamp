# Guía de Aprendizaje — R2-04 · Fundamentos de Machine Learning

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 4 · Semana 10

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-04 · Fundamentos de Machine Learning |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Intermedio — requiere R2-03 |
| **Prerrequisitos** | Filtrar por fechas, `groupby`, `dropna`; idea de correlación y estacionalidad (R2-03) |
| **Competencia de salida** | Plantear un problema supervisado, fabricar una *feature* de rezago, separar entrenamiento y prueba con corte temporal, comparar contra un baseline, entrenar una regresión lineal y evaluarla con MAE en datos no vistos |
| **Entregable** | Las 5 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` — PM2.5 diario, temperatura y humedad de Cerro Navia 2020–2025 (SINCA, MMA). Profundización: `matricula.csv` (MINEDUC 2025) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Muchas decisiones del Estado son **anticipaciones**: cuántas consultas llegarán a urgencia, cuántos estudiantes tendrá un colegio, si mañana el aire será malo. Un modelo de *machine learning* aprende ese patrón de los datos pasados y lo aplica a casos nuevos.

En este módulo pronosticas el **PM2.5 diario de Cerro Navia** — si pudieras anticiparlo, podrías avisar antes a la población y a la red de salud. Pero la lección central no es el algoritmo (la regresión lineal es simple), sino los **hábitos que hacen creíble un modelo**:

- Evaluar con datos que el modelo **no vio**, y **del futuro** (corte temporal: entrenar 2020–2024, probar 2025).
- Compararlo con una **regla ingenua**: «mañana = hoy» ya logra un error de **7,36 µg/m³**. El modelo lineal llega a **7,09**: gana, pero por poco — y reportarlo así es honestidad técnica.

> 🏛️ **Mensaje clave:** un modelo sin baseline y sin prueba honesta es un acto de fe. Con ellos, es evidencia.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el trabajo |
|----------|-----------|----------------------|
| **Aprendizaje supervisado** | Aprender de ejemplos con respuesta conocida | Ajustar una tendencia con datos históricos |
| **Features (`X`) / objetivo (`y`)** | Entradas del modelo / lo que se predice | Columnas explicativas / columna a estimar |
| **Regresión / clasificación** | Predecir un número / una categoría | µg/m³ mañana / ¿supera la norma? |
| **Rezago (`shift(1)`)** | Trae el valor del día anterior a la fila de hoy | Referenciar la celda de arriba |
| **Corte temporal** | Entrenar con el pasado, probar con el futuro | Validar con el año siguiente |
| **Baseline** | Predicción ingenua que el modelo debe superar | «Igual que ayer», «el promedio de siempre» |
| **`fit` / `predict`** | Aprender / responder | — |
| **MAE** | Error absoluto medio, en las unidades de `y` | «En promedio me equivoco por X µg/m³» |
| **Sobreajuste** | Bien en entrenamiento, mal en datos nuevos | Memorizar el solucionario |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar filas por una fecha (`datos[datos["fecha"] < corte]`) | ☐ |
| Crear una columna nueva a partir de otra | ☐ |
| Explicar qué es la estacionalidad del PM2.5 (R2-03) | ☐ |
| Distinguir una lista de columnas (`df[["a", "b"]]`) de una sola columna (`df["a"]`) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `aire_diario.csv` y quedarse con Cerro Navia (2.191 días, ordenados por fecha).

💡 **Concepto clave:** El orden importa: el rezago solo significa «ayer» si las filas están en orden cronológico y no faltan días (en este archivo no faltan).

---

### Sección 1 · Fabricar las features

🎯 **Objetivo:** Crear `pm25_ayer` (con `shift(1)`), `mes` y `dia_semana`, y quedarse con los **1.990 días** que tienen todas las features.

💡 **Concepto clave:** El rezago es la *feature* reina de los pronósticos: el aire de hoy se parece mucho al de ayer.

⚠️ **Error frecuente:** `shift(-1)` trae el valor de **mañana**: sería una fuga (usar el futuro para predecir el futuro).

---

### Sección 2 · Corte temporal

🎯 **Objetivo:** Entrenar con **1.637 días** (2020–2024) y probar con **353 días** de 2025.

💡 **Concepto clave:** La prueba debe imitar el uso real. Si barajas los días, el modelo entrena con vecinos de los días que luego «predice»: la evaluación deja de imitar el uso real y puede quedar maquillada. En R2-07 verás la validación temporal en profundidad.

✅ **Señal de que entendiste:** Puedes explicar por qué `train_test_split` al azar no es adecuado aquí.

---

### Sección 3 · Baseline

🎯 **Objetivo:** Medir el MAE de «mañana = hoy» (**7,36 µg/m³**) y de «siempre el promedio» (**18,37**).

💡 **Concepto clave:** La persistencia es una vara alta. Cualquier modelo que se presente a una autoridad debe compararse con ella.

---

### Sección 4 · fit / predict

🎯 **Objetivo:** Entrenar `LinearRegression`, predecir 2025 y comparar.

💡 **Concepto clave:** MAE en prueba **7,09** vs baseline 7,36: el modelo gana por poco. El MAE en entrenamiento (8,04) no es menor que el de prueba, así que **no hay sobreajuste** (2025 resultó incluso algo más predecible). Los coeficientes se leen como «µg/m³ por unidad»: cada °C más de temperatura media resta ~1,5 µg/m³; cada µg/m³ de ayer suma ~0,7 hoy.

⚠️ **Error frecuente:** Entrenar con `X_test` o reportar el MAE de entrenamiento como si fuera el desempeño real.

---

### Sección 5 · Un día nuevo

🎯 **Objetivo:** Pronosticar un miércoles de julio con 7 °C, 85% de humedad y 60 µg/m³ el día anterior.

💡 **Concepto clave:** El modelo estima **54,2 µg/m³** → sobre la norma. La entrada debe tener las mismas columnas, en el mismo orden, que el entrenamiento.

---

### Reflexión final

Dos límites honestos del modelo: usa la temperatura y humedad **del mismo día** (en producción vendrían de un pronóstico meteorológico, que también se equivoca) y lee `mes` como número (para la recta, diciembre es «más» que julio). R2-05 aborda el segundo.

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 1 — Crea `pm25_ayer`, `mes` y `dia_semana`

**Pistas progresivas:**
- 🟢 Pista suave: El rezago «corre» la columna una fila hacia abajo.
- 🟡 Pista media: `.shift(1)` sobre la columna `pm25`; el día de la semana sale de `.dt`.
- 🔴 Pista directa: `cn["pm25_ayer"] = cn["pm25"].shift(1)` y `cn["dia_semana"] = cn["fecha"].dt.dayofweek`.

**¿Qué significa el ✅?** Que cada fila tiene el PM2.5 del día anterior y no quedan nulos en las features.

---

### Ejercicio 2 — Corte temporal

**Pistas progresivas:**
- 🟢 Pista suave: Dos filtros por fecha, uno con `<` y otro con `>=`.
- 🟡 Pista media: Compara `datos["fecha"]` con `corte`.
- 🔴 Pista directa: `train = datos[datos["fecha"] < corte]` y `test = datos[datos["fecha"] >= corte]`.

**¿Qué significa el ✅?** Que todo el entrenamiento es anterior a la prueba y la prueba es 2025 completo.

---

### Ejercicio 3 — MAE del baseline

**Pistas progresivas:**
- 🟢 Pista suave: La predicción ingenua ya está en una columna de `X_test`.
- 🟡 Pista media: Usa `mean_absolute_error(real, predicho)`.
- 🔴 Pista directa: `pred_base = X_test["pm25_ayer"]` y `mae_base = mean_absolute_error(y_test, pred_base)`.

**¿Qué significa el ✅?** Que tienes la vara (7,36 µg/m³) antes de entrenar nada.

---

### Ejercicio 4 — Entrena, predice y compara

**Pistas progresivas:**
- 🟢 Pista suave: Tres pasos: crear, `fit`, `predict`.
- 🟡 Pista media: `fit` recibe `X_train, y_train`; `predict` recibe `X_test`.
- 🔴 Pista directa: `modelo = LinearRegression()`, `modelo.fit(X_train, y_train)`, `y_pred = modelo.predict(X_test)`.

**¿Qué significa el ✅?** Que tu modelo (7,09) le ganó al baseline (7,36) en datos que nunca vio.

---

### Ejercicio 5 — Pronostica un día nuevo

**Pistas progresivas:**
- 🟢 Pista suave: `predict` devuelve un arreglo; toma el primer elemento.
- 🟡 Pista media: `modelo.predict(dia_nuevo)[0]`, convertido a `float`.
- 🔴 Pista directa: `pm25_estimado = float(modelo.predict(dia_nuevo)[0])` y `supera_norma = pm25_estimado > 50`.

**¿Qué significa el ✅?** Que usaste el modelo para lo que sirve: estimar lo que aún no ocurre (54,2 µg/m³).

---

> 🔬 **En la profundización:** el mismo método sobre la **matrícula 2025**. Predices los **cursos** de un colegio desde su matrícula (MAE 2,59 cursos vs 8,0 del baseline; ≈ 2,6 cursos por cada 100 estudiantes), aprendes cuándo **sí** vale el corte aleatorio (una foto sin tiempo), y caes a propósito en una **fuga de datos**: predecir `mat_total` con `mat_hombres` + `mat_mujeres` da R² ≈ 1 porque es una suma. El modelo honesto (con `cursos` y `rural`) logra R² 0,897 y MAE de 90 estudiantes — peor, pero real.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué no se barajan los días al separar entrenamiento y prueba en este módulo?

- A) Porque `train_test_split` no funciona con fechas
- B) Porque queremos pronosticar el futuro: la prueba debe ser posterior al entrenamiento ✅
- C) Porque hay pocos datos
- D) Para que el modelo entrene más rápido

**Explicación:** Barajar mezcla días de 2025 en el entrenamiento y deja que el modelo aprenda de «vecinos del futuro». El corte temporal imita el uso real.

---

**Pregunta 2:** El baseline «mañana = hoy» tiene MAE 7,36 y el modelo lineal 7,09. ¿Qué reportas?

- A) Que el modelo es excelente
- B) Que el modelo mejora levemente a la persistencia; el aire de ayer ya explica casi todo ✅
- C) Que el modelo no sirve
- D) Solo el 7,09, sin comparar

**Explicación:** Sin baseline, 7,09 no dice nada. Con él, sabes cuánto aporta el modelo (poco) y dónde buscar mejoras.

---

**Pregunta 3:** ¿Qué indica que el MAE de entrenamiento sea mucho menor que el de prueba?

- A) Que el modelo generaliza muy bien
- B) Sobreajuste: el modelo memorizó el entrenamiento ✅
- C) Que faltan features
- D) Que la prueba está mal hecha

**Explicación:** Memorizar da error bajo en lo conocido y alto en lo nuevo. Aquí no pasa (8,04 vs 7,09).

---

**Pregunta 4:** ¿Por qué `shift(-1)` sería un error grave en la *feature* de rezago?

- A) Porque da error de sintaxis
- B) Porque trae el valor de mañana: el modelo vería la respuesta (fuga de datos) ✅
- C) Porque borra la primera fila
- D) No es error, da lo mismo

**Explicación:** Una feature solo vale si estaría disponible al momento de predecir.

---

**Pregunta 5:** Un modelo predice la matrícula total con R² = 0,99999 usando hombres y mujeres matriculados. ¿Qué pasa?

- A) Es un modelo excepcional
- B) Hay fuga: el total es la suma de esas columnas ✅
- C) Falta normalizar
- D) Hay sobreajuste por profundidad

**Explicación:** «Demasiado bueno para ser cierto» suele ser fuga. Pregunta siempre si tendrías esa feature antes de conocer la respuesta.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Machine learning** | Aprender reglas a partir de ejemplos | Estimar a partir de la experiencia registrada |
| **Feature / objetivo** | Entrada / lo que se predice | Variables explicativas / indicador a anticipar |
| **Rezago (lag)** | Valor de un período anterior | «El dato de ayer» |
| **Conjunto de prueba** | Datos reservados para evaluar | El examen sin solucionario |
| **Corte temporal** | Probar con datos posteriores al entrenamiento | Validar con el año siguiente |
| **Baseline** | Predicción ingenua de referencia | «Lo que diría cualquiera sin modelo» |
| **`fit` / `predict`** | Entrenar / predecir | — |
| **MAE** | Error absoluto medio | «Me equivoco en promedio por X» |
| **Sobreajuste** | Memorizar en vez de aprender | Regla hecha a la medida de los casos ya vistos |
| **Fuga de datos** | Usar información que no tendrías al predecir | Mirar la respuesta antes de responder |

---

## 9. Conexión con el Módulo Siguiente

En R2-04 entrenaste tu primer modelo con los hábitos correctos: features con sentido, corte temporal, baseline y MAE en datos no vistos.

En **R2-05 · Modelos basados en árboles** cambiarás la recta por **árboles de decisión** y **bosques aleatorios** — con el **mismo dato, el mismo corte y la misma vara** (7,36 del baseline, 7,09 de la recta), para comparar de forma justa. Verás el sobreajuste con tus propios ojos al dejar crecer un árbol sin límite, y aprenderás a leer qué *feature* pesa más.

> 💡 **Pregunta para reflexionar:** si el PM2.5 de ayer explica casi todo, ¿qué tendría que aportar un modelo más complejo para que valga la pena explicarlo a una autoridad?
