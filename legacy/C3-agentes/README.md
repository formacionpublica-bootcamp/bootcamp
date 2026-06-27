# D18 · Agentes y proyecto integrador de IA aplicada

**Formación Pública — Bootcamp de Ciencia de Datos para funcionarios públicos**
Bloque avanzado · IA aplicada (opcional) · Semana 21 · **Módulo de cierre**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C3-agentes/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

---

## De qué trata

El cierre del bloque avanzado. Construyes un **agente**: un asistente que recibe una petición en lenguaje natural, **decide qué herramienta usar**, la ejecuta y responde. Y lo armas **integrando todo lo del bloque**: pronóstico (D14), clasificación (D15/D16), RAG (D17) y guardrail de privacidad (D16), sobre datos reales del Estado.

## Qué vas a aprender

- Qué es un agente y su ciclo **decidir → actuar → responder**.
- Empaquetar capacidades como **herramientas** invocables.
- Construir un **enrutador** que elige la herramienta correcta.
- Hacer el agente **transparente** (traza auditable) y **seguro** (bloquea datos personales).

**Competencia de salida:** orquestar varias capacidades de IA en un único asistente que resuelve tareas reales de gobierno de principio a fin.

## Cómo está construido

- **Herramientas provistas:** versiones compactas de módulos previos, incluyendo clasificación de compras de MercadoPúblico, consulta de ficha de licitación (RAG de ChileCompra) y pronóstico de gasto público basado en datos de ChileCompra / MercadoPúblico.
- **Enrutador por reglas:** determinista y verificable sin conexión. La lección explica que en producción esa decisión la toma un LLM (D16); el patrón es idéntico.
- **LLM:** Google Gemini (`gemini-2.5-flash`) con el patrón **"en vivo o caché"**.

## Funciona en vivo o en caché

Con `GEMINI_API_KEY` en los Secrets de Colab, las herramientas que usan LLM trabajan en vivo; sin ella, usan caché. Los 4 ejercicios se completan igual (el enrutador y la mayoría de las herramientas no dependen de la red).

## Contenido del módulo

| Archivo | Qué es |
|---|---|
| `leccion.ipynb` | La lección completa: teoría + 4 ejercicios con celdas de chequeo (✅ / ❌). |
| `solucion.ipynb` | Versión resuelta (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `README.md` | Esta presentación. |
| `gasto_anual.csv` | Dataset estático con la serie anual de gasto público (ChileCompra). |

## Cómo se usa

1. Pulsa **Open in Colab** arriba.
2. (Opcional) Configura tu `GEMINI_API_KEY` en los Secrets de Colab.
3. Completa los `TODO` y ejecuta las **celdas de chequeo** (✅ o pista amable).
4. El módulo está completo cuando las **4 celdas de chequeo** muestran ✅.

## Requisitos previos

Todo el bloque avanzado: D14 (series), D15 (NLP), D16 (LLMs) y D17 (RAG).

> **Hacia dónde sigue:** con esto cierras D14–D18. El siguiente hito es el **Proyecto Final**: resolver un problema real de tu institución de punta a punta.

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: el ciclo **decidir → actuar → responder**, el ***tool use***, **por qué fallan los
agentes** (errores que se acumulan, elegir mal la herramienta), **determinismo vs enrutamiento por LLM**,
y **humano en el bucle, gobernanza, auditabilidad y costo/seguridad**. Con 4 ejercicios conceptuales
auto-corregidos. **Todo es conceptual y verificable sin conexión ni API key** (enrutador por reglas;
ningún ejercicio llama a un LLM).

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/C3-agentes/profundiza.ipynb)

---
*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*

*Contenido bajo licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es).*
