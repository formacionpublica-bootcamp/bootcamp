# Guía de Aprendizaje — R3-00 · Onramp express + Prueba de Nivel

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · Especialista en IA Aplicada · Módulo 0 · Semana 0–1

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-00 · Onramp express + Prueba de Nivel |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas (vía completa) · 30 minutos (solo Prueba de Nivel) |
| **Nivel** | Inicial — no requiere saber programar |
| **Prerrequisitos** | Ninguno. Una cuenta Google para usar Colab |
| **Competencia de salida** | Tener listo el prerequisito de Python y JSON para la rama: strings, listas, comprensiones, diccionarios, funciones, JSON y el patrón «en vivo o caché» |
| **Entregable** | Las 7 celdas de chequeo deben mostrar ✅ (o solo la del ejercicio 7, si vas por la vía b) |
| **Dataset** | `fichas.csv` — 245 fichas de trámites de ChileAtiende con su texto completo (18 temas, 64 instituciones). Profundización: `aire_diario.csv` + `estaciones.csv` (PM2,5 diario del SINCA, 14 estaciones, 2020-2025) |

### Doble vía de entrada a la rama R3

| Vía | ¿Para quién? | ¿Qué haces? |
|---|---|---|
| **(a) Cursar completo** | Nunca has programado, o tu Python está oxidado | Recorres los ejercicios 1 a 6 y cierras con la Prueba de Nivel (ejercicio 7). |
| **(b) Prueba de Nivel directa** | Ya manejas listas, funciones y diccionarios | Ejecutas la preparación y vas directo al **ejercicio 7**. Si lo resuelves **sin ayuda** y muestra ✅, saltas a **R3-01**. |

> Ninguna vía es «de segunda»: ambas te dejan en el mismo punto de partida. Si dudas, intenta la Prueba de Nivel; si te trabas, vuelve al ejercicio 1 sin culpa.

---

## 2. ¿Para qué me sirve esto como funcionario público?

La rama R3 te enseña a usar inteligencia artificial sobre **texto del Estado**: clasificar documentos, resumirlos en lenguaje claro, extraer requisitos y responder preguntas de la ciudadanía citando la fuente. El texto con que trabajaremos toda la rama son las **fichas de trámites de ChileAtiende**: 245 fichas reales — Bono de Invierno, Pensión Garantizada Universal, certificados, becas, subsidios — cada una con su texto completo (una ficha típica tiene unas 435 palabras; la más larga, *Asignación Familiar*, 1.915).

Pero toda esa IA se apoya en cuatro habilidades muy terrenales que este módulo instala:

1. **Leer texto con código:** partir una ficha en palabras y líneas, buscar si menciona al IPS o a FONASA.
2. **Recorrer colecciones:** contar cuántas fichas hay por tema o cuántas superan las 1.000 palabras, sin abrir 245 páginas.
3. **Escribir funciones:** empaquetar una regla («una ficha de 700 palabras o más es extensa») para aplicarla a todas.
4. **Hablar JSON:** el idioma de las APIs, incluida la del modelo de lenguaje que usarás desde R3-02.

Y el patrón **«en vivo o caché»**: intentar la llamada a un servicio y, si falla, usar un respaldo. En el Estado, donde las plataformas se caen justo cuando las necesitas, es la diferencia entre un informe que sale y uno que queda «esperando al sistema».

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en la oficina |
|----------|-----------|----------------------|
| **String (`str`)** | Guarda texto | El contenido de una celda de texto |
| **`.split()` / `.split("\n")`** | Parte el texto en palabras / en líneas | «Texto en columnas» |
| **`in`** | ¿Aparece esto dentro del texto? | `BUSCAR()` o Ctrl+F |
| **Lista** | Colección ordenada de valores | Una columna de la planilla |
| **Comprensión de lista** | Lista nueva filtrando otra, en una línea | Filtro + copiar el resultado a otra hoja |
| **Diccionario (`dict`)** | Pares clave → valor | Una ficha: tema → cantidad |
| **`.get(clave, 0)`** | Lee el valor o un 0 si no existe | `SI.ERROR(BUSCARV(...); 0)` |
| **Función (`def`)** | Empaqueta una regla reutilizable | Un instructivo: mismos pasos, cualquier caso |
| **JSON** | Texto con estructura de llaves y corchetes | El «oficio digital» con que responden las plataformas |
| **`json.dumps` / `json.loads`** | Python → JSON / JSON → Python | Ensobrar el oficio / abrir el sobre |
| **`try / except`** | Intenta algo y captura el error | El plan B del procedimiento |
| **En vivo o caché** | Llama al servicio; si falla, usa el respaldo | Trabajar con el último reporte descargado cuando el sistema está caído |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Abrir un notebook en Google Colab con mi cuenta | ☐ |
| Ejecutar una celda con ▶︎ o `Shift`+`Enter` | ☐ |
| Leer un mensaje ❌ con pista sin cerrar la pestaña (los errores son parte del método) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `fichas.csv` en `df` (245 filas × 7 columnas: `id`, `titulo`, `tema`, `institucion`, `url`, `n_palabras`, `texto`) y mirar una ficha concreta: el **Bono de Invierno** (id 39484, Instituto de Previsión Social, 765 palabras).

💡 **Concepto clave:** La primera celda ya usa el patrón «en vivo o caché»: si el archivo está en la carpeta lo usa; si no (Colab), lo descarga del repositorio.

⚠️ **Error frecuente:** Saltarse esta celda. `NameError: name 'df' is not defined` significa que no la ejecutaste.

---

### Sección 1 · Strings

🎯 **Objetivo:** Leer la ficha con código: título en mayúsculas, número de palabras, primera línea y si menciona al IPS.

💡 **Concepto clave:** `texto.split()` parte por espacios (palabras); `texto.split("\n")` parte por saltos de línea (líneas). `len(texto.split())` da **765**, exactamente lo que dice la columna `n_palabras`: así se calculó.

⚠️ **Error frecuente:** `len(texto)` cuenta **caracteres**, no palabras.

---

### Sección 2 · Listas y comprensiones

🎯 **Objetivo:** Sin pandas: cuántos títulos contienen «certificado» (**25**), cuántas fichas superan las 1.000 palabras (**11**) y el promedio de palabras por ficha (**471**).

💡 **Concepto clave:** `[t for t in titulos if "certificado" in t.lower()]` se lee «cada título t, si contiene certificado». El `.lower()` evita perder «Certificado» con mayúscula.

✅ **Señal de que entendiste:** Puedes explicar por qué el promedio (471) es mayor que la mediana (435): unas pocas fichas muy largas tiran el promedio hacia arriba.

---

### Sección 3 · Diccionarios

🎯 **Objetivo:** Contar las fichas por tema con un dict y encontrar el tema con más fichas.

💡 **Concepto clave:** `conteo[tema] = conteo.get(tema, 0) + 1` es el patrón universal de conteo. Resultado: **18 temas**; siete empatan en el máximo de 15 fichas, y `max` devuelve el primero que encontró (`emprendimiento-e-innovacion`). Un empate es un dato: «el tema con más fichas» no existe aquí.

---

### Sección 4 · Funciones

🎯 **Objetivo:** `extension(n_palabras)` → `"breve"` (< 300), `"media"` (< 700) o `"extensa"`.

💡 **Concepto clave:** El orden de los `if` importa: se pregunta primero por el umbral menor. Aplicada a todas: **125 medias, 77 breves, 43 extensas**.

⚠️ **Error frecuente:** `print("breve")` en vez de `return "breve"`: la función devolvería `None`.

---

### Sección 5 · JSON

🎯 **Objetivo:** Armar el `registro` de la ficha (id, título, institución, n° de palabras, dos primeras líneas), convertirlo a texto JSON y recuperarlo.

💡 **Concepto clave:** `json.dumps(registro, ensure_ascii=False, indent=2)` produce un texto legible con tildes; `json.loads` lo devuelve a dict idéntico al original.

⚠️ **Error frecuente:** `TypeError: Object of type int64 is not JSON serializable`. Lo que sale de pandas es `numpy.int64`; envuélvelo en `int(...)`.

---

### Sección 6 · En vivo o caché

🎯 **Objetivo:** `cargar_o_cache(url, respaldo)`: intenta bajar un JSON; si falla, devuelve el respaldo.

💡 **Concepto clave:** Es el mismo diseño de `preguntar_llm()` en R3-02: sin clave o sin red, el notebook no se cae, usa un respaldo.

---

### Sección 7 · Prueba de Nivel

🎯 **Objetivo:** Tres funciones de corte: `filtra_mayores`, `cuenta_palabras` y `conteo_por_clave` (que debe reproducir el conteo de fichas por institución: 64 instituciones).

✅ **Señal de que entendiste:** Lo resolviste sin mirar los ejercicios anteriores.

---

## 6. Guía de los 7 Ejercicios

### Ejercicio 1 — Explora el texto de la ficha

**Pistas progresivas:**
- 🟢 Pista suave: Cada variable es un método del string o el operador `in`.
- 🟡 Pista media: `.upper()`, `.split()`, `.split("\n")[0]`, `"IPS" in texto`.
- 🔴 Pista directa: `titulo_mayus = titulo.upper()`, `n_palabras = len(texto.split())`, `primera_linea = texto.split("\n")[0]`, `menciona_ips = "IPS" in texto`.

**¿Qué significa el ✅?** Que tu conteo de palabras coincide con la columna oficial `n_palabras` (765).

---

### Ejercicio 2 — Filtra y resume con listas

**Pistas progresivas:**
- 🟢 Pista suave: Una comprensión con `if` para filtrar; `len` para contar.
- 🟡 Pista media: `[t for t in titulos if "certificado" in t.lower()]`.
- 🔴 Pista directa: `n_extensas = len([p for p in palabras if p > 1000])` y `promedio = sum(palabras) / len(palabras)`.

**¿Qué significa el ✅?** Que tus resultados en Python puro coinciden con los de pandas: 25, 11 y 471,2.

---

### Ejercicio 3 — Cuenta las fichas por tema con un dict

**Pistas progresivas:**
- 🟢 Pista suave: Dentro del `for`, súmale 1 a lo que ya había para ese tema.
- 🟡 Pista media: `conteo.get(tema, 0)` devuelve 0 la primera vez.
- 🔴 Pista directa: `conteo[tema] = conteo.get(tema, 0) + 1` y `tema_top = max(conteo, key=conteo.get)`.

**¿Qué significa el ✅?** Que tu dict es idéntico a `df["tema"].value_counts()`.

---

### Ejercicio 4 — Escribe `extension`

**Pistas progresivas:**
- 🟢 Pista suave: Tres casos, tres `return`.
- 🟡 Pista media: `if ... < 300` / `elif ... < 700` / el resto.
- 🔴 Pista directa: `if n_palabras < 300: return "breve"`, `elif n_palabras < 700: return "media"`, `return "extensa"`.

**¿Qué significa el ✅?** Que también aciertas en los bordes: 300 es `"media"` y 700 es `"extensa"`.

---

### Ejercicio 5 — Arma el JSON de la ficha y recupéralo

**Pistas progresivas:**
- 🟢 Pista suave: Completa las dos claves que faltan y usa las dos funciones de `json`.
- 🟡 Pista media: `int(ficha["n_palabras"])`; `json.dumps(..., ensure_ascii=False, indent=2)`; `json.loads(...)`.
- 🔴 Pista directa: `"institucion": ficha["institucion"]`, `"n_palabras": int(ficha["n_palabras"])`, `texto_json = json.dumps(registro, ensure_ascii=False, indent=2)`, `recuperado = json.loads(texto_json)`.

**¿Qué significa el ✅?** Que el viaje Python → JSON → Python no perdió nada.

---

### Ejercicio 6 — Escribe `cargar_o_cache`

**Pistas progresivas:**
- 🟢 Pista suave: Solo falta qué hacer cuando la llamada falla.
- 🟡 Pista media: El `except` debe devolver algo.
- 🔴 Pista directa: `return respaldo`.

**¿Qué significa el ✅?** Que tu función nunca deja al notebook tirado.

---

### Ejercicio 7 — Prueba de Nivel

**Pistas progresivas:**
- 🟢 Pista suave: Son los ejercicios 2, 1 y 3 en forma de función.
- 🟡 Pista media: Comprensión con `if`; `len(texto.split())`; el patrón `.get(..., 0) + 1`.
- 🔴 Pista directa: `return [x for x in lista if x > umbral]`; `return len(texto.split())`; un `for r in registros:` que acumula `out[r[clave]] = out.get(r[clave], 0) + 1`.

**¿Qué significa el ✅?** Que estás listo para R3-01.

---

> 🔬 **En la profundización:** transferencia a otro dato real — la **calidad del aire** (PM2,5 diario de 14 estaciones del SINCA). Conviertes una tabla en lista de dicts, escribes una función `a_numero` que no se cae con datos sucios (ni con `NaN`), empaquetas el resumen de una estación como **respuesta tipo API** y lees un JSON anidado. Junio de 2024: Las Encinas (Temuco) promedió **29,6 µg/m³** con 6 días sobre 50; **Cerro Navia**, **49,2 µg/m³** con 15 días sobre 50 — la peor de las tres comparadas.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué devuelve `len(texto.split())`?

- A) El número de caracteres del texto
- B) El número de palabras del texto ✅
- C) El número de líneas del texto
- D) El texto en mayúsculas

**Explicación:** `.split()` parte por espacios y devuelve una lista de palabras; `len` la cuenta. Para líneas se usa `.split("\n")`.

---

**Pregunta 2:** ¿Qué hace `conteo.get(tema, 0)`?

- A) Borra el tema del diccionario
- B) Devuelve el valor guardado para `tema`, o 0 si todavía no existe ✅
- C) Agrega 0 a todos los temas
- D) Lanza un error si el tema no existe

**Explicación:** Es lo que permite contar sin preguntar antes «¿ya vi este tema?».

---

**Pregunta 3:** `json.dumps(registro)` falla con «Object of type int64 is not JSON serializable». ¿Qué haces?

- A) Borro el campo
- B) Envuelvo el número en `int(...)` al armar el dict ✅
- C) Cambio a `json.loads`
- D) Lo convierto a texto con comillas a mano

**Explicación:** pandas entrega tipos de numpy; JSON solo conoce los tipos nativos de Python.

---

**Pregunta 4:** ¿Para qué sirve el patrón «en vivo o caché»?

- A) Para que el código sea más rápido
- B) Para que el notebook siga funcionando aunque el servicio externo falle ✅
- C) Para guardar contraseñas
- D) Para evitar usar internet siempre

**Explicación:** Intenta lo real; si falla, usa el respaldo. En R3-02 lo usarás con el LLM.

---

**Pregunta 5:** Tu función `extension` devuelve `None` para todas las fichas. ¿La causa más probable?

- A) El dataset está vacío
- B) Usaste `print` en vez de `return` ✅
- C) Faltó importar pandas
- D) Las fichas no tienen palabras

**Explicación:** `print` muestra en pantalla, pero la función solo entrega lo que dice `return`; sin `return`, devuelve `None`.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **String** | Texto dentro de Python | El contenido de una ficha |
| **Lista** | Colección ordenada | Una columna de la planilla |
| **Comprensión de lista** | Lista filtrada/transformada en una línea | Filtro de Excel |
| **Diccionario** | Pares clave → valor | Una tabla de dos columnas: tema → cantidad |
| **Función** | Regla con nombre, reutilizable | Un instructivo interno |
| **JSON** | Formato de texto para datos estructurados | El oficio digital entre sistemas |
| **API** | Servicio que entrega datos a pedido | La ventanilla digital de una institución |
| **`try / except`** | Intenta; si falla, plan B | Procedimiento de contingencia |
| **Caché / respaldo** | Copia local que se usa si el servicio falla | El último reporte descargado |
| **`numpy.int64`** | Tipo numérico de pandas | Un número «con formato» que hay que limpiar antes de enviarlo |
| **PM2,5** | Material particulado fino (µg/m³), indicador de calidad del aire | El dato que gatilla una alerta ambiental |

---

## 9. Conexión con el Módulo Siguiente

En R3-00 aprendiste a manipular las fichas de ChileAtiende con Python: leerlas, contarlas, empaquetarlas como JSON y no depender de que el servicio responda.

En **R3-01 · Introducción al NLP** darás el primer paso de IA sobre esas mismas fichas: normalizar y tokenizar su texto, contar las palabras que importan, convertirlas en números con **TF-IDF** y entrenar un modelo que **adivina el tema de una ficha leyendo su texto** — y, lo más importante, aprenderás a leer sus errores.

> 💡 **Pregunta para reflexionar:** Contaste que 7 temas empatan con 15 fichas. Si un modelo tuviera que adivinar el tema de una ficha nueva, ¿qué pistas del texto usarías tú? ¿«pensión», «beca», «vivienda»…? Ese es exactamente el problema de R3-01.
