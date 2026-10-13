"""build_R1-04.py — módulo R1-04 (Limpieza de datos).

Rama R1 (Análisis y Visualización). Diagnosticar y limpiar un dataset sucio:
texto (strip/mayúsculas), sinónimos de categorías, la trampa del punto de miles
("2.425" no es 2,425), faltantes honestos, valores imposibles, duplicados, todo en
una función limpiar() — y, al final, auditar la limpieza contra la fuente oficial.

Rearmado 2026 (reemplaza la versión legacy): lección sobre
matricula_sucia.csv (matrícula MINEDUC 2025 con errores típicos inyectados, seed 42)
verificada contra matricula.csv por RBD. Profundiza = transferencia: faltantes REALES
de las estaciones SINCA en 2026 (aire_nuevos.csv). Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-04.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-04-limpieza-de-datos")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["matricula_sucia.csv", "matricula.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

def cargar():
    """Devuelve una copia FRESCA del archivo sucio: cada ejercicio parte de cero."""
    return pd.read_csv("matricula_sucia.csv")

# Catálogos oficiales (así escribe el MINEDUC las regiones y las dependencias)
REGIONES_OFICIALES = ["Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", "Coquimbo",
                      "Valparaíso", "Metropolitana", "O'Higgins", "Maule", "Ñuble", "Biobío",
                      "La Araucanía", "Los Ríos", "Los Lagos", "Aysén", "Magallanes"]
DEPENDENCIAS_OFICIALES = ["Municipal", "Particular subvencionado", "Particular pagado",
                          "Servicio Local de Educación", "Administración delegada"]

df = cargar()
print("Datos cargados:", df.shape, "filas x columnas")
df.head(8)'''

INTRO = '''## El problema: la planilla consolidada

Imagina que la Seremi te manda un consolidado de matrícula armado con las planillas de
varias oficinas. Cada oficina escribió a su manera: unos ponen «RM», otros «Región
Metropolitana»; unos escriben la comuna en MAYÚSCULAS con espacios de más; alguien anotó la
matrícula con punto de miles («2.425») y otro escribió «s/i» (sin información). Además, una
oficina pegó su parte dos veces.

`matricula_sucia.csv` es exactamente eso: **1.545 filas** de la matrícula oficial 2025
(MINEDUC) a las que les inyectamos (con semilla fija) los errores típicos de una planilla
real. La ventaja pedagógica: **al final vas a comparar tu limpieza contra la fuente oficial,
fila por fila**, y sabrás si de verdad quedó bien.

> 🧭 **Regla de oro:** primero se **diagnostica**, después se limpia. Y cada decisión de
> limpieza (botar, corregir, dejar en blanco) se **declara**.'''

EJ = [
 # ── 1 ─────────────────────────────────────────────────────────────────────────
 ("## 1. Diagnosticar antes de limpiar",
  '''Cuatro herramientas que conviene correr **siempre** al abrir una tabla nueva:

- `df.info()` → tipo de cada columna y cuántos valores no nulos tiene.
- `df.isna().sum()` → cuántas **celdas vacías** (`NaN`) hay por columna.
- `df.duplicated().sum()` → cuántas **filas repetidas** exactas hay.
- `df["columna"].value_counts()` → los valores distintos y cuántas veces aparecen
  (para cazar el mismo dato escrito de varias formas).''',
  '''# Mira el diagnóstico antes de resolver el ejercicio
df.info()
print()
print(df["region"].value_counts())''',
  "Mide el desorden",
  '''df = cargar()
n_duplicados = int(df.duplicated().sum())
n_faltantes = int(df["mat_total"].isna().sum())
tipo_mat_total = str(df["mat_total"].dtype)
n_regiones = df["region"].nunique()
print("duplicadas:", n_duplicados, "| mat_total vacías:", n_faltantes,
      "| tipo de mat_total:", tipo_mat_total, "| regiones escritas distinto:", n_regiones)''',
  '''df = cargar()
# TODO: filas duplicadas exactas (en toda la tabla)
n_duplicados = ...
# TODO: celdas vacías (NaN) en la columna mat_total
n_faltantes = ...
# TODO: el tipo de la columna mat_total, como texto: str(df["mat_total"].dtype)
tipo_mat_total = ...
# TODO: cuántas formas distintas de escribir la región hay (nunique)
n_regiones = ...
print("duplicadas:", n_duplicados, "| mat_total vacías:", n_faltantes,
      "| tipo de mat_total:", tipo_mat_total, "| regiones escritas distinto:", n_regiones)''',
  '''_d = cargar()
assert n_duplicados == int(_d.duplicated().sum()), "Cuenta las filas duplicadas con df.duplicated().sum()"
assert n_faltantes == int(_d["mat_total"].isna().sum()), "Cuenta los NaN de mat_total con .isna().sum()"
assert tipo_mat_total == "object", "El tipo debería ser 'object' (texto): ¡mat_total no es número todavía!"
assert n_regiones == _d["region"].nunique(), "Usa df['region'].nunique()"
assert n_regiones > len(REGIONES_OFICIALES), "Chile tiene 16 regiones: deberías ver más formas de escribirlas"''',
  "duplicated().sum(), isna().sum(), str(df['mat_total'].dtype) y nunique().",
  '''print(f"Chile tiene {len(REGIONES_OFICIALES)} regiones, pero el archivo dice que hay {df['region'].nunique()}.")
print("Y mat_total es texto: no se puede sumar todavía. Hay trabajo que hacer.")'''),

 # ── 2 ─────────────────────────────────────────────────────────────────────────
 ("## 2. Limpiar texto: espacios y mayúsculas",
  '''Para una persona, `"  LA FLORIDA "` y `"La Florida"` son lo mismo; para el computador, **no**:
`value_counts()` las contaría como dos comunas. El accesor `.str` aplica operaciones de texto
a toda la columna, y se pueden **encadenar**:

- `.str.strip()` → quita espacios al inicio y al final.
- `.str.title()` → Primera Letra De Cada Palabra En Mayúscula.
- `.str.lower()` / `.str.upper()` → todo minúscula / todo mayúscula.

¿Por qué `title()` y no otra? Porque **normalizar es llevar el dato al formato de la fuente
oficial**, no al gusto de cada uno: el MINEDUC escribe `"Viña Del Mar"`, `"La Florida"`.''',
  '''# repr() deja ver los espacios invisibles entre comillas
sucias = df.loc[df["comuna"] != df["comuna"].str.strip(), "comuna"]
print("comunas con espacios de más:", len(sucias))
print([repr(c) for c in sucias.head(5)])''',
  "Normaliza la columna comuna",
  '''df = cargar()
df["comuna"] = df["comuna"].str.strip().str.title()
n_comunas = df["comuna"].nunique()
print("comunas distintas:", cargar()["comuna"].nunique(), "→", n_comunas)''',
  '''df = cargar()
# TODO: quita los espacios y deja la comuna en formato Título (encadena dos métodos .str)
df["comuna"] = ...
# TODO: cuántas comunas distintas quedan
n_comunas = ...
print("comunas distintas tras limpiar:", n_comunas)''',
  '''assert (df["comuna"] == df["comuna"].str.strip()).all(), "Quedan espacios al inicio o al final"
assert not df["comuna"].str.isupper().any(), "Quedan comunas escritas en MAYÚSCULAS"
assert n_comunas == cargar()["comuna"].str.strip().str.title().nunique(), "Revisa n_comunas: df['comuna'].nunique()"''',
  'df["comuna"].str.strip().str.title() — y no olvides reasignar con df["comuna"] = ...',
  None),

 # ── 3 ─────────────────────────────────────────────────────────────────────────
 ("## 3. Categorías con sinónimos: un diccionario de equivalencias",
  '''`"RM"`, `"Región Metropolitana"` y `"metropolitana"` son la **misma** región escrita de tres
formas. Ningún método de texto lo arregla solo: hay que **decidir** la equivalencia y dejarla
escrita en un **diccionario** `{"como viene": "como debe quedar"}`. Ese diccionario es, además,
la documentación de tu limpieza: cualquiera puede auditarlo.

- `.replace(diccionario)` → cambia los valores que están en el diccionario y **deja igual** el resto.
- `.map(diccionario)` → traduce **todos** los valores; lo que no está en el diccionario queda `NaN`.
  Útil cuando quieres que un valor imprevisto **salte a la vista**.

La columna `rural` trae `"Sí"`, `"No"`, `"1"` y `"0"`: la llevamos al formato oficial **1 / 0**.''',
  '''print(df["dependencia"].value_counts(), "\\n")
print(df["rural"].value_counts())''',
  "Unifica región, dependencia y rural",
  '''df = cargar()
mapa_region = {
    "RM": "Metropolitana",
    "Región Metropolitana": "Metropolitana",
    "metropolitana": "Metropolitana",
    "V Región": "Valparaíso",
    "Valparaiso": "Valparaíso",
    "Bio Bio": "Biobío",
    "Biobio": "Biobío",
}
mapa_dependencia = {
    "Part. Subv.": "Particular subvencionado",
    "Part. Pagado": "Particular pagado",
    "MUNICIPAL": "Municipal",
}
mapa_rural = {"Sí": 1, "No": 0, "1": 1, "0": 0}

df["region"] = df["region"].replace(mapa_region)
df["dependencia"] = df["dependencia"].replace(mapa_dependencia)
df["rural"] = df["rural"].map(mapa_rural)
print("regiones:", df["region"].nunique(), "| dependencias:", df["dependencia"].nunique(),
      "| rural:", sorted(df["rural"].dropna().unique().tolist()))''',
  '''df = cargar()
mapa_region = {
    "RM": "Metropolitana",
    "V Región": "Valparaíso",
    # TODO: agrega los 5 sinónimos que faltan (mira el value_counts de la región en el Ej. 1)
}
mapa_dependencia = {
    # TODO: las 3 formas abreviadas o en MAYÚSCULAS → su nombre oficial
}
mapa_rural = {
    "Sí": 1,
    # TODO: completa "No", "1" y "0"
}

df["region"] = df["region"].replace(mapa_region)
df["dependencia"] = df["dependencia"].replace(mapa_dependencia)
df["rural"] = df["rural"].map(mapa_rural)
print("regiones:", df["region"].nunique(), "| dependencias:", df["dependencia"].nunique(),
      "| rural:", sorted(df["rural"].dropna().unique().tolist()))''',
  '''assert set(df["region"]) == set(REGIONES_OFICIALES), f"Regiones fuera del catálogo: {sorted(set(df['region']) - set(REGIONES_OFICIALES))}"
assert set(df["dependencia"]) == set(DEPENDENCIAS_OFICIALES), f"Dependencias fuera del catálogo: {sorted(set(df['dependencia']) - set(DEPENDENCIAS_OFICIALES))}"
assert df["rural"].isna().sum() == 0, "Hay valores de rural sin traducir (quedaron NaN): completa mapa_rural"
assert set(df["rural"]) == {0, 1}, "rural debe quedar solo con 0 y 1"''',
  "Compara df['region'].value_counts() con REGIONES_OFICIALES: cada forma rara es una llave del diccionario.",
  '''fuera = sorted(set(cargar()["region"]) - set(REGIONES_OFICIALES))
print("Formas que NO estaban en el catálogo oficial:", fuera)'''),

 # ── 4 ─────────────────────────────────────────────────────────────────────────
 ("## 4. De texto a número: la trampa del punto",
  '''`mat_total` llegó como **texto** porque algunas celdas dicen `"s/i"` y otras traen punto de
miles (`"2.425"`). La tentación es `pd.to_numeric(...)`, que convierte lo que puede. Mira lo que
pasa con `"2.425"` en la celda de abajo: en Chile el punto separa **miles**, pero Python (y casi
todo el software) lo lee como **punto decimal**. Resultado: un liceo de 2.425 estudiantes queda
con **2,425 estudiantes**. Sin error, sin aviso. Es la trampa más peligrosa de este módulo.

La receta correcta:

1. Quitar el punto de miles: `.str.replace(".", "", regex=False)` (con `regex=False`, porque
   en una *expresión regular* el punto significa «cualquier carácter» y borraría todo).
2. Convertir con `pd.to_numeric(..., errors="coerce")`: lo que no es número (`"s/i"`) queda `NaN`.

> Al leer un CSV chileno desde el principio también puedes usar
> `pd.read_csv(..., thousands=".", decimal=",")`.''',
  '''ingenuo = pd.to_numeric(df["mat_total"], errors="coerce")
fila = df["mat_total"] == "2.425"
print("En el archivo dice:", repr(df.loc[fila, "mat_total"].iloc[0]))
print("pd.to_numeric lo convirtió en:", ingenuo[fila].iloc[0], " ← ¡dos estudiantes y fracción!")''',
  "Convierte mat_total sin caer en la trampa",
  '''df = cargar()
df["mat_total"] = pd.to_numeric(df["mat_total"].str.replace(".", "", regex=False), errors="coerce")
n_sin_dato = int(df["mat_total"].isna().sum())
print("tipo:", df["mat_total"].dtype, "| sin dato (vacías + 's/i'):", n_sin_dato)
print(df.loc[cargar()["mat_total"] == "2.425", "mat_total"])''',
  '''df = cargar()
# TODO: quita el punto de miles (regex=False) y convierte a número (errors="coerce")
df["mat_total"] = ...
# TODO: cuántas filas quedaron sin dato (NaN) después de convertir
n_sin_dato = ...
print("tipo:", df["mat_total"].dtype, "| sin dato (vacías + 's/i'):", n_sin_dato)''',
  '''_crudo = cargar()["mat_total"]
assert pd.api.types.is_numeric_dtype(df["mat_total"]), "mat_total todavía no es numérica"
assert df.loc[_crudo == "2.425", "mat_total"].iloc[0] == 2425, "'2.425' debe quedar como 2425, no 2.425"
assert (df["mat_total"].dropna() % 1 == 0).all(), "Quedaron matrículas con decimales: ¿quitaste el punto de miles?"
assert n_sin_dato == int(_crudo.isna().sum() + (_crudo == "s/i").sum()), "n_sin_dato = df['mat_total'].isna().sum()"''',
  'pd.to_numeric(df["mat_total"].str.replace(".", "", regex=False), errors="coerce").',
  None),

 # ── 5 ─────────────────────────────────────────────────────────────────────────
 ("## 5. Valores imposibles y faltantes: no inventes",
  '''Un dato puede estar **presente y ser imposible**: un establecimiento no puede tener **-1**
hombres matriculados. Eso no es un número pequeño, es un **código de error** de quien llenó la
planilla. Lo honesto es marcarlo como **faltante** (`NaN`), no dejarlo ni reemplazarlo por un
número «parecido».

- `serie.mask(condicion)` → «tapa» con `NaN` los valores donde la condición es verdadera.

> 🚫 **Nunca inventes un dato.** Rellenar con 0 o con el promedio un valor que no conoces baja
> (o sube) los totales y miente sin que nadie se dé cuenta. Si no puedes recuperarlo de una
> fuente confiable, déjalo en blanco y **decláralo**.''',
  '''print(df["mat_hombres"].describe())
print("\\nValores negativos:", (df["mat_hombres"] < 0).sum())''',
  "Marca los imposibles como faltantes",
  '''df = cargar()
imposibles = df["mat_hombres"] < 0
n_imposibles = int(imposibles.sum())
df["mat_hombres"] = df["mat_hombres"].mask(imposibles)
print("imposibles:", n_imposibles, "| mínimo ahora:", df["mat_hombres"].min(),
      "| NaN en mat_hombres:", df["mat_hombres"].isna().sum())''',
  '''df = cargar()
# TODO: condición de valor imposible (mat_hombres negativo)
imposibles = ...
# TODO: cuántos son
n_imposibles = ...
# TODO: tápalos con NaN usando .mask(...)
df["mat_hombres"] = ...
print("imposibles:", n_imposibles)''',
  '''assert n_imposibles == int((cargar()["mat_hombres"] < 0).sum()), "Cuenta los negativos con (df['mat_hombres'] < 0).sum()"
assert df["mat_hombres"].min() >= 0, "Quedan valores negativos"
assert df["mat_hombres"].isna().sum() == n_imposibles, "Los imposibles deben quedar como NaN (no como 0 ni borrados)"
assert len(df) == len(cargar()), "No borres filas: solo marca el dato imposible"''',
  'imposibles = df["mat_hombres"] < 0 ; df["mat_hombres"] = df["mat_hombres"].mask(imposibles).',
  None),

 # ── 6 ─────────────────────────────────────────────────────────────────────────
 ("## 6. Duplicados: la planilla pegada dos veces",
  '''Una fila **duplicada** infla los totales: sumarías esos estudiantes dos veces. Y rompe la
**llave**: en R1-03 viste que el RBD identifica a cada establecimiento, así que no debería
repetirse nunca.

- `df.duplicated()` → `True` en cada fila que repite a una anterior.
- `df.drop_duplicates()` → bota las repetidas y conserva la primera.
- `df["rbd"].is_unique` → `True` si la llave no se repite.

> Orden importa: normaliza el texto **antes** de buscar duplicados; dos filas «iguales»
> escritas con distinta mayúscula no se detectan como duplicadas.''',
  None,
  "Elimina los duplicados y verifica la llave",
  '''df = cargar()
n_antes = len(df)
df = df.drop_duplicates()
n_despues = len(df)
llave_unica = df["rbd"].is_unique
print("filas:", n_antes, "→", n_despues, "| ¿rbd único?:", llave_unica)''',
  '''df = cargar()
n_antes = len(df)
# TODO: elimina las filas duplicadas
df = ...
# TODO: filas después, y si la llave rbd quedó única (.is_unique)
n_despues = ...
llave_unica = ...
print("filas:", n_antes, "→", n_despues, "| ¿rbd único?:", llave_unica)''',
  '''_d = cargar()
assert n_despues == len(_d) - int(_d.duplicated().sum()), "Usa df = df.drop_duplicates()"
assert llave_unica, "El rbd todavía se repite"
assert df.duplicated().sum() == 0, "Quedan filas duplicadas"''',
  'df = df.drop_duplicates(); n_despues = len(df); llave_unica = df["rbd"].is_unique.',
  None),

 # ── 7 ─────────────────────────────────────────────────────────────────────────
 ("## 7. Todo junto: una función `limpiar()` reutilizable",
  '''El próximo mes llegará otro consolidado con los mismos vicios. En vez de repetir los pasos a
mano, se empaquetan en una **función**: una «receta» que recibe la tabla sucia y devuelve la
limpia, siempre igual. Es la versión profesional de una macro de Excel — y queda escrita, así que
cualquiera puede revisar qué decidiste.

Orden sugerido: texto → categorías → números → imposibles → duplicados. Reutiliza tus
diccionarios del Ejercicio 3.''',
  None,
  "Escribe la función limpiar(df)",
  '''def limpiar(df):
    out = df.copy()
    out["comuna"] = out["comuna"].str.strip().str.title()
    out["region"] = out["region"].replace(mapa_region)
    out["dependencia"] = out["dependencia"].replace(mapa_dependencia)
    out["rural"] = out["rural"].map(mapa_rural)
    out["mat_total"] = pd.to_numeric(out["mat_total"].str.replace(".", "", regex=False), errors="coerce")
    out["mat_hombres"] = out["mat_hombres"].mask(out["mat_hombres"] < 0)
    out = out.drop_duplicates()
    return out

limpio = limpiar(cargar())
print("tabla limpia:", limpio.shape)
limpio.head()''',
  '''def limpiar(df):
    out = df.copy()
    out["comuna"] = out["comuna"].str.strip().str.title()      # Ej. 2 (ya hecho)
    # TODO: región, dependencia y rural con tus diccionarios (Ej. 3)
    ...
    # TODO: mat_total a número sin caer en la trampa del punto (Ej. 4)
    ...
    # TODO: mat_hombres negativos → NaN (Ej. 5)
    ...
    # TODO: elimina duplicados (Ej. 6)
    ...
    return out

limpio = limpiar(cargar())
print("tabla limpia:", limpio.shape)
limpio.head()''',
  '''assert len(limpio) == cargar().drop_duplicates().shape[0], "Faltan por botar los duplicados"
assert set(limpio["region"]) == set(REGIONES_OFICIALES), "La región no quedó con el catálogo oficial"
assert set(limpio["dependencia"]) == set(DEPENDENCIAS_OFICIALES), "La dependencia no quedó con el catálogo oficial"
assert set(limpio["rural"]) == {0, 1}, "rural debe quedar en 0/1"
assert pd.api.types.is_numeric_dtype(limpio["mat_total"]), "mat_total no quedó numérica"
assert limpio["mat_total"].max() < 10000, "Algo raro en mat_total"
assert (limpio["mat_total"].dropna() % 1 == 0).all(), "Hay matrículas con decimales: la trampa del punto"
assert limpio["mat_hombres"].min() >= 0, "Quedan mat_hombres negativos"
assert len(cargar()) == 1545, "¡limpiar() no debe modificar el archivo original!"''',
  "Copia dentro de limpiar() la línea clave de cada ejercicio, aplicada a out (no a df).",
  None),

 # ── 8 ─────────────────────────────────────────────────────────────────────────
 ("## 8. Auditoría: ¿quedó igual a la fuente oficial?",
  '''En la vida real casi nunca tienes la «respuesta correcta» para comparar. Aquí sí: la
matrícula oficial 2025 (`matricula.csv`). Cruza tu tabla limpia con la oficial **por RBD** (lo
aprendiste en R1-03) y mide, columna por columna, **qué proporción de filas coincide**.

`(cruce["region"] == cruce["region_oficial"]).mean()` da la proporción de coincidencias: los
`True` cuentan como 1 y los `False` como 0. Si tu limpieza está bien, cada columna debería dar
**1.0** (100%).

Para `mat_total` compara **solo las filas donde tienes dato**: las que quedaron `NaN` no son un
error de limpieza, son información que no venía en la planilla.''',
  None,
  "Mide la coincidencia con la fuente oficial",
  '''oficial = pd.read_csv("matricula.csv")
limpio = limpiar(cargar())
cruce = pd.merge(limpio, oficial, on="rbd", how="left", suffixes=("", "_oficial"))

coincide = {}
for col in ["region", "comuna", "dependencia", "rural"]:
    coincide[col] = (cruce[col] == cruce[col + "_oficial"]).mean()
con_dato = cruce["mat_total"].notna()
coincide["mat_total"] = (cruce.loc[con_dato, "mat_total"] == cruce.loc[con_dato, "mat_total_oficial"]).mean()
n_sin_dato = int((~con_dato).sum())

for col, tasa in coincide.items():
    print(f"{col:12s} {tasa:.1%}")
print("filas sin mat_total (no recuperable desde la planilla):", n_sin_dato)''',
  '''oficial = pd.read_csv("matricula.csv")
limpio = limpiar(cargar())
cruce = pd.merge(limpio, oficial, on="rbd", how="left", suffixes=("", "_oficial"))

coincide = {}
for col in ["region", "comuna", "dependencia", "rural"]:
    # TODO: proporción de filas donde tu columna es igual a la oficial
    coincide[col] = ...
con_dato = cruce["mat_total"].notna()
# TODO: proporción de coincidencia en mat_total, SOLO en las filas con_dato
coincide["mat_total"] = ...
# TODO: cuántas filas quedaron sin mat_total
n_sin_dato = ...

for col, tasa in coincide.items():
    print(col, tasa)
print("filas sin mat_total:", n_sin_dato)''',
  '''assert len(cruce) == len(limpio), "El cruce no debería cambiar el número de filas"
for _col in ["region", "comuna", "dependencia", "rural", "mat_total"]:
    assert float(coincide[_col]) == 1.0, f"La columna {_col} no coincide 100% con la oficial ({coincide[_col]}): revisa ese paso de limpiar()"
assert n_sin_dato == int(cruce["mat_total"].isna().sum()), "n_sin_dato = cuántos NaN quedaron en mat_total"''',
  '(cruce[col] == cruce[col + "_oficial"]).mean(); para mat_total filtra antes con cruce.loc[con_dato, ...].',
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Te quedaron filas sin `mat_total` y algunas sin `mat_hombres`. En la tabla oficial, la matrícula
total es casi siempre la suma de hombres y mujeres. ¿Usarías esa regla para **reconstruir** los
datos que faltan, o los dejarías en blanco? Si los reconstruyes, ¿cómo lo declararías en el informe
para que nadie confunda un dato reconstruido con uno reportado?

> Limpiar no es neutral: cada decisión cambia los números. Por eso se escribe en código y se declara.'''

CIERRE = '''## Errores típicos al limpiar

- **Limpiar sin diagnosticar** → arreglas a ciegas y se te escapan problemas.
- **Olvidar reasignar** → `df["comuna"].str.strip()` calcula y bota el resultado; hay que guardar con `df["comuna"] = ...`.
- **`pd.to_numeric` sobre «2.425»** → lo lee como 2,425 sin avisar. Quita el punto de miles primero (`regex=False`).
- **Rellenar con 0 lo que no sabes** → baja los totales y los promedios. Un faltante se declara, no se inventa.
- **Buscar duplicados antes de normalizar** → filas iguales escritas distinto no se detectan.
- **No auditar** → si tienes una fuente de referencia, compara contra ella.

## Cierre

- **Diagnóstico primero**: `info`, `isna`, `duplicated`, `value_counts`.
- Texto con `.str`, sinónimos con un **diccionario** (que además documenta), números con cuidado
  del **punto de miles**, imposibles a `NaN`, duplicados fuera.
- Todo en una función `limpiar()` reproducible, y una **auditoría** contra la fuente oficial.

> *En R1-05 le preguntarás a una base de datos directamente con SQL — sobre esta misma
> matrícula, ya limpia.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-04", "Limpieza de datos", "R1", "Analista de Datos", "5",
                      ["**Diagnosticar** un dataset sucio antes de tocarlo.",
                       "Normalizar **texto** y unificar **sinónimos** con un diccionario.",
                       "Convertir texto a número sin caer en la **trampa del punto de miles**.",
                       "Tratar **faltantes, imposibles y duplicados** sin inventar datos.",
                       "Empaquetar todo en `limpiar()` y **auditar** contra la fuente oficial."],
                      "dejar un dataset del Estado listo para analizar, con decisiones de limpieza declaradas y verificadas.",
                      "matrícula escolar 2025 (MINEDUC) con errores típicos de planilla inyectados, auditada contra la cifra oficial por RBD.",
                      n_checks=len(EJ)),
        h.code(SETUP),
        h.md(INTRO),
    ]
    for i, (sec_t, sec_b, demo, ej_t, sol, todo, chk, hint, post) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        if demo:
            cells.append(h.code(demo))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if post:
            cells.append(h.code(post))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundiza: faltantes REALES en las estaciones de calidad del aire ─────────
PROF_PREP = f'''import pandas as pd, os, urllib.request
CSV = "aire_nuevos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/aire_nuevos.csv", CSV)
aire = pd.read_csv(CSV, parse_dates=["fecha"])
print("filas:", aire.shape, "| estaciones:", aire["estacion"].nunique(),
      "| desde", aire["fecha"].min().date(), "hasta", aire["fecha"].max().date())
print(aire.isna().sum())'''

PROF_EJ = [
 ("## 1. ¿Qué estaciones tienen más días sin dato?",
  "Datos nuevos y **reales**: PM2.5 diario de 14 estaciones SINCA entre enero y septiembre de "
  "2026. Aquí nadie inyectó errores: los huecos son de verdad (equipos en mantención, fallas de "
  "transmisión, datos no validados). Primero, el diagnóstico: **% de días sin PM2.5 por estación**.",
  "Porcentaje de faltantes por estación",
  '''pct_faltante = (aire.assign(falta=aire["pm25"].isna())
                    .groupby("estacion")["falta"].mean() * 100).sort_values(ascending=False)
peor = pct_faltante.idxmax()
print(pct_faltante.round(1))
print("peor estación:", peor)''',
  '''# TODO: % de días con pm25 vacío por estación, de mayor a menor
# pista: aire.assign(falta=aire["pm25"].isna()).groupby("estacion")["falta"].mean() * 100
pct_faltante = ...
# TODO: la estación con más faltantes
peor = ...
print("peor estación:", peor)''',
  '''_esp = aire["pm25"].isna().groupby(aire["estacion"]).mean() * 100
assert abs(pct_faltante.max() - _esp.max()) < 1e-9, "Revisa el cálculo del porcentaje"
assert list(pct_faltante.values) == sorted(pct_faltante.values, reverse=True), "Ordena de mayor a menor"
assert peor == _esp.idxmax()''',
  "La media de un booleano es la proporción de True; multiplica por 100 y ordena con sort_values(ascending=False)."),

 ("## 2. ¿Cuándo faltan? Al azar o en bloque",
  "No es lo mismo que falten días sueltos (al azar) que **meses enteros** seguidos. Mira la peor "
  "estación mes a mes: ¿cuántos días hay y cuántos faltan?",
  "Faltantes por mes en la peor estación",
  '''est = aire[aire["estacion"] == peor].copy()
est["mes"] = est["fecha"].dt.month
por_mes = est.assign(falta=est["pm25"].isna()).groupby("mes")["falta"].agg(["size", "sum"])
meses_vacios = list(por_mes.index[por_mes["sum"] == por_mes["size"]])
primer_dato = est.loc[est["pm25"].notna(), "fecha"].min()
print(por_mes)
print("meses completamente vacíos:", meses_vacios, "| primer dato:", primer_dato.date())''',
  '''est = aire[aire["estacion"] == peor].copy()
est["mes"] = est["fecha"].dt.month
por_mes = est.assign(falta=est["pm25"].isna()).groupby("mes")["falta"].agg(["size", "sum"])
print(por_mes)
# TODO: lista de meses donde faltan TODOS los días (sum == size)
meses_vacios = ...
# TODO: fecha del primer día con pm25 medido
primer_dato = ...
print("meses completamente vacíos:", meses_vacios, "| primer dato:", primer_dato)''',
  '''_e = aire[(aire["estacion"] == peor)]
_m = _e.assign(falta=_e["pm25"].isna()).groupby(_e["fecha"].dt.month)["falta"].agg(["size", "sum"])
assert list(meses_vacios) == list(_m.index[_m["sum"] == _m["size"]]), "Filtra por_mes.index donde sum == size"
assert pd.Timestamp(primer_dato) == _e.loc[_e["pm25"].notna(), "fecha"].min(), "Busca el mínimo de fecha donde pm25 no es nulo"''',
  'list(por_mes.index[por_mes["sum"] == por_mes["size"]]) y est.loc[est["pm25"].notna(), "fecha"].min().'),

 ("## 3. Nunca rellenes con cero",
  "Un cero en PM2.5 significa «aire perfectamente limpio», no «no hay dato». Compara el promedio "
  "honesto (ignorando los `NaN`, que es lo que hace `.mean()`) con el de alguien que rellenó con 0.",
  "Mide el sesgo de rellenar con 0",
  '''prom_honesto = est["pm25"].mean()
prom_con_ceros = est["pm25"].fillna(0).mean()
sesgo_pct = 100 * (prom_con_ceros - prom_honesto) / prom_honesto
print(f"honesto: {prom_honesto:.1f} µg/m³ | con ceros: {prom_con_ceros:.1f} µg/m³ | sesgo: {sesgo_pct:.0f}%")''',
  '''# TODO: promedio ignorando NaN, y promedio si rellenas con 0 (fillna(0))
prom_honesto = ...
prom_con_ceros = ...
# TODO: sesgo en %: 100 * (con_ceros - honesto) / honesto
sesgo_pct = ...
print(prom_honesto, prom_con_ceros, sesgo_pct)''',
  '''assert abs(prom_honesto - est["pm25"].mean()) < 1e-9
assert abs(prom_con_ceros - est["pm25"].fillna(0).mean()) < 1e-9
assert abs(sesgo_pct - 100 * (prom_con_ceros - prom_honesto) / prom_honesto) < 1e-9
assert sesgo_pct < -20, "Rellenar con 0 debería bajar mucho el promedio"''',
  'est["pm25"].mean() y est["pm25"].fillna(0).mean().'),

 ("## 4. La comparación justa",
  "Pero incluso el promedio «honesto» engaña si los huecos caen en una **época del año**. "
  "En Santiago el PM2.5 sube en otoño-invierno. Si la peor estación solo tiene datos desde mayo, "
  "su promedio es **de invierno**. Compárala con Cerro Navia (también en Santiago): primero ingenuamente, "
  "después **solo en los días en que ambas midieron**.",
  "Compara en los mismos días",
  '''otra = aire[aire["estacion"] == "Cerro Navia"]
ingenua = {peor: est["pm25"].mean(), "Cerro Navia": otra["pm25"].mean()}
ambas = pd.merge(est[["fecha", "pm25"]], otra[["fecha", "pm25"]], on="fecha",
                 suffixes=("_peor", "_cn")).dropna()
justa = {peor: ambas["pm25_peor"].mean(), "Cerro Navia": ambas["pm25_cn"].mean()}
print("ingenua:", {k: round(float(v), 1) for k, v in ingenua.items()})
print("justa (", len(ambas), "días comunes):", {k: round(float(v), 1) for k, v in justa.items()})
mas_alta_ingenua = max(ingenua, key=ingenua.get)
mas_alta_justa = max(justa, key=justa.get)
print("más contaminada — ingenua:", mas_alta_ingenua, "| justa:", mas_alta_justa)''',
  '''otra = aire[aire["estacion"] == "Cerro Navia"]
ingenua = {peor: est["pm25"].mean(), "Cerro Navia": otra["pm25"].mean()}
# Unimos por fecha y botamos los días donde alguna de las dos no midió
ambas = pd.merge(est[["fecha", "pm25"]], otra[["fecha", "pm25"]], on="fecha",
                 suffixes=("_peor", "_cn")).dropna()
# TODO: promedio de cada estación SOLO en los días comunes (columnas de 'ambas')
justa = {peor: ..., "Cerro Navia": ...}
mas_alta_ingenua = max(ingenua, key=ingenua.get)
# TODO: la estación más contaminada según la comparación justa
mas_alta_justa = ...
print("ingenua:", mas_alta_ingenua, "| justa:", mas_alta_justa)''',
  '''assert abs(justa[peor] - ambas["pm25_peor"].mean()) < 1e-9
assert abs(justa["Cerro Navia"] - ambas["pm25_cn"].mean()) < 1e-9
assert mas_alta_justa == max(justa, key=justa.get)''',
  'justa = {peor: ambas["pm25_peor"].mean(), "Cerro Navia": ambas["pm25_cn"].mean()}.'),

 ("## 5. Faltante estructural: «no se mide» no es «se perdió»",
  "La temperatura falta en muchas filas, pero no por fallas: varias estaciones **no tienen sensor "
  "meteorológico**. Eso es un faltante **estructural** y se documenta distinto: no hay nada que "
  "recuperar ni que corregir.",
  "Encuentra las estaciones sin meteorología",
  '''sin_meteo = sorted(aire.groupby("estacion")["temp_media"].apply(lambda s: s.isna().all())
                   .loc[lambda s: s].index)
print(len(sin_meteo), "estaciones sin temperatura en todo el período:", sin_meteo)''',
  '''# TODO: lista ordenada de estaciones cuya temp_media está vacía TODOS los días
# pista: aire.groupby("estacion")["temp_media"].apply(lambda s: s.isna().all())
sin_meteo = ...
print(sin_meteo)''',
  '''_t = aire.groupby("estacion")["temp_media"].count()
assert sorted(sin_meteo) == sorted(_t[_t == 0].index), "Son las estaciones con 0 valores de temp_media"''',
  "Agrupa por estación, revisa si isna().all() y quédate con las que dan True."),

 ("## 6. Documentar la decisión (la nota metodológica)",
  "Ahora decide, con una regla **escrita y pareja para todas**: menos de 10% de faltantes → "
  "*usar*; entre 10% y 30% → *usar con advertencia*; más de 30% → *excluir de comparaciones*. "
  "Una tabla así va como anexo de cualquier informe.",
  "Arma la tabla de decisiones",
  '''def decidir(pct):
    if pct < 10:
        return "usar"
    elif pct <= 30:
        return "usar con advertencia"
    return "excluir de comparaciones"

nota = pd.DataFrame({
    "dias": aire.groupby("estacion").size(),
    "dias_validos": aire.groupby("estacion")["pm25"].count(),
    "pct_faltante": (100 * aire["pm25"].isna().groupby(aire["estacion"]).mean()).round(1),
})
nota["decision"] = nota["pct_faltante"].apply(decidir)
nota = nota.sort_values("pct_faltante", ascending=False)
print(nota)''',
  '''def decidir(pct):
    # TODO: devuelve "usar", "usar con advertencia" o "excluir de comparaciones" según la regla
    ...

nota = pd.DataFrame({
    "dias": aire.groupby("estacion").size(),
    "dias_validos": aire.groupby("estacion")["pm25"].count(),
    "pct_faltante": (100 * aire["pm25"].isna().groupby(aire["estacion"]).mean()).round(1),
})
nota["decision"] = nota["pct_faltante"].apply(decidir)
nota = nota.sort_values("pct_faltante", ascending=False)
print(nota)''',
  '''assert decidir(5) == "usar" and decidir(20) == "usar con advertencia" and decidir(45) == "excluir de comparaciones"
assert set(nota["decision"]) <= {"usar", "usar con advertencia", "excluir de comparaciones"}
assert nota.loc[peor, "decision"] == "excluir de comparaciones"''',
  "if pct < 10: ... elif pct <= 30: ... y por defecto 'excluir de comparaciones'."),
]

PROF_HEADER = '''# R1-04 · Limpieza de datos — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: en la lección los errores eran inyectados; aquí los faltantes
son **reales**. PM2.5 diario de 14 estaciones de monitoreo SINCA, enero–septiembre de 2026
(`aire_nuevos.csv`). Vas a diagnosticar por estación, ver si faltan **al azar o en bloque**,
medir el sesgo de rellenar con cero, hacer una **comparación justa** y escribir la
**nota metodológica** con tu decisión.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_CIERRE = '''## ✍️ Para tu informe

Escribe en tres líneas la nota metodológica que acompañaría un ranking de estaciones 2026: qué
estaciones excluiste, por qué, y qué le pasaba al ranking si no lo hacías.

> Lo honesto no es tener datos completos (casi nunca los tendrás): es **decir qué falta y qué
> hiciste con eso**.

---

*Fin de la profundización de R1-04.*'''


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


README = '''# R1-04 · Limpieza de datos

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-04-limpieza-de-datos/leccion.ipynb)

Dejar un dataset sucio listo para analizar: **diagnóstico** (`info`, `isna`, `duplicated`,
`value_counts`), **texto** (`.str.strip().str.title()`), **sinónimos** con diccionario
(`replace`/`map`), la **trampa del punto de miles** (`"2.425"` no es 2,425), **imposibles** a
`NaN` sin inventar, **duplicados**, una función `limpiar()` reutilizable y una **auditoría**
contra la fuente oficial.

**Datos.** `matricula_sucia.csv`: 1.545 establecimientos de la matrícula oficial 2025 (MINEDUC)
con errores típicos de planilla inyectados con semilla fija (regiones escritas de 23 formas,
dependencias abreviadas, rural como «Sí/No/0/1», comunas en MAYÚSCULAS con espacios, matrícula
como texto con «s/i» y punto de miles, -1 imposibles, 45 filas pegadas dos veces). Se audita
contra `matricula.csv` (cifra oficial) por RBD. La profundización usa `aire_nuevos.csv`:
PM2.5 diario de 14 estaciones SINCA, ene–sep 2026, con faltantes **reales**.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: faltantes reales por estación, al azar vs en bloque, comparación justa, nota metodológica.
- [`GUIA_APRENDIZAJE.md`](GUIA_APRENDIZAJE.md) — pistas progresivas, errores frecuentes y autoevaluación.
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
