# R3-04 · Agentes: herramientas, trazas y supervisión humana

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-04-agentes/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías y autoevaluación.

Un **agente** que recibe peticiones en lenguaje natural y usa **herramientas** (funciones de
Python) sobre datos reales de las otras dos ramas: **calidad del aire** SINCA
(`aire_diario.csv` + `estaciones.csv`, ancla de R2) y **matrícula escolar** MINEDUC
(`matricula.csv`, ancla de R1). El LLM **propone** el siguiente paso en JSON y el código lo
**valida**; si no hay clave o la propuesta es inválida, decide un **planificador de reglas**
determinista. Cada paso queda en una **traza**, hay **límite de pasos** y toda acción con efecto
(enviar una alerta, simulada) exige **aprobación humana**, denegada por defecto. Cierra con una
tabla de **riesgos** y mitigaciones. Funciona completo **sin clave ni red**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅). 6 chequeos.
- `profundiza.ipynb` — opcional 🔬: herramienta `buscar_ficha` sobre `fichas.csv` (el RAG de
  R3-03), medir el planificador, y guardas de argumentos, calidad del dato y privacidad. 5 chequeos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-04-agentes/profundiza.ipynb) ← profundización

*Fuentes: SINCA · Ministerio del Medio Ambiente (PM2.5 diario 2020–2025); MINEDUC · Resumen de
matrícula por establecimiento 2025; fichas de trámites de ChileAtiende.*
