# R3-CAP · Capstone — un asistente de IA para tu servicio

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-CAP-capstone-ia-aplicada/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, rúbrica comentada y autoevaluación.

Proyecto final de la rama R3: un **asistente de trámites** con RAG que responde **citando la
fuente**, se **abstiene** cuando no sabe y se **evalúa** con preguntas reales (hit@k). La
plantilla usa las 245 fichas de ChileAtiende (`fichas.csv`) como ejemplo; lo ideal es usar
**documentos o datos de tu propio servicio** (o el banco del bootcamp: `fichas`, `matricula`,
`aire_diario`, `reclamos`, `sismos`; o datos.gob.cl). Si tu corpus es tabular, el camino es el
agente de R3-04. Incluye **ficha de uso responsable** (riesgos y ética) y **rúbrica** con
criterios de Pertinencia y Riesgos/ética. Corre completo **sin clave ni red**.

- `leccion.ipynb` — plantilla con `TODO`; se autoverifica (✅). 4 chequeos.
- `profundiza.ipynb` — opcional 🔬: calibrar el umbral de abstención, filtrar por tema y
  bitácora de auditoría anonimizada. 3 chequeos.

*Fuente del corpus de ejemplo: fichas de trámites de [ChileAtiende](https://www.chileatiende.gob.cl).*
