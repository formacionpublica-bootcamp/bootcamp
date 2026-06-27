# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A4 (SQL fundamentos):
A4/profundiza.ipynb (estudiante) + A4/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A4-sql-fundamentos"

TITULO = """# A4 · SQL — Profundización (opcional) 🔬

**Formación Pública — Capa A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A4 y quieres entender el *porqué* —no solo
el *cómo*—, aquí vas a un nivel más hondo: por qué SQL te hace pensar por **conjuntos** y no fila a
fila, en qué **orden de verdad** ejecuta la base tu consulta (que **no** es el orden en que la
escribes), la trampa de los **NULL** (la lógica de tres valores que arruina tantos `WHERE`), y por qué
existen los **índices** (la diferencia entre una consulta instantánea y una que tarda una eternidad).

Menos sintaxis nueva, más **pensamiento de base de datos**. Los ejercicios del final son más conceptuales.

> Requisito: haber hecho `leccion.ipynb` de A4. Mismo dataset: 24 parques nacionales de Chile (CONAF)."""

CARGA = """import os, urllib.request, time
import pandas as pd
import sqlite3

if not os.path.exists("parques.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A4-sql-fundamentos/parques.csv"
        urllib.request.urlretrieve(url, "parques.csv")
    except Exception:
        print("Si estás en Colab, sube parques.csv manualmente.")

df = pd.read_csv("parques.csv")
conn = sqlite3.connect(":memory:")
df.to_sql("parques", conn, index=False, if_exists="replace")

def consultar(sql):
    \"\"\"Ejecuta una consulta SQL y devuelve el resultado como tabla.\"\"\"
    return pd.read_sql_query(sql, conn)

print(f"Base lista. La tabla 'parques' tiene {len(df)} filas y columnas: {list(df.columns)}")
consultar("SELECT * FROM parques LIMIT 3")"""

S1 = """## 1. El modelo relacional: pensar por CONJUNTOS, no fila a fila

En Python, cuando recorres datos, sueles pensar **fila a fila**: "para cada parque, mira su superficie,
y si es grande, guárdalo". Es un `for`. SQL te obliga a pensar distinto: **por conjuntos**.

Una consulta SQL no dice *cómo* recorrer los datos; describe **qué conjunto de filas quieres** y deja
que la base decida cómo conseguirlo. Por eso SQL es **declarativo**: tú declaras el resultado, no el
procedimiento.

- **Fila a fila (imperativo):** "empieza arriba, baja una por una, ve evaluando…". Es lo que harías a mano.
- **Por conjuntos (declarativo):** "del conjunto de parques, quédate con el **subconjunto** de los que
  cumplen la condición". No hay un "primero" ni un "después": es una operación sobre todo el grupo.

Esto tiene una consecuencia profunda y práctica: **sin `ORDER BY`, una tabla no tiene orden**. Un
conjunto, en matemáticas, no está ordenado: {parque A, parque B} es el mismo conjunto que {parque B,
parque A}. La base puede devolverte las filas en cualquier orden, y puede cambiarlo entre ejecuciones.
Si quieres un orden, **tienes que pedirlo**. Veámoslo: la misma pregunta, resuelta "a la pandas"
(fila a fila) y "a la SQL" (por conjuntos), dan lo mismo, pero el camino mental es distinto."""

S1_CODE = """# Pregunta: ¿cuántos parques superan las 200.000 hectáreas?

# (a) Estilo "fila a fila" en Python: un recorrido explícito
contador = 0
for valor in df["superficie_ha"]:
    if valor > 200000:        # evaluamos una fila a la vez
        contador += 1
print(f"Estilo fila a fila (Python): {contador} parques")

# (b) Estilo "por conjuntos" en SQL: describimos el subconjunto, no el recorrido
r = consultar("SELECT COUNT(*) AS n FROM parques WHERE superficie_ha > 200000")
print(f"Estilo por conjuntos (SQL):  {r.iloc[0]['n']} parques")

print("\\nMismo resultado. Pero en SQL nunca dijiste 'recorre'; describiste el conjunto que querías.")"""

S2 = """## 2. El orden LÓGICO de ejecución (no es el orden en que lo escribes)

Escribes la consulta empezando por `SELECT`… pero la base **no la ejecuta en ese orden**. El orden
*lógico* en que se procesa una consulta es:

```
1. FROM      ┐  de qué tabla(s) salen las filas
2. WHERE     │  filtra filas individuales
3. GROUP BY  │  arma los grupos
4. HAVING    │  filtra grupos (no filas)
5. SELECT    │  recién aquí se eligen/calculan las columnas
6. ORDER BY  ┘  por último, se ordena el resultado
```

*(Y `LIMIT`, si existe, va al final de todo: después de `ORDER BY`, para quedarse solo con las primeras filas.)*

Saber esto **explica varios misterios** que confunden a todo el mundo:

- **Por qué `WHERE` no debería usar un alias de `SELECT`.** Si escribes
  `SELECT superficie_ha/10000 AS km2 ... WHERE km2 > 5`, en la mayoría de los motores (PostgreSQL,
  BigQuery, SQL Server) **da error**: cuando se ejecuta `WHERE`, el `SELECT` **todavía no ocurrió**, así
  que el alias `km2` no existe aún. SQLite lo **tolera** por ser más permisivo, pero es un hábito
  peligroso que se romperá en cualquier otro motor: escribe la expresión completa en el `WHERE`.
- **Por qué para filtrar un conteo se usa `HAVING` y no `WHERE`.** `WHERE` filtra **antes** de agrupar
  (no existen los grupos todavía); `HAVING` filtra **después** de `GROUP BY`, cuando ya hay grupos con
  su `COUNT`. Por eso "regiones con más de 2 parques" va en `HAVING COUNT(*) > 2`.
- **Por qué `ORDER BY` sí puede usar un alias.** Se ejecuta al final, después del `SELECT`, así que el
  alias ya existe.

Veámoslo con un ejemplo que junta las dos cosas: filtrar grupos con `HAVING` y ordenar por un alias."""

S2_CODE = """# Regiones con MÁS DE 2 parques, ordenadas por superficie total (usando alias en ORDER BY)
r = consultar('''
    SELECT region,
           COUNT(*)          AS n_parques,
           SUM(superficie_ha) AS hectareas
    FROM parques
    WHERE anio >= 1940           -- (2) filtra FILAS: solo declarados desde 1940
    GROUP BY region              -- (3) arma un grupo por región
    HAVING COUNT(*) > 2          -- (4) filtra GRUPOS: solo regiones con 3+ parques
    ORDER BY hectareas DESC      -- (6) ordena por el alias (ya existe al final)
''')
print(r.to_string(index=False))

print("\\nWHERE filtró filas ANTES de agrupar; HAVING filtró grupos DESPUÉS. Distinto momento, distinto rol.")"""

S3 = """## 3. La trampa del NULL: la lógica de TRES valores

`NULL` en SQL **no es** cero, ni texto vacío, ni "0". Significa **"desconocido / no hay dato"**. Y eso
cambia las reglas de la lógica. En la vida normal una afirmación es **verdadera o falsa**. En SQL, al
meter `NULL`, hay **tres** posibles resultados: `TRUE`, `FALSE` y `UNKNOWN` (desconocido).

La regla clave: **cualquier comparación con `NULL` da `UNKNOWN`**, no `TRUE` ni `FALSE`. Y `WHERE` solo
deja pasar las filas cuya condición es `TRUE`. Las `UNKNOWN` **se descartan**, igual que las `FALSE`.

Esto produce la trampa más clásica de SQL:

> Si una columna tiene `NULL`, **`WHERE columna != 'X'` NO devuelve esas filas**. Uno espera "todo lo
> que no sea X", e intuitivamente un dato faltante "no es X"… pero para SQL, `NULL != 'X'` es `UNKNOWN`,
> no `TRUE`, así que esa fila **no aparece**. El dato desconocido se cae silenciosamente del resultado.

Para preguntar por datos faltantes hay operadores especiales: **`IS NULL`** y **`IS NOT NULL`**
(nunca `= NULL`, que siempre da `UNKNOWN` y no sirve). Vamos a crear una tabla con un parque al que le
falta la región para verlo en vivo."""

S3_CODE = """# Creamos una tabla 'parques_nul' = copia + un parque NUEVO con region desconocida (NULL)
df_nul = df.copy()
fila_nueva = {"nombre": "Parque Sin Datos", "region": None, "anio": 2024, "superficie_ha": 5000}
df_nul = pd.concat([df_nul, pd.DataFrame([fila_nueva])], ignore_index=True)
df_nul.to_sql("parques_nul", conn, index=False, if_exists="replace")
print(f"Tabla parques_nul: {len(df_nul)} filas (una con region = NULL)")

# La trampa: "parques que NO son de Magallanes"
trampa = consultar("SELECT COUNT(*) AS n FROM parques_nul WHERE region != 'Magallanes'")
print(f"\\nWHERE region != 'Magallanes'  ->  {trampa.iloc[0]['n']} filas")
print("¡El 'Parque Sin Datos' NO está incluido, aunque su región claramente no es Magallanes!")
print("Su region es NULL: la comparación dio UNKNOWN y la fila se descartó.")

# La forma correcta de encontrar los datos faltantes
faltantes = consultar("SELECT nombre FROM parques_nul WHERE region IS NULL")
print(f"\\nWHERE region IS NULL  ->  encontró: {list(faltantes['nombre'])}")"""

S4 = """## 4. Por qué existen los ÍNDICES: consultas rápidas vs lentas

Hasta aquí la tabla tiene 24 filas: cualquier consulta es instantánea. Pero las bases del Estado tienen
**millones** de filas. Ahí aparece el problema central de rendimiento, y su solución: los **índices**.

Sin índice, para responder `WHERE region = 'Magallanes'` la base hace un **escaneo completo**
(*full scan*): recorre **todas** las filas una por una preguntando "¿esta es de Magallanes?". Con
millones de filas, eso es lentísimo.

Un **índice** es como el **índice alfabético al final de un libro**: en vez de leer el libro entero
buscando una palabra, vas al índice (ordenado), encuentras la página y saltas directo. La base
mantiene una estructura ordenada de los valores de una columna, así que `WHERE region = 'X'` salta
directo a las filas correctas sin recorrer todo.

El precio de un índice (no es gratis):
- **Ocupa espacio** en disco (es una copia ordenada de la columna).
- **Hace más lentas las escrituras**: cada `INSERT`/`UPDATE` debe actualizar también el índice.

Por eso no se indexa *todo*: se indexan las columnas por las que **se filtra o se ordena seguido**.
Vamos a demostrar el efecto creando una tabla grande (~120.000 filas) y midiendo el tiempo
de la misma consulta **sin** y **con** índice."""

S4_CODE = """# Construimos una tabla grande replicando los parques muchas veces (~120.000 filas)
df_grande = pd.concat([df] * 5000, ignore_index=True)
df_grande.to_sql("parques_grande", conn, index=False, if_exists="replace")
n = len(df_grande)
print(f"Tabla parques_grande: {n:,} filas\\n")

consulta = "SELECT COUNT(*) AS n FROM parques_grande WHERE region = 'Magallanes'"

# (a) SIN índice: la base escanea las ~120.000 filas
t0 = time.perf_counter()
for _ in range(50):
    consultar(consulta)
t_sin = time.perf_counter() - t0
print(f"SIN índice (50 corridas): {t_sin*1000:7.1f} ms  -> escaneo completo de la tabla")

# (b) Creamos un índice sobre la columna 'region' y repetimos
conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON parques_grande(region)")
t0 = time.perf_counter()
for _ in range(50):
    consultar(consulta)
t_con = time.perf_counter() - t0
print(f"CON índice (50 corridas): {t_con*1000:7.1f} ms  -> salto directo, como un índice de libro")

if t_con < t_sin:
    print(f"\\nEl índice hizo la consulta ~{t_sin/t_con:.1f}x más rápida. A más filas, más brutal la diferencia.")
else:
    print("\\n(Con tan pocas filas a veces no se nota; con millones, el índice es decisivo.)")"""

S5 = """## 5. Juntando todo: leer una consulta como la lee la base

Cuando te enfrentes a una consulta ajena (o depures la tuya), no la leas de arriba abajo: léela en el
**orden lógico** de ejecución y pregúntate en cada paso "¿sobre qué conjunto estoy operando?".

```
FROM parques_nul          → conjunto inicial: todas las filas
WHERE superficie_ha > 0   → subconjunto: filas con superficie positiva
                            (¡las de superficie NULL se caerían aquí!)
GROUP BY region           → ese subconjunto se parte en grupos por región
HAVING COUNT(*) >= 2      → se quedan solo los grupos con 2+ parques
SELECT region, COUNT(*)   → recién ahora se calculan las columnas del resultado
ORDER BY ...              → y al final se ordena
```

Tres reflejos de "pensamiento de base de datos" que te llevas:
1. **¿Estoy filtrando filas (`WHERE`) o grupos (`HAVING`)?** Son momentos distintos.
2. **¿Hay columnas que pueden tener `NULL`?** Si sí, cuidado con `!=`, `<`, `>`: revisa con `IS NULL`.
3. **Esta consulta, ¿sobre millones de filas, filtra por una columna sin índice?** Entonces será lenta.

Veámoslo en una sola consulta integradora."""

S5_CODE = """# Consulta integradora: por región, superficie total y promedio, solo regiones con 2+ parques,
# ignorando filas sin superficie, ordenado por superficie total.
r = consultar('''
    SELECT region,
           COUNT(*)               AS n_parques,
           SUM(superficie_ha)     AS total_ha,
           ROUND(AVG(superficie_ha)) AS promedio_ha
    FROM parques_nul
    WHERE superficie_ha IS NOT NULL   -- descarta explícitamente filas sin dato
    GROUP BY region
    HAVING COUNT(*) >= 2
    ORDER BY total_ha DESC
''')
print(r.to_string(index=False))
print("\\nNota: 'Parque Sin Datos' (region NULL) PASA el WHERE porque su superficie_ha = 5000 (no es NULL),")
print("pero su grupo de región NULL tiene solo 1 fila, así que es HAVING COUNT(*)>=2 quien lo deja fuera.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Esperar un orden sin `ORDER BY`.** Una tabla es un *conjunto*: sin pedir orden, la base entrega las filas como quiera.
- **Filtrar un `COUNT`/`SUM` con `WHERE`.** Para filtrar **grupos** se usa `HAVING`; `WHERE` filtra filas antes de agrupar.
- **Usar un alias de `SELECT` dentro de `WHERE`.** Cuando corre `WHERE`, el `SELECT` aún no ocurrió: el alias no existe (da error en PostgreSQL/BigQuery/SQL Server; SQLite lo tolera, pero no te acostumbres).
- **Comparar con `NULL` usando `=` o `!=`.** Siempre da `UNKNOWN`. Usa `IS NULL` / `IS NOT NULL`.
- **Olvidar que `WHERE col != 'X'` esconde los `NULL`.** Las filas con dato faltante se caen silenciosamente.
- **Filtrar/ordenar millones de filas por una columna sin índice.** Será un escaneo completo, lento. Indexa lo que consultas seguido."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: calculas algo **y** eliges la **interpretación correcta** (una letra).
Completa cada `TODO` y ejecuta la celda de chequeo. Las tablas `parques`, `parques_nul` y
`parques_grande` ya están creadas arriba; usa `consultar(...)`."""

# ---- E1 conjuntos / orden no garantizado
E1 = """## Ejercicio 01 · Sin ORDER BY no hay orden garantizado
Una tabla es un **conjunto**: sin `ORDER BY` el orden no está garantizado.

- En `n_grandes` guarda **cuántos** parques superan las 100.000 ha. Pista:
  `consultar("SELECT COUNT(*) AS n FROM parques WHERE superficie_ha > 100000").iloc[0]["n"]`.
- Luego elige en `conclusion` (letra) la afirmación correcta sobre `SELECT nombre FROM parques` (sin `ORDER BY`):
  - **A.** Siempre devuelve los parques en orden alfabético.
  - **B.** Siempre los devuelve en el orden del archivo CSV original.
  - **C.** El orden **no está garantizado**: si quieres uno, debes pedirlo con `ORDER BY`."""
E1_TODO = """n_grandes = None    # TODO: cuántos parques superan 100.000 ha
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """n_grandes = int(consultar("SELECT COUNT(*) AS n FROM parques WHERE superficie_ha > 100000").iloc[0]["n"])
conclusion = "C"
"""
E1_CHK = """try:
    _n = int(consultar("SELECT COUNT(*) AS n FROM parques WHERE superficie_ha > 100000").iloc[0]["n"])
    assert n_grandes is not None, "Aún no calculaste n_grandes."
    assert int(n_grandes) == _n, f"Esperaba {_n} parques sobre 100.000 ha, obtuve {n_grandes}"
    _correcta = "C"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿un conjunto tiene orden por sí solo?"
    print(f"✅ Correcto. {_n} parques superan 100.000 ha, y sin ORDER BY el orden no está garantizado.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)
except Exception as e:
    print("❌ Revisa tu consulta:", e)"""

# ---- E2 WHERE vs HAVING / orden de ejecución
E2 = """## Ejercicio 02 · WHERE filtra filas, HAVING filtra grupos
Queremos las **regiones con 3 o más parques**.

- Escribe en `sql_regiones` una consulta con `GROUP BY region` y `HAVING COUNT(*) >= 3`, que devuelva
  `region` y el conteo como `n`.
- Guarda en `n_regiones` cuántas regiones cumplen (= número de filas del resultado).
- Elige en `conclusion` por qué el filtro `COUNT(*) >= 3` va en `HAVING` y no en `WHERE`:
  - **A.** Da lo mismo, `WHERE` y `HAVING` son intercambiables.
  - **B.** Porque `WHERE` filtra filas **antes** de agrupar (cuando los grupos aún no existen);
    el conteo del grupo solo existe **después** de `GROUP BY`, y eso lo filtra `HAVING`.
  - **C.** Porque `HAVING` es más rápido que `WHERE`."""
E2_TODO = """sql_regiones = ""   # TODO: SELECT region, COUNT(*) AS n FROM parques GROUP BY region HAVING COUNT(*) >= 3
n_regiones = None   # TODO: cuántas filas devuelve esa consulta
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = '''sql_regiones = "SELECT region, COUNT(*) AS n FROM parques GROUP BY region HAVING COUNT(*) >= 3"
n_regiones = len(consultar(sql_regiones))
conclusion = "B"
'''
E2_CHK = """try:
    _r = consultar("SELECT region, COUNT(*) AS n FROM parques GROUP BY region HAVING COUNT(*) >= 3")
    _n = len(_r)
    assert sql_regiones.strip() != "", "Aún no escribiste sql_regiones."
    _tuya = consultar(sql_regiones)
    assert "region" in [c.lower() for c in _tuya.columns], "Tu consulta debe devolver la columna region."
    assert len(_tuya) == _n, f"Tu consulta devuelve {len(_tuya)} regiones; esperaba {_n} (las de 3+ parques)."
    assert n_regiones is not None and int(n_regiones) == _n, f"n_regiones debería ser {_n}"
    assert str(conclusion).strip().upper() == "B", "Pista: ¿en qué momento existe el COUNT de cada grupo?"
    print(f"✅ Correcto. {_n} regiones tienen 3+ parques. HAVING filtra grupos; WHERE filtraría filas antes de existir los grupos.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)
except Exception as e:
    print("❌ Revisa tu consulta:", e)"""

# ---- E3 NULL three-valued logic
E3 = """## Ejercicio 03 · La trampa del NULL
Usa la tabla `parques_nul` (24 parques + 1 "Parque Sin Datos" con `region = NULL`).

- En `n_distinto` guarda cuántas filas devuelve `WHERE region != 'Magallanes'`.
- En `n_total_no_mag` guarda cuántas filas **realmente** no son de Magallanes, contando también las de
  región desconocida: usa `WHERE region != 'Magallanes' OR region IS NULL`.
- Elige en `conclusion` la lectura correcta:
  - **A.** `n_distinto` y `n_total_no_mag` son iguales: `!=` ya incluye los `NULL`.
  - **B.** `n_total_no_mag` es **mayor**: el `!=` dejó fuera la fila con `region` NULL porque
    `NULL != 'Magallanes'` da `UNKNOWN`, no `TRUE`. Para incluir faltantes hay que pedir `IS NULL` aparte.
  - **C.** `n_distinto` es mayor porque `!=` cuenta los NULL dos veces."""
E3_TODO = """n_distinto = None       # TODO: filas de WHERE region != 'Magallanes'
n_total_no_mag = None   # TODO: filas de WHERE region != 'Magallanes' OR region IS NULL
conclusion = None       # TODO: "A", "B" o "C"
"""
E3_SOL = '''n_distinto = int(consultar("SELECT COUNT(*) AS n FROM parques_nul WHERE region != 'Magallanes'").iloc[0]["n"])
n_total_no_mag = int(consultar("SELECT COUNT(*) AS n FROM parques_nul WHERE region != 'Magallanes' OR region IS NULL").iloc[0]["n"])
conclusion = "B"
'''
E3_CHK = """try:
    _d = int(consultar("SELECT COUNT(*) AS n FROM parques_nul WHERE region != 'Magallanes'").iloc[0]["n"])
    _t = int(consultar("SELECT COUNT(*) AS n FROM parques_nul WHERE region != 'Magallanes' OR region IS NULL").iloc[0]["n"])
    assert n_distinto is not None and int(n_distinto) == _d, f"n_distinto debería ser {_d}"
    assert n_total_no_mag is not None and int(n_total_no_mag) == _t, f"n_total_no_mag debería ser {_t}"
    _correcta = "B" if _t > _d else "A"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿qué pasó con la fila de region NULL al usar !=?"
    print(f"✅ Correcto. != dio {_d}; contando los NULL aparte son {_t}. NULL != 'X' es UNKNOWN, no TRUE.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)
except Exception as e:
    print("❌ Revisa tu consulta:", e)"""

# ---- E4 índices (conceptual)
E4 = """## Ejercicio 04 · Por qué existen los índices (conceptual)
Mides la consulta `SELECT COUNT(*) ... WHERE region = 'Magallanes'` sobre `parques_grande` (~120.000
filas), **sin** y **con** el índice `idx_region` que creaste en la sección 4.

- En `gano_velocidad` guarda `True` si la versión **con** índice fue al menos tan rápida como la versión
  **sin** índice (en una tabla grande casi siempre lo es), o `False` si no. Pista: ya mediste `t_sin` y
  `t_con` en la sección 4; puedes usar `gano_velocidad = t_con <= t_sin`.
- Elige en `conclusion` la afirmación correcta sobre los índices:
  - **A.** Un índice acelera **toda** operación y no tiene ningún costo; deberías indexar todas las columnas.
  - **B.** Un índice es como el índice de un libro: permite **saltar directo** a las filas buscadas en vez
    de escanear toda la tabla. A cambio, **ocupa espacio** y **hace más lentas las escrituras**, por eso se
    indexan las columnas por las que se filtra/ordena seguido, no todas.
  - **C.** Los índices solo sirven para ordenar resultados, nunca para filtrar.

*(Opcional, no se corrige): en `reflexion` escribe qué columna del Estado indexarías primero y por qué.)*"""
E4_TODO = """gano_velocidad = None   # TODO: True/False — ¿con índice fue al menos tan rápido? (usa t_con <= t_sin)
conclusion = None       # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """gano_velocidad = t_con <= t_sin
conclusion = "B"
reflexion = "Indexaría el RUT en las tablas de personas: se filtra/cruza por RUT constantemente."
"""
E4_CHK = """try:
    assert gano_velocidad is not None, "Aún no definiste gano_velocidad (True/False)."
    assert isinstance(gano_velocidad, bool) or gano_velocidad in (0, 1), "gano_velocidad debe ser True o False."
    assert bool(gano_velocidad) == bool(t_con <= t_sin), "Compara t_con con t_sin: ¿con índice fue al menos tan rápido?"
    assert str(conclusion).strip().upper() == "B", "Pista: ¿un índice es gratis? ¿qué le cuesta a las escrituras?"
    print("✅ Correcto. El índice deja saltar directo a las filas, a costa de espacio y escrituras más lentas.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable (¿corriste la sección 4 que define t_sin y t_con?):", e)
except Exception as e:
    print("❌ Revisa tu cálculo:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo escribes SQL: entiendes **cómo piensa la base**. Pasaste del recorrido fila-a-fila al
razonamiento por **conjuntos**; sabes que la consulta se ejecuta en un **orden lógico** distinto al que
la escribes (y por eso `WHERE` filtra filas y `HAVING` filtra grupos); reconoces la **trampa del NULL**
y la lógica de tres valores; y entiendes por qué los **índices** hacen la diferencia entre una consulta
instantánea y una eterna.

La regla de oro que te llevas: **antes de confiar en un resultado, pregunta por el orden, por los NULL
y por la escala.** Eso distingue a quien *escribe* SQL de quien *entiende* la base de datos."""


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
        md(E1, "p14"), code(g(E1_SOL, E1_TODO), "p15"), code(E1_CHK, "p16"),
        md(E2, "p17"), code(g(E2_SOL, E2_TODO), "p18"), code(E2_CHK, "p19"),
        md(E3, "p20"), code(g(E3_SOL, E3_TODO), "p21"), code(E3_CHK, "p22"),
        md(E4, "p23"), code(g(E4_SOL, E4_TODO), "p24"), code(E4_CHK, "p25"),
        md(CIERRE, "p26"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "profundiza.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "profundiza_solucion.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Generados: profundiza.ipynb y profundiza_solucion.ipynb en", BASE)
