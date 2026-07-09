# 📘 Guía de Aprendizaje — R3-01 · Introducción al NLP

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R3-01 · Introducción al NLP (Procesamiento de Lenguaje Natural) |
| **Pista / Rama** | R3 — IA Aplicada (bloque avanzado, optativo) |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Avanzado (primer módulo técnico de la rama R3) |
| **Prerrequisitos** | R3-00 aprobado, o prueba de nivel de la rama R3 aprobada |
| **Competencia de salida** | Dado un texto real del Estado, prepararlo (normalizar, tokenizar, quitar stopwords) y extraer de él información cuantificable: frecuencias, bolsa de palabras y un clasificador simple por palabras clave |
| **Dataset** | `rubros.csv` — los 45 rubros reales del catálogo de compras públicas de ChileCompra / MercadoPúblico |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |
| **Extra opcional** | `profundiza.ipynb` — teoría más honda (TF-IDF, n-gramas, sesgos del lenguaje) con 4 ejercicios auto-corregidos |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Hasta ahora, en las ramas R1 y R2, tus datos fueron **números y categorías** ordenados en columnas: montos, cantidades, regiones, fechas. Pero piensa en tu día a día: buena parte de la información que produce el Estado es **texto libre**. El nombre de una licitación. La glosa de una orden de compra. Un reclamo ciudadano en la OIRS. La descripción de un convenio. Las observaciones de un acta.

Ese texto hoy se lee **a mano**, uno por uno, o directamente no se analiza. El **NLP** (Procesamiento de Lenguaje Natural) es la disciplina que enseña a la máquina a leer y analizar texto **a escala**: miles de reclamos, millones de órdenes de compra.

En este módulo trabajarás con texto real: los **45 rubros oficiales** del catálogo de compras de ChileCompra (`rubros.csv`), es decir, las categorías con las que el Estado clasifica todo lo que compra — desde "Alimentos, bebidas y tabaco" hasta "Servicios de limpieza industrial". Es texto en español, "sucio" de verdad: con tildes, mayúsculas inconsistentes y palabras vacías.

**¿Qué decisiones permite?** Con la tubería básica que aprenderás podrías: contar de qué hablan miles de reclamos sin leerlos uno a uno, detectar qué términos dominan las licitaciones de tu servicio, o construir un asistente simple que sugiera el rubro correcto cuando un funcionario describe lo que necesita comprar (¡el Ejercicio 4 hace exactamente eso!). Todo con la librería estándar de Python y pandas: nada nuevo que instalar.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en Excel / sector público |
|---|---|---|
| **NLP** | Técnicas para que la máquina analice texto | Un equipo que "lee" miles de expedientes por ti y te entrega el resumen contable |
| **Corpus** | El conjunto de textos con que se trabaja | La carpeta con todos los oficios del año; aquí, los 45 rubros de ChileCompra |
| **Normalizar** | Uniformar el texto: minúsculas, sin tildes ni signos | Como cuando estandarizas "STGO.", "Santiago" y "santiago" antes de una tabla dinámica |
| **Tokenizar** | Partir el texto en palabras (tokens) | Usar "Texto en columnas" de Excel con el espacio como separador |
| **Stopwords (palabras vacías)** | Palabras que aparecen en todo y no aportan tema ("de", "y", "para"…) | El "timbre y firma" de los oficios: está en todos, no distingue ninguno |
| **Bolsa de palabras** | Contar cuántas veces aparece cada término, ignorando el orden | Un `CONTAR.SI` por cada palabra del catálogo |
| **`Counter`** | Objeto de Python que cuenta ocurrencias | Una tabla dinámica de conteo, pero para listas de palabras |
| **Frecuencia** | Cuántas veces aparece un token en el corpus | "¿Cuántas veces aparece 'servicios' en el catálogo?" → 10 veces |
| **Clasificador por palabras clave** | Asigna categoría según palabras compartidas | El funcionario experimentado que, al leer "vacunas y jeringas", dice al tiro: "eso va a Salud" |
| **`re.sub` (expresión regular)** | Buscar y reemplazar por patrón, no por texto exacto | Un "Buscar y reemplazar" de Word con superpoderes |
| **`unicodedata`** | Descomponer caracteres para quitar tildes | Separar la "é" en "e" + tilde, y botar la tilde |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Esta rama es optativa y avanzada: se asume que el núcleo del bootcamp ya es terreno conocido. Responde honestamente antes de abrir el notebook:

| ¿Puedo...? | Estado |
|---|---|
| Escribir una función propia con `def` y `return` | ✅ Sí / 🔄 Repasar antes de seguir |
| Usar métodos de string como `.lower()`, `.split()`, `.strip()` | ✅ Sí / 🔄 Repasar antes de seguir |
| Escribir una comprensión de lista con condición (`[x for x in ... if ...]`) | ✅ Sí / 🔄 Repasar antes de seguir |
| Recorrer una lista con un bucle `for` y acumular resultados | ✅ Sí / 🔄 Repasar antes de seguir |
| Cargar un CSV con `pd.read_csv` y convertir una columna a lista | ✅ Sí / 🔄 Revisar R1-02 |
| Explicar qué es un `set` y para qué sirve la intersección de conjuntos | ✅ Sí / 🔄 Basta con leer la pista del Ejercicio 4 |

Si aprobaste R3-00 o la prueba de nivel, deberías marcar "Sí" en casi todo. Si dudas en más de dos filas, dedica 30 minutos a repasar funciones y listas: este módulo es 100% "programar funciones pequeñas", sin scikit-learn ni matemática nueva.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 1: Por qué el texto es un dato difícil

🎯 **Objetivo:** entender por qué la máquina no puede usar el texto crudo y conocer la **tubería básica del NLP**.

💡 **Concepto clave — para el computador, "Aseo" y "aseo" son cosas distintas:**
El notebook abre con tres formas de escribir lo mismo: `"Artículos de Aseo e Higiene"`, `"ARTICULOS DE ASEO E HIGIENE"` y `"articulos aseo, higiene"`. Tú ves un solo concepto; el computador ve **tres textos diferentes**, porque compara caracteres, no significados. Es el mismo drama que viviste alguna vez en Excel cuando "Región Metropolitana", "R.M." y "RM" te arruinaron una tabla dinámica. Por eso todo proyecto de NLP **empieza limpiando**, y la tubería estándar tiene 4 pasos: **normalizar → tokenizar → quitar stopwords → representar** (bolsa de palabras).

🔍 **Qué hace esta sección:** es solo lectura (no hay código que completar), pero define el mapa de ruta: los Ejercicios 1, 2 y 3 son exactamente los pasos de la tubería, y el Ejercicio 4 la usa para algo útil.

⚠️ **Error frecuente:** leerla por encima "porque no tiene código". Los 4 pasos de la tubería son la estructura de todo el módulo; si los tienes claros, cada ejercicio es obvio.

✅ **Señal de comprensión:** puedes explicarle a un colega, sin mirar el notebook, por qué contar la palabra "aseo" en un CSV sin limpiar daría un conteo equivocado.

---

### 🔷 Sección 2: Preparación y datos

🎯 **Objetivo:** cargar el corpus real y dejar disponibles las dos variables globales del módulo: `CORPUS` y `STOPWORDS`.

💡 **Concepto clave — el corpus es tu "archivador":**
Un **corpus** es simplemente el conjunto de textos con que trabajas. Aquí es pequeño pero real: los **45 rubros** del catálogo de ChileCompra, la taxonomía oficial con que el Estado clasifica sus compras. Junto al corpus se define `STOPWORDS`: un conjunto de 23 palabras vacías del español ("de", "y", "para", "la"… y también "general", que en este catálogo no aporta tema).

🔍 **Qué hace el código:**
- Si `rubros.csv` no existe localmente (por ejemplo, en Colab), intenta descargarlo desde GitHub automáticamente.
- `pd.read_csv("rubros.csv")` carga el archivo (una sola columna: `rubro`, 45 filas).
- `CORPUS = df_rubros["rubro"].tolist()` convierte la columna en una lista de Python de 45 textos.
- `STOPWORDS = {...}` define el conjunto de palabras vacías que usarás en el Ejercicio 2.
- El `print` final confirma: `Corpus: 45 rubros reales del Estado` y muestra un ejemplo (el rubro número 12: *"Equipamiento y suministros médicos"*).

⚠️ **Error frecuente:** saltarse esta celda e ir directo al Ejercicio 1. Sin ejecutarla, `CORPUS` y `STOPWORDS` no existen y los chequeos posteriores fallarán con `NameError`.

✅ **Señal de comprensión:** sabes qué contiene `CORPUS` (una lista de 45 strings) y para qué existirá `STOPWORDS` más adelante.

---

### 🔷 Sección Ejercicio 1: Normalizar el texto

🎯 **Objetivo:** programar `normalizar(texto)`, la función que uniforma cualquier texto en español.

💡 **Concepto clave — el orden de la limpieza importa:**
Normalizar tiene 4 pasos **en orden**: minúsculas → quitar tildes → quitar signos → colapsar espacios. El truco de las tildes es elegante: `unicodedata.normalize("NFKD", texto)` descompone cada "é" en una "e" más una marca de acento separada, y luego se descartan las marcas con `unicodedata.combining(c)`. Es como despegar el post-it de tilde que trae cada vocal y quedarse solo con la letra.

🔍 **Qué hace el código (el que escribirás tú):**
- `.lower()` baja todo a minúsculas.
- El par de líneas de `unicodedata` (la pista del notebook te las regala) elimina las tildes.
- `re.sub` reemplaza todo lo que **no** sea letra, número o espacio por un espacio.
- Un segundo `re.sub` colapsa espacios múltiples y `.strip()` recorta los extremos.
- La prueba rápida convierte `"Artículos ELÉCTRICOS, y de Iluminación!"` en `"articulos electricos y de iluminacion"`.

⚠️ **Error frecuente:** quitar los signos **antes** de bajar a minúsculas y descomponer las tildes. Si tu patrón de `re.sub` solo acepta `a-z` y todavía hay mayúsculas o vocales con tilde, las borrarás como si fueran signos. Respeta el orden.

✅ **Señal de comprensión:** puedes predecir, sin ejecutar, qué devuelve tu función para `"Á É Í Ó Ú ñ 2025!!"` (respuesta del chequeo: `"a e i o u n 2025"` — fíjate que la "ñ" se convierte en "n").

---

### 🔷 Sección Ejercicio 2: Tokenizar y quitar palabras vacías

🎯 **Objetivo:** programar `tokenizar(texto)`, que parte el texto limpio en palabras útiles.

💡 **Concepto clave — no todas las palabras informan:**
Si contaras todas las palabras de cualquier texto en español, "de" ganaría siempre — y no te diría nada del tema. Las **stopwords** son ese ruido. Tokenizar aquí es: normalizar, partir por espacios, y quedarse solo con los tokens que **no** son stopwords **y** tienen **3 o más letras** (así se cuelan menos restos sin valor). Es el equivalente a archivar un oficio ignorando el membrete y los saludos protocolares: vas directo a lo que distingue el documento.

🔍 **Qué hace el código:**
- Reutiliza tu `normalizar` del Ejercicio 1 (¡las funciones se encadenan, como en toda tubería!).
- `.split()` parte por espacios.
- Una comprensión de lista filtra: `t not in STOPWORDS and len(t) >= 3`.
- La prueba: `"Servicios de Limpieza Industrial"` → `["servicios", "limpieza", "industrial"]` (el "de" desapareció).

⚠️ **Error frecuente:** tokenizar el texto **crudo** en vez de reutilizar `normalizar`. Si lo haces, `"Médicos!"` y `"medicos"` quedan como tokens distintos y el chequeo te lo dirá con el caso `"Equipamiento y suministros médicos"`.

✅ **Señal de comprensión:** puedes explicar por qué el filtro tiene **dos** condiciones y qué pasaría si quitaras la de `len(t) >= 3`.

---

### 🔷 Sección Ejercicio 3: Bolsa de palabras — ¿qué compra más el Estado?

🎯 **Objetivo:** construir un `Counter` llamado `frecuencias` con todos los tokens del corpus y leer el top 8.

💡 **Concepto clave — contar ya es analizar:**
La **bolsa de palabras** es la representación más simple del NLP: juntar todos los tokens e ignorar el orden, quedándose solo con los conteos. Suena tosca, pero responde una pregunta real: ¿de qué habla, en conjunto, el catálogo de compras del Estado? En este corpus la respuesta verificada es: **"servicios" (10 veces)**, seguida de "productos" (8), "suministros" (7), "equipos" (6) y "maquinaria" (6). O sea: el catálogo del Estado está dominado por servicios, productos y suministros — algo que acabas de descubrir **contando**, sin leer los 45 rubros.

🔍 **Qué hace el código:**
- `frecuencias = Counter()` crea el contador vacío.
- Un bucle recorre `CORPUS` y en cada vuelta hace `frecuencias.update(tokenizar(rubro))`: agrega los tokens de ese rubro al conteo acumulado.
- `frecuencias.most_common(8)` devuelve las 8 palabras más frecuentes con su conteo.

⚠️ **Error frecuente:** contar los rubros como frases completas (hacer `Counter(CORPUS)`) en vez de acumular **tokens**. Cada rubro aparece una sola vez, así que ese conteo daría puros unos. Queremos contar palabras, no textos enteros.

✅ **Señal de comprensión:** sabes por qué "servicios" gana y puedes decir qué significaría, en términos de gestión pública, que una palabra domine el catálogo.

---

### 🔷 Sección Ejercicio 4: Un clasificador simple — ¿a qué rubro va mi compra?

🎯 **Objetivo:** programar `clasificar(texto)`, que sugiere el rubro del catálogo más parecido a una solicitud escrita en lenguaje natural.

💡 **Concepto clave — clasificar por palabras compartidas:**
Imagina la pantalla de un sistema de compras: el funcionario escribe "necesito comprar medicamentos y productos farmacéuticos" y el sistema le sugiere el rubro correcto. La versión más simple y honesta de ese asistente: tokenizar la solicitud como un **conjunto** (`set`), tokenizar cada rubro, y elegir el rubro que **comparte más palabras** (intersección de conjuntos, el operador `&`). Es la bolsa de palabras aplicada a similitud.

🔍 **Qué hace el código:**
- `consulta = set(tokenizar(texto))` convierte la solicitud en un conjunto de palabras limpias.
- `max(CORPUS, key=...)` recorre los 45 rubros y se queda con el que maximiza `len(consulta & set(tokenizar(r)))`, es decir, el de mayor intersección.
- Las pruebas del notebook: la solicitud de medicamentos debe caer en *"Medicamentos y productos farmacéuticos"* y la de limpieza de oficina en *"Servicios de limpieza industrial"*.

⚠️ **Error frecuente (y límite honesto):** creer que este clasificador "entiende". Solo acierta si la solicitud usa palabras **parecidas** a las del nombre del rubro. Escribe "necesito jeringas" y no sabrá que eso es médico: no conoce sinónimos ni contexto. Ese límite no es un bug del ejercicio — es la frontera exacta donde empiezan los modelos de lenguaje de R3-02.

✅ **Señal de comprensión:** puedes dar un ejemplo de solicitud que este clasificador acertaría y otro que fallaría, y explicar **por qué** falla.

---

### 🔷 Sección de cierre: Lo que te llevas

🎯 **Objetivo:** consolidar la tubería y ver su alcance real.

💡 **Concepto clave:** normalizar → tokenizar → quitar stopwords → representar. Con eso ya respondes preguntas reales sobre cualquier columna de texto libre de tu servicio: descripciones, observaciones, reclamos, glosas. Y conoces el límite: **contar palabras no captura significado**. El "Para llevar al trabajo" del notebook lo resume bien: es asombroso cuánto se entiende de un montón de texto solo contando bien las palabras correctas.

✅ **Señal de comprensión (del módulo completo):** las 4 celdas de chequeo muestran ✅ y puedes recitar la tubería sin mirar.

---

## 6. Guía de los Ejercicios

### ✍️ Ejercicio 1 — Normalizar el texto

**Objetivo:** que `"Médicos"`, `"MEDICOS"` y `"medicos"` sean la misma palabra.
**Habilidad que entrena:** limpieza de texto con métodos de string, `unicodedata` y expresiones regulares.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son 4 transformaciones encadenadas sobre la misma variable, en el orden que da el enunciado. La más difícil (quitar tildes) el notebook te la regala completa en el recuadro 💡.
2. 🟡 *Pista media:* después de `.lower()` y de las dos líneas de `unicodedata` de la pista, usa `re.sub` con un patrón que signifique "todo lo que NO sea letra minúscula, dígito o espacio" y reemplázalo por un espacio. Luego otro `re.sub` para colapsar espacios repetidos (`\s+`) en uno, y `.strip()` al final.
3. 🔴 *Pista directa:* la función tiene 5 líneas antes del `return`: una de minúsculas, dos de tildes (copiadas de la pista), una de `re.sub(r"[^a-z0-9\s]", " ", texto)` y una que combina la colapsación de espacios con el recorte de extremos.

**Lógica de la solución (en prosa):** se transforma el texto paso a paso — minúsculas primero, luego descomponer y descartar tildes, luego convertir en espacios todos los signos, y finalmente compactar los espacios — devolviendo la versión limpia.

**Qué valida el chequeo ✅:** tres casos exactos, incluyendo que `"Artículos ELÉCTRICOS, y de Iluminación!"` dé `"articulos electricos y de iluminacion"` y que `"Á É Í Ó Ú ñ 2025!!"` dé `"a e i o u n 2025"` (vocales sin tilde, "ñ"→"n", números conservados, sin signos).

---

### ✍️ Ejercicio 2 — Tokenizar y quitar palabras vacías

**Objetivo:** partir texto limpio en tokens útiles.
**Habilidad que entrena:** composición de funciones y filtrado con comprensión de listas.

**Pistas progresivas:**
1. 🟢 *Pista suave:* toda la función cabe en una línea, y el recuadro 💡 del notebook te la muestra casi entera. Tu trabajo real es entenderla: normaliza, parte, filtra.
2. 🟡 *Pista media:* el filtro tiene dos condiciones unidas con `and`: que el token no esté en `STOPWORDS` y que su largo sea al menos 3. Y el texto que partes con `.split()` debe ser el **normalizado**, no el crudo.
3. 🔴 *Pista directa:* el `return` es una comprensión de lista sobre `normalizar(texto).split()`, con la doble condición del enunciado. Compárala carácter a carácter con la pista 💡 de la celda si algo no calza.

**Lógica de la solución (en prosa):** se reutiliza `normalizar` para limpiar, se parte por espacios y se conservan solo las palabras informativas (ni vacías ni demasiado cortas).

**Qué valida el chequeo ✅:** que `"Servicios de Limpieza Industrial"` dé exactamente `["servicios", "limpieza", "industrial"]`, que las tildes de "médicos" desaparezcan, y que la stopword "de" no sobreviva en `"Productos de papel"`.

---

### ✍️ Ejercicio 3 — Bolsa de palabras

**Objetivo:** acumular las frecuencias de todos los tokens del corpus en un `Counter`.
**Habilidad que entrena:** recorrer un corpus y acumular conteos (el patrón más usado del NLP básico).

**Pistas progresivas:**
1. 🟢 *Pista suave:* son dos ideas: crear un contador vacío antes del bucle, y dentro del bucle "sumarle" los tokens de cada rubro. `Counter` tiene un método pensado justo para eso.
2. 🟡 *Pista media:* `frecuencias = Counter()` fuera del bucle; luego `for rubro in CORPUS:` y dentro, el método `.update(...)` recibiendo la lista que devuelve `tokenizar(rubro)`.
3. 🔴 *Pista directa:* tres líneas: la creación del `Counter` vacío, el `for` sobre `CORPUS`, y el `frecuencias.update(tokenizar(rubro))` indentado dentro. La celda ya trae el código que imprime el top 8.

**Lógica de la solución (en prosa):** se parte con un contador en cero y se recorre el corpus rubro por rubro, tokenizando cada uno y acumulando sus palabras; al final, `most_common(8)` revela el vocabulario dominante del catálogo.

**Qué valida el chequeo ✅:** que `frecuencias` sea un `Counter`, que la palabra más común coincida con la verdad recomputada de forma independiente — **"servicios", con 10 apariciones** — y que los conteos de "servicios" (10), "suministros" (7) y "productos" (8) calcen exactamente. Si todo va bien, verás además el mensaje: *"El Estado compra, sobre todo: servicios, productos, suministros, equipos, maquinaria"*.

---

### ✍️ Ejercicio 4 — Un clasificador simple por palabras clave

**Objetivo:** sugerir el rubro del catálogo más afín a una solicitud en lenguaje natural.
**Habilidad que entrena:** similitud entre textos vía intersección de conjuntos; usar `max` con `key`.

**Pistas progresivas:**
1. 🟢 *Pista suave:* piensa en dos pasos: convertir la solicitud en un conjunto de palabras limpias, y luego preguntarle a cada rubro "¿cuántas palabras compartes conmigo?" quedándote con el que más comparta. El recuadro 💡 de la celda trae la línea del ganador.
2. 🟡 *Pista media:* la primera línea es `consulta = set(tokenizar(texto))`. Para la segunda, `max` puede recorrer `CORPUS` usando como criterio (`key=`) una función lambda que mida el tamaño de la intersección `&` entre `consulta` y el conjunto de tokens de cada rubro.
3. 🔴 *Pista directa:* dos líneas: el `set` de la consulta, y un `return max(CORPUS, key=lambda r: ...)` donde el `...` es `len(consulta & set(tokenizar(r)))` — exactamente la expresión de la pista 💡 del notebook.

**Lógica de la solución (en prosa):** se tokeniza la solicitud como conjunto y se elige, entre los 45 rubros, aquel cuyo nombre tokenizado comparte más palabras con ella. Empates y ausencias los resuelve `max` quedándose con el primero, lo que basta para las pruebas del módulo.

**Qué valida el chequeo ✅:** dos clasificaciones exactas: la solicitud de medicamentos debe devolver *"Medicamentos y productos farmacéuticos"* y la de limpieza de oficina, *"Servicios de limpieza industrial"*.

---

## 7. Sección Especial: El Ejercicio de Política Pública

El Ejercicio 4 es el corazón de política pública del módulo: construiste, en dos líneas, un prototipo de algo que existe de verdad en los sistemas del Estado — un **asistente que clasifica solicitudes de compra en el rubro correcto** del catálogo de ChileCompra.

**Reflexión guiada:**
- Clasificar bien el rubro **no es un detalle administrativo**: de esa clasificación dependen las estadísticas de compras públicas, los estudios de mercado del Estado y la capacidad de detectar, por ejemplo, cuánto se gasta en "Equipamiento y suministros médicos" a nivel nacional. Un texto mal clasificado es gasto invisible.
- Tu clasificador acierta cuando la solicitud usa las **mismas palabras** que el rubro, y falla en cuanto aparece un sinónimo ("jeringas" no matchea con "médicos") o lenguaje coloquial ("cosas de escritorio"). Si el Estado automatizara la clasificación con esta técnica, ¿quiénes serían los más perjudicados? Probablemente los servicios pequeños o municipios que describen sus compras con lenguaje menos "de catálogo".
- La bolsa de palabras del Ejercicio 3 mostró que el catálogo está dominado por términos genéricos ("servicios" aparece 10 veces en solo 45 rubros; "productos", 8). Cuando las categorías comparten tanto vocabulario entre sí, un clasificador por palabras clave confunde con facilidad — otro argumento para técnicas que entiendan significado.

**Pregunta de debate abierta:**
> Si ChileCompra pusiera este clasificador (mejorado) a sugerir rubros automáticamente en MercadoPúblico, ¿debería la sugerencia ser obligatoria, editable o solo informativa? ¿Quién responde cuando el algoritmo clasifica mal una compra y esta se vuelve invisible para la fiscalización?

**Datos que complementarían el análisis:**
- Las **descripciones reales de órdenes de compra** (no solo el catálogo): texto libre masivo para probar el clasificador en condiciones reales.
- El **historial de clasificaciones hechas por humanos**, para medir cuánto acierta el algoritmo contra el criterio experto.
- Los **reclamos y preguntas del foro** de cada licitación: otra fuente de texto donde contar palabras ya revela problemas recurrentes.
- Sinónimos y jerga regional en las solicitudes, para dimensionar cuánto pierde un enfoque de palabras exactas.

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Por qué el texto es un dato "difícil" para el computador?

- a) Porque los archivos de texto pesan mucho
- b) **Porque la máquina compara caracteres, no significados: "Aseo", "ASEO" y "aseo" son tres textos distintos para ella ✅**
- c) Porque el español tiene demasiadas palabras
- d) Porque pandas no puede leer columnas de texto

**Explicación:** el computador solo opera con símbolos y números; no sabe que dos escrituras distintas nombran lo mismo. Por eso toda la primera mitad de la tubería del NLP (normalizar, tokenizar) existe para **uniformar** el texto antes de contar o comparar.

---

**Pregunta 2:** ¿Cuál es el orden correcto de la tubería básica del NLP que practicaste?

- a) Tokenizar → normalizar → representar → quitar stopwords
- b) Representar → tokenizar → normalizar → quitar stopwords
- c) **Normalizar → tokenizar → quitar stopwords → representar (bolsa de palabras) ✅**
- d) Quitar stopwords → normalizar → representar → tokenizar

**Explicación:** primero se limpia el texto (minúsculas, tildes, signos), luego se parte en tokens, luego se filtran las palabras vacías y recién entonces se convierte en números (conteos). El orden importa: si tokenizas antes de normalizar, "Médicos!" y "medicos" quedan como tokens distintos.

---

**Pregunta 3:** ¿Por qué se eliminan las stopwords antes de contar frecuencias?

- a) Para que el programa corra más rápido
- b) Porque son palabras mal escritas
- c) Porque Python no puede contar palabras de dos letras
- d) **Porque aparecen en casi todo texto y no aportan tema: sin quitarlas, "de" sería siempre la palabra más común y no diría nada ✅**

**Explicación:** las palabras vacías ("de", "y", "para"…) son el ruido de fondo del idioma. Al filtrarlas, el top de frecuencias pasa a reflejar el **contenido**: en este corpus, "servicios" (10), "productos" (8) y "suministros" (7) — un retrato real de lo que compra el Estado.

---

**Pregunta 4:** En el Ejercicio 3, la palabra más frecuente del catálogo de 45 rubros resultó ser "servicios", con 10 apariciones. ¿Qué representa ese resultado?

- a) Que el clasificador está entrenado
- b) **Que la bolsa de palabras resume de qué trata el corpus completo, sin leerlo rubro por rubro ✅**
- c) Que hay un error, porque "de" debería ser más frecuente
- d) Que el Estado gasta 10 veces más en servicios que en productos

**Explicación:** la bolsa de palabras ignora el orden y cuenta términos: es un resumen temático, no financiero. "Servicios" domina el **vocabulario** del catálogo, lo que no dice nada de montos de gasto (¡cuidado con esa sobre-interpretación!). Y "de" no aparece porque es stopword.

---

**Pregunta 5:** Tu clasificador acierta con "necesito medicamentos" pero falla con "necesito jeringas". ¿Cuál es la explicación correcta?

- a) Falta ejecutar de nuevo la celda de chequeo
- b) El corpus tiene un error en ese rubro
- c) **El clasificador solo compara palabras exactas compartidas: no conoce sinónimos ni contexto, y "jeringas" no aparece en ningún nombre de rubro ✅**
- d) Las stopwords borraron la palabra "jeringas"

**Explicación:** la similitud por intersección de conjuntos es literal: si la palabra de la solicitud no está en el nombre del rubro, la coincidencia es cero. Entender que "jeringa" es un implemento médico requiere **significado**, no conteo — y ese es exactamente el salto que dan los modelos de lenguaje en R3-02.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en Excel / administración pública |
|---|---|---|
| **NLP (Procesamiento de Lenguaje Natural)** | Técnicas para que la máquina analice texto a escala | Leer y clasificar miles de reclamos sin hacerlo uno por uno |
| **Corpus** | Conjunto de textos con que se trabaja | El archivador con los 45 rubros del catálogo de ChileCompra |
| **Normalizar** | Uniformar el texto: minúsculas, sin tildes ni signos | Estandarizar "R.M.", "RM" y "Región Metropolitana" antes de tabular |
| **Token** | Cada unidad (normalmente palabra) en que se parte un texto | Cada celda que resulta de "Texto en columnas" |
| **Tokenizar** | Partir el texto en tokens | Separar una glosa en sus palabras |
| **Stopword (palabra vacía)** | Palabra frecuente que no aporta tema ("de", "y", "para") | El membrete que está en todos los oficios y no distingue ninguno |
| **Bolsa de palabras** | Representar un texto por sus conteos de palabras, ignorando el orden | Un `CONTAR.SI` por cada palabra distinta |
| **`Counter`** | Objeto de Python que cuenta ocurrencias y entrega el top con `most_common` | Tabla dinámica de conteo lista para ordenar |
| **Frecuencia** | Número de veces que aparece un token en el corpus | "servicios" aparece 10 veces en el catálogo |
| **Expresión regular (`re.sub`)** | Buscar/reemplazar por patrones en vez de texto exacto | Buscar y reemplazar de Word, pero con comodines potentes |
| **Intersección de conjuntos (`&`)** | Elementos que dos conjuntos tienen en común | Las palabras que comparten la solicitud y el nombre del rubro |
| **Clasificador por palabras clave** | Asignar categoría según palabras compartidas con cada opción | Sugerir el rubro de una compra según las palabras de la solicitud |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R3-02 · IA generativa y LLMs

En este módulo le enseñaste a la máquina a **contar** palabras, y con eso llegaste sorprendentemente lejos: resumiste el catálogo de compras del Estado y construiste un clasificador funcional en dos líneas. Pero también chocaste con el muro, y lo chocaste a propósito: tu clasificador no sabe que "jeringa" es algo médico, ni que "aseo" y "limpieza" son casi lo mismo. Cuenta palabras; no las **entiende**.

**R3-02 cruza ese muro:** los **modelos de lenguaje (LLMs)** — la tecnología detrás de herramientas como ChatGPT o Claude — representan las palabras por su **significado**, no por sus letras. Verás qué es la IA generativa, cómo funciona un LLM por dentro (a grandes rasgos), cómo pedirle cosas bien (*prompts*) y, sobre todo, qué usos responsables tiene en el trabajo del Estado: resumir, clasificar entendiendo sinónimos, redactar borradores, extraer datos de texto libre.

**Pregunta motivadora para llegar a R3-02:**
> Tu clasificador falla con "necesito jeringas" porque ninguna palabra coincide con "Equipamiento y suministros médicos". Un LLM lo clasifica bien al primer intento, sin que nadie le programe la regla. ¿Cómo puede una máquina "saber" que una jeringa es material médico... y qué deberías verificar antes de confiarle esa decisión en un proceso real de compras públicas?

---

*Formación Pública Chile · Licencia CC BY 4.0*
