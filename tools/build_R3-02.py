"""build_R3-02.py — módulo R3-02 (IA generativa y LLMs).

Rama R3 (IA Aplicada). Un LLM (Gemini, detrás de preguntar_llm() de
build_helpers.GET_LLM_SNIPPET) sobre el ANCLA de la rama: las fichas de ChileAtiende.
Prompts para resumir en lenguaje claro, extracción de requisitos como JSON con
parser y validador propios, few-shot, temperatura y alucinación (verificar montos
contra la fuente), verificación humana y guardrail de datos personales.
Rearmado 2026 (nueva versión sobre fichas).

Todo corre SIN clave ni red: preguntar_llm() devuelve respaldos deterministas
(escritos a partir del texto de la ficha) y NINGÚN chequeo depende de la respuesta
en vivo — se verifican las funciones propias (prompt, parser, validador, verificador).
Profundiza = fidelidad de un resumen frente a su fuente y reescritura en lectura fácil.

Uso:  /opt/anaconda3/bin/python tools/build_R3-02.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-02-ia-generativa-y-llms")

IMPORTS = "import pandas as pd\nimport json, re"

FICHAS_CELL = r'''# Las dos fichas con que trabajaremos
pgu = df[df["id"] == 130457].iloc[0]        # Aumento de la PGU
invierno = df[df["id"] == 39484].iloc[0]    # Bono de Invierno

# Cada ficha tiene una introducción y luego secciones que empiezan con "## ".
def secciones(texto):
    return re.findall(r"^## (.+)$", texto, flags=re.M)

# Para extraer datos del Bono de Invierno usamos su introducción: lo que va antes de la primera sección.
fragmento = invierno["texto"].split("\n## ")[0].strip()

for f in [pgu, invierno]:
    print(f["titulo"], "·", f["institucion"], "·", f["n_palabras"], "palabras")
    print("   secciones:", secciones(f["texto"]))
print()
print(pgu["texto"][:700], "...")'''

QUE_ES = '''## 1. ¿Qué es un LLM y qué cambia respecto de R3-01?

En R3-01 el modelo **contaba palabras**: no sabía que «PGU» y «Pensión Garantizada Universal» son
lo mismo. Un **LLM** (*Large Language Model*: Gemini, ChatGPT, Claude) se entrena con una tarea
engañosamente simple — **predecir la siguiente palabra** — sobre cantidades enormes de texto, y
para hacerlo bien termina capturando significado, sinónimos y contexto. Por eso puede **resumir,
reescribir, extraer y clasificar** sin que nadie lo programe para cada tarea.

Tú lo diriges con el **prompt** (la instrucción). Tres reglas que rinden de inmediato:

1. **Sé específico:** qué quieres, para quién y en qué formato («resume en lenguaje claro, máximo 60 palabras»).
2. **Da contexto:** pega el texto fuente, las opciones válidas, ejemplos.
3. **Acota la salida:** si quieres JSON, dilo, define las claves y prohíbe el texto extra.

Y una regla de oro para programar con LLMs: **el modelo es probabilístico** — el mismo prompt
puede dar respuestas distintas, y a veces **inventa** con total seguridad (*alucina*). Por eso,
en este módulo, **tu código no confía en la respuesta: la verifica**. Los chequeos revisan tus
funciones (el prompt, el parser, el validador, el verificador), nunca el texto exacto del LLM.'''

CLAVE = '''## 2. Tu clave gratuita de Gemini (opcional) y la regla de privacidad

Usaremos **Gemini** a través de **Google AI Studio**: gratis, sin tarjeta, con tu cuenta de Google.

1. Entra a **https://aistudio.google.com/apikey** e inicia sesión.
2. Pulsa **Create API key** y copia la clave.
3. En Colab: panel izquierdo → 🔑 **Secretos** → **Agregar un secreto nuevo** → nombre
   `GEMINI_API_KEY`, pega el valor y activa **Acceso del notebook**.

> 🔒 **Nunca pegues la clave en una celda**: quedaría guardada en el archivo y en cualquier copia
> que compartas. Úsala siempre desde los Secretos.

> 🛡️ **No envíes datos personales al LLM.** En la capa gratuita, el proveedor puede usar tus textos
> para mejorar sus modelos. Aquí trabajamos con fichas **públicas** de ChileAtiende; nunca con RUT,
> nombres de personas, datos de salud ni información reservada (lo automatizamos en el ejercicio 6).

**¿Sin clave?** No pasa nada: `preguntar_llm()` devuelve una **respuesta de respaldo** y todo el
notebook corre igual. La celda siguiente define `preguntar_llm(prompt, respaldo=...)`: es la única
puerta al modelo (cambiar de proveedor = cambiar solo esa celda). Colab ya trae el paquete
`google-genai`; si en otro entorno ves *No module named google*, ejecuta `!pip install -q google-genai`.'''

ESTADO = '''if _clave_gemini():
    print("🔑 Clave detectada → modo EN VIVO con", MODELO)
else:
    print("ℹ️ Sin GEMINI_API_KEY → modo RESPALDO: verás respuestas de ejemplo y todo funciona igual.")

print(preguntar_llm("Explica en una frase qué es ChileAtiende.",
                    respaldo="ChileAtiende es la red del Estado que orienta a las personas sobre trámites y beneficios públicos."))'''

RESPALDOS_MD = '''### Las respuestas de respaldo

Sin clave, `preguntar_llm()` devuelve el `respaldo` que le pases. Abajo están los de este
módulo: **respuestas de ejemplo escritas a mano a partir del texto de las fichas** (no generadas
en vivo), con el formato típico de un LLM — incluido el JSON envuelto en ```` ```json ```` con una
frase antes. `RESPUESTA_DUDOSA` es una extracción con errores plantados, como las que produce un
modelo cuando alucina: la usaremos para probar que tu verificador los atrapa.'''

RESPALDOS = r'''RESPALDO_RESUMEN = ("Con la Reforma de Pensiones, la Pensión Garantizada Universal (PGU) subió. "
    "Desde febrero de 2026, si tienes 82 años o más recibes hasta $250.275, y si tienes entre 65 y 81 años, "
    "hasta $231.732. Desde septiembre de 2026, las personas de 75 años o más podrán recibir el monto máximo. "
    "Consulta con tu RUN cuándo aumentará tu PGU.")

RESPALDO_EXTRACCION = """Aquí está el JSON solicitado:
```json
{
  "tramite": "Bono de Invierno",
  "institucion": "Instituto de Previsión Social",
  "requisitos": [
    "Tener 65 años o más al 1 de mayo de 2026",
    "Recibir una pensión que no supere los $231.440"
  ],
  "montos_clp": [81257, 231440]
}
```"""

RESPUESTA_DUDOSA = """```json
{
  "tramite": "Bono de Invierno",
  "institucion": "Instituto de Previsión Social",
  "requisitos": [
    "Tener 65 años o más al 1 de mayo de 2026",
    "Postular en tu AFP antes del 30 de abril"
  ],
  "montos_clp": [85000, 231440]
}
```"""

RESPALDO_TEMA = "bonos-y-beneficios-del-estado"
print("Respaldos listos.")'''

EXTRACCION_MD = '''## Extraer requisitos como datos estructurados

Una de las tareas más útiles de un LLM en el Estado: convertir **texto libre** en **datos con
forma** — un JSON con claves fijas que después se guarda en una tabla. El prompt de abajo define
el **contrato**: qué claves, de qué tipo, y la prohibición de inventar. Ejecútalo para ver la
respuesta (en vivo o de respaldo): fíjate que el LLM suele **envolver** el JSON en ```` ``` ```` y
agregar una frase antes. `json.loads` sobre esa respuesta cruda **falla**: necesitas un parser.'''

PROMPT_EXTRACCION = r'''def prompt_extraccion(ficha, fragmento):
    return f"""Extrae del texto los datos del trámite «{ficha['titulo']}» ({ficha['institucion']}).
Responde SOLO con un JSON con exactamente estas claves:
- "tramite": nombre del trámite (texto)
- "institucion": institución responsable (texto)
- "requisitos": lista de requisitos, cada uno una frase corta (lista de textos)
- "montos_clp": montos en pesos que aparezcan en el texto, como enteros sin $ ni puntos (lista de enteros)
No agregues requisitos ni montos que no estén en el texto.

TEXTO:
{fragmento}"""

respuesta_cruda = preguntar_llm(prompt_extraccion(invierno, fragmento), respaldo=RESPALDO_EXTRACCION)
print(respuesta_cruda)
try:
    json.loads(respuesta_cruda)
except json.JSONDecodeError as e:
    print("\n⚠️ json.loads directo falla:", e)'''

TEMPERATURA_MD = '''## Temperatura y alucinación

La **temperatura** controla cuánto «se arriesga» el modelo al elegir cada palabra: cerca de **0**
elige casi siempre la opción más probable (respuestas estables, repetibles); valores altos
(1 a 2) eligen opciones menos probables (más variedad… y más riesgo de inventar). Para extraer
datos de una ficha quieres temperatura **baja**; para lluvia de ideas, puedes subirla.

Con clave, la celda de abajo pide la misma extracción dos veces con temperatura 0 y dos con 1,8:
compara. Sin clave verás el respaldo — y la lección es la misma: **ninguna temperatura garantiza
la verdad**. Un modelo puede inventar con temperatura 0. Por eso, lo que sigue es **verificar**.'''

TEMPERATURA = r'''def preguntar_llm_temperatura(prompt, temperatura, respaldo):
    """Como preguntar_llm, pero fijando la temperatura (0 = estable, 2 = muy variable)."""
    clave = _clave_gemini()
    if not clave:
        return respaldo
    try:
        from google import genai
        from google.genai import types
        cliente = genai.Client(api_key=clave)
        r = cliente.models.generate_content(
            model=MODELO, contents=prompt,
            config=types.GenerateContentConfig(temperature=temperatura))
        return r.text
    except Exception as e:
        print("⚠️ No se pudo llamar al LLM:", e)
        return respaldo

for t in [0.0, 1.8]:
    for intento in [1, 2]:
        r = preguntar_llm_temperatura(prompt_extraccion(invierno, fragmento), t, RESPALDO_EXTRACCION)
        d = parsear_json(r)
        print(f"temperatura {t} · intento {intento}:", d["montos_clp"] if d else "(JSON inválido)")'''

VERIF_HUMANA = '''## La verificación humana no se automatiza del todo

Tu verificador atrapó el monto inventado (`85000`). Pero mira los **requisitos** de la
`RESPUESTA_DUDOSA` junto al texto fuente:'''

VERIF_HUMANA_CODE = r'''dudosa = parsear_json(RESPUESTA_DUDOSA)
for req in dudosa["requisitos"]:
    print("•", req)
print("\nFUENTE:\n" + fragmento)'''

VERIF_HUMANA_2 = '''«Postular en tu AFP antes del 30 de abril» **no está en la fuente** — y la fuente dice lo
contrario: es un beneficio **no postulable**. Ninguna regla simple lo detecta: hace falta una
persona que lea. Lista de verificación mínima antes de publicar algo producido por un LLM:

1. **Cifras y fechas:** ¿cada monto, edad y fecha aparece en la fuente oficial? (automatizable, ejercicio 5)
2. **Requisitos y condiciones:** ¿cada uno está en la fuente, sin agregados ni contradicciones? (lectura humana)
3. **Omisiones:** ¿falta algo que cambia quién accede al beneficio? (lectura humana)
4. **Datos personales:** ¿el texto enviado al LLM estaba libre de ellos? (automatizable, ejercicio 6)
5. **Responsable:** ¿quién firma? El LLM asiste; la responsabilidad pública es de una persona.'''

EJ = [
 ("## 3. Un prompt para resumir en lenguaje claro",
  "La ficha de la PGU tiene 893 palabras repartidas en una introducción y 4 secciones, con "
  "siglas (PBSI, APSI, DIPRECA) y frases largas. "
  "Escribe `prompt_resumen(ficha, max_palabras=60)`, que arme un prompt con cuatro partes: "
  "**rol** (ya está), **tarea** (resumir la ficha — con su título — en *lenguaje claro*, en "
  "máximo `max_palabras` palabras), **reglas** (ya están) y la **fuente**: el texto completo "
  "precedido de `TEXTO DE LA FICHA:`.",
  "Escribe `prompt_resumen`",
  r'''def prompt_resumen(ficha, max_palabras=60):
    rol = "Eres un funcionario de ChileAtiende que explica trámites a la ciudadanía."
    tarea = f"Resume la ficha «{ficha['titulo']}» en lenguaje claro, en máximo {max_palabras} palabras."
    reglas = ("Usa solo la información del texto; si un dato no está, no lo inventes. "
              "Conserva montos, edades y fechas tal como aparecen.")
    fuente = "TEXTO DE LA FICHA:\n" + ficha["texto"]
    return "\n".join([rol, tarea, reglas, "", fuente])

print(prompt_resumen(pgu)[:400], "...")''',
  r'''def prompt_resumen(ficha, max_palabras=60):
    rol = "Eres un funcionario de ChileAtiende que explica trámites a la ciudadanía."
    # TODO: f-string que pida resumir la ficha «{ficha['titulo']}» en lenguaje claro, en máximo {max_palabras} palabras
    tarea = ...
    reglas = ("Usa solo la información del texto; si un dato no está, no lo inventes. "
              "Conserva montos, edades y fechas tal como aparecen.")
    # TODO: "TEXTO DE LA FICHA:\n" seguido del texto completo de la ficha
    fuente = ...
    return "\n".join([rol, tarea, reglas, "", fuente])

print(prompt_resumen(pgu)[:400], "...")''',
  r'''_p = prompt_resumen(pgu)
assert pgu["titulo"] in _p, "el prompt debe nombrar la ficha"
assert _p.count(pgu["texto"]) == 1, "el texto completo de la ficha debe ir una vez"
assert "lenguaje claro" in _p.lower()
assert "60" in _p and "45" in prompt_resumen(pgu, 45), "el límite debe salir de max_palabras"
assert "TEXTO DE LA FICHA:" in _p''',
  "tarea = f\"Resume la ficha «{ficha['titulo']}» en lenguaje claro, en máximo {max_palabras} palabras.\"; fuente = \"TEXTO DE LA FICHA:\\n\" + ficha[\"texto\"].",
  r'''resumen = preguntar_llm(prompt_resumen(pgu), respaldo=RESPALDO_RESUMEN)
print(resumen)
print(f"\n→ {len(resumen.split())} palabras (la ficha tiene {pgu['n_palabras']})")'''),

 ("## 4. Un parser que no confía en el formato",
  "Escribe `parsear_json(respuesta)`: busca la **primera** `{` y la **última** `}` del texto, "
  "intenta `json.loads` sobre ese trozo y devuelve el `dict`; si no hay llaves o el JSON es "
  "inválido, devuelve `None` (sin lanzar error). Así sobrevive a los ```` ``` ```` y a las frases "
  "de cortesía del modelo.",
  "Escribe `parsear_json`",
  r'''def parsear_json(respuesta):
    texto = respuesta.strip()
    inicio = texto.find("{")
    fin = texto.rfind("}")
    if inicio == -1 or fin == -1 or fin < inicio:
        return None
    try:
        return json.loads(texto[inicio:fin + 1])
    except json.JSONDecodeError:
        return None

extraccion = parsear_json(respuesta_cruda)
print(extraccion)''',
  r'''def parsear_json(respuesta):
    texto = respuesta.strip()
    # TODO: posición de la primera "{" (texto.find) y de la última "}" (texto.rfind)
    inicio = ...
    fin = ...
    if inicio == -1 or fin == -1 or fin < inicio:
        return None
    try:
        # TODO: json.loads del trozo texto[inicio:fin + 1]
        return ...
    except json.JSONDecodeError:
        return None

extraccion = parsear_json(respuesta_cruda)
print(extraccion)''',
  r'''_d = parsear_json(RESPALDO_EXTRACCION)
assert isinstance(_d, dict) and _d["tramite"] == "Bono de Invierno"
assert parsear_json("Lo siento, no puedo ayudarte con eso.") is None
assert parsear_json('{"a": 1,}') is None, "un JSON inválido debe dar None, no un error"
assert parsear_json('Aquí va: {"a": [1, 2]} ¡listo!') == {"a": [1, 2]}''',
  "inicio = texto.find('{'); fin = texto.rfind('}'); return json.loads(texto[inicio:fin + 1]).",
  None),

 ("## 5. Validar el JSON contra el contrato",
  "Que el JSON se pueda leer no significa que cumpla el contrato del prompt. Escribe "
  "`validar_extraccion(d)`, que devuelva una **lista de problemas** (vacía si todo está bien): "
  "claves que faltan, claves con el tipo equivocado, y montos que no sean enteros.",
  "Escribe `validar_extraccion`",
  r'''CONTRATO = {"tramite": str, "institucion": str, "requisitos": list, "montos_clp": list}

def validar_extraccion(d):
    if not isinstance(d, dict):
        return ["la respuesta no es un objeto JSON"]
    problemas = []
    for clave, tipo in CONTRATO.items():
        if clave not in d:
            problemas.append(f"falta la clave '{clave}'")
        elif not isinstance(d[clave], tipo):
            problemas.append(f"'{clave}' debería ser {tipo.__name__}")
    if isinstance(d.get("requisitos"), list) and len(d["requisitos"]) == 0:
        problemas.append("la lista de requisitos está vacía")
    if isinstance(d.get("montos_clp"), list) and not all(isinstance(m, int) for m in d["montos_clp"]):
        problemas.append("los montos deben ser enteros (sin $ ni puntos)")
    return problemas

print("respaldo:", validar_extraccion(parsear_json(RESPALDO_EXTRACCION)))
print("malo:    ", validar_extraccion({"tramite": "Bono", "requisitos": "tener 65 años", "montos_clp": ["$81.257"]}))''',
  r'''CONTRATO = {"tramite": str, "institucion": str, "requisitos": list, "montos_clp": list}

def validar_extraccion(d):
    if not isinstance(d, dict):
        return ["la respuesta no es un objeto JSON"]
    problemas = []
    for clave, tipo in CONTRATO.items():
        # TODO: si falta la clave → agrega f"falta la clave '{clave}'"
        #       si existe pero no es del tipo → agrega f"'{clave}' debería ser {tipo.__name__}"
        ...
    if isinstance(d.get("requisitos"), list) and len(d["requisitos"]) == 0:
        problemas.append("la lista de requisitos está vacía")
    # TODO: si montos_clp es lista y algún elemento NO es int → agrega un problema
    ...
    return problemas

print("respaldo:", validar_extraccion(parsear_json(RESPALDO_EXTRACCION)))
print("malo:    ", validar_extraccion({"tramite": "Bono", "requisitos": "tener 65 años", "montos_clp": ["$81.257"]}))''',
  r'''assert validar_extraccion(parsear_json(RESPALDO_EXTRACCION)) == []
_malo = validar_extraccion({"tramite": "Bono", "requisitos": "tener 65 años", "montos_clp": ["$81.257"]})
assert isinstance(_malo, list) and len(_malo) == 3, "esperaba 3 problemas: falta institucion, requisitos no es lista, montos no enteros"
assert len(validar_extraccion(None)) == 1
assert validar_extraccion({"tramite": "x", "institucion": "y", "requisitos": [], "montos_clp": []}) == ["la lista de requisitos está vacía"]''',
  "Dentro del for: if clave not in d: problemas.append(...) / elif not isinstance(d[clave], tipo): problemas.append(...). Luego: if isinstance(d.get('montos_clp'), list) and not all(isinstance(m, int) for m in d['montos_clp']): problemas.append(...).",
  None),

 ("## 6. Few-shot: enseñar con ejemplos dentro del prompt",
  "En R3-01 entrenaste un clasificador con 183 fichas. Con un LLM basta mostrar **unos pocos "
  "ejemplos** en el propio prompt (*few-shot*) y la lista de temas válidos. Completa "
  "`prompt_few_shot(titulo, ejemplos, temas)`: agrega cada ejemplo como dos líneas "
  "`Trámite: …` / `Tema: …`. El prompt termina en `Tema:` para que el modelo solo complete la etiqueta.",
  "Escribe `prompt_few_shot`",
  r'''TEMAS = sorted(df["tema"].unique())
EJEMPLOS = [
    ("Bono Logro Escolar", "educacion"),
    ("Certificado de nacimiento para chilenos y chilenas en el extranjero", "chilenos-en-el-exterior"),
    ("Anticipo de primera pensión de CAPREDENA", "jubilacion"),
]

def prompt_few_shot(titulo, ejemplos, temas):
    lineas = ["Clasifica el trámite en UNO de estos temas (responde solo el tema):",
              ", ".join(temas), "", "Ejemplos:"]
    for tramite, tema in ejemplos:
        lineas.append(f"Trámite: {tramite}")
        lineas.append(f"Tema: {tema}")
    lineas += ["", f"Trámite: {titulo}", "Tema:"]
    return "\n".join(lineas)

print(prompt_few_shot("Aguinaldo de Navidad para pensionados IPS", EJEMPLOS, TEMAS))''',
  r'''TEMAS = sorted(df["tema"].unique())
EJEMPLOS = [
    ("Bono Logro Escolar", "educacion"),
    ("Certificado de nacimiento para chilenos y chilenas en el extranjero", "chilenos-en-el-exterior"),
    ("Anticipo de primera pensión de CAPREDENA", "jubilacion"),
]

def prompt_few_shot(titulo, ejemplos, temas):
    lineas = ["Clasifica el trámite en UNO de estos temas (responde solo el tema):",
              ", ".join(temas), "", "Ejemplos:"]
    for tramite, tema in ejemplos:
        # TODO: agrega a lineas "Trámite: {tramite}" y luego "Tema: {tema}"
        ...
    lineas += ["", f"Trámite: {titulo}", "Tema:"]
    return "\n".join(lineas)

print(prompt_few_shot("Aguinaldo de Navidad para pensionados IPS", EJEMPLOS, TEMAS))''',
  r'''_p = prompt_few_shot("Aguinaldo de Navidad para pensionados IPS", EJEMPLOS, TEMAS)
for _t, _tema in EJEMPLOS:
    assert f"Trámite: {_t}\nTema: {_tema}" in _p, f"falta el ejemplo «{_t}»"
assert all(t in _p for t in TEMAS), "el prompt debe listar los temas válidos"
assert _p.rstrip().endswith("Trámite: Aguinaldo de Navidad para pensionados IPS\nTema:")''',
  'Dentro del for: lineas.append(f"Trámite: {tramite}") y lineas.append(f"Tema: {tema}").',
  r'''def elegir_tema(respuesta, temas):
    """Acepta la respuesta solo si es uno de los temas válidos; si no, None."""
    r = respuesta.strip().strip(".\"'«»").lower()
    return r if r in temas else None

resp = preguntar_llm(prompt_few_shot("Aguinaldo de Navidad para pensionados IPS", EJEMPLOS, TEMAS),
                     respaldo=RESPALDO_TEMA)
print("respuesta:", repr(resp), "→ tema válido:", elegir_tema(resp, TEMAS))
print("tema oficial en ChileAtiende:", df.loc[df["titulo"] == "Aguinaldo de Navidad para pensionados IPS", "tema"].iloc[0])'''),

 ("## 7. Verificar las cifras contra la fuente",
  "La primera defensa contra la alucinación es **automática**: todo monto que el LLM extrajo "
  "debe aparecer en el texto fuente. `montos_en_texto` (ya escrita) encuentra los montos con "
  "`$` de un texto y los convierte a enteros. Escribe `montos_no_respaldados(montos, fuente)`: "
  "la lista de montos extraídos que **no** están en la fuente.",
  "Escribe `montos_no_respaldados`",
  r'''def montos_en_texto(texto):
    """{81257, 231440} a partir de '... $81.257 ... $231.440 ...'"""
    return {int(m.replace(".", "")) for m in re.findall(r"\$\s?(\d{1,3}(?:\.\d{3})+|\d+)", texto)}

def montos_no_respaldados(montos, fuente):
    en_fuente = montos_en_texto(fuente)
    return [m for m in montos if m not in en_fuente]

print("montos en la fuente:", montos_en_texto(fragmento))
print("respaldo:", montos_no_respaldados(parsear_json(RESPALDO_EXTRACCION)["montos_clp"], fragmento))
print("dudosa:  ", montos_no_respaldados(parsear_json(RESPUESTA_DUDOSA)["montos_clp"], fragmento))''',
  r'''def montos_en_texto(texto):
    """{81257, 231440} a partir de '... $81.257 ... $231.440 ...'"""
    return {int(m.replace(".", "")) for m in re.findall(r"\$\s?(\d{1,3}(?:\.\d{3})+|\d+)", texto)}

def montos_no_respaldados(montos, fuente):
    # TODO: montos de la fuente (montos_en_texto) y lista de los montos que NO están ahí
    ...

print("montos en la fuente:", montos_en_texto(fragmento))
print("respaldo:", montos_no_respaldados(parsear_json(RESPALDO_EXTRACCION)["montos_clp"], fragmento))
print("dudosa:  ", montos_no_respaldados(parsear_json(RESPUESTA_DUDOSA)["montos_clp"], fragmento))''',
  r'''assert montos_en_texto(fragmento) == {81257, 231440}
assert montos_no_respaldados(parsear_json(RESPALDO_EXTRACCION)["montos_clp"], fragmento) == []
assert montos_no_respaldados(parsear_json(RESPUESTA_DUDOSA)["montos_clp"], fragmento) == [85000]
assert montos_no_respaldados([250275, 1], pgu["texto"]) == [1]''',
  "en_fuente = montos_en_texto(fuente); return [m for m in montos if m not in en_fuente].",
  None),

 ("## 8. Guardrail: nada con RUT sale hacia el LLM",
  "Antes de enviar cualquier texto a un servicio externo, revisa que no lleve datos personales. "
  "El caso más típico en Chile es el **RUT** (`12.345.678-9`, con o sin puntos, dígito "
  "verificador número o `K`). Escribe `es_seguro_enviar(texto)`: `False` si encuentra un RUT, "
  "`True` si no. Patrón: `r\"\\b\\d{1,2}\\.?\\d{3}\\.?\\d{3}-[\\dkK]\\b\"`.",
  "Escribe `es_seguro_enviar`",
  r'''PATRON_RUT = r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b"

def es_seguro_enviar(texto):
    return re.search(PATRON_RUT, texto) is None

consulta = "Mi RUT es 12.345.678-9 y quiero saber si me corresponde el Bono de Invierno"
print(es_seguro_enviar(pgu["texto"]), es_seguro_enviar(consulta))''',
  r'''PATRON_RUT = r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b"

def es_seguro_enviar(texto):
    # TODO: True si re.search(PATRON_RUT, texto) NO encuentra nada
    ...

consulta = "Mi RUT es 12.345.678-9 y quiero saber si me corresponde el Bono de Invierno"
print(es_seguro_enviar(pgu["texto"]), es_seguro_enviar(consulta))''',
  r'''assert es_seguro_enviar(pgu["texto"]) == True
assert es_seguro_enviar(consulta) == False
assert es_seguro_enviar("RUT 9876543-K, pensionado") == False, "también sin puntos y con K"
assert all(es_seguro_enviar(t) for t in df["texto"]), "las fichas públicas no traen RUT: deben pasar"''',
  "return re.search(PATRON_RUT, texto) is None.",
  None),
]

CIERRE = '''## Cierre

- Un **LLM** capta significado: resume, extrae y clasifica con pocas instrucciones — tú lo diriges con el **prompt** (rol, tarea, reglas, fuente).
- El prompt define un **contrato**; tu código lo hace cumplir: **parser** tolerante, **validador** de claves y tipos.
- **Few-shot**: unos pocos ejemplos en el prompt reemplazan el entrenamiento — pero la salida igual se **valida** contra la lista de temas.
- La **temperatura** regula la variabilidad, no la verdad: las cifras se **verifican contra la fuente** y los requisitos los **lee una persona**.
- **Nunca** pegues tu clave en el notebook ni envíes datos personales: secretos de Colab y guardrail.

> *En R3-03 (RAG) le darás al LLM las fichas como **fuente** para responder preguntas de la
> ciudadanía citando de dónde sacó cada dato — con la verificación de hoy como red de seguridad.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-02", "IA generativa y LLMs", "R3", "Especialista en IA Aplicada", "3",
                      ["Escribir **prompts** con rol, tarea, reglas y fuente para **resumir en lenguaje claro**.",
                       "Extraer **requisitos como JSON** y hacerlo cumplir con un **parser** y un **validador** propios.",
                       "Clasificar con **few-shot** y aceptar solo salidas válidas.",
                       "Entender **temperatura y alucinación** y **verificar cifras contra la fuente**.",
                       "Proteger datos personales con un **guardrail** y aplicar **verificación humana**."],
                      "usar un LLM sobre texto del Estado de forma verificable y responsable: el código no confía en la respuesta, la valida.",
                      "fichas de ChileAtiende — Aumento de la PGU y Bono de Invierno (texto oficial vigente).",
                      n_checks=len(EJ)),
        h.setup_cell("fichas.csv", IMPORTS),
        h.code(FICHAS_CELL),
        h.md(QUE_ES),
        h.md(CLAVE),
        h.code(h.GET_LLM_SNIPPET),
        h.code(ESTADO),
        h.md(RESPALDOS_MD),
        h.code(RESPALDOS),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        if i == 2:   # antes del parser: el prompt de extracción y la respuesta cruda
            cells.append(h.md(EXTRACCION_MD))
            cells.append(h.code(PROMPT_EXTRACCION))
        if i == 5:   # antes de verificar: temperatura
            cells.append(h.md(TEMPERATURA_MD))
            cells.append(h.code(TEMPERATURA))
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
        if i == 5:   # después de verificar montos: lo que no se automatiza
            cells.append(h.md(VERIF_HUMANA))
            cells.append(h.code(VERIF_HUMANA_CODE))
            cells.append(h.md(VERIF_HUMANA_2))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización: fidelidad frente a la fuente y lectura fácil ─────────────
PROF_PREP = r'''import os, re, json, unicodedata, urllib.request
import pandas as pd

if not os.path.exists("fichas.csv"):
    urllib.request.urlretrieve("''' + h.REPO_RAW + r'''/fichas.csv", "fichas.csv")
df = pd.read_csv("fichas.csv")
pgu = df[df["id"] == 130457].iloc[0]
# Trabajamos con la introducción de la ficha (lo que va antes de la primera sección "## ").
fuente = pgu["texto"].split("\n## ")[0].strip()

STOP = {"de", "la", "el", "los", "las", "y", "en", "a", "con", "por", "para", "que", "se", "su",
        "sus", "un", "una", "del", "al", "o", "tu", "si", "mas", "es", "como", "desde", "hasta"}

def tokens_contenido(texto):
    """Palabras con contenido, en minúsculas y sin tildes (como en R3-01)."""
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [w for w in re.findall(r"[a-z]+", t) if w not in STOP and len(w) >= 3]

# Dos resúmenes de la ficha de la PGU: uno fiel y uno con datos inventados.
RESUMEN_FIEL = ("Con la Reforma de Pensiones, la Pensión Garantizada Universal (PGU) subió. "
    "Desde febrero de 2026, si tienes 82 años o más recibes hasta $250.275, y si tienes entre 65 y 81 años, "
    "hasta $231.732. Desde septiembre de 2026, las personas de 75 años o más podrán recibir el monto máximo. "
    "Consulta con tu RUN cuándo aumentará tu PGU.")
RESUMEN_INFIEL = ("La PGU es un bono de $300.000 que se paga a todas las personas desde los 60 años. "
    "Para recibirla debes postular en tu municipalidad con tu Registro Social de Hogares.")
print(pgu["titulo"], "· introducción:", len(fuente.split()), "palabras")'''

PROF_LLM_MD = '''La celda siguiente define `preguntar_llm()` (la misma de la lección). Sin clave, devuelve el
respaldo y todo funciona igual.'''

PROF_EJ = [
 ("## 1. Partir un texto en oraciones",
  "Para medir legibilidad y fidelidad necesitamos **oraciones**. Escribe `oraciones(texto)`: "
  "parte después de `.`, `!` o `?` seguidos de espacio, y también en cada salto de línea; "
  "descarta los trozos vacíos. Pista: `re.split(r\"(?<=[.!?])\\s+|\\n+\", texto)`.",
  "Escribe `oraciones`",
  r'''def oraciones(texto):
    return [o.strip() for o in re.split(r"(?<=[.!?])\s+|\n+", texto) if o.strip()]

print(len(oraciones(fuente)), "oraciones en la introducción de la ficha")
oraciones(fuente)[:3]''',
  r'''def oraciones(texto):
    # TODO: re.split con el patrón de la pista; quita espacios (strip) y descarta vacíos
    ...

print(oraciones(fuente))''',
  r'''assert oraciones("Hola. ¿Cómo estás? Bien!\nFin") == ["Hola.", "¿Cómo estás?", "Bien!", "Fin"]
assert oraciones("Monto: $250.275 al mes.") == ["Monto: $250.275 al mes."], "el punto de miles no corta"
assert len(oraciones(fuente)) == 9''',
  r"return [o.strip() for o in re.split(r'(?<=[.!?])\s+|\n+', texto) if o.strip()]"),

 ("## 2. Cobertura: ¿de dónde salen las palabras del resumen?",
  "Una medida simple de **fidelidad**: qué fracción de las palabras con contenido del resumen "
  "aparece también en la fuente. No prueba que el resumen sea correcto (puede reordenar "
  "palabras y cambiar el sentido), pero un valor bajo es una **alerta**.",
  "Escribe `cobertura`",
  r'''def cobertura(resumen, fuente):
    del_resumen = tokens_contenido(resumen)
    de_la_fuente = set(tokens_contenido(fuente))
    if not del_resumen:
        return 0.0
    return sum(w in de_la_fuente for w in del_resumen) / len(del_resumen)

print(f"fiel: {cobertura(RESUMEN_FIEL, fuente):.0%} | infiel: {cobertura(RESUMEN_INFIEL, fuente):.0%}")''',
  r'''def cobertura(resumen, fuente):
    del_resumen = tokens_contenido(resumen)
    de_la_fuente = set(tokens_contenido(fuente))
    if not del_resumen:
        return 0.0
    # TODO: fracción de palabras de del_resumen que están en de_la_fuente
    ...

print(cobertura(RESUMEN_FIEL, fuente), cobertura(RESUMEN_INFIEL, fuente))''',
  r'''assert cobertura(fuente, fuente) == 1.0
assert 0 <= cobertura(RESUMEN_INFIEL, fuente) < cobertura(RESUMEN_FIEL, fuente) <= 1
assert cobertura("", fuente) == 0.0''',
  "return sum(w in de_la_fuente for w in del_resumen) / len(del_resumen)."),

 ("## 3. Números que no están en la fuente",
  "La alerta más fuerte: un **número** (monto, edad, año) del resumen que no aparece en la "
  "fuente. Escribe `numeros_no_respaldados(resumen, fuente)`: extrae los números de ambos "
  "textos (con `numeros(texto)`, ya escrita, que quita los puntos de miles) y devuelve, "
  "ordenados, los del resumen que no están en la fuente.",
  "Escribe `numeros_no_respaldados`",
  r'''def numeros(texto):
    return {n.replace(".", "") for n in re.findall(r"\d+(?:\.\d{3})*", texto)}

def numeros_no_respaldados(resumen, fuente):
    return sorted(numeros(resumen) - numeros(fuente))

print("fiel:  ", numeros_no_respaldados(RESUMEN_FIEL, fuente))
print("infiel:", numeros_no_respaldados(RESUMEN_INFIEL, fuente))''',
  r'''def numeros(texto):
    return {n.replace(".", "") for n in re.findall(r"\d+(?:\.\d{3})*", texto)}

def numeros_no_respaldados(resumen, fuente):
    # TODO: números del resumen que NO están en la fuente, ordenados (resta de conjuntos + sorted)
    ...

print("fiel:  ", numeros_no_respaldados(RESUMEN_FIEL, fuente))
print("infiel:", numeros_no_respaldados(RESUMEN_INFIEL, fuente))''',
  r'''assert numeros_no_respaldados(RESUMEN_FIEL, fuente) == []
assert numeros_no_respaldados(RESUMEN_INFIEL, fuente) == ["300000", "60"]
assert numeros_no_respaldados("Hasta $250.275 desde los 82", fuente) == []''',
  "return sorted(numeros(resumen) - numeros(fuente))."),

 ("## 4. Lectura fácil: medir antes de reescribir",
  "**Lectura fácil** es una forma de redactar para que todas las personas entiendan: frases "
  "cortas, una idea por oración, palabras comunes, siglas explicadas. Un indicador simple es el "
  "promedio de **palabras por oración**. Escríbelo y compáralo entre la ficha y una versión en "
  "lectura fácil (abajo verás el prompt que la pide al LLM).",
  "Escribe `palabras_por_oracion`",
  r'''def palabras_por_oracion(texto):
    ors = oraciones(texto)
    return len(texto.split()) / len(ors) if ors else 0.0

print(f"introducción original: {palabras_por_oracion(fuente):.1f} palabras por oración")''',
  r'''def palabras_por_oracion(texto):
    ors = oraciones(texto)
    # TODO: total de palabras (texto.split()) dividido por el número de oraciones; 0.0 si no hay oraciones
    ...

print("introducción original:", palabras_por_oracion(fuente))''',
  r'''assert abs(palabras_por_oracion(fuente) - len(fuente.split()) / 9) < 1e-9
assert palabras_por_oracion("Uno dos. Tres cuatro cinco seis.") == 3.0
assert palabras_por_oracion("") == 0.0''',
  "return len(texto.split()) / len(ors) if ors else 0.0."),
]

PROF_LECTURA = r'''RESPALDO_LECTURA_FACIL = """La Pensión Garantizada Universal (PGU) subió.
El cambio es por la Reforma de Pensiones.
Desde febrero de 2026, el monto depende de tu edad.
Si tienes 82 años o más, recibes hasta $250.275.
Si tienes entre 65 y 81 años, recibes hasta $231.732.
Desde septiembre de 2026, desde los 75 años recibes hasta $250.275.
Consulta con tu RUN cuándo sube tu PGU."""

def prompt_lectura_facil(texto):
    return ("Reescribe este texto en lectura fácil para personas mayores.\n"
            "Reglas: una idea por oración; máximo 12 palabras por oración; palabras comunes; "
            "explica o evita las siglas; no agregues datos que no estén en el texto; "
            "conserva todos los montos, edades y fechas.\n\nTEXTO:\n" + texto)

PATRON_RUT = r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b"      # guardrail de R3-02
if re.search(PATRON_RUT, fuente) is None:
    facil = preguntar_llm(prompt_lectura_facil(fuente), respaldo=RESPALDO_LECTURA_FACIL)
else:
    facil = ""
    print("⚠️ La fuente trae un RUT: no se envía al LLM.")
print(facil, "\n")
print(f"palabras por oración → original: {palabras_por_oracion(fuente):.1f} | lectura fácil: {palabras_por_oracion(facil):.1f}")
print("números no respaldados:", numeros_no_respaldados(facil, fuente),
      f"| cobertura: {cobertura(facil, fuente):.0%}")'''

PROF_HEADER = '''# R3-02 · IA generativa y LLMs — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional. Dos preguntas que todo servicio debería hacerse antes de publicar un texto escrito
por un LLM: **¿es fiel a la fuente?** y **¿se entiende?** Construirás medidas simples de
**fidelidad** (cobertura de palabras, números no respaldados) y de **legibilidad** (palabras
por oración), y las aplicarás a una reescritura de la introducción de la ficha de la PGU en **lectura fácil**.
Todo corre sin clave: las funciones que escribes se prueban sobre textos fijos.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP), h.md(PROF_LLM_MD), h.code(h.GET_LLM_SNIPPET)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("## 5. Todo junto: pedir lectura fácil y auditarla\n\n"
                      "El guardrail revisa la fuente, el LLM reescribe (o se usa el respaldo) y tus tres "
                      "medidas auditan el resultado. Si hay números no respaldados o la cobertura cae, "
                      "el texto vuelve a revisión humana antes de publicarse."))
    cells.append(h.code(PROF_LECTURA))
    cells.append(h.md('''## Para llevar

- Las medidas automáticas son **alertas**, no certificados: un resumen con 100 % de cobertura puede invertir el sentido de una frase.
- Los **números** son lo primero que se verifica: son lo que más daño hace si está mal.
- Lectura fácil se puede **medir** (palabras por oración) y **pedir** con reglas explícitas en el prompt — y luego se audita igual.

---

*Fin de la profundización de R3-02.*'''))
    nb.cells = cells
    return nb


README = '''# R3-02 · IA generativa y LLMs

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-02-ia-generativa-y-llms/leccion.ipynb)

Un **LLM** (Gemini, detrás de una sola función `preguntar_llm()`) sobre las fichas de
ChileAtiende (`fichas.csv`): prompts para **resumir en lenguaje claro** la ficha de la PGU,
**extraer requisitos como JSON** del Bono de Invierno con un parser y un validador propios,
**few-shot** para clasificar el tema, **temperatura y alucinación** (verificar los montos contra
la fuente), **verificación humana** y un **guardrail** que bloquea RUT. Funciona **sin clave y sin
red** (respuestas de respaldo); con una clave gratuita de aistudio.google.com guardada en los
Secretos de Colab, habla con el modelo en vivo. La profundización mide **fidelidad** y
**legibilidad** de un resumen y lo reescribe en **lectura fácil**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: cobertura, números no respaldados y lectura fácil.

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
