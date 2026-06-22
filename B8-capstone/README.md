# Capstone B · Predice y explica

**Proyecto final de la Capa B (Ciencia de datos aplicada)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B8-capstone/proyecto.ipynb)

## Qué es
Planteas un **problema predictivo**, entrenas un modelo, lo evalúas **con honestidad** (en datos de
prueba) y lo documentas con una **model card**. Integra todo lo de la Capa B.

## Cómo entregar
- **Opción A (recomendada):** dataset provisto `compras_ml.csv` (compras de alimentos reales de ChileCompra).
- **Opción B:** trae un CSV de **tu institución** con un objetivo a predecir.

## Los pasos
1. **Problema** — qué predices (regresión o clasificación) y con qué.
2. **Features y objetivo** — `X` e `y`, sin *leakage*.
3. **Train/test** — con semilla (reproducible).
4. **Modela** — entrena (empieza simple).
5. **Evalúa** — métrica en **prueba** (ej. MAE).
6. **Model card** — uso previsto, datos, límites, riesgos éticos.

## Rúbrica (0–3 c/u · aprobado 12/18)
| Criterio | Qué se evalúa |
|---|---|
| Problema bien planteado | Útil y respondible con los datos. |
| Features y objetivo | Correctos y sin *leakage*. |
| Train/test con semilla | Evaluación reproducible y honesta. |
| Modelo entrenado | Corre y predice. |
| Evaluación en PRUEBA | Mide en datos no vistos. |
| Model card | Documenta límites y ética. |

## Archivos
| Archivo | Para qué |
| --- | --- |
| `proyecto.ipynb` | Scaffold del estudiante (los pasos con TODO). |
| `ejemplo_resuelto.ipynb` | Ejemplo completo de referencia (uso interno / modelo). |
| `compras_ml.csv` | Dataset provisto: compras de alimentos reales de ChileCompra. |
| `README.md` | Esta portada + rúbrica. |

→ Al aprobarlo, junto con el resto de la Capa B, obtienes la **certificación: Data Scientist del
sector público**.

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Dirección ChileCompra (datos-abiertos.chilecompra.cl)
