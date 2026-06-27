# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B6 (despliegue de modelos):
B6/profundiza.ipynb (estudiante) + B6/profundiza_solucion.ipynb (resuelto).

TODO el cuaderno es CONCEPTUAL y verificable SIN servidores ni API:
demos OFFLINE en pandas/numpy/sklearn sobre el dataset del módulo (compras_ml.csv).
Profundiza en el *porqué* del despliegue: producción real, contrato del modelo,
validación de entrada, drift de datos vs de concepto, cadencia de reentrenamiento,
model card y humano en el bucle. NO se monta ningún servicio (sin Flask/FastAPI)."""
import json, os

BASE = "B6-despliegue-de-modelos"

TITULO = """# B6 · Despliegue de modelos — Profundización (opcional) 🔬

**Formación Pública — Capa B · Ciencia de datos aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B6 —donde dejaste tu modelo *usable* con una
función de predicción, validación de rango y puntuación por lotes— aquí vamos al *porqué*: **qué implica
de verdad poner un modelo en producción**, qué es el **contrato del modelo**, por qué la validación de
entrada es más que un `if`, qué es el **drift** (y por qué hay **dos tipos**: de datos y de concepto),
cada cuánto **reentrenar**, qué es una **model card** y por qué el Estado necesita un **humano en el bucle**.

Menos código de despliegue, más **modelo mental de operación**. **No montamos ningún servicio** (nada de
Flask/FastAPI ni servidores): todo corre **offline** con `pandas`, `numpy` y `scikit-learn`, para *ver*
funcionar los mecanismos que sostienen un modelo en el tiempo. Los ejercicios del final son **conceptuales**
y se autocorrigen.

> Requisito: haber hecho `leccion.ipynb` de B6. Mismo dataset: `compras_ml.csv`."""

CARGA = """import os, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

SEMILLA = 42

if not os.path.exists("compras_ml.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B6-despliegue-de-modelos/compras_ml.csv"
        urllib.request.urlretrieve(url, "compras_ml.csv")
    except Exception:
        print("Si estás en Colab, sube compras_ml.csv manualmente.")

df = pd.read_csv("compras_ml.csv")

# Entrenamos el MISMO modelo simple de la lección (en memoria, offline)
X = df[["cantidad", "tamano_num"]]
y = df["monto_total"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEMILLA)
modelo = Pipeline([("escalador", StandardScaler()),
                   ("knn", KNeighborsRegressor(n_neighbors=3))])
modelo.fit(X_train, y_train)

print(f"{len(df)} compras cargadas | modelo entrenado en {len(X_train)} filas")
print("Este cuaderno NO levanta ningún servidor: todo corre en memoria, offline.")"""

# ----------------------------------------------------------------------------
S1 = """## 1. "Producción" no es el modelo: es todo lo que lo rodea

En la lección dejaste el modelo *usable*: una función que recibe datos y devuelve un monto. Eso es el
**punto de partida**, no el final. Llevar un modelo a **producción** de verdad —que lo use gente real,
todos los días, sin que tú estés mirando— significa hacerse cargo de todo lo que rodea a ese `.predict()`.

La analogía pública: el modelo es como **un trámite nuevo en una oficina**. Diseñar el formulario (el
modelo) es la parte fácil. Lo difícil —y lo que hace que el trámite *funcione*— es lo de alrededor:

- **¿Qué datos entran y en qué formato?** (el contrato — sección 2)
- **¿Qué pasa si llega un dato basura o malicioso?** (validación — sección 3)
- **¿Cómo sé si el modelo sigue acertando meses después?** (monitoreo y *drift* — secciones 4 y 5)
- **¿Cada cuánto lo actualizo?** (cadencia de reentrenamiento — sección 5)
- **¿Quién responde si se equivoca y afecta a una persona?** (model card y humano en el bucle — sección 6)

A esa disciplina de **operar** modelos en el tiempo se le llama **MLOps**. La idea central de este cuaderno:
**el código que entrena el modelo es la punta del iceberg**; debajo está todo lo que evita que el modelo
te traicione en silencio. Veamos primero cuánto "sabe" realmente tu modelo: solo conoce el rango de datos
con que lo entrenaste."""

S1_CODE = """# ¿En qué 'mundo' fue entrenado el modelo? Solo conoce el rango de sus datos de entrenamiento.
rango_entrenado = {
    "cantidad":   (int(X_train["cantidad"].min()),   int(X_train["cantidad"].max())),
    "tamano_num": (int(X_train["tamano_num"].min()), int(X_train["tamano_num"].max())),
}
print("El modelo SOLO ha 'visto' datos en estos rangos:")
for col, (lo, hi) in rango_entrenado.items():
    print(f"  {col:<11}: de {lo} a {hi}")

# Si le pedimos predecir MUY fuera de ese mundo, igual responde un número... sin avisar que extrapola.
fuera = pd.DataFrame({"cantidad": [99999], "tamano_num": [2]})
print(f"\\nPredicción para cantidad=99999 (jamás vista): {modelo.predict(fuera)[0]:,.0f} CLP")
print("El modelo NO se queja: devuelve un número aunque esté inventando fuera de su experiencia.")
print("Por eso producción necesita reglas ALREDEDOR del modelo, no solo el modelo.")"""

# ----------------------------------------------------------------------------
S2 = """## 2. El contrato del modelo: esquema de entrada y de salida

Antes de exponer un modelo, hay que escribir su **contrato**: un acuerdo explícito de **qué entra** y
**qué sale**. Es el equivalente al **encabezado de un formulario oficial**: define cada campo, su tipo,
su rango válido y qué obtienes de vuelta. Sin contrato, cada quien manda los datos "como le parece" y el
sistema se cae (o, peor, responde cualquier cosa sin avisar).

Un contrato tiene dos lados:

- **Esquema de ENTRADA:** qué campos exige (`cantidad`, `tamano_num`), de qué **tipo** (entero), en qué
  **rango** válido, cuáles son obligatorios. Es la "letra chica" que protege al modelo.
- **Esquema de SALIDA:** qué devuelve y en qué forma. En la lección devolviste un **diccionario**
  (`{"ok": True, "monto_estimado": ...}`). Eso *es* un contrato de salida: quien te consume sabe que
  siempre recibirá esa estructura, con esos nombres, pase lo que pase.

¿Por qué importa tanto en el Estado? Porque un modelo desplegado lo consumen **otros sistemas y otras
personas**, hoy y dentro de dos años. El contrato es lo que permite que el de al lado integre tu modelo
sin llamarte por teléfono, y lo que hace que un cambio tuyo no rompa silenciosamente a tres oficinas.
Construyamos el contrato a partir de los datos reales."""

S2_CODE = """# Derivamos el contrato de ENTRADA directamente de los datos de entrenamiento.
CONTRATO_ENTRADA = {
    "cantidad":   {"tipo": "int", "min": int(X_train["cantidad"].min()),
                                   "max": int(X_train["cantidad"].max()), "obligatorio": True},
    "tamano_num": {"tipo": "int", "min": int(X_train["tamano_num"].min()),
                                   "max": int(X_train["tamano_num"].max()), "obligatorio": True},
}
# Contrato de SALIDA: SIEMPRE esta forma, haya éxito o error (como en la lección).
CONTRATO_SALIDA = {"ok": "bool", "monto_estimado": "float|None", "error": "str|None"}

print("ESQUEMA DE ENTRADA (qué exige el modelo):")
for campo, regla in CONTRATO_ENTRADA.items():
    print(f"  {campo:<11} tipo={regla['tipo']}  rango=[{regla['min']}, {regla['max']}]  obligatorio={regla['obligatorio']}")
print("\\nESQUEMA DE SALIDA (qué promete devolver, siempre igual):")
print(" ", CONTRATO_SALIDA)
print("\\nQuien consuma el modelo se apoya en este contrato: no en cómo está hecho por dentro.")"""

# ----------------------------------------------------------------------------
S3 = """## 3. Validación de entrada: rechazar lo que el modelo no puede honrar

En la lección validaste **rangos** con un `if`. Eso es el primer escalón. Un despliegue serio valida la
entrada **contra el contrato completo**, en este orden, y se detiene en el primer problema:

1. **¿Está el campo?** Si falta un obligatorio, no hay nada que predecir.
2. **¿Es del tipo correcto?** Un `"50"` (texto) o un `50.5` donde se esperaba un entero es un dato malo,
   aunque "parezca" un número. Validar el **tipo** evita errores silenciosos.
3. **¿Está en rango?** Una `cantidad` de `99999` (noventa y nueve mil) está fuera del mundo que el modelo conoce (sección 1):
   predeciría **extrapolando**, sin base. Mejor rechazarla que devolver un número inventado.

La regla de oro: **es preferible un "no puedo con este dato" honesto que una predicción segura pero
basura.** En el Estado, una cifra equivocada que *parece* válida puede terminar en una resolución,
un pago o una negativa a un ciudadano. La validación es la barrera que evita que el modelo "responda"
cuando en realidad no debería. Escribamos la validación contra el contrato y probémosla con datos sanos
y datos malos."""

S3_CODE = """def validar_entrada(registro):
    \"\"\"Devuelve (es_valido, lista_de_errores) comparando el registro contra CONTRATO_ENTRADA.\"\"\"
    errores = []
    for campo, regla in CONTRATO_ENTRADA.items():
        if campo not in registro:                      # 1. ¿falta?
            errores.append(f"falta el campo obligatorio '{campo}'")
            continue
        valor = registro[campo]
        # 2. ¿tipo correcto? (bool es subclase de int en Python: lo excluimos a propósito)
        if not isinstance(valor, (int, np.integer)) or isinstance(valor, bool):
            errores.append(f"'{campo}' debe ser entero, llegó {type(valor).__name__}")
            continue
        if valor < regla["min"] or valor > regla["max"]:   # 3. ¿en rango?
            errores.append(f"'{campo}'={valor} fuera de rango [{regla['min']}, {regla['max']}]")
    return (len(errores) == 0, errores)

casos = [
    {"cantidad": 50,    "tamano_num": 2},     # ok
    {"cantidad": 99999, "tamano_num": 2},     # fuera de rango
    {"cantidad": 50,    "tamano_num": 9},     # tamano inexistente
    {"cantidad": 50.5,  "tamano_num": 2},     # tipo equivocado (no entero)
    {"cantidad": 50},                          # falta un campo
]
for c in casos:
    ok, errs = validar_entrada(c)
    print(f"{str(c):<42} -> {'ACEPTADO' if ok else 'RECHAZADO: ' + '; '.join(errs)}")"""

# ----------------------------------------------------------------------------
S4 = """## 4. Monitoreo y *drift* de DATOS: el mundo cambia bajo tus pies

Un modelo entrenado es una **foto** del mundo en el momento del entrenamiento. Pero el mundo **se mueve**:
cambian los proveedores, los precios, las regiones que compran, las políticas. Cuando los **datos nuevos**
empiezan a verse **distintos** a los datos de entrenamiento, hablamos de ***drift* de datos** (*data drift*).
El modelo no se "rompe" de golpe: **se va volviendo menos confiable en silencio**. Por eso se **monitorea**.

La analogía pública: es como un **mapa de la ciudad de hace 10 años**. El mapa sigue ahí, nadie te avisa
que está viejo, pero cada vez te lleva peor porque la ciudad cambió. El monitoreo es **comparar el mapa con
la calle de hoy**.

¿Cómo se *detecta* drift sin tener todavía los resultados reales? Comparando la **distribución** de un campo
entre "entrenamiento" y "datos nuevos". Una medida simple y robusta es la **diferencia estandarizada de
medias**: cuánto se movió el promedio del campo, medido en "desviaciones estándar" del entrenamiento.

> `drift = |media_nueva − media_entrenamiento| / desviación_estándar_entrenamiento`

Regla práctica: **bajo ~0,5** → estable; **sobre ~0,5** → la distribución se corrió, conviene investigar
*(umbral heurístico; cada equipo puede calibrarlo según su dominio, no es un estándar universal)*.
Simulemos dos llegadas de datos nuevos: una **parecida** al entrenamiento y otra con **drift** (compras
mucho más grandes que antes)."""

S4_CODE = """rng = np.random.default_rng(SEMILLA)

# 'Histórico' (con qué se entrenó) y dos tandas de 'datos nuevos' del resto del dataset
historico = df.sample(frac=0.5, random_state=SEMILLA)
resto = df.drop(historico.index)
nuevos_estables = resto.sample(1000, random_state=SEMILLA)
nuevos_con_drift = nuevos_estables.copy()
nuevos_con_drift["cantidad"] = (nuevos_con_drift["cantidad"] * 2.5 + 20).round().astype(int)  # el mundo cambió

def drift_score(referencia, nuevos, col):
    return abs(nuevos[col].mean() - referencia[col].mean()) / referencia[col].std()

ds_estable = drift_score(historico, nuevos_estables, "cantidad")
ds_drift   = drift_score(historico, nuevos_con_drift, "cantidad")
print(f"media 'cantidad' histórico:        {historico['cantidad'].mean():.1f}")
print(f"media 'cantidad' nuevos estables:  {nuevos_estables['cantidad'].mean():.1f}   drift={ds_estable:.2f}  -> ESTABLE")
print(f"media 'cantidad' nuevos con drift: {nuevos_con_drift['cantidad'].mean():.1f}  drift={ds_drift:.2f}  -> ¡DRIFT!")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(historico["cantidad"], bins=40, range=(0, 300), alpha=0.6, label="histórico (entrenamiento)", color="#0a7e7e")
ax.hist(nuevos_con_drift["cantidad"], bins=40, range=(0, 300), alpha=0.6, label="datos nuevos (con drift)", color="crimson")
ax.set_title("Drift de datos: la distribución de 'cantidad' se corrió")
ax.set_xlabel("cantidad"); ax.set_ylabel("frecuencia"); ax.legend()
plt.tight_layout(); plt.show()"""

# ----------------------------------------------------------------------------
S5 = """## 5. *Drift* de CONCEPTO y cadencia de reentrenamiento

El drift de datos (sección 4) es que **cambian las entradas**. Existe uno más traicionero: el ***drift* de
concepto** (*concept drift*), que es cuando **cambia la relación** entre las entradas y la respuesta. Las
mismas `cantidad` y `tamano_num` que antes predecían bien el monto, **ahora predicen mal**, porque la regla
del mundo cambió.

Ejemplo público clarísimo: llega **inflación**. La misma compra (misma cantidad, mismo proveedor) hoy
**cuesta más** que cuando se entrenó el modelo. Las entradas pueden verse iguales, pero el modelo, que
aprendió precios viejos, **subestima sistemáticamente**. Eso **no** lo detectas mirando solo las entradas:
necesitas comparar predicciones con la **realidad** (el monto real cuando llega).

La consecuencia operativa es la **cadencia de reentrenamiento**: cada cuánto vuelves a entrenar con datos
frescos. No hay número mágico; depende de qué tan rápido cambie tu dominio:

- **Dominio estable** (poca variación) → reentrenar cada varios meses o por año.
- **Dominio volátil** (precios, demanda, crisis) → reentrenar seguido, incluso mensual.
- **Lo correcto es disparar por señal, no por calendario:** reentrenar **cuando el monitoreo lo pide**
  (drift alto o error que sube), no "porque toca".

Veamos el efecto de la inflación sobre el error del modelo (MAE = error promedio **absoluto** en pesos;
"absoluto" = mide la magnitud del error sin importar si subestima o sobreestima)."""

S5_CODE = """# Error 'normal' del modelo sobre el test (mundo igual al de entrenamiento)
# (usamos nombres mae_estable / mae_inflado para no confundirlos con los que
#  calcularás tú mismo en el Ejercicio 03, mae_normal / mae_drift.)
mae_estable = mean_absolute_error(y_test, modelo.predict(X_test))

# Drift de CONCEPTO: mismas entradas, pero el monto REAL subió 40% (inflación). El modelo no lo sabe.
y_test_inflado = y_test * 1.4
mae_inflado = mean_absolute_error(y_test_inflado, modelo.predict(X_test))

print(f"MAE con el mundo estable:            {mae_estable:,.0f} CLP")
print(f"MAE tras 40% de inflación (concepto): {mae_inflado:,.0f} CLP")
print(f"El error subió {(mae_inflado/mae_estable - 1):.0%}: el modelo quedó desactualizado SIN que cambien las entradas.")
# Nota: el MAE no sube exactamente 40% porque el modelo no predecía el monto real exacto antes de la
# inflación (ya tenía algo de error). El 40% infla los montos REALES; el error es la distancia entre esa
# realidad inflada y lo que el modelo —desactualizado— sigue prediciendo. Lo importante es la dirección: sube.

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(["mundo estable", "tras inflación 40%"], [mae_estable, mae_inflado],
       color=["#0a7e7e", "crimson"])
ax.set_title("Drift de concepto: el error sube aunque las entradas se vean iguales")
ax.set_ylabel("MAE (error promedio absoluto en CLP)")
plt.tight_layout(); plt.show()
print("Por eso se monitorea el ERROR contra la realidad y se REENTRENA cuando se degrada.")"""

# ----------------------------------------------------------------------------
S6 = """## 6. Model card y humano en el bucle: gobernanza del modelo

Te queda lo más importante para el sector público, donde una predicción puede afectar **derechos**.

**La model card (ficha del modelo):** un documento breve y honesto que acompaña al modelo y responde, en
lenguaje claro: *¿para qué sirve y para qué NO?, ¿con qué datos se entrenó?, ¿qué tan bueno es y dónde
falla?, ¿qué sesgos o límites tiene?, ¿quién es responsable?, ¿cada cuánto se actualiza?*. Es el equivalente
al **prospecto de un medicamento**: nadie debería "recetar" un modelo sin leer sus indicaciones,
contraindicaciones y efectos adversos. En el Estado, la model card es lo que permite **auditar**,
**rendir cuentas** y **transparentar** una decisión asistida por un algoritmo.

**El humano en el bucle (*human in the loop*):** el modelo **asiste**, no **decide** lo que afecta a
personas. El monto estimado entra a una resolución, pero **una persona la firma**; una postulación se
prioriza, pero **alguien revisa** antes de rechazarla. Esto no es burocracia: es la diferencia entre un
error que **se atrapa** y uno que **se ejecuta** sobre un ciudadano. Y es coherente con todo lo anterior:
como el modelo puede driftear (4 y 5) y solo conoce su rango (1), **necesita supervisión humana donde hay
algo en juego.**

Resumamos la ficha del modelo de este módulo en una mini *model card* generada desde los datos reales."""

S6_CODE = """model_card = {
    "nombre": "Estimador de monto de compra (KNN, k=3)",
    "proposito": "Estimar monto_total a partir de cantidad y tamano_num (apoyo, NO decisión final)",
    "datos_entrenamiento": f"{len(X_train)} compras de ChileCompra (alimentos)",
    "rango_valido_cantidad": (int(X_train["cantidad"].min()), int(X_train["cantidad"].max())),
    "rango_valido_tamano_num": (int(X_train["tamano_num"].min()), int(X_train["tamano_num"].max())),
    "error_tipico_MAE_CLP": round(float(mean_absolute_error(y_test, modelo.predict(X_test)))),
    "limites_conocidos": "no extrapola fuera de rango; sensible a inflación (concept drift)",
    "supervision": "humano en el bucle: una persona revisa antes de usar la cifra en una decisión",
    "responsable": "equipo de datos de la institución",
}
print("MODEL CARD (ficha del modelo):")
for k, v in model_card.items():
    print(f"  {k:<24}: {v}")
print("\\nEsta ficha es lo que permite auditar, transparentar y rendir cuentas de una decisión asistida.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Creer que "el modelo entrena bien" = "está listo para producción".** Producción es todo lo de
  alrededor: contrato, validación, monitoreo, reentrenamiento y responsable.
- **Exponer un modelo sin contrato de entrada/salida.** Sin esquema, cada quien manda datos como quiere
  y el sistema falla o responde basura.
- **Validar solo el rango y olvidar el tipo y los campos faltantes.** Un `"50"` o un campo ausente también
  son entradas inválidas.
- **Asumir que el modelo "avisa" cuando extrapola.** No avisa: devuelve un número aunque el dato esté
  fuera del mundo que conoce.
- **Confundir drift de datos con drift de concepto.** El de datos cambia las *entradas*; el de concepto
  cambia la *relación* entrada→salida y solo se ve comparando con la realidad.
- **Reentrenar "por calendario" en vez de por señal.** Lo correcto es reentrenar cuando el monitoreo
  (drift o error) lo pide.
- **Automatizar una decisión que afecta derechos sin humano en el bucle ni model card.** En el Estado,
  el responsable es una persona, y debe poder explicar el modelo."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula algo** y te pide **elegir la interpretación correcta**.
**Ninguno levanta un servidor:** todo corre offline. Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: drift de datos ----
E1 = """## Ejercicio 01 · Detectar drift de datos
Usa `drift_score`, `historico` y `nuevos_con_drift` (definidos en la sección 4) sobre la columna `"cantidad"`.

- Guarda en `ds` el `drift_score(historico, nuevos_con_drift, "cantidad")`.
- Usando el umbral práctico **0,5**, elige en `conclusion` (letra) la lectura correcta:
  - **A.** `ds` es bajo (< 0,5): los datos nuevos se parecen al entrenamiento, todo estable.
  - **B.** `ds` es alto (≥ 0,5): la distribución de `cantidad` se corrió, hay **drift de datos** y conviene investigar/reentrenar.
  - **C.** El `drift_score` no sirve para decidir nada sin tener los montos reales."""
E1_TODO = """ds = None           # TODO: drift_score(historico, nuevos_con_drift, "cantidad")
conclusion = None   # TODO: "A", "B" o "C"
"""
E1_SOL = """ds = drift_score(historico, nuevos_con_drift, "cantidad")
conclusion = "B"
"""
E1_CHK = """try:
    _ds = drift_score(historico, nuevos_con_drift, "cantidad")
    _correcta = "B" if _ds >= 0.5 else "A"
    assert ds is not None and abs(ds - _ds) < 1e-6, f"ds debería ser ~{_ds:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Pista: compara ds con el umbral 0.5"
    print(f"✅ Correcto. drift_score = {_ds:.2f} (≥ 0.5): la distribución se corrió, hay drift de datos.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: validación de entrada por lotes ----
E2 = """## Ejercicio 02 · Validar un lote contra el contrato
Usa `validar_entrada` (sección 3) sobre este lote de 5 registros que ya está en la celda de respuesta.

- Guarda en `n_ok` cuántos registros **pasan** la validación (es decir, `validar_entrada(r)[0]` es `True`).
- Elige en `conclusion` la lectura correcta:
  - **A.** Todos los registros son válidos: la validación no rechaza nada.
  - **B.** Algunos registros se **rechazan** (faltan campos, tipo equivocado o fuera de rango): la validación
    protege al modelo de datos que no puede honrar.
  - **C.** La validación rechaza todo: ningún registro sirve.

Pista: `sum(1 for r in lote if validar_entrada(r)[0])`."""
E2_TODO = """lote = [
    {"cantidad": 50,   "tamano_num": 2},   # ok
    {"cantidad": 600,  "tamano_num": 3},   # cantidad fuera de rango
    {"cantidad": 10,   "tamano_num": 1},   # ok
    {"cantidad": 20,   "tamano_num": 9},   # tamano inexistente
    {"cantidad": 5,    "tamano_num": 4},   # ok
]
n_ok = None         # TODO: cuántos registros pasan validar_entrada
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """lote = [
    {"cantidad": 50,   "tamano_num": 2},   # ok
    {"cantidad": 600,  "tamano_num": 3},   # cantidad fuera de rango
    {"cantidad": 10,   "tamano_num": 1},   # ok
    {"cantidad": 20,   "tamano_num": 9},   # tamano inexistente
    {"cantidad": 5,    "tamano_num": 4},   # ok
]
n_ok = sum(1 for r in lote if validar_entrada(r)[0])
conclusion = "B"
"""
E2_CHK = """try:
    _lote = [
        {"cantidad": 50,   "tamano_num": 2},
        {"cantidad": 600,  "tamano_num": 3},
        {"cantidad": 10,   "tamano_num": 1},
        {"cantidad": 20,   "tamano_num": 9},
        {"cantidad": 5,    "tamano_num": 4},
    ]
    _n = sum(1 for r in _lote if validar_entrada(r)[0])
    _correcta = "A" if _n == len(_lote) else ("C" if _n == 0 else "B")
    assert n_ok is not None and int(n_ok) == _n, f"Deberían pasar {_n} de {len(_lote)} registros"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿la validación dejó pasar todo, nada o algunos?"
    print(f"✅ Correcto. Pasan {_n} de {len(_lote)}: la validación rechaza los que el modelo no puede honrar.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: drift de concepto / reentrenamiento ----
E3 = """## Ejercicio 03 · Drift de concepto y reentrenamiento
Reproduce el experimento de inflación de la sección 5 con `y_test`, `X_test` y `modelo`.

- Guarda en `mae_normal` el `mean_absolute_error(y_test, modelo.predict(X_test))`.
- Guarda en `mae_drift` el `mean_absolute_error(y_test * 1.4, modelo.predict(X_test))` (inflación del 40%).
- Elige en `conclusion` la lectura correcta:
  - **A.** El error baja con la inflación: el modelo mejora solo.
  - **B.** El error **sube** aunque las entradas no cambiaron: es **drift de concepto** y toca **reentrenar**
    con datos frescos.
  - **C.** El error no cambia: la inflación no afecta a un modelo entrenado."""
E3_TODO = """mae_normal = None   # TODO: error del modelo en y_test
mae_drift = None    # TODO: error contra y_test * 1.4 (inflación)
conclusion = None   # TODO: "A", "B" o "C"
"""
E3_SOL = """mae_normal = mean_absolute_error(y_test, modelo.predict(X_test))
mae_drift = mean_absolute_error(y_test * 1.4, modelo.predict(X_test))
conclusion = "B"
"""
E3_CHK = """try:
    _pred = modelo.predict(X_test)
    _mn = mean_absolute_error(y_test, _pred)
    _md = mean_absolute_error(y_test * 1.4, _pred)
    _correcta = "B" if _md > _mn else "A"
    assert mae_normal is not None and abs(mae_normal - _mn) < 1, f"mae_normal debería ser ~{_mn:,.0f}"
    assert mae_drift is not None and abs(mae_drift - _md) < 1, f"mae_drift debería ser ~{_md:,.0f}"
    assert str(conclusion).strip().upper() == _correcta, "Pista: ¿el error sube o baja con la inflación?"
    print(f"✅ Correcto. MAE {_mn:,.0f} -> {_md:,.0f} CLP: drift de concepto, toca reentrenar.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: humano en el bucle / model card (conceptual) ----
E4 = """## Ejercicio 04 · Humano en el bucle y model card (conceptual)
Una institución despliega tu estimador de monto. Un equipo propone: *"Conectemos el modelo directo al
sistema de pagos: que el monto estimado se apruebe y se pague automáticamente, sin que nadie lo revise,
para ahorrar tiempo"*.

Elige en `conclusion` la lectura correcta:
- **A.** Buena idea: si el modelo entrena bien, automatizar el pago sin revisión humana ahorra trabajo y no tiene riesgos.
- **B.** Riesgoso: el modelo puede **driftear** o **extrapolar** y solo *estima*. Una cifra que afecta un
  **pago** necesita **humano en el bucle** y una **model card** que documente límites y responsable. El modelo
  asiste; **decide y responde una persona**.
- **C.** Da igual: como hay validación de entrada, ya no hace falta ninguna supervisión humana.

*(Opcional, no se corrige): en `reflexion` escribe qué control humano agregarías antes de usar la cifra.)*"""
E4_TODO = """conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """conclusion = "B"
reflexion = "Un revisor humano aprueba el monto antes del pago, con alerta automática si el dato cae fuera de rango o el drift sube."
"""
E4_CHK = """try:
    assert conclusion is not None, "Aún no elegiste una letra en 'conclusion'."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿conviene pagar automáticamente con una cifra solo ESTIMADA, que puede driftear?"
    print("✅ Correcto. El modelo asiste; donde hay derechos en juego, decide y responde una persona (humano en el bucle).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir conclusion:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no piensas el despliegue como "una función que predice": entiendes que **producción es todo lo que
rodea al modelo** — el **contrato** de entrada/salida, la **validación** que rechaza lo que no puede
honrar, el **monitoreo** del **drift de datos** y del **drift de concepto**, la **cadencia de
reentrenamiento** disparada por señal, la **model card** que lo documenta y el **humano en el bucle**
que responde.

La regla de oro que te llevas para el Estado: **un modelo no es para siempre, y donde hay derechos en
juego, la decisión —y la responsabilidad— siempre es humana.** Eso distingue a quien *entrena* un modelo
de quien sabe **operarlo** con responsabilidad pública."""


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
