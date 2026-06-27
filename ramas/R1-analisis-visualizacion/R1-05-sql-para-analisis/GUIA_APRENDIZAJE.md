# Guía de Aprendizaje — R1-05 · SQL para análisis

> **Rama:** R1 · Análisis y Visualización | **Módulo:** R1-05 | **Nivel:** Introductorio-Intermedio  
> **Duración estimada:** 3–4 horas | **Prerrequisitos:** R1-04 · Limpieza de datos  
> **Competencia de salida:** Consultar una base de datos SQLite desde Python usando `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY` y funciones de agregación para responder preguntas reales de gestión pública.

---

## 1. ¿Para qué me sirve esto como funcionario/a público/a?

Los sistemas del Estado — SIGFE, ChileCompra, el Registro Civil, los sistemas de salud — no guardan sus datos en archivos Excel. Los guardan en **bases de datos relacionales** que se consultan con SQL. Cada vez que buscas un beneficiario, filtras una licitación o descargas un reporte, alguien (o algo) escribió una consulta SQL.

Aprender SQL te da **acceso directo a los datos** sin depender de que alguien más te exporte un archivo. Puedes pedir exactamente lo que necesitas — sin descargar millones de filas que no vas a usar — y recibir la respuesta en segundos.

En este módulo trabajarás con los **24 Parques Nacionales de Chile** registrados por la CONAF en el Sistema Nacional de Áreas Silvestres Protegidas del Estado (SNASPE). Son datos públicos reales: nombre, región, año de declaración y superficie en hectáreas.

---

## 2. Mapa conceptual del módulo

| Operación | SQL | pandas equivalente | Pregunta que responde |
|---|---|---|---|
| Seleccionar columnas | `SELECT nombre, region` | `df[["nombre", "region"]]` | ¿Qué columnas quiero ver? |
| Todas las filas | `SELECT * FROM parques` | `df` | Ver la tabla completa |
| Filtrar filas | `WHERE region = 'Magallanes'` | `df[df["region"]=="Magallanes"]` | ¿Qué filas cumplen la condición? |
| Ordenar | `ORDER BY superficie_ha DESC` | `.sort_values(ascending=False)` | ¿Cuál es el más grande? |
| Limitar resultados | `LIMIT 5` | `.head(5)` | ¿Cuáles son los 5 primeros? |
| Contar filas | `COUNT(*)` | `len(df)` o `.count()` | ¿Cuántos registros hay? |
| Sumar | `SUM(superficie_ha)` | `.sum()` | ¿Cuánto suman en total? |
| Promedio | `AVG(superficie_ha)` | `.mean()` | ¿Cuál es el promedio? |
| Agrupar | `GROUP BY region` | `.groupby("region")` | ¿Cuánto hay por categoría? |

---

## 3. Antes de empezar: Verificación de prerrequisitos

- [ ] Sé cargar un CSV con `pd.read_csv()` y leer sus columnas
- [ ] Entiendo qué es un DataFrame y cómo filtrar filas
- [ ] Sé usar `.groupby()` para agrupar y resumir datos
- [ ] Entiendo qué es `NaN` y cómo detectarlo
- [ ] Puedo ejecutar celdas de Python en Google Colab

Si tienes dudas en `.groupby()`, repasa **R1-03 · Cruzar y resumir tablas**.

---

## 4. El dataset real: Parques Nacionales de Chile (CONAF/SNASPE)

24 parques nacionales con datos reales de la CONAF. Columnas: `nombre`, `region`, `anio` (de declaración como parque nacional), `superficie_ha`.

**Datos clave del dataset:**

| Dato | Valor |
|---|---|
| Total de parques | 24 |
| Parque más antiguo | Vicente Pérez Rosales (1926) |
| Parque más reciente | Patagonia (2018) |
| Parque más grande | Bdo. O’Higgins — 3.524.648 ha |
| Parque más pequeño | Pali Aike — 5.030 ha |
| Región con más parques | Magallanes (5 parques) |
| Región con más superficie | Magallanes (~5.295.013 ha) |
| Región con menos parques | Varias con 1 parque |

---

## 5. Cómo funciona SQLite desde Python

Antes de entrar al contenido del notebook, entender el flujo de trabajo es clave:

```python
import sqlite3
import pandas as pd

# 1. Crear la base de datos en memoria (no necesitas instalar nada)
con = sqlite3.connect(":memory:")

# 2. Cargar el CSV y escribirlo como tabla SQL
df = pd.read_csv("parques.csv")
df.to_sql("parques", con, index=False, if_exists="replace")

# 3. Consultar con SQL y recibir el resultado como DataFrame
resultado = pd.read_sql("SELECT * FROM parques", con)
```

**¿Qué es `:memory:`?** Una base de datos que vive en la RAM del proceso — no crea ningún archivo en disco. Es perfecta para aprender y analizar: rápida, limpia, desaparece cuando cierras Colab.

**El ciclo completo siempre tiene 3 pasos:** conectar → cargar datos → consultar con `pd.read_sql()`.

---

## 6. Guía paso a paso por sección del notebook

### Sección 1 · Conectar y cargar

**🎯 Objetivo:** Crear la base de datos en memoria y cargar los parques como tabla SQL.

**💡 Concepto clave:** `sqlite3.connect(":memory:")` abre una base de datos que vive solo en RAM. `df.to_sql()` escribe el DataFrame como una tabla SQL con el nombre que tú elijas. Desde ese momento, puedes hacer cualquier consulta SQL sobre esa tabla.

**⚠️ Error frecuente:** Olvidar el parámetro `index=False` en `df.to_sql()`. Sin él, el índice numérico del DataFrame se escribe como una columna extra llamada `index` que contamina la tabla.

**✅ Sabes esta sección cuando puedes:** Ejecutar `pd.read_sql("SELECT COUNT(*) FROM parques", con)` y ver `24`.

---

### Sección 2 · SELECT y WHERE: elegir y filtrar

**🎯 Objetivo:** Seleccionar columnas específicas y filtrar filas por condición.

**💡 Concepto clave:** Una consulta SQL básica tiene siempre dos partes obligatorias: `SELECT` (qué columnas quiero) y `FROM` (de qué tabla). `WHERE` es opcional pero es la cláusula más poderosa: filtra exactamente las filas que cumplen la condición.

**🔍 Ejemplos con datos reales:**

```sql
-- Todos los parques de Magallanes
SELECT nombre, anio, superficie_ha
FROM parques
WHERE region = 'Magallanes';
```
Resultado: 5 parques — Cabo de Hornos, Torres del Paine, Alberto de Agostini, Bdo. O’Higgins, Pali Aike.

```sql
-- Parques declarados antes de 1950
SELECT nombre, region, anio
FROM parques
WHERE anio < 1950;
```
Resultado: 8 parques (desde Vicente Pérez Rosales 1926 hasta Cabo de Hornos 1945).

**Operadores disponibles en `WHERE`:** `=`, `!=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `LIKE`, `IN`, `AND`, `OR`, `NOT`.

**⚠️ Error frecuente:** Usar comillas dobles para texto en SQLite (`WHERE region = "Magallanes"`). SQL usa comillas **simples** para texto: `'Magallanes'`. Las comillas dobles son para nombres de columnas con espacios.

**✅ Sabes esta sección cuando puedes:** Escribir una consulta `WHERE` que devuelva exactamente los parques de La Araucanía (deben ser 4).

---

### Sección 3 · ORDER BY y LIMIT: ordenar y rankear

**🎯 Objetivo:** Producir rankings — los parques más grandes, los más antiguos, el Top 5.

**💡 Concepto clave:** `ORDER BY` ordena el resultado por una columna. `DESC` (descendente) va de mayor a menor; `ASC` (ascendente, el defecto) va de menor a mayor. `LIMIT n` recorta el resultado a las primeras `n` filas — útil para rankings.

**🔍 Ejemplo con datos reales:**

```sql
-- Top 5 parques más grandes de Chile
SELECT nombre, region, superficie_ha
FROM parques
ORDER BY superficie_ha DESC
LIMIT 5;
```

| nombre | region | superficie_ha |
|---|---|---|
| Bernardo O’Higgins | Magallanes | 3.524.648 |
| Laguna San Rafael | Aysén | 1.742.000 |
| Alberto de Agostini | Magallanes | 1.460.000 |
| Patagonia | Aysén | 304.527 |
| Corcovado | Los Lagos | 287.623 |

**Nota:** Los 3 parques más grandes del país concentran más del 85% de la superficie total protegida.

**⚠️ Error frecuente:** Confundir `ORDER BY` con `GROUP BY`. `ORDER BY` solo ordena filas; `GROUP BY` agrupa para calcular agregados. Son operaciones completamente distintas.

**✅ Sabes esta sección cuando puedes:** Obtener el parque con **menor** superficie en una sola consulta SQL (sin filtrar manualmente).

---

### Sección 4 · Funciones de agregación: COUNT, SUM, AVG, MAX, MIN

**🎯 Objetivo:** Resumir toda la tabla en un solo número — o un número por grupo.

**💡 Concepto clave:** Las funciones de agregación colapsan múltiples filas en un único valor. `COUNT(*)` cuenta filas; `SUM()` suma; `AVG()` promedia; `MAX()` y `MIN()` encuentran el extremo.

**🔍 Consultas con datos reales:**

```sql
-- Estadísticas generales
SELECT
  COUNT(*)              AS total_parques,
  SUM(superficie_ha)    AS superficie_total,
  AVG(superficie_ha)    AS superficie_promedio,
  MAX(superficie_ha)    AS parque_mas_grande,
  MIN(superficie_ha)    AS parque_mas_pequeno
FROM parques;
```

| total_parques | superficie_total | superficie_promedio | parque_mas_grande | parque_mas_pequeno |
|---|---|---|---|---|
| 24 | 8.952.904 | 373.038 | 3.524.648 | 5.030 |

**Dato para reflexionar:** El promedio de 373.038 ha no representa ningún parque real — está completamente distorsionado por los 3 mega-parques de la Patagonia. Es un ejemplo clásico de por qué el promedio puede engañar cuando la distribución es muy asimétrica.

**⚠️ Error frecuente:** Usar `COUNT(nombre)` en lugar de `COUNT(*)`. `COUNT(columna)` cuenta solo las filas donde esa columna no es NULL; `COUNT(*)` cuenta todas las filas. Para contar el total de registros, usa siempre `COUNT(*)`.

**✅ Sabes esta sección cuando puedes:** Calcular la superficie promedio de los parques declarados después de 1980 (combinando `WHERE` con `AVG`).

---

### Sección 5 · GROUP BY: resumir por categoría

**🎯 Objetivo:** Calcular un agregado por cada región — la tabla dinámica de SQL.

**💡 Concepto clave:** `GROUP BY` divide la tabla en grupos según el valor de una columna y aplica una función de agregación dentro de cada grupo. Es el equivalente exacto del `.groupby()` de pandas, pero escrito al revés: en SQL la agregación va en el `SELECT` y el agrupador va en el `GROUP BY`.

**🔍 Consulta con datos reales:**

```sql
-- Parques y superficie total por región, ordenado de mayor a menor
SELECT
  region,
  COUNT(*)           AS n_parques,
  SUM(superficie_ha) AS superficie_total
FROM parques
GROUP BY region
ORDER BY superficie_total DESC;
```

| region | n_parques | superficie_total |
|---|---|---|
| Magallanes | 5 | 5.295.013 |
| Aysén | 2 | 2.046.527 |
| Los Lagos | 3 | 584.460 |
| Tarapacá | 1 | 174.744 |
| Arica y Parinacota | 1 | 137.883 |
| Antofagasta | 1 | 268.670 |
| ... | ... | ... |

**Reflexión:** Magallanes concentra el 59% de la superficie de parques nacionales con solo 5 de los 24 parques. Aysén suma otro 23%. Esto refleja la política histórica de conservación en zonas despobladas del sur, no necesariamente en las regiones con mayor biodiversidad en riesgo.

**⚠️ Error frecuente:** Incluir en el `SELECT` una columna que no está en el `GROUP BY` ni dentro de una función de agregación. En SQLite esto a veces funciona sin error pero devuelve un valor arbitrario — en otros motores SQL (PostgreSQL, MySQL) falla. La regla: en el `SELECT` de una consulta con `GROUP BY`, solo van columnas del `GROUP BY` o funciones de agregación.

**✅ Sabes esta sección cuando puedes:** Obtener el año del parque más antiguo por región usando `MIN(anio)` en el `GROUP BY`.

---

## 7. Guía de los 5 Ejercicios

### Ejercicio 01 · Conectar y verificar

**Habilidad que entrena:** Crear la conexión SQLite, cargar el CSV como tabla y confirmar que los datos están.

**Pista suave 🟢:** Necesitas: `sqlite3.connect()`, `df.to_sql()` y `pd.read_sql()` para contar los registros.

**Pista media 🟡:** La consulta de verificación es `SELECT COUNT(*) FROM parques`. El resultado debe ser un DataFrame con una celda: `24`.

**Pista directa 🔴:**
```python
con = sqlite3.connect(":memory:")
df.to_sql("parques", con, index=False, if_exists="replace")
result = pd.read_sql("SELECT COUNT(*) AS total FROM parques", con)
n_parques = result["total"].iloc[0]
```

**✅ El chequeo automático valida que:** `n_parques == 24`.

---

### Ejercicio 02 · Filtrar por región

**Habilidad que entrena:** Usar `WHERE` con condición de igualdad sobre texto.

**Pista suave 🟢:** Escribe una consulta que traiga solo los parques cuya `region` sea `'La Araucanía'`. ¿Cuántos hay?

**Pista media 🟡:** El texto en SQL va entre comillas **simples**. Escribe la región exactamente como aparece en el dataset.

**Pista directa 🔴:**
```python
df_araucania = pd.read_sql(
    "SELECT nombre, anio, superficie_ha FROM parques WHERE region = 'La Araucan\u00eda'",
    con
)
n_araucania = len(df_araucania)
```

**Lógica de la solución:** La Araucanía tiene 4 parques: Tolhuaca (1935), Nahuelbuta (1939), Villarrica (1940), Huerquehue (1967), Conguillío (1987).

**✅ El chequeo automático valida que:** `n_araucania == 5`.

---

### Ejercicio 03 · Top 3 parques más grandes

**Habilidad que entrena:** Combinar `ORDER BY DESC` con `LIMIT` para producir un ranking.

**Pista suave 🟢:** Ordena los parques de mayor a menor superficie y recorta a los 3 primeros.

**Pista media 🟡:** Necesitas `ORDER BY superficie_ha DESC` y `LIMIT 3`. El resultado debe tener exactamente 3 filas.

**Pista directa 🔴:**
```python
top3 = pd.read_sql(
    "SELECT nombre, region, superficie_ha FROM parques ORDER BY superficie_ha DESC LIMIT 3",
    con
)
parque_top1 = top3["nombre"].iloc[0]
```

**Lógica de la solución:** El parque más grande es Bernardo O’Higgins con 3.524.648 ha, seguido por Laguna San Rafael (1.742.000) y Alberto de Agostini (1.460.000).

**✅ El chequeo automático valida que:** `parque_top1 == "Bernardo O'Higgins"` y `len(top3) == 3`.

---

### Ejercicio 04 · Superficie total y promedio

**Habilidad que entrena:** Usar `SUM` y `AVG` para resumir toda la tabla en una sola consulta.

**Pista suave 🟢:** Escribe una consulta con dos funciones de agregación en el mismo `SELECT`: una para la suma total y otra para el promedio.

**Pista media 🟡:** Usa alias con `AS` para nombrar cada columna del resultado: `SUM(superficie_ha) AS total` y `AVG(superficie_ha) AS promedio`.

**Pista directa 🔴:**
```python
estadisticas = pd.read_sql(
    "SELECT SUM(superficie_ha) AS total, AVG(superficie_ha) AS promedio FROM parques",
    con
)
superficie_total = estadisticas["total"].iloc[0]
```

**Lógica de la solución:** Superficie total = 8.952.904 ha. Promedio = ~373.038 ha (muy distorsionado por los mega-parques patagónicos).

**✅ El chequeo automático valida que:** `superficie_total == 8952904`.

---

### Ejercicio 05 · Parques por región

**Habilidad que entrena:** Usar `GROUP BY` con `COUNT(*)` para producir un conteo por categoría.

**Pista suave 🟢:** Quieres saber cuántos parques hay en cada región. Agrupa por `region` y cuenta las filas de cada grupo.

**Pista media 🟡:** `GROUP BY region` y `COUNT(*) AS n_parques`. Para encontrar la región con más parques, ordena de mayor a menor y toma la primera fila.

**Pista directa 🔴:**
```python
por_region = pd.read_sql(
    "SELECT region, COUNT(*) AS n_parques FROM parques GROUP BY region ORDER BY n_parques DESC",
    con
)
region_top = por_region["region"].iloc[0]
```

**Lógica de la solución:** Magallanes lidera con 5 parques, seguida por La Araucanía con 5 y Los Lagos con 3. La región con más parques es Magallanes.

**✅ El chequeo automático valida que:** `region_top == "Magallanes"`.

---

## 8. Sección especial: Conservación, territorio y política ambiental

### El mapa de la protección en Chile

El dataset completo permite ver la evolución de la política de conservación ambiental chilena en casi 100 años:

| Período | Parques declarados | Hito |
|---|---|---|
| 1926–1945 | 7 | Primeras declaraciones, foco en el sur |
| 1958–1970 | 8 | Expansión hacia la Patagonia y el norte |
| 1981–1995 | 5 | Diversificación regional |
| 2005–2018 | 2 | Adiciones recientes, incluyendo el Parque Patagonia |

### Reflexión de política pública

Magallanes y Aysén concentran el **82% de la superficie** de parques nacionales. Pero ¿eso significa que Chile protege bien su biodiversidad?

No necesariamente. Las regiones del centro y norte — donde la presión urbana, agrícola y minera es mayor — tienen muy pocos parques y de pequeña superficie. La Región Metropolitana, con la mayor concentración de población, no tiene ningún parque nacional en este dataset.

> *¿Debería el criterio de declaración de parques nacionales considerar la presión humana sobre el territorio, no solo la disponibilidad de tierras fiscales? ¿Cómo cambiaría el mapa si el criterio fuera la biodiversidad amenazada?*

---

## 9. Conexión con el módulo `profundiza.ipynb`

| Aspecto | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| **Modelo mental** | SQL como herramienta de consulta | Pensar por conjuntos vs. fila a fila |
| **Orden de ejecución** | No se menciona | `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` |
| **NULL** | Se evita | Lógica de tres valores: `TRUE / FALSE / UNKNOWN` |
| **Índices** | No se menciona | Por qué una consulta puede ser instantánea o eterna |
| **¿Para quién?** | Todo participante | Quienes vayan a escribir SQL en producción |

---

## 10. Autoevaluación Final

**Pregunta 1.** ¿Qué hace `SELECT nombre FROM parques WHERE anio < 1950`?
- A) Devuelve todos los campos de los parques declarados antes de 1950
- B) Devuelve solo el nombre de los parques declarados antes de 1950 ✅
- C) Elimina los parques declarados antes de 1950
- D) Ordena los parques por año

*Explicación: `SELECT nombre` elige solo la columna `nombre`. `WHERE anio < 1950` filtra las filas. El resultado es una lista de nombres — sin otras columnas.*

---

**Pregunta 2.** ¿Cuál es la diferencia entre `ORDER BY` y `GROUP BY`?
- A) `ORDER BY` agrupa y `GROUP BY` ordena
- B) `ORDER BY` ordena filas existentes; `GROUP BY` colapsa filas en grupos para agregar ✅
- C) Son sinónimos en SQLite
- D) `GROUP BY` solo funciona con `COUNT`

*Explicación: `ORDER BY` no cambia el número de filas, solo su orden. `GROUP BY` reduce el número de filas: una fila por grupo.*

---

**Pregunta 3.** Ejecutas `SELECT COUNT(*) FROM parques WHERE region = "Magallanes"` y obtienes un error. ¿Cuál es la causa más probable?
- A) La tabla `parques` no existe
- B) `COUNT` no acepta `*` como argumento
- C) Se usaron comillas dobles para el texto; SQL requiere comillas simples ✅
- D) `WHERE` no funciona con `COUNT`

*Explicación: En SQL estándar, los literales de texto van entre comillas simples (`'Magallanes'`). Las comillas dobles se reservan para identificadores (nombres de columnas o tablas).*

---

**Pregunta 4.** ¿Qué devuelve `SELECT region, COUNT(*) FROM parques GROUP BY region`?
- A) Una fila por parque con su región
- B) Una fila por región con el número de parques en esa región ✅
- C) El total de parques en todo el país
- D) Un error porque `COUNT(*)` no se puede usar con `GROUP BY`

*Explicación: `GROUP BY region` colapsa todas las filas de la misma región en un solo grupo. `COUNT(*)` cuenta las filas de cada grupo. Resultado: una fila por región.*

---

**Pregunta 5.** ¿Para qué sirve `LIMIT 5` en una consulta SQL?
- A) Filtra las 5 primeras filas del dataset original
- B) Elimina las filas que no cumplen la condición
- C) Recorta el resultado a las primeras 5 filas del resultado de la consulta ✅
- D) Es equivalente a `WHERE id <= 5`

*Explicación: `LIMIT` actúa al final de la consulta, después de filtrar y ordenar. Recorta el resultado final, no los datos originales.*

---

## 11. Glosario del Módulo

| Término | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **SQL** | Lenguaje estándar para consultar bases de datos relacionales | El idioma para hablar con los sistemas del Estado |
| **SQLite** | Motor de base de datos liviano incluido en Python | Base de datos que no necesita servidor |
| **`SELECT`** | Elige qué columnas mostrar | Seleccionar columnas en Excel |
| **`FROM`** | Indica de qué tabla leer | La hoja de Excel de donde tomas los datos |
| **`WHERE`** | Filtra filas que cumplen la condición | Filtro de Excel |
| **`ORDER BY`** | Ordena el resultado por una columna | Ordenar de mayor a menor en Excel |
| **`LIMIT`** | Recorta el resultado a N filas | Ver solo las primeras N filas |
| **`COUNT(*)`** | Cuenta el número de filas | `CONTAR()` en Excel |
| **`SUM()`** | Suma los valores de una columna | `SUMA()` en Excel |
| **`AVG()`** | Calcula el promedio | `PROMEDIO()` en Excel |
| **`GROUP BY`** | Agrupa filas por categoría para agregar | Tabla dinámica en Excel |
| **`:memory:`** | Base de datos en RAM que no crea archivo en disco | Un cuaderno temporal que desaparece al cerrar |

---

## 12. Conexión con el siguiente módulo

Ya sabes consultar datos con SQL: filtrar, ordenar, rankear y agrupar. A partir de ahora puedes extraer exactamente lo que necesitas de cualquier base de datos — sin descargar todo.

El próximo módulo es **R1-06 · Estadística descriptiva**, donde aprenderás a:
- Calcular e interpretar medidas de tendencia central (media, mediana, moda)
- Entender la dispersión de los datos (desviación estándar, rango intercuartílico)
- Detectar outliers y entender cuándo distorsionan el análisis
- Interpretar un `df.describe()` completo

Pregunta motivadora:

> *En este módulo calculaste que el promedio de superficie de los parques es ~373.000 ha. Pero la mayoría de los parques tienen menos de 100.000 ha. ¿El promedio representa bien la situación típica? ¿Qué otra medida sería más honesta?*

Esa es exactamente la pregunta que abre R1-06. ¡Nos vemos ahí!

---

*Guía elaborada para el Bootcamp de Datos — Formación Pública Chile · Licencia CC BY 4.0*
