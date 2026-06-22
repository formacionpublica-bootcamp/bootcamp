# Capstone C · Tu asistente con IA

**Proyecto final de la Capa C (IA aplicada al Estado)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C4-capstone/proyecto.ipynb)

## Qué es
Construyes un **asistente RAG** que responde preguntas sobre documentos públicos **citando la fuente**
(para no inventar). Integra C1 (NLP / TF-IDF), A7 (LLMs) y C2 (RAG).

## Cómo entregar
- **Opción A (recomendada):** `documentos.csv` provisto (resúmenes referenciales de compras públicas).
- **Opción B:** trae tus propios documentos (CSV con `titulo`, `texto`, `fuente`).

## Los pasos
1. **Propósito** — qué preguntas atenderá tu asistente.
2. **Recuperar** — buscador TF-IDF que encuentra el documento relevante.
3. **Responder citando** — devuelve el contenido + la fuente (LLM opcional con `GEMINI_API_KEY`).
4. **Probar** — varias preguntas.
5. **Ética** — manejo del "no sé", alucinaciones y privacidad.

## Funciona sin conexión
La recuperación (TF-IDF) corre **offline y es verificable**. La redacción con LLM (Gemini) es
**opcional** y sigue el patrón **en-vivo-o-caché**.

## Rúbrica (0–3 c/u · aprobado 12/18)
| Criterio | Qué se evalúa |
|---|---|
| Propósito claro | El asistente tiene un foco acotado. |
| Recuperación funciona | Encuentra el documento correcto. |
| Cita la fuente | Nunca responde sin indicar de dónde sale. |
| Prueba con varias preguntas | Demuestra que funciona. |
| Manejo del "no sé" | Reconoce baja similitud / falta de cobertura. |
| Ética y privacidad | Reflexiona sobre riesgos y datos personales. |

## Archivos
| Archivo | Para qué |
| --- | --- |
| `proyecto.ipynb` | Scaffold del estudiante (los pasos con TODO). |
| `ejemplo_resuelto.ipynb` | Ejemplo completo de referencia (uso interno / modelo). |
| `documentos.csv` | Documentos provistos (resúmenes referenciales de compras públicas). |
| `README.md` | Esta portada + rúbrica. |

> **Nota:** los documentos son **resúmenes educativos referenciales**, no el texto legal oficial. La
> fuente autoritativa es la normativa de compras públicas y chilecompra.cl.

→ Al aprobarlo obtienes la **Especialización: IA aplicada al sector público**.

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** elaboración propia referencial sobre ChileCompra.
