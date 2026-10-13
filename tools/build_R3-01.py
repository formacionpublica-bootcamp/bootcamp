"""build_R3-01.py — módulo R3-01 (Introducción al NLP).

Rama R3 (IA Aplicada). La tubería clásica de NLP sobre el ANCLA de la rama, las
245 fichas de trámites de ChileAtiende (fichas.csv): normalizar → tokenizar →
stopwords → frecuencias → TF-IDF → clasificar el `tema` desde el texto
(LogisticRegression, train/test estratificado) → leer los errores del
clasificador. Rearmado 2026 (nueva versión sobre fichas).
Profundiza = transferencia: texto corto de reclamos SERNAC 2011 (producto → mercado),
donde la exactitud global esconde a las clases pequeñas.

Uso:  /opt/anaconda3/bin/python tools/build_R3-01.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-01-introduccion-al-nlp")

RAW = h.REPO_RAW
IMPORTS = "import pandas as pd\nimport re, unicodedata\nfrom collections import Counter"

STOPWORDS_CELL = '''# Palabras vacías (stopwords) del español, YA sin tildes (se comparan contra texto normalizado).
# Aparecen en cualquier texto y no dicen nada del tema. Lista provista para todo el módulo.
STOPWORDS = set("""
a al algo algunas algunos ante antes como con contra cual cuales cuando de del desde donde
durante e el ella ellas ellos en entre era es esa esas ese eso esos esta estan estar estas
este esto estos fue ha han hasta hay la las le les lo los mas me mi mis muy no nos o otra
otras otro otros para pero por porque puede pueden que quien quienes se sea segun ser si sin
sobre son su sus tambien te tiene tienen todo todos tu tus u un una uno unos usted y ya
""".split())
print(len(STOPWORDS), "stopwords. Ejemplo de texto real:")
print(df.loc[df["id"] == 39484, "texto"].iloc[0][:300], "...")'''

INTRO = '''## Por qué el texto es un dato difícil

Hasta ahora tus datos fueron **números y categorías** en columnas. Pero buena parte de la
información del Estado es **texto libre**: fichas de trámites, oficios, reclamos, glosas. El
**NLP** (Procesamiento de Lenguaje Natural) enseña a la máquina a **leer texto a escala**.

Una máquina no «entiende» palabras: solo opera con números. Y el lenguaje es irregular:
`"Pensión"`, `"PENSION"` y `"pensión,"` son la misma palabra para ti y tres textos distintos
para el computador. Por eso todo proyecto de texto sigue la misma **tubería**:

1. **Normalizar:** minúsculas, sin tildes, sin signos.
2. **Tokenizar:** partir en unidades (palabras) llamadas *tokens*.
3. **Quitar stopwords:** palabras vacías (*de, la, que, para…*) que están en todo texto.
4. **Representar:** convertir cada texto en un vector de números (conteos, **TF-IDF**).
5. **Modelar:** con esos números, un modelo aprende a **clasificar** — aquí, el `tema` de cada ficha.

Trabajamos con las **245 fichas de ChileAtiende**. Cada una trae su `tema` asignado por
ChileAtiende (18 temas): eso permite entrenar un clasificador y **medir** cuánto acierta.

> Una analogía: normalizar y tokenizar es **ordenar la bodega** antes del inventario. Si los
> mismos productos están con etiquetas distintas, cualquier conteo te miente.'''

EJ = [
 ("## 1. Normalizar el texto",
  "Programa `normalizar(texto)`, en este orden: **minúsculas** → **quitar tildes** "
  "(descomponer con `unicodedata.normalize(\"NFKD\", ...)` y descartar las marcas con "
  "`unicodedata.combining`) → reemplazar todo lo que no sea letra o número por espacio "
  "(`re.sub`) → colapsar espacios y recortar.\n\n"
  "> ⚠️ La `ñ` también se descompone (n + virgulilla) y queda como `n`: «año» → «ano». "
  "Es un costo conocido de este método; para contar temas casi nunca importa.",
  "Escribe `normalizar`",
  '''def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9\\s]", " ", texto)
    texto = re.sub(r"\\s+", " ", texto).strip()
    return texto

print(normalizar("Pensión Garantizada Universal (PGU): ¡$250.275!"))''',
  '''def normalizar(texto):
    texto = texto.lower()
    # TODO: descompone con unicodedata.normalize("NFKD", texto)
    ...
    # TODO: descarta las marcas de acento: "".join(c for c in texto if not unicodedata.combining(c))
    ...
    # TODO: reemplaza todo lo que no sea a-z, 0-9 o espacio por " " (re.sub)
    ...
    texto = re.sub(r"\\s+", " ", texto).strip()
    return texto

print(normalizar("Pensión Garantizada Universal (PGU): ¡$250.275!"))''',
  '''assert normalizar("Pensión Garantizada Universal (PGU): ¡$250.275!") == "pension garantizada universal pgu 250 275"
assert normalizar("  BONO   de Invierno ") == "bono de invierno"
assert normalizar("Á É Í Ó Ú ñ 2026!!") == "a e i o u n 2026"''',
  "Tres líneas: texto = unicodedata.normalize('NFKD', texto); texto = ''.join(c for c in texto if not unicodedata.combining(c)); texto = re.sub(r'[^a-z0-9\\s]', ' ', texto).",
  None),

 ("## 2. Tokenizar y quitar palabras vacías",
  "Programa `tokenizar(texto)`: normaliza (reutiliza tu función), parte por espacios y "
  "devuelve solo los tokens que **no** están en `STOPWORDS` **y** tienen **3 o más** caracteres.",
  "Escribe `tokenizar`",
  '''def tokenizar(texto):
    return [t for t in normalizar(texto).split()
            if t not in STOPWORDS and len(t) >= 3]

print(tokenizar("Es un beneficio no postulable de $81.257 que recibirás junto con tu pensión de mayo"))''',
  '''def tokenizar(texto):
    # TODO: comprensión sobre normalizar(texto).split() que descarte STOPWORDS y tokens de < 3 caracteres
    ...

print(tokenizar("Es un beneficio no postulable de $81.257 que recibirás junto con tu pensión de mayo"))''',
  '''assert tokenizar("Es un beneficio no postulable de $81.257") == ["beneficio", "postulable", "257"]
assert tokenizar("Pensión de VEJEZ para la persona") == ["pension", "vejez", "persona"]
assert "de" not in tokenizar("Certificado de nacimiento")''',
  "[t for t in normalizar(texto).split() if t not in STOPWORDS and len(t) >= 3]",
  None),

 ("## 3. Frecuencias: ¿de qué hablan las fichas?",
  "Con el texto tokenizado podemos **contar**. Junta los tokens de las 245 fichas en un "
  "`Counter` y mira las palabras más frecuentes. Pregúntate: ¿te dicen algo del **tema** de "
  "una ficha en particular?",
  "Construye la bolsa de palabras del corpus",
  '''frecuencias = Counter()
for texto in df["texto"]:
    frecuencias.update(tokenizar(texto))
print(len(frecuencias), "palabras distintas")
print(frecuencias.most_common(10))''',
  '''frecuencias = Counter()
for texto in df["texto"]:
    # TODO: agrega los tokens de este texto al contador (frecuencias.update(...))
    ...
print(len(frecuencias), "palabras distintas")
print(frecuencias.most_common(10))''',
  '''_esperado = Counter()
for _t in df["texto"]:
    _esperado.update([w for w in normalizar(_t).split() if w not in STOPWORDS and len(w) >= 3])
assert isinstance(frecuencias, Counter) and len(frecuencias) > 0
assert frecuencias.most_common(1) == _esperado.most_common(1)
assert frecuencias["pension"] == _esperado["pension"]''',
  "Dentro del for: frecuencias.update(tokenizar(texto)).",
  None),

 ("## 4. TF-IDF: las palabras que distinguen",
  "Las más frecuentes (*web, trámite, sitio, certificado*) vienen de instrucciones que se "
  "repiten en casi **todas** las fichas («ingresa al sitio web…»): no distinguen a ninguna. **TF-IDF** corrige eso: pesa cada palabra por cuánto aparece "
  "en *esta* ficha (**TF**) y la castiga si aparece en muchas fichas (**IDF**). Las palabras con "
  "TF-IDF alto son las que **caracterizan** a un documento.\n\n"
  "`TfidfVectorizer` de scikit-learn hace el cálculo; le pasamos **tu** `tokenizar` como "
  "`analyzer` y `min_df=2` (ignora palabras que aparecen en una sola ficha). El resultado `X` es "
  "una matriz: una fila por ficha, una columna por palabra.",
  "Vectoriza las fichas y lee el Bono de Invierno",
  '''from sklearn.feature_extraction.text import TfidfVectorizer

vectorizador = TfidfVectorizer(analyzer=tokenizar, min_df=2)
X = vectorizador.fit_transform(df["texto"])
terminos = vectorizador.get_feature_names_out()

i = df.index[df["id"] == 39484][0]            # fila del Bono de Invierno
pesos = X[i].toarray()[0]
top_tfidf = list(terminos[pesos.argsort()[::-1][:6]])
print("matriz:", X.shape, "(fichas x palabras)")
print("TF-IDF más alto:", top_tfidf)
print("solo conteo:    ", [w for w, _ in Counter(tokenizar(df.loc[i, "texto"])).most_common(6)])''',
  '''from sklearn.feature_extraction.text import TfidfVectorizer

# TODO: crea el vectorizador con analyzer=tokenizar y min_df=2
vectorizador = ...
# TODO: ajústalo y transforma df["texto"] en una sola llamada (fit_transform)
X = ...
terminos = vectorizador.get_feature_names_out()

i = df.index[df["id"] == 39484][0]            # fila del Bono de Invierno
pesos = X[i].toarray()[0]
# TODO: los 6 términos de mayor peso: terminos[pesos.argsort()[::-1][:6]] (envuelto en list)
top_tfidf = ...
print("matriz:", X.shape, "(fichas x palabras)")
print("TF-IDF más alto:", top_tfidf)''',
  '''assert X.shape[0] == len(df) and X.shape[1] == len(terminos)
assert len(top_tfidf) == 6 and top_tfidf[0] == terminos[pesos.argmax()]
assert "pension" in top_tfidf and "tramite" not in top_tfidf''',
  "TfidfVectorizer(analyzer=tokenizar, min_df=2); X = vectorizador.fit_transform(df['texto']); top_tfidf = list(terminos[pesos.argsort()[::-1][:6]]).",
  None),

 ("## 5. Clasificar el tema desde el texto",
  "Ahora el modelo: ¿puede una máquina adivinar el `tema` de una ficha leyendo solo su texto?\n\n"
  "1. Separa las fichas en **entrenamiento** (75 %) y **prueba** (25 %) con "
  "`train_test_split(..., stratify=df[\"tema\"], random_state=42)`. *Estratificar* mantiene la "
  "proporción de cada tema en ambos lados.\n"
  "2. Ajusta un vectorizador **solo con entrenamiento** (`fit_transform`) y aplícalo a prueba "
  "(`transform`). Si el vectorizador «viera» las fichas de prueba, la evaluación quedaría "
  "contaminada.\n"
  "3. Entrena una **regresión logística** y mide la **exactitud** (*accuracy*) en prueba.\n"
  "4. Compárala con la **línea base**: adivinar siempre el tema más común.",
  "Entrena y evalúa el clasificador",
  '''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X_train_txt, X_test_txt, y_train, y_test = train_test_split(
    df["texto"], df["tema"], test_size=0.25, stratify=df["tema"], random_state=42)

vec = TfidfVectorizer(analyzer=tokenizar, min_df=2)
X_train = vec.fit_transform(X_train_txt)
X_test = vec.transform(X_test_txt)

modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_train, y_train)
pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, pred)
linea_base = y_test.value_counts().max() / len(y_test)
print(f"fichas de prueba: {len(y_test)} | exactitud: {exactitud:.1%} | línea base: {linea_base:.1%}")''',
  '''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X_train_txt, X_test_txt, y_train, y_test = train_test_split(
    df["texto"], df["tema"], test_size=0.25, stratify=df["tema"], random_state=42)

vec = TfidfVectorizer(analyzer=tokenizar, min_df=2)
# TODO: fit_transform con el texto de ENTRENAMIENTO; solo transform con el de PRUEBA
X_train = ...
X_test = ...

modelo = LogisticRegression(max_iter=1000)
# TODO: entrena el modelo con X_train, y_train y predice sobre X_test
...
pred = ...

# TODO: exactitud en prueba (accuracy_score) y línea base (tema más común / total de prueba)
exactitud = ...
linea_base = ...
print("exactitud:", exactitud, "| línea base:", linea_base)''',
  '''assert len(pred) == len(y_test) == 62
assert abs(exactitud - accuracy_score(y_test, pred)) < 1e-12
assert abs(linea_base - y_test.value_counts().max() / len(y_test)) < 1e-12
assert exactitud > 3 * linea_base, "el modelo debería superar con creces a la línea base"''',
  "X_train = vec.fit_transform(X_train_txt); X_test = vec.transform(X_test_txt); modelo.fit(X_train, y_train); pred = modelo.predict(X_test); accuracy_score(y_test, pred).",
  None),

 ("## 6. Leer los errores del clasificador",
  "Una exactitud cercana al 56 % suena modesta, pero con 18 temas posibles es ~9 veces la línea "
  "base. Lo más valioso, sin embargo, está en **los errores**: arma una tabla con las fichas mal "
  "clasificadas y mira cuál es el tema que **más «atrae»** predicciones equivocadas.",
  "Arma la tabla de errores",
  '''tabla = pd.DataFrame({
    "titulo": df.loc[y_test.index, "titulo"],
    "real": y_test,
    "predicho": pred,
})
errores = tabla[tabla["real"] != tabla["predicho"]]
n_errores = len(errores)
tema_iman = errores["predicho"].value_counts().idxmax()
print(n_errores, "errores | tema que más atrae errores:", tema_iman)
errores[errores["predicho"] == tema_iman]''',
  '''tabla = pd.DataFrame({
    "titulo": df.loc[y_test.index, "titulo"],
    "real": y_test,
    "predicho": pred,
})
# TODO: filas donde el tema real es distinto del predicho
errores = ...
n_errores = ...
# TODO: el tema que más aparece como "predicho" dentro de los errores (value_counts().idxmax())
tema_iman = ...
print(n_errores, "errores | tema que más atrae errores:", tema_iman)''',
  '''assert n_errores == int((y_test.values != pred).sum())
assert set(errores.columns) == {"titulo", "real", "predicho"}
assert (errores["real"] != errores["predicho"]).all()
assert tema_iman == errores["predicho"].value_counts().idxmax()''',
  'errores = tabla[tabla["real"] != tabla["predicho"]]; n_errores = len(errores); errores["predicho"].value_counts().idxmax().',
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Mira la tabla de arriba: el modelo mandó a *trabajo-y-cesantía* fichas como **Aportes del
empleador al Sistema de Pensiones** (real: jubilación), **Beneficios asociados a la ley Bono
Laboral** (real: bonos) o **apelar el porcentaje de incapacidad por accidente del trabajo**
(real: previsión). Algo parecido ocurre con el propio **Bono de Invierno** (real: jubilación;
predicho: bonos-y-beneficios-del-estado) y con la *Beca Residencia Indígena* (real:
pueblos-originarios; predicho: becas-y-créditos).

En una o dos frases: ¿son **errores del modelo** o señales de que una ficha puede pertenecer
legítimamente a **más de un tema**? Si este clasificador se usara para sugerir el tema de las
fichas nuevas, ¿lo dejarías decidir solo, o como **sugerencia** que revisa una persona?

> Leer los errores — no solo la exactitud — es lo que separa un modelo útil de uno peligroso.'''

CIERRE = '''## Errores típicos

- **Vectorizar antes de separar** → el vectorizador «ve» las fichas de prueba (fuga de información) y la exactitud sale optimista.
- **`ValueError` al estratificar** → algún tema tiene un solo ejemplo; no se puede repartir entre entrenamiento y prueba.
- **Tokens raros como `257`** → los números sobreviven a la normalización; a veces conviene filtrarlos.
- **Mirar solo la exactitud** → esconde qué temas fallan y por qué (lo verás en la profundización).

## Cierre

- La tubería: **normalizar → tokenizar → stopwords → representar (TF-IDF) → modelar**.
- Las palabras **más frecuentes** no distinguen; **TF-IDF** destaca las que caracterizan a cada documento.
- Un clasificador lineal sobre TF-IDF adivina el tema de una ficha ~9 veces mejor que la línea base.
- Sus **errores** muestran el límite del método: cuenta palabras, no entiende — y una etiqueta única no siempre describe un documento.

> *En R3-02 darás el salto a un **modelo de lenguaje (LLM)** que sí capta significado: le pedirás
> que resuma una ficha en lenguaje claro y que extraiga sus requisitos como datos estructurados.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-01", "Introducción al NLP", "R3", "Especialista en IA Aplicada", "2",
                      ["**Normalizar** y **tokenizar** texto en español, quitando *stopwords*.",
                       "Medir **frecuencias** y entender por qué no bastan.",
                       "Representar documentos con **TF-IDF**.",
                       "Entrenar y evaluar un **clasificador de temas** (train/test estratificado, línea base).",
                       "**Leer los errores** del clasificador con criterio."],
                      "dado un conjunto de textos del Estado, prepararlos, representarlos y clasificarlos, evaluando honestamente el resultado.",
                      "245 fichas de trámites de ChileAtiende con texto completo y su tema oficial (18 temas).",
                      n_checks=len(EJ)),
        h.setup_cell("fichas.csv", IMPORTS),
        h.code(STOPWORDS_CELL),
        h.md(INTRO),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización (transferencia: texto corto de reclamos SERNAC) ───────────
PROF_PREP = f'''import os, urllib.request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), se baja del repo.
if not os.path.exists("reclamos.csv"):
    urllib.request.urlretrieve(f"{RAW}/reclamos.csv", "reclamos.csv")

reclamos = pd.read_csv("reclamos.csv")   # muestra de 20.000 reclamos SERNAC 2011 (dato histórico)
print(reclamos.shape)
reclamos[["producto", "mercado"]].head()'''

PROF_EJ = [
 ("## 1. Clases con muy pocos ejemplos",
  "Aquí el «texto» es corto: el **producto** reclamado (`\"LINEA DE CREDITO Y CUENTA CORRIENTE\"`), "
  "y la etiqueta es el **mercado** (financieros, telecomunicaciones…). Antes de entrenar, mira "
  "cuántos reclamos tiene cada mercado: uno tiene **un solo** reclamo, y con un solo ejemplo "
  "`stratify` no puede repartirlo entre entrenamiento y prueba (lanza `ValueError`). Decisión "
  "declarada: trabajamos con los mercados que tienen **al menos 50 reclamos**.",
  "Filtra los mercados con suficientes ejemplos",
  '''conteo = reclamos["mercado"].value_counts()
mercados_ok = conteo[conteo >= 50].index
rec = reclamos[reclamos["mercado"].isin(mercados_ok)]
n_mercados = rec["mercado"].nunique()
print("mercados:", reclamos["mercado"].nunique(), "→", n_mercados, "| reclamos:", len(reclamos), "→", len(rec))
print(conteo.tail(6))''',
  '''conteo = reclamos["mercado"].value_counts()
# TODO: índices (nombres) de los mercados con al menos 50 reclamos
mercados_ok = ...
# TODO: quédate solo con las filas de esos mercados (isin)
rec = ...
n_mercados = ...
print("mercados:", reclamos["mercado"].nunique(), "→", n_mercados)
print(conteo.tail(6))''',
  '''assert rec["mercado"].value_counts().min() >= 50
assert n_mercados == int((conteo >= 50).sum())
assert len(rec) == int(conteo[conteo >= 50].sum())''',
  'mercados_ok = conteo[conteo >= 50].index; rec = reclamos[reclamos["mercado"].isin(mercados_ok)]; n_mercados = rec["mercado"].nunique().'),

 ("## 2. El mismo pipeline, con texto corto y muchos datos",
  "Repite la receta de la lección: split estratificado (25 % prueba, `random_state=42`), "
  "TF-IDF ajustado solo con entrenamiento (aquí basta el `TfidfVectorizer()` por defecto: el "
  "texto ya viene en mayúsculas sin tildes), regresión logística, exactitud y línea base.",
  "Entrena y evalúa producto → mercado",
  '''X_tr, X_te, y_tr, y_te = train_test_split(
    rec["producto"], rec["mercado"], test_size=0.25, stratify=rec["mercado"], random_state=42)
vec = TfidfVectorizer()
modelo = LogisticRegression(max_iter=1000).fit(vec.fit_transform(X_tr), y_tr)
pred = modelo.predict(vec.transform(X_te))
exactitud = accuracy_score(y_te, pred)
linea_base = y_te.value_counts().max() / len(y_te)
print(f"exactitud: {exactitud:.1%} | línea base: {linea_base:.1%} ({y_te.value_counts().idxmax()})")''',
  '''X_tr, X_te, y_tr, y_te = train_test_split(
    rec["producto"], rec["mercado"], test_size=0.25, stratify=rec["mercado"], random_state=42)
vec = TfidfVectorizer()
# TODO: entrena LogisticRegression(max_iter=1000) con vec.fit_transform(X_tr) y predice con vec.transform(X_te)
modelo = ...
pred = ...
exactitud = ...
linea_base = ...
print("exactitud:", exactitud, "| línea base:", linea_base)''',
  '''assert abs(exactitud - accuracy_score(y_te, pred)) < 1e-12
assert exactitud > 0.9 and linea_base < 0.4''',
  "modelo = LogisticRegression(max_iter=1000).fit(vec.fit_transform(X_tr), y_tr); pred = modelo.predict(vec.transform(X_te))."),

 ("## 3. La exactitud esconde a las minorías",
  "Una exactitud de ~95 % parece un éxito. Pero los mercados grandes (financieros, "
  "telecomunicaciones) dominan el promedio. El **recall** de un mercado responde: de los reclamos "
  "que *de verdad* eran de ese mercado, ¿qué fracción detectó el modelo? Encuentra el peor.",
  "Encuentra el mercado peor detectado",
  '''reporte = classification_report(y_te, pred, output_dict=True, zero_division=0)
recall = {m: reporte[m]["recall"] for m in sorted(set(y_te))}
peor = min(recall, key=recall.get)
print(f"peor mercado: {peor} (recall {recall[peor]:.0%}, {int((y_te == peor).sum())} reclamos en prueba)")''',
  '''reporte = classification_report(y_te, pred, output_dict=True, zero_division=0)
# TODO: dict {mercado: reporte[mercado]["recall"]} para cada mercado de y_te
recall = ...
# TODO: el mercado con menor recall
peor = ...
print("peor mercado:", peor)''',
  '''assert len(recall) == n_mercados
assert peor == min(recall, key=recall.get)
assert recall[peor] < 0.5 < exactitud''',
  'recall = {m: reporte[m]["recall"] for m in sorted(set(y_te))}; peor = min(recall, key=recall.get).'),

 ("## 4. ¿Por qué falla? El texto no trae la información",
  "Mira los productos del peor mercado: *ELECTRÓNICA, COMPUTACIÓN, MUEBLES…* — los mismos que "
  "se reclaman en **locales comerciales**. El canal (tienda física o internet) no está en el "
  "texto del producto, así que **ningún** modelo de palabras puede distinguirlos. Mide qué "
  "fracción de los reclamos del peor mercado tiene un producto que también aparece en locales comerciales.",
  "Mide el solapamiento de productos",
  '''prod_peor = set(rec.loc[rec["mercado"] == peor, "producto"])
prod_locales = set(rec.loc[rec["mercado"] == "LOCALES COMERCIALES", "producto"])
compartidos = prod_peor & prod_locales
fraccion = rec.loc[rec["mercado"] == peor, "producto"].isin(compartidos).mean()
print(f"{len(compartidos)} productos compartidos | {fraccion:.0%} de los reclamos de {peor} usan uno de ellos")''',
  '''prod_peor = set(rec.loc[rec["mercado"] == peor, "producto"])
prod_locales = set(rec.loc[rec["mercado"] == "LOCALES COMERCIALES", "producto"])
# TODO: productos que están en AMBOS conjuntos (intersección &)
compartidos = ...
# TODO: fracción de reclamos del peor mercado cuyo producto está en compartidos (isin(...).mean())
fraccion = ...
print(len(compartidos), "productos compartidos | fracción:", fraccion)''',
  '''assert compartidos == prod_peor & prod_locales
assert abs(fraccion - rec.loc[rec["mercado"] == peor, "producto"].isin(compartidos).mean()) < 1e-12
assert fraccion > 0.5''',
  'compartidos = prod_peor & prod_locales; fraccion = rec.loc[rec["mercado"] == peor, "producto"].isin(compartidos).mean().'),
]

PROF_HEADER = '''# R3-01 · Introducción al NLP — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional y de **transferencia**: el mismo pipeline (TF-IDF + regresión logística), con un texto
muy distinto — el **producto** de 20.000 reclamos SERNAC de 2011 (dato histórico; SERNAC no
publica una base abierta más reciente) — para predecir el **mercado**. Texto corto y muchos
datos dan una exactitud altísima… que esconde a las clases pequeñas. Verás por qué el problema
no es el modelo, sino lo que el texto **no dice**.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md('''## Para llevar

- **Pocos ejemplos** por clase rompen la estratificación: agrupa, filtra o consigue más datos — y **declara** la decisión.
- Una exactitud global alta puede convivir con clases que el modelo casi nunca detecta: revisa el **recall por clase**.
- Si el texto no contiene la información (el canal de venta), ningún modelo la inventa. Es un problema de **datos**, no de algoritmo.

---

*Fin de la profundización de R3-01.*'''))
    nb.cells = cells
    return nb


README = '''# R3-01 · Introducción al NLP

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-01-introduccion-al-nlp/leccion.ipynb)

Primer contacto con el **texto como dato**, sobre las **245 fichas de trámites de ChileAtiende**
(`fichas.csv`): normalizar, tokenizar, quitar *stopwords*, contar frecuencias, representar con
**TF-IDF** y entrenar un **clasificador del tema** de cada ficha (train/test estratificado,
regresión logística, línea base) — para terminar **leyendo sus errores**. La profundización
transfiere el pipeline al texto corto de **reclamos SERNAC 2011** (`reclamos.csv`: producto →
mercado), donde la exactitud global esconde a las clases pequeñas.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: clases con pocos ejemplos, recall por clase y el límite del texto.

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.
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
