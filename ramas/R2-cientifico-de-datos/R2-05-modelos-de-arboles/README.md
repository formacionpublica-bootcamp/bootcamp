# R2-05 · Modelos basados en árboles

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-05-modelos-de-arboles/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.

**Árboles de decisión** y **bosques aleatorios** sobre el mismo problema de R2-04 — el PM2.5 de mañana
en Cerro Navia (`aire_diario.csv`, SINCA), con el mismo corte temporal — para comparar de forma justa
contra el baseline y la regresión lineal. Sobreajuste según la profundidad, **importancia de variables**
y el paso de la predicción a la **alerta** sobre la norma de 50 µg/m³. La profundización transfiere los
árboles a los sismos de Chile (`sismos.csv`, USGS): predecir la profundidad y descubrir la subducción.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: un árbol interpretable sobre sismos M ≥ 4,5 (2020–2025).
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.

*Fuentes: SINCA — Ministerio del Medio Ambiente; USGS — catálogo sísmico FDSN.*
