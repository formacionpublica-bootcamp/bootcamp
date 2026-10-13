# R1-04 · Limpieza de datos

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-04-limpieza-de-datos/leccion.ipynb)

Dejar un dataset sucio listo para analizar: **diagnóstico** (`info`, `isna`, `duplicated`,
`value_counts`), **texto** (`.str.strip().str.title()`), **sinónimos** con diccionario
(`replace`/`map`), la **trampa del punto de miles** (`"2.425"` no es 2,425), **imposibles** a
`NaN` sin inventar, **duplicados**, una función `limpiar()` reutilizable y una **auditoría**
contra la fuente oficial.

**Datos.** `matricula_sucia.csv`: 1.545 establecimientos de la matrícula oficial 2025 (MINEDUC)
con errores típicos de planilla inyectados con semilla fija (regiones escritas de 23 formas,
dependencias abreviadas, rural como «Sí/No/0/1», comunas en MAYÚSCULAS con espacios, matrícula
como texto con «s/i» y punto de miles, -1 imposibles, 45 filas pegadas dos veces). Se audita
contra `matricula.csv` (cifra oficial) por RBD. La profundización usa `aire_nuevos.csv`:
PM2.5 diario de 14 estaciones SINCA, ene–sep 2026, con faltantes **reales**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: faltantes reales por estación, al azar vs en bloque, comparación justa, nota metodológica.
- [`GUIA_APRENDIZAJE.md`](GUIA_APRENDIZAJE.md) — pistas progresivas, errores frecuentes y autoevaluación.
