# D14 · Series temporales (pronóstico)

**Formación Pública — Bootcamp de Ciencia de Datos para funcionarios públicos**
Bloque avanzado · IA aplicada (opcional) · Semana 17

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B7-series-temporales/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

---

## De qué trata

Primer contacto con datos donde **el orden en el tiempo importa**. Trabajamos con el gasto público de Chile año a año (datos reales de ChileCompra) y aprendemos a **pronosticar**: estimar el futuro y, sobre todo, saber **cuánto confiar** en esa estimación.

## Qué vas a aprender

- Qué es una serie temporal y sus tres componentes: tendencia, estacionalidad y ruido.
- Cargar una serie real, graficarla y describir su tendencia con números (crecimiento año a año).
- Construir tres pronósticos base: **ingenuo**, **crecimiento medio** y **tendencia lineal**.
- **Validar** un pronóstico de forma honesta (hold-out / backtest) y elegir el mejor método.

**Competencia de salida:** dado un registro temporal real del Estado, producir un pronóstico defendible y justificar por qué es confiable.

## Contenido del módulo

| Archivo | Qué es |
|---|---|
| `leccion.ipynb` | La lección completa: teoría + 4 ejercicios con celdas de chequeo (✅ / ❌). |
| `solucion.ipynb` | Versión resuelta (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `gasto_anual.csv` | Dataset histórico de gasto anual acumulado de ChileCompra. |
| `README.md` | Esta presentación. |

## Cómo se usa

1. Pulsa **Open in Colab** arriba.
2. Lee cada sección y completa los `TODO`.
3. Ejecuta la **celda de chequeo** al final de cada ejercicio: muestra ✅ si está correcto o una pista amable si falta algo.
4. El módulo está completo cuando las **4 celdas de chequeo** muestran ✅.

## Datos y Fuente

- **Fuente:** Dirección de Compras y Contratación Pública (**ChileCompra** / MercadoPúblico) — indicador de monto acumulado del Estado (gasto anual en compras públicas, 2019–2025).
- **Dataset:** El archivo `gasto_anual.csv` ya viene guardado estáticamente en la carpeta del módulo. El notebook lo cargará automáticamente (cuenta con un descargador de respaldo para Google Colab).
- Dato ancla (coincide con M0): gasto 2025 = **$18.430.546.563.769 CLP**.

## Requisitos previos

Haber completado el núcleo del bootcamp (M0–D13). Se da por sabido `pandas`, `numpy` y `matplotlib`.

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: por qué la **validación es temporal** (sin barajar, sin fuga del futuro),
**tendencia/estacionalidad/ruido**, la **estacionariedad**, los **baselines ingenuos**, el **backtesting**
(*walk-forward*) y por qué la **incertidumbre crece con el horizonte**. Con 4 ejercicios conceptuales
auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B7-series-temporales/profundiza.ipynb)

---
*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
