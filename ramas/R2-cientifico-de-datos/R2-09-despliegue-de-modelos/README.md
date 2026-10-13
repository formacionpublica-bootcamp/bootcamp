# R2-09 · Despliegue, ficha de modelo y monitoreo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-09-despliegue-de-modelos/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Un modelo en un cuaderno no le sirve a nadie. Se reconstruye un **pronóstico de PM2.5 del día
siguiente** (14 estaciones SINCA, `aire_diario.csv` 2020–2025), se guarda con `joblib` y se
**despliega**: función de predicción con **validación de entrada**, **puntuación por lotes** con
faltantes reales, **entregable CSV**, y luego se pone en **producción** sobre `aire_nuevos.csv`
(enero–septiembre de 2026, datos que el modelo nunca vio): **monitoreo** de desempeño con
comparación justa, ***drift*** de faltantes y **ficha de modelo** honesta. Interfaz Gradio opcional.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: monitoreo **por estación** (dónde se degrada y por qué) y
  **umbral de alerta** elegido en 2025 y evaluado en 2026.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
- El cuaderno crea `modelo_pm25.joblib` y `predicciones_pm25_2026.csv` en la carpeta de trabajo
  (no se versionan).
