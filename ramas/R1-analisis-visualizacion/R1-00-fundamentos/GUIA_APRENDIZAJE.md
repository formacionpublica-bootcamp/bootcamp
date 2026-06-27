# Guía de Aprendizaje — R1-00 · Fundamentos: Python con datos reales

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 0 · Semana 1

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-00 · Fundamentos |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Inicial — no se requiere experiencia previa en Python |
| **Prerrequisitos** | Ninguno. Solo tener acceso a Google Colab. |
| **Competencia de salida** | Manipular datos públicos con Python puro (variables, listas, diccionarios, bucles y condicionales) desde cero, en Colab. |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `compras_ml.csv` — montos, regiones y categorías de compras públicas (ChileCompra) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Antes de abrir el notebook, detente un momento a pensar por qué esto importa.

En el trabajo del Estado, lidiamos todos los días con datos: listados de proveedores, montos de contratos, registros de beneficiarios, bases de licitaciones. Habitualmente esos datos viven en Excel y los procesamos manualmente, copiando y pegando, filtrando con el ratón, escribiendo fórmulas una por una.

Python hace exactamente lo mismo que Excel, pero de forma **automatizable, repetible y documentada**. Una vez que escribes el código para calcular el gasto total por región, puedes ejecutarlo en segundos con datos nuevos cada mes, sin tocar nada más.

Este primer módulo te enseña el **alfabeto de Python**: variables, listas, diccionarios y bucles. Son exactamente las cuatro operaciones que haces a mano en Excel, pero escritas en código. Con ellas ya puedes responder preguntas reales sobre compras públicas de ChileCompra.

---

## 3. Mapa Conceptual del Módulo

| Concepto Python | ¿Qué hace? | Equivalente en Excel/trabajo diario |
|-----------------|-----------|-------------------------------------|
| **Variable** | Guarda un valor con nombre | Una celda con nombre (`=SUMA(B2:B100)` guardada en `total`) |
| **Lista** | Agrupa muchos valores en orden | Una columna de datos |
| **Comprensión de lista** | Filtra la lista en una línea | Filtro de columna o `=SI(...)` masivo |
| **Diccionario** | Asocia clave → valor | Tabla de dos columnas: región → monto acumulado |
| **Bucle `for`** | Recorre cada fila y hace algo | Arrastrar una fórmula por toda la columna |
| **Condicional `if`** | Clasifica según una condición | `=SI(monto<100000,"bajo","alto")` |

---

## 4. Verificación de Prerrequisitos

Este módulo es el punto de partida: **no necesitas saber Python**. Antes de empezar, verifica que puedas hacer lo siguiente:

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Abrir Google Colab en el navegador (colab.research.google.com) | ☐ |
| Ejecutar una celda haciendo clic en ▶ o presionando Shift+Enter | ☐ |
| Leer un número y entender qué significa "monto total de una compra" | ☐ |
| Distinguir entre un número (1000) y un texto ("Región Metropolitana") | ☐ |

Si respondiste Sí a todas, estás listo. Si alguna respuesta es No, el README del módulo tiene un enlace a los pasos de instalación.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación del entorno (celda inicial)

🎯 **Objetivo:** Cargar el dataset de compras públicas y confirmar que todo funciona.

💡 **Concepto clave:** Antes de analizar cualquier dato, hay que traerlo al entorno de trabajo. Esta celda descarga el archivo `compras_ml.csv` desde GitHub si no existe localmente, y lo carga como un DataFrame de pandas. Piénsalo como abrir el archivo Excel antes de trabajar con él.

🔍 **Qué hace el código, línea por línea:**
- `import os, urllib.request` → trae herramientas del sistema para buscar archivos y descargarlos
- `import pandas as pd` → carga la librería de tablas de datos (la usaremos de apoyo)
- `if not os.path.exists(CSV)` → revisa si el archivo ya está en el disco; si no está, lo baja
- `df = pd.read_csv(CSV)` → lee el CSV y lo convierte en una tabla llamada `df`
- `df.head()` → muestra las primeras 5 filas para confirmar que los datos cargaron bien

⚠️ **Error frecuente:** Si ves `FileNotFoundError`, significa que el archivo no se descargó. Verifica tu conexión a internet y ejecuta la celda de nuevo.

✅ **Señal de que entendiste:** Ves una tabla con columnas como `monto_total` y `region_comprador` al ejecutar la celda.

---

### Sección 1 · Variables: guardar para reutilizar

🎯 **Objetivo:** Calcular el total y el promedio de los montos de compras usando solo Python puro, sin pandas.

💡 **Concepto clave:** Una **variable** es una caja con nombre donde guardas un valor. En vez de escribir `3.141592` cada vez que necesitas pi, guardas `pi = 3.141592` y usas el nombre. En el contexto del Estado: en vez de recalcular el gasto total cada vez, lo calculas una vez y lo guardas en `total`.

🔍 **Qué hace el código:**
- `montos = df["monto_total"].tolist()` → extrae la columna de montos como una lista de Python
- `total = ...` → aquí debes escribir `sum(montos)`, que suma todos los elementos de la lista
- `promedio = ...` → aquí debes escribir `total / len(montos)`, que divide el total por la cantidad de compras
- `round(total)` → redondea el resultado para que sea más legible

⚠️ **Error frecuente:** Escribir `total = montos` en vez de `total = sum(montos)`. Recuerda: quieres el *resultado* de la suma, no la lista original.

✅ **Señal de que entendiste:** Puedes explicar la diferencia entre `montos` (la lista completa) y `total` (un único número).

---

### Sección 2 · Listas y comprensiones: filtrar

🎯 **Objetivo:** Contar cuántas compras superan los $500.000 usando una comprensión de lista.

💡 **Concepto clave:** Una **comprensión de lista** es la forma elegante de Python para filtrar. La sintaxis es `[elemento for elemento in lista if condición]`. Es exactamente lo que hace el filtro de Excel, pero en una línea de código. En el trabajo público: útil para aislar contratos sobre cierto monto, o proveedores de determinada región.

🔍 **Qué hace el código:**
- `caros = [m for m in montos if m > 500_000]` → crea una nueva lista solo con los montos mayores a 500.000
- `n_caros = len(caros)` → cuenta cuántos hay
- El número `500_000` con guion bajo es solo una forma de escribir 500000 más legible (Python lo acepta igual)

⚠️ **Error frecuente:** Confundir `caros` (la lista filtrada) con `n_caros` (el conteo). La celda de chequeo pide `n_caros`, no `caros`.

✅ **Señal de que entendiste:** Puedes cambiar el umbral a 1.000.000 y obtener un número menor de compras.

---

### Sección 3 · Diccionarios y bucles: acumular por clave

🎯 **Objetivo:** Construir un resumen de gasto total por región usando un diccionario y un bucle `for`.

💡 **Concepto clave:** Un **diccionario** es como una tabla de dos columnas: una de claves (nombres de regiones) y una de valores (gasto acumulado). El **bucle `for`** recorre cada fila del dataset y va sumando el monto al acumulado de la región correspondiente. Es lo que hace una tabla dinámica de Excel, pero construida manualmente para que veas cómo funciona por dentro.

🔍 **Qué hace el código:**
- `gasto_region = {}` → crea un diccionario vacío (sin regiones todavía)
- `for region, monto in zip(...)` → recorre ambas columnas al mismo tiempo, tomando un par (región, monto) por iteración
- `gasto_region.get(region, 0)` → busca el acumulado actual de esa región; si no existe aún, devuelve 0
- `gasto_region[region] = ... + monto` → actualiza el acumulado sumando el monto nuevo

⚠️ **Error frecuente:** Olvidar el `.get(region, 0)` y escribir directamente `gasto_region[region] + monto`. Si la región aún no existe en el diccionario, Python lanza un `KeyError`. El `.get(..., 0)` evita ese error.

✅ **Señal de que entendiste:** El diccionario final tiene tantas claves como regiones únicas hay en el dataset, y la suma de todos los valores es igual al `total` calculado en el ejercicio 1.

---

### Sección 4 · Condicionales: clasificar en tramos

🎯 **Objetivo:** Clasificar cada compra en "bajo", "medio" o "alto" según su monto, y contar cuántas hay en cada tramo.

💡 **Concepto clave:** Un **condicional `if/elif/else`** toma una decisión basada en una condición. Es el equivalente de la función `=SI()` de Excel, pero más legible cuando hay más de dos opciones. En el sector público se usa todo el tiempo: clasificar licitaciones por tipo, tramos de asignación de recursos, categorías de gasto.

🔍 **Qué hace el código:**
- `tramos = {"bajo": 0, "medio": 0, "alto": 0}` → inicializa el contador en cero para cada tramo
- `for m in montos:` → recorre cada monto uno por uno
- `if m < 100_000:` → si el monto es menor a $100.000, es "bajo"
- `elif m < 1_000_000:` → si no era bajo pero es menor a $1.000.000, es "medio"
- `else:` → todo lo demás es "alto"
- `tramos["bajo"] += 1` → suma 1 al contador del tramo correspondiente

⚠️ **Error frecuente:** Usar `if` en vez de `elif` para la segunda condición. Si usas dos `if` independientes, una compra de $200.000 contaría como "bajo" Y como "medio" al mismo tiempo.

✅ **Señal de que entendiste:** La suma `tramos["bajo"] + tramos["medio"] + tramos["alto"]` es igual a `len(montos)`. Ninguna compra se perdió ni se contó dos veces.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Total y promedio de los montos

**Objetivo:** Calcular el gasto total y promedio de las compras públicas del dataset.
**Habilidad que entrena:** Uso de variables y funciones básicas de Python (`sum`, `len`).

**Pistas progresivas:**
- 🟢 Pista suave: Python tiene una función incorporada que suma todos los elementos de una lista. También tiene una que cuenta cuántos elementos tiene una lista.
- 🟡 Pista media: El total es `sum(lista)`. El promedio es total dividido por la cantidad de elementos.
- 🔴 Pista directa: `total = sum(montos)` y `promedio = total / len(montos)`.

**Lógica de la solución:** La lista `montos` ya contiene todos los valores numéricos. `sum()` los recorre internamente y los acumula. Luego dividimos por `len(montos)` para obtener el valor representativo por compra.

**¿Qué significa el ✅?** Que tu `total` y `promedio` coinciden exactamente con lo que calcularía pandas (`df["monto_total"].sum()` y `.mean()`). Si los números son iguales, tu lógica es correcta.

---

### Ejercicio 2 — Cuenta los montos sobre $500.000

**Objetivo:** Filtrar las compras que superan un umbral y contarlas.
**Habilidad que entrena:** Comprensión de lista con condición (`if`).

**Pistas progresivas:**
- 🟢 Pista suave: Piensa en la comprensión de lista como una oración: "dame todos los montos de la lista, pero solo los que cumplen esta condición".
- 🟡 Pista media: La estructura es `[m for m in montos if m > umbral]`. Luego usas `len()` para contar.
- 🔴 Pista directa: `caros = [m for m in montos if m > 500_000]` y `n_caros = len(caros)`.

**Lógica de la solución:** La comprensión de lista evalúa la condición para cada elemento y solo incluye en la nueva lista los que la cumplen. `len()` cuenta cuántos pasaron el filtro.

**¿Qué significa el ✅?** Que `n_caros` coincide con `(df["monto_total"] > 500_000).sum()`. Es decir, tu filtro manual produce el mismo resultado que el filtro de pandas.

---

### Ejercicio 3 — Gasto total por región con un bucle

**Objetivo:** Construir un resumen regional del gasto acumulando en un diccionario.
**Habilidad que entrena:** Diccionarios, bucles `for`, método `.get()`.

**Pistas progresivas:**
- 🟢 Pista suave: Necesitas un diccionario vacío donde la clave sea la región y el valor sea el gasto acumulado. Por cada fila, sumas el monto al acumulado de esa región.
- 🟡 Pista media: Usa `gasto_region.get(region, 0)` para obtener el valor actual sin error cuando la región aparece por primera vez.
- 🔴 Pista directa: Dentro del bucle: `gasto_region[region] = gasto_region.get(region, 0) + monto`.

**Lógica de la solución:** El `.get(region, 0)` es el truco clave: si la región ya está en el diccionario, devuelve su valor actual; si no existe todavía, devuelve 0. Luego sumamos el monto y guardamos el resultado.

**¿Qué significa el ✅?** Que el diccionario tiene tantas claves como regiones únicas (`nunique()`) y que la suma de todos los valores es igual al total nacional.

---

### Ejercicio 4 — Cuenta las compras por tramo de monto

**Objetivo:** Clasificar cada compra en bajo/medio/alto y contar las de cada categoría.
**Habilidad que entrena:** Condicionales `if/elif/else`, actualización de diccionarios.

**Pistas progresivas:**
- 🟢 Pista suave: Tienes un diccionario con tres categorías ya definidas. Por cada monto, debes decidir a cuál categoría pertenece y sumar 1 a esa categoría.
- 🟡 Pista media: Usa `if m < 100_000` para "bajo", `elif m < 1_000_000` para "medio", y `else` para "alto". Luego `tramos["bajo"] += 1`.
- 🔴 Pista directa: En el `for`, tres ramas: `if m < 100_000: tramos["bajo"] += 1`, `elif m < 1_000_000: tramos["medio"] += 1`, `else: tramos["alto"] += 1`.

**Lógica de la solución:** El `elif` es fundamental: garantiza que las condiciones se evalúan en orden y que cada monto cae en exactamente un tramo. El gráfico de barras al final visualiza los resultados automáticamente.

**¿Qué significa el ✅?** Que la suma de los tres tramos es igual al total de montos. Ninguna compra se perdió ni se contó dos veces.

---

## 7. Autoevaluación Final

Responde sin mirar el código. Si dudas, vuelve a la sección correspondiente.

**Pregunta 1:** ¿Cuál es la diferencia entre `montos` y `total`?

- A) Son lo mismo, solo tienen nombres distintos
- B) `montos` es una lista con todos los valores; `total` es un único número con su suma ✅
- C) `total` es más grande que `montos` porque tiene más datos
- D) `montos` solo tiene los montos altos

**Explicación:** Una variable puede contener cualquier tipo de dato: una lista entera, un número, un texto. `montos` guarda toda la columna; `total` guarda el resultado de sumarla.

---

**Pregunta 2:** ¿Qué devuelve `[m for m in montos if m > 1_000_000]`?

- A) El número de montos mayores a un millón
- B) El total acumulado de esos montos
- C) Una lista con solo los montos que superan un millón ✅
- D) Un error, porque no se puede usar `if` dentro de una lista

**Explicación:** La comprensión de lista devuelve siempre una nueva lista. Si quieres el conteo, envuelves el resultado en `len(...)`.

---

**Pregunta 3:** ¿Por qué es importante usar `.get(region, 0)` en vez de `gasto_region[region]` directamente?

- A) Porque `.get()` es más rápido
- B) Porque si la región no existe aún, `gasto_region[region]` lanza un error; `.get()` devuelve 0 en ese caso ✅
- C) Porque `.get()` suma automáticamente el monto
- D) No hay diferencia, son equivalentes

**Explicación:** Intentar leer una clave inexistente en un diccionario Python produce un `KeyError`. `.get(clave, valor_por_defecto)` evita ese error devolviendo el valor por defecto cuando la clave no existe.

---

**Pregunta 4:** ¿Cuál es el error en este código?

```python
for m in montos:
    if m < 100_000:
        tramos["bajo"] += 1
    if m < 1_000_000:
        tramos["medio"] += 1
    else:
        tramos["alto"] += 1
```

- A) No hay error, el código es correcto
- B) Falta el `elif`: una compra de $50.000 contaría como "bajo" Y como "medio" al mismo tiempo ✅
- C) El problema es que `tramos` no está definido
- D) `+=` no funciona con diccionarios

**Explicación:** Con dos `if` independientes, una compra de $50.000 cumple ambas condiciones (`< 100.000` y `< 1.000.000`) y se cuenta dos veces. El `elif` garantiza exclusividad: si ya entró por el primer `if`, no evalúa el segundo.

---

**Pregunta 5:** Después de ejecutar el módulo completo, ¿qué estructura de datos usarías para saber cuánto gastó la Región del Maule en compras públicas?

- A) Una lista
- B) El diccionario `gasto_region`, consultando `gasto_region["Región del Maule"]` ✅
- C) Una variable llamada `maule`
- D) El DataFrame `df` directamente

**Explicación:** El diccionario `gasto_region` fue diseñado exactamente para responder esa pregunta: clave = nombre de región, valor = gasto acumulado.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Variable** | Caja con nombre que guarda un valor | Celda de Excel con nombre definido |
| **Lista** | Colección ordenada de valores | Columna de una planilla |
| **Comprensión de lista** | Forma compacta de filtrar una lista | Filtro de columna en Excel |
| **Diccionario** | Colección de pares clave→valor | Tabla resumen: región → monto |
| **Bucle `for`** | Instrucción que repite una acción por cada elemento | Arrastrar fórmula por toda la columna |
| **Condicional `if/elif/else`** | Decisión según una condición | Función `=SI()` de Excel |
| **`sum()`** | Función que suma todos los elementos de una lista | `=SUMA()` |
| **`len()`** | Función que cuenta los elementos de una lista | `=CONTAR()` |
| **`.get(clave, 0)`** | Busca en un diccionario; si no existe, devuelve 0 | `=SIERROR(BUSCARV(...), 0)` |
| **`assert`** | Verifica que una condición sea verdadera; si no, lanza un error | Validación de datos en formulario |
| **`zip()`** | Combina dos listas recorriéndolas en paralelo | Trabajar con dos columnas a la vez |
| **DataFrame** | Tabla de datos de pandas (se verá en detalle en R1-02) | Toda la hoja de cálculo |

---

## 9. Conexión con el Módulo Siguiente

En R1-00 aprendiste a manipular datos con Python puro: variables, listas, diccionarios y bucles. Construiste todo "a mano" para entender cómo funciona por dentro.

En **R1-01 · Traer el dato** aprenderás a traer datos desde distintas fuentes: archivos CSV locales, URLs directas y APIs públicas. Ya no dependerás de que el archivo esté descargado previamente: podrás apuntar tu código a cualquier fuente de datos del Estado y traer la información en segundos.

> 💡 **Pregunta para reflexionar antes del próximo módulo:** ¿Cuántas fuentes de datos diferentes usas en tu trabajo hoy? ¿Cuántas de ellas tienen una URL pública o un archivo descargable? ¿Qué pasaría si pudieras actualizar tu análisis con un solo clic?
