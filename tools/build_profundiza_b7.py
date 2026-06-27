# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de B7 (series temporales):
B7/profundiza.ipynb (estudiante) + B7/profundiza_solucion.ipynb (resuelto).

Más teórico que la lección: explica el *porqué* de la validación temporal, la
descomposición tendencia/estacionalidad/ruido, la estacionariedad, los baselines
ingenuos, el backtesting (walk-forward) y por qué la incertidumbre crece con el
horizonte. Demos reales sobre gasto_anual.csv (excluyendo 2026 parcial)."""
import json, os

BASE = "B7-series-temporales"

TITULO = """# B7 · Series temporales — Profundización (opcional) 🔬

**Formación Pública — Bloque avanzado · IA aplicada · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de B7 —donde construiste pronósticos y los
validaste escondiendo el último año— aquí vamos al *porqué*: **por qué con el tiempo no se puede barajar**
(usar el futuro para predecir el pasado es trampa), cómo se piensa una serie como **tendencia +
estacionalidad + ruido**, qué significa que una serie sea **estacionaria** (y por qué *diferenciar* la
estabiliza), por qué los **baselines ingenuos** son la vara mínima sagrada, cómo se hace un **backtest
walk-forward** honesto, y por qué la **incertidumbre crece** mientras más lejos pronosticas.

Menos recetas, más **forma de pensar el tiempo**. Los ejercicios del final son más conceptuales: cada uno
**calcula** algo y te pide **elegir la interpretación correcta**.

> Requisito: haber hecho `leccion.ipynb` de B7. Mismo dataset: `gasto_anual.csv`."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("gasto_anual.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/B7-series-temporales/gasto_anual.csv"
        urllib.request.urlretrieve(url, "gasto_anual.csv")
    except Exception:
        print("Si estás en Colab, sube gasto_anual.csv manualmente.")

df = pd.read_csv("gasto_anual.csv")
# Serie de trabajo: SOLO años completos (excluimos el 2026 parcial), indexada por año.
gasto = df[df["parcial"] == False].set_index("anio")["gasto_clp"].astype(float)
print(f"Serie de {len(gasto)} años completos: {gasto.index.min()}–{gasto.index.max()}")
print(f"Gasto 2019: {gasto.loc[2019]/1e12:,.2f} billones  →  2025: {gasto.loc[2025]/1e12:,.2f} billones CLP")"""

S1 = """## 1. Por qué con el tiempo NO se puede barajar

En todos los módulos anteriores, cuando querías evaluar un modelo, **barajabas** las filas y separabas un
trozo al azar para test. Con datos donde cada fila es independiente (un proveedor, una comuna) eso está
bien. **Con series temporales es trampa**, y vale la pena entender exactamente por qué.

El problema es la **fuga de información desde el futuro** (*data leakage* temporal). Si barajas y un año
del **medio** cae en el test, su evaluación es ridículamente fácil: el modelo "vio" el año **anterior** y
el **posterior**, así que solo tiene que **interpolar** entre dos vecinos que ya conoce. Pero en la vida
real **nunca** tendrás el año posterior: cuando pronosticas 2026, el 2027 todavía no existe. Pronosticar
es **extrapolar** (estirar hacia un futuro desconocido), no **interpolar** (rellenar un hueco rodeado de
datos). Evaluar interpolando te hace creer que tu modelo es mucho mejor de lo que será.

La regla de oro: **el test siempre va DESPUÉS del entrenamiento en el tiempo.** Nunca al azar, nunca con
el futuro a la vista. Vamos a *medirlo*: comparemos el error de "adivinar" un año del medio sabiendo sus
vecinos (lo que permite un split aleatorio) contra extrapolar el último año solo con el pasado."""

S1_CODE = """# TRAMPA (split aleatorio): el 2022 cae en test; el modelo conoce 2021 Y 2023 (¡el futuro!).
# Interpolar entre vecinos es facilísimo:
interp_2022 = (gasto.loc[2021] + gasto.loc[2023]) / 2      # usa 2023 = un año POSTERIOR
err_interp = abs(interp_2022 - gasto.loc[2022])

# HONESTO (split temporal): predecir 2025 SOLO con el pasado (≤2024). Hay que extrapolar:
extrap_2025 = gasto.loc[2024]                              # baseline ingenuo, solo pasado
err_extrap = abs(extrap_2025 - gasto.loc[2025])

print(f"Interpolar 2022 sabiendo 2023 (TRAMPA): error = {err_interp/gasto.loc[2022]*100:5.1f}%")
print(f"Extrapolar 2025 solo con el pasado    : error = {err_extrap/gasto.loc[2025]*100:5.1f}%")
print("\\nEl split aleatorio reporta un error ~5× menor en términos porcentuales (2.9% vs 15.4%)...")
print("pero está usando el FUTURO. En producción jamás tendrás el año siguiente:")
print("por eso la validación debe ser TEMPORAL.")"""

S2 = """## 2. Separar señal de ruido: la recta y sus residuos

En la lección ya viste que una serie se piensa como **tendencia + estacionalidad + ruido**. Aquí no
repetimos esas definiciones: vamos a la pregunta que la lección no respondió — **¿cómo separamos, en la
práctica, la *señal* (la tendencia) del *ruido*?**

(Recordatorio breve de un matiz importante: la **estacionalidad** solo se ve con datos *sub-anuales*
—meses, trimestres—. Con datos **anuales** como los nuestros queda "promediada hacia adentro" de cada
año, así que aquí **no la podemos observar**: solo modelamos tendencia + ruido.)

Una forma simple de separar señal de ruido: ajustar una **recta** (la tendencia) y mirar lo que queda,
los **residuos**. Si los residuos no tienen forma —ni suben, ni bajan, ni dibujan una ola—, capturaste
bien la tendencia y lo demás es ruido. Veámoslo."""

S2_CODE = """anios = gasto.index.values.astype(float)
coef = np.polyfit(anios, gasto.values, 1)        # recta: tendencia
tendencia = np.polyval(coef, anios)
residuos = gasto.values - tendencia              # lo que la recta NO explica = ruido

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.6))
ax1.plot(anios, gasto.values/1e12, "o-", label="Gasto real")
ax1.plot(anios, tendencia/1e12, "--", color="crimson", label="Tendencia (recta)")
ax1.set_title("Serie = tendencia + ruido"); ax1.set_ylabel("Billones CLP"); ax1.legend()
ax2.axhline(0, color="gray", lw=1)
ax2.bar(anios, residuos/1e12, color="#0a7e7e")
ax2.set_title("Residuos (lo que la tendencia NO explica = ruido)"); ax2.set_ylabel("Billones CLP")
plt.tight_layout(); plt.show()

print(f"Pendiente de la tendencia: +{coef[0]/1e12:,.2f} billones por año.")
print(f"Residuo más grande: {np.abs(residuos).max()/1e12:,.2f} billones (el ruido que la recta no captura).")"""

S3 = """## 3. Estacionariedad: por qué *diferenciar* estabiliza la serie

Una serie es **estacionaria** cuando sus propiedades **no cambian con el tiempo**: su media y su varianza
se mantienen estables, sin tendencia ni cambios de escala. Muchos métodos clásicos de pronóstico
**suponen** estacionariedad, así que conviene saber reconocerla.

Nuestro gasto **no** es estacionario: su media **sube** año tras año (eso es, justamente, tener
tendencia). La primera mitad de la serie promedia mucho menos que la segunda. El truco estándar para
"quitarle" la tendencia es **diferenciar**: en vez de mirar el *nivel* ($valor_t$), miras el *cambio*
($valor_t - valor_{t-1}$). La serie de **cambios** suele ser mucho más estable —ya no arrastra el nivel
hacia arriba—, y por eso es más fácil de modelar.

Intuición de funcionario: el *nivel* de gasto crece sin parar (no es estable), pero el *cambio
porcentual anual* es menos extremo que el nivel absoluto (se mueve en un rango más estrecho, en la
misma escala año a año). Diferenciar —o mirar el cambio porcentual— es pasar de "¿cuánto gastamos?" a
"¿cuánto **más** gastamos que el año pasado?". Veámoslo comparando la media de la primera y la segunda
mitad, antes y después de pasar del nivel al cambio porcentual."""

S3_CODE = """mitad = len(gasto) // 2

# NIVEL: ¿la media es estable entre la 1ª y la 2ª mitad?
m1_niv = gasto.iloc[:mitad].mean()
m2_niv = gasto.iloc[mitad:].mean()
ratio_niv = m2_niv / m1_niv

# CAMBIO PORCENTUAL año a año (diferenciar relativo): quita la tendencia compuesta
dif_pct = gasto.pct_change().dropna()
m1_pct = dif_pct.iloc[:len(dif_pct)//2].mean()
m2_pct = dif_pct.iloc[len(dif_pct)//2:].mean()
ratio_pct = m2_pct / m1_pct

print("NIVEL (no estacionario):")
print(f"   media 1ª mitad = {m1_niv/1e12:,.2f}  vs  2ª mitad = {m2_niv/1e12:,.2f} billones  -> sube {ratio_niv:.2f}×")
print("CAMBIO PORCENTUAL ANUAL (más estable entre mitades):")
print(f"   media 1ª mitad = {m1_pct*100:,.1f}%  vs  2ª mitad = {m2_pct*100:,.1f}%  -> sube {ratio_pct:.2f}×")
print(f"\\nEl NIVEL crece {ratio_niv:.2f}× entre mitades (media inestable = tendencia).")
print(f"El CAMBIO PORCENTUAL sube solo {ratio_pct:.2f}× entre mitades: pasar del nivel al cambio relativo")
print("reduce la inestabilidad de la media. (Ojo: con crecimiento compuesto, la diferencia ABSOLUTA")
print("año a año NO se estabiliza —empeora—; por eso aquí miramos el cambio porcentual, no la resta.)")"""

S4 = """## 4. Baselines ingenuos: la vara mínima que TODO modelo debe vencer

El error más común de quien empieza a pronosticar es saltar directo a un modelo sofisticado sin tener
contra qué compararlo. Un número de error "suena" bien o mal **solo en relación a algo**. Ese algo son los
**baselines ingenuos**: pronósticos tan tontos que dan vergüenza, pero que fijan la **vara mínima**.

- **Naïve (ingenuo):** "mañana será igual a hoy". Pronóstico del año $t$ = valor del año $t-1$. Cero
  cálculo, cero parámetros. Si tu modelo elaborado **no le gana al naïve**, tu modelo no sirve.
- **Promedio móvil:** "mañana será el promedio de los últimos $k$". Suaviza el ruido, pero **reacciona
  tarde** a una tendencia fuerte (siempre mira hacia atrás).

La pregunta correcta nunca es "¿mi error es chico?", sino **"¿mi error es menor que el del naïve?"**.
Comparemos el naïve contra un promedio móvil de 3 años, prediciendo cada año con la info previa."""

S4_CODE = """# Baseline NAÏVE: predigo el año t con el valor del año t-1
pred_naive = gasto.shift(1)

# Baseline PROMEDIO MÓVIL de 3 años: predigo el año t con el promedio de los 3 previos
pred_mm3 = gasto.shift(1).rolling(3).mean()

comparacion = pd.DataFrame({
    "real": gasto,
    "naive": pred_naive,
    "media_movil_3": pred_mm3,
})
comparacion["err_naive"] = (comparacion["real"] - comparacion["naive"]).abs()
comparacion["err_mm3"]   = (comparacion["real"] - comparacion["media_movil_3"]).abs()

mae_naive = comparacion["err_naive"].mean()
mae_mm3   = comparacion["err_mm3"].mean()
print((comparacion[["real", "naive", "media_movil_3"]] / 1e12).round(2).to_string())
print(f"\\nMAE naïve         : {mae_naive/1e12:,.2f} billones")
print(f"MAE promedio móvil : {mae_mm3/1e12:,.2f} billones")
print("\\nEn una serie con tendencia FUERTE y al alza, el promedio móvil va siempre atrasado")
print("(promedia años viejos y más bajos), así que el naïve —que copia el último— le gana.")"""

S5 = """## 5. Backtesting walk-forward: validar como se vivirá en la realidad

En la lección escondiste **un** año (el 2025) y mediste ahí. Eso es un *hold-out* de un punto. El método
más honesto y completo se llama **backtest walk-forward** (validación hacia adelante): simula que avanzas
en el tiempo **paso a paso**, y en cada paso pronosticas el siguiente año usando **solo lo que ya habrías
conocido** en ese momento. Nunca miras el futuro.

La mecánica es un bucle:

1. Párate en el año $t$. Entrena/usa solo los datos **hasta** $t$.
2. Pronostica el año $t+1$.
3. **Destapa** el valor real de $t+1$ y anota el error.
4. Avanza un año ($t \\to t+1$) y repite.

Así obtienes **varios** errores (uno por paso), no uno solo, y tu evaluación es mucho más robusta. Es,
literalmente, ensayar el modelo como se va a usar: prediciendo siempre hacia adelante, a ciegas del
mañana. Hagámoslo con el baseline naïve."""

S5_CODE = """def backtest_walkforward_naive(serie):
    anios = serie.index.tolist()
    filas = []
    for i in range(1, len(anios)):
        t = anios[i]
        pred = serie.loc[anios[i - 1]]      # SOLO el pasado: el valor del año anterior
        real = serie.loc[t]
        filas.append({"anio": t, "pred": pred, "real": real, "err_abs": abs(pred - real)})
    return pd.DataFrame(filas).set_index("anio")

bt = backtest_walkforward_naive(gasto)
print((bt / 1e12).round(2).to_string())
mae_bt = bt["err_abs"].mean()
print(f"\\nMAE walk-forward (naïve, 1 paso adelante): {mae_bt/1e12:,.2f} billones")
print("Cada fila es un pronóstico hecho A CIEGAS del futuro: así de honesta es la validación temporal.")"""

S6 = """## 6. Por qué la incertidumbre CRECE con el horizonte

Una última intuición clave para no prometer de más. Pronosticar **el año que viene** es relativamente
seguro; pronosticar **dentro de cinco años** es casi adivinar. ¿Por qué? Porque los errores **se
acumulan**: cada paso hacia el futuro se construye **sobre** el paso anterior, que ya traía su propio
error. Si te equivocas un poco en 2026, ese error contaminado entra como "base" para estimar 2027, que
suma su propio error, y así sucesivamente. La incertidumbre **se compone**.

Por eso un pronóstico serio nunca es una sola línea: es una **banda** que se **ensancha** con el horizonte
(un embudo que se abre). Decir "el gasto de 2030 será exactamente X" es ingenuo; lo honesto es "entre X y
Z, y mientras más lejos, más ancha la banda".

Lo veremos proyectando con el crecimiento medio a 1, 2 y 3 años, y poniéndole una banda de incertidumbre
que crece con el horizonte (más ancha mientras más lejos miramos)."""

S6_CODE = """g = gasto.pct_change().mean()              # crecimiento medio anual histórico
sigma = gasto.pct_change().std()           # cuánto varía ese crecimiento (fuente de incertidumbre)
ult = gasto.loc[2025]

horizontes = [1, 2, 3, 4, 5]
centro = [ult * (1 + g) ** h for h in horizontes]
# La banda se ensancha ~ con la raíz del horizonte (los errores se acumulan paso a paso)
ancho = [ult * (1 + g) ** h * sigma * np.sqrt(h) for h in horizontes]

aniosf = [2025 + h for h in horizontes]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(gasto.index, gasto.values/1e12, "o-", label="Histórico")
ax.plot(aniosf, np.array(centro)/1e12, "s--", color="crimson", label="Pronóstico central")
ax.fill_between(aniosf, (np.array(centro)-np.array(ancho))/1e12, (np.array(centro)+np.array(ancho))/1e12,
                color="crimson", alpha=0.15, label="Banda de incertidumbre")
ax.set_title("La banda se ENSANCHA con el horizonte"); ax.set_xlabel("Año"); ax.set_ylabel("Billones CLP")
ax.legend(); plt.tight_layout(); plt.show()

print(f"Ancho de la banda a 1 año : ±{ancho[0]/1e12:,.2f} billones")
print(f"Ancho de la banda a 5 años: ±{ancho[-1]/1e12:,.2f} billones (mucho más ancha)")
print("Pronosticar lejos no es 'más o menos igual de difícil': la incertidumbre se COMPONE.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Barajar la serie para hacer train/test.** Mezcla el futuro con el pasado: el modelo "interpola" y te miente sobre su calidad. El test va **después** en el tiempo, siempre.
- **Saltar a un modelo sofisticado sin baseline.** Si no le ganas al **naïve**, tu modelo no sirve. La vara mínima primero.
- **Confundir nivel con cambio.** Una serie con tendencia no es estacionaria; **diferenciar** (mirar el cambio anual) la estabiliza antes de modelar.
- **Validar con un solo punto y darlo por robusto.** El **walk-forward** te da varios errores; uno solo puede salir bien (o mal) por suerte.
- **Prometer un número exacto a 5 años.** La incertidumbre **crece** con el horizonte: reporta una **banda** que se ensancha, no una línea.
- **Comparar un año parcial con uno cerrado.** El 2026 está a medias: nunca lo midas contra un pronóstico de año completo."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: cada uno **calcula** algo y te pide **elegir la interpretación
correcta** (asigna `"A"`, `"B"` o `"C"` a `conclusion`). Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1: validación temporal (interpolar vs extrapolar) ----
E1 = """## Ejercicio 01 · Por qué barajar es trampa
Mide los dos errores que viste en la sección 1, usando la serie `gasto`:

- `err_interp`: error absoluto de **interpolar** el 2022 con el promedio de sus vecinos 2021 y 2023
  (esto es lo que un split aleatorio permitiría: ver el futuro 2023).
- `err_extrap`: error absoluto de **extrapolar** el 2025 con el baseline ingenuo (el valor de 2024, solo pasado).

Luego elige en `conclusion` la lectura correcta:
- **A.** `err_interp` es **mayor** que `err_extrap`: interpolar es más difícil.
- **B.** `err_interp` es **menor** que `err_extrap`: el split aleatorio "hace trampa" usando el año
  posterior, y por eso reporta un error artificialmente bajo. La validación debe ser **temporal**.
- **C.** Ambos errores son iguales: barajar o no da lo mismo."""
E1_TODO = """err_interp = None    # TODO: abs( (gasto[2021]+gasto[2023])/2  -  gasto[2022] )
err_extrap = None    # TODO: abs( gasto[2024]  -  gasto[2025] )
conclusion = None    # TODO: "A", "B" o "C"
"""
E1_SOL = """err_interp = abs((gasto.loc[2021] + gasto.loc[2023]) / 2 - gasto.loc[2022])
err_extrap = abs(gasto.loc[2024] - gasto.loc[2025])
conclusion = "B"
"""
E1_CHK = """try:
    _ei = abs((gasto.loc[2021] + gasto.loc[2023]) / 2 - gasto.loc[2022])
    _ee = abs(gasto.loc[2024] - gasto.loc[2025])
    _correcta = "B" if _ei < _ee else "A"
    assert err_interp is not None and abs(err_interp - _ei) < 1, "Revisa err_interp (interpola 2022 con 2021 y 2023)."
    assert err_extrap is not None and abs(err_extrap - _ee) < 1, "Revisa err_extrap (naïve: valor de 2024 vs 2025)."
    assert str(conclusion).strip().upper() == _correcta, "¿Cuál error salió más chico, y por qué eso es trampa?"
    print(f"✅ Correcto. Interpolar (con el futuro) erró {_ei/gasto.loc[2022]*100:.1f}% vs extrapolar {_ee/gasto.loc[2025]*100:.1f}%.")
    print("   Por eso barajar 'hace trampa': el test debe ir DESPUÉS en el tiempo.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2: estacionariedad (nivel vs diferenciada) ----
E2 = """## Ejercicio 02 · Estacionariedad y cambio porcentual
Compara la **estabilidad de la media** entre la primera y la segunda mitad de la serie, en el **nivel** y
en el **cambio porcentual** año a año.

- `ratio_nivel`: media de la 2ª mitad del **nivel** dividida por la media de la 1ª mitad del nivel.
- `dif_pct`: el cambio porcentual `gasto.pct_change().dropna()`.

Pista: `mitad = len(gasto) // 2`; usa `gasto.iloc[:mitad]` y `gasto.iloc[mitad:]`.

Elige en `conclusion` la interpretación correcta:
- **A.** `ratio_nivel` está cerca de 1: el nivel ya es estacionario, no hace falta transformarlo.
- **B.** `ratio_nivel` es claramente mayor que 1 (la media sube entre mitades): el nivel **no** es
  estacionario por la tendencia, y por eso pasar al **cambio porcentual** ayuda a estabilizarlo.
- **C.** El nivel es estacionario y el cambio porcentual no: transformarlo empeora todo."""
E2_TODO = """mitad = len(gasto) // 2
ratio_nivel = None   # TODO: media 2ª mitad del nivel / media 1ª mitad del nivel
dif_pct = None       # TODO: gasto.pct_change().dropna()
conclusion = None    # TODO: "A", "B" o "C"
"""
E2_SOL = """mitad = len(gasto) // 2
ratio_nivel = gasto.iloc[mitad:].mean() / gasto.iloc[:mitad].mean()
dif_pct = gasto.pct_change().dropna()
conclusion = "B"
"""
E2_CHK = """try:
    _m = len(gasto) // 2
    _ratio = gasto.iloc[_m:].mean() / gasto.iloc[:_m].mean()
    _dif = gasto.pct_change().dropna()
    _correcta = "B" if _ratio > 1.1 else "A"
    assert ratio_nivel is not None and abs(ratio_nivel - _ratio) < 0.01, f"ratio_nivel debería ser ~{_ratio:.2f}"
    assert dif_pct is not None and len(dif_pct) == len(_dif), "Revisa `dif_pct` (usa gasto.pct_change().dropna())."
    assert str(conclusion).strip().upper() == _correcta, "¿La media del nivel se mantiene estable entre mitades?"
    print(f"✅ Correcto. El nivel sube {_ratio:.2f}× entre mitades (media inestable = no estacionario).")
    print("   Pasar a 'cuánto MÁS gastamos en %' acerca la media entre mitades: eso estabiliza la serie.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3: baselines / walk-forward MAE naïve vs media móvil ----
E3 = """## Ejercicio 03 · ¿Le gana algo al baseline naïve?
Pronostica cada año con la info previa y compara, vía **error absoluto medio (MAE)**, el baseline
**naïve** (predecir con el año anterior) contra el **promedio móvil de 3 años**.

- `pred_naive = gasto.shift(1)`
- `pred_mm3 = gasto.shift(1).rolling(3).mean()`
- `mae_naive`: media de `abs(gasto - pred_naive)` (ignora los `NaN`).
- `mae_mm3`: media de `abs(gasto - pred_mm3)` (ignora los `NaN`).

Pista: `(gasto - pred_naive).abs().mean()` ya ignora los `NaN`.

Elige en `conclusion` la lectura correcta:
- **A.** `mae_naive` < `mae_mm3`: en esta serie con tendencia fuerte y al alza, el naïve le **gana** al
  promedio móvil, que va siempre atrasado. El naïve es una vara difícil de vencer.
- **B.** `mae_naive` > `mae_mm3`: el promedio móvil es mejor acá.
- **C.** Son exactamente iguales: el baseline no importa."""
E3_TODO = """pred_naive = None    # TODO: gasto.shift(1)
pred_mm3 = None      # TODO: gasto.shift(1).rolling(3).mean()
mae_naive = None     # TODO: (gasto - pred_naive).abs().mean()
mae_mm3 = None       # TODO: (gasto - pred_mm3).abs().mean()
conclusion = None    # TODO: "A", "B" o "C"
"""
E3_SOL = """pred_naive = gasto.shift(1)
pred_mm3 = gasto.shift(1).rolling(3).mean()
mae_naive = (gasto - pred_naive).abs().mean()
mae_mm3 = (gasto - pred_mm3).abs().mean()
conclusion = "A"
"""
E3_CHK = """try:
    _pn = gasto.shift(1)
    _pm = gasto.shift(1).rolling(3).mean()
    _mae_n = (gasto - _pn).abs().mean()
    _mae_m = (gasto - _pm).abs().mean()
    _correcta = "A" if _mae_n < _mae_m else "B"
    assert mae_naive is not None and abs(mae_naive - _mae_n) < 1, "Revisa mae_naive."
    assert mae_mm3 is not None and abs(mae_mm3 - _mae_m) < 1, "Revisa mae_mm3."
    assert str(conclusion).strip().upper() == _correcta, "¿Qué baseline tiene MENOR MAE en esta serie?"
    print(f"✅ Correcto. MAE naïve = {_mae_n/1e12:,.2f}  vs  MAE media móvil = {_mae_m/1e12:,.2f} billones.")
    print("   Con tendencia fuerte al alza, el naïve gana: el promedio móvil promedia años viejos y bajos.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4: incertidumbre crece con el horizonte ----
E4 = """## Ejercicio 04 · La incertidumbre crece con el horizonte
Usa el crecimiento medio `g = gasto.pct_change().mean()`, su desviación `sigma = gasto.pct_change().std()`
y el último valor `ult = gasto.loc[2025]`. El ancho de la banda de incertidumbre a horizonte `h` lo
aproximamos como `ult * (1+g)**h * sigma * sqrt(h)` (los errores se acumulan paso a paso).

- `ancho_1`: ancho de la banda a `h = 1`.
- `ancho_5`: ancho de la banda a `h = 5`.

Pista: `import numpy as np` ya está; usa `np.sqrt(h)`.

Elige en `conclusion` la interpretación correcta:
- **A.** `ancho_5` < `ancho_1`: pronosticar más lejos es más fácil y más preciso.
- **B.** `ancho_5` > `ancho_1`: la banda se **ensancha** con el horizonte; la incertidumbre se **acumula**,
  así que un pronóstico a 5 años es mucho menos confiable que a 1 año. Hay que reportar una banda, no una línea.
- **C.** `ancho_1` y `ancho_5` son iguales: el horizonte no afecta la incertidumbre."""
E4_TODO = """g = gasto.pct_change().mean()
sigma = gasto.pct_change().std()
ult = gasto.loc[2025]
ancho_1 = None    # TODO: ult * (1+g)**1 * sigma * np.sqrt(1)
ancho_5 = None    # TODO: ult * (1+g)**5 * sigma * np.sqrt(5)
conclusion = None # TODO: "A", "B" o "C"
"""
E4_SOL = """g = gasto.pct_change().mean()
sigma = gasto.pct_change().std()
ult = gasto.loc[2025]
ancho_1 = ult * (1 + g) ** 1 * sigma * np.sqrt(1)
ancho_5 = ult * (1 + g) ** 5 * sigma * np.sqrt(5)
conclusion = "B"
"""
E4_CHK = """try:
    _g = gasto.pct_change().mean()
    _s = gasto.pct_change().std()
    _u = gasto.loc[2025]
    _a1 = _u * (1 + _g) ** 1 * _s * np.sqrt(1)
    _a5 = _u * (1 + _g) ** 5 * _s * np.sqrt(5)
    _correcta = "B" if _a5 > _a1 else "A"
    assert ancho_1 is not None and abs(ancho_1 - _a1) < 1, "Revisa ancho_1 (h=1)."
    assert ancho_5 is not None and abs(ancho_5 - _a5) < 1, "Revisa ancho_5 (h=5)."
    assert str(conclusion).strip().upper() == _correcta, "¿La banda se ensancha o se angosta con el horizonte?"
    print(f"✅ Correcto. Banda a 1 año: ±{_a1/1e12:,.2f}  vs  a 5 años: ±{_a5/1e12:,.2f} billones.")
    print("   La incertidumbre se compone: pronosticar lejos es mucho menos confiable. Reporta una banda.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo construyes un pronóstico: entiendes **por qué la validación tiene que ser temporal** (barajar
es trampa: usa el futuro), cómo se descompone una serie en **tendencia + estacionalidad + ruido**, qué
significa la **estacionariedad** (y por qué *diferenciar* estabiliza), por qué un **baseline ingenuo** es
la vara sagrada, cómo se hace un **backtest walk-forward** honesto, y por qué la **incertidumbre crece**
con el horizonte.

La regla de oro que te llevas: **en el tiempo, nunca mires hacia adelante para evaluar hacia atrás, y
nunca prometas un número lejano sin una banda.** Eso distingue a quien *proyecta con rigor* de quien
*dibuja una línea bonita* y la presenta como certeza."""


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
