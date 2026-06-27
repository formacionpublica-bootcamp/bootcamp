# D16 · IA generativa y LLMs

**Formación Pública — Bootcamp de Ciencia de Datos para funcionarios públicos**
Bloque avanzado · IA aplicada (opcional) · Semana 19

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A7-ia-generativa-y-llms/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

---

## De qué trata

El salto de *contar* palabras (D15) a *entender* texto. Conectas el cuaderno a un **LLM real y gratuito** (Google Gemini) y lo usas para tareas concretas de gobierno —explicar, clasificar y extraer datos estructurados— con foco en el **uso responsable**.

## Qué vas a aprender

- Qué es un LLM, a nivel intuitivo, y por qué entiende significado y sinónimos.
- **Llamar a un LLM desde Python** y dirigirlo con buenos *prompts*.
- **Clasificar** por significado (superando al método de palabras clave de D15).
- **Extraer información estructurada** (JSON) de texto libre.
- **Uso responsable:** verificación de cifras y protección de datos personales.

**Competencia de salida:** resolver una tarea real de texto del Estado con un LLM, de forma reproducible y responsable.

## Proveedor de LLM: Google Gemini (gratis, sin tarjeta)

Este módulo usa **Google AI Studio / Gemini API**, modelo `gemini-2.5-flash`.

- **Gratis y sin tarjeta de crédito:** solo necesitas tu cuenta de Google (la misma de Colab).
- **Cómo obtener tu API key (2 min):**
  1. Entra a **https://aistudio.google.com/apikey** e inicia sesión.
  2. Pulsa *Create API key* y copia la clave.
  3. En Colab: panel 🔑 **Secrets** → *Add new secret* → nombre `GEMINI_API_KEY`, pega el valor y habilita el acceso al notebook.
- **Nunca** pegues la API key dentro de una celda: usa los *Secrets* de Colab.
- **Privacidad:** en la capa gratuita, Google puede usar los textos para mejorar sus modelos. Por eso el módulo enseña a **no enviar datos personales**.

## Funciona en vivo o en caché

El notebook sigue el patrón **"en vivo o caché"**:

- **Con API key:** habla con Gemini **en vivo**.
- **Sin API key / sin conexión:** usa respuestas reales **en caché** y los 4 ejercicios se completan igual.

Así nadie se queda fuera y el cuaderno es siempre verificable.

## Contenido del módulo

| Archivo | Qué es |
|---|---|
| `leccion.ipynb` | La lección completa: teoría + 4 ejercicios con celdas de chequeo (✅ / ❌). |
| `solucion.ipynb` | Versión resuelta (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `README.md` | Esta presentación. |

## Cómo se usa

1. Pulsa **Open in Colab** arriba.
2. (Opcional) Configura tu `GEMINI_API_KEY` en los Secrets de Colab.
3. Completa los `TODO` y ejecuta las **celdas de chequeo** (✅ o pista amable).
4. El módulo está completo cuando las **4 celdas de chequeo** muestran ✅.

## 🔬 Profundización (opcional)
¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría —y corre **sin API key ni conexión**, con demos de juguete que dejan *ver* los
mecanismos reales: **tokens y predicción del siguiente token**, **por qué alucinan** (optimizan
plausibilidad, no verdad), qué hace la **temperatura** (*softmax* con `T`), la **ventana de contexto**,
los **sesgos heredados** de los datos de entrenamiento y los **límites para el uso responsable en el
Estado** (verificar cifras, privacidad). Con 4 ejercicios conceptuales auto-corregidos.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A7-ia-generativa-y-llms/profundiza.ipynb)

## Requisitos previos

Núcleo completo (M0–D13) y, idealmente, D15 (NLP), cuyo límite este módulo resuelve.

> **Hacia dónde sigue:** en **D17 (RAG)** le darás al LLM **tus propios documentos** para que responda con datos del Estado citando la fuente; en **D18**, encadenarás todo en **agentes**.

---
*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
