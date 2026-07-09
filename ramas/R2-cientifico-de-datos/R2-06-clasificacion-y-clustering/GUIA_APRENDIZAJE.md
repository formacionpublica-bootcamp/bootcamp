# 📘 Guía de Aprendizaje — R2-06 · Clasificación y clustering

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-06 · Clasificación y clustering |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 3–4 horas |
| **Semana** | Semana 12 |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-04 (fundamentos de ML y regresión) y R2-05 (árboles de decisión) |
| **Competencia de salida** | Entrenar y evaluar un clasificador (exactitud y matriz de confusión) y aplicar clustering con K-Means (incluido el escalado), distinguiendo cuándo un problema es supervisado y cuándo no |
| **Dataset** | `compras_ml.csv` — 7.412 órdenes de compra de alimentos de MercadoPúblico / ChileCompra |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Hasta ahora, en R2-04 y R2-05, tus modelos predecían **números**: el monto de una compra, la duración de un proceso. Pero en el trabajo del Estado, muchas decisiones no son numéricas sino de **categoría**: ¿este trámite es prioritario u ordinario? ¿Esta licitación es de riesgo alto, medio o bajo? ¿Este proveedor es micro, pequeño, mediano o grande?

Este módulo te da dos herramientas nuevas para eso:

- **Clasificación (supervisada):** con datos históricos donde ya conoces la categoría correcta, entrenas un modelo que la predice para casos nuevos. Aquí lo harás con órdenes de compra reales: a partir de la **cantidad de artículos** y el **monto total**, el modelo deduce el **tamaño del proveedor**.
- **Clustering (no supervisado):** cuando **no tienes etiquetas** — nadie ha clasificado nada — el algoritmo descubre grupos por sí solo. Es como recibir miles de expedientes sin clasificar y separarlos en pilas de "parecidos entre sí".

**Conexión con el dataset real:** `compras_ml.csv` contiene 7.412 compras públicas de alimentos de ChileCompra, con la cantidad comprada, el monto total (mediana de $25.000, pero con órdenes que superan los $4,9 millones) y el tamaño del proveedor adjudicado. ¿Qué decisiones permite? Detectar perfiles de compra (¿cuáles son las compras "gigantes" que merecen más revisión?), entender qué tipo de proveedor gana qué tipo de orden, y sentar las bases para políticas de fomento a las empresas de menor tamaño en compras públicas — un objetivo explícito de ChileCompra.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en Excel / sector público |
|---|---|---|
| **Clasificación** | Predice una categoría (texto), no un número | Decidir si un trámite es "Prioritario" u "Ordinario" según reglas aprendidas de casos anteriores |
| **Aprendizaje supervisado** | Aprende de ejemplos con respuesta conocida | Capacitar a un funcionario nuevo mostrándole expedientes ya resueltos con su resolución |
| **Aprendizaje no supervisado** | Encuentra estructura sin respuestas conocidas | Ordenar un archivador heredado sin ninguna pauta: agrupas lo que se parece |
| **`DecisionTreeClassifier`** | Árbol de decisión que predice categorías | El mismo diagrama de flujo de R2-05, pero terminando en una etiqueta, no en un número |
| **Exactitud (*accuracy*)** | % de casos bien clasificados | Tasa de aciertos de una revisión: de 100 expedientes, ¿cuántos clasifiqué bien? |
| **Matriz de confusión** | Tabla real vs. predicho: muestra *en qué* se equivoca | Planilla que cruza "lo que dijo el revisor" con "lo que era en verdad" |
| **`stratify=y`** | Mantiene la proporción de clases al dividir train/test | Muestra representativa: si el 80% de las órdenes son de proveedores Pequeños, el test también debe tenerlo |
| **Clustering / K-Means** | Agrupa registros parecidos en *k* grupos | Separar miles de expedientes en 3 pilas por volumen y costo, sin pauta previa |
| **`StandardScaler`** | Lleva las variables a la misma escala (media 0, desv. 1) | Convertir pesos y unidades a un "índice común" para poder compararlos con justicia |
| **`pd.crosstab`** | Tabla cruzada de frecuencias entre dos variables | Una tabla dinámica de Excel que cruza dos columnas y cuenta |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Responde honestamente antes de abrir el notebook:

| ¿Puedo...? | Estado |
|---|---|
| Cargar un CSV con pandas y seleccionar columnas con `df[["a", "b"]]` | ✅ Sí / 🔄 Revisar R1-02 |
| Explicar la diferencia entre entrenamiento y prueba, y usar `train_test_split` | ✅ Sí / 🔄 Revisar R2-04 |
| Entrenar un modelo de scikit-learn con `.fit()` y predecir con `.predict()` | ✅ Sí / 🔄 Revisar R2-04 |
| Explicar cómo decide un árbol de decisión (preguntas encadenadas) | ✅ Sí / 🔄 Revisar R2-05 |
| Leer una tabla de frecuencias (`value_counts`) e interpretar proporciones | ✅ Sí / 🔄 Revisar R1-02 |

Si marcaste más de dos "Revisar", dedica 30 minutos a repasar esos módulos antes de continuar. Este módulo reutiliza el flujo `fit`/`predict` completo: si ese flujo te resulta natural, lo nuevo se aprende rápido.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección: Dos preguntas, dos tipos de aprendizaje + preparación del entorno

🎯 **Objetivo:** entender la diferencia entre aprendizaje supervisado y no supervisado, y cargar el dataset.

💡 **Concepto clave — ¿tengo o no tengo la respuesta correcta?**
Toda la diferencia entre los dos mundos de este módulo es una sola pregunta: ¿existen etiquetas conocidas para aprender? Si tienes compras con su tamaño de proveedor conocido, es **supervisado** (clasificación). Si solo tienes las compras y quieres descubrir perfiles, es **no supervisado** (clustering). Es la diferencia entre capacitar con expedientes ya resueltos y ordenar un archivador sin pauta.

🔍 **Qué hace el código:**
- Si `compras_ml.csv` no existe localmente (por ejemplo en Colab), intenta descargarlo desde GitHub como respaldo.
- `pd.read_csv("compras_ml.csv")` carga las 7.412 compras.
- `df["tamano_proveedor"].value_counts()` muestra la distribución de clases: Pequeña 5.976, Mediana 1.137, Grande 178, Micro 121. Fíjate bien en esos números: ¡el 80,6% de las órdenes las gana un proveedor Pequeño!

⚠️ **Error frecuente:** saltarse la celda de preparación e ir directo a los ejercicios. Sin esa celda, `df` no existe y todo lo demás falla con `NameError`.

✅ **Señal de comprensión:** puedes explicarle a un colega por qué predecir el tamaño del proveedor es supervisado y agrupar compras por perfil es no supervisado.

---

### 🔷 Sección 1: Clasificación — predecir una categoría

🎯 **Objetivo:** preparar los datos (Ejercicio 1) y entrenar un `DecisionTreeClassifier` midiendo su exactitud (Ejercicio 2).

💡 **Concepto clave — es el mismo flujo, con `y` de texto:**
La clasificación no es un mundo nuevo: es el mismo `fit`/`predict` de R2-04 y el mismo árbol de R2-05, pero ahora `y` es una **categoría** ("Micro", "Pequeña", "Mediana", "Grande") en vez de un número. Como las clases están muy desbalanceadas (80,6% Pequeña vs 1,6% Micro), el `stratify=y` en la división es crucial: garantiza que entrenamiento y prueba conserven la misma proporción de cada clase. Sin eso, podría tocarte un test casi sin proveedores Grandes y la evaluación sería una lotería.

🔍 **Qué hace el código:**
- `X = df[["cantidad", "monto_total"]]` define las dos features; `y = df["tamano_proveedor"]` el objetivo.
- `train_test_split(..., test_size=0.3, random_state=42, stratify=y)` divide en 5.188 compras de entrenamiento y 2.224 de prueba.
- `DecisionTreeClassifier(max_depth=3, random_state=42)` crea un árbol clasificador poco profundo (3 niveles de preguntas) para que sea interpretable.
- `accuracy_score(y_test, y_pred)` calcula el porcentaje de aciertos: ≈ 0,81 (81% de las 2.224 compras de prueba bien clasificadas).

⚠️ **Error frecuente:** olvidar el `stratify=y` u ordenar mal los cuatro resultados de `train_test_split` (el orden es `X_train, X_test, y_train, y_test` — mezclar `y_train` con `X_test` es un clásico).

✅ **Señal de comprensión:** entiendes por qué una exactitud de 0,81 aquí es *menos impresionante* de lo que parece: un modelo tonto que dijera siempre "Pequeña" ya acertaría el 80,6% de las veces. Este matiz es la puerta de entrada a R2-07.

---

### 🔷 Sección: La matriz de confusión (celda ilustrativa)

🎯 **Objetivo:** ver *en qué* se equivoca el modelo, no solo *cuánto*.

💡 **Concepto clave — el tipo de error importa más que la cantidad:**
En el Estado, no es lo mismo confundir "riesgo bajo" con "riesgo medio" que con "riesgo alto". La matriz de confusión cruza la categoría **real** (filas) con la **predicha** (columnas): los aciertos quedan en la diagonal y los errores fuera de ella. Un vistazo te dice, por ejemplo, si el modelo confunde sistemáticamente a los proveedores Micro con Pequeños.

🔍 **Qué hace el código:**
- `confusion_matrix(yi_te, y_pred_te, labels=[...])` construye la tabla con las clases en el orden Micro → Pequeña → Mediana → Grande.
- `sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")` la pinta como mapa de calor con los conteos visibles.

⚠️ **Error frecuente:** leer la matriz al revés. Recuerda la convención del gráfico: **filas = real, columnas = predicho**. La celda (fila Mediana, columna Pequeña) son proveedores Medianos que el modelo etiquetó como Pequeños.

✅ **Señal de comprensión:** mirando el heatmap puedes decir cuál clase concentra los errores y por qué las clases minoritarias (Micro, Grande) son las más difíciles de acertar.

---

### 🔷 Sección 2: Clustering — descubrir grupos sin etiquetas

🎯 **Objetivo:** escalar las variables y agrupar las 7.412 compras en 3 clusters con K-Means (Ejercicio 3), visualizándolos después.

💡 **Concepto clave — escalar antes de agrupar no es opcional:**
K-Means agrupa por **distancia** entre puntos. Pero `cantidad` se mueve entre 0 y 492 artículos, mientras `monto_total` va desde $100 hasta $4.947.600. Sin escalar, el monto aplastaría por completo a la cantidad: sería como comparar expedientes midiendo uno en hojas y otro en toneladas. `StandardScaler` lleva ambas variables a la misma escala (media 0, desviación 1) para que las dos opinen por igual.

🔍 **Qué hace el código:**
- `StandardScaler().fit_transform(X_compras)` produce la versión escalada de cantidad y monto.
- `KMeans(n_clusters=3, random_state=42, n_init=10)` pide 3 grupos; `n_init=10` prueba 10 puntos de partida distintos y se queda con el mejor (K-Means es sensible al azar inicial).
- `km.fit_predict(X_escalado)` entrena y devuelve la etiqueta de cluster (0, 1 o 2) de cada compra, que se guarda en `df["cluster"]`.
- La celda ilustrativa siguiente dibuja el scatter cantidad vs monto coloreado por cluster: verás un grupo masivo de compras chicas y grupos pequeños de compras grandes o voluminosas.

⚠️ **Error frecuente:** pasarle a K-Means los datos **sin escalar** (`X_compras` en vez de `X_escalado`). El chequeo puede incluso dar ✅ (hay 3 clusters igual), pero los grupos estarían dominados solo por el monto y la interpretación sería engañosa. Escalar primero es el hábito que te llevas de este módulo.

✅ **Señal de comprensión:** puedes explicar por qué el número 3 lo elegiste **tú** y no el algoritmo, y qué pasaría con las distancias si no escalaras.

---

### 🔷 Sección: ¿Coinciden grupos y tamaños de proveedor? (Ejercicio 4)

🎯 **Objetivo:** comparar los clusters descubiertos con la etiqueta real usando una tabla cruzada.

💡 **Concepto clave — los clusters no son "la verdad":**
K-Means nunca vio el tamaño del proveedor; agrupó solo por cantidad y monto. Al cruzar cluster contra tamaño real descubres algo valioso: **no calzan perfectamente**. En la ejecución de referencia, un cluster gigante concentra la enorme mayoría de las compras (cerca de 6.900 de las 7.412) mezclando proveedores de todos los tamaños, mientras dos clusters pequeños capturan las compras de montos o volúmenes atípicos. Lección didáctica: los clusters describen **perfiles de compra**, no categorías administrativas. Que no coincidan no es un fracaso — es información.

🔍 **Qué hace el código:**
- `pd.crosstab(df["tamano_proveedor"], df["cluster"])` cuenta cuántas compras de cada tamaño cayeron en cada cluster (la suma total debe dar 7.412).

⚠️ **Error frecuente:** interpretar el número del cluster (0, 1, 2) como un ranking. Las etiquetas de K-Means son arbitrarias: el cluster 2 no es "mejor" ni "más grande" que el 0; incluso pueden cambiar de número si re-ejecutas con otra semilla o versión de scikit-learn.

✅ **Señal de comprensión:** puedes explicar con la tabla en la mano por qué "el algoritmo agrupó parecido pero no igual" y qué perfil de compra representa cada cluster.

---

## 6. Guía de los Ejercicios

### ✍️ Ejercicio 1 — Preparar la clasificación

**Objetivo:** definir `X`, `y` y dividir con estratificación.
**Habilidad que entrena:** preparar datos para clasificación con clases desbalanceadas.

**Pistas progresivas:**
1. 🟢 *Pista suave:* `X` e `y` ya vienen definidos en la celda. Solo falta reemplazar la línea PLACEHOLDER por una llamada real a `train_test_split`, que ya usaste en R2-04. La novedad es un parámetro extra que preserva las proporciones de clase.
2. 🟡 *Pista media:* la función recibe `X`, `y` y tres parámetros con nombre: `test_size=0.3`, `random_state=42` y `stratify=y`. Devuelve **cuatro** cosas, en el orden: primero los dos X (train, test), luego los dos y (train, test).
3. 🔴 *Pista directa:* la línea tiene la forma `X_train, X_test, y_train, y_test = train_test_split(...)` con los cinco argumentos mencionados adentro, en ese orden: `X`, `y` y los tres parámetros con nombre.

**Lógica de la solución (en prosa):** se reemplaza el placeholder por la división real: 70% para entrenar, 30% para probar, con semilla fija para reproducibilidad y estratificando por `y` para que ambas partes tengan la misma proporción de Micro/Pequeña/Mediana/Grande.

**Qué valida el chequeo ✅:** que `X_train` tenga exactamente las columnas `cantidad` y `monto_total`, que la división produzca 5.188 filas de entrenamiento y 2.224 de prueba, y que `y_train` contenga las cuatro clases.

---

### ✍️ Ejercicio 2 — Entrenar y medir la exactitud

**Objetivo:** entrenar el `DecisionTreeClassifier` y calcular la accuracy en prueba.
**Habilidad que entrena:** el ciclo completo `fit` → `predict` → métrica en clasificación.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son tres pasos que ya conoces de la regresión: entrenar con los datos de entrenamiento, predecir sobre los de prueba, y comparar predicción contra realidad con una función de `sklearn.metrics` que ya está importada.
2. 🟡 *Pista media:* el `clasificador` ya está creado; entrénalo con `.fit(X_train, y_train)`. Luego genera `y_pred` con `.predict(X_test)`. La exactitud compara `y_test` (lo real) con `y_pred` (lo predicho).
3. 🔴 *Pista directa:* tres líneas: el `.fit(...)` sobre el clasificador, un `y_pred = clasificador.predict(X_test)`, y `exactitud = accuracy_score(y_test, y_pred)`. Recuerda que las funciones de métricas reciben primero los valores reales y después los predichos.

**Lógica de la solución (en prosa):** se entrena el árbol con el 70% de entrenamiento, se predice el tamaño del proveedor para las 2.224 compras de prueba, y se calcula qué fracción quedó bien clasificada. El resultado esperado es ≈ 0,81 (81% de aciertos).

**Qué valida el chequeo ✅:** que el clasificador esté efectivamente entrenado (tiene atributo `tree_`) y que tu `exactitud` coincida (±0,01) con la de un árbol de referencia idéntico.

---

### ✍️ Ejercicio 3 — Agrupar las compras con K-Means

**Objetivo:** escalar las features y asignar cada compra a uno de 3 clusters.
**Habilidad que entrena:** el flujo estándar de clustering: escalar → agrupar → guardar etiquetas.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son dos pasos y el enunciado de la celda te los deja casi listos en el comentario TODO: primero transformar los datos a una escala común, después pedirle a K-Means que forme los grupos y guardarlos como columna nueva.
2. 🟡 *Pista media:* el escalado es una sola línea: crear un `StandardScaler()` y aplicar `fit_transform` sobre `X_compras`. Para agrupar, crea el `KMeans` con los tres parámetros que indica el enunciado (`n_clusters=3`, `random_state=42`, `n_init=10`) y usa su método que entrena y devuelve etiquetas en un solo paso.
3. 🔴 *Pista directa:* dos líneas de trabajo: `X_escalado = StandardScaler().fit_transform(X_compras)` y luego crear `km = KMeans(...)` para asignar `df["cluster"] = km.fit_predict(X_escalado)`. El error típico es pasarle `X_compras` (sin escalar) al `fit_predict`.

**Lógica de la solución (en prosa):** se estandarizan cantidad y monto para que pesen lo mismo en las distancias, se ejecuta K-Means con 3 grupos y semilla fija, y la etiqueta resultante de cada compra (0, 1 o 2) se guarda como columna `cluster` del DataFrame.

**Qué valida el chequeo ✅:** que exista la columna `cluster`, que tenga una etiqueta para cada una de las 7.412 compras, y que haya exactamente 3 valores de cluster distintos.

---

### ✍️ Ejercicio 4 — ¿Coinciden grupos y tamaños de proveedor?

**Objetivo:** cruzar la etiqueta real (`tamano_proveedor`) contra el cluster descubierto.
**Habilidad que entrena:** evaluar cualitativamente un clustering comparándolo con una variable conocida.

**Pistas progresivas:**
1. 🟢 *Pista suave:* es una sola línea con una función de pandas que ya usaste en la rama R1: la que arma una tabla de frecuencias cruzando dos columnas (la versión pandas de una tabla dinámica de Excel).
2. 🟡 *Pista media:* `pd.crosstab` recibe dos argumentos: primero la serie que irá en las **filas** (el tamaño real) y luego la que irá en las **columnas** (el cluster). El enunciado te da el llamado casi textual.
3. 🔴 *Pista directa:* `tabla = pd.crosstab(...)` pasando `df["tamano_proveedor"]` como primer argumento y `df["cluster"]` como segundo. El `print(tabla)` ya está en la celda.

**Lógica de la solución (en prosa):** la tabla cruzada cuenta cuántas compras de cada tamaño de proveedor cayeron en cada cluster. Al leerla verás que un cluster concentra la gran mayoría de las compras de todos los tamaños y que los otros dos capturan perfiles atípicos — es decir, los grupos descubiertos **no replican** la clasificación administrativa, y eso es justamente lo que hay que interpretar.

**Qué valida el chequeo ✅:** que `tabla` exista, que sus celdas sumen las 7.412 compras, y que las filas sean los cuatro tamaños de proveedor.

---

## 7. Sección Especial: El Ejercicio de Política Pública

El Ejercicio 4 es el corazón de política pública del módulo: comparaste una **categoría administrativa** (el tamaño del proveedor según su registro) con los **perfiles de compra reales** que descubrió el algoritmo. Y no coinciden.

**Reflexión guiada:**
- El 80,6% de las órdenes de compra de alimentos las adjudican proveedores Pequeños, y solo el 2,4% proveedores Grandes. Sin embargo, el clustering muestra que el comportamiento de compra (cantidad y monto) no distingue nítidamente los tamaños: hay proveedores Pequeños con compras enormes y Medianos con compras mínimas.
- Si una política de fomento a las EMT (empresas de menor tamaño) usa **solo la categoría administrativa** para focalizar, podría estar tratando igual a realidades muy distintas. Los clusters sugieren que el "perfil de compra" es otra dimensión relevante.
- Al revés: si usaras solo los clusters para fiscalizar (por ejemplo, revisar el cluster de compras de montos altos), estarías mirando el perfil de la orden, no del proveedor. Ninguna de las dos miradas basta sola.

**Pregunta de debate abierta:**
> Si ChileCompra quisiera priorizar la fiscalización de órdenes de compra "atípicas", ¿deberían usar los clusters de K-Means, la categoría de tamaño del proveedor, o una combinación? ¿Qué riesgos de injusticia tendría automatizar esa decisión con lo que sabes hasta ahora?

**Datos que complementarían el análisis:**
- Historial de adjudicaciones por proveedor (¿concentración de mercado en pocas manos?).
- Región del comprador (el dataset la trae: 15 regiones) para detectar diferencias territoriales de precios.
- Rubro específico y precios unitarios de referencia, para saber si un monto alto es "caro" o simplemente "grande".
- Fechas de las órdenes, para descubrir estacionalidad (por ejemplo, compras de alimentos de JUNAEB en año escolar).

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la diferencia esencial entre clasificación y clustering?

- a) La clasificación usa árboles y el clustering usa regresión
- b) **La clasificación aprende de etiquetas conocidas; el clustering descubre grupos sin etiquetas ✅**
- c) La clasificación es para números y el clustering para texto
- d) No hay diferencia, son sinónimos

**Explicación:** es la distinción supervisado vs. no supervisado. En clasificación existe una respuesta correcta (`y`) con la que aprender; en clustering el algoritmo agrupa por similitud sin que nadie le diga qué buscar. Los algoritmos concretos (árbol, K-Means) son secundarios frente a esta diferencia.

---

**Pregunta 2:** En este dataset, el 80,6% de las compras son de proveedores "Pequeña". Tu clasificador logra 81% de exactitud. ¿Qué deberías concluir?

- a) El modelo es excelente, 81% es una nota alta
- b) El modelo está sobreajustado
- c) **La exactitud apenas supera a un modelo que dijera siempre "Pequeña"; hay que mirar la matriz de confusión ✅**
- d) Hay fuga de datos

**Explicación:** con clases desbalanceadas, la exactitud tiene un "piso" alto: predecir siempre la clase mayoritaria ya da ~80,6%. Un 81% aporta poco por sí solo; la matriz de confusión revela si el modelo realmente distingue las clases minoritarias (Micro, Grande) o si vive de la mayoritaria.

---

**Pregunta 3:** ¿Para qué sirve `stratify=y` en `train_test_split`?

- a) Para que el split sea más rápido
- b) Para ordenar los datos alfabéticamente
- c) Para eliminar las clases minoritarias
- d) **Para que entrenamiento y prueba conserven la misma proporción de cada clase ✅**

**Explicación:** sin estratificar, el azar podría dejar el conjunto de prueba casi sin proveedores Grandes (solo hay 178 en total). Estratificar garantiza que ambas particiones sean representativas de la distribución original, haciendo la evaluación justa y estable.

---

**Pregunta 4:** ¿Por qué es necesario usar `StandardScaler` antes de K-Means en este módulo?

- a) Porque K-Means no acepta números decimales
- b) **Porque el monto (hasta $4,9 millones) aplastaría a la cantidad (hasta 492) en el cálculo de distancias ✅**
- c) Porque scikit-learn lo exige y lanza error si no
- d) Para eliminar los valores atípicos del dataset

**Explicación:** K-Means agrupa por distancia. Si una variable se mide en millones y otra en unidades, la primera domina totalmente la distancia y los clusters ignoran a la segunda. El escalado pone ambas en igualdad de condiciones (media 0, desviación 1). Scikit-learn no lanza error: el resultado simplemente sería engañoso, que es peor.

---

**Pregunta 5:** La tabla cruzada muestra que los clusters de K-Means no coinciden con los tamaños de proveedor. ¿Qué significa?

- a) El ejercicio quedó malo y hay que repetirlo
- b) K-Means necesita más clusters para que coincidan
- c) El dataset tiene errores
- d) **Los clusters describen perfiles de compra (cantidad/monto), que son una dimensión distinta a la categoría administrativa ✅**

**Explicación:** K-Means nunca vio la etiqueta: agrupó solo por comportamiento numérico. Que los grupos no calcen con la clasificación administrativa es información valiosa, no un error: dice que el tamaño legal del proveedor no determina el perfil de sus órdenes de compra. Forzar la coincidencia subiendo *k* tampoco tendría sentido conceptual.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en Excel / administración pública |
|---|---|---|
| **Clasificación** | Predecir una categoría (etiqueta discreta) a partir de features | Asignar "Prioritario/Ordinario" a un trámite según sus características |
| **Aprendizaje supervisado** | Entrenar con ejemplos que traen la respuesta correcta | Aprender revisando expedientes ya resueltos, con su resolución a la vista |
| **Aprendizaje no supervisado** | Modelar datos sin respuestas conocidas | Ordenar un archivador heredado sin pauta ni criterio previo |
| **`DecisionTreeClassifier`** | Árbol de decisión que termina en una etiqueta | Diagrama de flujo de decisiones que desemboca en una categoría |
| **Exactitud (*accuracy*)** | Porcentaje de casos bien clasificados sobre el total | Tasa de aciertos de una revisión de expedientes |
| **Matriz de confusión** | Tabla que cruza clase real (filas) vs predicha (columnas) | Planilla de control de calidad: qué se dijo vs qué era |
| **Clase desbalanceada** | Una categoría es mucho más frecuente que las demás | Registro donde el 80% de las órdenes son de proveedores Pequeños |
| **`stratify`** | Mantener las proporciones de clase al dividir los datos | Tomar una muestra representativa, no una al voleo |
| **Clustering** | Agrupar registros por similitud matemática | Hacer pilas de expedientes parecidos entre sí |
| **K-Means** | Algoritmo que reparte los datos en *k* grupos que tú eliges | Decidir de antemano "haré 3 pilas" y dejar que la similitud las llene |
| **`StandardScaler`** | Transformar variables a media 0 y desviación 1 | Convertir montos y cantidades a un índice común comparable |
| **`pd.crosstab`** | Tabla de frecuencias que cruza dos variables | Tabla dinámica de Excel con conteo |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R2-07 · Evaluación y validación

En este módulo entrenaste tu primer clasificador y lo evaluaste con la métrica más simple: la exactitud. Pero ya te topaste con su límite: en un dataset donde el 80,6% de las órdenes son de proveedores Pequeños, un 81% de exactitud puede esconder un modelo que casi no distingue nada. La matriz de confusión fue tu primera ventana a ese problema.

**R2-07 lo enfrenta de lleno:** aprenderás métricas que no se dejan engañar por el desbalance (precision, recall, F1), a detectar cuándo un modelo "hace trampa" con información que no debería tener (*data leakage* — y ojo, que `compras_ml.csv` trae una columna trampa esperándote), a validar con *cross-validation* en vez de un solo split, y a auditar si el modelo trata igual a todas las regiones del país (*fairness*).

**Pregunta motivadora para llegar a R2-07:**
> Tu clasificador acierta el 81% de las veces... pero un modelo que dijera siempre "Pequeña" acertaría el 80,6% sin aprender nada. Si tu jefatura te pide defender el modelo ante la Contraloría, ¿con qué evidencia demostrarías que realmente sirve — y que sirve igual en Arica que en Magallanes?

---

*Formación Pública Chile · Licencia CC BY 4.0*
