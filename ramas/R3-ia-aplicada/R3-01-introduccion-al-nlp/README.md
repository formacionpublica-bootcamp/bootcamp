# R3-01 · Introducción al NLP

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-01-introduccion-al-nlp/leccion.ipynb)

Primer contacto con el **texto como dato**, sobre las **245 fichas de trámites de ChileAtiende**
(`fichas.csv`): normalizar, tokenizar, quitar *stopwords*, contar frecuencias, representar con
**TF-IDF** y entrenar un **clasificador del tema** de cada ficha (train/test estratificado,
regresión logística, línea base) — para terminar **leyendo sus errores**. La profundización
transfiere el pipeline al texto corto de **reclamos SERNAC 2011** (`reclamos.csv`: producto →
mercado), donde la exactitud global esconde a las clases pequeñas.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: clases con pocos ejemplos, recall por clase y el límite del texto.

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.
