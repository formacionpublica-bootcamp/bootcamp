"""build_R2-03.py — módulo R2-03 (Estadística para modelar).

Rama R2 (Científico de Datos). Rearmado 2026: ancla de la
rama = calidad del aire (PM2.5 diario SINCA, 2020–2025). Mismo arco que la versión
anterior — describir la distribución, intervalo de confianza, prueba de hipótesis y
correlación — más asimetría/log, estacionalidad, bootstrap y «correlación ≠
causalidad» (la estación del año como variable de confusión). Profundiza =
transferencia con matrícula 2025 (MINEDUC) × población comunal: estudiantes por
1.000 habitantes y su correlación con el tamaño de la comuna. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-03-estadistica-para-modelar")

RAW = h.REPO_RAW


def guardado(n, src):
    """Celda de ilustración que no se cae si el ejercicio n aún tiene TODO."""
    cuerpo = "\n".join("    " + ln for ln in src.strip("\n").splitlines())
    primera, _, resto = cuerpo.partition("\n")
    return f"""{primera.strip()}
try:
{resto}
except (NameError, TypeError, ValueError):
    print("ℹ️ Completa el ejercicio {n} para ver este gráfico.")"""

SETUP = f'''# ── Preparación del entorno (ejecuta esta celda primero) ──────────────────────
import os, urllib.request
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# "En vivo o caché": usa el archivo local; si falta (ej. Colab), lo baja del repo.
CSV = "aire_diario.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve(f"{RAW}/{{CSV}}", CSV)

df = pd.read_csv(CSV, parse_dates=["fecha"])
df["mes"] = df["fecha"].dt.month
df["anio"] = df["fecha"].dt.year

# Estación ancla: Cerro Navia (Región Metropolitana) — mide PM2.5, temperatura y humedad.
cn = df[df["estacion"] == "Cerro Navia"].copy()
print("Todas las estaciones:", df.shape, "| Cerro Navia:", cn.shape)
df.head()'''

INTRO = '''## El dato: PM2.5 diario en 14 estaciones de Chile

Cada fila es **un día en una estación** del SINCA (Ministerio del Medio Ambiente):
`pm25` es la concentración promedio del día de material particulado fino, en µg/m³.
Algunas estaciones también miden `temp_media` (°C) y `humedad_media` (%).

> 🏛️ **La vara de comparación:** la norma chilena de PM2.5 para 24 horas es **50 µg/m³**
> (D.S. 12/2011 del MMA). La usaremos como referencia a lo largo del módulo.

**¿Por qué estadística antes de modelar?** Porque un modelo hereda todo lo que no viste:
una cola larga, una estacionalidad fuerte, una correlación que en realidad es otra cosa.
En este módulo vas a **describir**, **estimar con incertidumbre**, **contrastar** y
**correlacionar** — y a desconfiar con método.'''

EJ = [
 ("## 1. Describir antes de modelar: centro, cola y asimetría",
  "El PM2.5 no se reparte como una campana: la mayoría de los días son tranquilos y unos pocos "
  "son muy contaminados. Esa **cola larga** se mide con la **asimetría** (*skew*): 0 es simétrico, "
  "más de 1 es muy cargado a la derecha. Un truco clásico para domarla es mirar el **logaritmo** "
  "(usamos `np.log1p`, que es log(1 + x), porque hay días con PM2.5 = 0).",
  "Resumen descriptivo y asimetría del PM2.5 (todas las estaciones)",
  '''x = df["pm25"].dropna()
desc = {
    "media":     float(x.mean()),
    "mediana":   float(x.median()),
    "p90":       float(x.quantile(0.90)),
    "asimetria": float(x.skew()),
}
asim_log = float(np.log1p(x).skew())
print(desc)
print("asimetría tras log1p:", round(asim_log, 2))''',
  '''x = df["pm25"].dropna()
desc = {
    "media":     ...,   # TODO: x.mean()
    "mediana":   ...,   # TODO: x.median()
    "p90":       ...,   # TODO: percentil 90 -> x.quantile(0.90)
    "asimetria": ...,   # TODO: x.skew()
}
# TODO: asimetría del logaritmo -> np.log1p(x).skew()
asim_log = ...
print(desc)
print("asimetría tras log1p:", asim_log)''',
  '''assert set(desc) == {"media", "mediana", "p90", "asimetria"}
assert desc["media"] > desc["mediana"], "Con cola a la derecha, la media queda sobre la mediana"
assert desc["asimetria"] > 1, "El PM2.5 diario es muy asimétrico"
assert abs(asim_log) < abs(desc["asimetria"]), "El log debería reducir la asimetría"''',
  "x.mean(), x.median(), x.quantile(0.90), x.skew(); y np.log1p(x).skew() para el logaritmo.",
  '''# (ilustración) La misma variable, en escala original y en escala log
fig, ax = plt.subplots(1, 2, figsize=(10, 3.5))
ax[0].hist(x, bins=60, color="#4240e5"); ax[0].set_title("PM2.5 diario (µg/m³)")
ax[0].axvline(50, color="#c0392b", ls="--", label="norma 24 h (50)"); ax[0].legend()
ax[1].hist(np.log1p(x), bins=60, color="#ff6b35"); ax[1].set_title("log(1 + PM2.5)")
for a in ax: a.set_ylabel("días")
plt.tight_layout(); plt.show()'''),

 ("## 2. Estacionalidad: el invierno manda",
  "Antes de cualquier modelo, pregunta **cuándo** pasa lo que mides. En Santiago, el PM2.5 sube en "
  "otoño-invierno (más calefacción a leña, inversión térmica que atrapa el aire frío y la "
  "contaminación cerca del suelo). Trabajamos con la estación ancla, **Cerro Navia** (`cn`).",
  "Promedio por mes y días sobre la norma en Cerro Navia",
  '''por_mes = cn.groupby("mes")["pm25"].mean()
mes_peor = int(por_mes.idxmax())
dias_sobre_norma = int((cn["pm25"] > 50).sum())
print(por_mes.round(1))
print("mes con mayor promedio:", mes_peor, "| días sobre 50 µg/m³ (2020–2025):", dias_sobre_norma)''',
  '''# TODO: PM2.5 promedio por mes (groupby "mes")
por_mes = ...
# TODO: número del mes con mayor promedio (idxmax)
mes_peor = ...
# TODO: cuántos días de Cerro Navia superaron 50 µg/m³
dias_sobre_norma = ...
print("mes con mayor promedio:", mes_peor, "| días sobre 50:", dias_sobre_norma)''',
  '''assert len(por_mes) == 12
assert mes_peor in (5, 6, 7, 8), "El peor mes debería caer en otoño-invierno"
assert dias_sobre_norma == int((cn["pm25"] > 50).sum())''',
  'cn.groupby("mes")["pm25"].mean(); int(por_mes.idxmax()); int((cn["pm25"] > 50).sum()).',
  '''# (ilustración) Distribución diaria por mes: la caja muestra el 50% central de los días
meses = [cn.loc[cn["mes"] == m, "pm25"].dropna() for m in range(1, 13)]
plt.figure(figsize=(9, 4))
plt.boxplot(meses, showfliers=False)
plt.axhline(50, color="#c0392b", ls="--", label="norma 24 h (50 µg/m³)")
plt.xticks(range(1, 13), ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"])
plt.ylabel("PM2.5 diario (µg/m³)"); plt.title("Cerro Navia 2020–2025: PM2.5 diario por mes")
plt.legend(); plt.tight_layout(); plt.show()'''),

 ("## 3. Intervalo de confianza para la media invernal",
  "«El PM2.5 promedio del invierno en Cerro Navia es X» es una **estimación**: con otros "
  "inviernos daría otro número. El **intervalo de confianza al 95%** acompaña la cifra con su "
  "incertidumbre. Definimos invierno = junio, julio y agosto.",
  "IC 95% de la media de PM2.5 en invierno",
  '''inv = cn[cn["mes"].isin([6, 7, 8])]["pm25"].dropna()
media_inv = inv.mean()
ic_low, ic_high = stats.t.interval(0.95, len(inv) - 1, loc=media_inv, scale=stats.sem(inv))
print("días de invierno:", len(inv), "| media:", round(media_inv, 1),
      "| IC95%: [", round(ic_low, 1), ",", round(ic_high, 1), "] µg/m³")''',
  '''inv = cn[cn["mes"].isin([6, 7, 8])]["pm25"].dropna()
media_inv = inv.mean()
# TODO: stats.t.interval(0.95, len(inv)-1, loc=media_inv, scale=stats.sem(inv))
ic_low, ic_high = ..., ...
print("media:", round(media_inv, 1), "| IC95%: [", ic_low, ",", ic_high, "]")''',
  '''assert ic_low < media_inv < ic_high
assert 0 < ic_high - ic_low < 10, "Con ~550 días el intervalo debería ser angosto (pocos µg/m³)"''',
  "stats.t.interval(0.95, len(inv)-1, loc=media_inv, scale=stats.sem(inv)) devuelve (bajo, alto).",
  None),

 ("## 4. *Bootstrap*: la diferencia invierno − verano, sin fórmulas",
  "¿Cuánto más contaminado es el invierno que el verano (diciembre a febrero)? El **bootstrap** "
  "responde con fuerza bruta: remuestrea los días **con reemplazo** miles de veces, calcula la "
  "diferencia de medias en cada remuestra y toma los percentiles 2,5 y 97,5. Sin supuestos de "
  "normalidad — útil con colas largas como esta.",
  "IC 95% por bootstrap de la diferencia de medias",
  '''ver = cn[cn["mes"].isin([12, 1, 2])]["pm25"].dropna()
dif_obs = inv.mean() - ver.mean()
rng = np.random.default_rng(42)
difs = [rng.choice(inv.values, len(inv)).mean() - rng.choice(ver.values, len(ver)).mean()
        for _ in range(2000)]
b_low, b_high = np.percentile(difs, [2.5, 97.5])
print("diferencia observada:", round(dif_obs, 1), "µg/m³ | IC95% bootstrap: [",
      round(b_low, 1), ",", round(b_high, 1), "]")''',
  '''ver = cn[cn["mes"].isin([12, 1, 2])]["pm25"].dropna()
dif_obs = inv.mean() - ver.mean()
rng = np.random.default_rng(42)
# TODO: 2000 diferencias de medias de remuestras:
#       rng.choice(inv.values, len(inv)).mean() - rng.choice(ver.values, len(ver)).mean()
difs = ...
# TODO: percentiles 2,5 y 97,5 de difs -> np.percentile(difs, [2.5, 97.5])
b_low, b_high = ..., ...
print("diferencia observada:", round(dif_obs, 1), "| IC95% bootstrap:", b_low, b_high)''',
  '''assert len(difs) == 2000
assert b_low < dif_obs < b_high
assert b_low > 0, "El intervalo no toca el 0: el invierno es claramente peor"''',
  "Lista por comprensión: [rng.choice(inv.values, len(inv)).mean() - rng.choice(ver.values, len(ver)).mean() for _ in range(2000)].",
  guardado(4, '''# (ilustración) La distribución bootstrap de la diferencia
plt.figure(figsize=(6, 3.5))
plt.hist(difs, bins=40, color="#4240e5")
for v in (b_low, b_high):
    plt.axvline(v, color="#c0392b", ls="--")
plt.xlabel("invierno − verano (µg/m³)"); plt.ylabel("remuestras")
plt.title("2.000 diferencias bootstrap (líneas: IC 95%)"); plt.tight_layout(); plt.show()''')),

 ("## 5. Prueba de hipótesis: ¿el invierno 2025 fue más limpio que el 2024?",
  "Una autoridad anuncia: «el PM2.5 invernal bajó este año». ¿Es una mejora real o cabe en el azar "
  "de un invierno a otro? El **test de Welch** (`stats.ttest_ind(..., equal_var=False)`) compara "
  "dos medias: si el *p-valor* < 0,05 diríamos que la diferencia es **significativa**.\n\n"
  "> ⚠️ **Letra chica honesta:** los días seguidos se parecen entre sí (no son independientes), "
  "así que con series diarias los p-valores tienden a ser **optimistas**. Úsalos como guía, no como veredicto.",
  "Compara los inviernos 2024 y 2025 en Cerro Navia",
  '''en_invierno = cn["mes"].isin([6, 7, 8])
inv_2024 = cn[en_invierno & (cn["anio"] == 2024)]["pm25"].dropna()
inv_2025 = cn[en_invierno & (cn["anio"] == 2025)]["pm25"].dropna()
t_stat, p_valor = stats.ttest_ind(inv_2024, inv_2025, equal_var=False)
significativa = bool(p_valor < 0.05)
print("media 2024:", round(inv_2024.mean(), 1), "| media 2025:", round(inv_2025.mean(), 1))
print("t:", round(t_stat, 2), "| p-valor:", round(p_valor, 3), "| ¿significativa al 5%?", significativa)''',
  '''en_invierno = cn["mes"].isin([6, 7, 8])
inv_2024 = cn[en_invierno & (cn["anio"] == 2024)]["pm25"].dropna()
inv_2025 = cn[en_invierno & (cn["anio"] == 2025)]["pm25"].dropna()
# TODO: test de Welch -> stats.ttest_ind(inv_2024, inv_2025, equal_var=False)
t_stat, p_valor = ..., ...
# TODO: True si p_valor < 0.05
significativa = ...
print("media 2024:", round(inv_2024.mean(), 1), "| media 2025:", round(inv_2025.mean(), 1))
print("p-valor:", p_valor, "| ¿significativa al 5%?", significativa)''',
  '''assert 0.0 <= p_valor <= 1.0
assert significativa == (p_valor < 0.05)
assert not significativa, "Con estos datos la baja de 2025 NO es distinguible del azar"''',
  "stats.ttest_ind(inv_2024, inv_2025, equal_var=False) devuelve (t, p); significativa = p_valor < 0.05.",
  None),

 ("## 6. Correlación ≠ causalidad: la estación del año como confusor",
  "La correlación de Pearson (−1 a 1) mide si dos variables se mueven juntas. En Cerro Navia, "
  "más humedad parece ir con más PM2.5. ¿La humedad «causa» contaminación? Mira qué pasa al comparar "
  "**solo días de pleno invierno** (junio y julio): si el signo se da vuelta, la relación global era "
  "obra de un tercero — **el invierno**, que trae a la vez aire húmedo y más contaminación.",
  "Correlaciones globales vs dentro del invierno",
  '''s = cn.dropna(subset=["pm25", "temp_media", "humedad_media"])
r_temp, p_temp = stats.pearsonr(s["temp_media"], s["pm25"])
r_hum_todo = s["pm25"].corr(s["humedad_media"])
pleno = s[s["mes"].isin([6, 7])]
r_hum_invierno = pleno["pm25"].corr(pleno["humedad_media"])
print("r(temperatura, PM2.5):", round(r_temp, 2), "| p-valor:", p_temp)
print("r(humedad, PM2.5) todo el año:", round(r_hum_todo, 2))
print("r(humedad, PM2.5) solo jun-jul:", round(r_hum_invierno, 2))''',
  '''s = cn.dropna(subset=["pm25", "temp_media", "humedad_media"])
# TODO: stats.pearsonr(s["temp_media"], s["pm25"]) -> (r, p)
r_temp, p_temp = ..., ...
# TODO: correlación humedad–PM2.5 en todos los días -> s["pm25"].corr(s["humedad_media"])
r_hum_todo = ...
pleno = s[s["mes"].isin([6, 7])]
# TODO: la misma correlación, pero solo en los días de `pleno`
r_hum_invierno = ...
print("r temp:", r_temp, "| r hum (todo):", r_hum_todo, "| r hum (jun-jul):", r_hum_invierno)''',
  '''assert -1 <= r_temp <= 1 and 0 <= p_temp <= 1
assert r_temp < 0, "Días más fríos, más PM2.5"
assert r_hum_todo > 0, "En el año completo, humedad y PM2.5 suben juntas"
assert r_hum_invierno < 0, "Dentro del invierno el signo se invierte"''',
  "stats.pearsonr(x, y) devuelve (r, p); para la correlación simple usa serie1.corr(serie2), primero en s y luego en pleno.",
  guardado(6, '''# (ilustración) La paradoja en un gráfico: global vs dentro de jun-jul
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
ax[0].scatter(s["humedad_media"], s["pm25"], s=6, alpha=0.3, color="#4240e5")
ax[0].set_title(f"Todo el año: r = {r_hum_todo:.2f}")
ax[1].scatter(pleno["humedad_media"], pleno["pm25"], s=8, alpha=0.5, color="#ff6b35")
ax[1].set_title(f"Solo junio-julio: r = {r_hum_invierno:.2f}")
for a in ax: a.set_xlabel("humedad media (%)")
ax[0].set_ylabel("PM2.5 (µg/m³)"); plt.tight_layout(); plt.show()''')),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

En el ejercicio 6, la temperatura también correlaciona fuerte con el PM2.5 (r ≈ −0,55): días fríos,
aire sucio. Si un municipio propusiera «subir la temperatura» como política de aire limpio, sería
absurdo — el frío actúa **a través** de la calefacción a leña y de la inversión térmica. En una o dos
frases: ¿qué variable **sí** podría intervenir una política pública, y qué dato te faltaría para medirla?'''

CIERRE = '''## Cierre

- **Describe antes de modelar:** el PM2.5 tiene cola larga (media > mediana, asimetría > 1); el log la doma.
- La **estacionalidad** es la primera estructura de cualquier serie pública: el invierno manda.
- Un **intervalo de confianza** (fórmula t o *bootstrap*) acompaña cada cifra con su incertidumbre.
- Una **prueba de hipótesis** separa una mejora real de la variación normal — y un p > 0,05 también es un resultado.
- **Correlación ≠ causalidad:** una tercera variable (la estación del año) puede crear, borrar o invertir una relación.

> *En R2-04 usarás todo esto para construir tu primer modelo: predecir el PM2.5 de mañana.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-03", "Estadística para modelar", "R2", "Científico de Datos", "5–6",
                      ["Describir una distribución real: centro, cola, **asimetría** y escala log.",
                       "Detectar **estacionalidad** antes de modelar.",
                       "Estimar con **intervalos de confianza** (fórmula t y *bootstrap*).",
                       "Contrastar grupos con una **prueba de hipótesis** e interpretar un p-valor.",
                       "Medir **correlación** y reconocer una **variable de confusión**."],
                      "usar estadística descriptiva e inferencial para sustentar —y cuestionar— decisiones de modelado.",
                      "PM2.5 diario 2020–2025 de 14 estaciones SINCA (MMA), con temperatura y humedad en Cerro Navia.",
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


# ── Profundización (transferencia: matrícula × población comunal) ─────────────
PROF_PREP = f'''import pandas as pd, numpy as np, os, urllib.request
import matplotlib.pyplot as plt
from scipy import stats
for archivo in ["matricula.csv", "comunas.csv"]:
    if not os.path.exists(archivo):
        urllib.request.urlretrieve(f"{RAW}/{{archivo}}", archivo)
mat = pd.read_csv("matricula.csv")       # matrícula 2025 por establecimiento (MINEDUC)
comunas = pd.read_csv("comunas.csv")     # población de 30 comunas de Chile
print("matrícula:", mat.shape, "| comunas:", comunas.shape)'''

PROF_EJ = [
 ("## 1. Construir el indicador: estudiantes por 1.000 habitantes",
  "Suma la matrícula por comuna, crúzala con la población y calcula la **tasa**. "
  "Comparar conteos brutos entre comunas de tamaños tan distintos no dice nada; la tasa sí.",
  "Calcula la tasa y encuentra los extremos",
  '''est = mat.groupby("comuna")["mat_total"].sum().reset_index()
c = pd.merge(est, comunas, on="comuna")
c["tasa"] = 1000 * c["mat_total"] / c["poblacion"]
comuna_max = c.loc[c["tasa"].idxmax(), "comuna"]
comuna_min = c.loc[c["tasa"].idxmin(), "comuna"]
print("comunas:", len(c), "| tasa mediana:", round(c["tasa"].median(), 1))
print("mayor tasa:", comuna_max, "| menor tasa:", comuna_min)''',
  '''est = mat.groupby("comuna")["mat_total"].sum().reset_index()
c = pd.merge(est, comunas, on="comuna")      # el cruce de R2-01
# TODO: tasa = 1000 * mat_total / poblacion
c["tasa"] = ...
# TODO: nombre de la comuna con mayor y con menor tasa (idxmax / idxmin + loc)
comuna_max = ...
comuna_min = ...
print("mayor tasa:", comuna_max, "| menor tasa:", comuna_min)''',
  '''assert len(c) == 30
assert comuna_max == c.loc[c["tasa"].idxmax(), "comuna"]
assert comuna_min == c.loc[c["tasa"].idxmin(), "comuna"]''',
  '1000 * c["mat_total"] / c["poblacion"]; el nombre con c.loc[c["tasa"].idxmax(), "comuna"].'),

 ("## 2. La correlación que no dice nada: conteos vs tamaño",
  "¿Las comunas con más gente tienen más estudiantes? Obvio. Una correlación altísima entre dos "
  "**conteos** suele ser solo el **tamaño** hablando — por eso se trabaja con tasas.",
  "Correlación entre población y matrícula total",
  '''r_conteos, p_conteos = stats.pearsonr(c["poblacion"], c["mat_total"])
print("r(población, matrícula):", round(r_conteos, 3))''',
  '''# TODO: stats.pearsonr(c["poblacion"], c["mat_total"])
r_conteos, p_conteos = ..., ...
print("r(población, matrícula):", r_conteos)''',
  '''assert r_conteos > 0.9, "Dos conteos del mismo territorio correlacionan casi perfecto"''',
  'stats.pearsonr(c["poblacion"], c["mat_total"]) devuelve (r, p).'),

 ("## 3. Pearson vs Spearman: ¿las comunas grandes son menos «escolares»?",
  "Ahora la pregunta interesante: ¿la **tasa** baja cuando la comuna es más grande? Pearson mide "
  "relación **lineal** y es sensible a valores extremos; **Spearman** usa rangos (orden) y es robusto. "
  "Si discrepan, la relación depende de unos pocos casos.",
  "Correlación de la tasa con la población, con ambos métodos",
  '''r_p, p_p = stats.pearsonr(c["poblacion"], c["tasa"])
rho, p_s = stats.spearmanr(c["poblacion"], c["tasa"])
print("Pearson:", round(r_p, 2), "(p =", round(p_p, 3), ") | Spearman:", round(rho, 2), "(p =", round(p_s, 3), ")")''',
  '''# TODO: Pearson y Spearman entre c["poblacion"] y c["tasa"]
r_p, p_p = ..., ...
rho, p_s = ..., ...
print("Pearson:", r_p, p_p, "| Spearman:", rho, p_s)''',
  '''assert r_p < 0, "Pearson sugiere una relación negativa"
assert abs(rho) < abs(r_p), "Spearman es más débil: la relación depende de pocos casos"
assert p_p < 0.05 < p_s''',
  'stats.pearsonr(...) y stats.spearmanr(...), ambos con (c["poblacion"], c["tasa"]).'),

 ("## 4. *Bootstrap* de la correlación: ¿cuánto confiar con 30 comunas?",
  "Remuestrea las 30 comunas con reemplazo 2.000 veces y recalcula Pearson en cada una. "
  "El ancho del intervalo te dice cuán frágil es la conclusión.",
  "IC 95% bootstrap del r de Pearson",
  '''rng = np.random.default_rng(42)
rs = []
for _ in range(2000):
    idx = rng.integers(0, len(c), len(c))
    m = c.iloc[idx]
    rs.append(m["poblacion"].corr(m["tasa"]))
ic_low, ic_high = np.percentile(rs, [2.5, 97.5])
print("r observado:", round(r_p, 2), "| IC95% bootstrap: [", round(ic_low, 2), ",", round(ic_high, 2), "]")''',
  '''rng = np.random.default_rng(42)
rs = []
for _ in range(2000):
    idx = rng.integers(0, len(c), len(c))
    m = c.iloc[idx]
    # TODO: agrega a rs la correlación poblacion–tasa de la remuestra m
    ...
# TODO: percentiles 2,5 y 97,5 de rs -> np.percentile(rs, [2.5, 97.5])
ic_low, ic_high = ..., ...
print("IC95% bootstrap:", ic_low, ic_high)''',
  '''assert len(rs) == 2000
assert ic_low < r_p < ic_high
assert ic_high - ic_low > 0.3, "Con 30 comunas el intervalo es ancho"''',
  'rs.append(m["poblacion"].corr(m["tasa"])).'),
]

PROF_CIERRE = '''## Para pensar: ¿qué mide de verdad la tasa?

La matrícula se cuenta **donde está el colegio**, no donde vive el estudiante. Una comuna con
muchos colegios que reciben alumnos de comunas vecinas tendrá una tasa «inflada», y su vecina
una «desinflada». La correlación con el tamaño puede ser, en parte, un efecto de **cómo se mide**
— otra forma de confusor. Antes de recomendar «más colegios en las comunas grandes», habría que
cruzar con la comuna de residencia de los estudiantes.

---

*Fin de la profundización de R2-03.*'''

PROF_HEADER = '''# R2-03 · Estadística para modelar — Profundización (opcional) 🔬

**Formación Pública — Rama R2 · Científico de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas herramientas de la lección — correlación, Pearson vs
Spearman, *bootstrap* — sobre otro dato del Estado: la **matrícula escolar 2025** (MINEDUC) cruzada
con la **población** de 30 comunas. ¿Las comunas grandes tienen menos estudiantes por habitante?

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if i == 3:
            cells.append(h.code(guardado(3, '''# (ilustración) Tasa vs población: ¿quién arrastra la recta?
plt.figure(figsize=(7, 4))
plt.scatter(c["poblacion"], c["tasa"], color="#4240e5")
for _, f in c[(c["poblacion"] > 400000) | (c["tasa"] < 160)].iterrows():
    plt.annotate(f["comuna"], (f["poblacion"], f["tasa"]), fontsize=8,
                 xytext=(4, 4), textcoords="offset points")
plt.xlabel("Población"); plt.ylabel("Estudiantes por 1.000 habitantes")
plt.title("30 comunas: tasa de matrícula vs tamaño"); plt.tight_layout(); plt.show()''')))
    cells.append(h.md(PROF_CIERRE))
    nb.cells = cells
    return nb


README = '''# R2-03 · Estadística para modelar

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-03-estadistica-para-modelar/leccion.ipynb)

> 📖 **¿Trabado o quieres ir paso a paso?** Abre la [**Guía de Aprendizaje**](GUIA_APRENDIZAJE.md)
> del módulo: pistas progresivas 🟢🟡🔴, errores frecuentes y autoevaluación.

Describir antes de modelar: distribución y **asimetría** del PM2.5 diario, **estacionalidad**,
**intervalos de confianza** (fórmula t y *bootstrap*), **prueba de hipótesis** (¿el invierno 2025
fue más limpio que el 2024?) y **correlación ≠ causalidad** (la estación del año como confusor),
sobre datos reales del SINCA (`aire_diario.csv`, 14 estaciones, 2020–2025). La profundización
transfiere las herramientas a la matrícula 2025 (`matricula.csv`) × población comunal (`comunas.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: estudiantes por 1.000 habitantes, Pearson vs Spearman, *bootstrap* de una correlación.
- `solucion.ipynb` / `profundiza_solucion.ipynb` — uso interno.

*Fuentes: SINCA — Ministerio del Medio Ambiente; MINEDUC — datos abiertos (matrícula 2025).*
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
