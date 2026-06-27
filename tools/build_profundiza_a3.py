# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A3 (limpieza de datos):
A3/profundiza.ipynb (estudiante) + A3/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A3-limpieza-de-datos"

TITULO = """# A3 · Limpieza de datos — Profundización (opcional) 🔬

**Formación Pública — Capa A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A3 y quieres entender el *porqué* —no solo
el *cómo*—, aquí vas un nivel más hondo. En la lección aprendiste a *ejecutar* la limpieza (strip,
capitalize, dropna, drop_duplicates). Acá vas a entender lo que **nadie te cuenta**: que limpiar
**no es neutral**, que cada decisión introduce un **sesgo**, que un faltante puede esconder
información, y que un dato sin **procedencia** no se puede defender ante una autoridad.

Cubrimos: los tres tipos de dato faltante (**MCAR / MAR / MNAR**), el **sesgo** que mete cada estrategia
(eliminar filas vs. imputar media/mediana), por qué **limpiar codifica supuestos**, las **trampas de la
normalización de texto**, y la **procedencia / linaje** del dato (*garbage in, garbage out*).

Menos sintaxis nueva, más **criterio**. Los ejercicios del final son más conceptuales.

> Requisito: haber hecho `leccion.ipynb` de A3. Mismo caso: compras públicas (ChileCompra), `compras_rubros.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np

if not os.path.exists("compras_rubros.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A3-limpieza-de-datos/compras_rubros.csv"
        urllib.request.urlretrieve(url, "compras_rubros.csv")
    except Exception:
        print("Si estás en Colab, sube compras_rubros.csv manualmente.")

def cargar():
    \"\"\"Devuelve una copia fresca del export crudo (siempre igual).\"\"\"
    return pd.read_csv("compras_rubros.csv")

df = cargar()
print(f"Export crudo: {len(df)} filas | faltantes en monto: {df['monto'].isnull().sum()} | duplicadas: {df.duplicated().sum()}")"""

S1 = """## 1. Limpiar NO es neutral: cada decisión codifica un supuesto

En la lección, limpiar parecía una secuencia mecánica de pasos correctos. La verdad incómoda es que
**toda limpieza es una cadena de decisiones**, y cada decisión **codifica un supuesto** sobre el mundo.

Mira la lección de nuevo. Cuando hiciste `df.dropna(subset=["monto"])` para quitar el rubro sin monto,
asumiste algo: *"ese rubro no me importa para el análisis"*. Pero `Tecnologías de la información` es un
rubro real con gasto real; lo que faltaba era **el dato**, no el gasto. Al borrar la fila, no eliminaste
un problema: **eliminaste un rubro entero del informe**. El total de "rubros más comprados" pasó de 6 a 5
sin que nadie lo decidiera explícitamente.

La frase clave de este cuaderno:

> **Los datos no se "limpian solos". Alguien decide qué es ruido y qué es señal — y esa persona eres tú.**

Eso no significa que limpiar esté mal. Significa que cada paso debe ser **consciente, justificable y
documentado**. Veamos cómo una misma tabla cruda produce números distintos según qué supuesto adoptes."""

S1_CODE = """df = cargar()
total_crudo_rubros = df["rubro"].nunique()

# Supuesto A: "el faltante no importa" -> borro la fila (lo que hizo la lección)
opcion_borrar = df.dropna(subset=["monto"])

# Supuesto B: "el rubro importa aunque falte el monto" -> lo conservo y marco el monto como desconocido
opcion_conservar = df.copy()  # mantengo la fila; el monto sigue siendo NaN (desconocido)

print(f"Rubros distintos en el crudo:           {total_crudo_rubros}")
print(f"Rubros que sobreviven si BORRO faltante: {opcion_borrar['rubro'].nunique()}")
print(f"Rubros que sobreviven si los CONSERVO:   {opcion_conservar['rubro'].nunique()}")
print("\\nMisma tabla, dos supuestos, dos universos de análisis distintos.")
print("Ninguno es 'el correcto': depende de la pregunta. Pero hay que ELEGIR a conciencia.")"""

S2 = """## 2. Los tres tipos de dato faltante: MCAR, MAR y MNAR

No todos los faltantes son iguales. La estadística distingue **tres mecanismos** según *por qué* falta
el dato. Entenderlos es lo que separa borrar a ciegas de decidir con criterio.

- **MCAR** — *Missing Completely At Random* (falta completamente al azar). El dato falta por puro azar,
  sin relación con nada. Ejemplo: a un funcionario se le cortó internet justo al cargar una fila. Borrar
  estas filas **no introduce sesgo** (solo pierdes tamaño de muestra).

- **MAR** — *Missing At Random* (falta al azar, *condicionado* a otra variable observable). Falta más en
  ciertos grupos, pero el grupo **sí lo conoces**. Ejemplo: los organismos pequeños declaran el monto con
  menos frecuencia. Si borras, **subrepresentas a los organismos pequeños** — pero como tienes la columna
  "tamaño de organismo", puedes **corregirlo**.

- **MNAR** — *Missing Not At Random* (falta de forma no aleatoria, ligada al **propio valor que falta**).
  El dato falta *precisamente por su valor*. Ejemplo: los montos **más altos** se omiten "para no llamar la
  atención". Aquí borrar es **peligrosísimo**: estarías eliminando justo los casos grandes y tu total
  quedaría falsamente bajo. Y lo peor: **no puedes detectarlo solo mirando los datos**, porque el dato que
  lo probaría es justo el que falta.

> Regla de bolsillo: **MCAR** → borrar es razonable. **MAR** → borrar sesga, pero es corregible. **MNAR**
> → borrar miente, y casi nunca te das cuenta. En datos públicos autodeclarados, **MNAR es más común de lo
> que parece**. Simulemos los tres para *ver* el sesgo."""

S2_CODE = """rng = np.random.default_rng(7)
# Universo simulado: 200 órdenes de compra con su monto real (ilustrativo)
montos = rng.integers(100_000, 5_000_000, size=200)
verdad = montos.mean()  # la media REAL que querríamos estimar

# MCAR: ocultamos 40 montos al azar
mcar = montos.copy().astype(float)
mcar[rng.choice(200, 40, replace=False)] = np.nan

# MNAR: ocultamos los 40 montos MÁS ALTOS (faltan por su propio valor)
mnar = montos.copy().astype(float)
idx_altos = np.argsort(montos)[-40:]
mnar[idx_altos] = np.nan

print(f"Media REAL (sin faltantes):        {verdad:,.0f}")
print(f"Media tras BORRAR faltantes MCAR:  {np.nanmean(mcar):,.0f}  (≈ igual: borrar no sesga)")
print(f"Media tras BORRAR faltantes MNAR:  {np.nanmean(mnar):,.0f}  (¡MUY por debajo! borrar mintió)")"""

S3 = """## 3. El sesgo de imputar: media, mediana y la varianza que desaparece

"Imputar" es rellenar un faltante con un valor calculado. La lección te advirtió *"nunca inventes un
valor"*; aquí está el **mecanismo exacto** del daño, para que sepas *por qué*.

Imputar con la **media** (`fillna(media)`) tiene dos efectos perversos:

1. **No agrega información**, solo la finge. Estás poniendo en la celda vacía "el promedio de los demás",
   que no es el dato real.
2. **Aplasta la varianza.** Como metes muchos valores idénticos (todos = la media), los datos se ven
   *artificialmente más concentrados* de lo que son. La desviación estándar **baja sola**, y eso te hará
   creer que el gasto es más parejo de lo que realmente es.

Imputar con la **mediana** es más **robusto** ante extremos (no se deja arrastrar por un monto gigante),
pero **comparte el segundo problema**: también aplasta la varianza.

> El punto profundo: **imputar cambia la forma de la distribución.** A veces es aceptable (necesitas la
> columna completa para un modelo); a veces es inaceptable (vas a reportar la dispersión del gasto). La
> decisión depende de **para qué** usarás el dato — nunca es automática."""

S3_CODE = """rng = np.random.default_rng(3)
real = rng.integers(100_000, 5_000_000, size=100).astype(float)
de_real = real.std()

# Ocultamos 30 valores y los imputamos con la media de los que quedan
con_faltante = real.copy()
con_faltante[rng.choice(100, 30, replace=False)] = np.nan
media_observada = np.nanmean(con_faltante)
imputado = np.where(np.isnan(con_faltante), media_observada, con_faltante)

print(f"Desviación estándar REAL:            {de_real:,.0f}")
print(f"Desviación estándar tras IMPUTAR media: {imputado.std():,.0f}")
print(f"\\nLa dispersión se redujo un {100*(1 - imputado.std()/de_real):.0f}%: la varianza 'desapareció'.")
print("Reportar esa DE haría creer que el gasto es mucho más parejo de lo que es.")"""

S4 = """## 4. Trampas de la normalización de texto

`.str.strip().str.capitalize()` parecía inofensivo en la lección. Pero normalizar texto es **destructivo**:
transforma valores, y a veces **funde cosas que NO eran iguales** o **rompe** lo que estaba bien.

Trampas reales que muerden en datos públicos:

- **`.str.capitalize()` arruina las siglas y los nombres propios compuestos.** `"SENCE"` → `"Sence"`,
  `"MOP"` → `"Mop"`, `"Servicio de Impuestos Internos"` → `"Servicio de impuestos internos"`. Para una
  persona dará lo mismo; para un informe oficial, escribir mal un nombre propio resta credibilidad.

- **Colapsar mayúsculas puede *fundir* categorías distintas.** Si `"PYME"` (un tipo de proveedor) y
  `"Pyme"` (otra cosa en tu tabla) coexistieran, al bajar todo a minúsculas se mezclarían **dos
  categorías reales en una sola**. Normalizar de menos deja duplicados; normalizar de más **borra
  distinciones verdaderas**.

- **Los acentos y los caracteres invisibles.** `"Tecnología"` y `"Tecnologia"` (sin tilde) son distintos
  para el computador. Y existen espacios "no visibles" (tabuladores, espacios duros) que `.strip()` a
  veces no quita. Lo que ves en pantalla **no siempre es lo que hay en la celda**.

> Moraleja: normaliza **lo justo y necesario para tu pregunta**, y **revisa el resultado** con
> `.unique()` antes de seguir. La normalización correcta para un caso puede ser un error en otro."""

S4_CODE = """# Caso real: aplicar capitalize() a una columna con siglas las destruye
ejemplo = pd.Series(["SENCE", "MOP", "Servicio de Impuestos Internos", "  ChileCompra  "])
print("Original              -> capitalize()")
for v in ejemplo:
    print(f"{v!r:35} -> {v.strip().capitalize()!r}")

print("\\nEn el dataset real, capitalize() también 'baja' los acentos de las MAYÚSCULAS:")
df = cargar()
rubro_ejemplo = df["rubro"].iloc[3]        # 'EQUIPAMIENTO Y SUMINISTROS MÉDICOS'
print("Antes:  ", repr(rubro_ejemplo))
print("Después:", repr(rubro_ejemplo.strip().capitalize()))"""

S5 = """## 5. Procedencia, linaje y reproducibilidad: *garbage in, garbage out*

El principio más viejo de la computación: **basura entra, basura sale** (*garbage in, garbage out*).
Ningún análisis brillante salva un dato de origen malo. Por eso, en el sector público, importa tanto
*de dónde viene* el dato como *qué dice*.

Tres conceptos que te van a salvar de un papelón ante una autoridad:

- **Procedencia (*provenance*)**: el **origen** del dato. ¿Quién lo generó, cuándo, con qué definición?
  El propio portal de ChileCompra advierte que los datos van *"tal como fueron ingresados por los
  usuarios"*. Saber eso **cambia cómo lo interpretas** (son autodeclarados, no auditados).

- **Linaje (*lineage*)**: la **cadena de transformaciones** desde el crudo hasta tu número final. Cada
  `dropna`, cada `capitalize`, cada conversión es un eslabón. Si no anotas la cadena, **nadie (ni tú en
  tres meses) puede reconstruir cómo llegaste a esa cifra**.

- **Reproducibilidad**: que **otra persona, con el archivo crudo y tu código, obtenga exactamente el mismo
  resultado**. Por eso en la lección la limpieza vive en una **función** (`limpiar(df)`) y no en pasos
  sueltos a mano: una función es linaje ejecutable y reproducible.

> En un análisis público defendible, la cifra final **viene acompañada de su linaje**: "partí del export
> oficial X del día Y; eliminé 1 fila duplicada y 1 con monto faltante; convertí montos quitando '\\$' y
> puntos". Eso es lo que distingue un dato **auditable** de un número que apareció por arte de magia."""

S5_CODE = """def limpiar_con_linaje(df):
    \"\"\"Limpia y devuelve (tabla_limpia, bitácora). La bitácora ES el linaje.\"\"\"
    log = []
    out = df.copy()
    log.append(f"crudo: {len(out)} filas")

    out["rubro"] = out["rubro"].str.strip().str.capitalize()
    log.append("rubro: strip + capitalize")

    antes = len(out); out = out.dropna(subset=["monto"])
    log.append(f"dropna(monto): -{antes - len(out)} fila(s)")

    antes = len(out); out = out.drop_duplicates()
    log.append(f"drop_duplicates: -{antes - len(out)} fila(s)")

    out["monto"] = out["monto"].str.replace("$", "", regex=False).str.replace(".", "", regex=False).astype(int)
    log.append("monto: texto -> entero (quité '$' y puntos)")
    return out, log

limpio, bitacora = limpiar_con_linaje(cargar())
print("LINAJE de la cifra final:")
for paso in bitacora:
    print("  -", paso)
print(f"\\nGasto total auditable (5 rubros): ${limpio['monto'].sum():,.0f}".replace(",", "."))"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Borrar filas con faltantes sin preguntarse el mecanismo.** Si el faltante es MNAR (falta por su propio valor), borrar **sesga el resultado** y casi nunca te das cuenta.
- **Imputar con la media "porque sí".** Aplasta la varianza: reportarás una dispersión falsamente baja. Decide según **para qué** usas la columna.
- **Aplicar `capitalize()` a ciegas.** Destroza siglas y nombres propios (`SENCE` → `Sence`). Normaliza lo justo y revisa con `.unique()`.
- **Normalizar de más.** Colapsar mayúsculas/acentos puede **fundir categorías que eran distintas**. Perder una distinción real es peor que dejar un duplicado.
- **Reportar una cifra sin su linaje.** Un número sin procedencia ni cadena de transformaciones no es auditable: ante una autoridad, no lo puedes defender.
- **Confundir "celda vacía" con "cero".** `NaN` significa *no sé*, no *cero*. `fillna(0)` en montos miente."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: calculas algo **y** eliges la interpretación correcta (una letra).
Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: mecanismo de faltante (MCAR vs MNAR) y su sesgo
E1 = """## Ejercicio 01 · El sesgo del faltante (MCAR vs MNAR)
Te damos un universo simulado de 150 montos. Vas a comparar qué pasa al **borrar** los faltantes según
el mecanismo.

- Calcula `media_real` = media de `universo` (sin faltantes).
- Calcula `media_mnar` = media (ignorando NaN) de `universo_mnar`, donde se ocultaron los montos **más altos**.
- Luego elige en `conclusion` (letra) la lectura correcta:
  - **A.** Borrar los faltantes MNAR no afecta: `media_mnar` ≈ `media_real`.
  - **B.** Borrar faltantes MNAR **subestima** el total: `media_mnar` queda muy por **debajo** de `media_real`,
    porque eliminamos justo los casos grandes.
  - **C.** Borrar faltantes MNAR **sobreestima**: `media_mnar` queda por encima de `media_real`.

Pista: `np.nanmean(...)` calcula la media ignorando los NaN."""
E1_SETUP = """_rng = np.random.default_rng(11)
universo = _rng.integers(100_000, 5_000_000, size=150).astype(float)
universo_mnar = universo.copy()
universo_mnar[np.argsort(universo)[-30:]] = np.nan  # ocultamos los 30 MÁS altos (MNAR)
print("Universo listo:", len(universo), "montos | faltantes MNAR:", int(np.isnan(universo_mnar).sum()))"""
E1_TODO = """media_real = None    # TODO: media de universo
media_mnar = None    # TODO: np.nanmean de universo_mnar
conclusion = None    # TODO: "A", "B" o "C"
"""
E1_SOL = """media_real = universo.mean()
media_mnar = np.nanmean(universo_mnar)
conclusion = "B"
"""
E1_CHK = """try:
    _real = universo.mean()
    _mnar = np.nanmean(universo_mnar)
    _correcta = "B" if _mnar < _real * 0.97 else ("C" if _mnar > _real * 1.03 else "A")
    assert media_real is not None and abs(media_real - _real) < 1, "Revisa media_real"
    assert media_mnar is not None and abs(media_mnar - _mnar) < 1, "Revisa media_mnar (usa np.nanmean)"
    assert str(conclusion).strip().upper() == _correcta, "¿Qué montos eliminamos? Mira si media_mnar quedó por debajo."
    print(f"✅ Correcto. Real={_real:,.0f} vs MNAR={_mnar:,.0f}: borrar MNAR subestima el gasto.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: imputar media aplasta varianza
E2 = """## Ejercicio 02 · Imputar con la media aplasta la varianza
Sobre el arreglo `datos` (100 montos, 25 ocultos como NaN):

- Calcula `de_observada` = desviación estándar de los valores **no faltantes** (`np.nanstd(datos)`).
- Crea `imputado` reemplazando cada NaN por la **media observada** (`np.nanmean(datos)`), y calcula
  `de_imputada` = `imputado.std()`.
- Elige en `conclusion` la interpretación correcta:
  - **A.** `de_imputada` es **mayor** que `de_observada`: imputar agrega dispersión.
  - **B.** `de_imputada` es **menor** que `de_observada`: meter muchos valores iguales a la media
    **aplasta la varianza** (la dispersión se ve falsamente más baja).
  - **C.** Son iguales: imputar la media no afecta la dispersión.

Pista: `np.where(np.isnan(datos), media, datos)` reemplaza los NaN por `media`."""
E2_SETUP = """_rng = np.random.default_rng(5)
datos = _rng.integers(100_000, 5_000_000, size=100).astype(float)
datos[_rng.choice(100, 25, replace=False)] = np.nan
print("Datos listos:", len(datos), "montos | faltantes:", int(np.isnan(datos).sum()))"""
E2_TODO = """de_observada = None   # TODO: np.nanstd(datos)
imputado = None       # TODO: np.where(np.isnan(datos), np.nanmean(datos), datos)
de_imputada = None    # TODO: imputado.std()
conclusion = None     # TODO: "A", "B" o "C"
"""
E2_SOL = """de_observada = np.nanstd(datos)
imputado = np.where(np.isnan(datos), np.nanmean(datos), datos)
de_imputada = imputado.std()
conclusion = "B"
"""
E2_CHK = """try:
    _obs = np.nanstd(datos)
    _imp = np.where(np.isnan(datos), np.nanmean(datos), datos).std()
    _correcta = "B" if _imp < _obs else ("A" if _imp > _obs else "C")
    assert de_observada is not None and abs(de_observada - _obs) < 1, "Revisa de_observada (np.nanstd)"
    assert de_imputada is not None and abs(de_imputada - _imp) < 1, "Revisa de_imputada"
    assert str(conclusion).strip().upper() == _correcta, "Compara las dos desviaciones: ¿cuál quedó menor?"
    print(f"✅ Correcto. DE observada={_obs:,.0f} -> imputada={_imp:,.0f}: la varianza se aplastó.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: trampa de capitalize sobre siglas
E3 = """## Ejercicio 03 · La trampa de `capitalize()` con siglas
Tienes una lista de siglas y nombres de organismos. Vas a medir **cuántos nombres se deforman** al aplicar
`.str.strip().str.capitalize()`.

- Crea `normalizados` aplicando `.str.strip().str.capitalize()` a la columna `organismo`.
- Guarda en `n_deformados` cuántos valores **cambiaron** respecto del original ya sin espacios
  (compara `org["organismo"].str.strip()` con `normalizados`).
- Elige en `conclusion`:
  - **A.** Ningún nombre se deformó: `capitalize()` es seguro para siglas.
  - **B.** Varios se deformaron (`SENCE`→`Sence`, etc.): `capitalize()` **no** sirve para siglas/nombres
    propios; hay que normalizar con criterio, no a ciegas.

Pista: `(serie_a != serie_b).sum()` cuenta cuántos elementos difieren."""
E3_SETUP = """org = pd.DataFrame({"organismo": [
    "SENCE", "MOP", "  ChileCompra ", "Servicio de Impuestos Internos", "JUNAEB"
]})
print(org["organismo"].tolist())"""
E3_TODO = """normalizados = None   # TODO: org["organismo"].str.strip().str.capitalize()
n_deformados = None   # TODO: cuántos difieren respecto de org["organismo"].str.strip()
conclusion = None     # TODO: "A" o "B"
"""
E3_SOL = """normalizados = org["organismo"].str.strip().str.capitalize()
n_deformados = int((org["organismo"].str.strip() != normalizados).sum())
conclusion = "B"
"""
E3_CHK = """try:
    _norm = org["organismo"].str.strip().str.capitalize()
    _n = int((org["organismo"].str.strip() != _norm).sum())
    _correcta = "B" if _n > 0 else "A"
    assert normalizados is not None and list(normalizados) == list(_norm), "Revisa 'normalizados'"
    assert n_deformados is not None and int(n_deformados) == _n, f"Esperaba {_n} nombres deformados"
    assert str(conclusion).strip().upper() == _correcta, "¿`SENCE` sigue siendo `SENCE` tras capitalize()?"
    print(f"✅ Correcto. {_n} de {len(org)} nombres se deformaron: capitalize() no sirve a ciegas para siglas.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: limpiar no es neutral / linaje (conceptual)
E4 = """## Ejercicio 04 · Limpiar no es neutral (conceptual)
Vuelve al export crudo (`cargar()`). La lección, al hacer `dropna(subset=["monto"])`, **eliminó el rubro
`Tecnologías de la información`** porque le faltaba el monto. Una autoridad te pide "el listado de los
rubros más comprados por el Estado en 2026".

- Calcula `rubros_crudo` = N° de rubros distintos en el **crudo** (`cargar()["rubro"].nunique()`).
- Calcula `rubros_tras_dropna` = N° de rubros distintos **después** de `dropna(subset=["monto"])`.

Luego elige en `conclusion` la lectura correcta:
- **A.** Da igual: `dropna` es un paso técnico neutro, no afecta el contenido del informe.
- **B.** `dropna` **eliminó un rubro real** del informe (no solo un dato faltante). Limpiar codificó un
  supuesto ("ese rubro no importa") que **nadie decidió explícitamente**; hay que documentarlo o conservar
  la fila marcando el monto como desconocido.
- **C.** El crudo y el limpio tienen el mismo número de rubros, así que no se perdió nada.

*(Opcional, no se corrige): en `reflexion` escribe qué le dirías a la autoridad sobre el rubro eliminado.)*"""
E4_TODO = """rubros_crudo = None         # TODO: cargar()["rubro"].nunique()
rubros_tras_dropna = None   # TODO: nunique tras dropna(subset=["monto"])
conclusion = None           # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """rubros_crudo = cargar()["rubro"].nunique()
rubros_tras_dropna = cargar().dropna(subset=["monto"])["rubro"].nunique()
conclusion = "B"
reflexion = "Le diría que falta el monto de Tecnologías de la información: el rubro existe, lo que falta es el dato, y conviene reportarlo aparte en vez de omitirlo."
"""
E4_CHK = """try:
    _crudo = cargar()["rubro"].nunique()
    _tras = cargar().dropna(subset=["monto"])["rubro"].nunique()
    _correcta = "B" if _tras < _crudo else "C"
    assert rubros_crudo is not None and int(rubros_crudo) == _crudo, f"rubros_crudo debería ser {_crudo}"
    assert rubros_tras_dropna is not None and int(rubros_tras_dropna) == _tras, f"rubros_tras_dropna debería ser {_tras}"
    assert str(conclusion).strip().upper() == _correcta, "¿El dropna dejó el mismo número de rubros, o eliminó uno real?"
    print(f"✅ Correcto. De {_crudo} rubros a {_tras}: dropna borró un rubro REAL. Limpiar no es neutral.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *ejecutas* una limpieza: entiendes que **cada paso codifica un supuesto**, que un faltante
tiene un **mecanismo** (MCAR/MAR/MNAR) que cambia si borrar es honesto o engañoso, que **imputar
distorsiona** la forma de los datos, que normalizar texto puede **fundir o romper** categorías, y que una
cifra sin **procedencia ni linaje** no se puede defender.

La regla de oro que te llevas: **antes de limpiar, pregunta *por qué* falta el dato y *para qué* vas a usar
la columna; y deja siempre el rastro de lo que hiciste.** Eso distingue a quien *limpia datos* de quien
*manipula datos sin querer*."""


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
        md(ERRORES, "p12"), md(EJ_HEADER, "p13"),
        md(E1, "p14"), code(E1_SETUP, "p15"), code(g(E1_SOL, E1_TODO), "p16"), code(E1_CHK, "p17"),
        md(E2, "p18"), code(E2_SETUP, "p19"), code(g(E2_SOL, E2_TODO), "p20"), code(E2_CHK, "p21"),
        md(E3, "p22"), code(E3_SETUP, "p23"), code(g(E3_SOL, E3_TODO), "p24"), code(E3_CHK, "p25"),
        md(E4, "p26"), code(g(E4_SOL, E4_TODO), "p27"), code(E4_CHK, "p28"),
        md(CIERRE, "p29"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "profundiza.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "profundiza_solucion.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Generados: profundiza.ipynb y profundiza_solucion.ipynb en", BASE)
