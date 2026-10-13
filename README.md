# Formación Pública — Datos e IA para funcionarios públicos

Bootcamp **gratuito, autoguiado y práctico** de datos e IA para funcionarios públicos chilenos que
**parten desde cero** (sin programación previa). El objetivo es **upskilling**: usar datos —y luego
IA— para hacer mejor tu trabajo. Todo se ejecuta en **Google Colab** (solo necesitas una cuenta de
Google), con **datos públicos chilenos reales** y ejercicios autocorregidos.

> 🌐 Campus: **[formacionpublica.cl/campus.html](https://formacionpublica.cl/campus.html)** ·
> Datos y procedencia: [data/README.md](data/README.md) ·
> Modo tutor de IA: [TUTOR_IA.md](TUTOR_IA.md)

**Datos ancla por rama** (un dataset en todas las lecciones de la rama; cada `profundiza` cambia de
dataset para practicar la transferencia):

| Rama | Dataset ancla | Fuente |
|---|---|---|
| R1 | Matrícula escolar 2025: 10.945 establecimientos | MINEDUC, datos abiertos |
| R2 | Calidad del aire: PM2.5 + meteorología, 14 estaciones, 2020–2025, y 2026 como datos nuevos | SINCA, Ministerio del Medio Ambiente |
| R3 | 245 fichas de trámites con texto completo | ChileAtiende |

---

## Cómo está organizado: 3 ramas independientes

El programa **no es un solo camino largo**: son **tres ramas autocontenidas** en [`ramas/`](ramas/).
Eliges **una** según tu rol — no hay prerrequisitos entre ellas, cada una parte de cero y se
certifica por separado.

| Rama | Para quién | Duración | Qué te llevas |
|---|---|---|---|
| [**R1 · Análisis y Visualización**](ramas/R1-analisis-visualizacion/) | Quien quiere responder preguntas con datos y comunicarlas. **El punto de partida para la mayoría.** | ~10–12 sem | Conseguir, limpiar y cruzar datos reales, SQL, estadística para no engañarse, gráficos honestos y un dashboard. *No incluye ML.* |
| [**R2 · Científico de Datos**](ramas/R2-cientifico-de-datos/) | Quien quiere modelar y predecir. | ~16–18 sem | El ciclo completo: preparar datos, entrenar y evaluar modelos con honestidad, pipelines reproducibles y despliegue responsable. *Esto ya es un paso hacia un rol nuevo, no solo upskilling del puesto actual.* |
| [**R3 · IA Aplicada**](ramas/R3-ia-aplicada/) | Quien quiere construir con IA generativa. | ~6–7 sem | Resolver tareas de texto con LLMs, RAG que responde **citando la fuente** y agentes con supervisión humana. Entrada directa con prueba de nivel. |

**Honestidad de cada rama:** en la portada de cada una se dice qué te llevas **y qué no**. Terminar
R1 ya es un logro completo: te convierte en alguien que no le teme a los datos.

## Rama R1 · Análisis y Visualización de Datos

| Módulo | Tema |
|---|---|
| [R1-00](ramas/R1-analisis-visualizacion/R1-00-fundamentos/) | Fundamentos: Python con datos reales |
| [R1-01](ramas/R1-analisis-visualizacion/R1-01-traer-el-dato/) | Traer el dato: archivos, JSON y APIs |
| [R1-02](ramas/R1-analisis-visualizacion/R1-02-exploracion-con-pandas/) | Exploración con pandas |
| [R1-03](ramas/R1-analisis-visualizacion/R1-03-cruzar-y-resumir-tablas/) | Cruzar y resumir tablas |
| [R1-04](ramas/R1-analisis-visualizacion/R1-04-limpieza-de-datos/) | Limpieza de datos |
| [R1-05](ramas/R1-analisis-visualizacion/R1-05-sql-para-analisis/) | SQL para análisis |
| [R1-06](ramas/R1-analisis-visualizacion/R1-06-estadistica-descriptiva/) | Estadística descriptiva (no dejarse engañar) |
| [R1-07](ramas/R1-analisis-visualizacion/R1-07-visualizacion-exploratoria/) | Visualización exploratoria — ver para entender |
| [R1-08](ramas/R1-analisis-visualizacion/R1-08-visualizacion-comunicar-etica/) | Visualización para comunicar + ética |
| [R1-09](ramas/R1-analisis-visualizacion/R1-09-dashboards-ligeros/) | Dashboards ligeros (Gradio) |
| [R1-CAP](ramas/R1-analisis-visualizacion/R1-CAP-capstone-analisis/) | **Capstone**: informe/dashboard con datos de tu organismo → certificación *Analista de Datos del sector público* |

## Rama R2 · Científico de Datos

| Módulo | Tema |
|---|---|
| [R2-00](ramas/R2-cientifico-de-datos/R2-00-fundamentos-express/) | Fundamentos express: Python + pandas |
| [R2-01](ramas/R2-cientifico-de-datos/R2-01-datos-traer-cruzar-limpiar/) | Datos: traer, cruzar, limpiar |
| [R2-02](ramas/R2-cientifico-de-datos/R2-02-sql-para-features/) | SQL para *features* |
| [R2-03](ramas/R2-cientifico-de-datos/R2-03-estadistica-para-modelar/) | Estadística para modelar |
| [R2-04](ramas/R2-cientifico-de-datos/R2-04-fundamentos-de-ml/) | Fundamentos de Machine Learning |
| [R2-05](ramas/R2-cientifico-de-datos/R2-05-modelos-de-arboles/) | Modelos basados en árboles |
| [R2-06](ramas/R2-cientifico-de-datos/R2-06-clasificacion-y-clustering/) | Clasificación y clustering |
| [R2-07](ramas/R2-cientifico-de-datos/R2-07-evaluacion-y-validacion/) | Evaluación y validación (métricas, fuga de datos, CV, fairness) |
| [R2-08](ramas/R2-cientifico-de-datos/R2-08-pipelines-reproducibles/) | Pipelines reproducibles |
| [R2-09](ramas/R2-cientifico-de-datos/R2-09-despliegue-de-modelos/) | Despliegue + ficha de modelo + monitoreo |
| [R2-10](ramas/R2-cientifico-de-datos/R2-10-series-temporales/) | Series temporales *(optativa)* |
| [R2-CAP](ramas/R2-cientifico-de-datos/R2-CAP-capstone-modelo/) | **Capstone**: modelo predictivo de punta a punta → certificación en ciencia de datos aplicada al sector público |

## Rama R3 · IA Aplicada

| Módulo | Tema |
|---|---|
| [R3-00](ramas/R3-ia-aplicada/R3-00-onramp-express-prueba-nivel/) | Onramp express: Python + JSON *(o entra directo con la prueba de nivel)* |
| [R3-01](ramas/R3-ia-aplicada/R3-01-introduccion-al-nlp/) | Introducción al NLP |
| [R3-02](ramas/R3-ia-aplicada/R3-02-ia-generativa-y-llms/) | IA generativa y LLMs |
| [R3-03](ramas/R3-ia-aplicada/R3-03-rag/) | RAG: tu asistente que cita la fuente |
| [R3-04](ramas/R3-ia-aplicada/R3-04-agentes/) | Agentes (con supervisión humana) |
| [R3-CAP](ramas/R3-ia-aplicada/R3-CAP-capstone-ia-aplicada/) | **Capstone**: proyecto integrador de IA aplicada → certificación *Especialista en IA aplicada del sector público* |

---

## Cómo empezar

1. Elige tu rama (¿dudas? parte por **R1**) y abre su primer módulo.
2. Pulsa **Open in Colab** en el `README` del módulo.
3. Ejecuta las celdas en orden y completa cada `# TODO`.
4. Cada ejercicio termina en una **celda de chequeo**: ✅ si está bien, o una pista amable.
5. El módulo está completo cuando todas las celdas de chequeo muestran ✅.

**Cada módulo trae una [Guía de Aprendizaje]** (`GUIA_APRENDIZAJE.md` en su carpeta): el mapa del
módulo con analogías de Excel, pistas progresivas por ejercicio, errores frecuentes y autoevaluación.

> **¿Te trancaste?** Es normal y parte del oficio. Tu escalera de ayuda, en orden:
> 1. La **`GUIA_APRENDIZAJE.md`** del módulo (en su misma carpeta): pistas progresivas 🟢🟡🔴,
>    errores frecuentes y autoevaluación.
> 2. **Gemini dentro de Colab** (botón ✨): pégale el error completo junto con tu código y pídele
>    que te explique qué significa — **sin pegar datos personales**.
> 3. **[Antigravity como tutor de IA](GUIA_GRAVITY.md)** *(opcional)*: un IDE gratuito de Google
>    con un asistente que ve todo el curso y, con el modo tutor ([TUTOR_IA.md](TUTOR_IA.md)),
>    te da pistas en vez de resolverte los ejercicios.

## Certificación y capstone

Cada rama cierra con un **capstone sobre datos de tu propio organismo** (o el dataset provisto),
evaluado con **rúbrica pública** (está en el README de cada capstone). Al aprobarlo obtienes la
certificación de la rama; tu **portafolio en GitHub es la credencial real**. Si usas datos de tu
institución: **anonimiza antes** de subirlos o de pasarlos por un LLM.

## Recursos y mantención

- [**Recursos/**](Recursos/): chuleta de Python + pandas + SQL y glosario (~50 términos).
- **Verificación automática** ([`notebooks.yml`](.github/workflows/notebooks.yml)): en cada cambio y
  cada lunes se ejecutan todas las soluciones (`solucion.ipynb` y `profundiza_solucion.ipynb`), y el
  build falla si una celda de chequeo da ❌. Localmente: `python tools/run_notebooks.py`.
- **Datos al día** ([`fuentes.yml`](.github/workflows/fuentes.yml)): cada mes se revisa que las
  fuentes oficiales respondan y si MINEDUC publicó un año nuevo. Para regenerar todo:
  `python tools/make_datasets.py todo` (ver [data/README.md](data/README.md)).
- **Los notebooks no se editan a mano**: se generan con `tools/build_<módulo>.py` a partir de los
  helpers de [`tools/build_helpers.py`](tools/build_helpers.py). Para cambiar un ejercicio, edita su
  builder, ejecútalo y verifica.
- **LLM (R3):** `preguntar_llm()` usa Gemini con el SDK `google-genai`. El modelo se define en
  `build_helpers.GEMINI_MODEL` y cada persona puede cambiarlo con `GEMINI_MODEL`. Sin clave, los
  notebooks corren igual con respuestas de respaldo.
- El curso v1 (Prework + Capas A/B/C) se conserva en la rama `curso-v1-legacy`.

---

*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es) · Formación Pública.*
