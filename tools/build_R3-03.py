"""build_R3-03.py — módulo R3-03 (RAG: tu asistente de trámites que cita la fuente).

Rama R3 (IA Aplicada). Rearmado 2026 (reemplaza la versión legacy, cuya fuente de datos
se retiró): RAG sobre el corpus COMPLETO de fichas ChileAtiende (fichas.csv, 245
trámites). Mantiene el arco del módulo — recuperación LÉXICA (sin embeddings) →
prompt aumentado → generar o abstenerse — y agrega trocear, citas (id/url) y una
evaluación simple de la recuperación (hit@k). LLM: preguntar_llm() común
(h.GET_LLM_SNIPPET) con respaldo extractivo: todo corre SIN clave ni red y ningún
assert depende de la respuesta en vivo del LLM. Profundiza = mejorar la recuperación
(peso del título, n-gramas, tamaño de trozo) y MEDIR cada cambio.

Uso:  /opt/anaconda3/bin/python tools/build_R3-03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-03-rag")

RAW = h.REPO_RAW

# ─────────────────────────────────────────────────────────────────────────────
# Piezas compartidas
# ─────────────────────────────────────────────────────────────────────────────
STOPWORDS_SRC = '''# Palabras vacías (sin tilde, porque el vectorizador quita las tildes antes de comparar)
STOPWORDS = """a al algo como con cual cuales cuando de del desde donde e el en entre es esta este esto
estos fue ha hay la las le les lo los mas me mi mis muy ni no o para pero por que quien se sea
segun si sin sobre son su sus te tiene tu tus un una uno unos y ya yo""".split()'''

PREGUNTAS_SRC = '''# Set de evaluación: preguntas redactadas como las haría una persona en la ventanilla,
# con la ficha que DEBERÍA aparecer (id de fichas.csv). Revisadas a mano una por una.
PREGUNTAS_EVAL = [
    ("¿Cómo saco el certificado de antecedentes?", 3442),
    ("¿Cómo me afilio a Fonasa?", 9715),
    ("¿Cómo obtengo un certificado de alumno regular?", 33265),
    ("¿Qué necesito para celebrar el acuerdo de unión civil?", 37532),
    ("¿Cómo saco la licencia para pescar como deporte?", 4636),
    ("¿Cuándo pagan el aguinaldo de Navidad a los pensionados?", 30171),
    ("¿Quiénes reciben el bono de invierno?", 39484),
    ("¿Cómo renuevo mi carnet si vivo fuera de Chile?", 48164),
    ("Me rechazaron la licencia médica porque la presenté tarde, ¿cómo apelo?", 9620),
    ("¿Cómo aviso que voy a hacer una quema en mi campo?", 742),
    ("¿Cómo busco trabajo en la bolsa de empleo del Estado?", 5072),
    ("¿Cómo cobro el fondo de cesantía solidario?", 36646),
    ("¿Cómo obtengo el certificado de discapacidad?", 83219),
    ("¿Qué es el bono marzo?", 38913),
    ("¿Dónde compro la entrada a un parque nacional?", 107334),
    ("Necesito un abogado gratis para divorciarme", 316),
    ("¿Cómo saco la ClaveÚnica estando en el extranjero?", 44751),
    ("Me despidieron injustamente, ¿dónde reclamo?", 120584),
    ("¿Cómo pido la pensión de alimentos para mis hijos?", 313),
    ("¿Cómo obtengo la tarjeta de alimentación para la universidad?", 2125),
]
print("Preguntas de evaluación:", len(PREGUNTAS_EVAL))'''

TROCEAR_SOL = '''def trocear(texto, max_palabras=120):
    trozos, actual, n = [], [], 0
    for linea in texto.split("\\n"):
        if not linea.strip():                    # las líneas en blanco no aportan
            continue
        palabras = len(linea.split())
        if actual and (linea.startswith("## ") or n + palabras > max_palabras):
            trozos.append("\\n".join(actual))
            actual, n = [], 0
        actual.append(linea)
        n += palabras
    if actual:
        trozos.append("\\n".join(actual))
    return trozos'''

# ─────────────────────────────────────────────────────────────────────────────
# LECCIÓN
# ─────────────────────────────────────────────────────────────────────────────
SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, re, urllib.request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "fichas.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/fichas.csv", CSV)

fichas = pd.read_csv(CSV)
print("Fichas:", len(fichas), "| temas:", fichas["tema"].nunique(),
      "| instituciones:", fichas["institucion"].nunique(),
      "| palabras por ficha (mediana):", int(fichas["n_palabras"].median()))
fichas[["id", "titulo", "tema", "institucion", "n_palabras"]].head()'''

LLM_MD = '''### El LLM detrás de una sola función

La celda siguiente define `preguntar_llm(prompt, respaldo=...)`, la misma de R3-02. Si configuraste
`GEMINI_API_KEY` en los **Secretos** de Colab (🔑), habla con Gemini en vivo; si no, devuelve el
`respaldo` y el notebook **sigue funcionando igual**. Ningún chequeo depende de lo que responda el LLM.

> Si en tu entorno falta el SDK de Google, instálalo con `!pip install -q google-genai`.'''

LLM_CELL = h.GET_LLM_SNIPPET + '''
print("Modelo:", MODELO, "| modo:", "EN VIVO" if _clave_gemini() else "RESPALDO (sin clave, todo funciona igual)")'''

INTRO = '''## RAG: un examen con libro abierto

Un LLM solo es un examen **a libro cerrado**: responde de memoria y, si no sabe, **inventa con
seguridad**. Pregúntale qué documentos pide un trámite específico y puede darte una lista
verosímil… y equivocada. **RAG** (*Retrieval-Augmented Generation*) lo convierte en un examen
**a libro abierto**: primero **busca** la página correcta y recién entonces **responde con ella
a la vista**, citando de dónde la sacó.

Hoy el «libro» es real: las **245 fichas de trámites de ChileAtiende** (18 temas, 64
instituciones), el mismo corpus que vienes usando en la rama. El flujo completo:

| Paso | Qué hace | Ejercicio |
|---|---|---|
| **Trocear** | Partir cada ficha en trozos manejables (una ficha mediana tiene ~435 palabras) | 1 |
| **Indexar** | Convertir cada trozo en un vector TF-IDF (la recuperación **léxica** de R3-01) | 2 |
| **Recuperar** | Encontrar los `k` trozos más parecidos a la pregunta | 3 |
| **Aumentar** | Armar el prompt con esos trozos, sus **citas** y la instrucción de no inventar | 4 |
| **Generar o abstenerse** | Responder con el LLM… o decir «no lo encontré» | 5 |
| **Evaluar** | Medir con preguntas reales si la ficha correcta aparece (hit@k) | 6 |

> Los sistemas grandes usan *embeddings* (vectores de significado) para recuperar. Aquí usamos
> TF-IDF a propósito: corre en cualquier computador, sin descargar modelos, y se entiende de punta
> a punta. El flujo RAG es **idéntico**; solo cambia cómo se mide el parecido.'''

STOP_MD = '''### Palabras vacías

Para buscar, «de», «la» o «para» no aportan nada: están en todas las fichas. Las dejamos fuera
con una lista corta de *stopwords* (la idea de R3-01).'''

EJ = [
 ("## 1. Trocear: de fichas a trozos",
  "Un LLM no puede leer las 245 fichas en cada pregunta (y aunque pudiera, sería caro y lento). "
  "Además, buscar sobre una ficha **entera** mezcla temas: la sección de requisitos y la de "
  "costos compiten. Por eso partimos cada ficha en **trozos** (*chunks*).\n\n"
  "Las fichas ya vienen organizadas en **secciones** con subtítulo (`## Requisitos`, `## Costo`, "
  "`## Trámite en línea`…): 244 de las 245 las traen, unas 4 por ficha. La sección es la unidad "
  "natural de corte. Pero algunas secciones son largas, así que hay un segundo criterio de tamaño.\n\n"
  "Regla de corte: se cierra el trozo actual y se empieza uno nuevo cuando (a) aparece un "
  "subtítulo `## ` **o** (b) agregar la línea haría pasar el trozo de `max_palabras`. Cada trozo "
  "conserva el `id`, el `titulo` y la `url` de su ficha: **eso es lo que después permite citar**.",
  "Completa la regla de corte de `trocear`",
  TROCEAR_SOL + '''

filas = []
for f in fichas.itertuples():
    for i, t in enumerate(trocear(f.texto)):
        filas.append({"id": f.id, "titulo": f.titulo, "url": f.url, "n_trozo": i, "texto": t})
trozos = pd.DataFrame(filas)
print("trozos:", len(trozos), "| trozos por ficha (mediana):", trozos.groupby("id").size().median())
trozos.head(3)''',
  '''def trocear(texto, max_palabras=120):
    trozos, actual, n = [], [], 0
    for linea in texto.split("\\n"):
        if not linea.strip():                    # las líneas en blanco no aportan
            continue
        palabras = len(linea.split())
        # TODO: cierra el trozo si YA hay algo en `actual` Y además
        #       (la línea empieza con "## "  O  n + palabras supera max_palabras)
        if ...:
            trozos.append("\\n".join(actual))
            actual, n = [], 0
        actual.append(linea)
        n += palabras
    if actual:
        trozos.append("\\n".join(actual))
    return trozos

filas = []
for f in fichas.itertuples():
    for i, t in enumerate(trocear(f.texto)):
        filas.append({"id": f.id, "titulo": f.titulo, "url": f.url, "n_trozo": i, "texto": t})
trozos = pd.DataFrame(filas)
print("trozos:", len(trozos))''',
  '''demo = "Intro corta.\\n## Requisitos\\nTener cédula vigente.\\n## Cómo hacerlo\\nIngresa al sitio."
partes = trocear(demo)
assert len(partes) == 3, f"el texto de prueba debería dar 3 trozos, dio {len(partes)}"
assert partes[1].startswith("## Requisitos"), "cada subtítulo '## ' debe abrir un trozo nuevo"
largo = "\\n".join(["uno dos tres cuatro cinco"] * 60)          # 300 palabras, sin subtítulos
assert all(len(p.split()) <= 120 for p in trocear(largo)), "ningún trozo debe pasar de max_palabras"
assert "" not in trocear(largo), "no debe haber trozos vacíos"
assert set(trozos["id"]) == set(fichas["id"]), "todas las fichas deben quedar troceadas"''',
  "La condición es: actual and (linea.startswith('## ') or n + palabras > max_palabras).",
  None),

 ("## 2. Indexar: cada trozo, un vector TF-IDF",
  "Ahora convertimos cada trozo en números con **TF-IDF** (R3-01): una palabra pesa más si es "
  "frecuente en el trozo y **rara** en el resto del corpus. «Fonasa» pesa mucho; «trámite», poco.\n\n"
  "Un detalle que hace una gran diferencia: a cada trozo le **anteponemos el título de su ficha**. "
  "Un trozo como «Presenta tu cédula de identidad en la sucursal» no dice de qué trámite habla; "
  "con el título adelante, sí. (En la profundización vas a **medir** cuánto aporta.)\n\n"
  "`TfidfVectorizer(strip_accents=\"unicode\", stop_words=STOPWORDS)` quita tildes y palabras "
  "vacías; `.fit_transform(documentos)` aprende el vocabulario y devuelve la matriz.",
  "Construye el vectorizador y la matriz `X`",
  '''documentos = trozos["titulo"] + "\\n" + trozos["texto"]     # cada trozo lleva su título
vectorizador = TfidfVectorizer(strip_accents="unicode", stop_words=STOPWORDS)
X = vectorizador.fit_transform(documentos)
print("matriz:", X.shape, "→ (trozos, palabras del vocabulario)")''',
  '''documentos = trozos["titulo"] + "\\n" + trozos["texto"]     # cada trozo lleva su título
# TODO: crea el vectorizador TF-IDF (strip_accents="unicode", stop_words=STOPWORDS)
vectorizador = ...
# TODO: ajústalo a `documentos` y transfórmalos en la matriz X
X = ...
print("matriz:", getattr(X, "shape", "todavía vacía"))''',
  '''assert X.shape[0] == len(trozos), "X debe tener una fila por trozo"
assert "fonasa" in vectorizador.vocabulary_, "el vocabulario debería incluir 'fonasa'"
assert "de" not in vectorizador.vocabulary_, "las stopwords no deben quedar en el vocabulario"''',
  'vectorizador = TfidfVectorizer(strip_accents="unicode", stop_words=STOPWORDS) y X = vectorizador.fit_transform(documentos).',
  None),

 ("## 3. Recuperar: los `k` trozos más parecidos",
  "La pregunta se transforma con el **mismo** vectorizador y se compara con todos los trozos. "
  "Como TF-IDF entrega vectores normalizados, el producto `X @ q.T` es directamente la "
  "**similitud coseno**: 0 = nada en común, 1 = idénticos.\n\n"
  "`np.argsort(-puntajes)` ordena los índices de mayor a menor puntaje; nos quedamos con los "
  "`k` primeros.",
  "Completa `recuperar`",
  '''def recuperar(pregunta, k=3):
    q = vectorizador.transform([pregunta])
    puntajes = (X @ q.T).toarray().ravel()
    mejores = np.argsort(-puntajes, kind="stable")[:k]
    resultado = trozos.iloc[mejores].copy()
    resultado["puntaje"] = puntajes[mejores]
    return resultado

recuperar("¿Cómo me afilio a Fonasa?")[["id", "titulo", "n_trozo", "puntaje"]]''',
  '''def recuperar(pregunta, k=3):
    q = vectorizador.transform([pregunta])
    # TODO: similitud de la pregunta con cada trozo: (X @ q.T).toarray().ravel()
    puntajes = ...
    # TODO: índices de los k mayores puntajes (usa np.argsort(-puntajes, kind="stable")[:k])
    mejores = ...
    resultado = trozos.iloc[mejores].copy()
    resultado["puntaje"] = puntajes[mejores]
    return resultado

# Pruébala cuando la completes:  recuperar("¿Cómo me afilio a Fonasa?")''',
  '''r = recuperar("¿Cómo me afilio a Fonasa?")
assert len(r) == 3 and len(recuperar("¿Cómo me afilio a Fonasa?", k=5)) == 5
assert r["id"].iloc[0] == 9715, f"el primer trozo debería ser de la ficha 9715 (Afiliación a Fonasa), salió {r['id'].iloc[0]}"
assert list(r["puntaje"]) == sorted(r["puntaje"], reverse=True), "los resultados deben ir de mayor a menor puntaje"''',
  "puntajes = (X @ q.T).toarray().ravel() y mejores = np.argsort(-puntajes, kind='stable')[:k].",
  None),

 ("## 4. Aumentar: el prompt con contexto y citas",
  "Con los trozos recuperados armamos el **prompt aumentado**. Tres ingredientes no negociables:\n\n"
  "1. Cada trozo va **etiquetado con su cita**: `[Ficha 9715 · https://www.chileatiende.gob.cl/fichas/9715]`.\n"
  "2. La instrucción de usar **SOLO** esos documentos y de **citar** la ficha usada.\n"
  "3. Una salida pactada para cuando no está la respuesta: `NO_ENCONTRADO`. Así el código puede "
  "detectar la abstención sin interpretar frases.",
  "Escribe `armar_prompt`",
  '''def armar_prompt(pregunta, contexto):
    bloques = [f"[Ficha {r.id} · {r.url}]\\n{r.texto}" for r in contexto.itertuples()]
    return ("Eres un asistente de trámites del Estado de Chile. Responde usando SOLO la "
            "información de los documentos.\\n"
            "Cita entre corchetes la ficha que usaste, por ejemplo [Ficha 9715].\\n"
            "Si los documentos no contienen la respuesta, responde exactamente: NO_ENCONTRADO\\n\\n"
            "Documentos:\\n" + "\\n\\n".join(bloques) +
            f"\\n\\nPregunta: {pregunta}\\nRespuesta:")

print(armar_prompt("¿Cómo me afilio a Fonasa?", recuperar("¿Cómo me afilio a Fonasa?", k=2))[:900])''',
  '''def armar_prompt(pregunta, contexto):
    # TODO: un bloque por trozo: f"[Ficha {r.id} · {r.url}]\\n{r.texto}"  (recorre contexto.itertuples())
    bloques = ...
    # TODO: instrucción (SOLO los documentos + citar + NO_ENCONTRADO) + documentos + pregunta
    return ...

# Pruébala:  print(armar_prompt("¿Cómo me afilio a Fonasa?", recuperar("¿Cómo me afilio a Fonasa?", k=2)))''',
  '''ctx = recuperar("¿Cómo me afilio a Fonasa?")
p = armar_prompt("¿Cómo me afilio a Fonasa?", ctx)
assert isinstance(p, str), "armar_prompt debe devolver un texto"
assert all(u in p for u in ctx["url"]), "cada trozo debe ir con su cita (la url de su ficha)"
assert all(t in p for t in ctx["texto"]), "el prompt debe incluir el texto de los trozos"
assert "¿Cómo me afilio a Fonasa?" in p, "falta la pregunta"
assert "solo" in p.lower() and "NO_ENCONTRADO" in p, "faltan la instrucción SOLO y la salida NO_ENCONTRADO"''',
  "bloques = [f'[Ficha {r.id} · {r.url}]\\n{r.texto}' for r in contexto.itertuples()] y une instrucción + bloques + pregunta.",
  None),

 ("## 5. Generar… o abstenerse",
  "Un asistente público confiable tiene **dos barreras** antes de responder:\n\n"
  "1. **Barrera de recuperación:** si ni el mejor trozo se parece a la pregunta "
  "(puntaje bajo `UMBRAL`), no llamamos al LLM: no hay nada que citar.\n"
  "2. **Barrera del LLM:** si el modelo responde `NO_ENCONTRADO`, también nos abstenemos.\n\n"
  "En ambos casos devolvemos un mensaje honesto que **deriva** a una persona. Si no hay clave, "
  "`preguntar_llm` devuelve un **respaldo extractivo**: el inicio del trozo más pertinente, con su cita.\n\n"
  "Fíjate en el parámetro `llm=preguntar_llm`: recibir el LLM como argumento permite **probar** "
  "la función con un LLM «falso» y predecible. Así los chequeos nunca dependen de lo que conteste "
  "el modelo en vivo.",
  "Implementa las dos barreras en `responder`",
  '''UMBRAL = 0.15
NO_SE = ("No encontré esa información en las fichas disponibles. "
         "Te sugiero consultar en chileatiende.gob.cl o con una persona de atención.")

def respaldo_extractivo(contexto):
    r = contexto.iloc[0]
    extracto = " ".join(r["texto"].split()[:60])
    return f"(Modo sin LLM) Lo más pertinente está en «{r['titulo']}» [Ficha {r['id']}]: {extracto}…"

def responder(pregunta, k=3, llm=preguntar_llm):
    contexto = recuperar(pregunta, k)
    if contexto["puntaje"].iloc[0] < UMBRAL:                     # barrera 1
        return {"respuesta": NO_SE, "fuentes": []}
    texto = llm(armar_prompt(pregunta, contexto), respaldo=respaldo_extractivo(contexto))
    if "NO_ENCONTRADO" in texto:                                  # barrera 2
        return {"respuesta": NO_SE, "fuentes": []}
    return {"respuesta": texto, "fuentes": list(contexto["url"].unique())}

r = responder("¿Cómo me afilio a Fonasa?")
print(r["respuesta"][:500]); print("Fuentes:", r["fuentes"])''',
  '''UMBRAL = 0.15
NO_SE = ("No encontré esa información en las fichas disponibles. "
         "Te sugiero consultar en chileatiende.gob.cl o con una persona de atención.")

def respaldo_extractivo(contexto):
    r = contexto.iloc[0]
    extracto = " ".join(r["texto"].split()[:60])
    return f"(Modo sin LLM) Lo más pertinente está en «{r['titulo']}» [Ficha {r['id']}]: {extracto}…"

def responder(pregunta, k=3, llm=preguntar_llm):
    contexto = recuperar(pregunta, k)
    # TODO barrera 1: si el mejor puntaje (contexto["puntaje"].iloc[0]) es menor que UMBRAL,
    #                 devuelve {"respuesta": NO_SE, "fuentes": []} SIN llamar al LLM
    ...
    texto = llm(armar_prompt(pregunta, contexto), respaldo=respaldo_extractivo(contexto))
    # TODO barrera 2: si "NO_ENCONTRADO" aparece en texto, devuelve lo mismo que en la barrera 1
    ...
    return {"respuesta": texto, "fuentes": list(contexto["url"].unique())}

# Pruébala:  responder("¿Cómo me afilio a Fonasa?")''',
  '''def llm_falso(prompt, respaldo=""):
    return "Debes inscribirte en Fonasa [Ficha 9715]."
def llm_no_sabe(prompt, respaldo=""):
    return "NO_ENCONTRADO"
def llm_prohibido(prompt, respaldo=""):
    raise RuntimeError("¡no se debía llamar al LLM sin contexto!")
dentro = responder("¿Cómo me afilio a Fonasa?", llm=llm_falso)
assert dentro["respuesta"] != NO_SE and "https://www.chileatiende.gob.cl/fichas/9715" in dentro["fuentes"], "con contexto relevante debe responder y citar la ficha 9715"
assert responder("¿Cómo me afilio a Fonasa?", llm=llm_no_sabe) == {"respuesta": NO_SE, "fuentes": []}, "barrera 2: si el LLM dice NO_ENCONTRADO, abstente"
fuera = responder("¿Cómo se prepara una empanada de pino?", llm=llm_prohibido)
assert fuera == {"respuesta": NO_SE, "fuentes": []}, "barrera 1: sin trozos parecidos, abstente sin llamar al LLM"''',
  "Barrera 1: if contexto['puntaje'].iloc[0] < UMBRAL: return {...}. Barrera 2: if 'NO_ENCONTRADO' in texto: return {...}.",
  '''# ¿Y si la pregunta NO está en el corpus pero comparte palabras? Mira los puntajes.
for q in ["¿Cómo se prepara una empanada de pino?", "¿Quién ganó la Copa América 2015?",
          "¿Cuál es la capital de Francia?"]:
    try:
        top = recuperar(q, k=1).iloc[0]
        print(f"{top['puntaje']:.2f}  «{top['titulo'][:45]}»  ← {q}")
    except Exception:
        print("Completa los ejercicios 1 a 3 para ver esta comparación.")
        break'''),
]

FALSO_POSITIVO = '''### ⚠️ El límite de la recuperación léxica

La empanada se queda en 0: ninguna ficha comparte sus palabras, y la barrera 1 funciona. Pero
mira las otras dos: «¿Cuál es la **capital** de Francia?» supera el umbral con holgura (≈ 0,43)
porque la ficha «Capital Abeja Emprende» contiene la palabra *capital*, y la Copa América también
pasa (≈ 0,24) por coincidencias sueltas. La búsqueda léxica compara **palabras**, no
**significados**. Y al revés: una pregunta legítima como «¿Cómo obtengo la tarjeta de alimentación
para la universidad?» queda **bajo** el umbral (≈ 0,15). El umbral es un compromiso, no una
garantía. Por eso existen las otras capas:

- La **barrera 2**: con el contexto a la vista, un LLM bien instruido responde `NO_ENCONTRADO`.
- La **cita**: aunque todo falle, quien lee ve que la «fuente» es un fondo para emprendedoras y desconfía.
- La **persona** que revisa: un asistente público no publica respuestas sin supervisión.

Ninguna capa es perfecta sola; juntas, hacen un sistema confiable.'''

EVAL_MD = '''## Evaluar: ¿la ficha correcta aparece?

«Funciona en las preguntas que probé» no es evidencia. Para saber si la recuperación sirve
necesitamos un **set de evaluación**: preguntas reales con su **respuesta esperada** (la ficha
correcta), escritas **antes** de mirar los resultados.

La métrica más simple es **hit@k**: la fracción de preguntas en las que la ficha esperada aparece
entre los `k` primeros trozos recuperados. hit@1 = «acertó al primer intento»; hit@3 = «estaba en
el contexto que vio el LLM».'''

EJ6 = ("## 6. Medir: hit@1 y hit@3",
  "Escribe `hit_at_k(preguntas, k)`: para cada `(pregunta, id_esperado)`, ¿está `id_esperado` "
  "entre los `id` de `recuperar(pregunta, k)`? Devuelve la fracción de aciertos.",
  "Escribe `hit_at_k`",
  '''def hit_at_k(preguntas, k):
    aciertos = [esperado in set(recuperar(p, k)["id"]) for p, esperado in preguntas]
    return sum(aciertos) / len(preguntas)

h1 = hit_at_k(PREGUNTAS_EVAL, 1)
h3 = hit_at_k(PREGUNTAS_EVAL, 3)
print(f"hit@1 = {h1:.2f}   |   hit@3 = {h3:.2f}")''',
  '''def hit_at_k(preguntas, k):
    # TODO: lista de True/False: ¿esperado está en set(recuperar(p, k)["id"])?
    aciertos = ...
    # TODO: fracción de aciertos
    return ...

h1 = hit_at_k(PREGUNTAS_EVAL, 1)
h3 = hit_at_k(PREGUNTAS_EVAL, 3)
print("hit@1 =", h1, "| hit@3 =", h3)''',
  '''ref1 = sum(e in set(recuperar(p, 1)["id"]) for p, e in PREGUNTAS_EVAL) / len(PREGUNTAS_EVAL)
ref3 = sum(e in set(recuperar(p, 3)["id"]) for p, e in PREGUNTAS_EVAL) / len(PREGUNTAS_EVAL)
assert abs(h1 - ref1) < 1e-9 and abs(h3 - ref3) < 1e-9, "revisa el cálculo de la fracción de aciertos"
assert 0 <= h1 <= h3 <= 1, "hit@3 nunca puede ser menor que hit@1"
assert hit_at_k([("¿Cómo me afilio a Fonasa?", 9715)], 1) == 1.0''',
  "aciertos = [esperado in set(recuperar(p, k)['id']) for p, esperado in preguntas]; return sum(aciertos) / len(preguntas).",
  '''# Diagnóstico: ¿en qué preguntas falla y qué recuperó en su lugar?
try:
    for p, e in PREGUNTAS_EVAL:
        top = recuperar(p, 3)
        if e not in set(top["id"]):
            esperado = fichas.loc[fichas["id"] == e, "titulo"].iloc[0]
            print(f"✗ {p}\\n   esperaba: «{esperado}»\\n   obtuvo:   «{top['titulo'].iloc[0]}»")
except Exception:
    print("Completa los ejercicios anteriores para ver el diagnóstico.")''')

CIERRE = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Mira las preguntas que fallaron. En casi todas, la persona usa **otras palabras** que la ficha:
«carnet» vs «cédula de identidad», «pescar» vs «pesca», «divorciarme» vs «divorcio». ¿Qué le dirías a
tu jefatura antes de poner este asistente en la página del servicio? ¿Qué porcentaje de hit@3
te parecería suficiente, y quién revisaría las respuestas?

## Errores típicos

- **Vectorizar la pregunta con un vectorizador nuevo** → los vectores no son comparables: usa
  siempre `vectorizador.transform`, nunca otro `fit`.
- **Responder sin cita** → si no puedes mostrar de qué ficha salió, no es RAG: es un LLM opinando.
- **Evaluar con las mismas preguntas con que ajustaste el sistema** → el número sale inflado.
- **Enviar datos personales en la pregunta** (RUT, diagnósticos) a un LLM externo: el prompt sale
  de tu institución. Anonimiza antes.

## Cierre

- **RAG = trocear → indexar → recuperar → aumentar → generar o abstenerse.** No hace al modelo más
  listo: le pone **la página correcta enfrente**.
- La **cita** (id + url de la ficha) es lo que vuelve **verificable** la respuesta.
- La **abstención** en dos barreras (umbral + `NO_ENCONTRADO`) es lo que lo vuelve **confiable**.
- Sin **evaluación** (hit@k con preguntas reales), «funciona» es solo una impresión.

> *En la profundización vas a subir esos números: título con más peso, n-gramas y otros tamaños
> de trozo — midiendo cada cambio. En R3-04 este buscador se vuelve una **herramienta** que un
> agente decide cuándo usar.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-03", "RAG: tu asistente de trámites que cita la fuente", "R3", "IA Aplicada", "4",
                      ["**Trocear** documentos largos en trozos con su cita (id y url).",
                       "Construir un **índice léxico TF-IDF** y **recuperar** los trozos más parecidos.",
                       "Armar un **prompt aumentado** con contexto, citas y salida de abstención.",
                       "**Generar o abstenerse** con dos barreras, sin depender de la red.",
                       "**Evaluar** la recuperación con preguntas reales (hit@k)."],
                      "construir un asistente de preguntas y respuestas sobre documentos públicos que cita la fuente, se abstiene cuando no sabe y se evalúa con evidencia.",
                      "las 245 fichas de trámites de ChileAtiende (texto completo, 18 temas, 64 instituciones).",
                      n_checks=6),
        h.code(SETUP),
        h.md(LLM_MD),
        h.code(LLM_CELL),
        h.md(INTRO),
        h.md(STOP_MD),
        h.code(STOPWORDS_SRC),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(FALSO_POSITIVO))
    cells.append(h.md(EVAL_MD))
    cells.append(h.code(PREGUNTAS_SRC))
    sec_t, sec_b, ej_t, sol, todo, chk, hint, viz = EJ6
    cells.append(h.md(sec_t + "\n\n" + sec_b))
    cells.append(h.exercise_md(6, ej_t))
    cells.append(h.code(sol if con_sol else todo))
    cells.append(h.check_cell(6, chk, hint))
    cells.append(h.code(viz))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ─────────────────────────────────────────────────────────────────────────────
# PROFUNDIZA — mejorar la recuperación y medir
# ─────────────────────────────────────────────────────────────────────────────
PROF_HEADER = '''# R3-03 · RAG — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional. En la lección la recuperación acertó la ficha correcta al primer intento en
**la mitad** de las preguntas (hit@1 = 0,50). Aquí la vas a mejorar como se hace en serio:
**un cambio a la vez, midiendo cada uno** con el mismo set de preguntas.

Palancas que vas a probar: **peso del título**, **n-gramas** (de palabras y de caracteres) y
**tamaño del trozo**. Todo corre sin red ni LLM: es pura recuperación.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_PREP = f'''import os, urllib.request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

CSV = "fichas.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/fichas.csv", CSV)
fichas = pd.read_csv(CSV)

{STOPWORDS_SRC}

{TROCEAR_SOL}

def construir_indice(max_palabras=120, peso_titulo=1, **opciones):
    """Trocea (max_palabras=None = ficha completa), antepone el título `peso_titulo` veces
    y vectoriza con TF-IDF.
    `opciones` se pasan tal cual a TfidfVectorizer (ej. ngram_range, analyzer)."""
    filas = [{{"id": f.id, "titulo": f.titulo, "url": f.url, "texto": t}}
             for f in fichas.itertuples()
             for t in ([f.texto] if max_palabras is None else trocear(f.texto, max_palabras))]
    trozos = pd.DataFrame(filas)
    documentos = (trozos["titulo"] + "\\n") * peso_titulo + trozos["texto"]
    opciones = {{"strip_accents": "unicode", **opciones}}
    if opciones.get("analyzer", "word") == "word":
        opciones.setdefault("stop_words", STOPWORDS)
    vect = TfidfVectorizer(**opciones)
    return {{"trozos": trozos, "vect": vect, "X": vect.fit_transform(documentos)}}

def recuperar(indice, pregunta, k=3):
    puntajes = (indice["X"] @ indice["vect"].transform([pregunta]).T).toarray().ravel()
    mejores = np.argsort(-puntajes, kind="stable")[:k]
    res = indice["trozos"].iloc[mejores].copy()
    res["puntaje"] = puntajes[mejores]
    return res

def hit_at_k(indice, k, preguntas=None):
    preguntas = preguntas or PREGUNTAS_EVAL
    return sum(e in set(recuperar(indice, p, k)["id"]) for p, e in preguntas) / len(preguntas)

{PREGUNTAS_SRC}'''

PROF_EJ = [
 ("## 1. La línea base (y cuánto vale el título)",
  "Primero, el punto de partida: el índice de la lección (`construir_indice()` con sus valores "
  "por defecto: trozos de 120 palabras, título una vez, palabras sueltas). Después, la misma "
  "receta **sin** título (`peso_titulo=0`). Nunca cambies algo sin saber desde dónde partes.",
  "Mide la línea base y la versión sin título",
  '''base = construir_indice()
sin_titulo = construir_indice(peso_titulo=0)
resultados = {
    "base":       (hit_at_k(base, 1), hit_at_k(base, 3)),
    "sin_titulo": (hit_at_k(sin_titulo, 1), hit_at_k(sin_titulo, 3)),
}
for nombre, (h1, h3) in resultados.items():
    print(f"{nombre:12s} hit@1={h1:.2f}  hit@3={h3:.2f}")''',
  '''base = construir_indice()
# TODO: índice SIN título (peso_titulo=0)
sin_titulo = ...
# TODO: completa los hit@1 y hit@3 de cada índice con hit_at_k(indice, k)
resultados = {
    "base":       (..., ...),
    "sin_titulo": (..., ...),
}
print(resultados)''',
  '''assert resultados["base"] == (hit_at_k(base, 1), hit_at_k(base, 3))
assert resultados["sin_titulo"] == (hit_at_k(sin_titulo, 1), hit_at_k(sin_titulo, 3))
assert resultados["sin_titulo"][0] < resultados["base"][0], "sin título, hit@1 debería caer"''',
  "sin_titulo = construir_indice(peso_titulo=0); cada tupla es (hit_at_k(indice, 1), hit_at_k(indice, 3))."),

 ("## 2. Títulos con más peso",
  "Si el título ayuda tanto, ¿y si pesa más? Repetir el título `n` veces es un truco simple para "
  "que sus palabras cuenten más en TF-IDF. Prueba `peso_titulo` en 1, 2, 3 y 5 y quédate con el "
  "mejor (primero por hit@1; si empatan, por hit@3).",
  "Encuentra el mejor `peso_titulo`",
  '''por_peso = {}
for peso in [1, 2, 3, 5]:
    ind = construir_indice(peso_titulo=peso)
    por_peso[peso] = (hit_at_k(ind, 1), hit_at_k(ind, 3))
    print(f"peso {peso}: hit@1={por_peso[peso][0]:.2f}  hit@3={por_peso[peso][1]:.2f}")
mejor_peso = max(por_peso, key=lambda p: por_peso[p])
print("mejor peso:", mejor_peso)''',
  '''por_peso = {}
for peso in [1, 2, 3, 5]:
    # TODO: construye el índice con ese peso y guarda (hit@1, hit@3) en por_peso[peso]
    ...
# TODO: el peso con mejor (hit@1, hit@3)  — pista: max(por_peso, key=lambda p: por_peso[p])
mejor_peso = ...
print(por_peso, "→ mejor:", mejor_peso)''',
  '''assert set(por_peso) == {1, 2, 3, 5}
assert por_peso[mejor_peso] == max(por_peso.values())
assert por_peso[mejor_peso][0] > resultados["base"][0], "el mejor peso debería superar a la línea base en hit@1"''',
  "Dentro del for: ind = construir_indice(peso_titulo=peso); por_peso[peso] = (hit_at_k(ind, 1), hit_at_k(ind, 3))."),

 ("## 3. N-gramas: pares de palabras y trozos de palabra",
  "Muchas fallas eran de **vocabulario**: «pescar» vs «pesca», «divorciarme» vs «divorcio». Dos "
  "variantes de TF-IDF atacan eso de distinta forma:\n\n"
  "- `ngram_range=(1, 2)`: además de palabras sueltas, **pares** («licencia médica», «bono marzo»).\n"
  "- `analyzer=\"char_wb\", ngram_range=(3, 5)`: pedacitos de **3 a 5 letras** dentro de cada "
  "palabra. «pescar» y «pesca» comparten «pes», «esc», «pesc»… y se vuelven parecidas.\n\n"
  "Mide ambas con el mejor peso de título.",
  "Compara bigramas y n-gramas de caracteres",
  '''bigramas = construir_indice(peso_titulo=mejor_peso, ngram_range=(1, 2))
caracteres = construir_indice(peso_titulo=mejor_peso, analyzer="char_wb", ngram_range=(3, 5))
por_ngrama = {
    "palabras (1,2)":   (hit_at_k(bigramas, 1), hit_at_k(bigramas, 3)),
    "caracteres (3,5)": (hit_at_k(caracteres, 1), hit_at_k(caracteres, 3)),
}
for nombre, (h1, h3) in por_ngrama.items():
    print(f"{nombre:17s} hit@1={h1:.2f}  hit@3={h3:.2f}")
print(recuperar(caracteres, "¿Cómo saco la licencia para pescar como deporte?", 1)["titulo"].iloc[0])''',
  '''# TODO: índice con pares de palabras (ngram_range=(1, 2)) y el mejor peso de título
bigramas = ...
# TODO: índice con n-gramas de caracteres (analyzer="char_wb", ngram_range=(3, 5))
caracteres = ...
por_ngrama = {
    "palabras (1,2)":   (..., ...),
    "caracteres (3,5)": (..., ...),
}
print(por_ngrama)''',
  '''assert por_ngrama["palabras (1,2)"] == (hit_at_k(bigramas, 1), hit_at_k(bigramas, 3))
assert por_ngrama["caracteres (3,5)"] == (hit_at_k(caracteres, 1), hit_at_k(caracteres, 3))
assert por_ngrama["caracteres (3,5)"][1] > resultados["base"][1], "los n-gramas de caracteres deberían mejorar hit@3"''',
  'construir_indice(peso_titulo=mejor_peso, ngram_range=(1, 2)) y construir_indice(peso_titulo=mejor_peso, analyzer="char_wb", ngram_range=(3, 5)).'),

 ("## 4. Otro tamaño de trozo",
  "¿Trozos chicos (más precisos, pero con menos contexto) o grandes (más contexto, pero mezclan "
  "temas)? Con la mejor configuración hasta ahora (mejor peso + n-gramas de caracteres), prueba "
  "`max_palabras` = 60, 120, 250 y la **ficha completa** (`None` = no trocear).",
  "Mide el efecto del tamaño de trozo",
  '''filas = []
for mp in [60, 120, 250, None]:
    ind = construir_indice(max_palabras=mp, peso_titulo=mejor_peso, analyzer="char_wb", ngram_range=(3, 5))
    filas.append({"max_palabras": mp or "ficha completa", "trozos": len(ind["trozos"]),
                  "hit@1": hit_at_k(ind, 1), "hit@3": hit_at_k(ind, 3)})
tabla_trozos = pd.DataFrame(filas)
tabla_trozos''',
  '''filas = []
for mp in [60, 120, 250, None]:
    # TODO: 1) ind = índice con max_palabras=mp, peso_titulo=mejor_peso y n-gramas de caracteres (3, 5)
    #       2) agrega a `filas` un dict con: "max_palabras" (mp, o "ficha completa" si mp es None),
    #          "trozos" (len(ind["trozos"])), "hit@1" y "hit@3"
    ...
tabla_trozos = pd.DataFrame(filas)
tabla_trozos''',
  '''assert len(tabla_trozos) == 4 and list(tabla_trozos["max_palabras"])[:3] == [60, 120, 250]
assert tabla_trozos["trozos"].is_monotonic_decreasing, "más palabras por trozo = menos trozos"
completa = tabla_trozos.iloc[-1]
assert completa["trozos"] == len(fichas), "sin trocear debería quedar un trozo por ficha"
assert completa["hit@1"] < tabla_trozos["hit@1"].max(), "la ficha completa no debería ser la mejor opción"''',
  'ind = construir_indice(max_palabras=mp, peso_titulo=mejor_peso, analyzer="char_wb", ngram_range=(3, 5)).'),

 ("## 5. Desafío: la tabla final y la trampa del sobreajuste",
  "Junta todo en una tabla `comparacion` (una fila por configuración —incluidos los tamaños de "
  "trozo del ejercicio 4—, columnas `hit@1` y `hit@3`), "
  "ordénala de mejor a peor y elige la `ganadora`.\n\n"
  "**La trampa:** elegiste la configuración mirando **las mismas 20 preguntas** con que la mides. "
  "Es como estudiar con la prueba en la mano. Antes de llevarla a producción, escribe preguntas "
  "**nuevas** (idealmente, de personas reales de tu servicio) y vuelve a medir.",
  "Arma la comparación y elige la ganadora",
  '''comparacion = pd.DataFrame(
    {"base (lección)": resultados["base"],
     "sin título": resultados["sin_titulo"],
     f"título x{mejor_peso}": por_peso[mejor_peso],
     **{f"título x{mejor_peso} + {k}": v for k, v in por_ngrama.items()},
     **{f"título x{mejor_peso} + caracteres + trozos de {f['max_palabras']}": (f["hit@1"], f["hit@3"])
        for f in tabla_trozos.to_dict("records") if f["max_palabras"] != 120}},   # 120 ya está arriba
    index=["hit@1", "hit@3"]).T.sort_values(["hit@1", "hit@3"], ascending=False)
ganadora = comparacion.index[0]
print(comparacion)
print("\\nGanadora:", ganadora)''',
  '''# TODO: DataFrame con una fila por configuración y columnas hit@1, hit@3,
#       ordenado de mejor a peor (sort_values(["hit@1", "hit@3"], ascending=False))
comparacion = ...
# TODO: el nombre de la primera fila
ganadora = ...
print(comparacion)''',
  '''assert {"hit@1", "hit@3"} <= set(comparacion.columns)
assert len(comparacion) >= 4
assert list(comparacion["hit@1"]) == sorted(comparacion["hit@1"], reverse=True)
assert ganadora == comparacion.index[0]''',
  "pd.DataFrame({nombre: (h1, h3), ...}, index=['hit@1','hit@3']).T.sort_values(['hit@1','hit@3'], ascending=False); ganadora = comparacion.index[0]."),
]

PROF_CIERRE = '''## Para llevar

- **Un cambio a la vez, medido**: así se mejora un RAG. Sin set de evaluación, cada «mejora» es una opinión.
- El **título** es el metadato más barato y el que más aporta: un trozo sin contexto no se encuentra.
- Los **n-gramas de caracteres** absorben variaciones de palabras (conjugaciones, plurales, errores
  de tipeo) sin diccionarios ni modelos pesados.
- Trozos **demasiado grandes** diluyen la señal; la ficha completa casi nunca es la mejor unidad.
- **20 preguntas son pocas** y las usaste para elegir: la cifra final está inflada. Agrega
  preguntas nuevas antes de confiar en ella.

---

*Fin de la profundización de R3-03.*'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md(PROF_CIERRE))
    nb.cells = cells
    return nb


README = '''# R3-03 · RAG: tu asistente de trámites que cita la fuente

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-03-rag/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías y autoevaluación.

RAG sobre el corpus completo de **245 fichas de trámites de ChileAtiende** (`fichas.csv`):
trocear (por subtítulos `## ` y por tamaño), índice léxico **TF-IDF**, recuperación top-k,
prompt aumentado con **citas** (id y url de la ficha), generación con `preguntar_llm()` y
**abstención** en dos barreras. Cierra **midiendo** la recuperación con 20 preguntas reales
(hit@k). Funciona **sin clave ni red**: sin `GEMINI_API_KEY`, el LLM devuelve un respaldo
extractivo y todos los chequeos pasan igual.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅). 6 chequeos.
- `profundiza.ipynb` — opcional 🔬: mejorar la recuperación (peso del título, n-gramas de
  palabras y de caracteres, tamaño de trozo) **midiendo** cada cambio. 5 chequeos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-03-rag/profundiza.ipynb) ← profundización

*Fuente de datos: fichas de trámites de [ChileAtiende](https://www.chileatiende.gob.cl) (contenido público del Estado de Chile).*
'''


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(README)
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
