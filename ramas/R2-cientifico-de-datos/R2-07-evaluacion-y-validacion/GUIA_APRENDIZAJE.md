# Guía de Aprendizaje — R2-07 · Evaluación y validación de modelos

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 7 · Semana 12–13

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-07 · Evaluación y validación de modelos |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 3 horas |
| **Nivel** | Intermedio-avanzado — requiere R2-05 y R2-06 |
| **Prerrequisitos** | Matriz de confusión, precisión y recall (R2-06); bosques aleatorios (R2-05) |
| **Competencia de salida** | Evaluar un clasificador con rigor: métricas honestas, sin fuga de datos, con validación temporal cuando hay tiempo de por medio, y auditado por grupo |
| **Entregable** | Las 5 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 diario 2020–2025, 14 estaciones SINCA). Profundización: `matricula.csv` (10.945 establecimientos con matrícula 2025, MINEDUC) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Tarde o temprano alguien te va a ofrecer un modelo con un número impresionante: «F1 de 0,9», «95 % de exactitud», «validado con validación cruzada». Este módulo te enseña a **auditar ese número** antes de que el Estado adopte, implemente o publique algo basado en él.

Usamos el mismo problema de R2-06 —anticipar si un día supera la norma de PM2.5 de 24 h (50 µg/m³)— y lo atacamos por cuatro flancos donde los modelos suelen mentir sin que nadie lo note:

- **La métrica equivocada:** 0,968 de exactitud con un F1 de apenas 0,566.
- **La fuga de datos:** una columna de aspecto inocente («promedio móvil de 3 días») sube el F1 de 0,566 a **0,828**… porque incluye el dato de hoy y el de mañana.
- **Barajar el tiempo:** el mismo bosque aleatorio obtiene F1 **0,607** con validación cruzada barajada y **0,385** cuando se le exige predecir el futuro con `TimeSeriesSplit`.
- **El promedio que esconde:** el recall va de **0,09** en Centro Quintero a **0,58** en Cerro Navia. Una ciudad puede quedar mucho menos protegida que otra.

Saber hacer estas cuatro preguntas es lo que separa a quien usa modelos de quien los **gobierna**.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el Estado |
|----------|-----------|----------------------|
| **F1** | Promedio armónico de precisión y recall | Una nota que solo es alta si ambas lo son |
| **Fuga de datos** | Usar información que no existiría al decidir | Corregir una prueba con la pauta a la vista |
| **Promedio centrado** | Promedia ayer, hoy y mañana | Un indicador mensual que se calcula con el mes ya cerrado |
| **Validación cruzada (`KFold`)** | Evalúa en *k* cortes y promedia | Auditar varias muestras, no una |
| **`shuffle=True`** | Baraja las filas antes de cortar | Mezclar expedientes de distintos años |
| **`TimeSeriesSplit`** | Entrena con el pasado, evalúa con lo siguiente | Evaluar el pronóstico 2025 solo con lo sabido hasta 2024 |
| **Desempeño por grupo** | La métrica calculada por estación/región | Desagregar un indicador nacional por territorio |
| **Disparidad** | Máximo − mínimo de la métrica entre grupos | La brecha entre la mejor y la peor región |
| **AUC / ROC** (profundización) | Qué tan bien separa en todos los umbrales | Calidad de un ranking de prioridades |
| **Calibración / Brier** (profundización) | Si las probabilidades son creíbles | Que «70 % de riesgo» signifique 7 de cada 10 |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué son precisión y recall y qué error mide cada una | ☐ |
| Entrenar un `RandomForestClassifier` con `.fit()` | ☐ |
| Explicar qué hace `groupby(...).shift(1)` | ☐ |
| Recorrer los valores únicos de una columna con un `for` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Construir variables que se conocen la víspera y dejar los datos en orden cronológico.

💡 **Concepto clave:** `pm25_ayer` y `pm25_prom7` (promedio de los 7 días **previos**) usan solo el pasado. `dia` cuenta los días desde el 1-ene-2020. `pm25_centrado` es la trampa deliberada del ejercicio 2. Quedan 29.171 días-estación, con 4,4 % sobre la norma. Al final, `d` se ordena por **fecha**: imprescindible para el ejercicio 4.

---

### Sección 1 · Métricas más allá de la accuracy

🎯 **Objetivo:** Reportar las cuatro métricas del modelo limpio.

💡 **Concepto clave:** accuracy **0,968**, precisión **0,684**, recall **0,483**, F1 **0,566**. La accuracy está 0,4 por encima del F1: es el número que más luce y el que menos informa.

---

### Sección 2 · Fuga de datos

🎯 **Objetivo:** Ver cuánto «mejora» un modelo que hace trampa.

💡 **Concepto clave:** `rolling(3, center=True)` promedia ayer, **hoy** y **mañana**. El PM2.5 de hoy es justamente la respuesta. Con esa columna el F1 sube a **0,828**. La víspera, cuando se decide, esa columna no existe: el desempeño real es el de 0,566.

⚠️ **Error frecuente:** Pensar que una fuga siempre se ve «perfecta» (F1 = 1). Las fugas reales suelen ser **parciales** y por eso pasan inadvertidas: aquí el modelo sigue equivocándose, solo que bastante menos de lo que debería.

✅ **Señal de que entendiste:** Ante cada variable preguntas: «¿a qué hora del día anterior conozco este valor?».

---

### Sección 3 · Validación cruzada (barajada)

🎯 **Objetivo:** Evaluar un bosque aleatorio con `dia` usando `KFold(5, shuffle=True)`.

💡 **Concepto clave:** Cinco folds con F1 entre 0,588 y 0,619, media **0,607**. Parece estable y mejor que la logística. Guarda ese número.

---

### Sección 4 · Validación temporal

🎯 **Objetivo:** Repetir con `TimeSeriesSplit(5)` y comparar.

💡 **Concepto clave:** El F1 cae a **0,385**. Al barajar, el bosque entrenaba con el 14 y el 16 de julio y se evaluaba en el 15: con `dia` «recordaba» el episodio de esa semana. `TimeSeriesSplit` corta en orden: cada fold de prueba es casi un año completo **posterior** a todo su entrenamiento (2021, 2022, 2023, 2024 y 2025). La ilustración muestra el contraste: con variables honestas y una logística sin `dia`, ambas validaciones dan **0,590** — barajar infla cuando el modelo puede memorizar el tiempo.

✅ **Señal de que entendiste:** Puedes explicar por qué la diferencia aparece con el bosque + `dia` y no con la logística sin `dia`.

---

### Sección 5 · Desempeño por grupo

🎯 **Objetivo:** Calcular el recall por estación (solo las que tienen al menos 10 días malos en la prueba) y la disparidad.

💡 **Concepto clave:** Seis estaciones califican. Recall: Centro Quintero **0,09**, Nielol 0,38, El Bosque 0,44, Rancagua I 0,50, Las Encinas 0,51, Cerro Navia **0,58**. Disparidad **0,49**. Ojo: Quintero tiene solo 11 días malos en la prueba, así que su cifra es frágil — pero la señal es que sus episodios no se anticipan bien con el PM2.5 de ayer. Por qué, hay que investigarlo (no lo dice el modelo).

---

### Reflexión final

La reflexión pide tres preguntas para un proveedor que ofrece «F1 = 0,9 validado». No tiene chequeo porque la respuesta es un criterio profesional: ¿qué variables usa y cuándo se conocen? ¿barajó las fechas? ¿cómo le va en cada ciudad?

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 1 — Entrena un modelo limpio y calcula las 4 métricas

**Pistas progresivas:**
- 🟢 Pista suave: Cada métrica tiene su función en `sklearn.metrics`, todas con `(real, predicho)`.
- 🟡 Pista media: `accuracy_score`, `precision_score`, `recall_score`, `f1_score`.
- 🔴 Pista directa: `"precision": precision_score(yte, pred, zero_division=0)` y análogo para las otras.

**¿Qué significa el ✅?** Que tienes el panorama completo y viste que la accuracy supera al F1 por mucho.

---

### Ejercicio 2 — Compara el F1 CON fuga vs SIN fuga

**Pistas progresivas:**
- 🟢 Pista suave: El modelo con fuga ya está entrenado (`m_fuga`); solo falta evaluarlo.
- 🟡 Pista media: Predice sobre `Xte_f` (la prueba que incluye la columna con fuga).
- 🔴 Pista directa: `f1_con_fuga = f1_score(yte, m_fuga.predict(Xte_f))` y `f1_sin_fuga = f1_score(yte, pred)`.

**¿Qué significa el ✅?** Que mediste cuánto infla una sola variable que mira el futuro (+0,26 de F1).

---

### Ejercicio 3 — 5-fold con KFold barajado

**Pistas progresivas:**
- 🟢 Pista suave: `cross_val_score` hace los 5 entrenamientos por ti.
- 🟡 Pista media: Recibe el modelo, `X`, `y`, `cv=` y `scoring=`.
- 🔴 Pista directa: `scores_barajada = cross_val_score(bosque, d[F_dia], y, cv=cv_barajada, scoring="f1")` y `f1_barajada = scores_barajada.mean()`.

**¿Qué significa el ✅?** Que tienes una estimación promediada… que en el siguiente ejercicio vas a cuestionar.

---

### Ejercicio 4 — Compara la validación barajada con la temporal

**Pistas progresivas:**
- 🟢 Pista suave: Es el mismo `cross_val_score`; solo cambia el `cv`.
- 🟡 Pista media: `cv=cv_temporal`.
- 🔴 Pista directa: `scores_temporal = cross_val_score(bosque, d[F_dia], y, cv=cv_temporal, scoring="f1")` y `f1_temporal = scores_temporal.mean()`.

**¿Qué significa el ✅?** Que comprobaste que barajar una serie de tiempo infló el F1 de 0,385 a 0,607.

---

### Ejercicio 5 — Recall por estación y su disparidad

**Pistas progresivas:**
- 🟢 Pista suave: Dentro del `for`, `m` ya selecciona las filas de la estación.
- 🟡 Pista media: `recall_score(yte[m], pred[m], zero_division=0)`; la disparidad usa `max` y `min` sobre `.values()`.
- 🔴 Pista directa: `recall_por_estacion[e] = recall_score(yte[m], pred[m], zero_division=0)` y `disparidad = max(recall_por_estacion.values()) - min(recall_por_estacion.values())`.

**¿Qué significa el ✅?** Que desagregaste el desempeño y encontraste una brecha de 0,49 entre estaciones.

---

> 🔬 **En la profundización:** transferencia a la **matrícula 2025** (MINEDUC): un clasificador que reconoce establecimientos **rurales** (28,2 % del total) por su tamaño, niveles y dependencia. AUC **0,948**; bajar el umbral de 0,5 a **0,33** sube el recall de 0,822 a **0,902**; calibrar con `CalibratedClassifierCV` (isotónica) baja el Brier de 0,0766 a 0,0754; y el recall rural por región revela que el modelo casi no ve a los rurales de la **Región Metropolitana** (0,17, frente a 0,95 en Ñuble).

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué el F1 es más informativo que la accuracy en este problema?

- A) Porque es más fácil de calcular
- B) Porque solo es alto si precisión y recall lo son, y no lo infla la clase mayoritaria ✅
- C) Porque siempre es mayor que la accuracy
- D) Porque no depende de la matriz de confusión

**Explicación:** La accuracy premia acertar los miles de días normales; el F1 mira solo la clase que importa.

---

**Pregunta 2:** ¿Cuál de estas variables tiene fuga para anticipar el PM2.5 de mañana?

- A) El PM2.5 de hoy
- B) El promedio de los últimos 7 días
- C) El promedio del mes calendario completo al que pertenece mañana ✅
- D) El mes del año

**Explicación:** El promedio del mes incluye días posteriores (y el propio día a predecir). No existe al momento de decidir.

---

**Pregunta 3:** Un modelo saca F1 0,61 con `KFold(shuffle=True)` y 0,39 con `TimeSeriesSplit`. ¿Cuál reportas?

- A) 0,61, porque es mayor
- B) El promedio de ambos
- C) 0,39, porque es el escenario real: entrenar con el pasado y predecir el futuro ✅
- D) Ninguno, la validación cruzada no sirve

**Explicación:** Con datos en el tiempo, barajar permite al modelo «ver» días vecinos del futuro. La validación temporal imita el uso real.

---

**Pregunta 4:** El recall de un modelo es 0,58 en Cerro Navia y 0,09 en Quintero. ¿Qué haces?

- A) Nada, el promedio nacional está bien
- B) Reportar la brecha, revisar si hay pocos casos en el grupo y buscar por qué el modelo falla ahí antes de usarlo en esa zona ✅
- C) Eliminar Quintero del dataset
- D) Subir el umbral para todos

**Explicación:** Un promedio bueno puede dejar a una población menos protegida. Desagregar, declarar la brecha y su incertidumbre (¡11 casos!) es parte de evaluar.

---

**Pregunta 5:** Un proveedor reporta F1 = 1,0 en su modelo de alertas. Tu primera sospecha:

- A) Que es un excelente modelo
- B) Que hay fuga de datos o que la evaluación se hizo sobre los mismos datos de entrenamiento ✅
- C) Que usó muchos datos
- D) Que usó redes neuronales

**Explicación:** En problemas reales y ruidosos, la perfección es una alarma, no un logro.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **F1** | Promedio armónico de precisión y recall | Nota exigente que no se infla con lo fácil |
| **Fuga de datos** | Información del futuro o de la respuesta en las variables | Conocer el resultado antes de evaluar |
| **Validación cruzada** | Entrenar y evaluar en varios cortes | Auditar varias muestras |
| **`TimeSeriesSplit`** | Cortes que respetan el orden del tiempo | Evaluar 2025 con lo sabido hasta 2024 |
| **Desempeño por grupo** | Métrica desagregada | Indicador por región o comuna |
| **Disparidad** | Brecha entre el mejor y el peor grupo | Brecha territorial |
| **Umbral** | Probabilidad desde la que se decide «sí» | El puntaje de corte de un programa |
| **AUC** | Capacidad de ordenar casos de mayor a menor riesgo | Calidad de una lista de priorización |
| **Brier** | Error de las probabilidades | Qué tan creíble es un «70 % de riesgo» |

---

## 9. Conexión con el Módulo Siguiente

En R2-07 aprendiste a desconfiar con método: métricas correctas, variables que no miran el futuro, validación temporal y desempeño por grupo.

En **R2-08 · Pipelines reproducibles** vas a blindar todo eso: un `Pipeline` con `ColumnTransformer` que imputa la meteorología faltante, escala y codifica la estación **dentro** de cada fold (la fuga queda cerrada por diseño), una función de entrenamiento con semilla que cualquiera puede repetir, y el modelo guardado en un archivo para reutilizarlo.

> 💡 **Pregunta para reflexionar:** En este módulo calculaste a mano `pm25_ayer` y `pm25_prom7` antes de dividir. ¿Hay algún paso de preparación (por ejemplo, rellenar faltantes con la mediana) que, hecho antes de dividir, introduciría una fuga?
