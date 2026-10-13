"""build_R3-CAP.py — Capstone de la rama R3 (IA Aplicada).

Proyecto-plantilla integrador. Rearmado 2026 (reemplaza el mini-RAG legacy, cuya
fuente se retiró): un ASISTENTE DE TRÁMITES con RAG sobre las 245 fichas de ChileAtiende
(fichas.csv) como ejemplo — reemplazable por documentos o datos propios del servicio
(banco: propio > banco bootcamp > datos.gob.cl). Recorre: preparar el corpus con un
adaptador de columnas → índice (receta de la profundización de R3-03) → evaluación con
preguntas propias (hit@k) → responder con citas y abstención con preguntar_llm()
común → ficha de uso responsable (riesgos/ética) → rúbrica con Pertinencia y
Riesgos/ética. Todo corre SIN clave ni red; ningún assert depende del LLM en vivo.
Profundiza: calibrar el umbral de abstención con evidencia, filtrar por metadatos
(tema) y bitácora de auditoría anonimizada. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R3-CAP.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-CAP-capstone-ia-aplicada")

RAW = h.REPO_RAW

TROCEAR_SRC = '''def trocear(texto, max_palabras=120):
    """Corta en cada subtítulo '## ' o al pasar de max_palabras (la función de R3-03)."""
    trozos, actual, n = [], [], 0
    for linea in str(texto).split("\\n"):
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

MIS_PREGUNTAS_SRC = '''# Tus preguntas de evaluación: (pregunta, id del documento que DEBERÍA aparecer).
# Escríbelas ANTES de mirar resultados. Estas son de ejemplo para el corpus de fichas:
# reemplázalas por preguntas reales de las personas que atiende tu servicio.
MIS_PREGUNTAS = [
    ("¿Cuándo se paga el aguinaldo de Fiestas Patrias a los pensionados?", 26553),
    ("¿Qué es la Pensión Garantizada Universal y cuánto aumentó?", 130457),
    ("¿Cómo cambio mi domicilio si soy pensionado del IPS y vivo afuera?", 6347),
    ("¿Cómo pido asesoría previsional gratuita?", 9648),
    ("¿Cómo obtengo el certificado de alumno prioritario?", 20613),
    ("¿Qué es el Bolsillo Familiar Electrónico?", 115303),
    ("¿Cómo postulo al Capital Semilla Emprende?", 20608),
    ("¿Cómo pido la Beca Bicentenario?", 2227),
    ("¿Quién recibe el Aporte Familiar Permanente?", 38913),
    ("¿Cómo me inscribo en la Bolsa Nacional de Empleo?", 5072),
    ("Me rechazaron la licencia porque dicen que no hice reposo, ¿qué hago?", 3976),
    ("¿Hay ayuda para pagar la casa de reposo de mi mamá?", 5039),
]'''

# ─────────────────────────────────────────────────────────────────────────────
# LECCIÓN (plantilla)
# ─────────────────────────────────────────────────────────────────────────────
SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, re, json, urllib.request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# 👉 Cambia esto por tu propio corpus (un CSV con una fila por documento).
CORPUS_CSV = "fichas.csv"
if not os.path.exists(CORPUS_CSV):                     # "en vivo o caché"
    urllib.request.urlretrieve(f"{RAW}/{{CORPUS_CSV}}", CORPUS_CSV)

crudo = pd.read_csv(CORPUS_CSV)
print("Corpus crudo:", crudo.shape)
crudo.head(3)'''

LLM_MD = '''### El LLM detrás de una sola función

La misma `preguntar_llm(prompt, respaldo=...)` de toda la rama. Con `GEMINI_API_KEY` en los
Secretos de Colab responde en vivo; sin ella devuelve el respaldo. **Tu capstone debe correr
completo sin clave** (es el criterio de reproducibilidad de la rúbrica).

> Si en tu entorno falta el SDK de Google, instálalo con `!pip install -q google-genai`.'''

LLM_CELL = h.GET_LLM_SNIPPET + '''
print("Modelo:", MODELO, "| modo:", "EN VIVO" if _clave_gemini() else "RESPALDO (sin clave)")'''

ENMARCA = '''## 0. Enmarca tu proyecto

Antes de escribir código, responde en una frase cada una:

> **¿Quién pregunta?** _(ciudadanía, funcionarios de otra unidad, tu propia jefatura…)_
>
> **¿Qué pregunta?** _(el tipo de consultas que hoy se responden a mano, una y otra vez)_
>
> **¿Con qué documentos o datos se responde?** _(y quién es su dueño)_
>
> **¿Qué pasa si el asistente se equivoca?** _(esto define cuánta supervisión humana necesitas)_

### Elige tu corpus (en este orden de preferencia)

1. **Documentos o datos de tu propio servicio** — el capstone vale el doble si resuelve un
   problema real: preguntas frecuentes, instructivos, reglamentos internos, respuestas tipo de
   la OIRS… **siempre públicos y sin datos personales**.
2. El **banco del bootcamp** (todos reales, en `data/` del repositorio):
   `fichas.csv` (245 trámites de ChileAtiende con texto completo — el ejemplo de esta plantilla) ·
   `matricula.csv` (matrícula escolar 2025, MINEDUC) · `aire_diario.csv` + `estaciones.csv`
   (PM2.5 diario SINCA) · `reclamos.csv` (reclamos de consumo SERNAC, por categoría) ·
   `sismos.csv` (catálogo USGS).
3. Cualquier conjunto de **datos.gob.cl**.

### Dos caminos

| Si tu corpus es… | Construye… | Plantilla |
|---|---|---|
| **Texto** (fichas, instructivos, normas) | Un **asistente RAG** que responde citando y se abstiene | Este notebook |
| **Tablas** (matrícula, aire, tus registros) | Un **agente** con herramientas, traza y aprobación humana | R3-04 (cambia las herramientas por consultas a tus datos) |

> Esta plantilla sigue el camino **RAG** con `fichas.csv`. Para usar tus documentos, ajusta
> `CORPUS_CSV` y el diccionario `COLUMNAS` del ejercicio 1; el resto funciona igual.'''

EJ = [
 ("## 1. Prepara el corpus (el adaptador)",
  "Cada fuente trae sus columnas con otros nombres. El **adaptador** traduce tu tabla al formato "
  "que espera el resto del notebook: `id`, `titulo`, `url` y `texto` (la `url` es la **cita**; si "
  "tus documentos no tienen url, usa el nombre del archivo o el número de resolución). Además "
  "limpia: sin textos vacíos y sin `id` repetidos.",
  "Completa `preparar_corpus`",
  '''# Nombre de TU columna para cada campo que necesita el asistente
COLUMNAS = {"id": "id", "titulo": "titulo", "url": "url", "texto": "texto"}

def preparar_corpus(df, columnas=COLUMNAS):
    corpus = df.rename(columns={v: k for k, v in columnas.items()})[list(columnas)]
    corpus = corpus.dropna(subset=["texto"])
    corpus = corpus[corpus["texto"].str.strip() != ""]
    corpus = corpus.drop_duplicates(subset="id")
    return corpus.reset_index(drop=True)

corpus = preparar_corpus(crudo)
print("Documentos:", len(corpus))
corpus.head(3)''',
  '''# Nombre de TU columna para cada campo que necesita el asistente
COLUMNAS = {"id": "id", "titulo": "titulo", "url": "url", "texto": "texto"}

def preparar_corpus(df, columnas=COLUMNAS):
    corpus = df.rename(columns={v: k for k, v in columnas.items()})[list(columnas)]
    # TODO: quita filas con texto nulo (dropna), con texto vacío ("") y con id repetido (drop_duplicates)
    ...
    return corpus.reset_index(drop=True)

corpus = preparar_corpus(crudo)
print("Documentos:", len(corpus))''',
  '''assert list(corpus.columns) == ["id", "titulo", "url", "texto"]
assert corpus["id"].is_unique, "no puede haber id repetidos"
prueba = pd.DataFrame({"id": [1, 1, 2, 3], "titulo": ["a", "a", "b", "c"], "url": ["u", "u", "v", "w"],
                       "texto": ["hola", "hola", None, "  "]})
assert len(preparar_corpus(prueba)) == 1, "debe quitar duplicados, nulos y textos vacíos"''',
  'corpus = corpus.dropna(subset=["texto"]); corpus = corpus[corpus["texto"].str.strip() != ""]; corpus = corpus.drop_duplicates(subset="id").',
  None),

 ("## 2. Construye el índice",
  "Usamos la receta que mejor funcionó en la profundización de R3-03: el **título repetido 3 "
  "veces** y n-gramas de **caracteres** (3 a 5), que absorben variaciones como «pescar»/«pesca». "
  "El tamaño de trozo (aquí 120 palabras; en R3-03 también rindió bien 60) depende de tu corpus: "
  "pruébalo con tu evaluación del ejercicio 3. `recuperar` ya está escrita; completa `construir_indice`.",
  "Completa `construir_indice`",
  TROCEAR_SRC + '''

def construir_indice(corpus, max_palabras=120, peso_titulo=3):
    trozos = pd.DataFrame([{"id": d.id, "titulo": d.titulo, "url": d.url, "texto": t}
                           for d in corpus.itertuples() for t in trocear(d.texto, max_palabras)])
    vect = TfidfVectorizer(strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5))
    X = vect.fit_transform((trozos["titulo"] + "\\n") * peso_titulo + trozos["texto"])
    return {"trozos": trozos, "vect": vect, "X": X}

def recuperar(indice, pregunta, k=3):
    puntajes = (indice["X"] @ indice["vect"].transform([pregunta]).T).toarray().ravel()
    mejores = np.argsort(-puntajes, kind="stable")[:k]
    res = indice["trozos"].iloc[mejores].copy()
    res["puntaje"] = puntajes[mejores]
    return res

indice = construir_indice(corpus)
print("Trozos:", len(indice["trozos"]), "| matriz:", indice["X"].shape)
recuperar(indice, "¿Cómo me afilio a Fonasa?")[["id", "titulo", "puntaje"]]''',
  TROCEAR_SRC + '''

def construir_indice(corpus, max_palabras=120, peso_titulo=3):
    trozos = pd.DataFrame([{"id": d.id, "titulo": d.titulo, "url": d.url, "texto": t}
                           for d in corpus.itertuples() for t in trocear(d.texto, max_palabras)])
    # TODO: vectorizador TF-IDF con strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5)
    vect = ...
    # TODO: X = ajusta y transforma (título + "\\n") * peso_titulo + texto de cada trozo
    X = ...
    return {"trozos": trozos, "vect": vect, "X": X}

def recuperar(indice, pregunta, k=3):
    puntajes = (indice["X"] @ indice["vect"].transform([pregunta]).T).toarray().ravel()
    mejores = np.argsort(-puntajes, kind="stable")[:k]
    res = indice["trozos"].iloc[mejores].copy()
    res["puntaje"] = puntajes[mejores]
    return res

indice = construir_indice(corpus)
print("Trozos:", len(indice["trozos"]))''',
  '''assert indice["X"].shape[0] == len(indice["trozos"]), "una fila de X por trozo"
assert set(indice["trozos"]["id"]) == set(corpus["id"]), "todos los documentos deben quedar indexados"
r = recuperar(indice, "¿Cómo me afilio a Fonasa?")
assert len(r) == 3 and list(r["puntaje"]) == sorted(r["puntaje"], reverse=True)''',
  'vect = TfidfVectorizer(strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5)); X = vect.fit_transform((trozos["titulo"] + "\\n") * peso_titulo + trozos["texto"]).',
  None),

 ("## 3. Evalúa con TUS preguntas",
  "Sin evaluación no hay capstone. Escribe al menos **8 preguntas** reales con el documento que "
  "debería aparecer, y mide **hit@1** y **hit@3** (R3-03). Si tu hit@3 queda bajo 0,7, vuelve al "
  "ejercicio 2 y prueba otra configuración — y **anótalo** en tu informe.",
  "Arma tu `informe_eval`",
  MIS_PREGUNTAS_SRC + '''

def hit_at_k(indice, preguntas, k):
    return sum(e in set(recuperar(indice, p, k)["id"]) for p, e in preguntas) / len(preguntas)

informe_eval = {"n_preguntas": len(MIS_PREGUNTAS),
                "hit@1": hit_at_k(indice, MIS_PREGUNTAS, 1),
                "hit@3": hit_at_k(indice, MIS_PREGUNTAS, 3)}
print(informe_eval)''',
  MIS_PREGUNTAS_SRC + '''

def hit_at_k(indice, preguntas, k):
    return sum(e in set(recuperar(indice, p, k)["id"]) for p, e in preguntas) / len(preguntas)

# TODO: completa el informe con el número de preguntas, hit@1 y hit@3
informe_eval = {"n_preguntas": ..., "hit@1": ..., "hit@3": ...}
print(informe_eval)''',
  '''assert len(MIS_PREGUNTAS) >= 8, "necesitas al menos 8 preguntas de evaluación"
assert all(e in set(corpus["id"]) for _, e in MIS_PREGUNTAS), "cada id esperado debe existir en tu corpus"
assert informe_eval["n_preguntas"] == len(MIS_PREGUNTAS)
assert informe_eval["hit@1"] == hit_at_k(indice, MIS_PREGUNTAS, 1)
assert informe_eval["hit@3"] == hit_at_k(indice, MIS_PREGUNTAS, 3)''',
  'informe_eval = {"n_preguntas": len(MIS_PREGUNTAS), "hit@1": hit_at_k(indice, MIS_PREGUNTAS, 1), "hit@3": hit_at_k(indice, MIS_PREGUNTAS, 3)}.',
  None),

 ("## 4. Responde con citas… o abstente",
  "El corazón del asistente (R3-03): prompt con los trozos **citados**, instrucción de usar **solo** "
  "esos documentos, y **dos barreras** de abstención — el umbral de recuperación y la salida "
  "`NO_ENCONTRADO` del LLM. Con n-gramas de caracteres los puntajes son más altos que con "
  "palabras, por eso aquí el umbral es **0,30** (en la profundización lo calibras con evidencia).\n\n"
  "Completa las dos barreras. Recuerda: `llm` es un parámetro para poder probar con LLM «falsos».",
  "Completa las barreras de `responder`",
  '''UMBRAL = 0.30
NO_SE = ("No encontré esa información en los documentos disponibles. "
         "Te sugiero consultar con una persona de atención.")

def armar_prompt(pregunta, contexto):
    bloques = [f"[Doc {r.id} · {r.url}]\\n{r.texto}" for r in contexto.itertuples()]
    return ("Eres un asistente de atención del Estado de Chile. Responde en lenguaje claro usando SOLO "
            "los documentos. Cita entre corchetes el documento usado, por ejemplo [Doc 9715]. "
            "Si los documentos no contienen la respuesta, responde exactamente: NO_ENCONTRADO\\n\\n"
            "Documentos:\\n" + "\\n\\n".join(bloques) + f"\\n\\nPregunta: {pregunta}\\nRespuesta:")

def responder(pregunta, k=3, llm=preguntar_llm):
    contexto = recuperar(indice, pregunta, k)
    if contexto["puntaje"].iloc[0] < UMBRAL:                      # barrera 1
        return {"respuesta": NO_SE, "fuentes": []}
    primero = contexto.iloc[0]
    respaldo = (f"(Modo sin LLM) Revisa «{primero['titulo']}» [Doc {primero['id']}]: "
                + " ".join(primero["texto"].split()[:50]) + "…")
    texto = llm(armar_prompt(pregunta, contexto), respaldo=respaldo)
    if "NO_ENCONTRADO" in texto:                                   # barrera 2
        return {"respuesta": NO_SE, "fuentes": []}
    return {"respuesta": texto, "fuentes": list(contexto["url"].unique())}

r = responder("¿Cómo pido la Beca Bicentenario?")
print(r["respuesta"][:400]); print("Fuentes:", r["fuentes"])''',
  '''UMBRAL = 0.30
NO_SE = ("No encontré esa información en los documentos disponibles. "
         "Te sugiero consultar con una persona de atención.")

def armar_prompt(pregunta, contexto):
    bloques = [f"[Doc {r.id} · {r.url}]\\n{r.texto}" for r in contexto.itertuples()]
    return ("Eres un asistente de atención del Estado de Chile. Responde en lenguaje claro usando SOLO "
            "los documentos. Cita entre corchetes el documento usado, por ejemplo [Doc 9715]. "
            "Si los documentos no contienen la respuesta, responde exactamente: NO_ENCONTRADO\\n\\n"
            "Documentos:\\n" + "\\n\\n".join(bloques) + f"\\n\\nPregunta: {pregunta}\\nRespuesta:")

def responder(pregunta, k=3, llm=preguntar_llm):
    contexto = recuperar(indice, pregunta, k)
    # TODO barrera 1: si contexto["puntaje"].iloc[0] < UMBRAL → return {"respuesta": NO_SE, "fuentes": []}
    ...
    primero = contexto.iloc[0]
    respaldo = (f"(Modo sin LLM) Revisa «{primero['titulo']}» [Doc {primero['id']}]: "
                + " ".join(primero["texto"].split()[:50]) + "…")
    texto = llm(armar_prompt(pregunta, contexto), respaldo=respaldo)
    # TODO barrera 2: si "NO_ENCONTRADO" está en texto → la misma abstención
    ...
    return {"respuesta": texto, "fuentes": list(contexto["url"].unique())}''',
  '''def llm_falso(prompt, respaldo=""):
    return "Postula en el FUAS [Doc 2227]."
def llm_no_sabe(prompt, respaldo=""):
    return "NO_ENCONTRADO"
def llm_prohibido(prompt, respaldo=""):
    raise RuntimeError("¡no se debía llamar al LLM!")
url_esperada = corpus.loc[corpus["id"] == MIS_PREGUNTAS[7][1], "url"].iloc[0]
dentro = responder(MIS_PREGUNTAS[7][0], llm=llm_falso)
assert dentro["respuesta"] != NO_SE and url_esperada in dentro["fuentes"], "debe responder y citar el documento esperado"
assert responder(MIS_PREGUNTAS[7][0], llm=llm_no_sabe) == {"respuesta": NO_SE, "fuentes": []}, "barrera 2"
assert responder("¿Quién ganó la Copa América 2015?", llm=llm_prohibido) == {"respuesta": NO_SE, "fuentes": []}, "barrera 1, sin llamar al LLM"''',
  'Barrera 1: if contexto["puntaje"].iloc[0] < UMBRAL: return {"respuesta": NO_SE, "fuentes": []}. Barrera 2: if "NO_ENCONTRADO" in texto: return lo mismo.',
  None),
]

DEMO_MD = '''## 5. Tu demo

Prueba tu asistente con preguntas de tu público — incluidas algunas que **no** debería saber
responder. Esta salida (con y sin clave) es parte de tu entrega.'''

DEMO_CELL = '''DEMO = ["¿Cómo pido la Beca Bicentenario?",
        "¿Hay ayuda para pagar la casa de reposo de mi mamá?",
        "¿Quién ganó la Copa América 2015?"]
try:
    for p in DEMO:
        r = responder(p)
        print(f"▶ {p}\\n  {r['respuesta'][:300]}\\n  fuentes: {r['fuentes']}\\n")
except Exception as e:
    print("Completa los ejercicios anteriores para ver la demo.", e)'''

FICHA = '''## 6. Ficha de uso responsable (riesgos y ética)

Toda solución de IA en el Estado se entrega con esta ficha. Complétala para **tu** proyecto:

> **Uso previsto y público:** _(qué preguntas responde, para quién, por qué canal)_
>
> **Fuentes y vigencia:** _(qué documentos usa, quién los mantiene, cada cuánto se actualizan; una
> ficha desactualizada produce respuestas «bien citadas» pero equivocadas)_
>
> **Evaluación:** _(n.º de preguntas, hit@1, hit@3, y cómo se comporta con preguntas fuera del corpus)_
>
> **Privacidad:** _(qué datos personales podrían llegar en las preguntas; cómo se evita enviarlos al
> LLM externo y guardarlos en registros)_
>
> **Sesgos y exclusión:** _(¿a quién le funciona peor? lenguaje coloquial, pueblos originarios,
> baja alfabetización digital, personas mayores)_
>
> **Supervisión humana:** _(quién revisa, en qué casos se deriva a una persona, cómo se corrige un error)_
>
> **Costo:** _(capa gratuita, tokens estimados por consulta, qué pasa si se cae el servicio del LLM)_
>
> **Lo que el asistente NO hace:** _(no decide beneficios, no reemplaza la atención, no interpreta casos particulares)_'''

RUBRICA = '''## Rúbrica de evaluación

| Criterio | Qué se evalúa |
|---|---|
| **Utilidad pública** | Resuelve consultas reales que hoy consumen tiempo de atención. |
| **Evaluación con evidencia** | Set de ≥ 8 preguntas escrito antes de mirar resultados; hit@1 y hit@3 reportados, con sus límites. |
| **Groundedness / citas** | Cada respuesta cita el documento del que sale; sin fuente, no se responde. |
| **Abstención** | Se abstiene ante preguntas fuera del corpus (umbral + `NO_ENCONTRADO`) y deriva a una persona. |
| **Riesgos y ética** | Ficha de uso responsable completa: privacidad, sesgos, supervisión humana, vigencia de las fuentes. |
| **Reproducibilidad y costo** | El notebook corre de punta a punta **sin clave ni red**; costo del LLM estimado. |
| **Comunicación** | Demo clara y ficha comprensible para una jefatura no técnica. |
| **Pertinencia** | (Bonus) El corpus o los datos son de tu propio organismo o responden una pregunta real de gestión. |

> **Entregable:** notebook reproducible + demo + informe de evaluación + ficha de uso responsable.'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-CAP", "Capstone — un asistente de IA para tu servicio", "R3", "IA Aplicada", "6–7",
                      ["Adaptar **tu propio corpus** (o uno del banco) al formato del asistente.",
                       "Construir el **índice** con la mejor configuración de R3-03.",
                       "**Evaluar** con preguntas reales (hit@1, hit@3) antes de confiar.",
                       "Responder **con citas** y **abstenerse** cuando no hay respuesta.",
                       "Documentar **riesgos y ética** en una ficha de uso responsable."],
                      "diseñar, evaluar y documentar un asistente de IA generativa para un problema real del servicio, con citas, abstención y supervisión humana.",
                      "las 245 fichas de trámites de ChileAtiende (ejemplo) o los documentos de tu organismo.",
                      n_checks=4),
        h.code(SETUP),
        h.md(LLM_MD),
        h.code(LLM_CELL),
        h.md(ENMARCA),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells += [h.md(DEMO_MD), h.code(DEMO_CELL), h.md(FICHA), h.md(RUBRICA)]
    nb.cells = cells
    return nb


# ─────────────────────────────────────────────────────────────────────────────
# PROFUNDIZA
# ─────────────────────────────────────────────────────────────────────────────
PROF_HEADER = '''# R3-CAP · Capstone — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional. Tres mejoras que separan una demo de un servicio en producción:

1. **Calibrar el umbral** de abstención con evidencia (preguntas dentro y fuera del corpus).
2. **Filtrar por metadatos**: si sabes el tema de la consulta, busca solo ahí.
3. **Bitácora de auditoría** anonimizada: registrar cada consulta sin guardar datos personales.

Todo corre sin red ni LLM. Usa el corpus de fichas; cámbialo por el tuyo igual que en la lección.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_PREP = f'''import os, re, json, urllib.request
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

CORPUS_CSV = "fichas.csv"
if not os.path.exists(CORPUS_CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CORPUS_CSV}}", CORPUS_CSV)
corpus = pd.read_csv(CORPUS_CSV)[["id", "titulo", "tema", "url", "texto"]]

{TROCEAR_SRC}

trozos = pd.DataFrame([{{"id": d.id, "titulo": d.titulo, "tema": d.tema, "url": d.url, "texto": t}}
                       for d in corpus.itertuples() for t in trocear(d.texto)])
vect = TfidfVectorizer(strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5))
X = vect.fit_transform((trozos["titulo"] + "\\n") * 3 + trozos["texto"])

def puntajes(pregunta):
    return (X @ vect.transform([pregunta]).T).toarray().ravel()

def recuperar(pregunta, k=3):
    p = puntajes(pregunta)
    mejores = np.argsort(-p, kind="stable")[:k]
    res = trozos.iloc[mejores].copy()
    res["puntaje"] = p[mejores]
    return res

{MIS_PREGUNTAS_SRC}

# Preguntas que el asistente NO debería responder (fuera del corpus)
FUERA_DEL_CORPUS = [
    "¿Cómo se prepara una empanada de pino?", "¿Quién ganó la Copa América 2015?",
    "¿Cuál es la capital de Francia?", "¿Cuánto cuesta un kilo de pan?",
    "¿Qué tiempo hará mañana?", "¿Cuál es el horario del metro?",
    "¿Cómo renuevo el pasaporte?", "¿Quién es el presidente de Argentina?",
]
print("Trozos:", len(trozos), "| preguntas dentro:", len(MIS_PREGUNTAS), "| fuera:", len(FUERA_DEL_CORPUS))'''

PROF_EJ = [
 ("## 1. Calibrar el umbral con evidencia",
  "El umbral decide cuándo abstenerse. Muy bajo: responde cosas que no sabe. Muy alto: se "
  "abstiene ante preguntas legítimas. Para cada umbral candidato, cuenta las **decisiones "
  "correctas**: responder (mejor puntaje ≥ umbral) las de `MIS_PREGUNTAS` y abstenerse "
  "(< umbral) en las de `FUERA_DEL_CORPUS`. Quédate con el que más acierta.",
  "Construye la tabla de calibración",
  '''mejor_dentro = [puntajes(p).max() for p, _ in MIS_PREGUNTAS]
mejor_fuera = [puntajes(p).max() for p in FUERA_DEL_CORPUS]
filas = []
for u in [0.10, 0.20, 0.30, 0.40]:
    responde_bien = sum(s >= u for s in mejor_dentro)
    se_abstiene_bien = sum(s < u for s in mejor_fuera)
    filas.append({"umbral": u, "responde_bien": responde_bien, "se_abstiene_bien": se_abstiene_bien,
                  "aciertos": responde_bien + se_abstiene_bien})
calibracion = pd.DataFrame(filas)
umbral_elegido = calibracion.loc[calibracion["aciertos"].idxmax(), "umbral"]
print(calibracion); print("umbral elegido:", umbral_elegido)''',
  '''mejor_dentro = [puntajes(p).max() for p, _ in MIS_PREGUNTAS]
mejor_fuera = [puntajes(p).max() for p in FUERA_DEL_CORPUS]
filas = []
for u in [0.10, 0.20, 0.30, 0.40]:
    # TODO: responde_bien = cuántos de mejor_dentro son >= u
    #       se_abstiene_bien = cuántos de mejor_fuera son < u
    #       agrega a filas {"umbral": u, "responde_bien": ..., "se_abstiene_bien": ..., "aciertos": suma}
    ...
calibracion = pd.DataFrame(filas)
# TODO: el umbral de la fila con más aciertos (idxmax)
umbral_elegido = ...
print(calibracion)''',
  '''assert list(calibracion["umbral"]) == [0.10, 0.20, 0.30, 0.40]
for f in calibracion.itertuples():
    assert f.responde_bien == sum(s >= f.umbral for s in mejor_dentro)
    assert f.se_abstiene_bien == sum(s < f.umbral for s in mejor_fuera)
assert umbral_elegido == calibracion.loc[calibracion["aciertos"].idxmax(), "umbral"]''',
  'responde_bien = sum(s >= u for s in mejor_dentro); se_abstiene_bien = sum(s < u for s in mejor_fuera); umbral_elegido = calibracion.loc[calibracion["aciertos"].idxmax(), "umbral"].'),

 ("## 2. Filtrar por metadatos (tema)",
  "Si tu asistente vive en la página de **un** tema (por ejemplo, «Chilenos en el exterior»), no tiene sentido "
  "buscar en todo el corpus: un filtro por metadatos evita que gane un trozo parecido pero de "
  "otro tema. Escribe `recuperar_en_tema(pregunta, temas, k)` que solo considere trozos cuyo "
  "`tema` esté en `temas`.",
  "Escribe `recuperar_en_tema`",
  '''def recuperar_en_tema(pregunta, temas, k=3):
    p = puntajes(pregunta)
    p = np.where(trozos["tema"].isin(temas), p, -1.0)       # fuera del tema: descartado
    mejores = np.argsort(-p, kind="stable")[:k]
    res = trozos.iloc[mejores].copy()
    res["puntaje"] = p[mejores]
    return res

pregunta = "¿Cómo saco el certificado de antecedentes?"
print(recuperar(pregunta, 1)[["id", "titulo", "tema"]])                                  # todo el corpus
print(recuperar_en_tema(pregunta, ["chilenos-en-el-exterior"], 1)[["id", "titulo", "tema"]])  # solo ese tema''',
  '''def recuperar_en_tema(pregunta, temas, k=3):
    p = puntajes(pregunta)
    # TODO: deja en -1.0 los puntajes de trozos cuyo tema NO esté en `temas`
    #       (pista: np.where(trozos["tema"].isin(temas), p, -1.0))
    p = ...
    mejores = np.argsort(-p, kind="stable")[:k]
    res = trozos.iloc[mejores].copy()
    res["puntaje"] = p[mejores]
    return res''',
  '''r = recuperar_en_tema("¿Cómo saco el certificado de antecedentes?", ["chilenos-en-el-exterior"])
assert len(r) == 3 and set(r["tema"]) == {"chilenos-en-el-exterior"}, "solo deben volver trozos del tema pedido"
assert r["id"].iloc[0] == 49064, "en ese tema, la ficha correcta es la del certificado para chilenos en el extranjero"
r2 = recuperar_en_tema("¿Cómo me afilio a Fonasa?", ["salud", "certificados"], k=5)
assert set(r2["tema"]) <= {"salud", "certificados"} and (r2["puntaje"] >= 0).all()''',
  'p = np.where(trozos["tema"].isin(temas), p, -1.0).'),

 ("## 3. Bitácora de auditoría, sin datos personales",
  "Un servicio en producción **registra** cada consulta: para auditar, medir y mejorar. Pero la "
  "bitácora no puede convertirse en una base de datos personales. Escribe `anonimizar(texto)` "
  "(reemplaza RUT por `[RUT]` y correos por `[CORREO]`) y `registrar(ruta, pregunta, resultado)`, "
  "que agrega **una línea JSON** con fecha, pregunta anonimizada, si se abstuvo y las fuentes.",
  "Escribe `anonimizar` y `registrar`",
  '''def anonimizar(texto):
    texto = re.sub(r"\\b\\d{1,2}\\.?\\d{3}\\.?\\d{3}-[\\dkK]\\b", "[RUT]", texto)
    return re.sub(r"\\b[\\w.+-]+@[\\w-]+\\.[\\w.]+\\b", "[CORREO]", texto)

def registrar(ruta, pregunta, resultado):
    linea = {"fecha": datetime.now().isoformat(timespec="seconds"),
             "pregunta": anonimizar(pregunta),
             "abstuvo": not resultado["fuentes"],
             "fuentes": resultado["fuentes"]}
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\\n")

BITACORA = "bitacora_demo.jsonl"
if os.path.exists(BITACORA):
    os.remove(BITACORA)
registrar(BITACORA, "Soy 12.345.678-5, escríbanme a ana@correo.cl: ¿cómo pido la PGU?",
          {"respuesta": "...", "fuentes": ["https://www.chileatiende.gob.cl/fichas/130457"]})
registrar(BITACORA, "¿Quién ganó la Copa América 2015?", {"respuesta": "No encontré…", "fuentes": []})
print(open(BITACORA, encoding="utf-8").read())''',
  '''def anonimizar(texto):
    # TODO: reemplaza los RUT (r"\\b\\d{1,2}\\.?\\d{3}\\.?\\d{3}-[\\dkK]\\b") por "[RUT]"
    #       y los correos (r"\\b[\\w.+-]+@[\\w-]+\\.[\\w.]+\\b") por "[CORREO]" con re.sub
    return ...

def registrar(ruta, pregunta, resultado):
    # TODO: arma un dict con "fecha" (datetime.now().isoformat(timespec="seconds")),
    #       "pregunta" (anonimizada), "abstuvo" (not resultado["fuentes"]) y "fuentes";
    #       y agrégalo como UNA línea JSON al archivo `ruta` (open(ruta, "a", encoding="utf-8"))
    ...

BITACORA = "bitacora_demo.jsonl"
if os.path.exists(BITACORA):
    os.remove(BITACORA)''',
  '''assert anonimizar("Soy 12.345.678-5 y mi correo es ana@correo.cl") == "Soy [RUT] y mi correo es [CORREO]"
if os.path.exists(BITACORA):
    os.remove(BITACORA)
registrar(BITACORA, "Mi RUT es 9.876.543-K, ¿cómo pido la PGU?", {"respuesta": "x", "fuentes": ["u1"]})
registrar(BITACORA, "¿Quién ganó la Copa América 2015?", {"respuesta": "y", "fuentes": []})
lineas = [json.loads(l) for l in open(BITACORA, encoding="utf-8")]
assert len(lineas) == 2, "debe haber una línea por consulta"
assert "9.876.543-K" not in open(BITACORA, encoding="utf-8").read(), "¡la bitácora guardó un RUT!"
assert lineas[0]["abstuvo"] is False and lineas[1]["abstuvo"] is True
assert {"fecha", "pregunta", "abstuvo", "fuentes"} <= set(lineas[0])''',
  're.sub(PATRON_RUT, "[RUT]", texto) y luego el correo; en registrar: f.write(json.dumps(linea, ensure_ascii=False) + "\\n") con open(ruta, "a").'),
]

PROF_CIERRE = '''## Para llevar

- El **umbral** no se adivina: se calibra con preguntas dentro y fuera del corpus, y se
  recalibra cuando cambia el corpus o el índice.
- Los **metadatos** (tema, institución, fecha de vigencia) son filtros baratos y poderosos.
- Una **bitácora** permite auditar y mejorar el asistente; anonimizar **antes** de guardar es
  parte del diseño, no un detalle. Las expresiones regulares son una primera barrera: revisa
  qué otros datos personales podrían llegar (direcciones, diagnósticos, nombres).

---

*Fin de la profundización del capstone R3.*'''


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


README = '''# R3-CAP · Capstone — un asistente de IA para tu servicio

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-CAP-capstone-ia-aplicada/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, rúbrica comentada y autoevaluación.

Proyecto final de la rama R3: un **asistente de trámites** con RAG que responde **citando la
fuente**, se **abstiene** cuando no sabe y se **evalúa** con preguntas reales (hit@k). La
plantilla usa las 245 fichas de ChileAtiende (`fichas.csv`) como ejemplo; lo ideal es usar
**documentos o datos de tu propio servicio** (o el banco del bootcamp: `fichas`, `matricula`,
`aire_diario`, `reclamos`, `sismos`; o datos.gob.cl). Si tu corpus es tabular, el camino es el
agente de R3-04. Incluye **ficha de uso responsable** (riesgos y ética) y **rúbrica** con
criterios de Pertinencia y Riesgos/ética. Corre completo **sin clave ni red**.

- `leccion.ipynb` — plantilla con `TODO`; se autoverifica (✅). 4 chequeos.
- `profundiza.ipynb` — opcional 🔬: calibrar el umbral de abstención, filtrar por tema y
  bitácora de auditoría anonimizada. 3 chequeos.

*Fuente del corpus de ejemplo: fichas de trámites de [ChileAtiende](https://www.chileatiende.gob.cl).*
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
