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
| **Dataset** | `matricula.csv` — matrícula oficial 2025 de los 10.945 establecimientos educacionales de Chile (MINEDUC) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Antes de abrir el notebook, detente un momento a pensar por qué esto importa.

En el trabajo del Estado, lidiamos todos los días con datos: registros de beneficiarios, listados de establecimientos, dotaciones, coberturas de programas. Habitualmente esos datos viven en Excel y los procesamos manualmente, copiando y pegando, filtrando con el ratón, escribiendo fórmulas una por una.

Python hace exactamente lo mismo que Excel, pero de forma **automatizable, repetible y documentada**. Una vez que escribes el código para contar los estudiantes por región, puedes ejecutarlo en segundos con los datos del próximo año, sin tocar nada más.

Este primer módulo te enseña el **alfabeto de Python**: variables, listas, diccionarios y bucles. Son exactamente las cuatro operaciones que haces a mano en Excel, pero escritas en código. Con ellas ya puedes responder preguntas reales sobre el sistema escolar chileno con el dato oficial del MINEDUC.

---

## 3. Mapa Conceptual del Módulo

| Concepto Python | ¿Qué hace? | Equivalente en Excel/trabajo diario |
|-----------------|-----------|-------------------------------------|
| **Variable** | Guarda un valor con nombre | Una celda con nombre (`=SUMA(B2:B100)` guardada en `total`) |
| **Lista** | Agrupa muchos valores en orden | Una columna de datos |
| **Comprensión de lista** | Filtra una lista en una línea | Filtro de columna en Excel |
| **Diccionario** | Asocia clave → valor | Tabla de dos columnas: región → estudiantes acumulados |
| **Bucle `for`** | Repite una acción por cada elemento | Arrastrar una fórmula por toda la columna |
| **Condicional `if`** | Clasifica según una condición | `=SI(matricula<100,"chico","grande")` |

---

## 4. Antes de Partir — Checklist de Entrada

| ¿Puedes…? | ✔ |
|-----------|---|
| Abrir un notebook en Google Colab y ejecutar una celda con ▶︎ | ☐ |
| Leer un número y entender qué significa "matrícula total de un establecimiento" | ☐ |
| Distinguir entre un número (1000) y un texto ("Metropolitana") | ☐ |

Si alguna te falta, no te preocupes: la lección parte de cero. Esta lista es solo para que sepas dónde estás parado.

---

## 5. Recorrido de la Lección

### Celda de preparación

🎯 **Objetivo:** Cargar el dataset de matrícula escolar y confirmar que todo funciona.

💡 **Concepto clave:** Antes de analizar cualquier dato, hay que traerlo al entorno de trabajo. Esta celda descarga el archivo `matricula.csv` desde GitHub si no existe localmente, y lo carga como un DataFrame de pandas. Piénsalo como abrir el archivo Excel antes de trabajar con él. Cada fila es un establecimiento: su nombre, comuna, dependencia y cuántos estudiantes tiene matriculados en 2025.

✅ **Señal de que entendiste:** Ves una tabla con columnas como `mat_total`, `region` y `dependencia` al ejecutar la celda.

### Ejercicio 1 · Variables

🎯 **Objetivo:** Calcular el total nacional de estudiantes y el promedio por establecimiento usando solo Python puro, sin pandas.

💡 **Lectura del código:**
- `matriculas = df["mat_total"].tolist()` → extrae la columna de matrícula como una lista de Python
- `total = ...` → aquí debes escribir `sum(matriculas)`, que suma todos los elementos de la lista
- `promedio = ...` → aquí debes escribir `total / len(matriculas)`, que divide el total por la cantidad de establecimientos

⚠️ **Error frecuente:** Escribir `total = matriculas` en vez de `total = sum(matriculas)`. Recuerda: quieres el *resultado* de la suma, no la lista original.

✅ **Señal de que entendiste:** Puedes explicar la diferencia entre `matriculas` (la lista completa) y `total` (un único número: los ~3,5 millones de estudiantes del país).

### Ejercicio 2 · Comprensiones

🎯 **Objetivo:** Contar cuántos establecimientos tienen más de 1.000 estudiantes usando una comprensión de lista.

💡 **Concepto clave:** Una **comprensión de lista** es la forma elegante de Python para filtrar. La sintaxis es `[elemento for elemento in lista if condición]`. Es exactamente lo que hace el filtro de Excel, pero en una línea de código. En el trabajo público: útil para aislar establecimientos sobre cierta matrícula, o programas sobre cierto presupuesto.

- `grandes = [m for m in matriculas if m > 1_000]` → crea una nueva lista solo con las matrículas mayores a 1.000
- El número `1_000` con guion bajo es solo una forma de escribir 1000 más legible (Python lo acepta igual)

✅ **Señal de que entendiste:** Puedes cambiar el umbral a 2.000 y obtener un número menor de establecimientos.

### Ejercicio 3 · Diccionarios y bucles

🎯 **Objetivo:** Construir el total de estudiantes por región acumulando en un diccionario.

💡 **Concepto clave:** Un **diccionario** es como una tabla de dos columnas: una de claves (nombres de regiones) y una de valores (estudiantes acumulados). El **bucle `for`** recorre cada establecimiento y va sumando su matrícula al acumulado de la región correspondiente. Es lo que hace una tabla dinámica de Excel, pero construida manualmente para que veas cómo funciona por dentro.

- `est_region = {}` → crea un diccionario vacío (sin regiones todavía)
- `for region, m in zip(...)` → recorre ambas columnas al mismo tiempo, tomando un par (región, matrícula) por iteración
- `est_region.get(region, 0)` → busca el acumulado actual de esa región; si no existe aún, devuelve 0
- `est_region[region] = ... + m` → actualiza el acumulado sumando la matrícula nueva

⚠️ **Error frecuente:** Olvidar el `.get(region, 0)` y escribir directamente `est_region[region] + m`. Si la región aún no existe en el diccionario, Python lanza un `KeyError`. El `.get(..., 0)` evita ese error.

✅ **Señal de que entendiste:** El diccionario final tiene 16 claves (las 16 regiones de Chile) y la suma de todos los valores es igual al `total` calculado en el ejercicio 1.

### Ejercicio 4 · Condicionales

🎯 **Objetivo:** Clasificar cada establecimiento en "chico", "medio" o "grande" según su matrícula, y contar cuántos hay en cada tramo.

💡 **Lectura del código:**
- `for m in matriculas:` → recorre cada establecimiento uno por uno
- `if m < 100:` → si tiene menos de 100 estudiantes, es "chico" (piensa en escuelas rurales)
- `elif m < 500:` → si no, y tiene menos de 500, es "medio"
- `else:` → en cualquier otro caso, es "grande"

✅ **Señal de que entendiste:** La suma `tramos["chico"] + tramos["medio"] + tramos["grande"]` es igual a `len(matriculas)`. Ningún establecimiento se perdió ni se contó dos veces.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Total de estudiantes y promedio por establecimiento

**Objetivo:** Calcular cuántos estudiantes hay en Chile y el promedio por establecimiento.
**Habilidad que entrena:** Uso de variables y funciones básicas de Python (`sum`, `len`).

**Pistas progresivas:**
- 🟢 Pista suave: Python tiene una función incorporada que suma todos los elementos de una lista. También tiene una que cuenta cuántos elementos tiene una lista.
- 🟡 Pista media: El total es `sum(lista)`. El promedio es total dividido por la cantidad de elementos.
- 🔴 Pista directa: `total = sum(matriculas)` y `promedio = total / len(matriculas)`.

**Lógica de la solución:** La lista `matriculas` ya contiene todos los valores numéricos. `sum()` los recorre internamente y los acumula. Luego dividimos por `len(matriculas)` para obtener el tamaño típico de un establecimiento.

**¿Qué significa el ✅?** Que tu `total` y `promedio` coinciden exactamente con lo que calcularía pandas (`df["mat_total"].sum()` y `.mean()`). Si los números son iguales, tu lógica es correcta.

---

### Ejercicio 2 — Cuenta los establecimientos con más de 1.000 estudiantes

**Objetivo:** Filtrar los establecimientos que superan un umbral de matrícula y contarlos.
**Habilidad que entrena:** Comprensión de lista con condición (`if`).

**Pistas progresivas:**
- 🟢 Pista suave: Piensa en la comprensión de lista como una oración: "dame todas las matrículas de la lista, pero solo las que cumplen esta condición".
- 🟡 Pista media: La estructura es `[m for m in matriculas if m > umbral]`. Luego usas `len()` para contar.
- 🔴 Pista directa: `grandes = [m for m in matriculas if m > 1_000]` y `n_grandes = len(grandes)`.

**Lógica de la solución:** La comprensión de lista evalúa la condición para cada elemento y solo incluye en la nueva lista los que la cumplen. `len()` cuenta cuántos pasaron el filtro.

**¿Qué significa el ✅?** Que `n_grandes` coincide con `(df["mat_total"] > 1_000).sum()`. Es decir, tu filtro manual produce el mismo resultado que el filtro de pandas.

---

### Ejercicio 3 — Estudiantes por región con un bucle

**Objetivo:** Construir un resumen regional de la matrícula acumulando en un diccionario.
**Habilidad que entrena:** Diccionarios, bucles `for`, método `.get()`.

**Pistas progresivas:**
- 🟢 Pista suave: Necesitas un diccionario vacío donde la clave sea la región y el valor sean los estudiantes acumulados. Por cada establecimiento, sumas su matrícula al acumulado de esa región.
- 🟡 Pista media: Usa `est_region.get(region, 0)` para obtener el valor actual sin error cuando la región aparece por primera vez.
- 🔴 Pista directa: Dentro del bucle: `est_region[region] = est_region.get(region, 0) + m`.

**Lógica de la solución:** El `.get(region, 0)` es el truco clave: si la región ya está en el diccionario, devuelve su valor actual; si no existe todavía, devuelve 0. Luego sumamos la matrícula y guardamos el resultado.

**¿Qué significa el ✅?** Que el diccionario tiene tantas claves como regiones únicas (`nunique()`, 16 en Chile) y que la suma de todos los valores es igual al total nacional.

---

### Ejercicio 4 — Cuenta los establecimientos por tramo de tamaño

**Objetivo:** Clasificar cada establecimiento en chico/medio/grande y contar los de cada categoría.
**Habilidad que entrena:** Condicionales `if/elif/else`, actualización de diccionarios.

**Pistas progresivas:**
- 🟢 Pista suave: Tienes un diccionario con tres categorías ya definidas. Por cada matrícula, debes decidir a cuál categoría pertenece y sumar 1 a esa categoría.
- 🟡 Pista media: Usa `if m < 100` para "chico", `elif m < 500` para "medio", y `else` para "grande". Luego `tramos["chico"] += 1`.
- 🔴 Pista directa: En el `for`, tres ramas: `if m < 100: tramos["chico"] += 1`, `elif m < 500: tramos["medio"] += 1`, `else: tramos["grande"] += 1`.

**Lógica de la solución:** El `elif` es fundamental: garantiza que las condiciones se evalúan en orden y que cada establecimiento cae en exactamente un tramo. El gráfico de barras al final visualiza los resultados automáticamente.

**¿Qué significa el ✅?** Que la suma de los tres tramos es igual al total de establecimientos. Ninguno se perdió ni se contó dos veces.

---

## 7. Autoevaluación Final

Responde sin mirar el código. Si dudas, vuelve a la sección correspondiente.

**Pregunta 1:** ¿Cuál es la diferencia entre `matriculas` y `total`?

- A) Son lo mismo, solo tienen nombres distintos
- B) `matriculas` es una lista con todos los valores; `total` es un único número con su suma ✅
- C) `total` es más grande que `matriculas` porque tiene más datos
- D) `matriculas` solo tiene las matrículas altas

**Explicación:** Una variable puede contener cualquier tipo de dato: una lista entera, un número, un texto. `matriculas` guarda toda la columna; `total` guarda el resultado de sumarla.

---

**Pregunta 2:** ¿Qué devuelve `[m for m in matriculas if m > 2_000]`?

- A) El número de establecimientos con más de 2.000 estudiantes
- B) El total acumulado de esas matrículas
- C) Una lista con solo las matrículas que superan 2.000 ✅
- D) Un error, porque no se puede usar `if` dentro de una lista

**Explicación:** La comprensión de lista devuelve siempre una nueva lista. Si quieres el conteo, envuelves el resultado en `len(...)`.

---

**Pregunta 3:** ¿Por qué es importante usar `.get(region, 0)` en vez de `est_region[region]` directamente?

- A) Porque `.get()` es más rápido
- B) Porque si la región no existe aún, `est_region[region]` lanza un error; `.get()` devuelve 0 en ese caso ✅
- C) Porque `.get()` suma automáticamente la matrícula
- D) No hay diferencia, son equivalentes

**Explicación:** Intentar leer una clave inexistente en un diccionario Python produce un `KeyError`. `.get(clave, valor_por_defecto)` evita ese error devolviendo el valor por defecto cuando la clave no existe.

---

**Pregunta 4:** ¿Cuál es el error en este código?

```python
for m in matriculas:
    if m < 100:
        tramos["chico"] += 1
    if m < 500:
        tramos["medio"] += 1
    else:
        tramos["grande"] += 1
```

- A) No hay error, el código es correcto
- B) Falta el `elif`: una escuela de 80 estudiantes contaría como "chico" Y como "medio" al mismo tiempo ✅
- C) El problema es que `tramos` no está definido
- D) `+=` no funciona con diccionarios

**Explicación:** Con dos `if` independientes, una escuela de 80 estudiantes cumple ambas condiciones (`< 100` y `< 500`) y se cuenta dos veces. El `elif` garantiza exclusividad: si ya entró por el primer `if`, no evalúa el segundo.

---

**Pregunta 5:** Después de ejecutar el módulo completo, ¿qué estructura de datos usarías para saber cuántos estudiantes tiene la región del Maule?

- A) Una lista
- B) El diccionario `est_region`, consultando `est_region["Maule"]` ✅
- C) Una variable llamada `maule`
- D) El DataFrame `df` directamente

**Explicación:** El diccionario `est_region` fue diseñado exactamente para responder esa pregunta: clave = nombre de región, valor = estudiantes acumulados.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Variable** | Caja con nombre que guarda un valor | Celda de Excel con nombre definido |
| **Lista** | Colección ordenada de valores | Columna de una planilla |
| **Comprensión de lista** | Forma compacta de filtrar una lista | Filtro de columna en Excel |
| **Diccionario** | Colección de pares clave→valor | Tabla resumen: región → estudiantes |
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
