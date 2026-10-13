# Guía de Aprendizaje — R3-01 · Introducción al NLP

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R3 · Especialista en IA Aplicada · Módulo 1 · Semana 2

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R3-01 · Introducción al NLP |
| **Rama** | R3 — IA Aplicada |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Básico-intermedio — requiere R3-00 (o su Prueba de Nivel aprobada) |
| **Prerrequisitos** | Strings, listas, comprensiones, diccionarios y funciones en Python |
| **Competencia de salida** | Dado un conjunto de textos del Estado, prepararlos (normalizar, tokenizar, stopwords), representarlos con TF-IDF, clasificarlos con un modelo evaluado honestamente (línea base, train/test estratificado) y leer sus errores |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `fichas.csv` — 245 fichas de trámites de ChileAtiende con texto completo y su tema oficial (18 temas). Profundización: `reclamos.csv` — muestra de 20.000 reclamos SERNAC 2011 (dato histórico, solo categorías) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Buena parte de la información del Estado es **texto libre**: fichas de trámites, oficios, reclamos, observaciones, glosas. Leerlos uno por uno no escala. El NLP (Procesamiento de Lenguaje Natural) te da el primer kit para **leer texto a escala**: limpiarlo, contar lo que importa y clasificarlo.

El caso del módulo es real: las **245 fichas de ChileAtiende**, cada una con su tema oficial asignado (bonos, salud, jubilación, vivienda…). Vas a entrenar un modelo que adivina el tema de una ficha **leyendo solo su texto**, y obtendrás una exactitud de **56,5 %** con 18 temas posibles — casi 9 veces la línea base de adivinar siempre el tema más común (6,5 %).

Pero la lección más valiosa no es la exactitud: son **los errores**. De los 27 errores, 5 fueron fichas que el modelo mandó a *trabajo-y-cesantía* — como los **aportes del empleador al sistema de pensiones**, el **Bono Laboral** o **apelar la incapacidad por un accidente del trabajo**, que ChileAtiende clasificó en *jubilación*, *bonos* o *previsión*. Y el propio Bono de Invierno (tema oficial: jubilación) fue a parar a *bonos-y-beneficios-del-estado*. ¿Error del modelo, o una ficha que pertenece legítimamente a dos temas? Esa pregunta — si un clasificador decide solo o sugiere a una persona — es exactamente la que enfrentarás cuando tu servicio quiera automatizar la derivación de solicitudes o la clasificación de reclamos.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en la oficina |
|----------|-----------|----------------------|
| **Normalizar** | Minúsculas, sin tildes, sin signos | `MINUSC()` + buscar y reemplazar |
| **Token** | Unidad de texto (una palabra) | Cada palabra separada con «Texto en columnas» |
| **Stopwords** | Palabras vacías (*de, la, que*) que se descartan | Las palabras que nadie busca en el archivo |
| **Bolsa de palabras / `Counter`** | Cuenta cuántas veces aparece cada palabra | Una tabla dinámica de palabras |
| **TF-IDF** | Pesa una palabra por cuánto aparece aquí y la castiga si aparece en todos lados | Lo que hace distinto a este expediente del resto del archivo |
| **Matriz documento-término** | Una fila por documento, una columna por palabra | Una planilla enorme, casi toda en cero |
| **Train / test estratificado** | Separar datos para entrenar y para evaluar, manteniendo la proporción de temas | Corregir una prueba con preguntas que el alumno no vio |
| **Regresión logística** | Modelo lineal que asigna una probabilidad a cada tema | Una pauta de puntaje: cada palabra suma o resta puntos a cada tema |
| **Exactitud (accuracy)** | Fracción de aciertos en prueba | Porcentaje de expedientes bien derivados |
| **Línea base** | Lo que lograrías sin modelo (siempre el tema más común) | El mínimo que el sistema nuevo debe superar |
| **Fuga de información** | Que el modelo «vea» los datos de prueba al entrenar | Filtrar las respuestas antes del examen |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Escribir una comprensión de lista con `if` | ☐ |
| Escribir una función con `return` | ☐ |
| Contar con un diccionario o un `Counter` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar las 245 fichas y la lista `STOPWORDS` (97 palabras vacías, ya sin tildes).

💡 **Concepto clave:** Las stopwords están escritas sin tildes porque se comparan contra texto **ya normalizado**. Si la lista tuviera «también» y el texto normalizado dice «tambien», nunca coincidirían.

---

### Sección 1 · Normalizar

🎯 **Objetivo:** `normalizar("Pensión Garantizada Universal (PGU): ¡$250.275!")` → `"pension garantizada universal pgu 250 275"`.

💡 **Concepto clave:** El orden importa: minúsculas → descomponer tildes (NFKD) → descartar marcas → reemplazar signos → colapsar espacios. Ojo: la `ñ` también se descompone y «año» queda «ano» (por eso verás `ano` y `anos` entre las palabras frecuentes). Es un costo conocido.

⚠️ **Error frecuente:** Quitar signos con `[^a-z0-9\s]` **antes** de descomponer las tildes: «Pensión» perdería la `ó` completa y quedaría «pensi n».

---

### Sección 2 · Tokenizar

🎯 **Objetivo:** Partir en palabras, sin stopwords ni tokens de menos de 3 caracteres.

💡 **Concepto clave:** Reutilizar `normalizar` dentro de `tokenizar` garantiza que todo el pipeline trate el texto igual. Nota que `257` sobrevive (viene de «$81.257»): los números son tokens también.

---

### Sección 3 · Frecuencias

🎯 **Objetivo:** Un `Counter` con todas las palabras de las 245 fichas: **6.910 palabras distintas**.

💡 **Concepto clave:** Las más frecuentes son *web* (413), *tramite* (409), *sitio* (402), *certificado* (345), *informacion* (311): vienen de instrucciones como «ingresa al sitio web» que se repiten en casi todas las fichas: **no distinguen a ninguna**. Ese es el problema que resuelve TF-IDF.

---

### Sección 4 · TF-IDF

🎯 **Objetivo:** Convertir las fichas en una matriz de **245 × 3.704** (palabras que aparecen en al menos 2 fichas) y leer las palabras que caracterizan al Bono de Invierno.

💡 **Concepto clave:** TF-IDF del Bono de Invierno: *pension, bono, vejez, 231, minima, invierno* (el «231» viene del tope de $231.440). Con solo conteo se colaban *anos* («años») y *personas*, que están en todas partes. TF-IDF la castiga por ser común.

⚠️ **Error frecuente:** Olvidar que `X` es una matriz «dispersa» (casi todo ceros, guardada de forma compacta): para mirar una fila se usa `X[i].toarray()[0]`.

---

### Sección 5 · Clasificar el tema

🎯 **Objetivo:** Split 75/25 estratificado (`random_state=42`, 183 fichas de entrenamiento y 62 de prueba), TF-IDF ajustado **solo** con entrenamiento, regresión logística y exactitud: **56,5 %** (35 de 62) frente a una línea base de **6,5 %**.

💡 **Concepto clave:** `fit_transform` en entrenamiento, **solo** `transform` en prueba. Si el vectorizador aprende el vocabulario de las fichas de prueba, la evaluación ya no mide lo que pasaría con fichas nuevas.

✅ **Señal de que entendiste:** Puedes explicar por qué 56 % no es «reprobar»: con 18 temas, adivinar al azar daría ~6 %.

---

### Sección 6 · Leer los errores

🎯 **Objetivo:** La tabla de los **27 errores** y el tema que más los atrae: **trabajo-y-cesantía** (5).

💡 **Concepto clave:** Varios «errores» son discutibles: los aportes del empleador o el Bono Laboral hablan del mundo del trabajo aunque su tema oficial sea jubilación o bonos; y dos apelaciones de licencia médica fueron a *salud* aunque su tema oficial sea laboral o familiar. Un clasificador con etiqueta única es un instrumento imperfecto para documentos que pertenecen a varios temas.

---

### Reflexión final

No tiene celda de chequeo porque no tiene respuesta única. Lo que importa: un modelo de 56 % puede ser muy útil **como sugerencia revisada por una persona** y peligroso **como decisión automática**. La diferencia la hace el diseño del proceso, no el algoritmo.

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Escribe `normalizar`

**Pistas progresivas:**
- 🟢 Pista suave: Faltan tres pasos entre las minúsculas y el colapso de espacios.
- 🟡 Pista media: `unicodedata.normalize("NFKD", ...)`, luego un `"".join(...)` que descarte `unicodedata.combining(c)`, luego `re.sub`.
- 🔴 Pista directa: `texto = unicodedata.normalize("NFKD", texto)`; `texto = "".join(c for c in texto if not unicodedata.combining(c))`; `texto = re.sub(r"[^a-z0-9\s]", " ", texto)`.

**¿Qué significa el ✅?** Que tres variantes de un mismo texto quedan idénticas.

---

### Ejercicio 2 — Escribe `tokenizar`

**Pistas progresivas:**
- 🟢 Pista suave: Una sola comprensión de lista con dos condiciones.
- 🟡 Pista media: Recorre `normalizar(texto).split()`.
- 🔴 Pista directa: `return [t for t in normalizar(texto).split() if t not in STOPWORDS and len(t) >= 3]`.

**¿Qué significa el ✅?** Que «de», «un», «no» desaparecen y las tildes ya no separan palabras.

---

### Ejercicio 3 — Construye la bolsa de palabras del corpus

**Pistas progresivas:**
- 🟢 Pista suave: El `Counter` sabe sumar listas de tokens.
- 🟡 Pista media: `frecuencias.update(...)` dentro del `for`.
- 🔴 Pista directa: `frecuencias.update(tokenizar(texto))`.

**¿Qué significa el ✅?** Que tu conteo coincide con uno calculado de forma independiente (la más común: *web*, 413).

---

### Ejercicio 4 — Vectoriza las fichas y lee el Bono de Invierno

**Pistas progresivas:**
- 🟢 Pista suave: Crear el vectorizador, ajustarlo y transformar es un solo método.
- 🟡 Pista media: `TfidfVectorizer(analyzer=tokenizar, min_df=2)` y `.fit_transform(df["texto"])`.
- 🔴 Pista directa: `top_tfidf = list(terminos[pesos.argsort()[::-1][:6]])` (ordena de menor a mayor, invierte, toma 6).

**¿Qué significa el ✅?** Que *pension* está entre las palabras características y *tramite* no.

---

### Ejercicio 5 — Entrena y evalúa el clasificador

**Pistas progresivas:**
- 🟢 Pista suave: Entrenamiento: aprender y transformar. Prueba: solo transformar.
- 🟡 Pista media: `vec.fit_transform(X_train_txt)`, `vec.transform(X_test_txt)`, `modelo.fit(...)`, `modelo.predict(...)`.
- 🔴 Pista directa: `exactitud = accuracy_score(y_test, pred)`; `linea_base = y_test.value_counts().max() / len(y_test)`.

**¿Qué significa el ✅?** Que tu modelo supera con creces la línea base (56,5 % vs 6,5 %).

---

### Ejercicio 6 — Arma la tabla de errores

**Pistas progresivas:**
- 🟢 Pista suave: Un filtro booleano: real distinto de predicho.
- 🟡 Pista media: `tabla[tabla["real"] != tabla["predicho"]]`.
- 🔴 Pista directa: `tema_iman = errores["predicho"].value_counts().idxmax()`.

**¿Qué significa el ✅?** Que puedes pasar de «56 % de exactitud» a «qué falla y por qué».

---

> 🔬 **En la profundización:** transferencia a un texto muy distinto — el **producto** de 20.000 reclamos SERNAC 2011 para predecir el **mercado**. Un mercado tiene un solo reclamo (rompe la estratificación): se filtran los que tienen al menos 50 (quedan 18 mercados, 19.908 reclamos). Texto corto y muchos datos dan **94,6 %** de exactitud (línea base 33,6 %)… pero el recall de *comercio a distancia/electrónico* es apenas **11 %**: el **97 %** de sus reclamos usa un producto (electrónica, computación, muebles…) que también se reclama en locales comerciales. El canal de venta no está en el texto, y ningún modelo lo puede inventar.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué las palabras más frecuentes del corpus (*trámite, certificado, personas*) sirven poco para clasificar?

- A) Porque están mal escritas
- B) Porque aparecen en casi todas las fichas y no distinguen a ninguna ✅
- C) Porque son stopwords oficiales
- D) Porque tienen tildes

**Explicación:** Una palabra que está en todas partes no ayuda a separar temas. TF-IDF la castiga con el factor IDF.

---

**Pregunta 2:** ¿Por qué el vectorizador se ajusta (`fit`) solo con las fichas de entrenamiento?

- A) Porque es más rápido
- B) Para que la evaluación simule fichas realmente nuevas, sin fuga de información ✅
- C) Porque `transform` no existe para entrenamiento
- D) Da lo mismo

**Explicación:** Si el vocabulario y los pesos IDF se calculan con las fichas de prueba, el modelo «ya las vio» y la exactitud sale optimista.

---

**Pregunta 3:** Tu clasificador tiene 56 % de exactitud con 18 temas. ¿Cómo lo comunicas?

- A) «Falla casi la mitad: no sirve»
- B) Junto a la línea base (6,5 %) y con ejemplos de sus errores, como apoyo a una persona ✅
- C) Redondeado a 60 % para que suene mejor
- D) Sin cifra, solo «funciona bien»

**Explicación:** Una cifra sin referencia no dice nada; la línea base y los errores típicos permiten decidir si sirve y para qué.

---

**Pregunta 4:** ¿Qué significa estratificar el `train_test_split`?

- A) Ordenar las fichas por tema
- B) Mantener la proporción de cada tema en entrenamiento y en prueba ✅
- C) Eliminar los temas pequeños
- D) Usar siempre las mismas fichas

**Explicación:** Con temas de 7 a 15 fichas, un split al azar podría dejar un tema sin ejemplos de prueba (o de entrenamiento).

---

**Pregunta 5:** El modelo dice *salud* para una apelación de licencia médica que ChileAtiende clasificó como *trabajo-y-cesantía*. ¿Qué concluyes?

- A) El modelo está roto
- B) La ficha toca dos temas; el «error» revela el límite de una etiqueta única ✅
- C) ChileAtiende se equivocó
- D) Hay que borrar esa ficha

**Explicación:** Leer los errores separa los fallos reales del modelo de los casos ambiguos — y orienta si conviene permitir varias etiquetas o una revisión humana.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **NLP** | Técnicas para que una máquina procese texto | Leer miles de expedientes sin abrirlos uno por uno |
| **Corpus** | El conjunto de textos que se analiza | El archivo completo de fichas |
| **Normalizar** | Uniformar el texto (minúsculas, tildes, signos) | Estandarizar cómo se escriben los nombres |
| **Token** | Unidad mínima (palabra) | Cada palabra del documento |
| **Stopword** | Palabra vacía, sin tema | «de», «la», «que» |
| **TF-IDF** | Peso de una palabra: frecuente aquí, rara en el resto | Lo que distingue a este trámite de los demás |
| **Vectorizar** | Convertir texto en números | Codificar respuestas abiertas |
| **Clasificador** | Modelo que asigna una categoría | El funcionario de partes que deriva cada documento |
| **Exactitud (accuracy)** | Porcentaje de aciertos | Tasa de derivaciones correctas |
| **Línea base** | Resultado sin modelo | El estándar mínimo a superar |
| **Recall** | De los casos reales de una clase, cuántos detectó el modelo | Cuántos reclamos de un tipo llegaron a la unidad correcta |
| **Fuga de información** | Usar datos de prueba al entrenar | Filtrar el examen |

---

## 9. Conexión con el Módulo Siguiente

En R3-01 le enseñaste a la máquina a **contar** palabras para clasificar fichas — y viste su límite: no entiende significado, solo coincidencias de palabras.

En **R3-02 · IA generativa y LLMs** darás el salto a un **modelo de lenguaje grande** (Gemini) que sí capta significado: le pedirás que **resuma una ficha en lenguaje claro**, que **extraiga sus requisitos como JSON** que tu código valida, que clasifique con pocos ejemplos (*few-shot*) — y aprenderás a **verificar** lo que responde, porque un LLM puede inventar con total seguridad.

> 💡 **Pregunta para reflexionar:** Tu clasificador falló en las fichas que tocan dos temas. Un LLM podría leer la ficha y explicar *por qué* pertenece a cada uno. ¿Confiarías más en esa explicación — o sería otra cosa que verificar?
