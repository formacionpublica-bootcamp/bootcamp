"""build_R2-09.py — módulo R2-09 (Despliegue + ficha de modelo + monitoreo).

Rama R2 (Científico de Datos). Rearmado 2026: se reemplaza el ejemplo anterior
por un caso de calidad del aire. El módulo reconstruye de forma autocontenida un pronóstico de PM2.5 del
día siguiente (SINCA, 14 estaciones, 2020–2025), lo guarda con joblib, lo
"despliega" (función en línea con validación + puntuación por lotes con faltantes
reales) y lo pone en PRODUCCIÓN sobre aire_nuevos.csv (2026, datos que el modelo no
vio): entregable CSV, monitoreo de desempeño (comparación justa por meses), drift de
faltantes y ficha de modelo honesta. Gradio opcional y protegido.
Profundiza: monitoreo por estación (El Bosque: el test 2025 no tenía invierno) y
umbral de alerta elegido en 2025 y evaluado en 2026.

Uso:  /opt/anaconda3/bin/python tools/build_R2-09.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-09-despliegue-de-modelos")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import numpy as np
import pandas as pd

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "aire_nuevos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

historia = pd.read_csv("aire_diario.csv", parse_dates=["fecha"])  # 2020–2025: lo que el modelo conoce
nuevos = pd.read_csv("aire_nuevos.csv", parse_dates=["fecha"])    # 2026: "producción", nunca lo vio
print("historia:", historia.shape, historia["fecha"].min().date(), "→", historia["fecha"].max().date())
print("nuevos:  ", nuevos.shape, nuevos["fecha"].min().date(), "→", nuevos["fecha"].max().date())'''

INTRO = '''## Un modelo en un cuaderno no le sirve a nadie

**Desplegar** es poner el modelo a trabajar para otras personas o sistemas, sobre datos que
**todavía no existían** cuando lo entrenaste. En este módulo harás el recorrido completo con un
caso real: un **pronóstico de PM2.5 del día siguiente** para 14 estaciones de monitoreo del SINCA.

Hay dos formas de usar un modelo desplegado:

- **En línea (uno a uno):** llega **un** caso y se necesita la respuesta al instante — por ejemplo,
  un formulario donde alguien de la SEREMI escribe el PM2.5 de hoy y ve el pronóstico de mañana.
- **Por lotes (*batch*):** llega una **tabla** con muchos casos — por ejemplo, todas las estaciones
  y todos los días de 2026 — y se devuelve un archivo con las predicciones.

Y hay una tercera parte que casi siempre se olvida: **cuidar el modelo** cuando ya está andando
(monitoreo, *drift*, faltantes) y **documentarlo** con una ficha honesta.

> **Producción de verdad:** `aire_nuevos.csv` trae enero–septiembre de **2026**, con los huecos
> reales de las estaciones (El Bosque perdió casi la mitad de sus días). El modelo nunca lo vio.'''

MODELO_MD = '''## 0. El modelo que vas a desplegar

En R2-08 encadenaste pasos en un **pipeline** de PM2.5 y lo guardaste con `joblib`. Aquí
reconstruimos, en una sola celda y sin depender de aquel archivo, una **variante más simple**
pensada para producción: **sin meteorología** (solo 7 de las 14 estaciones la miden, y un
imputador la «rellenaría» en silencio en las otras 7). La celda ya está hecha: ejecútala y lee
los comentarios.

- **Objetivo:** el PM2.5 de **mañana** (`pm25_manana`, µg/m³) en cada estación.
- **Features:** la estación, el PM2.5 de hoy y de ayer, la media de los últimos 7 días y el mes.
- **Partición temporal:** entrena con 2020–2024 y se prueba con 2025 (nunca al revés).
- **La receta de features es UNA sola función** (`construir_features`), que se usa igual al
  entrenar y en producción. Si las dos recetas difieren, el modelo falla **sin avisar**.'''

MODELO = '''import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

FEATURES = ["estacion", "pm25_hoy", "pm25_ayer", "media_7d", "mes"]
OBJETIVO = "pm25_manana"

def construir_features(df):
    """La MISMA receta para entrenar y para producción."""
    partes = []
    for estacion, d in df.groupby("estacion"):
        d = d.set_index("fecha").sort_index().asfreq("D")   # calendario completo: un día sin dato queda NaN
        d["estacion"] = estacion
        d["pm25_hoy"] = d["pm25"]
        d["pm25_ayer"] = d["pm25"].shift(1)
        d["media_7d"] = d["pm25"].rolling(7, min_periods=5).mean()
        d["mes"] = d.index.month
        d["pm25_manana"] = d["pm25"].shift(-1)               # lo que queremos predecir
        partes.append(d.reset_index())
    return pd.concat(partes, ignore_index=True)

# Historia + nuevos juntos: en producción el modelo SÍ conoce los días anteriores a hoy.
todo = construir_features(pd.concat([historia, nuevos], ignore_index=True))
completo = todo[FEATURES + [OBJETIVO]].notna().all(axis=1)
entrenamiento = todo[(todo["fecha"] < "2025-01-01") & completo]
prueba = todo[(todo["fecha"].dt.year == 2025) & completo]
produccion = todo[todo["fecha"] >= "2026-01-01"].reset_index(drop=True)

pre = ColumnTransformer([("est", OneHotEncoder(handle_unknown="ignore"), ["estacion"])],
                        remainder="passthrough")
pipeline = Pipeline([("pre", pre),
                     ("bosque", RandomForestRegressor(n_estimators=100, min_samples_leaf=10,
                                                      random_state=42, n_jobs=-1))])
pipeline.fit(entrenamiento[FEATURES], entrenamiento[OBJETIVO])
joblib.dump(pipeline, "modelo_pm25.joblib")                 # el ARTEFACTO que se despliega
print("Entrenado con", len(entrenamiento), "días-estación (2020–2024) → modelo_pm25.joblib")

# ── Desplegar empieza por CARGAR el artefacto (como lo haría otro equipo u otro servidor) ──
modelo = joblib.load("modelo_pm25.joblib")
ESTACIONES = sorted(entrenamiento["estacion"].unique())     # las que el modelo conoce
mae_prueba = mean_absolute_error(prueba[OBJETIVO], modelo.predict(prueba[FEATURES]))
mae_ingenuo_prueba = mean_absolute_error(prueba[OBJETIVO], prueba["pm25_hoy"])
print(f"MAE en prueba 2025: {mae_prueba:.2f} µg/m³  ·  línea base 'mañana = hoy': {mae_ingenuo_prueba:.2f}")
print("Filas de producción (2026):", len(produccion))'''

EJ = [
 ("## 1. La función de predicción: el corazón del despliegue",
  "Casi todo despliegue se reduce a **una función** que recibe datos nuevos y devuelve una "
  "predicción. Como guardamos el **pipeline completo**, la función no codifica la estación a "
  "mano: el pipeline ya sabe hacerlo.",
  "Escribe `predecir_pm25` (predicción en línea)",
  '''def predecir_pm25(estacion, pm25_hoy, pm25_ayer, media_7d, mes):
    entrada = pd.DataFrame({"estacion": [estacion], "pm25_hoy": [pm25_hoy], "pm25_ayer": [pm25_ayer],
                            "media_7d": [media_7d], "mes": [mes]})
    return round(float(modelo.predict(entrada)[0]), 1)

print("PM2.5 estimado para mañana en Cerro Navia:", predecir_pm25("Cerro Navia", 60, 55, 48, 6), "µg/m³")''',
  '''def predecir_pm25(estacion, pm25_hoy, pm25_ayer, media_7d, mes):
    entrada = pd.DataFrame({"estacion": [estacion], "pm25_hoy": [pm25_hoy], "pm25_ayer": [pm25_ayer],
                            "media_7d": [media_7d], "mes": [mes]})
    # TODO: usa modelo.predict(entrada), toma el elemento [0] y devuélvelo como float redondeado a 1 decimal
    return ...

print("PM2.5 estimado para mañana en Cerro Navia:", predecir_pm25("Cerro Navia", 60, 55, 48, 6), "µg/m³")''',
  '''_e = pd.DataFrame({"estacion": ["Cerro Navia"], "pm25_hoy": [60], "pm25_ayer": [55], "media_7d": [48], "mes": [6]})
esperado = round(float(modelo.predict(_e)[0]), 1)
obtenido = predecir_pm25("Cerro Navia", 60, 55, 48, 6)
assert isinstance(obtenido, float), "predecir_pm25 debe devolver un número (float)"
assert abs(obtenido - esperado) < 0.05, f"se esperaba ~{esperado}"''',
  "return round(float(modelo.predict(entrada)[0]), 1)",
  None),

 ("## 2. Un despliegue robusto valida la entrada",
  "Al modelo desplegado le van a llegar datos **malos**: una estación que no existe, un PM2.5 "
  "negativo, un **dato faltante** porque el monitor estuvo en mantención. Ojo: el bosque "
  "aleatorio de scikit-learn (≥1.4) **acepta NaN sin reclamar** y entrega un número igual — o "
  "sea, sin validación el modelo **inventa en silencio**. La validación es tuya.\n\n"
  "Devolvemos un **diccionario** (así conversan las APIs web): `{\"ok\": True, \"pm25_manana\": ...}` "
  "o `{\"ok\": False, \"error\": \"...\"}`.",
  "Escribe `predecir_seguro`",
  '''def predecir_seguro(estacion, pm25_hoy, pm25_ayer, media_7d, mes):
    if estacion not in ESTACIONES:
        return {"ok": False, "error": f"Estación desconocida: {estacion}"}
    valores = [pm25_hoy, pm25_ayer, media_7d]
    if any(pd.isna(v) for v in valores):
        return {"ok": False, "error": "Dato faltante: no se predice con huecos"}
    if not all(0 <= v <= 1000 for v in valores):
        return {"ok": False, "error": "PM2.5 fuera de rango físico (0–1000 µg/m³)"}
    if mes not in range(1, 13):
        return {"ok": False, "error": "Mes inválido"}
    return {"ok": True, "pm25_manana": predecir_pm25(estacion, pm25_hoy, pm25_ayer, media_7d, mes)}

print(predecir_seguro("Cerro Navia", 60, 55, 48, 6))
print(predecir_seguro("Cerro Navia", np.nan, 55, 48, 6))
print(predecir_seguro("Estación Inventada", 60, 55, 48, 6))''',
  '''def predecir_seguro(estacion, pm25_hoy, pm25_ayer, media_7d, mes):
    if estacion not in ESTACIONES:
        return {"ok": False, "error": f"Estación desconocida: {estacion}"}
    valores = [pm25_hoy, pm25_ayer, media_7d]
    # TODO 1: si algún valor es faltante (usa pd.isna) → {"ok": False, "error": "Dato faltante"}
    # TODO 2: si algún valor está fuera de 0–1000 µg/m³ → {"ok": False, "error": "Fuera de rango"}
    # TODO 3: si mes no está entre 1 y 12 → {"ok": False, "error": "Mes inválido"}
    return {"ok": True, "pm25_manana": predecir_pm25(estacion, pm25_hoy, pm25_ayer, media_7d, mes)}

print(predecir_seguro("Cerro Navia", 60, 55, 48, 6))
print(predecir_seguro("Cerro Navia", np.nan, 55, 48, 6))
print(predecir_seguro("Estación Inventada", 60, 55, 48, 6))''',
  '''bueno = predecir_seguro("Cerro Navia", 60, 55, 48, 6)
assert bueno["ok"] and abs(bueno["pm25_manana"] - predecir_pm25("Cerro Navia", 60, 55, 48, 6)) < 0.05, "el caso bueno debe predecir"
assert not predecir_seguro("Cerro Navia", np.nan, 55, 48, 6)["ok"], "un dato faltante debe rechazarse"
assert not predecir_seguro("Cerro Navia", -5, 55, 48, 6)["ok"], "un PM2.5 negativo debe rechazarse"
assert not predecir_seguro("Cerro Navia", 60, 55, 48, 13)["ok"], "el mes 13 debe rechazarse"
assert not predecir_seguro("Estación Inventada", 60, 55, 48, 6)["ok"]''',
  "Revisa con any(pd.isna(v) for v in valores), luego all(0 <= v <= 1000 for v in valores) y mes in range(1, 13).",
  None),

 ("## 3. Puntuación por lotes en producción (con faltantes reales)",
  "Ahora la tabla entera: `produccion` tiene **todas las estaciones y todos los días de 2026**. "
  "Las filas con algún feature faltante **no se predicen** (no inventamos): quedan con "
  "`pm25_predicho` vacío y `estado = \"sin_prediccion\"`, para que se vean y se cuenten.",
  "Escribe `puntuar_lote` y aplícalo a 2026",
  '''def puntuar_lote(tabla):
    resultado = tabla.copy()
    completo = resultado[FEATURES].notna().all(axis=1)
    resultado["pm25_predicho"] = np.nan
    resultado.loc[completo, "pm25_predicho"] = modelo.predict(resultado.loc[completo, FEATURES]).round(1)
    resultado["estado"] = np.where(completo, "ok", "sin_prediccion")
    return resultado

pred_2026 = puntuar_lote(produccion)
n_sin_prediccion = int((pred_2026["estado"] == "sin_prediccion").sum())
print("filas:", len(pred_2026), "| sin predicción:", n_sin_prediccion,
      f"({100 * n_sin_prediccion / len(pred_2026):.1f}%)")''',
  '''def puntuar_lote(tabla):
    resultado = tabla.copy()
    completo = resultado[FEATURES].notna().all(axis=1)     # True si la fila trae todos los datos
    resultado["pm25_predicho"] = np.nan
    # TODO: predice SOLO las filas completas, redondeado a 1 decimal:
    #       resultado.loc[completo, "pm25_predicho"] = modelo.predict(...).round(1)
    resultado["estado"] = np.where(completo, "ok", "sin_prediccion")
    return resultado

pred_2026 = puntuar_lote(produccion)
# TODO: cuántas filas quedaron con estado "sin_prediccion"
n_sin_prediccion = ...
print("filas:", len(pred_2026), "| sin predicción:", n_sin_prediccion)''',
  '''compl = produccion[FEATURES].notna().all(axis=1).values
assert len(pred_2026) == len(produccion), "debe haber una fila por cada fila de producción"
assert pred_2026["pm25_predicho"].notna().values.tolist() == compl.tolist(), "predice solo (y todas) las filas completas"
esp = modelo.predict(produccion.loc[compl, FEATURES]).round(1)
assert np.allclose(pred_2026.loc[compl, "pm25_predicho"].values, esp), "las predicciones no calzan con el modelo"
assert n_sin_prediccion == int((~compl).sum())''',
  'resultado.loc[completo, "pm25_predicho"] = modelo.predict(resultado.loc[completo, FEATURES]).round(1); '
  'n_sin_prediccion = int((pred_2026["estado"] == "sin_prediccion").sum()).',
  '''# ¿Dónde se concentran las filas sin predicción? (proporción por estación)
try:
    print((pred_2026["estado"] == "sin_prediccion").groupby(pred_2026["estacion"]).mean()
          .sort_values(ascending=False).round(2).head(6))
except Exception as e:
    print("Completa el ejercicio 3 para ver este resumen.", e)'''),

 ("## 4. Entregar el resultado",
  "El producto de un lote es un **archivo** que alguien más usa. Dos detalles de oficio: decir "
  "explícitamente **para qué día** es cada pronóstico (`fecha_objetivo` = fecha + 1 día) y "
  "dejar visible el `estado` de cada fila.",
  "Genera `predicciones_pm25_2026.csv`",
  '''entregable = pred_2026[["fecha", "estacion", "pm25_predicho", "estado"]].copy()
entregable["fecha_objetivo"] = entregable["fecha"] + pd.Timedelta(days=1)
entregable.to_csv("predicciones_pm25_2026.csv", index=False)
print("archivo creado:", os.path.exists("predicciones_pm25_2026.csv"), "| filas:", len(entregable))''',
  '''entregable = pred_2026[["fecha", "estacion", "pm25_predicho", "estado"]].copy()
# TODO: agrega la columna "fecha_objetivo" = fecha + 1 día  (pista: pd.Timedelta(days=1))
# TODO: guarda entregable en "predicciones_pm25_2026.csv" sin el índice
...
print("archivo creado:", os.path.exists("predicciones_pm25_2026.csv"))''',
  '''assert "fecha_objetivo" in entregable.columns, "falta la columna fecha_objetivo"
assert (entregable["fecha_objetivo"] - entregable["fecha"]).dt.days.eq(1).all()
leido = pd.read_csv("predicciones_pm25_2026.csv")
assert {"fecha_objetivo", "pm25_predicho", "estado"} <= set(leido.columns)
assert len(leido) == len(entregable)''',
  'entregable["fecha_objetivo"] = entregable["fecha"] + pd.Timedelta(days=1); luego entregable.to_csv("predicciones_pm25_2026.csv", index=False).',
  None),

 ("## 5. Monitoreo de desempeño: ¿sigue funcionando?",
  "En producción la verdad llega **un día después**: mañana sabremos cuánto marcó la estación. "
  "Con eso calculamos el **MAE en 2026**. Pero ojo con la comparación: la prueba 2025 cubre "
  "**todo el año**, y 2026 solo **enero–septiembre**, que incluye el invierno (cuando el PM2.5 "
  "es más alto y más difícil). La comparación **justa** es contra la prueba de los **mismos meses**. "
  "Y siempre contra la línea base: ¿el modelo le sigue ganando a «mañana = hoy»?",
  "MAE en 2026 vs prueba (mismos meses) vs línea base",
  '''con_verdad = pred_2026.dropna(subset=["pm25_predicho", "pm25_manana"])   # días con predicción Y dato real
mae_2026 = mean_absolute_error(con_verdad["pm25_manana"], con_verdad["pm25_predicho"])
prueba_mismos_meses = prueba[prueba["fecha"].dt.month <= 9]
mae_prueba_mismos_meses = mean_absolute_error(prueba_mismos_meses[OBJETIVO],
                                              modelo.predict(prueba_mismos_meses[FEATURES]))
mae_ingenuo_2026 = mean_absolute_error(con_verdad["pm25_manana"], con_verdad["pm25_hoy"])
print(f"MAE prueba 2025 (año completo): {mae_prueba:.2f}")
print(f"MAE prueba 2025 (ene–sep):      {mae_prueba_mismos_meses:.2f}   ← la comparación justa")
print(f"MAE producción 2026 (ene–sep):  {mae_2026:.2f}")
print(f"Línea base 2026 'mañana = hoy': {mae_ingenuo_2026:.2f}")''',
  '''con_verdad = pred_2026.dropna(subset=["pm25_predicho", "pm25_manana"])   # días con predicción Y dato real
# TODO: MAE en producción 2026 (pm25_manana real vs pm25_predicho)
mae_2026 = ...
# TODO: filas de `prueba` con mes <= 9, y su MAE (usa modelo.predict sobre sus FEATURES)
prueba_mismos_meses = ...
mae_prueba_mismos_meses = ...
# TODO: MAE de la línea base "mañana = hoy" en 2026 (pm25_manana vs pm25_hoy de con_verdad)
mae_ingenuo_2026 = ...
print("MAE 2026:", mae_2026, "| prueba ene–sep:", mae_prueba_mismos_meses, "| ingenuo 2026:", mae_ingenuo_2026)''',
  '''_cv = pred_2026.dropna(subset=["pm25_predicho", "pm25_manana"])
assert len(_cv) > 0, "primero completa el ejercicio 3"
assert abs(mae_2026 - mean_absolute_error(_cv["pm25_manana"], _cv["pm25_predicho"])) < 1e-6
_pm = prueba[prueba["fecha"].dt.month <= 9]
assert abs(mae_prueba_mismos_meses - mean_absolute_error(_pm[OBJETIVO], modelo.predict(_pm[FEATURES]))) < 1e-6
assert abs(mae_ingenuo_2026 - mean_absolute_error(_cv["pm25_manana"], _cv["pm25_hoy"])) < 1e-6''',
  'mean_absolute_error(con_verdad["pm25_manana"], con_verdad["pm25_predicho"]); prueba[prueba["fecha"].dt.month <= 9].',
  None),

 ("## 6. *Drift*: ¿los datos de entrada cambiaron?",
  "El desempeño se mide con días de atraso; los **datos de entrada** se pueden vigilar el mismo "
  "día. Un cambio en la distribución de la entrada se llama ***drift***. El más básico y el más "
  "olvidado: la **proporción de faltantes**. Si una estación deja de reportar, el modelo no "
  "puede predecir para ella, aunque «el sistema funcione».",
  "Compara faltantes (y niveles) entre historia y 2026",
  '''falt_hist = historia["pm25"].isna().groupby(historia["estacion"]).mean()
falt_2026 = nuevos["pm25"].isna().groupby(nuevos["estacion"]).mean()
hist_ene_sep = historia[historia["fecha"].dt.month <= 9]
drift = pd.DataFrame({
    "faltantes_historia": falt_hist,
    "faltantes_2026": falt_2026,
    "media_historia_ene_sep": hist_ene_sep.groupby("estacion")["pm25"].mean(),
    "media_2026": nuevos.groupby("estacion")["pm25"].mean(),
}).round(3)
estaciones_alerta = sorted(drift[drift["faltantes_2026"] > 0.20].index)
print(drift.sort_values("faltantes_2026", ascending=False))
print("\\nEstaciones con más de 20% de días sin dato en 2026:", estaciones_alerta)''',
  '''falt_hist = historia["pm25"].isna().groupby(historia["estacion"]).mean()
# TODO: la misma proporción de faltantes, por estación, en los datos nuevos (2026)
falt_2026 = ...
# TODO: lista ORDENADA (sorted) de estaciones cuyo faltantes_2026 supera 0.20
estaciones_alerta = ...
print("faltantes historia:", falt_hist.round(3).to_dict())
print("Estaciones en alerta:", estaciones_alerta)''',
  '''_esp = nuevos["pm25"].isna().groupby(nuevos["estacion"]).mean()
assert np.allclose(pd.Series(falt_2026).reindex(_esp.index).astype(float).values, _esp.values, atol=1e-3), "falt_2026 no calza: proporción de pm25 nulo por estación en `nuevos`"
assert list(estaciones_alerta) == sorted(_esp[_esp > 0.20].index), "revisa el umbral (> 0.20) y ordena con sorted"''',
  'nuevos["pm25"].isna().groupby(nuevos["estacion"]).mean(); luego sorted(falt_2026[falt_2026 > 0.20].index).',
  None),

 ("## 7. La ficha del modelo (*model card*)",
  "Un modelo desplegado sin documentación es una caja negra con consecuencias. La **ficha de "
  "modelo** dice qué hace, con qué datos, cuánto se equivoca (con números **verificados**), "
  "**para qué NO usarlo** y quién responde. Honestidad ante todo: si apenas le gana a la línea "
  "base, se dice.",
  "Completa la ficha con los números reales",
  '''ficha = {
    "nombre": "Pronóstico de PM2.5 del día siguiente por estación",
    "version": "1.0 — entrenado con 2020–2024, probado con 2025",
    "uso_previsto": "Apoyo a equipos de gestión ambiental para anticipar días de mala calidad del aire, con revisión humana.",
    "no_usar_para": "Decretar episodios o restricciones de forma automática; no reemplaza el pronóstico oficial.",
    "datos": "SINCA: PM2.5 diario de 14 estaciones (2020–2025). Producción: ene–sep 2026.",
    "mae_prueba": round(mae_prueba, 2),
    "mae_linea_base": round(mae_ingenuo_prueba, 2),
    "mae_2026": round(mae_2026, 2),
    "limitaciones": "Solo usa el PM2.5 reciente y el mes (sin meteorología: la miden 7 de 14 estaciones); "
                    "le gana por poco a 'mañana = hoy'; no predice si falta el dato de hoy o ayer.",
    "monitoreo": "MAE mensual vs prueba de los mismos meses; faltantes por estación. "
                 f"En 2026 con >20% de faltantes: {', '.join(estaciones_alerta)}.",
    "responsable": "Equipo de datos (completa con el nombre real)",
}
from IPython.display import Markdown, display
display(Markdown("\\n".join(f"- **{k}:** {v}" for k, v in ficha.items())))''',
  '''ficha = {
    "nombre": "Pronóstico de PM2.5 del día siguiente por estación",
    "version": "1.0 — entrenado con 2020–2024, probado con 2025",
    "uso_previsto": ...,      # TODO: para qué y para quién (con revisión humana)
    "no_usar_para": ...,      # TODO: qué decisiones NO debe tomar este modelo
    "datos": "SINCA: PM2.5 diario de 14 estaciones (2020–2025). Producción: ene–sep 2026.",
    "mae_prueba": ...,        # TODO: round(mae_prueba, 2)
    "mae_linea_base": round(mae_ingenuo_prueba, 2),
    "mae_2026": ...,          # TODO: round(mae_2026, 2)
    "limitaciones": ...,      # TODO: qué no sabe hacer, con honestidad
    "monitoreo": "MAE mensual vs prueba de los mismos meses; faltantes por estación.",
    "responsable": "Equipo de datos (completa con el nombre real)",
}
from IPython.display import Markdown, display
display(Markdown("\\n".join(f"- **{k}:** {v}" for k, v in ficha.items())))''',
  '''_claves = {"nombre", "uso_previsto", "no_usar_para", "datos", "mae_prueba", "mae_linea_base",
           "mae_2026", "limitaciones", "monitoreo", "responsable"}
assert _claves <= set(ficha), f"faltan claves: {_claves - set(ficha)}"
for _k in ["uso_previsto", "no_usar_para", "limitaciones"]:
    assert isinstance(ficha[_k], str) and len(ficha[_k]) > 15, f"escribe '{_k}' con una frase real"
assert abs(ficha["mae_prueba"] - mae_prueba) < 0.01
assert abs(ficha["mae_2026"] - mae_2026) < 0.01''',
  "Reemplaza cada ... por una frase (texto entre comillas) o por round(mae_prueba, 2) y round(mae_2026, 2).",
  None),
]

GRADIO_MD = '''## 8. (Opcional) Una interfaz para personas: Gradio

`predecir_seguro` es **exactamente** lo que envuelven las formas más avanzadas de despliegue: una
API web (FastAPI/Flask) o una app sencilla con **Gradio**, como la de R1-09. En Colab, instala
con `!pip -q install gradio` y descomenta `demo.launch(share=True)`. La celda está protegida para
no bloquear el cuaderno si Gradio no está instalado.'''

GRADIO_CELL = '''# ── App Gradio (opcional; en Colab) ──────────────────────────────────────────
try:
    import gradio as gr

    def app(estacion, pm25_hoy, pm25_ayer, media_7d, mes):
        r = predecir_seguro(estacion, pm25_hoy, pm25_ayer, media_7d, int(mes))
        if not r["ok"]:
            return "⚠️ " + r["error"]
        aviso = " — sobre la norma diaria (50 µg/m³)" if r["pm25_manana"] > 50 else ""
        return f"PM2.5 estimado para mañana: {r['pm25_manana']} µg/m³{aviso}"

    demo = gr.Interface(
        app,
        [gr.Dropdown(ESTACIONES, value="Cerro Navia", label="Estación"),
         gr.Number(value=40, label="PM2.5 hoy (µg/m³)"),
         gr.Number(value=35, label="PM2.5 ayer (µg/m³)"),
         gr.Number(value=30, label="Media últimos 7 días (µg/m³)"),
         gr.Slider(1, 12, value=6, step=1, label="Mes")],
        gr.Text(label="Pronóstico"),
        title="Pronóstico de PM2.5 del día siguiente (uso interno, con revisión humana)",
    )
    # demo.launch(share=True)   # ← descomenta en Colab para obtener un link
    print("✔ App Gradio construida. En Colab ejecuta: demo.launch(share=True)")
except ModuleNotFoundError:
    print("ℹ Gradio no está instalado aquí. En Colab corre primero:  !pip -q install gradio")
except Exception as e:
    print("ℹ La app no se construyó (¿completaste los ejercicios 1 y 2?):", e)'''

CIERRE = '''## Cierre

- Desplegar = **cargar el artefacto** + una **función de predicción** + **validar la entrada** +
  **puntuar lotes** + **entregar un archivo** que otro pueda usar.
- En producción **no se inventa**: las filas con datos faltantes se marcan y se cuentan
  (en 2026, una de cada ~7 filas no se pudo predecir, concentradas en 4 estaciones).
- **Monitorear** es comparar con justicia: la misma época del año y contra la línea base. El
  MAE de 2026 es mayor que el de la prueba 2025 completa, pero buena parte se explica porque
  enero–septiembre incluye el invierno.
- El ***drift* de faltantes** se vigila el mismo día; el desempeño, con días de atraso.
- La **ficha de modelo** acompaña al modelo siempre: qué hace, cuánto se equivoca, para qué NO
  usarlo y quién responde.

> *Ética distribuida:* un pronóstico de calidad del aire puede mover decisiones que afectan la
> salud de la gente. Por eso «con revisión humana» no es una frase de relleno en la ficha: es el
> diseño. *En la profundización verás **dónde** se degrada el modelo (y por qué) y cómo elegir
> un **umbral de alerta**.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-09", "Despliegue, ficha de modelo y monitoreo", "R2", "Científico de Datos", "15",
                      ["Convertir un modelo guardado en una **función de predicción** con **validación de entrada**.",
                       "**Puntuar por lotes** datos nuevos con **faltantes reales** sin inventar predicciones.",
                       "**Monitorear** el desempeño en producción y el ***drift*** de los datos de entrada.",
                       "Documentar el modelo en una **ficha de modelo** honesta."],
                      "dejar un modelo usable y vigilado: predicción en línea y por lotes, entregable, monitoreo y ficha.",
                      "PM2.5 diario de 14 estaciones SINCA (2020–2025) y sus datos nuevos de 2026 como «producción».",
                      n_checks=len(EJ)),
        h.code(SETUP),
        h.md(INTRO),
        h.md(MODELO_MD),
        h.code(MODELO),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(GRADIO_MD))
    cells.append(h.code(GRADIO_CELL))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización ───────────────────────────────────────────────────────────
PROF_PREP = f'''# Reconstruye el modelo y sus predicciones (misma receta que la lección; tarda unos segundos)
import os, urllib.request
import numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, recall_score, precision_score

for archivo in ["aire_diario.csv", "aire_nuevos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)
historia = pd.read_csv("aire_diario.csv", parse_dates=["fecha"])
nuevos = pd.read_csv("aire_nuevos.csv", parse_dates=["fecha"])

FEATURES = ["estacion", "pm25_hoy", "pm25_ayer", "media_7d", "mes"]
OBJETIVO = "pm25_manana"

def construir_features(df):
    partes = []
    for estacion, d in df.groupby("estacion"):
        d = d.set_index("fecha").sort_index().asfreq("D")
        d["estacion"] = estacion
        d["pm25_hoy"] = d["pm25"]
        d["pm25_ayer"] = d["pm25"].shift(1)
        d["media_7d"] = d["pm25"].rolling(7, min_periods=5).mean()
        d["mes"] = d.index.month
        d["pm25_manana"] = d["pm25"].shift(-1)
        partes.append(d.reset_index())
    return pd.concat(partes, ignore_index=True)

todo = construir_features(pd.concat([historia, nuevos], ignore_index=True))
completo = todo[FEATURES + [OBJETIVO]].notna().all(axis=1)
entrenamiento = todo[(todo["fecha"] < "2025-01-01") & completo]
prueba = todo[(todo["fecha"].dt.year == 2025) & completo].copy()
prod = todo[(todo["fecha"] >= "2026-01-01") & completo].copy()   # 2026 con predicción y dato real

pre = ColumnTransformer([("est", OneHotEncoder(handle_unknown="ignore"), ["estacion"])], remainder="passthrough")
modelo = Pipeline([("pre", pre), ("bosque", RandomForestRegressor(n_estimators=100, min_samples_leaf=10,
                                                                  random_state=42, n_jobs=-1))])
modelo.fit(entrenamiento[FEATURES], entrenamiento[OBJETIVO])
prueba["pred"] = modelo.predict(prueba[FEATURES])
prod["pred"] = modelo.predict(prod[FEATURES])
print("prueba 2025:", len(prueba), "filas · producción 2026:", len(prod), "filas")'''

PROF_EJ = [
 ("## 1. Monitoreo por estación: ¿dónde se degrada?",
  "El MAE global esconde diferencias. Calcula el MAE **por estación** en la prueba 2025 y en "
  "2026, y la razón `2026 / prueba`. Una razón cercana a 1 = estable; muy sobre 1 = se degradó.",
  "Tabla de MAE por estación y la peor",
  '''def mae_por_estacion(d):
    return (d["pred"] - d[OBJETIVO]).abs().groupby(d["estacion"]).mean()

por_estacion = pd.DataFrame({"mae_prueba": mae_por_estacion(prueba), "mae_2026": mae_por_estacion(prod)})
por_estacion["razon"] = por_estacion["mae_2026"] / por_estacion["mae_prueba"]
peor_estacion = por_estacion["razon"].idxmax()
print(por_estacion.round(2).sort_values("razon", ascending=False).head(5))
print("Peor estación:", peor_estacion)''',
  '''def mae_por_estacion(d):
    # TODO: error absoluto |pred - real| promediado por estación
    return ...

# TODO: DataFrame con columnas "mae_prueba" (de `prueba`) y "mae_2026" (de `prod`),
#       más la columna "razon" = mae_2026 / mae_prueba
por_estacion = ...
# TODO: la estación con la mayor razón
peor_estacion = ...
print("Peor estación:", peor_estacion)''',
  '''_m = (prod["pred"] - prod[OBJETIVO]).abs().groupby(prod["estacion"]).mean()
assert np.allclose(por_estacion["mae_2026"].astype(float).values, _m.reindex(por_estacion.index).values)
assert peor_estacion == por_estacion["razon"].astype(float).idxmax()''',
  '(d["pred"] - d[OBJETIVO]).abs().groupby(d["estacion"]).mean(); la peor con .idxmax().'),

 ("## 2. ¿Por qué? Revisa qué midió la prueba",
  "Antes de culpar al modelo, mira **qué contenía la prueba** para esa estación. El PM2.5 de "
  "Santiago se dispara en invierno (mayo–agosto). Cuenta, por estación, cuántos días de "
  "**invierno** tuvo la prueba 2025. Si una estación no tiene invierno en la prueba, su MAE "
  "de prueba solo midió los meses fáciles.",
  "Días de invierno evaluados en la prueba",
  '''invierno = prueba["fecha"].dt.month.between(5, 8)
dias_invierno_prueba = invierno.groupby(prueba["estacion"]).sum()
sin_invierno = sorted(dias_invierno_prueba[dias_invierno_prueba == 0].index)
print(dias_invierno_prueba.sort_values().head(4))
print("Estaciones SIN invierno en la prueba 2025:", sin_invierno)''',
  '''invierno = prueba["fecha"].dt.month.between(5, 8)      # True si el día es de mayo a agosto
# TODO: suma de días de invierno por estación (groupby sobre prueba["estacion"])
dias_invierno_prueba = ...
# TODO: lista ordenada de estaciones con 0 días de invierno en la prueba
sin_invierno = ...
print("Estaciones SIN invierno en la prueba 2025:", sin_invierno)''',
  '''_d = prueba["fecha"].dt.month.between(5, 8).groupby(prueba["estacion"]).sum()
assert list(sin_invierno) == sorted(_d[_d == 0].index)
assert peor_estacion in sin_invierno, "¿coincide con la peor estación del ejercicio 1?"''',
  'invierno.groupby(prueba["estacion"]).sum(); luego sorted(dias_invierno_prueba[dias_invierno_prueba == 0].index).'),

 ("## 3. De pronóstico a alerta: el umbral ingenuo",
  "Un uso práctico: **alertar** cuando el pronóstico supera la norma diaria de PM2.5 "
  "(50 µg/m³, D.S. 12/2011 del MMA). Mide en la **prueba 2025** qué fracción de los días que "
  "realmente superaron la norma fue alertada (*recall*) y qué fracción de las alertas fue "
  "correcta (*precision*).",
  "Recall y precision del umbral 50",
  '''real_prueba = prueba[OBJETIVO] > 50
alerta_50 = prueba["pred"] >= 50
recall_50 = recall_score(real_prueba, alerta_50)
precision_50 = precision_score(real_prueba, alerta_50)
print(f"Días sobre la norma en 2025: {real_prueba.sum()} · recall {recall_50:.2f} · precision {precision_50:.2f}")''',
  '''real_prueba = prueba[OBJETIVO] > 50          # días que de verdad superaron la norma
# TODO: alerta cuando la predicción es >= 50
alerta_50 = ...
recall_50 = ...       # TODO: recall_score(real, alerta)
precision_50 = ...    # TODO: precision_score(real, alerta)
print("recall:", recall_50, "| precision:", precision_50)''',
  '''_a = prueba["pred"] >= 50
assert abs(recall_50 - recall_score(prueba[OBJETIVO] > 50, _a)) < 1e-9
assert abs(precision_50 - precision_score(prueba[OBJETIVO] > 50, _a)) < 1e-9''',
  'alerta_50 = prueba["pred"] >= 50; recall_score(real_prueba, alerta_50); precision_score(real_prueba, alerta_50).'),

 ("## 4. Elegir el umbral con 2025, evaluarlo con 2026",
  "Un umbral de 50 deja pasar muchos días sobre la norma: el modelo tiende a **suavizar los "
  "picos**. Para la salud, perder un episodio es peor que una falsa alarma. Elige el umbral "
  "**más alto** (entre 20 y 50) que logre **recall ≥ 0,80 en 2025** — y **recién después** mira "
  "cómo se comporta en 2026. Elegir el umbral mirando 2026 sería hacer trampa.",
  "Umbral de alerta validado",
  '''candidatos = range(20, 51)
recall_por_umbral = {u: recall_score(real_prueba, prueba["pred"] >= u) for u in candidatos}
umbral = max(u for u, r in recall_por_umbral.items() if r >= 0.80)
real_2026 = prod[OBJETIVO] > 50
alerta_2026 = prod["pred"] >= umbral
recall_2026 = recall_score(real_2026, alerta_2026)
precision_2026 = precision_score(real_2026, alerta_2026)
print(f"Umbral elegido en 2025: {umbral} µg/m³")
print(f"En 2026: {real_2026.sum()} días sobre la norma · recall {recall_2026:.2f} · precision {precision_2026:.2f} · alertas {alerta_2026.sum()}")''',
  '''candidatos = range(20, 51)
# TODO: recall en la PRUEBA 2025 para cada umbral candidato (diccionario umbral → recall)
recall_por_umbral = ...
# TODO: el umbral MÁS ALTO con recall >= 0.80
umbral = ...
real_2026 = prod[OBJETIVO] > 50
# TODO: aplica ese umbral a 2026 y calcula recall y precision
recall_2026 = ...
precision_2026 = ...
print("umbral:", umbral, "| recall 2026:", recall_2026, "| precision 2026:", precision_2026)''',
  '''_r = {u: recall_score(prueba[OBJETIVO] > 50, prueba["pred"] >= u) for u in range(20, 51)}
_u = max(u for u, r in _r.items() if r >= 0.80)
assert umbral == _u, f"el umbral elegido con 2025 debería ser {_u}"
assert abs(recall_2026 - recall_score(prod[OBJETIVO] > 50, prod["pred"] >= _u)) < 1e-9
assert abs(precision_2026 - precision_score(prod[OBJETIVO] > 50, prod["pred"] >= _u)) < 1e-9''',
  '{u: recall_score(real_prueba, prueba["pred"] >= u) for u in candidatos}; luego max(u for u, r in ... if r >= 0.80).'),
]

PROF_HEADER = '''# R2-09 · Despliegue y monitoreo — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional. Dos preguntas que todo equipo se hace cuando el modelo ya está andando:

1. **¿Dónde se degrada y por qué?** — monitoreo **por estación** (spoiler: una estación «se
   degradó» porque su prueba nunca vio el invierno).
2. **¿Cuándo alertar?** — convertir el pronóstico en **alerta**, eligiendo el umbral con 2025 y
   evaluándolo honestamente en 2026.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_CIERRE = '''## Para llevar

- Una estación que «se degrada» puede ser una **prueba que no representaba** su realidad: El
  Bosque no reportó entre abril de 2025 y abril de 2026, así que su MAE de prueba solo midió
  verano. **Monitorear también es auditar la prueba.**
- Un umbral de alerta es una **decisión de política**, no un detalle técnico: cambia cuántos
  episodios se pierden y cuántas falsas alarmas se aceptan. Se elige con datos de validación y
  se **declara** en la ficha.

---

*Fin de la profundización de R2-09.*'''


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


README = '''# R2-09 · Despliegue, ficha de modelo y monitoreo

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-09-despliegue-de-modelos/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Un modelo en un cuaderno no le sirve a nadie. Se reconstruye un **pronóstico de PM2.5 del día
siguiente** (14 estaciones SINCA, `aire_diario.csv` 2020–2025), se guarda con `joblib` y se
**despliega**: función de predicción con **validación de entrada**, **puntuación por lotes** con
faltantes reales, **entregable CSV**, y luego se pone en **producción** sobre `aire_nuevos.csv`
(enero–septiembre de 2026, datos que el modelo nunca vio): **monitoreo** de desempeño con
comparación justa, ***drift*** de faltantes y **ficha de modelo** honesta. Interfaz Gradio opcional.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: monitoreo **por estación** (dónde se degrada y por qué) y
  **umbral de alerta** elegido en 2025 y evaluado en 2026.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
- El cuaderno crea `modelo_pm25.joblib` y `predicciones_pm25_2026.csv` en la carpeta de trabajo
  (no se versionan).
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
