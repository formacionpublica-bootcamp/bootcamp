# M4 · Limpieza de datos

Quinto módulo (tronco común) del **Bootcamp de Datos para Funcionarios Públicos — Formación Pública**.
Módulo compartido. Modalidad autoguiada, se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A3-limpieza-de-datos/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

## ¿Qué vas a aprender?
A dejar un dataset sucio listo para analizar: diagnosticar problemas (faltantes, duplicados, tipos), normalizar texto (`.str.strip()`, `.str.capitalize()`), convertir texto a número, resolver valores faltantes (`dropna`/`fillna`) y eliminar duplicados (`drop_duplicates`), todo empaquetado en una función de limpieza reutilizable.

## Datos
Caso conductor: **compras públicas (ChileCompra)**. Se usa una cifra real y actual — los **rubros más comprados por el Estado en 2026** con su monto bruto — tomada del portal oficial *Datos Abiertos* de la Dirección ChileCompra (datos-abiertos.chilecompra.cl). Se presenta como un *export crudo* con los defectos típicos de los datos autodeclarados (espacios, mayúsculas, monto como texto, un faltante y una fila duplicada). Las cifras son las oficiales reales.

## Contenido
- `leccion.ipynb` — teoría + ejercicios + celdas de chequeo (para el estudiante).
- `solucion.ipynb` — soluciones de referencia (uso interno).
- `profundiza.ipynb` — **notebook opcional de profundización teórica** (ver abajo).
- `profundiza_solucion.ipynb` — solución del profundiza (uso interno).
- `README.md` — esta presentación.

## Cómo se cursa
1. Abre `leccion.ipynb` con el botón **Open in Colab**.
2. Lee y ejecuta cada sección.
3. Resuelve los cinco ejercicios y ejecuta sus celdas de chequeo hasta ver ✅.

## 🔬 Profundización (opcional)
¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: por qué **limpiar no es neutral** (cada paso codifica un supuesto), los tres tipos de
dato faltante (**MCAR / MAR / MNAR**) y el **sesgo** que mete cada estrategia (**eliminar filas vs.
imputar media/mediana**), las **trampas de la normalización de texto** (siglas y categorías que se
funden), y la **procedencia / linaje** del dato y la reproducibilidad (*garbage in, garbage out*).
Con 4 ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A3-limpieza-de-datos/profundiza.ipynb)

## Licencia
Contenido bajo **CC BY 4.0**.
