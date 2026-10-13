# Guía de Aprendizaje — R1-02 · Exploración con pandas

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 2 · Semana 3

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-02 · Exploración con pandas |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Básico — requiere R1-00 y R1-01 |
| **Prerrequisitos** | Variables, listas, funciones; cargar un CSV |
| **Competencia de salida** | Explorar cualquier dataset público con pandas: inspeccionar, seleccionar, filtrar, contar y resumir |
| **Entregable** | Las 5 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula.csv` — matrícula oficial 2025 (MINEDUC). Profundización: `establecimientos.csv` — Servicio Médico Legal (datos.gob.cl) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Este es el módulo donde pandas reemplaza al ratón. Todo lo que haces en Excel con clics — ocultar columnas, aplicar filtro, tabla dinámica rápida, mirar las sumas del pie de página — aquí se escribe en una línea de código que queda **documentada y repetible**.

La diferencia práctica es enorme: el filtro de Excel que aplicaste ayer nadie sabe reproducirlo; el `df[df["region"] == "Maule"]` de hoy queda escrito, se audita y se corre de nuevo el próximo año con el archivo nuevo. En un servicio público, donde los análisis se heredan entre funcionarios, esa trazabilidad vale más que la velocidad.

Las cinco operaciones de este módulo — inspeccionar, seleccionar, filtrar, contar, resumir — son el 80% del trabajo exploratorio real con datos. El resto del curso las combina.

---

## 3. Mapa Conceptual del Módulo

| Operación pandas | ¿Qué hace? | Equivalente en Excel |
|------------------|-----------|----------------------|
| **`df.shape` / `len(df)`** | Dimensiones de la tabla | Mirar la barra de estado |
| **`df.columns`** | Nombres de las columnas | La fila de encabezados |
| **`df.head()`** | Primeras filas | El primer pantallazo |
| **`df["col"]`** | Una columna (Serie) | Seleccionar una columna |
| **`df[["a", "b"]]`** | Varias columnas (tabla) | Ocultar las demás columnas |
| **`df[df["col"] == v]`** | Filas que cumplen la condición | El botón de filtro |
| **`value_counts()`** | Conteo por categoría, ordenado | Tabla dinámica de conteo |
| **`.mean() / .max() / .min()`** | Estadísticos de una columna | Las sumas del pie de página |
| **`.idxmax()` + `.loc`** | Qué fila tiene el máximo | Ordenar y mirar la primera |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué es una variable y una lista | ☐ |
| Escribir una función con `def` y `return` | ☐ |
| Cargar un CSV con `pd.read_csv` | ☐ |

Si respondiste No a alguna, vuelve a R1-00 y R1-01 antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar la matrícula 2025 como DataFrame.

💡 **Concepto clave:** Un **DataFrame** es la planilla en memoria: filas (establecimientos) × columnas (atributos). Cada fila de este dataset es un establecimiento educacional real de Chile, con su dependencia, comuna y cuántos estudiantes tiene.

✅ **Señal de que entendiste:** `df.head()` muestra la tabla con `rbd`, `nombre`, `dependencia`, `mat_total`…

---

### Sección 1 · Auditoría visual

🎯 **Objetivo:** Saber qué tienes antes de calcular nada.

💡 **Concepto clave:** La disciplina profesional: **nunca** calcules sobre una tabla que no has inspeccionado. `len(df)` (o `df.shape`) te dice el tamaño; `df.columns` los nombres exactos — con sus mayúsculas y guiones bajos, que necesitarás escribir bien después.

⚠️ **Error frecuente:** `KeyError` por escribir una columna «de memoria»: `Mat_Total` no es `mat_total`.

✅ **Señal de que entendiste:** Sabes decir cuántos establecimientos hay (10.945) y qué columnas existen, sin abrir el CSV en Excel.

---

### Sección 2 · Seleccionar columnas

🎯 **Objetivo:** Crear una vista con solo las columnas que importan.

💡 **Concepto clave:** El **doble corchete**: `df["col"]` devuelve una columna (Serie); `df[["a", "b", "c"]]` devuelve una tabla con esas columnas. La lista interior es exactamente eso: una lista de nombres, como las de R1-00.

✅ **Señal de que entendiste:** `vista` tiene las mismas 10.945 filas pero solo 3 columnas.

---

### Sección 3 · Filtrar filas

🎯 **Objetivo:** Quedarte solo con los establecimientos del Maule.

💡 **Concepto clave:** `df["region"] == "Maule"` produce una columna de `True/False` (una por fila); ponerla dentro de `df[...]` selecciona las filas con `True`. Es el botón de filtro de Excel, pero componible: mañana le agregas otra condición con `&`.

✅ **Señal de que entendiste:** `maule` solo contiene filas con región Maule, y puedes cambiar la región sin tocar nada más.

---

### Sección 4 · Contar por categoría

🎯 **Objetivo:** ¿Cuántos establecimientos hay de cada dependencia?

💡 **Concepto clave:** `value_counts()` es la tabla dinámica de conteo en una llamada: agrupa por valor único y cuenta, ordenando de mayor a menor. El resultado es una Serie indexada por categoría: `por_dependencia["Municipal"]` extrae un valor concreto.

✅ **Señal de que entendiste:** La suma de todos los conteos da el total de establecimientos — nadie se pierde.

---

### Sección 5 · Estadísticos rápidos

🎯 **Objetivo:** Promedio, máximo y el nombre del establecimiento más grande.

💡 **Concepto clave:** `.mean()`, `.max()`, `.min()` resumen una columna numérica. El paso extra profesional: `.idxmax()` devuelve el **índice** de la fila con el máximo, y `df.loc[idx, "nombre"]` recupera su nombre. Saber *cuál* es el máximo suele importar más que saber *cuánto* vale.

✅ **Señal de que entendiste:** Puedes nombrar el establecimiento más grande de Chile y decir su matrícula.

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 1 — Inspecciona la tabla

**Pistas progresivas:**
- 🟢 Pista suave: Una función de Python cuenta elementos; un atributo del DataFrame lista las columnas.
- 🟡 Pista media: `len(df)` y `df.columns` (conviértelo a lista).
- 🔴 Pista directa: `n_establecimientos = len(df)` y `columnas = list(df.columns)`.

**¿Qué significa el ✅?** Que conoces el tamaño de la tabla y sus columnas — la auditoría mínima antes de cualquier análisis.

---

### Ejercicio 2 — Crea una vista con nombre, comuna y matrícula

**Pistas progresivas:**
- 🟢 Pista suave: Para varias columnas necesitas pasar una lista de nombres.
- 🟡 Pista media: La lista va dentro de los corchetes: doble corchete.
- 🔴 Pista directa: `vista = df[["nombre", "comuna", "mat_total"]]`.

**¿Qué significa el ✅?** Que la vista tiene exactamente esas 3 columnas en ese orden, con todas las filas.

---

### Ejercicio 3 — Filtra los establecimientos del Maule

**Pistas progresivas:**
- 🟢 Pista suave: La condición va dentro de los corchetes del DataFrame.
- 🟡 Pista media: `df[df["region"] == "Maule"]` y cuentas con `len(...)`.
- 🔴 Pista directa: `maule = df[df["region"] == "Maule"]` y `n_maule = len(maule)`.

**¿Qué significa el ✅?** Que el conteo coincide con la suma de la condición booleana, y el filtrado solo contiene el Maule.

---

### Ejercicio 4 — Cuenta establecimientos por dependencia

**Pistas progresivas:**
- 🟢 Pista suave: Hay un método que cuenta por categoría en una llamada.
- 🟡 Pista media: `df["dependencia"].value_counts()`; para un valor concreto, indexa la Serie con el nombre.
- 🔴 Pista directa: `por_dependencia = df["dependencia"].value_counts()` y `n_municipales = int(por_dependencia["Municipal"])`.

**¿Qué significa el ✅?** Que el conteo total cuadra con las filas y extrajiste bien el valor de «Municipal».

---

### Ejercicio 5 — Estadísticos de la matrícula

**Pistas progresivas:**
- 🟢 Pista suave: Son dos métodos de la columna numérica; el nombre del más grande ya está resuelto en el código.
- 🟡 Pista media: `.mean()` para el promedio, `.max()` para el máximo (conviértelo a entero).
- 🔴 Pista directa: `promedio = df["mat_total"].mean()` y `maximo = int(df["mat_total"].max())`.

**¿Qué significa el ✅?** Que tus estadísticos coinciden con los de pandas y sabes qué establecimiento es el mayor del país.

---

> 🔬 **En la profundización** cambia el dominio: los **establecimientos del Servicio Médico Legal** de Chile (datos.gob.cl). Mismas cinco operaciones — `value_counts` por región, estadísticos de latitud (¿cuál es el SML más austral?) y una función de consulta `cuantos_en()`. Si las resuelves sin volver a la lección, la técnica ya es tuya.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué diferencia hay entre `df["region"]` y `df[["region"]]`?

- A) Ninguna
- B) El primero devuelve una Serie (columna suelta); el segundo, un DataFrame de una columna ✅
- C) El segundo da error
- D) El primero es más lento

**Explicación:** Corchete simple = Serie; doble corchete (lista adentro) = tabla. Importa porque algunos métodos existen en una y no en la otra.

---

**Pregunta 2:** ¿Qué produce la expresión `df["region"] == "Maule"` por sí sola?

- A) Las filas del Maule
- B) Una Serie de True/False, una por fila ✅
- C) El número de filas del Maule
- D) Un error si hay otras regiones

**Explicación:** La comparación produce la «máscara» booleana. Recién al ponerla dentro de `df[...]` se seleccionan las filas donde es True.

---

**Pregunta 3:** ¿Qué devuelve `df["dependencia"].value_counts()`?

- A) El número de dependencias distintas
- B) Una Serie con cada categoría y cuántas filas tiene, ordenada de mayor a menor ✅
- C) Las filas duplicadas
- D) La dependencia más común solamente

**Explicación:** Es conteo por categoría con orden incluido. Para el número de categorías distintas existe `nunique()`.

---

**Pregunta 4:** Quieres saber el NOMBRE del establecimiento con mayor matrícula. ¿Qué usas?

- A) `df["mat_total"].max()`
- B) `df.loc[df["mat_total"].idxmax(), "nombre"]` ✅
- C) `df["nombre"].max()`
- D) `df.sort_values("nombre").head(1)`

**Explicación:** `.max()` da el valor; `.idxmax()` da la fila del valor, y `.loc[fila, "nombre"]` recupera el atributo que buscas. (La C daría el nombre alfabéticamente mayor — un clásico error silencioso.)

---

**Pregunta 5:** ¿Por qué inspeccionar (`shape`, `columns`, `head`) antes de calcular?

- A) Es opcional si el archivo es conocido
- B) Porque los cálculos sobre columnas mal escritas o datos inesperados fallan o, peor, dan resultados silenciosamente incorrectos ✅
- C) Para que el notebook se vea más largo
- D) Solo es necesario con archivos grandes

**Explicación:** El `KeyError` es el error amable; el peligroso es calcular sobre la columna equivocada sin error. La auditoría visual de 10 segundos previene ambos.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **DataFrame** | Tabla de pandas: filas × columnas | La planilla en memoria |
| **Serie** | Una columna con índice | Una columna de la planilla |
| **`shape`** | (filas, columnas) | Dimensiones de la tabla |
| **`head()`** | Primeras 5 filas | El vistazo inicial |
| **Máscara booleana** | Serie de True/False que filtra | El criterio del filtro |
| **`value_counts()`** | Conteo por categoría ordenado | Tabla dinámica exprés |
| **`nunique()`** | Número de valores distintos | «¿Cuántas regiones hay?» |
| **`idxmax()`** | Índice de la fila con el máximo | «¿Quién es el mayor?» |
| **`loc[fila, col]`** | Acceso por etiqueta a una celda | La celda exacta de la planilla |
| **`KeyError`** | La columna no existe (revisa el nombre) | Error de tipeo en el encabezado |

---

## 9. Conexión con el Módulo Siguiente

En R1-02 aprendiste a explorar una tabla: inspeccionar, seleccionar, filtrar, contar, resumir. Pero los datos reales del Estado rara vez viven en una sola tabla.

En **R1-03 · Cruzar y resumir tablas** aprenderás el superpoder de pandas: el `merge` — cruzar la matrícula con el directorio de establecimientos por RBD, el equivalente profesional del BUSCARV, más el `groupby` en serio para responder preguntas que ninguna tabla responde sola.

> 💡 **Pregunta para reflexionar:** Piensa en dos planillas de tu servicio que hoy cruzas con BUSCARV (o peor, a ojo). ¿Cuál es la columna que las conecta? Esa columna es tu «RBD».
