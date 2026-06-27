# Capstone A · Tu pregunta, tus datos

**Proyecto final de la Capa A (Datos sin miedo)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A8-capstone/proyecto.ipynb)

## Qué es
Tu primera pieza de portafolio: **eliges una pregunta pública, la respondes con datos reales y la
comunicas**. Integra todo lo de la Capa A (pandas, cruzar y resumir, limpieza, estadística,
visualización y ética, e IA como copiloto). No hay una respuesta única.

## Cómo entregar
- **Opción A (recomendada para partir):** usa el dataset provisto `compras_capstone.csv` (órdenes de
  compra reales de ChileCompra).
- **Opción B:** trae un CSV de **tu propia institución** y cámbialo en la celda de carga.

## Los 6 pasos (Ciclo Pública)
1. **Pregunta** — una pregunta concreta y pública.
2. **Limpia** — deja la tabla lista (`df_limpio`).
3. **Explora y responde** — `groupby`/`value_counts`/estadística → `respuesta`.
4. **Comunica** — un gráfico honesto (título, ejes, fuente).
5. *(Opcional)* **IA como copiloto** — redactar y **verificar** con un LLM.
6. **Conclusión y reflexión** — hallazgo, qué le dirías a tu jefatura y qué **no** concluir.

## Rúbrica (0–3 cada una · aprobado 12/18)
| Criterio | Qué se evalúa |
|---|---|
| Pregunta clara y pública | Es concreta y respondible con los datos. |
| Datos bien tratados | Revisó nulos/tipos/texto; documentó. |
| Análisis válido | El cálculo responde de verdad la pregunta. |
| Visualización honesta | Clara, rotulada, sin engañar. |
| Conclusión accionable | Dice algo útil para una jefatura. |
| Reflexión / ética | Reconoce límites y qué no concluir. |

## Archivos
| Archivo | Para qué |
| --- | --- |
| `proyecto.ipynb` | El scaffold del estudiante (los 6 pasos con TODO). |
| `ejemplo_resuelto.ipynb` | Un ejemplo completo de referencia (uso interno / modelo). |
| `compras_capstone.csv` | Dataset provisto: órdenes de compra reales de ChileCompra. |
| `README.md` | Esta portada + rúbrica. |

## Datos
Órdenes de compra de licitaciones de **ChileCompra / MercadoPúblico** (datos-abiertos.chilecompra.cl):
`codigo_oc`, `fecha`, `mes`, `organismo`, `region`, `rubro`, `proveedor`, `monto`. Es una **muestra
de licitaciones** (no incluye convenio marco ni trato directo): sirve para aprender, no para juzgar
a un organismo.

→ Al aprobarlo obtienes la **certificación de Alfabetización de datos públicos** (Capa A).

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Dirección ChileCompra (datos-abiertos.chilecompra.cl)
