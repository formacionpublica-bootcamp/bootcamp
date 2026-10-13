# R2-06 · Clasificación y clustering

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-06-clasificacion-y-clustering/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Los dos grandes tipos de aprendizaje sobre la **calidad del aire** (PM2.5 diario 2020–2025 de 14
estaciones SINCA, `aire_diario.csv` + `estaciones.csv`). **Clasificación:** ¿mañana se supera
la norma de 50 µg/m³? — clases desbalanceadas (≈4 % de días sobre la norma), la trampa de la
exactitud, matriz de confusión, precisión vs recall y qué error es más caro para la autoridad
sanitaria. **Clustering:** K-Means sobre el perfil mensual estandarizado de cada estación, que
separa solo a Temuco, a las estaciones del centro y a las del norte/costa. La profundización
transfiere la clasificación a reclamos SERNAC 2011 (`reclamos.csv`, dato histórico) con one-hot.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: one-hot, línea base y desbalance multiclase con reclamos.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
