# 📘 Guía de Aprendizaje — R2-02 · SQL para *features*

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-02 · SQL para *features* (D8) |
| **Pista / Rama** | R2 — Científico/a de Datos · Línea B |
| **Duración estimada** | 3–4 horas (Semana 9) |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-00 y R2-01 completados; conocimiento básico de SQL (consultas SELECT, WHERE, GROUP BY del tronco común M5). |
| **Competencia de salida** | Construir con SQL una tabla analítica (una fila por entidad, varias columnas de *features*) lista para entrenar un modelo, usando agregaciones, lógica condicional, rezago temporal y entendiendo qué es el *data leakage*. |
| **Dataset** | `sismos.csv` — 15 últimos sismos publicados por el Centro Sismológico Nacional (CSN), Universidad de Chile, capturados el 2026-06-18. |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En el Estado constantemente se acumulan tablas de **eventos**: registros de prestaciones de salud, solicitudes ciudadanas, licitaciones adjudicadas, denuncias recibidas, multas cursadas. Cada fila es un evento, pero un modelo de datos no trabaja con eventos: trabaja con **entidades** y sus atributos.

¿Cómo pasas de miles de eventos a una tabla útil para análisis o predicción? Con SQL y la fabricación de *features*. Este módulo te enseña exactamente eso, usando datos sísmicos reales del CSN como campo de práctica.

La lógica es directamente aplicable a:

- **Prestaciones de salud:** una fila por persona, con *features* como número de atenciones, promedio de días de espera, tipo de prestación más frecuente.
- **Licitaciones:** una fila por organismo, con *features* como monto promedio adjudicado, proporción de licitaciones desiertas, categorías más usadas.
- **Seguridad ciudadana:** una fila por comuna, con *features* como denuncias por tipo, tendencia mes a mes.

> 🏛️ **Idea clave:** SQL no es solo para consultar lo que ya existe. En ciencia de datos, SQL es la herramienta que construye las variables que los modelos necesitan para aprender.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|---|---|---|
| ***Feature* (característica)** | Columna que describe una entidad y que un modelo puede usar para aprender | Indicador de un servicio público (ej. tasa de aprobación de licitaciones) |
| **Tabla analítica (ABT)** | Tabla con una fila por entidad y una columna por *feature* | Tablero de indicadores por organismo o región |
| **Entidad** | La unidad de análisis; tendrá una fila en la tabla final | Región, organismo, beneficiario, proveedor |
| `GROUP BY` + agregación | Resume muchas filas en una por grupo | Tabla dinámica con totales y promedios por categoría |
| `COUNT(*)` | Cuenta cuántos eventos hay en cada grupo | Número de licitaciones por región |
| `AVG()`, `MAX()` | Promedio y máximo dentro de cada grupo | Monto promedio o mayor gasto por organismo |
| `CASE WHEN ... THEN ... END` | Lógica condicional para crear etiquetas | Clasificar proveedores por tamaño o tipo |
| `LAG()` | Función de ventana: trae el valor de la fila anterior | Mirar el mes anterior en un registro cronológico |
| `OVER (ORDER BY ...)` | Define la ventana de tiempo para `LAG` | Ordenar por fecha antes de mirar hacia atrás |
| ***Data leakage*** | Usar información del futuro como *feature* predictiva | Incluir el resultado en los indicadores que se usan para predecirlo |
| `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` | Cuenta cuántos registros cumplen una condición dentro de un grupo | Contar cuántos eventos de un tipo ocurrieron en cada zona |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Escribir un `SELECT` con `WHERE` y `GROUP BY` en SQL | ✅ | Repasa el módulo M5 del tronco común |
| Usar `AVG()`, `COUNT(*)` y `MAX()` en SQL | ✅ | Si no los conoces, dedica 20 min al recap del notebook |
| Trabajar en Colab con pandas y `pd.read_sql_query` | ✅ | Revisa R2-00 si esto te parece nuevo |
| Entender qué es una tabla de *eventos* vs. una tabla de *entidades* | ✅ | Piensa: eventos = filas de Excel; entidades = resumen por categoria |
| No tener miedo de ver `NULL` en resultados SQL | ✅ | `NULL` es simplemente “no hay dato”, no es un error |

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno

**🎯 Objetivo:** Cargar el CSV de sismos, crear una base de datos SQLite en memoria y definir la función `correr()` para ejecutar consultas.

**💡 Concepto clave:** SQLite es una base de datos que vive completamente en la memoria del computador. No necesitas instalar nada: Python la incluye. Aquí se crea una base temporal donde se vuelca el CSV, y se define `correr(sql)` que ejecuta cualquier consulta y devuelve un DataFrame.

**🔍 Qué hace el código:**
1. Descarga `sismos.csv` si no está disponible localmente.
2. Lo carga con `pd.read_csv()` y lo vuelca a SQLite con `.to_sql()`.
3. Define `correr(sql)` como atajo para `pd.read_sql_query(sql, con)`.

**⚠️ Error frecuente:** No ejecutar esta celda primero. Todas las consultas siguientes dependen de que `con` y `correr` existan.

**✅ Señal de comprensión:** Ves el mensaje `Listo. Tabla 'sismos' creada con 15 eventos reales` y la tabla aparece debajo con sus columnas.

---

### 🔷 Sección 1 — La idea central: de eventos a *features*

**🎯 Objetivo:** Entender el viaje conceptual del módulo antes de escribir código.

**💡 Concepto clave:** Una *feature* es una columna descriptiva que un modelo puede usar para aprender. El viaje de hoy es: `tabla de sismos (1 fila = 1 sismo)` → SQL → `tabla analítica (1 fila = 1 región, varias *features*)`. Cada región tendrá como atributos cuántos sismos tuvo, cuál fue la magnitud promedio, etc.

**🔍 Qué hace el código:** Esta sección es solo teoría y setup. No hay `TODO` aquí.

**⚠️ Error frecuente:** Saltarse la lectura conceptual e ir directo a los ejercicios. Los bloques de texto de esta sección explican el *por qué* de cada herramienta. Vale la pena leerlos.

**✅ Señal de comprensión:** Puedes explicar con tus palabras la diferencia entre un **evento** y una **entidad**, y por qué necesitas transformar unos en otros.

---

### 🔷 Sección 2 — *Features* de agregación con `GROUP BY`

**🎯 Objetivo:** Construir un resumen por región con 5 columnas: `region`, `n_sismos`, `magnitud_promedio`, `magnitud_maxima`, `profundidad_promedio`.

**💡 Concepto clave:** `GROUP BY` junta todas las filas que comparten un valor (por ejemplo, todos los sismos de la misma región) y aplica funciones de agregación a cada grupo. El resultado tiene **una fila por grupo**. Es exactamente igual a una tabla dinámica de Excel, pero escrito en SQL y mucho más potente.

**🔍 Qué hace el código:**
- `GROUP BY region` agrupa todos los sismos de cada región.
- `COUNT(*)` cuenta cuántos sismos hay en cada grupo.
- `AVG(magnitud)` calcula el promedio de magnitud por grupo.
- `MAX(magnitud)` devuelve la mayor magnitud registrada en cada grupo.
- `ROUND(..., 2)` redondea a 2 decimales para que sea legible.
- `ORDER BY n_sismos DESC` ordena de mayor a menor.

**⚠️ Error frecuente:** Olvidar el `AS` para nombrar las columnas. Si no usas `AS n_sismos`, la celda de chequeo no encontrará la columna porque su nombre automático sería algo como `COUNT(*)`.

**✅ Señal de comprensión:** La tabla resultante tiene 6 filas (una por región) y `n_sismos` suma exactamente 15.

---

### 🔷 Sección 3 — *Features* condicionales con `CASE WHEN`

**🎯 Objetivo:** Clasificar cada sismo según su profundidad: superficial, intermedio o profundo.

**💡 Concepto clave:** `CASE WHEN` es el `SI()` de Excel pero en SQL. Le dices: *si la profundidad es menor a 70 km, entonces escribe 'superficial'*. SQL evalúa las condiciones de arriba hacia abajo y se queda con la primera que se cumple. Es ideal para convertir números en etiquetas útiles.

**🔍 Qué hace el código:**
```sql
CASE
    WHEN profundidad_km < 70   THEN 'superficial'
    WHEN profundidad_km <= 300 THEN 'intermedio'
    ELSE 'profundo'
END AS profundidad_tipo
```
- Primera condición: profundidad menor a 70 km → superficial.
- Si no cumple lo anterior y es menor o igual a 300 → intermedio.
- Todo lo demás → profundo.

**⚠️ Error frecuente:** Poner las condiciones en orden incorrecto. Si pones primero `< 300` y luego `< 70`, todos los sismos menores a 70 entrarán en la primera condición y nunca se clasificarán como superficiales.

**✅ Señal de comprensión:** La tabla resultante tiene 15 filas (una por sismo) y la columna `profundidad_tipo` muestra solo `'superficial'` o `'intermedio'` para estos datos (en nuestra muestra no hay sismos muy profundos).

---

### 🔷 Sección 4 — *Features* temporales con `LAG`

**🎯 Objetivo:** Agregar a cada sismo la magnitud del sismo inmediatamente anterior como *feature* de rezago.

**💡 Concepto clave:** `LAG` es una **función de ventana**: en vez de colapsar filas como `GROUP BY`, mantiene todas las filas y agrega información de las filas vecinas. `LAG(magnitud) OVER (ORDER BY fecha_hora)` dice: *ordena los sismos por fecha y para cada uno, trae la magnitud del que ocurrió antes*. Es como tener una columna extra que dice “¿qué pasó justo antes?”.

**🔍 Qué hace el código:**
- `ORDER BY fecha_hora` dentro del `OVER` establece el orden cronológico.
- `LAG(magnitud)` trae el valor de la fila anterior en ese orden.
- La primera fila queda con `NULL` porque no tiene fila anterior.

**⚠️ Error frecuente:** Olvidar el `ORDER BY` dentro del `OVER(...)`. Sin ordenamiento explícito, “la fila anterior” no tiene significado y el resultado es impredecible.

**✅ Señal de comprensión:** La primera fila (el sismo más antiguo) tiene `NULL` en `magnitud_anterior` y la segunda fila tiene el valor de magnitud de la primera.

---

### 🔷 Sección 5 — La tabla analítica completa

**🎯 Objetivo:** Construir la tabla analítica final: una fila por región con `n_sismos`, `magnitud_promedio`, `n_superficiales` y `n_profundos`.

**💡 Concepto clave:** El truco clave de este ejercicio es `SUM(CASE WHEN condicion THEN 1 ELSE 0 END)`. Cada sismo que cumple la condición aporta un `1`; los demás aportan `0`. Al sumar dentro de cada grupo, obtienes el conteo de los que cumplen. Es como levantar la mano en una asamblea: cuento cuántas manos levantadas hay en cada región.

**🔍 Qué hace el código:**
- `SUM(CASE WHEN profundidad_km < 70 THEN 1 ELSE 0 END) AS n_superficiales` cuenta los superficiales.
- `SUM(CASE WHEN profundidad_km >= 70 THEN 1 ELSE 0 END) AS n_profundos` cuenta los de 70+ km.
- `GROUP BY region` agrupa todo por región.

**⚠️ Error frecuente:** Que `n_superficiales + n_profundos` no sume el total de sismos de la región. Eso significa que las condiciones no son mutuamente excluyentes y exhaustivas.

**✅ Señal de comprensión:** La tabla tiene 6 filas, `n_sismos` suma 15, `n_superficiales` suma 6 y `n_profundos` suma 9.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Resumen sísmico por región

**Habilidad que desarrolla:** Construir *features* de agregación con `GROUP BY`.

**Pista 1 (conceptual):** Necesitas comprimir 15 filas de sismos en 6 filas, una por región. ¿Qué cláusula SQL agrupa filas por categoría?

**Pista 2 (técnica):** La estructura es `SELECT region, COUNT(*) AS n_sismos, AVG(magnitud) AS magnitud_promedio, ... FROM sismos GROUP BY region`. ¿Qué funciones necesitas para la magnitud máxima y la profundidad promedio?

**Pista 3 (casi solución):** Los nombres de columna deben ser exactamente: `region`, `n_sismos`, `magnitud_promedio`, `magnitud_maxima`, `profundidad_promedio`. Usa `ROUND(..., 2)` para redondear los promedios. No olvides `ORDER BY n_sismos DESC`.

**Lógica de solución:** `SELECT region, COUNT(*) AS n_sismos, ROUND(AVG(magnitud), 2) AS magnitud_promedio, MAX(magnitud) AS magnitud_maxima, ROUND(AVG(profundidad_km), 2) AS profundidad_promedio FROM sismos GROUP BY region ORDER BY n_sismos DESC`.

---

### ✍️ Ejercicio 2 — Clasificar cada sismo por profundidad

**Habilidad que desarrolla:** Crear *features* condicionales con `CASE WHEN`.

**Pista 1 (conceptual):** Necesitas una columna nueva que no existe en la tabla, basada en una regla: si la profundidad cumple ciertas condiciones, asigna una etiqueta.

**Pista 2 (técnica):** `CASE WHEN ... THEN ... WHEN ... THEN ... ELSE ... END AS nombre_columna` es la estructura. El orden de las condiciones importa: empieza por la más restrictiva.

**Pista 3 (casi solución):** Primero `< 70` es superficial, luego `<= 300` es intermedio, y todo lo demás es profundo. Devuelve `id`, `lugar`, `profundidad_km` y la nueva columna `profundidad_tipo`, ordenado por `id`.

**Lógica de solución:** Usar `CASE WHEN profundidad_km < 70 THEN 'superficial' WHEN profundidad_km <= 300 THEN 'intermedio' ELSE 'profundo' END AS profundidad_tipo` en el SELECT, sin GROUP BY porque se evalúa por fila.

---

### ✍️ Ejercicio 3 — La magnitud del sismo anterior

**Habilidad que desarrollas:** Crear *features* temporales de rezago con `LAG`.

**Pista 1 (conceptual):** Quieres una columna nueva que diga “¿cuál fue la magnitud del sismo que ocurrió justo antes de este?”. Eso requiere mirar la fila anterior, no agregar un grupo.

**Pista 2 (técnica):** `LAG(columna) OVER (ORDER BY columna_orden)` es la sintaxis. El `OVER` define la ventana; el `ORDER BY` dentro del `OVER` define cuál es “la fila anterior”.

**Pista 3 (casi solución):** Devuelve `id`, `fecha_hora`, `magnitud` y `LAG(magnitud) OVER (ORDER BY fecha_hora) AS magnitud_anterior`. La primera fila tendrá `NULL` en `magnitud_anterior`, lo cual es correcto.

**Lógica de solución:** Usar función de ventana `LAG` con `ORDER BY fecha_hora` dentro del `OVER`, sin GROUP BY.

---

### ✍️ Ejercicio 4 — Tu primera tabla analítica

**Habilidad que desarrollas:** Combinar agregación y lógica condicional para construir la tabla analítica completa.

**Pista 1 (conceptual):** Necesitas una tabla con 6 filas (una por región) y columnas que cuenten sismos por tipo. ¿Cómo cuentas, dentro de un grupo, solo los que cumplen una condición?

**Pista 2 (técnica):** El truco es `SUM(CASE WHEN condicion THEN 1 ELSE 0 END)`. Combina `GROUP BY region` con este patrón para cada tipo.

**Pista 3 (casi solución):** Las columnas necesarias son `region`, `n_sismos` (COUNT), `magnitud_promedio` (AVG), `n_superficiales` (SUM CASE < 70) y `n_profundos` (SUM CASE >= 70). Ordena por `n_sismos DESC`.

**Lógica de solución:** Combinar `GROUP BY region` con `COUNT(*)`, `AVG()`, y dos `SUM(CASE WHEN ...)` para los dos tipos de profundidad.

---

## 7. Sección en Profundidad: Ejercicio 4 — La tabla analítica y su impacto en política pública

El ejercicio 4 es el más estratégico porque **produce el producto final de un científico de datos**: la tabla analítica (ABT). Entender bien este concepto es lo que separa a alguien que “hace SQL” de alguien que “prepara datos para modelos”.

### ¿Qué hace especial a una tabla analítica?

Tiene tres propiedades:
1. **Una fila por entidad:** cada fila representa la unidad sobre la que se quiere decidir o predecir.
2. **Una columna por *feature*:** cada columna es un atributo calculado, no un dato crudo.
3. **Lista para un modelo:** ningún modelo de ML puede trabajar con eventos crudos directamente; necesita esta transformación.

### Aplicaciones directas en el Estado chileno

| Dominio público | Eventos crudos | Entidad | *Features* posibles |
|---|---|---|---|
| Compras públicas | Órdenes de compra | Organismo | nº licitaciones, monto promedio, % adjudicado |
| Salud | Consultas médicas | Beneficiario | visitas al año, promedio de días de espera |
| Educación | Evaluaciones | Estudiante | promedio SIMCE, asistencia, tipo de establecimiento |
| Seguridad | Denuncias | Comuna | denuncias por tipo, variación respecto al año anterior |
| Sísmico (este módulo) | Eventos sísmicos | Región | nº sismos, magnitud promedio, sismos superficiales |

### El concepto de *data leakage* aplicado al sector público

Si quisieras predecir si un organismo va a tener problemas de ejecución presupuestaria, **no podrías usar el porcentaje de ejecución del mismo año** como *feature*: eso es exactamente lo que intentas predecir. Ese error se llama *data leakage* y es muy común en modelos construidos sin rigor metodológico.

> 🚨 **Regla de oro:** las *features* solo pueden contener información que estaba disponible **antes** del momento que intentas predecir.

---

## 8. Conexión con profundiza.ipynb

Este módulo tiene un `profundiza.ipynb` que va más allá del *cómo* y entra en el *por qué*.

### Comparativa leccion vs. profundiza

| Tema | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| Foco | Construir *features* con SQL | Entender qué hace buena a una *feature* |
| *Data leakage* | Mencionado, conceptual | Profundizado: leakage temporal y de objetivo |
| Correción punto-en-el-tiempo | No aborda | Explicada con ejercicios |
| Granularidad del tablón | Uno fijo (región) | Debate sobre cómo elegir la entidad correcta |
| Complejidad | ⭐⭐⭐ Intermedio | ⭐⭐⭐⭐ Avanzado-conceptual |

### Guía de decisión

```
¿Tienes las 4 celdas en ✅?
    ├── No → Termina la lección principal primero.
    └── Sí → ¿Te interesa construir modelos predictivos con rigor?
              ├── Sí → El profundiza es imprescindible para ti.
              └── No → Avanza a R2-03. Los conceptos básicos ya los tienes.
```

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Qué es una *feature* en el contexto de machine learning?

- a) Una fila de la tabla original de eventos
- b) Una columna que describe una entidad y que un modelo puede usar para aprender
- c) El resultado que quieres predecir
- d) Un parámetro del modelo

✅ **Respuesta correcta: b)**
**Explicación:** Las *features* son los atributos de la entidad que el modelo recibe como entrada. No son los eventos crudos ni el resultado a predecir, sino las variables descriptivas construidas para el modelo.

---

**Pregunta 2:** En una consulta `GROUP BY region`, ¿puedes pedir la columna `lugar` directamente en el `SELECT`?

- a) Sí, siempre que uses `ORDER BY`
- b) Sí, si la tabla tiene pocas filas
- c) No, porque cada región tiene varios lugares y SQL no sabría cuál mostrar
- d) Sí, si usas `DISTINCT`

✅ **Respuesta correcta: c)**
**Explicación:** Con `GROUP BY`, cada columna en el `SELECT` debe estar en el `GROUP BY` o dentro de una función de agregación. Si agrupas por región pero pides `lugar`, SQLite dará error o un resultado incorrecto.

---

**Pregunta 3:** ¿Qué hace `SUM(CASE WHEN profundidad_km < 70 THEN 1 ELSE 0 END)`?

- a) Suma las profundidades menores a 70
- b) Cuenta cuántos sismos tienen profundidad menor a 70 km
- c) Filtra los sismos superficiales
- d) Promedia la profundidad de los sismos superficiales

✅ **Respuesta correcta: b)**
**Explicación:** El `CASE WHEN` asigna 1 a los que cumplen y 0 a los que no. El `SUM` suma esos 1s, obteniendo el conteo de los que cumplían la condición. Es el patrón estándar para contar condicionalmente en SQL.

---

**Pregunta 4:** ¿Qué diferencia hay entre `LAG` y `GROUP BY`?

- a) `LAG` es más rápido que `GROUP BY`
- b) `GROUP BY` colapsa filas en grupos; `LAG` mantiene todas las filas y mira a la fila anterior
- c) `LAG` solo funciona con fechas
- d) No hay diferencia, hacen lo mismo

✅ **Respuesta correcta: b)**
**Explicación:** `GROUP BY` reduce muchas filas a una por grupo. `LAG` es una función de ventana: mantiene el mismo número de filas y agrega una columna que mira a la fila anterior en el orden definido.

---

**Pregunta 5:** ¿Qué es el *data leakage*?

- a) Un error de conexión a la base de datos
- b) Cuando el dataset tiene valores nulos
- c) Usar información del futuro o del resultado como *feature* predictiva
- d) Cuando dos tablas tienen columnas con el mismo nombre

✅ **Respuesta correcta: c)**
**Explicación:** El *leakage* ocurre cuando las *features* contienen información que no estaría disponible en el momento de la predicción real. El modelo aparece excelente en entrenamiento pero falla en producción porque “trampeaba” con datos del futuro.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente sector público / Excel |
|---|---|---|
| ***Feature* / Característica** | Variable descriptiva de una entidad para un modelo | Indicador en un tablero de control |
| **Tabla analítica (ABT)** | Tabla final: una fila por entidad, columnas son *features* | Dashboard con una fila por organismo y sus indicadores |
| **Entidad** | Unidad de análisis (lo que tendrá una fila en la tabla final) | Región, organismo, proveedor, beneficiario |
| **Evento** | Registro crudo en la tabla de origen | Una orden de compra, una consulta médica, un sismo |
| `GROUP BY` | Agrupa filas por una columna y aplica funciones | Tabla dinámica de Excel por categoría |
| `CASE WHEN` | Lógica condicional en SQL | Función `SI()` de Excel |
| `LAG()` | Función de ventana que trae el valor de la fila anterior | “Mes anterior” en un registro cronológico |
| `OVER (ORDER BY ...)` | Define el orden para funciones de ventana | Ordenar por fecha antes de calcular diferencias |
| **Rezago / *Lag*** | Valor de una observación anterior usado como *feature* | Valor del mes pasado en un informe de tendencias |
| ***Data leakage*** | Usar información del futuro como *feature* | Incluir el resultado final en los indicadores que lo predicen |
| `SUM(CASE WHEN ...)` | Cuenta filas que cumplen una condición dentro de un grupo | CONTAR.SI() en Excel |
| **SQLite** | Base de datos liviana que funciona en memoria | Una base de datos que no necesita servidor |

---

## 11. Conexión con el Módulo Siguiente

En R2-02 construiste una **tabla analítica**: la materia prima que alimenta un modelo de machine learning. Eso es exactamente lo que usarás en el siguiente paso.

**El siguiente módulo es R2-03 · Estadística para modelar.**

Antes de entrenar un modelo hay que entender los datos que le estás pasando. En R2-03 aprenderás a:

- **Describir y explorar** datos: distribuciones, medidas de tendencia central, dispersión.
- **Detectar correlaciones:** qué variables se mueven juntas y qué implica eso para un modelo.
- **Identificar variables relevantes** usando estadístrica antes de entrenar.

> 🔗 **Conexión pedagógica:** R2-02 te enseña a *fabricar* las variables; R2-03 te enseña a *entenderlas* antes de meterlas en un modelo. Un buen científico/a de datos siempre analiza sus *features* antes de entrenar.

¡Sigue con todo! Ya estás construyendo los cimientos del machine learning con datos públicos reales 🚀
