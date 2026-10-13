# R2-04 · Fundamentos de Machine Learning

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-04-fundamentos-de-ml/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.

Tu primer modelo: **pronosticar el PM2.5 de mañana** en Cerro Navia con temperatura, humedad, mes,
día de la semana y el PM2.5 de ayer (`aire_diario.csv`, SINCA). Aprendizaje supervisado, *feature*
de rezago, **corte temporal** (entrenar 2020–2024, probar 2025), **baseline** «mañana = hoy»,
regresión lineal con `fit`/`predict`, **MAE** honesto y un pronóstico nuevo. La profundización
transfiere el método a la matrícula 2025 (`matricula.csv`): predecir cursos y cazar la **fuga de datos**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: corte aleatorio vs temporal, coeficientes y fuga de datos.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.

*Fuentes: SINCA — Ministerio del Medio Ambiente; MINEDUC — datos abiertos (matrícula 2025).*
