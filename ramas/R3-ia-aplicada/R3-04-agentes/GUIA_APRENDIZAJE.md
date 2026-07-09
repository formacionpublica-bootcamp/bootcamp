# 📘 Guía de Aprendizaje — R3-04 · Agentes

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R3-04 · Agentes (proyecto integrador de IA aplicada) |
| **Pista / Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Avanzado · **Módulo de cierre de la rama** |
| **Prerrequisitos** | R3-01 (NLP), R3-02 (IA generativa y LLMs), R3-03 (RAG). Ayuda haber visto pronóstico por crecimiento medio (R2-10), pero la lección lo repasa |
| **Competencia de salida** | Orquestar varias capacidades de IA en un único asistente que resuelve tareas reales de gobierno de principio a fin |
| **Dataset** | `gasto_anual.csv` — serie anual de gasto público 2019–2025 (ChileCompra) + catálogo de rubros de MercadoPúblico + ficha de licitación 2239-8-LR25 |
| **LLM** | Google Gemini (`gemini-2.5-flash`) con patrón **"en vivo o caché"**: funciona con o sin `GEMINI_API_KEY` |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Piensa en tu bandeja de entrada un lunes cualquiera. Llegan consultas de todo tipo: "¿en qué rubro clasifico esta compra de insumos?", "¿cuánto pondera el precio en esa licitación?", "¿cuánto se proyecta gastar el próximo año?". Cada una requiere una habilidad distinta: buscar en un catálogo, leer unas bases, hacer un cálculo. Tú **decides** qué hacer con cada una y luego lo haces. Esa decisión, tan natural para ti, es exactamente lo que aprenderás a programar hoy.

Un **agente** es un asistente que recibe una petición en lenguaje natural, **decide qué herramienta usar**, la ejecuta y responde. Es el patrón detrás de los asistentes de IA que "hacen cosas", no solo "conversan". Y es el módulo que integra todo el bloque: el pronóstico, la clasificación de texto, el RAG sobre documentos y el guardrail de privacidad que ya construiste.

**Lo concreto que aprenderás:**
- Entender el ciclo del agente: **percibir → decidir → actuar → responder**.
- Empaquetar capacidades previas como **herramientas** invocables.
- Construir un **enrutador** que elige la herramienta correcta para cada petición.
- Hacer el agente **transparente** (traza auditable: qué herramienta usó y por qué) y **seguro** (bloquea peticiones con datos personales antes de que salgan a un servicio externo).

**La clave para el Estado:** automatizar una tarea repetitiva está muy bien — responder 200 consultas de rubro al mes es un uso perfecto —, pero automatizar **con criterio y con supervisión humana**. Por eso el módulo no termina cuando el agente "funciona": termina cuando el agente **deja registro de lo que hizo** y **se niega a procesar datos personales**. Esa diferencia es la que separa un juguete tecnológico de una herramienta usable en un servicio público.

**Conexión con los datos reales:** tu agente trabajará sobre tres fuentes reales de ChileCompra / MercadoPúblico: la serie de gasto público anual 2019–2025 (que creció de $8,1 a $18,4 billones de pesos, un +126% en seis años), un catálogo de 8 rubros de compra, y las bases de la licitación 2239-8-LR25.

---

## 3. Mapa Conceptual del Módulo

La mejor analogía del módulo: **un agente es como un practicante nuevo en tu unidad**. Le das herramientas concretas (el catálogo de rubros, las bases de la licitación, la planilla de gasto), instrucciones claras de cuándo usar cada una, y —fundamental— **le revisas el trabajo**. No le entregas la clave del sistema el primer día ni dejas que firme oficios solo.

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| **Agente** | Recibe una petición, decide qué herramienta usar, actúa y responde | Practicante capacitado: recibe el encargo, elige el procedimiento correcto y ejecuta |
| **Herramienta (tool)** | Función que hace una cosa bien y el agente puede invocar | Cada recurso de la oficina: el catálogo, el archivador de bases, la planilla de gasto |
| **Enrutador (router)** | La pieza que decide qué herramienta corresponde a cada petición | El criterio de la jefatura al derivar cada consulta a la unidad correcta |
| **Ciclo decidir → actuar → responder** | El flujo interno del agente en cada petición | Recibir el memo → derivarlo → tramitarlo → responder con copia al expediente |
| **Enrutador por reglas** | Decide con palabras clave; determinista y verificable sin conexión | Protocolo escrito de derivación: "si dice 'licitación', va a Compras" |
| **Enrutador por LLM** | Un LLM elige la herramienta; flexible pero no determinista | Funcionario experimentado que deriva "a ojo": acierta más casos raros, pero hay que auditarlo |
| **Traza de auditoría** | Registro de qué herramienta se usó para cada respuesta | El timbre y la hoja de ruta del expediente: se puede reconstruir quién hizo qué |
| **Guardrail de privacidad** | Filtro que bloquea peticiones con datos personales (ej: RUT) | Control previo que impide enviar datos de ciudadanos a un servicio externo |
| **Salida por defecto** | Herramienta "general" cuando ninguna regla calza | Oficina de partes: nada se queda sin respuesta, aunque sea "esto no me corresponde" |
| **Patrón "en vivo o caché"** | Con API key el LLM responde en vivo; sin ella, respuestas guardadas | Trabajar con el sistema en línea o con el respaldo impreso: el trámite avanza igual |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Este es el módulo integrador de la rama: usa piezas de los tres módulos anteriores. Responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Definir una función en Python con `def`, parámetros y `return` | ✅ Sí / 🔄 Revisar R3-00 |
| Escribir condicionales `if / elif / else` encadenados | ✅ Sí / 🔄 Revisar R3-00 |
| Explicar qué hace un clasificador de texto por palabras | ✅ Sí / 🔄 Revisar R3-01 |
| Explicar qué es un LLM y el patrón "en vivo o caché" | ✅ Sí / 🔄 Revisar R3-02 |
| Explicar por qué no se envían datos personales a un LLM externo | ✅ Sí / 🔄 Revisar R3-02 |
| Explicar cómo un RAG responde con pasajes de un documento | ✅ Sí / 🔄 Revisar R3-03 |
| Trabajar con diccionarios Python (`{"clave": valor}`) | ✅ Sí / 🔄 Revisar R3-00 |

Si tienes más de dos "Revisar", vuelve primero a R3-02: el guardrail y el patrón de LLM de ese módulo son piezas directas de los ejercicios de hoy. La buena noticia: las herramientas complejas vienen **provistas**; tu trabajo es la orquestación.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0: Tabla de datos reales

🎯 **Objetivo:** conocer las tres fuentes de datos reales de la administración pública chilena que tu agente usará para responder.

💡 **Concepto clave — un agente vale lo que valen sus fuentes:**
Antes de programar nada, el notebook te muestra el "archivador" del agente. Igual que un practicante no puede responder consultas sin acceso al catálogo y a las bases, tu agente depende por completo de estas tres fuentes:

- **Catálogo de rubros de MercadoPúblico (simplificado):** 8 rubros reales, desde "Alimentos, bebidas y tabaco" hasta "Servicios de limpieza industrial".
- **Bases de la licitación 2239-8-LR25:** criterios de evaluación (precio 75%, experiencia 20%, programa de integridad 3%, requisitos formales 2%), garantía de fiel cumplimiento de $400.000, contrato de 36 meses, sin exigencia de garantía de seriedad.
- **Gasto público histórico anual 2019–2025 (`gasto_anual.csv`):** desde $8.141.600.896.708 en 2019 hasta $18.430.546.563.769 en 2025.

🔍 **Qué hace la sección:** es solo lectura (una celda Markdown), pero conviene detenerse en la serie de gasto: en seis años el monto registrado se multiplicó por más de 2,2. Esa serie alimenta la herramienta de pronóstico que construirás en el Ejercicio 1.

⚠️ **Error frecuente:** confundir la magnitud de las cifras. Están en **pesos chilenos** (CLP): $18.430.546.563.769 son unos $18,4 **billones** de pesos (millones de millones), no "18 mil millones".

✅ **Señal de comprensión:** puedes decir qué fuente usará el agente para cada tipo de consulta: rubro → catálogo, licitación → ficha, gasto futuro → serie histórica.

---

### 🔷 Sección 1: ¿Qué es un agente?

🎯 **Objetivo:** entender la diferencia entre un programa de receta fija y un agente que decide, y conocer las cuatro herramientas que usará el tuyo.

💡 **Concepto clave — la pieza nueva es la decisión:**
Un programa normal sigue una receta: haz A, luego B, luego C. Un agente, ante cada petición, **primero decide** qué hacer y recién entonces actúa. Su ciclo es: **percibir** (recibe la petición) → **decidir** (elige una herramienta) → **actuar** (la ejecuta) → **responder** (entrega el resultado diciendo qué hizo). Es como derivar correspondencia en una oficina de partes: el valor no está en tramitar, sino en derivar bien.

Tu agente tendrá 4 herramientas, todas heredadas del bootcamp:

| Herramienta | Qué hace | Viene de |
|---|---|---|
| `clasificar_compra` | dice a qué rubro pertenece una compra | R3-01 / R3-02 |
| `consultar_ficha` | responde preguntas sobre una licitación (RAG) | R3-03 |
| `pronosticar_gasto` | proyecta el gasto público de un año | pronóstico por crecimiento medio (la construyes tú en el Ejercicio 1) |
| `responder_general` | responde con el LLM cuando nada encaja | R3-02 |

⚠️ **Error frecuente:** creer que en este módulo el LLM decide todo. Aquí la decisión la toma un **enrutador por reglas** (palabras clave), a propósito: así el notebook es 100% reproducible y verificable sin conexión. La lección explica que en producción esa decisión suele tomarla un LLM (como viste en R3-02: darle opciones y pedirle que elija) — el patrón es idéntico, solo cambia el "cerebro".

✅ **Señal de comprensión:** puedes explicar con tus palabras por qué "transparente" (traza auditable) y "seguro" (no filtrar datos personales) **no son opcionales** en un agente del Estado.

---

### 🔷 Sección 2: Preparación — tus herramientas, ya listas

🎯 **Objetivo:** ejecutar la celda de preparación y entender qué deja lista cada pieza.

💡 **Concepto clave — te entregan el kit del practicante:**
Para que te concentres en el agente (la orquestación), la celda provee versiones compactas de lo que ya construiste. Es como recibir la oficina con el archivador ordenado: catálogo de rubros, ficha de licitación y planilla de gasto ya cargados.

🔍 **Qué hace el código:**
- Instala el SDK oficial de Google (`google-genai`) y fija `MODELO = "gemini-2.5-flash"`.
- Carga `gasto_anual.csv` (lo descarga desde GitHub si no está) y arma el diccionario `GASTO` con la serie 2019–2025.
- Define `RUBROS` (8 rubros reales de MercadoPúblico) y `KB` (4 pasajes de la ficha 2239-8-LR25: evaluación con precio 75% y experiencia 20%, garantía de fiel cumplimiento de $400.000, contrato de 36 meses, sin garantía de seriedad).
- Define `preguntar_llm` con el patrón **"en vivo o caché"**: si hay `GEMINI_API_KEY` (en los Secrets de Colab o como variable de entorno), llama a Gemini en vivo; si no, usa una respuesta guardada. El módulo completo funciona igual en ambos modos.
- Provee las herramientas `clasificar_compra` (coincidencia de palabras contra los rubros), `consultar_ficha` (RAG compacto sobre `KB`), `responder_general` (el LLM), más dos auxiliares: `es_seguro_enviar` (detecta RUT con una expresión regular) y `_extraer_anio` (saca un año de 4 dígitos del texto).

⚠️ **Error frecuente:** preocuparse porque dice "Modo LLM: CACHÉ (offline)". Es normal y esperado sin API key: los 4 ejercicios se completan igual, porque el enrutador y casi todas las herramientas no dependen de la red.

✅ **Señal de comprensión:** el print muestra las herramientas listas y sabes decir cuál de las 4 usa el LLM (solo `responder_general`) y cuáles funcionan sin conexión.

---

### 🔷 Sección 3: Manejo de errores comunes

🎯 **Objetivo:** conocer de antemano los 4 tropiezos típicos al construir el agente, para reconocerlos cuando aparezcan.

💡 **Concepto clave — el error también deja lecciones de gestión:**
Dos de los cuatro errores son técnicos (año ausente en el pronóstico, condicionales mal ordenados) y dos son **institucionales**: perder la traza de auditoría y filtrar datos personales. Que el notebook los trate al mismo nivel no es casualidad: en el Estado, una respuesta sin registro o una fuga de RUT son fallas tan graves como un programa caído.

🔍 **Qué revisa la sección:**
- **`AttributeError` con `NoneType`:** si la petición no trae año, `_extraer_anio` devuelve `None`. Solución: `anio = _extraer_anio(peticion) or 2026`.
- **Enrutamiento fallido:** las reglas se evalúan en orden y son excluyentes; si una consulta cae en la herramienta equivocada, revisa el orden de los `if` y las palabras clave.
- **Pérdida de traza:** `agente_seguro` debe devolver siempre el diccionario `{"herramienta": ..., "respuesta": ...}`.
- **Fuga de datos personales:** `es_seguro_enviar` debe ser el **primer** filtro, antes de cualquier procesamiento.

✅ **Señal de comprensión:** puedes explicar por qué el guardrail va primero y no al final (si filtras después de procesar, el dato ya salió).

---

## 6. Guía de los Ejercicios

El notebook tiene **4 ejercicios**, cada uno con su celda de chequeo (✅ / ❌). Se construyen en cadena: la herramienta (1), la decisión (2), el agente (3) y la versión auditable y segura (4).

### ✍️ Ejercicio 1 — Construye una herramienta: pronosticar el gasto

**Objetivo:** programar `pronosticar_gasto(anio)`, que proyecta el gasto público con el método del **crecimiento medio**.

**Habilidad que entrena:** convertir una lógica de análisis (pronóstico) en una **herramienta** reutilizable por el agente.

**Pistas progresivas:**
1. 🟢 *Pista suave:* la serie 2019–2025 está en el diccionario `GASTO`. La idea es: ¿cuánto creció el gasto en promedio cada año? Aplica ese mismo ritmo hacia adelante, año por año, desde 2025 hasta el año pedido.
2. 🟡 *Pista media:* necesitas tres pasos: (a) los años ordenados con `sorted(GASTO)` y sus valores; (b) la lista de crecimientos año a año — cada uno es "valor de este año dividido por el del anterior, menos 1" — y su promedio; (c) un bucle que parta del valor de 2025 y lo multiplique por (1 + crecimiento medio) tantas veces como años falten.
3. 🔴 *Pista directa:* la cantidad de vueltas del bucle es `anio - anios[-1]` (para 2026 es 1 vuelta; para 2027, 2). Dentro del bucle, actualiza el valor acumulado multiplicándolo por `(1 + g)`. El notebook incluye además una pista con la estructura en la celda del enunciado — úsala solo si las anteriores no bastaron.

**Lógica de la solución en prosa:** calculas los 6 crecimientos anuales de la serie (van de 8,6% a 25,0%), los promedias (~14,7% anual) y compones ese crecimiento desde el último valor conocido ($18,43 billones en 2025) hasta el año solicitado. Recuerda la advertencia de la lección: es una **estimación con supuestos** (que el ritmo histórico continúa), una referencia y no una certeza.

**Qué valida el chequeo ✅:** que `pronosticar_gasto(2026)` coincida (con tolerancia mínima) con el crecimiento medio aplicado una vez, y que 2027 aplique el crecimiento **año a año** (no de un solo salto). Si está bien, imprime los montos proyectados: ~$21,1 billones para 2026 y ~$24,3 billones para 2027.

---

### ✍️ Ejercicio 2 — El enrutador: ¿qué herramienta uso?

**Objetivo:** programar `elegir_herramienta(peticion)`, que devuelve `"clasificar"`, `"pronostico"`, `"ficha"` o `"general"` según palabras clave.

**Habilidad que entrena:** programar la **decisión** del agente como reglas ordenadas y excluyentes — el corazón del módulo.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son 4 reglas en orden fijo: compras (comprar/adquirir/rubro), pronóstico (pronóstico/proyección/gastar/futuro), licitación (licitación/ficha/garantía/plazo/evaluación/contrato/precio) y, si nada calza, `"general"`. Piensa en un protocolo de derivación escrito.
2. 🟡 *Pista media:* normaliza primero el texto con `_sa(peticion)` (minúsculas y sin tildes, así "pronóstico" y "pronostico" calzan igual). Para cada grupo, pregunta si **alguna** palabra del grupo aparece en el texto.
3. 🔴 *Pista directa:* la construcción `any(palabra in texto for palabra in [...])` dentro de un `if` por grupo resuelve cada regla; el `return "general"` va al final, fuera de todos los `if`, como salida por defecto. Truco útil: usar raíces como `"pronostic"` o `"proyec"` calza con "pronóstico", "pronosticar" y "proyección" a la vez.

**Lógica de la solución en prosa:** el texto normalizado se compara contra tres listas de palabras clave, en el orden indicado; la primera regla que calza gana y devuelve el nombre de su herramienta. Si ninguna calza, la petición va a la salida general. El orden importa porque las reglas son secuenciales y excluyentes.

**Qué valida el chequeo ✅:** cuatro casos, uno por herramienta: una compra de muebles → `"clasificar"`, cuánto gastará el Estado el 2027 → `"pronostico"`, qué pondera el precio en la evaluación → `"ficha"`, y un saludo → `"general"`.

---

### ✍️ Ejercicio 3 — El agente: decidir y actuar

**Objetivo:** programar `agente(peticion)`, que une el enrutador con las herramientas: decide y despacha.

**Habilidad que entrena:** la orquestación completa del ciclo **decidir → actuar → responder**.

**Pistas progresivas:**
1. 🟢 *Pista suave:* primero pregunta a `elegir_herramienta` cuál corresponde; luego, con un `if/elif` por caso, llama a la herramienta correcta pasándole la petición.
2. 🟡 *Pista media:* tres de los cuatro casos son una línea (llamar a `clasificar_compra`, `consultar_ficha` o `responder_general` con la petición). El caso `"pronostico"` requiere dos pasos: extraer el año y armar el texto de respuesta.
3. 🔴 *Pista directa:* para el pronóstico, `anio = _extraer_anio(peticion) or 2026` cubre el caso sin año; la respuesta es un f-string con el formato `f"Gasto proyectado para {anio}: {pronosticar_gasto(anio):,.0f} CLP"`. Y no olvides el `return` final para `"general"`: un agente robusto siempre tiene salida por defecto.

**Lógica de la solución en prosa:** el agente delega la decisión en el enrutador del Ejercicio 2 y ejecuta la herramienta elegida. Nota cómo el agente no "sabe" clasificar ni pronosticar: solo sabe **a quién preguntarle**. Igual que una buena jefatura.

**Qué valida el chequeo ✅:** que la compra de muebles devuelva el rubro de muebles, que el pronóstico del 2027 mencione el año y el monto en CLP, y que la consulta de evaluación traiga el pasaje de la ficha con el precio al 75%.

---

### ✍️ Ejercicio 4 — Cierre: un agente transparente y seguro

**Objetivo:** programar `agente_seguro(peticion)`, que devuelve un diccionario con la **traza** de la decisión y **bloquea** peticiones con datos personales.

**Habilidad que entrena:** convertir un agente que funciona en uno **usable en el Estado**: auditable y con guardrail de privacidad.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son dos caminos. Si la petición no es segura, devuelves el diccionario de bloqueo sin procesar nada. Si es segura, ejecutas el agente normal y devuelves el resultado junto con el nombre de la herramienta usada.
2. 🟡 *Pista media:* el guardrail va **primero**: `if not es_seguro_enviar(peticion):` y ahí devuelves `{"herramienta": "bloqueado", "respuesta": "Petición bloqueada: contiene datos personales (RUT)."}` (texto exacto según el enunciado).
3. 🔴 *Pista directa:* en el camino seguro necesitas dos llamadas: `elegir_herramienta(peticion)` para saber **qué** se usó (la traza) y `agente(peticion)` para obtener la respuesta. Ambas van dentro del diccionario `{"herramienta": ..., "respuesta": ...}`.

**Lógica de la solución en prosa:** es el patrón "fail fast" aplicado a la privacidad: primero el filtro, después el trabajo. El diccionario resultante es tu hoja de ruta del expediente: cualquier auditor puede reconstruir qué herramienta respondió cada petición.

**Qué valida el chequeo ✅:** que la respuesta sea un diccionario con las claves `herramienta` y `respuesta`, que la compra de muebles registre `"clasificar"` como herramienta usada, y que una petición que incluye un RUT (`12.345.678-9`) quede con herramienta `"bloqueado"`.

---

## 7. Sección Especial: Automatizar decisiones públicas... ¿sin nadie mirando?

Tu agente ya decide solo. Y justo ahí empieza la conversación más importante del módulo.

**Reflexión guiada.** El agente de hoy hace tareas de bajo riesgo: clasificar una compra, citar una ficha, proyectar un monto. Pero el mismo patrón —petición, decisión automática, acción— podría aplicarse a decisiones con efectos directos sobre personas: priorizar postulaciones a un beneficio, filtrar reclamos "improcedentes", preseleccionar proveedores. Antes de automatizar una decisión pública, conviene preguntarse al menos:

1. **¿Qué pasa cuando se equivoca?** Tu enrutador acierta los 4 casos del chequeo, pero una petición redactada de forma inusual puede caer en la herramienta equivocada. Si el costo del error lo paga un ciudadano (un beneficio denegado, un trámite mal derivado), el agente puede **proponer**, pero una persona debe **decidir**. Es el principio de *humano en el bucle*.
2. **¿Puede explicarse?** La traza del Ejercicio 4 permite responder "¿por qué el sistema hizo esto?". Sin traza no hay auditoría; sin auditoría no hay responsabilidad administrativa posible. Un agente que no registra sus decisiones no debería operar en el Estado.
3. **¿Protege los datos de las personas?** Tu guardrail bloquea RUT antes de que el texto salga a un servicio externo. Es un piso mínimo: la ley 19.628 (y el marco de protección de datos que la reemplaza) exige tratar los datos personales con fines específicos y resguardo — y un LLM comercial externo no es un lugar autorizado para ellos.
4. **¿El pronóstico se usa con la humildad debida?** Tu herramienta proyecta ~$21,1 billones para 2026 asumiendo que el crecimiento medio histórico (~14,7% anual) continúa. Pero ese promedio esconde años de 8,6% y años de 25,0%. Presentarlo como certeza en una glosa presupuestaria sería un mal uso; presentarlo como escenario de referencia, uno legítimo.

**Pregunta de debate abierta:** en tu institución, ¿qué tarea repetitiva delegarías hoy a un agente como este, y qué decisión te negarías a delegar aunque técnicamente se pudiera? ¿Dónde pondrías la línea del "humano en el bucle"?

**Datos que complementarían el análisis:** la serie mensual de gasto (para capturar estacionalidad que el promedio anual esconde), el registro histórico de reclasificaciones manuales de rubro (para medir cuánto se equivoca el clasificador en la práctica), y un registro de las peticiones bloqueadas por el guardrail (para saber cuántos datos personales circulan por los canales de consulta).

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Qué distingue a un agente de un programa tradicional?

- a) El agente usa siempre un LLM
- b) **El agente decide qué herramienta usar ante cada petición, en vez de seguir una receta fija ✅**
- c) El agente es más rápido
- d) El agente no necesita código

**Explicación:** la pieza nueva del agente es la **decisión**. Las herramientas (clasificar, pronosticar, consultar) ya existían; lo distinto es que ahora un enrutador elige cuál usar según la petición. Puede haber agentes sin LLM (como el de este módulo, con reglas).

---

**Pregunta 2:** En este módulo el enrutador funciona con reglas de palabras clave y no con un LLM. ¿Por qué?

- a) Porque los LLM no pueden elegir herramientas
- b) Porque las reglas siempre son mejores en producción
- c) **Para que el notebook sea determinista, reproducible y verificable sin conexión; el patrón de decisión es el mismo ✅**
- d) Porque Gemini no está disponible en Chile

**Explicación:** en producción la decisión suele tomarla un LLM (darle las opciones y pedirle que elija, como en R3-02). Aquí se usa reglas para que los chequeos den siempre el mismo resultado, con o sin API key. Cambia el "cerebro" que decide, no el patrón.

---

**Pregunta 3:** Tu agente recibe "¿Cuánto se gastará a futuro?" (sin año). ¿Qué debe pasar?

- a) Debe lanzar un error, porque falta información
- b) Debe derivar la petición a la herramienta general
- c) **Debe usar un año por defecto (2026), porque `_extraer_anio` devuelve `None` cuando no hay año ✅**
- d) Debe pedir el año al LLM

**Explicación:** es el primer error común de la lección: `re.search` devuelve `None` si no encuentra un año de 4 dígitos, y eso rompería el f-string del pronóstico. El patrón `anio = _extraer_anio(peticion) or 2026` da un valor por defecto razonable y el agente responde igual.

---

**Pregunta 4:** ¿Por qué `agente_seguro` devuelve `{"herramienta": ..., "respuesta": ...}` en vez de solo el texto?

- a) Porque los diccionarios ocupan menos memoria
- b) **Porque el nombre de la herramienta es la traza de auditoría: permite reconstruir y explicar qué hizo el sistema ✅**
- c) Porque Gemini exige ese formato
- d) Por estética del código

**Explicación:** en el Estado, poder responder "¿por qué el sistema hizo esto?" es un requisito, no un lujo. La traza registra qué herramienta atendió cada petición, lo que habilita depuración, auditoría y responsabilidad sobre las decisiones automatizadas.

---

**Pregunta 5:** Llega la petición "El proveedor RUT 12.345.678-9 entrega el martes". ¿Qué hace un agente bien construido?

- a) La clasifica en el rubro de servicios
- b) La envía al LLM para que responda con cuidado
- c) La procesa, pero borra el RUT de la respuesta
- d) **La bloquea antes de procesarla, porque contiene datos personales ✅**

**Explicación:** el guardrail (`es_seguro_enviar`) va **primero**, antes de cualquier procesamiento. Filtrar después no sirve: si el texto ya viajó a un servicio externo, el dato personal ya se filtró. Bloquear e informar es la conducta correcta.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Agente** | Programa que decide qué herramienta usar ante cada petición, actúa y responde | Practicante capacitado que deriva y tramita cada encargo con criterio |
| **Herramienta (tool)** | Función que hace una cosa bien y que el agente puede invocar | Cada recurso de la oficina: catálogo, archivador, planilla |
| **Enrutador (router)** | Componente que elige la herramienta adecuada para cada petición | Criterio de derivación de la oficina de partes |
| **Ciclo decidir → actuar → responder** | Flujo del agente: percibir la petición, elegir, ejecutar, informar | Recibir → derivar → tramitar → responder con registro |
| **Enrutamiento por reglas** | Decisión con palabras clave; determinista y auditable | Protocolo escrito de derivación de consultas |
| **Enrutamiento por LLM** | Un modelo de lenguaje elige la herramienta; más flexible, menos predecible | Derivación "a ojo" de un funcionario experimentado |
| **Salida por defecto** | Caso `"general"` cuando ninguna regla calza | Nada queda sin respuesta: si no corresponde, se informa igual |
| **Traza de auditoría** | Registro de qué herramienta respondió cada petición | Hoja de ruta del expediente: reconstruir quién hizo qué |
| **Guardrail** | Filtro previo que bloquea entradas riesgosas (ej: datos personales) | Control de admisibilidad antes de ingresar el trámite |
| **Humano en el bucle** | Diseño donde una persona revisa o aprueba las decisiones del sistema | La jefatura firma; el sistema solo propone |
| **Crecimiento medio** | Promedio de las variaciones anuales, usado para proyectar | Estimar el presupuesto del próximo año con el alza promedio histórica |
| **Patrón "en vivo o caché"** | Con API key, el LLM responde en línea; sin ella, respuestas guardadas | Trabajar con el sistema en línea o con el respaldo impreso |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R3-CAP · Capstone de IA Aplicada

Mira lo que acabas de cerrar: partiste la rama clasificando texto con palabras (R3-01), aprendiste a conversar con un LLM de forma segura (R3-02), le enseñaste a responder con tus propios documentos (R3-03) y hoy orquestaste todo en un agente que decide, actúa, deja traza y protege datos personales — sobre gasto real del Estado que creció de $8,1 a $18,4 billones entre 2019 y 2025. Eso es IA aplicada al servicio público, hecha por ti.

En el **capstone** el andamiaje desaparece: tomas un problema real de tu institución y lo resuelves de punta a punta con las piezas de la rama — datos, clasificación, RAG, agente, guardrails — y lo documentas para que otra persona pueda evaluarlo y usarlo.

**Pregunta motivadora:** en tu servicio hay una tarea que alguien repite todas las semanas — clasificar correos, buscar en bases de licitación, proyectar un gasto. Si tuvieras que convertirla en tu capstone, ¿qué herramientas tendría tu agente, qué reglas usaría su enrutador... y en qué punto exacto del flujo pondrías a la persona que supervisa?

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos de Chile · Formación Pública Chile*
*Contenido bajo licencia CC BY 4.0*
