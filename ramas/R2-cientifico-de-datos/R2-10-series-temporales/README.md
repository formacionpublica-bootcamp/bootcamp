# R2-10 · Series temporales *(optativo)*

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-10-series-temporales/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Datos donde **el orden en el tiempo importa**. Con el PM2.5 diario de la estación **Cerro Navia**
(`aire_diario.csv`, SINCA 2020–2025): serie con calendario completo, **remuestreo** semanal y
mensual, **media móvil**, **estacionalidad** anual y semanal, **descomposición**, y
**validación temporal** de pronósticos (ingenuo, ingenuo estacional, promedio estacional y una
regresión mes + tendencia). La prueba de fuego: enfrentar el método elegido a lo que de verdad
pasó en enero–septiembre de 2026 (`aire_nuevos.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: los **sismos** (`sismos.csv`, USGS M≥4,5) como conteo
  mensual. ¿Hay temporada sísmica? Un test ingenuo dice que sí; uno honesto, que no.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
