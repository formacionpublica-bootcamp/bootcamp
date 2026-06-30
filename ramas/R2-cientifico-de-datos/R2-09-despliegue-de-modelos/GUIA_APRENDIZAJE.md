# 📘 Guía de Aprendizaje — R2-09 · Despliegue de modelos

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-09 · Despliegue de modelos |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 2–3 horas |
| **Semana** | Semana 13–14 |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-08 (pipelines reproducibles) — el archivo `modelo_compras.joblib` debe existir |
| **Competencia de salida** | Dejar tu modelo usable por otra persona: función de predicción con validación de entrada, scoring por lotes y archivo de resultados |
| **Dataset** | `compras_ml.csv` + `compras_nuevas.csv` — órdenes de compra de alimentos, ChileCompra |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ + archivo `predicciones_monto.csv` |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Entrenaste el modelo, lo evaluaste, lo guardaste. Hasta aquí tú puedes usarlo. Pero el valor real en el Estado surge cuando **otras personas pueden usarlo sin saber de machine learning**. El analista de la unidad de compras que recibe un Excel con 500 órdenes nuevas y necesita la estimación de monto. El jefe de unidad que envía una solicitud y espera que el sistema valide los datos antes de procesar. El equipo de control que quiere revisar un mes de predicciones en bloque.

Este módulo te enseña a construir esa "interfaz" entre tu modelo y el mundo: funciones claras, con validación, que no se caen con datos raros, y que exportan resultados en formatos que la administración pública ya conoce (CSV, que cualquiera abre en Excel).

**Lo concreto que aprenderás:**
- Cómo hacer una **función de predicción** que cualquier colega puede llamar.
- Cómo hacer **predicción por lotes**: procesar una tabla entera de golpe.
- Cómo **validar la entrada**: rechazar valores imposibles antes de que lleguen al modelo.
- Cómo **exportar los resultados** a un CSV listo para compartir.

**Una nota importante:** en este módulo NO montas un servidor ni una API real en internet. Aprendes los conceptos y construyes las funciones que son el corazón de cualquier despliegue. Llevar eso a producción completa (con servidor, monitoreo, etc.) es trabajo de un equipo técnico especializado, y aquí entenderás qué implica ese siguiente paso.

**Conexión con el dataset real:** `compras_nuevas.csv` simula el lote de órdenes que llegaría al final del mes. Procesar esa tabla y exportar `predicciones_monto.csv` es exactamente el flujo de trabajo que podría automatizarse en un servicio público.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **Predicción en línea (online)** | Llega un caso, se responde al instante | Funcionario que llena formulario y el sistema entrega estimación en segundos |
| **Predicción por lotes (batch)** | Llega una tabla de miles de casos, se procesan todos de una vez | Procesar el cierre mensual de órdenes de compra en una sola ejecución |
| **Función de predicción** | Función que recibe parámetros y devuelve la estimación | Formulario digital que calcula automáticamente el valor estimado |
| **Validación de entrada** | Comprobar que los datos recibidos están en rangos válidos antes de predecir | Control de integridad de datos antes de ingresar una solicitud al sistema |
| **Diccionario de respuesta** | Estructura `{"ok": True/False, "resultado": ...}` que comunica éxito o error | Notificación de sistema que dice "solicitud aprobada" o "error: dato inválido" |
| **Scoring por lotes** | Aplicar el modelo a una tabla entera con `modelo.predict(tabla)` | Ejecutar una macro de Excel sobre toda la planilla de una vez |
| **API web (conceptual)** | Servicio en internet que expone la función de predicción vía URL | Servicio web de ChileCompra al que otros sistemas se conectan para consultar |
| **Monitoreo (conceptual)** | Vigilar si las predicciones siguen siendo buenas con el tiempo | Auditoría periódica del modelo: ¿sigue prediciendo bien con datos recientes? |
| **Reentrenamiento (conceptual)** | Actualizar el modelo con datos más recientes cuando se desajusta | Actualizar las tablas de parámetros de gestión cada año con datos frescos |

---

## 4. Verificación de Prerrequisitos

Antes de empezar este módulo, responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Cargar un CSV con pandas | ✅ Sí / 🔄 Revisar R2-00 |
| Crear y entrenar un Pipeline de scikit-learn | ✅ Sí / 🔄 Revisar R2-08 |
| Guardar y recargar un modelo con `joblib.dump` / `joblib.load` | ✅ Sí / 🔄 Revisar R2-08 |
| Usar `modelo.predict()` sobre un DataFrame | ✅ Sí / 🔄 Revisar R2-08 |
| Definir una función en Python con `def` y `return` | ✅ Sí / 🔄 Revisar R2-00 |
| Exportar un DataFrame a CSV con `to_csv()` | ✅ Sí / 🔄 Revisar R2-01 |

Si tienes más de dos "Revisar", prioriza R2-08 que es el prerrequisito directo de este módulo.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección: Preparación y las dos formas de usar un modelo

🎯 **Objetivo:** cargar el entorno, reentrenar el pipeline del módulo anterior, y entender la diferencia entre predicción en línea y por lotes.

💡 **Concepto clave — dos flujos de trabajo distintos en el Estado:**
La predicción **en línea** responde una solicitud individual al instante: un funcionario llena un formulario y el sistema devuelve el monto estimado mientras espera. La predicción **por lotes** procesa un archivo completo: al cierre del mes, se suben las 5.000 órdenes nuevas y el sistema las puntea todas de una vez. Ambos flujos comparten el mismo modelo, pero tienen requisitos distintos de código.

🔍 **Qué hace el código:**
- Recrea el pipeline del módulo anterior (StandardScaler + KNeighborsRegressor).
- Carga `compras_nuevas.csv` (el lote de órdenes que se procesará en los ejercicios).
- No hay TODO en esta sección: ejecutar y observar.

⚠️ **Error frecuente:** no tener `compras_nuevas.csv` disponible. Si estás en Colab, asegúrate de subirlo junto con `compras_ml.csv`. El notebook intenta descargarlo automáticamente desde GitHub.

✅ **Señal de comprensión:** el print dice "Modelo cargado y entrenado exitosamente" y puedes distinguir los dos escenarios de uso (uno a uno vs. por lotes).

---

### 🔷 Sección 1: La función de predicción, el corazón del despliegue

🎯 **Objetivo:** crear `predecir_monto(cantidad, tamano_num)` — una función que cualquier persona puede llamar para obtener una estimación de monto.

💡 **Concepto clave — encapsular la complejidad:**
Una buena función de predicción esconde la complejidad del modelo detrás de una interfaz simple. Quien la llama no necesita saber que hay un KNN con escalado dentro: solo escribe `predecir_monto(100, 2)` y obtiene la respuesta. Es el mismo principio que un formulario web del Estado: el usuario llena campos simples y el sistema hace el trabajo internamente.

🔍 **Qué hace el código:**
- La función recibe `cantidad` y `tamano_num` como parámetros individuales.
- Construye internamente el DataFrame que el pipeline necesita: `pd.DataFrame({"cantidad": [cantidad], "tamano_num": [tamano_num]})`.
- Llama a `modelo.predict(...)`, toma el primer (y único) elemento, y lo redondea a 1 decimal.

⚠️ **Error frecuente:** no poner los valores en listas dentro del DataFrame. `pd.DataFrame({"cantidad": 100})` falla; debe ser `pd.DataFrame({"cantidad": [100]})` — pandas espera iterables, no escalares.

✅ **Señal de comprensión:** `predecir_monto(100, 2)` devuelve un número real (no 0.0) y es aproximadamente el mismo valor que el pipeline entrenado predice para esos parámetros.

---

### 🔷 Sección 2: Puntuación por lotes

🎯 **Objetivo:** crear `predecir_lote(tabla)` — una función que agrega la columna `monto_estimado` a una tabla completa.

💡 **Concepto clave — el modelo procesa tablas enteras de una vez:**
No hace falta llamar a `predecir_monto` cien veces para cien órdenes. El método `modelo.predict(tabla)` puede recibir una tabla de cualquier tamaño y devuelve todas las predicciones en un array. Es como aplicar una fórmula de Excel a toda la columna en vez de celda por celda: el resultado es el mismo, pero mucho más rápido y menos propenso a errores.

🔍 **Qué hace el código:**
- Recibe una tabla (DataFrame) con columnas `cantidad` y `tamano_num`.
- Agrega una columna nueva `monto_estimado` con las predicciones del modelo, redondeadas a 1 decimal.
- Devuelve la tabla completa con la nueva columna.

⚠️ **Error frecuente:** modificar la tabla original en vez de trabajar con una copia. El código ya incluye `resultado = tabla.copy()` para proteger el DataFrame original. Si eliminas esa línea, puedes alterar datos que se usan en otras partes del notebook.

✅ **Señal de comprensión:** `compras_predichas` tiene una columna `monto_estimado` y exactamente la misma cantidad de filas que `compras_nuevas`.

---

### 🔷 Sección 3: Un despliegue robusto valida la entrada

🎯 **Objetivo:** crear `predecir_seguro(cantidad, tamano_num)` — una función que valida los rangos de entrada antes de predecir y devuelve un diccionario estructurado.

💡 **Concepto clave — el modelo no debe caerse con datos raros:**
En el Estado, los datos llegan de sistemas heredados, formularios manuales, integraciones entre plataformas. Una `cantidad` de -5, un `tamano_num` de 99 o un campo en blanco son completamente posibles. Un despliegue que falla con esos datos es inutilizable. La solución es validar la entrada antes de predecir y devolver un mensaje claro cuando algo está mal. El diccionario de respuesta (`{"ok": True/False, ...}`) es la forma estándar en que los servicios web comunican éxito o error.

🔍 **Qué hace el código:**
- Verifica que `cantidad` esté entre 1 y 500, y que `tamano_num` esté entre 1 y 4.
- Si cualquier valor está fuera de rango: devuelve `{"ok": False, "error": "Valores fuera de rango"}`.
- Si todo está bien: devuelve `{"ok": True, "monto_estimado": predecir_monto(cantidad, tamano_num)}`.

⚠️ **Error frecuente:** usar `and` en vez de `or` en las condiciones de invalidez. Si escribes `cantidad < 1 and tamano_num > 4`, solo detectarás el caso donde AMBOS están mal al mismo tiempo. Con `or` detectas cualquiera de los dos.

✅ **Señal de comprensión:** `predecir_seguro(100, 2)["ok"] == True` y `predecir_seguro(800, 2)["ok"] == False`. La función maneja ambos casos sin lanzar excepciones.

---

### 🔷 Sección 4: Entregar el resultado

🎯 **Objetivo:** guardar `compras_predichas` en un archivo CSV listo para compartir.

💡 **Concepto clave — el CSV como formato de entrega en la administración:**
El resultado final de un proceso de scoring en el Estado casi siempre es un archivo. El CSV es el mínimo común múltiplo: cualquier funcionario puede abrirlo en Excel, cualquier sistema puede importarlo. `to_csv("predicciones_monto.csv", index=False)` exporta el DataFrame sin el índice (que no tiene significado y solo agrega una columna extra confusa).

🔍 **Qué hace el código:**
- `compras_predichas.to_csv("predicciones_monto.csv", index=False)` guarda la tabla con predicciones en disco.
- El parámetro `index=False` evita que pandas agregue una columna numérica extra que no tiene significado de negocio.

⚠️ **Error frecuente:** no incluir `index=False`. El archivo resultante tendrá una columna extra con números 0, 1, 2... que confunde a quienes abren el archivo en Excel.

✅ **Señal de comprensión:** el archivo `predicciones_monto.csv` existe, tiene la columna `monto_estimado` y el mismo número de filas que `compras_nuevas`.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Tu función de predicción

**Habilidad:** encapsular la predicción del pipeline en una función reutilizable.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* la función recibe dos números y debe devolver uno. Internamente necesita construir un DataFrame, pasarlo al modelo, y extraer la predicción.
2. 🟠 *Pista 2 (técnica):* el DataFrame debe tener exactamente las columnas con que el modelo fue entrenado: `"cantidad"` y `"tamano_num"`. Los valores deben estar en listas: `{"cantidad": [cantidad], "tamano_num": [tamano_num]}`.
3. 🔴 *Pista 3 (estructura):* dentro de la función: (1) `entrada = pd.DataFrame({"cantidad": [cantidad], "tamano_num": [tamano_num]})`, (2) `resultado = modelo.predict(entrada)[0]`, (3) `return round(float(resultado), 1)`.

**Lógica de solución:** creas un DataFrame de una fila con las columnas correctas, lo pasas al pipeline (que aplica el escalado y predice), extraes el primer elemento del array resultado, y lo redondeas a 1 decimal.

---

### ✍️ Ejercicio 2 — Puntuar un lote

**Habilidad:** aplicar el modelo a una tabla completa y agregar la columna de predicciones.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* la tabla `compras_nuevas` ya tiene las columnas `cantidad` y `tamano_num`. El modelo puede recibir toda la tabla de una vez.
2. 🟠 *Pista 2 (técnica):* `modelo.predict(tabla[["cantidad", "tamano_num"]])` devuelve un array con una predicción por fila. Ese array se puede asignar directamente a una nueva columna del DataFrame.
3. 🔴 *Pista 3 (estructura):* dentro de la función: `resultado["monto_estimado"] = modelo.predict(tabla[["cantidad", "tamano_num"]]).round(1)`. Luego `return resultado`.

**Lógica de solución:** el pipeline recibe la tabla con las columnas de features, predice para todas las filas a la vez, y el resultado (array de predicciones) se agrega como nueva columna `monto_estimado`.

---

### ✍️ Ejercicio 3 — Validar la entrada

**Habilidad:** agregar validación de rangos a la función de predicción.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* la función debe verificar DOS condiciones antes de predecir: que `cantidad` esté entre 1 y 500, y que `tamano_num` esté entre 1 y 4. Si alguna falla, devuelve un diccionario con `"ok": False`.
2. 🟠 *Pista 2 (técnica):* la estructura de respuesta es un diccionario Python. Para el caso de error: `{"ok": False, "error": "Valores fuera de rango"}`. Para el caso correcto: `{"ok": True, "monto_estimado": predecir_monto(cantidad, tamano_num)}`.
3. 🔴 *Pista 3 (estructura):* `if not (1 <= cantidad <= 500) or not (1 <= tamano_num <= 4): return {"ok": False, "error": "Valores fuera de rango"}`. Después del if: `return {"ok": True, "monto_estimado": predecir_monto(cantidad, tamano_num)}`.

**Lógica de solución:** primero validar (con `if` + `return` temprano), luego predecir. Este patrón se llama "fail fast": si algo está mal, retornas inmediatamente con el error, sin llegar al código de predicción.

---

### ✍️ Ejercicio 4 — Generar el archivo de predicciones

**Habilidad:** exportar el resultado del scoring por lotes a un CSV.

**Pistas progresivas:**
1. 🟡 *Pista 1 (orientación):* ya tienes `compras_predichas` (el DataFrame con la columna `monto_estimado`). Solo necesitas guardarlo en disco con un nombre específico.
2. 🟠 *Pista 2 (técnica):* pandas tiene el método `.to_csv(nombre_archivo, index=False)`. El parámetro `index=False` evita que se agregue una columna numérica extra sin significado.
3. 🔴 *Pista 3 (estructura):* `compras_predichas.to_csv("predicciones_monto.csv", index=False)`. Eso es todo. El chequeo verifica que el archivo exista y tenga la columna correcta.

**Lógica de solución:** una sola línea de código. La clave es recordar el nombre exacto del archivo (`predicciones_monto.csv`) y el parámetro `index=False`.

---

## 7. Profundización: El despliegue en el contexto del Estado digital

Lo que construiste en este módulo — función de predicción con validación, scoring por lotes, archivo de resultados — es la base sobre la que se construyen los despliegues más avanzados.

**Las tres formas de despliegue y su relevancia para el Estado:**

**1. Scoring por lotes (lo que hiciste):**
Ideal para procesos periódicos: cierre mensual de órdenes, actualización semanal de rankings de proveedores, estimación trimestral de presupuestos. El proceso se ejecuta como un script, genera un CSV, y ese CSV alimenta informes y dashboards.

**2. API web (el siguiente nivel):**
Una API expone la función `predecir_seguro` a través de una URL. Otros sistemas (el portal de ChileCompra, el sistema de gestión de contratos de un ministerio) pueden consultarla en tiempo real. La implementación típica usa Flask o FastAPI. El cuerpo de la API es literalmente tu función `predecir_seguro` envuelta en un endpoint HTTP.

**3. App web simple (Gradio):**
Permite que personas no técnicas usen el modelo a través de una página web con campos de formulario. Una analista de la unidad de compras puede escribir `cantidad: 200, tamano_num: 2` y ver el resultado sin saber nada de Python.

**Lo más importante: cuidar el modelo en el tiempo.**

Un modelo entrenado en datos de 2023 puede degradarse en 2025 si los patrones de compra cambiaron. Los dos pilares del mantenimiento son:
- **Monitoreo:** comparar periódicamente las predicciones con los valores reales. Si el MAE empieza a crecer, es señal de degradación.
- **Reentrenamiento:** volver a entrenar el modelo con datos frescos. Con el pipeline de R2-08, el proceso es reproducible y documentado.

**Transparencia como requisito público:** cualquier modelo usado para apoyar decisiones en el Estado debe tener una **model card** que documente qué datos usó, cuál es su desempeño, sus limitaciones, y quién responde por él. Esto conecta directamente con el módulo R2-CAP.

---

## 8. Conexión con el cuaderno siguiente

| Tema | En `leccion.ipynb` | Lo que viene en R2-10 y R2-CAP |
|---|---|---|
| Predicción sobre datos estáticos | Tabla con órdenes ya existentes | En R2-10: datos ordenados en el tiempo (series temporales) |
| Modelo de regresión | Predice montos de compras individuales | En R2-CAP: ciclo completo con tu propio dataset y model card |
| Validación de entrada | Rangos numéricos simples | En R2-CAP: documentación completa de limitaciones del modelo |
| Despliegue básico | Función + CSV | Conceptual: API, Gradio, monitoreo, reentrenamiento |

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la diferencia entre predicción en línea y por lotes?

- a) La predicción en línea usa un modelo mejor
- b) **La predicción en línea responde un caso al instante; el lote procesa muchos casos a la vez ✅**
- c) El lote es más preciso que la predicción individual
- d) Son lo mismo, solo cambia el nombre

**Explicación:** el mismo modelo puede usarse para ambos. La diferencia es el flujo de trabajo: en línea es una consulta puntual en tiempo real; por lotes es un proceso periódico que procesa muchos casos de una vez.

---

**Pregunta 2:** Tu función `predecir_monto` recibe `cantidad=100` y `tamano_num=2`. ¿Cómo debe construir el DataFrame para el pipeline?

- a) `pd.DataFrame([100, 2])`
- b) `pd.DataFrame({"cantidad": 100, "tamano_num": 2})`
- c) **`pd.DataFrame({"cantidad": [100], "tamano_num": [2]})` ✅**
- d) `pd.DataFrame([[100, 2]])`

**Explicación:** pandas necesita iterables para crear DataFrames con nombres de columna. `[100]` es una lista de un elemento; `100` solo es un escalar y genera error. La opción d) crea un DataFrame pero sin nombres de columna, lo que rompería el pipeline.

---

**Pregunta 3:** ¿Por qué `predecir_seguro` devuelve un diccionario en vez de solo el número?

- a) Porque los diccionarios son más rápidos que los números
- b) **Para comunicar tanto el resultado como si la predicción fue exitosa o falló la validación ✅**
- c) Por convención de Python
- d) Porque joblib requiere diccionarios

**Explicación:** el diccionario `{"ok": True/False, ...}` permite que quien llama la función sepa si tuvo éxito y, en caso de falla, cuál fue el error. Es el patrón estándar de respuesta en APIs web (JSON) y en integraciones entre sistemas.

---

**Pregunta 4:** Exportas `compras_predichas` con `to_csv("predicciones_monto.csv")` (sin `index=False`). ¿Qué problema genera?

- a) El archivo no se crea
- b) Los datos se corrompen
- c) **Se agrega una columna extra numérica sin significado (el índice del DataFrame) ✅**
- d) El archivo es demasiado grande

**Explicación:** por defecto, pandas incluye el índice del DataFrame (0, 1, 2, 3...) como primera columna del CSV. Esa columna no tiene significado de negocio y confunde a quienes abren el archivo en Excel. `index=False` la elimina.

---

**Pregunta 5:** ¿Por qué es importante el monitoreo de un modelo en producción en el Estado?

- a) Para que el código no tenga bugs
- b) Para cumplir con la ley de datos
- c) **Porque los patrones en los datos cambian con el tiempo y el modelo puede degradarse sin darse cuenta ✅**
- d) Para mejorar la velocidad del servidor

**Explicación:** un modelo entrenado con datos de 2023 puede volverse impreciso en 2025 si los proveedores, las categorías de compra, o los montos cambiaron significativamente. El monitoreo detecta esa degradación antes de que cause problemas en decisiones reales.

---

## 10. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Despliegue (deployment)** | Hacer que el modelo sea usado por otros en la práctica | Publicar un formulario o servicio para que otros lo usen |
| **Predicción en línea** | Una consulta, una respuesta, al instante | Funcionario llena formulario, sistema responde en tiempo real |
| **Predicción por lotes** | Tabla de muchos casos procesados de una vez | Correr una macro sobre toda la planilla de cierre mensual |
| **Función de predicción** | Función que recibe parámetros y devuelve estimación | Formulario con cálculo automático encapsulado |
| **Validación de entrada** | Verificar que los datos recibidos están en rangos válidos | Control de integridad antes de ingresar al sistema |
| **Diccionario de respuesta** | Estructura `{"ok": True, "resultado": ...}` | Respuesta estructurada del sistema: éxito o error con detalle |
| **Batch scoring** | Aplicar el modelo a una tabla entera en una ejecución | Ejecución masiva de fórmulas sobre toda la planilla |
| **API web** | Servicio accesible vía URL que expone la predicción | Servicio web al que otros sistemas se conectan para consultar |
| **Gradio** | Librería para crear apps web simples de ML sin servidor | Formulario web autogenerado para que no-técnicos usen el modelo |
| **Monitoreo** | Vigilar si las predicciones siguen siendo buenas con el tiempo | Auditoría periódica del modelo contra la realidad |
| **Reentrenamiento** | Actualizar el modelo con datos más recientes | Actualizar las tablas de parámetros con datos del año en curso |
| **Model card** | Documento que describe el modelo, sus datos, límites y uso responsable | Ficha técnica del instrumento de gestión con sus condiciones de uso |

---

## 11. Conexión con el Módulo Siguiente

**Módulo siguiente:** R2-10 · Series temporales

Con este módulo completaste el tronco principal del ciclo de machine learning: datos → features → modelo → evaluación → pipeline → despliegue. Eso es un logro enorme.

R2-10 abre una nueva dimensión: el **tiempo**. Hasta ahora cada fila de datos era independiente (una orden de compra no "sabía nada" de la orden anterior). En una serie temporal, el orden importa: el gasto de enero predice algo sobre febrero, y la tendencia de los últimos 5 años dice algo sobre el año que viene.

**Serás capaz de:** cargar la serie de gasto anual de ChileCompra, graficarla, medir su crecimiento, construir tres tipos de pronóstico y elegir el mejor con backtest.

**Preconcepto clave para llevar:** en R2-10, el "modelo" ya no es un clasificador ni un regresor de scikit-learn — son fórmulas matemáticas simples (promedio de crecimiento, regresión lineal) aplicadas a una secuencia temporal. La evaluación honesta (hold-out / backtest) sigue siendo el mismo principio que aprendiste en R2-07.

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos de Chile · Formación Pública*
*Contenido bajo licencia CC BY 4.0*
