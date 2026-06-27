# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de C3 (Agentes):
C3/profundiza.ipynb (estudiante) + C3/profundiza_solucion.ipynb (resuelto).

TODO el cuaderno es CONCEPTUAL y verificable SIN conexión ni API key:
mini-agente con ENRUTADOR POR REGLAS y herramientas deterministas en Python puro
sobre gasto_anual.csv. NINGÚN ejercicio ni demo llama a un LLM ni requiere red
(salvo el fallback de descarga del CSV)."""
import json, os

BASE = "C3-agentes"

TITULO = """# C3 · Agentes — Profundización (opcional) 🔬

**Formación Pública — Bloque avanzado · IA aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de C3 —donde *construiste* un agente que decide
qué herramienta usar y la ejecuta— aquí vamos al *porqué*: por qué el ciclo **decidir → actuar → responder**
es en realidad una **traza auditable**, por qué los agentes **fallan** (errores que se **acumulan** paso a
paso, y la trampa de **elegir mal la herramienta**), cuándo un **enrutador por reglas** es más **auditable y
barato** que un LLM, y por qué en el Estado el **humano en el bucle**, la **gobernanza** y el **costo/seguridad**
no son opcionales.

Menos código nuevo, más **modelo mental**. Todo lo de aquí corre **sin API key y sin conexión**: el mini-agente
usa un enrutador por reglas y herramientas deterministas en Python puro. Los ejercicios del final son
**conceptuales** y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de C3. Mismo dataset: `gasto_anual.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# gasto_anual.csv del módulo (mismo dato de la lección). Si no está, se intenta descargar.
if not os.path.exists("gasto_anual.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/C3-agentes/gasto_anual.csv"
        urllib.request.urlretrieve(url, "gasto_anual.csv")
    except Exception:
        print("Si estás en Colab, sube gasto_anual.csv manualmente.")

df = pd.read_csv("gasto_anual.csv")
GASTO = dict(zip(df["anio"], df["gasto"]))
print(f"{len(GASTO)} años cargados ({min(GASTO)}–{max(GASTO)}). Serie de gasto público anual (CLP).")
print("Este cuaderno NO usa API key ni LLM: todo el agente corre offline y es determinista.")"""

S1 = """## 1. El ciclo decidir → actuar → responder es una *traza auditable*

En la lección armaste el ciclo del agente: **decidir** qué herramienta usar, **actuar** (ejecutarla) y
**responder**. Aquí está el *porqué* importa tanto ese orden en el Estado: cada paso deja un **registro**.

Un programa común es una **caja negra**: entra una petición, sale un número, y nadie sabe *por qué*. Un agente
bien diseñado es lo contrario: cada decisión queda **anotada** en una **traza** (un *log*). Esa traza permite
responder la pregunta que un órgano de control SIEMPRE hará: *"¿por qué el sistema entregó esta respuesta?"*.

Analogía pública: es la diferencia entre un funcionario que firma una resolución **sin** dejar el expediente
(imposible de auditar) y uno que adjunta **cada paso** del trámite (decisión, norma aplicada, resultado). El
segundo es **auditable**: si algo sale mal, se puede reconstruir *dónde*.

Vamos a *verlo*: definimos herramientas deterministas y un agente que, además de responder, **registra la
traza** de lo que hizo en cada paso."""

S1_CODE = """import unicodedata, re

def _sa(s):
    # quita tildes y baja a minúsculas (para comparar palabras clave sin sorpresas)
    s = unicodedata.normalize("NFKD", str(s).lower())
    return "".join(c for c in s if not unicodedata.combining(c))

# ---- HERRAMIENTAS deterministas (Python puro, sin LLM, sin red) ----
def tool_total(g):
    return sum(g.values())

def tool_max(g):
    anio = max(g, key=g.get)        # año con mayor gasto
    return (anio, g[anio])

def tool_variacion(g):
    a0, a1 = min(g), max(g)
    return (g[a1] / g[a0] - 1) * 100   # variación % entre el primer y último año

# ---- ENRUTADOR POR REGLAS (palabras clave -> herramienta) ----
def enrutar(peticion):
    t = _sa(peticion)
    if any(w in t for w in ["total", "suma", "acumulad"]):
        return "total"
    if any(w in t for w in ["maximo", "mayor", "peak", "mas alto", "record"]):
        return "max"
    if any(w in t for w in ["variacion", "creci", "aument", "subio", "cambio"]):
        return "variacion"
    return "desconocida"

# ---- AGENTE con TRAZA auditable: decidir -> actuar -> responder, registrando cada paso ----
def agente_con_traza(peticion):
    traza = []
    traza.append(("decidir", f"petición='{peticion}'"))
    herr = enrutar(peticion)
    traza.append(("herramienta_elegida", herr))
    if herr == "total":
        resultado = tool_total(GASTO); resp = f"Gasto total acumulado: {resultado:,.0f} CLP"
    elif herr == "max":
        anio, val = tool_max(GASTO); resp = f"Año de mayor gasto: {anio} con {val:,.0f} CLP"
    elif herr == "variacion":
        resultado = tool_variacion(GASTO); resp = f"Variación del periodo: {resultado:+.1f}%"
    else:
        resp = "No tengo una herramienta para esa petición."
    # logueamos qué tool se EJECUTÓ y su resultado; 'responder' es la versión final para el usuario
    traza.append(("actuar", f"ejecutó {herr} -> {resp}"))
    traza.append(("responder", resp))
    return {"respuesta": resp, "traza": traza}

salida = agente_con_traza("¿Cuál es el gasto total del periodo?")
print("RESPUESTA:", salida["respuesta"])
print("\\nTRAZA AUDITABLE (cada paso queda registrado):")
for paso, detalle in salida["traza"]:
    print(f"  - {paso:18s}: {detalle}")"""

S2 = """## 2. *Tool use*: el agente elige una herramienta y la ejecuta (no "sabe" la respuesta)

Una confusión común: creer que el agente *calcula* o *sabe* las cosas. No. El agente solo **elige** cuál de
sus herramientas usar y la **ejecuta**; el cálculo lo hace la **herramienta** (código determinista que tú
escribiste y puedes auditar). Esto se llama ***tool use*** y es la idea central: el "cerebro" decide, las
"manos" (herramientas) hacen.

¿Por qué es bueno para el Estado? Porque la parte que produce el número es **código verificable**, no una
caja negra. `tool_total` siempre suma igual; `tool_max` siempre encuentra el mismo año. Puedes testearla,
auditarla y exigir que sea correcta. El agente puede equivocarse **eligiendo** la herramienta (sección 4),
pero la herramienta en sí es **confiable y reproducible**.

Veamos las tres herramientas ejecutándose sobre el dataset real, y luego el enrutador eligiendo entre ellas."""

S2_CODE = """# Las herramientas, ejecutadas directamente sobre el dataset real:
print("tool_total     ->", f"{tool_total(GASTO):,.0f} CLP (suma de los 7 años)")
anio_pk, val_pk = tool_max(GASTO)
print("tool_max       ->", f"{anio_pk} con {val_pk:,.0f} CLP")
print("tool_variacion ->", f"{tool_variacion(GASTO):+.1f}% entre {min(GASTO)} y {max(GASTO)}")

# El enrutador eligiendo herramienta para varias peticiones (esto es la 'decisión' del agente):
print("\\nEnrutador por reglas (palabra clave -> herramienta):")
for p in ["dame el total gastado",
          "¿qué año tuvo el gasto máximo?",
          "¿cuánto creció el gasto?",
          "¿cuál es la capital de Chile?"]:
    print(f"  {enrutar(p):12s} <- {p}")"""

S3 = """## 3. Determinismo vs enrutamiento por LLM: cuándo una regla simple es **mejor**

En producción, muchos agentes usan un **LLM** como enrutador: le das la petición y él decide la herramienta.
Es flexible (entiende frases raras), pero tiene tres costos que en el Estado pesan mucho:

- **Auditabilidad:** un `if "total" in texto` es **leíble línea por línea** y siempre decide igual. Un LLM
  decide con miles de millones de parámetros opacos: explicar *por qué* eligió algo es difícil.
- **Reproducibilidad:** la regla da **exactamente** la misma salida siempre. El LLM puede variar entre
  llamadas (incluso con la misma entrada) y cambia entre versiones del modelo.
- **Costo y dependencia:** la regla es **gratis, instantánea y offline**. El LLM cuesta plata por llamada,
  agrega latencia y te ata a un proveedor externo (y a enviarle tus datos).

La moraleja **no** es "el LLM es malo". Es: **usa la herramienta más simple que resuelva el problema.** Si una
regla de palabras clave clasifica bien tus peticiones, es **más auditable, más barata y más segura** que un
LLM. Reserva el LLM para lo que de verdad necesita lenguaje natural ambiguo. Comparemos las dos filosofías en
una pequeña tabla."""

S3_CODE = """comparacion = pd.DataFrame({
    "criterio":        ["¿auditable?", "¿reproducible?", "costo por consulta", "¿offline?", "maneja frases ambiguas"],
    "enrutador_reglas":["sí, línea a línea", "siempre igual",   "$0",                "sí",        "limitado"],
    "enrutador_LLM":   ["opaco",            "puede variar",     "$ por llamada",     "no",        "muy bueno"],
})
print(comparacion.to_string(index=False))
print("\\nRegla de oro: usa lo MÁS SIMPLE que resuelva el problema.")
print("Para este dataset, el enrutador por reglas basta y es más auditable que un LLM.")"""

S4 = """## 4. Por qué fallan los agentes (I): elegir **mal** la herramienta propaga el error

El agente puede tener herramientas perfectas y aun así dar una respuesta **equivocada**: basta que el
**enrutador elija la herramienta incorrecta**. Y aquí está lo traicionero: como cada herramienta devuelve un
número con buena forma, la respuesta equivocada **se ve igual de convincente** que la correcta. El error de
*decisión* se **propaga** silenciosamente a la *respuesta*.

Analogía pública: un formulario de ayuda social bien diseñado, pero derivado a la **oficina equivocada**.
Cada oficina hace su trabajo impecable… resolviendo el trámite que **no era**. El ciudadano recibe una
respuesta formalmente correcta y materialmente errónea.

Vamos a forzarlo: una petición que claramente pide la **variación**, pero un enrutador con una regla mal
puesta la manda a `tool_total`. Compararemos la respuesta **equivocada** con la **correcta** para ver cómo el
error de enrutamiento contamina todo lo que viene después."""

S4_CODE = """# Enrutador DEFECTUOSO: por error, manda TODO lo que diga 'gasto' a 'total'
def enrutar_malo(peticion):
    t = _sa(peticion)
    if "gasto" in t:        # regla demasiado amplia: atrapa peticiones que NO son de total
        return "total"
    return enrutar(peticion)

peticion = "¿cuánto creció el gasto entre 2019 y 2025?"   # pide VARIACIÓN, claramente
print("Petición:", peticion, "\\n")

herr_buena = enrutar(peticion)
herr_mala  = enrutar_malo(peticion)
print(f"Enrutador correcto  -> elige '{herr_buena}'  -> {tool_variacion(GASTO):+.1f}%  (la respuesta REAL)")
print(f"Enrutador defectuoso -> elige '{herr_mala}'  -> {tool_total(GASTO):,.0f} CLP  (respuesta CONVINCENTE pero EQUIVOCADA)")
print("\\nMismo dato, herramientas perfectas: el ÚNICO error fue ELEGIR MAL.")
print("Y la respuesta equivocada se ve tan 'seria' como la correcta. Por eso la traza importa.")"""

S5 = """## 5. Por qué fallan los agentes (II): los errores se **acumulan** paso a paso

El segundo gran motivo de fallo es **matemático**, no de programación. Un agente que encadena varios pasos
(decidir, llamar una herramienta, pasar el resultado a otra, etc.) solo acierta si **todos** los pasos
aciertan. Y las probabilidades **se multiplican**.

Supón que cada paso es confiable al **90%** (0,9). Suena bien. Pero:

- 1 paso → 0,9 (90% de éxito)
- 3 pasos → 0,9 × 0,9 × 0,9 = 0,729 (**72,9%**, ≈73%)
- 5 pasos → 0,9⁵ ≈ **0,59** (¡menos del 60%!)
- 10 pasos → 0,9¹⁰ ≈ **0,35**

Cada paso "casi perfecto" **erosiona** la fiabilidad total. Por eso los agentes largos y autónomos son
**frágiles**: no porque un paso falle mucho, sino porque fallan **un poquito muchos**. La lección de diseño:
**menos pasos, más cortos, y un humano que revise** en los puntos críticos (sección 6). Grafiquémoslo."""

S5_CODE = """def exito_encadenado(p_paso, n_pasos):
    return p_paso ** n_pasos

pasos = np.arange(1, 11)
for p in (0.9, 0.95):
    fiab = [exito_encadenado(p, n) for n in pasos]
    plt.plot(pasos, fiab, marker="o", label=f"{p:.0%} por paso")

plt.axhline(0.5, color="crimson", linestyle="--", label="50% (moneda al aire)")
plt.title("Fiabilidad total = (fiabilidad por paso) ^ (número de pasos)")
plt.xlabel("N° de pasos encadenados"); plt.ylabel("Probabilidad de éxito total")
plt.ylim(0, 1); plt.legend(); plt.tight_layout(); plt.show()

print(f"Con 90% por paso y 5 pasos, el éxito total cae a {0.9**5:.2%}.")
print("La fiabilidad NO se suma: se MULTIPLICA. Pocos pasos = agente más robusto.")"""

S6 = """## 6. Humano en el bucle, gobernanza, auditabilidad y costo/seguridad

Si los agentes fallan por elegir mal (sección 4) y por acumular errores (sección 5), la conclusión de diseño
para el Estado es clara: **el agente asiste; el humano decide y responde.** Esto se llama **humano en el bucle**
(*human-in-the-loop*) y no es burocracia: es lo que evita que un error técnico se convierta en una **injusticia**
o un **daño** a un ciudadano.

Las reglas no negociables que se desprenden de todo el cuaderno:

1. **Humano en el bucle en lo crítico.** Toda decisión que afecte **derechos** (un beneficio, una sanción, una
   adjudicación) pasa por una persona que revisa la **traza** y firma. El agente propone; el humano dispone.
2. **Auditabilidad por diseño.** Cada respuesta debe poder reconstruirse: qué herramienta, con qué dato, con qué
   resultado. Sin traza, no hay control posible (ni transparencia activa).
3. **Gobernanza:** definir **qué puede y qué no puede** hacer el agente solo, y los límites (no ejecutar pagos,
   no enviar datos personales a terceros, no decidir sin revisión).
4. **Costo y seguridad:** prefiere lo **simple, barato y offline** cuando alcance (sección 3); cada llamada a un
   servicio externo cuesta plata y **expone datos**. Menos pasos y menos dependencias = menos superficie de riesgo.

Cerramos con un mini-experimento de **gobernanza**: una capa que **revisa** la respuesta del agente y, si el
resultado supera un umbral de impacto (mucha plata), la **deriva a revisión humana** en vez de ejecutarla sola."""

S6_CODE = """UMBRAL_REVISION = 10_000_000_000_000   # 10 billones CLP: sobre esto, NO decide solo el agente

def agente_gobernado(peticion):
    salida = agente_con_traza(peticion)
    herr = dict(salida["traza"])["herramienta_elegida"]
    # Si la herramienta produce una CIFRA grande de impacto, se exige revisión humana
    monto = None
    if herr == "total":
        monto = tool_total(GASTO)
    elif herr == "max":
        monto = tool_max(GASTO)[1]
    requiere_humano = monto is not None and monto > UMBRAL_REVISION
    salida["requiere_revision_humana"] = bool(requiere_humano)
    return salida

for p in ["dame el total gastado", "¿cuánto creció el gasto?"]:
    s = agente_gobernado(p)
    flag = "🛑 DERIVAR A HUMANO" if s["requiere_revision_humana"] else "🟢 puede responder solo"
    print(f"{flag}  <- {p}")
    print(f"     respuesta: {s['respuesta']}")
print(f"\\nUmbral de gobernanza: {UMBRAL_REVISION:,.0f} CLP. Sobre eso, decide una persona, no el agente.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Creer que el agente "sabe" la respuesta.** No: solo **elige** una herramienta y la ejecuta (*tool use*). El cálculo lo hace código determinista que puedes auditar.
- **Usar un LLM como enrutador cuando bastaba una regla.** Más caro, menos reproducible y menos auditable. Usa lo **más simple** que resuelva el problema.
- **Confiar en la respuesta porque "tiene buena forma".** Un enrutamiento equivocado da un número convincente y **falso**. Revisa la **traza**, no solo el resultado.
- **Encadenar muchos pasos autónomos.** La fiabilidad se **multiplica** (0,9⁵ ≈ 0,59): más pasos = más frágil. Menos pasos y más cortos.
- **Automatizar decisiones que afectan derechos sin revisión.** Falta **humano en el bucle**: el agente propone, una persona decide y firma.
- **No registrar la traza.** Sin auditabilidad no hay control, ni transparencia, ni forma de explicar "por qué el sistema hizo esto"."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula algo** Y pide **elegir la interpretación correcta**.
**Ninguno usa LLM, API key ni conexión.** Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 acumulación de errores ----
E1 = """## Ejercicio 01 · La fiabilidad se multiplica
Un agente encadena **5 pasos**, y cada paso es confiable al **90%** (0,9).

- Guarda en `exito_total` la probabilidad de que **los 5 pasos** salgan bien: `0.9 ** 5`.
- Luego elige en `conclusion` (letra) la lectura correcta:
  - **A.** Como cada paso es 90%, el total también es ~90%: encadenar pasos no afecta la fiabilidad.
  - **B.** El total cae bastante por debajo de 90% (a ~0,59): los errores se **acumulan** al multiplicarse, así que menos pasos = agente más robusto.
  - **C.** El total sube por encima de 90%: encadenar pasos **mejora** la fiabilidad."""
E1_TODO = """exito_total = None    # TODO: 0.9 ** 5
conclusion = None     # TODO: "A", "B" o "C"
"""
E1_SOL = """exito_total = 0.9 ** 5
conclusion = "B"
"""
E1_CHK = """try:
    _esp = 0.9 ** 5
    # 'B' si el éxito total cae BASTANTE por debajo de 90% (umbral pedagógico 0.75); con 0.9**5≈0.59, cae claramente
    _correcta = "B" if _esp < 0.75 else "A"
    assert exito_total is not None and abs(exito_total - _esp) < 1e-9, f"exito_total debería ser ~{_esp:.4f} (0.9**5)"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿el éxito total sube o baja al encadenar pasos?"
    print(f"✅ Correcto. 0.9^5 = {_esp:.4f}: la fiabilidad se MULTIPLICA, no se mantiene. Menos pasos = más robusto.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 tool_total ----
E2 = """## Ejercicio 02 · Tool use: ejecutar la herramienta correcta
El agente decide usar `tool_total` para la petición *"dame el gasto total del periodo"*.

- Llama a la herramienta y guarda el resultado en `total` (usa `tool_total(GASTO)`).
- Elige en `conclusion` la interpretación correcta:
  - **A.** El agente "calculó" el total con su inteligencia; sin la herramienta no podría.
  - **B.** El agente solo **eligió** la herramienta; el número lo produjo `tool_total`, código determinista y auditable. El agente podría equivocarse eligiendo, pero la herramienta es confiable.
  - **C.** El total no se puede verificar porque lo generó un LLM.

Pista: `tool_total(GASTO)`."""
E2_TODO = """total = None        # TODO: tool_total(GASTO)
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """total = tool_total(GASTO)
conclusion = "B"
"""
E2_CHK = """try:
    _esp = sum(GASTO.values())
    assert total is not None and total == _esp, f"total debería ser {_esp:,.0f} (usa tool_total(GASTO))"
    # letra fija: ejercicio puramente conceptual (el agente elige, la herramienta calcula); no depende de ningún número del CSV
    assert str(conclusion).strip().upper() == "B", "Pista: ¿quién produce el número, el agente o la herramienta?"
    print(f"✅ Correcto. Total = {_esp:,.0f} CLP. El agente ELIGE; la herramienta (código auditable) CALCULA.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 enrutamiento que se propaga ----
E3 = """## Ejercicio 03 · Un enrutamiento equivocado propaga el error
La petición *"¿cuánto creció el gasto?"* pide claramente la **variación**. Compara dos rutas:

- Guarda en `resp_buena` el resultado de la herramienta **correcta**: `tool_variacion(GASTO)`.
- Guarda en `resp_mala` el resultado de la herramienta **equivocada** (la que elige `enrutar_malo`): `tool_total(GASTO)`.
- Elige en `conclusion` la lectura correcta:
  - **A.** Da lo mismo qué herramienta elija: ambas responden bien la pregunta.
  - **B.** Como las herramientas son correctas, la respuesta siempre es correcta aunque el enrutador falle.
  - **C.** El enrutador equivocado eligió `tool_total` y devolvió un número **convincente pero que NO responde** la pregunta de variación: el error de **decisión** se propagó a la respuesta. Por eso hay que auditar la **traza**, no solo el resultado.

Pista: `tool_variacion(GASTO)` y `tool_total(GASTO)` dan cifras **muy distintas**."""
E3_TODO = """resp_buena = None   # TODO: tool_variacion(GASTO)
resp_mala = None    # TODO: tool_total(GASTO)
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = """resp_buena = tool_variacion(GASTO)
resp_mala = tool_total(GASTO)
conclusion = "C"
"""
E3_CHK = """try:
    _buena = (GASTO[max(GASTO)] / GASTO[min(GASTO)] - 1) * 100
    _mala = sum(GASTO.values())
    _muy_distintas = abs(_mala - _buena) > 1   # son de órdenes de magnitud totalmente distintos
    _correcta = "C" if _muy_distintas else "A"
    assert resp_buena is not None and abs(resp_buena - _buena) < 1e-6, f"resp_buena debería ser ~{_buena:.1f} (tool_variacion)"
    assert resp_mala is not None and abs(resp_mala - _mala) < 1, f"resp_mala debería ser {_mala:,.0f} (tool_total)"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿la herramienta equivocada responde la pregunta de variación?"
    print(f"✅ Correcto. Correcta: {_buena:+.1f}%  vs  equivocada: {_mala:,.0f} CLP. El mal enrutamiento se propagó.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 gobernanza / humano en el bucle (conceptual) ----
E4 = """## Ejercicio 04 · Gobernanza y humano en el bucle (conceptual)
Tu agente puede responder consultas de gasto solo, pero una unidad de control propone una regla: *toda
respuesta cuyo monto supere un **umbral** de impacto debe ir a **revisión humana** antes de ejecutarse o
publicarse*. El agente seguirá calculando, pero **no decidirá solo** sobre cifras grandes.

Elige en `conclusion` la lectura correcta:
- **A.** Es burocracia inútil: si el agente ya calcula bien, revisar es perder el tiempo.
- **B.** Es **humano en el bucle**: el agente **propone** y una persona **decide y firma** en lo que afecta
  derechos o mucha plata. Sumado a la **traza auditable**, es lo que hace gobernable y seguro un agente público.
- **C.** Basta con que el agente sea muy preciso; si acierta el 90% por paso, no hace falta revisión humana.

*(Opcional, no se corrige): en `reflexion` escribe qué decisión de tu institución NUNCA dejarías 100% en manos de un agente.)*"""
E4_TODO = """conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """conclusion = "B"
reflexion = "Una adjudicación de licitación o la aprobación de un beneficio social: el agente prepara, pero firma una persona."
"""
E4_CHK = """try:
    assert conclusion is not None, "Aún no elegiste una letra en 'conclusion'."
    # letra fija: ejercicio puramente conceptual (gobernanza / humano en el bucle); no depende de ningún número del CSV
    assert str(conclusion).strip().upper() == "B", "Pista: ¿quién debe firmar lo que afecta derechos o mucha plata?"
    print("✅ Correcto. Humano en el bucle + traza auditable: el agente propone, la persona decide y responde.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir conclusion:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *construyes* un agente: entiendes **por qué** el ciclo decidir → actuar → responder es una **traza
auditable**, qué es de verdad el ***tool use*** (el agente elige, la herramienta calcula), cuándo un **enrutador
por reglas** le gana a un LLM en **auditabilidad, costo y seguridad**, y las **dos formas en que los agentes
fallan**: elegir **mal** la herramienta (el error se propaga) y **encadenar** pasos (la fiabilidad se multiplica
hacia abajo).

La regla de oro que te llevas para el Estado: **el agente asiste; el humano decide y responde.** Usa lo más
simple que resuelva el problema, registra cada paso en la traza, pon un humano en el bucle donde se juegan
derechos, y recuerda que la responsabilidad **siempre es humana**. Eso distingue a quien *usa* un agente de
quien *se deja gobernar* por uno."""


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
