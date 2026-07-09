# 📘 Guía de Aprendizaje — R3-02 · IA generativa y LLMs

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R3-02 · IA generativa y LLMs |
| **Pista / Rama** | R3 — IA Aplicada (para funcionarios públicos chilenos) |
| **Posición** | Módulo 3 de 6 de la rama R3 |
| **Duración estimada** | 2–3 horas (+ 2 minutos para crear tu API key, opcional) |
| **Nivel** | Intermedio (rama avanzada, sin matemáticas nuevas) |
| **Prerrequisitos** | R3-00 (on-ramp exprés) y, muy recomendado, R3-01 (introducción al NLP) |
| **Competencia de salida** | Resolver una tarea real de texto del Estado con un LLM, de forma reproducible y responsable |
| **Dataset** | `rubros.csv` — 12 rubros reales (subconjunto del catálogo de ChileCompra), columna única `rubro` |
| **LLM** | Google Gemini (`gemini-2.5-flash`), capa gratuita de Google AI Studio — **sin tarjeta de crédito** |
| **Entregable** | Las **4 celdas de chequeo** del notebook mostrando ✅ |

> 🔌 **Este módulo funciona con o sin internet y con o sin API key.** El notebook usa el patrón
> **"en vivo o caché"**: si configuras tu clave gratuita, hablas con Gemini en vivo; si no,
> usa respuestas reales guardadas en caché y los 4 ejercicios se completan igual. Nadie se queda fuera.

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En R3-01 le enseñaste a la máquina a **contar palabras**. Funcionó… hasta que llegó una solicitud
que decía *"jeringas y guantes para el hospital"* y tu clasificador de palabras clave se quedó en
blanco: ninguna de esas palabras aparece en el nombre del rubro "Equipamiento y suministros médicos".
Contar no es entender.

Este módulo da el salto: vas a conectar tu cuaderno a un **modelo de lenguaje grande (LLM)** —la
misma tecnología detrás de ChatGPT, Gemini o Claude— y usarlo para tres tareas que aparecen todas
las semanas en un servicio público:

- **Explicar:** pedirle una explicación clara y breve de un concepto (una licitación, un trámite) para un informe o un correo ciudadano.
- **Clasificar por significado:** asignar solicitudes de compra al rubro correcto del catálogo de ChileCompra, aunque el texto no comparta ni una palabra con el nombre del rubro.
- **Extraer datos estructurados:** convertir la descripción libre de una licitación en un JSON limpio (`objeto`, `categoria`, `es_servicio`) que puedes guardar en una tabla.

Y hay una cuarta habilidad, tan importante como las anteriores: el **uso responsable**. Los LLMs
inventan datos con total seguridad (alucinan), y la capa gratuita de muchos proveedores puede usar
tus textos para entrenar sus modelos. En el Estado eso no es un detalle: es protección de datos
personales y probidad. Por eso el último ejercicio construye un **guardrail** que bloquea el envío
de textos con RUT antes de que salgan de tu computador.

**Decisiones de política pública que habilita:** estandarizar la clasificación de compras públicas
(hoy manual y dispareja entre servicios), estructurar texto libre de licitaciones para análisis
masivo, y sentar reglas internas de uso de IA generativa que protejan los datos de las personas.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **LLM** | Modelo entrenado para predecir la siguiente palabra; de paso captura significado | Un funcionario recién llegado que leyó *toda* la biblioteca del Congreso: no sabe tu caso, pero entiende de qué le hablas |
| **Prompt** | La instrucción que le das al modelo | El memo que le mandas a un asesor: mientras más claro el encargo, mejor el producto |
| **API / API key** | Puerta de acceso al modelo desde Python; la key es tu credencial personal | La clave única del Estado: te identifica ante el servicio y **no se comparte** |
| **Secrets de Colab** | Bodega segura para guardar la API key fuera del código | La caja fuerte de la oficina: la clave no queda anotada en el informe que circulará |
| **Patrón "en vivo o caché"** | Usa la API real si hay key; si no, respuestas reales guardadas | Atender con el sistema en línea o, si se cae, con el respaldo impreso: el trámite sale igual |
| **Respuesta probabilística** | El mismo prompt puede dar respuestas algo distintas cada vez | Dos abogados redactan el mismo dictamen con palabras distintas pero igual conclusión |
| **Clasificación por significado** | Asigna categoría entendiendo sinónimos y contexto | El funcionario experimentado que sabe que "jeringas" va a insumos médicos sin buscar la palabra en el catálogo |
| **Extracción estructurada (JSON)** | Convierte texto libre en campos con nombre y tipo | Pasar un oficio en prosa al formulario estándar: cada dato en su casillero |
| **Alucinación** | El modelo inventa datos plausibles pero falsos | Un informe con cifras "de memoria" sin citar la fuente: se ve serio, pero no resiste una contraloría |
| **Guardrail** | Barrera automática que revisa antes de enviar | El visto bueno de la oficina de partes: nada sale sin pasar el filtro |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Este módulo no exige matemáticas nuevas, pero sí manejo básico de Python y la experiencia de R3-01
(para valorar lo que el LLM resuelve). Responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Ejecutar celdas en Google Colab y leer errores simples | ✅ Sí / 🔄 Revisar R3-00 |
| Definir una función en Python (`def`) que reciba texto y devuelva un valor | ✅ Sí / 🔄 Revisar R3-00 |
| Usar f-strings para armar un texto con variables (`f"Hola {nombre}"`) | ✅ Sí / 🔄 Revisar R3-00 |
| Trabajar con diccionarios de Python (crear, leer claves) | ✅ Sí / 🔄 Revisar R3-00 |
| Explicar por qué clasificar por palabras clave falla con sinónimos | ✅ Sí / 🔄 Revisar R3-01 |
| (Opcional) Crear una cuenta de Google / usar la de Colab | ✅ Sí — es la misma cuenta |

Si tienes más de dos "Revisar", dedica 30 minutos a repasar esos módulos antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 1: ¿Qué es un LLM (y por qué funciona)?

🎯 **Objetivo:** entender, a nivel intuitivo, qué es un LLM, cómo se dirige con prompts, por qué es probabilístico y cuáles son las reglas de uso responsable.

💡 **Concepto clave — predecir la próxima palabra:**
Un LLM está entrenado para una tarea engañosamente simple: dado un texto, predecir la palabra que
sigue ("El cielo es de color…" → "azul"). Repetido miles de millones de veces sobre casi todo el
texto de internet, el modelo termina **capturando patrones del lenguaje y del mundo**. Es como un
funcionario que, a fuerza de leer decenas de miles de expedientes, ya "cacha" de qué trata uno nuevo
con solo mirar el primer párrafo. Por eso el LLM sabe que "jeringa", "guante quirúrgico" e "insumo
clínico" pertenecen al mundo médico aunque las palabras no coincidan — exactamente lo que el conteo
de palabras de R3-01 no podía hacer.

🔍 **Qué aprenderás en esta sección (es teórica, sin código):**
- Las **3 reglas de un buen prompt**: sé específico (qué quieres y en qué formato), da contexto (pega las opciones, el texto), acota la salida (una palabra, un JSON, sin texto extra).
- Que el LLM **no es determinista**: el mismo prompt puede dar respuestas algo distintas. Por eso los chequeos del notebook validan la **estructura** de la respuesta (¿es JSON válido? ¿la categoría está permitida?), no el texto exacto.
- Las 3 reglas de **uso responsable en el Estado**: verificar toda cifra contra la fuente oficial (alucinaciones), no enviar datos personales ni información reservada (la capa gratuita puede usar tus textos para entrenar), y recordar que la responsabilidad de la decisión pública sigue siendo **humana**.

⚠️ **Error frecuente:** tratar al LLM como un buscador de hechos. No lo es: optimiza *plausibilidad*, no verdad. Una cifra, una ley o un nombre que entregue un LLM **nunca** se publica sin verificar.

✅ **Señal de comprensión:** puedes explicarle a un colega, sin tecnicismos, por qué "predecir la próxima palabra" termina produciendo algo que entiende sinónimos — y por qué eso mismo lo hace capaz de inventar datos con total seguridad.

---

### 🔷 Sección 2: Tu API key gratuita (Google AI Studio)

🎯 **Objetivo:** obtener (opcionalmente) tu API key gratuita de Gemini y guardarla de forma segura en los Secrets de Colab.

💡 **Concepto clave — la API key es una credencial, no un dato más:**
La key te identifica ante Google igual que tu clave única te identifica ante el Estado. Quien la
tenga puede consumir tu cuota haciéndose pasar por ti. Por eso la regla de oro del notebook:
**nunca** se escribe la key dentro de una celda (quedaría guardada en el archivo `.ipynb` que
después compartes o subes a un repositorio). Se guarda en el panel 🔑 **Secrets** de Colab, que
funciona como caja fuerte: el código puede leerla, pero no queda escrita en el cuaderno.

🔍 **Qué hace el procedimiento (3 pasos, ~2 minutos):**
1. Entras a `https://aistudio.google.com/apikey` con tu cuenta de Google (la misma de Colab) — **gratis y sin tarjeta de crédito**.
2. Pulsas *Create API key* y copias la clave.
3. En Colab: panel izquierdo → 🔑 *Secrets* → *Add new secret* → nombre `GEMINI_API_KEY`, pegas el valor y habilitas el acceso para el notebook.

La capa gratuita permite del orden de 1.500 solicitudes al día — más que suficiente para el módulo
completo. Y una advertencia que el notebook repite con razón: en el plan gratuito, **Google puede
usar tus textos para mejorar sus modelos**. Por eso aquí se practica solo con datos públicos de
ChileCompra, nunca con datos personales.

⚠️ **Error frecuente:** pegar la key directamente en una celda "solo para probar". Ese cuaderno luego se comparte, se sube a GitHub o queda en un Drive compartido… y la key queda expuesta. Si te pasó, revócala en AI Studio y crea otra.

✅ **Señal de comprensión:** sabes explicar por qué la key va en Secrets y no en el código, y qué implica la política de datos de la capa gratuita para tu trabajo en el Estado.

---

### 🔷 Sección 3: La celda de configuración (patrón "en vivo o caché")

🎯 **Objetivo:** ejecutar la celda que instala el SDK, carga la API key (si existe) y define `preguntar_llm()`, la función que usarás en todos los ejercicios.

💡 **Concepto clave — "en vivo o caché", nadie se queda fuera:**
La función `preguntar_llm(prompt, tarea=...)` decide sola cómo responder. Si detecta tu API key,
llama a Gemini **en vivo**. Si no hay key (o la llamada en vivo falla), usa el diccionario `CACHE`,
que guarda **respuestas reales** del modelo para las tres tareas del módulo (`generico`,
`clasificar`, `extraer`). Es como atender público con el sistema en línea o, si se cae la red, con
el respaldo: el trámite sale igual. Así el cuaderno es siempre ejecutable y verificable, con o sin
conexión.

🔍 **Qué hace el código:**
- `!pip install -q google-genai` instala el SDK oficial de Google (en Colab; si ya está, no hace nada).
- `MODELO = "gemini-2.5-flash"` fija el modelo gratuito de la capa sin tarjeta.
- `_cargar_api_key()` busca la key primero en los Secrets de Colab y luego en las variables de entorno (`GEMINI_API_KEY` o `GOOGLE_API_KEY`); si no la encuentra, devuelve `None`.
- `CACHE` es un diccionario con respuestas reales pregrabadas para cada tarea.
- `preguntar_llm(prompt, tarea)` implementa el patrón: con key llama a `_llamar_gemini(prompt)`; sin key (o si la llamada falla) devuelve `CACHE[tarea]`.
- `_sa(s)` es un auxiliar de los chequeos: pasa el texto a minúsculas y le quita las tildes, para comparar sin pelear con "clasificación" vs "clasificacion".
- El `print` final te dice en qué modo estás: `🔑 API key detectada → modo EN VIVO` o `ℹ️ Sin API key → modo CACHÉ (offline)`.

⚠️ **Error frecuente:** creer que el modo caché es "de mentira". Las respuestas de `CACHE` son salidas reales del modelo; los 4 ejercicios y sus chequeos funcionan idéntico. Lo único que cambia es que en modo caché el modelo no ve *tu* prompt específico.

✅ **Señal de comprensión:** al ejecutar la celda sabes en qué modo quedaste y puedes explicar la cadena de decisión: Secrets → variable de entorno → caché.

---

### 🔷 Sección 4: Prueba de humo

🎯 **Objetivo:** verificar que todo el circuito funciona antes de los ejercicios.

💡 **Concepto clave — probar antes de construir:**
Igual que en una implementación de sistemas en tu servicio: antes de cargar los datos reales,
mandas una transacción de prueba. Aquí la prueba es una sola línea que pide explicar en una frase
qué es una licitación pública.

🔍 **Qué hace el código:** `print(preguntar_llm("Explica en una frase qué es una licitación pública.", tarea="generico"))` — en modo en vivo verás la respuesta fresca de Gemini; en modo caché, la respuesta guardada.

⚠️ **Error frecuente:** saltarse esta celda e ir directo al Ejercicio 1. Si algo falla después, no sabrás si el problema es tu código o la conexión. Ejecuta la prueba de humo primero.

✅ **Señal de comprensión:** ves una explicación coherente de qué es una licitación pública, en cualquiera de los dos modos.

---

## 6. Guía de los Ejercicios

El módulo tiene **4 ejercicios**, cada uno con su celda de chequeo (✅ / ❌ con pista amable).
Importante: como el LLM es probabilístico, los chequeos **no validan texto exacto** sino estructura
y categoría — ese estilo de validación es en sí mismo una lección de cómo se programa con LLMs.

### ✍️ Ejercicio 1 — Tu primer prompt

**Objetivo:** escribir en `prompt1` una instrucción que pida explicar, en una sola frase y en lenguaje simple, qué es una licitación pública. La línea provista llama al modelo y guarda la respuesta en `respuesta1`.

**Habilidad que entrena:** redactar prompts específicos (tema + formato + audiencia).

**Pistas progresivas:**
1. 🟢 *Pista suave:* no hay que programar nada nuevo — solo reemplazar el `None` por un texto entre comillas. Piensa en las 3 reglas de la Sección 1: qué quieres, en qué formato, para quién.
2. 🟡 *Pista media:* tu prompt debe mencionar explícitamente la palabra "licitación" y pedir el formato "una sola frase". Agregar la audiencia ("para un funcionario público", "en lenguaje simple") mejora notablemente la respuesta.
3. 🔴 *Pista directa:* estructura sugerida: *"Explica en una sola frase, en lenguaje simple para un funcionario, qué es una licitación pública."* Escríbelo con tus palabras — lo que importa es que estén el tema, el formato y la audiencia.

**Lógica de la solución (en prosa):** se asigna a `prompt1` una instrucción clara que combine tema, formato y audiencia. La celda ya llama a `preguntar_llm(prompt1, tarea="generico")` por ti.

**Qué valida el chequeo ✅:** que `prompt1` sea un string con sentido (15+ caracteres), que mencione "licitaci…" (sin importar tildes ni mayúsculas), y que `respuesta1` haya llegado no vacía.

---

### ✍️ Ejercicio 2 — Clasificar *con comprensión* (lo que R3-01 no podía)

**Objetivo:** programar `clasificar_llm(texto)` que arme un prompt con la lista `RUBROS` (los 12 rubros reales de `rubros.csv`), pida elegir el más adecuado y devuelva solo el nombre exacto del rubro.

**Habilidad que entrena:** clasificación por significado con un LLM — dar contexto (las opciones) y acotar la salida (solo el nombre).

**Pistas progresivas:**
1. 🟢 *Pista suave:* la función tiene 3 pasos: (a) convertir la lista `RUBROS` en un texto de opciones, (b) armar un prompt que incluya esas opciones, el texto a clasificar y la instrucción de responder solo con el nombre exacto, (c) llamar a `preguntar_llm` y limpiar espacios.
2. 🟡 *Pista media:* para las opciones, el propio notebook te sugiere `"\n".join("- " + r for r in RUBROS)` — una línea por rubro con guion. Luego usa una f-string para insertar las opciones y el `texto` en el prompt. La llamada lleva `tarea="clasificar"`.
3. 🔴 *Pista directa:* el prompt del notebook tiene 4 partes: un rol ("Eres un asistente de compras públicas…"), la lista de opciones, la solicitud entre comillas, y la orden final "Responde SOLO con el nombre exacto del rubro". Al resultado de `preguntar_llm(...)` aplícale `.strip()` antes de devolverlo.

**Lógica de la solución (en prosa):** se construye el prompt con las 12 opciones y la solicitud, se pide una salida acotada (solo el nombre), y se devuelve la respuesta sin espacios sobrantes. La gracia está en el caso de prueba: *"jeringas, guantes de látex y mascarillas para el hospital"* no comparte ninguna palabra con "Equipamiento y suministros médicos" — el clasificador de palabras clave de R3-01 fallaba aquí; el LLM lo resuelve por significado.

**Qué valida el chequeo ✅:** que la función no devuelva `None`, que devuelva texto no vacío, y que para el caso del hospital la respuesta contenga "medic…" (es decir, un rubro médico) — sin exigir texto exacto, porque el modelo es probabilístico.

---

### ✍️ Ejercicio 3 — Extraer datos estructurados (JSON)

**Objetivo:** programar `extraer_json(texto)` que pida al modelo un JSON con exactamente las claves `"objeto"` (texto), `"categoria"` (texto) y `"es_servicio"` (booleano), limpie la respuesta y la convierta a diccionario.

**Habilidad que entrena:** convertir texto libre del Estado en datos ordenados listos para una tabla — la tarea estrella de los LLMs en gestión pública.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son dos mitades: el prompt (describe las 3 claves, sus tipos, y exige "responde SOLO el JSON, sin explicaciones ni ```") y el post-procesamiento (limpiar la respuesta y parsearla).
2. 🟡 *Pista media:* la llamada lleva `tarea="extraer"`. Los LLMs a veces envuelven el JSON en un bloque de código con ``` — hay que quitarle ese envoltorio antes de parsear. El notebook te muestra los métodos exactos: `.strip()`, `.removeprefix(...)` y `.removesuffix(...)`.
3. 🔴 *Pista directa:* la secuencia de limpieza del notebook es: recibir el texto bruto, quitarle espacios con `.strip()`, remover los prefijos ```` ```json ```` y ```` ``` ```` y el sufijo ```` ``` ````, volver a hacer `.strip()`, y finalmente `json.loads(bruto)` para obtener el diccionario.

**Lógica de la solución (en prosa):** el prompt define el contrato (claves exactas, tipos, "solo el JSON") y el código limpia defensivamente la respuesta antes de `json.loads`. Fíjate en el doble seguro: un buen prompt *reduce* el texto extra, y la limpieza *tolera* el que igual aparezca. Así se programa con un componente probabilístico.

**Qué valida el chequeo ✅:** que el resultado sea un diccionario (no `None`, no string), que tenga las tres claves `objeto`, `categoria` y `es_servicio`, que `es_servicio` sea booleano de verdad (`true`/`false`, no texto) y que `objeto` sea texto no vacío.

---

### ✍️ Ejercicio 4 — Uso responsable: no entregues datos personales

**Objetivo:** programar el guardrail `es_seguro_enviar(texto)` que devuelva `False` si el texto contiene un RUT chileno y `True` si está limpio.

**Habilidad que entrena:** proteger datos personales *antes* de que salgan hacia un servicio externo — con código, no solo con buenas intenciones.

**Pistas progresivas:**
1. 🟢 *Pista suave:* el patrón de expresión regular ya viene dado en la celda (`patron_rut`). Solo necesitas buscarlo en el texto y devolver el booleano correcto según haya o no coincidencia.
2. 🟡 *Pista media:* `re.search(patron_rut, texto)` devuelve un objeto si encuentra un RUT y `None` si no. Tu función debe devolver `True` exactamente cuando esa búsqueda **no** encuentra nada.
3. 🔴 *Pista directa:* el propio notebook te lo sopla: `re.search(patron, texto) is None` es `True` cuando el texto está limpio. Esa expresión, con el patrón y el texto correctos, es todo lo que la función necesita devolver.

**Lógica de la solución (en prosa):** una sola línea que invierte el resultado de la búsqueda: si el patrón de RUT aparece, no es seguro enviar. El patrón cubre RUT con y sin puntos y con dígito verificador numérico o letra K.

**Qué valida el chequeo ✅:** que un texto administrativo limpio ("Comprar 500 resmas de papel…") dé `True`, que un texto con RUT (`12.345.678-9`) dé `False`, y que también detecte el dígito verificador `K` (`9.876.543-K`).

---

## 7. Sección Especial: El Ejercicio de Política Pública

El Ejercicio 4 es el más corto en código y el más importante en implicancias. Un guardrail de una
línea encarna una decisión de política institucional: **nada sale hacia un servicio externo sin
pasar un filtro automático**.

**Reflexión guiada:**
- La capa gratuita de Gemini puede usar tus textos para entrenar. Un RUT, un nombre asociado a un diagnóstico, o el detalle de una investigación en curso, enviados "para que el modelo me ayude a redactar", pasan a estar fuera del control del Estado. La Ley 19.628 (protección de la vida privada) y su sucesora hacen de esto una obligación legal, no una cortesía.
- El guardrail del módulo detecta RUT, pero ese es solo el caso más típico. ¿Qué otros patrones debería bloquear una versión institucional? Nombres junto a datos de salud, direcciones particulares, números de causas reservadas, correos personales de ciudadanos.
- Nota la asimetría: el LLM puede *ayudar* a clasificar y extraer, pero la **verificación de cifras** y la **decisión** siguen siendo humanas. Si el JSON extraído en el Ejercicio 3 alimentara pagos o adjudicaciones, ¿qué control humano pondrías entre el modelo y la decisión?

**Pregunta de debate abierta:**
> Tu servicio quiere usar un LLM gratuito para clasificar automáticamente las miles de solicitudes
> de compra que llegan al mes. ¿Bajo qué condiciones dirías que sí? ¿Qué guardrails, qué
> verificación humana y qué reglas de datos exigirías antes de firmar el visto bueno?

**Otros datos que complementarían el análisis:**
- El catálogo completo de rubros de ChileCompra (aquí usamos un subconjunto de 12), para medir si el LLM acierta también con categorías muy parecidas entre sí.
- Un conjunto de solicitudes reales ya clasificadas a mano, para calcular la tasa de acierto del LLM contra el criterio humano (como aprendiste a evaluar en la rama R2).
- Los términos de servicio de niveles pagados/empresariales del proveedor, donde el tratamiento de datos suele ser distinto al de la capa gratuita.

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Cuál es la tarea básica para la que se entrena un LLM?

- a) Buscar información en internet en tiempo real
- b) **Predecir la siguiente palabra de un texto ✅**
- c) Traducir entre idiomas
- d) Detectar datos personales

**Explicación:** el entrenamiento consiste en predecir la próxima palabra, miles de millones de veces. Resumir, clasificar o traducir son capacidades que *emergen* de haber capturado patrones del lenguaje y del mundo para predecir bien — nadie programó cada tarea explícitamente.

---

**Pregunta 2:** El LLM te entrega, con total seguridad, la cifra del presupuesto 2026 de un servicio. ¿Qué haces antes de ponerla en un informe?

- a) La uso: el modelo la dio con mucha confianza
- b) La redondeo para no comprometerme
- c) **La verifico contra la fuente oficial (DIPRES, Ley de Presupuestos) ✅**
- d) Le pregunto de nuevo al modelo para confirmar

**Explicación:** los LLMs optimizan *plausibilidad*, no verdad: pueden inventar cifras, leyes y nombres con total seguridad (alucinaciones). Preguntar de nuevo no verifica nada — el modelo puede repetir o variar el invento. Toda cifra se contrasta con la fuente oficial antes de publicarse.

---

**Pregunta 3:** ¿Por qué las celdas de chequeo del notebook validan la *estructura* de la respuesta (JSON válido, categoría permitida) y no el texto exacto?

- a) Porque validar texto exacto es técnicamente imposible
- b) **Porque el LLM es probabilístico: el mismo prompt puede dar respuestas algo distintas ✅**
- c) Porque el texto exacto está protegido por derechos de autor
- d) Porque la caché no guarda el texto completo

**Explicación:** un LLM no es determinista. Si el chequeo exigiera un texto idéntico, fallaría aunque la respuesta fuera correcta. Por eso, al programar con LLMs, se define un *contrato de estructura* (claves del JSON, categoría dentro de la lista, formato) y se valida eso.

---

**Pregunta 4:** ¿Cuál de estos textos es seguro enviar a la capa gratuita de un LLM?

- a) "Paciente Juan Pérez, RUT 12.345.678-9, diagnóstico pendiente"
- b) "Listado de deudores morosos con nombres y direcciones"
- c) **"Convenio Marco para la adquisición de productos de aseo e higiene" ✅**
- d) Todos, porque el servicio es de Google y es confiable

**Explicación:** en la capa gratuita, el proveedor puede usar tus textos para entrenar sus modelos. Los textos con datos personales (RUT, nombres asociados a salud o deudas) no deben salir del Estado. La descripción de un Convenio Marco es información pública de ChileCompra: esa sí.

---

**Pregunta 5:** Tu prompt "clasifica esto" da resultados erráticos. Según las reglas del módulo, ¿cuál es la mejora más efectiva?

- a) Repetir la llamada varias veces y quedarse con la más frecuente
- b) Cambiar a un modelo más grande y caro
- c) **Incluir la lista de opciones válidas y exigir responder solo con el nombre exacto ✅**
- d) Escribir el prompt en inglés

**Explicación:** las tres reglas del buen prompt son especificidad, contexto y salida acotada. Darle las opciones (contexto) y prohibir texto extra (salida acotada) es exactamente lo que hace `clasificar_llm` en el Ejercicio 2 — y suele rendir más que cambiar de modelo.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **LLM (Large Language Model)** | Modelo entrenado para predecir la siguiente palabra que, de paso, captura significado | Asesor que leyó todo el archivo institucional: entiende contexto y sinónimos |
| **IA generativa** | IA que produce contenido nuevo (texto, código) en vez de solo clasificar lo existente | Redactar el borrador del oficio, no solo archivarlo en la carpeta correcta |
| **Prompt** | La instrucción que le das al modelo | El memo de encargo: tema + formato + audiencia |
| **API** | Puerta para usar un servicio desde tu código | Ventanilla de interoperabilidad entre sistemas del Estado |
| **API key** | Credencial personal que te identifica ante el servicio | Tu clave única: personal e intransferible, jamás se anota en un documento que circula |
| **Secrets de Colab** | Almacenamiento seguro de claves, fuera del código del notebook | La caja fuerte de la oficina: se usa, no se exhibe |
| **Caché** | Respuestas reales guardadas que se usan cuando no hay conexión o key | El respaldo impreso del sistema: permite seguir atendiendo si se cae la red |
| **Probabilístico (no determinista)** | El mismo input puede producir outputs algo distintos | Dos redactores del mismo dictamen: palabras distintas, misma conclusión |
| **Alucinación** | Dato inventado por el modelo, entregado con total seguridad | Cifra "de memoria" en un informe: plausible, pero no resiste contraloría |
| **JSON** | Formato de texto para datos estructurados con claves y valores | El formulario estándar: cada dato en su casillero, listo para la planilla |
| **`json.loads`** | Función de Python que convierte texto JSON en un diccionario | Traspasar el formulario recibido a la base de datos interna |
| **Guardrail** | Barrera automática que revisa/bloquea antes de una acción riesgosa | El filtro de la oficina de partes: nada sale sin visto bueno |
| **Expresión regular (regex)** | Patrón para buscar formatos de texto (p. ej., un RUT) | El ojo entrenado que detecta un RUT en cualquier documento, con o sin puntos |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R3-03 · RAG (Retrieval-Augmented Generation)

En este módulo el LLM respondió solo con lo que "sabe" de su entrenamiento: conocimiento general
de internet, congelado en el tiempo. Te sirvió para explicar, clasificar y extraer. Pero apenas
intentes preguntarle por **tu** realidad —el instructivo interno de tu servicio, las bases de una
licitación específica, la circular que salió el mes pasado— chocarás con el límite: el modelo
nunca vio esos documentos, y si le preguntas igual, corre el riesgo de alucinar una respuesta.

**R3-03 resuelve exactamente eso** con RAG: una técnica para **darle al LLM tus propios
documentos** en el momento de la pregunta, de modo que responda con datos del Estado **citando la
fuente**. Es el paso que convierte al LLM de "asistente culto general" en "asistente que se leyó
tu normativa". Y en R3-04 encadenarás todo en **agentes** que ejecutan tareas de varios pasos.

**Pregunta motivadora para llevar contigo:**
> Ya sabes que el modelo alucina cuando no sabe. Si pudieras "pasarle" los documentos oficiales de
> tu servicio antes de cada pregunta… ¿cómo harías para que encuentre solo los párrafos relevantes
> entre miles de páginas — y para que te demuestre, con la cita exacta, que no está inventando?

---

*Formación Pública Chile · Licencia CC BY 4.0*
