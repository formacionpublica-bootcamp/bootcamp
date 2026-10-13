# R3-02 · IA generativa y LLMs

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-02-ia-generativa-y-llms/leccion.ipynb)

Un **LLM** (Gemini, detrás de una sola función `preguntar_llm()`) sobre las fichas de
ChileAtiende (`fichas.csv`): prompts para **resumir en lenguaje claro** la ficha de la PGU,
**extraer requisitos como JSON** del Bono de Invierno con un parser y un validador propios,
**few-shot** para clasificar el tema, **temperatura y alucinación** (verificar los montos contra
la fuente), **verificación humana** y un **guardrail** que bloquea RUT. Funciona **sin clave y sin
red** (respuestas de respaldo); con una clave gratuita de aistudio.google.com guardada en los
Secretos de Colab, habla con el modelo en vivo. La profundización mide **fidelidad** y
**legibilidad** de un resumen y lo reescribe en **lectura fácil**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: cobertura, números no respaldados y lectura fácil.

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.
