"""build_R2-02.py — módulo R2-02 (SQL para features).

Rama R2 (Científico de Datos). Usar SQL no para *mirar* datos sino para FABRICAR
variables (features) y armar una tabla analítica (ABT). Rearmado 2026: reemplaza el
snapshot de juguete de 15 sismos por datos reales.
- Lección (ancla de la rama): PM2.5 diario SINCA (aire_diario.csv) cargado en SQLite:
  GROUP BY estación × mes, CASE WHEN con los niveles de episodio del D.S. 12/2011 MMA,
  funciones de ventana LAG y AVG OVER (media móvil de 7 días SIN el día actual: anti
  fuga de información) y la ABT por estación.
- Profundiza (transferencia): sismos.csv real (USGS, M≥4,5, Chile 2020–2025):
  features por zona/año, CASE WHEN de profundidad, días desde el sismo anterior (LAG
  con julianday) y ABT por zona con una CTE (WITH).
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-02.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-02-sql-para-features")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request, sqlite3
import pandas as pd, numpy as np

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "aire_diario.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/aire_diario.csv", CSV)

df = pd.read_csv(CSV)

# Cargamos la tabla en una base SQLite en memoria: desde aquí, todo es SQL.
con = sqlite3.connect(":memory:")
df.to_sql("aire", con, index=False)

# Atajo para no repetir: corre una consulta y la devuelve como tabla de pandas.
def correr(sql):
    return pd.read_sql_query(sql, con)

print("Tabla 'aire' creada en SQLite:", len(df), "filas (un día por estación).")
correr("SELECT * FROM aire LIMIT 5")'''

INTRO = '''## 1. La idea central: de *mediciones* a *features*

### ¿Qué es una *feature*?
Una *feature* es **una columna que describe algo y que un modelo puede usar para aprender**.
Si más adelante quisieras un modelo que anticipe *«¿mañana esta estación superará la norma?»*,
el modelo no puede «mirar» el cielo: solo ve **números en columnas**. Tu trabajo es traducir el
fenómeno a columnas útiles: el PM2.5 *promedio* del mes, el de *ayer*, la *media de la última
semana*, *cuántos días* superó la norma… Cada una de esas columnas es una *feature*.

> 🧠 **Analogía.** Describes a una persona para que alguien que no la ve pueda reconocerla:
> estatura, edad, color de pelo. Esas descripciones son *features*. El modelo es ese «alguien
> que no ve»: solo conoce el mundo a través de las *features* que tú le pasas. Buenas
> *features* → buen modelo. Por eso se dice que **fabricar *features* es el 80 % del trabajo**.

### Tres palabras que usaremos todo el módulo
- **Observación en bruto:** una fila de los datos crudos. Aquí, **un día en una estación**.
- **Entidad:** la *cosa* sobre la que queremos decidir y que tendrá **una fila** en la tabla
  final. Aquí, la **estación de monitoreo**.
- **Tabla analítica** (*Analytical Base Table*, **ABT**): **una fila por entidad** y **una
  columna por *feature***. Es lo que se le entrega a un modelo. Construirla es la meta de hoy.

### El viaje de hoy
```
tabla 'aire'               agregar / clasificar / mirar atrás        TABLA ANALITICA
(1 fila = 1 día-estación) ───────────────  con SQL  ──────────▶   (1 fila = 1 estación,
                                                                  varias features)
```

> 🏛️ **Los umbrales que usaremos** (D.S. 12/2011 del Ministerio del Medio Ambiente, norma de
> PM2.5): **50 µg/m³** es el valor de la norma de 24 horas (su cumplimiento formal se evalúa con
> el percentil 98 anual; aquí contamos días sobre ese valor). Para gestionar **episodios
> críticos** el decreto define niveles de concentración de 24 h: **Alerta 80–109**,
> **Preemergencia 110–169** y **Emergencia ≥ 170 µg/m³**.'''

SEC = [
'''## 2. *Features* de agregación con `GROUP BY`

La forma más común de fabricar *features* es **resumir muchas filas en una sola por grupo**.
`GROUP BY` junta las filas que comparten un valor y aplica una **función de agregación**:

| Función | Qué calcula | *Feature* de ejemplo |
| --- | --- | --- |
| `COUNT(*)` | cuántas filas hay en el grupo | días en el registro |
| `COUNT(col)` | cuántas filas **con dato** (ignora `NULL`) | días con PM2.5 medido |
| `AVG(col)` | promedio (ignora `NULL`) | PM2.5 promedio |
| `MAX(col)` / `MIN(col)` | mayor / menor | peor día del grupo |

Se puede agrupar por **varias columnas** a la vez, y agrupar por algo **calculado**: SQLite
extrae el mes de una fecha con `strftime('%m', fecha)` (devuelve texto `'01'`…`'12'`; con
`CAST(... AS INTEGER)` lo dejas como número).

```sql
SELECT estacion,
       CAST(strftime('%m', fecha) AS INTEGER) AS mes,
       AVG(pm25) AS pm25_promedio
FROM aire
GROUP BY estacion, mes
```

> ⚠️ **Errores típicos**
> - **Pedir una columna que no está en el `GROUP BY` ni dentro de una agregación** (p. ej.
>   `fecha` suelta): cada grupo tiene muchas fechas y SQL no sabría cuál mostrar.
> - **`COUNT(*)` vs `COUNT(pm25)`:** el primero cuenta filas; el segundo, solo las que tienen
>   dato. Con faltantes reales, la diferencia importa.
> - **Olvidar el alias `AS`:** las celdas de chequeo buscan las columnas por su nombre.''',

'''## 3. *Features* condicionales con `CASE WHEN`

A veces la *feature* útil no es un promedio sino una **etiqueta**: ¿ese día fue de alerta,
preemergencia o emergencia? `CASE WHEN` es el «si… entonces…» de SQL:

```sql
CASE
    WHEN pm25 IS NULL THEN 'sin dato'
    WHEN pm25 >= 170  THEN 'emergencia'
    WHEN pm25 >= 110  THEN 'preemergencia'
    ...
    ELSE 'bajo norma'
END AS nivel
```

SQL evalúa las condiciones **de arriba hacia abajo** y se queda con la **primera** que se cumple.
Por eso el orden importa: si pusieras primero `pm25 > 50`, un día de emergencia (284 µg/m³)
quedaría etiquetado como simple «sobre norma».

> ⚠️ **Errores típicos**
> - **Olvidar el caso `NULL`.** Un `NULL` no cumple ninguna comparación y cae en el `ELSE`:
>   un día **sin medición** quedaría como «bajo norma». Trátalo primero, explícitamente.
> - **Orden de las condiciones al revés** (de menor a mayor umbral con `>=`).
> - **Olvidar `END` o el `AS`.**''',

'''## 4. *Features* temporales con funciones de ventana (`LAG`, `AVG OVER`)

Muchas veces la *feature* más poderosa es **«¿qué pasó antes?»**: el PM2.5 de **ayer**, el
promedio de **la última semana**. Para mirar filas vecinas sin colapsar la tabla se usan las
**funciones de ventana** (`... OVER (...)`):

```sql
LAG(pm25) OVER (PARTITION BY estacion ORDER BY fecha) AS pm25_ayer,
AVG(pm25) OVER (PARTITION BY estacion ORDER BY fecha
                ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS pm25_media_7d
```

Léelo así:
- `PARTITION BY estacion` — cada estación es su propia fila del banco: Temuco no mira a Antofagasta.
- `ORDER BY fecha` — dentro de cada estación, en orden cronológico.
- `LAG(pm25)` — trae el valor de la fila **anterior** (ayer). La primera fila de cada estación
  no tiene pasado: queda `NULL`.
- `ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING` — la ventana son las **7 filas anteriores, sin la
  actual**. Como el registro tiene un día por fila, eso es «la semana previa».

### 🚨 *Data leakage* (fuga de información)
Si quieres predecir el PM2.5 de **hoy**, solo puedes usar lo que se sabía **antes de hoy**. Una
media móvil que incluye el día actual (`ROWS 6 PRECEDING AND CURRENT ROW`) le «sopla» al modelo
parte de la respuesta: en pruebas parece magia, en la realidad fracasa. Por eso la ventana
termina en `1 PRECEDING`. **Regla de oro: una *feature* nunca contiene información del momento
que intentas predecir ni posterior a él** (tampoco uses `LEAD`, que mira al futuro).

> ⚠️ **Errores típicos**
> - **Olvidar `PARTITION BY`:** el «ayer» del primer día de Temuco sería el último día de otra estación.
> - **Olvidar `ORDER BY` dentro del `OVER`:** «anterior» no significa nada sin un orden.
> - **Asustarse por los `NULL` del inicio:** son correctos; el primer día no tiene pasado.''',

'''## 5. Juntar todo: la **tabla analítica**

El paso final es **reunir varias *features* en una sola tabla con una fila por entidad**. Un truco
muy usado combina `GROUP BY` con `CASE WHEN`: contar cuántas filas cumplen una condición dentro de
cada grupo con **`SUM(CASE WHEN … THEN 1 ELSE 0 END)`** — cada día que cumple aporta un `1`.

```sql
SUM(CASE WHEN pm25 > 50 THEN 1 ELSE 0 END) AS dias_sobre_norma
```

Y si dejas el `CASE` **sin `ELSE`** dentro de un `AVG`, los días que no cumplen quedan `NULL` y el
promedio los ignora: así sacas el **PM2.5 promedio de invierno** (mayo a agosto) en una línea.

> 🧠 **Analogía.** Es levantar la mano: por cada día sobre la norma alguien levanta la mano;
> al final cuentas las manos de cada estación.''',
]

EJ = [
 ("Features por estación y mes",
  '''Crea una consulta con **una fila por estación y mes** (los 12 meses del año, juntando 2020–2025)
y estas columnas (usa exactamente estos nombres con `AS`):

`estacion`, `mes` (entero 1–12), `n_dias` (días **con** PM2.5 medido), `pm25_promedio`
(redondeado a 1 decimal) y `pm25_maximo`. Ordena por `estacion` y `mes`. Completa `consulta_1`.''',
  '''consulta_1 = """
SELECT estacion,
       CAST(strftime('%m', fecha) AS INTEGER) AS mes,
       COUNT(pm25)            AS n_dias,
       ROUND(AVG(pm25), 1)    AS pm25_promedio,
       MAX(pm25)              AS pm25_maximo
FROM aire
GROUP BY estacion, mes
ORDER BY estacion, mes
"""
correr(consulta_1)''',
  '''consulta_1 = """
SELECT estacion,
       -- TODO: el mes como entero: CAST(strftime('%m', fecha) AS INTEGER) AS mes
       -- TODO: COUNT(pm25) AS n_dias, ROUND(AVG(pm25), 1) AS pm25_promedio, MAX(pm25) AS pm25_maximo
FROM aire
-- TODO: GROUP BY ... y ORDER BY ...
"""
correr(consulta_1)''',
  '''r = correr(consulta_1)
assert {"estacion", "mes", "n_dias", "pm25_promedio", "pm25_maximo"}.issubset(r.columns), "faltan columnas o tienen otro nombre"
assert len(r) == df["estacion"].nunique() * 12, f"deben ser 14 estaciones x 12 meses = 168 filas, no {len(r)}"
assert int(r["n_dias"].sum()) == int(df["pm25"].notna().sum()), "n_dias debe contar solo días CON dato: COUNT(pm25)"
assert r["pm25_maximo"].max() == df["pm25"].max()
assert set(r["mes"]) == set(range(1, 13)), "mes debe ser un entero de 1 a 12 (usa CAST)"''',
  "GROUP BY estacion, mes con CAST(strftime('%m', fecha) AS INTEGER) AS mes; COUNT(pm25) cuenta solo los días con dato."),

 ("Etiquetar cada día con su nivel de episodio",
  '''Devuelve `fecha`, `estacion`, `pm25` y una columna nueva `nivel` con estos valores, **en este
orden de evaluación**:

| condición | `nivel` |
| --- | --- |
| `pm25` es `NULL` | `'sin dato'` |
| `pm25 >= 170` | `'emergencia'` |
| `pm25 >= 110` | `'preemergencia'` |
| `pm25 >= 80` | `'alerta'` |
| `pm25 > 50` | `'sobre norma'` |
| en otro caso | `'bajo norma'` |

Completa `consulta_2`.''',
  '''consulta_2 = """
SELECT fecha, estacion, pm25,
       CASE
           WHEN pm25 IS NULL THEN 'sin dato'
           WHEN pm25 >= 170  THEN 'emergencia'
           WHEN pm25 >= 110  THEN 'preemergencia'
           WHEN pm25 >= 80   THEN 'alerta'
           WHEN pm25 > 50    THEN 'sobre norma'
           ELSE 'bajo norma'
       END AS nivel
FROM aire
"""
niveles = correr(consulta_2)
niveles["nivel"].value_counts()''',
  '''consulta_2 = """
SELECT fecha, estacion, pm25,
       CASE
           WHEN pm25 IS NULL THEN 'sin dato'
           -- TODO: emergencia (>= 170), preemergencia (>= 110), alerta (>= 80), sobre norma (> 50)
           ELSE 'bajo norma'
       END AS nivel
FROM aire
"""
niveles = correr(consulta_2)
niveles["nivel"].value_counts()''',
  '''r = correr(consulta_2)
assert "nivel" in r.columns, "falta la columna nivel (cierra el CASE con END AS nivel)"
assert len(r) == len(df), "debe haber una fila por día-estación"
c = r["nivel"].value_counts()
p = df["pm25"]
assert c.get("sin dato", 0) == int(p.isna().sum()), "los NULL deben quedar como 'sin dato'"
assert c.get("emergencia", 0) == int((p >= 170).sum()), "revisa el umbral de emergencia (>= 170)"
assert c.get("preemergencia", 0) == int(((p >= 110) & (p < 170)).sum()), "revisa preemergencia (110–169) y el ORDEN de las condiciones"
assert c.get("alerta", 0) == int(((p >= 80) & (p < 110)).sum()), "revisa alerta (80–109)"
assert c.get("sobre norma", 0) == int(((p > 50) & (p < 80)).sum()), "revisa 'sobre norma' (> 50 y < 80)"''',
  "Ordena de mayor a menor umbral: WHEN pm25 >= 170 THEN 'emergencia' WHEN pm25 >= 110 THEN 'preemergencia' WHEN pm25 >= 80 THEN 'alerta' WHEN pm25 > 50 THEN 'sobre norma'."),

 ("El PM2.5 de ayer y la media de la semana previa",
  '''Agrega a cada día dos *features* temporales **por estación**:

- `pm25_ayer`: el PM2.5 del día anterior (`LAG`).
- `pm25_media_7d`: el promedio de los **7 días anteriores, sin el día actual** (`AVG ... OVER` con
  `ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING`), redondeado a 1 decimal.

Devuelve `fecha`, `estacion`, `pm25`, `pm25_ayer`, `pm25_media_7d`, ordenado por `estacion` y
`fecha`. Completa `consulta_3`.''',
  '''consulta_3 = """
SELECT fecha, estacion, pm25,
       LAG(pm25) OVER (PARTITION BY estacion ORDER BY fecha) AS pm25_ayer,
       ROUND(AVG(pm25) OVER (PARTITION BY estacion ORDER BY fecha
                             ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING), 1) AS pm25_media_7d
FROM aire
ORDER BY estacion, fecha
"""
temporales = correr(consulta_3)
temporales[temporales["estacion"] == "Las Encinas Temuco"].iloc[180:190]''',
  '''consulta_3 = """
SELECT fecha, estacion, pm25,
       -- TODO: LAG(pm25) OVER (PARTITION BY ... ORDER BY ...) AS pm25_ayer,
       -- TODO: ROUND(AVG(pm25) OVER (PARTITION BY ... ORDER BY ...
       --                 ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING), 1) AS pm25_media_7d
FROM aire
ORDER BY estacion, fecha
"""
temporales = correr(consulta_3)
temporales.head(10)''',
  '''r = correr(consulta_3)
assert {"pm25_ayer", "pm25_media_7d"}.issubset(r.columns), "faltan pm25_ayer y/o pm25_media_7d"
assert len(r) == len(df)
r = r.sort_values(["estacion", "fecha"]).reset_index(drop=True)
ref = df.sort_values(["estacion", "fecha"]).reset_index(drop=True)
ayer = ref.groupby("estacion")["pm25"].shift(1)
assert np.allclose(r["pm25_ayer"], ayer, equal_nan=True), "pm25_ayer no calza: ¿usaste PARTITION BY estacion ORDER BY fecha?"
media = ayer.groupby(ref["estacion"]).transform(lambda s: s.rolling(7, min_periods=1).mean())
assert np.allclose(r["pm25_media_7d"], media, atol=0.051, equal_nan=True), "pm25_media_7d no calza: la ventana es 7 PRECEDING a 1 PRECEDING (sin el día actual)"''',
  "LAG(pm25) OVER (PARTITION BY estacion ORDER BY fecha) y AVG(pm25) OVER (PARTITION BY estacion ORDER BY fecha ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING)."),

 ("Tu primera tabla analítica: una fila por estación",
  '''Construye una tabla con **una fila por estación** y estas columnas:

`estacion`, `n_dias` (días con PM2.5), `pm25_promedio` (1 decimal), `dias_sobre_norma`
(PM2.5 > 50), `dias_alerta_o_peor` (PM2.5 ≥ 80) y `pm25_invierno` (promedio de mayo a agosto,
1 decimal). Ordena por `dias_sobre_norma` de mayor a menor. Completa `consulta_4`.

Cuando salga ✅, mira la tabla: **eso** es lo que en R2-04 le entregarás a un modelo.''',
  '''consulta_4 = """
SELECT estacion,
       COUNT(pm25)                                         AS n_dias,
       ROUND(AVG(pm25), 1)                                 AS pm25_promedio,
       SUM(CASE WHEN pm25 > 50  THEN 1 ELSE 0 END)         AS dias_sobre_norma,
       SUM(CASE WHEN pm25 >= 80 THEN 1 ELSE 0 END)         AS dias_alerta_o_peor,
       ROUND(AVG(CASE WHEN CAST(strftime('%m', fecha) AS INTEGER) BETWEEN 5 AND 8
                      THEN pm25 END), 1)                   AS pm25_invierno
FROM aire
GROUP BY estacion
ORDER BY dias_sobre_norma DESC
"""
abt = correr(consulta_4)
abt''',
  '''consulta_4 = """
SELECT estacion,
       COUNT(pm25)          AS n_dias,
       ROUND(AVG(pm25), 1)  AS pm25_promedio,
       -- TODO: dias_sobre_norma   = SUM(CASE WHEN pm25 > 50 THEN 1 ELSE 0 END)
       -- TODO: dias_alerta_o_peor = SUM(CASE WHEN pm25 >= 80 ...)
       -- TODO: pm25_invierno = ROUND(AVG(CASE WHEN mes entre 5 y 8 THEN pm25 END), 1)
FROM aire
GROUP BY estacion
ORDER BY dias_sobre_norma DESC
"""
abt = correr(consulta_4)
abt''',
  '''r = correr(consulta_4)
esperadas = {"estacion", "n_dias", "pm25_promedio", "dias_sobre_norma", "dias_alerta_o_peor", "pm25_invierno"}
assert esperadas.issubset(r.columns), f"faltan columnas: {sorted(esperadas - set(r.columns))}"
assert len(r) == 14, "una fila por estación: deben ser 14"
assert int(r["dias_sobre_norma"].sum()) == int((df["pm25"] > 50).sum())
assert int(r["dias_alerta_o_peor"].sum()) == int((df["pm25"] >= 80).sum())
inv = df[pd.to_datetime(df["fecha"]).dt.month.between(5, 8)].groupby("estacion")["pm25"].mean()
assert np.allclose(r.set_index("estacion")["pm25_invierno"].sort_index(), inv.sort_index(), atol=0.051), "pm25_invierno: promedio solo de meses 5 a 8"
assert r["dias_sobre_norma"].is_monotonic_decreasing, "ordena por dias_sobre_norma DESC"''',
  "SUM(CASE WHEN pm25 > 50 THEN 1 ELSE 0 END) cuenta días; AVG(CASE WHEN CAST(strftime('%m', fecha) AS INTEGER) BETWEEN 5 AND 8 THEN pm25 END) promedia solo invierno."),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige)

Mira tu tabla analítica. Las estaciones con más días sobre la norma tienen un `pm25_invierno`
mucho mayor que su `pm25_promedio`. Si tuvieras que decidir **dónde reforzar la fiscalización de
calefacción a leña en invierno**, ¿qué columna mirarías primero y por qué? ¿Qué *feature* nueva
le agregarías a esta tabla?'''

CIERRE = '''## 6. Cierre

Hoy dejaste de *consultar* datos para empezar a *fabricar variables*:

1. **Agregar** con `GROUP BY` (también por columnas calculadas como el mes) — `COUNT(col)` ignora faltantes.
2. **Etiquetar** con `CASE WHEN` (los niveles de episodio del D.S. 12/2011), tratando el `NULL` primero.
3. **Mirar al pasado** con funciones de ventana: `LAG` y una media móvil que **excluye** el día actual.
4. **Reunir** todo en una **tabla analítica**: una fila por entidad, lista para un modelo.

### Mini-glosario
- ***Feature*:** columna que describe una entidad y que un modelo puede usar.
- **Entidad:** la unidad de análisis; una fila en la tabla final (aquí, la estación).
- **Tabla analítica (ABT):** una fila por entidad, una columna por *feature*.
- ***Lag* (rezago):** valor de una observación anterior usado como *feature*.
- **Media móvil:** promedio de una ventana de filas vecinas que se desplaza en el tiempo.
- ***Data leakage*:** usar información del futuro (o del propio resultado) como *feature*.

> *En R2-03 vas a medir con estadística lo que hoy resumiste; en R2-04, esta tabla será la
> entrada de tu primer modelo.*

---
*Fuente de datos: SINCA — Sistema de Información Nacional de Calidad del Aire, Ministerio del
Medio Ambiente ([sinca.mma.gob.cl](https://sinca.mma.gob.cl)). Contenido bajo licencia CC BY 4.0 · Formación Pública.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-02", "SQL para *features*", "R2", "Científico de Datos", "4",
                      ["Fabricar *features* de **agregación** con `GROUP BY` (por estación y mes).",
                       "Crear **etiquetas** con `CASE WHEN` (niveles de episodio de PM2.5).",
                       "Crear *features* **temporales** con funciones de ventana (`LAG`, media móvil) sin fuga de información.",
                       "Reunir todo en una **tabla analítica** (una fila por estación)."],
                      "a partir de mediciones en bruto, construir con SQL una tabla analítica lista para un modelo, cuidando la fuga de información.",
                      "PM2.5 diario de 14 estaciones del SINCA (Ministerio del Medio Ambiente), 2020–2025, cargado en SQLite.",
                      n_checks=4),
        h.code(SETUP),
        h.md(INTRO),
    ]
    for i, ((ej_t, ej_b, sol, todo, chk, hint), sec) in enumerate(zip(EJ, SEC), 1):
        cells.append(h.md(sec))
        cells.append(h.exercise_md(i, ej_t, ej_b))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización: sismos reales (transferencia) ─────────────────────────────
PROF_PREP = f'''import os, urllib.request, sqlite3
import pandas as pd, numpy as np

CSV = "sismos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/sismos.csv", CSV)
sis = pd.read_csv(CSV)    # sismos M>=4,5 en Chile 2020–2025 (catálogo USGS)

con = sqlite3.connect(":memory:")
sis.to_sql("sismos", con, index=False)

def correr(sql):
    return pd.read_sql_query(sql, con)

print("Tabla 'sismos':", len(sis), "eventos;", "zonas:", sorted(sis["zona"].unique()))
correr("SELECT * FROM sismos LIMIT 5")'''

PROF_EJ = [
 ("## 1. *Features* por zona y año",
  "Mismo `GROUP BY` de la lección, otra entidad: la **zona** del país y el **año**. "
  "`strftime('%Y', fecha)` extrae el año.",
  "Resumen sísmico por zona y año",
  '''Una fila por `zona` y `anio` (entero) con `n_sismos`, `magnitud_promedio` (2 decimales) y
`magnitud_maxima`. Ordena por `zona` y `anio`.''',
  '''consulta_1 = """
SELECT zona,
       CAST(strftime('%Y', fecha) AS INTEGER) AS anio,
       COUNT(*)                 AS n_sismos,
       ROUND(AVG(magnitud), 2)  AS magnitud_promedio,
       MAX(magnitud)            AS magnitud_maxima
FROM sismos
GROUP BY zona, anio
ORDER BY zona, anio
"""
correr(consulta_1)''',
  '''consulta_1 = """
SELECT zona,
       -- TODO: CAST(strftime('%Y', fecha) AS INTEGER) AS anio,
       -- TODO: COUNT(*) AS n_sismos, ROUND(AVG(magnitud), 2) AS magnitud_promedio, MAX(magnitud) AS magnitud_maxima
FROM sismos
-- TODO: GROUP BY ... ORDER BY ...
"""
correr(consulta_1)''',
  '''r = correr(consulta_1)
assert {"zona", "anio", "n_sismos", "magnitud_promedio", "magnitud_maxima"}.issubset(r.columns)
assert len(r) == sis.groupby([sis["zona"], sis["fecha"].str[:4]]).ngroups
assert int(r["n_sismos"].sum()) == len(sis)
assert r["magnitud_maxima"].max() == sis["magnitud"].max()''',
  "GROUP BY zona, anio con CAST(strftime('%Y', fecha) AS INTEGER) AS anio."),

 ("## 2. Etiquetas con `CASE WHEN`: profundidad y sismo fuerte",
  "Dos *features* condicionales por evento: el tipo de profundidad (superficial < 70 km, "
  "intermedio 70–300 km, profundo > 300 km) y una **bandera 0/1** `es_fuerte` para M ≥ 6.",
  "Clasifica cada sismo",
  '''Devuelve `fecha`, `zona`, `profundidad_km`, `magnitud`, `profundidad_tipo` y `es_fuerte`.''',
  '''consulta_2 = """
SELECT fecha, zona, profundidad_km, magnitud,
       CASE
           WHEN profundidad_km < 70   THEN 'superficial'
           WHEN profundidad_km <= 300 THEN 'intermedio'
           ELSE 'profundo'
       END AS profundidad_tipo,
       CASE WHEN magnitud >= 6 THEN 1 ELSE 0 END AS es_fuerte
FROM sismos
"""
r2 = correr(consulta_2)
print(r2["profundidad_tipo"].value_counts(), "\\nfuertes:", r2["es_fuerte"].sum())''',
  '''consulta_2 = """
SELECT fecha, zona, profundidad_km, magnitud,
       -- TODO: CASE WHEN profundidad_km < 70 THEN 'superficial' WHEN ... <= 300 THEN 'intermedio' ELSE 'profundo' END AS profundidad_tipo,
       -- TODO: CASE WHEN magnitud >= 6 THEN 1 ELSE 0 END AS es_fuerte
FROM sismos
"""
r2 = correr(consulta_2)
r2.head()''',
  '''r = correr(consulta_2)
assert {"profundidad_tipo", "es_fuerte"}.issubset(r.columns)
c = r["profundidad_tipo"].value_counts()
assert c.get("superficial", 0) == int((sis["profundidad_km"] < 70).sum())
assert c.get("intermedio", 0) == int(((sis["profundidad_km"] >= 70) & (sis["profundidad_km"] <= 300)).sum())
assert int(r["es_fuerte"].sum()) == int((sis["magnitud"] >= 6).sum())''',
  "Dos CASE: el de profundidad (de menor a mayor umbral con <) y CASE WHEN magnitud >= 6 THEN 1 ELSE 0 END AS es_fuerte."),

 ("## 3. Rezago temporal: días desde el sismo anterior en la zona",
  "`LAG(fecha)` trae la fecha del sismo anterior **de la misma zona**; `julianday()` convierte "
  "fechas en números de días, así que la resta da los días transcurridos. Es una *feature* "
  "**punto-en-el-tiempo** correcta: en el momento de cada sismo, el anterior ya ocurrió.\n\n"
  "> 🚨 Lo contrario sería *leakage*: «días **hasta el próximo** sismo» (`LEAD`) no se conoce "
  "cuando ocurre el evento y jamás debe entrar a un modelo predictivo.",
  "Calcula `dias_desde_anterior`",
  '''Devuelve `fecha`, `zona`, `magnitud` y `dias_desde_anterior`, ordenado por `zona` y `fecha`.''',
  '''consulta_3 = """
SELECT fecha, zona, magnitud,
       julianday(fecha) - julianday(LAG(fecha) OVER (PARTITION BY zona ORDER BY fecha))
           AS dias_desde_anterior
FROM sismos
ORDER BY zona, fecha
"""
r3 = correr(consulta_3)
r3.groupby("zona")["dias_desde_anterior"].describe().round(1)''',
  '''consulta_3 = """
SELECT fecha, zona, magnitud,
       -- TODO: julianday(fecha) - julianday(LAG(fecha) OVER (PARTITION BY zona ORDER BY fecha)) AS dias_desde_anterior
FROM sismos
ORDER BY zona, fecha
"""
r3 = correr(consulta_3)
r3.head()''',
  '''r = correr(consulta_3)
assert "dias_desde_anterior" in r.columns
assert len(r) == len(sis)
assert int(r["dias_desde_anterior"].isna().sum()) == sis["zona"].nunique(), "solo el primer sismo de cada zona debe quedar NULL"
assert r["dias_desde_anterior"].min() >= 0, "¿ordenaste por fecha dentro del OVER?"
esperado = sis.assign(f=pd.to_datetime(sis["fecha"])).sort_values(["zona", "f"]).groupby("zona")["f"].diff().dt.days
assert abs(r["dias_desde_anterior"].sum() - esperado.sum()) < 1e-6''',
  "julianday(fecha) - julianday(LAG(fecha) OVER (PARTITION BY zona ORDER BY fecha))."),

 ("## 4. La tabla analítica por zona (con una CTE)",
  "Para agregar una *feature* de ventana hay que calcularla **primero** y agrupar **después**. "
  "Una **CTE** (`WITH t AS (...)`) es una tabla temporal con nombre: calculas la ventana en `t` "
  "y agrupas sobre `t`.",
  "Una fila por zona",
  '''Una fila por `zona` con `n_sismos`, `magnitud_promedio` (2 decimales), `n_fuertes` (M ≥ 6) y
`dias_entre_sismos` (promedio de `dias_desde_anterior`, 1 decimal). Ordena por `n_sismos` desc.''',
  '''consulta_4 = """
WITH t AS (
    SELECT zona, magnitud,
           julianday(fecha) - julianday(LAG(fecha) OVER (PARTITION BY zona ORDER BY fecha))
               AS dias_desde_anterior
    FROM sismos
)
SELECT zona,
       COUNT(*)                                         AS n_sismos,
       ROUND(AVG(magnitud), 2)                          AS magnitud_promedio,
       SUM(CASE WHEN magnitud >= 6 THEN 1 ELSE 0 END)   AS n_fuertes,
       ROUND(AVG(dias_desde_anterior), 1)               AS dias_entre_sismos
FROM t
GROUP BY zona
ORDER BY n_sismos DESC
"""
correr(consulta_4)''',
  '''consulta_4 = """
WITH t AS (
    SELECT zona, magnitud,
           -- TODO: la misma columna dias_desde_anterior del ejercicio 3
    FROM sismos
)
SELECT zona,
       -- TODO: n_sismos, magnitud_promedio, n_fuertes, dias_entre_sismos
FROM t
GROUP BY zona
ORDER BY n_sismos DESC
"""
correr(consulta_4)''',
  '''r = correr(consulta_4)
assert {"zona", "n_sismos", "magnitud_promedio", "n_fuertes", "dias_entre_sismos"}.issubset(r.columns)
assert len(r) == sis["zona"].nunique()
assert int(r["n_sismos"].sum()) == len(sis)
assert int(r["n_fuertes"].sum()) == int((sis["magnitud"] >= 6).sum())
assert r.set_index("zona")["dias_entre_sismos"].idxmax() == "austral", "la zona con menos sismos debería tener los intervalos más largos"''',
  "WITH t AS (SELECT zona, magnitud, <la resta de julianday con LAG> AS dias_desde_anterior FROM sismos) SELECT zona, COUNT(*), ..., AVG(dias_desde_anterior) FROM t GROUP BY zona."),
]

PROF_HEADER = '''# R2-02 · SQL para *features* — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: el mismo oficio de fabricar *features* con SQL sobre otro dato
público — los **1.601 sismos de magnitud ≥ 4,5** registrados en Chile entre 2020 y 2025 (catálogo
del Servicio Geológico de EE.UU., USGS). Cambia la entidad (la **zona** del país), aparecen las
banderas 0/1, el rezago entre **fechas** con `julianday`, y una herramienta nueva: la **CTE**
(`WITH`) para agregar una *feature* de ventana.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, ej_b, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t, ej_b))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-02.* "
                      "Fuente: USGS Earthquake Catalog ([earthquake.usgs.gov](https://earthquake.usgs.gov))."))
    nb.cells = cells
    return nb


README = '''# R2-02 · SQL para *features*

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-02-sql-para-features/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Usar SQL no para *mirar* datos sino para **fabricar variables** (*features*) y armar una **tabla
analítica** lista para un modelo. El dato es el PM2.5 diario de 14 estaciones del SINCA,
2020–2025 (`aire_diario.csv`, 30.674 días-estación), cargado en SQLite: agregaciones por
estación y mes (`GROUP BY`), niveles de episodio del D.S. 12/2011 con `CASE WHEN` (alerta
80–109, preemergencia 110–169, emergencia ≥ 170 µg/m³), el PM2.5 de ayer y la media móvil de
la semana previa con funciones de ventana (`LAG`, `AVG OVER`) **sin fuga de información**, y la
tabla analítica por estación. La profundización transfiere el oficio a los 1.601 sismos
M ≥ 4,5 de Chile 2020–2025 (`sismos.csv`, catálogo USGS): *features* por zona y año, banderas,
días desde el sismo anterior y una CTE (`WITH`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: sismos reales por zona, `julianday` + `LAG`, CTE.
- `solucion.ipynb`, `profundiza_solucion.ipynb` — soluciones de referencia.
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
