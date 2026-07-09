# 📘 Guía de Aprendizaje — R3-03 · RAG (Retrieval-Augmented Generation)

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R3-03 · RAG (Retrieval-Augmented Generation) |
| **Pista / Rama** | R3 — IA Aplicada (bloque avanzado, opcional) |
| **Duración estimada** | 2–3 horas |
| **Semana** | Semana 20 |
| **Nivel** | Avanzado |
| **Prerrequisitos** | R3-01 (Introducción al NLP, para la recuperación) y R3-02 (IA generativa y LLMs, para la generación) |
| **Competencia de salida** | Construir un sistema de preguntas y respuestas sobre documentos reales del Estado, con respuestas fundamentadas en la fuente y que se abstiene honestamente cuando no sabe |
| **Dataset** | `licitacion.csv` — 8 fragmentos reales de la Ficha de Licitación **2239-8-LR25** (Convenio Marco de productos de aseo e higiene), fuente: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico) |
| **LLM** | Google Gemini (`gemini-2.5-flash`), con el patrón **"en vivo o caché"**: funciona con o sin API key |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En R3-02 viste el gran poder de un LLM... y también su gran problema: **solo sabe lo que vio en su entrenamiento**, y cuando no sabe, **inventa con seguridad**. Pregúntale por el detalle de *tu* licitación, *tu* norma interna o *tu* ficha de compra, y no tiene cómo saberlo. Para el Estado, una respuesta inventada sobre una garantía o un plazo no es un error menor: puede significar una oferta rechazada, un reclamo o un sumario.

**RAG** (Generación Aumentada por Recuperación) es la técnica que resuelve esto, y hoy es la forma más usada de poner LLMs a trabajar con información propia. La idea es elegante: en vez de confiar en la memoria del modelo, **primero buscamos los documentos relevantes** y luego se los **entregamos al modelo** para que responda **basándose en ellos, citando la fuente**.

Piensa en las preguntas que llegan todos los días a una unidad de compras:

- *"¿Cuánto pondera el precio en la evaluación de esta licitación?"* → Está en la ficha: **75%**.
- *"¿De cuánto es la garantía de fiel cumplimiento y cómo se entrega?"* → Está en la ficha: **$400.000**, electrónica (Ley 19.799) o física en Oficina de Partes, dentro de **20 días hábiles** desde la notificación de la adjudicación.
- *"¿Cuál es la capital de Francia?"* → **No está en la ficha**, y un asistente serio debe decir "no lo sé" en vez de responder desde su memoria.

Con la receta de este módulo, cualquier conjunto de documentos propios —un reglamento interno, bases tipo, las preguntas frecuentes de tu unidad— puede convertirse en un asistente de preguntas y respuestas. Y como el asistente **cita la fuente** (el pasaje exacto de la ficha), la respuesta **siempre se puede verificar**. Eso es lo que separa una herramienta útil de un riesgo institucional.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **RAG** | Recuperar documentos relevantes → aumentar el prompt → generar la respuesta | Pedirle el informe al colega que **primero busca en el archivador correcto** y responde con la carpeta a la vista, citando el folio |
| **LLM a libro cerrado** | Responde solo desde su memoria de entrenamiento | Contestar un oficio "de memoria", sin revisar el expediente: si no te acuerdas, inventas |
| **RAG = libro abierto** | El modelo responde con la página correcta enfrente | Rendir el examen del reglamento de compras con el reglamento sobre la mesa |
| **Base de conocimiento (KB)** | Colección de pasajes con `id`, `fuente` y `texto` | El archivador de tu unidad: cada documento foliado y con su origen identificado |
| **Indexar** | Precalcular el conjunto de palabras útiles de cada pasaje | Hacer el índice temático del archivador antes de que lleguen las consultas |
| **Recuperar (retrieve)** | Encontrar los k pasajes que más palabras comparten con la pregunta | El funcionario de partes que ubica los expedientes que calzan con la consulta |
| **Aumentar (augment)** | Armar un prompt con los pasajes + la pregunta + "responde SOLO con esto" | Adjuntar al memo los antecedentes y la instrucción: "responda en base a lo adjunto" |
| **Generar (generate)** | El LLM redacta la respuesta a partir del contexto entregado | El redactor del oficio de respuesta, que escribe bien pero solo con los antecedentes que le pasaron |
| **Fundamentar (grounding)** | Anclar la respuesta a los documentos, no a la imaginación del modelo | Todo lo afirmado en el informe tiene su respaldo en el expediente |
| **Abstenerse** | Decir "no lo sé" cuando la respuesta no está en los documentos | Responder "no consta en los antecedentes disponibles" en vez de aventurar una cifra |
| **Embeddings** (mención) | Vectores que capturan el significado del texto; el "siguiente nivel" de la recuperación | Un archivador que agrupa por tema aunque los documentos usen palabras distintas |
| **"En vivo o caché"** | Con API key llama a Gemini; sin ella usa respuestas guardadas | Plan A con el servicio en línea, plan B con el respaldo impreso: el trámite avanza igual |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Este módulo **reutiliza piezas de los dos anteriores**: la tokenización de R3-01 para recuperar, y la conexión al LLM de R3-02 para generar. Responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Explicar qué hace `tokenizar`: normalizar el texto y quedarse con las palabras útiles (sin tildes ni stopwords) | ✅ Sí / 🔄 Revisar R3-01 |
| Usar conjuntos (`set`) en Python y calcular su intersección con `&` | ✅ Sí / 🔄 Revisar R3-01 |
| Explicar qué es un prompt y por qué su redacción cambia la respuesta del LLM | ✅ Sí / 🔄 Revisar R3-02 |
| Explicar qué es una alucinación de un LLM y por qué es peligrosa en el Estado | ✅ Sí / 🔄 Revisar R3-02 |
| Configurar (opcionalmente) mi `GEMINI_API_KEY` en los Secrets de Colab | ✅ Sí / 🔄 Revisar R3-02 |
| Escribir funciones en Python que reciben argumentos y devuelven valores | ✅ Sí / 🔄 Revisar R1 |

Si tienes más de dos "Revisar", dedica 20 minutos a repasar esos módulos antes de continuar. **La API key no es requisito:** sin ella el notebook funciona en modo caché y los 4 ejercicios se completan igual.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección: Tabla de Datos Reales

🎯 **Objetivo:** conocer la base de conocimiento con la que trabajarás: 8 fragmentos reales de la Ficha de Licitación **2239-8-LR25**.

💡 **Concepto clave — documentos reales, no de juguete:**
La KB es una tabla con 3 columnas (`id`, `fuente`, `texto`) y 8 pasajes (p1 a p8) de un Convenio Marco de productos de aseo e higiene de ChileCompra. Entre otros: es una licitación tipo LR (igual o superior a 5.000 UTM), el contrato dura 36 meses, la evaluación pondera precio 75% / experiencia 20% / programa de integridad 3% / requisitos formales 2%, no exige garantía de seriedad de la oferta, y la garantía de fiel cumplimiento es de $400.000. Tu RAG responderá **sobre esto**, no sobre trivia de internet.

🔍 **Qué hace:** es una celda de texto: presenta los 8 pasajes en una tabla para que sepas qué "sabe" tu sistema antes de construirlo.

⚠️ **Error frecuente:** saltarse esta tabla. Después, cuando el chequeo diga "el mejor pasaje es p6", no sabrás de qué habla. Léela: son 8 filas.

✅ **Señal de comprensión:** puedes decir sin mirar qué pasaje contiene los criterios de evaluación (p4) y cuál la garantía de fiel cumplimiento (p6).

---

### 🔷 Sección 1: La idea de RAG — examen con libro abierto

🎯 **Objetivo:** entender el problema que RAG resuelve y sus tres piezas: **recuperar → aumentar → generar**.

💡 **Concepto clave — libro cerrado vs. libro abierto:**
Un LLM solo es un examen **a libro cerrado**: responde de memoria y, si no se acuerda, inventa. RAG es el examen **a libro abierto**: primero buscas la página correcta, la lees, y respondes con eso a la vista. RAG no hace al modelo "más inteligente": **le pone la página correcta enfrente**. En términos de oficina: no le preguntas al colega memorión, le preguntas al colega metódico que primero va al archivador, saca la carpeta correcta y te responde citando el folio.

🔍 **Qué explica el texto:**
- **Recuperar:** dada una pregunta, encontrar los pasajes más relevantes. Aquí se hace con búsqueda por **palabras en común** (lo de R3-01); se menciona que los sistemas avanzados usan *embeddings*, pero el flujo es el mismo.
- **Aumentar:** construir un prompt que incluya esos pasajes como contexto, la pregunta, y la instrucción de oro: *"responde solo con esta información"*.
- **Generar:** el LLM redacta la respuesta a partir del contexto entregado, no de su memoria.
- Y los dos comportamientos que hacen confiable al sistema: **fundamentar** (grounding) y **abstenerse** cuando la respuesta no está.

⚠️ **Error frecuente:** creer que RAG "entrena" o "actualiza" al modelo. No: el modelo queda igual; lo que cambia es **lo que le muestras** en cada pregunta.

✅ **Señal de comprensión:** puedes explicar las tres piezas con la analogía del archivador y decir por qué la abstención es la que evita los errores más graves en un contexto público.

---

### 🔷 Sección 2: Preparación — documentos, NLP y el LLM

🎯 **Objetivo:** ejecutar la celda que carga las tres piezas de trabajo: la KB, el tokenizador y la conexión al LLM.

💡 **Concepto clave — nada aquí es nuevo, es reutilización:**
Esta celda arma el taller con herramientas que ya conoces: el `tokenizar` de R3-01 (normaliza, quita tildes y stopwords, descarta palabras de menos de 3 letras) y el patrón **"en vivo o caché"** de R3-02 para hablar con Gemini.

🔍 **Qué hace el código:**
- Instala el SDK oficial de Google (`google-genai`) y fija `MODELO = "gemini-2.5-flash"`.
- Carga `licitacion.csv` con pandas (si no existe localmente, intenta descargarlo desde GitHub) y lo convierte en `KB`, una lista de diccionarios `{id, fuente, texto}`.
- Define `normalizar` y `tokenizar` (con su lista de `STOPWORDS`), tal como en R3-01.
- Busca tu `GEMINI_API_KEY` en los Secrets de Colab o en variables de entorno.
- Define `preguntar_llm(prompt, tarea)`: **si hay API key**, llama a Gemini en vivo; **si no hay** (o la llamada falla), devuelve una respuesta del diccionario `CACHE`. Así el módulo funciona con o sin conexión.

⚠️ **Error frecuente:** frustrarse porque "no tengo API key". No la necesitas: el modo caché devuelve respuestas pregrabadas coherentes y los 4 chequeos pasan igual. La celda de "Manejo de Errores Comunes" del notebook cubre además los errores de cuota (cae solo a caché) y el `TypeError` con `&` cuando algo no es `set`.

✅ **Señal de comprensión:** puedes explicar qué devuelve `preguntar_llm` en cada uno de los dos modos y por qué `KB` es una lista de diccionarios y no un DataFrame.

---

### 🔷 Sección 3: Los cuatro ejercicios = las piezas del RAG

🎯 **Objetivo:** entender que los ejercicios no son sueltos: **son el sistema completo**, pieza por pieza.

💡 **Concepto clave — la línea de producción:**
Ejercicio 1 construye el **índice** (el archivador ordenado), Ejercicio 2 la **recuperación** (encontrar la carpeta), Ejercicio 3 el **prompt aumentado** (el memo con antecedentes adjuntos) y Ejercicio 4 lo une todo en `responder` (el asistente que fundamenta o se abstiene). Al final del cuarto, tienes un RAG funcionando de punta a punta.

🔍 **Qué hace el flujo completo:** `responder(consulta)` → `recuperar(consulta, k=2)` → si hay pasajes, `armar_prompt(...)` → `preguntar_llm(...)`; si no hay pasajes, abstención sin llamar al modelo.

⚠️ **Error frecuente:** avanzar al ejercicio siguiente con un ❌ pendiente. Cada pieza usa la anterior: si `INDICE` está malo, `recuperar` fallará aunque tu código sea correcto.

✅ **Señal de comprensión:** puedes dibujar el flujo recuperar → aumentar → generar y decir qué ejercicio implementa cada flecha.

---

### 🔷 Sección: Cierre — lo que te llevas

🎯 **Objetivo:** consolidar las cuatro ideas del módulo y proyectarlas a tu trabajo.

💡 **Concepto clave — la receta es transferible:**
El cierre del notebook lo resume así: RAG no hace al modelo más listo, **le pone la página correcta enfrente**; la recuperación puede empezar simple (palabras en común) y crecer hacia *embeddings* sin cambiar el flujo; la instrucción "responde SOLO con esto" es lo que ancla la respuesta; y lo más valioso en el Estado es la **abstención**. Cualquier conjunto de documentos de tu servicio —reglamento interno, bases tipo, preguntas frecuentes— puede convertirse en asistente con esta misma receta. Y como cita la fuente, **siempre puedes verificar**.

🔍 **Qué hace:** es una celda de texto de síntesis; no hay código nuevo que ejecutar.

⚠️ **Error frecuente:** cerrar el notebook sin probar `responder` con preguntas propias. Prueba una que esté en la ficha (los plazos de p7, por ejemplo) y una que no, y observa cuándo fundamenta y cuándo se abstiene.

✅ **Señal de comprensión:** las 4 celdas de chequeo muestran ✅ y puedes nombrar un conjunto de documentos de tu propio servicio que convertirías en RAG.

---

## 6. Guía de los Ejercicios

> Las pistas van de suave a directa. Intenta con la 🟢 antes de mirar la 🟡, y guarda la 🔴 para cuando de verdad estés pegado/a.

### ✍️ Ejercicio 1 — Indexar los documentos

**Objetivo:** programar `indexar(kb)` que devuelva un diccionario `{id_del_pasaje: conjunto_de_tokens}`.

**Habilidad que entrena:** preparar los documentos para búsqueda rápida (el índice del archivador).

**Pistas progresivas:**
1. 🟢 *Pista suave:* para cada pasaje `p` de la lista, necesitas dos cosas: su identificador (`p["id"]`) como llave, y sus palabras útiles como valor. La función que extrae palabras útiles ya existe y viene de R3-01.
2. 🟡 *Pista media:* `tokenizar(p["texto"])` devuelve una **lista**; el chequeo exige un **conjunto** (`set`). Conviértela. ¿Por qué un set? Porque para medir "palabras en común" da igual cuántas veces se repite una palabra, solo si está o no, y los conjuntos hacen la intersección directa.
3. 🔴 *Pista directa:* una comprensión de diccionario de una sola línea lo resuelve: recorre `kb`, usa el `id` como llave y el `set` de los tokens del `texto` como valor.

**Lógica de la solución (en prosa):** recorrer la KB una sola vez y, por cada pasaje, guardar bajo su `id` el conjunto de tokens de su texto. Nada más: el trabajo pesado lo hace `tokenizar`.

**Qué valida el chequeo ✅:** que `INDICE` sea un diccionario con 8 entradas (una por pasaje), que cada valor sea un `set`, y que el pasaje `p4` incluya los tokens `"precio"` y `"pondera"`.

---

### ✍️ Ejercicio 2 — Recuperar: encontrar los pasajes relevantes

**Objetivo:** programar `recuperar(consulta, k=2)` que devuelva los `k` pasajes que más palabras comparten con la pregunta, descartando los de puntaje 0.

**Habilidad que entrena:** el corazón del *retrieval* — puntuar, ordenar y filtrar.

**Pistas progresivas:**
1. 🟢 *Pista suave:* la receta tiene tres pasos: (1) tokeniza la consulta y guárdala como conjunto, (2) calcula para cada pasaje cuántas palabras comparte con la consulta, (3) quédate con los mejores. "Cuántas palabras comparte" es el tamaño de una intersección de conjuntos.
2. 🟡 *Pista media:* acumula pares `(puntaje, pasaje)` **solo cuando el puntaje sea mayor que 0**, luego ordena esa lista de mayor a menor por el puntaje y toma los primeros `k`. Recuerda devolver solo los pasajes, no los pares.
3. 🔴 *Pista directa:* la intersección es `consulta_tokens & INDICE[p["id"]]` y su tamaño se mide con `len(...)`. Para ordenar una lista de tuplas por su primer elemento de mayor a menor, usa `.sort()` con `key` y `reverse=True`. El corte final es un slicing `[:k]`.

**Lógica de la solución (en prosa):** convertir la pregunta en un conjunto de tokens, medir la superposición con el conjunto de cada pasaje (que ya está precalculado en `INDICE`), guardar solo los que comparten algo, ordenarlos de más a menos parecido y devolver los k mejores.

**Qué valida el chequeo ✅:** que para *"¿qué porcentaje pondera el precio en la evaluación?"* el mejor pasaje sea **p4**, que para *"¿cuánto es la garantía de fiel cumplimiento?"* sea **p6**, y que para *"¿cuál es la capital de Francia?"* devuelva **lista vacía** (nada comparte palabras → nada que recuperar).

> ⚠️ **El detalle que importa:** descartar el puntaje 0 no es una manía estética. Es lo que después permite **abstenerse**: si nada comparte palabras con la pregunta, esa lista vacía es una señal valiosa.

---

### ✍️ Ejercicio 3 — Aumentar: el prompt con contexto

**Objetivo:** programar `armar_prompt(consulta, pasajes)` que devuelva un texto con la instrucción de fundamentar, los pasajes como contexto y la pregunta.

**Habilidad que entrena:** diseño de prompts con anclaje (*grounding*) — la pieza de R3-02 aplicada a RAG.

**Pistas progresivas:**
1. 🟢 *Pista suave:* el prompt es un solo string con tres bloques, en este orden: (1) la instrucción ("responde usando SOLO la información de los Documentos; si no está, dilo claramente"), (2) los textos de los pasajes recuperados, (3) la pregunta del usuario.
2. 🟡 *Pista media:* para el bloque de contexto, une los pasajes en un solo texto, uno por línea, incluyendo su `id` entre corchetes antes del texto — así la respuesta puede **citar la fuente**. El método `"\n".join(...)` sobre una expresión generadora es tu amigo.
3. 🔴 *Pista directa:* construye primero la variable `contexto` uniendo `[id] texto` de cada pasaje, y luego arma el prompt concatenando: instrucción + salto de línea + `"Documentos:"` con el contexto + `"Pregunta:"` con la consulta + `"Respuesta:"` al final. Los f-strings hacen el ensamblaje limpio.

**Lógica de la solución (en prosa):** es un problema de redacción más que de programación: escribir el memo perfecto para el modelo. La frase restrictiva es lo que **ancla** la respuesta a tus documentos; sin ella, el modelo vuelve a su memoria y puede alucinar.

**Qué valida el chequeo ✅:** que el prompt sea un string, que incluya el **texto** de los pasajes, que incluya la **pregunta** literal, y que contenga las palabras "solo" y "documentos" (la instrucción de fundamentar).

---

### ✍️ Ejercicio 4 — Generar (y saber decir "no lo sé")

**Objetivo:** programar `responder(consulta)` que une todo: recupera, y según el resultado, genera o se abstiene.

**Habilidad que entrena:** orquestar el flujo completo y garantizar la abstención **por diseño**.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son tres pasos con una bifurcación: recuperar con `k=2`; si la lista viene vacía, devolver el mensaje de abstención; si trae pasajes, armar el prompt y pasárselo al LLM.
2. 🟡 *Pista media:* el mensaje de abstención debe ser **exactamente** `"No encontré esa información en los documentos disponibles."` (el chequeo busca "no encontr" en la respuesta). Y la llamada al modelo es `preguntar_llm(prompt, tarea="rag")`.
3. 🔴 *Pista directa:* `pasajes = recuperar(consulta, k=2)`; luego un `if not pasajes:` que devuelve el mensaje; y en el camino feliz, `armar_prompt(consulta, pasajes)` seguido de `preguntar_llm(...)`. Cuatro líneas bien puestas.

**Lógica de la solución (en prosa):** la regla de oro es que si la recuperación no trae nada, **ni siquiera llamamos al modelo**: respondemos honestamente que no está en los documentos. Así la abstención no depende de la buena voluntad del LLM — está garantizada por el código.

**Qué valida el chequeo ✅:** que ante *"¿Cuál es la capital de Francia?"* la función **se abstenga** (aunque cualquier LLM "sabe" la respuesta), y que ante *"¿Qué porcentaje pondera el precio en la evaluación?"* devuelva una respuesta fundamentada no vacía, sin abstenerse.

---

## 7. Sección Especial: RAG y Política Pública

**Reflexión guiada:** tu RAG responde sobre una licitación real —la 2239-8-LR25— citando el pasaje exacto de la ficha. Imagina esto desplegado en una mesa de ayuda de ChileCompra: un proveedor pyme pregunta a las 11 de la noche *"¿necesito garantía de seriedad para ofertar?"* y recibe al instante *"No: esta licitación no exige garantía de seriedad de la oferta [p5]"*. Eso baja barreras de entrada, descarga a los equipos de las preguntas repetidas y deja registro verificable de cada respuesta.

Pero el mismo diseño te obliga a pensar en los riesgos:

- **Cobertura:** tu KB tiene 8 pasajes. Si un proveedor pregunta por los productos incluidos en el Convenio Marco o por cómo impugnar la adjudicación, el sistema (bien diseñado) se abstiene. ¿Quién decide qué documentos entran a la KB y quién la mantiene al día cuando la ficha se modifica?
- **Falsa seguridad:** una recuperación por palabras en común puede traer el pasaje equivocado si la pregunta usa sinónimos ("boleta de garantía" vs. "garantía de fiel cumplimiento"). La respuesta sonará segura e igual estará mal fundamentada. Por eso la **cita de la fuente** no es decoración: es lo que permite al humano verificar.
- **Responsabilidad:** si el asistente responde mal y un proveedor pierde el plazo de 20 días hábiles para entregar la garantía, ¿quién responde? El pie de página "verifique en la ficha oficial" no es opcional en un despliegue estatal.

**Pregunta de debate abierta:** ¿debería un servicio público permitir que un asistente RAG responda **directamente al ciudadano**, o solo como borrador que un funcionario revisa antes de enviar? ¿Cambia tu respuesta según si la consulta es sobre plazos (verificable en un dato) o sobre interpretación de bases?

**Datos que complementarían el análisis:** el texto completo de las bases (no solo 8 fragmentos), el historial de preguntas y respuestas del foro de la licitación (para saber qué se pregunta de verdad), las modificaciones y aclaraciones publicadas después, y la normativa marco (Ley 19.886 y su reglamento) para preguntas que cruzan varias licitaciones.

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Qué problema de los LLM resuelve RAG?

- a) Que los modelos son lentos para responder
- b) **Que solo saben lo de su entrenamiento y, cuando no saben, inventan con seguridad ✅**
- c) Que las API de LLM son caras
- d) Que los modelos no entienden español

**Explicación:** RAG ataca la memoria limitada y las alucinaciones: en vez de confiar en lo que el modelo "recuerda", le entrega los documentos relevantes para que responda basándose en ellos. No lo hace más rápido ni más barato: lo hace **verificable**.

---

**Pregunta 2:** En el flujo recuperar → aumentar → generar, ¿qué significa "aumentar"?

- a) Aumentar el tamaño del modelo con más parámetros
- b) Aumentar la cantidad de documentos de la base de conocimiento
- c) **Construir un prompt que incluye los pasajes recuperados, la pregunta y la instrucción de responder solo con esa información ✅**
- d) Aumentar la temperatura del modelo para respuestas más creativas

**Explicación:** "aumentar" se refiere al **prompt aumentado**: el contexto recuperado se adjunta a la pregunta junto con la instrucción de anclaje. Es el memo con los antecedentes adjuntos, no un cambio en el modelo.

---

**Pregunta 3:** Tu función `recuperar` devuelve lista vacía para *"¿cuál es la capital de Francia?"*. ¿Qué hace el RAG bien diseñado del módulo?

- a) Llama igual al LLM, que seguro sabe la respuesta
- b) Busca la respuesta en internet
- c) **Se abstiene: responde que no encontró esa información en los documentos, sin llamar al modelo ✅**
- d) Devuelve el pasaje p1 por defecto

**Explicación:** la regla de oro del Ejercicio 4: si la recuperación no trae nada, ni siquiera se llama al modelo. La abstención queda garantizada **por código**, no por la buena voluntad del LLM. En un contexto público, preferir callar a inventar es lo que hace confiable al sistema.

---

**Pregunta 4:** ¿Por qué el índice del Ejercicio 1 guarda los tokens de cada pasaje como `set` y no como lista?

- a) Porque los sets ocupan menos memoria en todos los casos
- b) **Porque para medir "palabras en común" solo importa si la palabra está o no, y los sets permiten la intersección directa con `&` ✅**
- c) Porque pandas solo acepta sets
- d) Porque las listas no pueden contener strings

**Explicación:** el puntaje de relevancia es el tamaño de la intersección entre los tokens de la consulta y los del pasaje. Los conjuntos hacen esa operación de forma directa y rápida; cuántas veces se repite una palabra no aporta a este método.

---

**Pregunta 5:** Ejecutas el notebook sin `GEMINI_API_KEY`. ¿Qué pasa?

- a) El notebook falla en la celda de preparación
- b) Los ejercicios 3 y 4 no se pueden completar
- c) **`preguntar_llm` usa respuestas en caché y los 4 chequeos pueden pasar igual ✅**
- d) Gemini responde igual pero más lento

**Explicación:** el patrón "en vivo o caché" (heredado de R3-02) revisa si hay API key; si no la hay —o si la llamada en vivo falla, por ejemplo por cuota—, devuelve una respuesta pregrabada del diccionario `CACHE`. El módulo completo es realizable sin conexión.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **RAG** | Técnica que busca documentos relevantes y se los entrega al LLM para que responda basándose en ellos | El colega metódico: primero el archivador, después la respuesta, siempre citando el folio |
| **Base de conocimiento (KB)** | Colección de pasajes con identificador, fuente y texto | El archivador oficial de la unidad, con documentos foliados |
| **Pasaje** | Fragmento de documento con `id`, `fuente` y `texto` (aquí, p1 a p8 de la ficha) | Un párrafo citado del expediente, con su referencia |
| **Índice** | Diccionario que asocia cada pasaje con su conjunto de palabras útiles | El índice temático que se arma una vez para buscar mil veces |
| **Token** | Palabra útil que queda tras normalizar y filtrar stopwords | Las palabras clave de un documento, sin los "de", "la", "que" |
| **Recuperación (retrieval)** | Encontrar los pasajes más relevantes para una pregunta | Ubicar los expedientes que calzan con la consulta ciudadana |
| **Prompt aumentado** | Instrucción + pasajes de contexto + pregunta, todo en un solo texto | El memo con antecedentes adjuntos y la nota "responda en base a lo adjunto" |
| **Fundamentar (grounding)** | Que la respuesta se base en los documentos entregados, no en la memoria del modelo | Ninguna afirmación del informe sin respaldo en el expediente |
| **Abstención** | Responder "no lo sé" cuando la información no está en los documentos | "No consta en los antecedentes disponibles" en vez de aventurar |
| **Alucinación** | Respuesta inventada por el LLM con tono seguro | El dato "de memoria" que nadie verificó y terminó en el oficio |
| **Embeddings** | Vectores numéricos que capturan el significado del texto; permiten recuperar por semejanza de sentido, no solo de palabras | Archivar por tema y no por orden alfabético: encuentra "boleta de garantía" aunque preguntes por "caución" |
| **Patrón "en vivo o caché"** | Con API key llama al modelo real; sin ella usa respuestas guardadas | Plan A en línea, plan B con respaldo: el trámite no se detiene |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R3-04 · Agentes

En este módulo construiste un sistema que hace **una** cosa muy bien: responder preguntas sobre documentos, citando la fuente y absteniéndose cuando no sabe. Pero mira tu propia rama R3: ya sabes **clasificar** texto (R3-01), **extraer y generar** con un LLM (R3-02) y **recuperar y responder** con RAG (R3-03). Son cuatro herramientas distintas... y hasta ahora, eres tú quien decide cuál usar en cada caso.

En **R3-04** darás el último paso antes del capstone: construir un **agente**, un sistema donde el propio LLM **decide qué herramienta usar** para resolver una tarea de principio a fin. Llega un correo ciudadano: ¿hay que clasificarlo, extraerle datos, buscar en la normativa o las tres cosas en orden? El agente lo encadena solo.

**Pregunta motivadora:** si tu RAG ya sabe decir "no lo sé", ¿qué debería hacer un agente cuando **ninguna** de sus herramientas sirve para la tarea que le pidieron... y cómo te aseguras de que también prefiera detenerse antes que improvisar?

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos de Chile · Formación Pública*
*Formación Pública Chile · Licencia CC BY 4.0*
