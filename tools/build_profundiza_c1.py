# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de C1 (Introducción al NLP):
C1/profundiza.ipynb (estudiante) + C1/profundiza_solucion.ipynb (resuelto).

TODO el cuaderno es CONCEPTUAL y verificable SIN conexión ni API key:
demos pequeñas (matriz término-documento, dispersión, TF-IDF a mano, fallo por
sinónimos, n-gramas, sesgos del lenguaje) en Python/sklearn OFFLINE sobre el
dataset del módulo (rubros.csv). NINGUNA llamada a un LLM ni a la red
(salvo el fallback de descarga del CSV)."""
import json, os

BASE = "C1-introduccion-al-nlp"

TITULO = """# C1 · Introducción al NLP — Profundización (opcional) 🔬

**Formación Pública — Bloque avanzado · IA aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de C1 —donde *limpiaste*, *tokenizaste* y armaste
un **clasificador por palabras clave**— aquí vamos al *porqué*: por qué el texto se vuelve una **matriz
gigantesca y casi vacía**, qué calcula de verdad el **TF-IDF** y por qué el **IDF** baja el peso de las
palabras comunes y sube el de las distintivas, **por qué los métodos por palabra clave fallan** con
sinónimos, contexto y polisemia, qué aportan los **n-gramas**, y cómo el lenguaje **arrastra sesgos**.

Menos sintaxis nueva, más **modelo mental**. Aquí usamos `scikit-learn` (`CountVectorizer`,
`TfidfVectorizer`, coseno) pero **todo corre offline**: no hay LLM, no hay API key, no hay red. Cada
demo imprime un número que puedes interpretar. Los ejercicios del final son **conceptuales** y se
autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de C1. Mismo dataset: `rubros.csv`."""

CARGA = """import os, urllib.request, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# rubros.csv del módulo (mismo dato de la lección). Si no está, se intenta descargar.
if not os.path.exists("rubros.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/C1-introduccion-al-nlp/rubros.csv"
        urllib.request.urlretrieve(url, "rubros.csv")
    except Exception:
        print("Si estás en Colab, sube rubros.csv manualmente.")

df = pd.read_csv("rubros.csv")
CORPUS = df["rubro"].tolist()

# Mismas palabras vacías de la lección (para comparar peras con peras).
STOPWORDS = ["de", "y", "e", "o", "u", "para", "el", "la", "los", "las", "un", "una",
             "en", "con", "a", "del", "al", "por", "su", "sus", "se", "que", "general"]

print(f"{len(CORPUS)} rubros cargados. Ejemplo:", CORPUS[12])
print("Este cuaderno NO usa API key ni red: TF-IDF, coseno y n-gramas corren 100% offline.")"""

S1 = """## 1. Texto como dato: de palabras a vectores (vocabulario)

En la lección convertiste texto en **conteos** con `Counter`. Demos un paso atrás para ver la idea
grande: para que una máquina opere con texto, primero hay que **traducirlo a números**, y la traducción
más usada es la **bolsa de palabras** (*bag of words*).

La receta es:

1. Se junta **todo** el corpus y se arma el **vocabulario**: la lista de palabras distintas que aparecen
   (después de normalizar y quitar *stopwords*). Cada palabra recibe una **posición fija** (una columna).
2. Cada documento (cada rubro) se vuelve un **vector** de largo = tamaño del vocabulario: en cada columna
   va **cuántas veces** aparece esa palabra en ese documento. La inmensa mayoría serán **ceros**, porque
   un rubro de 4 palabras no contiene casi ninguna de las ~100 del vocabulario.

`CountVectorizer` de `scikit-learn` hace los cuatro pasos de la lección (minúsculas, tokenizar, quitar
*stopwords*, contar) y te entrega esa tabla **término-documento** directamente. Lo importante conceptual:
**el orden de las palabras se pierde** ("agua de mar" y "mar de agua" dan el mismo vector). Por eso se
llama *bolsa*: importa **qué** palabras hay y **cuántas**, no en qué orden.

> **Una diferencia con la lección:** allá *quitábamos las tildes* a mano. Aquí **no**: `sklearn` trata las
> tildes (`á`, `é`, `í`, …) como letras válidas de palabra, así que "médicos" se conserva con tilde. No es
> un error: todos los rubros del catálogo ya están escritos con sus tildes correctas, de modo que las
> palabras del vocabulario quedan bien formadas. Solo hay que recordar que, sin normalizar acentos, una
> consulta sin tilde ("farmacos") **no** coincidiría con un término con tilde ("farmacéuticos")."""

S1_CODE = """# CountVectorizer = la tubería de la lección, automatizada. token_pattern pide >=2 letras;
# afinamos a >=3 para parecernos a la lección (que descartaba tokens de <3 letras).
vectorizador = CountVectorizer(stop_words=STOPWORDS, token_pattern=r"(?u)\\b[a-záéíóúñ]{3,}\\b")
X = vectorizador.fit_transform(CORPUS)            # matriz término-documento (dispersa)
vocabulario = vectorizador.get_feature_names_out()

print(f"Vocabulario: {len(vocabulario)} palabras distintas en {len(CORPUS)} rubros.")
print("Primeras 12 palabras del vocabulario:", list(vocabulario[:12]))

# Veamos el VECTOR de un rubro concreto: casi todo ceros, salvo sus pocas palabras.
i = CORPUS.index("Equipamiento y suministros médicos")
fila = X[i].toarray().ravel()
presentes = [(vocabulario[j], int(fila[j])) for j in fila.nonzero()[0]]
print(f"\\nEl rubro «{CORPUS[i]}» como vector tiene {len(fila)} columnas,")
print(f"pero solo {len(presentes)} son distintas de cero:", presentes)"""

S2 = """## 2. Alta dimensión y dispersión: una matriz enorme y casi vacía

Acabas de ver que un rubro de 3 palabras vive en un vector de ~100 columnas, con casi todo en cero. Eso
no es una rareza de este dataset: es **la regla** en NLP, y tiene nombre.

- **Alta dimensión:** el vocabulario crece con el corpus. Con textos reales (millones de documentos) el
  vocabulario tiene **decenas o cientos de miles** de palabras: cada documento es un vector con esa
  cantidad de columnas. Trabajamos en un espacio de **muchísimas dimensiones**.
- **Dispersión** (*sparsity*): como cada documento usa solo un puñado de palabras del vocabulario total,
  la inmensa mayoría de las celdas son **cero**. Una matriz así se llama **dispersa**.

¿Por qué te importa esto como funcionario que analiza datos?

- **Memoria:** guardar todos esos ceros sería un derroche. Por eso `scikit-learn` usa una **matriz
  dispersa**, que solo almacena las celdas distintas de cero. Es lo que hace viable procesar millones de
  documentos en un computador normal.
- **Significado:** que dos documentos compartan palabras es **raro y por lo tanto informativo**. Si dos
  rubros coinciden en "suministros", esa coincidencia *dice algo*. La dispersión es la base de medir
  **parecido** entre textos (lo veremos con el coseno).

Pongámosle número a "casi vacía"."""

S2_CODE = """n_docs, n_palabras = X.shape
celdas_totales = n_docs * n_palabras
celdas_llenas = X.nnz                       # nnz = number of non-zeros (solo cuenta las distintas de 0)
ceros = celdas_totales - celdas_llenas
dispersion = ceros / celdas_totales         # proporción de celdas en cero

print(f"Matriz término-documento: {n_docs} filas (rubros) x {n_palabras} columnas (palabras)")
print(f"  = {celdas_totales} celdas en total")
print(f"  celdas con un conteo (>0): {celdas_llenas}")
print(f"  celdas en CERO:            {ceros}")
print(f"  dispersión = {dispersion:.1%} de la matriz son ceros")
print("\\nGuardar todos esos ceros sería un derroche: por eso se usan matrices DISPERSAS.")

fig, ax = plt.subplots(figsize=(9, 4))
ax.spy(X, markersize=2, aspect="auto", color="#0a7e7e")
ax.set_title(f"Matriz término-documento (cada punto = una palabra presente; {dispersion:.0%} es vacío)")
ax.set_xlabel("Palabras del vocabulario"); ax.set_ylabel("Rubros")
plt.tight_layout(); plt.show()"""

S3 = """## 3. TF-IDF: por qué bajamos el peso de lo común y subimos el de lo distintivo

Contar palabras (bolsa de palabras pura) tiene un problema: **trata todas las palabras igual**. Pero no
todas valen lo mismo para distinguir un texto. En este catálogo, "servicios" aparece en **muchísimos**
rubros: saber que un texto contiene "servicios" casi no te ayuda a ubicarlo. En cambio "medicamentos"
aparece en **uno solo**: es una palabra **distintiva**, casi una huella digital.

El **TF-IDF** corrige justo eso. El peso de una palabra en un documento es el producto de dos factores:

- **TF** (*term frequency*): cuántas veces aparece la palabra **en ese documento**. Más apariciones,
  más peso. (Mide importancia *local*.)
- **IDF** (*inverse document frequency*): cuán **rara** es la palabra **en todo el corpus**. La fórmula
  habitual es `IDF = ln( (1 + N) / (1 + df) ) + 1`, donde `N` es el número de documentos y `df` es en
  **cuántos documentos** aparece la palabra. Fíjate en la intuición: si `df` es grande (palabra común),
  el cociente baja y el IDF es **chico**; si `df` es chico (palabra rara), el IDF es **grande**.

El efecto neto es el corazón del TF-IDF: **las palabras que están en todas partes pesan poco; las
distintivas pesan mucho**. Es exactamente lo contrario de las *stopwords*, pero hecho de forma
automática y graduada (no es "dentro o fuera", es "cuánto"). Calculemos el IDF a mano para verlo."""

S3_CODE = """N = len(CORPUS)

def df_documental(palabra):
    # En cuántos rubros aparece la palabra (al menos una vez)
    j = list(vocabulario).index(palabra)
    columna = X[:, j].toarray().ravel()
    return int((columna > 0).sum())

def idf_a_mano(palabra):
    df_p = df_documental(palabra)
    return math.log((1 + N) / (1 + df_p)) + 1     # misma fórmula que usa sklearn (smooth_idf)

print(f"Corpus de N = {N} rubros.\\n")
print(f"{'palabra':14s} {'aparece en':>10s}   {'IDF':>6s}")
for w in ["servicios", "productos", "suministros", "medicamentos", "musicales"]:
    print(f"{w:14s} {df_documental(w):>7d} doc {idf_a_mano(w):>9.2f}")

# Comprobamos que coincide con el IDF interno de sklearn (no es magia, es la fórmula)
tfidf = TfidfVectorizer(stop_words=STOPWORDS, token_pattern=r"(?u)\\b[a-záéíóúñ]{3,}\\b")
tfidf.fit(CORPUS)
idf_sklearn = tfidf.idf_[list(tfidf.get_feature_names_out()).index("servicios")]
print(f"\\nIDF de 'servicios' a mano: {idf_a_mano('servicios'):.4f}  |  sklearn: {idf_sklearn:.4f}")
print("La palabra común ('servicios') pesa MENOS que la rara ('medicamentos'). Eso hace el IDF.")"""

S4 = """## 4. Por qué los métodos por palabra clave FALLAN: sinónimos, contexto, polisemia

La lección fue honesta: el clasificador por palabras clave **solo acierta si el texto usa las MISMAS
palabras** que el rubro. Aquí vemos *por qué* eso es una limitación de fondo, no un detalle a pulir.

Tanto la búsqueda por palabra clave como la bolsa de palabras / TF-IDF comparan **palabras literales**.
Si dos textos quieren decir lo mismo con **palabras distintas**, para la máquina **no se parecen en
nada**. Tres formas en que esto rompe:

- **Sinónimos:** "remedios", "fármacos" y "medicamentos" son lo mismo para una persona; para la bolsa de
  palabras son **tres columnas sin relación**. Buscar "remedios" no encuentra el rubro de medicamentos.
- **Contexto / frases hechas:** "orden público" significa algo muy distinto de "poner orden en los
  archivos públicos", pero comparten las palabras "orden" y "público".
- **Polisemia:** una misma palabra con **dos sentidos**. "banco" puede ser una entidad financiera o un
  asiento de plaza; "planta" puede ser un vegetal, una fábrica o un piso. La bolsa de palabras **no
  distingue** el sentido: ve la misma columna.

Por eso el salto siguiente (los **modelos de lenguaje**, próximo bloque) no cuenta palabras: aprende a
ubicar palabras con significado parecido **cerca** en un espacio, de modo que "remedios" y "medicamentos"
queden vecinas aunque se escriban distinto. Veamos el fallo del sinónimo en vivo."""

S4_CODE = """def buscar_por_palabra_clave(consulta):
    # Búsqueda literal: ¿qué rubros CONTIENEN ese texto? (lo que haría un 'Ctrl+F' o un LIKE en SQL)
    c = consulta.lower()
    return [r for r in CORPUS if c in r.lower()]

for termino in ["medicamentos", "remedios", "farmacos"]:
    hits = buscar_por_palabra_clave(termino)
    print(f"Buscar «{termino:12s}» -> {len(hits)} resultado(s): {hits}")

print("\\n'remedios' y 'farmacos' son SINÓNIMOS de 'medicamentos', pero la búsqueda literal")
print("devuelve CERO: 'remedios' no aparece como subcadena dentro del nombre del rubro.")
print("La búsqueda literal busca la PALABRA EXACTA dentro del texto; no entiende relaciones semánticas.")

# Lo mismo con TF-IDF + coseno: si no hay palabras en común, la similitud es 0 exacto.
consulta = "remedios para el hospital"
vec_consulta = tfidf.transform([consulta])
sims = cosine_similarity(vec_consulta, tfidf.transform(CORPUS)).ravel()
mejor = CORPUS[sims.argmax()]
print(f"\\nTF-IDF + coseno para «{consulta}»:")
print(f"  mejor match = «{mejor}»  con similitud {sims.max():.3f}")
print("  Similitud 0.000: sin palabras compartidas, ni el TF-IDF rescata el sinónimo.")
print("  (Nota: con similitud 0 cualquier resultado es igualmente (no) relevante; el 'mejor match'")
print("   es solo el primero que devuelve argmax cuando todas las similitudes empatan en cero.)")"""

S5 = """## 5. N-gramas: devolverle algo de contexto a la bolsa de palabras

La bolsa de palabras tira el orden, y a veces el orden **es** el significado: "público orden" no es lo
mismo que "orden público". Una forma barata de recuperar **algo** de contexto sin saltar todavía a los
modelos de lenguaje son los **n-gramas**: en vez de contar palabras sueltas (*unigramas*), cuentas
**secuencias de N palabras seguidas**.

- **Unigrama** (1 palabra): "orden", "público".
- **Bigrama** (2 palabras seguidas): "orden público".
- **Trigrama** (3 palabras): "orden público seguridad".

Al agregar bigramas, expresiones que solo significan algo **juntas** pasan a tener su propia columna. El
costo es que el vocabulario **crece** (más columnas, más dispersión todavía): hay un equilibrio entre
capturar contexto y no explotar la dimensión. `CountVectorizer` lo hace con un parámetro, `ngram_range`.
Veamos qué bigramas son los más frecuentes en el catálogo: cuáles son las **frases hechas** del Estado
comprador."""

S5_CODE = """vec_bi = CountVectorizer(stop_words=STOPWORDS, token_pattern=r"(?u)\\b[a-záéíóúñ]{3,}\\b",
                         ngram_range=(2, 2))               # SOLO bigramas
Xbi = vec_bi.fit_transform(CORPUS)
bigramas = vec_bi.get_feature_names_out()
conteos = np.asarray(Xbi.sum(axis=0)).ravel()

orden = np.argsort(-conteos)[:6]
print("Bigramas (pares de palabras seguidas) más frecuentes del catálogo:")
for j in orden:
    print(f"  «{bigramas[j]:24s}» aparece en {int(conteos[j])} rubro(s)")

print(f"\\nVocabulario de unigramas: {len(vocabulario)} columnas")
print(f"Vocabulario de bigramas:  {len(bigramas)} columnas (más contexto, pero más dimensión)")
print("Un bigrama como «orden público» captura un significado que las palabras sueltas pierden.")"""

S6 = """## 6. Sesgos del lenguaje: el modelo refleja lo que MÁS aparece, no lo que es JUSTO

Todo lo anterior parte de **contar** lo que hay en los textos. Y ahí está el riesgo silencioso: si los
textos están **desbalanceados**, el modelo hereda ese desbalance. Una palabra que aparece muchísimo más
que las demás **domina** las representaciones, y el sistema tiende a sobre-representarla.

En este catálogo es inofensivo: solo significa que ciertas categorías de compra usan palabras más
genéricas. Pero el **mecanismo** es exactamente el mismo que produce los **sesgos sociales** en NLP:

- Si en los textos de entrenamiento ciertos cargos aparecen ligados a un género (p. ej. "ingeniero"
  junto a "hombre", "enfermera" junto a "mujer"), el modelo **aprende esa asociación** —no porque sea
  verdad, sino porque fue **frecuente**— y la reproduce al redactar o clasificar.
- Si un grupo, comuna o tema está **subrepresentado** en los datos, el modelo lo "entiende" peor y puede
  tratarlo con menos precisión.

La regla para el Estado: **un modelo de texto no es neutral; refleja sus datos.** Antes de usarlo en
algo que afecte derechos, hay que revisar **qué hay y qué falta** en el corpus. Midamos la concentración
del vocabulario como espejo de ese fenómeno."""

S6_CODE = """frec_total = np.asarray(X.sum(axis=0)).ravel()           # cuántas veces aparece cada palabra en total
ranking = sorted(zip(vocabulario, frec_total), key=lambda t: -t[1])

print("Palabras más frecuentes del catálogo (las que 'dominan' la representación):")
for w, n in ranking[:6]:
    print(f"  {w:14s}: {int(n)}")

palabra_top, veces_top = ranking[0]
cuota = veces_top / frec_total.sum()
print(f"\\nLa palabra más frecuente ('{palabra_top}') concentra el {cuota:.0%} de TODAS las apariciones.")

fig, ax = plt.subplots(figsize=(8, 3.5))
top10 = ranking[:10]
ax.bar([w for w, _ in top10], [n for _, n in top10], color="#0a7e7e")
ax.set_title("Concentración del vocabulario (espejo del sesgo: lo frecuente manda)")
ax.set_ylabel("Apariciones"); plt.xticks(rotation=45, ha="right")
plt.tight_layout(); plt.show()

print("Aquí es solo concentración léxica de un catálogo chico, pero el MECANISMO es el mismo")
print("que el sesgo social: el modelo refleja lo que MÁS aparece, no lo que es JUSTO.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Creer que la bolsa de palabras "entiende" el texto.** Solo **cuenta** palabras literales; pierde el orden y el significado.
- **Pesar todas las palabras igual.** Sin **IDF**, las palabras comunes ("servicios", "de") ahogan a las distintivas. El IDF las desinfla.
- **Esperar que una búsqueda por palabra clave encuentre sinónimos.** "remedios" no halla "medicamentos": la búsqueda literal exige que la palabra aparezca **tal cual** (como subcadena) en el texto.
- **Confiar la similitud de textos al coseno con pocas palabras compartidas.** Sin palabras en común, la similitud es **0** aunque el tema sea el mismo.
- **Olvidar la dispersión.** La matriz término-documento es casi toda **ceros**; guardarla densa es un derroche de memoria.
- **Tratar un modelo de texto como neutral.** **Hereda** el desbalance de sus datos: revisa qué hay y qué falta antes de decidir con él."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula** algo y te pide **elegir la interpretación
correcta**. **Ninguno requiere API key ni conexión.** Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: dispersión de la matriz ----
E1 = """## Ejercicio 01 · La matriz casi vacía (dispersión)
Usa la matriz `X` (término-documento) y su atributo `X.nnz` (número de celdas distintas de cero).

- Guarda en `total_celdas` el número total de celdas de `X` (filas × columnas; usa `X.shape`).
- Guarda en `proporcion_ceros` la proporción de celdas que están en **cero**
  (es decir, `(total_celdas - X.nnz) / total_celdas`).
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** La matriz está casi llena: casi todas las palabras aparecen en casi todos los rubros.
  - **B.** La matriz es **dispersa**: la enorme mayoría de las celdas son cero, porque cada rubro usa
    muy pocas palabras del vocabulario total. Por eso se guarda como matriz dispersa.
  - **C.** La proporción de ceros no se puede calcular sin entrenar un modelo."""
E1_TODO = """total_celdas = None       # TODO: filas * columnas de X (mira X.shape)
proporcion_ceros = None   # TODO: (total_celdas - X.nnz) / total_celdas
conclusion = None         # TODO: "A", "B" o "C"
"""
E1_SOL = """total_celdas = X.shape[0] * X.shape[1]
proporcion_ceros = (total_celdas - X.nnz) / total_celdas
conclusion = "B"
"""
E1_CHK = """try:
    _total = X.shape[0] * X.shape[1]
    _prop = (_total - X.nnz) / _total
    _correcta = "B" if _prop > 0.5 else "A"
    assert total_celdas is not None and int(total_celdas) == _total, f"total_celdas debería ser {_total}"
    assert proporcion_ceros is not None and abs(proporcion_ceros - _prop) < 1e-6, f"proporcion_ceros debería ser ~{_prop:.3f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿la matriz está llena o casi vacía?"
    print(f"✅ Correcto. {_prop:.1%} de la matriz son ceros: es DISPERSA. Por eso se guarda comprimida.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: IDF común vs raro ----
E2 = """## Ejercicio 02 · El IDF: común pesa poco, raro pesa mucho
Usa `idf_a_mano` (definida en la sección 3) sobre dos palabras: una **muy común** y una **muy rara**.

- Guarda en `idf_comun` el IDF de `"servicios"` (aparece en muchos rubros).
- Guarda en `idf_raro` el IDF de `"medicamentos"` (aparece en un solo rubro).
- Elige en `conclusion` la interpretación correcta:
  - **A.** `idf_comun` es **mayor** que `idf_raro`: las palabras comunes pesan más.
  - **B.** `idf_comun` es **menor** que `idf_raro`: el IDF **baja** el peso de lo común y **sube** el de
    lo distintivo. Por eso "medicamentos" es más informativo que "servicios".
  - **C.** Ambos IDF son iguales: el IDF no depende de qué tan frecuente sea la palabra.

Pista: `idf_a_mano("servicios")` y `idf_a_mano("medicamentos")`."""
E2_TODO = """idf_comun = None    # TODO: idf_a_mano de "servicios"
idf_raro = None     # TODO: idf_a_mano de "medicamentos"
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """idf_comun = idf_a_mano("servicios")
idf_raro = idf_a_mano("medicamentos")
conclusion = "B"
"""
E2_CHK = """try:
    _comun = idf_a_mano("servicios")
    _raro = idf_a_mano("medicamentos")
    _correcta = "B" if _comun < _raro else "A"
    assert idf_comun is not None and abs(idf_comun - _comun) < 1e-4, f"idf_comun debería ser ~{_comun:.2f}"
    assert idf_raro is not None and abs(idf_raro - _raro) < 1e-4, f"idf_raro debería ser ~{_raro:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿qué palabra pesa más, la común o la rara?"
    print(f"✅ Correcto. IDF servicios={_comun:.2f} < IDF medicamentos={_raro:.2f}: el IDF premia lo distintivo.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: fallo por sinónimo ----
E3 = """## Ejercicio 03 · Por qué la palabra clave falla con sinónimos
Usa `buscar_por_palabra_clave` (definida en la sección 4).

- Guarda en `n_medicamentos` cuántos rubros encuentra al buscar `"medicamentos"`.
- Guarda en `n_remedios` cuántos rubros encuentra al buscar `"remedios"` (sinónimo de medicamentos).
- Elige en `conclusion` la lectura correcta:
  - **A.** Encuentra lo mismo con ambas palabras: la búsqueda entiende que son sinónimos.
  - **B.** "medicamentos" encuentra el rubro pero "remedios" encuentra **cero**: la búsqueda literal
    **no entiende sinónimos**, solo coincidencias de letras. Ese es el límite de los métodos por palabra clave.
  - **C.** "remedios" encuentra más rubros que "medicamentos" porque es una palabra más general.

Pista: `len(buscar_por_palabra_clave("..."))`."""
E3_TODO = """n_medicamentos = None   # TODO: cuántos rubros encuentra buscar_por_palabra_clave("medicamentos")
n_remedios = None       # TODO: cuántos rubros encuentra buscar_por_palabra_clave("remedios")
conclusion = None       # TODO: "A", "B" o "C"
"""
E3_SOL = """n_medicamentos = len(buscar_por_palabra_clave("medicamentos"))
n_remedios = len(buscar_por_palabra_clave("remedios"))
conclusion = "B"
"""
E3_CHK = """try:
    _med = len(buscar_por_palabra_clave("medicamentos"))
    _rem = len(buscar_por_palabra_clave("remedios"))
    _correcta = "B" if (_med > 0 and _rem == 0) else "A"
    assert n_medicamentos is not None and int(n_medicamentos) == _med, f"n_medicamentos debería ser {_med}"
    assert n_remedios is not None and int(n_remedios) == _rem, f"n_remedios debería ser {_rem}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿encontró el sinónimo 'remedios'?"
    print(f"✅ Correcto. 'medicamentos' -> {_med}, 'remedios' -> {_rem}. La palabra clave no ve sinónimos.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: coseno TF-IDF entre dos rubros ----
E4 = """## Ejercicio 04 · Similitud por coseno (qué mide y qué no)
La **similitud por coseno** entre dos vectores TF-IDF mide cuánto se parecen **por las palabras que
comparten**: va de 0 (nada en común) a 1 (idénticos). Vamos a comparar dos pares de rubros.

Ya tienes `tfidf` (ajustado en la sección 3). Te dejamos los vectores calculados; tú interpretas.

- `par_relacionado`: similitud entre *«Equipos y suministros de defensa, orden público, protección y
  seguridad»* y *«Servicios de defensa nacional, orden público y seguridad»* (comparten varias palabras).
- `par_ajeno`: similitud entre el primero y *«Alimentos, bebidas y tabaco»* (no comparten palabras).

- Elige en `conclusion` la interpretación correcta:
  - **A.** `par_ajeno` es mayor: textos sin palabras compartidas se parecen más.
  - **B.** `par_relacionado` es mayor que `par_ajeno`: el coseno detecta el parecido **por palabras
    compartidas**; cuando no hay palabras en común, da 0 aunque el tema pudiera ser cercano.
  - **C.** Ambas similitudes son 1: el coseno siempre da 1.

*(Opcional, no se corrige): en `reflexion` escribe por qué el coseno NO detectaría dos rubros que hablan
de lo mismo con palabras distintas.)*"""
E4_TODO = """_M = tfidf.transform(CORPUS)
_a = CORPUS.index("Equipos y suministros de defensa, orden público, protección y seguridad")
_b = CORPUS.index("Servicios de defensa nacional, orden público y seguridad")
_c = CORPUS.index("Alimentos, bebidas y tabaco")
par_relacionado = float(cosine_similarity(_M[_a], _M[_b])[0, 0])
par_ajeno = float(cosine_similarity(_M[_a], _M[_c])[0, 0])
conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """_M = tfidf.transform(CORPUS)
_a = CORPUS.index("Equipos y suministros de defensa, orden público, protección y seguridad")
_b = CORPUS.index("Servicios de defensa nacional, orden público y seguridad")
_c = CORPUS.index("Alimentos, bebidas y tabaco")
par_relacionado = float(cosine_similarity(_M[_a], _M[_b])[0, 0])
par_ajeno = float(cosine_similarity(_M[_a], _M[_c])[0, 0])
conclusion = "B"
reflexion = "Porque el coseno compara palabras literales: dos rubros sinónimos con palabras distintas darían similitud baja o cero."
"""
E4_CHK = """try:
    _M2 = tfidf.transform(CORPUS)
    _a2 = CORPUS.index("Equipos y suministros de defensa, orden público, protección y seguridad")
    _b2 = CORPUS.index("Servicios de defensa nacional, orden público y seguridad")
    _c2 = CORPUS.index("Alimentos, bebidas y tabaco")
    _rel = float(cosine_similarity(_M2[_a2], _M2[_b2])[0, 0])
    _aje = float(cosine_similarity(_M2[_a2], _M2[_c2])[0, 0])
    _correcta = "B" if _rel > _aje else "A"
    assert par_relacionado is not None and abs(par_relacionado - _rel) < 1e-6, "Revisa par_relacionado"
    assert par_ajeno is not None and abs(par_ajeno - _aje) < 1e-6, "Revisa par_ajeno"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿qué par comparte palabras?"
    print(f"✅ Correcto. relacionado={_rel:.2f} > ajeno={_aje:.2f}: el coseno mide parecido por palabras compartidas.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *limpias y cuentas* texto: entiendes **por qué** el NLP clásico funciona así. Sabes que un
texto se vuelve un **vector** en un espacio de **alta dimensión** y **disperso** (casi todo ceros); que
el **TF-IDF** desinfla lo común y premia lo distintivo gracias al **IDF**; **por qué** los métodos por
palabra clave fallan con **sinónimos, contexto y polisemia**; qué recuperan los **n-gramas**; y cómo el
lenguaje **arrastra los sesgos** de sus datos.

La regla de oro que te llevas: **contar palabras no es entenderlas.** La bolsa de palabras compara
**palabras literales**, no significados. Ese salto —de contar a comprender— es justo lo que traen los
**modelos de lenguaje** del próximo bloque, que ubican "remedios" y "medicamentos" como vecinos aunque
se escriban distinto.

> **Hacia dónde sigue:** los **embeddings** y los **LLM** reemplazan la columna-por-palabra por vectores
> densos que capturan **significado**, resolviendo justo el problema del sinónimo que viste aquí."""


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
