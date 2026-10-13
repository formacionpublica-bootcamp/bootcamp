# Guía de Aprendizaje — R1-03 · Cruzar y resumir tablas

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 3 · Semana 4

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-03 · Cruzar y resumir tablas |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Básico-intermedio — requiere R1-02 |
| **Prerrequisitos** | Filtrar, `value_counts`, estadísticos de columna |
| **Competencia de salida** | Cruzar tablas del Estado con criterio: merge con llave, inner vs left, auditoría de lo que no calza, groupby tras el cruce |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula_rbd.csv` (conteos por RBD) × `directorio_establecimientos.csv` (catálogo oficial). Profundización: `matricula.csv` × `comunas.csv`, y `parques.csv` |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Los datos del Estado viven repartidos en tablas que se apuntan entre sí por códigos: el RUT conecta al beneficiario con su historial, el código de comuna conecta el programa con el territorio, y el **RBD** conecta la matrícula de una escuela con su identidad. Casi ninguna pregunta de gestión se responde con una tabla sola.

Este módulo enseña el **BUSCARV profesional**: `pd.merge`. Pero la lección más valiosa no es pegar tablas — es qué pasa con **lo que no calza**. Este módulo usa un caso real: al cruzar los conteos de matrícula 2025 con el directorio oficial, quedan **4 establecimientos huérfanos** — reportan estudiantes pero no figuran «funcionando» en el registro. En Excel, el BUSCARV los dejaría como `#N/A` y alguien los borraría sin mirar. Aquí aprenderás a **cazarlos, contarlos y decidir qué hacer con ellos** — que es, literalmente, el trabajo de auditoría de datos del sector público.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Llave** | Columna compartida que conecta dos tablas | La columna que le das a BUSCARV |
| **RBD** | Código único de cada establecimiento | El RUT de las escuelas |
| **`pd.merge(a, b, on=...)`** | Pega a cada fila de `a` las columnas de `b` | BUSCARV para todas las columnas de una vez |
| **`how="inner"`** | Solo las filas que calzan en ambas | Filtrar los #N/A después del BUSCARV |
| **`how="left"`** | Todas las de la izquierda; sin pareja → nulo | Dejar los #N/A visibles |
| **Fila huérfana** | Fila cuya llave no existe en la otra tabla | El #N/A que nadie investiga |
| **`groupby` tras el cruce** | La pregunta real, con las columnas ya unidas | Tabla dinámica sobre la tabla combinada |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar filas con una condición | ☐ |
| Usar `groupby(...).sum()` | ☐ |
| Explicar qué es un valor nulo (`NaN`) y detectarlo con `isna()` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar las DOS tablas: `df_matricula` (10.949 conteos por RBD) y `df_directorio` (10.945 establecimientos oficiales).

💡 **Concepto clave:** Fíjate en los tamaños: **no son iguales**. Esa diferencia de 4 filas no es un error del curso — es el dato real, y es el corazón del ejercicio 3.

---

### Sección 1 · Encontrar la llave

🎯 **Objetivo:** Identificar la columna que ambas tablas comparten.

💡 **Concepto clave:** La llave debe existir en ambas tablas **y significar lo mismo**. Aquí es `rbd`: el Rol Base de Datos, la cédula de identidad de cada establecimiento chileno. Antes de cualquier cruce profesional, la pregunta es siempre: ¿cuál es la llave y es única en cada tabla?

⚠️ **Error frecuente:** Cruzar por nombre («Liceo A-1» vs «LICEO A 1») en vez del código. Los nombres varían; los códigos no. Por eso el Estado usa RBD, RUT, CUT.

---

### Sección 2 · El primer cruce

🎯 **Objetivo:** `pd.merge(df_matricula, df_directorio, on="rbd")`.

💡 **Concepto clave:** El resultado tiene las columnas de **ambas** tablas: cada conteo de estudiantes ahora sabe su nombre, dependencia, región y comuna. Nota que el cruce tiene 10.945 filas — menos que las 10.949 de matrícula: el modo por defecto (`inner`) **botó silenciosamente** las 4 que no calzan. Eso motiva la sección siguiente.

✅ **Señal de que entendiste:** Puedes explicar por qué el cruce tiene menos filas que `df_matricula`.

---

### Sección 3 · Inner vs left: cazar la fila huérfana

🎯 **Objetivo:** Con `how="left"`, conservar las 10.949 y contar las que quedaron con región nula.

💡 **Concepto clave:** `left` mantiene todas las filas de la izquierda; donde la llave no encontró pareja, las columnas de la derecha quedan `NaN`. `df_left["region"].isna().sum()` cuenta las huérfanas: **4 establecimientos reales** con matrícula pero sin estado «funcionando» en el directorio. El inner las bota sin avisar; el left te las muestra. **Auditar es elegir left primero.**

✅ **Señal de que entendiste:** Puedes mostrar las 4 filas huérfanas y decir qué les falta.

---

### Sección 4 · La pregunta real

🎯 **Objetivo:** Con el cruce hecho, responder: ¿qué región concentra los estudiantes?

💡 **Concepto clave:** El cruce es infraestructura; `groupby("region")["mat_total"].sum()` es la respuesta. `idxmax()` te da el nombre de la región líder sin leer la tabla a ojo.

---

### Reflexión final

La pregunta sobre las 4 huérfanas no tiene celda de chequeo porque no tiene respuesta única: incluirlas, excluirlas o reportarlas aparte son decisiones **defendibles si se declaran**. Lo indefendible es no haberlas visto.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Identifica la llave y el tamaño de cada tabla

**Pistas progresivas:**
- 🟢 Pista suave: Compara `df_matricula.columns` con `df_directorio.columns`: ¿cuál se repite?
- 🟡 Pista media: La llave es el código único de los establecimientos. Los tamaños, con `len()`.
- 🔴 Pista directa: `llave = "rbd"`, `n_matricula = len(df_matricula)`, `n_directorio = len(df_directorio)`.

**¿Qué significa el ✅?** Que identificaste la columna común y notaste que las tablas NO miden lo mismo (10.949 vs 10.945).

---

### Ejercicio 2 — Cruza las dos tablas

**Pistas progresivas:**
- 🟢 Pista suave: La función recibe las dos tablas y el nombre de la llave.
- 🟡 Pista media: `pd.merge(izquierda, derecha, on="llave")`.
- 🔴 Pista directa: `df_cruce = pd.merge(df_matricula, df_directorio, on="rbd")` y `n_cruce = len(df_cruce)`.

**¿Qué significa el ✅?** Que el cruce tiene columnas de ambas tablas (`region` y `mat_total` juntas por primera vez).

---

### Ejercicio 3 — Encuentra los establecimientos huérfanos

**Pistas progresivas:**
- 🟢 Pista suave: Es el mismo merge, con un argumento extra que cambia el tipo de cruce. Las huérfanas se reconocen porque su región quedó nula.
- 🟡 Pista media: `how="left"` conserva todo; `isna()` detecta los nulos y `.sum()` los cuenta.
- 🔴 Pista directa: `df_left = pd.merge(df_matricula, df_directorio, on="rbd", how="left")` y `n_huerfanas = int(df_left["region"].isna().sum())`.

**¿Qué significa el ✅?** Que conservaste las 10.949 filas y cazaste las 4 huérfanas reales — la auditoría que el inner escondía.

---

### Ejercicio 4 — Estudiantes por región y la región líder

**Pistas progresivas:**
- 🟢 Pista suave: Es el groupby de siempre, sobre la tabla cruzada, más el método que da el índice del máximo.
- 🟡 Pista media: `groupby("region")["mat_total"].sum().sort_values(ascending=False)` y `.idxmax()`.
- 🔴 Pista directa: `est_por_region = df_cruce.groupby("region")["mat_total"].sum().sort_values(ascending=False)` y `region_top = est_por_region.idxmax()`.

**¿Qué significa el ✅?** Que respondiste una pregunta de gestión que ninguna de las dos tablas podía responder sola.

---

> 🔬 **En la profundización:** el patrón completo en un caso de transferencia — cruzar la matrícula por comuna con la **población comunal** para construir el indicador «estudiantes por 1.000 habitantes» (que solo existe después del cruce), y un groupby directo sobre los **parques nacionales**. Dos fuentes distintas, una llave de texto (`comuna`), y un indicador nuevo: el ciclo completo del análisis territorial.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué el MINEDUC guarda la matrícula y el directorio en tablas separadas conectadas por RBD?

- A) Por limitaciones técnicas antiguas
- B) Para no duplicar los atributos del establecimiento en cada registro; el código conecta sin repetir ✅
- C) Para dificultar el análisis
- D) Porque son de años distintos

**Explicación:** Es el principio de diseño de datos relacionales: la medida en una tabla, el catálogo en otra, el código como puente. Todo el Estado funciona así (RUT, CUT, RBD).

---

**Pregunta 2:** Tu cruce inner tiene menos filas que la tabla izquierda. ¿Qué significa?

- A) Un error de pandas
- B) Algunas llaves de la izquierda no existen en la derecha, y el inner las botó silenciosamente ✅
- C) El merge eliminó duplicados
- D) Faltó ordenar las tablas

**Explicación:** `inner` = intersección. La diferencia de filas ES el dato de auditoría: filas con llave sin pareja.

---

**Pregunta 3:** ¿Cuándo usar `how="left"`?

- A) Nunca, inner es más limpio
- B) Cuando necesitas conservar todas las filas de tu tabla principal y ver explícitamente cuáles no calzaron ✅
- C) Cuando las tablas son grandes
- D) Solo con llaves de texto

**Explicación:** Left es el modo auditoría: lo que no calza queda nulo y contable, en vez de desaparecer.

---

**Pregunta 4:** Tras un cruce, aparecen MÁS filas que en la tabla izquierda. ¿La causa más probable?

- A) pandas agregó filas de relleno
- B) La llave está repetida en la tabla derecha: cada fila izquierda se cruzó con varias parejas ✅
- C) El archivo estaba corrupto
- D) Es lo normal en un left join

**Explicación:** Merge con llaves repetidas multiplica combinaciones (1-a-muchos). Verificar unicidad de la llave en el catálogo es parte del checklist previo.

---

**Pregunta 5:** ¿Qué haces con las 4 filas huérfanas en un informe oficial?

- A) Borrarlas sin mencionarlas
- B) Decidir con criterio (incluir, excluir o reportar aparte) y **declarar la decisión** en el informe ✅
- C) Inventarles una región
- D) Detener el análisis hasta que alguien las corrija

**Explicación:** No hay respuesta única — hay decisiones defendibles y declaradas. Lo indefendible es la opción A: alterar el universo del análisis sin dejar rastro.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Llave (key)** | Columna compartida que conecta tablas | RUT, RBD, código de comuna (CUT) |
| **RBD** | Rol Base de Datos: código único del establecimiento | La cédula de identidad de la escuela |
| **`pd.merge`** | Cruce de dos tablas por una llave | BUSCARV de todas las columnas a la vez |
| **`inner`** | Solo lo que calza en ambas | Intersección |
| **`left`** | Todo lo de la izquierda; sin pareja → nulo | BUSCARV con los #N/A visibles |
| **Fila huérfana** | Llave sin pareja en la otra tabla | El registro que amerita investigación |
| **`isna().sum()`** | Cuenta los nulos | El conteo de #N/A |
| **1-a-muchos** | Una llave de un lado, varias del otro | Una comuna, muchos establecimientos |
| **`reset_index()`** | Convierte el resultado del groupby en tabla | Aplanar la tabla dinámica |

---

## 9. Conexión con el Módulo Siguiente

En R1-03 aprendiste a cruzar con criterio: llave, inner vs left, y la auditoría de lo que no calza — con 4 huérfanas reales del sistema escolar como evidencia.

En **R1-04 · Limpieza de datos** enfrentarás la otra mitad del trabajo sucio: valores imposibles, textos inconsistentes, duplicados y nulos — sobre una versión deliberadamente ensuciada de la matrícula que tendrás que dejar impecable, columna por columna.

> 💡 **Pregunta para reflexionar:** Las 4 huérfanas de hoy eran detectables porque el RBD es un código limpio. ¿Qué pasa en tu servicio cuando la «llave» es un nombre escrito a mano? ¿Cuántas huérfanas invisibles produce eso?
