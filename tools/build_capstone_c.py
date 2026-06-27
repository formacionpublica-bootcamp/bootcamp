# -*- coding: utf-8 -*-
"""Capstone C (IA aplicada): asistente RAG sobre documentos públicos que responde
citando la fuente. Recuperación TF-IDF (offline, verificable) + LLM opcional.
Carpeta: C4-capstone."""
import json, os
import pandas as pd

BASE = "C4-capstone"
REPO = "formacionpublica-bootcamp/bootcamp"
os.makedirs(BASE, exist_ok=True)

# 1. Documentos provistos (resúmenes educativos referenciales de compras públicas)
DOCS = [
    ("D1", "Ley de Compras Públicas",
     "Las compras y contrataciones de bienes y servicios de los organismos del Estado se rigen principalmente por la Ley N° 19.886, conocida como Ley de Compras Públicas, y su reglamento."),
    ("D2", "Mercado Público",
     "Mercado Público es la plataforma electrónica administrada por la Dirección ChileCompra donde los organismos del Estado publican sus compras y los proveedores presentan sus ofertas."),
    ("D3", "Licitación pública",
     "La licitación pública es un procedimiento concursal y abierto en el que cualquier proveedor puede ofertar. Es la regla general para las contrataciones de mayor monto."),
    ("D4", "Convenio Marco",
     "El Convenio Marco es una modalidad en la que ChileCompra licita y pone a disposición un catálogo electrónico; los organismos compran directamente desde ese catálogo, lo que agiliza el proceso."),
    ("D5", "Trato directo",
     "El trato directo es una modalidad excepcional que permite contratar sin licitación en casos calificados y fundados que establece la ley, por ejemplo emergencias o cuando existe un único proveedor."),
    ("D6", "Orden de compra",
     "La orden de compra es el documento que formaliza la adquisición: indica el organismo comprador, el proveedor, los productos o servicios, las cantidades y el monto."),
    ("D7", "Datos abiertos",
     "ChileCompra publica datos abiertos de las órdenes de compra y licitaciones en su portal de transparencia, lo que permite a cualquier persona analizar el gasto público."),
    ("D8", "Principios de la compra pública",
     "Las compras públicas se orientan por principios de transparencia, probidad, eficiencia y libre concurrencia de los oferentes."),
]
pd.DataFrame(DOCS, columns=["id", "titulo", "texto"]).assign(
    fuente="Resumen educativo · referencial (fuente oficial: chilecompra.cl)"
).to_csv(os.path.join(BASE, "documentos.csv"), index=False)
print("documentos.csv:", len(DOCS), "documentos")

# 2. Celdas
TITULO = """# Capstone C · Tu asistente con IA

**Formación Pública — Capa C · IA aplicada al Estado · Proyecto final**

Construyes un **asistente que responde preguntas sobre documentos públicos citando la fuente** (un
RAG). Integra C1 (NLP), A7 (LLMs) y C2 (RAG): primero **recuperas** el documento relevante y luego
**respondes citándolo**, para no inventar.

Sigue el **Ciclo Pública** con foco en *Obtén/Modela/Comunica*. Al final, autoevaluación y rúbrica.

**Entregable:** este notebook con tu asistente funcionando sobre un conjunto de documentos, que
responde **citando la fuente**. Súbelo a tu GitHub como portafolio."""

PASO0 = """## Paso 0 · Elige tus documentos
- **Opción A (recomendada):** `documentos.csv` provisto — resúmenes referenciales de compras públicas
  (`id`, `titulo`, `texto`, `fuente`).
- **Opción B:** trae tus propios documentos (un CSV con una columna `texto` y un `titulo`/`fuente`)."""

CARGA = """import os, urllib.request
import pandas as pd

ARCHIVO = "documentos.csv"   # cámbialo por tus documentos si usas la Opción B
if not os.path.exists(ARCHIVO):
    try:
        url = "https://raw.githubusercontent.com/%s/main/C4-capstone/documentos.csv"
        urllib.request.urlretrieve(url, ARCHIVO)
    except Exception:
        print("Si estás en Colab, sube el archivo manualmente.")

docs = pd.read_csv(ARCHIVO)
print(f"{len(docs)} documentos cargados")
docs[["titulo", "texto"]].head()""" % REPO

PASO1 = """## Paso 1 · ¿Qué debe responder tu asistente?
Define el tipo de preguntas que atenderá (ej. "¿qué es el convenio marco?", "¿cuándo se usa trato
directo?"). Un buen asistente tiene un propósito claro y acotado."""
PASO1_TODO = """**✍️ Tu asistente responde sobre:** _(descríbelo aquí)_"""
PASO1_SOL = """**✍️ Mi asistente responde sobre:** conceptos básicos de **compras públicas** (modalidades, plataforma, normativa), siempre **citando el documento** de donde sale la respuesta."""

PASO2 = """## Paso 2 · Indexar y recuperar (el "buscador" del RAG)
El corazón de un RAG es **recuperar** el documento más parecido a la pregunta. Usamos **TF-IDF**
(de C1): convierte texto en números y mide la similitud. Crea una función `recuperar(pregunta)` que
devuelva el documento más relevante."""
PASO2_TODO = """from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TODO: ajusta el vectorizador sobre docs["texto"] y crea la función recuperar()
vectorizer = None
matriz = None

def recuperar(pregunta, k=1):
    # TODO: transforma la pregunta, calcula similitud y devuelve los k docs más parecidos
    pass"""
PASO2_SOL = """from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()
matriz = vectorizer.fit_transform(docs["texto"])

def recuperar(pregunta, k=1):
    consulta = vectorizer.transform([pregunta])
    sims = cosine_similarity(consulta, matriz)[0]
    idx = sims.argsort()[::-1][:k]
    return docs.iloc[idx]

recuperar("¿qué es el convenio marco?")[["titulo"]]"""

PASO3 = """## Paso 3 · Responder citando la fuente
Un asistente público **nunca debe inventar**. Crea `responder(pregunta)` que recupere el documento y
devuelva su contenido **junto con la fuente**. *(Opcional, si hiciste A7: con `GEMINI_API_KEY`
puedes pedirle al LLM que redacte la respuesta usando ese texto como contexto — patrón en-vivo-o-caché.)*"""
PASO3_TODO = """def responder(pregunta):
    # TODO: recupera el doc más relevante y devuelve su texto + "Fuente: <titulo> (<fuente>)"
    pass"""
PASO3_SOL = """def responder(pregunta):
    doc = recuperar(pregunta, k=1).iloc[0]
    # (Opcional) Con GEMINI_API_KEY, aquí pedirías al LLM redactar usando doc["texto"] como contexto.
    return f'{doc["texto"]}\\n\\nFuente: {doc["titulo"]} ({doc["fuente"]})'"""

PASO4 = """## Paso 4 · Prueba tu asistente
Hazle 2–3 preguntas y revisa que **recupere el documento correcto** y **cite la fuente**."""
PASO4_TODO = """# TODO: prueba responder() con 2-3 preguntas
print(responder("¿qué es una licitación pública?"))"""
PASO4_SOL = """for p in ["¿qué es una licitación pública?", "¿cuándo se usa trato directo?", "¿dónde se publican las compras del Estado?"]:
    print("P:", p)
    print(responder(p))
    print("=" * 60)"""

PASO5 = """## Paso 5 · Conclusión y ética
Responde en tus palabras:

- **Qué hace tu asistente** y para quién es útil.
- **Riesgos (A7):** ¿qué pasa si la pregunta no está en los documentos? ¿cómo evitas que **invente**?
- **Privacidad:** ¿por qué no debes cargar documentos con datos personales a un LLM externo?"""
PASO5_TODO = PASO5 + """

_(reemplaza estas líneas con tus respuestas)_"""
PASO5_SOL = PASO5 + """

- **Qué hace:** responde dudas frecuentes de compras públicas citando el documento de origen; útil
  para orientar a funcionarios y proveedores nuevos.
- **Riesgos:** si la pregunta no está cubierta, el buscador igual devuelve "lo más parecido", que
  puede no servir; por eso **siempre se muestra la fuente** para que la persona verifique, y conviene
  avisar cuando la similitud es baja. Citar la fuente es lo que evita inventar.
- **Privacidad:** enviar documentos con datos personales a un LLM externo puede exponerlos; se
  trabaja solo con documentos públicos o se anonimiza antes."""

AUTOEVAL = """# Autoevaluación suave — confirma que armaste el asistente (no califica la redacción).
hechos = {}
hechos["Cargaste documentos"] = "docs" in dir() and len(docs) > 0
hechos["Creaste el buscador (recuperar)"] = "recuperar" in dir() and callable(recuperar)
try:
    _r = responder("¿qué es una licitación pública?")
    hechos["Responde citando la fuente"] = isinstance(_r, str) and "Fuente" in _r
except Exception:
    hechos["Responde citando la fuente"] = False
for paso, ok in hechos.items():
    print(("✅ " if ok else "⬜ ") + paso)
print("\\nEvalúate con la rúbrica del README (aprobado: 12/18).")"""

RUBRICA = """## Rúbrica (autoevalúate, 0–3 cada una)
| Criterio | 0–3 |
|---|---|
| Propósito del asistente claro | |
| Recuperación funciona (encuentra el doc correcto) | |
| Responde **citando la fuente** | |
| Prueba con varias preguntas | |
| Manejo del "no sé" / baja similitud | |
| Reflexión de ética y privacidad | |

**Aprobado: 12 de 18.** → **Especialización: IA aplicada al sector público.** 🎉"""


def md(t, cid): return {"cell_type": "markdown", "metadata": {}, "id": cid, "source": t}
def code(t, cid): return {"cell_type": "code", "metadata": {}, "id": cid, "execution_count": None, "outputs": [], "source": t}

def build(resuelto):
    g = lambda sol, todo: sol if resuelto else todo
    cells = [
        md(TITULO, "c00"), md(PASO0, "c01"), code(CARGA, "c02"),
        md(PASO1, "c03"), md(g(PASO1_SOL, PASO1_TODO), "c04"),
        md(PASO2, "c05"), code(g(PASO2_SOL, PASO2_TODO), "c06"),
        md(PASO3, "c07"), code(g(PASO3_SOL, PASO3_TODO), "c08"),
        md(PASO4, "c09"), code(g(PASO4_SOL, PASO4_TODO), "c10"),
        md(g(PASO5_SOL, PASO5_TODO), "c11"),
        code(AUTOEVAL, "c12"), md(RUBRICA, "c13"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "proyecto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "ejemplo_resuelto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

README = """# Capstone C · Tu asistente con IA

**Proyecto final de la Capa C (IA aplicada al Estado)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/%s/blob/main/C4-capstone/proyecto.ipynb)

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
""" % REPO

open(os.path.join(BASE, "README.md"), "w", encoding="utf-8").write(README)
print("Capstone C generado en:", BASE)
print("Archivos:", sorted(os.listdir(BASE)))
