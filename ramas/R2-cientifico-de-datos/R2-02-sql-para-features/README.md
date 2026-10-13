# R2-02 · SQL para *features*

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-02-sql-para-features/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Usar SQL no para *mirar* datos sino para **fabricar variables** (*features*) y armar una **tabla
analítica** lista para un modelo. El dato es el PM2.5 diario de 14 estaciones del SINCA,
2020–2025 (`aire_diario.csv`, 30.674 días-estación), cargado en SQLite: agregaciones por
estación y mes (`GROUP BY`), niveles de episodio del D.S. 12/2011 con `CASE WHEN` (alerta
80–109, preemergencia 110–169, emergencia ≥ 170 µg/m³), el PM2.5 de ayer y la media móvil de
la semana previa con funciones de ventana (`LAG`, `AVG OVER`) **sin fuga de información**, y la
tabla analítica por estación. La profundización transfiere el oficio a los 1.601 sismos
M ≥ 4,5 de Chile 2020–2025 (`sismos.csv`, catálogo USGS): *features* por zona y año, banderas,
días desde el sismo anterior y una CTE (`WITH`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: sismos reales por zona, `julianday` + `LAG`, CTE.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
