# Formación Pública — Syllabus de Ciencia de Datos
### Benchmark contra los mejores bootcamps del mundo + programa completo módulo por módulo

> Documento de diseño curricular **v3**. Reescribe la v2 (21 módulos en un solo itinerario) hacia
> la estructura vigente del proyecto: **3 capas escalonadas por ambición** (A para todos, B y C
> opcionales), nomenclatura **capa+módulo**, y datos reales de compras públicas. Mantiene las
> decisiones cerradas: cero-código de entrada, autoguiado, Colab + notebooks, GitHub como hogar,
> licencia CC BY 4.0. Norte estratégico: **ONS Data Science Campus** (ciencia de datos para el bien
> público), con el modelo **escalonado del ONS** (awareness → developing → practitioner) como guía
> de arquitectura.
>
> Documentos hermanos: [BLUEPRINT_FORMACION_PUBLICA.md](BLUEPRINT_FORMACION_PUBLICA.md) (el porqué
> del rediseño) y [README.md](README.md) (índice navegable + sitio).

---

## 0. Qué cambió respecto de la v2 (y por qué)

La v2 era un **itinerario único** cuyo perfil de salida era "Data Scientist del sector público".
Eso contradecía el objetivo declarado (**upskilling, no reconversión**): pedir a un funcionario
part-time y sin código que llegue a *desplegar y monitorear modelos* es, de hecho, un cambio de
carrera. La v3 resuelve esa tensión **escalonando por ambición** (como hace el ONS):

- **Capa A · Datos sin miedo** — el producto real de *upskilling*, **para todos**. Alfabetización
  de datos + IA como copiloto. *No te convierte en data scientist, y está bien.*
- **Capa B · Ciencia de datos aplicada** *(opcional)* — para quien quiere modelar. *Aquí sí es un
  paso hacia un rol nuevo, y se dice con todas sus letras.*
- **Capa C · IA aplicada al Estado** *(opcional)* — LLMs, RAG y agentes.

Otros cambios integrados en esta v3:

| Cambio | Detalle |
|---|---|
| **Nomenclatura** | `M0…M18` → `P1–P4` (Prework), `A1–A7`, `B1–B7`, `C1–C3`. URLs legibles (`A1-exploracion-con-pandas`). |
| **Módulo nuevo A2** | *Cruzar y resumir tablas* (`merge` + `groupby`): tapaba un vacío crítico (no se enseñaba `JOIN`/`merge` en ningún lado). |
| **IA generativa adelantada** | El módulo de LLMs es **A7** (cierre de Capa A, alcanzable por todos), no un módulo terminal. La Capa C lo usa como base. |
| **Datos reales** | La línea de ML (B2–B6) usa **compras públicas reales** (`data/process_licitaciones.py` → `compras_ml.csv` desde las órdenes de compra de ChileCompra), no datos sintéticos. |
| **Fuente corregida** | Los datos son de **ChileCompra / MercadoPúblico** (no DIPRES). Coherente con la ética de citar fuentes (A6). |
| **Capstones por capa** | Cada capa cierra con su propio proyecto (Capstone A/B/C), no un único Proyecto Final. |
| **Sitio + despliegue** | Sitio en **MkDocs Material** desplegado a **GitHub Pages** (decisión "puerta de entrada" resuelta). |
| **Proveedor LLM** | **Google Gemini** (`gemini-2.5-flash`), capa gratuita sin tarjeta, alineado con la cuenta Google de Colab. Decisión cerrada. |

---

## 1. Los 10 mejores bootcamps del mundo (y qué le robamos a cada uno)

Ordenados por relevancia para **nuestro** caso (funcionario público, upskilling en el puesto), no
por marketing. (Sin cambios de fondo respecto de la v2: sigue siendo material de referencia válido.)

| # | Programa | País / formato | Por qué destaca | Qué adoptamos |
|---|----------|----------------|-----------------|----------------|
| 1 | **ONS Data Science Campus** | Reino Unido · sector público | El referente mundial de DS para el bien público; oferta **escalonada** (awareness/developing/practitioner), mentoría (Accelerator) y proyecto aplicado a la propia institución. | El **modelo escalonado** (= nuestras 3 capas); ética y código reproducible como **hilos transversales**; capstone con datos del propio organismo. |
| 2 | **Le Wagon** (Data Science & AI) | Global · 27 ciudades + online | El mejor valorado del mundo. 80% práctico. Arco completo Python→stats→ML→deployment→LLMs/RAG/agentes; proyecto final con *pitch*. Usa Colab. | El arco "datos→modelo→despliegue→IA generativa"; landing pulido + currículo por fases (inspira el sitio). |
| 3 | **Springboard** (DS Career Track) | Online · part-time 6 meses | Estructura por **"Data Science Method"** (6 pasos repetibles); muchos mini-proyectos + capstones; software engineering ligero. | El método de 6 pasos → nuestro **"Ciclo Pública"** (§3). |
| 4 | **General Assembly** | Global | Capstone profesional; foco en empleabilidad y comunicación a no técnicos. | Capstone "presentable a stakeholders". |
| 5 | **Flatiron School** | EE.UU. · 15 sem | Base sólida + 3 proyectos de portafolio. | Cadencia de proyectos de portafolio. |
| 6 | **BrainStation** | Global | Producción muy pulida, datos reales. | Estándar de calidad de materiales y "look & feel" (aplicado al sitio MkDocs). |
| 7 | **DataCamp** | Online · self-paced | Aprendizaje por celdas con *checks* automáticos inline. | Nuestro patrón de **celda de chequeo** ✅/pista amable. |
| 8 | **WBS Coding School** | Alemania/UE | Currículo amplio + financiación pública (Bildungsgutschein). | Modelo de financiamiento/certificación con respaldo institucional. |
| 9 | **4Geeks Academy** | LatAm/EE.UU. · part-time | Referente hispano, project-based, prework cero-código. *(Contrapunto: cambio de carrera y de pago.)* | Formato hispano, *aprender construyendo*, proyecto por nivel; referencia de alcance, no de propósito. |
| 10 | **Bloom Institute** | EE.UU. · 6 meses | Python/SQL/ML + deployment en la nube; modelo ISA. | Énfasis en desplegar de verdad (Capa B). |

> *Menciones de honor: Metis (rigor estadístico), Coursera/IBM (escala y gratuidad parcial),
> Georgia Tech / UT Austin OMSA (profundidad académica a bajo costo), OSSU y 4Geeks open-source.*

---

## 2. Lo que hacen TODOS los mejores (los 7 patrones del syllabus)

Estado: ✅ ya cerrado · ➕ a reforzar.

1. **Project-based desde el día 1** ✅ — datos reales en cada lección; el portafolio *es* el certificado.
2. **Un método repetible que estructura todo** ✅ — adoptado: el **"Ciclo Pública"** (§3), declarado módulo a módulo.
3. **Reproducibilidad como hilo transversal** ➕ — práctica en cada notebook (estructura, semillas, "en vivo o caché"); módulo dedicado en B5.
4. **Ética y uso responsable, transversal y temprano** ➕ — vive en A6, pero se siembra antes y se retoma en B-deployment y en toda la Capa C.
5. **Cadencia de hitos visibles** ✅ — tres capstones (A/B/C), cada uno una certificación independiente.
6. **Arco que llega hasta el despliegue** ✅ — Capa B llega a desplegar (B6); honestamente etiquetado como "paso a rol nuevo".
7. **Bloque de IA generativa actualizado** ✅ — LLMs (A7), RAG (C2) y agentes (C3), estándar 2026, con Gemini.

**Veredicto:** el programa está alineado con el estado del arte. La v3 no rehace módulos: **escalona
la ambición, explicita el método y vuelve transversales reproducibilidad y ética**.

---

## 3. La columna vertebral: el "Ciclo Pública" (6 pasos)

Adaptación del *Data Science Method* al Estado. Cada módulo declara en qué paso trabaja.

1. **Pregunta** — ¿qué decisión pública mejora si respondo esto?
2. **Obtén** — consigo los datos (MCP ChileCompra, datos.gob.cl, API, archivo).
3. **Limpia** — los preparo, documento supuestos, cuido sesgos.
4. **Explora** — describo, visualizo, formulo hipótesis.
5. **Modela** — SQL/estadística/ML según la pregunta; evalúo honestamente.
6. **Comunica & Despliega** — cuento la historia a una audiencia no técnica y, si aplica, dejo el modelo usable y reproducible.

> Transversal a los 6: **reproducibilidad** (semilla, estructura, versionado, "en vivo o caché") y
> **ética** (equidad, privacidad, transparencia, no automatizar daño).

---

## 4. La estructura: 3 capas escalonadas

| Capa | Para quién | Duración realista | Perfil de salida (honesto) | Certificación |
|---|---|---|---|---|
| **Prework** | Quien nunca programó | ~3 sem · 4 h/sem | Ejecuta código, lo básico de Python, trae datos. | — |
| **A · Datos sin miedo** | **Todos** | ~7 sem · 4–5 h/sem | Responde preguntas con datos reales, limpia, consulta con SQL, visualiza honesto y usa IA con criterio. | **Alfabetización de datos públicos** |
| **B · Ciencia de datos** *(opc.)* | Quien quiere modelar | ~7 sem · 6–8 h/sem | Plantea, entrena, evalúa y despliega modelos de ML de forma reproducible. *(Es un paso hacia un rol nuevo.)* | **Data Scientist del sector público** |
| **C · IA aplicada** *(opc.)* | Quien quiere construir con IA | ~4 sem · 6–8 h/sem | Resuelve tareas de texto con LLMs, hace RAG sobre documentos propios y orquesta agentes. | **Especialización IA aplicada** |

**Caso conductor:** compras públicas (ChileCompra/MercadoPúblico) atraviesa el programa; se abre a
otros dominios (salud, censo, energía) cuando enseñan mejor un concepto. La **personalización fuerte
va en el capstone**: cada estudiante lo aplica a datos de **su propia institución** (modelo ONS).

---

## 5. Syllabus completo módulo por módulo

Formato de ficha: **objetivo · competencia de salida · paso(s) del Ciclo · contenidos · ejercicio
real · chequeos · entregable**. Plantilla y profundidad estilo P1; cada módulo es carpeta con
`README.md` (+ *Open in Colab*), `leccion.ipynb` y `solucion.ipynb`. Verificación: la solución da
4/4 ✅; la lección con TODO sin completar da ❌ amables sin romperse.

### PREWORK — *"De cero a leer datos"* (P1–P4)

#### P1 · Setup y sintaxis de Python — Ciclo: Pregunta/Obtén
- **Competencia:** abre un notebook, escribe y corre Python básico, interpreta errores típicos.
- **Contenidos:** Colab (cero instalación); celdas; `print`/f-strings; variables; tipos; operadores; condicionales; **métodos de texto** (`.strip/.lower/.title/.replace/.split`) y **formato de números** (`:,`); cómo leer un error. *(5 ejercicios.)*
- **Ejercicio real:** **dato ancla 2025** (gasto $18.430.546.563.769 CLP, 1.867.076 órdenes, 1.165 organismos) → gasto promedio por orden y por organismo.
- **Entregable:** "primer cálculo del gasto público de Chile".

#### P2 · Colecciones y bucles — Ciclo: Obtén/Explora
- **Competencia:** listas y diccionarios; recorre con `for`; filtra con `if`.
- **Ejercicio real:** lista de organismos con montos → mayor gasto, conteo por umbral, diccionario {organismo: monto}.
- **Entregable:** "ranking de organismos en Python puro".

#### P3 · Funciones y lectura de archivos — Ciclo: Obtén/Limpia
- **Competencia:** define funciones con parámetros/retorno; lee CSV; `try/except`.
- **Ejercicio real:** `gasto_total(organismo)` sobre un CSV de órdenes.
- **Entregable:** mini-librería `compras.py`.

#### P4 · Datos desde la web: JSON y APIs *(opcional)* — Ciclo: Obtén
- **Competencia:** llama una API, parsea JSON, cae a copia local sin red.
- **Contenidos:** HTTP/JSON; `requests`; **patrón en-vivo-o-caché**.
- **Chequeos:** validan **estructura y relaciones**, no valores exactos.
- **Entregable:** notebook que "se conecta al Estado en vivo".

> **Hito Prework:** sabe ejecutar, programar lo básico y traer datos reales.

---

### CAPA A · DATOS SIN MIEDO — *"Pensar con datos"* (A1–A7, para todos)

> **🔬 Profundización (opcional):** **cada** módulo de la Capa A (A1–A7) tiene un `profundiza.ipynb`
> con la teoría a fondo (el *porqué*) + 4 ejercicios conceptuales auto-corregidos. Construidos con el
> patrón de A5 y **revisados adversarialmente por un agente experto en datos** (correctitud + pedagogía).

#### A1 · Exploración con pandas — Ciclo: Explora
- **Competencia:** carga, inspecciona, filtra, cuenta y resume un dataset.
- **Contenidos:** `DataFrame`/`Series`; `read_csv`; `head/shape/info`; selección, filtrado; `value_counts`; estadísticos rápidos.
- **Ejercicio real:** **establecimientos del SML** (salud, MINSAL) → conteo por región, filtros, estadísticos de coordenadas. *(Dominio salud: muestra que las skills transfieren.)*
- **Entregable:** "EDA exprés".

#### A2 · Cruzar y resumir tablas (`merge` + `groupby`) — Ciclo: Obtén/Explora · **módulo nuevo**
- **Competencia:** relaciona dos tablas por su llave, elige el cruce correcto (`inner`/`left`), caza filas huérfanas y resume con `groupby`.
- **Contenidos:** `pd.merge` (analogía BUSCARV); `inner` vs `left`; fila huérfana; `groupby().sum()` (la tabla dinámica de verdad).
- **Ejercicio real:** **órdenes de compra ↔ catálogo de organismos** (datos reales ChileCompra) → gasto por región. Incluye una huérfana inyectada a propósito y una **celda de reflexión** ("¿qué le dirías a tu jefatura?").
- **Por qué importa:** cruzar y agrupar es lo que separa "abrir un CSV" de "responder una pregunta real".
- **Entregable:** "gasto por región cruzando dos tablas".

#### A3 · Limpieza de datos — Ciclo: Limpia
- **Competencia:** detecta y corrige nulos, duplicados, tipos y categorías; **documenta supuestos**.
- **Ejercicio real:** **rubros de compras públicas 2026** (ChileCompra) como export crudo: espacios, mayúsculas, monto como texto, un faltante y un duplicado.
- **Entregable:** dataset limpio + **README de supuestos** (semilla de buenas prácticas).

#### A4 · SQL fundamentos (SQLite) — Ciclo: Obtén/Explora
- **Competencia:** `SELECT` con filtros, `ORDER BY`, agregaciones y `GROUP BY`.
- **Contenidos:** modelo relacional; `SELECT/WHERE/ORDER BY/LIMIT`; `COUNT/SUM/AVG`; `GROUP BY`; SQLite en Colab. *(Recomendado añadir `JOIN`, eco de A2.)*
- **Ejercicio real:** **Parques Nacionales (CONAF)** → consultas por región y superficie. *(Dominio medio ambiente.)*
- **Entregable:** cuaderno de consultas tipo "preguntas de una jefatura".

#### A5 · Estadística descriptiva — Ciclo: Explora/Modela
- **Competencia:** describe con rigor; entiende por qué el promedio engaña con datos sesgados.
- **Contenidos:** media/mediana/moda; dispersión; percentiles; `describe()`; "correlación ≠ causalidad".
- **Ejercicio real:** **población de comunas (Censo 2024, INE)** → media vs mediana en datos sesgados.
- **Entregable:** "ficha estadística" reutilizable.
- **🔬 Profundización (opcional):** `profundiza.ipynb` — robustez, varianza/CV, asimetría, IQR/outliers, muestreo, y **correlación ≠ causalidad + paradoja de Simpson**; 4 ejercicios conceptuales. **Piloto del formato "profundiza"** (revisado por un experto en datos; replicable al resto de módulos).

#### A6 · Visualización y ética de datos — Ciclo: Comunica + (transversal Ética)
- **Competencia:** elige el gráfico correcto, lo hace legible y reconoce riesgos éticos.
- **Contenidos:** matplotlib (barras/líneas); títulos/ejes/fuente; **gráficos engañosos** (eje Y truncado); **ética**: privacidad, citar fuentes, no inducir a error, límites de los datos.
- **Ejercicio real:** **matriz eléctrica de Chile (CEN)** → gráfico claro + "nota ética" de qué NO concluir. *(Dominio energía.)*
- **Entregable:** gráfico honesto + checklist ético.

#### A7 · IA generativa y LLMs — Ciclo: Modela/Comunica + Ética
- **Competencia:** resuelve una tarea real de texto con un LLM, de forma reproducible y responsable.
- **Contenidos:** qué es un LLM (intuición); llamar a **Gemini** desde Python; *prompting*; clasificar y extraer JSON; **uso responsable** (verificar cifras, no enviar datos personales). Patrón **en-vivo-o-caché**.
- **Ejercicio real:** clasificar/extraer datos de **glosas de compra** con un LLM, verificando.
- **Por qué aquí:** en 2026, usar IA con criterio es la skill de upskilling más relevante para el funcionario mediano. Por eso cierra la Capa A (todos la alcanzan) y es la base de la Capa C.
- **Entregable de portafolio (HITO):** **"Informe de datos públicos"** que use A1–A7.

> **Capstone A — *Tu pregunta, tus datos*** ✅ *construido* (`A8-capstone/`): **dataset real provisto**
> (órdenes de ChileCompra) + **scaffold de 6 pasos** + **ejemplo resuelto** + **rúbrica**. El estudiante
> responde una pregunta con esos datos o con los de **su propia institución** (tabla limpia + gráfico
> honesto + conclusión + reflexión). **Rúbrica (0–3 c/u, aprobado 12/18):** pregunta clara · datos bien
> tratados · análisis válido · visual honesta · conclusión accionable · reflexión. → **Certificación:
> Alfabetización de datos públicos.**

---

### CAPA B · CIENCIA DE DATOS APLICADA — *"Predecir y desplegar"* (B1–B7, opcional)

> Requisito: Capa A. Honestidad: esta capa ya es un paso hacia un perfil más técnico.

> **🔬 Profundización (opcional):** **cada** módulo de la Capa B (B1–B7) tiene un `profundiza.ipynb`
> con la teoría a fondo (el *porqué*) + 4 ejercicios conceptuales auto-corregidos. Construidos con el
> patrón de A5 y **revisados adversarialmente por un agente experto en datos** (correctitud + pedagogía).

#### B1 · SQL para features — Ciclo: Obtén/Limpia
- **Competencia:** crea *features* con SQL (agregaciones por entidad, ventanas, fechas) listas para ML.
- **Contenidos:** `JOIN` avanzados; funciones de ventana; `CASE`; tablón analítico (una fila por entidad); evitar *leakage* temporal.
- **Entregable:** "feature store" SQL para los modelos de B2–B4.

#### B2 · Fundamentos de Machine Learning — Ciclo: Modela
- **Competencia:** separa train/test, entrena un modelo base, evalúa sin engañarse, entiende el sobreajuste.
- **Contenidos:** supervisado vs no supervisado; regresión; `train_test_split`; MAE/RMSE; **semillas**; generalización.
- **Ejercicio real:** **compras de alimentos (ChileCompra, `compras_ml.csv`)** → predecir `monto_total` (regresión).
- **Nota de diseño:** `monto≈precio×cantidad` hace la relación muy intuitiva (bueno para "verlo funcionar"); para subir el nivel, sumar `categoria`/`region`/`tamaño` como features.
- **Entregable:** primer modelo evaluado con honestidad.

#### B3 · Modelos basados en árboles — Ciclo: Modela
- **Competencia:** entrena árboles / ensembles; interpreta importancia de variables.
- **Contenidos:** árbol de decisión; random forest / boosting; hiperparámetros clave; importancia de features.
- **Ejercicio real:** sobre `compras_ml.csv`, modelar con árboles y leer "qué variables explican".
- **Entregable:** modelo + lectura de importancias.

#### B4 · Clasificación y clustering — Ciclo: Modela/Explora
- **Competencia:** clasifica (exactitud, matriz de confusión) y descubre grupos con K-Means.
- **Contenidos:** clasificación supervisada; matriz de confusión; K-Means; **escalado**; interpretación de clusters.
- **Ejercicio real:** predecir `tamano_proveedor` (Micro→Grande) desde cantidad y monto (exactitud ≈0,81) + clustering + `crosstab` (lección honesta: los clusters no calzan perfecto con las etiquetas).
- **Entregable de portafolio:** "segmentación de compras/proveedores" presentable.

#### B5 · Pipelines reproducibles — Ciclo: transversal Reproducibilidad
- **Competencia:** arma un `Pipeline` de sklearn (preproceso + modelo); versiona; separa datos/código.
- **Contenidos:** `Pipeline`/`ColumnTransformer`; estructura de proyecto; `requirements`; git básico; semillas; tests mínimos con `assert`; principios ONS de *reproducible code*.
- **Ejercicio real:** empaquetar el modelo de B3/B4 en un pipeline de datos crudos → predicción.
- **Entregable:** repo modelo, limpio y reproducible (`modelo_compras.joblib`).

#### B6 · Despliegue de modelos — Ciclo: Comunica & Despliega
- **Competencia:** expone un modelo guardado de forma usable (función de predicción, lote, validación) y entiende los cuidados de un despliegue real.
- **Contenidos:** serializar (`joblib`); función de predicción robusta; puntuación por lotes; validación de entradas; *model card* (uso previsto, límites, riesgos); idea de API/Gradio + monitoreo/reentrenamiento.
- **Ejercicio real:** puntuar **5 órdenes de compra nuevas** con el modelo de B5 y generar el CSV de predicciones.
- **✅ De-escalado (hecho):** el hands-on llega a "modelo usable" (función + lote + validación + CSV); la *producción* (API, monitoreo, reentrenamiento) queda a nivel **conceptual**. Reencuadre aplicado en el módulo (competencia y notebook).
- **Entregable de portafolio:** modelo usable + *model card*.

#### B7 · Series temporales (pronóstico) — Ciclo: Modela
- **Competencia:** descompone una serie, valida con partición temporal, pronostica con honestidad.
- **Contenidos:** tendencia/estacionalidad/ruido; pronósticos base (ingenuo, crecimiento medio, tendencia lineal); *hold-out/backtest*; (Prophet/ARIMA a nivel aplicado, opcional).
- **Ejercicio real:** **serie anual de gasto público (ChileCompra, 2019–2025; `gasto_anual.csv`)** → pronóstico defendible.
- **Entregable:** "pronóstico de gasto público".

> **Capstone B — *Predice y explica*** ✅ *construido* (`B8-capstone/`): **dataset provisto**
> (`compras_ml.csv`) + **scaffold** (problema → features → train/test → modela → evalúa en prueba →
> *model card*) + **ejemplo resuelto** (regresión `monto_total`, MAE en prueba ≈ $107.000) +
> **rúbrica**. Para institución que lo pida más extenso: ampliar a Propuesta → Análisis → Pitch.
> **Rúbrica (0–3 c/u, aprobado 12/18):** problema · features sin *leakage* · train/test con semilla ·
> modelo · evaluación honesta · model card. → **Certificación: Data Scientist del sector público.**

---

### CAPA C · IA APLICADA AL ESTADO — *"IA responsable con datos del Estado"* (C1–C3, opcional)

> Requisito recomendado: **A7** (IA generativa). Proveedor: **Gemini**, patrón en-vivo-o-caché.

> **🔬 Profundización (opcional):** **cada** módulo de la Capa C (C1–C3) tiene un `profundiza.ipynb`
> con la teoría a fondo (el *porqué*) + 4 ejercicios conceptuales auto-corregidos, **verificables sin
> conexión ni API key** (TF-IDF, coseno, enrutador por reglas). Construidos con el patrón de A5/A7 y
> **revisados adversarialmente por un agente experto en datos** (correctitud + pedagogía).

#### C1 · Introducción al NLP — Ciclo: Limpia/Modela
- **Competencia:** convierte texto en datos: limpia, vectoriza y clasifica/agrupa documentos.
- **Contenidos:** tokenización, *stopwords*, lematización (español); bolsa de palabras / TF-IDF; clasificación de texto; *topic modeling* básico; sesgos del lenguaje.
- **Ejercicio real:** **texto de licitaciones** → clasificar por rubro o detectar temas. (Su límite motiva A7/LLMs.)
- **Entregable:** "analizador de bases de licitación".

#### C2 · RAG (Retrieval-Augmented Generation) — Ciclo: Obtén/Modela
- **Competencia:** construye un RAG: indexa documentos, recupera y genera **citando la fuente**.
- **Contenidos:** *embeddings*; base vectorial simple; *chunking*; recuperación; generación con citas; evaluación de fidelidad.
- **Ejercicio real:** **RAG sobre normativa / fichas de compra** → "pregúntale a la normativa".
- **Entregable:** "buscador inteligente de normativa".

#### C3 · Agentes y proyecto integrador — Ciclo: los 6 pasos
- **Competencia:** diseña un agente que decide → actúa → responde usando herramientas, con traza auditable y guardrail de privacidad.
- **Contenidos:** qué es un agente y *tool use*; enrutador; "humano en el bucle"; riesgos, costos y gobernanza; integración de pronóstico (B7), clasificación (C1/A7) y RAG (C2).
- **Ejercicio real:** agente que, ante una pregunta de compras, elige la herramienta correcta y responde con fuentes.
- **Entregable de portafolio:** proyecto integrador de IA aplicada.

> **Capstone C — *Tu asistente con IA*** ✅ *construido* (`C4-capstone/`): **documentos provistos** +
> **scaffold** (propósito → recuperar con TF-IDF → responder citando la fuente → probar → ética) +
> **ejemplo resuelto** (RAG offline verificable) + **rúbrica**. LLM (Gemini) opcional, en-vivo-o-caché.
> **Rúbrica (0–3 c/u, aprobado 12/18):** propósito · recuperación · cita la fuente · pruebas · manejo
> del "no sé" · ética/privacidad. → **Especialización: IA aplicada al sector público.**

---

## 6. Mapa de competencias de salida

| Competencia | Se construye en | Se evalúa en |
|-------------|-----------------|--------------|
| Programar en Python para datos | P1–A1 | A1, Capstone A |
| Obtener datos (archivo, SQL, API/MCP) | P3, P4, A4, B1 | A4, B1, Capstone B |
| Cruzar y resumir tablas | A2 | A2, Capstone A |
| Limpiar y documentar supuestos | A3, B5 | A3, Capstone A/B |
| Explorar y describir con rigor | A1, A5 | A5, A6 |
| Visualizar y comunicar a no técnicos | A6, capstones | A6, Capstone A/B |
| Usar IA generativa con criterio | A7 | A7, Capstone A |
| Modelar (estadística + ML) | B2–B4, B7 | B3, B4, Capstone B |
| Reproducibilidad e ingeniería ligera | B5 (transversal) | B5, Capstone B |
| Desplegar un modelo usable | B6 | B6, Capstone B |
| Ética y uso responsable | A6 + transversal | A6, A7, capstones |
| RAG y agentes (especialización) | C1–C3 | C2, C3, Capstone C |

**Hitos/certificación:** (1) Capstone A → *Alfabetización de datos públicos*; (2) Capstone B →
*Data Scientist del sector público*; (3) Capstone C → *Especialización IA aplicada*.

---

## 7. Estándares de calidad por módulo (checklist "listo para publicar")

- [ ] `README.md` con presentación + botón **Open in Colab** (ruta = nombre real de carpeta).
- [ ] `leccion.ipynb`: teoría profunda estilo P1 (qué es, para qué, analogías, errores típicos) + **datos reales** desde la primera celda.
- [ ] Cada ejercicio cierra con **celda de chequeo** `assert` → ✅ / pista amable (sin pytest); los chequeos **recomputan lo esperado** (no son *gameable* con un número fijo).
- [ ] Al menos un ejercicio de **interpretación**, no solo de sintaxis (estilo A2: cruza → agrupa → decide; + reflexión no corregida).
- [ ] `solucion.ipynb` corre **4/4 ✅**; la lección con TODO da **4/4 ❌ amables sin romperse**.
- [ ] Módulos con API externa (P4, A7, C2, C3): patrón **en-vivo-o-caché**; chequeos validan estructura/relaciones.
- [ ] Declara **paso(s) del Ciclo Pública** y **competencia de salida**.
- [ ] **Fuente de datos citada correctamente** (ChileCompra/MercadoPúblico, MINSAL, CONAF, INE, CEN…).
- [ ] Nota/checklist **ético** cuando aplica (A6, A7, B4, B6, C1–C3).
- [ ] Licencia **CC BY 4.0**.

---

## 8. Decisiones: resueltas vs. abiertas

**Resueltas en esta v3:**
1. **Estructura escalonada** en 3 capas (resuelve la tensión upskilling vs. reconversión).
2. **Nomenclatura** capa+módulo; rutas Colab unificadas.
3. **A7 (IA generativa) en la Capa A** (alcanzable por todos) y base de la Capa C.
4. **Datos reales de ChileCompra** en la línea ML (B2–B6) y en A2; fuente citada correctamente.
5. **Proveedor LLM: Google Gemini** (`gemini-2.5-flash`), capa gratuita sin tarjeta.
6. **Puerta de entrada:** sitio **MkDocs Material → GitHub Pages**.

**Abiertas (impactan adopción, no contenido):**
1. **Modalidad: cohortes vs. siempre-abierto.** Recomendación del blueprint: **cohorte piloto** (una
   institución, ~30 personas, comunidad + sesión semanal opcional) → medir completitud antes de abrir.
2. ✅ **Capstones A, B y C construidos** (`A8-capstone/`, `B8-capstone/`, `C4-capstone/`) — las tres capas son terminables.
3. ✅ **Ejercicio de interpretación** (auto-verificado, estilo A2) agregado a A1, A3, A4, A5 y A6.
4. ✅ **B6 de-escalado** a conceptual (hands-on = modelo usable; producción = awareness).
5. **Hogar institucional de la certificación** (universidad asociada modelo MDataGov del ONS, CENIA,
   Lab. de Gobierno, Secretaría de Gobierno Digital, INE). *No bloqueante* para un proyecto libre,
   pero define si la certificación "vale" para carrera funcionaria.
6. **KPIs de impacto en el puesto** (no solo completitud): "¿aplicaste algo en tu trabajo?".

---

*Documento de diseño v3 · Formación Pública · estructura de 3 capas (Prework + A/B/C), 21 módulos.
La fuente de verdad es GitHub; Notion se actualiza después. CC BY 4.0.*
