# 📘 Guía de Aprendizaje — R3-00 · Onramp express + Prueba de Nivel

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R3-00 · Onramp express + Prueba de Nivel |
| **Pista / Rama** | R3 — IA Aplicada (Especialista en IA aplicada) |
| **Duración estimada** | 2–3 horas (Semana 0–1) |
| **Nivel** | Inicial (cero conocimientos de programación) |
| **Prerrequisitos** | Ninguno. Solo una cuenta Google para usar Colab. |
| **Competencia de salida** | Tener listo el prerequisito de Python/datos para la rama de IA Aplicada: recorrer colecciones, escribir funciones, leer JSON y aplicar el patrón "en vivo o caché" con APIs. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de alimentos (ChileCompra): 7.412 órdenes con monto, categoría, tamaño de proveedor y región compradora. |
| **Entregable** | Las **5 celdas de chequeo** del `leccion.ipynb` muestran ✅. |

### 🚪 Doble vía de entrada a la rama R3

Este módulo es la **puerta de entrada** a IA Aplicada, y tiene dos caminos válidos:

| Vía | ¿Para quién? | ¿Qué haces? |
|---|---|---|
| **(a) Cursar completo** | Nunca has programado, o vienes con Python oxidado | Recorres las secciones 1 a 4 completando los `TODO`, y cierras con la Prueba de Nivel. |
| **(b) Prueba de Nivel directa** | Ya manejas Python básico (listas, funciones, diccionarios) | Vas directo al **Ejercicio 5 (Prueba de Nivel)**. Si lo resuelves **sin ayuda** y la celda de chequeo muestra ✅, saltas directo a **R3-01 · Introducción al NLP**. |

> 💡 No hay vía "de primera" ni "de segunda": ambas te dejan en el mismo punto de partida. Si dudas cuál tomar, intenta la Prueba de Nivel primero; si te trabas, vuelve a la sección 1 sin culpa.

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

La rama R3 te va a enseñar a usar **inteligencia artificial aplicada** en tu trabajo: clasificar reclamos ciudadanos, resumir oficios, extraer datos de textos, conversar con documentos. Pero toda esa magia se apoya en tres habilidades muy terrenales que este módulo instala:

1. **Recorrer colecciones de datos** (listas de montos, registros de compras) y resumirlas con unas pocas líneas.
2. **Escribir funciones** que empaquetan reglas del servicio: "si el monto es menor a $100.000 es compra menor; si supera $1.000.000, requiere otra revisión".
3. **Leer JSON**, que es el idioma en que hablan las APIs — incluidas las APIs de los modelos de lenguaje (LLM) que usarás desde R3-01 en adelante.

El dataset es real: **7.412 órdenes de compra de alimentos de ChileCompra** (frutas y verduras, panadería, lácteos, pescados y mariscos, entre 12 categorías), que suman más de **$807 millones** en gasto público. Cuando en el Ejercicio 1 cuentas cuántas órdenes superan el millón de pesos, no estás haciendo un ejercicio de juguete: estás respondiendo la misma pregunta que se hace un analista de abastecimiento un lunes en la mañana.

Además aprenderás el patrón **"en vivo o caché"**: intentar una llamada a una API y, si falla (sin red, servicio caído, límite de uso), usar una copia local. En el Estado, donde las plataformas a veces se caen justo cuando las necesitas, esta es la diferencia entre un informe que sale y uno que queda "esperando al sistema".

> 💡 **La clave:** este módulo no te convierte en programador/a; te da el vocabulario mínimo de Python para que en R3-01 puedas concentrarte en la IA y no en la sintaxis.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| Variable | Guarda un valor con un nombre (`total = ...`) | Una celda con nombre en Excel |
| Lista | Colección ordenada de valores | Una columna de montos en la planilla |
| Comprensión de lista | Crea una lista nueva filtrando/transformando otra | Filtro de Excel + pegar el resultado en otra hoja, en una sola línea |
| `sum()` / `len()` | Suma los elementos / cuenta cuántos hay | SUMA() y CONTARA() en Excel |
| Función (`def`) | Empaqueta una regla reutilizable con nombre | Un instructivo interno: mismos pasos, cualquier caso |
| `if / elif / else` | Decide entre alternativas según una condición | El flujograma de un procedimiento: "si el monto supera X, entonces..." |
| Diccionario (`dict`) | Pares clave → valor | Una ficha: RUT → nombre, región → gasto |
| JSON | Formato de texto para intercambiar datos estructurados | El "oficio digital" con que responden las plataformas del Estado |
| `json.loads()` | Convierte texto JSON en diccionarios y listas de Python | Abrir el sobre y leer el contenido del oficio |
| API | Servicio que entrega datos a pedido por internet | La ventanilla digital de Mercado Público o del SII |
| `try / except` | Intenta algo y captura el error si falla | Plan B del procedimiento: si la plataforma no responde, se usa el respaldo |
| Patrón "en vivo o caché" | Llama a la API; si falla, usa una copia local | Trabajar con el último reporte descargado cuando el sistema está caído |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

No necesitas saber programar. Solo verifica tu punto de partida:

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Abrir Google Colab (colab.research.google.com) con mi cuenta Google | ✅ | Si no tienes cuenta Google, créala primero |
| Ejecutar una celda en Colab con ▶︎ o Shift+Enter | ✅ | Practica 5 minutos con un notebook vacío |
| Entender qué es una tabla con filas y columnas | ✅ | Piensa en Excel: filas son registros, columnas son campos |
| Reconocer un archivo .csv | ✅ | Es una planilla separada por comas, como las descargas de ChileCompra |
| Ver un mensaje de error sin cerrar la pestaña | ✅ | Los ❌ de las celdas de chequeo traen pistas; son parte del método |

**¿Y si ya sé Python?** Si puedes escribir de memoria una comprensión de lista, una función con `if/elif/else` y recorrer una lista de diccionarios, salta directo a la **sección 5 del notebook (Prueba de Nivel)**. Si la celda de chequeo muestra ✅ sin que pidas ayuda, tu siguiente parada es R3-01.

> 🟢 Si marcaste todo ✅, adelante. Si algo dice 🔄, dedícale 10 minutos antes de seguir.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno (celda inicial)

**🎯 Objetivo:** Cargar las librerías y el dataset `compras_ml.csv`.

**💡 Concepto clave:** La primera celda ya usa el patrón estrella del módulo, **"en vivo o caché"**: si el archivo está en la carpeta local lo usa; si no (como en Colab), lo descarga del repositorio. Es como revisar primero el archivador de la oficina antes de pedir el documento a otra unidad.

**🔍 Qué hace el código:**
1. `import os, urllib.request`, `pandas` y `json`: trae las cajas de herramientas.
2. `if not os.path.exists(CSV)`: pregunta si el archivo ya existe en la carpeta.
3. `urllib.request.urlretrieve(...)`: si falta, lo descarga desde GitHub.
4. `pd.read_csv(CSV)` lo carga como tabla y `df.head()` muestra las primeras filas.

**⚠️ Error frecuente:** Saltarse esta celda. Si más abajo ves `NameError: name 'df' is not defined`, es porque no la ejecutaste primero.

**✅ Señal de comprensión:** Ves `Datos cargados: (7412, 6) filas x columnas` y una tabla con las columnas `cantidad`, `tamano_num`, `monto_total`, `categoria`, `tamano_proveedor` y `region_comprador`.

---

### 🔷 Sección 1 — Variables, listas y comprensiones

**🎯 Objetivo:** Resumir la lista de montos reales **sin pandas**: total gastado y cuántas órdenes superan $1.000.000.

**💡 Concepto clave:** En Python casi todo es **recorrer una colección**. Una **comprensión de lista** — `[m for m in montos if m > 1_000_000]` — se lee casi como castellano: "dame cada monto m de la lista, si m supera un millón". Es el filtro de Excel escrito en una línea.

**🔍 Qué hace el código:**
- `df["monto_total"].tolist()` convierte la columna de montos en una lista simple de Python.
- Tu tarea: calcular `total` (la suma de todos los montos) y `sobre_un_millon` (cuántos superan $1.000.000, usando una comprensión).
- El separador `1_000_000` es solo un truco de legibilidad: Python ignora los guiones bajos en números.

**⚠️ Error frecuente:** Confundir *la lista filtrada* con *cuántos elementos tiene*. La comprensión te da una lista de montos; para contarlos necesitas medir su largo. Otro clásico: escribir `1.000.000` con puntos — en Python eso no es un millón, es un error de sintaxis.

**✅ Señal de comprensión:** La celda de chequeo muestra ✅ y puedes decir en voz alta qué hace `[m for m in montos if m > 1_000_000]` sin mirar el notebook. (Spoiler verificado: son **159** órdenes sobre $1 millón, de un total que bordea los **$807,9 millones**.)

---

### 🔷 Sección 2 — Funciones: empaquetar una decisión

**🎯 Objetivo:** Escribir la función `clasificar(monto)` que devuelve `"bajo"`, `"medio"` o `"alto"` según el tramo.

**💡 Concepto clave:** Una **función** encapsula una regla para reutilizarla mil veces. En tu servicio ya existen: "toda compra bajo cierto umbral sigue el procedimiento simplificado". `def clasificar(monto):` convierte ese instructivo en código: se lo aplicas a $50.000 o a $2.000.000 y siempre responde con el mismo criterio.

**🔍 Qué hace el código:**
- `def clasificar(monto):` define la función con un parámetro de entrada.
- Dentro, un `if / elif / else` (o `return` final) decide: `"bajo"` si el monto es menor a 100.000; `"medio"` si es menor a 1.000.000; `"alto"` en cualquier otro caso.
- `return` entrega el resultado; sin `return`, la función devuelve `None` (nada).

**⚠️ Error frecuente:** Usar `print("bajo")` en vez de `return "bajo"`. Imprimir muestra el texto en pantalla, pero la función sigue devolviendo `None` y el chequeo falla. Otro: invertir el orden de las condiciones — si preguntas primero `monto < 1_000_000`, un monto de $50.000 quedará mal clasificado como "medio".

**✅ Señal de comprensión:** `clasificar(50_000)`, `clasificar(500_000)` y `clasificar(2_000_000)` imprimen `bajo medio alto`, y entiendes por qué el orden de los `if` importa.

---

### 🔷 Sección 3 — JSON: el idioma de las APIs

**🎯 Objetivo:** Convertir un texto JSON en estructuras de Python y sumar el `monto` de los ítems de una orden.

**💡 Concepto clave:** Cuando consultas una API — Mercado Público, el Banco Central, o el LLM de R3-01 — la respuesta llega como **JSON**: texto con estructura de llaves y corchetes. `json.loads()` lo traduce a diccionarios y listas de Python. Piensa en el JSON como un expediente digital: la orden tiene un número y adentro una lista de ítems, cada uno con nombre y monto.

**🔍 Qué hace el código:**
- `texto` es una respuesta típica: la orden `123` con dos ítems (pan por $500 y leche por $800).
- `json.loads(texto)` lo convierte en un diccionario: `data["orden"]` da el número, `data["items"]` da la lista de ítems.
- Tu tarea: recorrer `data["items"]` sumando el campo `"monto"` de cada uno. El resultado esperado es **1300**.

**⚠️ Error frecuente:** Confundir `json.loads()` (convierte un *string*) con `json.load()` (lee un *archivo o respuesta*). También, intentar `data["items"]["monto"]`: los ítems son una **lista**, hay que recorrerla elemento por elemento.

**✅ Señal de comprensión:** Puedes dibujar en un papel la estructura del JSON (dict → lista → dicts) y explicar por qué `monto_items` da 1300.

---

### 🔷 Sección 4 — En vivo o caché: APIs que no te dejan tirado

**🎯 Objetivo:** Completar la función `cargar_o_cache(url, fallback)` para que devuelva el respaldo cuando la API falla.

**💡 Concepto clave:** Una API real puede fallar: sin red, servicio caído, límite de uso. El patrón **en vivo o caché** dice: *intenta la llamada en vivo; si falla, usa la copia local*. Así tu notebook siempre corre. Es el equivalente a trabajar con el último reporte descargado cuando la plataforma institucional "está lenta".

**🔍 Qué hace el código:**
- `try:` intenta abrir la URL con `urllib.request.urlopen(url, timeout=2)` y leer el JSON.
- `except Exception:` captura **cualquier** falla (URL inválida, sin conexión, timeout).
- Tu tarea: en el `except`, devolver el `fallback` recibido como parámetro.
- La prueba usa una URL inventada (`http://no-existe.invalid/x.json`) justamente para forzar el camino de caché: `datos` debe terminar siendo `{"fuente": "cache", "n": 3}`.

**⚠️ Error frecuente:** Escribir `return "fallback"` (el texto) en vez de `return fallback` (la variable). O poner el `return` fuera del `except`, con la indentación incorrecta: en Python, la sangría define qué línea pertenece a qué bloque.

**✅ Señal de comprensión:** Puedes explicar por qué `datos["fuente"]` vale `"cache"` aunque la función *intentó* llamar a la API, y se te ocurre al menos un sistema de tu servicio donde aplicarías este patrón.

---

### 🔷 Sección 5 — Prueba de Nivel (PN): ¿puedes saltar directo a R3-01?

**🎯 Objetivo:** Resolver **sin ayuda** las tres tareas de corte que certifican el prerequisito de la rama.

**💡 Concepto clave:** La PN combina todo lo anterior en tres mini funciones. Si las resuelves de corrido, dominas Python + colecciones + funciones y estás listo/a para el NLP. Es el examen de conocimientos relevantes de la rama: no mide memoria, mide que puedas *construir* con las piezas.

**🔍 Qué pide cada tarea:**
1. `filtra_mayores(lista, umbral)` → los elementos de la lista mayores que el umbral. Con `[1, 5, 3, 8]` y umbral 4 debe dar `[5, 8]`.
2. `cuenta_palabras(texto)` → cuántas palabras tiene el texto. `"compras públicas del estado"` → 4.
3. `gasto_por_clave(registros)` → un diccionario `{region: suma de montos}` recorriendo una lista de registros. Dos compras de la región "A" ($100 y $50) → `{"A": 150}`.

**⚠️ Error frecuente:** En `gasto_por_clave`, intentar sumar sobre una clave que aún no existe en el diccionario (`KeyError`). El método `.get(clave, 0)` resuelve elegantemente el "primer registro de cada región".

**✅ Señal de comprensión:** La celda de chequeo del Ejercicio 5 muestra ✅ **sin que hayas mirado la solución ni pedido ayuda**. Ese es el corte de la vía (b): si lo lograste, estás habilitado/a para R3-01.

---

### 🔬 Extra opcional — `profundiza.ipynb`

Si terminaste la lección y te sobran 30 minutos, el `profundiza.ipynb` (Python puro, sin dependencias) afianza el prerequisito con tres ejercicios:

| Ejercicio | Tema | ¿Por qué importa para R3? |
|---|---|---|
| 1 — `por_region` | Diccionarios **por comprensión** | Agregar datos en dicts es pan de cada día al preparar insumos para un LLM |
| 2 — `a_numero` | Manejo de errores robusto (`try/except` que devuelve `None`) | Los textos reales vienen sucios: `"$mil"` no es un número |
| 3 — `normaliza` | **Normalización de texto** (minúsculas, espacios, separar palabras) | Es literalmente el primer paso del pipeline de NLP de R3-01 |

---

## 6. Guía de los Ejercicios

> Las pistas van de suave 🟢 a directa 🔴. Intenta cada nivel antes de pasar al siguiente. La solución en código **no** está aquí — está en `solucion.ipynb`, para después de intentarlo de verdad.

### ✍️ Ejercicio 1 — Resume la lista de montos

**Objetivo:** Calcular `total` y `sobre_un_millon` a partir de la lista `montos`.
**Habilidad que entrena:** Operar colecciones con funciones built-in y comprensiones.

- 🟢 **Pista suave:** Python trae funciones ya hechas para sumar una lista completa y para medir el largo de una lista. No necesitas escribir ningún ciclo `for` tradicional.
- 🟡 **Pista media:** Para `sobre_un_millon`, primero construye la lista de los montos que superan `1_000_000` con una comprensión con `if`; luego pregunta cuántos elementos tiene esa lista.
- 🔴 **Pista directa:** La estructura es `sum(montos)` para el total, y `len([... for ... in montos if ... > 1_000_000])` para el conteo. Completa los espacios.

**Lógica de la solución (en prosa):** sumar la lista completa con la función de suma; filtrar con una comprensión los montos sobre un millón y contar el resultado.
**Qué valida el chequeo ✅:** que `total` coincida con `df["monto_total"].sum()` (≈ $807,9 millones) y que `sobre_un_millon` sea exactamente el conteo de montos > $1.000.000 (159).

---

### ✍️ Ejercicio 2 — Escribe `clasificar`

**Objetivo:** Devolver `"bajo"`, `"medio"` o `"alto"` según el tramo del monto.
**Habilidad que entrena:** Funciones con lógica condicional.

- 🟢 **Pista suave:** Piensa en el flujograma: primera pregunta, ¿es menor que 100.000? Segunda, ¿es menor que 1.000.000? Si ninguna, es alto. El **orden** de las preguntas es la clave.
- 🟡 **Pista media:** Necesitas `if`, `elif` y un caso final. Cada rama debe **devolver** (no imprimir) el texto del tramo.
- 🔴 **Pista directa:** `if monto < 100_000: return "bajo"`, luego un `elif` contra `1_000_000`, y un `return "alto"` final. Cuida la indentación de 4 espacios.

**Lógica de la solución (en prosa):** comparar primero contra el umbral menor, luego contra el mayor, y dejar "alto" como caso residual.
**Qué valida el chequeo ✅:** `clasificar(50_000) == "bajo"`, `clasificar(500_000) == "medio"` y `clasificar(2_000_000) == "alto"`.

---

### ✍️ Ejercicio 3 — Parsea el JSON y suma los ítems

**Objetivo:** Calcular `monto_items` sumando el monto de cada ítem de la orden.
**Habilidad que entrena:** Navegar estructuras JSON (dict → lista → dict).

- 🟢 **Pista suave:** `data` ya es un diccionario. `data["items"]` es una lista donde cada elemento es a su vez un diccionario con las claves `"nombre"` y `"monto"`.
- 🟡 **Pista media:** Puedes recorrer la lista con una comprensión que extraiga `it["monto"]` de cada ítem, y sumar el resultado.
- 🔴 **Pista directa:** La forma compacta es pasar una expresión generadora directo a la suma: `sum(it["monto"] for it in data["items"])`. También sirve un `for` con acumulador.

**Lógica de la solución (en prosa):** recorrer la lista de ítems extrayendo el campo monto de cada uno y sumar todos los valores.
**Qué valida el chequeo ✅:** `data["orden"] == 123` y `monto_items == 1300` (pan $500 + leche $800).

---

### ✍️ Ejercicio 4 — Escribe `cargar_o_cache`

**Objetivo:** Que la función devuelva el `fallback` cuando la llamada a la URL falla.
**Habilidad que entrena:** Manejo de errores con `try/except` y el patrón en vivo o caché.

- 🟢 **Pista suave:** El `try` ya está escrito. Tu trabajo vive solo dentro del `except`: ¿qué debería entregar la función cuando todo lo demás falló?
- 🟡 **Pista media:** El respaldo llegó como **parámetro** de la función. Devuélvelo tal cual, sin comillas ni transformaciones.
- 🔴 **Pista directa:** Reemplaza los `...` del `except` por una sola línea que retorne el parámetro de respaldo, alineada con la misma indentación del bloque.

**Lógica de la solución (en prosa):** en la rama de error, retornar el objeto de respaldo recibido como argumento; la URL inválida del ejemplo garantiza que ese camino se ejecute.
**Qué valida el chequeo ✅:** que `datos["fuente"] == "cache"` (es decir, se usó el respaldo) y que `cargar_o_cache` sea efectivamente una función invocable.

---

### ✍️ Ejercicio 5 — Prueba de Nivel: las tres tareas de corte

**Objetivo:** Resolver `filtra_mayores`, `cuenta_palabras` y `gasto_por_clave` sin ayuda.
**Habilidad que entrena:** Integrar comprensiones, strings y diccionarios — el prerequisito completo de R3.

**`filtra_mayores(lista, umbral)`**
- 🟢 Es el Ejercicio 1 generalizado: en vez de un millón fijo, el umbral llega como parámetro.
- 🟡 Una comprensión de lista con condición `if` resuelve todo en una línea.
- 🔴 La estructura es `[x for x in lista if x > umbral]` — piensa qué va en cada espacio y por qué.

**`cuenta_palabras(texto)`**
- 🟢 ¿Cómo separarías "compras públicas del estado" en pedazos? Los strings de Python traen un método que corta por espacios.
- 🟡 `texto.split()` devuelve una **lista** de palabras. Contar elementos de una lista ya lo hiciste en el Ejercicio 1.
- 🔴 Encadena: separar el texto en palabras y medir el largo de la lista resultante. Una sola línea.

**`gasto_por_clave(registros)`**
- 🟢 Necesitas un diccionario que parte vacío y va acumulando: la primera vez que aparece una región, parte de cero; las siguientes, suma sobre lo acumulado.
- 🟡 El método `.get(clave, 0)` devuelve el valor acumulado si la clave existe, o 0 si es la primera vez. Es la pieza que evita el `KeyError`.
- 🔴 Recorre los registros con un `for`; en cada vuelta, `out[region] = out.get(region, 0) + monto`, sacando región y monto del registro actual.

**Lógica de la solución (en prosa):** filtrar con comprensión parametrizada; separar el texto por espacios y contar; acumular montos por clave en un diccionario usando el valor por defecto 0.
**Qué valida el chequeo ✅:** `filtra_mayores([1,5,3,8], 4) == [5,8]`, `cuenta_palabras("compras públicas del estado") == 4` y `gasto_por_clave(...) == {"A": 150}`. Si los tres pasan **sin ayuda**, apruebas la Prueba de Nivel.

---

## 7. Sección Especial: El Ejercicio de Política Pública

El corazón de política pública del módulo está en la dupla **Ejercicio 1 + Ejercicio 2**: contar órdenes sobre un umbral y clasificar el gasto en tramos. Con los datos reales del módulo, `clasificar` produce esta radiografía del gasto en alimentos:

| Tramo | Regla | Órdenes (verificado en `compras_ml.csv`) |
|---|---|---|
| Bajo | menos de $100.000 | 6.188 |
| Medio | entre $100.000 y $1.000.000 | 1.064 |
| Alto | $1.000.000 o más | 160 |

Es decir: el **83%** de las órdenes son compras chicas, pero las 160 órdenes del tramo alto concentran una parte desproporcionada de los $807,9 millones totales (la orden más grande llega a **$4.947.600**, casi 45 veces el monto promedio de ~$108.992).

### Reflexión guiada

- Los **umbrales importan**: en compras públicas chilenas, los tramos de monto determinan el procedimiento (compra ágil, licitación, trato directo). Una función `clasificar` mal ordenada — el error frecuente de la sección 2 — no es solo un bug: aplicada a un sistema real, enviaría compras al procedimiento equivocado.
- **Contar sobre un umbral es fiscalizar:** las 159 órdenes sobre $1 millón son exactamente el tipo de universo que una unidad de auditoría interna revisa primero.
- El patrón **en vivo o caché** también es política pública: un tablero de gasto que se cae cuando la API falla deja a la jefatura sin información justo cuando la pide.

### Pregunta de debate abierta

> Si tu servicio fijara umbrales de revisión automática de compras con una función como `clasificar`, ¿quién debería definir los cortes ($100.000, $1.000.000) y con qué evidencia? ¿Qué riesgo hay en que los proveedores conozcan el umbral exacto?

### Datos que complementarían el análisis

- **Fechas de las órdenes:** para detectar fraccionamiento (varias compras "bajo" el mismo día al mismo proveedor).
- **RUT del proveedor:** para medir concentración por tramo (¿las órdenes "alto" van siempre a los mismos?).
- **Precios de referencia por categoría:** para marcar órdenes con sobreprecio dentro de cada una de las 12 categorías de alimentos.
- **Región compradora vs. región del proveedor:** el dataset trae 15 regiones compradoras; cruzarlas con el origen del proveedor mostraría cuánto gasto queda en la economía local.

---

## 8. Autoevaluación Final

Responde sin mirar el notebook.

**Pregunta 1:** ¿Qué produce la comprensión `[m for m in montos if m > 1_000_000]`?

- a) La cantidad de montos que superan un millón
- b) Una lista nueva solo con los montos que superan un millón
- c) La suma de los montos que superan un millón
- d) Modifica la lista `montos`, eliminando los menores a un millón

✅ **Respuesta correcta: b)**
**Explicación:** Una comprensión con `if` construye una **lista nueva** filtrada; la original queda intacta. Para *contar* (opción a) habría que aplicar `len()` sobre el resultado, y para *sumar* (opción c), `sum()`.

---

**Pregunta 2:** En la función `clasificar`, ¿por qué importa preguntar primero `monto < 100_000` y después `monto < 1_000_000`?

- a) No importa; el resultado es el mismo en cualquier orden
- b) Porque Python exige ordenar las condiciones de menor a mayor
- c) Porque si se pregunta primero por el millón, un monto de $50.000 también cumple esa condición y quedaría mal clasificado como "medio"
- d) Porque `elif` solo acepta números mayores que el `if` anterior

✅ **Respuesta correcta: c)**
**Explicación:** Los `if/elif` se evalúan en orden y gana la **primera** condición verdadera. $50.000 es menor que un millón, así que si esa pregunta va primero, la función devuelve "medio" antes de llegar a la regla del tramo bajo. Python no impone ningún orden (b y d son inventadas); el orden es responsabilidad de quien diseña la regla.

---

**Pregunta 3:** ¿Qué hace `json.loads(texto)`?

- a) Descarga un JSON desde internet
- b) Convierte un string con formato JSON en diccionarios y listas de Python
- c) Valida que una API esté en línea
- d) Guarda un diccionario de Python como archivo .json

✅ **Respuesta correcta: b)**
**Explicación:** `json.loads()` (load **s**tring) traduce texto JSON a estructuras de Python. Descargar es tarea de `urllib`; guardar sería `json.dump()`. Es el paso obligado entre "la API respondió" y "puedo trabajar con los datos".

---

**Pregunta 4:** En el patrón "en vivo o caché", ¿qué papel cumple el bloque `except`?

- a) Reintenta la llamada a la API hasta que funcione
- b) Detiene el notebook y muestra el error completo
- c) Entrega los datos de respaldo cuando la llamada en vivo falla
- d) Borra la caché para forzar una descarga nueva

✅ **Respuesta correcta: c)**
**Explicación:** El `try` intenta la vía en vivo; si cualquier cosa falla (sin red, timeout, URL caída), el `except` toma el control y devuelve el `fallback`. El notebook nunca se cae: degrada con elegancia a la copia local. No hay reintentos ni borrado; eso serían patrones distintos.

---

**Pregunta 5:** En `gasto_por_clave`, ¿para qué sirve `out.get(region, 0)`?

- a) Para ordenar las regiones alfabéticamente
- b) Para obtener el acumulado de esa región, o 0 si es la primera vez que aparece
- c) Para eliminar las regiones con gasto cero
- d) Para validar que la región exista en el dataset oficial

✅ **Respuesta correcta: b)**
**Explicación:** `.get(clave, valor_por_defecto)` consulta el diccionario sin lanzar `KeyError`: si la región ya tiene acumulado, lo devuelve; si no, entrega 0 para partir la suma. Sin este método, el primer registro de cada región rompería el programa.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Variable** | Nombre que guarda un valor para reutilizarlo | Una celda con nombre definido en Excel |
| **Lista** | Colección ordenada de valores entre corchetes `[...]` | Una columna de la planilla |
| **Comprensión de lista** | Sintaxis compacta para filtrar/transformar una lista en una línea | Filtrar en Excel y pegar el resultado, en un solo paso |
| **Función (`def`)** | Bloque de código con nombre que recibe entradas y devuelve un resultado | Un instructivo del servicio: mismos pasos ante cualquier caso |
| **`return`** | Instrucción que entrega el resultado de una función | La resolución final del trámite (distinta de solo "comentarla" con `print`) |
| **`if / elif / else`** | Estructura que decide entre alternativas en orden | El flujograma de un procedimiento administrativo |
| **Diccionario (`dict`)** | Colección de pares clave → valor | Ficha de registro: RUT → nombre, región → gasto |
| **`.get(clave, 0)`** | Consulta un dict devolviendo un valor por defecto si la clave no existe | Buscar en el archivador y, si no hay carpeta, abrir una nueva en cero |
| **JSON** | Formato de texto estándar para intercambiar datos estructurados | El "oficio digital" con que responden las plataformas del Estado |
| **API** | Servicio que entrega datos a pedido a través de internet | La ventanilla digital de Mercado Público |
| **`try / except`** | Intenta ejecutar código y captura el error si algo falla | El plan B escrito en el procedimiento: si el sistema no responde, usar el respaldo |
| **En vivo o caché** | Patrón: intentar la fuente en vivo y, si falla, usar una copia local | Trabajar con el último reporte descargado cuando la plataforma está caída |
| **Prueba de Nivel (PN)** | Ejercicio de corte que certifica el prerequisito y habilita saltar a R3-01 | El examen de conocimientos relevantes de un concurso |

---

## 10. Conexión con el Módulo Siguiente

Has completado **R3-00 · Onramp express** — por la vía que sea. Ya recorres colecciones, escribes funciones, lees JSON y tus notebooks sobreviven a APIs caídas. Como dice el cierre de la lección: eso es el 80% de lo que usarás en toda la rama R3.

**El próximo módulo es R3-01 · Introducción al NLP.**

Ahí los datos dejan de ser solo números: pasan a ser **texto** — reclamos ciudadanos, glosas de compras, oficios. Vas a aprender a que el computador "entienda" lenguaje: normalizar, tokenizar y representar texto para analizarlo a escala. Y aparecerá el primer **LLM** del bootcamp (Gemini, detrás de la función `get_llm()`), consumido exactamente como practicaste aquí: una API que responde JSON, con su respaldo en caché por si falla.

Si hiciste el `profundiza.ipynb`, ya escribiste `normaliza()` — literalmente el primer paso del pipeline de NLP que viene.

> 🤔 **Pregunta motivadora:** Tu servicio recibe 5.000 reclamos ciudadanos al mes, escritos con mayúsculas, faltas de ortografía y modismos. Hoy tres personas los leen y clasifican a mano. Con lo que sabes ahora — funciones, JSON, APIs — ¿qué parte de ese trabajo crees que puede hacer una máquina, y qué parte debería seguir haciendo una persona? En R3-01 empezamos a responderlo con código.

**Antes de pasar:** asegúrate de que tus 5 celdas de chequeo muestren ✅. Nos vemos en el NLP. 🚀

---

*Formación Pública Chile · Licencia CC BY 4.0*
