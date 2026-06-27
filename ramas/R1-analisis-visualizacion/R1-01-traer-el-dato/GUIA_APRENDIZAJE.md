# Guía de Aprendizaje — R1-01 · Traer el dato: archivos, JSON y APIs

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 1 · Semana 2

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-01 · Traer el dato |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Básico — requiere haber completado R1-00 |
| **Prerrequisitos** | R1-00 completo (variables, listas, diccionarios, bucles) |
| **Competencia de salida** | Traer datos públicos desde archivos y APIs de forma robusta, aplicando el patrón en vivo o caché |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `compras_ml.csv` — compras públicas (ChileCompra) + respuestas JSON tipo API |

---

## 2. ¿Para qué me sirve esto como funcionario público?

En el Estado, los datos viven en lugares distintos: archivos que te mandan por correo, portales web con descarga directa, sistemas que exponen APIs, bases de datos institucionales. Hoy, para cada fuente, tienes que hacer un proceso manual distinto: descargar, abrir, copiar, pegar.

Este módulo te enseña a **automatizar ese proceso de ingesta**. Aprenderás a escribir funciones que cargan datos desde cualquier fuente en una sola línea, a leer el formato JSON que usan las APIs públicas (como el API de ChileCompra o el SIAF), y a construir código que **no se rompe** cuando la fuente remota falla.

El resultado práctico: en vez de descargar manualmente el reporte mensual de compras, tu script lo trae solo, lo procesa y guarda el resumen. Cada mes, un clic.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en el trabajo del Estado |
|----------|-----------|--------------------------------------|
| **Función** | Encapsula instrucciones reutilizables con nombre | Macro de Excel o procedimiento estándar documentado |
| **`pd.read_csv(ruta)`** | Lee un archivo CSV y lo convierte en tabla | Abrir un archivo Excel |
| **JSON** | Formato de texto para intercambiar datos entre sistemas | El XML de los oficios, pero más legible |
| **`json.loads(texto)`** | Convierte un texto JSON en diccionarios/listas de Python | Copiar datos de un correo a una planilla |
| **Patrón en vivo o caché** | Intenta la fuente remota; si falla, usa la copia local | Tener una copia de respaldo del informe por si el sistema cae |
| **`try / except`** | Maneja errores sin que el programa se detenga | Tener un plan B para cuando el sistema está caído |
| **`df.to_csv(ruta)`** | Guarda un DataFrame como archivo CSV | Exportar desde Excel a CSV para compartir |
| **`groupby().sum()`** | Agrupa filas y suma los valores de una columna | Tabla dinámica de Excel |

---

## 4. Verificación de Prerrequisitos

Antes de empezar, verifica que puedas hacer lo siguiente:

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué es una variable en Python | ☐ |
| Escribir un bucle `for` que recorre una lista | ☐ |
| Usar `.get(clave, 0)` en un diccionario | ☐ |
| Haber completado los 4 ejercicios de R1-00 con ✅ | ☐ |

Si respondiste No a alguna, vuelve a R1-00 antes de continuar. Este módulo construye directamente sobre esas bases.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación del entorno

🎯 **Objetivo:** Cargar el dataset base de compras públicas y tener el entorno listo.

💡 **Concepto clave:** Esta celda aplica ya el patrón que aprenderás en la sección 3: primero revisa si el archivo existe localmente, y si no lo baja desde el repositorio. Es la primera vez que ves el patrón "en vivo o caché" en acción, aunque todavía no lo hayas estudiado formalmente.

🔍 **Qué hace el código:**
- `import json, urllib.request, os` → trae las herramientas para manejar JSON, descargar URLs y el sistema de archivos
- `if not os.path.exists(CSV)` → verifica si el CSV ya está en disco
- `urllib.request.urlretrieve(url, CSV)` → descarga el archivo desde GitHub si no existe
- `df = pd.read_csv(CSV)` → carga el CSV como DataFrame
- `df.head()` → muestra las primeras filas para confirmar que todo cargó

⚠️ **Error frecuente:** Si ves `ConnectionError` o `URLError`, Colab no tiene acceso a internet. Verifica que el runtime esté conectado (menú Runtime → Connect).

✅ **Señal de que entendiste:** Ves la tabla con columnas `monto_total`, `categoria`, `region_comprador`.

---

### Sección 1 · Funciones para cargar datos

🎯 **Objetivo:** Escribir una función `cargar_csv` que recibe una ruta y devuelve un DataFrame.

💡 **Concepto clave:** Una **función** es un bloque de código con nombre que recibe entradas (`parámetros`) y devuelve una salida (`return`). En vez de repetir `pd.read_csv("archivo.csv")` en cada parte del código, lo encapsulas en `cargar_csv(ruta)` y lo llamas cuando lo necesitas. Si mañana cambia la forma de cargar el archivo, solo cambias la función, no todo el código. En el Estado: equivale a tener un procedimiento estándar documentado que todos usan igual.

🔍 **Qué hace el código:**
- `def cargar_csv(ruta):` → define la función con un parámetro llamado `ruta`
- el cuerpo de la función debe contener `return pd.read_csv(ruta)`
- `datos = cargar_csv("compras_ml.csv")` → llama la función con una ruta concreta
- `datos.shape` → verifica que la tabla tiene el número correcto de filas y columnas

⚠️ **Error frecuente:** Olvidar la palabra `return`. Una función sin `return` ejecuta el código pero no entrega nada; `datos` quedaría como `None`.

✅ **Señal de que entendiste:** `cargar_csv("compras_ml.csv").shape` devuelve el mismo resultado que `df.shape`.

---

### Sección 2 · JSON: el formato de las APIs

🎯 **Objetivo:** Parsear una respuesta JSON y extraer datos estructurados de ella.

💡 **Concepto clave:** **JSON** (JavaScript Object Notation) es el formato en que casi todas las APIs públicas devuelven datos: el API de ChileCompra, el SIAF, el Registro Civil, Datos Abiertos. Es texto que parece un diccionario de Python. `json.loads()` convierte ese texto en objetos Python reales (diccionarios y listas) que puedes recorrer normalmente. En el trabajo del Estado: cuando conectas un sistema con otro (interoperabilidad), el JSON es el idioma común.

🔍 **Qué hace el código:**
- `respuesta` → una cadena de texto que simula la respuesta de una API
- `data = json.loads(respuesta)` → convierte el texto en un diccionario Python
- `data["results"]` → accede a la lista de registros dentro del diccionario
- `montos = [r["monto"] for r in data["results"]]` → extrae el campo `monto` de cada registro (comprensión de lista)
- `total = sum(montos)` → suma todos los montos

⚠️ **Error frecuente:** Confundir la cadena JSON (`respuesta`, que es texto) con el objeto Python (`data`, que es un diccionario). No puedes hacer `respuesta["results"]` directamente; primero debes pasar por `json.loads()`.

✅ **Señal de que entendiste:** `total` es 1300 (500 + 800) y `len(data["results"])` es 2.

---

### Sección 3 · En vivo o caché: APIs que no fallan

🎯 **Objetivo:** Escribir una función que intenta cargar datos de una URL remota y, si falla, usa un archivo local de respaldo.

💡 **Concepto clave:** El patrón **en vivo o caché** es fundamental en entornos públicos donde los sistemas pueden estar caídos por mantenimiento, por feriado o por incidentes. La idea: intenta siempre la fuente más fresca (URL remota); si falla por cualquier razón, usa la copia local que tienes guardada. Tu análisis siempre corre, aunque el sistema esté caído. `try/except` es la estructura de Python para implementarlo: el bloque `try` intenta algo, y si lanza cualquier error, el bloque `except` ejecuta el plan B.

🔍 **Qué hace el código:**
- `def cargar_o_cache(url, ruta_local):` → función con dos parámetros: la URL remota y el archivo local de respaldo
- `try: return pd.read_csv(url)` → intenta cargar desde la URL
- `except Exception:` → captura cualquier error (conexión fallida, URL inválida, timeout)
- en el `except` debes escribir `return pd.read_csv(ruta_local)` → el plan B
- la prueba usa una URL inválida a propósito para forzar el camino de caché

⚠️ **Error frecuente:** Poner el `return pd.read_csv(ruta_local)` dentro del `try` en vez del `except`. Si lo pones en el `try`, siempre cargará el archivo local sin intentar la URL.

✅ **Señal de que entendiste:** `len(d)` es igual a `len(df)`, aunque la URL era inválida. La función cayó silenciosamente al plan B.

---

### Sección 4 · Guardar el resultado

🎯 **Objetivo:** Agrupar los datos por categoría, calcular el gasto total por cada una y guardar el resumen como CSV.

💡 **Concepto clave:** Después de procesar datos, siempre hay que **persistir el resultado** para compartirlo con otros o reutilizarlo sin tener que reprocesar todo. `to_csv()` guarda un DataFrame en disco. El parámetro `index=False` evita que se escriba la columna de índice numérico que no forma parte de los datos reales. En el Estado: equivale a generar el informe final y guardarlo en la carpeta compartida del equipo.

🔍 **Qué hace el código:**
- `df.groupby("categoria")["monto_total"].sum()` → agrupa por categoría y suma los montos (tabla dinámica)
- `.reset_index()` → convierte el resultado en un DataFrame normal con columnas `categoria` y `monto_total`
- la línea `TODO` debe ser `resumen.to_csv("resumen_categorias.csv", index=False)`
- `os.path.exists(...)` → verifica que el archivo efectivamente quedó guardado en disco

⚠️ **Error frecuente:** Omitir `index=False`. El archivo se guardará con una columna extra de números (0, 1, 2...) que no tiene significado y puede confundir a quien abra el CSV después.

✅ **Señal de que entendiste:** El archivo `resumen_categorias.csv` existe, tiene exactamente tantas filas como categorías únicas hay en el dataset, y no tiene columna de índice.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Escribe `cargar_csv`

**Objetivo:** Crear una función que encapsula la carga de un CSV.
**Habilidad que entrena:** Definición de funciones con `def` y `return`.

**Pistas progresivas:**
- 🟢 Pista suave: Una función en Python se define con `def nombre(parametros):` y termina con `return resultado`. Tu función recibe una ruta y devuelve una tabla.
- 🟡 Pista media: Dentro de la función, usa `pd.read_csv(ruta)` para cargar el archivo y `return` para devolverlo.
- 🔴 Pista directa: `def cargar_csv(ruta): return pd.read_csv(ruta)`

**Lógica de la solución:** La función es un envoltorio minimal: recibe el nombre del archivo, se lo pasa a pandas y devuelve el resultado. La utilidad está en que ahora puedes llamar `cargar_csv("cualquier_archivo.csv")` en cualquier parte del código sin repetir la lógica.

**¿Qué significa el ✅?** Que `cargar_csv("compras_ml.csv").shape` coincide con `df.shape`. La función carga exactamente los mismos datos.

---

### Ejercicio 2 — Parsea una respuesta y suma los montos

**Objetivo:** Convertir un texto JSON en objetos Python y extraer valores de él.
**Habilidad que entrena:** `json.loads()`, acceso a diccionarios anidados, comprensión de lista.

**Pistas progresivas:**
- 🟢 Pista suave: `data` ya está definido arriba con `json.loads(respuesta)`. Es un diccionario. Dentro tiene una clave `"results"` que contiene una lista de diccionarios, cada uno con un campo `"monto"`.
- 🟡 Pista media: Para extraer los montos, recorre `data["results"]` con una comprensión de lista y toma `r["monto"]` de cada elemento.
- 🔴 Pista directa: `montos = [r["monto"] for r in data["results"]]` y `total = sum(montos)`.

**Lógica de la solución:** `json.loads` transforma el texto en una estructura Python. Luego navegas igual que con cualquier diccionario: `data["results"]` es la lista, y cada elemento de la lista es un diccionario con claves `"categoria"` y `"monto"`.

**¿Qué significa el ✅?** Que `total` es exactamente 1300 (500 + 800) y que procesaste los dos registros correctamente.

---

### Ejercicio 3 — Escribe `cargar_o_cache`

**Objetivo:** Implementar el patrón en vivo o caché con `try/except`.
**Habilidad que entrena:** Manejo de errores, `try/except`, funciones con plan B.

**Pistas progresivas:**
- 🟢 Pista suave: La estructura `try/except` ejecuta el bloque `try` y, si ocurre cualquier error, salta al bloque `except`. Tu plan B está en el `except`.
- 🟡 Pista media: En el `except`, carga el archivo local con `pd.read_csv(ruta_local)` y devuelve el resultado.
- 🔴 Pista directa: En el bloque `except Exception`: `return pd.read_csv(ruta_local)`.

**Lógica de la solución:** La URL `http://no-existe.invalid/x.csv` falla intencionalmente. Python lanza una excepción, el `except` la captura y ejecuta el plan B: cargar desde `ruta_local`. El resultado es el mismo que si la URL hubiera funcionado.

**¿Qué significa el ✅?** Que `len(d) == len(df)`: la función entregó los datos correctos a pesar de que la URL era inválida.

---

### Ejercicio 4 — Guarda un resumen por categoría

**Objetivo:** Persistir un resumen agrupado como archivo CSV.
**Habilidad que entrena:** `groupby`, `reset_index`, `to_csv(index=False)`.

**Pistas progresivas:**
- 🟢 Pista suave: `resumen` ya está calculado arriba. Solo necesitas guardarlo en disco con el nombre `"resumen_categorias.csv"`.
- 🟡 Pista media: Los DataFrames de pandas tienen un método `.to_csv()` que acepta el nombre del archivo. Usa el parámetro `index=False` para no incluir la columna de índice.
- 🔴 Pista directa: `resumen.to_csv("resumen_categorias.csv", index=False)`.

**Lógica de la solución:** `groupby("categoria")["monto_total"].sum()` hace el equivalente de una tabla dinámica. `.reset_index()` convierte el resultado en un DataFrame limpio. `to_csv` lo escribe al disco.

**¿Qué significa el ✅?** Que el archivo existe (`existe is True`) y que tiene exactamente tantas filas como categorías únicas. El resumen está guardado y listo para compartir.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la diferencia entre `pd.read_csv("archivo.csv")` y una función `cargar_csv(ruta)`?

- A) No hay diferencia, son exactamente lo mismo
- B) La función encapsula la lógica con un nombre reutilizable; si cambia la forma de cargar, solo se modifica la función ✅
- C) La función es más rápida que llamar `pd.read_csv` directamente
- D) La función solo funciona con archivos locales

**Explicación:** La función no cambia el rendimiento, pero sí mejora el mantenimiento del código. Si mañana necesitas agregar validaciones (verificar que el archivo exista, manejar encoding), solo modificas la función en un lugar.

---

**Pregunta 2:** Tienes este texto: `'{"total": 5, "datos": [1, 2, 3]}'`. ¿Cómo accedes al primer elemento de `"datos"`?

- A) `texto["datos"][0]`
- B) `json.loads(texto)["datos"][0]` ✅
- C) `json.read(texto).datos[0]`
- D) No se puede acceder a elementos individuales en JSON

**Explicación:** Primero debes convertir el texto en objeto Python con `json.loads()`. Después lo navegas como cualquier diccionario: `["datos"]` para la lista, `[0]` para el primer elemento.

---

**Pregunta 3:** ¿Qué ocurre si pones `return pd.read_csv(ruta_local)` dentro del bloque `try` en `cargar_o_cache`?

- A) La función funciona igual, no hay diferencia
- B) La función siempre cargará el archivo local sin intentar la URL remota nunca ✅
- C) Python lanza un error de sintaxis
- D) La función intenta ambas fuentes y elige la más reciente

**Explicación:** Si el `return ruta_local` está en el `try`, se ejecuta antes de intentar la URL (o justo después, según el orden). En cualquier caso, el `except` nunca se activa porque no hay error. El patrón solo funciona si el plan B está en el `except`.

---

**Pregunta 4:** ¿Qué diferencia hay entre estos dos códigos?

```python
# Código A
resumen.to_csv("resultado.csv")

# Código B
resumen.to_csv("resultado.csv", index=False)
```

- A) Ninguna, son equivalentes
- B) El Código A incluye una columna extra de números (0, 1, 2...) en el archivo; el B no ✅
- C) El Código B no guarda el archivo
- D) `index=False` elimina la primera fila de datos

**Explicación:** Por defecto, pandas escribe el índice del DataFrame (0, 1, 2...) como primera columna. Esa columna no tiene significado en los datos. `index=False` la omite para producir un CSV limpio.

---

**Pregunta 5:** En el contexto del sector público, ¿cuál es la principal ventaja del patrón en vivo o caché?

- A) Hace el código más rápido porque siempre usa el archivo local
- B) Garantiza que el análisis pueda ejecutarse aunque el sistema externo esté caído por mantenimiento o falla ✅
- C) Evita tener que actualizar los datos
- D) Solo es útil cuando no tienes internet

**Explicación:** Los sistemas del Estado tienen mantenciones programadas, ventanas de no disponibilidad y caídas inesperadas. El patrón garantiza continuidad operacional: tu análisis siempre corre con los datos más recientes disponibles.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Función** | Bloque de código con nombre que recibe entradas y devuelve salidas | Procedimiento estándar documentado |
| **Parámetro** | Variable que recibe la función como entrada | Campo de un formulario |
| **`return`** | Instrucción que entrega el resultado de la función | La respuesta final de un oficio |
| **JSON** | Formato de texto para intercambiar datos entre sistemas | XML simplificado; idioma común de las APIs |
| **`json.loads()`** | Convierte texto JSON en diccionarios/listas Python | Importar datos de un sistema externo |
| **API** | Interfaz que permite a sistemas intercambiar datos automáticamente | Interoperabilidad entre servicios del Estado |
| **`try/except`** | Estructura para manejar errores sin detener el programa | Plan A y plan B documentados |
| **Patrón en vivo o caché** | Intenta fuente remota; si falla, usa copia local | Respaldo operacional ante caída de sistema |
| **`to_csv()`** | Guarda un DataFrame como archivo CSV | Exportar informe a formato compartible |
| **`groupby()`** | Agrupa filas por una columna y aplica una operación | Tabla dinámica de Excel |
| **`reset_index()`** | Convierte el índice de un DataFrame en columna normal | Desagrupar una tabla resumen |
| **`index=False`** | Parámetro de `to_csv` que omite la columna de índice | Guardar sin la columna de número de fila |

---

## 9. Conexión con el Módulo Siguiente

En R1-01 aprendiste a traer datos de cualquier fuente: archivos locales, URLs y APIs JSON. Tu código ahora es robusto ante fallos de red y guarda los resultados para reutilizarlos.

En **R1-02 · Exploración con pandas** entrarás de lleno al corazón del análisis de datos: cargar un dataset, inspeccionarlo, filtrar filas, seleccionar columnas y obtener los primeros estadísticos. Todo con pandas, la librería más usada en ciencia de datos.

> 💡 **Pregunta para reflexionar:** Ahora que sabes cargar datos desde una URL, ¿cuáles son los 3 datasets del Estado que más te servirían en tu trabajo y que están disponibles en datos.gob.cl?
