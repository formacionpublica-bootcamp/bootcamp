"""build_R2-10.py — módulo R2-10 (Series temporales, optativo).

Rama R2 (Científico de Datos). Rearmado 2026: se reemplaza la serie anual anterior
por datos diarios. Lección = PM2.5 diario de Cerro Navia (SINCA, 2020–2025): serie con
calendario completo, remuestreo semanal/mensual, media móvil, estacionalidad anual
y semanal, descomposición, validación temporal (ingenuo, ingenuo estacional,
promedio estacional, regresión mes+tendencia) y prueba de fuego contra enero–
septiembre de 2026 (aire_nuevos.csv). Conserva el arco del módulo anterior:
construir la serie → describirla → pronósticos base → validar escondiendo el
último período → pronosticar el siguiente con honestidad.
Profundiza = transferencia honesta: sismos USGS M≥4,5 agregados a conteo mensual —
¿hay estacionalidad? (No: el chi-cuadrado ingenuo se deja engañar por las réplicas;
la permutación por meses no encuentra evidencia.)

Uso:  /opt/anaconda3/bin/python tools/build_R2-10.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-10-series-temporales")

RAW = h.REPO_RAW

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# "En vivo o caché": usa los archivos locales; si faltan (ej. Colab), se bajan del repo.
for archivo in ["aire_diario.csv", "aire_nuevos.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)

aire = pd.read_csv("aire_diario.csv", parse_dates=["fecha"])     # 2020–2025, 14 estaciones
nuevos = pd.read_csv("aire_nuevos.csv", parse_dates=["fecha"])   # ene–sep 2026: el futuro "real"
ESTACION = "Cerro Navia"                                          # comuna de Cerro Navia, Región Metropolitana
print("Datos:", aire.shape, "| estaciones:", aire["estacion"].nunique())
aire[aire["estacion"] == ESTACION].head(3)'''

INTRO = '''## ¿Qué es una serie temporal?

Una **serie temporal** es una secuencia de valores **ordenados en el tiempo** y medidos a
intervalos regulares: el PM2.5 de cada día, las solicitudes de cada semana, las atenciones de
cada mes. La palabra clave es *ordenados*: si desordenas las filas, pierdes lo más valioso — si
venía subiendo, si cada invierno se dispara, hacia dónde apunta. **La fila de al lado importa.**

Casi cualquier serie se puede pensar como la suma de tres ingredientes:

1. **Tendencia:** hacia dónde va a largo plazo (¿el aire de Santiago mejora año a año?).
2. **Estacionalidad:** patrones que se **repiten** en ciclos fijos. En el PM2.5 de Santiago, el
   invierno es inconfundible: frío, poca ventilación y calefacción. Con datos **diarios** también
   podemos buscar un ciclo **semanal**.
3. **Ruido:** lo que queda. Ningún pronóstico lo elimina; un buen análisis no lo confunde con señal.

Hoy trabajamos con el PM2.5 diario de la estación **Cerro Navia** (2020–2025) y, al final, lo
ponemos a prueba contra lo que **de verdad pasó** en 2026.

> Norma chilena de PM2.5 para 24 horas: **50 µg/m³** (D.S. 12/2011 del Ministerio del Medio Ambiente).'''

EJ = [
 ("## 1. Construir la serie: el tiempo como índice",
  "El primer paso siempre es el mismo: quedarte con una estación, dejar la **fecha como índice** "
  "y exigir un **calendario completo** con `.asfreq(\"D\")`. Si falta un día, debe aparecer como "
  "`NaN` — no desaparecer. Una serie con días «saltados» engaña a todo lo que viene después "
  "(medias móviles, desfases, pronósticos).",
  "Arma la serie diaria y cuenta los días sin dato",
  '''pm = (aire[aire["estacion"] == ESTACION]
        .set_index("fecha")["pm25"]
        .sort_index()
        .asfreq("D"))
n_dias = len(pm)
n_faltantes = int(pm.isna().sum())
print("días:", n_dias, "| sin dato:", n_faltantes, f"({100 * n_faltantes / n_dias:.1f}%)")
print(pm.index.min().date(), "→", pm.index.max().date())''',
  '''# TODO: filtra ESTACION, deja "fecha" como índice, toma "pm25", ordena y fuerza frecuencia diaria
pm = ...
n_dias = ...        # TODO: largo de la serie
n_faltantes = ...   # TODO: días con pm25 nulo
print("días:", n_dias, "| sin dato:", n_faltantes)''',
  '''assert isinstance(pm, pd.Series) and isinstance(pm.index, pd.DatetimeIndex)
assert pm.index.freqstr == "D", "usa .asfreq('D') para tener un calendario completo"
assert n_dias == len(pm) == (pm.index.max() - pm.index.min()).days + 1
assert n_faltantes == int(pm.isna().sum()) and n_faltantes > 0''',
  'aire[aire["estacion"] == ESTACION].set_index("fecha")["pm25"].sort_index().asfreq("D"); len(pm) y pm.isna().sum().',
  None),

 ("## 2. Cambiar la escala del tiempo: remuestreo y media móvil",
  "El dato diario es ruidoso. Dos herramientas para ver la forma:\n\n"
  "- **Remuestrear** (`resample`): pasar de días a semanas (`\"W\"`) o meses (`\"MS\"`, inicio de "
  "mes), promediando. Es la tabla dinámica del tiempo.\n"
  "- **Media móvil** (`rolling`): el promedio de los últimos 30 días, recalculado cada día. "
  "Suaviza sin cambiar la frecuencia. Con `min_periods=20` exigimos al menos 20 días con dato.",
  "Serie semanal, mensual y media móvil de 30 días",
  '''semanal = pm.resample("W").mean()
mensual = pm.resample("MS").mean()
movil_30 = pm.rolling(30, min_periods=20).mean()
print("semanas:", len(semanal), "| meses:", len(mensual))
print("mes más alto del período:", mensual.idxmax().strftime("%Y-%m"), f"({mensual.max():.1f} µg/m³)")''',
  '''# TODO: promedio semanal ("W") y mensual ("MS") con resample
semanal = ...
mensual = ...
# TODO: media móvil de 30 días con al menos 20 días con dato
movil_30 = ...
print("semanas:", len(semanal) if hasattr(semanal, "__len__") else semanal)''',
  '''assert len(mensual) == 72 and abs(mensual.iloc[0] - pm["2020-01"].mean()) < 1e-9
assert len(semanal) == len(pm.resample("W").mean())
assert np.allclose(movil_30.dropna().values, pm.rolling(30, min_periods=20).mean().dropna().values)''',
  'pm.resample("W").mean(), pm.resample("MS").mean() y pm.rolling(30, min_periods=20).mean().',
  '''# Las tres escalas en un gráfico
try:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(pm.index, pm.values, color="#c9c9d6", lw=0.6, label="diario")
    ax.plot(movil_30.index, movil_30.values, color="#4240e5", lw=1.6, label="media móvil 30 días")
    ax.plot(mensual.index, mensual.values, "o", color="#ff6b35", ms=3, label="promedio mensual")
    ax.axhline(50, color="crimson", ls="--", lw=1, label="norma 24 h (50 µg/m³)")
    ax.set_ylim(bottom=0); ax.set_ylabel("PM2.5 (µg/m³)"); ax.set_title(f"PM2.5 en {ESTACION}, 2020–2025")
    ax.legend(loc="upper right", fontsize=8); plt.tight_layout(); plt.show()
except Exception as e:
    print("Completa el ejercicio 2 para ver el gráfico.", e)'''),

 ("## 3. Estacionalidad: el año y la semana",
  "¿Cuánto pesa el invierno? Promedia el PM2.5 por **mes del calendario** (todos los eneros "
  "juntos, todos los febreros juntos…). Luego haz lo mismo por **día de la semana** "
  "(`dayofweek`: 0 = lunes … 6 = domingo) y compara fines de semana con días hábiles.",
  "Perfil mensual y semanal",
  '''perfil_mes = pm.groupby(pm.index.month).mean()
mes_peak = int(perfil_mes.idxmax())
razon_invierno_verano = perfil_mes.max() / perfil_mes.min()
perfil_semana = pm.groupby(pm.index.dayofweek).mean()
dif_fin_de_semana = pm[pm.index.dayofweek >= 5].mean() - pm[pm.index.dayofweek < 5].mean()
print(perfil_mes.round(1).to_dict())
print(f"Mes más alto: {mes_peak} · el peor mes promedia {razon_invierno_verano:.1f} veces el mejor")
print(f"Fin de semana vs hábil: {dif_fin_de_semana:+.1f} µg/m³")''',
  '''# TODO: promedio por mes del calendario (pm.index.month)
perfil_mes = ...
mes_peak = ...                  # TODO: el mes con el mayor promedio (idxmax)
razon_invierno_verano = ...     # TODO: máximo / mínimo del perfil mensual
# TODO: promedio sábado-domingo (dayofweek >= 5) menos promedio lunes-viernes
dif_fin_de_semana = ...
print("mes peak:", mes_peak, "| fin de semana - hábil:", dif_fin_de_semana)''',
  '''_p = pm.groupby(pm.index.month).mean()
assert mes_peak == int(_p.idxmax())
assert abs(razon_invierno_verano - _p.max() / _p.min()) < 1e-9
assert abs(dif_fin_de_semana - (pm[pm.index.dayofweek >= 5].mean() - pm[pm.index.dayofweek < 5].mean())) < 1e-9''',
  'pm.groupby(pm.index.month).mean(); .idxmax(); pm[pm.index.dayofweek >= 5].mean() - pm[pm.index.dayofweek < 5].mean().',
  None),

 ("## 4. Descomposición: tendencia + estacionalidad + resto",
  "`seasonal_decompose` separa la serie **mensual** en sus tres ingredientes (con `period=12`: el "
  "ciclo se repite cada 12 meses). La **amplitud estacional** (máximo − mínimo del componente "
  "estacional) dice cuánto mueve el calendario; el cambio de la **tendencia** dice si el aire "
  "mejora o empeora de fondo.",
  "Descompón la serie mensual",
  '''from statsmodels.tsa.seasonal import seasonal_decompose
desc = seasonal_decompose(mensual, model="additive", period=12)
amplitud_estacional = desc.seasonal.max() - desc.seasonal.min()
tendencia = desc.trend.dropna()
cambio_tendencia = tendencia.iloc[-1] - tendencia.iloc[0]
print(f"Amplitud estacional: {amplitud_estacional:.1f} µg/m³")
print(f"Tendencia: {tendencia.iloc[0]:.1f} ({tendencia.index[0]:%Y-%m}) → {tendencia.iloc[-1]:.1f} ({tendencia.index[-1]:%Y-%m})")''',
  '''from statsmodels.tsa.seasonal import seasonal_decompose
# TODO: descompón `mensual` (aditivo, period=12)
desc = ...
amplitud_estacional = ...   # TODO: desc.seasonal.max() - desc.seasonal.min()
cambio_tendencia = ...      # TODO: último menos primer valor de desc.trend (sin NaN)
print("amplitud:", amplitud_estacional, "| cambio de tendencia:", cambio_tendencia)''',
  '''_d = seasonal_decompose(mensual, model="additive", period=12)
assert abs(amplitud_estacional - (_d.seasonal.max() - _d.seasonal.min())) < 1e-6
_t = _d.trend.dropna()
assert abs(cambio_tendencia - (_t.iloc[-1] - _t.iloc[0])) < 1e-6''',
  'seasonal_decompose(mensual, model="additive", period=12); desc.trend.dropna() y luego .iloc[-1] - .iloc[0].',
  '''try:
    desc.plot(); plt.gcf().set_size_inches(9, 6); plt.tight_layout(); plt.show()
except Exception as e:
    print("Completa el ejercicio 4 para ver la descomposición.", e)'''),

 ("## 5. Validación temporal: tres pronósticos base",
  "La regla de oro: **nunca evalúes un pronóstico con los datos que usaste para construirlo**. "
  "En series temporales eso significa **esconder el final**: entrenamos con los meses de "
  "2020–2024 y pronosticamos los 12 meses de 2025 como si no los conociéramos. Nada de barajar.\n\n"
  "Tres pronósticos base, de más tonto a menos:\n\n"
  "- **Ingenuo:** todos los meses de 2025 = el último mes conocido (diciembre 2024).\n"
  "- **Ingenuo estacional:** cada mes de 2025 = el mismo mes de 2024.\n"
  "- **Promedio estacional:** cada mes de 2025 = el promedio de ese mes en 2020–2024.\n\n"
  "Error: **MAE** (error absoluto medio, en µg/m³).",
  "Pronostica 2025 con los tres métodos y mide el error",
  '''entrena = mensual[:"2024"]
real_2025 = mensual["2025"]
pron = {
    "ingenuo": pd.Series(entrena.iloc[-1], index=real_2025.index),
    "ingenuo_estacional": pd.Series(entrena["2024"].values, index=real_2025.index),
    "promedio_estacional": pd.Series(entrena.groupby(entrena.index.month).mean().values, index=real_2025.index),
}
errores = {k: float((p - real_2025).abs().mean()) for k, p in pron.items()}
print({k: round(v, 2) for k, v in errores.items()})''',
  '''entrena = mensual[:"2024"]          # 60 meses: 2020–2024
real_2025 = mensual["2025"]          # 12 meses escondidos
pron = {
    "ingenuo": pd.Series(entrena.iloc[-1], index=real_2025.index),
    # TODO: los 12 valores de 2024, con el índice de 2025
    "ingenuo_estacional": ...,
    # TODO: el promedio de cada mes del calendario en `entrena`, con el índice de 2025
    "promedio_estacional": ...,
}
# TODO: MAE de cada pronóstico contra real_2025 → diccionario {nombre: error}
errores = ...
print(errores)''',
  '''_e = mensual[:"2024"]; _r = mensual["2025"]
_esp = {"ingenuo": abs(_e.iloc[-1] - _r).mean(),
        "ingenuo_estacional": np.abs(_e["2024"].values - _r.values).mean(),
        "promedio_estacional": np.abs(_e.groupby(_e.index.month).mean().values - _r.values).mean()}
for _k, _v in _esp.items():
    assert abs(errores[_k] - _v) < 1e-6, f"el error de '{_k}' no calza"''',
  'pd.Series(entrena["2024"].values, index=real_2025.index); entrena.groupby(entrena.index.month).mean().values; '
  '{k: float((p - real_2025).abs().mean()) for k, p in pron.items()}.',
  None),

 ("## 6. Un modelo simple: mes + tendencia",
  "¿Le gana un modelo a los métodos base? Uno muy simple: una **regresión lineal** con 12 "
  "columnas 0/1 (una por mes) más una columna de **tiempo** (años desde enero de 2020). Captura "
  "la estacionalidad **y** la tendencia de fondo. La función que arma esas columnas ya está "
  "escrita; tú entrenas, pronosticas 2025 y eliges al ganador.",
  "Entrena la regresión y elige el mejor método",
  '''from sklearn.linear_model import LinearRegression

def X_mes_tendencia(idx):
    meses = np.eye(12)[idx.month - 1]                                    # 12 columnas 0/1
    t = ((idx.year - 2020) * 12 + idx.month - 1).to_numpy().reshape(-1, 1) / 12   # años desde ene-2020
    return np.hstack([meses, t])

reg = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(entrena.index), entrena.values)
pron["regresion"] = pd.Series(reg.predict(X_mes_tendencia(real_2025.index)), index=real_2025.index)
errores["regresion"] = float((pron["regresion"] - real_2025).abs().mean())
mejor_metodo = min(errores, key=errores.get)
print({k: round(v, 2) for k, v in errores.items()})
print(f"Tendencia estimada: {reg.coef_[-1]:+.2f} µg/m³ por año · mejor método en 2025: {mejor_metodo}")''',
  '''from sklearn.linear_model import LinearRegression

def X_mes_tendencia(idx):
    meses = np.eye(12)[idx.month - 1]                                    # 12 columnas 0/1
    t = ((idx.year - 2020) * 12 + idx.month - 1).to_numpy().reshape(-1, 1) / 12   # años desde ene-2020
    return np.hstack([meses, t])

# TODO: entrena LinearRegression(fit_intercept=False) con X_mes_tendencia(entrena.index) y entrena.values
reg = ...
# TODO: pronóstico de 2025 como Serie con el índice de real_2025, guárdalo en pron["regresion"]
# TODO: su MAE en errores["regresion"]
# TODO: el método con menor error
mejor_metodo = ...
print("mejor método:", mejor_metodo)''',
  '''_reg = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(mensual[:"2024"].index), mensual[:"2024"].values)
_p = _reg.predict(X_mes_tendencia(mensual["2025"].index))
assert "regresion" in errores and abs(errores["regresion"] - np.abs(_p - mensual["2025"].values).mean()) < 1e-6
assert mejor_metodo == min(errores, key=errores.get)''',
  'reg = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(entrena.index), entrena.values); '
  'pron["regresion"] = pd.Series(reg.predict(X_mes_tendencia(real_2025.index)), index=real_2025.index); '
  'mejor_metodo = min(errores, key=errores.get).',
  None),

 ("## 7. Prueba de fuego: lo que de verdad pasó en 2026",
  "Elegiste el método con 2025. Ahora, como en la vida real, lo **reentrenas con todo lo que "
  "sabes** (2020–2025) y lo enfrentas a enero–septiembre de 2026, que el modelo nunca vio "
  "(`nuevos`). Compáralo con el ingenuo estacional (cada mes de 2026 = el mismo mes de 2025). "
  "¿Se sostiene la elección?",
  "Evalúa contra enero–septiembre de 2026",
  '''real_2026 = (nuevos[nuevos["estacion"] == ESTACION]
             .set_index("fecha")["pm25"].sort_index().asfreq("D")
             .resample("MS").mean())
reg_total = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(mensual.index), mensual.values)
pron_2026 = pd.Series(reg_total.predict(X_mes_tendencia(real_2026.index)), index=real_2026.index)
ingenuo_est_2026 = pd.Series(mensual["2025"].values[:len(real_2026)], index=real_2026.index)
mae_2026_regresion = float((pron_2026 - real_2026).abs().mean())
mae_2026_ingenuo_est = float((ingenuo_est_2026 - real_2026).abs().mean())
print(pd.DataFrame({"real": real_2026, "regresion": pron_2026, "ingenuo_est": ingenuo_est_2026}).round(1))
print(f"MAE 2026 → regresión: {mae_2026_regresion:.2f} · ingenuo estacional: {mae_2026_ingenuo_est:.2f}")''',
  '''# TODO: serie mensual 2026 de ESTACION (misma receta del ejercicio 1 + resample("MS").mean())
real_2026 = ...
# TODO: reentrena la regresión con TODO `mensual` (2020–2025) y pronostica los meses de real_2026
reg_total = ...
pron_2026 = ...
ingenuo_est_2026 = ...      # TODO: los primeros len(real_2026) meses de 2025, con el índice de 2026
mae_2026_regresion = ...
mae_2026_ingenuo_est = ...
print("MAE 2026 regresión:", mae_2026_regresion, "| ingenuo estacional:", mae_2026_ingenuo_est)''',
  '''_r26 = nuevos[nuevos["estacion"] == ESTACION].set_index("fecha")["pm25"].sort_index().asfreq("D").resample("MS").mean()
assert len(real_2026) == len(_r26) == 9 and np.allclose(real_2026.values, _r26.values)
_rg = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(mensual.index), mensual.values)
assert abs(mae_2026_regresion - np.abs(_rg.predict(X_mes_tendencia(_r26.index)) - _r26.values).mean()) < 1e-6
assert abs(mae_2026_ingenuo_est - np.abs(mensual["2025"].values[:9] - _r26.values).mean()) < 1e-6''',
  'Repite la receta del ejercicio 1 sobre `nuevos` y agrega .resample("MS").mean(); '
  'reentrena con X_mes_tendencia(mensual.index), mensual.values; ingenuo: mensual["2025"].values[:len(real_2026)].',
  '''try:
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(mensual["2024":].index, mensual["2024":].values, color="#888", label="historia")
    ax.plot(real_2026.index, real_2026.values, "o-", color="black", label="real 2026")
    ax.plot(pron_2026.index, pron_2026.values, "s--", color="#4240e5", label="regresión")
    ax.plot(ingenuo_est_2026.index, ingenuo_est_2026.values, "^--", color="#ff6b35", label="ingenuo estacional")
    ax.set_ylim(bottom=0); ax.set_ylabel("PM2.5 mensual (µg/m³)"); ax.legend(fontsize=8)
    ax.set_title(f"{ESTACION}: pronósticos vs lo que pasó en 2026"); plt.tight_layout(); plt.show()
except Exception as e:
    print("Completa el ejercicio 7 para ver el gráfico.", e)'''),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

En 2025 ganó la regresión; en 2026, por poco, el ingenuo estacional. Julio de 2026 fue mucho
más limpio de lo habitual y **ningún** método lo anticipó. Si tu jefatura te pide «el pronóstico
de PM2.5 para el próximo invierno», ¿qué le entregas: un número, un rango, o dos métodos con su
historial de error? Escríbelo en dos frases.'''

CIERRE = '''## Cierre

- Una serie temporal necesita **calendario completo** (`asfreq`): los días sin dato se ven, no se saltan.
- **Remuestrear** y **media móvil** cambian la escala para ver la forma; la **descomposición**
  separa tendencia, estacionalidad y resto.
- En el PM2.5 de Cerro Navia, el **invierno** manda (el peor mes promedia casi 5 veces el mejor);
  el ciclo **semanal** existe pero es chico en comparación.
- **Validación temporal:** se esconde el final, nunca se baraja. El **ingenuo estacional** es la
  vara mínima: en esta serie, ganarle no es fácil.
- Un método que gana un año puede perder el siguiente: reporta el **error histórico**, no solo el número.

> *En la profundización aplicarás lo mismo a los **sismos**: ¿tienen temporada? La respuesta
> honesta es otra, y aprenderás a no dejarte engañar por un test mal elegido.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-10", "Series temporales", "R2", "Científico de Datos", "16 (optativa)",
                      ["Construir una **serie diaria** con calendario completo y contar sus huecos.",
                       "**Remuestrear** (semana, mes) y suavizar con **media móvil**.",
                       "Medir la **estacionalidad** anual y semanal y **descomponer** la serie.",
                       "Comparar pronósticos con **validación temporal** y probarlos contra **2026**."],
                      "dado un registro temporal real, describir su forma y producir un pronóstico validado que le gane (o no) a la línea base, y decirlo con honestidad.",
                      "PM2.5 diario de la estación Cerro Navia (SINCA, 2020–2025) y lo que pasó en enero–septiembre de 2026.",
                      n_checks=len(EJ)),
        h.code(SETUP),
        h.md(INTRO),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización: sismos ───────────────────────────────────────────────────
PROF_PREP = f'''import os, urllib.request
import numpy as np, pandas as pd
CSV = "sismos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)
sismos = pd.read_csv(CSV, parse_dates=["fecha"])   # USGS: sismos M≥4,5 en Chile, 2020–2025
print("sismos:", sismos.shape, sismos["fecha"].min().date(), "→", sismos["fecha"].max().date())
sismos.head(3)'''

PROF_EJ = [
 ("## 1. De eventos a serie: conteo mensual",
  "Un catálogo de sismos no es una serie temporal: es una lista de **eventos**. Se convierte en "
  "serie **contando** eventos por período. `resample(\"MS\").size()` cuenta por mes (y un mes sin "
  "sismos aparecería con 0, no desaparecería).\n\n"
  "Si los sismos ocurrieran al azar e independientes (proceso de Poisson), la **varianza** del "
  "conteo sería parecida a su **media**. Si la varianza es bastante mayor, los eventos vienen "
  "**en racimos**.",
  "Conteo mensual, media y razón varianza/media",
  '''conteo = sismos.set_index("fecha").resample("MS").size()
media_mensual = conteo.mean()
razon_var_media = conteo.var() / conteo.mean()
print("meses:", len(conteo), f"| media: {media_mensual:.1f} sismos/mes | varianza/media: {razon_var_media:.2f}")''',
  '''# TODO: número de sismos por mes (resample("MS").size() sobre la fecha como índice)
conteo = ...
media_mensual = ...     # TODO
razon_var_media = ...   # TODO: varianza / media del conteo
print("media:", media_mensual, "| varianza/media:", razon_var_media)''',
  '''_c = sismos.set_index("fecha").resample("MS").size()
assert len(conteo) == len(_c) == 72 and int(conteo.sum()) == len(sismos)
assert abs(razon_var_media - _c.var() / _c.mean()) < 1e-9''',
  'sismos.set_index("fecha").resample("MS").size(); conteo.var() / conteo.mean().'),

 ("## 2. El perfil por mes del calendario (y quién lo mueve)",
  "Igual que con el PM2.5: promedia el conteo por **mes del calendario**. Después busca el "
  "**día** con más sismos del catálogo: ¿cae en el mes «más sísmico»?",
  "Perfil mensual y día récord",
  '''perfil = conteo.groupby(conteo.index.month).mean()
mes_max = int(perfil.idxmax())
dia_record = sismos["fecha"].value_counts().idxmax()
print(perfil.round(1).to_dict())
print("Mes con más sismos en promedio:", mes_max)
print("Día récord:", dia_record.date(), "con", sismos["fecha"].value_counts().max(), "sismos")
print(sismos[sismos["fecha"] == dia_record].nlargest(3, "magnitud")[["magnitud", "lugar"]])''',
  '''# TODO: promedio del conteo por mes del calendario
perfil = ...
mes_max = ...      # TODO: el mes con el mayor promedio
# TODO: la fecha que más se repite en sismos["fecha"] (value_counts + idxmax)
dia_record = ...
print("mes máx:", mes_max, "| día récord:", dia_record)''',
  '''assert mes_max == int(conteo.groupby(conteo.index.month).mean().idxmax())
assert pd.Timestamp(dia_record) == sismos["fecha"].value_counts().idxmax()
assert pd.Timestamp(dia_record).month == mes_max, "¿el día récord cae en el mes máximo?"''',
  'conteo.groupby(conteo.index.month).mean(); .idxmax(); sismos["fecha"].value_counts().idxmax().'),

 ("## 3. ¿Estacionalidad real o racimos? Un test honesto",
  "La celda de abajo aplica un test **chi-cuadrado** a los sismos individuales por mes del "
  "calendario: da un p-valor bajo, que parece decir «hay estacionalidad». **Pero ese test supone "
  "eventos independientes**, y las réplicas no lo son: un solo terremoto aporta decenas de sismos "
  "al mismo mes.\n\n"
  "Un test que respeta los racimos: **permutar meses completos**. Si el calendario no importa, "
  "barajar los 72 conteos mensuales entre sí debería producir perfiles tan dispares como el real. "
  "El p-valor es la fracción de barajadas con una diferencia máx−mín **igual o mayor** que la real.",
  "Test de permutación",
  '''observado = perfil.max() - perfil.min()
rng = np.random.default_rng(42)
mayores = 0
N = 2000
for _ in range(N):
    barajado = pd.Series(rng.permutation(conteo.values), index=conteo.index)
    p = barajado.groupby(barajado.index.month).mean()
    mayores += (p.max() - p.min()) >= observado
p_valor = mayores / N
print(f"diferencia observada: {observado:.1f} sismos/mes · p-valor por permutación: {p_valor:.2f}")''',
  '''observado = perfil.max() - perfil.min()
rng = np.random.default_rng(42)
mayores = 0
N = 2000
for _ in range(N):
    barajado = pd.Series(rng.permutation(conteo.values), index=conteo.index)
    # TODO: perfil por mes del calendario de `barajado` y suma 1 a `mayores` si su (máx - mín) >= observado
    ...
p_valor = mayores / N
print("p-valor por permutación:", p_valor)''',
  '''assert 0.10 < p_valor < 0.60, "con 2000 permutaciones el p-valor debería rondar 0,3"''',
  'p = barajado.groupby(barajado.index.month).mean(); mayores += (p.max() - p.min()) >= observado.'),

 ("## 4. Entonces, ¿cómo se pronostica?",
  "Valida igual que con el PM2.5: entrena con 2020–2024 y pronostica los 12 meses de 2025 con "
  "(a) el **promedio** plano de todos los meses, (b) el **promedio estacional** y (c) el **ingenuo** "
  "(último mes). Si la estacionalidad fuera real, (b) debería ganar con claridad.",
  "Tres pronósticos de conteo para 2025",
  '''entrena = conteo[:"2024"]
real = conteo["2025"]
errores = {
    "promedio": float(np.abs(entrena.mean() - real.values).mean()),
    "promedio_estacional": float(np.abs(entrena.groupby(entrena.index.month).mean().values - real.values).mean()),
    "ingenuo": float(np.abs(entrena.iloc[-1] - real.values).mean()),
}
print({k: round(v, 2) for k, v in errores.items()})''',
  '''entrena = conteo[:"2024"]
real = conteo["2025"]
errores = {
    "promedio": float(np.abs(entrena.mean() - real.values).mean()),
    "promedio_estacional": ...,   # TODO: promedio de cada mes del calendario en `entrena` vs real
    "ingenuo": ...,               # TODO: último valor de `entrena` vs real
}
print(errores)''',
  '''_e = conteo[:"2024"]; _r = conteo["2025"].values
assert abs(errores["promedio_estacional"] - np.abs(_e.groupby(_e.index.month).mean().values - _r).mean()) < 1e-9
assert abs(errores["ingenuo"] - np.abs(_e.iloc[-1] - _r).mean()) < 1e-9''',
  'np.abs(entrena.groupby(entrena.index.month).mean().values - real.values).mean() y np.abs(entrena.iloc[-1] - real.values).mean().'),
]

PROF_CHI = '''# El test ingenuo (ilustrativo): chi-cuadrado sobre sismos individuales por mes del calendario,
# con lo esperado proporcional a los días de cada mes. Supone eventos INDEPENDIENTES.
from scipy.stats import chisquare
obs = sismos["fecha"].dt.month.value_counts().sort_index()
dias = pd.Series(pd.date_range("2020-01-01", "2025-12-31").month).value_counts().sort_index()
esperado = obs.sum() * dias / dias.sum()
print(f"chi-cuadrado ingenuo: p = {chisquare(obs.values, esperado.values).pvalue:.3f}  ← parece 'significativo'")'''

PROF_HEADER = '''# R2-10 · Series temporales — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas herramientas sobre otra serie del país — los
**sismos** de magnitud 4,5 o más registrados por el USGS en Chile entre 2020 y 2025. Primero hay
que **convertir eventos en serie** (conteo mensual), y después responder con honestidad una
pregunta que suena razonable: *¿hay meses más sísmicos que otros?*

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''

PROF_CIERRE = '''## Para llevar

- Los sismos vienen **en racimos** (varianza/media ≈ 1,7): un terremoto trae decenas de réplicas.
  Eso basta para que un mes «parezca» más sísmico.
- Un test que supone independencia (chi-cuadrado sobre eventos) **se deja engañar** por los
  racimos; permutar meses completos no encuentra evidencia de estacionalidad.
- La validación lo confirma: el promedio estacional no le gana de forma apreciable al promedio
  plano. Lo honesto es pronosticar una **tasa** (≈ 22 sismos M≥4,5 al mes), no una «temporada».
- Saber decir **«no hay patrón»** también es un resultado. En el Estado, evita planificar en
  torno a un ciclo que no existe.

---

*Fin de la profundización de R2-10.*'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        if i == 3:
            cells.append(h.code(PROF_CHI))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md(PROF_CIERRE))
    nb.cells = cells
    return nb


README = '''# R2-10 · Series temporales *(optativo)*

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-10-series-temporales/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes, analogías con Excel y autoevaluación.

Datos donde **el orden en el tiempo importa**. Con el PM2.5 diario de la estación **Cerro Navia**
(`aire_diario.csv`, SINCA 2020–2025): serie con calendario completo, **remuestreo** semanal y
mensual, **media móvil**, **estacionalidad** anual y semanal, **descomposición**, y
**validación temporal** de pronósticos (ingenuo, ingenuo estacional, promedio estacional y una
regresión mes + tendencia). La prueba de fuego: enfrentar el método elegido a lo que de verdad
pasó en enero–septiembre de 2026 (`aire_nuevos.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: los **sismos** (`sismos.csv`, USGS M≥4,5) como conteo
  mensual. ¿Hay temporada sísmica? Un test ingenuo dice que sí; uno honesto, que no.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.
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
