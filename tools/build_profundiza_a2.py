# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A2 (cruzar y resumir):
A2/profundiza.ipynb (estudiante) + A2/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A2-cruzar-y-resumir-tablas"

TITULO = """# A2 · Cruzar y resumir tablas — Profundización (opcional) 🔬

**Formación Pública — Pista A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A2 y quieres entender el *porqué* —no solo
el *cómo*—, aquí vas a un nivel más hondo: qué es **de verdad** cada tipo de cruce (`inner`, `left`,
`right`, `outer`) visto como **teoría de conjuntos**; por qué un cruce a veces te devuelve **más filas
de las que pusiste** (la temida **explosión** por llaves duplicadas), cómo **detectarla y evitarla**;
y qué hace `groupby` por dentro —el modelo **dividir-aplicar-combinar** (*split-apply-combine*)— y la
diferencia entre **agregar** (un valor por grupo) y **transformar** (un valor por fila).

Menos sintaxis nueva, más **pensamiento sobre datos relacionales**. Los ejercicios del final son más
conceptuales: calculas algo **y** eliges la interpretación correcta.

> Requisito: haber hecho `leccion.ipynb` de A2. Mismo caso: compras públicas reales de ChileCompra
> (`ordenes.csv` y `organismos.csv`)."""

CARGA = """import os, urllib.request
import pandas as pd

for archivo in ["ordenes.csv", "organismos.csv"]:
    if not os.path.exists(archivo):
        try:
            url = f"https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A2-cruzar-y-resumir-tablas/{archivo}"
            urllib.request.urlretrieve(url, archivo)
        except Exception:
            print(f"Si estás en Colab, sube {archivo} manualmente.")

df_ordenes = pd.read_csv("ordenes.csv")
df_organismos = pd.read_csv("organismos.csv")
print(f"Órdenes: {len(df_ordenes)} filas  |  Catálogo de organismos: {len(df_organismos)} filas")
print(f"Códigos (entcode) en órdenes: {sorted(df_ordenes['entcode'].unique())}")
print(f"Códigos (entcode) en catálogo: {sorted(df_organismos['entcode'].unique())}")"""

S1 = """## 1. Los cuatro cruces como **teoría de conjuntos**

En la lección viste `inner` y `left`. Hay cuatro tipos de cruce, y la forma más clara de entenderlos
es pensar en **conjuntos de llaves**. Imagina dos bolsas de códigos `entcode`:

- **I** = los códigos que están en la tabla **izquierda** (órdenes).
- **D** = los códigos que están en la tabla **derecha** (catálogo).

Cada tipo de `merge` decide **qué llaves sobreviven** al cruce:

| `how=` | Qué llaves conserva | En conjuntos | Analogía pública |
|---|---|---|---|
| `inner` | solo las que están en **ambas** | **intersección** (I ∩ D) | "solo órdenes que SÍ tienen ficha en el catálogo" |
| `left` | **todas** las de la izquierda | I (con D donde haya) | "todas las órdenes, tengan o no ficha" |
| `right` | **todas** las de la derecha | D (con I donde haya) | "todos los organismos del catálogo, compren o no" |
| `outer` | **todas** las de cualquiera | **unión** (I ∪ D) | "no perder absolutamente nada, de ninguna tabla" |

El indicador `indicator=True` agrega una columna `_merge` que dice de dónde salió cada fila:
`both` (estaba en las dos), `left_only` (solo izquierda) o `right_only` (solo derecha). Es la mejor
herramienta para **auditar** un cruce y entender qué se emparejó y qué quedó suelto."""

S1_CODE = """# outer = unión total + indicador de procedencia de cada fila
outer = pd.merge(df_ordenes, df_organismos, on="entcode", how="outer", indicator=True)
print("Procedencia de cada fila tras un cruce OUTER:")
print(outer["_merge"].value_counts())
print()
print("Conteo de filas por tipo de cruce (mismo par de tablas):")
for how in ["inner", "left", "right", "outer"]:
    n = len(pd.merge(df_ordenes, df_organismos, on="entcode", how=how))
    print(f"  how={how:<6} -> {n} filas")
print()
print("Lectura: 'left_only' son órdenes sin ficha en el catálogo (huérfanas);")
print("'right_only' serían organismos del catálogo sin ninguna orden de compra.")"""

S2 = """## 2. Cardinalidad: uno-a-muchos vs muchos-a-muchos

La pregunta clave **antes** de cruzar es: ¿cuántas veces se repite cada llave en cada tabla? A eso se
le llama **cardinalidad** de la relación.

- **Uno-a-muchos (1:N):** la llave es **única** en una tabla y se **repite** en la otra. Es el caso
  sano y más común. Aquí: cada `entcode` aparece **una sola vez** en el catálogo (cada organismo tiene
  **una** ficha), pero **muchas veces** en las órdenes (un organismo hace **muchas** compras). El
  catálogo es el lado "uno"; las órdenes, el lado "muchos".
- **Muchos-a-muchos (N:M):** la llave se **repite en ambas** tablas. Aquí es donde aparecen los
  problemas (lo vemos en la sección 3).

Por qué importa: en un cruce **1:N**, cada fila del lado "muchos" encuentra **exactamente una** pareja,
así que el número de filas del resultado es **predecible** (igual a las del lado "muchos", para las
llaves que emparejan). El catálogo bien hecho **debe** tener su llave única. Verifiquémoslo."""

S2_CODE = """# ¿Es la llave única en cada tabla? (.is_unique responde sí/no)
print("entcode único en el catálogo (organismos)?", df_organismos["entcode"].is_unique)
print("entcode único en las órdenes?            ", df_ordenes["entcode"].is_unique)
print()
# ¿Cuántas órdenes hay por cada organismo? (el lado 'muchos')
print("N° de órdenes por entcode:")
print(df_ordenes["entcode"].value_counts().sort_index())
print()
print("Catálogo único + órdenes repetidas = relación UNO-A-MUCHOS (1:N): el caso sano.")
print("En 1:N el cruce no infla filas: cada orden encuentra UNA sola ficha.")"""

S3 = """## 3. La **explosión** de filas: cuando la llave está duplicada

Aquí está la trampa más cara de los cruces. Si la llave **se repite en la tabla derecha** (el lado que
debería ser "uno"), `merge` empareja **cada fila izquierda con CADA fila derecha** que comparta la
llave. Es un **producto**: si un código tiene 3 órdenes a la izquierda y aparece 2 veces a la derecha,
salen **3 × 2 = 6** filas. La tabla **explota**.

¿Por qué es tan peligroso en el sector público? Porque al sumar `monto` después, **cada monto se cuenta
tantas veces como se duplicó la llave**, y el gasto reportado queda **inflado** sin que nadie lo note.
Un catálogo con una ficha repetida puede **duplicar** un gasto de miles de millones en un informe.

Lo provocamos a propósito: agregamos al catálogo una **ficha duplicada** de un organismo (mismo
`entcode`, otra región mal cargada) y miramos qué le pasa al cruce y a la suma de montos."""

S3_CODE = """# Catálogo SANO: contamos filas y montos de referencia
sano = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")
gasto_sano = sano["monto"].sum()

# Catálogo ROTO: duplicamos la ficha del organismo 6919 (misma llave, otra región)
fila_dup = df_organismos[df_organismos["entcode"] == 6919].copy()
fila_dup["region"] = "Region MAL CARGADA"
catalogo_roto = pd.concat([df_organismos, fila_dup], ignore_index=True)

roto = pd.merge(df_ordenes, catalogo_roto, how="inner", on="entcode")
gasto_roto = roto["monto"].sum()

print(f"Catálogo sano:  {len(sano)} filas tras el cruce | gasto total = {gasto_sano:,}")
print(f"Catálogo roto:  {len(roto)} filas tras el cruce | gasto total = {gasto_roto:,}")
print(f"\\nEl organismo 6919 tenía {(df_ordenes['entcode']==6919).sum()} órdenes;")
print(f"al duplicar su ficha, esas órdenes aparecen DOBLE y su gasto se contó dos veces.")
print(f"Inflación del gasto total: {gasto_roto - gasto_sano:,} pesos de más. Pura ilusión.")"""

S4 = """## 4. Detectar y **evitar** la explosión: `validate`

No hay que cazar la explosión a mano cada vez. `pd.merge` tiene un seguro: el parámetro **`validate`**,
que **verifica la cardinalidad antes de cruzar** y **lanza un error** si no se cumple. Opciones:

- `validate="one_to_many"` (`"1:m"`) → exige llave **única a la izquierda**.
- `validate="many_to_one"` (`"m:1"`) → exige llave **única a la derecha** (¡el caso del catálogo!).
- `validate="one_to_one"` (`"1:1"`) → única en ambas.

Como nuestras órdenes (izquierda) tienen la llave repetida y el catálogo (derecha) debería tenerla
única, lo correcto es **`validate="many_to_one"`**. Si el catálogo está sano, el cruce pasa; si está
roto (ficha duplicada), `merge` **se niega a cruzar** y te avisa, en vez de inflar tus números en
silencio. Es la diferencia entre un error **ruidoso** (bueno) y un error **silencioso** (peligroso)."""

S4_CODE = """# Con el catálogo SANO y validate='many_to_one': el cruce pasa sin problema
ok = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner", validate="many_to_one")
print(f"Catálogo sano + validate='many_to_one': OK, {len(ok)} filas. Cardinalidad correcta.")

# Con el catálogo ROTO: validate detecta el duplicado y LANZA un error (lo atrapamos)
fila_dup = df_organismos[df_organismos["entcode"] == 6919].copy()
catalogo_roto = pd.concat([df_organismos, fila_dup], ignore_index=True)
try:
    pd.merge(df_ordenes, catalogo_roto, on="entcode", how="inner", validate="many_to_one")
    print("(no debería llegar aquí)")
except Exception as e:
    print(f"\\nCatálogo roto + validate='many_to_one': merge se NEGÓ a cruzar.")
    print(f"  -> {type(e).__name__}: {e}")
    print("\\nEso es lo que queremos: un error RUIDOSO que frena la explosión a tiempo.")"""

S5 = """## 5. Qué hace `groupby` por dentro: **dividir-aplicar-combinar**

`groupby("region")["monto"].sum()` se siente mágico, pero por dentro sigue una receta de tres pasos
llamada **split-apply-combine** (dividir-aplicar-combinar):

1. **Dividir (*split*):** parte la tabla en grupos, uno por cada valor distinto de la llave de
   agrupación (una "pila" de filas por región).
2. **Aplicar (*apply*):** ejecuta una función **sobre cada pila por separado** (sumar el `monto`,
   contar filas, promediar…).
3. **Combinar (*combine*):** junta los resultados de cada grupo en una sola tabla de salida.

Entenderlo te libera de memorizar recetas: puedes aplicar **cualquier** función a cada grupo. Y con
`.agg()` puedes pedir **varias** agregaciones a la vez (suma, promedio, conteo) en una sola pasada,
que es como se arma una verdadera tabla resumen de gestión."""

S5_CODE = """cruce = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")

# 1) DIVIDIR: cuántas pilas (grupos) y de qué tamaño
g = cruce.groupby("region")
print("Grupos (regiones) y N° de órdenes en cada uno:")
print(g.size().sort_values(ascending=False))

# 2-3) APLICAR varias funciones a la vez y COMBINAR en una tabla resumen
resumen = cruce.groupby("region")["monto"].agg(
    n_ordenes="count", gasto_total="sum", gasto_promedio="mean"
).sort_values("gasto_total", ascending=False)
print("\\nTabla resumen por región (split-apply-combine con varias métricas):")
print(resumen.round(0).to_string())"""

S6 = """## 6. Agregar vs **transformar**: ¿un valor por grupo o uno por fila?

Hay dos formas de usar un `groupby`, y confundirlas es un error clásico:

- **Agregar (`.sum()`, `.mean()`, `.agg(...)`):** devuelve **un valor por grupo**. La tabla **encoge**:
  6 regiones → 6 filas. Sirve para el resumen final ("gasto por región").
- **Transformar (`.transform(...)`):** devuelve **un valor por cada fila original**, repitiendo el
  resultado del grupo a lo largo de todas sus filas. La tabla **conserva su tamaño**. Sirve para
  **comparar cada fila con su grupo** sin perder el detalle.

Ejemplo de gestión: ¿qué **porcentaje del gasto de su región** representa **cada orden**? Necesitas,
en la misma fila de cada orden, el total de su región. Eso es exactamente lo que hace `transform`:
te trae el total del grupo **pegado a cada fila**, para luego dividir."""

S6_CODE = """cruce = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")

# AGREGAR: una fila por región (la tabla encoge)
agregado = cruce.groupby("region")["monto"].sum()
print(f"Agregar -> {len(agregado)} filas (una por región). La tabla encoge.")

# TRANSFORMAR: el total de la región pegado a CADA orden (mismo tamaño que el cruce)
cruce["gasto_region"] = cruce.groupby("region")["monto"].transform("sum")
cruce["pct_de_su_region"] = (cruce["monto"] / cruce["gasto_region"] * 100).round(1)
print(f"Transformar -> {len(cruce)} filas (una por orden). La tabla NO cambia de tamaño.")
print("\\nCada orden con el peso que tiene DENTRO de su región:")
print(cruce[["codigo_oc", "region", "monto", "gasto_region", "pct_de_su_region"]].head(6).to_string(index=False))"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Asumir que un cruce nunca agrega filas.** Solo es cierto si el lado derecho tiene la llave **única**.
  Si está duplicada, el cruce **multiplica** (explota). Verifica con `.is_unique` o usa `validate=`.
- **Sumar montos después de una explosión.** Cada duplicado de llave **cuenta el monto de nuevo** e
  infla el total. Antes de sumar, confirma que el cruce no creció más de lo esperado.
- **No usar `validate=` en cruces de gestión.** Es una línea que convierte una explosión silenciosa en
  un error ruidoso. Para cruzar contra un catálogo, `validate="many_to_one"`.
- **Confundir agregar con transformar.** Si la tabla resultante "encogió" cuando esperabas el detalle,
  usaste `.sum()` donde querías `.transform("sum")` (o al revés).
- **Olvidar `right_only` / `left_only`.** `indicator=True` te dice qué quedó suelto en cada lado; no
  asumas que todo emparejó."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula** algo y te pide **elegir la interpretación
correcta** (una letra). Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: tipos de cruce / conjuntos
E1 = """## Ejercicio 01 · Los cruces como conjuntos
Cruza `df_ordenes` y `df_organismos` por `entcode` con cada `how` y guarda el N° de filas:

- `n_inner` = filas del cruce `how="inner"`.
- `n_left` = filas del cruce `how="left"`.

Luego elige en `conclusion` (letra) la lectura correcta:
- **A.** `inner` y `left` dan lo mismo: no hay órdenes huérfanas.
- **B.** `left` tiene **más** filas que `inner`: conserva las órdenes huérfanas (sin ficha en el catálogo)
  que `inner` descarta. La diferencia es la **intersección** vs **todo el lado izquierdo**.
- **C.** `inner` tiene más filas que `left` porque agrega los organismos sin órdenes."""
E1_TODO = """n_inner = None      # TODO: len del cruce inner
n_left = None       # TODO: len del cruce left
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """n_inner = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="inner"))
n_left = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="left"))
conclusion = "B"
"""
E1_CHK = """try:
    _ni = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="inner"))
    _nl = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="left"))
    _correcta = "B" if _nl > _ni else "A"
    assert n_inner is not None and int(n_inner) == _ni, f"n_inner debería ser {_ni}"
    assert n_left is not None and int(n_left) == _nl, f"n_left debería ser {_nl}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿cuál conserva las huérfanas?"
    print(f"✅ Correcto. inner={_ni} (intersección), left={_nl} (todo el lado izquierdo).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: cardinalidad
E2 = """## Ejercicio 02 · Cardinalidad de la relación
Determina la cardinalidad entre órdenes y catálogo:

- `unico_en_catalogo` = ¿es `entcode` único en `df_organismos`? (booleano, usa `.is_unique`).
- `unico_en_ordenes` = ¿es `entcode` único en `df_ordenes`? (booleano).

Elige en `conclusion` (letra) la lectura correcta:
- **A.** Es **uno-a-uno** (1:1): la llave es única en ambas tablas.
- **B.** Es **uno-a-muchos** (1:N): única en el catálogo, repetida en las órdenes (cada organismo hace
  muchas compras). Es el caso sano: el cruce no infla filas.
- **C.** Es **muchos-a-muchos** (N:M): se repite en ambas, hay riesgo de explosión."""
E2_TODO = """unico_en_catalogo = None   # TODO: df_organismos["entcode"].is_unique
unico_en_ordenes = None    # TODO: df_ordenes["entcode"].is_unique
conclusion = None          # TODO: "A", "B" o "C"
"""
E2_SOL = """unico_en_catalogo = df_organismos["entcode"].is_unique
unico_en_ordenes = df_ordenes["entcode"].is_unique
conclusion = "B"
"""
E2_CHK = """try:
    _uc = bool(df_organismos["entcode"].is_unique)
    _uo = bool(df_ordenes["entcode"].is_unique)
    if _uc and _uo: _correcta = "A"
    elif _uc and not _uo: _correcta = "B"
    else: _correcta = "C"
    assert unico_en_catalogo is not None and bool(unico_en_catalogo) == _uc, "Revisa unico_en_catalogo (.is_unique)"
    assert unico_en_ordenes is not None and bool(unico_en_ordenes) == _uo, "Revisa unico_en_ordenes (.is_unique)"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿en qué tabla se repite la llave?"
    print("✅ Correcto. Catálogo único + órdenes repetidas = uno-a-muchos (1:N), el caso sano.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: explosion
E3 = """## Ejercicio 03 · La explosión por llave duplicada
Te damos un catálogo **roto** (`catalogo_roto`) con la ficha del organismo 6919 **duplicada**. Cruza
`df_ordenes` con él y compara con el cruce sano:

- `n_sano` = filas del cruce de `df_ordenes` con `df_organismos` (inner).
- `n_roto` = filas del cruce de `df_ordenes` con `catalogo_roto` (inner).

Elige en `conclusion` (letra) la lectura correcta:
- **A.** Dan igual: duplicar una ficha del catálogo no afecta el cruce.
- **B.** `n_roto` > `n_sano`: las 3 órdenes del 6919 se emparejaron con las **2** fichas duplicadas,
  generando filas de más. Sumar `monto` ahora **inflaría** el gasto de ese organismo.
- **C.** `n_roto` < `n_sano`: duplicar una ficha **borra** órdenes."""
E3_PRE = """# (ya preparado) catálogo ROTO: ficha del 6919 duplicada
_dup = df_organismos[df_organismos["entcode"] == 6919].copy()
catalogo_roto = pd.concat([df_organismos, _dup], ignore_index=True)
"""
E3_TODO = E3_PRE + """n_sano = None       # TODO: filas del cruce inner con df_organismos
n_roto = None       # TODO: filas del cruce inner con catalogo_roto
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = E3_PRE + """n_sano = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="inner"))
n_roto = len(pd.merge(df_ordenes, catalogo_roto, on="entcode", how="inner"))
conclusion = "B"
"""
E3_CHK = """try:
    _ns = len(pd.merge(df_ordenes, df_organismos, on="entcode", how="inner"))
    _nr = len(pd.merge(df_ordenes, catalogo_roto, on="entcode", how="inner"))
    _correcta = "B" if _nr > _ns else ("C" if _nr < _ns else "A")
    assert n_sano is not None and int(n_sano) == _ns, f"n_sano debería ser {_ns}"
    assert n_roto is not None and int(n_roto) == _nr, f"n_roto debería ser {_nr}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿la ficha duplicada multiplica las órdenes del 6919?"
    print(f"✅ Correcto. sano={_ns}, roto={_nr}: la ficha duplicada hizo explotar {_nr-_ns} fila(s).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: aggregate vs transform
E4 = """## Ejercicio 04 · Agregar vs transformar
Parte del cruce sano `cruce = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")` (ya creado).

- `agregado` = gasto total por región con `groupby("region")["monto"].sum()`.
- `transformado` = el total de su región pegado a **cada orden**, con
  `cruce.groupby("region")["monto"].transform("sum")`.
- `n_agregado` = `len(agregado)` ; `n_transformado` = `len(transformado)`.

Elige en `conclusion` (letra) la lectura correcta:
- **A.** Tienen el mismo largo: agregar y transformar son lo mismo.
- **B.** `agregado` es **más corto** (una fila por región) y `transformado` tiene **una fila por orden**
  (mismo largo que el cruce): agregar **encoge** la tabla, transformar la **conserva**.
- **C.** `transformado` es más corto porque resume más."""
E4_PRE = """cruce = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")
"""
E4_TODO = E4_PRE + """agregado = None         # TODO: groupby region, suma de monto
transformado = None     # TODO: groupby region, transform("sum") de monto
n_agregado = None       # TODO: len(agregado)
n_transformado = None   # TODO: len(transformado)
conclusion = None       # TODO: "A", "B" o "C"
"""
E4_SOL = E4_PRE + """agregado = cruce.groupby("region")["monto"].sum()
transformado = cruce.groupby("region")["monto"].transform("sum")
n_agregado = len(agregado)
n_transformado = len(transformado)
conclusion = "B"
"""
E4_CHK = """try:
    _ag = cruce.groupby("region")["monto"].sum()
    _tr = cruce.groupby("region")["monto"].transform("sum")
    _correcta = "B" if (len(_ag) < len(_tr) and len(_tr) == len(cruce)) else "A"
    assert agregado is not None and len(agregado) == len(_ag), f"agregado debería tener {len(_ag)} filas"
    assert transformado is not None and len(transformado) == len(_tr), f"transformado debería tener {len(_tr)} filas"
    assert int(n_agregado) == len(_ag), "n_agregado no coincide"
    assert int(n_transformado) == len(_tr), "n_transformado no coincide"
    assert str(conclusion).strip().upper() == _correcta, "Revisa: ¿cuál devuelve un valor por grupo y cuál uno por fila?"
    print(f"✅ Correcto. Agregar -> {len(_ag)} filas (encoge); transformar -> {len(_tr)} filas (conserva).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo cruzas y resumes tablas: entiendes **por qué** funcionan. Sabes que cada `how` es una
**operación de conjuntos** sobre las llaves; reconoces la **cardinalidad** de una relación antes de
cruzar; sabes que una llave **duplicada** hace **explotar** las filas e **inflar** los montos, y cómo
**blindarte** con `validate=`; entiendes `groupby` como **dividir-aplicar-combinar**; y distingues
**agregar** (un valor por grupo) de **transformar** (un valor por fila).

La regla de oro que te llevas: **antes de cruzar, pregunta por la cardinalidad; después de cruzar,
verifica que el N° de filas sea el esperado.** Eso evita el error más caro de un informe público:
**duplicar gasto sin darse cuenta.**"""


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
