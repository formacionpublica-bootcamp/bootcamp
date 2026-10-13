# Guía de Aprendizaje — R2-05 · Modelos basados en árboles

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 5 · Semana 11

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-05 · Modelos basados en árboles |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Intermedio — requiere R2-04 |
| **Prerrequisitos** | Corte temporal, baseline, `fit`/`predict`, MAE (R2-04) |
| **Competencia de salida** | Entrenar, comparar e interpretar árboles de decisión y bosques aleatorios; controlar el sobreajuste con la profundidad; leer la importancia de variables; convertir predicciones en alertas |
| **Entregable** | Las 5 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` — PM2.5 diario, temperatura y humedad de Cerro Navia 2020–2025 (SINCA, MMA), el mismo problema de R2-04. Profundización: `sismos.csv` (USGS, M ≥ 4,5, 2020–2025) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Los árboles de decisión son los modelos que mejor se **explican**: un árbol chico es literalmente un flujograma de preguntas sí/no, como los que ya usa el Estado en protocolos y guías de trámite. Los **bosques aleatorios** promedian cientos de árboles y suelen ganar en precisión, y además dicen **qué variable pesa más** — información de diseño de política.

En este módulo los pones a prueba sobre el mismo pronóstico de PM2.5 de R2-04, con la misma vara:

- Un árbol de 3 preguntas (MAE **7,74**) es fácil de explicar, pero **pierde** contra la recta (7,09) y la persistencia (7,36).
- Un árbol sin límite **memoriza**: error 0,0 en entrenamiento y **9,2** en 2025.
- El bosque gana a todos (**6,37 µg/m³**) y revela que el **PM2.5 de ayer** pesa el 80% de la decisión.
- Convertido en **alerta** de días sobre 50 µg/m³, el bosque detecta 36 de 54 días con solo 6 falsas alarmas; la persistencia detecta 39 pero con 15 falsas alarmas. Elegir entre ambos **no es técnico**: es una decisión de salud pública.

> 🏛️ **Mensaje clave:** un modelo más complejo no es automáticamente mejor; se gana su lugar contra el baseline, con datos que no vio.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el trabajo |
|----------|-----------|----------------------|
| **Árbol de decisión** | Predice con una secuencia de preguntas sí/no | Flujograma de un protocolo |
| **Nodo / hoja** | Pregunta / respuesta final (valor estimado) | Criterio / resultado del trámite |
| **`max_depth`** | Máximo de preguntas seguidas | Cuántos pasos tiene el flujograma |
| **`min_samples_leaf`** | Mínimo de casos por hoja | No hacer reglas para un solo caso |
| **Sobreajuste** | Memorizar el entrenamiento y fallar en lo nuevo | Regla a la medida de los casos conocidos |
| **Bosque aleatorio** | Promedia muchos árboles con datos y features al azar | Comisión de varios evaluadores |
| **`feature_importances_`** | Cuánto aportó cada variable (suman 1) | Ranking de factores |
| **Hiperparámetro** | Ajuste que se fija antes de entrenar | Reglas del concurso antes de abrirlo |
| **Alerta** | Predicción convertida en decisión con un umbral | «Avisar si se esperan más de 50» |
| **Falsa alarma / día no detectado** | Los dos errores posibles de una alerta | Avisar de más / avisar de menos |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Hacer un corte temporal de entrenamiento y prueba (R2-04) | ☐ |
| Explicar qué es el baseline «mañana = hoy» y por qué importa | ☐ |
| Usar `fit` y `predict` y calcular `mean_absolute_error` | ☐ |
| Combinar condiciones booleanas con `&` y negarlas con `~` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar Cerro Navia con las **mismas features** de R2-04, ya fabricadas: `temp_media`, `humedad_media`, `mes`, `dia_semana`, `pm25_ayer` (1.990 días completos).

💡 **Concepto clave:** Mismo dato, mismo corte, misma vara: así la comparación entre modelos es justa.

---

### Sección 1 · Preparar el corte y las varas

🎯 **Objetivo:** Repetir el corte temporal (1.637 días de 2020–2024 / 353 de 2025) y recalcular el baseline (7,36) y la regresión lineal (7,09).

💡 **Concepto clave:** Sin estas dos cifras a la vista, cualquier MAE nuevo es imposible de juzgar.

---

### Sección 2 · Tu primer árbol

🎯 **Objetivo:** Árbol con `max_depth=3`, MAE en 2025 y dibujo del árbol.

💡 **Concepto clave:** MAE **7,74**: peor que la recta y que la persistencia. A cambio, se lee solo: casi todas las preguntas son sobre `pm25_ayer`, y una sobre la temperatura (si ayer hubo entre 19,5 y 33,5 µg/m³ y hoy la media es ≤ 8,7 °C, el árbol espera ~42 µg/m³). Interpretabilidad y precisión a veces tiran para lados distintos.

✅ **Señal de que entendiste:** Puedes leer en voz alta una rama del árbol como una regla.

---

### Sección 3 · El sobreajuste, visible

🎯 **Objetivo:** Árbol sin límite: MAE en entrenamiento vs prueba.

💡 **Concepto clave:** El árbol crece hasta profundidad **25** con **1.432 hojas** — casi una por día de entrenamiento —, error **0,0** en entrenamiento y **9,2** en 2025. El gráfico muestra que el error de prueba es mínimo en profundidad 5 (7,38, casi igual al baseline) y luego sube.

⚠️ **Error frecuente:** Elegir la profundidad mirando el conjunto de prueba. En rigor se usa un conjunto de **validación** aparte (R2-07); aquí la curva es solo ilustrativa.

---

### Sección 4 · Bosque e importancias

🎯 **Objetivo:** `RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)`, su MAE y la variable más importante.

💡 **Concepto clave:** MAE **6,37**: el mejor de todos. Importancias: `pm25_ayer` **0,80**, temperatura 0,07, humedad 0,07, día de la semana 0,04, mes 0,03. A diferencia de la recta, el árbol no lee `mes` como un número que «crece»: lo corta en tramos.

⚠️ **Error frecuente:** Leer la importancia como causa. `pm25_ayer` manda porque el aire **persiste**, no porque el de ayer «provoque» el de hoy.

---

### Sección 5 · De la predicción a la alerta

🎯 **Objetivo:** Contar días reales sobre 50 µg/m³ en 2025 (**54**), cuántos detecta el bosque (**36**) y cuántas falsas alarmas da (**6**); comparar con el baseline (39 detectados, 15 falsas alarmas).

💡 **Concepto clave:** Ningún modelo es «el mejor» en abstracto: uno avisa de menos, el otro de más. Cuál conviene depende del costo de cada error, y eso lo decide la política pública, no el algoritmo.

---

### Reflexión final

La pregunta de qué error es más caro (avisar de más o de menos) no tiene celda de chequeo: es la conversación con la autoridad sanitaria. En R2-06 y R2-07 estos dos errores tendrán nombre — *precision* y *recall* — y aprenderás a mover el umbral con criterio.

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 1 — Corte temporal y MAE de referencia

**Pistas progresivas:**
- 🟢 Pista suave: Es el mismo corte del ejercicio 2 de R2-04.
- 🟡 Pista media: Dos filtros sobre `datos["fecha"]`, con `<` y `>=` contra `corte`.
- 🔴 Pista directa: `train = datos[datos["fecha"] < corte]` y `test = datos[datos["fecha"] >= corte]`.

**¿Qué significa el ✅?** Que tienes a la vista las varas: baseline 7,36 y recta 7,09.

---

### Ejercicio 2 — Árbol de profundidad 3

**Pistas progresivas:**
- 🟢 Pista suave: Igual que la regresión: crear, `fit`, `predict`, MAE.
- 🟡 Pista media: `DecisionTreeRegressor(max_depth=3, random_state=42)`.
- 🔴 Pista directa: `arbol = DecisionTreeRegressor(max_depth=3, random_state=42)`, `arbol.fit(X_train, y_train)`, `mae_arbol = mean_absolute_error(y_test, arbol.predict(X_test))`.

**¿Qué significa el ✅?** Que entrenaste un modelo legible (MAE 7,74) y puedes ver sus reglas.

---

### Ejercicio 3 — Árbol sin límite

**Pistas progresivas:**
- 🟢 Pista suave: Es el mismo árbol, sin `max_depth`. Luego mide el error dos veces.
- 🟡 Pista media: Un MAE con `predict(X_train)` contra `y_train`; otro con `predict(X_test)` contra `y_test`.
- 🔴 Pista directa: `arbol_profundo = DecisionTreeRegressor(random_state=42).fit(X_train, y_train)`; `mae_train = mean_absolute_error(y_train, arbol_profundo.predict(X_train))`; ídem para prueba.

**¿Qué significa el ✅?** Que viste la firma del sobreajuste: 0,0 en entrenamiento, 9,2 en prueba.

---

### Ejercicio 4 — Bosque aleatorio e importancias

**Pistas progresivas:**
- 🟢 Pista suave: El bosque se usa igual que el árbol; las importancias ya quedan en una Serie ordenada.
- 🟡 Pista media: `bosque.fit(X_train, y_train)`; el nombre del máximo de una Serie es `.idxmax()`.
- 🔴 Pista directa: `bosque = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)`, `bosque.fit(X_train, y_train)` y `feature_top = importancias.idxmax()`.

**¿Qué significa el ✅?** Que el bosque (6,37) supera a la recta y al baseline, y que `pm25_ayer` manda.

---

### Ejercicio 5 — Detectados y falsas alarmas

**Pistas progresivas:**
- 🟢 Pista suave: Una alerta es una condición sobre la predicción; los aciertos y errores son combinaciones de dos condiciones.
- 🟡 Pista media: `&` es «y»; `~real` es «no real».
- 🔴 Pista directa: `alerta = pred_bosque > 50`, `detectados = int((alerta & real).sum())`, `falsas_alarmas = int((alerta & ~real).sum())`.

**¿Qué significa el ✅?** Que llevaste el modelo al terreno de la decisión: 36 de 54 días detectados, 6 falsas alarmas.

---

> 🔬 **En la profundización:** transferencia a los **sismos M ≥ 4,5 de Chile 2020–2025** (USGS). Predices la **profundidad** con latitud, longitud y magnitud: un árbol de 3 preguntas baja el error de 54,3 km (baseline) a **19,9 km**, el árbol sin límite memoriza (0,0 en entrenamiento, 14,7 en prueba) y el bosque llega a **12,4 km**. La importancia de la **longitud (0,84)** revela la **subducción**: mientras más al este, más profundo el sismo — la placa de Nazca hundiéndose bajo la Sudamericana. La magnitud casi no aporta (0,01).

---

## 7. Autoevaluación Final

**Pregunta 1:** Un árbol de profundidad 3 tiene MAE 7,74 y la regresión lineal 7,09. ¿Por qué podrías igual querer el árbol?

- A) Porque siempre es más preciso
- B) Porque se puede leer como un conjunto de reglas y explicarse a una autoridad ✅
- C) Porque entrena más rápido
- D) No hay razón

**Explicación:** Precisión e interpretabilidad son valores distintos. A veces un modelo algo menos preciso pero explicable es el adecuado para una decisión pública.

---

**Pregunta 2:** Un árbol sin límite tiene MAE 0,0 en entrenamiento y 9,2 en prueba. ¿Qué pasó?

- A) Es el mejor modelo posible
- B) Sobreajuste: memorizó cada día de entrenamiento y no generaliza ✅
- C) El conjunto de prueba tiene errores
- D) Faltan árboles

**Explicación:** Un error de entrenamiento cercano a cero con un error de prueba alto es la firma clásica de memorizar en vez de aprender.

---

**Pregunta 3:** ¿Por qué un bosque aleatorio suele generalizar mejor que un solo árbol?

- A) Porque usa árboles más profundos
- B) Porque promedia muchos árboles distintos y los errores individuales se compensan ✅
- C) Porque no necesita datos de entrenamiento
- D) Porque elimina variables

**Explicación:** Cada árbol ve una muestra distinta de datos y features; el promedio es más estable que cualquiera de ellos.

---

**Pregunta 4:** La importancia de `pm25_ayer` es 0,80. ¿Qué **no** puedes concluir?

- A) Que es la variable que más usa el bosque
- B) Que el PM2.5 de ayer causa el de hoy ✅
- C) Que el aire tiende a persistir de un día a otro
- D) Que las demás variables aportan poco

**Explicación:** La importancia mide uso en el modelo, no causalidad (recuerda R2-03).

---

**Pregunta 5:** El bosque detecta 36 de 54 días sobre la norma con 6 falsas alarmas; el baseline detecta 39 con 15 falsas alarmas. ¿Cuál elegir?

- A) Siempre el bosque, porque tiene menor MAE
- B) Siempre el baseline, porque detecta más
- C) Depende del costo de cada error para la salud pública; es una decisión que se explicita ✅
- D) Ninguno sirve

**Explicación:** Avisar de menos y avisar de más tienen costos distintos. El modelo informa; la decisión del umbral es de política pública.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Árbol de decisión** | Modelo de preguntas sí/no | Flujograma de un protocolo |
| **Hoja** | Final de una rama, con el valor estimado | Resultado del trámite |
| **`max_depth`** | Límite de preguntas seguidas | Pasos máximos del protocolo |
| **`min_samples_leaf`** | Casos mínimos por hoja | No crear reglas para un solo caso |
| **Sobreajuste** | Memorizar en vez de aprender | Regla a la medida del pasado |
| **Bosque aleatorio** | Promedio de muchos árboles | Comisión de evaluadores |
| **Importancia de variables** | Peso de cada feature en el modelo | Ranking de factores |
| **Hiperparámetro** | Ajuste fijado antes de entrenar | Bases del concurso |
| **Alerta** | Predicción + umbral = decisión | Aviso de episodio |
| **Falsa alarma** | Alertar un día que no superó la norma | Avisar de más |
| **Subducción** | Una placa tectónica se hunde bajo otra | Por qué Chile tiene sismos profundos al este |

---

## 9. Conexión con el Módulo Siguiente

En R2-05 comparaste árboles y bosques contra el baseline y la recta, viste el sobreajuste con tus ojos, leíste qué variable manda y llevaste el modelo hasta una alerta.

En **R2-06 · Clasificación y clustering** darás el paso que el ejercicio 5 dejó abierto: en vez de predecir un número y luego aplicarle un umbral, entrenarás modelos que predicen directamente una **categoría**, y aprenderás a **agrupar** casos parecidos sin etiquetas. Las falsas alarmas y los días no detectados de hoy se convertirán en métricas con nombre propio.

> 💡 **Pregunta para reflexionar:** si tuvieras que explicarle el bosque a la Seremi de Salud en dos frases, ¿qué le dirías: el MAE, la importancia de variables o las alertas?
