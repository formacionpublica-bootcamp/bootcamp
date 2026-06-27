# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A7 (IA generativa y LLMs):
A7/profundiza.ipynb (estudiante) + A7/profundiza_solucion.ipynb (resuelto).

TODO el cuaderno es CONCEPTUAL y verificable SIN conexión ni API key:
demos pequeñas (tokens, predicción del siguiente token, temperatura/softmax,
ventana de contexto) en Python puro sobre el dataset del módulo (rubros.csv)."""
import json, os

BASE = "A7-ia-generativa-y-llms"

TITULO = """# A7 · IA generativa y LLMs — Profundización (opcional) 🔬

**Formación Pública — Bloque avanzado · IA aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A7 —donde *usaste* un LLM real (Gemini) para
clasificar y extraer datos— aquí vamos al *porqué*: **cómo funciona por dentro** un modelo de lenguaje,
**por qué alucina**, qué hace de verdad la **temperatura**, qué es la **ventana de contexto**, por qué
hereda **sesgos** de sus datos, y dónde están los **límites para usarlo de forma responsable en el Estado**.

Menos llamadas al modelo, más **modelo mental**. Todo lo de aquí corre **sin API key y sin conexión**:
construiremos versiones de juguete de los mecanismos reales para *verlos* funcionar. Los ejercicios del
final son **conceptuales** y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de A7. Mismo dataset del módulo: `rubros.csv` (catálogo de rubros
> de compras públicas, estilo ChileCompra). **No necesitas API key para este cuaderno.**"""

CARGA = """import os, urllib.request, math, re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# rubros.csv del módulo (mismo dato de la lección). Si no está, se intenta descargar.
if not os.path.exists("rubros.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A7-ia-generativa-y-llms/rubros.csv"
        urllib.request.urlretrieve(url, "rubros.csv")
    except Exception:
        print("Si estás en Colab, sube rubros.csv manualmente.")

df = pd.read_csv("rubros.csv")
RUBROS = df["rubro"].tolist()
print(f"{len(RUBROS)} rubros cargados. Ejemplo:", RUBROS[0])
print("Este cuaderno NO usa API key: todo corre offline.")"""

S1 = """## 1. Por dentro: tokens y predicción del siguiente token

En la lección dijimos que un LLM "predice la próxima palabra". Afinemos eso, porque el *cómo* explica
casi todo su comportamiento (lo bueno y lo malo).

**Primero: no trabaja con palabras, sino con *tokens*.** Un token es un pedacito de texto: a veces una
palabra entera, a veces un trozo ("medica" + "mentos"), a veces un signo. El modelo parte el texto en
tokens y a cada uno le asigna un número. Esto importa por dos razones prácticas para ti:

- Lo que cobras/consumes se mide en **tokens**, no en palabras. (En los tokenizadores reales el español
  suele usar *más* tokens que el inglés para decir lo mismo, porque parten las palabras en trozos más
  finos. **Ojo:** nuestro tokenizador de juguete de abajo parte solo *por palabras*, así que **no**
  ilustra ese punto —sirve para ver el mecanismo, no para comparar idiomas.)
- El modelo "ve" tokens, no conceptos: por eso a veces tropieza con cosas que a un humano le parecen
  triviales (contar letras, aritmética larga).

**Segundo: lo único que hace el modelo es, dado lo anterior, asignar una probabilidad a cada token
posible y proponer el siguiente.** No "consulta una base de datos de verdades": estima qué continuación
es la más **plausible** según los patrones que vio al entrenar. Encadenando esa predicción token a token,
genera frases enteras.

Vamos a *verlo*: armaremos un mini-modelo de bigramas (qué palabra suele seguir a cuál) entrenado solo
con los nombres de los rubros. Es un LLM de juguete, pero el **mecanismo** —contar continuaciones y
predecir la siguiente— es el mismo en espíritu."""

S1_CODE = """# Tokenizador de juguete: minúsculas, partimos por palabras (los LLM reales parten más fino)
def tokenizar(texto):
    return re.findall(r"[a-záéíóúñ]+", texto.lower())

ejemplo = RUBROS[4]  # "Equipamiento y suministros médicos"
print("Texto :", ejemplo)
print("Tokens:", tokenizar(ejemplo))

# Cuántos tokens tiene TODO el catálogo (así se mide el 'consumo' real)
total_tokens = sum(len(tokenizar(r)) for r in RUBROS)
print(f"\\nEl catálogo completo son {total_tokens} tokens (en {len(RUBROS)} rubros).")
print("Regla práctica: en español, ~1 token por palabra corta; las palabras largas se parten en varios.")"""

S2 = """## 2. El mini-modelo: contar continuaciones y predecir

Un LLM aprende, de los datos, **qué token tiende a seguir a cuál**. Nuestro modelo de juguete hace
exactamente eso a nivel de palabra: recorre todos los rubros y cuenta, para cada palabra, qué palabras
aparecen justo después. Eso es una **distribución de probabilidad sobre el siguiente token**.

Ojo con la idea clave: el modelo **no sabe** qué es "correcto". Solo sabe qué fue **frecuente**. Esa es
la raíz de casi todo —incluidas las alucinaciones (sección 3) y los sesgos (sección 6)."""

S2_CODE = """from collections import defaultdict, Counter

# 'Entrenamiento': contar qué palabra sigue a cuál en el catálogo
siguientes = defaultdict(Counter)
for r in RUBROS:
    toks = tokenizar(r)
    for a, b in zip(toks, toks[1:]):
        siguientes[a][b] += 1

def probabilidades_siguiente(palabra):
    cont = siguientes[palabra]
    total = sum(cont.values())
    if total == 0:
        return {}
    return {w: n / total for w, n in cont.most_common()}

# ¿Qué suele seguir a 'suministros' en este catálogo?
print("Después de 'suministros', el modelo de juguete predice:")
for w, p in probabilidades_siguiente("suministros").items():
    print(f"  {w:>12}  prob = {p:.2f}")
print("\\nNo 'entiende' nada: solo aprendió qué fue frecuente. Igual que un LLM, a otra escala.")"""

S3 = """## 3. Por qué alucinan: optimizan plausibilidad, no verdad

Aquí está la idea más importante del cuaderno. Un LLM fue entrenado para que su salida **suene
probable**, no para que sea **verdadera**. Verdad y plausibilidad coinciden la mayoría de las veces
(por eso es útil), pero **no siempre** — y cuando se separan, el modelo elige sonar bien.

Una **alucinación** es justo eso: una afirmación fluida, segura y con buena forma… pero **falsa**. El
modelo no "miente" (no tiene intención): produce la continuación más plausible aunque por debajo no haya
ningún dato real que la respalde. Por eso inventa con total seguridad:

- una **cifra** de presupuesto que "suena" razonable,
- un **número de ley** o un artículo que no existe,
- una **cita** o un nombre de fantasía con formato impecable.

La consecuencia para el Estado es directa: **la fluidez no es evidencia**. Que una respuesta esté bien
redactada y suene confiada **no** te dice nada sobre si es correcta. Lo veremos con el mini-modelo:
generará frases perfectamente "con forma de rubro". A veces caerá, por casualidad, en un rubro que **sí**
existe; otras veces armará uno que **no existe** en el catálogo. Lo clave es que **el modelo no distingue
entre ambos casos**: en los dos hizo exactamente lo mismo —encadenar continuaciones plausibles— sin
ninguna noción de cuál es real. Esa indiferencia entre lo verdadero y lo inventado es, en miniatura, la
raíz de la alucinación."""

S3_CODE = """def generar_frase(inicio, n=4, rng=None):
    rng = rng or np.random.default_rng(0)
    frase = [inicio]
    actual = inicio
    for _ in range(n):
        probs = probabilidades_siguiente(actual)
        if not probs:
            break
        palabras = list(probs.keys())
        pesos = np.array(list(probs.values()))
        actual = rng.choice(palabras, p=pesos / pesos.sum())
        frase.append(actual)
    return " ".join(frase)

# Catálogo normalizado del MISMO modo que generamos (por tokens: sin comas ni mayúsculas),
# para que la comparación sea justa para todos los rubros (con o sin coma en el original).
catalogo_norm = [" ".join(tokenizar(r)) for r in RUBROS]

# Generamos varias frases con la misma semilla (reproducible) y clasificamos cada una:
# ¿el modelo "cayó" en un rubro real, o se "inventó" uno nuevo? Él NO lo sabe ni lo distingue.
rng = np.random.default_rng(7)
print("Frases que arma el modelo encadenando continuaciones plausibles:\\n")
for _ in range(8):
    frase = generar_frase("servicios", n=4, rng=rng)
    existe = frase in catalogo_norm
    etiqueta = "EXISTE en el catálogo" if existe else "INVENTADA (no existe)"
    print(f"  {frase:<50} -> {etiqueta}")

print("\\nEl punto NO es que siempre invente: a veces reproduce un rubro real y a veces fabrica uno.")
print("El modelo hizo lo mismo en ambos casos y NO distingue cuál es verdadero. Esa indiferencia")
print("entre lo real y lo plausible-pero-falso es, en miniatura, una ALUCINACIÓN.")"""

S4 = """## 4. La temperatura: el dial entre "seguro" y "creativo"

Cuando el modelo tiene la lista de probabilidades del siguiente token, ¿cómo elige? Ahí entra la
**temperatura**, un número —en las APIs más comunes (Gemini, OpenAI) entre **0 y 2**— que **reescala**
esas probabilidades antes de sortear. Como referencia: **0** para máxima precisión, **~1** para uso
general y **hasta 2** para máxima creatividad:

- **Temperatura baja (≈0):** el modelo casi siempre toma el token **más probable**. Respuestas
  **predecibles, repetitivas y conservadoras**. Ideal cuando quieres precisión y consistencia
  (clasificar, extraer JSON, seguir un formato estricto).
- **Temperatura alta (hacia 2):** **aplana** las probabilidades, así que tokens poco probables tienen
  más chance. Respuestas **más variadas y creativas**… y **más propensas a desvariar**.

La mecánica exacta es el ***softmax* con temperatura**: se toman las "puntuaciones" (logits), se dividen
por la temperatura `T` y se renormalizan. Dividir por una `T` chica **exagera** las diferencias (gana el
favorito); dividir por una `T` grande las **achata** (todos compiten). Lo implementamos para *verlo*."""

S4_CODE = """def softmax_temp(logits, T):
    logits = np.array(logits, dtype=float)
    z = logits / T                      # dividir por la temperatura
    z = z - z.max()                     # truco numérico (no cambia el resultado)
    e = np.exp(z)
    return e / e.sum()

# Tres opciones con puntuaciones crudas: una clara favorita y dos menos probables
opciones = ["médicos", "de oficina", "de limpieza"]
logits =   [2.0,       1.0,          0.5]

for T in [0.2, 1.0, 2.0]:
    p = softmax_temp(logits, T)
    reparto = "  ".join(f"{o}:{pi:.2f}" for o, pi in zip(opciones, p))
    print(f"T={T:<4} -> {reparto}   (favorito = {p.max():.2f})")

print("\\nT baja: el favorito casi se lo lleva todo (preciso, repetitivo).")
print("T alta: las probabilidades se achatan (creativo, pero más riesgo de desvarío).")"""

S5 = """## 5. La ventana de contexto: la "memoria de trabajo" del modelo

Un LLM no recuerda toda tu conversación para siempre. Tiene una **ventana de contexto**: un límite
máximo de **tokens** (tu prompt + lo que va generando) que puede tener "a la vista" al predecir el
siguiente token. Lo que cae **fuera** de la ventana, sencillamente **no existe** para el modelo en ese
momento.

Implicancias muy concretas para el trabajo público:

- Si pegas un documento larguísimo, **lo que excede la ventana se ignora** (o el sistema lo recorta): el
  modelo puede responder sin haber "leído" el final.
- En conversaciones largas, el modelo puede **"olvidar"** instrucciones que diste al principio, porque
  quedaron fuera de la ventana.
- Por eso conviene **resumir, recortar y poner lo importante cerca de la pregunta**. (Y por eso existe
  **RAG**, el próximo módulo: en vez de pegar *todo*, se le entrega solo el fragmento relevante.)

Simulemos una ventana pequeña y veamos qué "alcanza a ver" el modelo de un texto largo."""

S5_CODE = """def recortar_a_ventana(tokens, ventana):
    # Los sistemas suelen conservar lo más RECIENTE (el final): los últimos `ventana` tokens
    return tokens[-ventana:] if len(tokens) > ventana else tokens

# Un 'documento' largo: pegamos todos los rubros como si fueran un texto corrido
documento = " ".join(RUBROS)
toks_doc = tokenizar(documento)
VENTANA = 10

vistos = recortar_a_ventana(toks_doc, VENTANA)
print(f"El documento tiene {len(toks_doc)} tokens; la ventana solo deja ver {VENTANA}.")
print("Tokens que el modelo ve (los últimos):", vistos)
fuera = len(toks_doc) - len(vistos)
print(f"\\nQuedaron FUERA de la ventana {fuera} tokens del inicio: para el modelo, no existen.")"""

S6 = """## 6. Sesgos heredados y límites para el uso responsable en el Estado

Un LLM aprende de **textos escritos por personas**: internet, libros, foros. Por eso **hereda los
patrones de esos datos**, incluidos los **sesgos**. Si en el material de entrenamiento ciertos cargos,
oficios o atributos aparecen ligados a un grupo, el modelo **reproducirá esa asociación** —no porque sea
verdad, sino porque fue **frecuente**. Ejemplo concreto: si en el corpus de entrenamiento palabras como
*ingeniero* o *director* aparecen sistemáticamente junto a *hombre*, y *enfermera* o *secretaria* junto a
*mujer*, el modelo asociará esos cargos a ese género —aunque sea injusto y falso— solo porque eso fue lo
más frecuente en los textos. Esto puede colarse en tareas en apariencia neutras (redactar un perfil,
priorizar candidaturas, "completar" datos faltantes) y traducirse en **trato desigual**.

Súmale lo que ya vimos —**alucinaciones** (sección 3) y **ventana de contexto** (sección 5)— y obtienes
la lista de reglas no negociables para usar IA generativa en el sector público:

1. **Verifica toda cifra, ley, fecha o nombre** contra la fuente oficial. La fluidez **no** es evidencia.
2. **No envíes datos personales ni reservados** (RUT, salud, datos identificables): la capa gratuita
   suele usar tus textos para entrenar (por eso el *guardrail* de la lección).
3. **Cuida la equidad:** revisa que las salidas no arrastren sesgos; no automatices decisiones que
   afecten derechos sin supervisión humana.
4. **El responsable es humano:** el LLM asiste y redacta; **decide y responde** una persona.

Veámoslo en cifras con un mini-experimento sobre **representación en los datos**, la raíz del sesgo."""

S6_CODE = """# Mini-experimento: ¿está 'equilibrado' el vocabulario del catálogo?
# (Si una palabra domina, el modelo tenderá a sobre-representarla: así nace un sesgo de datos.)
todas = [t for r in RUBROS for t in tokenizar(r) if len(t) > 3]  # ignoramos conectores cortos
frec = Counter(todas)
top = frec.most_common(5)

print("Palabras de contenido más frecuentes en el catálogo:")
for w, n in top:
    print(f"  {w:>14}: {n}")

palabra_top, veces_top = top[0]
cuota = veces_top / sum(frec.values())
print(f"\\nLa palabra más frecuente ('{palabra_top}') concentra el {cuota:.0%} de las apariciones de contenido.")
print("Aquí es solo concentración léxica (un catálogo chico), pero el MECANISMO es el mismo que")
print("produce el sesgo social: el modelo refleja lo que MÁS aparece, no lo que es JUSTO. Si el")
print("corpus liga 'ingeniero' a 'hombre' más seguido, el modelo heredará esa asociación injusta.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Confiar en una cifra/ley/fecha porque "suena bien".** El modelo optimiza **plausibilidad, no verdad**: verifica siempre contra la fuente.
- **Creer que temperatura 0 elimina los errores.** Baja la *variabilidad*, no la *falsedad*: un modelo puede alucinar lo mismo de forma consistente.
- **Pegar un documento enorme y asumir que lo "leyó" todo.** Lo que excede la **ventana de contexto** se ignora; resume o usa RAG.
- **Tratar la salida como neutral.** El modelo **hereda los sesgos** de sus datos; revisa equidad antes de usarla en decisiones.
- **Enviar datos personales a la capa gratuita.** Pueden usarse para entrenar; usa *guardrails* y datos públicos.
- **Automatizar una decisión pública "porque lo dijo la IA".** El LLM asiste; la responsabilidad sigue siendo **humana**."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan algo, **todos** piden **elegir la interpretación
correcta**. **Ninguno requiere API key ni conexión.** Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 tokens ----
E1 = """## Ejercicio 01 · Tokens (no palabras)
Usa `tokenizar` (definida en la sección 1) sobre el rubro `"Medicamentos y productos farmacéuticos"`.

- Guarda en `n_tokens` la **cantidad de tokens** de ese texto.
- Luego elige en `conclusion` (letra) la lectura correcta:
  - **A.** El consumo de un LLM se mide en *frases*, así que el largo del texto da igual.
  - **B.** Lo que el modelo procesa y "consume" se mide en **tokens**; por eso un texto largo cuesta más.
  - **C.** Tokens y palabras son siempre exactamente lo mismo en cualquier idioma."""
E1_TODO = """texto = "Medicamentos y productos farmacéuticos"
n_tokens = None       # TODO: cantidad de tokens de `texto` (usa tokenizar)
conclusion = None     # TODO: "A", "B" o "C"
"""
E1_SOL = """texto = "Medicamentos y productos farmacéuticos"
n_tokens = len(tokenizar(texto))
conclusion = "B"
"""
E1_CHK = """try:
    _n = len(tokenizar("Medicamentos y productos farmacéuticos"))
    assert n_tokens is not None, "Aún no calculas n_tokens."
    assert int(n_tokens) == _n, f"Deberían ser {_n} tokens (usa tokenizar)."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿en qué unidad 've' y 'consume' el modelo?"
    print(f"✅ Correcto. Son {_n} tokens: el modelo razona y cobra en tokens, no en frases.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 temperatura ----
E2 = """## Ejercicio 02 · Temperatura y concentración
Usa `softmax_temp` (sección 4) con `logits = [2.0, 1.0, 0.5]`.

- Guarda en `p_baja` la probabilidad **del favorito** (el máximo) con `T = 0.2`.
- Guarda en `p_alta` la probabilidad **del favorito** con `T = 2.0`.
- Elige en `conclusion` la interpretación correcta:
  - **A.** Con `T` baja el favorito se lleva una probabilidad **mayor**: la salida es más concentrada y predecible.
  - **B.** Con `T` baja todas las opciones quedan **igual de probables**.
  - **C.** La temperatura no cambia las probabilidades, solo el color de la respuesta.

Pista: `softmax_temp([2.0,1.0,0.5], T).max()`."""
E2_TODO = """logits = [2.0, 1.0, 0.5]
p_baja = None       # TODO: máximo de softmax_temp(logits, 0.2)
p_alta = None       # TODO: máximo de softmax_temp(logits, 2.0)
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """logits = [2.0, 1.0, 0.5]
p_baja = softmax_temp(logits, 0.2).max()
p_alta = softmax_temp(logits, 2.0).max()
conclusion = "A"
"""
E2_CHK = """try:
    _pb = softmax_temp([2.0, 1.0, 0.5], 0.2).max()
    _pa = softmax_temp([2.0, 1.0, 0.5], 2.0).max()
    _correcta = "A" if _pb > _pa else "B"
    assert p_baja is not None and abs(p_baja - _pb) < 1e-6, "Revisa p_baja (máximo con T=0.2)."
    assert p_alta is not None and abs(p_alta - _pa) < 1e-6, "Revisa p_alta (máximo con T=2.0)."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿con qué T el favorito acapara más?"
    print(f"✅ Correcto. Favorito con T=0.2: {_pb:.2f}  vs  T=2.0: {_pa:.2f}. T baja = más concentrado.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 ventana de contexto ----
E3 = """## Ejercicio 03 · Ventana de contexto
Usa `recortar_a_ventana` (sección 5) y `toks_doc` (los tokens del 'documento' largo).

- Con una ventana de **8** tokens, guarda en `vistos` los tokens que el modelo alcanza a ver.
- Guarda en `n_fuera` cuántos tokens quedaron **fuera** de la ventana.
- Elige en `conclusion` la lectura correcta:
  - **A.** El modelo siempre ve el documento completo, sin importar su largo.
  - **B.** Lo que excede la ventana **no existe** para el modelo: puede responder sin haber "leído" esa parte.
  - **C.** La ventana solo afecta la velocidad, nunca lo que el modelo "ve"."""
E3_TODO = """VENTANA_EJ = 8
vistos = None       # TODO: recortar_a_ventana(toks_doc, VENTANA_EJ)
n_fuera = None      # TODO: cuántos tokens quedaron fuera
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = """VENTANA_EJ = 8
vistos = recortar_a_ventana(toks_doc, VENTANA_EJ)
n_fuera = len(toks_doc) - len(vistos)
conclusion = "B"
"""
E3_CHK = """try:
    _vistos = recortar_a_ventana(toks_doc, 8)
    _fuera = len(toks_doc) - len(_vistos)
    assert vistos is not None and list(vistos) == list(_vistos), "Revisa `vistos` (usa recortar_a_ventana con 8)."
    assert n_fuera is not None and int(n_fuera) == _fuera, f"Deberían quedar {_fuera} tokens fuera."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿qué pasa con lo que excede la ventana?"
    print(f"✅ Correcto. La ventana deja ver {len(_vistos)} tokens y deja {_fuera} fuera: el modelo no los 've'.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 alucinación / uso responsable (conceptual) ----
E4 = """## Ejercicio 04 · Alucinaciones y verificación (conceptual)
Un funcionario le pide a un LLM: *"¿Cuánto fue el presupuesto de salud municipal de Pichilemu en 2023?"*.
El modelo responde, con redacción impecable y tono seguro: *"Fue de \\$4.812.337.000, según el acta N° 47
del concejo"*. No existe forma de saber si el modelo vio ese dato real.

Elige en `conclusion` la lectura correcta:
- **A.** Como la respuesta es detallada, segura y cita un acta, se puede publicar tal cual.
- **B.** El modelo optimiza **plausibilidad, no verdad**: la cifra y el "acta N° 47" podrían ser una
  **alucinación**. Hay que **verificar contra la fuente oficial** antes de usar el número.
- **C.** Basta con bajar la temperatura a 0 para garantizar que la cifra sea verdadera.

*(Opcional, no se corrige): en `reflexion` escribe qué fuente oficial consultarías para verificar.)*"""
E4_TODO = """conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """conclusion = "B"
reflexion = "Consultaría el sitio de transparencia del municipio o el portal de presupuesto público (DIPRES), y el acta real del concejo."
"""
E4_CHK = """try:
    assert conclusion is not None, "Aún no elegiste una letra en 'conclusion'."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿la fluidez y el detalle prueban que el dato es real?"
    print("✅ Correcto. Fluidez ≠ evidencia: toda cifra/ley/nombre se verifica contra la fuente oficial.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir conclusion:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *usas* un LLM: entiendes **cómo predice** (tokens y probabilidad del siguiente token), **por
qué alucina** (optimiza plausibilidad, no verdad), qué hace la **temperatura**, qué es la **ventana de
contexto** y cómo **hereda sesgos** de sus datos.

La regla de oro que te llevas para el Estado: **la fluidez no es evidencia.** Verifica las cifras, cuida
los datos personales, vigila la equidad y recuerda que la decisión —y la responsabilidad— **siempre es
humana**. Eso distingue a quien *usa* la IA de quien *se deja usar* por ella.

> **Hacia dónde sigue:** en **RAG** (próximo módulo) resolverás el límite de la ventana y de las
> alucinaciones dándole al modelo **tus propios documentos** para que responda **citando la fuente**."""


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
