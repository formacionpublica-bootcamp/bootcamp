# Guía de Aprendizaje · R3-CAP · Capstone — Proyecto integrador de IA aplicada

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · IA Aplicada · Semana 6–7 (cierre de rama) · Google Colab

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Módulo** | R3-CAP · Capstone — proyecto integrador de IA aplicada |
| **Rama** | R3 · IA Aplicada |
| **Semanas** | 6–7 de la rama (cierre) |
| **Duración estimada** | 4–6 horas de trabajo autónomo |
| **Nivel** | Integrador — aplica todo lo aprendido en R3-00 a R3-04 |
| **Prerrequisitos** | Haber completado R3-00 a R3-04 con ✅ en todos los notebooks |
| **Corpus de ejemplo** | 4 documentos de normativa de compras públicas (licitaciones, convenio marco, trato directo, tamaños de proveedor), embebidos en el notebook — reemplazables por documentos de tu organismo |
| **Competencia de salida** | Integrar recuperación y generación (RAG) para responder preguntas públicas con citas y criterio, documentando el uso responsable |
| **Entregable** | Notebook reproducible en modo caché con las 3 celdas de chequeo en ✅ + ficha de uso responsable + demo del RAG |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En los capstones de R1 y R2 (si vienes de esas ramas) demostraste que puedes analizar datos y construir un modelo. Este capstone cierra otra puerta distinta: demostrar que puedes **armar un asistente de IA que responde con los documentos de tu servicio** — y que lo sabes hacer sin que invente cosas.

Piensa en las preguntas que llegan todos los días a una unidad de abastecimiento, a una oficina de partes o a un OIRS: *¿cuándo procede el trato directo?, ¿qué es un convenio marco?, ¿dónde se publican las licitaciones?* Las respuestas existen — están en la normativa, en resoluciones, en manuales internos — pero encontrarlas toma tiempo y la persona que las conoce no siempre está. Un **RAG** (Retrieval-Augmented Generation) resuelve exactamente eso: **primero busca** el documento pertinente y **después responde** basándose en él, citando la fuente.

La palabra clave es *citando*. Un chatbot que responde "de memoria" puede alucinar un artículo de ley que no existe — y en el Estado, una respuesta normativa inventada no es un chascarro: puede inducir a error a un proveedor, a un colega o a la ciudadanía. Por eso este capstone no evalúa solo que el sistema funcione: evalúa que sea **verificable** (corre sin red, en modo caché), **fundamentado** (responde con documentos citables) y **responsable** (con ficha de uso y supervisión humana declarada).

### ⚠️ Si usas documentos o datos de tu propio organismo — lee esto primero

El capstone te invita a reemplazar el corpus de ejemplo por documentos reales de tu servicio. Antes de hacerlo:

1. **Anonimiza los datos personales.** Elimina o reemplaza RUT, nombres, direcciones, correos, teléfonos y cualquier combinación que permita reidentificar a una persona, **antes** de pegar el texto en el notebook, enviarlo a un LLM externo (Gemini, ChatGPT, Claude…) o subirlo a GitHub. La Ley 19.628 (y su reforma) te obliga; el sentido común también. Recuerda lo visto en R3-02: en la capa gratuita, el proveedor puede usar tus textos para mejorar sus modelos.
2. **No subas nada sensible a repositorios públicos.** Lo que subes a GitHub o envías a una API queda fuera de tu control. Si dudas de si un documento es publicable, pide autorización a tu jefatura o encargado/a de datos.
3. **Si no puedes anonimizar con seguridad, usa el corpus de ejemplo.** La normativa de compras públicas es pública por definición; el aprendizaje es el mismo y el riesgo es cero.

Regla simple: si el texto no podría aparecer en Transparencia Activa tal como está, no entra ni al notebook, ni al LLM, ni a GitHub.

### 📎 La exigencia del curso: el asistente cita sus fuentes

Formación Pública tiene una regla no negociable para todo proyecto de IA de la rama R3: **la respuesta debe apoyarse en un documento recuperado y citable**. Si el sistema no puede señalar de dónde sacó lo que dice, la respuesta no se publica. Esa regla — *groundedness* — es tu principal defensa contra la alucinación, y es uno de los 5 criterios de la rúbrica.

---

## 3. Mapa conceptual del Capstone

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MINI-RAG RESPONSABLE PARA EL SECTOR PÚBLICO                                  │
├─────────────────────┬─────────────────────────────────────────────────────────┤
│ Pieza               │ Analogía con tu trabajo                                 │
├─────────────────────┼─────────────────────────────────────────────────────────┤
│ 1. CORPUS           │ El archivador de tu unidad: la normativa y los          │
│                     │ documentos oficiales donde SÍ está la respuesta         │
│ 2. RECUPERAR        │ El funcionario con memoria de elefante que sabe en      │
│    (la R de RAG)    │ qué carpeta está el documento que necesitas             │
│ 3. LLM EN MODO      │ Un dictáfono de prueba: siempre responde igual al       │
│    CACHÉ            │ mismo insumo, para que cualquiera pueda verificar       │
│ 4. RESPONDER CON    │ Redactar el oficio de respuesta CON el documento a la   │
│    CONTEXTO         │ vista, no "de memoria"                                  │
│ 5. FICHA DE USO     │ La resolución que autoriza un sistema: para qué sirve,  │
│    RESPONSABLE      │ qué cuesta, qué no puede hacer y quién lo supervisa     │
└─────────────────────┴─────────────────────────────────────────────────────────┘
```

**Lo que integra este capstone:**

| Módulo anterior | Habilidad que aplicas aquí |
|---|---|
| R3-00 Onramp express | Python básico, funciones, y el patrón **en vivo o caché** de `get_llm()` |
| R3-01 Introducción al NLP | Normalizar y tokenizar texto; el **solapamiento de palabras** que usa `recuperar` |
| R3-02 IA generativa y LLMs | Llamar a un LLM con un prompt bien armado; verificación y privacidad |
| R3-03 RAG | La arquitectura completa: recuperar → aumentar → generar, con grounding |
| R3-04 Agentes | La mirada de sistema: tu RAG podría ser una herramienta más de un agente, con traza y guardrails |

---

## 4. Antes de empezar: Verificación de prerrequisitos

### ¿Qué necesito saber?

Checklist de verificación — responde honestamente:

| ¿Puedo…? | Módulo donde lo viste | ¿OK? |
|---|---|---|
| Escribir una función en Python que reciba parámetros y retorne un valor | R3-00 | ☐ |
| Explicar el patrón "en vivo o caché" y por qué el curso lo usa | R3-00 / R3-02 | ☐ |
| Pasar un texto a minúsculas y separarlo en palabras (`.lower()`, `.split()`) | R3-01 | ☐ |
| Explicar qué es un *prompt* y armar uno con un f-string | R3-02 | ☐ |
| Describir las tres piezas de un RAG: recuperar → aumentar → generar | R3-03 | ☐ |
| Explicar qué es una alucinación y por qué la cita de fuente la combate | R3-02 / R3-03 | ☐ |
| Usar `max()` con `key=` para elegir el mejor elemento de una lista | R3-00 / R3-03 | ☐ |

Si alguna casilla queda vacía, vuelve al módulo correspondiente antes de empezar. Un capstone se construye sobre terreno firme, no sobre memoria frágil.

### Configuración del entorno

Abre `leccion.ipynb` en Google Colab y ejecuta la primera celda. Debe imprimir `Corpus: 4 documentos | get_llm en modo cache`. No necesitas API key, ni conexión a un LLM, ni instalar nada: todo el capstone es verificable **offline**. Si quieres la versión con Gemini en vivo, el camino está en R3-00 y R3-02 (`GEMINI_API_KEY` en los Secrets de Colab) — pero es opcional y **no** lo exige la rúbrica.

### Conoce el corpus de ejemplo

El corpus son **4 documentos** (frases de normativa de compras públicas) definidos en la lista `CORPUS`:

| # | Tema del documento |
|---|---|
| 0 | Las licitaciones públicas: se rigen por la ley de compras y se publican en MercadoPúblico |
| 1 | El convenio marco: comprar a proveedores preacordados sin licitación |
| 2 | El trato directo: excepcional, requiere justificación formal documentada |
| 3 | Los proveedores del Estado: clasificación por tamaño (micro, pequeña, mediana, grande) |

Es deliberadamente chico: el objetivo del capstone es que domines el **mecanismo** de punta a punta. En tu proyecto real, cada elemento de la lista será un fragmento de los documentos de tu organismo.

---

## 5. Guía paso a paso por sección del notebook

---

### Sección 0 · Corpus y `get_llm()` en modo caché

🎯 **Objetivo:** Entender las dos piezas que el notebook te regala: el corpus de documentos y un LLM simulado.

💡 **Concepto clave:** `get_llm()` devuelve una función que **no** llama a Gemini ni a la red: ante cualquier prompt, responde con un texto fijo construido a partir del propio prompt. Eso la hace **determinista**: mismo prompt → misma salida, siempre. ¿Para qué sirve un LLM "de mentira"? Para lo mismo que sirve un simulacro de evacuación: practicar y **verificar el procedimiento completo** sin depender de condiciones externas (red, API key, cuota). El día que conectes el LLM real, solo cambias esa función — el resto del sistema ya está probado.

🔍 **Qué hace el código:** define la lista `CORPUS` (4 strings) y la función `get_llm()`, que retorna una función interna `generar(prompt)` que devuelve un texto que empieza con `"Respuesta (modo cache, sin LLM real)..."` seguido de los primeros 160 caracteres del prompt.

⚠️ **Error frecuente:** Pensar que el modo caché es "trampa" o que el capstone vale menos por no usar un LLM en vivo. Es al revés: la rúbrica **exige** que el notebook corra sin red, porque en el Estado un sistema que nadie puede verificar de forma reproducible no debería aprobarse.

✅ **Sabes esta sección cuando puedes:** Explicarle a un colega por qué un evaluador puede confiar en tu notebook aunque no tenga internet.

---

### Sección 1 · Recuperación (la R de RAG)

🎯 **Objetivo:** Escribir `recuperar(pregunta, corpus)`: la función que encuentra el documento más relevante para una pregunta.

💡 **Concepto clave:** Antes de responder, un RAG **busca**. La versión de este capstone usa la técnica más simple posible, heredada de R3-01: contar cuántas **palabras en común** tiene la pregunta con cada documento (solapamiento) y quedarse con el que más comparte. Es como cuando llega una consulta a tu oficina y alguien dice "eso está en la circular del convenio marco": la palabra clave te lleva a la carpeta correcta.

🔍 **Qué hace el código de la sección:** la primera línea convierte la pregunta en un conjunto de palabras (`set(pregunta.lower().split())`) — minúsculas para que "Convenio" y "convenio" cuenten igual, `set` para poder intersectar. El `TODO` te pide devolver el documento del corpus con mayor solapamiento. Después se prueba con `"¿que es el convenio marco?"` y debería imprimir el documento del convenio marco.

⚠️ **Error frecuente:** Devolver el **número** de palabras en común (el score) en vez del **documento**. La celda de chequeo espera un string que esté dentro de `CORPUS`. Otro clásico: olvidar el `.lower()` al comparar, con lo que las mayúsculas rompen el solapamiento.

✅ **Sabes esta sección cuando puedes:** Predecir, sin ejecutar, qué documento devolvería `recuperar` para "¿cómo se clasifican los proveedores?" — y explicar por qué.

---

### Sección 2 · El LLM en modo caché (determinista)

🎯 **Objetivo:** Comprobar empíricamente que el LLM-caché es determinista.

💡 **Concepto clave:** **Determinismo** = mismo insumo, misma salida. Los LLM reales son *estocásticos* (la misma pregunta puede dar respuestas distintas, lo viste con la temperatura en R3-02); eso los hace difíciles de auditar. El modo caché elimina esa variabilidad para que la evaluación del capstone sea justa y reproducible: cualquier persona que corra tu notebook verá exactamente lo mismo que tú.

🔍 **Qué hace el código:** obtiene el LLM con `llm = get_llm()`, y el `TODO` te pide llamarlo **dos veces con el mismo prompt**, guardando los resultados en `a` y `b`. La línea `es_determinista = (a == b)` compara ambas salidas; debería imprimir `determinista: True | tipo: str`.

⚠️ **Error frecuente:** Llamar a `llm` con **dos prompts distintos** y sorprenderte de que `a != b`. La prueba de determinismo exige el mismo texto exacto en ambas llamadas. También: dejar `a = llm` (sin paréntesis ni argumento) — eso guarda la función, no su respuesta.

✅ **Sabes esta sección cuando puedes:** Explicar la diferencia entre un sistema determinista y uno estocástico, y por qué el primero facilita la auditoría en el Estado.

---

### Sección 3 · Responder con contexto (RAG completo)

🎯 **Objetivo:** Escribir `responder(pregunta, llm)`: unir recuperación y generación en un RAG funcional.

💡 **Concepto clave:** Esta es la esencia del RAG y la lección central de R3-03: **el LLM no responde de memoria, responde con el documento a la vista**. La función primero recupera el documento relevante (`doc = recuperar(pregunta)`) y luego arma un prompt que incluye ese documento como **contexto** junto con la pregunta. Es la diferencia entre un examen de memoria y un examen con libro abierto: en el segundo, la respuesta se puede rastrear hasta la página exacta.

🔍 **Qué hace el código:** la primera línea ya está escrita (la recuperación). El `TODO` te pide construir el `prompt` combinando `doc` y `pregunta` en un solo texto, y retornar `llm(prompt)`. La celda de prueba consulta `"¿cuando se usa el trato directo?"` y, como el LLM está en modo caché, verás la respuesta simulada que incluye el inicio de tu prompt — ahí puedes comprobar a ojo que el contexto viajó dentro.

⚠️ **Error frecuente:** Pasar al LLM **solo la pregunta**, sin el documento. El chequeo puede no detectarlo (verifica que la respuesta sea un string no vacío), pero tu RAG quedaría cojo: sin contexto no hay grounding, y sin grounding tu proyecto no cumple la rúbrica. Revisa la salida impresa: si no ves rastro del documento en el prompt, corrígelo aunque tengas el ✅.

✅ **Sabes esta sección cuando puedes:** Dibujar en una servilleta el flujo pregunta → recuperar → prompt con contexto → LLM → respuesta, y decir qué pieza falla si la respuesta sale inventada.

---

### Sección 4 · Ficha de uso responsable

🎯 **Objetivo:** Completar la ficha que acompaña a toda solución de IA en el Estado.

💡 **Concepto clave:** Así como el capstone de R2 exige una *model card*, este exige una **ficha de uso responsable**. Es el documento que le dice a tu jefatura — y a cualquier auditor — bajo qué condiciones el sistema puede operar. La ficha del notebook tiene 5 campos:

| Campo | Qué declaras |
|---|---|
| **Uso previsto** | Qué pregunta responde el asistente y para quién |
| **Costo** | Proveedor con capa gratuita (Gemini) + patrón en vivo o caché; estimación de tokens por consulta |
| **Privacidad** | Los datos de compras son públicos; **no** se envían datos personales/sensibles a un LLM externo |
| **Verificabilidad (groundedness)** | La respuesta **cita** el documento recuperado; sin fuente, no se publica |
| **Supervisión humana** | Un funcionario revisa antes de cualquier decisión; el LLM **no decide** |

⚠️ **Error frecuente:** Llenar la ficha con generalidades ("se usará con responsabilidad"). Sé concreto: *el asistente responde consultas sobre normativa de compras para la unidad de abastecimiento; corpus de 4 documentos públicos; toda respuesta indica su documento fuente; las respuestas son insumo para un funcionario, nunca respuesta automática a terceros.* Una ficha vaga es una ficha que no protege a nadie.

✅ **Sabes esta sección cuando puedes:** Entregarle la ficha a alguien que no vio el código y que esa persona sepa qué puede esperar del sistema, qué no, y quién responde por él.

---

## 6. Guía de los 3 Ejercicios del Notebook

---

### Ejercicio 1 · Escribe `recuperar`

**Objetivo:** Completar la función que devuelve el documento del corpus con mayor solapamiento de palabras con la pregunta.

**Habilidad que entrena:** Recuperación léxica — el corazón de la "R" de RAG (R3-01 + R3-03).

**Pistas progresivas:**

- 🟢 **Pista suave:** Ya tienes `palabras` (el conjunto de palabras de la pregunta). Para cada documento puedes armar el mismo conjunto y preguntarte: ¿cuántas palabras comparten? El documento ganador es el que maximiza esa cuenta.
- 🟡 **Pista media:** La intersección de dos conjuntos en Python se escribe con `&`, y su tamaño con `len(...)`. Y para elegir "el elemento de una lista que maximiza algo" existe `max(lista, key=...)`, que ya usaste en R3-03.
- 🔴 **Pista directa:** Es una sola línea: `max` sobre `corpus`, cuyo `key` es una función `lambda` que recibe un documento, lo pasa a minúsculas, lo separa en palabras, lo convierte en conjunto, lo intersecta con `palabras` y mide el largo de esa intersección. Devuelve el resultado del `max`.

**Lógica de la solución:** Cada documento se convierte al mismo "idioma" que la pregunta (minúsculas, palabras sueltas, conjunto) para poder medir cuánto se parecen. `max` con `key` recorre el corpus y retorna el documento — no el puntaje — cuyo solapamiento es mayor.

**Qué significa el ✅:** La celda verifica que `recuperar("¿que es el convenio marco?")` devuelva un elemento de `CORPUS` y que ese elemento contenga la palabra "convenio". Es decir: que devuelves un documento real y que es el correcto.

---

### Ejercicio 2 · Comprueba que el LLM-caché es determinista

**Objetivo:** Llamar dos veces al LLM con el mismo prompt y verificar que ambas respuestas son idénticas.

**Habilidad que entrena:** Pensar en reproducibilidad — la condición que hace verificable todo el capstone (R3-00 / R3-02).

**Pistas progresivas:**

- 🟢 **Pista suave:** `llm` ya está creado y es una función: se usa como cualquier otra, pasándole un texto. Necesitas dos llamadas… ¿con qué relación entre sus argumentos?
- 🟡 **Pista media:** `a` y `b` deben guardar el **resultado** de llamar a `llm` con **exactamente el mismo** string de prompt (el contenido da lo mismo; la igualdad importa).
- 🔴 **Pista directa:** Escribe dos líneas casi idénticas: en la primera asigna a `a` el resultado de `llm(...)` con un prompt cualquiera; en la segunda asigna a `b` el resultado de `llm(...)` con ese mismo prompt, carácter por carácter.

**Lógica de la solución:** Si el LLM es determinista, dos llamadas idénticas producen strings idénticos y `a == b` es `True`. Con un LLM real en vivo este experimento podría fallar — y esa diferencia es justamente lo que el ejercicio te hace tocar con las manos.

**Qué significa el ✅:** La celda verifica que `es_determinista` sea verdadero y que `a` sea un string no vacío: hiciste llamadas reales (no guardaste la función) y comprobaste el determinismo.

---

### Ejercicio 3 · Escribe `responder`

**Objetivo:** Armar el prompt con el documento recuperado como contexto y pasárselo al LLM.

**Habilidad que entrena:** Aumentación — la "A" de RAG: inyectar conocimiento propio en el prompt (R3-02 + R3-03).

**Pistas progresivas:**

- 🟢 **Pista suave:** Ya tienes `doc` (el documento recuperado) y `pregunta`. El prompt debe ser **un solo texto** donde el LLM pueda distinguir qué parte es contexto y qué parte es la pregunta.
- 🟡 **Pista media:** Un f-string resuelve la combinación: algo con la forma "Contexto: … Pregunta: …", interpolando `doc` y `pregunta` donde corresponde. Luego retorna lo que el LLM responda a ese prompt.
- 🔴 **Pista directa:** Dos pasos: (1) asigna a `prompt` un f-string que etiquete primero el contexto (el contenido de `doc`) y después la pregunta (el contenido de `pregunta`); (2) en el `return`, llama a `llm` pasándole `prompt`.

**Lógica de la solución:** El prompt aumentado le entrega al LLM la evidencia antes de pedirle la respuesta. Con el LLM-caché, la salida repite el inicio de tu prompt, así que puedes **ver** el contexto viajando dentro — tu comprobación visual de que hay grounding.

**Qué significa el ✅:** La celda verifica que `responder("¿cuando se usa el trato directo?", get_llm())` devuelva un string no vacío y que la recuperación para esa pregunta encuentre el documento del trato directo. Ojo: el chequeo no puede leer tu mente — asegúrate tú de que el documento realmente esté dentro del prompt (mira la salida impresa).

---

## 7. Sección especial: un asistente de IA como decisión de política pública

Un RAG en el Estado nunca es solo técnica. Antes de dar por cerrado tu capstone, trabaja estas reflexiones:

### Reflexión guiada

1. **¿Qué pasa si el asistente responde mal una consulta normativa?** Si un proveedor pequeño pregunta por el trato directo y recibe una respuesta inventada, puede presentar mal una justificación y perder una venta legítima. Por eso la regla "sin fuente, no se publica" no es purismo académico: es protección de derechos.
2. **El corpus define lo que el sistema "sabe" — y lo que no.** Tu RAG de 4 documentos no puede responder sobre garantías ni plazos, porque no están en el corpus. Un corpus incompleto produce respuestas incompletas con tono seguro. ¿Quién decide qué documentos entran? Esa es una decisión editorial con consecuencias públicas.
3. **¿Quién supervisa y quién responde?** La ficha declara que el LLM no decide. En la práctica: ¿qué funcionario revisa las respuestas?, ¿queda registro (traza, como viste en R3-04)?, ¿qué pasa cuando el humano y el sistema discrepan? Si no puedes responder esto, el sistema no está listo para operar.

### Documentos que fortalecerían el corpus

La ley de compras completa y su reglamento (no solo resúmenes), dictámenes de Contraloría sobre trato directo (la interpretación oficial de los casos difíciles), y las preguntas frecuentes reales de tu OIRS (para que el corpus cubra lo que la gente de verdad pregunta, no lo que creemos que pregunta).

### Pregunta de debate

> Tu jefatura quiere publicar el asistente en la web institucional para que la ciudadanía consulte directamente, sin revisión humana intermedia: "si cita la fuente, ¿qué puede salir mal?". ¿Qué le responderías, considerando el fallback cuando no hay documento relevante, la calidad del corpus y quién asume el costo de un error? ¿Hay un punto medio entre "solo uso interno" y "abierto a todo público"?

---

## 8. Rúbrica de evaluación — cómo interpretar cada criterio

El notebook cierra con una rúbrica de 5 criterios. Así se lee cada uno:

| Criterio | ✅ Cumple | ❌ No cumple |
|---|---|---|
| **Utilidad pública** | El asistente resuelve una pregunta real de gestión, identificable y con destinatario claro | Un demo genérico sin caso de uso ("un chatbot que responde cosas") |
| **Groundedness / citas** | La respuesta se apoya en un documento recuperado y citable; se puede rastrear qué fuente sustenta qué respuesta | Respuestas "de memoria" del LLM, sin documento asociado |
| **Costo / privacidad** | Usa capa gratuita (Gemini) o modo caché; ningún dato personal o sensible viaja a un LLM externo ni a GitHub | Datos sin anonimizar en el corpus, el prompt o el repositorio |
| **Reproducibilidad** | `Runtime > Run all` corre de principio a fin **sin red** (modo caché) y las 3 celdas de chequeo muestran ✅ | Celdas que fallan, dependen de una API key o requieren intervención manual |
| **Uso responsable** | La ficha está completa y concreta, y declara la supervisión humana: el LLM no decide | Ficha vacía, genérica, o un sistema que responde a terceros sin revisión |

> **Entregable completo:** notebook reproducible (modo caché) + ficha de uso responsable + demo del RAG.

---

## 9. Conexión con `profundiza.ipynb` — hacia un RAG confiable

| Aspecto | `leccion.ipynb` | `profundiza.ipynb` 🔬 |
|---|---|---|
| **Enfoque** | El mecanismo: recuperar → LLM caché → responder con contexto → ficha | La confiabilidad: medir relevancia, citar la fuente, no alucinar |
| **Ejercicios** | 3 con chequeo automático | 3 con chequeo automático |
| **Obligatorio** | ✅ Sí — es el entregable del capstone | ☐ Opcional, muy recomendado |

El `profundiza` agrega las tres piezas que convierten tu demo en algo defendible ante un auditor: un **score de relevancia** explícito (¿cuánto confío en lo recuperado?), una función `responder_con_cita` que devuelve la respuesta **junto al índice y texto de su fuente** (la cita deja de ser promesa y pasa a ser dato), y `recuperar_robusto` con **umbral y fallback**: si ningún documento alcanza relevancia mínima, devuelve `None` — es más honesto no responder que inventar. Si piensas usar tu capstone con documentos reales de tu organismo, estas tres piezas no son opcionales en espíritu: son la diferencia entre un juguete y una herramienta.

---

## 10. Autoevaluación Final

Responde estas preguntas antes de dar por terminado el capstone:

**1. ¿Por qué el capstone usa `get_llm()` en modo caché en vez de un LLM en vivo?**

- a) Porque los LLM en vivo son ilegales en el Estado
- b) Porque el modo caché responde mejor que Gemini
- c) Para que el notebook sea determinista y verificable sin red: cualquiera puede reproducir exactamente el mismo resultado ✅
- d) Porque Google cobra por cada ejecución del notebook

*Respuesta correcta: c) — La reproducibilidad es un criterio de la rúbrica. Un evaluador (o un auditor) debe poder correr tu proyecto de principio a fin sin depender de una API key, de la red ni del azar del modelo. El LLM en vivo es un paso posterior (R3-00/R3-02), no un requisito.*

---

**2. En la función `responder`, ¿qué papel juega el documento recuperado?**

- a) Se usa solo para validar que el corpus no esté vacío
- b) Se inyecta en el prompt como contexto, para que el LLM responda basándose en él y no de memoria ✅
- c) Reemplaza a la pregunta del usuario
- d) Se guarda en un archivo de respaldo

*Respuesta correcta: b) — Es la esencia del RAG: recuperar → aumentar → generar. El documento viaja dentro del prompt y la respuesta queda anclada (grounded) a una fuente rastreable, en vez de depender de lo que el modelo "recuerda".*

---

**3. ¿Por qué el curso exige que el asistente cite sus fuentes?**

- a) Por formalidad académica: las citas dan apariencia seria
- b) Porque sin cita el texto no se puede indexar en MercadoPúblico
- c) Porque la cita permite verificar la respuesta contra el documento original: es la defensa concreta contra la alucinación ✅
- d) Porque los LLM no funcionan sin citas

*Respuesta correcta: c) — Un LLM optimiza plausibilidad, no verdad (lo viste en el profundiza de R3-02). La cita convierte cada respuesta en algo auditable: si el documento no dice lo que la respuesta afirma, el error se detecta. De ahí la regla: sin fuente, no se publica.*

---

**4. Quieres usar el capstone con documentos de tu organismo que incluyen nombres y RUT de personas. ¿Qué corresponde hacer?**

- a) Usarlos igual: la capa gratuita de Gemini es privada
- b) Anonimizar los datos personales antes de ponerlos en el corpus, enviarlos a un LLM o subirlos a GitHub — y si no es posible, usar el corpus de ejemplo ✅
- c) Subirlos a un repositorio privado de GitHub, con eso basta para enviarlos al LLM
- d) Pedirle al LLM que ignore los datos personales

*Respuesta correcta: b) — Lo que envías a un LLM externo o subes a un repositorio queda fuera de tu control, y en la capa gratuita el proveedor puede usar los textos. La Ley 19.628 protege los datos personales: se anonimiza antes, no después. Si no puedes anonimizar con seguridad, el corpus de ejemplo enseña lo mismo con riesgo cero.*

---

**5. La ficha de uso responsable declara "supervisión humana". ¿Qué significa en la práctica?**

- a) Que un funcionario revisa las respuestas antes de cualquier decisión: el LLM propone, no decide ✅
- b) Que el LLM fue entrenado por humanos
- c) Que el sistema solo funciona en horario de oficina
- d) Que hay un humano disponible por si el servidor se cae

*Respuesta correcta: a) — En el Estado, las decisiones que afectan a personas las toman (y las firman) funcionarios, no modelos. El asistente acelera la búsqueda y el borrador; la responsabilidad no se delega. Por eso la ficha lo declara explícitamente y la rúbrica lo evalúa.*

---

## 11. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **RAG** | Recuperar documentos relevantes y responder basándose en ellos | Contestar un oficio con el expediente a la vista |
| **Corpus** | El conjunto de documentos donde el sistema busca | El archivador oficial de tu unidad |
| **Recuperación** | Encontrar el documento más relevante para una pregunta | El colega que sabe en qué carpeta está cada cosa |
| **Solapamiento de palabras** | Contar cuántas palabras comparten pregunta y documento | Buscar por palabras clave en el gestor documental |
| **LLM** | Modelo de lenguaje que genera texto a partir de un prompt | Un redactor veloz que necesita instrucciones y evidencia |
| **Prompt** | La instrucción + contexto que recibe el LLM | El memo que le entregas al redactor: antecedentes y encargo |
| **Modo caché** | El LLM simulado que responde sin red, siempre igual | Un simulacro: se practica el procedimiento completo sin riesgo |
| **Determinista** | Mismo insumo → misma salida, siempre | Un formulario que calcula igual para todos los casos iguales |
| **Grounding / groundedness** | La respuesta se ancla en un documento citable | Todo informe indica su fuente; sin respaldo, no se firma |
| **Alucinación** | El LLM afirma con seguridad algo falso o inventado | Citar de memoria un artículo de ley… que no existe |
| **Umbral / fallback** | Si nada es suficientemente relevante, no se responde | "No tenemos ese antecedente" en vez de inventar la respuesta |
| **Ficha de uso responsable** | Documento con uso previsto, costo, privacidad y supervisión | La resolución que autoriza y acota un sistema institucional |

---

## 12. Has llegado al final de la Rama R3 🎓

Si completaste este capstone con las 3 celdas en ✅, una ficha de uso responsable concreta y un notebook que corre de punta a punta sin red, demostraste algo que muy pocos equipos públicos pueden mostrar: **sabes construir un asistente de IA fundamentado, verificable y con supervisión humana declarada**.

### Certificación

Al aprobar el capstone según la rúbrica de 5 criterios, obtienes la certificación de la rama R3: **Especialista en IA aplicada del sector público** de Formación Pública. No es un diploma de asistencia: certifica un proyecto real, evaluado con rúbrica, que cualquiera puede abrir, ejecutar y revisar.

### Tu portafolio es tu credencial

Sube tu capstone a GitHub (recuerda: **solo con el corpus de ejemplo o con documentos anonimizados y publicables**). Un repositorio con un RAG reproducible, su ficha de uso responsable y — si hiciste el profundiza — citas de fuente y fallback anti-alucinación, es evidencia verificable de una competencia que hoy escasea en el Estado. Vale más que cualquier línea en un currículum: no es promesa, es código que corre.

### ¿Qué sigue?

| Opción | Para quién | Qué encontrarás |
|---|---|---|
| **Rama R1 · Análisis y Visualización** | Aún no la tomas y quieres la base de datos tabulares | pandas, gráficos y un capstone de análisis sobre datos públicos |
| **Rama R2 · Científico de Datos** | Quieres modelos predictivos, no solo asistentes de texto | scikit-learn, evaluación honesta y una model card de verdad |
| **Comunidad Formación Pública** | Quieres seguir aprendiendo con otros funcionarios | Comparte tu capstone, revisa los de otros, encuentra aliados en otros servicios |
| **Llevarlo a tu servicio** | Quieres que este RAG deje de ser ejercicio | Amplía el corpus con documentos reales (anonimizados), conecta el LLM en vivo (R3-00/R3-02) y formaliza la ficha con tu jefatura |

**Pregunta motivadora para lo que sigue:** Tu mini-RAG responde con 4 documentos. En tu servicio hay miles: oficios, resoluciones, manuales, dictámenes. ¿Cuál sería el primer corpus que armarías, quién lo curaría, y qué pregunta de la ciudadanía — de esas que hoy demoran días — podría responderse en segundos, con fuente citada y un funcionario supervisando?

---

*Formación Pública Chile · Licencia CC BY 4.0*
