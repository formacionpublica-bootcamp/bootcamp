# D17 · RAG (Retrieval-Augmented Generation)

**Formación Pública — Bootcamp de Ciencia de Datos para funcionarios públicos**
Bloque avanzado · IA aplicada (opcional) · Semana 20

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C2-rag/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

---

## De qué trata

RAG resuelve el gran problema de los LLM (memoria limitada + alucinaciones): en vez de confiar en lo que el modelo "recuerda", **primero busca los documentos relevantes** y se los entrega para que responda **basándose en ellos** y cite la fuente. Aquí construyes un RAG completo sobre una **ficha de licitación real**.

## Qué vas a aprender

- El problema que RAG resuelve y la analogía del "examen con libro abierto".
- Las tres piezas: **recuperar → aumentar → generar**.
- Hacer que el modelo responda **solo con tus documentos** (*grounding*).
- Que **reconozca cuándo no sabe** y se **abstenga** en vez de inventar.

**Competencia de salida:** construir un sistema de preguntas y respuestas sobre documentos reales del Estado, con respuestas fundamentadas y honestas.

## Cómo está construido

- **Base de conocimiento:** fragmentos reales de la ficha de licitación **2239-8-LR25**. *Fuente oficial: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico)* — criterios de evaluación, garantías, plazos, duración del contrato.
- **Recuperación:** búsqueda léxica por palabras en común (reutiliza el NLP de D15). Se menciona el siguiente nivel (*embeddings*).
- **Generación:** Google Gemini (`gemini-2.5-flash`) con el patrón **"en vivo o caché"** de D16.

## Funciona en vivo o en caché

- **Con API key** (`GEMINI_API_KEY` en los Secrets de Colab): genera con Gemini en vivo.
- **Sin API key / sin conexión:** usa respuestas en caché. Los 4 ejercicios se completan igual.

## Contenido del módulo

| Archivo | Qué es |
|---|---|
| `leccion.ipynb` | La lección completa: teoría + 4 ejercicios con celdas de chequeo (✅ / ❌). |
| `solucion.ipynb` | Versión resuelta (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `README.md` | Esta presentación. |
| `licitacion.csv` | Dataset estático con fragmentos reales de la licitación. |

## Cómo se usa

1. Pulsa **Open in Colab** arriba.
2. (Opcional) Configura tu `GEMINI_API_KEY` en los Secrets de Colab.
3. Completa los `TODO` y ejecuta las **celdas de chequeo** (✅ o pista amable).
4. El módulo está completo cuando las **4 celdas de chequeo** muestran ✅.

## Requisitos previos

D15 (NLP, para la recuperación) y D16 (LLMs, para la generación).

> **Hacia dónde sigue:** en **D18** encadenarás clasificar, extraer, recuperar y responder en un **agente** que decide qué herramienta usar para resolver una tarea completa.

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: los **embeddings y la similitud por coseno** (por qué el coseno), el ***chunking*** y sus
compromisos, la **calidad de la recuperación**, por qué **RAG reduce pero no elimina la alucinación**, la
**fidelidad/cita** y los **modos de falla** (mala recuperación → respuesta segura pero equivocada). Con 4
ejercicios conceptuales auto-corregidos. **Todo es conceptual y verificable sin conexión ni API key**
(recuperación con TF-IDF; ningún ejercicio llama a un LLM).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C2-rag/profundiza.ipynb)

---
*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*

*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
