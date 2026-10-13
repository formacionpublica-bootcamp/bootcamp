# R2-08 · Pipelines reproducibles

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-08-pipelines-reproducibles/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Empaqueta preprocesamiento + modelo en un solo objeto sobre la **calidad del aire** (PM2.5 y
meteorología diarios 2020–2025 de 14 estaciones SINCA, `aire_diario.csv`): `ColumnTransformer`
(imputar la meteorología que 6 estaciones no miden, escalar, one-hot de la estación) + bosque
aleatorio en un `Pipeline`, validación temporal sin fugas, una función `entrenar()` con semilla
(reproducible) y persistencia con `joblib` (`modelo_aire.joblib`, que crea el propio notebook).
La profundización transfiere a la matrícula 2025 (`matricula.csv`, MINEDUC): pipeline con dos
categóricas y una categoría nunca vista.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: pipeline categórico con matrícula, línea base y `handle_unknown`.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
