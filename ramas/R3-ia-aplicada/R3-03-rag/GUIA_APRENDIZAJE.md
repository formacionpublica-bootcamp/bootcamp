# Guía de Aprendizaje — R3-03 · RAG: tu asistente de trámites que cita la fuente

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · IA Aplicada · Módulo 3 · Semana 4

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-03 · RAG: tu asistente de trámites que cita la fuente |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas (lección) + 1 hora (profundización opcional) |
| **Nivel** | Intermedio — requiere R3-01 (TF-IDF) y R3-02 (`preguntar_llm`) |
| **Prerrequisitos** | Funciones en Python, DataFrames, TF-IDF y similitud, qué es un prompt |
| **Competencia de salida** | Construir un asistente de preguntas y respuestas sobre documentos públicos que **cita la fuente**, **se abstiene** cuando no sabe y se **evalúa** con evidencia (hit@k) |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `fichas.csv` — 245 fichas de trámites de ChileAtiende con texto completo (18 temas, 64 instituciones, mediana de 435 palabras por ficha, 244 de ellas organizadas en secciones `## `) |
| **LLM** | `preguntar_llm()` (Gemini, modelo `gemini-3.5-flash-lite` por defecto). **Opcional:** sin `GEMINI_API_KEY` devuelve un respaldo extractivo y todo funciona igual |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Todos los días llegan a una ventanilla, a un correo o a un call center preguntas como «¿cómo me afilio a Fonasa?», «¿cuándo pagan el aguinaldo a los pensionados?» o «¿cómo saco el certificado de antecedentes?». La respuesta casi siempre **ya está escrita** en algún documento oficial; el problema es encontrarla rápido y citarla bien.

Un LLM solo no sirve para esto: responde de memoria y, cuando no sabe, **inventa con seguridad** una lista de requisitos verosímil y equivocada. En el Estado, eso puede significar a una persona que pierde un viaje, un plazo o un beneficio. **RAG** (*Retrieval-Augmented Generation*) cambia el juego: primero **busca** en tus documentos los trozos relevantes, se los entrega al modelo con la instrucción de responder **solo con eso**, y devuelve la respuesta **con la cita** (id y url de la ficha) para que cualquiera la verifique.

En este módulo construyes ese asistente sobre las **245 fichas reales de ChileAtiende**, y aprendes las dos cosas que separan una demo de una herramienta confiable: **abstenerse** cuando la respuesta no está, y **medir** con preguntas reales si la búsqueda encuentra la ficha correcta. La misma receta sirve para el reglamento interno de tu servicio, las bases tipo de tu unidad o las preguntas frecuentes de tu OIRS.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Analogía en la oficina |
|----------|-----------|------------------------|
| **RAG** | Recuperar → aumentar el prompt → generar | Responder un oficio con el expediente abierto sobre la mesa |
| **Trocear (*chunking*)** | Partir cada ficha por sus secciones `## ` y, si una sección es larga, en trozos de ≤120 palabras | Separar el expediente en fojas para encontrar la página exacta |
| **Cita** | Cada trozo conserva `id`, `titulo` y `url` de su ficha | El número de folio que acompaña cada antecedente |
| **TF-IDF** | Vector de pesos: palabras frecuentes en el trozo y raras en el corpus pesan más | Un índice temático que destaca lo distintivo de cada página |
| **Similitud coseno** | Puntaje 0–1 entre pregunta y trozo (`X @ q.T`) | Cuánto se parece la consulta a cada foja |
| **Top-k** | Los `k` trozos con mayor puntaje | Las 3 fojas que sacas del archivador |
| **Prompt aumentado** | Instrucción + trozos con cita + pregunta | El memo con antecedentes adjuntos y la orden «responda en base a lo adjunto» |
| **`NO_ENCONTRADO`** | Salida pactada para la abstención | El timbre «no consta en los antecedentes» |
| **Umbral** | Si el mejor puntaje es bajo, ni se llama al LLM | No redactar respuesta si el archivador no tiene nada parecido |
| **hit@k** | Fracción de preguntas cuya ficha correcta aparece en los `k` primeros | La tasa de aciertos del funcionario de partes |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué mide TF-IDF y para qué sirve la similitud coseno (R3-01) | ☐ |
| Recorrer un DataFrame con `itertuples()` y armar otro desde una lista de diccionarios | ☐ |
| Usar `preguntar_llm(prompt, respaldo=...)` y explicar qué pasa sin clave (R3-02) | ☐ |
| Explicar qué es una alucinación y por qué es grave en un servicio público | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación y el LLM

🎯 **Objetivo:** Cargar `fichas.csv` (245 fichas, 18 temas, 64 instituciones, mediana de 435 palabras) y definir `preguntar_llm`.

💡 **Concepto clave:** `preguntar_llm` es la misma de R3-02: con `GEMINI_API_KEY` en los Secretos de Colab habla con Gemini; sin ella devuelve el `respaldo`. **No necesitas clave**: los 6 chequeos se diseñaron para no depender de lo que diga el modelo.

---

### Sección 1 · Trocear

🎯 **Objetivo:** Completar la regla de corte de `trocear` y construir la tabla `trozos`.

💡 **Concepto clave:** 244 de las 245 fichas vienen organizadas en secciones con subtítulo (`## Requisitos`, `## Costo`, `## Trámite en línea`…), unas 4 por ficha: la sección es la unidad natural de corte. Como algunas secciones son largas, la regla combina dos criterios: cortar en cada subtítulo **o** cuando el trozo pasaría de 120 palabras (las líneas en blanco se saltan). Resultado: **1.656 trozos**, mediana de 6 por ficha. Cada trozo hereda `id`, `titulo` y `url`: sin eso no hay cita posible.

⚠️ **Error frecuente:** Olvidar el `actual and ...` de la condición: se generan trozos vacíos al inicio.

---

### Sección 2 · Indexar

🎯 **Objetivo:** Vectorizar los trozos con `TfidfVectorizer(strip_accents="unicode", stop_words=STOPWORDS)`.

💡 **Concepto clave:** A cada trozo se le **antepone el título** de su ficha. «Presenta tu cédula en la sucursal» no dice de qué trámite habla; con el título adelante, sí. La matriz queda de 1.656 trozos × 7.076 palabras. En la profundización mides cuánto aporta ese título (mucho).

---

### Sección 3 · Recuperar

🎯 **Objetivo:** Escribir `recuperar(pregunta, k)` que devuelve los `k` trozos más parecidos con su puntaje.

💡 **Concepto clave:** La pregunta se transforma con el **mismo** vectorizador (`transform`, nunca otro `fit`). Para «¿Cómo me afilio a Fonasa?» los tres trozos recuperados son de la ficha 9715 «Afiliación a Fonasa» (el primero con puntaje 0,43).

✅ **Señal de que entendiste:** Puedes explicar por qué `X @ q.T` ya es la similitud coseno (TF-IDF normaliza los vectores).

---

### Sección 4 · Aumentar con citas

🎯 **Objetivo:** `armar_prompt` con tres ingredientes: trozos etiquetados `[Ficha id · url]`, la instrucción de usar **SOLO** los documentos y citar, y la salida pactada `NO_ENCONTRADO`.

💡 **Concepto clave:** Pactar una palabra exacta para la abstención permite que el **código** la detecte, en vez de interpretar frases como «lamentablemente no cuento con…».

---

### Sección 5 · Generar o abstenerse

🎯 **Objetivo:** Dos barreras en `responder`: (1) si el mejor puntaje < `UMBRAL` (0,15) se abstiene **sin llamar al LLM**; (2) si el LLM devuelve `NO_ENCONTRADO`, también.

💡 **Concepto clave:** `llm=preguntar_llm` es un **parámetro**: el chequeo prueba la función con LLM «falsos» (uno que responde, uno que dice `NO_ENCONTRADO`, uno que explota si lo llamas). Así se prueba software con IA sin depender de la red.

⚠️ **El límite real:** la celda siguiente muestra los puntajes de tres preguntas ajenas al corpus. «¿Cómo se prepara una empanada de pino?» da 0,00 (bajo el umbral: abstención). Pero «¿Quién ganó la Copa América 2015?» pasa con 0,24 por coincidencias sueltas, y «¿Cuál es la **capital** de Francia?» da **0,43** porque la ficha «Capital Abeja Emprende» contiene la palabra *capital*. Y al revés, una pregunta legítima —«¿Cómo obtengo la tarjeta de alimentación para la universidad?»— queda bajo el umbral (0,15). La búsqueda léxica compara palabras, no significados, y el umbral es un compromiso: por eso existen la barrera 2, la cita visible y la revisión humana.

---

### Sección 6 · Evaluar con hit@k

🎯 **Objetivo:** Escribir `hit_at_k` y medir con 20 preguntas redactadas como las haría la ciudadanía, cada una con su ficha esperada.

💡 **Concepto clave:** Resultado de la lección: **hit@1 = 0,50** y **hit@3 = 0,85**. Las 3 preguntas que fallan en hit@3 son brechas de **vocabulario**: «pescar» vs «pesca recreativa», «carnet» vs «cédula de identidad», «divorciarme» vs «divorcio».

✅ **Señal de que entendiste:** Puedes explicar por qué hit@3 importa más que hit@1 en un RAG (el LLM ve los 3 trozos).

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Completa la regla de corte de `trocear`

- 🟢 Pista suave: Hay que cerrar el trozo solo si ya tiene algo, y por una de dos razones.
- 🟡 Pista media: `linea.startswith("## ")` detecta el subtítulo; `n + palabras > max_palabras`, el exceso.
- 🔴 Pista directa: `if actual and (linea.startswith("## ") or n + palabras > max_palabras):`

**¿Qué significa el ✅?** Que los subtítulos abren trozo, ningún trozo pasa de 120 palabras, no hay trozos vacíos y las 245 fichas quedaron troceadas.

### Ejercicio 2 — Construye el vectorizador y la matriz `X`

- 🟢 Pista suave: Son dos líneas: crear el objeto y ajustarlo a `documentos`.
- 🟡 Pista media: `TfidfVectorizer(...)` con `strip_accents` y `stop_words`; luego `.fit_transform`.
- 🔴 Pista directa: `vectorizador = TfidfVectorizer(strip_accents="unicode", stop_words=STOPWORDS)` y `X = vectorizador.fit_transform(documentos)`.

**¿Qué significa el ✅?** Una fila por trozo, «fonasa» en el vocabulario y las stopwords fuera.

### Ejercicio 3 — Completa `recuperar`

- 🟢 Pista suave: Multiplica la matriz por el vector de la pregunta y ordena.
- 🟡 Pista media: `(X @ q.T).toarray().ravel()` da un puntaje por trozo; `np.argsort(-puntajes)` ordena de mayor a menor.
- 🔴 Pista directa: `puntajes = (X @ q.T).toarray().ravel()` y `mejores = np.argsort(-puntajes, kind="stable")[:k]`.

**¿Qué significa el ✅?** Fonasa recupera primero la ficha 9715, el orden es descendente y `k` controla cuántos trozos vuelven.

### Ejercicio 4 — Escribe `armar_prompt`

- 🟢 Pista suave: Primero arma un bloque de texto por trozo, con su etiqueta de cita.
- 🟡 Pista media: `[f"[Ficha {r.id} · {r.url}]\n{r.texto}" for r in contexto.itertuples()]` y únelos con `"\n\n".join(...)`.
- 🔴 Pista directa: Concatena la instrucción (SOLO + citar + `NO_ENCONTRADO`), `"Documentos:\n"` + bloques y `f"Pregunta: {pregunta}\nRespuesta:"`.

**¿Qué significa el ✅?** El prompt trae cada url, cada texto, la pregunta, la palabra «solo» y `NO_ENCONTRADO`.

### Ejercicio 5 — Implementa las dos barreras en `responder`

- 🟢 Pista suave: Ambas barreras devuelven exactamente lo mismo: `{"respuesta": NO_SE, "fuentes": []}`.
- 🟡 Pista media: Barrera 1 antes de llamar al LLM (mira `contexto["puntaje"].iloc[0]`); barrera 2 después (mira `texto`).
- 🔴 Pista directa: `if contexto["puntaje"].iloc[0] < UMBRAL: return {"respuesta": NO_SE, "fuentes": []}` y `if "NO_ENCONTRADO" in texto: return {"respuesta": NO_SE, "fuentes": []}`.

**¿Qué significa el ✅?** Con contexto relevante responde y cita la ficha 9715; si el LLM no sabe, se abstiene; y ante la empanada se abstiene **sin** llamar al LLM.

### Ejercicio 6 — Escribe `hit_at_k`

- 🟢 Pista suave: Para cada par `(pregunta, esperado)`, ¿está `esperado` en los `id` recuperados?
- 🟡 Pista media: Una lista de `True/False` con comprensión; `sum` cuenta los `True`.
- 🔴 Pista directa: `aciertos = [esperado in set(recuperar(p, k)["id"]) for p, esperado in preguntas]` y `return sum(aciertos) / len(preguntas)`.

**¿Qué significa el ✅?** Que mides la recuperación con un número reproducible (0,50 y 0,85), no con impresiones.

---

> 🔬 **En la profundización:** mejoras la recuperación **un cambio a la vez, midiendo cada uno** con las mismas 20 preguntas. Sin título el hit@1 cae a 0,40 (y el hit@3 a 0,55); repetir el título 3 veces lo sube a 0,75; los **n-gramas de caracteres** (`char_wb`, 3–5) absorben «pescar»/«pesca» y llevan a hit@1 = 0,90 y hit@3 = 0,95; trozos más chicos (60 palabras) llegan a 0,95 / 1,00, mientras que la ficha completa sin trocear cae a 0,80 / 0,85. Cierra con la trampa del **sobreajuste**: elegiste la configuración mirando las mismas preguntas con que la mides.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué cambia RAG respecto de un LLM solo?

- A) Reentrena el modelo con tus documentos
- B) Le entrega al modelo los trozos relevantes de tus documentos en cada pregunta, para que responda con ellos y los cite ✅
- C) Hace que el modelo sea más grande
- D) Elimina por completo las alucinaciones

**Explicación:** El modelo no cambia; cambia lo que ve. Por eso RAG **reduce** la alucinación, pero no la elimina: si recupera mal, puede responder con seguridad algo equivocado.

---

**Pregunta 2:** ¿Por qué cada trozo conserva el `id` y la `url` de su ficha?

- A) Para ordenar la tabla
- B) Para poder citar la fuente y que la respuesta sea verificable ✅
- C) Porque TF-IDF lo exige
- D) Para que el LLM responda más rápido

**Explicación:** Una respuesta sin cita no se puede auditar. La cita es lo que permite que una persona compruebe la respuesta en la fuente oficial.

---

**Pregunta 3:** «¿Cuál es la capital de Francia?» supera el umbral con puntaje 0,43. ¿Qué lo explica?

- A) Un error de pandas
- B) La búsqueda léxica encontró la palabra «capital» en una ficha («Capital Abeja Emprende»): compara palabras, no significados ✅
- C) ChileAtiende tiene una ficha sobre Francia
- D) El umbral está bien y la respuesta es correcta

**Explicación:** Es el límite de la recuperación léxica. Por eso hay más capas: la instrucción `NO_ENCONTRADO`, la cita visible y la revisión humana.

---

**Pregunta 4:** ¿Por qué `responder` recibe el LLM como parámetro (`llm=preguntar_llm`)?

- A) Para gastar menos tokens
- B) Para poder probar la función con un LLM falso y predecible, sin depender de la red ni de la respuesta en vivo ✅
- C) Porque Gemini lo exige
- D) No tiene ninguna utilidad

**Explicación:** Es una práctica estándar de pruebas: separar la lógica (barreras, citas) del servicio externo para verificarla de forma reproducible.

---

**Pregunta 5:** Tu RAG obtiene hit@3 = 0,85 con 20 preguntas. ¿Qué afirmación es más honesta?

- A) El asistente acierta el 85% de las respuestas
- B) En 17 de 20 preguntas de prueba la ficha correcta estuvo entre los 3 trozos recuperados; la calidad de la respuesta final y su desempeño con preguntas nuevas aún no están medidos ✅
- C) Con 0,85 ya se puede publicar sin revisión
- D) hit@3 mide si el LLM alucinó

**Explicación:** hit@k mide **solo la recuperación**, con un set pequeño. Decir más que eso es inflar la evidencia.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **RAG** | Generación aumentada por recuperación | Responder con el expediente a la vista |
| **Corpus** | Colección de documentos sobre la que se busca | El archivo de fichas, normas o FAQ del servicio |
| **Trozo (*chunk*)** | Fragmento de un documento con su cita | Una foja con su número de folio |
| **TF-IDF** | Peso de una palabra según su frecuencia local y rareza global | Lo distintivo de cada documento |
| **Similitud coseno** | Parecido entre dos vectores, de 0 a 1 | Qué tanto calza la consulta con la página |
| **Top-k** | Los `k` resultados con mayor puntaje | Las primeras carpetas que saca el archivero |
| **Prompt aumentado** | Instrucción + contexto recuperado + pregunta | Memo con antecedentes adjuntos |
| **Abstención** | Responder «no lo encontré» en vez de inventar | «No consta en los antecedentes» |
| **Umbral** | Puntaje mínimo para considerar que hay algo relevante | Criterio para derivar a una persona |
| **hit@k** | Fracción de preguntas con la fuente correcta en los `k` primeros | Tasa de aciertos de la búsqueda |
| **Sobreajuste** | Elegir la configuración mirando las mismas preguntas con que se evalúa | Estudiar con la prueba en la mano |

---

## 9. Conexión con el Módulo Siguiente

En R3-03 construiste un asistente que **busca, cita y se abstiene**, y lo mediste con preguntas reales sobre las 245 fichas de ChileAtiende.

En **R3-04 · Agentes** el LLM deja de solo responder: **elige herramientas** (funciones de Python) que consultan la calidad del aire y la matrícula escolar, las ejecuta paso a paso dejando una **traza**, respeta un **límite de pasos** y pide **aprobación humana** antes de cualquier acción. En su profundización, el buscador de fichas que hiciste hoy se convierte en una de esas herramientas.

> 💡 **Pregunta para reflexionar:** ¿Qué documentos de tu servicio responden a diario las mismas preguntas? ¿Quién debería revisar las respuestas de un asistente antes de que lleguen a la ciudadanía?
