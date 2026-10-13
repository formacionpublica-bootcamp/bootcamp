# R2-01 · Datos: traer, cruzar y limpiar

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-01-datos-traer-cruzar-limpiar/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Construye un dataset analítico limpio sobre la **calidad del aire**: cruza el PM2.5 diario de
14 estaciones SINCA 2020–2025 (`aire_diario.csv`, 30.674 filas) con su catálogo
(`estaciones.csv`: comuna, región, coordenadas), convierte las fechas, diagnostica los
**faltantes reales** (7 de 14 estaciones sin sensor meteorológico, 1.030 días sin PM2.5) y toma
decisiones de limpieza declaradas: duplicados de llave y humedades de 0 % imposibles (los 240
registros de humedad de Las Encinas Temuco son 0 %; 230 quedan tras descartar los días sin PM2.5).
La profundización transfiere el cruce a la matrícula 2025 por RBD (`matricula_rbd.csv`) ×
directorio MINEDUC (`directorio_establecimientos.csv`), con 4 huérfanas reales.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: llave única, inner vs left, huérfanas, imputar con categoría explícita.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
