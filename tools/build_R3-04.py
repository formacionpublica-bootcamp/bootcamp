"""build_R3-04.py — módulo R3-04 (Agentes con herramientas y supervisión humana).

Rama R3 (IA Aplicada). Rearmado 2026 (reemplaza la versión legacy, cuya fuente de
datos se retiró): un agente cuyas herramientas son funciones de Python que consultan
datos REALES de las otras dos ramas — calidad del aire SINCA (aire_diario.csv,
ancla de R2) y matrícula escolar MINEDUC (matricula.csv, ancla de R1) — y una acción
con efecto (enviar una alerta, simulada). Cierra el arco de las 3 ramas.

Conserva el arco del módulo (decidir → actuar → responder, traza auditable, guardas)
y lo lleva a un agente de verdad: el LLM PROPONE el siguiente paso en JSON; si no hay
clave/red o la propuesta es inválida, decide un planificador de REGLAS determinista;
cada paso queda en una TRAZA; hay LÍMITE de pasos y APROBACIÓN HUMANA antes de toda
acción con efecto (por defecto, se niega). Ningún assert depende del LLM en vivo.
Profundiza = transferencia a fichas.csv (herramienta buscar_ficha) + guardas.

Uso:  /opt/anaconda3/bin/python tools/build_R3-04.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R3-ia-aplicada", "R3-04-agentes")

RAW = h.REPO_RAW

# ─────────────────────────────────────────────────────────────────────────────
# Piezas compartidas (lección y profundiza)
# ─────────────────────────────────────────────────────────────────────────────
CARGA = f'''import os, re, json, unicodedata, urllib.request
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "estaciones.csv", "matricula.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

aire = pd.read_csv("aire_diario.csv", parse_dates=["fecha"])   # PM2.5 diario SINCA (rama R2)
estaciones = pd.read_csv("estaciones.csv")                      # dónde está cada estación
matricula = pd.read_csv("matricula.csv")                        # matrícula 2025 MINEDUC (rama R1)

def normalizar(texto):
    """minúsculas y sin tildes, para comparar textos escritos por personas."""
    t = unicodedata.normalize("NFKD", str(texto).lower())
    return "".join(c for c in t if not unicodedata.combining(c))'''

HERR_BASE = '''NORMA_PM25_DIARIA = 50   # µg/m³: valor de la norma primaria diaria de PM2.5 en Chile (DS 12/2011 MMA)

def pm25_promedio(estacion, anio):
    """PM2.5 promedio de un año (µg/m³) en una estación SINCA."""
    d = aire[(aire["estacion"] == estacion) & (aire["fecha"].dt.year == anio)]["pm25"].dropna()
    if d.empty:
        raise ValueError(f"no hay datos de PM2.5 para «{estacion}» en {anio}")
    return {"estacion": estacion, "anio": anio, "pm25_promedio": round(float(d.mean()), 1),
            "dias_con_dato": int(d.size)}

def matricula_comuna(comuna):
    """Establecimientos y estudiantes matriculados (2025) en una comuna."""
    d = matricula[matricula["comuna"].map(normalizar) == normalizar(comuna)]
    if d.empty:
        raise ValueError(f"no conozco la comuna «{comuna}»")
    return {"comuna": d["comuna"].iloc[0], "establecimientos": int(len(d)),
            "estudiantes": int(d["mat_total"].sum())}

BANDEJA_SALIDA = []   # simula el correo institucional: aquí «llegan» las alertas enviadas

def enviar_alerta(destinatario, mensaje):
    """ACCIÓN CON EFECTO: envía (simulado) una alerta a un destinatario."""
    BANDEJA_SALIDA.append({"para": destinatario, "mensaje": mensaje})
    return {"enviado_a": destinatario}'''

DIAS_SOL = '''def dias_sobre_norma(estacion, anio, umbral=NORMA_PM25_DIARIA):
    """Días de un año con PM2.5 sobre el umbral (por defecto, 50 µg/m³) en una estación."""
    d = aire[(aire["estacion"] == estacion) & (aire["fecha"].dt.year == anio)]["pm25"].dropna()
    if d.empty:
        raise ValueError(f"no hay datos de PM2.5 para «{estacion}» en {anio}")
    return {"estacion": estacion, "anio": anio, "dias_sobre_norma": int((d > umbral).sum()),
            "dias_con_dato": int(d.size)}'''

REGISTRO = '''# El «menú» del agente: qué herramientas existen, qué argumentos piden y si tienen EFECTO
# (cambian algo en el mundo). El agente no puede usar nada que no esté aquí.
HERRAMIENTAS = {
    "pm25_promedio":    {"funcion": pm25_promedio,    "args": ["estacion", "anio"], "efecto": False,
                         "descripcion": "PM2.5 promedio anual (µg/m³) de una estación SINCA, años 2020-2025."},
    "dias_sobre_norma": {"funcion": dias_sobre_norma, "args": ["estacion", "anio"], "efecto": False,
                         "descripcion": "Días del año con PM2.5 sobre 50 µg/m³ en una estación, años 2020-2025."},
    "matricula_comuna": {"funcion": matricula_comuna, "args": ["comuna"], "efecto": False,
                         "descripcion": "Establecimientos y estudiantes matriculados en 2025 en una comuna."},
    "enviar_alerta":    {"funcion": enviar_alerta,    "args": ["destinatario", "mensaje"], "efecto": True,
                         "descripcion": "ENVÍA una alerta. Acción con efecto: requiere aprobación humana."},
}
for nombre, d in HERRAMIENTAS.items():
    print(f"{'⚠️ ' if d['efecto'] else '   '}{nombre}({', '.join(d['args'])})")'''

EXTRAER = '''# Del texto de la petición a los argumentos: estación, año y comuna.
ALIAS_ESTACION = {}
comunas_con_estacion = estaciones["comuna"].map(normalizar).value_counts()
for est, com in zip(estaciones["estacion"], estaciones["comuna"]):
    ALIAS_ESTACION[normalizar(re.sub(r"\\s*\\(.*\\)", "", est))] = est   # «El Bosque (Acreditada)» → «el bosque»
    if comunas_con_estacion[normalizar(com)] == 1:                      # la comuna sirve de alias si no es ambigua
        ALIAS_ESTACION.setdefault(normalizar(com), est)

def extraer_estacion(texto):
    t = normalizar(texto)
    for alias in sorted(ALIAS_ESTACION, key=len, reverse=True):
        if re.search(rf"\\b{re.escape(alias)}\\b", t):
            return ALIAS_ESTACION[alias]
    return None

def extraer_anio(texto):
    m = re.search(r"\\b(20\\d\\d)\\b", texto)
    return int(m.group(1)) if m else None

COMUNAS = sorted(matricula["comuna"].unique(), key=len, reverse=True)
def extraer_comuna(texto):
    t = normalizar(texto)
    for c in COMUNAS:
        if re.search(rf"\\b{re.escape(normalizar(c))}\\b", t):
            return c
    return None

print(extraer_estacion("calidad del aire en Rancagua"), "|", extraer_anio("en 2023"), "|",
      extraer_comuna("estudiantes de Ñuñoa"), "|", extraer_estacion("aire en Temuco"))'''

PLAN_REGLAS_CABEZA = '''def planificar_reglas(peticion, traza):
    """Planificador de RESPALDO, determinista: decide el siguiente paso con reglas simples."""
    t = normalizar(peticion)
    hechos = [p for p in traza if p["estado"] == "ok"]
    if any(p["estado"] in ("error", "bloqueado_por_guarda") for p in traza):   # algo falló: no insistir
        return {"herramienta": "fin", "args": {}}
    if hechos:                                               # ya tenemos el dato
        quiere_avisar = any(w in t for w in ["avisa", "alerta", "notifica"])
        ya_propuesta = any(p["herramienta"] == "enviar_alerta" for p in traza)
        if quiere_avisar and not ya_propuesta:
            return {"herramienta": "enviar_alerta",
                    "args": {"destinatario": "SEREMI de Medio Ambiente",
                             "mensaje": f"Resultado de la consulta: {hechos[-1]['resultado']}"}}
        return {"herramienta": "fin", "args": {}}
    # Primer paso: ¿qué dato hay que consultar?'''

PLAN_REGLAS_SOL = PLAN_REGLAS_CABEZA + '''
    if "norma" in t or "episodio" in t:
        return {"herramienta": "dias_sobre_norma",
                "args": {"estacion": extraer_estacion(peticion), "anio": extraer_anio(peticion)}}
    if "pm2" in t or "aire" in t or "contaminacion" in t:
        return {"herramienta": "pm25_promedio",
                "args": {"estacion": extraer_estacion(peticion), "anio": extraer_anio(peticion)}}
    if "matricula" in t or "estudiantes" in t or "colegios" in t:
        return {"herramienta": "matricula_comuna", "args": {"comuna": extraer_comuna(peticion)}}
    return {"herramienta": "fin", "args": {}}'''

INTERPRETAR_SOL = '''def interpretar_plan(texto):
    """Convierte la respuesta del LLM en un plan VÁLIDO, o None si no se puede confiar en ella."""
    m = re.search(r"\\{.*\\}", texto or "", flags=re.S)        # el JSON puede venir entre ```
    if not m:
        return None
    try:
        plan = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    herramienta = plan.get("herramienta")
    if herramienta == "fin":
        return {"herramienta": "fin", "args": {}}
    if herramienta not in HERRAMIENTAS:
        return None
    args = plan.get("args")
    if not isinstance(args, dict) or set(args) != set(HERRAMIENTAS[herramienta]["args"]):
        return None
    return {"herramienta": herramienta, "args": args}'''

EJECUTAR_SOL = '''def ejecutar_paso(plan, traza):
    """Ejecuta UNA herramienta y deja el registro en la traza (sin caerse si falla)."""
    nombre, args = plan["herramienta"], plan["args"]
    registro = {"paso": len(traza) + 1, "herramienta": nombre, "args": args,
                "origen": plan.get("origen", "manual")}
    try:
        registro["resultado"] = HERRAMIENTAS[nombre]["funcion"](**args)
        registro["estado"] = "ok"
    except Exception as e:
        registro["resultado"] = f"{type(e).__name__}: {e}"
        registro["estado"] = "error"
    traza.append(registro)
    return registro'''

SUPERVISADO_SOL = '''def ejecutar_supervisado(plan, traza, aprobador=None):
    """Si la herramienta tiene EFECTO, solo se ejecuta con aprobación humana explícita."""
    if HERRAMIENTAS[plan["herramienta"]]["efecto"]:
        if aprobador is None or not aprobador(plan):         # por defecto: NO
            registro = {"paso": len(traza) + 1, "herramienta": plan["herramienta"],
                        "args": plan["args"], "origen": plan.get("origen", "manual"),
                        "resultado": "acción NO ejecutada: sin aprobación humana",
                        "estado": "rechazado"}
            traza.append(registro)
            return registro
        registro = ejecutar_paso(plan, traza)
        registro["aprobado_por_humano"] = True
        return registro
    return ejecutar_paso(plan, traza)'''

AGENTE_SOL = '''def agente(peticion, planificador=None, aprobador=None, max_pasos=4):
    planificador = planificador or planificar
    traza, estado = [], "limite_de_pasos"
    for _ in range(max_pasos):
        plan = planificador(peticion, traza)
        if plan["herramienta"] == "fin":
            estado = "terminado"
            break
        ejecutar_supervisado(plan, traza, aprobador)
    return {"estado": estado, "traza": traza, "respuesta": redactar_respuesta(peticion, traza, estado)}'''

# ─────────────────────────────────────────────────────────────────────────────
# LECCIÓN
# ─────────────────────────────────────────────────────────────────────────────
SETUP = "# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────\n" + CARGA + '''

print("aire:", aire.shape, "|", aire["estacion"].nunique(), "estaciones,",
      aire["fecha"].min().date(), "a", aire["fecha"].max().date())
print("matrícula:", matricula.shape, "|", matricula["comuna"].nunique(), "comunas")'''

LLM_MD = '''### El LLM detrás de una sola función

La misma `preguntar_llm(prompt, respaldo=...)` de R3-02 y R3-03. Sin `GEMINI_API_KEY` devuelve el
`respaldo` y el agente usa su **planificador de reglas**: todo el notebook funciona igual y ningún
chequeo depende de lo que conteste el modelo.

> Si en tu entorno falta el SDK de Google, instálalo con `!pip install -q google-genai`.'''

LLM_CELL = h.GET_LLM_SNIPPET + '''
print("Modelo:", MODELO, "| modo:", "EN VIVO" if _clave_gemini() else "RESPALDO (planificador de reglas)")'''

INTRO = '''## ¿Qué es un agente?

Un programa normal sigue una receta fija. Un **agente** recibe una petición en lenguaje natural y
**decide qué hacer**, paso a paso:

1. **Planificar:** ¿qué herramienta uso ahora, y con qué argumentos? (aquí opina el LLM)
2. **Actuar:** ejecutar esa herramienta — una **función de Python** que tú escribiste.
3. **Observar:** mirar el resultado y volver a 1… hasta decidir que terminó.

Este módulo **cierra el arco de las tres ramas**: las herramientas consultan la **matrícula escolar**
(el dato ancla de R1) y la **calidad del aire** (el de R2); el LLM (R3) solo **orquesta**. Las
cifras nunca las inventa el modelo: salen de pandas.

### Las cuatro reglas de un agente público

| Regla | Por qué | Dónde la construyes |
|---|---|---|
| El LLM **propone**, el código **valida** | Un LLM puede pedir una herramienta que no existe o inventar argumentos | Ejercicio 3 |
| **Traza** de cada paso | Poder responder «¿por qué el sistema hizo esto?» | Ejercicio 4 |
| **Aprobación humana** antes de toda acción con efecto | Un agente no envía, borra ni paga nada por su cuenta | Ejercicio 5 |
| **Límite de pasos** | Evita bucles infinitos (y cuentas infinitas) | Ejercicio 6 |

> Siempre hay un **planificador de respaldo por reglas**, determinista: el agente funciona sin red
> y se puede verificar. Es también lo que usa cuando el LLM responde algo inválido.'''

TOOLS_MD = '''## Las herramientas (y el «menú» del agente)

Tres herramientas de **consulta** ya están listas — `pm25_promedio`, `matricula_comuna` — y una
**acción con efecto**: `enviar_alerta`, que simula el envío de un correo (lo deja en
`BANDEJA_SALIDA`). Falta una: la vas a escribir tú.'''

EJ = [
 ("## 1. Escribe una herramienta: días sobre la norma",
  "Una herramienta es una función normal de pandas con tres virtudes: hace **una** cosa, recibe "
  "argumentos **simples** (texto, números) y **avisa con un error claro** si no puede. Escribe "
  "`dias_sobre_norma(estacion, anio)`: cuántos días del año el PM2.5 superó 50 µg/m³ "
  "(el valor de la norma diaria) y con cuántos días con dato se calculó.\n\n"
  "> Ojo con la interpretación: legalmente la norma diaria se evalúa con el **percentil 98** del año, "
  "así que «días sobre 50» es un indicador de episodios, no un dictamen de incumplimiento.",
  "Escribe `dias_sobre_norma`",
  DIAS_SOL + '''

dias_sobre_norma("Cerro Navia", 2024)''',
  '''def dias_sobre_norma(estacion, anio, umbral=NORMA_PM25_DIARIA):
    """Días de un año con PM2.5 sobre el umbral (por defecto, 50 µg/m³) en una estación."""
    d = aire[(aire["estacion"] == estacion) & (aire["fecha"].dt.year == anio)]["pm25"].dropna()
    if d.empty:
        raise ValueError(f"no hay datos de PM2.5 para «{estacion}» en {anio}")
    # TODO: devuelve un diccionario con estacion, anio,
    #       "dias_sobre_norma" (cuántos valores de d superan el umbral, como int) y
    #       "dias_con_dato" (cuántos valores tiene d, como int)
    return ...

# Pruébala:  dias_sobre_norma("Cerro Navia", 2024)''',
  '''r = dias_sobre_norma("Cerro Navia", 2024)
d = aire[(aire["estacion"] == "Cerro Navia") & (aire["fecha"].dt.year == 2024)]["pm25"].dropna()
assert isinstance(r, dict), "la herramienta debe devolver un diccionario"
assert r["dias_sobre_norma"] == int((d > 50).sum()), "cuenta los días con pm25 > umbral"
assert r["dias_con_dato"] == int(d.size), "dias_con_dato = cantidad de días con medición"
try:
    dias_sobre_norma("Estación Inventada", 2024)
    raise AssertionError("con una estación inexistente debe lanzar ValueError")
except ValueError:
    pass''',
  'return {"estacion": estacion, "anio": anio, "dias_sobre_norma": int((d > umbral).sum()), "dias_con_dato": int(d.size)}.',
  None),
]

REG_MD = '''### El menú: `HERRAMIENTAS`

El agente solo puede usar lo que está en este diccionario. Cada entrada declara sus argumentos y
si tiene **efecto** (⚠️). Ese simple `True/False` es el que, en el ejercicio 5, activa la
aprobación humana. **Permisos mínimos:** si una herramienta no está en el menú, el agente no la tiene.'''

EXTRAER_MD = '''### Entender la petición

Para el planificador de reglas necesitamos sacar del texto la **estación**, el **año** y la
**comuna**. Fíjate en el último ejemplo: «Temuco» tiene **dos** estaciones (Las Encinas y Nielol),
así que no se usa como alias — es ambiguo, y es mejor no adivinar.'''

EJ2 = [
 ("## 2. El planificador de respaldo (reglas)",
  "El planificador recibe la petición y la **traza** (lo que ya se hizo) y devuelve el **siguiente "
  "paso**: `{\"herramienta\": ..., \"args\": {...}}`, o `{\"herramienta\": \"fin\", ...}` si ya terminó.\n\n"
  "La parte de «¿ya tenemos el dato? → ¿piden avisar?» está escrita. Completa la decisión del "
  "**primer paso**, en este orden:\n\n"
  "1. Si menciona **norma** o **episodio** → `dias_sobre_norma` (estación y año).\n"
  "2. Si menciona **pm2**, **aire** o **contaminacion** → `pm25_promedio` (estación y año).\n"
  "3. Si menciona **matricula**, **estudiantes** o **colegios** → `matricula_comuna` (comuna).\n"
  "4. Si nada calza → `fin` (mejor no hacer nada que inventar).\n\n"
  "`t` ya viene normalizado (minúsculas, sin tildes).",
  "Completa `planificar_reglas`",
  PLAN_REGLAS_SOL + '''

for p in ["¿Cuántos días sobre la norma tuvo Cerro Navia en 2024?",
          "¿Cuál fue el PM2.5 promedio de Rancagua en 2023?",
          "¿Cuántos estudiantes hay en Temuco?", "¿Cómo está el tráfico hoy?"]:
    print(planificar_reglas(p, []), "←", p)''',
  PLAN_REGLAS_CABEZA + '''
    # TODO 1: si "norma" o "episodio" está en t → dias_sobre_norma con
    #         args {"estacion": extraer_estacion(peticion), "anio": extraer_anio(peticion)}
    # TODO 2: si "pm2", "aire" o "contaminacion" está en t → pm25_promedio (mismos args)
    # TODO 3: si "matricula", "estudiantes" o "colegios" está en t → matricula_comuna
    #         con args {"comuna": extraer_comuna(peticion)}
    ...
    return {"herramienta": "fin", "args": {}}

# Pruébala:  planificar_reglas("¿Cuántos días sobre la norma tuvo Cerro Navia en 2024?", [])''',
  '''casos = {
    "¿Cuántos días sobre la norma tuvo Cerro Navia en 2024?":
        {"herramienta": "dias_sobre_norma", "args": {"estacion": "Cerro Navia", "anio": 2024}},
    "¿Cuál fue el PM2.5 promedio de Rancagua en 2023?":
        {"herramienta": "pm25_promedio", "args": {"estacion": "Rancagua I", "anio": 2023}},
    "¿Cuántos estudiantes hay en Temuco?":
        {"herramienta": "matricula_comuna", "args": {"comuna": "Temuco"}},
    "¿Cómo está el tráfico hoy?": {"herramienta": "fin", "args": {}},
}
for peticion, esperado in casos.items():
    obtenido = planificar_reglas(peticion, [])
    assert obtenido == esperado, f"«{peticion}» → esperaba {esperado}, obtuve {obtenido}"
ya = [{"herramienta": "dias_sobre_norma", "estado": "ok", "resultado": {"dias_sobre_norma": 56}}]
assert planificar_reglas("días sobre la norma en Cerro Navia 2024 y avisa a la SEREMI", ya)["herramienta"] == "enviar_alerta"
assert planificar_reglas("días sobre la norma en Cerro Navia 2024", ya)["herramienta"] == "fin"''',
  'if "norma" in t or "episodio" in t: return {"herramienta": "dias_sobre_norma", "args": {...}}; igual para las otras dos reglas.',
  None),

 ("## 3. El LLM propone, el código valida",
  "Cuando hay clave, el planificador le muestra al LLM el menú y le pide el siguiente paso **en "
  "JSON**. Pero lo que vuelve es **texto**: puede venir entre ```` ``` ````, pedir una herramienta "
  "que no existe («borrar_base»), olvidar un argumento… o no ser JSON. `interpretar_plan` es la "
  "aduana: devuelve un plan **válido** o `None` (y entonces decide el planificador de reglas).\n\n"
  "La extracción del JSON ya está; completa la **validación**: la herramienta debe estar en "
  "`HERRAMIENTAS` y los `args` deben ser un diccionario con **exactamente** los argumentos que "
  "declara el menú.",
  "Completa la validación de `interpretar_plan`",
  INTERPRETAR_SOL,
  '''def interpretar_plan(texto):
    """Convierte la respuesta del LLM en un plan VÁLIDO, o None si no se puede confiar en ella."""
    m = re.search(r"\\{.*\\}", texto or "", flags=re.S)        # el JSON puede venir entre ```
    if not m:
        return None
    try:
        plan = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    herramienta = plan.get("herramienta")
    if herramienta == "fin":
        return {"herramienta": "fin", "args": {}}
    # TODO: si la herramienta NO está en HERRAMIENTAS → return None
    ...
    args = plan.get("args")
    # TODO: si args no es dict, o set(args) != set(HERRAMIENTAS[herramienta]["args"]) → return None
    ...
    return {"herramienta": herramienta, "args": args}''',
  '''ok = interpretar_plan('```json\\n{"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}\\n```')
assert ok == {"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}, "un JSON válido entre ``` debe aceptarse"
assert interpretar_plan('{"herramienta": "borrar_base_de_datos", "args": {}}') is None, "herramienta inexistente → None"
assert interpretar_plan('{"herramienta": "pm25_promedio", "args": {"estacion": "Nielol"}}') is None, "falta un argumento → None"
assert interpretar_plan('{"herramienta": "matricula_comuna", "args": {"comuna": "Arica", "borrar": true}}') is None, "argumento de más → None"
assert interpretar_plan("Claro, con gusto te ayudo.") is None, "texto sin JSON → None"
assert interpretar_plan('{"herramienta": "fin"}') == {"herramienta": "fin", "args": {}}''',
  'if herramienta not in HERRAMIENTAS: return None  ·  if not isinstance(args, dict) or set(args) != set(HERRAMIENTAS[herramienta]["args"]): return None.',
  None),
]

PLANIFICAR_MD = '''### El planificador principal: LLM con respaldo

Esta función arma el prompt (menú + estaciones válidas + pasos ya hechos), se lo envía al LLM,
pasa la respuesta por tu `interpretar_plan` y, si no sirve —o no hay clave—, usa
`planificar_reglas`. Cada plan queda marcado con su **origen** (`llm` o `reglas`) para la traza.'''

PLANIFICAR_CELL = '''def describir_herramientas():
    return "\\n".join(f"- {n}({', '.join(d['args'])}): {d['descripcion']}" for n, d in HERRAMIENTAS.items())

def planificar(peticion, traza):
    prompt = ("Eres el planificador de un agente de datos públicos de Chile.\\n"
              f"Herramientas disponibles:\\n{describir_herramientas()}\\n"
              f"Estaciones válidas: {', '.join(estaciones['estacion'])}.\\n\\n"
              f"Petición: {peticion}\\n"
              f"Pasos ya realizados: {json.dumps(traza, ensure_ascii=False, default=str)}\\n\\n"
              'Decide SOLO el siguiente paso. Responde únicamente un JSON: '
              '{"herramienta": "...", "args": {...}}, o {"herramienta": "fin", "args": {}} si ya se puede responder.')
    plan = interpretar_plan(preguntar_llm(prompt, respaldo=""))
    if plan is None:
        plan = dict(planificar_reglas(peticion, traza), origen="reglas")
    else:
        plan["origen"] = "llm"
    return plan

print(planificar("¿Cuántos días sobre la norma tuvo Cerro Navia en 2024?", []))'''

EJ3 = [
 ("## 4. Ejecutar con traza",
  "Cada paso que da el agente queda **registrado**: número, herramienta, argumentos, quién lo "
  "propuso, resultado y estado. Si la herramienta falla (estación inexistente, año sin datos), el "
  "agente **no se cae**: registra el error y sigue. La traza es el **expediente** del agente.",
  "Completa `ejecutar_paso`",
  EJECUTAR_SOL + '''

traza_demo = []
ejecutar_paso({"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}, traza_demo)
ejecutar_paso({"herramienta": "pm25_promedio", "args": {"estacion": None, "anio": 2022}}, traza_demo)
pd.DataFrame(traza_demo)''',
  '''def ejecutar_paso(plan, traza):
    """Ejecuta UNA herramienta y deja el registro en la traza (sin caerse si falla)."""
    nombre, args = plan["herramienta"], plan["args"]
    registro = {"paso": len(traza) + 1, "herramienta": nombre, "args": args,
                "origen": plan.get("origen", "manual")}
    # TODO: dentro de un try, llama HERRAMIENTAS[nombre]["funcion"](**args), guarda el valor en
    #       registro["resultado"] y pon registro["estado"] = "ok".
    #       En el except Exception as e: registro["resultado"] = f"{type(e).__name__}: {e}"
    #       y registro["estado"] = "error".
    ...
    traza.append(registro)
    return registro''',
  '''t = []
r1 = ejecutar_paso({"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}, t)
assert r1["estado"] == "ok" and r1["resultado"] == pm25_promedio("Nielol", 2022), "un paso válido debe quedar 'ok' con su resultado"
r2 = ejecutar_paso({"herramienta": "pm25_promedio", "args": {"estacion": "No existe", "anio": 2022}}, t)
assert r2["estado"] == "error" and "ValueError" in r2["resultado"], "un paso que falla debe quedar 'error', sin caerse"
assert [p["paso"] for p in t] == [1, 2], "cada paso queda numerado en la traza"''',
  'try: registro["resultado"] = HERRAMIENTAS[nombre]["funcion"](**args); registro["estado"] = "ok"  /  except Exception as e: ... "error".',
  None),

 ("## 5. Supervisión humana: nada con efecto sin aprobación",
  "`enviar_alerta` **cambia el mundo**: llega un correo a la SEREMI. Ningún agente público debería "
  "hacer eso solo. Regla: si la herramienta tiene `efecto=True`, se ejecuta **solo si** un "
  "`aprobador` (una persona) dice que sí. Y si no hay aprobador, la respuesta es **no** "
  "(*denegar por defecto*). La negativa también queda en la traza.",
  "Completa `ejecutar_supervisado`",
  SUPERVISADO_SOL + '''

alerta = {"herramienta": "enviar_alerta", "args": {"destinatario": "SEREMI", "mensaje": "prueba"}}
print(ejecutar_supervisado(alerta, [], aprobador=None)["estado"], "| bandeja:", len(BANDEJA_SALIDA))''',
  '''def ejecutar_supervisado(plan, traza, aprobador=None):
    """Si la herramienta tiene EFECTO, solo se ejecuta con aprobación humana explícita."""
    if HERRAMIENTAS[plan["herramienta"]]["efecto"]:
        # TODO: si aprobador es None, o aprobador(plan) devuelve False:
        #       agrega a la traza un registro con estado "rechazado" (mismas claves que ejecutar_paso,
        #       resultado = "acción NO ejecutada: sin aprobación humana") y devuélvelo.
        ...
        registro = ejecutar_paso(plan, traza)
        registro["aprobado_por_humano"] = True
        return registro
    return ejecutar_paso(plan, traza)''',
  '''antes = len(BANDEJA_SALIDA)
alerta = {"herramienta": "enviar_alerta", "args": {"destinatario": "SEREMI", "mensaje": "prueba"}}
t = []
assert ejecutar_supervisado(alerta, t, aprobador=None)["estado"] == "rechazado", "sin aprobador: no se ejecuta"
assert ejecutar_supervisado(alerta, t, aprobador=lambda p: False)["estado"] == "rechazado", "si la persona dice no: no se ejecuta"
assert len(BANDEJA_SALIDA) == antes, "¡se envió una alerta sin aprobación!"
assert ejecutar_supervisado(alerta, t, aprobador=lambda p: True)["estado"] == "ok", "con aprobación sí se ejecuta"
assert len(BANDEJA_SALIDA) == antes + 1
assert ejecutar_supervisado({"herramienta": "matricula_comuna", "args": {"comuna": "Arica"}}, t)["estado"] == "ok", "las consultas no requieren aprobación"
assert len(t) == 4
BANDEJA_SALIDA.pop()   # limpiamos la alerta de prueba''',
  'if aprobador is None or not aprobador(plan): registro = {..., "estado": "rechazado"}; traza.append(registro); return registro.',
  None),
]

REDACTAR_MD = '''### La respuesta final

Con la traza lista, el LLM **redacta** la respuesta usando **solo** los resultados de las
herramientas (no puede agregar cifras). Sin clave, el respaldo es un resumen literal de la traza.'''

REDACTAR_CELL = '''def redactar_respuesta(peticion, traza, estado):
    resumen = " | ".join(f"{p['herramienta']} [{p['estado']}] → {p['resultado']}" for p in traza)
    respaldo = f"({estado}) {resumen}" if traza else "No tengo una herramienta para responder eso."
    if not any(p["estado"] == "ok" for p in traza):
        return respaldo
    prompt = ("Redacta en 2 o 3 frases, en español claro, la respuesta a esta petición usando SOLO "
              "estos resultados. No agregues cifras que no estén ahí. Si una acción fue rechazada, dilo.\\n"
              f"Petición: {peticion}\\nResultados: {resumen}")
    return preguntar_llm(prompt, respaldo=respaldo)'''

EJ6 = ("## 6. El bucle del agente, con límite de pasos",
  "Ahora todo junto: planificar → (supervisar) → ejecutar → volver a planificar… hasta que el "
  "planificador diga `fin` **o** se acabe el presupuesto de `max_pasos`. Ese límite existe porque "
  "los agentes con LLM a veces entran en bucles («consulto otra vez, por si acaso»), y cada vuelta "
  "cuesta tiempo y dinero. Si se alcanza el límite, el estado lo dice.",
  "Completa el bucle de `agente`",
  AGENTE_SOL + '''

r = agente("¿Cuántos días sobre la norma tuvo Cerro Navia en 2024? Avisa a la SEREMI.",
           planificador=planificar_reglas, aprobador=None)
print(r["estado"]); print(pd.DataFrame(r["traza"])[["paso", "herramienta", "estado", "resultado"]])''',
  '''def agente(peticion, planificador=None, aprobador=None, max_pasos=4):
    planificador = planificador or planificar
    traza, estado = [], "limite_de_pasos"
    for _ in range(max_pasos):
        plan = planificador(peticion, traza)
        # TODO: si plan["herramienta"] es "fin": estado = "terminado" y sal del bucle (break)
        ...
        # TODO: si no, ejecuta el plan con supervisión: ejecutar_supervisado(plan, traza, aprobador)
        ...
    return {"estado": estado, "traza": traza, "respuesta": redactar_respuesta(peticion, traza, estado)}''',
  '''antes = len(BANDEJA_SALIDA)
r = agente("¿Cuántos días sobre la norma tuvo Cerro Navia en 2024? Avisa a la SEREMI.",
           planificador=planificar_reglas, aprobador=lambda p: False)
assert r["estado"] == "terminado", "el agente debería terminar por sí mismo"
assert [p["herramienta"] for p in r["traza"]] == ["dias_sobre_norma", "enviar_alerta"]
assert [p["estado"] for p in r["traza"]] == ["ok", "rechazado"], "la alerta debe quedar rechazada (la persona dijo no)"
assert len(BANDEJA_SALIDA) == antes
def planificador_terco(peticion, traza):        # simula un LLM atrapado en un bucle
    return {"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}
r2 = agente("cualquier cosa", planificador=planificador_terco, max_pasos=3)
assert r2["estado"] == "limite_de_pasos" and len(r2["traza"]) == 3, "el límite de pasos debe cortar el bucle"''',
  'if plan["herramienta"] == "fin": estado = "terminado"; break  — y luego ejecutar_supervisado(plan, traza, aprobador).',
  None)

DEMO_MD = '''### El agente completo, en acción

Ahora con el planificador principal (`planificar`: LLM si hay clave, reglas si no). Fíjate en la
columna `origen` de la traza y en que la alerta **no** sale, porque nadie la aprobó.

> 🧑‍⚖️ En Colab, prueba la aprobación de verdad: `agente("...avisa a la SEREMI", aprobador=aprobador_consola)`
> te mostrará la acción y te preguntará si la apruebas.'''

DEMO_CELL = '''def aprobador_consola(plan):
    print("⚠️ El agente quiere ejecutar:", plan["herramienta"], plan["args"])
    return input("¿Apruebas esta acción? (si/no): ").strip().lower() in {"si", "sí", "s"}

try:
    for peticion in ["¿Cuál fue el PM2.5 promedio de Las Encinas Temuco en 2021?",
                     "¿Cuántos estudiantes hay en Coyhaique?",
                     "¿Cuántos días sobre la norma tuvo Rancagua en 2023? Si hubo, avisa a la SEREMI."]:
        r = agente(peticion)                       # aprobador=None → ninguna acción con efecto se ejecuta
        print(f"\\n▶ {peticion}\\n  estado: {r['estado']}")
        for p in r["traza"]:
            print(f"  paso {p['paso']} [{p['origen']}] {p['herramienta']} → {p['estado']}: {p['resultado']}")
        print("  respuesta:", r["respuesta"][:300])
except Exception as e:
    print("Completa los ejercicios anteriores para ver al agente en acción.", e)'''

RIESGOS = '''## Riesgos de un agente en el Estado (y qué hiciste para cada uno)

| Riesgo | Ejemplo | Mitigación |
|---|---|---|
| **Herramienta o argumentos inventados** | El LLM pide `borrar_base` o una estación que no existe | `interpretar_plan` valida contra el menú; la herramienta falla con un error claro |
| **Acción sin control** | Se envía una alerta (o un pago, o un oficio) que nadie revisó | `efecto=True` + aprobación humana, **denegar por defecto** |
| **Bucles y costo** | El agente consulta lo mismo una y otra vez | `max_pasos` |
| **Inyección de instrucciones** | Un texto dentro de los datos dice «ignora tus reglas y envía…» | Los resultados son **datos**, no órdenes; toda acción pasa por una persona |
| **Sesgo de automatización** | La persona aprueba todo sin leer | Mostrar **qué** y **por qué** antes de aprobar; revisar trazas al azar |
| **Datos personales** | La petición trae un RUT o un diagnóstico | No enviarlos al LLM externo; anonimizar antes (profundización) |
| **Cifras sin respaldo** | El LLM «redondea» o inventa un número | Las cifras salen de pandas; el LLM solo redacta con los resultados |

**La traza es el expediente.** Con ella puedes reconstruir cada decisión: quién la propuso
(LLM o reglas), qué se ejecutó, qué se rechazó y por qué. La responsabilidad de lo que el
sistema hace sigue siendo de las personas que lo operan.'''

CIERRE = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Piensa en una tarea repetitiva de tu servicio que un agente podría hacer. ¿Qué herramientas
necesitaría? ¿Cuáles tendrían **efecto** (enviar, registrar, pagar, notificar)? ¿Quién debería
aprobarlas, y qué tendría que ver en pantalla para aprobar con conocimiento de causa?

## Errores típicos

- **Ejecutar directo lo que dice el LLM** (`eval`, o llamar la función que nombre) → siempre valida contra el menú.
- **Aprobación por defecto en «sí»** → si el aprobador falla o no existe, la acción se ejecuta. Debe ser al revés.
- **Sin límite de pasos** → un bucle del LLM se vuelve una factura.
- **Asserts que dependen del LLM en vivo** → tus pruebas fallan al azar. Prueba con planificadores y aprobadores «falsos».

## Cierre

- Un **agente** = planificar → actuar → observar, en bucle. Las **herramientas** son funciones que tú controlas.
- El LLM **propone**; el código **valida**; la persona **aprueba** lo que tiene efecto.
- **Traza**, **límite de pasos** y **respaldo determinista** hacen que el agente sea auditable y verificable sin red.
- Cerraste el arco: datos de **R1** (matrícula) y **R2** (aire), orquestados con IA de **R3**.

> *En la profundización, el agente aprende a buscar en las fichas de ChileAtiende (tu RAG de
> R3-03 hecho herramienta) y suma guardas: argumentos válidos, calidad del dato y privacidad.
> Después viene el capstone.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R3-04", "Agentes: herramientas, trazas y supervisión humana", "R3", "IA Aplicada", "5",
                      ["Escribir **herramientas** (funciones de Python) que un agente puede usar.",
                       "Construir un **planificador de respaldo** por reglas y **validar** lo que propone el LLM.",
                       "Ejecutar paso a paso dejando una **traza** auditable.",
                       "Exigir **aprobación humana** antes de toda acción con efecto.",
                       "Cerrar el bucle del agente con un **límite de pasos**."],
                      "orquestar herramientas de datos con un LLM de forma segura, auditable y verificable sin red, manteniendo a una persona a cargo de las decisiones.",
                      "PM2.5 diario de 14 estaciones SINCA 2020–2025 (rama R2) y matrícula escolar 2025 MINEDUC (rama R1).",
                      n_checks=6),
        h.code(SETUP),
        h.md(LLM_MD),
        h.code(LLM_CELL),
        h.md(INTRO),
        h.md(TOOLS_MD),
        h.code(HERR_BASE),
    ]
    n = 0
    for (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in EJ:
        n += 1
        cells += [h.md(sec_t + "\n\n" + sec_b), h.exercise_md(n, ej_t),
                  h.code(sol if con_sol else todo), h.check_cell(n, chk, hint)]
    cells += [h.md(REG_MD), h.code(REGISTRO), h.md(EXTRAER_MD), h.code(EXTRAER)]
    for (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in EJ2:
        n += 1
        cells += [h.md(sec_t + "\n\n" + sec_b), h.exercise_md(n, ej_t),
                  h.code(sol if con_sol else todo), h.check_cell(n, chk, hint)]
    cells += [h.md(PLANIFICAR_MD), h.code(PLANIFICAR_CELL)]
    for (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in EJ3:
        n += 1
        cells += [h.md(sec_t + "\n\n" + sec_b), h.exercise_md(n, ej_t),
                  h.code(sol if con_sol else todo), h.check_cell(n, chk, hint)]
    cells += [h.md(REDACTAR_MD), h.code(REDACTAR_CELL)]
    sec_t, sec_b, ej_t, sol, todo, chk, hint, viz = EJ6
    n += 1
    cells += [h.md(sec_t + "\n\n" + sec_b), h.exercise_md(n, ej_t),
              h.code(sol if con_sol else todo), h.check_cell(n, chk, hint)]
    cells += [h.md(DEMO_MD), h.code(DEMO_CELL), h.md(RIESGOS), h.md(CIERRE)]
    nb.cells = cells
    return nb


# ─────────────────────────────────────────────────────────────────────────────
# PROFUNDIZA — herramienta de búsqueda en fichas + guardas
# ─────────────────────────────────────────────────────────────────────────────
PROF_HEADER = '''# R3-04 · Agentes — Profundización (opcional) 🔬

**Formación Pública — Rama R3 · IA Aplicada · Notebook de profundización**

Opcional y de **transferencia**: le das al agente una herramienta nueva sobre otro corpus —
**buscar en las 245 fichas de ChileAtiende** (tu RAG de R3-03, hecho herramienta)— y lo
blindas con **guardas**: argumentos válidos, calidad del dato y privacidad. Además **mides**
al planificador con un set de peticiones, igual que mediste la recuperación con hit@k.

Todo corre sin red ni LLM: el agente usa su planificador de reglas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_PREP = CARGA.replace('for archivo in ["aire_diario.csv", "estaciones.csv", "matricula.csv"]:',
                          'for archivo in ["aire_diario.csv", "estaciones.csv", "matricula.csv", "fichas.csv"]:') + '''
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
fichas = pd.read_csv("fichas.csv")

# ── Herramientas y agente de la lección (versión resuelta) ──
''' + HERR_BASE + "\n\n" + DIAS_SOL + "\n\n" + REGISTRO.split("for nombre, d in")[0].rstrip() + "\n\n" + \
    EXTRAER.split("print(extraer_estacion")[0].rstrip() + "\n\n" + PLAN_REGLAS_SOL + "\n\n" + \
    EJECUTAR_SOL + "\n\n" + SUPERVISADO_SOL + '''

def agente(peticion, planificador=None, aprobador=None, max_pasos=4):
    planificador = planificador or planificar_reglas      # aquí, sin LLM
    traza, estado = [], "limite_de_pasos"
    for _ in range(max_pasos):
        plan = planificador(peticion, traza)
        if plan["herramienta"] == "fin":
            estado = "terminado"
            break
        ejecutar_supervisado(plan, traza, aprobador)
    return {"estado": estado, "traza": traza}

# ── Índice de fichas (receta de la profundización de R3-03: título x3 + n-gramas de caracteres) ──
def trocear(texto, max_palabras=120):
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
    return trozos

trozos = pd.DataFrame([{"id": f.id, "titulo": f.titulo, "url": f.url, "texto": t}
                       for f in fichas.itertuples() for t in trocear(f.texto)])
vect_fichas = TfidfVectorizer(strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5))
X_fichas = vect_fichas.fit_transform((trozos["titulo"] + "\\n") * 3 + trozos["texto"])
print("Agente listo con", len(HERRAMIENTAS), "herramientas | índice de fichas:", X_fichas.shape)'''

PROF_EJ = [
 ("## 1. Una herramienta nueva: buscar en las fichas",
  "Escribe `buscar_ficha(consulta)`: transforma la consulta con `vect_fichas`, calcula la "
  "similitud con `X_fichas` y devuelve la ficha del **mejor trozo**: `id`, `titulo`, `url` y "
  "`puntaje` (redondeado a 2 decimales). Después regístrala en `HERRAMIENTAS` — sin efecto: "
  "solo consulta.",
  "Escribe y registra `buscar_ficha`",
  '''def buscar_ficha(consulta):
    puntajes = (X_fichas @ vect_fichas.transform([consulta]).T).toarray().ravel()
    i = int(np.argmax(puntajes))
    f = trozos.iloc[i]
    return {"id": int(f["id"]), "titulo": f["titulo"], "url": f["url"], "puntaje": round(float(puntajes[i]), 2)}

HERRAMIENTAS["buscar_ficha"] = {"funcion": buscar_ficha, "args": ["consulta"], "efecto": False,
                                "descripcion": "Busca la ficha de ChileAtiende más pertinente para un trámite."}
buscar_ficha("¿Cómo me afilio a Fonasa?")''',
  '''def buscar_ficha(consulta):
    # TODO: puntajes = similitud de la consulta con cada trozo (X_fichas @ vect_fichas.transform([consulta]).T)
    puntajes = ...
    # TODO: i = posición del mayor puntaje (int(np.argmax(puntajes)))
    i = ...
    f = trozos.iloc[i]
    return {"id": int(f["id"]), "titulo": f["titulo"], "url": f["url"], "puntaje": round(float(puntajes[i]), 2)}

# TODO: registra la herramienta en HERRAMIENTAS["buscar_ficha"] con funcion, args=["consulta"],
#       efecto=False y una descripcion
...''',
  '''r = buscar_ficha("¿Cómo me afilio a Fonasa?")
assert r["id"] == 9715 and r["url"].endswith("/9715"), "Fonasa debería llevar a la ficha 9715"
assert buscar_ficha("¿Cómo saco la licencia para pescar como deporte?")["id"] == 4636
assert "buscar_ficha" in HERRAMIENTAS and HERRAMIENTAS["buscar_ficha"]["efecto"] is False
assert HERRAMIENTAS["buscar_ficha"]["args"] == ["consulta"]''',
  'puntajes = (X_fichas @ vect_fichas.transform([consulta]).T).toarray().ravel(); i = int(np.argmax(puntajes)); y HERRAMIENTAS["buscar_ficha"] = {...}.'),

 ("## 2. Enseñarle al planificador… y medirlo",
  "Escribe `planificar_v2`: si es el **primer paso** y la petición suena a **trámite** (alguna de "
  "`PALABRAS_TRAMITE`), propone `buscar_ficha` con la petición como consulta; en cualquier otro "
  "caso, delega en `planificar_reglas`. Luego **mídelo** con un set de peticiones y su "
  "herramienta esperada: la fracción de aciertos es tu «hit@1» del planificador.",
  "Escribe `planificar_v2` y calcula su exactitud",
  '''PALABRAS_TRAMITE = ["como saco", "como obtengo", "como pido", "tramite", "requisitos",
                    "postular", "beca", "bono", "certificado", "beneficio"]

def planificar_v2(peticion, traza):
    t = normalizar(peticion)
    if not traza and any(w in t for w in PALABRAS_TRAMITE):
        return {"herramienta": "buscar_ficha", "args": {"consulta": peticion}}
    return planificar_reglas(peticion, traza)

PRUEBAS_PLAN = [
    ("¿Cómo saco el certificado de antecedentes?", "buscar_ficha"),
    ("¿Qué requisitos tiene el bono de invierno?", "buscar_ficha"),
    ("¿Cómo postular a la beca indígena?", "buscar_ficha"),
    ("¿Cuántos días sobre la norma tuvo Nielol en 2021?", "dias_sobre_norma"),
    ("¿Cómo estuvo el aire en Coyhaique en 2022?", "pm25_promedio"),
    ("PM2.5 promedio de Quintero en 2020", "pm25_promedio"),
    ("¿Cuántos estudiantes hay en Valdivia?", "matricula_comuna"),
    ("¿Cuántos colegios tiene Putre?", "matricula_comuna"),
    ("¿Qué beca hay para estudiantes con discapacidad?", "buscar_ficha"),
    ("¿Quién ganó el partido de ayer?", "fin"),
]
aciertos = [planificar_v2(p, [])["herramienta"] == esperada for p, esperada in PRUEBAS_PLAN]
exactitud = sum(aciertos) / len(PRUEBAS_PLAN)
print(f"exactitud del planificador: {exactitud:.2f}")
for (p, e), ok in zip(PRUEBAS_PLAN, aciertos):
    if not ok:
        print("✗", p, "→", planificar_v2(p, [])["herramienta"], "(esperaba", e + ")")''',
  '''PALABRAS_TRAMITE = ["como saco", "como obtengo", "como pido", "tramite", "requisitos",
                    "postular", "beca", "bono", "certificado", "beneficio"]

def planificar_v2(peticion, traza):
    t = normalizar(peticion)
    # TODO: si la traza está vacía y alguna palabra de PALABRAS_TRAMITE está en t →
    #       return {"herramienta": "buscar_ficha", "args": {"consulta": peticion}}
    ...
    return planificar_reglas(peticion, traza)

PRUEBAS_PLAN = [
    ("¿Cómo saco el certificado de antecedentes?", "buscar_ficha"),
    ("¿Qué requisitos tiene el bono de invierno?", "buscar_ficha"),
    ("¿Cómo postular a la beca indígena?", "buscar_ficha"),
    ("¿Cuántos días sobre la norma tuvo Nielol en 2021?", "dias_sobre_norma"),
    ("¿Cómo estuvo el aire en Coyhaique en 2022?", "pm25_promedio"),
    ("PM2.5 promedio de Quintero en 2020", "pm25_promedio"),
    ("¿Cuántos estudiantes hay en Valdivia?", "matricula_comuna"),
    ("¿Cuántos colegios tiene Putre?", "matricula_comuna"),
    ("¿Qué beca hay para estudiantes con discapacidad?", "buscar_ficha"),
    ("¿Quién ganó el partido de ayer?", "fin"),
]
# TODO: aciertos = lista de True/False (¿planificar_v2(p, [])["herramienta"] == esperada?)
aciertos = ...
# TODO: exactitud = fracción de aciertos
exactitud = ...
print("exactitud del planificador:", exactitud)''',
  '''assert planificar_v2("¿Cómo saco el certificado de antecedentes?", [])["herramienta"] == "buscar_ficha"
assert planificar_v2("¿Cuántos estudiantes hay en Valdivia?", [])["herramienta"] == "matricula_comuna"
assert planificar_v2("¿Cómo saco el certificado de antecedentes?", [{"estado": "ok", "herramienta": "buscar_ficha"}])["herramienta"] == "fin"
assert abs(exactitud - sum(planificar_v2(p, [])["herramienta"] == e for p, e in PRUEBAS_PLAN) / len(PRUEBAS_PLAN)) < 1e-9
assert exactitud >= 0.8''',
  'if not traza and any(w in t for w in PALABRAS_TRAMITE): return {"herramienta": "buscar_ficha", "args": {"consulta": peticion}}.'),

 ("## 3. Guarda de argumentos: no ejecutar a ciegas",
  "El planificador puede proponer una estación `None` («Temuco» es ambiguo), un año sin datos "
  "(2030) o una comuna inexistente. Mejor detectarlo **antes** de ejecutar y explicarlo. Escribe "
  "`validar_args(plan)` que devuelva `(True, \"\")` o `(False, motivo)`. Luego "
  "`ejecutar_con_guardas` lo usa: si no pasa, registra el paso como `bloqueado_por_guarda`.",
  "Escribe `validar_args`",
  '''ANIOS_CON_DATOS = set(aire["fecha"].dt.year.unique())     # 2020–2025

def validar_args(plan):
    a = plan["args"]
    if "estacion" in a and a["estacion"] not in set(estaciones["estacion"]):
        return False, f"estación no reconocida o ambigua ({a['estacion']}); opciones: {', '.join(estaciones['estacion'])}"
    if "anio" in a and a["anio"] not in ANIOS_CON_DATOS:
        return False, f"no hay datos para el año {a['anio']} (cobertura {min(ANIOS_CON_DATOS)}–{max(ANIOS_CON_DATOS)})"
    if "comuna" in a and a["comuna"] is None:
        return False, "no reconocí la comuna"
    return True, ""

def ejecutar_con_guardas(plan, traza, aprobador=None):
    ok, motivo = validar_args(plan)
    if not ok:
        traza.append({"paso": len(traza) + 1, "herramienta": plan["herramienta"], "args": plan["args"],
                      "origen": plan.get("origen", "manual"), "resultado": motivo, "estado": "bloqueado_por_guarda"})
        return traza[-1]
    return ejecutar_supervisado(plan, traza, aprobador)

print(validar_args(planificar_reglas("PM2.5 en Temuco en 2024", [])))
print(validar_args(planificar_reglas("PM2.5 en Nielol en 2030", [])))''',
  '''ANIOS_CON_DATOS = set(aire["fecha"].dt.year.unique())     # 2020–2025

def validar_args(plan):
    a = plan["args"]
    # TODO 1: si "estacion" está en a y no es una estación de estaciones["estacion"] →
    #         return False, "estación no reconocida o ambigua ..."
    # TODO 2: si "anio" está en a y no está en ANIOS_CON_DATOS →
    #         return False, f"no hay datos para el año {a['anio']} ..."
    # TODO 3: si "comuna" está en a y es None → return False, "no reconocí la comuna"
    ...
    return True, ""

def ejecutar_con_guardas(plan, traza, aprobador=None):
    ok, motivo = validar_args(plan)
    if not ok:
        traza.append({"paso": len(traza) + 1, "herramienta": plan["herramienta"], "args": plan["args"],
                      "origen": plan.get("origen", "manual"), "resultado": motivo, "estado": "bloqueado_por_guarda"})
        return traza[-1]
    return ejecutar_supervisado(plan, traza, aprobador)''',
  '''ok, motivo = validar_args({"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2030}})
assert ok is False and "2030" in motivo, "un año sin datos debe bloquearse, nombrando el año"
ok, motivo = validar_args({"herramienta": "pm25_promedio", "args": {"estacion": None, "anio": 2024}})
assert ok is False, "una estación None (ambigua) debe bloquearse"
assert validar_args({"herramienta": "matricula_comuna", "args": {"comuna": None}})[0] is False
assert validar_args({"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2022}}) == (True, "")
t = []
ejecutar_con_guardas({"herramienta": "pm25_promedio", "args": {"estacion": "Nielol", "anio": 2030}}, t)
assert t[-1]["estado"] == "bloqueado_por_guarda"''',
  'if "anio" in a and a["anio"] not in ANIOS_CON_DATOS: return False, f"no hay datos para el año {a[\'anio\']}"; igual para estación y comuna.'),

 ("## 4. Guarda de calidad: un cero que no es cero",
  "Pregúntale al agente por **El Bosque en 2025**: responde **0 días** sobre la norma. ¿Buena "
  "noticia? No: esa estación solo tiene **59 días con dato** ese año (en 2024 tuvo 45 días sobre "
  "la norma). Un agente honesto **advierte** cuando el dato es incompleto. Escribe "
  "`con_advertencia(resultado, minimo_dias=300)`: si el resultado trae `dias_con_dato` bajo el "
  "mínimo, devuelve una copia con la clave `advertencia`.",
  "Escribe `con_advertencia`",
  '''def con_advertencia(resultado, minimo_dias=300):
    if isinstance(resultado, dict) and resultado.get("dias_con_dato", minimo_dias) < minimo_dias:
        return {**resultado, "advertencia": f"solo {resultado['dias_con_dato']} días con dato: "
                                            "la cifra no es comparable con otros años"}
    return resultado

print(con_advertencia(dias_sobre_norma("El Bosque (Acreditada)", 2025)))
print(con_advertencia(dias_sobre_norma("El Bosque (Acreditada)", 2024)))''',
  '''def con_advertencia(resultado, minimo_dias=300):
    # TODO: si resultado es dict y resultado.get("dias_con_dato", minimo_dias) < minimo_dias,
    #       devuelve {**resultado, "advertencia": f"solo {resultado['dias_con_dato']} días con dato: ..."}
    ...
    return resultado''',
  '''r25 = con_advertencia(dias_sobre_norma("El Bosque (Acreditada)", 2025))
assert "advertencia" in r25 and "59" in r25["advertencia"], "El Bosque 2025 tiene solo 59 días con dato: debe advertirlo"
r24 = con_advertencia(dias_sobre_norma("El Bosque (Acreditada)", 2024))
assert "advertencia" not in r24, "con un año casi completo no hay advertencia"
assert con_advertencia({"comuna": "Arica", "estudiantes": 1}) == {"comuna": "Arica", "estudiantes": 1}, "resultados sin días quedan igual"''',
  'if isinstance(resultado, dict) and resultado.get("dias_con_dato", minimo_dias) < minimo_dias: return {**resultado, "advertencia": ...}.'),

 ("## 5. Desafío: guarda de privacidad y el agente blindado",
  "Si la petición trae un **RUT**, no debe salir hacia un LLM externo ni quedar en una traza "
  "que muchos pueden leer. Escribe `contiene_rut(texto)` y `agente_blindado(peticion, ...)`: "
  "si hay RUT, devuelve `{\"estado\": \"bloqueado_privacidad\", \"traza\": []}` **sin planificar "
  "nada**; si no, corre el agente usando `planificar_v2`, `ejecutar_con_guardas` y "
  "`con_advertencia` en cada resultado.",
  "Escribe `contiene_rut` y `agente_blindado`",
  '''def contiene_rut(texto):
    return re.search(r"\\b\\d{1,2}\\.?\\d{3}\\.?\\d{3}-[\\dkK]\\b", texto) is not None

def agente_blindado(peticion, aprobador=None, max_pasos=4):
    if contiene_rut(peticion):
        return {"estado": "bloqueado_privacidad", "traza": []}
    traza, estado = [], "limite_de_pasos"
    for _ in range(max_pasos):
        plan = planificar_v2(peticion, traza)
        if plan["herramienta"] == "fin":
            estado = "terminado"
            break
        registro = ejecutar_con_guardas(plan, traza, aprobador)
        registro["resultado"] = con_advertencia(registro["resultado"])
    return {"estado": estado, "traza": traza}

for p in ["¿Cuántos días sobre la norma tuvo El Bosque en 2025?",
          "¿Cómo pido la pensión de alimentos? Mi RUT es 12.345.678-5",
          "¿Cómo saco el certificado de antecedentes?"]:
    r = agente_blindado(p)
    print(r["estado"], [(x["herramienta"], x["estado"], x["resultado"]) for x in r["traza"]])''',
  '''def contiene_rut(texto):
    # TODO: busca un RUT con la expresión regular r"\\b\\d{1,2}\\.?\\d{3}\\.?\\d{3}-[\\dkK]\\b"
    return ...

def agente_blindado(peticion, aprobador=None, max_pasos=4):
    # TODO: si contiene_rut(peticion) → return {"estado": "bloqueado_privacidad", "traza": []}
    ...
    traza, estado = [], "limite_de_pasos"
    for _ in range(max_pasos):
        plan = planificar_v2(peticion, traza)
        if plan["herramienta"] == "fin":
            estado = "terminado"
            break
        # TODO: ejecuta con ejecutar_con_guardas y pasa su resultado por con_advertencia
        ...
    return {"estado": estado, "traza": traza}''',
  '''assert contiene_rut("Mi RUT es 12.345.678-5") and contiene_rut("rut 9876543-k")
assert not contiene_rut("¿Cuántos estudiantes hay en Arica en 2025?")
assert agente_blindado("¿Cómo pido la pensión de alimentos? Mi RUT es 12.345.678-5") == {"estado": "bloqueado_privacidad", "traza": []}
r = agente_blindado("¿Cuántos días sobre la norma tuvo El Bosque en 2025?")
assert r["estado"] == "terminado" and "advertencia" in r["traza"][0]["resultado"], "el resultado de El Bosque 2025 debe venir con advertencia"
r = agente_blindado("¿Cuál fue el PM2.5 de Nielol en 2030?")
assert r["traza"][0]["estado"] == "bloqueado_por_guarda"
assert agente_blindado("¿Cómo saco el certificado de antecedentes?")["traza"][0]["resultado"]["id"] == 3442''',
  'return re.search(PATRON, texto) is not None; en el bucle: registro = ejecutar_con_guardas(...); registro["resultado"] = con_advertencia(registro["resultado"]).'),
]

PROF_CIERRE = '''## Para llevar

- Agregar una **herramienta** = una función + una línea en el menú. Agregar **criterio** = enseñarle
  al planificador cuándo usarla… y **medirlo** con un set de peticiones.
- Las **guardas** van **antes** (argumentos válidos, privacidad) y **después** (calidad del
  resultado) de cada herramienta. Ninguna depende del LLM.
- Un **cero con 59 días de dato** no es un cero: un agente público advierte cuando el dato no da
  para concluir.
- La detección de RUT por expresión regular es una **primera barrera**, no una garantía: los datos
  personales se protegen también con diseño (qué se pide, qué se guarda, quién ve la traza).

---

*Fin de la profundización de R3-04.*'''


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


README = '''# R3-04 · Agentes: herramientas, trazas y supervisión humana

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-04-agentes/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías y autoevaluación.

Un **agente** que recibe peticiones en lenguaje natural y usa **herramientas** (funciones de
Python) sobre datos reales de las otras dos ramas: **calidad del aire** SINCA
(`aire_diario.csv` + `estaciones.csv`, ancla de R2) y **matrícula escolar** MINEDUC
(`matricula.csv`, ancla de R1). El LLM **propone** el siguiente paso en JSON y el código lo
**valida**; si no hay clave o la propuesta es inválida, decide un **planificador de reglas**
determinista. Cada paso queda en una **traza**, hay **límite de pasos** y toda acción con efecto
(enviar una alerta, simulada) exige **aprobación humana**, denegada por defecto. Cierra con una
tabla de **riesgos** y mitigaciones. Funciona completo **sin clave ni red**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅). 6 chequeos.
- `profundiza.ipynb` — opcional 🔬: herramienta `buscar_ficha` sobre `fichas.csv` (el RAG de
  R3-03), medir el planificador, y guardas de argumentos, calidad del dato y privacidad. 5 chequeos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R3-ia-aplicada/R3-04-agentes/profundiza.ipynb) ← profundización

*Fuentes: SINCA · Ministerio del Medio Ambiente (PM2.5 diario 2020–2025); MINEDUC · Resumen de
matrícula por establecimiento 2025; fichas de trámites de ChileAtiende.*
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
