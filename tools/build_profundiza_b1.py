# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B1 (SQL para *features*):
B1/profundiza.ipynb (estudiante) + B1/profundiza_solucion.ipynb (resuelto).

Es más TEÓRICO que la lección: explica el *porqué* de una buena feature, la FUGA DE
DATOS (leakage) de objetivo y temporal, la corrección punto-en-el-tiempo (point-in-time)
y el TABLÓN ANALÍTICO (1 fila por entidad). Todas las demos corren OFFLINE con pandas/
numpy/sklearn/matplotlib sobre el mismo dataset del módulo: sismos.csv."""
import json, os

BASE = "B1-sql-para-features"

TITULO = """# B1 · SQL para *features* — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B1 —donde *fabricaste* features con
`GROUP BY`, `CASE WHEN` y `LAG`— aquí vamos al *porqué*: **qué hace que una feature sea buena**
(relevante, disponible *al momento de predecir* y no trivialmente derivada del objetivo), qué es la
**fuga de datos** (*data leakage*) de objetivo y la **temporal**, en qué consiste la corrección
**punto-en-el-tiempo** (*point-in-time*: usar solo lo que existía **antes** del evento) y por qué el
**tablón analítico** (ABT) tiene **una fila por entidad**.

Menos sintaxis nueva, más **criterio de ciencia de datos**. Todo corre **sin conexión** sobre el mismo
dataset del módulo, y los ejercicios del final son **conceptuales** y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de B1. Mismo dataset: `sismos.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# sismos.csv del módulo (mismo dato de la lección). Si no está, se intenta descargar.
if not os.path.exists("sismos.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B1-sql-para-features/sismos.csv"
        urllib.request.urlretrieve(url, "sismos.csv")
    except Exception:
        print("Si estás en Colab, sube sismos.csv manualmente.")

df = pd.read_csv("sismos.csv")
# Lo ordenamos del más ANTIGUO al más reciente: clave para razonar el tiempo en este cuaderno.
df = df.sort_values("fecha_hora").reset_index(drop=True)
print(f"{len(df)} sismos | {df['region'].nunique()} regiones | magnitud media {df['magnitud'].mean():.2f}")
print("Ordenados del más antiguo al más reciente (así pensaremos el tiempo).")"""

S1 = """## 1. ¿Qué hace BUENA a una *feature*?

En la lección fabricaste columnas con SQL. Pero fabricar *cualquier* columna no sirve: una **buena
feature** cumple tres condiciones, y olvidar cualquiera arruina el modelo en la vida real:

1. **Relevante:** se mueve junto con lo que quieres predecir. Una columna constante (el mismo valor para
   todas las filas) no aporta **nada**: el modelo no puede distinguir un caso de otro mirándola.
2. **Disponible al momento de predecir:** tiene que existir **antes** del evento que intentas anticipar.
   Si solo la conocerás *después*, no podrás usarla cuando de verdad necesites predecir (lo veremos en las
   secciones 3 y 5).
3. **No trivialmente derivada del objetivo:** si la feature es, en el fondo, *el mismo objetivo disfrazado*,
   el modelo "acertará" todo en entrenamiento y fracasará en producción. Eso es **fuga de datos** (sección 2).

Empecemos por la más fácil de medir: la **relevancia**. Una feature que no varía (varianza ≈ 0) es ruido
puro. Comparemos una feature **constante** (inútil) con una feature **informativa**."""

S1_CODE = """# Una feature CONSTANTE: el mismo valor para todos los sismos -> no distingue nada
df["pais"] = "Chile"          # todas las filas iguales
# Una feature INFORMATIVA: la profundidad varía sismo a sismo
n_valores_pais = df["pais"].nunique()         # cardinalidad: 1 valor distinto = constante
var_informativa = df["profundidad_km"].std()  # dispersión real

# Como 'pais' es texto, medimos su cardinalidad (nunique). Si fuera numérica constante,
# su VARIANZA sería exactamente 0.0; lo comprobamos con una columna numérica constante:
var_pais_numerica = df.assign(pais_num=1)["pais_num"].var()  # columna constante -> varianza 0.0

print(f"Feature 'pais': {n_valores_pais} valor distinto (cardinalidad)  -> NO varía, INÚTIL.")
print(f"   (codificada como número constante, su varianza es {var_pais_numerica}: dispersión nula.)")
print(f"Feature 'profundidad_km': desviación estándar = {var_informativa:.1f} km -> VARÍA, informa.")
print(f"Rango de profundidad: de {df['profundidad_km'].min()} a {df['profundidad_km'].max()} km.")
print("\\nRegla: si una columna no varía, el modelo no aprende nada de ella. Bórrala.")"""

S2 = """## 2. Fuga de datos de OBJETIVO: la feature que es el objetivo disfrazado

La trampa más cara de la ciencia de datos tiene nombre: ***data leakage*** (fuga de datos). Ocurre cuando
una feature contiene —directa o disfrazadamente— **información del propio objetivo** que no tendrías al
momento real de predecir. El síntoma es siempre el mismo: **resultados demasiado buenos para ser verdad**
en las pruebas… y un fracaso total al ponerlo en producción.

Supongamos que el objetivo es marcar los sismos **fuertes** (magnitud ≥ 3,0). Una feature *con fuga* sería
usar la **propia magnitud** (o algo trivialmente derivado de ella, como `magnitud` redondeada): su
correlación con el objetivo se dispara y el modelo termina "acertando" el 100%… porque le estás **soplando
la respuesta**. La feature no *predice* el objetivo: **es** el objetivo.

> 🧠 **Analogía pública.** Es como "predecir" qué postulantes serán seleccionados usando como dato… la
> lista de seleccionados. Aciertas todo en la prueba, pero el día que llegue un postulante nuevo —sin esa
> lista— no tienes nada. Por eso la fuga **infla** el rendimiento de mentira y luego **colapsa**.

Veamos la correlación de una feature CON fuga (la magnitud misma) frente a una LEGÍTIMA (la profundidad,
que es un dato físico independiente de cómo definimos "fuerte")."""

S2_CODE = """# Objetivo ILUSTRATIVO: 1 si el sismo es 'fuerte' (magnitud >= 3.0), 0 si no
df["objetivo_fuerte"] = (df["magnitud"] >= 3.0).astype(int)

# Feature CON FUGA: la propia magnitud (de ella SALE el objetivo -> correlación altísima, pero inútil)
corr_fuga = np.corrcoef(df["magnitud"], df["objetivo_fuerte"])[0, 1]
# Feature LEGÍTIMA: la profundidad (dato físico, NO se usó para definir el objetivo)
corr_legit = np.corrcoef(df["profundidad_km"], df["objetivo_fuerte"])[0, 1]

print(f"corr(magnitud, objetivo)       = {corr_fuga:+.2f}   <- CON FUGA: es el objetivo disfrazado")
print(f"corr(profundidad, objetivo)    = {corr_legit:+.2f}   <- legítima: dato independiente")
print("\\nNota: una correlación moderada (0.52) es NORMAL y deseable: significa que la feature aporta")
print("información. El problema de fuga es específico de features que DEFINEN el objetivo, no de las")
print("que simplemente correlacionan con él. Una correlación sospechosamente alta (0.83) sobre una")
print("columna 'derivada del objetivo' es la señal clásica: el modelo ya casi sabe la respuesta de entrada.")"""

S3 = """## 3. Fuga TEMPORAL y corrección *point-in-time*

Hay una fuga más sutil que la anterior y muy común en datos de tiempo (la especialidad de la Línea B):
usar información del **futuro** para predecir el presente. Se llama **fuga temporal**.

La regla que la evita se llama **corrección punto-en-el-tiempo** (*point-in-time*): para predecir un
evento, **solo puedes usar información que ya existía justo ANTES de ese evento**. Ni el dato del propio
momento, ni nada posterior.

- **`LAG` (mirar atrás) es legítimo:** el sismo anterior **ya ocurrió** cuando llega el actual. Disponible.
- **`LEAD` o un promedio que incluye el futuro es fuga:** estás usando algo que **todavía no había pasado**.
  En entrenamiento parece magia; en producción ese dato **aún no existe**, y el modelo se queda ciego.

> 🧠 **Analogía pública.** Es como evaluar si una licitación va a tener problemas usando como "feature"
> el informe de auditoría que recién se escribió **un año después**. En la prueba aciertas; el día que
> tengas que evaluar una licitación *nueva*, ese informe **todavía no existe**.

Construyamos, sobre los sismos ordenados por tiempo, una feature **point-in-time correcta** (la magnitud
del sismo anterior, vía `shift(1)`, el `LAG` de pandas) y una **con fuga temporal** (la magnitud del sismo
*siguiente*, vía `shift(-1)`, el `LEAD`: información que *aún no había ocurrido*), y veamos en qué se delatan.

> 🔎 **Pista de detección.** Una feature construida con `shift(-1)` puro **deja un `NaN` justo en la última
> fila** (no hay "siguiente" para el último sismo). Por eso, si una columna solo falta **al final** de la
> serie, sospecha que mira el futuro. Cuidado: un `rolling` con `min_periods=1` puede *enmascarar* ese `NaN`;
> por eso la mejor práctica es revisar la **definición** de la feature, no solo dónde aparecen los `NaN`."""

S3_CODE = """# CORRECTA (point-in-time): magnitud del sismo ANTERIOR. shift(1) = el LAG de pandas.
df["mag_anterior"] = df["magnitud"].shift(1)
# CON FUGA TEMPORAL: magnitud del sismo SIGUIENTE (mira el futuro: shift(-1) = el LEAD).
# Es 'prom_futuro' por continuidad de nombre, pero es directamente la magnitud que AÚN NO ocurrió.
df["prom_futuro"] = df["magnitud"].shift(-1)

print("Primeras filas (df ya ordenado del más antiguo al más reciente):")
print(df[["id", "magnitud", "mag_anterior", "prom_futuro"]].head(4).to_string(index=False))

falta_inicio = int(df["mag_anterior"].isna().sum())   # el 1er sismo no tiene 'anterior'
falta_final = int(df["prom_futuro"].isna().sum())      # el último no tiene 'futuro'
print(f"\\n'mag_anterior' es NaN en {falta_inicio} fila (la PRIMERA): correcto, no tiene pasado.")
print(f"'prom_futuro' es NaN en {falta_final} fila (la ÚLTIMA): la pista de que MIRA EL FUTURO.")
print("Si una feature solo falta al FINAL de la serie, sospecha: probablemente usa el futuro = fuga.")"""

S4 = """## 4. El caso completo: una feature que "mira el futuro" engaña en la prueba

Veámoslo con un modelito de verdad (un árbol de decisión, *offline*). Entrenamos dos clasificadores para
el objetivo "sismo fuerte":

- Uno usa la feature **con fuga** (la propia magnitud, que define el objetivo).
- Otro usa una feature **legítima** (la profundidad, un dato físico independiente).

El de la fuga dará una precisión **perfecta o casi** en los mismos datos con que se entrenó. No es talento:
es que le pasamos la respuesta. La lección es que **una precisión sospechosamente alta es una alarma de
fuga**, no un trofeo."""

S4_CODE = """from sklearn.tree import DecisionTreeClassifier

y = df["objetivo_fuerte"].values
X_fuga = df[["magnitud"]].values        # feature CON fuga (de ella sale el objetivo)
X_legit = df[["profundidad_km"]].values # feature legítima (dato físico independiente)

acc_fuga = DecisionTreeClassifier(random_state=0).fit(X_fuga, y).score(X_fuga, y)
acc_legit = DecisionTreeClassifier(random_state=0, max_depth=2).fit(X_legit, y).score(X_legit, y)

print(f"Precisión en entrenamiento CON FUGA (magnitud):     {acc_fuga:.0%}  <- demasiado bueno")
print(f"Precisión en entrenamiento legítima (profundidad):  {acc_legit:.0%}")
print("\\nEl 100% no es talento: es que la feature ESCONDÍA la respuesta. En producción, donde la")
print("'magnitud' es justo lo que quieres anticipar, esa feature no existiría y el modelo fallaría.")"""

S5 = """## 5. Granularidad y el TABLÓN ANALÍTICO: una fila por entidad

El último concepto profundo es la **granularidad**: ¿qué representa **una fila** de tu tabla? En los datos
crudos, una fila es **un sismo** (un evento). Pero un modelo que decide *por región* necesita una tabla
donde una fila sea **una región**. Esa tabla —**una fila por entidad, una columna por feature**— es el
**tablón analítico** (*Analytical Base Table*, ABT).

¿Por qué importa tanto la regla "**una fila por entidad**"? Porque si por error te quedan **varias filas
por entidad**, el modelo "ve" a esa entidad varias veces: la **sobre-representa** y aprende sesgado hacia
ella. Pasar de la granularidad de **evento** a la de **entidad** es, justamente, lo que hace `GROUP BY`:
colapsa muchos eventos en una sola fila-resumen por entidad.

> 🧠 **Analogía pública.** Un registro de **atenciones** tiene una fila por atención; un tablón de
> **pacientes** tiene una fila por paciente (con su total de atenciones, su promedio, etc.). Confundir
> ambas granularidades es la causa #1 de tablas mal armadas en el Estado.

Construyamos el ABT por región y **verifiquemos** que de verdad quedó con una sola fila por entidad."""

S5_CODE = """# De granularidad EVENTO (1 fila = 1 sismo) a granularidad ENTIDAD (1 fila = 1 región)
abt = (df.groupby("region")
         .agg(n_sismos=("id", "size"),
              magnitud_promedio=("magnitud", "mean"),
              magnitud_maxima=("magnitud", "max"),
              profundidad_promedio=("profundidad_km", "mean"))
         .round(2)
         .reset_index())

print(f"Filas crudas (eventos): {len(df)}   ->   filas del ABT (entidades): {len(abt)}")
print(f"¿Una fila por región? Filas={len(abt)}, regiones únicas={df['region'].nunique()} -> "
      f"{'sí' if len(abt) == df['region'].nunique() else 'NO'}\\n")
print(abt.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 3.5))
orden = abt.sort_values("n_sismos", ascending=True)
ax.barh(orden["region"], orden["n_sismos"], color="#0a7e7e")
ax.set_title("Tablón analítico: n° de sismos por región (1 fila por entidad)")
ax.set_xlabel("N° de sismos"); plt.tight_layout(); plt.show()"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Celebrar una precisión casi perfecta.** En vez de festejar, sospecha **fuga de datos**: ¿alguna feature esconde el objetivo?
- **Usar una feature que solo conocerás *después* del evento.** Si no existe al momento de predecir, no sirve para predecir.
- **Construir features mirando el futuro (`LEAD`, promedios que incluyen filas posteriores).** Es **fuga temporal**: aplica *point-in-time*, usa solo el pasado.
- **Incluir el propio objetivo (o algo trivialmente derivado de él) entre las features.** El modelo "acierta" en la prueba y colapsa en producción.
- **Confundir granularidades:** dejar varias filas por entidad en el tablón. Una fila por entidad, o la entidad queda sobre-representada.
- **Agregar features constantes.** Una columna que no varía no aporta información: es ruido que estorba."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula algo** y luego pide **elegir la interpretación
correcta** (una letra). Todo corre **sin conexión**. Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 relevancia / feature constante ----
E1 = """## Ejercicio 01 · ¿Esta feature aporta? (relevancia)
En la sección 1 vimos que una feature **constante** no informa. Mídelo tú:

- Guarda en `n_valores_pais` cuántos **valores distintos** tiene la columna `df["pais"]` (pista: `.nunique()`).
- Guarda en `n_valores_region` cuántos valores distintos tiene `df["region"]`.
- Elige en `conclusion` (letra) la lectura correcta:
  - **A.** `pais` aporta más que `region` porque es más simple.
  - **B.** `pais` es **constante** (1 solo valor): no distingue filas, es inútil; `region` sí varía y aporta.
  - **C.** Ambas aportan lo mismo, da igual cuál uses."""
E1_TODO = """n_valores_pais = None     # TODO: df["pais"].nunique()
n_valores_region = None   # TODO: df["region"].nunique()
conclusion = None         # TODO: "A", "B" o "C"
"""
E1_SOL = """n_valores_pais = df["pais"].nunique()
n_valores_region = df["region"].nunique()
conclusion = "B"
"""
E1_CHK = """try:
    _p = df["pais"].nunique()
    _r = df["region"].nunique()
    _correcta = "B" if _p < _r else "A"
    assert n_valores_pais is not None and int(n_valores_pais) == _p, f"n_valores_pais debería ser {_p}."
    assert n_valores_region is not None and int(n_valores_region) == _r, f"n_valores_region debería ser {_r}."
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿cuál columna NO varía entre filas?"
    print(f"✅ Correcto. 'pais' tiene {_p} valor (constante, inútil) y 'region' {_r} (varía y aporta).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 fuga de objetivo / correlacion ----
E2 = """## Ejercicio 02 · Fuga de objetivo (correlación sospechosa)
Usa el objetivo `df["objetivo_fuerte"]` (creado en la sección 2). En **valor absoluto**:

- Guarda en `corr_fuga` la correlación entre `df["magnitud"]` y el objetivo (feature CON fuga).
- Guarda en `corr_legit` la correlación entre `df["profundidad_km"]` y el objetivo (feature legítima).
- Elige en `conclusion` la interpretación correcta:
  - **A.** `corr_fuga` es **mucho mayor** que `corr_legit`: esa correlación sospechosamente alta delata **fuga** (la magnitud *define* el objetivo), no una buena feature.
  - **B.** `corr_legit` es mayor, así que la profundidad tiene fuga.
  - **C.** Las dos correlaciones son iguales, no hay forma de distinguir fuga.

Pista: `abs(np.corrcoef(a, b)[0, 1])`."""
E2_TODO = """corr_fuga = None    # TODO: abs(corr de df["magnitud"] con df["objetivo_fuerte"])
corr_legit = None   # TODO: abs(corr de df["profundidad_km"] con df["objetivo_fuerte"])
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """corr_fuga = abs(np.corrcoef(df["magnitud"], df["objetivo_fuerte"])[0, 1])
corr_legit = abs(np.corrcoef(df["profundidad_km"], df["objetivo_fuerte"])[0, 1])
conclusion = "A"
"""
E2_CHK = """try:
    _cf = abs(np.corrcoef(df["magnitud"], df["objetivo_fuerte"])[0, 1])
    _cl = abs(np.corrcoef(df["profundidad_km"], df["objetivo_fuerte"])[0, 1])
    _correcta = "A" if _cf > _cl else "B"
    assert corr_fuga is not None and abs(corr_fuga - _cf) < 0.01, f"corr_fuga debería ser ~{_cf:.2f}."
    assert corr_legit is not None and abs(corr_legit - _cl) < 0.01, f"corr_legit debería ser ~{_cl:.2f}."
    assert str(conclusion).strip().upper() == _correcta, "Pista: una corr sospechosamente alta con algo derivado del objetivo = fuga."
    print(f"✅ Correcto. corr_fuga={_cf:.2f} >> corr_legit={_cl:.2f}: la magnitud esconde el objetivo (fuga).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 point-in-time ----
E3 = """## Ejercicio 03 · Point-in-time: ¿pasado o futuro?
`df` está ordenado del más antiguo al más reciente. En la sección 3 creamos `mag_anterior` (mira el
pasado, vía `shift(1)`) y `prom_futuro` (la magnitud del sismo *siguiente*, mira el futuro, vía `shift(-1)`).

- Guarda en `nan_anterior` cuántos `NaN` tiene `df["mag_anterior"]` (pista: `.isna().sum()`).
- Guarda en `nan_futuro` cuántos `NaN` tiene `df["prom_futuro"]`.
- Elige en `conclusion` la lectura correcta:
  - **A.** `mag_anterior` es point-in-time **correcta** (solo falta al inicio: no hay pasado para el 1°); `prom_futuro` **mira el futuro** (falta al final: no hay sismo siguiente para el último) y es **fuga temporal**.
  - **C.** `prom_futuro` es la correcta porque mirar el promedio siempre es bueno.
  - **B.** Ambas son igual de válidas porque las dos tienen un `NaN`."""
E3_TODO = """nan_anterior = None   # TODO: df["mag_anterior"].isna().sum()
nan_futuro = None     # TODO: df["prom_futuro"].isna().sum()
conclusion = None     # TODO: "A", "B" o "C"
"""
E3_SOL = """nan_anterior = int(df["mag_anterior"].isna().sum())
nan_futuro = int(df["prom_futuro"].isna().sum())
conclusion = "A"
"""
E3_CHK = """try:
    _na = int(df["mag_anterior"].isna().sum())
    _nf = int(df["prom_futuro"].isna().sum())
    assert nan_anterior is not None and int(nan_anterior) == _na, f"nan_anterior debería ser {_na}."
    assert nan_futuro is not None and int(nan_futuro) == _nf, f"nan_futuro debería ser {_nf}."
    # La conclusión correcta es siempre "A" porque es una pregunta CONCEPTUAL, no depende de los datos del CSV.
    assert str(conclusion).strip().upper() == "A", "Pista: ¿cuál usa solo el pasado y cuál mira hacia adelante?"
    print(f"✅ Correcto. 'mag_anterior' es point-in-time correcta; 'prom_futuro' mira el futuro = fuga temporal.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 granularidad / ABT ----
E4 = """## Ejercicio 04 · Granularidad del tablón analítico
Quieres un tablón con **una fila por región**. Cuenta y compara:

- Guarda en `filas_evento` el número de filas crudas de `df` (granularidad evento: `len(df)`).
- Guarda en `filas_entidad` cuántas **regiones distintas** hay (`df["region"].nunique()`): el tamaño que
  debe tener el ABT.
- Elige en `conclusion` la lectura correcta:
  - **A.** El ABT debe tener `filas_evento` filas, una por sismo.
  - **B.** El ABT debe tener `filas_entidad` filas (una por región); pasamos de evento a entidad con `GROUP BY`. Si quedan más, la región se **sobre-representa**.
  - **C.** Da igual cuántas filas tenga el ABT mientras estén los datos."""
E4_TODO = """filas_evento = None    # TODO: len(df)
filas_entidad = None   # TODO: df["region"].nunique()
conclusion = None      # TODO: "A", "B" o "C"
"""
E4_SOL = """filas_evento = len(df)
filas_entidad = df["region"].nunique()
conclusion = "B"
"""
E4_CHK = """try:
    _fe = len(df)
    _fent = df["region"].nunique()
    assert filas_evento is not None and int(filas_evento) == _fe, f"filas_evento debería ser {_fe}."
    assert filas_entidad is not None and int(filas_entidad) == _fent, f"filas_entidad debería ser {_fent}."
    # La conclusión correcta es siempre "B" porque es una pregunta CONCEPTUAL, no depende de los datos del CSV.
    assert str(conclusion).strip().upper() == "B", "Pista: el tablón tiene UNA fila por entidad (región)."
    print(f"✅ Correcto. De {_fe} eventos a {_fent} entidades: el ABT lleva una fila por región (GROUP BY).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo *fabricas* features con SQL: entiendes **qué hace buena a una feature** (relevante, disponible
al predecir, no derivada del objetivo), reconoces la **fuga de datos** —de objetivo y **temporal**—,
aplicas la corrección **point-in-time** (solo el pasado) y sabes por qué el **tablón analítico** lleva
**una fila por entidad**.

La regla de oro que te llevas: **antes de confiar en una feature, pregúntate si la conocerías de verdad
en el momento de predecir, y si no esconde la respuesta.** Una precisión "perfecta" casi nunca es un
trofeo: suele ser una **fuga**. Eso distingue a quien *entrena* modelos de quien *se deja engañar* por ellos.

> **Hacia dónde sigue:** con un tablón analítico limpio y sin fugas, en el próximo módulo entrenarás tu
> primer modelo de Machine Learning sobre features en las que de verdad se puede confiar."""


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
