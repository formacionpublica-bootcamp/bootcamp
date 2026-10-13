# Guía de Aprendizaje — R3-04 · Agentes: herramientas, trazas y supervisión humana

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · IA Aplicada · Módulo 4 · Semana 5

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-04 · Agentes: herramientas, trazas y supervisión humana |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas (lección) + 1 hora (profundización opcional) |
| **Nivel** | Intermedio — requiere R3-02 (`preguntar_llm`) y R3-03 (RAG) |
| **Prerrequisitos** | Funciones y diccionarios en Python, filtros de pandas, `try/except`, JSON |
| **Competencia de salida** | Orquestar herramientas de datos con un LLM de forma segura, auditable y verificable sin red, manteniendo a una persona a cargo de las decisiones |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 diario de 14 estaciones SINCA, 2020–2025) + `estaciones.csv` y `matricula.csv` (10.945 establecimientos MINEDUC 2025, 345 comunas). Profundización: `fichas.csv` (245 fichas ChileAtiende) |
| **LLM** | `preguntar_llm()` (Gemini). **Opcional:** sin `GEMINI_API_KEY` decide el planificador de reglas y todo funciona igual |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Hasta R3-03 el LLM **respondía**. Un **agente** además **hace cosas**: decide qué consulta correr, la ejecuta y, si se lo permites, actúa — envía un correo, registra un caso, notifica a otra institución. Es el patrón detrás de los asistentes que «resuelven tareas», y es justamente lo que más cuidado exige en el Estado: una acción automática equivocada no es un mal párrafo, es un oficio enviado, un dato publicado o un beneficio mal asignado.

Este módulo construye un agente **pequeño pero completo** sobre datos reales de las otras dos ramas: la **calidad del aire** (lo que modelaste en R2) y la **matrícula escolar** (lo que analizaste en R1). Una petición como «¿cuántos días sobre la norma tuvo Rancagua en 2023? Si hubo, avisa a la SEREMI» se convierte en una consulta a pandas (47 días) y en una **propuesta** de alerta que **no sale** hasta que una persona la aprueba.

Lo que te llevas no es el agente, sino las **cuatro reglas** para cualquier automatización con IA en tu servicio: el LLM propone y el código valida; todo queda en una traza; nada con efecto sin aprobación humana (y por defecto, no); y siempre hay un límite.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Analogía en la oficina |
|----------|-----------|------------------------|
| **Agente** | Bucle planificar → actuar → observar hasta terminar | Un asistente que va resolviendo un encargo paso a paso |
| **Herramienta** | Función de Python con argumentos simples y errores claros | Un formulario específico que solo sirve para una cosa |
| **`HERRAMIENTAS` (menú)** | Lo único que el agente puede usar, con sus argumentos y si tiene efecto | Las atribuciones delegadas por resolución: nada fuera de ellas |
| **Efecto** | La herramienta cambia algo en el mundo (enviar, registrar, pagar) | Firmar y despachar vs. solo consultar |
| **Planificador de reglas** | Respaldo determinista que decide el siguiente paso sin LLM | El procedimiento escrito que se sigue cuando no está el experto |
| **`interpretar_plan`** | Valida el JSON del LLM contra el menú; si no calza, `None` | La revisión de admisibilidad de una solicitud |
| **Traza** | Registro de cada paso: quién lo propuso, qué se ejecutó, resultado, estado | El expediente con todas sus actuaciones foliadas |
| **Aprobación humana** | Toda acción con efecto exige un «sí» explícito; sin aprobador, no | El visto bueno de la jefatura antes de despachar |
| **Límite de pasos** | Corta el bucle tras `max_pasos` | El plazo máximo de tramitación |
| **Guarda** | Chequeo antes o después de una herramienta (argumentos, calidad, privacidad) | Control de legalidad previo y posterior |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar un DataFrame por dos condiciones y contar con `.sum()` | ☐ |
| Escribir un `try/except` y explicar para qué sirve | ☐ |
| Leer y escribir un diccionario anidado (`{"args": {"anio": 2024}}`) | ☐ |
| Explicar qué es JSON y usar `json.loads` | ☐ |
| Usar `preguntar_llm(prompt, respaldo=...)` (R3-02) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación, el LLM y qué es un agente

🎯 **Objetivo:** Cargar `aire_diario.csv` (30.674 filas, 14 estaciones, 2020-01-01 a 2025-12-30), `estaciones.csv` y `matricula.csv` (10.945 establecimientos, 345 comunas); definir `preguntar_llm`.

💡 **Concepto clave:** Las cifras **nunca** las inventa el LLM: salen de pandas, dentro de las herramientas. El LLM solo **orquesta** (decide qué herramienta usar) y **redacta**.

---

### Sección 1 · Las herramientas

🎯 **Objetivo:** Conocer `pm25_promedio`, `matricula_comuna` y la acción con efecto `enviar_alerta` (simulada: deja el mensaje en `BANDEJA_SALIDA`), y escribir `dias_sobre_norma`.

💡 **Concepto clave:** Una buena herramienta hace **una** cosa, recibe argumentos simples y **falla con un error claro**. Cerro Navia 2024: **56 días** sobre 50 µg/m³ con **355 días** con dato. Ojo: legalmente la norma diaria se evalúa con el percentil 98 anual; «días sobre 50» es un indicador de episodios, no un dictamen.

---

### Sección 2 · El menú y entender la petición

🎯 **Objetivo:** Ver cómo `HERRAMIENTAS` declara argumentos y efecto, y cómo se extraen estación, año y comuna del texto.

💡 **Concepto clave:** «Temuco» tiene **dos** estaciones (Las Encinas y Nielol), así que no se usa como alias: `extraer_estacion("aire en Temuco")` devuelve `None`. Ante la ambigüedad, el sistema **no adivina**.

---

### Sección 3 · Planificador de reglas y validación del LLM

🎯 **Objetivo:** Completar `planificar_reglas` (primer paso según palabras clave) y la validación de `interpretar_plan`.

💡 **Concepto clave:** El planificador principal (`planificar`) le muestra el menú al LLM y le pide el siguiente paso **en JSON**; lo que vuelve pasa por `interpretar_plan` y, si es inválido o no hay clave, decide `planificar_reglas`. Cada plan queda marcado con su **origen** (`llm` o `reglas`).

⚠️ **Error frecuente:** Llamar directamente la función que nombra el LLM. Si dice `borrar_base_de_datos`, la validación debe devolver `None`.

---

### Sección 4 · Ejecutar con traza

🎯 **Objetivo:** `ejecutar_paso` registra paso, herramienta, argumentos, origen, resultado y estado, **sin caerse** si la herramienta falla.

💡 **Concepto clave:** Nielol 2022 da PM2.5 promedio 16,9 µg/m³ (`ok`); una estación `None` queda como `error` con su `ValueError`. La traza es el **expediente** del agente.

---

### Sección 5 · Supervisión humana

🎯 **Objetivo:** `ejecutar_supervisado`: si la herramienta tiene `efecto=True`, solo se ejecuta con un `aprobador` que diga que sí; sin aprobador, **no**.

💡 **Concepto clave:** *Denegar por defecto.* Si el aprobador falla o no existe, la acción no sale. La negativa también queda en la traza (`rechazado`). En Colab puedes probar `aprobador=aprobador_consola`, que te muestra la acción y te pregunta.

---

### Sección 6 · El bucle del agente y la demo

🎯 **Objetivo:** Cerrar `agente(peticion, planificador, aprobador, max_pasos)`.

💡 **Concepto clave:** El bucle termina cuando el planificador dice `fin` (estado `terminado`) o al agotar `max_pasos` (estado `limite_de_pasos`). En la demo: Las Encinas Temuco 2021 → PM2.5 promedio 25,8; Coyhaique → 41 establecimientos y 13.101 estudiantes; Rancagua 2023 → 47 días sobre la norma, y la alerta a la SEREMI queda **rechazada** porque nadie la aprobó.

---

### Riesgos

La tabla final del notebook resume siete riesgos (herramientas inventadas, acciones sin control, bucles y costo, inyección de instrucciones, sesgo de automatización, datos personales, cifras sin respaldo) y qué pieza del módulo mitiga cada uno. Léela como un **checklist** para cualquier proyecto con agentes en tu servicio.

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Escribe `dias_sobre_norma`

- 🟢 Pista suave: `d` ya tiene los valores de PM2.5 del año; falta contar y armar el diccionario.
- 🟡 Pista media: `(d > umbral).sum()` cuenta los días sobre el umbral; `d.size`, los días con dato.
- 🔴 Pista directa: `return {"estacion": estacion, "anio": anio, "dias_sobre_norma": int((d > umbral).sum()), "dias_con_dato": int(d.size)}`.

**¿Qué significa el ✅?** Que la herramienta devuelve cifras correctas (56 de 355 para Cerro Navia 2024) y lanza `ValueError` ante una estación inexistente.

### Ejercicio 2 — Completa `planificar_reglas`

- 🟢 Pista suave: Son tres `if` en orden, cada uno con su lista de palabras clave.
- 🟡 Pista media: `if "norma" in t or "episodio" in t:` y devuelve un diccionario con `herramienta` y `args`.
- 🔴 Pista directa: `return {"herramienta": "dias_sobre_norma", "args": {"estacion": extraer_estacion(peticion), "anio": extraer_anio(peticion)}}`; análogo para `pm25_promedio` y `matricula_comuna` (`{"comuna": extraer_comuna(peticion)}`).

**¿Qué significa el ✅?** Las cuatro peticiones de prueba van a la herramienta correcta con los argumentos correctos, y tras tener el dato propone la alerta solo si se pidió.

### Ejercicio 3 — Completa la validación de `interpretar_plan`

- 🟢 Pista suave: Dos controles: ¿existe la herramienta? ¿calzan los argumentos?
- 🟡 Pista media: `herramienta not in HERRAMIENTAS`; `set(args) != set(HERRAMIENTAS[herramienta]["args"])`.
- 🔴 Pista directa: `if herramienta not in HERRAMIENTAS: return None` y `if not isinstance(args, dict) or set(args) != set(HERRAMIENTAS[herramienta]["args"]): return None`.

**¿Qué significa el ✅?** Acepta un JSON válido entre ```` ``` ```` y rechaza herramientas inventadas, argumentos faltantes o sobrantes y texto sin JSON.

### Ejercicio 4 — Completa `ejecutar_paso`

- 🟢 Pista suave: Todo lo que puede fallar va dentro del `try`.
- 🟡 Pista media: `HERRAMIENTAS[nombre]["funcion"](**args)` llama la herramienta con sus argumentos con nombre.
- 🔴 Pista directa: en el `try`, `registro["resultado"] = ...` y `registro["estado"] = "ok"`; en `except Exception as e:`, `registro["resultado"] = f"{type(e).__name__}: {e}"` y `registro["estado"] = "error"`.

**¿Qué significa el ✅?** Un paso válido queda `ok`, uno que falla queda `error` sin detener el programa, y los pasos van numerados.

### Ejercicio 5 — Completa `ejecutar_supervisado`

- 🟢 Pista suave: La condición de rechazo tiene dos partes unidas por `or`.
- 🟡 Pista media: `if aprobador is None or not aprobador(plan):` → registra y devuelve el rechazo.
- 🔴 Pista directa: arma `registro = {"paso": len(traza) + 1, "herramienta": ..., "args": ..., "origen": ..., "resultado": "acción NO ejecutada: sin aprobación humana", "estado": "rechazado"}`, `traza.append(registro)` y `return registro`.

**¿Qué significa el ✅?** Sin aprobador o con un «no», la bandeja no cambia; con un «sí», la alerta sale; las consultas no piden aprobación.

### Ejercicio 6 — Completa el bucle de `agente`

- 🟢 Pista suave: Dentro del `for` hay dos casos: terminó o hay que ejecutar.
- 🟡 Pista media: `if plan["herramienta"] == "fin":` → `estado = "terminado"` y `break`.
- 🔴 Pista directa: después del `if`, `ejecutar_supervisado(plan, traza, aprobador)`.

**¿Qué significa el ✅?** El agente termina solo (consulta + alerta rechazada) y un planificador «terco» queda cortado en exactamente `max_pasos`.

---

> 🔬 **En la profundización:** transferencia a otro corpus. Agregas la herramienta `buscar_ficha` sobre las 245 fichas de ChileAtiende (con la receta que mejor funcionó en R3-03: título ×3 + n-gramas de caracteres, en 1.656 trozos), le enseñas al planificador cuándo usarla y lo **mides** con 10 peticiones (exactitud 1,00). Luego sumas guardas: **argumentos** (estación ambigua, año 2030 sin datos), **calidad** — El Bosque 2025 marca **0 días** sobre la norma, pero con solo **59 días con dato** (en 2024 fueron 45 días de 348) — y **privacidad** (una petición con RUT se bloquea antes de planificar).

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Qué distingue a un agente de un asistente RAG?

- A) Usa un modelo más grande
- B) Decide en bucle qué herramienta usar, la ejecuta, observa el resultado y puede actuar ✅
- C) No usa LLM
- D) Responde más rápido

**Explicación:** RAG recupera y responde. El agente **planifica y actúa**, por eso necesita menú, traza, límites y aprobación.

---

**Pregunta 2:** El LLM responde `{"herramienta": "borrar_registros", "args": {}}`. ¿Qué debe pasar?

- A) Ejecutarla: el LLM sabe lo que hace
- B) `interpretar_plan` devuelve `None` porque no está en el menú, y decide el planificador de reglas ✅
- C) Detener el computador
- D) Pedirle al LLM que se disculpe

**Explicación:** El LLM **propone**; el código **valida**. Lo que no está en `HERRAMIENTAS` no existe para el agente (permisos mínimos).

---

**Pregunta 3:** ¿Por qué `ejecutar_supervisado` rechaza la acción cuando `aprobador` es `None`?

- A) Por un error de programación
- B) Porque la regla segura es denegar por defecto: si no hay una persona que apruebe, la acción con efecto no se ejecuta ✅
- C) Para ahorrar memoria
- D) Porque `None` significa «sí» en Python

**Explicación:** Si el valor por defecto fuera «sí», cualquier falla del aprobador dejaría pasar la acción.

---

**Pregunta 4:** El agente responde «0 días sobre la norma en El Bosque en 2025». ¿Qué falta?

- A) Nada: es una buena noticia
- B) Advertir que ese año solo hay 59 días con dato, así que la cifra no es comparable ✅
- C) Redondear a un decimal
- D) Enviar la alerta igual

**Explicación:** Un cero con un sexto del año medido no es un cero. Por eso la herramienta devuelve `dias_con_dato` y la guarda de calidad lo convierte en advertencia.

---

**Pregunta 5:** ¿Por qué ningún chequeo del notebook depende de la respuesta del LLM en vivo?

- A) Porque Gemini es gratis
- B) Porque se prueban las piezas con planificadores y aprobadores «falsos» y deterministas; así las pruebas son reproducibles con o sin red ✅
- C) Porque el LLM no se usa
- D) Porque los asserts no funcionan con texto

**Explicación:** El LLM se usa (planifica y redacta cuando hay clave), pero la lógica que importa —validar, registrar, supervisar, limitar— se verifica de forma determinista.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Agente** | Programa que decide y ejecuta pasos con herramientas | Un asistente que tramita un encargo |
| **Herramienta (*tool*)** | Función que el agente puede invocar | Un procedimiento específico |
| **Menú de herramientas** | Lista cerrada de lo que el agente puede hacer | Atribuciones delegadas |
| **Efecto** | Cambio en el mundo (enviar, registrar, pagar) | Un acto que se despacha |
| **Planificador** | Quien decide el siguiente paso (LLM o reglas) | Quien instruye la siguiente actuación |
| **Respaldo determinista** | Reglas que deciden igual sin LLM | El procedimiento escrito |
| **Traza** | Registro de cada paso y su resultado | El expediente foliado |
| **Humano en el bucle** | Una persona aprueba las acciones con efecto | Visto bueno de la jefatura |
| **Denegar por defecto** | Sin aprobación explícita, no se actúa | «Lo que no está autorizado, está prohibido» |
| **Límite de pasos** | Máximo de vueltas del bucle | Plazo máximo de tramitación |
| **Guarda** | Control antes o después de una herramienta | Control de legalidad o de calidad |
| **Inyección de instrucciones** | Texto en los datos que intenta dar órdenes al LLM | Un documento adjunto que dice «apruébese sin revisar» |

---

## 9. Conexión con el Módulo Siguiente

En R3-04 cerraste el arco de las tres ramas: datos de **R1** (matrícula) y **R2** (aire), orquestados por un LLM de **R3** con validación, traza, límite de pasos y aprobación humana.

En **R3-CAP · Capstone** juntas todo en un proyecto propio: un **asistente de trámites** sobre las fichas de ChileAtiende —o, mejor aún, sobre documentos o datos de **tu servicio**— con recuperación evaluada, respuestas con cita, abstención, ficha de uso responsable y una rúbrica que premia la **pertinencia** y el manejo de **riesgos**.

> 💡 **Pregunta para reflexionar:** ¿Qué acción de tu trabajo **nunca** delegarías en un agente, aunque funcione bien en las pruebas? ¿Y cuál sí, con aprobación humana?
