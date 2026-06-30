# 📘 Guía de Aprendizaje — R2-04 · Fundamentos de Machine Learning

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-04 · Fundamentos de Machine Learning (D9) |
| **Pista / Rama** | R2 — Científico/a de Datos · Línea B |
| **Duración estimada** | 3–4 horas (Semana 10) |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-02 completado (tablas analíticas con SQL). R2-03 recomendado (estadística descriptiva). |
| **Competencia de salida** | Plantear un problema de aprendizaje supervisado, dividir datos en entrenamiento y prueba, entrenar un modelo de regresión con scikit-learn, evaluarlo con MAE y usarlo para predecir un caso nuevo. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de alimentos de ChileCompra/MercadoPúblico (cantidad, monto total). |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Imagina que tienes que estimar el gasto de un contrato antes de que ocurra, o predecir la demanda de un programa social antes de que lleguen los beneficiarios. Eso es exactamente lo que hace un modelo de machine learning: **aprende de ejemplos pasados para estimar casos futuros**.

Este módulo te da los fundamentos correctos para construir ese tipo de herramienta. Y lo más importante: te enseña los **hábitos correctos** desde el principio: separar datos de prueba, evaluar con honestidad, y entender el riesgo del sobreajuste.

Aplicaciones directas en el Estado:

- **Gestión de compras:** estimar el monto de una orden antes de aprobarla.
- **Salud:** estimar el tiempo de espera para un tipo de atención según la carga del servicio.
- **Presupuesto:** proyectar el gasto en función de variables operativas.
- **Planificación:** estimar la demanda de un programa según características del territorio.

> 🏛️ **Mensaje clave:** no necesitas ser matemático/a para entrenar un modelo. Lo que sí necesitas son los hábitos correctos: separar prueba, evaluar en datos que el modelo no vio, y entender lo que el error te dice.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|---|---|---|
| **Aprendizaje supervisado** | Aprende a partir de ejemplos con la respuesta correcta | Aprender a estimar gastos usando facturas históricas reales |
| **Features (`X`)** | Variables de entrada que el modelo usa para predecir | Indicadores de un trámite: cantidad, tipo, región |
| **Objetivo (`y`)** | La variable que queremos predecir | El monto total, el tiempo de espera, el resultado del proceso |
| **Regresión** | Predice un número continuo | Estimar el gasto de un contrato |
| **Clasificación** | Predice una categoría | ¿Este contrato tiene riesgo alto, medio o bajo? |
| **Entrenamiento (train)** | Datos con los que el modelo aprende | Historial de contratos pasados con sus resultados conocidos |
| **Prueba (test)** | Datos reservados para evaluar; el modelo no los ve al entrenar | Contratos nuevos que aun no se han ejecutado |
| **Sobreajuste (*overfitting*)** | El modelo memoriza el pasado pero no generaliza | Un modelo que predice perfecto en los datos viejos pero falla en los nuevos |
| `train_test_split` | Divide los datos en entrenamiento y prueba al azar | Separar el historial en “para aprender” y “para verificar” |
| `modelo.fit()` | El modelo aprende de los datos de entrenamiento | El modelo estudia los ejemplos históricos |
| `modelo.predict()` | El modelo genera predicciones para datos nuevos | El modelo responde: “para esta compra, el monto estimado es...” |
| **MAE (Error Absoluto Medio)** | Promedio del error absoluto en las predicciones | En promedio, ¿cuanto se equivoca el modelo? |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Cargar y filtrar un DataFrame con pandas | ✅ | Repasa R2-01 si esto te cuesta |
| Entender qué es una *feature* y por qué sirve | ✅ | Revisa la sección conceptual de R2-02 |
| Interpretar un promedio y entender la idea de “error” | ✅ | Piensa en el error como “cuanto me equivoco en promedio” |
| Ejecutar celdas en Colab sin problemas | ✅ | Ya tienes experiencia de los módulos anteriores |
| Entender intuitivamente que “memoizar” no es lo mismo que “aprender” | ✅ | Eso es todo lo que necesitas para entender el sobreajuste |

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno

**🎯 Objetivo:** Cargar el dataset de compras públicas de alimentos y visualizar la relación entre cantidad y monto.

**💡 Concepto clave:** Este módulo usa datos de compras de alimentos porque tienen una relación más clara entre cantidad y monto que el dataset general. El gráfico de dispersión que aparece al inicio es la relación que el modelo va a aprender a representar como una línea recta.

**🔍 Qué hace el código:** Descarga el CSV si no está disponible, lo carga en `df` y genera un scatter plot de `cantidad` vs `monto_total`.

**⚠️ Error frecuente:** Saltar al ejercicio sin ver el gráfico. El gráfico muestra visualmente la relación que se va a modelar y ayuda a entender si tiene sentido una regresión lineal.

**✅ Señal de comprensión:** Ves el scatter plot y puedes describir qué patrón general muestra (si a mayor cantidad el monto tiende a subir).

---

### 🔷 Sección 1 — ¿Qué es el machine learning?

**🎯 Objetivo:** Entender la lógica del aprendizaje supervisado antes de escribir código.

**💡 Concepto clave:** En vez de escribir reglas a mano (“si la cantidad supera 50, el monto es...”), le muestras al modelo miles de ejemplos y él descubre las reglas solo. Igual que un/a funcionario/a aprende a estimar gastos con experiencia, el modelo aprende de los registros históricos.

**🔍 Qué hace el código:** Solo explica los conceptos. No hay `TODO` aquí.

**⚠️ Error frecuente:** Saltarse la sección conceptual. La diferencia entre regresión y clasificación, y entre features y objetivo, son distinciones que aparecerán en todos los módulos siguientes.

**✅ Señal de comprensión:** Puedes explicar con tus palabras por qué este problema es de regresión (predice un número) y no de clasificación.

---

### 🔷 Sección 2 — La regla de oro: separar datos de prueba

**🎯 Objetivo:** Definir `X` e `y` y dividir los datos en entrenamiento (70%) y prueba (30%).

**💡 Concepto clave:** Evaluar un modelo con los mismos datos que usó para aprender es hacer trampa. Es como corregir un examen con el solucionario que el alumno/a ya vio. La “prueba” son datos que el modelo nunca vio durante el entrenamiento. Si se desempeña bien ahí, significa que realmente aprendió.

**🔍 Qué hace el código:**
- `X = df[["cantidad"]]` — **doble corchete** para obtener una tabla (no una columna).
- `y = df["monto_total"]` — **un corchete** para obtener la columna objetivo.
- `train_test_split(X, y, test_size=0.3, random_state=42)` divide al azar el 70% para entrenar y el 30% para probar.

**⚠️ Error frecuente:** Usar un corchete simple para `X`. `df["cantidad"]` devuelve una Serie (una columna), pero scikit-learn espera una tabla (DataFrame). Por eso se usa `df[["cantidad"]]` con doble corchete.

**✅ Señal de comprensión:** `X_train` tiene 5.188 filas y `X_test` tiene 2.224. La suma es el total del dataset.

---

### 🔷 Sección 3 — Entrenar tu primer modelo

**🎯 Objetivo:** Crear un `LinearRegression`, entrenarlo con los datos de entrenamiento y generar predicciones sobre los de prueba.

**💡 Concepto clave:** La regresión lineal busca la mejor línea recta que relaciona `cantidad` con `monto_total`. El coeficiente que aprende dice: “por cada unidad adicional comprada, el monto sube $X pesos”. El patrón `fit` + `predict` es idéntico para todos los modelos de scikit-learn.

**🔍 Qué hace el código:**
1. `modelo.fit(X_train, y_train)` — el modelo estudia los ejemplos de entrenamiento.
2. `modelo.predict(X_test)` — el modelo genera una estimación para cada fila de `X_test`.

**⚠️ Error frecuente:** Llamar `modelo.fit(X_test, y_test)`. Siempre se entrena con `train`, nunca con `test`.

**✅ Señal de comprensión:** Después del `fit`, el mensaje del chequeo muestra el coeficiente aprendido. Ese número tiene un significado real: cuanto sube el monto por cada unidad de cantidad.

---

### 🔷 Sección 4 — Evaluar con honestidad

**🎯 Objetivo:** Calcular el MAE sobre los datos de prueba.

**💡 Concepto clave:** El MAE (Error Absoluto Medio) mide en promedio cuánto se equivoca el modelo. Si el modelo predice $50.000 pero el monto real fue $80.000, el error absoluto es $30.000. El MAE es el promedio de esos errores en todos los casos de prueba.

**🔍 Qué hace el código:** `mean_absolute_error(y_test, y_pred)` calcula el MAE entre los valores reales (`y_test`) y los predichos (`y_pred`).

**⚠️ Error frecuente:** Calcular el MAE usando `y_train` en vez de `y_test`. Eso mide el desempeño en los datos con que aprendió, que casi siempre es mejor. La verdad está en los datos de prueba.

**✅ Señal de comprensión:** El MAE de entrenamiento y el de prueba son similares. Si fueran muy distintos, habría sobreajuste.

---

### 🔷 Sección 5 — Predecir un caso nuevo

**🎯 Objetivo:** Usar el modelo entrenado para estimar el monto total de una compra de 100 artículos.

**💡 Concepto clave:** Este es el propósito final de un modelo: estimar lo que no hemos medido. Una vez entrenado, el modelo puede responder a cualquier cantidad, incluso una que no estaba en el dataset.

**🔍 Qué hace el código:** Construye un DataFrame con la cantidad nueva, lo pasa a `modelo.predict()` y extrae el primer (y único) valor del resultado con `[0]`.

**⚠️ Error frecuente:** Pasar solo el número `100` a `predict` sin envolverlo en un DataFrame. Scikit-learn espera la misma estructura que usaste en `fit`.

**✅ Señal de comprensión:** El monto estimado tiene sentido (no es negativo ni un número absurdo) y puedes explicar por qué ese es el resultado esperado.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Separar X, y y reservar la prueba

**Habilidad que desarrollas:** Estructurar correctamente un problema de aprendizaje supervisado.

**Pista 1 (conceptual):** Necesitas separar los datos en dos grupos: uno para que el modelo aprenda y otro para probar si realmente aprendió. ¿Qué función de scikit-learn hace esa división?

**Pista 2 (técnica):** `train_test_split(X, y, test_size=0.3, random_state=42)` devuelve cuatro objetos en orden: `X_train, X_test, y_train, y_test`.

**Pista 3 (casi solución):** Recuerda usar doble corchete para `X`: `df[["cantidad"]]`. El resultado debe tener 5.188 filas de entrenamiento y 2.224 de prueba.

**Lógica de solución:** Llamar a `train_test_split` con los parámetros correctos y desempaquetar en cuatro variables.

---

### ✍️ Ejercicio 2 — Crear, entrenar y predecir

**Habilidad que desarrollas:** Usar el patrón `fit`/`predict` de scikit-learn.

**Pista 1 (conceptual):** El modelo ya está creado. Ahora necesitas dos pasos: que aprenda de los datos de entrenamiento, y que luego prediga sobre los de prueba.

**Pista 2 (técnica):** `modelo.fit(X_train, y_train)` no devuelve nada útil directamente. Después llamas `y_pred = modelo.predict(X_test)`.

**Pista 3 (casi solución):** Ambas líneas son necesarias. Sin `fit`, `predict` dará error. Sin `predict`, no tendrás `y_pred` para evaluar.

**Lógica de solución:** Ejecutar `modelo.fit(X_train, y_train)` y luego `y_pred = modelo.predict(X_test)`.

---

### ✍️ Ejercicio 3 — Calcular el MAE

**Habilidad que desarrollas:** Evaluar un modelo con honestidad usando métricas en datos de prueba.

**Pista 1 (conceptual):** El MAE mide cuánto se equivoca el modelo en promedio. Se calcula comparando los valores reales con los predichos.

**Pista 2 (técnica):** `mean_absolute_error(valores_reales, valores_predichos)` es la función de scikit-learn.

**Pista 3 (casi solución):** Los valores reales son `y_test` y los predichos son `y_pred`. El resultado se guarda en `mae`.

**Lógica de solución:** `mae = mean_absolute_error(y_test, y_pred)`.

---

### ✍️ Ejercicio 4 — Predecir un caso nuevo

**Habilidad que desarrollas:** Usar el modelo entrenado con datos reales nuevos.

**Pista 1 (conceptual):** El modelo espera un DataFrame con la misma estructura que usó al entrenar. Necesitas crear uno con la cantidad nueva.

**Pista 2 (técnica):** `pd.DataFrame({"cantidad": [100]})` crea un DataFrame con una fila y la columna correcta.

**Pista 3 (casi solución):** `modelo.predict(nueva_compra)[0]` devuelve el primer (y único) valor de la predicción. Guárdalo en `temp_estimada`.

**Lógica de solución:** Construir el DataFrame, pasarlo a `predict` y extraer el valor con `[0]`.

---

## 7. Sección en Profundidad: Ejercicio 2 — El patrón `fit`/`predict` y su impacto en política pública

El ejercicio 2 contiene el habito más importante de este módulo: el patrón **`fit` luego `predict`** es el mismo para todos los modelos de scikit-learn. Una vez que lo dominas con regresión lineal, puedes cambiar `LinearRegression()` por `RandomForestRegressor()` o `GradientBoostingClassifier()` con exactamente el mismo código alrededor.

### La regresión lineal como punto de partida

La regresión lineal aprende la ecuación:

```
monto_total = a * cantidad + b
```

Donde `a` (el coeficiente) es lo que aprende con `fit`. Ese número tiene un significado real: **cuántos pesos sube el monto por cada unidad adicional comprada**.

### Por qué el sobreajuste es especialmente peligroso en el Estado

Un modelo sobreajustado que se usa para decisiones públicas puede:

- **Estimar incorrectamente** presupuestos futuros porque “calió” solo en el pasado.
- **Dar falsas certezas** en informes técnicos que sostienen políticas.
- **Ser invalidado** en una auditoría si no hay un conjunto de prueba que demuestre que generaliza.

> 🚨 **Regla pública:** cualquier modelo usado para decisiones de política debe evaluarse obligatoriamente en datos que no participaron en el entrenamiento. No es burocracia: es rigor metodológico.

### Aplicaciones del patrón `fit`/`predict` en el Estado

| Caso de uso | `X` (*features*) | `y` (objetivo) | Tipo |
|---|---|---|---|
| Estimar gasto de compra | Cantidad, tipo | Monto total | Regresión |
| Clasificar riesgo de proveedor | Historial, mora, giro | Alto / Medio / Bajo | Clasificación |
| Estimar demanda de programa | Características del territorio | Número de beneficiarios | Regresión |
| Detectar anomalías en contratos | Tipo, monto, proveedor | Normal / Sospechoso | Clasificación |

---

## 8. Conexión con profundiza.ipynb

Este módulo no tiene `profundiza.ipynb` propio. El notebook `solucion.ipynb` sirve como referencia interna del equipo.

> 💡 **Alternativa de profundización:** Si quieres ir más allá, intenta cambiar `LinearRegression()` por `Ridge()` o `Lasso()` (importados desde `sklearn.linear_model`) y compara el MAE resultante. Son variantes de la regresión lineal con regularización, que veremos más a fondo en módulos posteriores.

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Qué diferencia hay entre un problema de regresión y uno de clasificación?

- a) La regresión usa más datos
- b) La regresión predice un número continuo; la clasificación predice una categoría
- c) La clasificación siempre es más precisa
- d) La regresión solo se usa con datos temporales

✅ **Respuesta correcta: b)**
**Explicación:** Si lo que quieres predecir es un número (monto, tiempo, demanda), es regresión. Si es una etiqueta (aprobado/rechazado, riesgo alto/bajo), es clasificación.

---

**Pregunta 2:** ¿Por qué es incorrecto evaluar el modelo con los datos de entrenamiento?

- a) Porque son demasiados datos y el cálculo tarda mucho
- b) Porque el modelo puede haber memorizado esas respuestas, lo que da una evaluación falsamente optimista
- c) Porque scikit-learn no permite usar `y_train` en `mean_absolute_error`
- d) Porque los datos de entrenamiento siempre tienen errores

✅ **Respuesta correcta: b)**
**Explicación:** El modelo aprende de los datos de entrenamiento. Evaluarlo con esos mismos datos puede dar una métrica excelente aunque el modelo sea pésimo con casos nuevos.

---

**Pregunta 3:** ¿Qué ocurre con `modelo.predict(X_test)` si el modelo nunca ejecutó `.fit()`?

- a) Devuelve ceros
- b) Lanza un error porque el modelo no ha aprendido nada
- c) Usa el modelo del último entrenamiento disponible
- d) Devuelve el promedio de y

✅ **Respuesta correcta: b)**
**Explicación:** Sin `fit`, el modelo no tiene parámetros aprendidos. scikit-learn lanzará `NotFittedError` indicando que el modelo no fue entrenado.

---

**Pregunta 4:** ¿Qué significa que el MAE de prueba sea mucho mayor que el MAE de entrenamiento?

- a) El modelo no tiene suficientes datos
- b) El modelo tiene sobreajuste: memorizó el entrenamiento pero no generaliza
- c) El MAE de prueba siempre es mayor, es normal
- d) Los datos de prueba son incorrectos

✅ **Respuesta correcta: b)**
**Explicación:** Esta brecha entre entrenamiento y prueba es la señal clásica del sobreajuste. El modelo “calió” demasiado a los datos de entrenamiento y pierde precisión con datos nuevos.

---

**Pregunta 5:** Si quisieras predecir el gasto de una compra de 200 artículos, ¿cómo le pasarías ese dato al modelo?

- a) `modelo.predict(200)`
- b) `modelo.predict([200])`
- c) `modelo.predict(pd.DataFrame({"cantidad": [200]}))`
- d) `modelo.fit(200)`

✅ **Respuesta correcta: c)**
**Explicación:** scikit-learn espera que la entrada tenga la misma estructura que la usada en `fit`. Como entrenaste con `df[["cantidad"]]` (un DataFrame), debes pasar un DataFrame con la misma columna.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente sector público / Excel |
|---|---|---|
| **Machine learning** | Computador aprende patrones de ejemplos en vez de reglas escritas a mano | Construir una fórmula de estimación aprendida del historial |
| **Aprendizaje supervisado** | Aprende de ejemplos con la respuesta correcta conocida | Aprender a estimar gastos con facturas históricas reales |
| **Features (`X`)** | Variables de entrada que el modelo usa para predecir | Indicadores de un trámite o contrato |
| **Objetivo (`y`)** | Variable que se quiere predecir | Monto, tiempo, resultado |
| **Regresión** | Predice un número continuo | Estimación de presupuesto |
| **Clasificación** | Predice una categoría | Aprobado / Rechazado / Riesgo alto |
| **Train / Test** | Conjunto de entrenamiento / conjunto de prueba | Historial para aprender / casos nuevos para verificar |
| **Sobreajuste** | El modelo memoriza en vez de aprender; falla con datos nuevos | Modelo que predice perfecto en el pasado pero falla en la operación real |
| `fit()` | El modelo aprende de los datos | “Estudiar” los ejemplos históricos |
| `predict()` | El modelo estima para datos nuevos | “Responder” a casos no vistos |
| **MAE** | Error absoluto medio: promedio de los errores de predicción | Cuánto me equivoco en promedio |
| **LinearRegression** | Modelo que aprende una línea recta entre X e y | Ajuste lineal entre dos variables |

---

## 11. Conexión con el Módulo Siguiente

En R2-04 entrenaste tu primer modelo de machine learning con las prácticas correctas. Lo que aprendiste aquí —el patrón `fit`/`predict`, la separación entrenamiento/prueba, la evaluación honesta— no cambia en los módulos siguientes.

**El siguiente módulo es R2-05 · Modelos basados en árboles.**

Allí cambiarás `LinearRegression()` por modelos más potentes y flexibles:

- Aprenderás cómo funcionan los **árboles de decisión** y los **Random Forest**.
- Podrás capturar relaciones no lineales que la regresión lineal no puede.
- Usarás el mismo patrón `fit`/`predict` que acabas de dominar.

> 🔗 **Conexión pedagógica:** R2-04 te da el esqueleto correcto del proceso ML; R2-05 lo potencia con algoritmos más sofisticados. Todo lo que hiciste aquí se reutiliza directamente.

¡Excelente trabajo! Ya entrenas modelos con rigor. Eso te distingue 🚀
