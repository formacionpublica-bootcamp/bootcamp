# Guía de Aprendizaje — R3-CAP · Capstone: un asistente de IA para tu servicio

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · IA Aplicada · Capstone · Semanas 6–7 (cierre de rama)

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-CAP · Capstone — un asistente de IA para tu servicio |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 4–6 horas de trabajo autónomo (más el tiempo de reunir tu propio corpus) |
| **Nivel** | Integrador — aplica R3-01 a R3-04 |
| **Prerrequisitos** | R3-03 (RAG, hit@k, abstención) y R3-04 (agentes, supervisión humana) con ✅ |
| **Competencia de salida** | Diseñar, evaluar y documentar un asistente de IA generativa para un problema real del servicio, con citas, abstención y supervisión humana |
| **Entregable** | Las 4 celdas de chequeo en ✅ + demo + informe de evaluación + ficha de uso responsable |
| **Corpus** | **A elección** (propio > banco del bootcamp > datos.gob.cl). La plantilla usa `fichas.csv`: 245 fichas de trámites de ChileAtiende |
| **LLM** | `preguntar_llm()` (Gemini). **Opcional:** el capstone debe correr completo sin clave ni red |

---

## 2. ¿Para qué me sirve esto como funcionario público?

En toda unidad hay preguntas que se responden a mano, una y otra vez, con información que ya está escrita: «¿cómo postulo a tal beca?», «¿qué documentos necesito?», «¿cuándo se paga?». Este capstone es tu oportunidad de convertir ese problema en un **asistente** que busca en los documentos oficiales, responde **citando la fuente** y, cuando no sabe, **lo dice y deriva a una persona**.

Pero el entregable no es «un chatbot». Es un asistente **evaluado** (con preguntas reales escritas antes de mirar resultados), **documentado** (qué hace, qué no hace, qué riesgos tiene y quién lo supervisa) y **reproducible** (corre sin clave ni red). Ese paquete es lo que una jefatura, un comité de ética de datos o una contraloría interna necesitan para decidir si se usa.

La plantilla trae un ejemplo completo sobre las fichas de ChileAtiende, pero el capstone vale el doble si lo haces con **documentos de tu propio servicio**: preguntas frecuentes, instructivos, respuestas tipo de la OIRS. Si tu problema es de datos tabulares (registros, indicadores), el camino es el **agente** de R3-04.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | En tu proyecto |
|----------|-----------|----------------|
| **Corpus** | Los documentos (o datos) sobre los que responde el asistente | Lo eliges tú: propio > banco > datos.gob.cl |
| **Adaptador (`COLUMNAS`)** | Traduce tus columnas al formato `id`, `titulo`, `url`, `texto` | Lo único que cambias para usar tu corpus |
| **Índice** | Trozos + TF-IDF de caracteres con el título ×3 | La receta que mejor funcionó en R3-03 |
| **Set de evaluación** | ≥ 8 preguntas reales con su documento esperado | Escrito **antes** de mirar resultados |
| **hit@1 / hit@3** | ¿El documento correcto aparece primero / entre los 3 primeros? | Tu evidencia de calidad |
| **Cita** | `[Doc id · url]` en cada respuesta | Lo que vuelve verificable la respuesta |
| **Umbral** | Puntaje mínimo para responder | Calibrado con preguntas dentro y fuera del corpus |
| **`NO_ENCONTRADO`** | Abstención pactada con el LLM | La segunda barrera |
| **Ficha de uso responsable** | Uso previsto, fuentes, evaluación, privacidad, sesgos, supervisión, costo | Tu documento de riesgos y ética |
| **Rúbrica** | Cómo se evalúa el capstone | Incluye **Pertinencia** y **Riesgos y ética** |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar trocear → indexar → recuperar → aumentar → generar o abstenerse (R3-03) | ☐ |
| Calcular e interpretar hit@k, y explicar por qué no basta con «lo probé y funciona» | ☐ |
| Probar una función con un LLM «falso» (`llm=...`) para no depender de la red | ☐ |
| Explicar por qué una acción con efecto necesita aprobación humana (R3-04) | ☐ |
| Tengo identificado un corpus público y sin datos personales para mi proyecto | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Enmarca tu proyecto

🎯 **Objetivo:** Responder en una frase: ¿quién pregunta?, ¿qué pregunta?, ¿con qué documentos se responde?, ¿qué pasa si el asistente se equivoca?

💡 **Concepto clave:** La última pregunta define cuánta supervisión humana necesitas. Un error sobre el horario de una biblioteca no pesa lo mismo que uno sobre los requisitos de una pensión. Elige tu corpus en orden de preferencia: **propio** (público y sin datos personales) > **banco del bootcamp** (`fichas`, `matricula`, `aire_diario`, `reclamos`, `sismos`) > **datos.gob.cl**. Texto → asistente RAG (esta plantilla); tablas → agente (R3-04).

---

### Sección 1 · Prepara el corpus

🎯 **Objetivo:** Ajustar `CORPUS_CSV` y `COLUMNAS`, y completar la limpieza de `preparar_corpus`.

💡 **Concepto clave:** El **adaptador** es el único punto de contacto con tu fuente: si tus documentos no tienen url, usa el nombre del archivo o el número de resolución como cita. Con la plantilla quedan 245 documentos.

---

### Sección 2 · Construye el índice

🎯 **Objetivo:** Completar `construir_indice` con título ×3 y n-gramas de caracteres (3 a 5).

💡 **Concepto clave:** Con las fichas, el índice queda en 1.656 trozos × 38.790 n-gramas, y «¿Cómo me afilio a Fonasa?» recupera tres trozos de la ficha 9715. El tamaño de trozo (120 palabras aquí; en R3-03 también rindió bien 60) **se decide con tu evaluación**, no a ojo.

---

### Sección 3 · Evalúa con TUS preguntas

🎯 **Objetivo:** Escribir ≥ 8 preguntas reales con su documento esperado y reportar hit@1 y hit@3.

💡 **Concepto clave:** Con las 12 preguntas de ejemplo: **hit@1 = 0,83** (10 de 12) y **hit@3 = 0,92** (11 de 12). La que falla — «Me rechazaron la licencia porque dicen que no hice reposo» — no recupera la ficha de apelación por incumplimiento de reposo: otra vez, la persona usa palabras distintas a las de la ficha. Reporta los fallos, no solo el promedio.

---

### Sección 4 · Responde con citas o abstente

🎯 **Objetivo:** Completar las dos barreras de `responder` (umbral 0,30 y `NO_ENCONTRADO`).

💡 **Concepto clave:** Con n-gramas de caracteres los puntajes son más altos que con palabras, por eso el umbral sube a 0,30 (en la profundización se calibra con evidencia). Sin clave, la respuesta es un respaldo extractivo con su cita.

---

### Sección 5 · Tu demo

🎯 **Objetivo:** Mostrar el asistente con preguntas de tu público, incluidas algunas que no debería responder.

💡 **Concepto clave:** En la demo de la plantilla, «¿Cómo pido la Beca Bicentenario?» responde citando la ficha 2227 y la Copa América se abstiene. Pero «¿Hay ayuda para pagar la casa de reposo de mi mamá?» **también se abstiene**, aunque la ficha correcta existe: su mejor puntaje (≈ 0,20) queda bajo el umbral. Es el costo de un umbral prudente — decláralo en tu informe.

---

### Sección 6 · Ficha de uso responsable y rúbrica

🎯 **Objetivo:** Completar la ficha (uso previsto, fuentes y vigencia, evaluación, privacidad, sesgos y exclusión, supervisión humana, costo, lo que el asistente NO hace) y revisar tu proyecto contra la rúbrica.

💡 **Concepto clave:** La rúbrica premia lo que hace confiable al asistente, no lo vistoso: evaluación con evidencia, citas, abstención, **riesgos y ética**, reproducibilidad sin red y, como bonus, **Pertinencia** (corpus propio o pregunta real de gestión).

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Completa `preparar_corpus`

- 🟢 Pista suave: Tres limpiezas: nulos, vacíos y repetidos.
- 🟡 Pista media: `dropna(subset=["texto"])`, un filtro con `.str.strip() != ""` y `drop_duplicates(subset="id")`.
- 🔴 Pista directa: `corpus = corpus.dropna(subset=["texto"])`, `corpus = corpus[corpus["texto"].str.strip() != ""]`, `corpus = corpus.drop_duplicates(subset="id")`.

**¿Qué significa el ✅?** Columnas estándar, `id` únicos, y la tabla de prueba (con un duplicado, un nulo y un texto en blanco) queda en 1 fila.

### Ejercicio 2 — Completa `construir_indice`

- 🟢 Pista suave: Es el vectorizador de la profundización de R3-03.
- 🟡 Pista media: `TfidfVectorizer(strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5))`.
- 🔴 Pista directa: `X = vect.fit_transform((trozos["titulo"] + "\n") * peso_titulo + trozos["texto"])`.

**¿Qué significa el ✅?** Una fila por trozo, todos los documentos indexados y resultados ordenados por puntaje.

### Ejercicio 3 — Arma tu `informe_eval`

- 🟢 Pista suave: `hit_at_k` ya está escrita; solo hay que llamarla.
- 🟡 Pista media: `len(MIS_PREGUNTAS)`, `hit_at_k(indice, MIS_PREGUNTAS, 1)` y con `3`.
- 🔴 Pista directa: `informe_eval = {"n_preguntas": len(MIS_PREGUNTAS), "hit@1": hit_at_k(indice, MIS_PREGUNTAS, 1), "hit@3": hit_at_k(indice, MIS_PREGUNTAS, 3)}`.

**¿Qué significa el ✅?** Tienes ≥ 8 preguntas, todos los id esperados existen en tu corpus y el informe es reproducible.

### Ejercicio 4 — Completa las barreras de `responder`

- 🟢 Pista suave: Las dos barreras devuelven lo mismo: `{"respuesta": NO_SE, "fuentes": []}`.
- 🟡 Pista media: La primera mira `contexto["puntaje"].iloc[0]` antes de llamar al LLM; la segunda mira `texto` después.
- 🔴 Pista directa: `if contexto["puntaje"].iloc[0] < UMBRAL: return {...}` y `if "NO_ENCONTRADO" in texto: return {...}`.

**¿Qué significa el ✅?** Responde citando el documento esperado, se abstiene si el LLM no sabe y ante preguntas ajenas se abstiene **sin** llamar al LLM.

---

> 🔬 **En la profundización:** tres mejoras de producción. (1) **Calibrar el umbral** con 12 preguntas dentro y 8 fuera del corpus: con 0,10 acierta 13 de 20 decisiones, con 0,20 18, con **0,30 19** (11 responde bien + 8 se abstiene bien) y con 0,40 18 — así se elige 0,30 con evidencia. (2) **Filtrar por metadatos**: «¿Cómo saco el certificado de antecedentes?» trae la ficha general (3442) en todo el corpus, pero la del certificado para chilenos en el extranjero (49064) si el asistente vive en el tema «Chilenos en el exterior». (3) **Bitácora de auditoría** en JSON, con RUT y correos anonimizados **antes** de guardar.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Cuál es el mejor corpus para tu capstone?

- A) El más grande que encuentres en internet
- B) Documentos públicos de tu propio servicio, sin datos personales, que respondan consultas reales ✅
- C) Correos de la ciudadanía con sus datos
- D) Cualquiera, el corpus no importa

**Explicación:** El criterio de Pertinencia premia resolver un problema real del servicio. Y los datos personales no deben entrar a un corpus que se envía a un LLM externo.

---

**Pregunta 2:** ¿Por qué el set de evaluación se escribe antes de mirar los resultados?

- A) Para terminar más rápido
- B) Para no elegir (consciente o inconscientemente) preguntas que el sistema ya responde bien ✅
- C) Porque hit@k lo exige
- D) No importa el orden

**Explicación:** Es la misma trampa del sobreajuste de R3-03: si eliges las preguntas mirando las respuestas, el número sale inflado.

---

**Pregunta 3:** Tu asistente se abstiene ante «¿Hay ayuda para pagar la casa de reposo de mi mamá?», aunque la ficha existe. ¿Qué haces?

- A) Bajar el umbral a 0 para que nunca se abstenga
- B) Reportarlo como costo del umbral, revisar la calibración con evidencia y considerar mejoras de recuperación (sinónimos, filtros, otro tamaño de trozo) ✅
- C) Borrar la pregunta del set de evaluación
- D) Ocultarlo en la demo

**Explicación:** Un umbral prudente produce algunas abstenciones de más; es preferible a respuestas inventadas, pero se declara y se mide.

---

**Pregunta 4:** ¿Qué debe contener, como mínimo, la ficha de uso responsable?

- A) Solo el nombre del modelo
- B) Uso previsto, fuentes y vigencia, evaluación, privacidad, sesgos, supervisión humana, costo y lo que el asistente NO hace ✅
- C) El código completo
- D) Una lista de preguntas frecuentes

**Explicación:** Es el documento con el que alguien que no programa puede decidir si el asistente se usa, cómo y bajo qué control.

---

**Pregunta 5:** ¿Por qué el capstone debe correr completo sin clave ni red?

- A) Porque Gemini no funciona en Chile
- B) Para que cualquier persona pueda reproducirlo y verificar sus resultados, y para que el servicio no se caiga si el LLM no está disponible ✅
- C) Para no usar IA
- D) Porque es más rápido

**Explicación:** La reproducibilidad es un criterio de la rúbrica: los chequeos y la evaluación no pueden depender de una respuesta en vivo que cambia cada vez.

---

## 8. Glosario del Módulo

| Término | Definición simple | En tu proyecto |
|---------|-------------------|----------------|
| **Asistente RAG** | Recupera documentos y responde con ellos, citando | El camino de esta plantilla |
| **Agente** | Elige y ejecuta herramientas, con traza y aprobación | El camino para datos tabulares (R3-04) |
| **Adaptador** | Traducción de tus columnas al formato estándar | `COLUMNAS` |
| **Set de evaluación** | Preguntas reales con su respuesta esperada | `MIS_PREGUNTAS` |
| **hit@k** | Fracción de preguntas con el documento correcto en los `k` primeros | Tu métrica de recuperación |
| **Umbral de abstención** | Puntaje mínimo para responder | `UMBRAL` (0,30) |
| **Calibración** | Elegir el umbral con preguntas dentro y fuera del corpus | Profundización, ejercicio 1 |
| **Metadatos** | Datos sobre el documento: tema, institución, vigencia | Filtros de recuperación |
| **Bitácora de auditoría** | Registro de cada consulta, sin datos personales | `bitacora.jsonl` |
| **Ficha de uso responsable** | Documento de riesgos, límites y supervisión | Parte del entregable |
| **Pertinencia** | Que el proyecto resuelva un problema real del organismo | Criterio (bonus) de la rúbrica |

---

## 9. Conexión con lo que sigue

Con este capstone cierras la rama R3: pasaste de tokenizar texto (R3-01) a usar un LLM con criterio (R3-02), a un asistente que cita y se abstiene (R3-03), a un agente supervisado (R3-04) y, hoy, a un **proyecto propio evaluado y documentado**. Aprobarlo te habilita la certificación *Especialista en IA aplicada del sector público*.

El paso siguiente no está en un notebook: es llevar tu asistente a una **prueba piloto** acotada en tu servicio, con una persona responsable, la bitácora activa y una fecha para revisar los resultados con la jefatura.

> 💡 **Pregunta para reflexionar:** Si tu asistente funcionara perfecto en las pruebas, ¿qué tendría que pasar —y quién tendría que firmar— para que lo use la ciudadanía?
