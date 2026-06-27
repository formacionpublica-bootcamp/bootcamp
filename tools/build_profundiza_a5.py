# -*- coding: utf-8 -*-
"""Construye el notebook OPCIONAL de profundización teórica de A5 (estadística):
A5/profundiza.ipynb (estudiante) + A5/profundiza_solucion.ipynb (resuelto)."""
import json, os

BASE = "A5-estadistica-descriptiva"

TITULO = """# A5 · Estadística — Profundización (opcional) 🔬

**Formación Pública — Capa A · Datos sin miedo · Notebook de profundización**

Este cuaderno es **opcional**. Si ya hiciste la lección de A5 y quieres entender el *porqué* —no solo
el *cómo*—, aquí vas a un nivel más hondo: por qué la media se "rompe" y la mediana no, qué mide de
verdad la desviación estándar, cómo leer la **forma** de una distribución, cómo detectar *outliers*
con un criterio, qué te dice (y qué **no**) una muestra, y la trampa más peligrosa para la política
pública: confundir **correlación con causalidad** (y la paradoja de Simpson).

Menos sintaxis nueva, más **pensamiento estadístico**. Los ejercicios del final son más conceptuales.

> Requisito: haber hecho `leccion.ipynb` de A5. Mismo dataset: 30 comunas del Censo 2024 (INE)."""

CARGA = """import os, urllib.request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if not os.path.exists("comunas.csv"):
    try:
        url = "https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/A5-estadistica-descriptiva/comunas.csv"
        urllib.request.urlretrieve(url, "comunas.csv")
    except Exception:
        print("Si estás en Colab, sube comunas.csv manualmente.")

df = pd.read_csv("comunas.csv")
pob = df["poblacion"]
print(f"{len(df)} comunas | media {pob.mean():,.0f} | mediana {pob.median():,.0f}")"""

S1 = """## 1. Robustez: por qué la media se "rompe" y la mediana no

En la lección viste que con datos sesgados la media se infla. Aquí está el **porqué**:

- La **media** se calcula **sumando** todos los valores. Cada dato empuja el promedio en proporción a
  su tamaño: un valor enorme tiene mucha "palanca". Si una sola comuna creciera al infinito, la media
  crecería al infinito con ella.
- La **mediana** solo depende del **orden** (es el valor del medio). El valor más grande sigue siendo
  el más grande lo agrandes cuanto lo agrandes: la mediana **no se mueve**.

Los estadísticos llaman a esto **punto de quiebre** (*breakdown point*): cuántos datos "malos" toleran
antes de dar un resultado absurdo. La media tiene punto de quiebre de **un solo dato** (≈0% del total: basta un extremo para arruinarla);
la mediana, del **50%** (tendría que corromperse la mitad de los datos para moverla). Veámoslo en acción."""

S1_CODE = """# Tomamos la comuna más grande y la hacemos 10 veces más grande (un dato "extremo")
pob_alterada = pob.copy()
idx_max = pob.idxmax()
pob_alterada.loc[idx_max] = pob.loc[idx_max] * 10

print(f"Media original:  {pob.mean():,.0f}   ->  alterada: {pob_alterada.mean():,.0f}")
print(f"Mediana original:{pob.median():,.0f}   ->  alterada: {pob_alterada.median():,.0f}")
print("\\nLa media se disparó; la mediana ni se inmutó. Eso es robustez.")"""

S2 = """## 2. Varianza, desviación estándar y coeficiente de variación

La **desviación estándar** (DE) mide cuánto se alejan, en promedio, los datos de la media. Su receta:

1. A cada dato le restas la media (su "alejamiento").
2. **Elevas al cuadrado** cada alejamiento. ¿Por qué? Por dos razones: (a) así los alejamientos hacia
   abajo (negativos) no **cancelan** a los de hacia arriba (positivos); (b) penaliza **más** los
   alejamientos grandes (un dato muy lejos pesa mucho). Ese promedio de cuadrados es la **varianza**.
   (El valor absoluto también evitaría las cancelaciones; se eleva al cuadrado porque tiene propiedades
   matemáticas que facilitan los cálculos, y por eso es el camino estándar de la estadística.)
3. Le sacas raíz cuadrada para volver a las **unidades originales** (habitantes): eso es la DE.

> Detalle fino: pandas divide por `n-1` (no `n`) al calcular `.std()` de una **muestra** (corrección
> de Bessel). Con 30 datos casi no cambia, pero es por qué el resultado puede diferir de "dividir por n".

**El problema de comparar dispersiones a distinta escala:** una DE de 200.000 habitantes ¿es mucho?
Depende del tamaño típico. El **coeficiente de variación** (CV = DE / media) vuelve la dispersión
**relativa** y sin unidades, para comparar peras con manzanas."""

S2_CODE = """varianza = pob.var()
de = pob.std()
cv = pob.std() / pob.mean()
print(f"Varianza:               {varianza:,.0f}  (en 'habitantes al cuadrado', poco intuitiva)")
print(f"Desviación estándar:    {de:,.0f} habitantes")
print(f"Coeficiente de variación: {cv:.2f}  (DE relativa a la media)")
print("\\nUn CV alto (> ~0.5) indica datos MUY dispersos respecto a su propia media:")
print("acá conviven comunas de pocos miles con otras de más de medio millón.")"""

S3 = """## 3. La forma importa: asimetría (*skew*)

Dos columnas pueden tener la misma media y la misma DE y verse **completamente distintas**. La
**forma** de la distribución importa. La más común en datos públicos es el **sesgo a la derecha**
(*right-skew*): muchos valores chicos y una **cola larga** de pocos valores grandes (ingresos,
poblaciones, montos de compra…).

Regla práctica (válida en la gran mayoría de los casos reales —poblaciones, ingresos, montos—, aunque existen excepciones teóricas):
- **media ≈ mediana** → aproximadamente **simétrica**.
- **media > mediana** → **sesgo a la derecha** (la cola larga de grandes tira la media hacia arriba).
- **media < mediana** → sesgo a la izquierda.

El histograma lo muestra de un vistazo: el eje horizontal son rangos de población, las barras cuántas
comunas caen en cada rango."""

S3_CODE = """fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(pob, bins=12, color="#0a7e7e", edgecolor="white")
ax.axvline(pob.mean(), color="crimson", linestyle="--", label=f"Media {pob.mean():,.0f}")
ax.axvline(pob.median(), color="navy", linestyle="-", label=f"Mediana {pob.median():,.0f}")
ax.set_title("Distribución de población de las comunas (Censo 2024)")
ax.set_xlabel("Habitantes"); ax.set_ylabel("N° de comunas"); ax.legend()
plt.tight_layout(); plt.show()

print(f"Coeficiente de asimetría (skew): {pob.skew():.2f}  (>0 = cola a la derecha)")"""

S4 = """## 4. *Outliers* con criterio: la regla del IQR

"Outlier" no es "el dato que no me gusta". Hay un criterio estándar basado en los cuartiles:

- **IQR (rango intercuartílico)** = Q3 − Q1: el ancho de la mitad central de los datos.
- Se consideran *outliers* los valores por **encima de Q3 + 1,5 × IQR** o por **debajo de Q1 − 1,5 × IQR**.

Ese "1,5 × IQR" es la regla clásica detrás del **diagrama de caja** (*boxplot*): la caja va de Q1 a Q3,
la línea del medio es la mediana, los "bigotes" llegan hasta el **dato más extremo que aún cae dentro**
del umbral (Q3 + 1,5 × IQR hacia arriba, Q1 − 1,5 × IQR hacia abajo), y los puntos más allá del umbral
son los *outliers*, marcados uno a uno. Un *outlier* **no es un error**: puede ser un dato real importantísimo (Puente Alto es una
comuna real, no una equivocación). El criterio solo te dice **a qué mirar con atención**."""

S4_CODE = """q1, q3 = pob.quantile(0.25), pob.quantile(0.75)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
outliers = df[df["poblacion"] > limite_superior]
print(f"Q1={q1:,.0f}  Q3={q3:,.0f}  IQR={iqr:,.0f}")
print(f"Límite superior (Q3 + 1.5·IQR): {limite_superior:,.0f}")
print(f"Comunas marcadas como outliers ({len(outliers)}):")
print(outliers[["comuna", "poblacion"]].to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 2.5))
ax.boxplot(pob, vert=False)
ax.set_title("Boxplot de población (la caja = mitad central; puntos = outliers)")
ax.set_xlabel("Habitantes"); plt.tight_layout(); plt.show()"""

S5 = """## 5. Muestra vs población: lo que estos 30 datos NO te dicen

Trabajamos con **30 comunas**, no con las 345 del país. Eso es una **muestra**. Y toda muestra trae
**incertidumbre**: si hubieras elegido otras 30 comunas, la media habría dado distinto. A esa
fluctuación se le llama **variabilidad muestral**.

Implicancias prácticas para un funcionario:
- Un promedio calculado sobre una muestra es una **estimación**, no una verdad exacta. Reportarlo como
  cifra final y precisa puede inducir a error.
- Mientras **más pequeña** la muestra, **más inestable** la estimación. Con 5 comunas, un solo dato
  manda; con miles, los extremos se diluyen.
- Cómo se **eligió** la muestra importa tanto como su tamaño: una muestra sesgada (p. ej. solo comunas
  grandes) da una foto sesgada por más datos que tenga.

Lo veremos con un experimento: tomar submuestras al azar y ver cómo baila la media."""

S5_CODE = """rng = np.random.default_rng(42)
print("Media de 6 submuestras de 5 comunas cada una (mira cómo varía):")
for i in range(6):
    sub = pob.sample(5, random_state=rng.integers(1_000_000))
    print(f"  Submuestra {i+1}: media = {sub.mean():,.0f}")
print(f"\\nMedia de las 30 comunas (más estable): {pob.mean():,.0f}")
print("Con pocas comunas, la media salta muchísimo: esa es la variabilidad muestral.")"""

S6 = """## 6. La trampa mayor: correlación ≠ causalidad (y la paradoja de Simpson)

Que dos cosas **se muevan juntas** (correlación) no significa que una **cause** la otra. Casi siempre
hay un tercer factor escondido, el **confusor**, moviendo a ambas. Ejemplo: las comunas con más
bomberos tienen más incendios — no porque los bomberos causen incendios, sino porque ambas crecen con
el **tamaño** de la comuna (el confusor).

La versión más traicionera es la **paradoja de Simpson**: una tendencia que aparece **dentro de cada
grupo** puede **invertirse** al juntar todos los datos. Es un peligro real al comparar servicios u
organismos con un solo número agregado. Veámoslo con un ejemplo ilustrativo de dos servicios públicos
que resuelven solicitudes (casos *simples* y *complejos*):"""

S6_CODE = """# Ejemplo ILUSTRATIVO (datos inventados para mostrar el fenómeno)
simpson = pd.DataFrame({
    "servicio":   ["A", "A", "B", "B"],
    "tipo_caso":  ["simple", "complejo", "simple", "complejo"],
    "aprobadas":  [90, 40, 19, 90],
    "total":      [100, 100, 20, 180],
})
simpson["tasa"] = (simpson["aprobadas"] / simpson["total"] * 100).round(1)
print("Por tipo de caso:")
print(simpson.to_string(index=False))

glob = simpson.groupby("servicio").apply(lambda g: g["aprobadas"].sum() / g["total"].sum() * 100, include_groups=False).round(1)
print("\\nTasa GLOBAL por servicio:")
print(glob.to_string())
print("\\n¡Paradoja! B es mejor en simples (95%>90%) Y en complejos (50%>40%),")
print("pero A gana en el total. Razón: B atendió muchos más casos complejos (difíciles).")"""

ERRORES = """## ⚠️ Errores típicos (nivel profundización)
- **Tratar un *outlier* como error y borrarlo.** A veces es el dato más importante. Investiga antes de eliminar.
- **Comparar dispersiones con la DE cruda entre grupos de distinta escala.** Usa el **coeficiente de variación**.
- **Reportar un estadístico de muestra como verdad exacta.** Es una estimación con incertidumbre.
- **Saltar de correlación a causalidad.** Pregunta siempre: ¿qué **confusor** podría explicar ambas?
- **Comparar organismos con un solo número agregado.** Revisa por subgrupos: la paradoja de Simpson acecha."""

EJ_HEADER = """---
# 🛠️ Ejercicios de profundización
Más conceptuales que de costumbre: algunos calculan, otros piden **elegir la interpretación correcta**.
Completa cada `TODO` y ejecuta la celda de chequeo."""

# ---- E1 robustez
E1 = """## Ejercicio 01 · Robustez en números
Usa `pob_alterada` (la población con la comuna más grande ×10, ya creada en la sección 1).

- Guarda en `media_alt` la media de `pob_alterada` y en `mediana_alt` su mediana.
- Luego elige en `conclusion` (letra) la lectura correcta:
  - **A.** Tanto la media como la mediana cambiaron mucho.
  - **B.** La media cambió mucho pero la mediana casi no se movió: la mediana es robusta a extremos.
  - **C.** La mediana cambió mucho pero la media casi no se movió."""
E1_TODO = """media_alt = None      # TODO: media de pob_alterada
mediana_alt = None    # TODO: mediana de pob_alterada
conclusion = None     # TODO: "A", "B" o "C"
"""
E1_SOL = """media_alt = pob_alterada.mean()
mediana_alt = pob_alterada.median()
conclusion = "B"
"""
E1_CHK = """try:
    _ma, _meda = pob_alterada.mean(), pob_alterada.median()
    _cambio_media = abs(_ma - pob.mean())
    _cambio_mediana = abs(_meda - pob.median())
    _correcta = "B" if _cambio_media > _cambio_mediana else "A"
    assert media_alt is not None and abs(media_alt - _ma) < 1, "Revisa media_alt"
    assert mediana_alt is not None and abs(mediana_alt - _meda) < 1, "Revisa mediana_alt"
    assert str(conclusion).strip().upper() == _correcta, "Revisa qué medida casi no cambió"
    print("✅ Correcto. La mediana apenas se movió: es robusta a los extremos.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E2 CV
E2 = """## Ejercicio 02 · Dispersión relativa (coeficiente de variación)
- Calcula `cv` = desviación estándar dividida por la media de `pob`.
- Elige en `conclusion` la interpretación correcta:
  - **A.** `cv` es muy bajo (< 0,1): las comunas son de tamaño muy parecido.
  - **B.** `cv` es alto (> 0,5): hay una dispersión enorme relativa a la media (tamaños muy distintos).
  - **C.** `cv` no se puede interpretar sin las unidades."""
E2_TODO = """cv = None           # TODO: pob.std() / pob.mean()
conclusion = None   # TODO: "A", "B" o "C"
"""
E2_SOL = """cv = pob.std() / pob.mean()
conclusion = "B"
"""
E2_CHK = """try:
    _cv = pob.std() / pob.mean()
    _correcta = "B" if _cv > 0.5 else "A"
    assert cv is not None and abs(cv - _cv) < 0.01, f"cv debería ser ~{_cv:.2f}"
    assert str(conclusion).strip().upper() == _correcta, "Revisa la interpretación del CV"
    print(f"✅ Correcto. CV = {_cv:.2f}: dispersión enorme relativa a la media.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E3 outliers IQR
E3 = """## Ejercicio 03 · Outliers con la regla del IQR
- Calcula `iqr` (Q3 − Q1) y `limite_superior` (Q3 + 1,5 × IQR) de `pob`.
- Guarda en `n_outliers` cuántas comunas superan ese `limite_superior`.

Pista: `pob.quantile(0.25)`, `pob.quantile(0.75)`, y `(pob > limite_superior).sum()`."""
E3_TODO = """iqr = None              # TODO: Q3 - Q1
limite_superior = None  # TODO: Q3 + 1.5 * IQR
n_outliers = None       # TODO: cuántas comunas superan el límite
"""
E3_SOL = """q1, q3 = pob.quantile(0.25), pob.quantile(0.75)
iqr = q3 - q1
limite_superior = q3 + 1.5 * iqr
n_outliers = int((pob > limite_superior).sum())
"""
E3_CHK = """try:
    _q1, _q3 = pob.quantile(0.25), pob.quantile(0.75)
    _iqr = _q3 - _q1
    _lim = _q3 + 1.5 * _iqr
    _n = int((pob > _lim).sum())
    assert iqr is not None and abs(iqr - _iqr) < 1, "Revisa el IQR"
    assert limite_superior is not None and abs(limite_superior - _lim) < 1, "Revisa el límite superior"
    assert int(n_outliers) == _n, f"Deberían ser {_n} outliers por encima del límite"
    print(f"✅ Correcto. {_n} comuna(s) superan Q3+1.5·IQR: a esas hay que mirarlas aparte.")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir una variable:", e)"""

# ---- E4 Simpson / causalidad (conceptual)
E4 = """## Ejercicio 04 · Correlación, causalidad y Simpson (conceptual)
Vuelve al ejemplo de los servicios A y B de la sección 6: **B tiene mejor tasa en los casos simples
Y en los complejos**, pero **A tiene mejor tasa global**. Un directivo concluye: *"A es mejor que B,
hay que premiar a A"*.

Elige en `conclusion` la lectura correcta:
- **A.** El directivo tiene razón: el número global manda.
- **B.** Hay paradoja de Simpson: B es mejor en cada tipo de caso; A gana en el total **solo** porque
  atendió más casos fáciles. Comparar con el agregado, sin mirar el tipo de caso (el confusor), es engañoso.
- **C.** Los datos están mal: es imposible que B sea mejor en cada grupo y peor en el total.

*(Opcional, no se corrige): en `reflexion` escribe qué información extra pedirías antes de "premiar" a un servicio.)*"""
E4_TODO = """conclusion = None   # TODO: "A", "B" o "C"
reflexion = ""
"""
E4_SOL = """conclusion = "B"
reflexion = "Pediría la distribución de tipos de caso por servicio y compararía tasas dentro de cada tipo."
"""
E4_CHK = """try:
    assert conclusion is not None, "Aún no elegiste una letra en 'conclusion'."
    assert str(conclusion).strip().upper() == "B", "Pista: ¿puede un agregado invertir lo que pasa en cada grupo?"
    print("✅ Correcto. Eso es la paradoja de Simpson: el agregado escondía el confusor (tipo de caso).")
except AssertionError as e:
    print("❌ Aún no:", e)
except NameError as e:
    print("❌ Falta definir conclusion:", e)"""

CIERRE = """---
## ¿Terminaste?
Si los cuatro chequeos muestran ✅, **profundizaste de verdad**. 🔬

Ya no solo calculas estadísticas: entiendes **por qué** se comportan así (robustez, escala, forma,
muestreo) y reconoces la trampa que más daño hace en decisiones públicas — **confundir correlación
con causalidad** y dejarse engañar por un **agregado** (Simpson).

La regla de oro que te llevas: **antes de concluir, pregunta por la forma, por la muestra y por el
confusor.** Eso distingue a quien *usa* datos de quien *se deja usar* por ellos."""


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
