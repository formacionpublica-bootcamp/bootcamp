# Guía de Aprendizaje — R1-04 · Limpieza de datos

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 4 · Semana 5

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-04 · Limpieza de datos |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 2 a 3 horas |
| **Nivel** | Básico-intermedio — requiere R1-03 |
| **Prerrequisitos** | `value_counts`, `isna`, filtrar filas, `pd.merge` por una llave |
| **Competencia de salida** | Dejar un dataset del Estado listo para analizar: diagnóstico, texto, sinónimos, números sin la trampa del punto, faltantes e imposibles sin inventar, duplicados, función `limpiar()` y auditoría contra la fuente oficial |
| **Entregable** | Las 8 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula_sucia.csv` (1.545 establecimientos de la matrícula 2025 con errores de planilla inyectados), auditado contra `matricula.csv` (cifra oficial MINEDUC). Profundización: `aire_nuevos.csv` (PM2.5 diario de 14 estaciones SINCA, ene–sep 2026, con faltantes reales) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Buena parte del trabajo con datos en el Estado no es analizar: es **dejar la tabla en condiciones** para poder analizarla. Los consolidados se arman pegando planillas de distintas oficinas, y cada una escribe a su manera: «RM», «Región Metropolitana» y «metropolitana» para la misma región; comunas en MAYÚSCULAS con espacios invisibles; matrículas con punto de miles o con «s/i»; un -1 donde alguien no sabía el dato; una planilla pegada dos veces.

Si analizas eso sin limpiar, tus conclusiones serán incorrectas aunque el análisis esté bien hecho. Y hay errores silenciosos: el más peligroso de este módulo es que `"2.425"` (dos mil cuatrocientos veinticinco, escrito a la chilena) **se convierte en 2,425** sin ningún aviso.

Este módulo usa un caso controlado: la matrícula oficial 2025 con errores inyectados con semilla fija. La ventaja es que, al final, **comparas tu limpieza contra la fuente oficial, fila por fila**, y compruebas que quedó al 100%. En la profundización ya no hay red de seguridad: los faltantes de las estaciones de calidad del aire son **reales** y tendrás que decidir —y declarar— qué hacer con ellos.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Diagnóstico** (`info`, `isna().sum()`, `duplicated().sum()`, `value_counts`) | Mide el desorden antes de tocar nada | Revisar filtros y contar en blanco |
| **`.str.strip()` / `.str.title()`** | Quita espacios y normaliza mayúsculas | ESPACIOS() / NOMPROPIO() |
| **Diccionario de equivalencias** + `.replace()` | Unifica sinónimos («RM» → «Metropolitana») | Buscar y reemplazar, uno por uno |
| **`.map()`** | Traduce todo; lo no previsto queda `NaN` y salta a la vista | BUSCARV a una tabla de códigos |
| **Trampa del punto de miles** | `"2.425"` leído como 2,425 en vez de 2425 | Excel en inglés abriendo un CSV chileno |
| **`pd.to_numeric(..., errors="coerce")`** | Convierte a número; lo que no se puede queda `NaN` | VALOR() con SI.ERROR |
| **`.mask(condición)`** | Tapa con `NaN` los valores imposibles | Borrar la celda dejando la fila |
| **`drop_duplicates()`** | Elimina filas repetidas | Datos → Quitar duplicados |
| **Función `limpiar()`** | Receta reproducible de limpieza | Una macro |
| **Auditoría contra la fuente** | Cruce por RBD y % de coincidencia por columna | Comparar dos hojas con BUSCARV |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Contar valores con `value_counts()` y nulos con `isna().sum()` | ☐ |
| Filtrar filas con una condición | ☐ |
| Cruzar dos tablas con `pd.merge(..., on="rbd")` (R1-03) | ☐ |
| Escribir una función simple con `def` y `return` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar la planilla sucia con `cargar()` y conocer los catálogos oficiales (`REGIONES_OFICIALES`, 16 regiones; `DEPENDENCIAS_OFICIALES`, 5 dependencias).

💡 **Concepto clave:** `cargar()` devuelve **siempre una copia fresca** del archivo sucio. Cada ejercicio parte de cero, así un error en uno no arrastra a los demás.

---

### Sección 1 · Diagnosticar antes de limpiar

🎯 **Objetivo:** Medir el desorden: 1.545 filas, **45 duplicadas**, **61** celdas vacías en `mat_total`, `mat_total` de tipo `object` (texto) y la región escrita de **23 formas** distintas cuando Chile tiene 16.

💡 **Concepto clave:** Que `mat_total` sea `object` es una alarma: hay algo en esa columna que no es número («s/i», «2.425»). Hasta convertirla, no se puede sumar.

✅ **Señal de que entendiste:** Puedes decir, antes de limpiar nada, qué columnas tienen problemas y de qué tipo.

---

### Sección 2 · Limpiar texto

🎯 **Objetivo:** `df["comuna"].str.strip().str.title()`: las 154 comunas en MAYÚSCULAS con espacios quedan normalizadas y las comunas distintas bajan de **385 a 292**.

💡 **Concepto clave:** Normalizar es llevar el dato **al formato de la fuente oficial** (el MINEDUC escribe «Viña Del Mar»), no al gusto de cada uno. Así el dato limpio se puede cruzar con el oficial.

⚠️ **Error frecuente:** Olvidar reasignar. `df["comuna"].str.strip()` calcula el resultado y lo bota; hay que guardar con `df["comuna"] = ...`.

---

### Sección 3 · Categorías con sinónimos

🎯 **Objetivo:** Escribir tres diccionarios: 7 sinónimos de región (`"RM"`, `"Región Metropolitana"`, `"metropolitana"`, `"V Región"`, `"Valparaiso"`, `"Bio Bio"`, `"Biobio"`), 3 de dependencia (`"Part. Subv."`, `"Part. Pagado"`, `"MUNICIPAL"`) y 4 de rural (`"Sí"`, `"No"`, `"1"`, `"0"` → 1/0).

💡 **Concepto clave:** `.replace()` cambia lo que está en el diccionario y deja el resto igual; `.map()` traduce todo y deja `NaN` lo no previsto. Para `rural` conviene `.map()`: si aparece un valor que no imaginaste, lo verás como `NaN` en vez de pasar inadvertido. El diccionario es, además, **documentación auditable** de tu decisión.

✅ **Señal de que entendiste:** La región queda con exactamente las 16 del catálogo y la dependencia con las 5.

---

### Sección 4 · La trampa del punto

🎯 **Objetivo:** Convertir `mat_total` a número sin caer en la trampa: `pd.to_numeric(df["mat_total"].str.replace(".", "", regex=False), errors="coerce")`.

💡 **Concepto clave:** La celda de demostración muestra que `pd.to_numeric("2.425")` devuelve **2.425** (dos coma algo): un liceo de 2.425 estudiantes queda con dos. Sin error ni aviso. En el archivo hay 7 valores así (de 1.082 a 2.425). Hay que **quitar el punto de miles antes** de convertir, y con `regex=False` (en una expresión regular el punto significa «cualquier carácter»). Después de convertir quedan **76** filas sin dato: 61 vacías + 15 «s/i».

⚠️ **Error frecuente:** Creer que «no dio error» significa «está bien». Las conversiones silenciosas son las más peligrosas.

---

### Sección 5 · Valores imposibles

🎯 **Objetivo:** Marcar como `NaN` los **7** establecimientos con `mat_hombres = -1`, usando `.mask()`.

💡 **Concepto clave:** Un -1 no es un número chico: es un código de «no sé». Lo honesto es dejarlo como faltante. Ni 0 ni el promedio: inventar un valor cambia los totales sin que nadie se entere. Y no se borra la fila: el resto de sus datos sí es válido.

---

### Sección 6 · Duplicados

🎯 **Objetivo:** `df.drop_duplicates()`: de 1.545 a **1.500** filas, y verificar que la llave `rbd` quedó única (`df["rbd"].is_unique`).

💡 **Concepto clave:** Un duplicado infla los totales y rompe la llave. Conecta con R1-03: si el RBD se repite, el cruce multiplica filas.

---

### Sección 7 · La función `limpiar()`

🎯 **Objetivo:** Empaquetar los pasos 2 a 6 en una función que recibe la tabla sucia y devuelve la limpia (1.500 filas).

💡 **Concepto clave:** El próximo consolidado traerá los mismos vicios. Con `limpiar()` lo procesas en un segundo, siempre igual, y cualquiera puede leer qué decidiste. Trabaja sobre `out = df.copy()` para no tocar el original.

---

### Sección 8 · Auditoría contra la fuente oficial

🎯 **Objetivo:** Cruzar la tabla limpia con `matricula.csv` por `rbd` y medir la proporción de coincidencias por columna: región, comuna, dependencia, rural y `mat_total` deben dar **100%**.

💡 **Concepto clave:** `(cruce[col] == cruce[col + "_oficial"]).mean()` da la proporción de coincidencias. En `mat_total` se compara solo donde tienes dato: las **75** filas sin matrícula (76 menos una que estaba duplicada) no son un error de limpieza, son información que la planilla no traía, y se **declaran**.

✅ **Señal de que entendiste:** Puedes explicar por qué 100% de coincidencia **no** significa que la tabla esté completa.

---

### Reflexión final

En la tabla oficial, `mat_total` es la suma de hombres y mujeres en 10.927 de 10.945 establecimientos (en 18 no calza). ¿Reconstruirías los totales faltantes con esa regla? Es defendible si lo **declaras** y marcas qué datos son reconstruidos; no lo es si se mezclan sin aviso con los reportados.

---

## 6. Guía de los 8 Ejercicios

### Ejercicio 1 — Mide el desorden

**Pistas progresivas:**
- 🟢 Pista suave: Son cuatro números: duplicados, vacíos de una columna, el tipo de una columna y cuántos valores distintos tiene otra.
- 🟡 Pista media: `df.duplicated().sum()`, `df["mat_total"].isna().sum()`, `str(df["mat_total"].dtype)`, `df["region"].nunique()`.
- 🔴 Pista directa: `n_duplicados = int(df.duplicated().sum())`, `n_faltantes = int(df["mat_total"].isna().sum())`, `tipo_mat_total = str(df["mat_total"].dtype)`, `n_regiones = df["region"].nunique()`.

**¿Qué significa el ✅?** Que mediste los problemas antes de tocar nada: 45 duplicadas, 61 vacías, `mat_total` como texto y 23 formas de escribir 16 regiones.

---

### Ejercicio 2 — Normaliza la columna comuna

**Pistas progresivas:**
- 🟢 Pista suave: Dos métodos de texto encadenados: uno quita espacios, el otro arregla las mayúsculas.
- 🟡 Pista media: `.str.strip()` y luego `.str.title()`. No olvides reasignar.
- 🔴 Pista directa: `df["comuna"] = df["comuna"].str.strip().str.title()` y `n_comunas = df["comuna"].nunique()`.

**¿Qué significa el ✅?** Que las comunas quedaron en el formato oficial: de 385 «comunas distintas» a 292.

---

### Ejercicio 3 — Unifica región, dependencia y rural

**Pistas progresivas:**
- 🟢 Pista suave: Mira el `value_counts()` de cada columna: cada forma que no está en el catálogo oficial es una llave del diccionario.
- 🟡 Pista media: Faltan 5 regiones (`"Región Metropolitana"`, `"metropolitana"`, `"Valparaiso"`, `"Bio Bio"`, `"Biobio"`), 3 dependencias y 3 valores de rural.
- 🔴 Pista directa: `mapa_dependencia = {"Part. Subv.": "Particular subvencionado", "Part. Pagado": "Particular pagado", "MUNICIPAL": "Municipal"}` y `mapa_rural = {"Sí": 1, "No": 0, "1": 1, "0": 0}`.

**¿Qué significa el ✅?** Que las tres columnas quedaron exactamente con los valores del catálogo oficial, sin `NaN` en rural.

---

### Ejercicio 4 — Convierte mat_total sin caer en la trampa

**Pistas progresivas:**
- 🟢 Pista suave: Antes de convertir a número, hay que sacar el carácter que en Chile separa los miles.
- 🟡 Pista media: `.str.replace(".", "", regex=False)` y luego `pd.to_numeric(..., errors="coerce")`.
- 🔴 Pista directa: `df["mat_total"] = pd.to_numeric(df["mat_total"].str.replace(".", "", regex=False), errors="coerce")` y `n_sin_dato = int(df["mat_total"].isna().sum())`.

**¿Qué significa el ✅?** Que `"2.425"` quedó como 2425, no hay matrículas con decimales, y contaste los 76 sin dato.

---

### Ejercicio 5 — Marca los imposibles como faltantes

**Pistas progresivas:**
- 🟢 Pista suave: Primero arma la condición de «imposible»; después usa un método que tapa con `NaN` donde la condición es verdadera.
- 🟡 Pista media: `df["mat_hombres"] < 0` y `.mask(...)`.
- 🔴 Pista directa: `imposibles = df["mat_hombres"] < 0`, `n_imposibles = int(imposibles.sum())`, `df["mat_hombres"] = df["mat_hombres"].mask(imposibles)`.

**¿Qué significa el ✅?** Que los 7 imposibles quedaron como faltantes, sin borrar filas ni inventar números.

---

### Ejercicio 6 — Elimina los duplicados y verifica la llave

**Pistas progresivas:**
- 🟢 Pista suave: Hay un método que bota las filas repetidas; y las Series tienen una propiedad que dice si sus valores son únicos.
- 🟡 Pista media: `drop_duplicates()` y `.is_unique`.
- 🔴 Pista directa: `df = df.drop_duplicates()`, `n_despues = len(df)`, `llave_unica = df["rbd"].is_unique`.

**¿Qué significa el ✅?** Que pasaste de 1.545 a 1.500 filas y el RBD vuelve a identificar a un solo establecimiento.

---

### Ejercicio 7 — Escribe la función limpiar(df)

**Pistas progresivas:**
- 🟢 Pista suave: Es copiar la línea clave de los ejercicios 3 a 6, pero aplicada a `out` en vez de `df`.
- 🟡 Pista media: Reutiliza `mapa_region`, `mapa_dependencia` y `mapa_rural`; termina con `out = out.drop_duplicates()` y `return out`.
- 🔴 Pista directa: `out["region"] = out["region"].replace(mapa_region)` … `out["mat_total"] = pd.to_numeric(out["mat_total"].str.replace(".", "", regex=False), errors="coerce")` … `out["mat_hombres"] = out["mat_hombres"].mask(out["mat_hombres"] < 0)` … `out = out.drop_duplicates()`.

**¿Qué significa el ✅?** Que una sola llamada a `limpiar(cargar())` deja la tabla lista, sin modificar el archivo original.

---

### Ejercicio 8 — Mide la coincidencia con la fuente oficial

**Pistas progresivas:**
- 🟢 Pista suave: Comparar dos columnas da `True`/`False` fila a fila; el promedio de eso es la proporción de coincidencias.
- 🟡 Pista media: `(cruce[col] == cruce[col + "_oficial"]).mean()`; en `mat_total`, filtra antes con `cruce.loc[con_dato, ...]`.
- 🔴 Pista directa: `coincide["mat_total"] = (cruce.loc[con_dato, "mat_total"] == cruce.loc[con_dato, "mat_total_oficial"]).mean()` y `n_sin_dato = int((~con_dato).sum())`.

**¿Qué significa el ✅?** Que tu limpieza reproduce la cifra oficial al 100% en todas las columnas con dato, y que sabes cuántas filas (75) quedan sin matrícula y por qué.

---

> 🔬 **En la profundización:** faltantes **reales**, sin respuesta oficial con la que comparar. PM2.5 diario de 14 estaciones SINCA entre enero y septiembre de 2026. El Bosque no tiene dato en el **47,8%** de los días y Copiapó en el **40,1%**. En El Bosque faltan **enero a abril completos** (el primer dato es del 5 de mayo), así que su promedio (34,0 µg/m³) es **de otoño-invierno**. Rellenar con 0 lo baja a 17,8 (−48%). Y la comparación ingenua con Cerro Navia (26,2) se **invierte** si se mira solo en los 142 días en que ambas midieron: Cerro Navia 36,1 vs El Bosque 34,0. Además, 6 estaciones no tienen sensor de temperatura (faltante **estructural**, no una falla). Cierras con una nota metodológica: usar / usar con advertencia / excluir de comparaciones.

---

## 7. Autoevaluación Final

**Pregunta 1:** `pd.to_numeric("2.425")` devuelve 2.425 sin error. ¿Qué significa?

- A) Que la conversión salió bien
- B) Que Python leyó el punto de miles chileno como punto decimal: el dato quedó mil veces más chico, en silencio ✅
- C) Que el archivo está corrupto
- D) Que hay que usar `int()` en vez de `to_numeric`

**Explicación:** Ningún aviso te salva aquí. Hay que saber cómo escribe los números tu fuente y quitar el separador de miles antes de convertir.

---

**Pregunta 2:** ¿Por qué conviene `.map()` en vez de `.replace()` para traducir `rural`?

- A) Porque es más rápido
- B) Porque `.map()` deja `NaN` lo que no está en el diccionario, y así un valor imprevisto salta a la vista ✅
- C) Porque `.replace()` no funciona con números
- D) Da exactamente lo mismo

**Explicación:** `.replace()` deja igual lo que no conoce y el error pasa inadvertido; `.map()` lo convierte en una alarma visible.

---

**Pregunta 3:** Un establecimiento tiene `mat_hombres = -1`. ¿Qué haces?

- A) Lo dejas: es solo un número negativo
- B) Lo reemplazas por 0
- C) Lo marcas como faltante (`NaN`) y lo declaras; no borras la fila ✅
- D) Lo reemplazas por el promedio de la columna

**Explicación:** Es un código de «no sé». Cualquier número inventado cambia los totales sin dejar rastro.

---

**Pregunta 4:** ¿Por qué se normaliza el texto **antes** de buscar duplicados?

- A) Por costumbre
- B) Porque dos filas iguales escritas con distinta mayúscula o espacios no se detectan como duplicadas hasta normalizar ✅
- C) Porque `drop_duplicates` borra el texto
- D) No importa el orden

**Explicación:** Para el computador, «LA FLORIDA » y «La Florida» son distintos. Primero se iguala la forma, después se buscan repetidos.

---

**Pregunta 5:** La auditoría dio 100% de coincidencia, pero quedan 75 filas sin `mat_total`. ¿Qué reportas?

- A) Que la tabla está completa
- B) Que la limpieza reproduce la fuente donde había dato, y que 75 establecimientos no traían matrícula en la planilla (declarado) ✅
- C) Rellenas las 75 con el promedio para que no se note
- D) Borras las 75 filas sin decir nada

**Explicación:** Coincidir al 100% habla de la calidad de tu limpieza, no de la completitud del dato. Lo que falta se declara.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Diagnóstico** | Medir los problemas antes de corregir | Revisar el consolidado antes de firmarlo |
| **`NaN`** | Marca de «aquí falta el dato» | La celda en blanco |
| **Normalizar** | Llevar el texto a un formato único | Escribir las comunas como en el registro oficial |
| **Catálogo oficial** | Lista válida de valores de una categoría | La lista de 16 regiones, la codificación de dependencias |
| **Diccionario de equivalencias** | `{"como viene": "como debe quedar"}` | La tabla de homologación |
| **Separador de miles** | En Chile el punto (2.425); en inglés la coma | El formato regional de Excel |
| **`errors="coerce"`** | Lo que no se puede convertir queda `NaN` | Marcar «s/i» como sin información |
| **Valor imposible** | Dato presente pero que no puede ser real | Un -1, una edad de 200 años |
| **Duplicado** | Fila repetida exacta | La planilla pegada dos veces |
| **Auditoría** | Comparar el resultado con una fuente confiable | Cuadrar contra el registro oficial |
| **Faltante estructural** | Falta porque no se mide, no porque se perdió | La estación sin sensor de temperatura |

---

## 9. Conexión con el Módulo Siguiente

En R1-04 dejaste una planilla sucia idéntica a la fuente oficial, y aprendiste a declarar lo que no se puede recuperar.

En **R1-05 · SQL para análisis** dejarás de traer tablas enteras a Python: le harás preguntas directamente a una **base de datos** con SQL, sobre la matrícula 2025 y su directorio oficial — filtrar, agrupar, cruzar con `JOIN` y volver a cazar los RBD huérfanos, ahora con `LEFT JOIN`.

> 💡 **Pregunta para reflexionar:** En tu servicio, ¿quién limpia los consolidados antes de que se publiquen? ¿Queda escrito en algún lado qué se corrigió?
