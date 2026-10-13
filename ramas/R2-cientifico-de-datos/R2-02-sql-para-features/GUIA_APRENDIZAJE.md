# Guía de Aprendizaje — R2-02 · SQL para *features*

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 2 · Semana 4

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-02 · SQL para *features* |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 3–4 horas |
| **Nivel** | Intermedio — requiere R2-01 |
| **Prerrequisitos** | `groupby`, fechas, faltantes; SQL básico (`SELECT`, `WHERE`) |
| **Competencia de salida** | A partir de mediciones en bruto, construir con SQL una tabla analítica (una fila por entidad, una columna por *feature*) lista para un modelo, cuidando la fuga de información |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` — PM2.5 diario de 14 estaciones SINCA, 2020–2025 (30.674 días-estación), cargado en SQLite. Profundización: `sismos.csv` — 1.601 sismos M ≥ 4,5 en Chile, 2020–2025 (catálogo USGS) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Un modelo que anticipe episodios críticos de contaminación —para activar a tiempo una restricción o una alerta sanitaria— no «ve» el cielo: ve **columnas**. El PM2.5 de ayer, la media de la última semana, cuántos días de alerta tuvo la estación el invierno pasado. Fabricar esas columnas (*features*) es el 80 % del trabajo de ciencia de datos, y SQL es la herramienta con la que se hace en las bases institucionales.

En este módulo pasas de **consultar** datos a **fabricar variables** sobre el registro real del SINCA, usando los umbrales oficiales del **D.S. 12/2011 del MMA**: 50 µg/m³ como valor de la norma de 24 horas y los niveles de episodio crítico **Alerta (80–109)**, **Preemergencia (110–169)** y **Emergencia (≥ 170 µg/m³)**. Al etiquetar cada día descubrirás que, entre 2020 y 2025, las 14 estaciones registraron **238 días-estación en nivel de alerta, 84 en preemergencia y 2 en emergencia**.

Y aprenderás la trampa número uno de la ciencia de datos: la **fuga de información**. Una media móvil que incluye el día que quieres predecir hace que el modelo parezca genial en pruebas y fracase en la realidad.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| ***Feature*** | Columna que describe una entidad y que un modelo usa | Una columna calculada de la planilla |
| **Tabla analítica (ABT)** | Una fila por entidad, una columna por *feature* | La tabla resumen que va al informe |
| **`GROUP BY`** | Resume muchas filas por grupo | Tabla dinámica |
| **`COUNT(col)`** | Cuenta solo filas con dato | `=CONTAR()` (ignora vacíos) |
| **`strftime('%m', fecha)`** | Extrae el mes de una fecha | `=MES()` |
| **`CASE WHEN`** | Etiqueta según reglas | `=SI(...; SI(...))` anidado |
| **`LAG() OVER (...)`** | Valor de la fila anterior dentro de un grupo | Referencia a la celda de arriba |
| **`AVG() OVER (ROWS ...)`** | Media móvil sobre filas vecinas | `=PROMEDIO()` de las 7 celdas de arriba, arrastrado |
| ***Data leakage*** | Usar información del futuro como *feature* | Ver la respuesta antes de la prueba |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Escribir un `SELECT ... FROM ... WHERE ...` simple | ☐ |
| Explicar qué hace `groupby` en pandas | ☐ |
| Explicar por qué un `NaN` (o `NULL`) no es lo mismo que un 0 | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `aire_diario.csv` y copiarlo a una tabla `aire` de SQLite en memoria con `df.to_sql`.

💡 **Concepto clave:** `correr(sql)` ejecuta una consulta y devuelve un DataFrame. Desde aquí todo es SQL; pandas solo muestra resultados. Los `NaN` de pandas se convierten en `NULL` en SQL.

---

### Sección 1 · La idea central: de mediciones a *features*

🎯 **Objetivo:** Entender las tres palabras del módulo: observación en bruto (un día-estación), entidad (la estación) y tabla analítica (una fila por estación).

💡 **Concepto clave:** El viaje es de 30.674 filas a 14 filas con muchas columnas. Ese «achicar ampliando» es el corazón del feature engineering.

---

### Sección 2 · *Features* de agregación con `GROUP BY`

🎯 **Objetivo:** Una fila por estación y mes con días medidos, promedio y máximo de PM2.5.

💡 **Concepto clave:** Se puede agrupar por algo **calculado**: `CAST(strftime('%m', fecha) AS INTEGER)` da el mes. El resultado tiene **168 filas** (14 × 12). `COUNT(pm25)` cuenta solo días con dato (29.644 en total), a diferencia de `COUNT(*)` (30.674).

⚠️ **Error frecuente:** Poner `fecha` suelta en el `SELECT` junto a un `GROUP BY estacion, mes`: cada grupo tiene muchas fechas.

---

### Sección 3 · *Features* condicionales con `CASE WHEN`

🎯 **Objetivo:** Etiquetar cada día como `sin dato`, `emergencia`, `preemergencia`, `alerta`, `sobre norma` o `bajo norma`.

💡 **Concepto clave:** El `CASE` se queda con la **primera** condición verdadera, así que los umbrales van de mayor a menor. Y el `NULL` va primero: un `NULL` no cumple ninguna comparación y caería en el `ELSE` como «bajo norma». Resultado real: 28.365 bajo norma, 1.030 sin dato, 955 sobre norma (50–79), 238 alerta, 84 preemergencia, 2 emergencia.

⚠️ **Error frecuente:** Ordenar los umbrales al revés: con `WHEN pm25 > 50` primero, el día de 284 µg/m³ quedaría como «sobre norma».

---

### Sección 4 · *Features* temporales con funciones de ventana

🎯 **Objetivo:** Agregar a cada día `pm25_ayer` (`LAG`) y `pm25_media_7d` (media de los 7 días **anteriores**).

💡 **Concepto clave:** `PARTITION BY estacion` separa las series; `ORDER BY fecha` les da sentido temporal; `ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING` excluye el día actual. Como el registro tiene exactamente un día por fila en cada estación (2.191 días), «7 filas» = «7 días». `AVG` ignora los `NULL` dentro de la ventana.

⚠️ **Error frecuente:** Escribir `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`: la media incluiría el PM2.5 de hoy, que es justamente lo que querrías predecir → **fuga de información**.

✅ **Señal de que entendiste:** Puedes explicar por qué el primer día de cada estación tiene `pm25_ayer` nulo y por qué eso es correcto.

---

### Sección 5 · La tabla analítica

🎯 **Objetivo:** Una fila por estación con `n_dias`, `pm25_promedio`, `dias_sobre_norma`, `dias_alerta_o_peor` y `pm25_invierno`.

💡 **Concepto clave:** `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` cuenta días que cumplen una condición; `AVG(CASE WHEN mes entre 5 y 8 THEN pm25 END)` —sin `ELSE`— promedia solo el invierno. La tabla lo deja claro: **Cerro Navia** lidera en días sobre 50 (332), **Las Encinas Temuco** en días de alerta o peor (131), y ambas promedian cerca de **47,5 µg/m³ en invierno** frente a 24–27 µg/m³ en todo el año. Seis estaciones (Alto Hospicio, Antofagasta, Copiapó Sivica, Coquimbo, Cuncumen y Concón) tienen **0** días sobre la norma.

---

### Reflexión final

Para focalizar fiscalización de calefacción a leña, la columna clave no es `pm25_promedio` sino `pm25_invierno` o `dias_alerta_o_peor`. Una *feature* nueva que valdría la pena: días de alerta del invierno anterior, o el PM2.5 promedio con temperatura mínima bajo 0 °C.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Features por estación y mes

**Pistas progresivas:**
- 🟢 Pista suave: Agrupa por dos cosas: la estación y el mes extraído de la fecha.
- 🟡 Pista media: `CAST(strftime('%m', fecha) AS INTEGER) AS mes` en el `SELECT` y `GROUP BY estacion, mes`.
- 🔴 Pista directa: `COUNT(pm25) AS n_dias, ROUND(AVG(pm25), 1) AS pm25_promedio, MAX(pm25) AS pm25_maximo ... GROUP BY estacion, mes ORDER BY estacion, mes`.

**¿Qué significa el ✅?** Que tienes 168 filas, que `n_dias` suma exactamente los 29.644 días con dato y que el máximo es 284.

---

### Ejercicio 2 — Etiquetar cada día con su nivel de episodio

**Pistas progresivas:**
- 🟢 Pista suave: Primero el caso sin dato; después los umbrales del más alto al más bajo.
- 🟡 Pista media: `WHEN pm25 >= 170 THEN 'emergencia'` va antes que `WHEN pm25 >= 110 ...`.
- 🔴 Pista directa: `WHEN pm25 IS NULL THEN 'sin dato' WHEN pm25 >= 170 THEN 'emergencia' WHEN pm25 >= 110 THEN 'preemergencia' WHEN pm25 >= 80 THEN 'alerta' WHEN pm25 > 50 THEN 'sobre norma' ELSE 'bajo norma' END AS nivel`.

**¿Qué significa el ✅?** Que cada nivel tiene exactamente los días que le corresponden según el D.S. 12/2011 (2 emergencia, 84 preemergencia, 238 alerta).

---

### Ejercicio 3 — El PM2.5 de ayer y la media de la semana previa

**Pistas progresivas:**
- 🟢 Pista suave: Ambas columnas usan `OVER (PARTITION BY ... ORDER BY ...)`; la media necesita además el marco de filas.
- 🟡 Pista media: `LAG(pm25) OVER (PARTITION BY estacion ORDER BY fecha)`.
- 🔴 Pista directa: `ROUND(AVG(pm25) OVER (PARTITION BY estacion ORDER BY fecha ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING), 1) AS pm25_media_7d`.

**¿Qué significa el ✅?** Que tus dos *features* coinciden fila a fila con un cálculo independiente en pandas — y que la media **no** usa el día actual.

---

### Ejercicio 4 — Tu primera tabla analítica

**Pistas progresivas:**
- 🟢 Pista suave: Una fila por estación = `GROUP BY estacion`. Para contar días que cumplen algo, suma unos y ceros.
- 🟡 Pista media: `SUM(CASE WHEN pm25 > 50 THEN 1 ELSE 0 END) AS dias_sobre_norma`.
- 🔴 Pista directa: `ROUND(AVG(CASE WHEN CAST(strftime('%m', fecha) AS INTEGER) BETWEEN 5 AND 8 THEN pm25 END), 1) AS pm25_invierno` y `ORDER BY dias_sobre_norma DESC`.

**¿Qué significa el ✅?** Que armaste la ABT: 14 filas, 1.279 días sobre norma y 324 de alerta o peor en total, ordenada de más a menos expuesta.

---

> 🔬 **En la profundización:** el mismo oficio sobre los **1.601 sismos M ≥ 4,5** de Chile 2020–2025 (catálogo USGS). *Features* por **zona y año** (24 filas), etiquetas de profundidad (584 superficiales, 1.017 intermedios, ninguno profundo) y la bandera `es_fuerte` (35 sismos M ≥ 6), **días desde el sismo anterior** en la misma zona con `julianday` + `LAG` (una *feature* punto-en-el-tiempo correcta; «días hasta el próximo» sería *leakage*) y una herramienta nueva, la **CTE** (`WITH`), para agregar una *feature* de ventana: en el norte hay un sismo M ≥ 4,5 cada 2,4 días en promedio; en la zona austral, cada 185.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué es una tabla analítica (ABT)?

- A) La tabla cruda tal como viene del sistema
- B) Una fila por entidad y una columna por *feature*, lista para un modelo ✅
- C) Un gráfico de resumen
- D) La tabla con todas las fechas

**Explicación:** La ABT es el producto final del feature engineering: lo que se le entrega al modelo.

---

**Pregunta 2:** ¿Cuál es la diferencia entre `COUNT(*)` y `COUNT(pm25)`?

- A) Ninguna
- B) `COUNT(*)` cuenta filas; `COUNT(pm25)` solo las filas con PM2.5 no nulo ✅
- C) `COUNT(pm25)` suma los valores
- D) `COUNT(*)` ignora los nulos

**Explicación:** Con 1.030 días sin dato, la diferencia es de 30.674 vs 29.644.

---

**Pregunta 3:** En un `CASE WHEN`, ¿por qué se trata `pm25 IS NULL` primero?

- A) Por estética
- B) Porque un `NULL` no cumple ninguna comparación y caería en el `ELSE`, quedando mal etiquetado ✅
- C) Porque SQL lo exige
- D) Porque es más rápido

**Explicación:** Sin ese caso, un día sin medición quedaría como «bajo norma»: un dato inventado.

---

**Pregunta 4:** Quieres predecir el PM2.5 de hoy. ¿Qué *feature* tiene fuga de información?

- A) `LAG(pm25)` (el PM2.5 de ayer)
- B) La media de los 7 días anteriores (`7 PRECEDING AND 1 PRECEDING`)
- C) La media de los últimos 7 días incluyendo hoy (`6 PRECEDING AND CURRENT ROW`) ✅
- D) El mes del año

**Explicación:** La C contiene el valor que se quiere predecir. En pruebas parece excelente; en operación, ese dato no existe todavía.

---

**Pregunta 5:** ¿Qué hace `PARTITION BY estacion` dentro de `LAG(...) OVER (...)`?

- A) Ordena las estaciones alfabéticamente
- B) Hace que cada estación tenga su propia serie: el «ayer» de una estación nunca viene de otra ✅
- C) Agrupa y colapsa las filas por estación
- D) Filtra una estación

**Explicación:** A diferencia de `GROUP BY`, una ventana no colapsa filas; `PARTITION BY` solo define dentro de qué grupo se mira.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| ***Feature*** | Columna que describe una entidad | Un indicador de gestión |
| **Entidad** | La unidad de análisis (una fila en la ABT) | La estación, la comuna, el establecimiento |
| **ABT** | Tabla analítica: una fila por entidad | La tabla resumen del informe |
| **Episodio crítico** | Nivel de PM2.5 de 24 h que activa medidas (D.S. 12/2011) | Alerta, preemergencia, emergencia ambiental |
| **Función de ventana** | Cálculo sobre filas vecinas sin colapsar la tabla | Fórmula arrastrada que mira celdas de arriba |
| ***Lag* (rezago)** | Valor de una observación anterior | «El dato de ayer» |
| **Media móvil** | Promedio de una ventana que se desplaza | Promedio de los últimos 7 días |
| ***Data leakage*** | Usar información del futuro como *feature* | Evaluar con la respuesta a la vista |
| **CTE (`WITH`)** | Tabla temporal con nombre dentro de una consulta | Una hoja auxiliar de cálculo |

---

## 9. Conexión con el Módulo Siguiente

En R2-02 fabricaste *features* con SQL —agregaciones, etiquetas de episodio, rezagos y medias móviles sin fuga— y las reuniste en una tabla analítica por estación.

En **R2-03 · Estadística para modelar** vas a medir con rigor lo que hoy resumiste: distribuciones, intervalos de confianza y pruebas de hipótesis para saber si una diferencia entre estaciones o temporadas es real o puro ruido. Y en **R2-04**, una tabla como la que armaste hoy será la entrada de tu primer modelo.

> 💡 **Pregunta para reflexionar:** En los indicadores de tu servicio, ¿hay alguno que se calcula con datos que en el momento de decidir todavía no existían? Eso también es *leakage*.
