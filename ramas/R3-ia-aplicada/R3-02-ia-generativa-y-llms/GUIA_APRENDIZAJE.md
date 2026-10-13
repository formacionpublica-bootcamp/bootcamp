# Guía de Aprendizaje — R3-02 · IA generativa y LLMs

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · Especialista en IA Aplicada · Módulo 2 · Semana 3

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-02 · IA generativa y LLMs |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas (+ 2 minutos para crear tu clave, opcional) |
| **Nivel** | Intermedio — requiere R3-00; muy recomendado R3-01 |
| **Prerrequisitos** | Funciones, diccionarios, JSON (`json.loads`) y expresiones regulares básicas (`re.search`) |
| **Competencia de salida** | Usar un LLM sobre texto del Estado de forma verificable y responsable: prompts con rol, tarea, reglas y fuente; parser y validador del JSON que devuelve; few-shot; verificación de cifras contra la fuente; guardrail de datos personales y verificación humana |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `fichas.csv` — fichas de ChileAtiende; se trabaja con **Aumento de la PGU** (id 130457, 893 palabras) y **Bono de Invierno** (id 39484, 765 palabras; para extraer se usa su introducción, lo que va antes de la primera sección «## ») |
| **LLM** | Gemini (modelo por defecto del curso: `gemini-3.5-flash-lite`, configurable con `GEMINI_MODEL`) vía Google AI Studio, capa gratuita. **Opcional:** sin clave, el notebook usa respuestas de respaldo y se completa igual |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Los LLM ya están en las oficinas: alguien les pide «resúmeme este oficio», «sácame los requisitos de esta resolución», «redáctalo más simple». Este módulo te enseña a hacerlo **bien**: con prompts precisos, con código que **no confía** en la respuesta sino que la **valida**, y con las reglas de cuidado que exige el Estado.

El caso es real y vigente: la ficha de ChileAtiende del **aumento de la Pensión Garantizada Universal** (montos máximos de $250.275 y $231.732 según edad) y la del **Bono de Invierno** ($81.257 para personas de 65 años o más con pensión de hasta $231.440). Vas a pedir al LLM un resumen en lenguaje claro (el respaldo baja de 893 a 58 palabras), extraer los requisitos como **JSON** que tu código lee y valida, y — lo más importante — **atrapar una alucinación**: una extracción que inventa un monto ($85.000) y un requisito («postular en tu AFP») que contradice la fuente (el bono es **no postulable**). Tu verificador automático atrapa el monto; el requisito inventado solo lo detecta una persona que lee. Esa división del trabajo — lo que se automatiza y lo que no — es la habilidad central para usar IA generativa en el sector público.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en la oficina |
|----------|-----------|----------------------|
| **LLM** | Modelo entrenado para predecir la siguiente palabra; de paso captura significado | Un asesor que leyó todo el archivo, pero no conoce tu caso |
| **Prompt** | La instrucción: rol, tarea, reglas, fuente | El memo de encargo: mientras más claro, mejor el producto |
| **Clave de API (API key)** | Tu credencial ante el servicio | Tu ClaveÚnica: personal, nunca anotada en un documento que circula |
| **Secretos de Colab** | Guardan la clave fuera del código | La caja fuerte de la oficina |
| **Respaldo** | Respuesta fija que se usa sin clave o sin red | El formulario impreso cuando el sistema se cae |
| **Contrato de salida (JSON)** | Claves y tipos que la respuesta debe cumplir | El formulario estándar: cada dato en su casillero |
| **Parser tolerante** | Extrae el JSON aunque venga con texto alrededor | Sacar el formulario del sobre, ignorando la carta de cortesía |
| **Validador** | Lista los problemas del JSON frente al contrato | La revisión de admisibilidad |
| **Few-shot** | Ejemplos dentro del prompt en vez de entrenar | Mostrarle al nuevo tres expedientes ya derivados |
| **Temperatura** | Cuánta variedad (y riesgo) hay en la respuesta | Cuánta libertad de redacción das al asesor |
| **Alucinación** | Dato inventado, dicho con seguridad | La cifra «de memoria» que no resiste una contraloría |
| **Guardrail** | Barrera automática antes de enviar | La oficina de partes: nada sale sin pasar el filtro |
| **Verificación humana** | Lectura de lo que no se puede automatizar | El visto bueno de quien firma |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Escribir una función que devuelve un string armado con un f-string | ☐ |
| Convertir texto JSON en dict con `json.loads` y capturar un error con `try/except` | ☐ |
| Usar `re.search` y `re.findall` con un patrón dado | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar las fichas y separar las dos de trabajo: `pgu` y el `fragmento` del Bono de Invierno, y ver la estructura de cada ficha con `secciones()`: una introducción y luego secciones que empiezan con «## » (*Conoce los requisitos…*, *Lee el marco legal*…).

💡 **Concepto clave:** Para la extracción se usa solo la **introducción** del Bono de Invierno (`texto.split("\n## ")[0]`, 103 palabras): ahí están el monto, la edad y el tope de pensión. El texto completo (765 palabras) detalla grupos y excepciones que harían más larga — y más difícil de verificar — la respuesta. Elegir **qué fuente** le das al LLM ya es una decisión de calidad.

---

### Sección 1 · ¿Qué es un LLM?

🎯 **Objetivo:** Entender el salto desde R3-01 (contar palabras) a un modelo que capta significado, y las tres reglas del buen prompt.

💡 **Concepto clave:** El modelo es **probabilístico** y puede **inventar**. Por eso los chequeos de este módulo revisan **tus funciones**, nunca el texto exacto del LLM.

---

### Sección 2 · Tu clave y la regla de privacidad

🎯 **Objetivo:** (Opcional) Crear una clave gratuita en **aistudio.google.com/apikey** y guardarla en los **Secretos** de Colab con el nombre `GEMINI_API_KEY`, con «Acceso del notebook» activado.

💡 **Concepto clave:** `preguntar_llm(prompt, respaldo=...)` es la **única** puerta al modelo: lee la clave desde los Secretos (o una variable de entorno), y si no hay clave o falla la red, devuelve el respaldo. El modelo se puede cambiar con `GEMINI_MODEL` sin tocar el resto.

⚠️ **Error frecuente:** Pegar la clave en una celda «para probar rápido». Queda guardada en el archivo y en todas sus copias. Si te pasó, **revócala** en AI Studio y crea otra.

---

### Las respuestas de respaldo

🎯 **Objetivo:** Conocer `RESPALDO_RESUMEN`, `RESPALDO_EXTRACCION`, `RESPUESTA_DUDOSA` y `RESPALDO_TEMA`.

💡 **Concepto clave:** Son respuestas **escritas a mano a partir de la ficha**, con el formato típico de un LLM (JSON envuelto en ```` ```json ```` con una frase antes). `RESPUESTA_DUDOSA` trae errores plantados para probar tu verificador.

---

### Sección 3 · Resumir en lenguaje claro (ejercicio 1)

🎯 **Objetivo:** `prompt_resumen(ficha, max_palabras=60)` con rol, tarea, reglas y fuente.

💡 **Concepto clave:** La regla «usa solo la información del texto; si un dato no está, no lo inventes» y pegar la fuente completa son las dos defensas más baratas contra la alucinación.

---

### Extraer requisitos (antes del ejercicio 2)

🎯 **Objetivo:** Ver el prompt de extracción (el **contrato**: 4 claves con sus tipos) y comprobar que `json.loads` sobre la respuesta cruda **falla** por los ```` ``` ```` y la frase de cortesía.

---

### Sección 4 · Parser (ejercicio 2)

🎯 **Objetivo:** `parsear_json` que toma de la primera `{` a la última `}` y devuelve `dict` o `None`.

💡 **Concepto clave:** Un parser que **nunca lanza error** permite que tu proceso decida qué hacer con una respuesta mala (reintentar, marcar para revisión) en vez de caerse.

---

### Sección 5 · Validador (ejercicio 3)

🎯 **Objetivo:** `validar_extraccion` devuelve la lista de problemas frente al contrato.

💡 **Concepto clave:** «Se puede leer» no es «está bien». Un JSON con `"requisitos": "tener 65 años"` (texto en vez de lista) o `"montos_clp": ["$81.257"]` (texto en vez de entero) rompería la tabla que lo recibe.

---

### Sección 6 · Few-shot (ejercicio 4)

🎯 **Objetivo:** Un prompt con la lista de 18 temas, tres ejemplos y el trámite a clasificar, terminado en `Tema:`.

💡 **Concepto clave:** En R3-01 entrenaste con 183 fichas; aquí bastan 3 ejemplos. Pero la salida igual pasa por `elegir_tema`, que solo acepta temas válidos. Para «Aguinaldo de Navidad para pensionados IPS», el tema oficial es *bonos-y-beneficios-del-estado*.

---

### Temperatura y alucinación (antes del ejercicio 5)

🎯 **Objetivo:** Con clave, comparar dos extracciones a temperatura 0 y dos a 1,8.

💡 **Concepto clave:** Temperatura baja = respuestas estables; alta = más variedad y más riesgo. **Ninguna** garantiza la verdad.

---

### Sección 7 · Verificar cifras (ejercicio 5)

🎯 **Objetivo:** `montos_no_respaldados`: los montos extraídos que no aparecen en la fuente. Respaldo: `[]`; dudosa: `[85000]`.

---

### La verificación humana

🎯 **Objetivo:** Leer los requisitos de la respuesta dudosa junto a la fuente y detectar «Postular en tu AFP antes del 30 de abril», que contradice «beneficio no postulable».

💡 **Concepto clave:** La lista de verificación de 5 puntos (cifras, requisitos, omisiones, datos personales, responsable) separa lo automatizable de lo que exige criterio humano.

---

### Sección 8 · Guardrail (ejercicio 6)

🎯 **Objetivo:** `es_seguro_enviar` bloquea textos con RUT (con o sin puntos, con `K`). Las 245 fichas públicas pasan.

⚠️ **Error frecuente:** Creer que el guardrail reemplaza el criterio. Detecta el caso más típico (RUT), no nombres asociados a diagnósticos ni causas reservadas.

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Escribe `prompt_resumen`

**Pistas progresivas:**
- 🟢 Pista suave: Faltan la tarea (con el título y el límite) y la fuente.
- 🟡 Pista media: Un f-string con `{ficha['titulo']}` y `{max_palabras}`; la fuente es un string fijo más `ficha["texto"]`.
- 🔴 Pista directa: `tarea = f"Resume la ficha «{ficha['titulo']}» en lenguaje claro, en máximo {max_palabras} palabras."` y `fuente = "TEXTO DE LA FICHA:\n" + ficha["texto"]`.

**¿Qué significa el ✅?** Que tu prompt nombra la ficha, pide lenguaje claro, toma el límite del parámetro e incluye la fuente completa una vez.

---

### Ejercicio 2 — Escribe `parsear_json`

**Pistas progresivas:**
- 🟢 Pista suave: El JSON empieza en una llave que abre y termina en una que cierra.
- 🟡 Pista media: `texto.find("{")` y `texto.rfind("}")`.
- 🔴 Pista directa: `return json.loads(texto[inicio:fin + 1])` dentro del `try`.

**¿Qué significa el ✅?** Que tu parser lee el respaldo con ```` ``` ```` y frase previa, y devuelve `None` (sin caerse) ante una negativa o un JSON inválido.

---

### Ejercicio 3 — Escribe `validar_extraccion`

**Pistas progresivas:**
- 🟢 Pista suave: Dos preguntas por clave: ¿está? ¿es del tipo correcto?
- 🟡 Pista media: `if clave not in d:` / `elif not isinstance(d[clave], tipo):`.
- 🔴 Pista directa: para los montos, `if isinstance(d.get("montos_clp"), list) and not all(isinstance(m, int) for m in d["montos_clp"]): problemas.append(...)`.

**¿Qué significa el ✅?** Que el respaldo pasa limpio y el JSON malo produce exactamente 3 problemas.

---

### Ejercicio 4 — Escribe `prompt_few_shot`

**Pistas progresivas:**
- 🟢 Pista suave: Cada ejemplo son dos líneas.
- 🟡 Pista media: Dos `lineas.append(...)` dentro del `for`.
- 🔴 Pista directa: `lineas.append(f"Trámite: {tramite}")` y `lineas.append(f"Tema: {tema}")`.

**¿Qué significa el ✅?** Que el prompt lista los temas válidos, los tres ejemplos en el formato exacto y termina en `Tema:`.

---

### Ejercicio 5 — Escribe `montos_no_respaldados`

**Pistas progresivas:**
- 🟢 Pista suave: Primero los montos de la fuente; después, los extraídos que no estén ahí.
- 🟡 Pista media: `montos_en_texto(fuente)` y una comprensión con `not in`.
- 🔴 Pista directa: `en_fuente = montos_en_texto(fuente)`; `return [m for m in montos if m not in en_fuente]`.

**¿Qué significa el ✅?** Que tu verificador atrapa el $85.000 inventado y deja pasar los montos reales.

---

### Ejercicio 6 — Escribe `es_seguro_enviar`

**Pistas progresivas:**
- 🟢 Pista suave: Seguro = el patrón no encuentra nada.
- 🟡 Pista media: `re.search` devuelve `None` cuando no hay coincidencia.
- 🔴 Pista directa: `return re.search(PATRON_RUT, texto) is None`.

**¿Qué significa el ✅?** Que bloqueas RUT con y sin puntos (y con `K`) y no bloqueas ninguna ficha pública.

---

> 🔬 **En la profundización:** dos preguntas antes de publicar un texto escrito por un LLM — **¿es fiel?** y **¿se entiende?** Trabajas con la introducción de la ficha de la PGU (179 palabras). Escribes `oraciones` (la introducción tiene 9), una medida de **cobertura** (qué fracción de las palabras del resumen está en la fuente: 77 % el resumen fiel, 23 % uno con datos inventados), **números no respaldados** (el infiel inventa `300000` y `60`) y **palabras por oración** (19,9 en la introducción original; 8,9 en la versión en **lectura fácil**). Al final, todo junto: guardrail, LLM (o respaldo) y auditoría automática del resultado.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué los chequeos verifican tus funciones y no el texto que devuelve el LLM?

- A) Porque el LLM siempre responde lo mismo
- B) Porque el LLM es probabilístico: la respuesta cambia, pero el contrato y tus verificaciones no ✅
- C) Porque el texto del LLM es privado
- D) Porque sin clave no hay respuesta

**Explicación:** Lo que se puede garantizar es tu código: el prompt que arma, el parser, el validador y el verificador.

---

**Pregunta 2:** ¿Dónde guardas tu `GEMINI_API_KEY` en Colab?

- A) En la primera celda, para no olvidarla
- B) En los Secretos de Colab (🔑), con acceso del notebook activado ✅
- C) En el nombre del archivo
- D) En un comentario del código

**Explicación:** En una celda quedaría guardada en el archivo y en cada copia que compartas.

---

**Pregunta 3:** El LLM extrae `"montos_clp": [85000, 231440]` y la fuente dice $81.257 y $231.440. ¿Qué haces?

- A) Promedio los dos valores
- B) Marco el 85.000 como no respaldado y la extracción vuelve a revisión ✅
- C) Subo la temperatura y pregunto de nuevo hasta que salga bien
- D) Lo publico: la diferencia es pequeña

**Explicación:** Todo número debe estar en la fuente oficial. Preguntar de nuevo no verifica nada.

---

**Pregunta 4:** ¿Qué detecta tu verificador automático en la `RESPUESTA_DUDOSA` y qué no?

- A) Detecta todo
- B) Detecta el monto inventado, pero no el requisito inventado («postular en tu AFP»), que exige lectura humana ✅
- C) No detecta nada
- D) Detecta el requisito pero no el monto

**Explicación:** Las cifras se comparan mecánicamente; el sentido de un requisito, no. Por eso la verificación humana sigue en el proceso.

---

**Pregunta 5:** ¿Cuál de estos textos puedes enviar a la capa gratuita de un LLM?

- A) «Mi RUT es 12.345.678-9 y quiero saber si me corresponde el bono»
- B) La ficha pública de ChileAtiende del Bono de Invierno ✅
- C) Un listado de beneficiarios con nombres y direcciones
- D) Cualquiera, si el proveedor es conocido

**Explicación:** En la capa gratuita el proveedor puede usar tus textos. Solo información pública, nunca datos personales.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **LLM** | Modelo de lenguaje grande | Asesor que leyó todo el archivo |
| **IA generativa** | IA que produce texto nuevo | Redactar el borrador, no solo archivarlo |
| **Prompt** | Instrucción al modelo | Memo de encargo |
| **API key** | Credencial personal ante el servicio | ClaveÚnica: intransferible |
| **Secretos de Colab** | Almacén seguro de claves | Caja fuerte |
| **Respaldo** | Respuesta fija cuando no hay modelo | Formulario impreso de contingencia |
| **JSON** | Texto estructurado con claves y valores | Formulario estándar |
| **Parser** | Código que extrae y lee el JSON | Abrir el sobre y sacar el formulario |
| **Validador** | Código que revisa claves y tipos | Revisión de admisibilidad |
| **Few-shot** | Ejemplos dentro del prompt | Mostrar casos ya resueltos |
| **Temperatura** | Grado de variabilidad de la respuesta | Libertad de redacción |
| **Alucinación** | Dato inventado con seguridad | Cifra sin fuente |
| **Guardrail** | Filtro automático antes de enviar | Oficina de partes |
| **Lectura fácil** | Redacción para que todas las personas entiendan | Lenguaje claro en la atención ciudadana |

---

## 9. Conexión con el Módulo Siguiente

En R3-02 el LLM trabajó con **una** ficha que tú le pegaste en el prompt, y tu código verificó lo que respondió.

En **R3-03 · RAG** escalarás eso a todo el archivo: ante una pregunta de la ciudadanía («¿me corresponde el Bono de Invierno si tengo 70 años?»), el sistema **buscará** primero las fichas relevantes entre las 245, se las **entregará** al LLM como fuente y le exigirá **citar** de dónde sacó cada dato — con la verificación de hoy (cifras contra la fuente, guardrail, revisión humana) como red de seguridad.

> 💡 **Pregunta para reflexionar:** Hoy elegiste a mano qué fragmento del Bono de Invierno darle al modelo. Si tuvieras que elegirlo automáticamente entre 245 fichas, ¿cómo encontrarías los párrafos que responden la pregunta — y cómo sabrías que el modelo no usó otra cosa?
