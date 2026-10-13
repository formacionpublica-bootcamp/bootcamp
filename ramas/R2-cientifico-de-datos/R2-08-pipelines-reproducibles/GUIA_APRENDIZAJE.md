# Guía de Aprendizaje — R2-08 · Pipelines reproducibles

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 8 · Semana 13

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-08 · Pipelines reproducibles |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 3 horas |
| **Nivel** | Intermedio-avanzado — requiere R2-05 y R2-07 |
| **Prerrequisitos** | Bosques aleatorios (R2-05), fuga de datos y `TimeSeriesSplit` (R2-07), faltantes reales del aire (R2-01) |
| **Competencia de salida** | Empaquetar preprocesamiento y modelo en un pipeline reproducible, validado sin fugas y guardado para reutilizarlo |
| **Entregable** | Las 5 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 y meteorología diarios 2020–2025, 14 estaciones SINCA). Profundización: `matricula.csv` (10.945 establecimientos con matrícula 2025, MINEDUC) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Un análisis que solo funciona en el computador de quien lo hizo, el día que lo hizo, no es un activo del servicio: es un riesgo. Cuando esa persona se va, nadie sabe qué columnas se rellenaron, con qué valor, en qué orden, ni por qué el número del informe no se puede volver a obtener.

Este módulo convierte un modelo en una **pieza de infraestructura**: un solo objeto que contiene **toda** la preparación de los datos y el modelo, que se entrena con una función con semilla (mismo resultado hoy y en un año, en tu equipo o en el de Contraloría) y que se guarda en un archivo para que otro sistema lo use (R2-09).

El dato lo exige: de las 14 estaciones SINCA, **6 no miden meteorología**; en el entrenamiento, la temperatura falta en el **51,3 %** de las filas y la humedad en el **58,2 %** (incluidas las humedades de 0 % imposibles que viste en R2-01). Un modelo directo se cae. Un pipeline lo resuelve —y lo resuelve **igual** cada vez.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el Estado |
|----------|-----------|----------------------|
| **`SimpleImputer`** | Rellena faltantes (aquí con la mediana del entrenamiento) | Completar celdas vacías con un criterio escrito |
| **`StandardScaler`** | Media 0, desviación 1 | Llevar todo a un índice común |
| **`OneHotEncoder`** | Una columna 0/1 por categoría | Casillas marcables por estación |
| **`handle_unknown="ignore"`** | No falla ante una categoría nueva | Un formulario que acepta «otra» |
| **`ColumnTransformer`** | Aplica una receta distinta a cada grupo de columnas | La oficina de partes que deriva cada documento |
| **`Pipeline`** | Encadena pasos en un solo objeto con `fit`/`predict` | Un procedimiento escrito que siempre se sigue igual |
| **Persistencia** | La predicción «mañana igual que hoy» | La línea base más difícil de batir en contaminación |
| **Semilla (`random_state`)** | Fija el azar | Que el sorteo se pueda repetir ante notario |
| **`joblib.dump` / `load`** | Guarda y recarga el objeto entrenado | Archivar el expediente completo, no solo la resolución |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué es una fuga de datos y dar un ejemplo (R2-07) | ☐ |
| Usar `cross_val_score` con `TimeSeriesSplit` | ☐ |
| Entrenar un `RandomForestRegressor` y medir su MAE | ☐ |
| Escribir una función con `def` que reciba argumentos y devuelva dos valores | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Construir `X` (5 numéricas + `estacion`) e `y` (el PM2.5 del día) con un **corte temporal**: 2020–2024 para entrenar (24.694 días-estación) y 2025 para probar (4.611).

💡 **Concepto clave:** Las humedades de 0 % se marcan como `NaN` antes de todo: es una decisión de limpieza declarada (R2-01), no algo que el pipeline deba adivinar. La tarea usa el PM2.5 del día anterior y la meteorología del día (que en la práctica vendría del pronóstico meteorológico).

La celda de ilustración intenta entrenar una regresión lineal con los datos crudos y **falla**: la columna `estacion` es texto, y además hay `NaN`. Ese error es la motivación del módulo.

---

### Sección 1 · El ColumnTransformer

🎯 **Objetivo:** Definir una receta para las numéricas (imputar → escalar) y otra para la categórica (one-hot).

💡 **Concepto clave:** El resultado tiene **19 columnas** (5 numéricas + 14 estaciones) y **cero** `NaN`. La mediana con que se imputa se calcula **solo con el entrenamiento**: el pipeline la recuerda y la aplica igual a la prueba y a los datos nuevos.

⚠️ **Error frecuente:** Invertir el orden imputar/escalar: `StandardScaler` no sabe qué hacer con `NaN`.

---

### Sección 2 · El pipeline completo

🎯 **Objetivo:** Encadenar preprocesador + bosque y compararlo con la persistencia.

💡 **Concepto clave:** MAE del pipeline **3,76 µg/m³** vs **4,18** de «mañana igual que hoy». La mejora es modesta y honesta: la persistencia es una línea base muy dura en contaminación, y superarla en datos de 2025 que el modelo nunca vio es una buena noticia.

✅ **Señal de que entendiste:** Puedes explicar por qué no basta con reportar «MAE 3,76» sin la línea base al lado.

---

### Sección 3 · Validación temporal sin fugas

🎯 **Objetivo:** Pasar el pipeline completo a `cross_val_score` con `TimeSeriesSplit(5)`.

💡 **Concepto clave:** MAE por fold entre **3,76 y 4,63**, promedio **4,14 µg/m³**. En cada fold el imputador y el escalador se reajustan solo con el entrenamiento de ese fold: la fuga queda cerrada **por diseño**, no por disciplina. sklearn entrega el error con signo negativo (`neg_mean_absolute_error`) porque internamente siempre «maximiza»: hay que cambiarle el signo.

---

### Sección 4 · Una función de entrenamiento con semilla

🎯 **Objetivo:** Escribir `entrenar(X_tr, y_tr, X_te, y_te, semilla)` que construya, entrene y evalúe todo desde cero.

💡 **Concepto clave:** Con semilla 42, dos ejecuciones dan exactamente **3,7598**; con semilla 7, **3,7726**. La semilla no cambia «la verdad», cambia el azar del bosque: por eso se fija y se **declara**. Que la función construya el pipeline adentro evita depender de variables sueltas modificadas más arriba.

---

### Sección 5 · Guardar, recargar y usar

🎯 **Objetivo:** Guardar `modelo_aire.joblib`, recargarlo y predecir dos días nuevos.

💡 **Concepto clave:** El archivo pesa unos 4 MB y lo crea el propio notebook (no hace falta descargarlo). El pipeline recargado acepta datos **crudos**: para un día de junio en Cerro Navia con 62 µg/m³ el día anterior estima ≈ **70,4**; para Antofagasta, que no mide meteorología (llega `NaN`), imputa solo y estima ≈ **11,3**.

⚠️ **Error frecuente:** Cargar `.joblib` de origen desconocido. `joblib.load` puede ejecutar código: abre solo archivos propios o de fuentes confiables, y anota la versión de scikit-learn con que se guardó.

---

### Reflexión final

La reflexión pide la lista de lo que alguien necesita, además del `.joblib`, para confiar en el modelo y reentrenarlo. No tiene chequeo: es la base de la documentación del modelo (la *model card* del capstone).

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 1 — Arma el preprocesador

**Pistas progresivas:**
- 🟢 Pista suave: Faltan tres piezas: el imputador, el escalador y el codificador.
- 🟡 Pista media: `SimpleImputer(strategy="median")`, `StandardScaler()`, `OneHotEncoder(handle_unknown="ignore")`.
- 🔴 Pista directa: `("num", Pipeline([("imputar", SimpleImputer(strategy="median")), ("escalar", StandardScaler())]), NUM)` y `("cat", OneHotEncoder(handle_unknown="ignore"), CAT)`.

**¿Qué significa el ✅?** Que el preprocesador produce 19 columnas numéricas sin un solo `NaN`.

---

### Ejercicio 2 — Entrena el pipeline y compáralo con la persistencia

**Pistas progresivas:**
- 🟢 Pista suave: El primer paso del pipeline es el preprocesador del ejercicio 1, con el nombre `"pre"`.
- 🟡 Pista media: `pipe.fit(X_train, y_train)`; la persistencia usa la columna `pm25_ayer` como predicción.
- 🔴 Pista directa: `("pre", preprocesador)`, `mae_pipe = mean_absolute_error(y_test, pipe.predict(X_test))`, `mae_persistencia = mean_absolute_error(y_test, X_test["pm25_ayer"])`.

**¿Qué significa el ✅?** Que el pipeline supera a la línea base más dura (3,76 vs 4,18).

---

### Ejercicio 3 — Validación temporal del pipeline

**Pistas progresivas:**
- 🟢 Pista suave: Es el `cross_val_score` de R2-07, ahora con el pipeline entero.
- 🟡 Pista media: `cv=TimeSeriesSplit(n_splits=5)` y `scoring="neg_mean_absolute_error"`.
- 🔴 Pista directa: `scores = cross_val_score(pipe, X_train, y_train, cv=TimeSeriesSplit(n_splits=5), scoring="neg_mean_absolute_error")` y `mae_cv = -scores.mean()`.

**¿Qué significa el ✅?** Que estimaste el error en el tiempo (4,14 µg/m³) sin ninguna fuga del preprocesamiento.

---

### Ejercicio 4 — Escribe `entrenar()` y comprueba que es reproducible

**Pistas progresivas:**
- 🟢 Pista suave: La semilla que recibe la función tiene que llegar al bosque.
- 🟡 Pista media: `random_state=semilla`; al final, entrenar y devolver dos cosas.
- 🔴 Pista directa: `random_state=semilla`, luego `p.fit(X_tr, y_tr)` y `return p, mean_absolute_error(y_te, p.predict(X_te))`.

**¿Qué significa el ✅?** Que dos ejecuciones con la misma semilla dan un MAE idéntico, igual al del ejercicio 2.

---

### Ejercicio 5 — Guarda `modelo_aire.joblib`, recárgalo y predice

**Pistas progresivas:**
- 🟢 Pista suave: `joblib` tiene una función para guardar y otra para cargar.
- 🟡 Pista media: `joblib.dump(objeto, "archivo")` y `joblib.load("archivo")`.
- 🔴 Pista directa: `joblib.dump(pipe, "modelo_aire.joblib")`, `pipe_cargado = joblib.load("modelo_aire.joblib")` y `pred_nuevos = pipe_cargado.predict(dias_nuevos)`.

**¿Qué significa el ✅?** Que el modelo recargado predice exactamente igual que el original, incluso con meteorología faltante.

---

> 🔬 **En la profundización:** el mismo pipeline con la **matrícula 2025** (MINEDUC): estimar la matrícula total de un establecimiento con sus cursos, si es rural, su dependencia (5 valores) y su región (16). El preprocesador produce 23 columnas; el pipeline baja el MAE de **257** estudiantes (predecir la mediana) a **71**; y el modelo guardado como `modelo_matricula.joblib` no se cae ante una región mal escrita gracias a `handle_unknown="ignore"` — aunque no fallar no es lo mismo que acertar.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la principal ventaja de meter el imputador dentro del pipeline?

- A) Que el código es más corto
- B) Que la mediana se aprende solo del entrenamiento (de cada fold) y se aplica igual a todo lo demás, sin fuga ✅
- C) Que imputa con valores más exactos
- D) Que el modelo entrena más rápido

**Explicación:** Imputar con la mediana de **todos** los datos antes de dividir filtra información de la prueba. El pipeline lo impide por construcción.

---

**Pregunta 2:** ¿Para qué sirve `handle_unknown="ignore"` en el `OneHotEncoder`?

- A) Para eliminar las categorías raras
- B) Para que el modelo no falle si llega una categoría que no vio al entrenar ✅
- C) Para corregir errores de tipeo
- D) Para imputar los `NaN` numéricos

**Explicación:** Sin él, una estación nueva (o una región mal escrita) rompe la predicción. Con él, se codifica como «ninguna conocida»; validar la entrada sigue siendo tu responsabilidad.

---

**Pregunta 3:** Ejecutas `entrenar()` dos veces con `semilla=42` y obtienes MAE distintos. ¿Qué pasó?

- A) Es normal, los bosques son aleatorios
- B) La semilla no está llegando al modelo (o algo fuera de la función cambió entre ejecuciones) ✅
- C) Los datos se corrompieron
- D) joblib alteró el modelo

**Explicación:** Con la semilla bien pasada, el resultado es idéntico. Si no lo es, el proceso no es reproducible y no se puede auditar.

---

**Pregunta 4:** Tu pipeline tiene MAE 3,76 y la persistencia («mañana igual que hoy») 4,18. ¿Cómo lo comunicas?

- A) «El modelo tiene un error de 3,76»
- B) «El modelo reduce el error de la regla más simple de 4,18 a 3,76 µg/m³ en 2025, un año que no vio al entrenar» ✅
- C) «El modelo es 90 % preciso»
- D) No vale la pena: la mejora es pequeña

**Explicación:** Una cifra sin línea base ni contexto de validación no permite decidir. Con ambos, la jefatura entiende cuánto aporta el modelo.

---

**Pregunta 5:** Un colega te manda un `.joblib` por correo para que lo uses. ¿Qué haces?

- A) Lo cargas directo, es solo un modelo
- B) Verificas que venga de una fuente confiable, con su versión de scikit-learn y la forma de reentrenarlo, antes de cargarlo ✅
- C) Lo abres en Excel
- D) Lo renombras a .csv

**Explicación:** `joblib.load` puede ejecutar código, y un modelo sin su receta de entrenamiento no es auditable.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Pipeline** | Pasos encadenados en un solo objeto | Procedimiento escrito y obligatorio |
| **ColumnTransformer** | Receta distinta por tipo de columna | Derivar cada documento a su unidad |
| **Imputar** | Rellenar faltantes con un criterio | Completar con un valor de referencia declarado |
| **One-hot** | Una columna 0/1 por categoría | Casillas por estación o región |
| **Persistencia (línea base)** | Predecir que mañana será igual que hoy | La regla de oficio que el modelo debe superar |
| **Semilla** | Número que fija el azar | Sorteo repetible |
| **Reproducibilidad** | Mismo código + mismos datos = mismo resultado | Un informe que se puede volver a obtener |
| **Persistencia (joblib)** | Guardar el objeto entrenado en disco | Archivar el expediente completo |
| **`.joblib`** | Archivo con el pipeline entrenado | El modelo listo para usar |

---

## 9. Conexión con el Módulo Siguiente

En R2-08 convertiste tu modelo en un objeto ordenado, sin fugas, reproducible y guardado en `modelo_aire.joblib`.

En **R2-09 · Despliegue de modelos** lo pondrás a trabajar: una función de predicción que otros puedan llamar, la puntuación de muchos casos a la vez (por lotes) y la **validación de entradas** — porque, como viste con la región mal escrita, que un modelo no falle no significa que su respuesta tenga sentido.

> 💡 **Pregunta para reflexionar:** El modelo de hoy se entrenó con 2020–2024. ¿Cada cuánto habría que reentrenarlo, y cómo sabrías que llegó el momento?
