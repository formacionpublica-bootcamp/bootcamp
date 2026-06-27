# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A1 (exploración con pandas):
A1/profundiza.ipynb (estudiante) + A1/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A1-exploracion-con-pandas"

TITULO = """# A1 · Exploración con pandas — Profundización (opcional) 🔬

**Formación Pública — Capa A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A1 y quieres entender el *porqué* —no solo
el *cómo*— de pandas, aquí vas un nivel más hondo. En la lección aprendiste a cargar, inspeccionar,
seleccionar, filtrar y resumir. Ahora vamos por debajo del capó: **cómo está hecho un DataFrame**,
por qué pandas es **rápido** sin escribir bucles, cómo funcionan de verdad **`.loc` / `.iloc`** y las
**máscaras booleanas**, qué son las **vistas vs. copias** (y ese molesto `SettingWithCopyWarning`),
qué guarda cada columna según su **tipo de dato** (`dtype`) y cuánta **memoria** ocupa, y la semántica
del **valor faltante (`NaN`)**.

Menos sintaxis nueva, más **modelo mental correcto**. Los ejercicios del final son más conceptuales.

> Requisito: haber hecho `leccion.ipynb` de A1. Mismo dataset: establecimientos del Servicio Médico
> Legal (`establecimientos.csv`)."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np

if not os.path.exists("establecimientos.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A1-exploracion-con-pandas/establecimientos.csv"
        urllib.request.urlretrieve(url, "establecimientos.csv")
    except Exception:
        print("Si estás en Colab, sube establecimientos.csv manualmente.")

df = pd.read_csv("establecimientos.csv")
print(f"{len(df)} establecimientos | {df.shape[1]} columnas | {df['region'].nunique()} regiones")
df.head(3)"""

S1 = """## 1. Qué es un DataFrame por dentro: Series, índice y columnas

En la lección dijimos que un **DataFrame** es como una planilla Excel en memoria. Eso es cierto, pero
por dentro tiene una estructura muy precisa que conviene entender:

- Cada **columna** es una **Series**: una secuencia de valores **todos del mismo tipo** (todas
  latitudes son números decimales, todos los nombres de comuna son texto), acompañada de una
  **etiqueta de fila** llamada **índice** (*index*).
- El **DataFrame** es, en esencia, un conjunto de Series que **comparten el mismo índice** (las mismas
  etiquetas de fila). Por eso puedes alinear y combinar columnas sin esfuerzo: pandas las pega por su
  índice, no por el orden en que aparecen.
- El **índice no es lo mismo que una columna**. Es la "guía telefónica" que pandas usa para encontrar
  filas. Al cargar un CSV, pandas crea por defecto un índice numérico `0, 1, 2, …` (un `RangeIndex`).

La analogía pública: piensa en el **RUT** como índice de un padrón. La columna "nombre" y la columna
"comuna" son distintas, pero ambas se ordenan por el mismo RUT. Ese RUT (el índice) es lo que te
permite cruzar tablas sin equivocarte de persona."""

S1_CODE = """col = df["region"]          # una sola columna -> Series
print("Tipo de una columna:", type(col).__name__)
print("Tipo del df entero: ", type(df).__name__)

print("\\nEl índice (etiquetas de fila) del DataFrame:")
print(df.index)

print("\\nUna Series trae DOS cosas: el índice (izquierda) y los valores (derecha):")
print(df["comuna"].head(3))"""

S2 = """## 2. Vectorización: por qué pandas vuela sin bucles `for`

En el prework recorrías un CSV fila por fila con un `for`. pandas casi nunca necesita eso, y por una
razón de fondo: la **vectorización**.

- Cuando escribes `df["latitud"] * -1` o `df["latitud"] > -33`, pandas **no** hace un bucle lento en
  Python. Por debajo, los valores de una columna numérica (como `latitud`) viven en un bloque de memoria
  contiguo (un *array* de **NumPy**), y la operación se ejecuta de un golpe en **código compilado en C**,
  sobre toda la columna a la vez. (Las columnas de texto, tipo `object`, no son un bloque contiguo de
  números, pero igual evitan el bucle Python explícito con los métodos vectorizados de `.str`.)
- Un bucle `for` en Python interpreta cada paso uno por uno (lento). La operación vectorizada delega el
  trabajo pesado a C (rápido). La diferencia en datasets grandes es de **segundos vs. minutos**.

La regla mental: **si te descubres escribiendo un `for` sobre las filas de un DataFrame, casi siempre
hay una operación de columna entera que hace lo mismo, más corto y mucho más rápido.** Comparémoslo."""

S2_CODE = """import time

# IMPORTANTE: con solo 38 filas el costo de arrancar pandas/NumPy pesa MÁS que el
# trabajo real, y el bucle puede incluso ganar (el overhead no se amortiza). Para que
# la diferencia se vea de verdad, medimos sobre una Serie sintética GRANDE (1 millón
# de valores), que es el escenario realista donde la vectorización importa.
grande = pd.Series(range(1_000_000), dtype="float64")

# Forma LENTA (estilo prework): bucle fila por fila en Python interpretado
t0 = time.perf_counter()
positivas = []
for valor in grande:
    positivas.append(valor * -1)   # convertir a latitud "positiva" (hemisferio sur)
t_bucle = time.perf_counter() - t0

# Forma VECTORIZADA (estilo pandas): toda la columna de un golpe, en C compilado
t0 = time.perf_counter()
positivas_vec = grande * -1
t_vec = time.perf_counter() - t0

print(f"Resultado idéntico: {list(positivas)[:3]}  ==  {list(positivas_vec)[:3]}")
print(f"\\nMidiendo sobre {len(grande):,} valores:")
print(f"Bucle for:      {t_bucle*1e3:8.1f} milisegundos")
print(f"Vectorizado:    {t_vec*1e3:8.1f} milisegundos")
print(f"La vectorización fue ~{t_bucle/t_vec:.0f}x más rápida.")
print("\\nNota: con pocas filas (las 38 del dataset) el overhead de pandas puede invertir")
print("este resultado y hacer ganar al bucle; la ventaja vectorizada aparece con muchos datos.")"""

S3 = """## 3. `.loc` vs `.iloc`: por etiqueta vs por posición

Para seleccionar filas (y columnas) con precisión, pandas te da **dos accesos distintos** que la gente
suele confundir:

- **`.loc[fila, columna]`** selecciona por **etiqueta** (el nombre del índice y el nombre de la
  columna). `df.loc[5, "comuna"]` = "la fila cuya etiqueta de índice es 5, columna comuna".
- **`.iloc[fila, columna]`** selecciona por **posición** entera, como en una lista. `df.iloc[5, 2]` =
  "la sexta fila, tercera columna", sin importar cómo se llamen.

Detalle clave que confunde a todos: **`.loc` incluye el extremo final del rango y `.iloc` no.**
`df.loc[0:2]` te da las filas con etiqueta 0, 1 **y 2** (tres filas); `df.iloc[0:2]` te da las
posiciones 0 y 1 (dos filas), igual que el *slicing* normal de Python.

Cuándo usar cada uno: usa **`.loc`** cuando piensas en términos de *qué* fila/columna (nombres, lo
habitual y más legible); usa **`.iloc`** cuando piensas en *posiciones* ("las primeras 5 filas")."""

S3_CODE = """# Por etiqueta (.loc): incluye el extremo final -> filas 0, 1 y 2
print(".loc[0:2, ['comuna','region']]  (3 filas, extremo INCLUIDO):")
print(df.loc[0:2, ["comuna", "region"]])

# Por posición (.iloc): NO incluye el extremo -> posiciones 0 y 1
print("\\n.iloc[0:2, [2, 1]]  (2 filas, extremo EXCLUIDO):")
print(df.iloc[0:2, [2, 1]])

print("\\nUna celda concreta por etiqueta:", df.loc[0, "comuna"])
print("La MISMA celda por posición:    ", df.iloc[0, 2])"""

S4 = """## 4. Máscaras booleanas: qué pasa de verdad cuando filtras

En la lección filtraste con `df[df["region"] == "Maule"]`. Veamos qué ocurre por dentro, porque
entenderlo te da superpoderes para filtros complejos.

1. `df["region"] == "Maule"` **no** devuelve las filas. Devuelve una **Series de booleanos** (la
   **máscara**): `True` en las filas que cumplen, `False` en las que no. Tiene la misma largo que el
   DataFrame.
2. Cuando escribes `df[mascara]`, pandas conserva **solo las filas donde la máscara es `True`**.

Como la máscara es solo `True`/`False`, puedes **combinarla** con operadores lógicos:
- `&` = **y** (ambas condiciones), `|` = **o** (al menos una), `~` = **no** (lo contrario).
- **Cada condición va entre paréntesis**: `(df["latitud"] > -30) & (df["region"] == "Tarapacá")`.
  Es el error nº1 de filtrado: sin paréntesis, Python evalúa en el orden equivocado y falla.

Una máscara también responde preguntas sin filtrar: `.sum()` cuenta los `True` (porque `True` vale 1),
y `.mean()` te da la **proporción** que cumple la condición."""

S4_CODE = """mascara = df["region"] == "Maule"
print("La máscara es una Series de True/False, no las filas:")
print(mascara.head(5).to_string())

print(f"\\n.sum() cuenta los True  -> {mascara.sum()} establecimientos en el Maule")
print(f".mean() da la proporción -> {mascara.mean():.2%} del total están en el Maule")

# Filtro combinado: norte del país (latitud > -30) que además NO es del Maule
norte = df[(df["latitud"] > -30) & (df["region"] != "Maule")]
print(f"\\nEstablecimientos al norte de lat -30 (y no Maule): {len(norte)}")
print(norte[["comuna", "region", "latitud"]].head().to_string(index=False))"""

S5 = """## 5. Vistas vs copias y el temido `SettingWithCopyWarning`

Aquí está una de las trampas más confusas de pandas. Cuando seleccionas un trozo de un DataFrame,
pandas a veces te entrega una **vista** (una ventana que mira los **mismos datos** originales) y a
veces una **copia** (datos nuevos e independientes). El problema: si modificas algo creyendo que tienes
una cosa cuando tienes la otra, los cambios pueden **no guardarse** o tocar la tabla equivocada.

El síntoma clásico es el **encadenamiento de indexado** (*chained indexing*): hacer dos operaciones
seguidas con corchetes, como `df[df["region"]=="Maule"]["latitud"] = 0`. pandas no sabe si el primer
corchete creó una copia temporal; por eso lanza el `SettingWithCopyWarning`: *"oye, quizá estás
escribiendo sobre una copia que se va a tirar a la basura"*.

**La regla de oro para evitarlo:**
- Para **modificar** datos, usa **una sola** instrucción con `.loc`: `df.loc[mascara, "columna"] = valor`.
- Para **trabajar aparte** sin tocar el original, pide una copia **explícita** con `.copy()`.

La analogía pública: una **vista** es mirar el registro original por una ventana (lo que rayes ahí,
raya el original); una **copia** es una fotocopia tuya (puedes rayarla sin alterar el expediente).

> Nota para material de larga vida útil: en **pandas 3.0** este `SettingWithCopyWarning` desaparece
> gracias a *Copy-on-Write* (CoW) pleno, pero **usar `.loc` y `.copy()` seguirá siendo la práctica
> correcta** para escribir código claro y predecible."""

S5_CODE = """# MAL (genera el warning): indexado encadenado, dos corchetes seguidos
sub = df[df["region"] == "Maule"]      # ¿vista o copia? pandas no garantiza cuál
# sub["latitud"] = 0                    # <- esto dispararía SettingWithCopyWarning

# BIEN opción 1: copia explícita para trabajar aparte sin tocar df
maule = df[df["region"] == "Maule"].copy()
maule["latitud_positiva"] = maule["latitud"] * -1
print("Copia independiente: el df original NO cambió ->", "latitud_positiva" in df.columns)

# BIEN opción 2: modificar el original con UNA sola instrucción .loc
df2 = df.copy()
df2.loc[df2["region"] == "Maule", "comuna"] = df2["comuna"].str.upper()
print("\\nComunas del Maule en MAYÚSCULA (modificación segura con .loc):")
print(df2.loc[df2["region"] == "Maule", "comuna"].head().to_string(index=False))"""

S6 = """## 6. Tipos de dato (`dtype`), memoria y la semántica del faltante (`NaN`)

Cada columna tiene **un solo tipo de dato** (`dtype`), y elegir bien el tipo importa para la velocidad
y la memoria:

- **`object`**: normalmente texto (los nombres de comuna, región). Es flexible pero pesado.
- **`int64` / `float64`**: números enteros / decimales (las latitudes son `float64`).
- **`category`**: ideal para texto que se **repite mucho** (como "region", con pocos valores
  distintos). pandas guarda cada etiqueta **una sola vez** y usa códigos internos: ocupa **mucha menos
  memoria** y acelera agrupaciones. Para un padrón con millones de filas y pocas categorías, esto es oro.

Sobre el **valor faltante (`NaN`, *Not a Number*)**: es el "casillero en blanco". Su semántica tiene
dos reglas que sorprenden:
- **`NaN` se propaga**: cualquier cuenta que lo toque da `NaN` (`NaN + 5 = NaN`). Pero los resúmenes
  como `.mean()` o `.sum()` lo **ignoran** por defecto (no lo tratan como cero).
- **`NaN` no es igual a nada, ni a sí mismo**: `NaN == NaN` es `False`. Por eso para detectarlo se usa
  `.isna()`, **nunca** `== NaN`.

Nuestro dataset viene completo (sin faltantes), así que para ver la semántica del `NaN` usamos una
pequeña Series de ejemplo."""

S6_CODE = """print("Tipos de cada columna (dtype):")
print(df.dtypes.to_string())

# 'region' se repite mucho -> convertir a 'category' ahorra memoria
mem_object = df["region"].memory_usage(deep=True)
mem_cat = df["region"].astype("category").memory_usage(deep=True)
print(f"\\nMemoria de 'region' como object:   {mem_object:>6} bytes")
print(f"Memoria de 'region' como category: {mem_cat:>6} bytes  (mismos datos, menos memoria)")

# Semántica del NaN con una Series de ejemplo
ej = pd.Series([10.0, np.nan, 30.0])
print(f"\\nNaN se propaga en cuentas elemento a elemento: 10 + NaN = {ej[0] + ej[1]}")
print(f"Pero .mean() lo IGNORA (no lo trata como 0): media = {ej.mean()}  (= (10+30)/2)")
print(f"NaN no es igual ni a sí mismo: (np.nan == np.nan) -> {np.nan == np.nan}")
print(f"Por eso se detecta con .isna():  faltantes en la Series -> {ej.isna().sum()}")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Confundir `.loc` con `.iloc`.** `.loc` es por etiqueta (e incluye el extremo del rango); `.iloc` es por posición (lo excluye).
- **Filtrar sin paréntesis al combinar condiciones.** Escribe `(cond1) & (cond2)`, nunca `cond1 & cond2` suelto.
- **Usar `and`/`or` de Python en máscaras.** En pandas son `&`, `|`, `~` (operan elemento a elemento).
- **Indexado encadenado para modificar:** `df[mascara]["col"] = ...` dispara `SettingWithCopyWarning`. Usa `df.loc[mascara, "col"] = ...`.
- **Olvidar `.copy()`** cuando quieres trabajar un subconjunto sin tocar el original.
- **Detectar faltantes con `== NaN`.** Nunca funciona (`NaN != NaN`). Usa `.isna()`.
- **Asumir que `.mean()` trata el `NaN` como cero.** Lo ignora; el conteo cambia, no se rellena con 0."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan, otros piden **elegir la interpretación correcta**.
Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: Series, índice y tipo
E1 = """## Ejercicio 01 · ¿Columna o tabla? Series vs DataFrame
Selecciona la columna `"comuna"` de `df` de dos formas y observa qué tipo devuelve cada una:

- Guarda en `una_col` el resultado de `df["comuna"]` (corchete simple).
- Guarda en `sub_df` el resultado de `df[["comuna"]]` (corchete **doble**).
- Luego elige en `conclusion` (letra) la lectura correcta:
  - **A.** Ambas devuelven exactamente lo mismo: da igual usar corchete simple o doble.
  - **B.** El corchete simple devuelve una **Series** (una columna) y el corchete doble un **DataFrame** (una tabla de una columna).
  - **C.** El corchete doble devuelve una Series y el simple un DataFrame."""
E1_TODO = """una_col = None      # TODO: df["comuna"]  (corchete simple)
sub_df = None       # TODO: df[["comuna"]] (corchete doble)
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """una_col = df["comuna"]
sub_df = df[["comuna"]]
conclusion = "B"
"""
E1_CHK = """try:
    _es_series = isinstance(df["comuna"], pd.Series)
    _es_frame = isinstance(df[["comuna"]], pd.DataFrame)
    _correcta = "B" if (_es_series and _es_frame) else "A"
    assert isinstance(una_col, pd.Series), "una_col debe ser df['comuna'] (una Series)"
    assert isinstance(sub_df, pd.DataFrame), "sub_df debe ser df[['comuna']] (un DataFrame)"
    assert str(conclusion).strip().upper() == _correcta, "Revisa qué devuelve cada tipo de corchete"
    print("✅ Correcto. Corchete simple -> Series; corchete doble -> DataFrame.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: vectorización / máscara booleana
E2 = """## Ejercicio 02 · La máscara booleana por dentro
Sin filtrar todavía, crea la **máscara** de los establecimientos al norte del paralelo -30 (es decir,
con `latitud` **mayor** que -30) y úsala para contar y para sacar la proporción:

- `mascara` = la Series booleana `df["latitud"] > -30`.
- `n_norte` = cuántos cumplen (suma de la máscara, como entero).
- `prop_norte` = proporción que cumple (media de la máscara).

Pista: `mascara.sum()` cuenta los `True`; `mascara.mean()` da la proporción."""
E2_TODO = """mascara = None      # TODO: df["latitud"] > -30
n_norte = None      # TODO: int(mascara.sum())
prop_norte = None   # TODO: mascara.mean()
"""
E2_SOL = """mascara = df["latitud"] > -30
n_norte = int(mascara.sum())
prop_norte = mascara.mean()
"""
E2_CHK = """try:
    _m = df["latitud"] > -30
    _n = int(_m.sum())
    _p = _m.mean()
    assert mascara is not None and mascara.equals(_m), "mascara debe ser df['latitud'] > -30"
    assert n_norte is not None and int(n_norte) == _n, f"n_norte debería ser {_n} (cuenta los True con .sum())"
    assert prop_norte is not None and abs(prop_norte - _p) < 1e-9, f"prop_norte debería ser {_p:.4f} (.mean())"
    print(f"✅ Correcto. {_n} establecimientos al norte de -30 ({_p:.1%} del total).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: .loc vs .iloc (extremo incluido vs excluido) conceptual + cálculo
E3 = """## Ejercicio 03 · `.loc` incluye el extremo, `.iloc` no
Selecciona filas con cada acceso y cuenta cuántas trae cada uno:

- `n_loc` = número de filas de `df.loc[0:5]` (etiquetas 0 a 5).
- `n_iloc` = número de filas de `df.iloc[0:5]` (posiciones 0 a 4).

Luego elige en `conclusion` la lectura correcta:
- **A.** Ambos traen 5 filas: `.loc` y `.iloc` son intercambiables.
- **B.** `.loc[0:5]` trae 6 filas (incluye la etiqueta 5) y `.iloc[0:5]` trae 5 (excluye la posición 5).
- **C.** `.loc[0:5]` trae 5 y `.iloc[0:5]` trae 6."""
E3_TODO = """n_loc = None        # TODO: len(df.loc[0:5])
n_iloc = None       # TODO: len(df.iloc[0:5])
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = """n_loc = len(df.loc[0:5])
n_iloc = len(df.iloc[0:5])
conclusion = "B"
"""
E3_CHK = """try:
    _nl = len(df.loc[0:5])
    _ni = len(df.iloc[0:5])
    _correcta = "B" if _nl > _ni else "A"
    assert n_loc is not None and int(n_loc) == _nl, f"n_loc debería ser {_nl}"
    assert n_iloc is not None and int(n_iloc) == _ni, f"n_iloc debería ser {_ni}"
    assert str(conclusion).strip().upper() == _correcta, "Compara n_loc y n_iloc: ¿cuál incluye el extremo?"
    print(f"✅ Correcto. .loc[0:5]={_nl} filas (incluye el 5); .iloc[0:5]={_ni} filas (lo excluye).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: NaN semantics (conceptual)
E4 = """## Ejercicio 04 · La semántica del faltante (`NaN`)
Trabaja con esta pequeña Series de ejemplo (ya creada): `s = pd.Series([20.0, np.nan, 40.0])`.

- Guarda en `suma_directa` el resultado de `s[0] + s[1]` (sumar un número con el faltante).
- Guarda en `media` el resultado de `s.mean()`.
- Guarda en `n_faltantes` cuántos faltantes hay, usando `s.isna().sum()` (como entero).

Luego elige en `conclusion` la lectura correcta:
- **A.** `s.mean()` da 20 porque trata el `NaN` como un 0 más en el promedio.
- **B.** `s[0] + s[1]` da `NaN` (el faltante se propaga en cuentas directas), pero `s.mean()` lo
  **ignora** y promedia solo los valores presentes: (20+40)/2 = 30.
- **C.** `s.mean()` da `NaN` porque cualquier operación con un faltante siempre da `NaN`."""
E4_TODO = """s = pd.Series([20.0, np.nan, 40.0])
suma_directa = None   # TODO: s[0] + s[1]
media = None          # TODO: s.mean()
n_faltantes = None    # TODO: int(s.isna().sum())
conclusion = None     # TODO: "A", "B" o "C"
"""
E4_SOL = """s = pd.Series([20.0, np.nan, 40.0])
suma_directa = s[0] + s[1]
media = s.mean()
n_faltantes = int(s.isna().sum())
conclusion = "B"
"""
E4_CHK = """try:
    _s = pd.Series([20.0, np.nan, 40.0])
    _suma = _s[0] + _s[1]
    _media = _s.mean()
    _nf = int(_s.isna().sum())
    # La correcta se deduce: la suma directa es NaN y la media ignora el faltante
    _correcta = "B" if (pd.isna(_suma) and not pd.isna(_media)) else "A"
    assert pd.isna(suma_directa) == pd.isna(_suma), "suma_directa debe ser s[0] + s[1] (un NaN)"
    # Endurecido: además de ser NaN, debe ser un float que provenga de sumar sobre s
    # (descarta un np.nan hardcodeado que no usa s[0] + s[1]).
    assert isinstance(suma_directa, float), "suma_directa debe surgir de s[0] + s[1] (un float NaN), no un NaN suelto"
    assert pd.isna(s[0] + s[1]) and (s[0] + s[1] is not suma_directa or pd.isna(suma_directa)), "suma_directa debe calcularse como s[0] + s[1]"
    assert media is not None and abs(media - _media) < 1e-9, f"media debería ser {_media} (la media ignora el NaN)"
    assert n_faltantes is not None and int(n_faltantes) == _nf, f"n_faltantes debería ser {_nf} (usa s.isna().sum())"
    assert str(conclusion).strip().upper() == _correcta, "Compara la suma directa con la media: ¿qué hace cada una con el NaN?"
    print(f"✅ Correcto. La suma directa da NaN, pero .mean() lo ignora y da {_media:.0f} = (20+40)/2.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no usas pandas como una caja negra: sabes que un DataFrame es un conjunto de **Series** que comparten
**índice**, que la **vectorización** es lo que lo hace rápido (adiós bucles `for`), que **`.loc`** va
por etiqueta y **`.iloc`** por posición, que un filtro es una **máscara booleana** que puedes combinar
con `&`, `|`, `~`, que conviene distinguir **vistas de copias** (y modificar con `.loc` o `.copy()`),
y que el **`NaN`** tiene reglas propias (`.isna()`, nunca `== NaN`).

La regla de oro que te llevas: **entender qué objeto tienes en la mano** —Series o DataFrame, vista o
copia, etiqueta o posición, valor o faltante— es lo que separa a quien *pelea* con pandas de quien lo
*maneja*."""


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
