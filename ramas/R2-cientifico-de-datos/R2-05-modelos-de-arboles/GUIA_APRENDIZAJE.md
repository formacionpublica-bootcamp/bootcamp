# 📘 Guía de Aprendizaje — R2-05 · Modelos basados en árboles

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-05 · Modelos basados en árboles (D10) |
| **Pista / Rama** | R2 — Científico/a de Datos · Línea B |
| **Duración estimada** | 3–4 horas (Semana 11) |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-04 completado (patrón `fit`/`predict`, train/test split, MAE). |
| **Competencia de salida** | Entrenar y evaluar árboles de decisión y Random Forests, controlar el sobreajuste con `max_depth`, e interpretar la importancia de features. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de alimentos: cantidad, `tamano_num` (1=Micro a 4=Grande), monto total. |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Los árboles de decisión son, de lejos, los modelos más “explicables” en machine learning. A diferencia de otros algoritmos que son cajas negras, un árbol puede mostrarse gráficamente como un diagrama de preguntas y respuestas, similar a los “árboles de proceso” que se usan en normativas y procedimientos del Estado.

Pero el aporte más poderoso para el sector público viene del Random Forest: la **importancia de variables**. Saber qué factores pesan más en una predicción (por ejemplo, qué características de una licitación predicen mejor si habrá oferta o no) es información de diseño de política.

Aplicaciones directas en el Estado:

- **Clasificación de riesgo:** ¿este contrato tiene características de posible conflicto de interés?
- **Priorizar fiscalización:** qué variables predicen más incumplimientos.
- **Estimación de demanda:** cuantos beneficiarios esperar por características territoriales.
- **Toma de decisiones estructurada:** el árbol puede convertirse en un flujograma de apoyo a la decisión.

> 🏛️ **Mensaje clave:** los árboles son modelos que “piensa como un funcionario”: secuencias de preguntas con reglas claras. Son fáciles de explicar a autoridades y equipos no técnicos.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|---|---|---|
| **Árbol de decisión** | Hace preguntas sí/no sobre las features hasta predecir | Flujograma de toma de decisión como en guías de trámites |
| **Nodo** | Cada pregunta del árbol | Criterio en un proceso de evaluación |
| **Hoja** | Respuesta final del árbol | Resultado del proceso: monto estimado |
| **Profundidad (`max_depth`)** | Número de niveles del árbol | Cuantas preguntas puede hacer antes de dar una respuesta |
| **Sobreajuste** | El modelo memoriza el pasado y falla con lo nuevo | Regla diseñada sólo para los casos conocidos; no sirve para los nuevos |
| **Random Forest** | Muchos árboles, cada uno con datos distintos, se promedian | Comisión evaluadora de varios expertos: el promedio es más robusto que uno solo |
| **`n_estimators`** | Número de árboles en el bosque | Tamaño de la comisión evaluadora |
| **Importancia de features** | Cuánto pesa cada variable en las predicciones del bosque | ¿Qué factor es más determinante: la cantidad pedida o el tamaño del proveedor? |
| `feature_importances_` | Atributo del bosque con los pesos de cada variable | Ranking de factores influyentes |
| **Hiperparámetro** | Configuración del modelo que se define antes de entrenar | Parámetros del proceso antes de abrir el concurso |
| **Ensemble** | Combinar muchos modelos para obtener uno mejor | Panel de evaluación multidisciplinario |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Definir `X` con doble corchete y `y` con uno | ✅ | Repasa R2-04 si esto te cuesta |
| Usar `train_test_split` con `test_size` y `random_state` | ✅ | Lo hiciste en el ejercicio 1 de R2-04 |
| Aplicar el patrón `modelo.fit()` + `modelo.predict()` | ✅ | Es el mismo patrón que ya conoces |
| Interpretar el MAE como un error promedio | ✅ | Revisado en R2-04 |
| Entender qué es sobreajuste conceptualmente | ✅ | Revisado en R2-04 |

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación y visualización del árbol demo

**🎯 Objetivo:** Cargar el dataset y ver cómo se ve un árbol de decisión de profundidad 2.

**💡 Concepto clave:** El gráfico del árbol demo es la representación visual más directa de qué hace el modelo: cada caja es una pregunta, cada rama es una respuesta. Leer este gráfico es clave para explicar el modelo a personas no técnicas.

**🔍 Qué hace el código:** Carga el CSV, entrena un árbol de profundidad 2 y lo grafica con `plot_tree`.

**⚠️ Error frecuente:** Saltarse la visualización. El gráfico del árbol es una de las salidas más útiles del módulo para entender cómo funciona el modelo.

**✅ Señal de comprensión:** Puedes leer el árbol graficado y describir en voz alta la regla que usa para estimar el monto de una compra.

---

### 🔷 Sección 1 — ¿Qué es un árbol de decisión?

**🎯 Objetivo:** Entender la lógica de los árboles antes de usarlos.

**💡 Concepto clave:** Un árbol de decisión es exactamente como un flujograma: “¿la cantidad es mayor a 100?”, si sí, sigue por la izquierda; si no, por la derecha. Cada camino termina en una predicción. Es el modelo más fácil de explicar a un jefe de servicio que no es técnico.

**🔍 Qué hace el código:** Solo texto conceptual. No hay `TODO` en esta sección.

**⚠️ Error frecuente:** Creer que “más profundo = mejor”. El árbol puede crecer sin fin y memorizar cada contrato individual, lo que lo hace inútil para casos nuevos.

**✅ Señal de comprensión:** Puedes describir la diferencia entre regresión lineal (una ecuación) y un árbol (preguntas secuenciales).

---

### 🔷 Sección 2 — Ejercicio 1: preparar datos con dos features

**🎯 Objetivo:** Definir `X` con `cantidad` y `tamano_num`, y dividir en train/test.

**💡 Concepto clave:** Este módulo pasa de una sola feature a **dos**. Eso no cambia nada en la sintaxis (`df[["cantidad", "tamano_num"]]`), pero sí aumenta el poder del modelo: ahora puede hacer preguntas sobre ambas variables.

**🔍 Qué hace el código:** Define `X` con dos columnas e `y` con `monto_total`, luego divide con `train_test_split`.

**⚠️ Error frecuente:** Usar un solo corchete `df["cantidad", "tamano_num"]` que dará error. La lista de columnas debe ir dentro de doble corchete: `df[["cantidad", "tamano_num"]]`.

**✅ Señal de comprensión:** `X_train.columns` muestra `["cantidad", "tamano_num"]` y el tamaño es 5188 filas.

---

### 🔷 Sección 3 — Ejercicio 2: entrenar y evaluar el árbol

**🎯 Objetivo:** Entrenar `DecisionTreeRegressor(max_depth=3)` y calcular su MAE en prueba.

**💡 Concepto clave:** El parámetro `max_depth=3` limita el árbol a 3 niveles de preguntas. Es suficiente para capturar patrones sin memorizar. Cambiar este número cambia el comportamiento del modelo.

**🔍 Qué hace el código:** `arbol.fit(X_train, y_train)` entrena el árbol. `arbol.predict(X_test)` genera predicciones. `mean_absolute_error(y_test, y_pred)` mide el error.

**⚠️ Error frecuente:** Olvidar `from sklearn.tree import DecisionTreeRegressor`. Esta es una clase distinta a `LinearRegression`.

**✅ Señal de comprensión:** El MAE del árbol puede compararse con el de la regresión lineal de R2-04. No siempre el árbol gana en datos simples.

---

### 🔷 Sección 4 — El sobreajuste visible (ilustración + Ejercicio 3)

**🎯 Objetivo:** Ver con tus propios ojos cómo sube el MAE en prueba cuando el árbol crece sin límite.

**💡 Concepto clave:** El gráfico de la sección muestra algo crucial: a medida que aumenta la profundidad, el error en entrenamiento baja (el modelo memoriza mejor), pero el error en prueba primero baja y luego sube. El óptimo está en esa curva. Un árbol sin `max_depth` tiene error de entrenamiento cercano a cero, pero un error de prueba mucho mayor.

**🔍 Qué hace el código:** Entrena `DecisionTreeRegressor(random_state=42)` sin `max_depth`, calcula el MAE en entrenamiento y en prueba.

**⚠️ Error frecuente:** Esperar que el MAE de prueba también sea muy bajo. La señal del sobreajuste es precisamente que el entrenamiento es excelente y la prueba es mala.

**✅ Señal de comprensión:** `mae_train` es mucho menor que `mae_test`. Esa diferencia grande es la firma del sobreajuste.

---

### 🔷 Sección 5 — Ejercicio 4: Random Forest e importancia de features

**🎯 Objetivo:** Entrenar un bosque aleatorio, evaluar su MAE e identificar la variable más importante.

**💡 Concepto clave:** El bosque es más robusto que un solo árbol porque promedia 100 árboles distintos. Además, `feature_importances_` te da el ranking de variables: saber qué factor manda más en las predicciones es información de política, no solo técnica.

**🔍 Qué hace el código:** `RandomForestRegressor(n_estimators=100, random_state=42).fit(...)` entrena el bosque. `pd.Series(bosque.feature_importances_, index=X_train.columns).idxmax()` devuelve el nombre de la variable más importante.

**⚠️ Error frecuente:** El bosque tarda más que un solo árbol (entrena 100 modelos). Si Colab parece lento, es normal: dale unos segundos.

**✅ Señal de comprensión:** `feature_top == "cantidad"` y el MAE del bosque es mejor o comparable al del árbol individual.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Preparar datos con dos features

**Habilidad que desarrollas:** Ampliar el espacio de features y mantener el flujo train/test.

**Pista 1 (conceptual):** Ahora tienes dos variables predictoras. ¿Cómo pasas dos columnas a `X`?

**Pista 2 (técnica):** `df[["cantidad", "tamano_num"]]` con doble corchete y lista de columnas.

**Pista 3 (casi solución):** La línea completa de división es `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)`.

**Lógica de solución:** Exactamente igual que en R2-04 pero con dos columnas en `X`.

---

### ✍️ Ejercicio 2 — Entrenar y evaluar el árbol

**Habilidad que desarrollas:** Aplicar el patrón `fit`/`predict`/`MAE` con un nuevo modelo.

**Pista 1 (conceptual):** El proceso es idéntico a R2-04: crear el modelo, entrenarlo con train, predecir en test, calcular MAE.

**Pista 2 (técnica):** `DecisionTreeRegressor(max_depth=3, random_state=42)`. El `max_depth` ya está en el código del notebook.

**Pista 3 (casi solución):** `arbol.fit(X_train, y_train)`, luego `y_pred = arbol.predict(X_test)`, luego `mae_arbol = mean_absolute_error(y_test, y_pred)`.

**Lógica de solución:** Tres líneas: `fit`, `predict`, `mean_absolute_error`.

---

### ✍️ Ejercicio 3 — Ver el sobreajuste con tus manos

**Habilidad que desarrollas:** Detectar sobreajuste comparando errores de train y test.

**Pista 1 (conceptual):** El árbol profundo no tiene `max_depth`. Va a memorizar cada compra del entrenamiento.

**Pista 2 (técnica):** `mae_train = mean_absolute_error(y_train, arbol_profundo.predict(X_train))` y `mae_test = mean_absolute_error(y_test, arbol_profundo.predict(X_test))`.

**Pista 3 (casi solución):** El `fit` ya está implícito. Sólo faltan las dos líneas de MAE, una con `y_train/X_train` y otra con `y_test/X_test`.

**Lógica de solución:** Entrenar `arbol_profundo` y calcular dos MAE: uno en train y uno en test.

---

### ✍️ Ejercicio 4 — Random Forest e importancias

**Habilidad que desarrollas:** Entrenar un ensemble y extraer información sobre las variables.

**Pista 1 (conceptual):** El bosque usa el mismo patrón `fit`/`predict` que ya conoces. Lo nuevo es leer `feature_importances_`.

**Pista 2 (técnica):** `pd.Series(bosque.feature_importances_, index=X_train.columns)` crea una serie con los pesos de cada variable. `.idxmax()` devuelve el nombre de la más importante.

**Pista 3 (casi solución):** `feature_top = pd.Series(bosque.feature_importances_, index=X_train.columns).idxmax()`. El resultado esperado es `"cantidad"`.

**Lógica de solución:** Entrenar el bosque, calcular MAE en prueba, extraer la importancia con `pd.Series(...).idxmax()`.

---

## 7. Sección en Profundidad: Ejercicio 4 — Importancia de features como herramienta de política pública

El ejercicio 4 es el más relevante para política pública de este módulo. Saber qué variable pesa más en una predicción puede cambiar decisiones de diseño de programas.

### ¿Qué dice la importancia de features?

`feature_importances_` es un vector que suma 1. Cada valor indica qué proporción de las divisiones del bosque se basó en esa variable. Si `cantidad` tiene importancia 0.80 y `tamano_num` tiene 0.20, el bosque usó la cantidad en el 80% de sus decisiones.

### Uso en el diseño de políticas

| Situación | Lo que preguntamos | Lo que dice la importancia |
|---|---|---|
| Predecir gasto de contratos | ¿Qué factor determina más el monto? | Si es `cantidad`, debemos regularla. Si es `tamano_num`, el tamaño del proveedor importa más. |
| Predecir riesgo de incumplimiento | ¿Qué característica es más predictiva? | Permite diseñar criterios de elegibilidad basados en evidencia. |
| Priorizar fiscalización | ¿Qué variables definen mejor los casos problemáticos? | Permite asignar recursos de fiscalización donde más importan. |

### Advertencias importantes

> ⚠️ **Importancia ≠ causalidad.** Una variable importante para el modelo no es necesariamente la *causa* del resultado. Puede ser un proxy de otra variable no incluída.

> ⚠️ **Importancia en datos sesgados.** Si el dataset histórico tiene sesgos (por ejemplo, infrarepresentación de proveedores MIPYME), la importancia puede reflejar ese sesgo, no la realidad.

---

## 8. Conexión con profundiza.ipynb

Este módulo tiene `solucion.ipynb` como referencia. No hay `profundiza.ipynb` separado.

> 💡 **Alternativas de profundización:** Si quieres ir más allá, intenta:
> - Cambiar `n_estimators` de 100 a 10 y comparar el MAE.
> - Probar `GradientBoostingRegressor` de scikit-learn y comparar su MAE con el Random Forest.
> - Graficar la importancia de features con `plt.bar(X.columns, bosque.feature_importances_)`.

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Qué es un árbol de decisión?

- a) Un modelo que predice usando una fórmula lineal
- b) Un modelo que hace preguntas sí/no secuenciales sobre las features para llegar a una predicción
- c) Un algoritmo que agrupa datos similares sin supervisar
- d) Una red de neuronas artificiales

✅ **Respuesta correcta: b)**
**Explicación:** Un árbol de decisión es una secuencia jerárquica de preguntas binarias. Es equivalente a un flujograma de decisión con criterios cuantitativos.

---

**Pregunta 2:** Un árbol entrenado sin `max_depth` tiene MAE de entrenamiento muy bajo y MAE de prueba muy alto. ¿Qué significa esto?

- a) El modelo es excelente porque el error de entrenamiento es bajo
- b) El modelo tiene sobreajuste: memorizó el pasado pero no generaliza
- c) El dataset tiene errores
- d) Hay que agregar más features

✅ **Respuesta correcta: b)**
**Explicación:** La brecha entre MAE de train y MAE de test es la firma del sobreajuste. Un buen modelo tiene errores similares en ambos conjuntos.

---

**Pregunta 3:** ¿Para qué sirve `max_depth` en un árbol de decisión?

- a) Para aumentar el número de datos de entrenamiento
- b) Para limitar la complejidad del árbol y evitar el sobreajuste
- c) Para decidir cuántas features usar
- d) Para calcular el MAE automáticamente

✅ **Respuesta correcta: b)**
**Explicación:** `max_depth` define cuántos niveles de preguntas puede hacer el árbol. Un valor pequeño produce modelos simples que generalizan mejor.

---

**Pregunta 4:** Un Random Forest de 100 árboles es mejor que uno solo porque:

- a) Cada árbol se entrena con todos los datos
- b) Los 100 árboles promedian sus predicciones, lo que reduce el error y la variabilidad
- c) Solo usa los mejores 10 árboles de los 100
- d) Entrena más rápido

✅ **Respuesta correcta: b)**
**Explicación:** Cada árbol se entrena con una muestra aleatoria distinta de los datos. El promedio de muchos árboles débilmente correlacionados es más robusto y estable.

---

**Pregunta 5:** `bosque.feature_importances_` indica que `cantidad` tiene importancia 0.85 y `tamano_num` tiene 0.15. ¿Qué concluyes?

- a) La cantidad causa el 85% del monto de la compra
- b) El modelo usó la cantidad en el 85% de sus divisiones; es la variable más predictiva para el modelo
- c) El 85% de las compras son de cantidad alta
- d) El tamaño del proveedor no debería incluirse en el modelo

✅ **Respuesta correcta: b)**
**Explicación:** La importancia mide cuánto usó el modelo cada variable, no causalidad. Es una herramienta de interpretación, no de causalidad.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente sector público / Excel |
|---|---|---|
| **Árbol de decisión** | Modelo de preguntas sí/no secuenciales | Flujograma de decisión con criterios numéricos |
| **Nodo** | Pregunta en el árbol | Criterio de evaluación en un proceso |
| **Hoja** | Respuesta final del árbol | Resultado del proceso |
| **Profundidad** | Número de niveles del árbol | Complejidad del flujograma |
| **Sobreajuste** | Memorizar en vez de aprender; falla con datos nuevos | Regla pensada solo para casos conocidos |
| **Random Forest** | Ensemble de muchos árboles promediados | Comisión evaluadora multidisciplinaria |
| **`n_estimators`** | Número de árboles en el bosque | Tamaño de la comisión |
| **Importancia de features** | Peso de cada variable en las predicciones | Ranking de factores determinantes |
| **Ensemble** | Combinar múltiples modelos para reducir errores | Panel de expertos que promedian criterios |
| **Hiperparámetro** | Configuración del modelo definida antes de entrenar | Bases del concurso fijadas antes de abrir ofertas |
| **`max_depth`** | Profundidad máxima del árbol | Límite de complejidad del flujograma |
| **`feature_importances_`** | Vector con la importancia de cada variable | Ranking de criterios de decisión |

---

## 11. Conexión con el Módulo Siguiente

En R2-05 aprendiste a predecir con modelos más potentes: árboles y bosques. El patrón `fit`/`predict` sigue siendo el mismo.

**El siguiente módulo es R2-06 · Clasificación y Clustering.**

Allí cambiarás el objetivo de predicción:

- En vez de predecir un **número** (monto), predecirás una **categoría** (Grande/Micro, sí/no).
- Aprenderás métricas específicas para clasificación: accuracy, precisión, recall.
- También agruparás datos sin etiquetas con **clustering** (K-Means): encontrar patrones ocultos sin saber de antemano cuáles son los grupos.

> 🔗 **Conexión pedagógica:** R2-05 te enseña a predecir mejor; R2-06 te enseña a predecir diferente (categorías) y a descubrir estructura oculta en los datos. Las dos habilidades son complementarias para análisis de política pública.

¡Excelente! Ya conoces el modelo más explicable **y** el más robusto de ML. Eso es un combo muy poderoso 🌲
