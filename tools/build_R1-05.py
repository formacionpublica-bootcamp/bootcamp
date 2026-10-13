"""build_R1-05.py — módulo R1-05 (SQL para análisis).

Rama R1 (Análisis y Visualización). SQL desde Python con SQLite en memoria
(sqlite3 + pandas to_sql / read_sql_query): SELECT, WHERE, ORDER BY/LIMIT,
GROUP BY, HAVING, JOIN y LEFT JOIN, más la interpretación promedio vs mediana.

Rearmado 2026 (reemplaza la versión sobre parques): lección con la matrícula 2025
(MINEDUC) en dos tablas relacionales — conteos por RBD (matricula_rbd.csv) y el
directorio oficial (directorio_establecimientos.csv), con 4 RBD huérfanos reales.
Profundiza = transferencia: parques nacionales (parques.csv) con LIKE, HAVING,
subconsultas y CASE WHEN. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-05.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-05-sql-para-analisis")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request, sqlite3
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["matricula_rbd.csv", "directorio_establecimientos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

df_matricula = pd.read_csv("matricula_rbd.csv")                 # cuántos estudiantes (por RBD)
df_directorio = pd.read_csv("directorio_establecimientos.csv")  # quién es cada RBD

# Una base de datos SQLite en memoria con DOS tablas
conn = sqlite3.connect(":memory:")
df_matricula.to_sql("matricula", conn, index=False, if_exists="replace")
df_directorio.to_sql("directorio", conn, index=False, if_exists="replace")

def consultar(sql):
    """Ejecuta una consulta SQL y devuelve el resultado como tabla de pandas."""
    return pd.read_sql_query(sql, conn)

print("Tablas en la base:", list(consultar("SELECT name FROM sqlite_master WHERE type='table'")["name"]))
consultar("SELECT * FROM directorio LIMIT 5")'''

INTRO = '''## ¿Por qué SQL?

Hasta ahora traías **toda** la tabla a Python y la filtrabas con pandas. Los sistemas del Estado
(SIGE del MINEDUC, registros de salud, el Registro Social de Hogares) no viven en un CSV: viven en
**bases de datos** con millones de filas, y se consultan con **SQL**. SQL es la «boleta de pedido»
que le entregas a la base: describes **qué** quieres y ella te devuelve **solo eso**.

Usaremos **SQLite**, que viene incluido en Python (`sqlite3`): cero instalación, funciona en Colab.
La base tiene dos tablas, igual que en R1-03:

| Tabla | Filas | Columnas |
|---|---|---|
| `matricula` | 10.949 | `rbd`, `mat_total`, `mat_hombres`, `mat_mujeres` |
| `directorio` | 10.945 | `rbd`, `nombre`, `dependencia`, `rural` (1 = rural), `region`, `comuna` |

Toda consulta básica tiene esta forma (por costumbre, las palabras clave en MAYÚSCULAS):

```sql
SELECT columnas
FROM   tabla
WHERE  condición          -- filtra filas
GROUP BY columna          -- agrupa
HAVING condición          -- filtra grupos
ORDER BY columna DESC     -- ordena
LIMIT  n                  -- corta
```

> En cada ejercicio guardas tu consulta **como texto** en una variable (`sql_01`, `sql_02`, ...)
> y la ejecutas con `consultar(...)`.'''

EJ = [
 ("## 1. SELECT y FROM: elegir columnas",
  "`SELECT` dice **qué columnas**; `FROM`, de **qué tabla**. `SELECT *` trae todas. Es el "
  "equivalente a `df[[\"nombre\", \"comuna\"]]`, pero pidiéndoselo a la base.",
  '''consultar("SELECT nombre, region FROM directorio LIMIT 3")''',
  "Tu primer SELECT",
  '''sql_01 = "SELECT nombre, comuna, dependencia FROM directorio"
r = consultar(sql_01)
print(r.shape)
r.head()''',
  '''# TODO: las columnas nombre, comuna y dependencia de TODOS los establecimientos del directorio
sql_01 = "..."
r = consultar(sql_01) if sql_01 != "..." else None
r''',
  '''r = consultar(sql_01)
assert list(r.columns) == ["nombre", "comuna", "dependencia"], f"Columnas obtenidas: {list(r.columns)}"
assert len(r) == len(df_directorio), "Sin WHERE ni LIMIT deberías traer todas las filas"''',
  'SELECT nombre, comuna, dependencia FROM directorio',
  None),

 ("## 2. WHERE: filtrar filas",
  '''`WHERE` se queda con las filas que cumplen una condición. Operadores: `=` (¡uno solo, no `==`!),
`<>` (distinto), `>`, `<`, `>=`, `<=`, y se combinan con `AND` / `OR`. **Los textos van entre
comillas simples**: `WHERE region = 'Maule'`.

Pregunta real: la Seremi de La Araucanía planifica transporte escolar y quiere la lista de
**establecimientos rurales** de su región.''',
  None,
  "Los establecimientos rurales de La Araucanía",
  '''sql_02 = """
SELECT nombre, comuna
FROM directorio
WHERE region = 'La Araucanía' AND rural = 1
"""
r = consultar(sql_02)
print("establecimientos rurales en La Araucanía:", len(r))
r.head()''',
  '''# TODO: nombre y comuna de los establecimientos de 'La Araucanía' que son rurales (rural = 1)
sql_02 = """
SELECT nombre, comuna
FROM directorio
WHERE ...
"""
r = consultar(sql_02) if "..." not in sql_02 else None
r''',
  '''r = consultar(sql_02)
_esp = df_directorio[(df_directorio["region"] == "La Araucanía") & (df_directorio["rural"] == 1)]
assert len(r) == len(_esp), f"Esperaba {len(_esp)} filas, obtuve {len(r)}"
assert list(r.columns) == ["nombre", "comuna"]''',
  "WHERE region = 'La Araucanía' AND rural = 1  (comillas simples y tilde).",
  None),

 ("## 3. ORDER BY y LIMIT: rankings",
  "`ORDER BY columna DESC` ordena de mayor a menor (`ASC`, el defecto, de menor a mayor). "
  "`LIMIT n` se queda con las primeras `n` filas. Juntos arman un **ranking**: ¿cuáles son los "
  "5 establecimientos con más estudiantes del país?",
  None,
  "Los 5 establecimientos más grandes",
  '''sql_03 = "SELECT rbd, mat_total FROM matricula ORDER BY mat_total DESC LIMIT 5"
consultar(sql_03)''',
  '''# TODO: rbd y mat_total de la tabla matricula, de mayor a menor, solo los 5 primeros
sql_03 = "..."
consultar(sql_03) if sql_03 != "..." else None''',
  '''r = consultar(sql_03)
assert len(r) == 5, "Usa LIMIT 5"
assert list(r["mat_total"]) == sorted(df_matricula["mat_total"], reverse=True)[:5], "Ordena con ORDER BY mat_total DESC"''',
  "SELECT rbd, mat_total FROM matricula ORDER BY mat_total DESC LIMIT 5",
  '''# Ojo: solo vemos el RBD, no el nombre. Para ponerle nombre hay que CRUZAR con el directorio
# → lo harás con JOIN en el ejercicio 6.'''),

 ("## 4. GROUP BY: resumir por grupo",
  '''Las **funciones de agregación** convierten muchas filas en un número: `COUNT(*)`, `SUM(col)`,
`AVG(col)`, `MIN(col)`, `MAX(col)`. Con `GROUP BY` se aplican **a cada grupo** por separado (la
tabla dinámica de Excel). `AS` le pone nombre a la columna resultante.

> **Regla de oro:** en el `SELECT` solo van las columnas del `GROUP BY` y funciones de agregación.''',
  None,
  "Establecimientos por dependencia",
  '''sql_04 = """
SELECT dependencia, COUNT(*) AS n
FROM directorio
GROUP BY dependencia
ORDER BY n DESC
"""
consultar(sql_04)''',
  '''# TODO: cuántos establecimientos hay por dependencia (columna n), de mayor a menor
sql_04 = """
SELECT dependencia, ...
FROM directorio
...
"""
consultar(sql_04) if "..." not in sql_04 else None''',
  '''r = consultar(sql_04)
_esp = df_directorio["dependencia"].value_counts()
assert list(r.columns) == ["dependencia", "n"], "Columnas: dependencia y n (COUNT(*) AS n)"
assert list(r["n"]) == list(_esp.values), "Revisa el conteo y el orden (ORDER BY n DESC)"''',
  "SELECT dependencia, COUNT(*) AS n FROM directorio GROUP BY dependencia ORDER BY n DESC",
  None),

 ("## 5. HAVING: filtrar grupos (no filas)",
  '''`WHERE` filtra **filas** antes de agrupar; `HAVING` filtra **grupos** después de agrupar.
Por eso `WHERE COUNT(*) >= 40` da error (el conteo todavía no existe) y `HAVING COUNT(*) >= 40` funciona.

Pregunta real: ¿en qué **comunas** se concentra la educación rural? Busca las comunas con **al
menos 40 establecimientos rurales** (pistas para priorizar programas de escuelas multigrado y
transporte escolar).''',
  None,
  "Comunas con 40 o más establecimientos rurales",
  '''sql_05 = """
SELECT comuna, COUNT(*) AS n_rurales
FROM directorio
WHERE rural = 1
GROUP BY comuna
HAVING COUNT(*) >= 40
ORDER BY n_rurales DESC
"""
consultar(sql_05)''',
  '''# TODO: por comuna, cuántos establecimientos RURALES hay (n_rurales); deja solo las comunas con 40 o más
sql_05 = """
SELECT comuna, COUNT(*) AS n_rurales
FROM directorio
WHERE ...
GROUP BY comuna
HAVING ...
ORDER BY n_rurales DESC
"""
consultar(sql_05) if "..." not in sql_05 else None''',
  '''r = consultar(sql_05)
_c = df_directorio[df_directorio["rural"] == 1].groupby("comuna").size()
_esp = _c[_c >= 40].sort_values(ascending=False)
assert set(r["comuna"]) == set(_esp.index), f"Esperaba {len(_esp)} comunas: revisa WHERE rural = 1 y HAVING COUNT(*) >= 40"
assert int(r["n_rurales"].min()) >= 40''',
  "WHERE rural = 1 (filtra filas) ... HAVING COUNT(*) >= 40 (filtra grupos).",
  None),

 ("## 6. JOIN: cruzar dos tablas",
  '''`JOIN ... ON` cruza dos tablas por la llave, igual que `pd.merge` en R1-03. Se usan **alias**
cortos (`m`, `d`) para decir de qué tabla viene cada columna:

```sql
SELECT d.region, SUM(m.mat_total) AS estudiantes
FROM matricula AS m
JOIN directorio AS d ON m.rbd = d.rbd
GROUP BY d.region
```

Pregunta real: ¿cuántos estudiantes hay en cada región, de mayor a menor?''',
  None,
  "Estudiantes por región con JOIN",
  '''sql_06 = """
SELECT d.region, SUM(m.mat_total) AS estudiantes
FROM matricula AS m
JOIN directorio AS d ON m.rbd = d.rbd
GROUP BY d.region
ORDER BY estudiantes DESC
"""
r = consultar(sql_06)
r.head()''',
  '''# TODO: completa el JOIN (llave rbd) y el orden de mayor a menor
sql_06 = """
SELECT d.region, SUM(m.mat_total) AS estudiantes
FROM matricula AS m
JOIN directorio AS d ON ...
GROUP BY d.region
ORDER BY ...
"""
r = consultar(sql_06) if "..." not in sql_06 else None
r''',
  '''r = consultar(sql_06)
_esp = pd.merge(df_matricula, df_directorio, on="rbd").groupby("region")["mat_total"].sum().sort_values(ascending=False)
assert len(r) == len(_esp), "Debe haber una fila por región"
assert list(r["region"]) == list(_esp.index), "Revisa el orden (ORDER BY estudiantes DESC)"
assert list(r["estudiantes"]) == list(_esp.values)''',
  "JOIN directorio AS d ON m.rbd = d.rbd ... ORDER BY estudiantes DESC",
  None),

 ("## 7. LEFT JOIN: auditar lo que no calza",
  '''El `JOIN` normal (inner) **bota** las filas sin pareja. `LEFT JOIN` las conserva y deja en
`NULL` las columnas de la otra tabla. En SQL un nulo se pregunta con `IS NULL` (nunca con `= NULL`).

Es la misma auditoría de R1-03, ahora en SQL: ¿qué RBD reportan matrícula pero **no están** en
el directorio oficial?''',
  None,
  "Encuentra los RBD huérfanos",
  '''sql_07 = """
SELECT m.rbd, m.mat_total
FROM matricula AS m
LEFT JOIN directorio AS d ON m.rbd = d.rbd
WHERE d.rbd IS NULL
"""
consultar(sql_07)''',
  '''# TODO: RBD y matrícula de la tabla matricula que NO tienen pareja en el directorio
sql_07 = """
SELECT m.rbd, m.mat_total
FROM matricula AS m
LEFT JOIN directorio AS d ON m.rbd = d.rbd
WHERE ...
"""
consultar(sql_07) if "..." not in sql_07 else None''',
  '''r = consultar(sql_07)
_esp = set(df_matricula["rbd"]) - set(df_directorio["rbd"])
assert set(r["rbd"]) == _esp, f"Esperaba {len(_esp)} RBD huérfanos: usa WHERE d.rbd IS NULL"''',
  "WHERE d.rbd IS NULL  (los que el LEFT JOIN dejó sin pareja).",
  None),

 ("## 8. Interpretar: ¿promedio o mediana?",
  '''SQL calcula el promedio con `AVG`, pero SQLite **no tiene mediana**. Lo práctico: SQL trae
los datos justos y pandas termina el cálculo. Compara el tamaño de los establecimientos
**municipales** y **particulares subvencionados** (las dos dependencias más grandes del sistema):

1. `promedios`: con SQL, el promedio de `mat_total` por dependencia (`AVG`, con JOIN).
2. `medianas`: con pandas, la mediana por dependencia sobre una consulta que traiga
   `dependencia` y `mat_total`.
3. Elige la interpretación correcta en `conclusion` (`"A"`, `"B"` o `"C"`):

- **A.** El particular subvencionado típico es mucho más grande que el municipal típico: el
  promedio y la mediana dicen lo mismo.
- **B.** El promedio exagera la diferencia: unos pocos particulares subvencionados muy grandes
  inflan su promedio; con la **mediana**, el establecimiento típico de ambas dependencias tiene
  un tamaño parecido.
- **C.** Los municipales son más grandes que los particulares subvencionados.''',
  None,
  "Promedio (SQL) vs mediana (pandas)",
  '''promedios = consultar("""
SELECT d.dependencia, AVG(m.mat_total) AS promedio
FROM matricula AS m JOIN directorio AS d ON m.rbd = d.rbd
GROUP BY d.dependencia
""").set_index("dependencia")["promedio"]

datos = consultar("""
SELECT d.dependencia, m.mat_total
FROM matricula AS m JOIN directorio AS d ON m.rbd = d.rbd
""")
medianas = datos.groupby("dependencia")["mat_total"].median()

comparar = pd.DataFrame({"promedio": promedios.round(0), "mediana": medianas})
print(comparar.loc[["Municipal", "Particular subvencionado"]])
conclusion = "B"''',
  '''# TODO: promedio de mat_total por dependencia con SQL (función de agregación + JOIN + GROUP BY)
sql_prom = """
SELECT d.dependencia, ... AS promedio
FROM matricula AS m JOIN directorio AS d ON m.rbd = d.rbd
GROUP BY d.dependencia
"""
promedios = consultar(sql_prom).set_index("dependencia")["promedio"] if "..." not in sql_prom else None

datos = consultar("""
SELECT d.dependencia, m.mat_total
FROM matricula AS m JOIN directorio AS d ON m.rbd = d.rbd
""")
# TODO: mediana de mat_total por dependencia, con pandas sobre 'datos'
medianas = ...

# TODO: tu interpretación: "A", "B" o "C"
conclusion = ...''',
  '''_x = pd.merge(df_matricula, df_directorio, on="rbd")
_prom = _x.groupby("dependencia")["mat_total"].mean()
_med = _x.groupby("dependencia")["mat_total"].median()
assert abs(promedios["Municipal"] - _prom["Municipal"]) < 0.01, "Revisa el AVG por dependencia"
assert abs(medianas["Particular subvencionado"] - _med["Particular subvencionado"]) < 0.01, "Revisa la mediana por dependencia"
_r_prom = _prom["Particular subvencionado"] / _prom["Municipal"]
_r_med = _med["Particular subvencionado"] / _med["Municipal"]
_letra = "C" if _r_prom < 1 else ("B" if _r_med < 1.15 and _r_prom > 1.3 else "A")
assert str(conclusion).strip().upper() == _letra, "Compara la razón entre dependencias usando el promedio y usando la mediana"''',
  "promedios: AVG(m.mat_total); medianas: datos.groupby('dependencia')['mat_total'].median(). Luego compara.",
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige)

Un titular dice: «Los colegios particulares subvencionados tienen 44% más estudiantes que los
municipales». ¿Es falso? ¿Es engañoso? Escribe en una frase cómo lo reformularías con lo que
viste en el ejercicio 8.'''

CIERRE = '''## Errores típicos en SQL

- **Texto sin comillas** → `WHERE region = Maule` falla; es `WHERE region = 'Maule'`.
- **`==` en vez de `=`** → en SQL la igualdad es un solo `=`.
- **`= NULL`** → nunca es verdadero; se pregunta con `IS NULL` / `IS NOT NULL`.
- **Filtrar un conteo con WHERE** → `WHERE COUNT(*) > 40` falla; los grupos se filtran con `HAVING`.
- **Columna ambigua en un JOIN** → si `rbd` está en ambas tablas, di de cuál: `m.rbd`.
- **Esperar orden sin pedirlo** → sin `ORDER BY`, la base devuelve en cualquier orden.

## Cierre

- `SELECT/FROM` elige, `WHERE` filtra filas, `GROUP BY` resume, `HAVING` filtra grupos,
  `ORDER BY/LIMIT` rankea.
- `JOIN` cruza por la llave; `LEFT JOIN ... WHERE ... IS NULL` audita lo que no calza.
- SQL trae lo justo; pandas termina lo que SQL no sabe hacer (como la mediana).

> *En R1-06 vas a mirar esos promedios y medianas con lupa: estadística descriptiva para no
> dejarte engañar por un solo número.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-05", "SQL para análisis", "R1", "Analista de Datos", "6",
                      ["Consultar una base con **SELECT / FROM / WHERE**.",
                       "Armar rankings con **ORDER BY** y **LIMIT**.",
                       "Resumir con **GROUP BY** y filtrar grupos con **HAVING**.",
                       "Cruzar tablas con **JOIN** y auditar con **LEFT JOIN ... IS NULL**.",
                       "Combinar SQL y pandas para interpretar **promedio vs mediana**."],
                      "consultar una base de datos relacional con SQL para responder preguntas de gestión.",
                      "matrícula 2025 por RBD × directorio oficial de establecimientos (MINEDUC), en SQLite.",
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


# ── Profundiza: transferencia a parques nacionales ─────────────────────────────
PROF_PREP = f'''import pandas as pd, os, urllib.request, sqlite3
CSV = "parques.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/parques.csv", CSV)
df = pd.read_csv(CSV)            # 24 parques nacionales (CONAF / SNASPE)
conn = sqlite3.connect(":memory:")
df.to_sql("parques", conn, index=False, if_exists="replace")

def consultar(sql):
    return pd.read_sql_query(sql, conn)

consultar("SELECT * FROM parques LIMIT 5")'''

PROF_EJ = [
 ("## 1. LIKE: buscar texto parcial",
  "`LIKE` busca patrones: `%` significa «cualquier cosa». `nombre LIKE 'Laguna%'` = los que "
  "empiezan con «Laguna». Ordénalos por año de declaración.",
  "Parques cuyo nombre empieza con «Laguna»",
  '''sql_01 = "SELECT nombre, anio FROM parques WHERE nombre LIKE 'Laguna%' ORDER BY anio"
consultar(sql_01)''',
  '''# TODO: nombre y anio de los parques cuyo nombre empieza con 'Laguna', ordenados por anio
sql_01 = "..."
consultar(sql_01) if sql_01 != "..." else None''',
  '''r = consultar(sql_01)
_esp = df[df["nombre"].str.startswith("Laguna")].sort_values("anio")
assert list(r["nombre"]) == list(_esp["nombre"])''',
  "WHERE nombre LIKE 'Laguna%' ORDER BY anio"),

 ("## 2. GROUP BY + HAVING",
  "¿Qué regiones tienen **3 o más** parques nacionales? Muestra cuántos y cuántas hectáreas suman.",
  "Regiones con 3 o más parques",
  '''sql_02 = """
SELECT region, COUNT(*) AS n_parques, SUM(superficie_ha) AS hectareas
FROM parques
GROUP BY region
HAVING COUNT(*) >= 3
ORDER BY n_parques DESC, hectareas DESC
"""
consultar(sql_02)''',
  '''# TODO: por región, n_parques y hectareas; solo regiones con 3 o más parques
sql_02 = """
SELECT region, COUNT(*) AS n_parques, SUM(superficie_ha) AS hectareas
FROM parques
GROUP BY region
...
"""
consultar(sql_02) if "..." not in sql_02 else None''',
  '''r = consultar(sql_02)
_c = df["region"].value_counts()
assert set(r["region"]) == set(_c[_c >= 3].index)
assert int(r["n_parques"].min()) >= 3''',
  "HAVING COUNT(*) >= 3"),

 ("## 3. Subconsulta: comparar contra el promedio",
  "Una consulta puede ir **dentro** de otra. `(SELECT AVG(superficie_ha) FROM parques)` devuelve un "
  "número que puedes usar en el `WHERE`. ¿Cuántos parques son más grandes que el parque «promedio»?",
  "Parques sobre el promedio",
  '''sql_03 = """
SELECT nombre, superficie_ha
FROM parques
WHERE superficie_ha > (SELECT AVG(superficie_ha) FROM parques)
ORDER BY superficie_ha DESC
"""
r = consultar(sql_03)
print(len(r), "de", len(df), "parques superan el promedio")
r''',
  '''# TODO: nombre y superficie de los parques con superficie MAYOR al promedio (usa una subconsulta)
sql_03 = """
SELECT nombre, superficie_ha
FROM parques
WHERE superficie_ha > ...
ORDER BY superficie_ha DESC
"""
consultar(sql_03) if "..." not in sql_03 else None''',
  '''r = consultar(sql_03)
assert len(r) == int((df["superficie_ha"] > df["superficie_ha"].mean()).sum())
assert len(r) < len(df) / 2, "Pocos parques gigantes inflan el promedio: menos de la mitad lo supera"''',
  "WHERE superficie_ha > (SELECT AVG(superficie_ha) FROM parques)"),

 ("## 4. CASE WHEN: crear categorías dentro de la consulta",
  "`CASE WHEN condición THEN valor ... ELSE valor END` crea una columna nueva, como un `SI()` de "
  "Excel. Clasifica cada parque por **época de declaración** y cuenta cuántos hay en cada una.",
  "Parques por época",
  '''sql_04 = """
SELECT CASE
         WHEN anio < 1960 THEN '1. antes de 1960'
         WHEN anio < 1990 THEN '2. 1960-1989'
         ELSE '3. 1990 en adelante'
       END AS epoca,
       COUNT(*) AS n
FROM parques
GROUP BY epoca
ORDER BY epoca
"""
consultar(sql_04)''',
  '''# TODO: completa el CASE para las tres épocas: antes de 1960, 1960-1989, 1990 en adelante
sql_04 = """
SELECT CASE
         WHEN anio < 1960 THEN '1. antes de 1960'
         ...
       END AS epoca,
       COUNT(*) AS n
FROM parques
GROUP BY epoca
ORDER BY epoca
"""
consultar(sql_04) if "..." not in sql_04 else None''',
  '''r = consultar(sql_04)
_esp = [int((df["anio"] < 1960).sum()), int(((df["anio"] >= 1960) & (df["anio"] < 1990)).sum()), int((df["anio"] >= 1990).sum())]
assert list(r["n"]) == _esp, f"Esperaba {_esp} parques por época"''',
  "WHEN anio < 1990 THEN '2. 1960-1989' ELSE '3. 1990 en adelante' END"),

 ("## 5. WHERE y HAVING en la misma consulta",
  "El orden lógico de SQL es `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`. Primero se "
  "filtran filas, después se agrupa, después se filtran grupos. Pregunta: considerando **solo los "
  "parques declarados antes de 1970**, ¿qué regiones ya protegían **más de 1 millón de hectáreas**?",
  "Regiones con más de 1 millón de ha protegidas antes de 1970",
  '''sql_05 = """
SELECT region, SUM(superficie_ha) AS hectareas
FROM parques
WHERE anio < 1970
GROUP BY region
HAVING SUM(superficie_ha) > 1000000
ORDER BY hectareas DESC
"""
consultar(sql_05)''',
  '''# TODO: WHERE para los parques anteriores a 1970 y HAVING para las regiones con más de 1.000.000 ha
sql_05 = """
SELECT region, SUM(superficie_ha) AS hectareas
FROM parques
WHERE ...
GROUP BY region
HAVING ...
ORDER BY hectareas DESC
"""
consultar(sql_05) if "..." not in sql_05 else None''',
  '''r = consultar(sql_05)
_s = df[df["anio"] < 1970].groupby("region")["superficie_ha"].sum()
assert set(r["region"]) == set(_s[_s > 1_000_000].index)''',
  "WHERE anio < 1970 ... HAVING SUM(superficie_ha) > 1000000"),
]

PROF_HEADER = '''# R1-05 · SQL para análisis — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: el mismo SQL sobre otro dominio — los **24 parques nacionales**
de Chile (CONAF / SNASPE: nombre, región, año de declaración y superficie). Herramientas nuevas:
`LIKE`, **subconsultas**, `CASE WHEN` y `WHERE` + `HAVING` juntos (el orden lógico de SQL).

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-05.*"))
    nb.cells = cells
    return nb


README = '''# R1-05 · SQL para análisis

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-05-sql-para-analisis/leccion.ipynb)

Consultar una base de datos con **SQL** desde Python (SQLite en memoria, `sqlite3` +
`pandas.to_sql` / `read_sql_query`): `SELECT`/`WHERE`, `ORDER BY`/`LIMIT`, `GROUP BY`/`HAVING`,
`JOIN` y `LEFT JOIN ... IS NULL` para auditar, y SQL + pandas para interpretar promedio vs mediana.

**Datos.** La matrícula 2025 (MINEDUC) en dos tablas relacionales: `matricula_rbd.csv` (10.949
conteos por RBD) y `directorio_establecimientos.csv` (10.945 establecimientos oficiales, con
dependencia, ruralidad, región y comuna) — con 4 RBD huérfanos reales. La profundización usa
`parques.csv`: 24 parques nacionales de Chile (CONAF / SNASPE).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: `LIKE`, subconsultas, `CASE WHEN`, `WHERE` + `HAVING` sobre parques nacionales.
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
