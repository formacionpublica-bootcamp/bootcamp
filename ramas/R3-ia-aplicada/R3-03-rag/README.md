# R3-03 · RAG: tu asistente de trámites que cita la fuente

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-03-rag/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías y autoevaluación.

RAG sobre el corpus completo de **245 fichas de trámites de ChileAtiende** (`fichas.csv`):
trocear (por subtítulos `## ` y por tamaño), índice léxico **TF-IDF**, recuperación top-k,
prompt aumentado con **citas** (id y url de la ficha), generación con `preguntar_llm()` y
**abstención** en dos barreras. Cierra **midiendo** la recuperación con 20 preguntas reales
(hit@k). Funciona **sin clave ni red**: sin `GEMINI_API_KEY`, el LLM devuelve un respaldo
extractivo y todos los chequeos pasan igual.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅). 6 chequeos.
- `profundiza.ipynb` — opcional 🔬: mejorar la recuperación (peso del título, n-gramas de
  palabras y de caracteres, tamaño de trozo) **midiendo** cada cambio. 5 chequeos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-03-rag/profundiza.ipynb) ← profundización

*Fuente de datos: fichas de trámites de [ChileAtiende](https://www.chileatiende.gob.cl) (contenido público del Estado de Chile).*
