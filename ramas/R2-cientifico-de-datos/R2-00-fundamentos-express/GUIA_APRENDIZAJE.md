# Guía de Aprendizaje — R2-00 · Fundamentos express: Python + pandas

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 0 · Semana 1–2

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-00 · Fundamentos express: Python + pandas |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Inicial — cero conocimientos de Python |
| **Prerrequisitos** | Ninguno. Solo una cuenta Google para usar Colab |
| **Competencia de salida** | Manipular un DataFrame de datos públicos desde cero: cargar, inspeccionar, filtrar, seleccionar, ordenar y agregar con `groupby` |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` — PM2.5 diario de 14 estaciones del SINCA (Ministerio del Medio Ambiente), 2020–2025: 30.674 días-estación. Profundización: `matricula.csv` (matrícula 2025 por establecimiento, MINEDUC, 10.945 filas) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Imagina que llega un oficio urgente: *«¿Cuántos días el aire de nuestra región superó la norma en los últimos años, y cuáles fueron los peores?»*. Hasta ahora eso significaba descargar planillas de cada estación, filtrar a mano y rezar para que no hubiera errores de fórmula.

Con Python y pandas lo resuelves en cinco líneas que puedes volver a ejecutar mañana con datos nuevos. Este módulo trabaja con el registro real del **SINCA**: el material particulado fino (**PM2.5**) que miden 14 estaciones, de Alto Hospicio a Temuco, día a día entre 2020 y 2025. La norma chilena (D.S. 12/2011 del MMA) fija **50 µg/m³** como valor para la concentración de 24 horas.

Lo que vas a descubrir con tus propias manos: el PM2.5 **promedio** de todas las estaciones está muy por debajo de 50 (el más alto, El Bosque, promedia 27,5 µg/m³), y sin embargo hubo **1.279 días-estación sobre 50 µg/m³**, con un peor día de **284 µg/m³** (Bomberos, Tocopilla, 11-11-2024). El promedio tranquiliza; el conteo de días sobre el umbral informa. Esa diferencia es exactamente lo que un analista del Estado tiene que saber mostrar.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **DataFrame** | Tabla de datos en memoria (filas × columnas) | Una hoja de cálculo abierta |
| **`pd.read_csv()`** | Carga un archivo .csv como DataFrame | Abrir el archivo descargado |
| **`df.shape` / `df.columns`** | Tamaño y nombres de columnas | Ctrl+Fin y la fila de encabezados |
| **Máscara booleana `df[cond]`** | Filtra las filas que cumplen una condición | Autofiltro «mayor que 50» |
| **`df[["a", "b"]]`** | Selecciona solo ciertas columnas | Ocultar columnas |
| **`sort_values(..., ascending=False)`** | Ordena de mayor a menor | Ordenar Z→A |
| **`groupby().mean()`** | Promedio por grupo | Tabla dinámica con «Promedio de» |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Abrir Google Colab con mi cuenta Google y ejecutar una celda con ▶︎ o `Shift`+`Enter` | ☐ |
| Explicar qué es una tabla con filas (registros) y columnas (campos) | ☐ |
| Leer un mensaje de error sin pánico (es información, no un castigo) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar pandas, matplotlib y `aire_diario.csv` en el DataFrame `df`.

💡 **Concepto clave:** La celda aplica el patrón **«en vivo o caché»**: si el archivo está en la carpeta lo usa; si no (como en Colab), lo baja del repositorio. Debe imprimir `Datos cargados: (30674, 7)`.

⚠️ **Error frecuente:** Saltarse esta celda. Si ves `NameError: name 'df' is not defined`, vuelve arriba y ejecútala.

---

### Sección 1 · Cargar e inspeccionar un DataFrame

🎯 **Objetivo:** Conocer la forma y las columnas antes de tocar nada.

💡 **Concepto clave:** `df.shape` es una tupla `(filas, columnas)` que se puede «desempaquetar» en dos variables. Mira las columnas: `fecha`, `estacion`, `pm25` y cuatro de meteorología. Fíjate en los `NaN` de temperatura en las primeras filas: no es un error del curso, hay estaciones **sin sensor meteorológico** (lo trabajarás en R2-01).

⚠️ **Error frecuente:** Escribir `df.shape()` con paréntesis. `shape` es un atributo, no una función.

---

### Sección 2 · Filtrar filas con una condición

🎯 **Objetivo:** Quedarte con los días-estación con PM2.5 sobre 50 µg/m³.

💡 **Concepto clave:** `df["pm25"] > 50` crea una columna de `True`/`False`; `df[esa_mascara]` devuelve solo las filas `True`. Resultado real: **1.279** días-estación. Los días sin medición (`NaN`) no cumplen la condición y quedan fuera automáticamente.

⚠️ **Error frecuente:** Confundir `=` (asignar) con `==`/`>` (comparar).

✅ **Señal de que entendiste:** Puedes explicar por qué `n_sobre_norma` es mucho menor que 30.674.

---

### Sección 3 · Seleccionar columnas y ordenar

🎯 **Objetivo:** Ver los 10 peores días del registro con solo `fecha`, `estacion` y `pm25`.

💡 **Concepto clave:** Encadenar operaciones: ordenar descendente → `head(10)` → seleccionar columnas. El ranking muestra un patrón claro: el peor día es de **Bomberos (Tocopilla) con 284 µg/m³** el 11-11-2024, y **ocho** de los nueve siguientes son de **Las Encinas Temuco** en invierno (más uno de Nielol, también Temuco) — un patrón invernal consistente con la calefacción a leña.

⚠️ **Error frecuente:** Olvidar `ascending=False`: por defecto se ordena de menor a mayor y verías los días más limpios.

---

### Sección 4 · Agregar: una pregunta, una respuesta

🎯 **Objetivo:** PM2.5 promedio de cada estación.

💡 **Concepto clave:** `groupby` es la tabla dinámica de Python. El resultado tiene 14 valores; el más alto es **El Bosque (27,5 µg/m³)** y el más bajo **Cuncumen (5,4 µg/m³)**. El gráfico agrega la línea de 50 µg/m³: ninguna barra la alcanza, aunque todas las estaciones del centro-sur tuvieron cientos de días sobre ella.

✅ **Señal de que entendiste:** Puedes explicar por qué «ninguna estación promedia sobre 50» no significa «el aire está bien».

---

### Reflexión final

La reflexión no tiene celda de chequeo: pide explicar a una jefatura por qué el promedio esconde los episodios. La respuesta es mostrar **cuántos días** se superó el umbral, y **dónde y cuándo**.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Inspecciona la tabla

**Pistas progresivas:**
- 🟢 Pista suave: `df.shape` entrega dos números a la vez; puedes recibirlos en dos variables.
- 🟡 Pista media: `a, b = df.shape` y `list(...)` convierte las columnas en lista.
- 🔴 Pista directa: `n_filas, n_cols = df.shape` y `columnas = list(df.columns)`.

**¿Qué significa el ✅?** Que conoces el tamaño (30.674 × 7) y que existen las columnas `pm25` y `estacion`.

---

### Ejercicio 2 — Filtra los días con PM2.5 sobre 50

**Pistas progresivas:**
- 🟢 Pista suave: Primero arma la condición sobre la columna `pm25`; después pásala entre corchetes al DataFrame.
- 🟡 Pista media: `df["pm25"] > 50` es la máscara.
- 🔴 Pista directa: `sobre_norma = df[df["pm25"] > 50]`.

**¿Qué significa el ✅?** Que todas las filas filtradas superan 50 µg/m³ y no se te escapó ninguna (1.279).

---

### Ejercicio 3 — Top 10 días con más PM2.5

**Pistas progresivas:**
- 🟢 Pista suave: Ordena, recorta y elige columnas, en ese orden.
- 🟡 Pista media: `.sort_values("pm25", ascending=False).head(10)` y luego `[["fecha", "estacion", "pm25"]]`.
- 🔴 Pista directa: `top = df.sort_values("pm25", ascending=False).head(10)[["fecha", "estacion", "pm25"]]`.

**¿Qué significa el ✅?** Que el primer valor es el máximo del registro (284) y la lista viene en orden decreciente.

---

### Ejercicio 4 — PM2.5 promedio por estación

**Pistas progresivas:**
- 🟢 Pista suave: Agrupa por la columna de la estación y calcula un promedio de `pm25`.
- 🟡 Pista media: `df.groupby("columna_grupo")["columna_valor"].mean()`.
- 🔴 Pista directa: `pm25_estacion = df.groupby("estacion")["pm25"].mean()`.

**¿Qué significa el ✅?** Que tienes un valor por cada una de las 14 estaciones, listo para comparar.

---

> 🔬 **En la profundización:** las mismas herramientas sobre otro dato del Estado — la **matrícula escolar 2025** (MINEDUC, 10.945 establecimientos). **Filtros combinados** con `&` (hay **1.730** establecimientos rurales municipales), **`value_counts`** para ver cómo se reparten por dependencia (5.379 particulares subvencionados, 3.194 municipales, 1.707 de Servicios Locales de Educación…) y una primera **columna derivada**, `alumnos_por_curso` (mediana 19,4), el preludio del feature engineering de R2-02.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué devuelve `df.shape`?

- A) La lista de columnas
- B) Una tupla con el número de filas y de columnas ✅
- C) Solo el número de filas
- D) Un resumen estadístico

**Explicación:** `(filas, columnas)`. Para solo las filas, `len(df)`.

---

**Pregunta 2:** ¿Qué línea filtra correctamente los días con PM2.5 sobre 50?

- A) `df["pm25"] = 50`
- B) `df.filter("pm25" > 50)`
- C) `df[df["pm25"] > 50]` ✅
- D) `df.where("pm25", 50)`

**Explicación:** La máscara booleana va entre corchetes del DataFrame. La opción A asigna (con un solo `=`), no filtra.

---

**Pregunta 3:** Quieres los 5 peores días. ¿Qué código es correcto?

- A) `df.sort_values("pm25").head(5)`
- B) `df.sort_values("pm25", ascending=False).head(5)` ✅
- C) `df.head(5).sort_values("pm25", ascending=False)`
- D) `df.sort_values("pm25", ascending=False).tail(5)`

**Explicación:** Primero ordenar descendente, después recortar. La C ordena solo 5 filas cualquiera.

---

**Pregunta 4:** Ninguna estación promedia más de 50 µg/m³. ¿Qué conclusión es correcta?

- A) Ninguna estación tuvo días sobre la norma
- B) El promedio puede ocultar episodios: hay que contar los días sobre el umbral ✅
- C) La norma está mal calculada
- D) Los datos están corruptos

**Explicación:** Con 1.279 días-estación sobre 50 µg/m³, el promedio anual bajo convive con episodios graves en invierno.

---

**Pregunta 5:** ¿Qué hace `df.groupby("estacion")["pm25"].mean()`?

- A) Filtra las estaciones con PM2.5 promedio
- B) Calcula el promedio general ignorando estaciones
- C) Calcula el PM2.5 promedio de cada estación por separado ✅
- D) Ordena las estaciones por PM2.5

**Explicación:** `groupby` separa en grupos y `.mean()` resume cada uno: una fila por estación.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **DataFrame** | Tabla en memoria | Una planilla Excel abierta |
| **PM2.5** | Material particulado fino (≤ 2,5 micrones), en µg/m³ | Lo que mide el SINCA y gatilla episodios críticos |
| **Norma de 24 h** | 50 µg/m³ (D.S. 12/2011 MMA) | El umbral de referencia del informe |
| **Máscara booleana** | Columna `True`/`False` que selecciona filas | El autofiltro |
| **`sort_values`** | Ordena por una columna | Ordenar A→Z / Z→A |
| **`head(n)`** | Primeras n filas | Mirar el comienzo de la tabla |
| **`groupby`** | Agrupa y resume por categoría | Tabla dinámica |
| **`NaN`** | Valor faltante | La celda vacía de la planilla |
| **Días-estación** | Una fila = un día en una estación | La unidad del registro SINCA |

---

## 9. Conexión con el Módulo Siguiente

En R2-00 aprendiste el vocabulario base de pandas resolviendo preguntas reales sobre el aire: cuántos días sobre la norma, cuáles fueron los peores y qué estaciones están más expuestas.

En **R2-01 · Datos: traer, cruzar y limpiar** vas a cruzar estas mediciones con el **catálogo de estaciones** (comuna, región, coordenadas), convertir las fechas a fechas de verdad y enfrentar los **faltantes reales**: estaciones sin sensor de temperatura, días sin PM2.5 y una humedad imposible — tomando y declarando cada decisión de limpieza.

> 💡 **Pregunta para reflexionar:** Si tu jefatura solo mira promedios, ¿qué otros indicadores de tu servicio podrían estar escondiendo «episodios» importantes?
