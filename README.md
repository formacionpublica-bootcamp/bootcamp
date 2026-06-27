> ## 🆕 Rediseño en 3 ramas independientes
>
> El curso se reorganizó en **3 ramas autocontenidas** (elige una según tu rol), en [`ramas/`](ramas/):
> - **R1 · Análisis y Visualización de Datos** — `ramas/R1-analisis-visualizacion/`
> - **R2 · Científico de Datos** — `ramas/R2-cientifico-de-datos/`
> - **R3 · IA Aplicada** — `ramas/R3-ia-aplicada/`
>
> El curso anterior (Prework + Capa A/B/C) quedó archivado en [`legacy/`](legacy/) y respaldado en la rama `curso-v1-legacy`.

# Formación Pública — Datos para funcionarios públicos

Bootcamp **gratuito, autoguiado y práctico** de datos para funcionarios públicos chilenos que
**parten desde cero** (sin programación previa). El objetivo es **upskilling**: usar datos —y luego
IA— para hacer mejor tu trabajo. Todo se ejecuta en **Google Colab** (solo necesitas una cuenta de
Google), con datos públicos reales (compras públicas de ChileCompra/MercadoPúblico) y ejercicios
auto-corregidos.

> **Syllabus completo** (módulo por módulo, benchmark y método): [SYLLABUS.md](SYLLABUS.md) ·
> Diseño y razonamiento del rediseño: [BLUEPRINT_FORMACION_PUBLICA.md](BLUEPRINT_FORMACION_PUBLICA.md).

---

## Cómo está organizado: 3 pistas escalonadas

El programa **no es un solo camino largo**. Son tres pistas independientes, cada una con su propio
certificado y su proyecto final (*capstone*). **Terminar la Pista A ya es un logro completo.**

| Pista | Para quién | Duración realista | Qué te llevas |
|---|---|---|---|
| **A · Datos sin miedo** | **Todos** los funcionarios. El corazón del bootcamp. | ~6 sem · 4–5 h/sem | Responder preguntas con datos reales, limpiar tablas, consultar con SQL, hacer un gráfico honesto y usar IA con criterio. |
| **B · Ciencia de datos aplicada** *(opcional)* | Quien quiere modelar y predecir. | ~6 sem · 6–8 h/sem | Entrenar y evaluar modelos de ML, armar pipelines reproducibles. *Esto ya es un paso hacia un rol nuevo.* |
| **C · IA aplicada al Estado** *(opcional)* | Quien quiere construir con IA generativa. | ~5 sem · 6–8 h/sem | Resolver tareas de texto con LLMs, dar tus propios documentos a un LLM (RAG) y encadenar agentes. |

**Honestidad de cada pista:** la Pista A **no** te convierte en data scientist, y está perfecto:
te convierte en alguien que ya no le teme a los datos. Las Pistas B y C son para quien quiere más.

---

## Prework · Lo mínimo de Python para sobrevivir

No es un curso de programación: es lo justo para llegar rápido a pandas y SQL.

| Módulo | Tema |
|---|---|
| [P1](P1-setup-y-sintaxis/) | Setup y sintaxis de Python |
| [P2](P2-colecciones-y-bucles/) | Colecciones y bucles |
| [P3](P3-funciones-y-archivos/) | Funciones y lectura de archivos |
| [P4](P4-datos-web-json-apis/) | Datos desde la web: JSON y APIs *(opcional)* |

---

## Pista A · Datos sin miedo *(alfabetización — para todos)*

| Sem | Módulo | Tema | Entregable |
|---|---|---|---|
| 1 | [A1](A1-exploracion-con-pandas/) | Exploración con pandas | Top 10 organismos por gasto |
| 2 | [A2](A2-cruzar-y-resumir-tablas/) | Cruzar y resumir tablas (`merge` + `groupby`) | Gasto por sector cruzando dos tablas |
| 3 | [A3](A3-limpieza-de-datos/) | Limpieza de datos | Dejar un CSV sucio usable |
| 4 | [A4](A4-sql-fundamentos/) | SQL fundamentos | Responder 3 preguntas con consultas |
| 5 | [A5](A5-estadistica-descriptiva/) | Estadística descriptiva (no dejarse engañar) | Confirmar/desmentir un titular |
| 6 | [A6](A6-visualizacion-y-etica/) | Visualización y ética de datos | Un gráfico claro y honesto |
| 7 | [A7](A7-ia-generativa-y-llms/) | IA como copiloto (LLMs, uso responsable) | Clasificar glosas con un LLM, verificando |
| — | [Capstone A](A8-capstone/) | **Tu pregunta, tus datos** (dataset provisto + el tuyo) | Proyecto + rúbrica → certificación Capa A |

> A7 (IA generativa) cierra la Capa A como alfabetización de IA para todos, y la Capa C la retoma como base de RAG y agentes.

---

## Pista B · Ciencia de datos aplicada *(opcional)*

| Módulo | Tema |
|---|---|
| [B1](B1-sql-para-features/) | SQL para *features* |
| [B2](B2-fundamentos-de-ml/) | Fundamentos de Machine Learning |
| [B3](B3-modelos-de-arboles/) | Modelos basados en árboles |
| [B4](B4-clasificacion-y-clustering/) | Clasificación y clustering |
| [B5](B5-pipelines-reproducibles/) | Pipelines reproducibles |
| [B6](B6-despliegue-de-modelos/) | Despliegue de modelos *(práctico: modelo usable · producción: conceptual)* |
| [B7](B7-series-temporales/) | Series temporales (pronóstico) |
| [Capstone B](B8-capstone/) | **Predice y explica**: proyecto predictivo + *model card* + rúbrica |

---

## Pista C · IA aplicada al Estado *(opcional)*

| Módulo | Tema |
|---|---|
| [C1](C1-introduccion-al-nlp/) | Introducción al NLP |
| [A7](A7-ia-generativa-y-llms/) | IA generativa y LLMs *(compartido con Pista A; aquí se profundiza)* |
| [C2](C2-rag/) | RAG (Retrieval-Augmented Generation) |
| [C3](C3-agentes/) | **Agentes y proyecto integrador de IA aplicada** *(cierre)* |
| [Capstone C](C4-capstone/) | **Tu asistente con IA**: RAG que responde citando la fuente + rúbrica |

---

## Cómo empezar

1. Abre el módulo por el que partas (Prework → Pista A).
2. Pulsa **Open in Colab** en el `README` del módulo.
3. Ejecuta las celdas en orden y completa cada `# TODO`.
4. Cada ejercicio termina en una **celda de chequeo**: ✅ si está bien, o una pista amable.
5. El módulo está completo cuando todas las celdas de chequeo muestran ✅.

> **¿Te trancaste?** Es normal y parte del oficio. Lee el error completo, y si no lo entiendes,
> **pégaselo a la IA junto con tu código** (Gemini/ChatGPT) y pídele que te explique qué significa
> y cómo arreglarlo — **sin pegar datos personales**.

---

## Estado del programa

- ✅ Prework (P1–P4) y Capa A (A1–A7) — construidos, en revisión.
- ✅ Capa B (B1–B7) — construida, en revisión; **línea ML (B2–B6) sobre datos reales de compras públicas** (`data/process_licitaciones.py` → `compras_ml.csv`).
- ✅ Capa C (C1–C3) — construida, en revisión.
- ✅ Módulos renombrados a nomenclatura **capa+módulo**; rutas *Open in Colab* y de descarga corregidas; fuente citada como **ChileCompra**; crudos de `data/` excluidos de Git.
- ✅ **Sitio web** en MkDocs Material (`docs/`) con despliegue automático a GitHub Pages (`.github/workflows/deploy.yml`).
- ✅ **Capstones A, B y C** construidos (`A8-capstone/`, `B8-capstone/`, `C4-capstone/`): dataset provisto + scaffold + ejemplo resuelto + rúbrica cada uno. Las **3 capas son terminables**.
- ✅ **[Recursos/](Recursos/)**: chuleta (Python + pandas + SQL) y glosario (~50 términos). También en el sitio, menú *Recursos*.
- ✅ **Pulido aplicado:** ejercicio de interpretación auto-verificado en A1/A3/A4/A5/A6; B6 de-escalado a conceptual; fuente "DIPRES" corregida a ChileCompra en todos los notebooks; refuerzo de texto en P1.
- ✅ **Profundización (opcional)** en toda la Capa A (A1–A7): un `profundiza.ipynb` por módulo (teoría a fondo + 4 ejercicios conceptuales), revisado adversarialmente por un agente experto en datos.

---

*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) · Formación Pública.*
