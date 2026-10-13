# R2-07 · Evaluación y validación de modelos

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-07-evaluacion-y-validacion/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Evaluar un modelo con rigor sobre la **calidad del aire** (PM2.5 diario 2020–2025 de 14
estaciones SINCA, `aire_diario.csv`): ¿se supera mañana la norma de 50 µg/m³? Métricas
(precision/recall/F1) con clases desbalanceadas, **fuga de datos** (un promedio «centrado» que
mira el futuro), validación cruzada **barajada vs temporal** (`TimeSeriesSplit`: barajar una serie
de tiempo infla el desempeño) y **desempeño por estación**. La profundización transfiere a la
matrícula 2025 (`matricula.csv`, MINEDUC): ROC/AUC, umbral, calibración y recall por región.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: ROC/AUC, umbral, calibración y equidad por región.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
