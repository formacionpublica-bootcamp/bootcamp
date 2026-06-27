# D15 · Introducción al NLP

**Formación Pública — Bootcamp de Ciencia de Datos para funcionarios públicos**
Bloque avanzado · IA aplicada (opcional) · Semana 18

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C1-introduccion-al-nlp/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

---

## De qué trata

Primer contacto con el **texto como dato**. Buena parte de la información del Estado (nombres de licitaciones, descripciones, reclamos) es texto libre. Aquí aprendes la **tubería básica del NLP** para poder analizarlo a escala, usando texto real de compras públicas.

## Qué vas a aprender

- Por qué el texto es un dato difícil y cómo se prepara.
- **Normalizar** texto en español (minúsculas, tildes, signos).
- **Tokenizar** y quitar palabras vacías (*stopwords*).
- Medir **frecuencias** con una **bolsa de palabras**.
- Construir un **clasificador simple por palabras clave**.

**Competencia de salida:** dado un texto real del Estado, prepararlo y extraer de él información cuantificable y útil.

## Contenido del módulo

| Archivo | Qué es |
|---|---|
| `leccion.ipynb` | La lección completa: teoría + 4 ejercicios con celdas de chequeo (✅ / ❌). |
| `solucion.ipynb` | Versión resuelta (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `rubros.csv` | Dataset estático con las 45 categorías oficiales del catálogo de compras de ChileCompra. |
| `README.md` | Esta presentación. |

## Cómo se usa

1. Pulsa **Open in Colab** arriba.
2. Lee cada sección y completa los `TODO`.
3. Ejecuta la **celda de chequeo** de cada ejercicio: muestra ✅ o una pista amable.
4. El módulo está completo cuando las **4 celdas de chequeo** muestran ✅.

## Datos

- **Fuente:** Dirección de Compras y Contratación Pública de Chile (**ChileCompra** / MercadoPúblico).
- **Dataset:** `rubros.csv` con los 45 rubros reales del catálogo de compras públicas.
- El notebook incluye un descargador inteligente que obtiene el archivo automáticamente en entornos efímeros (como Google Colab).
- Solo se usa la **librería estándar** de Python (`re`, `unicodedata`, `collections`) y `pandas`: nada más que instalar.

## Requisitos previos

Haber completado el núcleo del bootcamp (M0–D13).

> **Hacia dónde sigue:** este módulo *cuenta* palabras pero no *entiende* significado. Ese salto lo dan los modelos de lenguaje (LLMs), tema del módulo **D16**.

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: el **texto como dato**, la **tokenización**, la intuición de **bolsa de palabras /
TF-IDF** (por qué el *IDF*), la **alta dimensión y dispersión**, **por qué fallan los métodos por palabra
clave** (sinónimos y contexto), los **n-gramas** y los **sesgos del lenguaje**. Con 4 ejercicios
conceptuales auto-corregidos. **Todo corre sin conexión ni API key.**

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C1-introduccion-al-nlp/profundiza.ipynb)

---
*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
