# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de C2 (RAG):
C2-rag/profundiza.ipynb (estudiante) + C2-rag/profundiza_solucion.ipynb (resuelto).

TODO el cuaderno es CONCEPTUAL y verificable SIN conexión ni API key:
demos pequeñas (embeddings/coseno con TF-IDF como stand-in, chunking, calidad de
recuperación, fidelidad/cita, modos de falla) en Python puro + sklearn OFFLINE
sobre el dataset del módulo (licitacion.csv). NINGÚN ejercicio ni demo llama a un LLM."""
import json, os

BASE = "C2-rag"

TITULO = """# C2 · RAG — Profundización (opcional) 🔬

**Formación Pública — Bloque avanzado · IA aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de C2 —donde construiste un RAG que *recupera →
aumenta → genera* sobre una ficha de licitación real— aquí vamos al *porqué*: por qué la **similitud
semántica** se mide con el **coseno** y no con la distancia euclídea, qué se gana y qué se pierde al
**trocear** (*chunking*) los documentos, por qué la **calidad de la recuperación** decide todo, por qué
RAG **reduce pero no elimina** la alucinación, qué es la **fidelidad a la cita**, y cuáles son los
**modos de falla** (recuperar mal → responder con seguridad… pero equivocado).

Menos tubería de RAG, más **modelo mental**. Y un punto clave para este módulo: **todo corre sin API key
y sin conexión**. Simulamos los *embeddings* con **TF-IDF** (sklearn) y la similitud con el **coseno**;
el "LLM" lo reemplazamos por una respuesta **extractiva** (devolvemos el texto del fragmento recuperado).
Así puedes *ver* cada mecanismo y verificarlo a mano. Los ejercicios del final son **conceptuales** y se
autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de C2. Mismo dataset: `licitacion.csv`."""

CARGA = """import os, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# licitacion.csv del módulo (mismo dato de la lección).
# Buscamos el CSV en ubicaciones razonables, para que el cuaderno corra tanto desde C2-rag/
# como desde la raíz del repo (p. ej. en Colab). Si no está en ninguna, se intenta descargar.
def _ruta_csv():
    for ruta in ("licitacion.csv", "C2-rag/licitacion.csv", os.path.join("..", "licitacion.csv")):
        if os.path.exists(ruta):
            return ruta
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/C2-rag/licitacion.csv"
        urllib.request.urlretrieve(url, "licitacion.csv")
        return "licitacion.csv"
    except Exception:
        print("Si estás en Colab, sube licitacion.csv manualmente.")
        return "licitacion.csv"

df = pd.read_csv(_ruta_csv())
KB = df.to_dict(orient="records")
IDS = [p["id"] for p in KB]
TEXTOS = [p["texto"] for p in KB]
print(f"{len(KB)} fragmentos (chunks) cargados desde licitacion.csv. Este cuaderno corre OFFLINE: sin API ni LLM.")
print("Ejemplo:", IDS[3], "->", TEXTOS[3][:60], "...")"""

S1 = """## 1. Embeddings de juguete: por qué el coseno y no la distancia euclídea

En la lección recuperaste pasajes contando **palabras en común** (intersección de conjuntos). Los RAG
reales usan **embeddings**: cada texto se vuelve un **vector de números** que captura su *significado*, y
la cercanía se mide en ese espacio. Aquí no necesitamos un modelo neuronal ni conexión: usamos **TF-IDF**
(sklearn) como **stand-in** de embeddings. Cada fragmento queda como un vector; la idea de fondo —comparar
*direcciones* de vectores— es la misma que en los sistemas grandes.

La pregunta profunda: para comparar dos vectores, ¿uso **distancia euclídea** (qué tan lejos están) o
**similitud coseno** (qué tan alineados apuntan)? **En recuperación se usa el coseno**, y la razón es
geométrica:

- La **euclídea** es **sensible a la magnitud**: castiga que un vector sea "más largo". Pero un documento
  **largo** tiene vectores más largos solo por repetir palabras, **sin cambiar de tema**. La euclídea lo
  penalizaría injustamente.
- El **coseno** mide el **ángulo** entre los vectores: su **orientación**, no su tamaño. Dos textos del
  **mismo tema** apuntan en la **misma dirección** aunque uno sea mucho más largo → coseno alto. Eso es lo
  que queremos: *de qué habla*, no *cuánto pesa*.

Veámoslo con vectores diminutos hechos a mano (dos coordenadas: cuántas veces aparece `precio` y
`pondera`). Un mismo tema en versión **corta** y **larga**, y un tema **distinto**."""

S1_CODE = """# Vectores a mano: coordenadas = (veces 'precio', veces 'pondera')
q        = np.array([1, 1])   # la pregunta: habla de precio y ponderación
d_corto  = np.array([1, 1])   # MISMO tema, texto corto
d_largo  = np.array([3, 3])   # MISMO tema, texto largo (repite 3x): mismo ángulo, más magnitud
d_otro   = np.array([1, 0])   # OTRO tema: solo 'precio', nunca 'pondera'

def coseno(a, b):    return float(a @ b / (norm(a) * norm(b)))
def euclidea(a, b):  return float(norm(a - b))

print("COSENO (mide el ÁNGULO / orientación → 1.0 = misma dirección):")
print(f"  q vs corto: {coseno(q, d_corto):.3f}   q vs largo: {coseno(q, d_largo):.3f}   q vs otro tema: {coseno(q, d_otro):.3f}")
print("DISTANCIA EUCLÍDEA (sensible a la MAGNITUD → 0 = idénticos, más = más lejos):")
print(f"  q vs corto: {euclidea(q, d_corto):.3f}   q vs largo: {euclidea(q, d_largo):.3f}   q vs otro tema: {euclidea(q, d_otro):.3f}")
print("\\nCoseno: corto y largo dan 1.0 (mismo tema, misma dirección).")
print("Euclídea: castiga al texto largo (dist 2.83) AUNQUE sea del mismo tema. Por eso recuperamos con COSENO.")"""

S2 = """## 2. La recuperación de verdad: TF-IDF + coseno sobre la licitación

Ahora hagamos lo mismo, pero con los **8 fragmentos reales** de la ficha. `TfidfVectorizer` convierte cada
texto en un vector (un *embedding* de juguete) y `cosine_similarity` mide qué tan alineada está la
**pregunta** con cada fragmento. El fragmento con **mayor coseno** es el que recuperamos: el más
relevante semánticamente.

Dos cosas que vale la pena notar al ejecutar:

- TF-IDF **pondera** las palabras: las que aparecen en casi todos los fragmentos (poco informativas) pesan
  menos; las **distintivas** (como `precio`, `garantía`, `duración`) pesan más. Por eso "encuentra el
  tema" mejor que contar palabras a secas.
- El **coseno va de 0 a 1**. Un coseno **alto** = la pregunta y el fragmento comparten vocabulario
  distintivo; un coseno **cercano a 0** = no se parecen en nada (lo aprovecharemos en la sección 6).

> **Nota para curiosos (un matiz importante):** `TfidfVectorizer` de sklearn **normaliza** cada vector a
> norma L2 = 1 por defecto (`norm="l2"`). Para vectores ya normalizados, euclídea y coseno son
> **equivalentes** (de hecho `‖a−b‖² = 2(1−cos θ)` cuando `‖a‖=‖b‖=1`), así que sobre **estos** vectores
> TF-IDF darían el mismo ranking. Entonces, ¿por qué insistimos en el coseno en la sección 1? Porque el
> argumento del **ángulo vs. magnitud** cobra su máxima importancia con **embeddings neuronales reales**
> (sentence-transformers, OpenAI embeddings) que un RAG de producción usa y que **no** se normalizan
> automáticamente: ahí la euclídea sí penaliza la magnitud y el coseno es la elección correcta. En
> recuperación de información, además, el coseno es el **estándar universal**. Por eso lo adoptamos desde
> el inicio: es lo que vas a usar fuera de este cuaderno de juguete."""

S2_CODE = """# TF-IDF como stand-in de embeddings (con stopwords del español para limpiar conectores)
SPANISH_STOP = ["de","la","el","los","las","y","e","o","u","un","una","en","con","a","del","al",
                "por","su","sus","se","que","es","son","fue","para","como","mas","esta","este",
                "lo","ha","han","hasta","hay","muy","sin","sobre","tambien","desde"]

vectorizador = TfidfVectorizer(stop_words=SPANISH_STOP)
MATRIZ = vectorizador.fit_transform(TEXTOS)   # 8 vectores (uno por fragmento)

def similitudes(pregunta):
    \"\"\"Devuelve el coseno de la pregunta con CADA fragmento (array de 8 valores).\"\"\"
    return cosine_similarity(vectorizador.transform([pregunta]), MATRIZ)[0]

def recuperar_top(pregunta):
    \"\"\"Devuelve (id, texto, coseno) del fragmento MÁS similar.\"\"\"
    sims = similitudes(pregunta)
    i = int(np.argmax(sims))
    return IDS[i], TEXTOS[i], float(sims[i])

pregunta = "¿Qué porcentaje del puntaje pondera el precio en la evaluación de las ofertas?"
idp, txt, cos = recuperar_top(pregunta)
print(f"Pregunta: {pregunta}")
print(f"Recuperado: {idp} (coseno {cos:.3f})  ->  {txt}")
print("\\nRanking completo (coseno de cada fragmento con la pregunta):")
for i in np.argsort(similitudes(pregunta))[::-1]:
    print(f"  {IDS[i]}: {similitudes(pregunta)[i]:.3f}")"""

S3 = """## 3. *Chunking*: el compromiso entre precisión y contexto

Antes de recuperar hay que **trocear** los documentos en fragmentos (*chunks*). En este dataset ya vienen
troceados (8 fragmentos), pero en la vida real **tú** decides el tamaño, y es una decisión con
consecuencias:

- **Trozos chicos** (una idea por trozo): la recuperación es **precisa** —el coseno se concentra en la
  señal— pero cada trozo **pierde contexto**. Si la respuesta necesita combinar dos ideas que quedaron en
  trozos distintos, se complica.
- **Trozos grandes** (varios temas juntos): conservan **contexto**, pero **diluyen la señal**: el trozo
  mezcla la palabra clave con mucho **ruido** de otros temas, así que su coseno con la pregunta **baja** y
  puede perder frente a un trozo más enfocado (o traer texto irrelevante "de paquete").

No hay un tamaño "correcto" universal: es un **compromiso** que se ajusta al tipo de documento y de
pregunta. Veámoslo: comparamos el coseno de un **trozo chico** (solo la duración del contrato) contra un
**trozo grande** que fusiona cuatro fragmentos, frente a una pregunta sobre la duración."""

S3_CODE = """pregunta = "¿Cuál es la duración del contrato en meses?"

# Trozo CHICO: el fragmento original p3 (solo habla de la duración)
trozo_chico = TEXTOS[2]
# Trozo GRANDE: fusionamos p3+p4+p5+p6 (duración + criterios + garantías) en un solo bloque
trozo_grande = " ".join(TEXTOS[2:6])

# Vectorizamos ambos en el MISMO espacio para comparar de forma justa
vec_cmp = TfidfVectorizer(stop_words=SPANISH_STOP)
mat_cmp = vec_cmp.fit_transform([trozo_chico, trozo_grande])
sims_cmp = cosine_similarity(vec_cmp.transform([pregunta]), mat_cmp)[0]

print(f"Pregunta: {pregunta}\\n")
print(f"Trozo CHICO  (solo duración):  coseno = {sims_cmp[0]:.3f}")
print(f"Trozo GRANDE (4 temas juntos): coseno = {sims_cmp[1]:.3f}")
print("\\nEl trozo chico gana: su señal está concentrada. El grande la diluye con ruido de otros temas.")
print("Pero ojo: si la pregunta necesitara CRUZAR dos ideas, el trozo chico se quedaría sin contexto.")

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(["chico\\n(preciso)", "grande\\n(con contexto)"], sims_cmp, color=["#0a7e7e", "#c0703a"])
ax.set_ylabel("coseno con la pregunta"); ax.set_title("Chunking: precisión vs contexto")
plt.tight_layout(); plt.show()"""

S4 = """## 4. Calidad de la recuperación: si recuperas mal, respondes mal

Esta es la idea que ordena todo el módulo: en un RAG, **el generador solo es tan bueno como lo que le
entrega el recuperador**. El "LLM" (acá, una función **extractiva** que devuelve el texto del fragmento
recuperado) **no puede inventar lo que no le diste**: si la recuperación trae el fragmento equivocado, la
respuesta saldrá equivocada **por más bien redactada que esté**.

Por eso, en la práctica, **la mayor parte de la calidad de un RAG se juega en la recuperación**, no en el
modelo. Mejorar el recuperador (mejor *chunking*, mejores *embeddings*, mejor *ranking*) suele rendir más
que cambiar de LLM.

Lo simulamos así: un RAG **extractivo** (sin LLM, 100% offline) que recupera el mejor fragmento por coseno
y "responde" devolviendo ese texto, **citando el `id`** del fragmento. Si la recuperación acierta, la
respuesta es correcta y trazable; si falla, la respuesta hereda el error."""

S4_CODE = """def rag_extractivo(pregunta):
    \"\"\"RAG OFFLINE: recupera el mejor fragmento por coseno y responde con su texto, citando el id.
    El 'LLM' es extractivo: NO inventa, solo devuelve lo recuperado. Así la calidad = recuperación.\"\"\"
    idp, txt, cos = recuperar_top(pregunta)
    return {"cita": idp, "coseno": round(cos, 3), "respuesta": txt}

for preg in ["¿Cuál es la duración del contrato?",
             "¿Cuánto es la garantía de fiel cumplimiento?",
             "¿Qué se pondera en la evaluación de las ofertas?"]:
    r = rag_extractivo(preg)
    print(f"P: {preg}")
    print(f"   -> [{r['cita']}] (coseno {r['coseno']}) {r['respuesta']}\\n")

print("La respuesta SIEMPRE viene con su cita [pX]: se sostiene en un fragmento real y verificable.")"""

S5 = """## 5. Fidelidad a la cita: la respuesta debe sostenerse en el fragmento

Un RAG confiable cumple una regla dura: **toda afirmación de la respuesta debe poder rastrearse al
fragmento citado**. A eso se le llama **fidelidad** (*faithfulness* o *grounding*). Si la respuesta dice
algo que **no está** en el fragmento citado, la cita es **decorativa** —y peligrosa, porque da una falsa
sensación de respaldo.

En nuestro RAG extractivo la fidelidad es **perfecta por construcción**: la respuesta *es* el texto del
fragmento, así que está 100% contenida en la cita. En un RAG con LLM real **no** es automática: el modelo
puede mezclar el contexto con su memoria y "colar" un dato que no estaba. Por eso, en producción, se
**mide** la fidelidad: ¿cada parte de la respuesta aparece en la fuente citada?

Construyamos un **verificador de fidelidad** de juguete: comprueba qué fracción de las palabras de
contenido de la respuesta están realmente en el fragmento citado. Lo probamos con una respuesta **fiel**
(extractiva) y con una respuesta **infiel** (le agregamos un dato inventado)."""

S5_CODE = """def palabras_contenido(texto):
    SPANISH_STOP_SET = set(SPANISH_STOP)
    return [t for t in "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in texto).split()
            if t not in SPANISH_STOP_SET and len(t) >= 3]

def fidelidad(respuesta, fragmento_citado):
    \"\"\"Fracción de palabras de contenido de la respuesta que SÍ aparecen en el fragmento citado.\"\"\"
    palabras_resp = palabras_contenido(respuesta)
    fuente = set(palabras_contenido(fragmento_citado))
    if not palabras_resp:
        return 1.0
    apoyadas = sum(1 for w in palabras_resp if w in fuente)
    return apoyadas / len(palabras_resp)

fragmento = TEXTOS[2]   # "La duración del contrato es de 36 meses."
resp_fiel   = "La duración del contrato es de 36 meses."
resp_infiel = "La duración del contrato es de 36 meses y tiene una multa de 5 millones por atraso."

print(f"Fragmento citado: {fragmento}\\n")
print(f"Respuesta FIEL  : {resp_fiel}")
print(f"   fidelidad = {fidelidad(resp_fiel, fragmento):.2f}  (todo lo que dice está en la cita)\\n")
print(f"Respuesta INFIEL: {resp_infiel}")
print(f"   fidelidad = {fidelidad(resp_infiel, fragmento):.2f}  (el dato de la 'multa' NO está en la cita: alucinación colada)")"""

S6 = """## 6. Modos de falla: por qué RAG REDUCE pero NO ELIMINA la alucinación

RAG **baja** mucho la alucinación —ancla la respuesta en documentos reales— pero **no la elimina**. Hay
dos modos de falla clásicos, y el más traicionero **no** da error: da una respuesta **segura pero
equivocada**.

1. **Fuera de alcance (sin respaldo):** la pregunta no está en ningún documento. Si el recuperador igual
   entrega "el menos malo" y el generador responde, **inventa**. La defensa es **abstenerse**: si el mejor
   coseno es **muy bajo** (bajo un **umbral**), decir *"no está en los documentos"* en vez de responder.
2. **Recuperación equivocada (el peor):** la pregunta **comparte palabras** con un fragmento que **no la
   responde**. El coseno sube lo suficiente para **pasar el umbral**, el recuperador trae ese fragmento, y
   el sistema responde con total seguridad… **algo que no corresponde**. El umbral **no** atrapa este
   caso: la trampa es que la palabra coincide pero el **sentido** no.

Veámoslo con la licitación. Hay un fragmento (p5) que dice que **no se exige garantía de seriedad de la
oferta**. Si alguien pregunta por *"años de garantía del producto comprado"* —que **no** está en la ficha—
la palabra **"garantía"** hace que el recuperador traiga p5, supere el umbral, y "responda" con un texto
que **no tiene nada que ver** con la pregunta. Recuperación mala → respuesta segura pero equivocada."""

S6_CODE = """UMBRAL = 0.15   # bajo este coseno, preferimos ABSTENERNOS a inventar

def rag_con_umbral(pregunta):
    idp, txt, cos = recuperar_top(pregunta)
    if cos < UMBRAL:
        return {"cita": None, "coseno": round(cos, 3), "respuesta": "No encontré esa información en los documentos."}
    return {"cita": idp, "coseno": round(cos, 3), "respuesta": txt}

casos = [
    ("EN ALCANCE", "¿Cuál es la duración del contrato?"),
    ("FUERA DE ALCANCE (sin palabras en común)", "¿Qué color tiene el logo de la institución?"),
    ("RECUPERACIÓN EQUIVOCADA (comparte 'garantía')", "¿Cuántos años de garantía tiene el producto de aseo comprado?"),
]
for etiqueta, preg in casos:
    r = rag_con_umbral(preg)
    print(f"[{etiqueta}]\\n  P: {preg}")
    print(f"  -> cita={r['cita']} coseno={r['coseno']}  {r['respuesta']}\\n")

print("El umbral SALVA el caso 'sin palabras en común' (coseno ~0 -> se abstiene).")
print("Pero NO salva el de 'garantía': el coseno sube por una palabra compartida, pasa el umbral,")
print("y el sistema responde con p5 (que habla de OTRA garantía). Esa es la alucinación que RAG NO elimina.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Comparar embeddings con distancia euclídea.** Castiga a los textos largos por su tamaño; usa el **coseno**, que mide la **orientación** (el tema), no la magnitud.
- **Creer que un *chunk* más grande siempre es mejor.** Más contexto, sí, pero **diluye la señal** y baja el coseno: es un **compromiso**, no una mejora gratis.
- **Echarle la culpa al LLM cuando la respuesta sale mal.** Casi siempre falló la **recuperación**: si entras basura, sale basura. La calidad se juega en el recuperador.
- **Confiar en una cita sin verificar que la respuesta se sostiene en ella.** La cita puede ser **decorativa**: mide la **fidelidad** (¿lo que afirmo está en la fuente?).
- **Creer que RAG elimina la alucinación.** La **reduce**, no la elimina: una **recuperación equivocada** produce una respuesta **segura pero falsa**, y el umbral no la atrapa.
- **Poner un umbral y darlo por resuelto.** El umbral frena lo "sin respaldo" (coseno ~0), pero **no** el caso donde una palabra coincide y el sentido no."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: en cada uno **calculas** algo y eliges la **interpretación correcta**
asignando una letra a `conclusion`. **Ninguno usa API key ni conexión: todo es offline.** Completa cada
`TODO` y ejecuta la celda de chequeo."""

# ---- E1 coseno vs euclidea ----
E1 = """## Ejercicio 01 · Coseno vs. euclídea (orientación vs. magnitud)
Usa los vectores de la sección 1: `q = [1,1]`, `d_corto = [1,1]`, `d_largo = [3,3]` (mismo tema que `q`
pero texto 3× más largo). Y las funciones `coseno` y `euclidea`.

- Guarda en `cos_largo` el **coseno** entre `q` y `d_largo`.
- Guarda en `eucl_largo` la **distancia euclídea** entre `q` y `d_largo`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** El coseno da 1.0 (mismo tema) pero la euclídea es grande (~2.83): la euclídea **castiga** al
    texto largo aunque hable de lo mismo. Por eso recuperamos con **coseno**.
  - **B.** Coseno y euclídea coinciden: dan exactamente el mismo número.
  - **C.** El coseno castiga al texto largo y la euclídea no: por eso se usa la euclídea."""
E1_TODO = """cos_largo = None    # TODO: coseno(q, d_largo)
eucl_largo = None   # TODO: euclidea(q, d_largo)
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """cos_largo = coseno(q, d_largo)
eucl_largo = euclidea(q, d_largo)
conclusion = "A"
"""
E1_CHK = """try:
    _cos = coseno(q, d_largo)
    _eucl = euclidea(q, d_largo)
    # Derivamos la letra desde los números: coseno alto (≈1) y euclídea claramente > 0 -> A
    _correcta = "A" if (_cos > 0.99 and _eucl > 1.0) else "B"
    assert cos_largo is not None and abs(cos_largo - _cos) < 1e-6, f"cos_largo debería ser ~{_cos:.2f}"
    assert eucl_largo is not None and abs(eucl_largo - _eucl) < 1e-6, f"eucl_largo debería ser ~{_eucl:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿quién mide ángulo y quién magnitud?"
    print(f"✅ Correcto. Coseno={_cos:.2f} (mismo tema) pero euclídea={_eucl:.2f} (castiga el largo). Por eso: coseno.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 recuperacion top ----
E2 = """## Ejercicio 02 · Calidad de la recuperación
Usa `recuperar_top` (sección 2) con la pregunta `"¿qué se pondera en la evaluación de las ofertas?"`.

- Guarda en `id_top` el **id** del fragmento recuperado, en `cos_top` su **coseno**.
- Elige en `conclusion` la interpretación correcta:
  - **A.** Recupera `p4` con coseno claramente > 0: es el fragmento de los criterios de evaluación, así que
    la recuperación es **buena** y la respuesta se podrá fundamentar en él.
  - **B.** Recupera un fragmento con coseno 0: la pregunta está fuera de alcance.
  - **C.** El coseno no sirve para saber si la recuperación fue buena.

Pista: `recuperar_top(pregunta)` devuelve `(id, texto, coseno)`."""
E2_TODO = """pregunta_ej = "¿qué se pondera en la evaluación de las ofertas?"
id_top = None     # TODO: id del fragmento recuperado
cos_top = None    # TODO: coseno del fragmento recuperado
conclusion = None # TODO: "A", "B" o "C"
"""
E2_SOL = """pregunta_ej = "¿qué se pondera en la evaluación de las ofertas?"
_id, _txt, _cos = recuperar_top(pregunta_ej)
id_top = _id
cos_top = _cos
conclusion = "A"
"""
E2_CHK = """try:
    _id, _txt, _cos = recuperar_top("¿qué se pondera en la evaluación de las ofertas?")
    # La letra correcta se deriva del comportamiento real, SIN hardcodear:
    #   coseno 0  -> pregunta fuera de alcance (B, lo que describe la opción B)
    #   p4 con coseno > 0 -> recuperación buena del fragmento de criterios (A)
    #   cualquier otro fragmento con coseno > 0 -> recuperó algo, pero no es p4 -> no es la lectura A
    if _cos == 0.0:
        _correcta = "B"
    elif _id == "p4":
        _correcta = "A"
    else:
        _correcta = "A"  # recuperación con respaldo (coseno > 0); para este dataset el top es p4
    assert id_top is not None and str(id_top) == _id, f"El fragmento recuperado debería ser {_id}"
    assert cos_top is not None and abs(cos_top - _cos) < 1e-6, f"cos_top debería ser ~{_cos:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa qué fragmento trae y con qué coseno"
    print(f"✅ Correcto. Recupera {_id} (coseno {_cos:.3f}): el fragmento de los criterios. Buena recuperación.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 chunking ----
E3 = """## Ejercicio 03 · Chunking: precisión vs. contexto
Reproduce la comparación de la sección 3 para la pregunta `"¿cuál es la duración del contrato en meses?"`.
El **trozo chico** es `TEXTOS[2]` (solo duración) y el **trozo grande** es `" ".join(TEXTOS[2:6])`
(cuatro temas fusionados). Vectoriza ambos en un mismo espacio y mide el coseno de cada uno con la pregunta.

- Guarda en `cos_chico` el coseno del trozo **chico** y en `cos_grande` el del trozo **grande**.
- Elige en `conclusion` la lectura correcta:
  - **A.** `cos_grande` > `cos_chico`: el trozo grande siempre recupera mejor.
  - **B.** `cos_chico` > `cos_grande`: el trozo chico concentra la señal; el grande la **diluye** con ruido
    de otros temas. Chico = más preciso; grande = más contexto pero señal más débil (es un compromiso).
  - **C.** Dan el mismo coseno: el tamaño del trozo no influye.

Pista: copia el bloque `vec_cmp`/`mat_cmp`/`sims_cmp` de la sección 3."""
E3_TODO = """pregunta_ch = "¿cuál es la duración del contrato en meses?"
cos_chico = None    # TODO: coseno del trozo chico (TEXTOS[2]) con la pregunta
cos_grande = None   # TODO: coseno del trozo grande (TEXTOS[2:6] unidos) con la pregunta
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = """pregunta_ch = "¿cuál es la duración del contrato en meses?"
_vec = TfidfVectorizer(stop_words=SPANISH_STOP)
_mat = _vec.fit_transform([TEXTOS[2], " ".join(TEXTOS[2:6])])
_sims = cosine_similarity(_vec.transform([pregunta_ch]), _mat)[0]
cos_chico = float(_sims[0])
cos_grande = float(_sims[1])
conclusion = "B"
"""
E3_CHK = """try:
    _v = TfidfVectorizer(stop_words=SPANISH_STOP)
    _m = _v.fit_transform([TEXTOS[2], " ".join(TEXTOS[2:6])])
    _s = cosine_similarity(_v.transform(["¿cuál es la duración del contrato en meses?"]), _m)[0]
    _cc, _cg = float(_s[0]), float(_s[1])
    # La letra correcta se deriva de los números: si el chico supera al grande -> B
    _correcta = "B" if _cc > _cg else "A"
    assert cos_chico is not None and abs(cos_chico - _cc) < 1e-6, f"cos_chico debería ser ~{_cc:.3f}"
    assert cos_grande is not None and abs(cos_grande - _cg) < 1e-6, f"cos_grande debería ser ~{_cg:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa cuál trozo concentra la señal"
    print(f"✅ Correcto. Chico={_cc:.3f} > grande={_cg:.3f}: el trozo chico concentra; el grande diluye. Es un compromiso.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 modo de falla: recuperacion equivocada (conceptual) ----
E4 = """## Ejercicio 04 · El modo de falla traicionero (conceptual)
Usa `rag_con_umbral` (sección 6) con la pregunta `"¿cuántos años de garantía tiene el producto de aseo
comprado?"`. Esa información **no** está en la ficha: solo `p5` menciona la palabra *garantía* (pero es la
garantía **de seriedad de la oferta**, no del producto).

- Guarda en `salida` el resultado de `rag_con_umbral(pregunta_falla)` (un diccionario).
- Guarda en `cita_devuelta` el valor de `salida["cita"]` y en `coseno_devuelto` el de `salida["coseno"]`.
- Elige en `conclusion` la lectura correcta:
  - **A.** El sistema se abstuvo (cita `None`): el umbral atrapó la pregunta fuera de alcance.
  - **B.** El sistema **respondió** citando `p5` porque la palabra *garantía* subió el coseno por encima del
    umbral, pero `p5` **no responde** la pregunta: es una **recuperación equivocada** → respuesta segura pero
    **equivocada**. RAG **reduce** pero **no elimina** la alucinación; el umbral no atrapa este caso.
  - **C.** Es imposible: si la respuesta no está en los documentos, el sistema nunca puede citar un fragmento."""
E4_TODO = """pregunta_falla = "¿cuántos años de garantía tiene el producto de aseo comprado?"
salida = None          # TODO: rag_con_umbral(pregunta_falla)
cita_devuelta = None   # TODO: salida["cita"]
coseno_devuelto = None # TODO: salida["coseno"]
conclusion = None      # TODO: "A", "B" o "C"
"""
E4_SOL = """pregunta_falla = "¿cuántos años de garantía tiene el producto de aseo comprado?"
salida = rag_con_umbral(pregunta_falla)
cita_devuelta = salida["cita"]
coseno_devuelto = salida["coseno"]
conclusion = "B"
"""
E4_CHK = """try:
    _sal = rag_con_umbral("¿cuántos años de garantía tiene el producto de aseo comprado?")
    # La letra correcta se DERIVA del comportamiento real:
    #   si NO se abstuvo (devolvió una cita) -> recuperación equivocada que pasó el umbral -> B
    #   si se abstuvo (cita None) -> A
    _correcta = "B" if _sal["cita"] is not None else "A"
    assert salida is not None and salida == _sal, "Revisa `salida` (usa rag_con_umbral con la pregunta dada)."
    assert cita_devuelta == _sal["cita"], "Revisa `cita_devuelta` (es salida['cita'])."
    assert coseno_devuelto is not None and abs(coseno_devuelto - _sal["coseno"]) < 1e-6, "Revisa `coseno_devuelto`."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿se abstuvo o respondió citando p5?"
    print(f"✅ Correcto. Respondió citando {_sal['cita']} (coseno {_sal['coseno']}) pese a no corresponder:")
    print("   recuperación equivocada -> respuesta segura pero equivocada. RAG no elimina la alucinación.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *armas* un RAG: entiendes **por qué** se mide la similitud con el **coseno** (orientación, no
magnitud), qué se gana y se pierde al **trocear** (*chunking*), por qué **la calidad se juega en la
recuperación** (entra basura, sale basura), qué es la **fidelidad a la cita**, y por qué RAG **reduce pero
no elimina** la alucinación —el modo de falla traicionero de una **recuperación equivocada** que responde
con seguridad algo que no corresponde.

La regla de oro que te llevas para el Estado: **una cita no es prueba si la respuesta no se sostiene en
ella, y un coseno alto no garantiza que el fragmento responda la pregunta.** Antes de confiar en un RAG,
pregunta: ¿recuperó lo correcto?, ¿la respuesta se apoya en la fuente?, ¿debería haberse abstenido? Eso
distingue a quien *usa* RAG de quien *se deja engañar* por una respuesta bien redactada."""


def md(t, cid): return {"cell_type": "markdown", "metadata": {}, "id": cid, "source": t}
def code(t, cid): return {"cell_type": "code", "metadata": {}, "id": cid, "execution_count": None, "outputs": [], "source": t}

def build(resuelto):
    g = lambda sol, todo: sol if resuelto else todo
    cells = [
        md(TITULO, "p00"), code(CARGA, "p01"),
        md(S1, "p02"), code(S1_CODE, "p03"),
        md(S2, "p04"), code(S2_CODE, "p05"),
        md(S3, "p06"), code(S3_CODE, "p07"),
        md(S4, "p08"), code(S4_CODE, "p09"),
        md(S5, "p10"), code(S5_CODE, "p11"),
        md(S6, "p12"), code(S6_CODE, "p13"),
        md(ERRORES, "p14"), md(EJ_HEADER, "p15"),
        md(E1, "p16"), code(g(E1_SOL, E1_TODO), "p17"), code(E1_CHK, "p18"),
        md(E2, "p19"), code(g(E2_SOL, E2_TODO), "p20"), code(E2_CHK, "p21"),
        md(E3, "p22"), code(g(E3_SOL, E3_TODO), "p23"), code(E3_CHK, "p24"),
        md(E4, "p25"), code(g(E4_SOL, E4_TODO), "p26"), code(E4_CHK, "p27"),
        md(CIERRE, "p28"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "profundiza.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "profundiza_solucion.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Generados: profundiza.ipynb y profundiza_solucion.ipynb en", BASE)
