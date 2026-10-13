# Guía de Aprendizaje — R2-01 · Datos: traer, cruzar y limpiar

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 1 · Semana 3

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-01 · Datos: traer, cruzar y limpiar |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Básico — requiere R2-00 |
| **Prerrequisitos** | Filtrar con máscaras, `groupby`, `isna()` |
| **Competencia de salida** | Construir un dataset analítico limpio: cruzar mediciones con su catálogo, corregir tipos, diagnosticar faltantes reales y declarar cada decisión de limpieza |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 y meteorología diaria, 14 estaciones SINCA, 2020–2025, 30.674 filas) × `estaciones.csv` (comuna, región y coordenadas de las 14 estaciones). Profundización: `matricula_rbd.csv` × `directorio_establecimientos.csv` (MINEDUC 2025) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Ningún dato del Estado llega listo para usar. Las mediciones viven en una tabla y el catálogo que dice **dónde** se midió, en otra; las fechas llegan como texto; y siempre hay huecos. Antes de cualquier modelo o informe, alguien tiene que armar el **dataset analítico** — y ese alguien eres tú.

Este módulo usa problemas **reales** del registro de calidad del aire, no errores inventados:

- **7 de las 14 estaciones nunca midieron temperatura ni humedad**: no tienen sensor. Imputar ahí sería inventar datos.
- **1.030 días-estación no tienen PM2.5** (mantenimiento, fallas).
- En **Las Encinas Temuco, los 240 registros de humedad son exactamente 0 %** — un valor imposible para una ciudad del sur de Chile. Es un sensor que reporta ceros, no un clima.

La lección más importante no es técnica: limpiar no es «borrar lo feo», es **diagnosticar, decidir y dejar escrito por qué**. Un informe que dice «se excluyeron 1.030 días sin medición y se anularon 230 humedades de 0 % por error de sensor» es auditable. Uno que no lo dice, no.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Llave** | Columna compartida que conecta dos tablas (`estacion`) | La columna que le das a BUSCARV |
| **`merge(..., how="left")`** | Pega el catálogo a cada medición sin perder filas | BUSCARV con los #N/A visibles |
| **Fila huérfana** | Medición cuya llave no está en el catálogo | El #N/A |
| **`pd.to_datetime`** | Convierte texto en fecha real | Formato de celda «Fecha» |
| **`.dt.year` / `.dt.month`** | Extrae año y mes | `=AÑO()` / `=MES()` |
| **`isna().groupby(...).mean()`** | Proporción de faltantes por grupo | Contar vacíos por estación con una tabla dinámica |
| **`dropna(subset=...)`** | Descarta filas sin dato en una columna | Filtrar y borrar vacíos |
| **`duplicated(subset=...)`** | Detecta llaves repetidas | Formato condicional «duplicados» |
| **`np.nan`** | Marca un valor como faltante | Dejar la celda vacía a propósito |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar filas con una máscara booleana | ☐ |
| Usar `groupby(...).mean()` | ☐ |
| Detectar valores faltantes con `isna()` y contarlos con `.sum()` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar las dos tablas: `df` (30.674 mediciones) y `estaciones` (14 filas).

💡 **Concepto clave:** La celda baja ambos archivos si faltan («en vivo o caché»). Mira las primeras filas de `df`: la estación «21 de Mayo» ya muestra `NaN` en temperatura. Es la primera pista del ejercicio 3.

---

### Sección 1 · Cruzar tablas con `merge`

🎯 **Objetivo:** Enriquecer cada medición con su `comuna` y `region`.

💡 **Concepto clave:** Con `how="left"` conservas las 30.674 mediciones; si alguna estación no estuviera en el catálogo, su región quedaría nula. Aquí el resultado es **0 huérfanas**: las 14 estaciones calzan. Ese 0 no es trivial — es **la prueba** de que el cruce es completo, y se reporta igual.

⚠️ **Error frecuente:** Cruzar con el modo por defecto (`inner`) y no revisar si se perdieron filas.

✅ **Señal de que entendiste:** Puedes explicar por qué contar huérfanas vale la pena incluso cuando el resultado es 0.

---

### Sección 2 · Corregir tipos: las fechas

🎯 **Objetivo:** Convertir `fecha` de texto a `datetime` y crear `anio` y `mes`.

💡 **Concepto clave:** Mientras `fecha` sea texto, pandas no sabe que «2024-07-01» es invierno. Tras `pd.to_datetime`, el accesor `.dt` extrae año (2020–2025) y mes (1–12). El mes es la variable que más explica el PM2.5: el gráfico final lo muestra.

⚠️ **Error frecuente:** Intentar `aire["fecha"].dt.month` **antes** de convertir: da `AttributeError` («Can only use .dt accessor with datetimelike values»).

---

### Sección 3 · Faltantes reales: diagnosticar antes de decidir

🎯 **Objetivo:** Medir la proporción de nulos de `temp_media` por estación, identificar las estaciones sin meteorología y descartar los días sin PM2.5.

💡 **Concepto clave:** Hay dos tipos de hueco y merecen decisiones distintas:

- **Estructural:** 7 estaciones (21 de Mayo, Antofagasta, Bomberos, Centro Quintero, Concón, Copiapó Sivica y Nielol) tienen **100 %** de nulos en temperatura: no tienen sensor. **No se imputa**; se declara que la meteorología solo existe en 7 de 14 estaciones.
- **Puntual:** 1.030 días-estación sin PM2.5. Para analizar PM2.5 no aportan: se **descartan** con `dropna(subset=["pm25"])`, quedando **29.644** filas.

⚠️ **Error frecuente:** Usar `dropna()` **sin** `subset`: botaría también todas las filas de las 7 estaciones sin meteorología — perderías la mitad del país sin darte cuenta.

✅ **Señal de que entendiste:** Puedes explicar por qué imputar la temperatura de Antofagasta con el promedio de las otras estaciones sería inventar datos.

---

### Sección 4 · Decisiones de limpieza: duplicados y valores imposibles

🎯 **Objetivo:** Verificar que la llave `(fecha, estacion)` no se repita y anular las humedades de 0 %.

💡 **Concepto clave:** El conteo de duplicados da **0**: cada estación tiene un registro por día. Las humedades de 0 % son **230** en `limpio` (240 en el archivo; 10 caen en días sin PM2.5 ya descartados) y **todas** son de Las Encinas Temuco — de hecho, **todos** los registros de humedad de esa estación son 0. Un dato imposible se convierte en `np.nan`: deja de mentir y queda contado como faltante.

⚠️ **Error frecuente:** Hacer `limpio[limpio["humedad_media"] == 0]["humedad_media"] = np.nan` (asignación encadenada): pandas avisa (`SettingWithCopyWarning` o similar) y la tabla puede quedar sin cambios. Usa `limpio.loc[condición, "humedad_media"] = np.nan`.

---

### Reflexión final

Escribir la nota metodológica (qué, por qué y cuántas filas) es parte del entregable profesional aunque no tenga chequeo. Ejemplo: *«Meteorología disponible en 7 de 14 estaciones (no imputada). Se excluyeron 1.030 días-estación sin PM2.5. Se anularon 230 registros de humedad 0 % (Las Encinas Temuco, error de sensor). Sin duplicados de llave.»*

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Enriquece cada medición con su comuna y región

**Pistas progresivas:**
- 🟢 Pista suave: La llave es la columna que aparece en ambas tablas. El tipo de cruce debe conservar todas las mediciones.
- 🟡 Pista media: `df.merge(estaciones, on="...", how="left")`; las huérfanas son las de `region` nula.
- 🔴 Pista directa: `aire = df.merge(estaciones, on="estacion", how="left")` y `n_huerfanas = int(aire["region"].isna().sum())`.

**¿Qué significa el ✅?** Que el cruce conservó las 30.674 filas, sumó `comuna` y `region`, y auditaste las huérfanas (0).

---

### Ejercicio 2 — Convierte `fecha` a datetime y crea `anio` y `mes`

**Pistas progresivas:**
- 🟢 Pista suave: Hay una función de pandas que convierte texto en fecha; después, un accesor para sacarle partes.
- 🟡 Pista media: `pd.to_datetime(...)` y luego `.dt.year` / `.dt.month`.
- 🔴 Pista directa: `aire["fecha"] = pd.to_datetime(aire["fecha"])`, `aire["anio"] = aire["fecha"].dt.year`, `aire["mes"] = aire["fecha"].dt.month`.

**¿Qué significa el ✅?** Que `fecha` es de tipo fecha, los meses van de 1 a 12 y los años de 2020 a 2025.

---

### Ejercicio 3 — Diagnostica los nulos y descarta los días sin PM2.5

**Pistas progresivas:**
- 🟢 Pista suave: `isna()` da `True` en los vacíos; el promedio de `True`/`False` es la proporción. Hazlo por estación.
- 🟡 Pista media: `aire["temp_media"].isna().groupby(aire["estacion"]).mean()`; las estaciones sin sensor tienen proporción `1`.
- 🔴 Pista directa: `sin_meteo = sorted(pct_nulos_temp[pct_nulos_temp == 1].index)`, `n_nulos_pm25 = int(aire["pm25"].isna().sum())`, `limpio = aire.dropna(subset=["pm25"])`.

**¿Qué significa el ✅?** Que encontraste las 7 estaciones sin meteorología y que `limpio` no tiene ningún PM2.5 faltante (29.644 filas).

---

### Ejercicio 4 — Cuenta duplicados y anula las humedades imposibles

**Pistas progresivas:**
- 🟢 Pista suave: `duplicated` acepta las columnas que forman la llave. Para el valor imposible, filtra `== 0` y asigna `np.nan` con `.loc`.
- 🟡 Pista media: `limpio.duplicated(subset=["fecha", "estacion"]).sum()`; `(limpio["humedad_media"] == 0).sum()`.
- 🔴 Pista directa: `limpio.loc[limpio["humedad_media"] == 0, "humedad_media"] = np.nan`.

**¿Qué significa el ✅?** Que verificaste la unicidad de la llave (0 duplicados) y que ya no quedan humedades de 0 % (230 anuladas).

---

> 🔬 **En la profundización:** el mismo oficio sobre la **matrícula 2025 por RBD** × el **directorio oficial** del MINEDUC. Verificas que el RBD sea único en ambas tablas, comparas `inner` (10.945 filas) con `left` (10.949), cazas las **4 huérfanas reales** (RBD con matrícula pero sin estado «funcionando», que suman **57 estudiantes**) y decides no botarlas sino etiquetarlas como `"Sin directorio"` con `fillna`, para que el total nacional de estudiantes no pierda a nadie.

---

## 7. Autoevaluación Final

**Pregunta 1:** Cruzas mediciones con su catálogo usando `how="left"` y obtienes 0 huérfanas. ¿Qué haces con ese dato?

- A) Nada, es irrelevante
- B) Lo reportas: demuestra que el cruce es completo ✅
- C) Cambias a `inner` para estar seguro
- D) Repites el cruce hasta que aparezcan huérfanas

**Explicación:** Un 0 verificado es evidencia de calidad. Lo que no se cuenta, no se puede afirmar.

---

**Pregunta 2:** 7 estaciones tienen 100 % de nulos en temperatura. ¿Qué es lo correcto?

- A) Imputar con el promedio nacional
- B) Imputar con la estación más cercana sin decirlo
- C) No imputar y declarar que la meteorología solo existe en 7 de 14 estaciones ✅
- D) Borrar esas 7 estaciones del dataset

**Explicación:** Un faltante estructural (no hay sensor) no se rellena: se declara. Borrar las estaciones perdería su PM2.5, que sí es válido.

---

**Pregunta 3:** ¿Por qué `aire.dropna()` sin argumentos es peligroso aquí?

- A) Es más lento
- B) Botaría toda fila con cualquier nulo, incluidas todas las de las estaciones sin meteorología ✅
- C) No elimina nada
- D) Cambia el tipo de las fechas

**Explicación:** `dropna(subset=["pm25"])` descarta solo lo que la pregunta necesita descartar.

---

**Pregunta 4:** Encuentras humedades de 0 % en todos los registros de una estación. ¿Qué haces?

- A) Las dejas: es el dato oficial
- B) Las conviertes en faltantes (`np.nan`) y lo declaras como error de sensor ✅
- C) Las reemplazas por 50 %
- D) Borras la estación completa

**Explicación:** Un valor imposible no es un dato, es un error de registro. Como faltante declarado, deja de sesgar promedios.

---

**Pregunta 5:** `aire["fecha"].dt.month` da `AttributeError`. ¿La causa más probable?

- A) La columna no existe
- B) `fecha` todavía es texto: falta `pd.to_datetime` ✅
- C) El mes no existe en pandas
- D) Hay nulos en la fecha

**Explicación:** El accesor `.dt` solo funciona sobre columnas de tipo fecha.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Dataset analítico** | Tabla limpia y cruzada lista para analizar o modelar | La base «oficial» del informe |
| **Catálogo** | Tabla que describe las entidades (aquí, estaciones) | El maestro de establecimientos, de comunas |
| **Llave** | Columna que conecta tablas | Código de estación, RBD, RUT, CUT |
| **`datetime`** | Tipo de dato fecha | Celda con formato fecha |
| **Faltante estructural** | Hueco porque el dato nunca se midió | La estación sin sensor |
| **Faltante puntual** | Hueco ocasional en un dato que sí se mide | El día de mantenimiento |
| **Valor imposible** | Valor fuera de lo físicamente posible | Humedad 0 % en Temuco |
| **Imputar** | Rellenar un faltante con un valor estimado | «Completar» una planilla |
| **Nota metodológica** | Registro de las decisiones de limpieza | El anexo metodológico del informe |

---

## 9. Conexión con el Módulo Siguiente

En R2-01 armaste un dataset analítico del aire: cruzado con su catálogo, con fechas reales, y con cada faltante diagnosticado y cada decisión declarada.

En **R2-02 · SQL para *features*** vas a cargar este mismo registro en una base SQLite y **fabricar variables** con SQL: promedios por estación y mes, la etiqueta de episodio de cada día (alerta, preemergencia, emergencia), el PM2.5 de ayer y la media de la semana previa — y vas a aprender por qué esa media **no puede incluir el día de hoy**.

> 💡 **Pregunta para reflexionar:** ¿Qué faltantes «estructurales» tienen las bases de tu servicio — datos que nunca se registraron — y quién los está rellenando sin decirlo?
