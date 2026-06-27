# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A6 (visualización y ética):
A6/profundiza.ipynb (estudiante) + A6/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A6-visualizacion-y-etica"

TITULO = """# A6 · Visualización y ética — Profundización (opcional) 🔬

**Formación Pública — Capa A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A6 y quieres entender el *porqué* —no solo
el *cómo*—, aquí vas a un nivel más hondo: por qué el ojo lee mejor unas formas que otras (**percepción
preatentiva**), cómo medir cuánto **miente** un gráfico (el ***lie factor*** de Tufte), por qué "menos
tinta es más" (***data-ink ratio*** y *chartjunk*), cómo el **color** deja gente afuera (daltonismo y
accesibilidad), y la trampa ética más sutil para la política pública: cómo un **agregado** esconde
desigualdad y por qué olvidar el **denominador** (las tasas base) lleva a conclusiones falsas.

Menos sintaxis nueva, más **pensamiento visual y ético**. Los ejercicios del final son más conceptuales.

> Requisito: haber hecho `leccion.ipynb` de A6. Mismo dataset: la matriz eléctrica de Chile
> (`generacion_fuentes.csv` y `generacion_renovable.csv`)."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

for archivo in ["generacion_fuentes.csv", "generacion_renovable.csv"]:
    if not os.path.exists(archivo):
        try:
            url = f"https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A6-visualizacion-y-etica/{archivo}"
            urllib.request.urlretrieve(url, archivo)
        except Exception:
            print(f"Si estás en Colab, sube {archivo} manualmente.")

fuentes = pd.read_csv("generacion_fuentes.csv")
renovable = pd.read_csv("generacion_renovable.csv")
print("Tabla 'fuentes':"); print(fuentes)
print("\\nTabla 'renovable':"); print(renovable)"""

S1 = """## 1. Percepción preatentiva: por qué las barras le ganan a la torta

Tu ojo no procesa todo un gráfico "pensando". Hay rasgos visuales que el cerebro detecta **antes de
prestar atención consciente**, en milisegundos y en paralelo: se llaman **atributos preatentivos**
(posición, longitud, color, tamaño, orientación). Mira una pantalla de números y busca el "7": tienes
que leerlos uno a uno. Pero si el "7" es rojo entre negros, **salta solo**. Eso es preatención.

Lo clave para nosotros: **no todos los atributos son igual de precisos para comparar cantidades.** El
**estadístico** William Cleveland (Cleveland & McGill, 1984) los ordenó por exactitud. Aquí va una
**versión simplificada**, de **más** a **menos** preciso (en el original de Cleveland hay más niveles
—p. ej. "posición en escalas no alineadas" y "volumen"— que omitimos por claridad):

- **Posición** sobre una escala común (puntos alineados en un eje) — el más preciso.
- **Longitud** (la altura de una barra).
- Pendiente / ángulo.
- Área.
- **Color / saturación** — el menos preciso para leer un número.

Una **barra** te pide comparar **longitudes alineadas**: facilísimo (está entre lo más preciso). Una
**torta** te pide comparar **ángulos y áreas**: tu ojo es malo para eso, sobre todo con muchas porciones
de tamaño parecido. Por eso, salvo casos muy simples, **una barra comunica mejor que una torta**. Veámoslo
con la matriz eléctrica: ¿puedes ordenar las fuentes de un vistazo en cada gráfico?"""

S1_CODE = """fig, (ax_torta, ax_barra) = plt.subplots(1, 2, figsize=(11, 4.5))

# Torta: comparar ángulos/áreas (difícil)
ax_torta.pie(fuentes["porcentaje"], labels=fuentes["fuente"], autopct="%1.0f%%")
ax_torta.set_title("Torta: ¿cuál es 2ª y cuál 3ª?")

# Barra ordenada: comparar longitudes alineadas (fácil)
orden = fuentes.sort_values("porcentaje", ascending=True)
ax_barra.barh(orden["fuente"], orden["porcentaje"], color="#0a7e7e")
ax_barra.set_title("Barras ordenadas: el orden salta solo")
ax_barra.set_xlabel("% de la generación")

plt.tight_layout(); plt.show()
print("En la torta cuesta distinguir Térmica (30) de Hidráulica (32). En la barra ordenada,")
print("el ranking es instantáneo: ese es el poder de comparar LONGITUDES sobre un eje común.")"""

S2 = """## 2. El *lie factor* de Tufte: cuánto miente un gráfico, en número

Edward Tufte, el referente de la visualización honesta, propuso una métrica para medir la distorsión:
el **factor de mentira** (*lie factor*).

$$\\text{lie factor} = \\frac{\\text{tamaño del efecto mostrado en el gráfico}}{\\text{tamaño del efecto en los datos}}$$

- Si vale **1**, el gráfico es honesto: la imagen crece lo mismo que los datos.
- Si es **mayor que 1**, **exagera** (típico del eje truncado que viste en la lección).
- Si es **menor que 1**, **minimiza** (esconde un cambio real).

El "tamaño del efecto" se mide como cambio **relativo**: `(valor_final − valor_inicial) / valor_inicial`.
Apliquémoslo al eje truncado del módulo. En los datos, lo renovable pasó de 56% a 70%. Pero si dibujas el
eje Y de 54 a 72 (como en el gráfico "engañoso" de la lección), la **barra/línea visible** crece mucho
más que el dato real. Pongámosle número a esa mentira.

> ⚠️ **Por qué el número saldrá tan grande (≈28).** El corte (54) queda **pegadísimo** al valor inicial
> (56): la altura visible del primer punto es de solo **2 unidades** (56 − 54). Como ese 2 es el
> denominador del "cambio visual", el factor se **dispara**. No es un error de cálculo: es justo el
> peligro del eje truncado. Cuanto más cerca pongas el corte del valor mínimo, más exagera el gráfico."""

S2_CODE = """v_ini, v_fin = renovable["pct_renovable"].iloc[0], renovable["pct_renovable"].iloc[-1]  # 56 -> 70

# Cambio REAL en los datos (relativo)
cambio_datos = (v_fin - v_ini) / v_ini

# Cambio que PERCIBE el ojo con el eje truncado de 54 a 72:
# la "altura visible" de cada punto es (valor - 54). El ojo compara esas alturas.
base = 54
cambio_visual = ((v_fin - base) - (v_ini - base)) / (v_ini - base)

lie_factor = cambio_visual / cambio_datos
print(f"Renovable: {v_ini}% -> {v_fin}%")
print(f"Cambio real en los datos:      {cambio_datos*100:.1f}%")
print(f"Cambio que aparenta el gráfico: {cambio_visual*100:.1f}%  (eje cortado en {base})")
print(f"\\nLIE FACTOR = {lie_factor:.1f}  -> el gráfico exagera la subida ~{lie_factor:.0f} veces.")
print(f"(Sale tan alto porque el corte {base} queda a solo {v_ini-base:.0f} unidades del valor inicial {v_ini}:")
print(" ese denominador minúsculo dispara el factor. Ese es el peligro del eje truncado.)")
print("Un lie factor honesto vale ~1. Cuanto más se aleja de 1, más distorsiona.")"""

S3 = """## 3. *Data-ink ratio* y *chartjunk*: menos tinta, más mensaje

Otra idea central de Tufte: la **razón dato-tinta** (*data-ink ratio*).

$$\\text{data-ink ratio} = \\frac{\\text{tinta que representa datos}}{\\text{tinta total del gráfico}}$$

Todo lo que dibujas pero **no aporta información** (fondos de colores, sombras 3D, rejillas pesadas,
bordes gruesos, degradados, *cliparts*) es **chartjunk**: ruido que compite con el dato. La meta es
**maximizar** la proporción de tinta que sí comunica. Regla práctica de Tufte: *"borra todo lo que
puedas borrar sin perder información"*.

Un gráfico recargado no es más "profesional"; es **más difícil de leer** y, en el Estado, da una
impresión de adorno por sobre rigor. Comparemos el mismo dato cargado de *chartjunk* contra una versión
limpia."""

S3_CODE = """fig, (ax_junk, ax_clean) = plt.subplots(1, 2, figsize=(11, 4.5))

# Recargado: chartjunk (rejilla densa, fondo, bordes gruesos, colores chillones)
ax_junk.set_facecolor("#ffe9b3")
ax_junk.bar(fuentes["fuente"], fuentes["porcentaje"],
            color=["red","lime","blue","magenta","cyan"], edgecolor="black", linewidth=3)
ax_junk.grid(True, which="both", color="gray", linewidth=1.5)
ax_junk.set_title("RECARGADO (mucho chartjunk)")
for s in ax_junk.spines.values():
    s.set_linewidth(3)

# Limpio: data-ink alto (sin marco superior/derecho, sin rejilla, un color sobrio)
ax_clean.bar(fuentes["fuente"], fuentes["porcentaje"], color="#0a7e7e")
ax_clean.set_title("LIMPIO (data-ink alto)")
ax_clean.spines["top"].set_visible(False)
ax_clean.spines["right"].set_visible(False)
ax_clean.set_ylabel("% de la generación")

plt.tight_layout(); plt.show()
print("Mismos datos. El de la derecha se lee más rápido: cada gota de tinta cuenta una parte del dato.")"""

S4 = """## 4. Color y accesibilidad: el gráfico que deja gente afuera

El color es el atributo **menos preciso** para leer cantidades (sección 1), pero además tiene un problema
de **equidad**: cerca del **8% de los hombres** (y ~0,5% de las mujeres) tiene algún tipo de **daltonismo**.
El más común es el **rojo-verde** (*deuteranopia/protanopia*): para esas personas, el rojo y el verde se
ven casi iguales. Un semáforo "rojo = malo / verde = bueno" en un dashboard puede ser **invisible** para
ellas.

En el sector público esto no es un detalle estético: es **accesibilidad**. Un informe oficial debe poder
leerlo todo el mundo. Buenas prácticas:

- **No codifiques información solo con color.** Agrega etiquetas, patrones o posición. Si quitas el color
  y el gráfico aún se entiende, vas bien.
- Evita la dupla **rojo/verde** para "malo/bueno". Prefiere paletas seguras (p. ej. **azul–naranjo**, que
  se distinguen aun con daltonismo).
- No uses **arcoíris** (*jet*) para escalas: confunde y no es perceptualmente uniforme.

Simulemos cómo "ve" un daltónico rojo-verde una paleta peligrosa frente a una segura.

> Nota técnica: la simulación de abajo es una **aproximación ilustrativa** (promediamos los canales rojo
> y verde), **no una simulación clínica exacta**. La simulación real usa transformaciones en el espacio
> de color LMS. Para captar la idea —rojo y verde se confunden— esta versión simple basta."""

S4_CODE = """def simula_daltonismo_rg(rgb):
    # Aproximación simple: en daltonismo rojo-verde, R y G se confunden -> los promediamos.
    r, g, b = rgb[0], rgb[1], rgb[2]
    rg = (r + g) / 2
    return (rg, rg, b)

paleta_mala = [(0.85, 0.0, 0.0), (0.0, 0.7, 0.0)]   # rojo y verde (peligrosa)
paleta_buena = [(0.0, 0.45, 0.74), (0.90, 0.50, 0.0)] # azul y naranjo (segura)

fig, axs = plt.subplots(2, 2, figsize=(9, 5))
for fila, (nombre, pal) in enumerate([("MALA: rojo/verde", paleta_mala),
                                       ("BUENA: azul/naranjo", paleta_buena)]):
    axs[fila,0].bar([0,1], [1,1], color=pal); axs[fila,0].set_title(f"{nombre} — visión normal")
    axs[fila,1].bar([0,1], [1,1], color=[simula_daltonismo_rg(c) for c in pal])
    axs[fila,1].set_title(f"{nombre} — daltonismo R-G")
    for ax in axs[fila]: ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout(); plt.show()
print("Arriba a la derecha: rojo y verde se vuelven CASI IGUALES -> la persona no distingue las series.")
print("Abajo: azul y naranjo siguen diferenciándose. Esa es una paleta accesible.")"""

S5 = """## 5. El agregado que esconde: un promedio puede ocultar desigualdad

Un solo número tranquiliza, pero puede **mentir por omisión**. "El 70% de la generación es renovable"
suena redondo y bueno. Pero un **promedio nacional** o un **total** puede esconder que el avance está
**muy repartido de forma desigual** entre regiones, grupos o servicios.

Esto enlaza con A5 (la media engaña con datos sesgados), pero el ángulo aquí es **visual y ético**: el
gráfico de un **agregado** —una sola barra grande, un único KPI— *invisibiliza* a quien quedó atrás. La
defensa es **desagregar**: mostrar la distribución, no solo el resumen.

Ejemplo **ilustrativo** (datos inventados para mostrar el fenómeno): imagina que ese 70% renovable
nacional se reparte de forma muy distinta por región. El promedio es 70, pero hay regiones rezagadas.
Veámoslo: un solo número vs. la realidad desagregada."""

S5_CODE = """# Ejemplo ILUSTRATIVO (regiones y cifras inventadas para mostrar el punto)
regiones = pd.DataFrame({
    "region": ["Norte", "Centro", "Sur", "Austral", "RM"],
    "pct_renovable": [95, 70, 78, 88, 19],   # promedio = 70, pero RM muy rezagada
})
promedio = regiones["pct_renovable"].mean()

fig, (ax_agg, ax_des) = plt.subplots(1, 2, figsize=(11, 4.5))
ax_agg.bar(["País"], [promedio], color="#0a7e7e")
ax_agg.set_ylim(0, 100); ax_agg.set_title(f"AGREGADO: '{promedio:.0f}% renovable' (tranquilizador)")
ax_agg.set_ylabel("% renovable")

ax_des.bar(regiones["region"], regiones["pct_renovable"], color="#0a7e7e")
ax_des.axhline(promedio, color="crimson", linestyle="--", label=f"Promedio {promedio:.0f}%")
ax_des.set_ylim(0, 100); ax_des.set_title("DESAGREGADO: la RM está MUY atrás")
ax_des.set_ylabel("% renovable"); ax_des.legend()

plt.tight_layout(); plt.show()
print(f"El promedio ({promedio:.0f}%) es idéntico en ambos, pero solo el desagregado revela")
print("que una región quedó en 19%. Un agregado tranquiliza; desagregar muestra la desigualdad.")"""

S6 = """## 6. El descuido del denominador: tasas base, no números crudos

La trampa ética más común con datos públicos: comparar **números absolutos** sin dividir por el
**tamaño** del grupo. Es el **descuido del denominador** (o de la **tasa base**).

"La región X tuvo el doble de cortes de luz que la región Y" suena alarmante… hasta que recuerdas que X
tiene **cinco veces más** clientes. Por cliente, X anda **mejor**. El número crudo (el numerador) no
significa nada sin su **denominador** (la población, los clientes, el total de casos).

Regla de oro para todo informe público: **¿esto debería ir como tasa, no como conteo?** Casi siempre la
respuesta es sí. Comparar conteos entre grupos de distinto tamaño es comparar peras con camiones.

Ejemplo **ilustrativo**: dos regiones, sus cortes de luz y sus clientes. Mira cómo cambia la conclusión
al pasar del conteo crudo a la **tasa por cada 1.000 clientes**."""

S6_CODE = """# Ejemplo ILUSTRATIVO (datos inventados)
cortes = pd.DataFrame({
    "region": ["Region X", "Region Y"],
    "cortes": [800, 400],          # X tiene el DOBLE de cortes (numerador)
    "clientes": [2_000_000, 400_000],  # pero X tiene MUCHOS más clientes (denominador)
})
cortes["tasa_x1000"] = cortes["cortes"] / cortes["clientes"] * 1000

fig, (ax_crudo, ax_tasa) = plt.subplots(1, 2, figsize=(11, 4.5))
ax_crudo.bar(cortes["region"], cortes["cortes"], color="crimson")
ax_crudo.set_title("CONTEO CRUDO: 'X tiene el doble de cortes'")
ax_crudo.set_ylabel("N° de cortes")

ax_tasa.bar(cortes["region"], cortes["tasa_x1000"], color="#0a7e7e")
ax_tasa.set_title("TASA por 1.000 clientes: ¡X anda MEJOR!")
ax_tasa.set_ylabel("Cortes por 1.000 clientes")

plt.tight_layout(); plt.show()
print(cortes.to_string(index=False))
print("\\nEn crudo X parece peor (800 vs 400). Por cliente, X tiene 0,4 y Y tiene 1,0:")
print("Y está peor. Sin el denominador, la conclusión se invierte.")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Usar torta con muchas categorías parecidas.** El ojo compara mal ángulos y áreas; usa barras ordenadas.
- **Truncar el eje y creer que "se ve mejor".** Mide el *lie factor*: si se aleja de 1, estás distorsionando.
- **Recargar el gráfico** (3D, sombras, rejillas, colores chillones). El *chartjunk* baja el data-ink ratio y entorpece la lectura.
- **Codificar información solo con color** (y peor, rojo/verde). Deja afuera a personas con daltonismo; agrega etiquetas o posición.
- **Reportar solo el agregado.** Un promedio o total puede esconder desigualdad; desagrega.
- **Comparar conteos crudos entre grupos de distinto tamaño.** Casi siempre debe ser una **tasa** (ojo con el denominador)."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan, otros piden **elegir la interpretación correcta**.
Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 lie factor
E1 = """## Ejercicio 01 · Mide la mentira (lie factor)
Un gráfico dibuja la participación renovable con el eje Y **truncado en 50** (en vez de empezar en 0).

> Nota: aquí usamos un corte **distinto** al de la sección 2 (que cortaba en **54** y daba lie factor ≈ 28).
> Con corte en **50** el margen visible es mayor (6 unidades en vez de 2), así que el factor saldrá más
> moderado (≈ 9). Practicas la misma fórmula en otro escenario; por eso el número no coincidirá con la sección 2.

Con los datos reales de `renovable` (56% en el primer año, 70% en el último):

- Guarda en `cambio_datos` el cambio **relativo real**: `(v_fin - v_ini) / v_ini`.
- Guarda en `cambio_visual` el cambio **aparente** con base 50: `((v_fin-50) - (v_ini-50)) / (v_ini-50)`.
- Guarda en `lie_factor` = `cambio_visual / cambio_datos`.
- Elige en `conclusion` (letra):
  - **A.** El lie factor es ~1: el gráfico es honesto.
  - **B.** El lie factor es bastante mayor que 1: el gráfico **exagera** la subida.
  - **C.** El lie factor es menor que 1: el gráfico minimiza la subida."""
E1_TODO = """v_ini = renovable["pct_renovable"].iloc[0]
v_fin = renovable["pct_renovable"].iloc[-1]
cambio_datos = None   # TODO: (v_fin - v_ini) / v_ini
cambio_visual = None  # TODO: ((v_fin-50) - (v_ini-50)) / (v_ini-50)
lie_factor = None     # TODO: cambio_visual / cambio_datos
conclusion = None     # TODO: "A", "B" o "C"
"""
E1_SOL = """v_ini = renovable["pct_renovable"].iloc[0]
v_fin = renovable["pct_renovable"].iloc[-1]
cambio_datos = (v_fin - v_ini) / v_ini
cambio_visual = ((v_fin-50) - (v_ini-50)) / (v_ini-50)
lie_factor = cambio_visual / cambio_datos
conclusion = "B"
"""
E1_CHK = """try:
    _vi = renovable["pct_renovable"].iloc[0]; _vf = renovable["pct_renovable"].iloc[-1]
    _cd = (_vf - _vi) / _vi
    _cv = ((_vf-50) - (_vi-50)) / (_vi-50)
    _lf = _cv / _cd
    _correcta = "B" if _lf > 1.5 else ("C" if _lf < 0.67 else "A")
    assert cambio_datos is not None and abs(cambio_datos - _cd) < 1e-6, "Revisa cambio_datos"
    assert cambio_visual is not None and abs(cambio_visual - _cv) < 1e-6, "Revisa cambio_visual"
    assert lie_factor is not None and abs(lie_factor - _lf) < 1e-6, "Revisa lie_factor"
    assert str(conclusion).strip().upper() == _correcta, "¿El gráfico exagera o minimiza? Mira si lie_factor>1"
    print(f"✅ Correcto. Lie factor = {_lf:.1f}: el eje truncado exagera la subida ~{_lf:.0f} veces.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 percepción / torta vs barra (conceptual con cálculo)
E2 = """## Ejercicio 02 · Por qué la torta cuesta (atributos preatentivos)
En la tabla `fuentes`, identifica las dos fuentes más grandes y qué tan **parecidas** son.

- Guarda en `top2` los porcentajes de las **dos fuentes más grandes** (una lista o serie de 2 números),
  por ejemplo con `fuentes.nlargest(2, "porcentaje")["porcentaje"]`.
- Guarda en `diferencia` la diferencia absoluta entre esos dos porcentajes.
- Elige en `conclusion` (letra):
  - **A.** La diferencia es grande (≥10 puntos): da igual usar torta, se distinguen fácil.
  - **B.** La diferencia es pequeña (<10 puntos): en una **torta** esos ángulos casi no se distinguen;
    una **barra** (comparar longitudes) lo deja claro.
  - **C.** No se puede saber sin ver el gráfico."""
E2_TODO = """top2 = None        # TODO: porcentajes de las 2 fuentes más grandes
diferencia = None  # TODO: diferencia absoluta entre esos dos porcentajes
conclusion = None  # TODO: "A", "B" o "C"
"""
E2_SOL = """top2 = fuentes.nlargest(2, "porcentaje")["porcentaje"]
diferencia = abs(top2.iloc[0] - top2.iloc[1])
conclusion = "B"
"""
E2_CHK = """try:
    _t2 = fuentes.nlargest(2, "porcentaje")["porcentaje"]
    _dif = abs(_t2.iloc[0] - _t2.iloc[1])
    _correcta = "B" if _dif < 10 else "A"
    assert top2 is not None, "Falta definir top2 (los 2 porcentajes más grandes)"
    _vals = list(top2.values) if hasattr(top2, "values") else list(top2)
    assert diferencia is not None and abs(diferencia - _dif) < 1e-6, f"La diferencia debería ser {_dif}"
    assert sorted([float(x) for x in _vals]) == sorted([float(x) for x in _t2.values]), "Revisa top2"
    assert str(conclusion).strip().upper() == _correcta, "¿La diferencia es <10? Entonces la torta confunde"
    print(f"✅ Correcto. Las dos mayores difieren en solo {_dif} puntos: en torta casi no se distinguen.")
    print("   Comparar longitudes (barras) es el atributo preatentivo más preciso.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 agregado vs desagregado
E3 = """## Ejercicio 03 · El agregado que esconde
Vuelve al ejemplo ilustrativo de la sección 5 (regiones inventadas). Reconstruye la tabla y calcula:

- Guarda en `promedio` el promedio de `pct_renovable` de las regiones.
- Guarda en `minimo` el **mínimo** (la región más rezagada).
- Guarda en `brecha` = `promedio - minimo`.
- Elige en `conclusion` (letra):
  - **A.** La brecha es chica (<15 puntos): el promedio describe bien a todas las regiones.
  - **B.** La brecha es grande (≥15 puntos): el promedio **esconde** que una región quedó muy atrás;
    hay que **desagregar**.
  - **C.** El promedio y el mínimo siempre son iguales."""
E3_TODO = """regiones = pd.DataFrame({
    "region": ["Norte", "Centro", "Sur", "Austral", "RM"],
    "pct_renovable": [95, 70, 78, 88, 19],
})
promedio = None    # TODO: promedio de pct_renovable
minimo = None      # TODO: mínimo de pct_renovable
brecha = None      # TODO: promedio - minimo
conclusion = None  # TODO: "A", "B" o "C"
"""
E3_SOL = """regiones = pd.DataFrame({
    "region": ["Norte", "Centro", "Sur", "Austral", "RM"],
    "pct_renovable": [95, 70, 78, 88, 19],
})
promedio = regiones["pct_renovable"].mean()
minimo = regiones["pct_renovable"].min()
brecha = promedio - minimo
conclusion = "B"
"""
E3_CHK = """try:
    _reg = pd.DataFrame({"region":["Norte","Centro","Sur","Austral","RM"],
                         "pct_renovable":[95,70,78,88,19]})
    _prom = _reg["pct_renovable"].mean(); _min = _reg["pct_renovable"].min()
    _brecha = _prom - _min
    _correcta = "B" if _brecha >= 15 else "A"
    assert promedio is not None and abs(promedio - _prom) < 1e-6, "Revisa el promedio"
    assert minimo is not None and abs(minimo - _min) < 1e-6, "Revisa el mínimo"
    assert brecha is not None and abs(brecha - _brecha) < 1e-6, "Revisa la brecha"
    assert str(conclusion).strip().upper() == _correcta, "¿La brecha es ≥15? Entonces el agregado esconde"
    print(f"✅ Correcto. Promedio {_prom:.0f}%, pero la peor región está en {_min}%: brecha de {_brecha:.0f} puntos.")
    print("   El agregado tranquiliza; desagregar revela la desigualdad.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 denominador / tasa base
E4 = """## Ejercicio 04 · No olvides el denominador (tasa base)
Dos regiones y sus cortes de luz (ejemplo ilustrativo de la sección 6). Calcula la **tasa por cada
1.000 clientes** y compara.

- Construye la tabla `cortes` (abajo) y agrega la columna `tasa` = `cortes / clientes * 1000`.
- Guarda en `tasa_x` la tasa de "Region X" y en `tasa_y` la de "Region Y".
- Elige en `conclusion` (letra):
  - **A.** X tiene más cortes en crudo, así que X está peor: el conteo basta.
  - **B.** Por cada 1.000 clientes, X tiene **menos** cortes que Y: ajustando por tamaño, **X está mejor**.
    El número crudo engañaba por ignorar el denominador.
  - **C.** No se pueden comparar dos regiones distintas.

*(Opcional, no se corrige): en `reflexion` escribe otra cifra pública que solo tenga sentido como tasa.)*"""
E4_TODO = """cortes = pd.DataFrame({
    "region": ["Region X", "Region Y"],
    "cortes": [800, 400],
    "clientes": [2_000_000, 400_000],
})
cortes["tasa"] = None  # TODO: cortes / clientes * 1000
tasa_x = None          # TODO: tasa de Region X
tasa_y = None          # TODO: tasa de Region Y
conclusion = None      # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """cortes = pd.DataFrame({
    "region": ["Region X", "Region Y"],
    "cortes": [800, 400],
    "clientes": [2_000_000, 400_000],
})
cortes["tasa"] = cortes["cortes"] / cortes["clientes"] * 1000
tasa_x = cortes.loc[cortes["region"] == "Region X", "tasa"].iloc[0]
tasa_y = cortes.loc[cortes["region"] == "Region Y", "tasa"].iloc[0]
conclusion = "B"
reflexion = "El número de delitos por comuna: sin dividir por población no se puede comparar."
"""
E4_CHK = """try:
    _c = pd.DataFrame({"region":["Region X","Region Y"],"cortes":[800,400],"clientes":[2_000_000,400_000]})
    _c["tasa"] = _c["cortes"] / _c["clientes"] * 1000
    _tx = _c.loc[_c["region"]=="Region X","tasa"].iloc[0]
    _ty = _c.loc[_c["region"]=="Region Y","tasa"].iloc[0]
    _correcta = "B" if _tx < _ty else "A"
    assert tasa_x is not None and abs(tasa_x - _tx) < 1e-6, f"tasa_x debería ser {_tx}"
    assert tasa_y is not None and abs(tasa_y - _ty) < 1e-6, f"tasa_y debería ser {_ty}"
    assert str(conclusion).strip().upper() == _correcta, "Compara las TASAS, no los conteos crudos"
    print(f"✅ Correcto. Tasa X = {_tx:.1f} y tasa Y = {_ty:.1f} por 1.000 clientes.")
    print("   En crudo X parecía peor; por cliente, X está mejor. El denominador lo cambia todo.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo dibujas gráficos: entiendes **por qué** unos comunican mejor que otros (**percepción
preatentiva**), sabes **medir** cuánto distorsiona un gráfico (***lie factor***), por qué conviene
**limpiar** la tinta (*data-ink*), cómo hacer gráficos **accesibles** (color y daltonismo), y reconoces
las dos trampas éticas que más daño hacen en decisiones públicas: el **agregado** que esconde desigualdad
y el **denominador** olvidado (tasas base).

La regla de oro que te llevas: **antes de mostrar un dato, pregúntate si tu gráfico ayuda a ver la
verdad o la disfraza —y si deja a alguien afuera.** Eso distingue a quien *informa* de quien *persuade
a la fuerza*."""


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
