# 📘 Guía de Aprendizaje — R2-08 · Pipelines reproducibles

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-08 · Pipelines reproducibles |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 2–3 horas |
| **Semana** | Semana 13 |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-04 (fundamentos de ML), R2-07 (evaluación y validación) |
| **Competencia de salida** | Construir pipelines reproducibles con scikit-learn, aplicar validación cruzada para estimar el error medio generalizado, y persistir modelos usando joblib para su posterior recarga |
| **Dataset** | `compras_ml.csv` — órdenes de compra de alimentos, ChileCompra (cantidad, tamano_num, monto_total) |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Has entrenado modelos, calculado métricas, detectado fugas de datos. Ahora el proceso real: llega un nuevo lote de órdenes de compra cada semana. ¿Cómo aplicas exactamente el mismo preprocesamiento que usaste en entrenamiento? Si escalas las variables a mano, ¿cómo recuerdas los valores exactos que usaste hace tres semanas? Y cuando el modelo necesita actualizarse, ¿cómo garantizas que el proceso sea reproducible para que otra persona del equipo pueda hacerlo?

En el Estado chileno, la **reproducibilidad no es un lujo técnico — es una exigencia de accountability**. Si ChileCompra implementa un modelo para priorizar auditorías y seis meses después Contraloría pregunta "cómo funciona", alguien tiene que poder ejecutar ese proceso de principio a fin, en cualquier máquina, y obtener el mismo resultado.

Lo que aprenderás aquí:
- **Cómo encadenar todos los pasos en un solo objeto** (el Pipeline) que no se puede ejecutar en el orden equivocado.
- **Por qué los pipelines previenen fugas de datos** automáticamente (aplican el escalado con los parámetros del train, nunca del test).
- **Cómo evaluar de forma más honesta** con validación cruzada.
- **Cómo guardar el modelo entrenado** en un archivo y recargarlo para usarlo en producción.

**Conexión con el dataset real:** el dataset usa `cantidad` (1–500 unidades) y `tamano_num` (1–4, codificación del tamaño del proveedor) para predecir `monto_total`. La diferencia de escala entre esas variables es exactamente el caso donde el escalado importa: el modelo KNN mide distancias, y sin escalar, el monto domina por tener valores mucho mayores.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **Pipeline** | Encadena preprocesamiento + modelo en un solo objeto con `fit`/`predict` | Protocolo de trabajo que obliga a seguir los pasos en orden, sin saltarse ninguno |
| **StandardScaler** | Transforma variables para que tengan media 0 y desviación estándar 1 | Convertir montos en pesos, dólares y UF a una misma escala para comparar |
| **KNeighborsRegressor (KNN)** | Predice el valor promediando los k casos más similares (vecinos más cercanos) | Estimar el monto de una nueva licitación buscando licitaciones históricas similares |
| **MAE (Mean Absolute Error)** | Error promedio en las mismas unidades de la variable objetivo | "Mi estimación de gasto se equivoca por X pesos en promedio" |
| **Fuga de datos en escalado** | Usar la media/desviación del test al escalar contamina los resultados | Establecer la línea base de un indicador usándola en la medición siguiente |
| **Validación cruzada (KFold)** | Evalúa el pipeline en k subdivisiones para estimar el error generalizado | Auditoría en 5 períodos distintos para obtener un promedio confiable |
| **`neg_mean_absolute_error`** | Scikit-learn devuelve el MAE negativo (convención interna); se niega para leerlo | Un indicador donde mayor es peor: se invierte para que el formato sea coherente |
| **joblib** | Serializa y guarda objetos de Python en disco (incluyendo el pipeline completo) | Exportar el modelo a un archivo como si fuera un informe en PDF firmado |
| **Persistencia del modelo** | El pipeline guardado incluye el escalador y el modelo: no hay que reentrenar | Tener la receta plastificada guardada: cualquiera puede seguirla más adelante |

---

## 4. Verificación de Prerrequisitos

Antes de empezar este módulo, responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Cargar un CSV con pandas y separar features del target | ✅ Sí / 🔄 Revisar R2-00 |
| Usar `train_test_split` para dividir datos | ✅ Sí / 🔄 Revisar R2-04 |
| Explicar qué es la fuga de datos y por qué es peligrosa | ✅ Sí / 🔄 Revisar R2-07 |
| Entrenar un modelo básico con `.fit()` y predecir con `.predict()` | ✅ Sí / 🔄 Revisar R2-04 |
| Calcular el MAE con `mean_absolute_error` | ✅ Sí / 🔄 Revisar R2-04 |
| Usar `cross_val_score` básico | ✅ Sí / 🔄 Revisar R2-07 |

Si tienes más de dos "Revisar", dedica 20 minutos a repasar esos módulos antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección: Preparación y el problema sin pipeline

🎯 **Objetivo:** cargar los datos, entender el problema de predicción (monto_total a partir de cantidad y tamano_num) y ver qué pasa con KNN sin escalar.

💡 **Concepto clave — por qué el escalado importa con KNN:**
KNN mide distancias: busca las órdenes "más parecidas" a la nueva. Pero `cantidad` va de 1 a 500, y `tamano_num` de 1 a 4. Sin escalar, la cantidad domina completamente la métrica de distancia y `tamano_num` queda irrelevante. Es como comparar funcionarios por talla (en cm) y edad (en años) sin normalizar: la talla en cm dominará porque tiene números mucho mayores.

🔍 **Qué hace el código:**
- Carga `compras_ml.csv` y define `X = df[["cantidad", "tamano_num"]]` e `y = df["monto_total"]`.
- Divide con `train_test_split` (70% train, 30% test).
- Entrena un `KNeighborsRegressor(n_neighbors=3)` **sin escalar** y calcula el MAE como línea base.

⚠️ **Error frecuente:** olvidar que el MAE que se muestra aquí es el **baseline** (punto de partida), no el resultado final. El objetivo es que el pipeline con escalado lo supere.

✅ **Señal de comprensión:** entiendes por qué el KNN sin escalar rinde mal y puedes explicarlo con la analogía de las escalas distintas.

---

### 🔷 Sección 1: El pipeline, encadenar pasos en un solo objeto

🎯 **Objetivo:** construir un `Pipeline` con `StandardScaler` + `KNeighborsRegressor` y entender por qué es mejor que aplicar los pasos por separado.

💡 **Concepto clave — la receta plastificada:**
Un pipeline es como una receta de trabajo oficializada. En vez de recordar cada paso suelto ("primero escalo", "con estos parámetros", "luego entreno", "con esa configuración"), tienes la secuencia fija y sellada. La sigues igual hoy, mañana y con datos nuevos, sin saltarte nada ni cambiar el orden. Y más importante: cuando llaman a `fit`, el escalador aprende sus parámetros *solo del conjunto de entrenamiento*. Cuando llaman a `predict`, aplica esos mismos parámetros al test. Nunca al revés. Así se elimina la fuga de datos en el preprocesamiento.

🔍 **Qué hace el código:**
- `Pipeline([("escalador", StandardScaler()), ("modelo", KNeighborsRegressor(n_neighbors=3))])` crea el pipeline con dos pasos nombrados.
- El pipeline se comporta exactamente como un modelo: tiene `.fit()` y `.predict()`.
- La documentación del módulo muestra el error típico de invertir el orden (modelar antes de escalar).

⚠️ **Error frecuente:** invertir el orden de los pasos (modelo primero, escalador después) o escalar a mano por fuera del pipeline "por si acaso". Eso duplica el trabajo y reintroduce exactamente el riesgo que el pipeline elimina.

✅ **Señal de comprensión:** puedes explicar la diferencia entre los pasos del pipeline y los nombres de los pasos (las strings `"escalador"` y `"modelo"` son etiquetas para acceder a ellos, no palabras clave).

---

### 🔷 Sección 2: Validación cruzada, una evaluación más honesta

🎯 **Objetivo:** usar `cross_val_score` con `KFold(n_splits=5)` para obtener una estimación más robusta del MAE del pipeline.

💡 **Concepto clave — 5 explotaciones distintas en vez de una:**
Un solo split puede mentir por azar. Imagina que por casualidad el test contiene solo las órdenes más simples de predecir: el MAE quedaría artificialmente bajo. Con validación cruzada de 5 folds, el proceso se repite 5 veces con distintas divisiones y se promedia. Es como hacer 5 revisiones de un informe en distintas épocas del año y reportar el promedio: más representativo, más honesto, más defendible.

🔍 **Qué hace el código:**
- `KFold(n_splits=5, shuffle=True, random_state=42)` define el esquema de partición.
- `cross_val_score(pipe, X, y, cv=cv, scoring="neg_mean_absolute_error")` ejecuta 5 entrenamientos y evaluaciones.
- `mae_cv = -cv_scores.mean()` convierte el MAE negativo (convención de scikit-learn) al valor real.

⚠️ **Error frecuente:** no negar el resultado de `cv_scores.mean()`. Scikit-learn devuelve el MAE como número negativo porque internamente trabaja con la convención "mayor es mejor". Olvida el signo negativo y parecerá que el MAE es `-450`, lo cual es confuso.

✅ **Señal de comprensión:** `len(cv_scores) == 5` y `mae_cv > 0`. Puedes explicar por qué el MAE de validación cruzada puede diferir del MAE de un solo split.

---

### 🔷 Sección 3: Guardar el modelo para reutilizarlo

🎯 **Objetivo:** guardar el pipeline completo (escalador + modelo) en un archivo con joblib y recargarlo para predecir nuevas órdenes.

💡 **Concepto clave — el modelo es un archivo, no un proceso mental:**
Reentrenar desde cero cada vez que necesitas una predicción es como recalcular a mano los promedios de tu planilla Excel cada mañana en vez de guardarla. Con `joblib.dump()` exportas el pipeline completo — escalador incluido — en un archivo `.joblib`. Con `joblib.load()` lo recargas en segundos. La ventaja clave: cuando llegan datos nuevos, no necesitas recordar cómo escalaste ni con qué valores — el pipeline lo sabe.

🔍 **Qué hace el código:**
- `joblib.dump(pipe, "modelo_compras.joblib")` guarda el pipeline entrenado en disco.
- `pipe_cargado = joblib.load("modelo_compras.joblib")` lo recarga en una nueva variable.
- `pipe_cargado.predict(pd.DataFrame({"cantidad": [100], "tamano_num": [2]}))` usa el pipeline recargado directamente.

⚠️ **Error frecuente:** cargar el pipeline pero olvidar que `predict` recibe un DataFrame, no una lista. Si pasas `[100, 2]` en vez de `pd.DataFrame({"cantidad": [100], "tamano_num": [2]})`, el pipeline lanzará un error porque no reconoce los nombres de columna.

✅ **Señal de comprensión:** el archivo `modelo_compras.joblib` existe en el directorio de trabajo y `pipe_cargado.predict(...)` da el mismo resultado que `pipe.predict(...)` sobre los mismos datos.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Construir el pipeline

**Habilidad:** armar un Pipeline con los pasos en el orden correcto usando nombres explícitos.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* un `Pipeline` recibe una lista de tuplas `(nombre, objeto)`. El primer elemento de la tupla es un string que tú eliges como etiqueta; el segundo es la instancia del transformador o modelo.
2. 🟠 *Pista 2 (técnica):* el Pipeline debe tener exactamente dos pasos: el primero con nombre `"escalador"` y un `StandardScaler()`, el segundo con nombre `"modelo"` y un `KNeighborsRegressor(n_neighbors=3)`. El orden importa: escalador va antes que modelo.
3. 🔴 *Pista 3 (estructura):* `pipe = Pipeline([("escalador", StandardScaler()), ("modelo", KNeighborsRegressor(n_neighbors=3))])`. Revisa que los strings entre comillas coincidan exactamente con los que pide el chequeo.

**Lógica de solución:** el constructor de `Pipeline` recibe una lista de 2 tuplas. La primera define el escalador con su etiqueta; la segunda, el modelo con su etiqueta. Eso es todo.

---

### ✍️ Ejercicio 2 — Entrenar y evaluar el pipeline

**Habilidad:** usar el pipeline como si fuera un modelo (`.fit()` + `.predict()`) y calcular el MAE.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* el pipeline tiene exactamente los mismos métodos que un modelo de scikit-learn. `pipe.fit(X_train, y_train)` entrena todos los pasos en secuencia (primero ajusta el escalador, luego entrena el KNN con los datos escalados).
2. 🟠 *Pista 2 (técnica):* `pipe.predict(X_test)` aplica el escalado (con los parámetros aprendidos del train) y luego predice. El resultado es un array de predicciones de monto.
3. 🔴 *Pista 3 (estructura):* `pipe.fit(X_train, y_train)`, luego `pred = pipe.predict(X_test)`, luego `mae_pipe = mean_absolute_error(y_test, pred)`.

**Lógica de solución:** se entrena el pipeline con los datos de entrenamiento, se predice sobre test, y se mide el MAE. El resultado debería ser notoriamente menor al MAE sin escalar del inicio del notebook.

---

### ✍️ Ejercicio 3 — Evaluar con validación cruzada

**Habilidad:** usar `cross_val_score` con `KFold` para una estimación robusta del MAE.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* necesitas dos cosas: un objeto `KFold` con 5 particiones (ya está creado como `cv`) y `cross_val_score` que recibe el pipeline, los datos completos (`X`, `y`), el esquema de CV y el scoring.
2. 🟠 *Pista 2 (técnica):* el scoring es `"neg_mean_absolute_error"` (MAE negativo, convención de scikit-learn). Para convertirlo al MAE real, niega el promedio: `mae_cv = -cv_scores.mean()`.
3. 🔴 *Pista 3 (estructura):* `cv_scores = cross_val_score(pipe, X, y, cv=cv, scoring="neg_mean_absolute_error")` y luego `mae_cv = -cv_scores.mean()`. Las dos variables deben quedar definidas.

**Lógica de solución:** `cross_val_score` internamente re-entrena el pipeline 5 veces con distintas divisiones. Cada vez entrena en 4/5 de los datos y evalúa en 1/5. Al final tienes 5 MAEs; el promedio (negado) es la estimación robusta.

---

### ✍️ Ejercicio 4 — Guardar, recargar y reutilizar

**Habilidad:** persistir el pipeline en disco con joblib y usarlo para predecir una nueva orden.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* joblib tiene dos funciones espejo: `joblib.dump(objeto, "archivo.joblib")` guarda, y `joblib.load("archivo.joblib")` recarga. El objeto puede ser cualquier cosa de Python, incluyendo un pipeline de scikit-learn.
2. 🟠 *Pista 2 (técnica):* una vez recargado en `pipe_cargado`, puedes usarlo directamente con `.predict()`. Para una nueva compra con cantidad 100 y tamano_num 2: `pd.DataFrame({"cantidad": [100], "tamano_num": [2]})`.
3. 🔴 *Pista 3 (estructura):* (1) `joblib.dump(pipe, "modelo_compras.joblib")`, (2) `pipe_cargado = joblib.load("modelo_compras.joblib")`, (3) `compra_nueva = pd.DataFrame({"cantidad": [100], "tamano_num": [2]})`, (4) `temp_nueva = pipe_cargado.predict(compra_nueva)[0]`.

**Lógica de solución:** se guarda el pipeline entrenado en disco, se recarga en una nueva variable, y se usa para predecir pasando un DataFrame con las mismas columnas que el pipeline fue entrenado. El resultado debe ser idéntico al que daría el pipeline original.

---

## 7. Profundización: Reproducibilidad como estándar de gobernanza

En el sector público chileno, la reproducibilidad no es un valor técnico — es un requisito de transparencia y accountability.

**¿Qué significa reproducibilidad en el contexto del Estado?**

Un modelo reproducible es aquel que, dado el mismo conjunto de datos de entrada, siempre produce el mismo resultado independientemente de quién lo ejecute, cuándo y en qué máquina. Esto es crítico cuando:

- **Contraloría audita el modelo:** deben poder ejecutarlo y verificar que los resultados coinciden con el informe original.
- **El equipo rota:** quien entró a trabajar hoy necesita poder continuar con el modelo del año pasado.
- **El modelo se actualiza:** el nuevo modelo debe ser comparable con el anterior en términos de metodología.

**Cómo los pipelines de scikit-learn garantizan reproducibilidad:**

1. **Orden fijo:** los pasos siempre se ejecutan en el mismo orden. No hay ambigüedad.
2. **Parámetros guardados:** el archivo `.joblib` contiene los parámetros exactos del escalador (media y desviación estándar calculadas en el train) y el modelo (los vecinos y sus pesos).
3. **Semilla aleatoria:** usando `random_state=42` en los pasos que tienen aleatoriedad, el resultado es siempre idéntico.
4. **Sin dependencia de memoria:** no necesitas tener el notebook ejecutado para hacer una predicción; solo necesitas el archivo `.joblib`.

**Recomendación para modelos en producción pública:** guarda junto al archivo `.joblib` un archivo de metadatos (`model_metadata.json`) con: fecha de entrenamiento, versión del dataset, MAE de validación cruzada, y nombre del responsable técnico. Esto permite auditar el modelo sin ejecutarlo.

---

## 8. Conexión con el cuaderno siguiente

| Tema | En `leccion.ipynb` | Lo que viene en R2-09 |
|---|---|---|
| Pipeline en disco | Guardar y recargar con joblib | ✅ Usar el archivo `.joblib` para predicción en producción |
| Predicción de un caso | Manual con `predict` | ✅ Función de predicción con validación de entrada |
| Predicción de muchos casos | No cubierto | ✅ Batch scoring: puntuar una tabla entera y exportar a CSV |
| Despliegue conceptual | Menciona APIs y apps | ✅ Panorama completo: API, Gradio, monitoreo, reentrenamiento |

**¿Cuándo revisar este módulo antes de continuar?**

Revisa R2-08 antes de continuar con R2-09 si:
- No lograste que el `mae_pipe` sea menor que el MAE sin escalar del inicio.
- No entiendes por qué el pipeline previene fugas de datos en el escalado.
- El archivo `modelo_compras.joblib` no se creó correctamente.

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la ventaja principal de usar un Pipeline sobre aplicar los pasos por separado?

- a) El pipeline es más rápido computacionalmente
- b) **El pipeline aplica el escalado con los parámetros del train en test, previniendo fugas de datos ✅**
- c) El pipeline solo funciona con ciertos modelos
- d) El pipeline requiere menos código

**Explicación:** la ventaja clave no es velocidad ni cantidad de código, sino que el pipeline garantiza que el preprocesamiento nunca "ve" el test set durante el entrenamiento. Eso elimina una categoría completa de fugas de datos.

---

**Pregunta 2:** `cross_val_score` con `scoring="neg_mean_absolute_error"` devuelve valores negativos. ¿Por qué?

- a) Porque el MAE siempre es negativo
- b) **Porque scikit-learn usa la convención "mayor es mejor" y devuelve el MAE negado ✅**
- c) Es un bug de la librería
- d) Porque el modelo está sobreajustado

**Explicación:** scikit-learn usa internamente la convención de que "mayor puntaje = mejor modelo". Como el MAE es "menor = mejor", lo niegan para que funcione con esa convención. Para obtener el MAE real, simplemente niegas el promedio: `mae_cv = -cv_scores.mean()`.

---

**Pregunta 3:** Entrenas un pipeline y lo guardas con `joblib.dump`. Después de 3 meses, lo recargas. ¿Necesitas reentrenarlo?

- a) Sí, siempre hay que reentrenar al recargar
- b) **No, el archivo contiene todos los parámetros aprendidos y está listo para predecir ✅**
- c) Solo si los datos cambiaron
- d) Depende de la versión de scikit-learn

**Explicación:** el archivo `.joblib` serializa el objeto completo, incluyendo los parámetros del escalador (media y desviación estándar del train) y el modelo entrenado. Al recargarlo, ya está listo para `predict` sin necesidad de `fit`.

---

**Pregunta 4:** Tu KNN sin escalar tiene MAE = 850,000 CLP. Tu pipeline con escalado tiene MAE = 320,000 CLP. ¿Qué concluyes?

- a) El pipeline es peor porque usa más código
- b) La diferencia es por azar del split
- c) **El escalado mejoró significativamente el modelo porque KNN depende de distancias y las variables tenían escalas muy distintas ✅**
- d) Debes usar otro modelo

**Explicación:** KNN mide distancias y es muy sensible a la escala de las variables. Sin escalar, `cantidad` (1–500) dominó completamente sobre `tamano_num` (1–4). Con escalado, ambas variables contribuyen equitativamente y el modelo puede aprender mejor los patrones.

---

**Pregunta 5:** Quieres predecir el monto de una nueva orden con cantidad=200 y tamano_num=3 usando el pipeline guardado. ¿Cómo llamas la predicción correctamente?

- a) `pipe_cargado.predict([200, 3])`
- b) `pipe_cargado.predict(200, 3)`
- c) **`pipe_cargado.predict(pd.DataFrame({"cantidad": [200], "tamano_num": [3]}))[0]` ✅**
- d) `pipe_cargado.fit_predict([200, 3])`

**Explicación:** el pipeline fue entrenado con un DataFrame que tenía columnas con nombres específicos. Debe recibir un DataFrame con exactamente las mismas columnas. La lista `[0]` al final extrae el primer (y único) valor del array de predicciones.

---

## 10. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Pipeline** | Cadena de transformadores + estimador tratada como un único objeto | Protocolo de trabajo sellado que nadie puede ejecutar en orden equivocado |
| **StandardScaler** | Transforma variables a media 0 y desviación estándar 1 | Normalizar indicadores a una escala común para comparar entre servicios |
| **KNeighborsRegressor** | Predice el valor promediando los k casos más similares | Estimar el gasto de un contrato buscando contratos históricos similares |
| **MAE** | Error absoluto medio: cuánto se equivoca el modelo en promedio | "Me equivoco por $X en promedio" en mis estimaciones de presupuesto |
| **Fuga de datos en escalado** | Contaminar el escalador con información del test | Calibrar el instrumento de medición usando los datos que quieres medir |
| **KFold** | Esquema de validación cruzada con k particiones rotativas | Plan de auditoría que cubre todos los períodos de manera rotativa |
| **neg_mean_absolute_error** | MAE negado (convención interna de scikit-learn) | Indicador inverso: más alto significa menor error |
| **joblib** | Librería de Python para guardar/cargar objetos en disco | Guardar una hoja de cálculo Excel con fórmulas y datos para compartir |
| **Persistencia** | Guardar el modelo entrenado en un archivo reutilizable | Exportar el modelo como "informe listo para usar" sin necesidad de reprocesar |
| **Reproducibilidad** | Mismos datos + mismo código = mismo resultado siempre | Un proceso auditado que cualquier funcionario puede replicar y verificar |
| **random_state** | Semilla para operaciones aleatorias (garantiza resultados idénticos) | Número de folio único que vincula todos los documentos de un proceso |
| **Baseline** | Resultado del modelo más simple como punto de referencia | Indicador histórico de base contra el que se comparan las mejoras |

---

## 11. Conexión con el Módulo Siguiente

**Módulo siguiente:** R2-09 · Despliegue de modelos

En este módulo lograste encadenar todo el proceso en un pipeline reproducible, validarlo honestamente con validación cruzada y guardarlo en disco. El archivo `modelo_compras.joblib` está listo.

Pero ¿cómo usa ese modelo alguien que no es ténico? ¿cómo proceso 10,000 órdenes de compra nuevas de un golpe? ¿Qué pasa si alguien envía datos incorrectos (cantidad -5, tamano_num 99)?

**R2-09 responde esas preguntas** mostrando cómo convertir el pipeline en algo **usable por otras personas**:
- Una **función de predicción** que cualquiera puede llamar con una nueva orden.
- Una **función de validación** que rechaza entradas inválidas antes de predecir.
- El **scoring por lotes** que procesa una tabla entera y exporta los resultados a CSV.

**Preconcepto clave para llevar:** el archivo `modelo_compras.joblib` que creaste en el Ejercicio 4 de este módulo es exactamente el archivo que R2-09 recarga al inicio para construir encima. No son módulos independientes: R2-09 toma donde R2-08 deja.

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos de Chile · Formación Pública*
*Contenido bajo licencia CC BY 4.0*
