# 📘 Guía de Aprendizaje — R2-07 · Evaluación y validación de modelos

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-07 · Evaluación y validación de modelos |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 3–4 horas |
| **Semana** | Semana 12–13 |
| **Nivel** | Intermedio-Avanzado |
| **Prerrequisitos** | R2-04 (fundamentos de ML), R2-05 (árboles), R2-06 (clasificación y clustering) |
| **Competencia de salida** | Evaluar un clasificador con rigor: métricas honestas, sin fuga de datos, validado con cross-validation y auditado por fairness |
| **Dataset** | `compras_ml.csv` — órdenes de compra de alimentos, ChileCompra (cantidad, monto_total, categoría, región, tamaño del proveedor) |
| **Entregable** | Las 5 celdas de chequeo del notebook mostrando ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Imagina que tu jefatura te pide desarrollar un modelo que detecte si una orden de compra la adjudica un proveedor grande. Entrenas el modelo, lo pruebas y el sistema dice: "95% de exactitud". Llevas el informe, alguien pregunta: "¿Y en las regiones del sur funciona igual que en la Región Metropolitana?". Silencio.

Ahí es donde este módulo te salva. En el Estado chileno, **un modelo que funciona bien en promedio pero falla en ciertas regiones o grupos no es un modelo justo**. Aprobar una herramienta de apoyo a decisiones sin validarla correctamente puede significar discriminar sin darse cuenta, o —peor— presentar resultados falsos frente a una contraloría.

Lo que aprenderás aquí:
- **Por qué la accuracy (exactitud) sola miente** cuando las clases están desbalanceadas.
- **Cómo detectar que tu modelo hace trampa** (fuga de datos / *data leakage*).
- **Cómo validar de verdad** con validación cruzada y no con un solo split.
- **Cómo auditar que el modelo sea justo** entre regiones (fairness).

**Conexión con el dataset real:** el dataset `compras_ml.csv` tiene órdenes de alimentos de ChileCompra. Los proveedores "Grandes" son minoría — exactamente la situación donde la accuracy engaña. Y hay compras en todas las regiones del país, lo que permite medir si el modelo trata igual a Arica que a Magallanes.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **Accuracy (exactitud)** | % de respuestas correctas en total | Tasa de resolución de solicitudes (puede ser alta y aun así ignorar las urgentes) |
| **Precision** | De los que el modelo dijo "Grande", ¿cuántos sí lo eran? | De las licitaciones que aprobé "sin irregularidades", ¿cuántas realmente eran correctas? |
| **Recall** | De todos los que realmente eran "Grande", ¿cuántos detecté? | De todos los casos irregulares reales, ¿cuántos alcancé a revisar? |
| **F1-score** | Promedio armonioso entre precision y recall | Índice que balancea no dejar pasar irregularidades Y no generar falsas alarmas |
| **Data leakage (fuga)** | Usar información que no tendrías al predecir en la realidad | Corregir un examen con el solucionario en la mano — los resultados parecen perfectos pero son mentira |
| **Validación cruzada** | Entrena y evalúa el modelo en múltiples subdivisiones del dato | Auditar un proceso en distintas épocas del año y promediar los resultados |
| **Calibración** | ¿Las probabilidades que entrega el modelo son creíbles? | Si el modelo dice "70% de chance de irregularidad", ¿realmente ocurre en ~70% de los casos? |
| **Fairness (equidad)** | Mide si el modelo rinde igual en distintos grupos (regiones, tipos) | Verificar que los servicios del Estado lleguen igual a todas las comunas |
| **Brier score** | Mide la calidad de las probabilidades predichas (0 = perfecto) | Error promedio en las estimaciones de riesgo de una unidad de auditoría |

---

## 4. Verificación de Prerrequisitos

Antes de empezar este módulo, responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Cargar un CSV con pandas y explorar sus columnas | ✅ Sí / 🔄 Revisar R2-00 |
| Separar datos en entrenamiento y prueba con `train_test_split` | ✅ Sí / 🔄 Revisar R2-04 |
| Entrenar una `LogisticRegression` básica de scikit-learn | ✅ Sí / 🔄 Revisar R2-04 |
| Usar `Pipeline` y `ColumnTransformer` para preprocesar | ✅ Sí / 🔄 Revisar R2-06 |
| Interpretar qué significa "clase desbalanceada" | ✅ Sí / 🔄 Revisar R2-06 |
| Explicar qué es la accuracy y cuándo falla | ✅ Sí / 🔄 Revisar R2-05 |

Si tienes más de dos "Revisar", dedica 30 minutos a repasar esos módulos antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección: Preparación de datos

🎯 **Objetivo:** cargar `compras_ml.csv`, definir el target (si el proveedor es "Grande") y construir el pipeline de preprocesamiento con variables numéricas y categóricas.

💡 **Concepto clave — el target desbalanceado:**
En este dataset, los proveedores "Grandes" son minoría. Es equivalente a una lista de contratos donde el 80% no tiene irregularidades: si tu modelo dice siempre "no Grande / sin irregularidad", ¡acertará el 80% de las veces sin hacer nada útil! La accuracy sola te haría creer que el modelo es bueno cuando en realidad no hace nada.

🔍 **Qué hace el código:**
- `y = (df["tamano_proveedor"] == "Grande").astype(int)` crea el target binario (1 = Grande, 0 = no Grande).
- `ColumnTransformer` con `OneHotEncoder` convierte las columnas de texto (`categoria`, `region_comprador`) en columnas numéricas que el modelo puede leer.
- `train_test_split(..., stratify=y)` divide los datos manteniendo la misma proporción de Grandes en train y test.

⚠️ **Error frecuente:** no usar `stratify=y`. Si las clases están desbalanceadas y no estratificas, puede que casi todos los "Grandes" queden en entrenamiento y el test quede casi vacío de esa clase, lo que hace imposible medir el desempeño real.

✅ **Señal de comprensión:** entiendes por qué el print dice "clase desbalanceada" y puedes explicarle a un colega qué significa en términos de compras públicas.

---

### 🔷 Sección 1: Métricas más allá de la accuracy

🎯 **Objetivo:** calcular las 4 métricas principales (accuracy, precision, recall, F1) y entender cuándo usar cada una.

💡 **Concepto clave — precision vs. recall, la eterna tensión:**
En una auditoría de contratos:
- **Precision alta** = cuando levanto una alerta, casi siempre es real (pocas falsas alarmas).
- **Recall alto** = detecto casi todos los casos irregulares (no se me escapa nada).

El problema: mejorar uno generalmente empeora el otro. El **F1** balancea ambos. En el sector público, debes decidir conscientemente: ¿es peor no detectar un proveedor grande (bajo recall) o alarmar a proveedores medianos innecesariamente (baja precision)?

🔍 **Qué hace el código:**
- Entrena un `Pipeline` con `LogisticRegression`.
- Predice sobre el test set con `modelo.predict(Xte)`.
- Calcula las 4 métricas usando `accuracy_score`, `precision_score`, `recall_score`, `f1_score` de `sklearn.metrics`.

⚠️ **Error frecuente:** olvidar `zero_division=0` en precision/recall/f1 cuando alguna clase no tiene predicciones. Scikit-learn lanza un warning molesto y puede interrumpir la ejecución.

✅ **Señal de comprensión:** puedes completar el diccionario `metricas` y explicar por qué el F1 es diferente del promedio simple de precision y recall (el F1 penaliza más cuando uno de los dos es muy bajo).

---

### 🔷 Sección 2: Fuga de datos (*data leakage*)

🎯 **Objetivo:** demostrar experimentalmente qué pasa cuando incluyes una variable "trampa" que contiene la respuesta.

💡 **Concepto clave — la variable `tamano_num` es trampa:**
En este dataset, `tamano_num` es un número que codifica el tamaño del proveedor (1=Micro, 2=Pequeño, 3=Mediano, 4=Grande). El target es si el proveedor es Grande. ¡Es básicamente la misma información! Incluirla en el modelo es como darle la respuesta al examen. El modelo aprende "si tamano_num es 4, es Grande" y acertará el 99%... pero ese 99% es completamente falso en la realidad, donde ese campo no estaría disponible al momento de predecir.

🔍 **Qué hace el código:**
- Crea una versión del dataset CON la variable trampa (`Xtr_f` con `tamano_num` agregada).
- Entrena un `DecisionTreeClassifier` con esa versión.
- Compara la accuracy CON fuga vs SIN fuga para demostrar el efecto.

⚠️ **Error frecuente:** confundir "el modelo es muy bueno" con "el modelo está haciendo trampa". Una accuracy >99% en un problema difícil casi siempre indica fuga de datos. En auditorías de modelos del Estado, esto es señal de alerta roja que debe revisarse antes de cualquier implementación.

✅ **Señal de comprensión:** `acc_con_fuga > 0.99` y `acc_sin_fuga < acc_con_fuga`. Puedes explicarle a tu jefatura por qué un modelo "casi perfecto" puede ser el menos confiable.

---

### 🔷 Sección 3: Validación cruzada

🎯 **Objetivo:** usar 5-fold cross-validation para obtener una estimación más robusta del desempeño real del modelo.

💡 **Concepto clave — un solo examen no define a un estudiante:**
Si evalúas tu modelo solo una vez con un split fijo, el resultado depende de qué datos cayeron en test por azar. Con validación cruzada, divides los datos en 5 partes, haces 5 evaluaciones distintas (cada vez una parte diferente es el test), y promedias. Es como hacer 5 auditorías en distintos períodos del año y reportar el promedio: más representativo, más justo, más defendible.

🔍 **Qué hace el código:**
- `cross_val_score(modelo, X, y, cv=5, scoring="f1")` devuelve un array de 5 valores F1.
- Cada valor corresponde a una "ronda" de evaluación con un subconjunto distinto como test.
- `scores.mean()` es el F1 promedio, más confiable que el de un solo split.

⚠️ **Error frecuente:** usar `cv=5` sobre el modelo ya entrenado con `fit`. El modelo de `cross_val_score` se re-entrena internamente en cada fold — no necesitas hacer `fit` antes, ni debes.

✅ **Señal de comprensión:** `len(scores) == 5` y puedes interpretar la varianza entre los scores: si hay mucha diferencia entre el mejor y el peor fold, el modelo es inestable con datos distintos.

---

### 🔷 Sección 4: Calibración

🎯 **Objetivo:** calcular el Brier score y entender si las probabilidades que entrega el modelo son confiables.

💡 **Concepto clave — "¿cuánto te puedo creer cuando dices 70%?":**
Un modelo no solo predice "Grande" o "no Grande": también entrega una probabilidad (por ejemplo, 0.73). La calibración evalúa si esa probabilidad es realista. Si el modelo dice "70% de probabilidad de ser Grande" para 100 casos, ¿realmente ~70 de esos 100 son Grandes? Si no, el modelo miente sobre su propia confianza. En decisiones de política pública (priorizar fiscalización, asignar recursos), una probabilidad mal calibrada puede llevar a errores sistemáticos.

🔍 **Qué hace el código:**
- `modelo.predict_proba(Xte)[:, 1]` extrae la probabilidad de la clase positiva (Grande).
- `brier_score_loss(yte, proba)` calcula el error cuadrático medio de las probabilidades (0 = perfecto, 1 = horrible).
- La curva de calibración grafica "probabilidad predicha" vs "fracción real observada" para visualizar el sesgo.

⚠️ **Error frecuente:** usar `predict_proba(Xte)` sin `[:, 1]`. Eso te da una matriz de 2 columnas (probabilidad de clase 0 y clase 1). Necesitas solo la columna 1, que corresponde a la clase positiva (Grande).

✅ **Señal de comprensión:** `0.0 <= brier <= 1.0`. Puedes mirar la curva y decir si el modelo sobreestima o subestima las probabilidades en distintos rangos.

---

### 🔷 Sección 5: Fairness por grupo

🎯 **Objetivo:** calcular el recall del modelo separado por región del comprador, y medir la disparidad entre la región con mejor y peor desempeño.

💡 **Concepto clave — el promedio esconde injusticia:**
Un modelo puede tener recall promedio de 0.75 y aun así tener recall 0.9 en la Región Metropolitana y 0.4 en la Región de Aysén. Si usas ese modelo para priorizar fiscalización, estás favoreciendo sistemáticamente a ciertas regiones. En el Estado chileno, donde la equidad territorial es un principio constitucional, este análisis es fundamental antes de implementar cualquier herramienta automatizada de apoyo a decisiones.

🔍 **Qué hace el código:**
- Itera por cada región única del test set.
- Calcula `recall_score` solo para las filas de esa región usando la máscara `m`.
- `disparidad = max(recall_por_region.values()) - min(recall_por_region.values())` cuantifica la brecha.
- El gráfico de barras horizontales muestra visualmente cuál región está mejor y peor servida.

⚠️ **Error frecuente:** no filtrar regiones con menos de 20 casos o sin positivos. El recall de una región con 3 casos es estadísticamente irrelevante y puede generar valores extremos que distorsionen el análisis de fairness.

✅ **Señal de comprensión:** `len(recall_por_region) >= 2` y `disparidad >= 0`. Puedes identificar cuál región tiene el recall más bajo y reflexionar sobre qué implicaría usar este modelo para priorizar recursos en esa región.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Calcula las 4 métricas

**Habilidad:** aplicar métricas de clasificación apropiadas para clases desbalanceadas.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* el diccionario `metricas` tiene 4 claves: `accuracy`, `precision`, `recall`, `f1`. Cada valor debe ser un número entre 0 y 1. Ya tienes `pred` disponible (las predicciones del modelo sobre `Xte`).
2. 🟠 *Pista 2 (técnica):* scikit-learn tiene funciones con nombres casi iguales a las claves: `accuracy_score(yte, pred)`, `precision_score(yte, pred, zero_division=0)`, `recall_score(yte, pred, zero_division=0)`, `f1_score(yte, pred, zero_division=0)`.
3. 🔴 *Pista 3 (estructura):* el diccionario se completa con una línea por clave: `"accuracy": accuracy_score(yte, pred)`, y análogamente para las otras tres. Todas las funciones reciben primero los valores reales (`yte`) y luego los predichos (`pred`).

**Lógica de solución:** se importan las cuatro funciones de `sklearn.metrics`, se aplican sobre `(yte, pred)` y se guarda cada resultado en la clave correspondiente del diccionario `metricas`.

---

### ✍️ Ejercicio 2 — Compara accuracy CON fuga vs SIN fuga

**Habilidad:** detectar data leakage comparando el desempeño con y sin variable trampa.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* ya tienes `m_fuga` (modelo entrenado CON fuga) y `modelo` (entrenado SIN fuga). Solo necesitas calcular la accuracy de cada uno sobre sus respectivos test sets.
2. 🟠 *Pista 2 (técnica):* para el modelo con fuga, el test set es `Xte_f` (que tiene la columna trampa). Para el modelo sin fuga, es `Xte` (sin esa columna). Usa `accuracy_score` en ambos casos.
3. 🔴 *Pista 3 (estructura):* `acc_con_fuga = accuracy_score(yte, m_fuga.predict(Xte_f))` y `acc_sin_fuga = accuracy_score(yte, modelo.predict(Xte))`.

**Lógica de solución:** la clave es usar el test set correcto para cada modelo. El modelo con fuga dará >0.99 de accuracy porque prácticamente "conoce" la respuesta a través de `tamano_num`. El modelo limpio rendirá bastante menos — ese resultado más bajo es el resultado honesto.

---

### ✍️ Ejercicio 3 — 5-fold cross-validation

**Habilidad:** usar validación cruzada para una estimación más confiable del F1.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* `cross_val_score` entrena y evalúa el modelo automáticamente en 5 subdivisiones. Solo le pasas el modelo, los datos completos (`X`, `y`) y la métrica que quieres medir.
2. 🟠 *Pista 2 (técnica):* los parámetros son: `cross_val_score(modelo, X, y, cv=5, scoring="f1")`. El resultado es un array de 5 números, uno por fold.
3. 🔴 *Pista 3 (estructura):* `scores = cross_val_score(modelo, X, y, cv=5, scoring="f1")`. Para el promedio: `scores.mean()`. Ambas variables deben quedar definidas.

**Lógica de solución:** `cross_val_score` maneja internamente el split, el entrenamiento y la evaluación en cada fold. El array resultante tiene exactamente 5 valores (uno por fold). El promedio es la estimación robusta del F1 real.

---

### ✍️ Ejercicio 4 — Brier score de las probabilidades

**Habilidad:** obtener las probabilidades predichas y evaluarlas con Brier score.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* el modelo entrenado puede entregar probabilidades además de predicciones. La función se llama `predict_proba` (no `predict`).
2. 🟠 *Pista 2 (técnica):* `modelo.predict_proba(Xte)` devuelve una matriz de 2 columnas: columna 0 es P(no Grande) y columna 1 es P(Grande). Necesitas solo la columna 1, que corresponde a la clase positiva.
3. 🔴 *Pista 3 (estructura):* `proba = modelo.predict_proba(Xte)[:, 1]` y luego `brier = brier_score_loss(yte, proba)`. Ambas variables deben quedar definidas.

**Lógica de solución:** extraes la probabilidad de la clase positiva con `[:, 1]`, luego pasas esas probabilidades junto con los labels reales a `brier_score_loss`. Un valor cercano a 0 indica buena calibración.

---

### ✍️ Ejercicio 5 — Recall por región y disparidad

**Habilidad:** calcular una métrica de fairness comparando el desempeño por subgrupos geográficos.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* el loop ya está estructurado por regiones. Para cada región `r`, tienes una máscara booleana `m` que filtra solo los casos de esa región en el test set.
2. 🟠 *Pista 2 (técnica):* dentro del loop, `recall_score(yte[m], pred[m], zero_division=0)` calcula el recall solo para los casos de la región `r`. Guarda ese valor en el diccionario con `recall_por_region[r] = ...`.
3. 🔴 *Pista 3 (estructura):* `recall_por_region[r] = recall_score(yte[m], pred[m], zero_division=0)`. Para la disparidad después del loop: `disparidad = max(recall_por_region.values()) - min(recall_por_region.values())`.

**Lógica de solución:** filtras filas por región con la máscara booleana, calculas recall sobre ese subconjunto, y la disparidad es la diferencia entre el máximo y mínimo recall entre regiones. Un valor alto de disparidad es señal de inequidad territorial del modelo.

---

## 7. Profundización: Fairness como política pública

El Ejercicio 5 no es solo técnico — es una pregunta de ética y política pública que deberías poder responder ante una autoridad.

**¿Por qué el recall varía por región?**

Hay varias razones posibles:
- **Tamaño de muestra:** las regiones con pocas órdenes de compra tienen estimaciones menos estables. La Región Metropolitana tiene muchas más transacciones que Aysén o Magallanes.
- **Distribución de proveedores:** en algunas regiones predominan proveedores locales medianos; en otras (especialmente RM), los grandes tienen más presencia. El modelo aprende esos patrones y puede generalizarlos mal a regiones con distribuciones distintas.
- **Patrones de compra distintos:** el comportamiento de compra en categorías de alimentos puede diferir por región (tipos de producto, estacionalidad, proveedores locales disponibles).

**¿Qué implicaría usar este modelo en producción?**

Imagina que DIPRES o ChileCompra decide usar este modelo para priorizar fiscalizaciones: revisar primero las licitaciones donde el modelo predice "proveedor grande" con alta confianza. Si el modelo tiene recall 0.9 en RM y 0.4 en la Región de Atacama, estaría **subdetectando sistemáticamente** la concentración de mercado en las regiones del norte. La política pública derivada sería injusta: se fiscalizaría menos donde el modelo falla, perpetuando una brecha.

**Estándar de fairness recomendado para el Estado chileno:**

La diferencia de recall entre el grupo más favorecido y el menos favorecido (disparidad) debería ser menor a 0.10 para una herramienta de apoyo a decisiones públicas. Si supera ese umbral, se recomienda:
1. Reentrenar con datos estratificados por región para balancear la representación.
2. Usar umbrales de clasificación distintos por región (ajuste post-hoc).
3. Incluir la región como variable de preprocesamiento explícita con más peso.
4. Documentar la limitación en la model card del sistema antes de cualquier despliegue.

---

## 8. Conexión con `profundiza.ipynb`

| Tema | En `leccion.ipynb` | En `profundiza.ipynb` |
|---|---|---|
| Curva ROC / AUC | No cubierto | ✅ Construye la curva ROC y calcula el AUC como métrica alternativa al F1 |
| Umbral de clasificación | No cubierto | ✅ Explora cómo cambiar el umbral (default 0.5) afecta precision/recall |
| Calibración avanzada | Brier score básico + curva | ✅ `CalibratedClassifierCV` para recalibrar el modelo automáticamente |
| Validación cruzada estratificada | `cross_val_score` simple | ✅ `StratifiedKFold` para preservar la proporción de clases en cada fold |

**¿Cuándo ir al `profundiza`?**

Ve a `profundiza.ipynb` si:
- Necesitas presentar resultados en un informe formal (la curva ROC es el estándar en la literatura académica y técnica).
- Tu jefatura pregunta "¿puedes ajustar el sistema para alarmar menos falsos positivos?" (ajuste de umbral).
- El modelo será usado para tomar decisiones con consecuencias significativas para personas (calibración crítica).

Quédate en `leccion.ipynb` si:
- Estás aprendiendo los conceptos base por primera vez.
- Solo necesitas comunicar un resultado general de desempeño a un equipo no técnico.

---

## 9. Autoevaluación Final

**Pregunta 1:** Tienes un dataset con 90% de casos "No irregularidad" y 10% "Irregularidad". Entrenas un modelo que predice siempre "No irregularidad". ¿Cuál será su accuracy?

- a) 10%
- b) 50%
- c) **90% ✅**
- d) 0%

**Explicación:** el modelo siempre acierta en el 90% de casos que son "No irregularidad", aunque sea completamente inútil para detectar irregularidades. Por eso la accuracy sola engaña con clases desbalanceadas — es la primera lección que debes llevarte de este módulo.

---

**Pregunta 2:** ¿Qué es la fuga de datos (*data leakage*)?

- a) Cuando los datos se borran accidentalmente
- b) **Cuando el modelo usa información que no estaría disponible al predecir casos nuevos ✅**
- c) Cuando hay valores faltantes en el dataset
- d) Cuando el dataset es demasiado pequeño

**Explicación:** la fuga ocurre cuando el modelo "espía" la respuesta a través de alguna variable que en la práctica no existiría al momento de predecir. Resultados casi perfectos (>99% accuracy) en problemas difíciles son la primera señal de sospecha.

---

**Pregunta 3:** Tienes un modelo con F1 = 0.78 medido en un solo split, y otro con F1 promedio = 0.74 medido con 5-fold cross-validation. ¿Cuál estimación confías más?

- a) El primero, porque 0.78 > 0.74
- b) **El segundo, porque la validación cruzada es más confiable ✅**
- c) Son equivalentes
- d) Ninguno, hay que probar con más datos

**Explicación:** la validación cruzada evalúa el modelo en 5 splits distintos y promedia. Es menos sensible a la "suerte" de cómo quedaron los datos en ese único split. El modelo con 0.74 promediado en 5 evaluaciones es más confiable que el de 0.78 en una sola evaluación.

---

**Pregunta 4:** El Brier score de tu modelo es 0.02. ¿Qué significa?

- a) El modelo tiene 2% de accuracy
- b) **Las probabilidades predichas son casi perfectas ✅**
- c) El modelo falla en el 2% de los casos
- d) El modelo tiene muy baja precision

**Explicación:** el Brier score mide el error cuadrático de las probabilidades (0 = perfecto, 1 = pésimo). Un valor de 0.02 indica que las probabilidades están muy bien calibradas — si el modelo dice 70%, ocurre cerca del 70% de las veces en la práctica.

---

**Pregunta 5:** Tu modelo tiene recall 0.88 en la RM y 0.41 en la Región de Aysén. ¿Cuál es la acción más apropiada?

- a) Publicar el modelo, el promedio nacional es bueno
- b) Descartar completamente el modelo
- c) **Documentar la disparidad, no usarlo para decisiones automáticas en Aysén, y buscar mejoras ✅**
- d) Aumentar los datos de la RM

**Explicación:** la disparidad de ~0.47 es grande. Un modelo con esa diferencia no debería usarse para tomar decisiones automáticas en la región peor servida. Pero tampoco se descarta: se documenta, se comunica la limitación a las autoridades, y se trabaja en mitigarla (más datos de Aysén, umbral diferenciado, variables adicionales).

---

## 10. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Accuracy** | % de predicciones correctas sobre el total | Tasa de respuestas correctas en un test de conocimiento |
| **Precision** | De lo que etiquetaste positivo, ¿qué fracción era realmente positivo? | De las alertas que generaste, ¿cuántas eran falsas alarmas? |
| **Recall** | De todos los positivos reales, ¿qué fracción detectaste? | De todos los contratos irregulares existentes, ¿cuántos encontraste? |
| **F1-score** | Promedio armonioso entre precision y recall | Índice compuesto de efectividad de detección (como un índice de gestión) |
| **Data leakage** | Usar información "trampa" que no estaría disponible en producción | Corregir un informe con información del futuro que aún no existe |
| **Validación cruzada** | Evaluar el modelo en múltiples subdivisiones del dataset | Hacer varias auditorías parciales en distintos períodos y promediar |
| **Fold** | Una de las subdivisiones en la validación cruzada | Un período o región específica en una auditoría rotativa |
| **Calibración** | Confiabilidad de las probabilidades del modelo | Si predigo "70% de riesgo", ¿ocurre en ~70% de los casos reales? |
| **Brier score** | Error cuadrático de las probabilidades (0=perfecto, 1=pésimo) | Error promedio en estimaciones de riesgo de la unidad de control |
| **Fairness** | Equidad del modelo entre distintos grupos | ¿El servicio llega igual a todas las comunas y regiones del país? |
| **Disparidad** | Diferencia entre el mejor y peor recall entre grupos | Brecha de cobertura entre la región mejor y peor atendida por el modelo |
| **Clase desbalanceada** | Cuando una categoría es mucho más frecuente que la otra | Lista donde el 95% son casos normales y solo 5% son irregulares |

---

## 11. Conexión con el Módulo Siguiente

**Módulo siguiente:** R2-08 · Pipelines reproducibles

En este módulo aprendiste a **evaluar bien** un modelo: métricas honestas, sin fuga, con validación cruzada y auditado por fairness.

El problema que surge después es: ¿cómo hago para que ese proceso (limpiar, preprocesar, entrenar, predecir) sea **reproducible y seguro**? ¿Qué pasa cuando llegan datos nuevos? ¿Cómo me aseguro de que el escalado que apliqué en entrenamiento se aplique exactamente igual en producción?

**R2-08 responde esas preguntas** con los **Pipelines de scikit-learn**: una forma de encadenar todos los pasos (transformación, modelo) en un solo objeto que se comporta como una "receta plastificada" — siempre aplica los pasos en el orden correcto, sin filtraciones, y se puede guardar en disco para reusar.

**Preconcepto clave para llevar:** la fuga de datos que detectaste en el Ejercicio 2 de este módulo es exactamente el tipo de error que los Pipelines previenen automáticamente. En R2-08 entenderás el mecanismo que lo hace posible: el pipeline aplica el escalado usando *solo* los parámetros aprendidos del conjunto de entrenamiento, nunca del test.

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos de Chile · Formación Pública*
*Contenido bajo licencia CC BY 4.0*
