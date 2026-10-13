# Guía de Aprendizaje — R1-05 · SQL para análisis

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 5 · Semana 6

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-05 · SQL para análisis |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 2 a 3 horas |
| **Nivel** | Básico-intermedio — requiere R1-03 y R1-04 |
| **Prerrequisitos** | Cruzar tablas por una llave (R1-03), `groupby`, mediana |
| **Competencia de salida** | Consultar una base de datos relacional con SQL: `SELECT`, `WHERE`, `ORDER BY`/`LIMIT`, `GROUP BY`, `HAVING`, `JOIN` y `LEFT JOIN ... IS NULL`, combinando SQL y pandas para interpretar |
| **Entregable** | Las 8 celdas de chequeo deben mostrar ✅ |
| **Dataset** | Base SQLite en memoria con dos tablas: `matricula` (`matricula_rbd.csv`, 10.949 conteos por RBD) y `directorio` (`directorio_establecimientos.csv`, 10.945 establecimientos oficiales). Profundización: `parques.csv` (24 parques nacionales, CONAF/SNASPE) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Los sistemas del Estado no guardan sus datos en planillas: los guardan en **bases de datos relacionales**. El SIGE del MINEDUC, los registros de salud, el Registro Social de Hogares, los sistemas de personal: todos se consultan con **SQL**. Cada reporte que alguien te exporta salió de una consulta SQL que otra persona escribió.

Saber SQL te da **acceso directo**: pides exactamente lo que necesitas («los establecimientos rurales de La Araucanía», «las comunas con más de 40 escuelas rurales») y la base te devuelve solo eso, sin descargar millones de filas. Y te permite **leer y auditar** las consultas que otros escriben.

Este módulo usa la matrícula 2025 tal como vive en un sistema real: separada en una tabla de **conteos** y una tabla de **directorio**, unidas por el RBD. Es el mismo caso de R1-03, ahora con SQL — incluidos los 4 RBD huérfanos, que vas a cazar con un `LEFT JOIN`.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / pandas |
|----------|-----------|----------------------|
| **`SELECT ... FROM`** | Elige columnas de una tabla | `df[["a", "b"]]` |
| **`WHERE`** | Filtra **filas** | Autofiltro / `df[condición]` |
| **`ORDER BY ... DESC` + `LIMIT`** | Ordena y corta: rankings | Ordenar de mayor a menor / `.head()` |
| **`COUNT`, `SUM`, `AVG`** | Agregan muchas filas en un número | CONTAR, SUMA, PROMEDIO |
| **`GROUP BY`** | Agrega por grupo | Tabla dinámica / `groupby` |
| **`HAVING`** | Filtra **grupos** (después de agregar) | Filtrar la tabla dinámica |
| **`JOIN ... ON`** | Cruza dos tablas por la llave | BUSCARV / `pd.merge` |
| **`LEFT JOIN ... WHERE ... IS NULL`** | Encuentra filas sin pareja | Los #N/A del BUSCARV |
| **`sqlite3` + `to_sql` / `read_sql_query`** | Base de datos dentro de Python | — |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué es una llave y qué hace `pd.merge` (R1-03) | ☐ |
| Usar `groupby(...).sum()` y `.median()` | ☐ |
| Distinguir un texto `"Maule"` de un nombre de variable `Maule` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Crear una base SQLite en memoria con dos tablas (`matricula` y `directorio`) y la función `consultar(sql)`, que devuelve el resultado como tabla de pandas.

💡 **Concepto clave:** `df.to_sql("nombre", conn)` sube un DataFrame a la base; `pd.read_sql_query(sql, conn)` trae el resultado de vuelta. SQLite viene con Python: cero instalación.

---

### Sección 1 · SELECT y FROM

🎯 **Objetivo:** `SELECT nombre, comuna, dependencia FROM directorio` → 10.945 filas, 3 columnas.

💡 **Concepto clave:** SQL es **declarativo**: describes *qué* quieres, no *cómo* buscarlo.

---

### Sección 2 · WHERE

🎯 **Objetivo:** Los establecimientos rurales de La Araucanía: `WHERE region = 'La Araucanía' AND rural = 1` → **567**.

💡 **Concepto clave:** Los textos van entre **comillas simples** y se escriben exactamente como en los datos (con tilde). La igualdad es un solo `=`.

⚠️ **Error frecuente:** `WHERE region = La Araucanía` (sin comillas): SQL cree que es una columna y falla.

---

### Sección 3 · ORDER BY y LIMIT

🎯 **Objetivo:** Los 5 RBD con más estudiantes: el primero es el **RBD 52**, con **3.923**.

💡 **Concepto clave:** La tabla `matricula` solo tiene el RBD, no el nombre. Para saber *quién* es, hay que cruzar con el directorio: eso motiva el `JOIN`.

---

### Sección 4 · GROUP BY

🎯 **Objetivo:** Establecimientos por dependencia: Particular subvencionado **5.379**, Municipal **3.194**, Servicio Local de Educación **1.707**, Particular pagado **595**, Administración delegada **70**.

💡 **Concepto clave:** En el `SELECT` solo van las columnas del `GROUP BY` y funciones de agregación. `AS n` le pone nombre a la columna.

---

### Sección 5 · HAVING

🎯 **Objetivo:** Las comunas con 40 o más establecimientos rurales: **Padre Las Casas (56), Ovalle (52), Panguipulli (45) y Puerto Montt (44)**.

💡 **Concepto clave:** `WHERE rural = 1` filtra **filas** antes de agrupar; `HAVING COUNT(*) >= 40` filtra **grupos** después. `WHERE COUNT(*) >= 40` da error porque en ese momento el conteo todavía no existe.

✅ **Señal de que entendiste:** Puedes explicar en qué orden se ejecutan `WHERE`, `GROUP BY` y `HAVING`.

---

### Sección 6 · JOIN

🎯 **Objetivo:** Estudiantes por región cruzando `matricula` y `directorio`: Metropolitana **1.335.361**, Valparaíso **357.245**, Biobío **306.525**.

💡 **Concepto clave:** `FROM matricula AS m JOIN directorio AS d ON m.rbd = d.rbd`. Los alias (`m.`, `d.`) dicen de qué tabla viene cada columna; sin ellos, `rbd` sería ambiguo.

---

### Sección 7 · LEFT JOIN: auditar

🎯 **Objetivo:** Los RBD con matrícula pero sin directorio: **4** (7395, 9474, 25206 y 26085).

💡 **Concepto clave:** `LEFT JOIN` conserva todas las filas de la izquierda y deja `NULL` donde no hay pareja; `WHERE d.rbd IS NULL` se queda con esas. En SQL un nulo se pregunta con `IS NULL`: `= NULL` nunca es verdadero.

---

### Sección 8 · Promedio (SQL) vs mediana (pandas)

🎯 **Objetivo:** Comparar municipales y particulares subvencionados. Promedio: **247 vs 355** estudiantes (+44%). Mediana: **149 vs 160** (+7%).

💡 **Concepto clave:** SQLite no tiene mediana: SQL trae los datos justos y pandas termina el cálculo. Los promedios exageran la diferencia porque unos pocos particulares subvencionados muy grandes inflan el suyo; el establecimiento **típico** de ambas dependencias tiene un tamaño parecido.

---

### Reflexión final

«Los particulares subvencionados tienen 44% más estudiantes que los municipales» es aritméticamente cierto en promedio, pero engaña sobre el establecimiento típico. Una versión honesta menciona la mediana o el rango en que se mueve la mayoría.

---

## 6. Guía de los 8 Ejercicios

### Ejercicio 1 — Tu primer SELECT

**Pistas progresivas:**
- 🟢 Pista suave: Nombra las tres columnas separadas por coma, y la tabla después de `FROM`.
- 🟡 Pista media: `SELECT col1, col2, col3 FROM directorio`.
- 🔴 Pista directa: `sql_01 = "SELECT nombre, comuna, dependencia FROM directorio"`.

**¿Qué significa el ✅?** Que trajiste exactamente esas columnas para los 10.945 establecimientos.

---

### Ejercicio 2 — Los establecimientos rurales de La Araucanía

**Pistas progresivas:**
- 🟢 Pista suave: Son dos condiciones que deben cumplirse a la vez.
- 🟡 Pista media: `region = '...'` y `rural = 1`, unidas con `AND`.
- 🔴 Pista directa: `WHERE region = 'La Araucanía' AND rural = 1`.

**¿Qué significa el ✅?** Que filtraste filas con texto y número: 567 establecimientos.

---

### Ejercicio 3 — Los 5 establecimientos más grandes

**Pistas progresivas:**
- 🟢 Pista suave: Ordena de mayor a menor y quédate con los primeros.
- 🟡 Pista media: `ORDER BY mat_total DESC` y `LIMIT 5`.
- 🔴 Pista directa: `SELECT rbd, mat_total FROM matricula ORDER BY mat_total DESC LIMIT 5`.

**¿Qué significa el ✅?** Que armaste un ranking. El primero (RBD 52) tiene 3.923 estudiantes.

---

### Ejercicio 4 — Establecimientos por dependencia

**Pistas progresivas:**
- 🟢 Pista suave: Una fila por dependencia, con cuántos establecimientos tiene cada una.
- 🟡 Pista media: `COUNT(*) AS n`, `GROUP BY dependencia`, `ORDER BY n DESC`.
- 🔴 Pista directa: `SELECT dependencia, COUNT(*) AS n FROM directorio GROUP BY dependencia ORDER BY n DESC`.

**¿Qué significa el ✅?** Que resumiste por grupo: la tabla dinámica en SQL.

---

### Ejercicio 5 — Comunas con 40 o más establecimientos rurales

**Pistas progresivas:**
- 🟢 Pista suave: Hay un filtro de filas (solo rurales) y un filtro de grupos (solo comunas con muchos).
- 🟡 Pista media: El de filas va en `WHERE`; el de grupos, en `HAVING`.
- 🔴 Pista directa: `WHERE rural = 1` … `HAVING COUNT(*) >= 40`.

**¿Qué significa el ✅?** Que distingues filtrar filas de filtrar grupos: 4 comunas concentran la ruralidad escolar.

---

### Ejercicio 6 — Estudiantes por región con JOIN

**Pistas progresivas:**
- 🟢 Pista suave: Falta decir por qué columna se unen las tablas y en qué orden mostrar el resultado.
- 🟡 Pista media: `ON m.rbd = d.rbd` y `ORDER BY estudiantes DESC`.
- 🔴 Pista directa: `JOIN directorio AS d ON m.rbd = d.rbd` … `ORDER BY estudiantes DESC`.

**¿Qué significa el ✅?** Que respondiste una pregunta que ninguna tabla sola podía responder: la Metropolitana concentra 1.335.361 estudiantes.

---

### Ejercicio 7 — Encuentra los RBD huérfanos

**Pistas progresivas:**
- 🟢 Pista suave: Después de un `LEFT JOIN`, las filas sin pareja tienen la columna de la otra tabla vacía.
- 🟡 Pista media: Pregunta por el nulo con `IS NULL`, no con `= NULL`.
- 🔴 Pista directa: `WHERE d.rbd IS NULL`.

**¿Qué significa el ✅?** Que hiciste en SQL la misma auditoría de R1-03: los 4 RBD que reportan matrícula sin estar en el directorio oficial.

---

### Ejercicio 8 — Promedio (SQL) vs mediana (pandas)

**Pistas progresivas:**
- 🟢 Pista suave: El promedio se pide con una función de agregación de SQL; la mediana la calcula pandas sobre los datos que trajo SQL.
- 🟡 Pista media: `AVG(m.mat_total) AS promedio`; `datos.groupby("dependencia")["mat_total"].median()`.
- 🔴 Pista directa: completa `SELECT d.dependencia, AVG(m.mat_total) AS promedio ...`, `medianas = datos.groupby("dependencia")["mat_total"].median()` y `conclusion = "B"`.

**¿Qué significa el ✅?** Que no te quedaste con el primer número: con el promedio la diferencia es +44%; con la mediana, +7%.

---

> 🔬 **En la profundización:** el mismo SQL sobre los **24 parques nacionales**, con herramientas nuevas. `LIKE 'Laguna%'` encuentra Laguna del Laja (1958) y Laguna San Rafael (1959). `HAVING COUNT(*) >= 3` deja a Magallanes, La Araucanía (5 parques cada una) y Los Lagos (3). Una **subconsulta** contra el promedio muestra que solo **3 de 24** parques lo superan. `CASE WHEN` clasifica por época (10 antes de 1960, 11 entre 1960 y 1989, 3 desde 1990). Y `WHERE` + `HAVING` juntos responden qué regiones ya protegían más de 1 millón de hectáreas antes de 1970: Magallanes y Aysén.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué `WHERE COUNT(*) >= 40` da error?

- A) Porque `COUNT` no existe en SQLite
- B) Porque `WHERE` filtra filas antes de agrupar: el conteo todavía no existe; los grupos se filtran con `HAVING` ✅
- C) Porque falta `ORDER BY`
- D) Porque 40 debe ir entre comillas

**Explicación:** Orden lógico: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`.

---

**Pregunta 2:** Escribes `WHERE region = Maule` y falla. ¿Por qué?

- A) Maule no existe
- B) Sin comillas simples, SQL interpreta `Maule` como el nombre de una columna ✅
- C) Hay que escribir `==`
- D) Falta el `LIMIT`

**Explicación:** Los textos siempre van entre comillas simples: `'Maule'`.

---

**Pregunta 3:** ¿Para qué sirve `LEFT JOIN ... WHERE d.rbd IS NULL`?

- A) Para borrar filas
- B) Para encontrar las filas de la tabla izquierda que no tienen pareja en la derecha ✅
- C) Para ordenar
- D) Es igual a un `JOIN` normal

**Explicación:** Es la auditoría de lo que no calza, la misma de R1-03 en versión SQL.

---

**Pregunta 4:** SQLite no tiene función de mediana. ¿Qué haces?

- A) Usas el promedio, que es casi lo mismo
- B) Traes con SQL los datos justos y calculas la mediana con pandas ✅
- C) Cambias de base de datos
- D) Renuncias a la mediana

**Explicación:** SQL y pandas se complementan: SQL filtra y cruza en la base, pandas termina lo que SQL no hace.

---

**Pregunta 5:** El promedio dice +44% y la mediana +7%. ¿Qué concluyes?

- A) Que hay un error en los datos
- B) Que unos pocos establecimientos muy grandes inflan el promedio de un grupo; el establecimiento típico es parecido en ambos ✅
- C) Que la mediana está mal calculada
- D) Que hay que reportar el número más grande

**Explicación:** Cuando media y mediana cuentan historias distintas, la diferencia es información sobre la forma de los datos.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **SQL** | Lenguaje para pedir datos a una base | La «boleta de pedido» a los sistemas |
| **Base relacional** | Datos en tablas conectadas por llaves | SIGE, registros administrativos |
| **SQLite** | Base de datos liviana incluida en Python | Una base de prueba en tu computador |
| **Consulta (*query*)** | Una instrucción SQL | El reporte que pides a informática |
| **`WHERE`** | Filtro de filas | Los criterios del reporte |
| **`GROUP BY`** | Agrupar para resumir | El «por región», «por dependencia» |
| **`HAVING`** | Filtro de grupos | «Solo comunas con más de 40» |
| **`JOIN`** | Cruce de tablas por una llave | Unir conteos con el directorio por RBD |
| **`NULL`** | Valor ausente en SQL | La celda en blanco |
| **Alias** | Nombre corto para una tabla (`m`, `d`) | — |

---

## 9. Conexión con el Módulo Siguiente

En R1-05 consultaste una base de datos con SQL: filtrar, agrupar, filtrar grupos, cruzar y auditar — y viste que el promedio y la mediana pueden contar historias distintas.

En **R1-06 · Estadística descriptiva** vas a mirar esa diferencia con lupa: media y mediana, dispersión, percentiles, atípicos, estudiantes por curso y comparación entre escuelas rurales y urbanas, para no dejarte engañar por un solo número.

> 💡 **Pregunta para reflexionar:** ¿Qué reporte pides todos los meses a informática que podrías escribir tú mismo con un `SELECT ... WHERE ... GROUP BY`?
