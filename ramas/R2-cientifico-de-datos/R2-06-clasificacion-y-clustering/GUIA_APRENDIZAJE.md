# Guía de Aprendizaje — R2-06 · Clasificación y clustering

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 6 · Semana 12

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-06 · Clasificación y clustering |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 3 horas |
| **Nivel** | Intermedio — requiere R2-04 y R2-05 |
| **Prerrequisitos** | `train_test_split`, `fit`/`predict`, árboles de decisión, `groupby` y `pivot_table` |
| **Competencia de salida** | Entrenar y evaluar un clasificador con clases desbalanceadas (matriz de confusión, precisión, recall) y aplicar clustering con K-Means distinguiendo cuándo un problema es supervisado y cuándo no |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 diario 2020–2025, 14 estaciones SINCA) + `estaciones.csv` (comuna y región). Profundización: `reclamos.csv` (muestra de 20.000 reclamos SERNAC 2011, dato histórico) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

En R2-04 y R2-05 tus modelos predecían **números**. Pero muchas decisiones del Estado son de **categoría**: ¿se decreta o no un episodio crítico mañana?, ¿este reclamo se resolverá o no?, ¿este establecimiento es rural o urbano? Y a veces ni siquiera tienes categorías: tienes muchos casos y quieres saber **qué tipos** hay.

Este módulo te da las dos herramientas, con un dato que le importa a millones de personas: el **material particulado fino (PM2.5)**. La norma de 24 horas es **50 µg/m³** (D.S. 12/2011 del Ministerio del Medio Ambiente). En los seis años de datos hay **1.279 mediciones diarias sobre la norma**: Cerro Navia acumula 332, Las Encinas (Temuco) 282, El Bosque 240, Rancagua 231 y Nielol 165; en seis estaciones del norte y la costa no hubo ninguna. Tras quedarnos con los días que tienen el dato del día anterior, quedan 29.305 días-estación, de los cuales **1.269 (4,3 %)** superan la norma.

- **Clasificación:** con el PM2.5 de ayer y la estación del año, ¿se puede anticipar si mañana se supera la norma? Vas a descubrir que un modelo con **96,8 % de exactitud** deja escapar **208 de 381** días malos del conjunto de prueba — y que decidir qué error es más caro es una **decisión de política pública**, no un detalle técnico.
- **Clustering:** sin decirle nada sobre leña, latitud ni industria, K-Means separa las 14 estaciones en tres tipos de ciudad que cualquier SEREMI reconocería.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el Estado |
|----------|-----------|----------------------|
| **Clasificación** | Predice una categoría (0/1), no un número | Una columna «¿Alerta?» con SÍ/NO en vez de un monto |
| **Clases desbalanceadas** | Una clase es mucho más rara que la otra | 4 de cada 100 días superan la norma |
| **Exactitud (*accuracy*)** | % de casos bien clasificados | Tasa de aciertos de una revisión — engañosa si casi todo es «no» |
| **Modelo tonto / línea base** | Predice siempre la clase más frecuente | Responder «no» a todo y acertar 95 % |
| **`stratify=y`** | Mantiene la proporción de clases al dividir | Muestra representativa por estrato |
| **Matriz de confusión** | Cruza lo real con lo predicho | Tabla dinámica «real» × «predicho» |
| **Falso negativo (FN)** | Día malo que el modelo no avisó | Población expuesta sin medidas |
| **Falso positivo (FP)** | Falsa alarma | Restricción innecesaria |
| **Precisión** | De lo que alerté, cuánto era cierto | Credibilidad de las alertas |
| **Recall** | De lo malo, cuánto detecté | Cobertura de protección |
| **`class_weight="balanced"`** | Hace pesar más los errores en la clase rara | Priorizar no perderse casos graves |
| **Clustering / K-Means** | Agrupa casos parecidos sin etiquetas | Ordenar fichas en pilas sin pauta previa |
| **`StandardScaler`** | Media 0 y desviación 1 por columna | Llevar todo a un «índice común» |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Dividir datos con `train_test_split` y entrenar con `.fit()` / `.predict()` | ☐ |
| Explicar cómo decide un árbol de decisión (R2-05) | ☐ |
| Crear una columna con `groupby(...).shift(1)` o entender qué hace | ☐ |
| Armar una tabla con `pivot_table` (filas × columnas × valor) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `aire_diario.csv` (30.674 filas) y `estaciones.csv` (14 estaciones), y construir las variables.

💡 **Concepto clave:** `pm25_ayer = groupby("estacion")["pm25"].shift(1)` trae, a cada día, el valor del día anterior **de la misma estación**. Es información que la autoridad **sí tiene** la víspera. `invierno` vale 1 de mayo a agosto. `sobre_norma = (pm25 > 50)` es la respuesta que queremos anticipar.

⚠️ **Error frecuente:** hacer `shift(1)` sin `groupby`: el primer día de Antofagasta recibiría el último día de Alto Hospicio.

---

### Sección 1 · Clasificación: predecir una categoría

🎯 **Objetivo:** Definir `X` e `y`, medir el desbalance y dividir con `stratify=y`.

💡 **Concepto clave:** Solo el **4,3 %** de los días supera la norma. Con `stratify=y`, entrenamiento (20.513 días) y prueba (8.792) quedan con la misma proporción: 4,33 % y 4,33 %.

✅ **Señal de que entendiste:** Puedes explicar qué pasaría con la prueba si, por azar, le tocaran muy pocos días malos.

---

### Sección 2 · La trampa de la exactitud

🎯 **Objetivo:** Entrenar una regresión logística y compararla con el modelo que siempre dice «no».

💡 **Concepto clave:** El modelo logra **0,968** de exactitud… y el modelo tonto, **0,957**. Once décimas de diferencia: la exactitud casi no distingue un modelo útil de uno que nunca avisa nada.

✅ **Señal de que entendiste:** Ante un «96 % de exactitud», tu primera pregunta es «¿y cuánto saca el que dice siempre que no?».

---

### Sección 3 · La matriz de confusión

🎯 **Objetivo:** Desarmar los aciertos y los dos tipos de error.

💡 **Concepto clave:** En la prueba: 8.338 días normales bien clasificados (TN), **73 falsas alarmas** (FP), **208 días malos que se escaparon** (FN) y 173 días malos detectados (TP). El orden de `ravel()` es siempre `tn, fp, fn, tp`.

---

### Sección 4 · Precisión, recall y el error más caro

🎯 **Objetivo:** Medir precisión y recall, y comparar con un modelo `class_weight="balanced"`.

💡 **Concepto clave:** El modelo normal tiene precisión **0,70** y recall **0,45**: sus alertas son creíbles, pero detecta menos de la mitad de los días malos. El balanceado sube el recall a **0,91** (solo 35 días malos se escapan) a cambio de bajar la precisión a **0,39** (548 falsas alarmas). Ninguno es «el correcto»: depende de cuánto cuesta cada error. Para la autoridad sanitaria, un día malo sin aviso suele ser más caro que una falsa alarma — pero esa decisión se **declara**.

✅ **Señal de que entendiste:** Puedes explicar el intercambio con números concretos de días.

---

### Sección 5 · Clustering

🎯 **Objetivo:** Armar el perfil mensual (14 estaciones × 12 meses), estandarizar y agrupar con K-Means (k = 3).

💡 **Concepto clave:** Aquí no hay `y`. Cada estación es una fila con su PM2.5 promedio de enero a diciembre. `StandardScaler` deja cada mes con media 0 y desviación 1 para que la distancia compare **formas y niveles** sin que un mes domine.

⚠️ **Error frecuente:** Olvidar `random_state=42` y `n_init=10`: los grupos pueden cambiar de número de etiqueta entre ejecuciones.

---

### Sección 6 · Interpretar los grupos

🎯 **Objetivo:** Ponerle nombre a cada cluster.

💡 **Concepto clave:** Los tres grupos que aparecen:

| Grupo | Estaciones | Perfil |
|---|---|---|
| **Temuco** | Las Encinas Temuco, Nielol | Aire limpio en verano (≈4 µg/m³ en enero) y el invierno más severo (≈46 en junio) |
| **Centro** | Cerro Navia, El Bosque, Rancagua I, Centro Quintero, Bomberos (Tocopilla) | Elevado todo el año (≈12–17) con pico invernal (≈41 en julio) |
| **Norte y costa** | 21 de Mayo, Alto Hospicio, Antofagasta, Copiapó, Coquimbo, Cuncumen, Concón | Plano y bajo (≈8–12 todo el año) |

> 🔎 **Ojo con el nombre del grupo.** Bomberos está en **Tocopilla** (Región de Antofagasta), a más de 1.000 km de Santiago, y aun así cae en el grupo «Centro». KMeans agrupa por el **perfil** de contaminación, no por la geografía: Tocopilla, una ciudad con historia de centrales termoeléctricas a carbón, se comporta como una estación urbana del centro. El nombre del grupo es una etiqueta que pones tú, así que revísalo contra los datos antes de usarlo en un informe.

El algoritmo no sabe de leña, de inversión térmica ni de industria: **tú** aportas esa interpretación, y debes decir que es una hipótesis.

---

### Reflexión final

Las dos preguntas de la reflexión no tienen celda de chequeo porque son decisiones: qué error tolerar en un sistema de alerta, y qué política distinta merece cada tipo de ciudad. Un buen análisis las deja **escritas y justificadas**.

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Prepara X, y y una división estratificada

**Pistas progresivas:**
- 🟢 Pista suave: `X` lleva dos columnas; `y` es la columna 0/1. El promedio de una columna 0/1 es una proporción.
- 🟡 Pista media: `train_test_split` recibe `test_size`, `random_state` y `stratify`.
- 🔴 Pista directa: `X = d[["pm25_ayer", "invierno"]]`, `y = d["sobre_norma"]`, `tasa_positivos = y.mean()` y `train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)`.

**¿Qué significa el ✅?** Que mediste el desbalance (≈4 %) y que la prueba tiene la misma proporción de días malos que el entrenamiento.

---

### Ejercicio 2 — Entrena el clasificador y compáralo con el que siempre dice «no»

**Pistas progresivas:**
- 🟢 Pista suave: El modelo tonto acierta exactamente en los días normales de la prueba.
- 🟡 Pista media: `accuracy_score(y_test, y_pred)`; la proporción de ceros es `(y_test == 0).mean()`.
- 🔴 Pista directa: `modelo.fit(X_train, y_train)`, `y_pred = modelo.predict(X_test)`, `exactitud = accuracy_score(y_test, y_pred)`, `exactitud_tonta = (y_test == 0).mean()`.

**¿Qué significa el ✅?** Que viste que 0,968 y 0,957 casi no se distinguen: la exactitud no basta.

---

### Ejercicio 3 — Cuenta los aciertos y los dos tipos de error

**Pistas progresivas:**
- 🟢 Pista suave: La matriz de 2×2 se puede «aplanar» en cuatro números.
- 🟡 Pista media: `confusion_matrix(real, predicho)` y luego `.ravel()`.
- 🔴 Pista directa: `cm = confusion_matrix(y_test, y_pred)` y `tn, fp, fn, tp = cm.ravel()`.

**¿Qué significa el ✅?** Que sabes cuántos días malos se escaparon (208) y cuántas falsas alarmas hubo (73).

---

### Ejercicio 4 — Compara precisión y recall del modelo normal y del balanceado

**Pistas progresivas:**
- 🟢 Pista suave: Las dos métricas se calculan igual que la exactitud, con otra función.
- 🟡 Pista media: `precision_score` y `recall_score`; el modelo nuevo es el mismo con `class_weight="balanced"`.
- 🔴 Pista directa: `modelo_bal = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)`, `y_pred_bal = modelo_bal.predict(X_test)` y las cuatro métricas sobre `(y_test, y_pred)` y `(y_test, y_pred_bal)`.

**¿Qué significa el ✅?** Que comprobaste el intercambio: recall de 0,45 a 0,91, precisión de 0,70 a 0,39.

---

### Ejercicio 5 — Arma el perfil mensual y agrupa con K-Means

**Pistas progresivas:**
- 🟢 Pista suave: Una fila por estación, una columna por mes, el promedio como valor.
- 🟡 Pista media: `pivot_table(index=..., columns=..., values=..., aggfunc="mean")`, luego `StandardScaler().fit_transform(...)`.
- 🔴 Pista directa: `perfil = df.pivot_table(index="estacion", columns="mes", values="pm25", aggfunc="mean")`, `Z = StandardScaler().fit_transform(perfil)`, `grupos = pd.Series(km.fit_predict(Z), index=perfil.index, name="cluster")`.

**¿Qué significa el ✅?** Que cada una de las 14 estaciones quedó asignada a uno de 3 grupos, con datos estandarizados.

---

### Ejercicio 6 — Ponle nombre al grupo del invierno más severo

**Pistas progresivas:**
- 🟢 Pista suave: Primero promedia el perfil de cada grupo; luego mira la columna de junio.
- 🟡 Pista media: `perfil.groupby(grupos).mean()` y `idxmax()` sobre la columna `6`.
- 🔴 Pista directa: `cluster_invierno = perfil_grupo[6].idxmax()` y `estaciones_invierno = list(grupos[grupos == cluster_invierno].index)`.

**¿Qué significa el ✅?** Que el algoritmo, sin saber nada de geografía, aisló a las dos estaciones de Temuco — y que tú puedes explicarlo.

---

> 🔬 **En la profundización:** clasificación con datos **solo categóricos** — 20.000 reclamos SERNAC de 2011 (dato histórico: el SERNAC no publica una base abierta más reciente con este detalle). Conviertes `mercado` y `motivo_legal` en 51 columnas con **one-hot**, superas la línea base (0,519 → 0,650 de exactitud prediciendo si el proveedor acoge el reclamo) y ves cómo el desbalance reaparece con 7 resultados posibles: exactitud 0,60, pero **recall macro 0,33**, con dos categorías que el modelo nunca predice.

---

## 7. Autoevaluación Final

**Pregunta 1:** Un modelo de alerta de episodios tiene 96 % de exactitud. ¿Qué preguntas primero?

- A) Si usó árboles o regresión logística
- B) Cuánta exactitud tiene el modelo que siempre dice «no hay episodio» ✅
- C) Cuántas filas tenía el dataset
- D) Si se entrenó en Colab

**Explicación:** Con clases desbalanceadas, la línea base ya es altísima (0,957 aquí). Sin compararla, el 96 % no dice nada.

---

**Pregunta 2:** En la matriz de confusión, un **falso negativo** es…

- A) Un día normal que el modelo marcó como malo
- B) Un día sobre la norma que el modelo no avisó ✅
- C) Un día sin dato
- D) Un acierto en la clase mayoritaria

**Explicación:** «Negativo» es lo que dijo el modelo («no se supera»); «falso» es que se equivocó.

---

**Pregunta 3:** La SEREMI prefiere no perderse ningún día malo aunque haya más falsas alarmas. ¿Qué métrica prioriza?

- A) Precisión
- B) Exactitud
- C) Recall ✅
- D) Ninguna, da lo mismo

**Explicación:** Recall = de los días realmente malos, cuántos detectó. Subirlo cuesta precisión (más falsas alarmas), y esa es una decisión que se declara.

---

**Pregunta 4:** ¿Por qué se estandariza el perfil antes de K-Means?

- A) Porque K-Means no acepta números decimales
- B) Porque K-Means mide distancias y una variable con números más grandes dominaría los grupos ✅
- C) Para que el resultado sea siempre 3 grupos
- D) Para eliminar los valores faltantes

**Explicación:** Sin escalar, la distancia la deciden las columnas de mayor magnitud. Escalar las pone en igualdad de condiciones.

---

**Pregunta 5:** K-Means puso a Temuco en un grupo aparte. ¿Qué puedes afirmar en un informe?

- A) Que la causa es la leña, porque el algoritmo lo demostró
- B) Que su perfil mensual es distinto (verano muy limpio, invierno muy severo); la causa es una hipótesis que hay que respaldar con otra evidencia ✅
- C) Que Temuco tiene un error de medición
- D) Nada, el clustering no sirve para informes

**Explicación:** El clustering describe parecidos; no explica causas. Interpretar es tu trabajo, y debe decir qué es dato y qué es hipótesis.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Clasificación** | Aprendizaje supervisado que predice categorías | Decidir «alerta / no alerta» |
| **Aprendizaje no supervisado** | Encontrar estructura sin respuestas conocidas | Ordenar un archivo heredado sin pauta |
| **Clases desbalanceadas** | Una categoría es mucho más rara | Pocos días críticos en un año |
| **Línea base** | El desempeño de una regla trivial | «Siempre no» |
| **Matriz de confusión** | Tabla real × predicho | Planilla de aciertos y errores por tipo |
| **Precisión** | TP / (TP + FP) | Credibilidad de las alertas |
| **Recall** | TP / (TP + FN) | Cobertura de los casos graves |
| **`class_weight="balanced"`** | Penaliza más los errores en la clase rara | Priorizar lo grave sobre lo frecuente |
| **K-Means** | Agrupa en *k* grupos por cercanía | Separar en pilas de parecidos |
| **Estandarizar** | Media 0 y desviación 1 | Índice común para comparar |
| **One-hot** | Una columna 0/1 por categoría | Convertir «mercado» en casillas marcables |

---

## 9. Conexión con el Módulo Siguiente

En R2-06 aprendiste los dos grandes tipos de aprendizaje y, sobre todo, a desconfiar de la exactitud cuando lo que importa es raro.

En **R2-07 · Evaluación y validación** vas a ir más lejos con el mismo problema del aire: el **F1**, la **fuga de datos** (una variable que mira el futuro y dispara el desempeño), la diferencia entre validación cruzada **barajada** y **temporal** — por qué con datos en el tiempo no se puede barajar — y el desempeño **por estación**: ¿el modelo protege igual a todas las ciudades?

> 💡 **Pregunta para reflexionar:** El modelo de hoy dividió los días al azar. Pero en la vida real se entrena con el pasado y se usa en el futuro. ¿Crees que el desempeño sería el mismo si lo evaluaras solo en 2025, habiendo entrenado con 2020–2024?
