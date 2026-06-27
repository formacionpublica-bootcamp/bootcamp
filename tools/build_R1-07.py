"""build_R1-07.py — módulo R1-07 (Visualización exploratoria: ver para entender).

Rama R1 (Análisis y Visualización). Split de A6, parte exploratoria: histograma,
boxplot, dispersión y barras para DESCUBRIR patrones (no aún para comunicar).
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-07.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-07-visualizacion-exploratoria")

IMPORTS = "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt"

EJ = [
 ("## 1. Histograma: la forma de una variable",
  "El **histograma** muestra cómo se distribuye un número. El monto de compras tiene cola larga "
  "(recortamos al p99 para verlo mejor).",
  "Dibuja el histograma del monto",
  '''montos = df["monto_total"].clip(upper=df["monto_total"].quantile(0.99))
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(montos, bins=40, color="#4240e5")
ax.set_xlabel("Monto (recortado al p99)"); ax.set_ylabel("Frecuencia"); ax.set_title("Distribución del monto")
plt.show()''',
  '''montos = df["monto_total"].clip(upper=df["monto_total"].quantile(0.99))
fig, ax = plt.subplots(figsize=(6, 4))
# TODO: dibuja un histograma de 'montos' con 40 bins
...
ax.set_xlabel("Monto (recortado al p99)"); ax.set_ylabel("Frecuencia"); ax.set_title("Distribución del monto")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(ax.patches) > 0''',
  "ax.hist(montos, bins=40).",
  None),

 ("## 2. Boxplot: comparar grupos",
  "El **boxplot** compara la distribución entre grupos. ¿Difiere el monto según el tamaño del proveedor?",
  "Boxplot del monto por tamaño",
  '''orden = ["Micro", "Pequeña", "Mediana", "Grande"]
tope = df["monto_total"].quantile(0.99)
grupos = [df[df["tamano_proveedor"] == t]["monto_total"].clip(upper=tope) for t in orden]
fig, ax = plt.subplots(figsize=(6, 4))
ax.boxplot(grupos, labels=orden)
ax.set_ylabel("Monto"); ax.set_title("Monto por tamaño de proveedor")
plt.show()''',
  '''orden = ["Micro", "Pequeña", "Mediana", "Grande"]
tope = df["monto_total"].quantile(0.99)
grupos = [df[df["tamano_proveedor"] == t]["monto_total"].clip(upper=tope) for t in orden]
fig, ax = plt.subplots(figsize=(6, 4))
# TODO: dibuja un boxplot de 'grupos' con labels=orden
...
ax.set_ylabel("Monto"); ax.set_title("Monto por tamaño de proveedor")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(grupos) == 4''',
  "ax.boxplot(grupos, labels=orden).",
  None),

 ("## 3. Dispersión: ¿se relacionan dos variables?",
  "El **gráfico de dispersión** revela relaciones. ¿Más cantidad implica más monto?",
  "Dispersión cantidad vs monto",
  '''m = df.sample(800, random_state=42)
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(m["cantidad"], m["monto_total"], s=10, alpha=0.4, color="#ff6b35")
ax.set_xlabel("Cantidad"); ax.set_ylabel("Monto"); ax.set_title("Cantidad vs monto")
plt.show()''',
  '''m = df.sample(800, random_state=42)
fig, ax = plt.subplots(figsize=(6, 4))
# TODO: dibuja un scatter de m["cantidad"] vs m["monto_total"]
...
ax.set_xlabel("Cantidad"); ax.set_ylabel("Monto"); ax.set_title("Cantidad vs monto")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(ax.collections) > 0''',
  "ax.scatter(m['cantidad'], m['monto_total']).",
  None),

 ("## 4. Barras: comparar categorías",
  "Las **barras** comparan magnitudes entre categorías. ¿Qué región concentra más gasto?",
  "Gasto por región (barras horizontales)",
  '''g = df.groupby("region_comprador")["monto_total"].sum().sort_values()
fig, ax = plt.subplots(figsize=(6, 5))
ax.barh(g.index, g.values, color="#4240e5")
ax.set_xlabel("Gasto total"); ax.set_title("Gasto por región")
plt.show()''',
  '''g = df.groupby("region_comprador")["monto_total"].sum().sort_values()
fig, ax = plt.subplots(figsize=(6, 5))
# TODO: dibuja barras horizontales (barh) con g.index y g.values
...
ax.set_xlabel("Gasto total"); ax.set_title("Gasto por región")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(g) == df["region_comprador"].nunique()''',
  "ax.barh(g.index, g.values).",
  None),
]

CIERRE = '''## Cierre

- El **histograma** muestra la forma; el **boxplot** compara grupos.
- La **dispersión** revela relaciones; las **barras** comparan categorías.
- Esta visualización es para **descubrir** (para ti). En R1-08 aprenderás a **comunicar** (para otros).

> *Ver para entender: una victoria temprana — un buen gráfico vale más que una tabla de números.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-07", "Visualización exploratoria — ver para entender", "A", "Analista de Datos", "8",
                      ["Leer la **forma** de una variable con histogramas.",
                       "Comparar grupos con **boxplots**.",
                       "Detectar relaciones con **dispersión**.",
                       "Comparar categorías con **barras**."],
                      "usar gráficos para descubrir patrones en datos públicos.",
                      "compras públicas (ChileCompra): monto, cantidad, región, tamaño de proveedor.",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Datos cargados arriba. Exploremos viendo."),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


PROF_PREP = '''import pandas as pd, numpy as np, os, urllib.request
import matplotlib.pyplot as plt
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Escala logarítmica para colas largas",
  "Cuando hay valores enormes, la **escala log** deja ver la masa de datos pequeños.",
  "Histograma en escala log",
  '''fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["monto_total"], bins=50, color="#4240e5")
ax.set_yscale("log")
ax.set_xlabel("Monto"); ax.set_ylabel("Frecuencia (log)")
plt.show()''',
  '''fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["monto_total"], bins=50, color="#4240e5")
# TODO: pon el eje y en escala logarítmica
...
ax.set_xlabel("Monto"); ax.set_ylabel("Frecuencia (log)")
plt.show()''',
  '''assert ax.get_yscale() == "log"''',
  "ax.set_yscale('log')."),

 ("## 2. Detección de outliers con la regla IQR",
  "Más allá del gráfico: calcula los límites estadísticos de outlier (Q1−1.5·IQR, Q3+1.5·IQR).",
  "Calcula los límites de outlier",
  '''q1, q3 = df["monto_total"].quantile([0.25, 0.75])
iqr = q3 - q1
lim_sup = q3 + 1.5 * iqr
n_outliers = int((df["monto_total"] > lim_sup).sum())
print("límite superior:", round(lim_sup), "| outliers:", n_outliers)''',
  '''q1, q3 = df["monto_total"].quantile([0.25, 0.75])
iqr = q3 - q1
# TODO: lim_sup = Q3 + 1.5*IQR ; n_outliers = cuántos montos lo superan
lim_sup = ...
n_outliers = ...
print("límite superior:", round(lim_sup), "| outliers:", n_outliers)''',
  '''assert lim_sup > df["monto_total"].median()
assert n_outliers == int((df["monto_total"] > lim_sup).sum())''',
  "lim_sup = q3 + 1.5*iqr ; (df['monto_total'] > lim_sup).sum()."),

 ("## 3. Pequeños múltiplos: una distribución por grupo",
  "Comparar la forma entre grupos: un histograma por tamaño de proveedor en una grilla.",
  "Grilla de histogramas por tamaño",
  '''orden = ["Micro", "Pequeña", "Mediana", "Grande"]
tope = df["monto_total"].quantile(0.95)
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, t in zip(axes.ravel(), orden):
    ax.hist(df[df["tamano_proveedor"] == t]["monto_total"].clip(upper=tope), bins=25, color="#4240e5")
    ax.set_title(t)
fig.tight_layout()
plt.show()''',
  '''orden = ["Micro", "Pequeña", "Mediana", "Grande"]
tope = df["monto_total"].quantile(0.95)
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, t in zip(axes.ravel(), orden):
    # TODO: histograma del monto (clip al 'tope') para el tamaño t y título t
    ...
fig.tight_layout()
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(fig.axes) == 4''',
  "Dentro del bucle: ax.hist(...) del subconjunto y ax.set_title(t)."),
]

PROF_HEADER = '''# R1-07 · Visualización exploratoria — Profundización (opcional) 🔬

**Formación Pública — Línea A · Analista de Datos · Notebook de profundización**

Opcional. **Escala logarítmica** para colas largas, detección de **outliers (IQR)** y **pequeños
múltiplos** (una distribución por grupo). Mismos datos de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-07.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-07 · Visualización exploratoria — ver para entender

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-07-visualizacion-exploratoria/leccion.ipynb)

Histograma, boxplot, dispersión y barras para **descubrir** patrones en datos reales de compras
públicas (`compras_ml.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: escala log, outliers (IQR), pequeños múltiplos.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
