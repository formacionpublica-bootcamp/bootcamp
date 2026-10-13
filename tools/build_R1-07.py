"""build_R1-07.py — módulo R1-07 (Visualización exploratoria: ver para entender).

Rama R1 (Análisis y Visualización). Histograma, boxplot, dispersión y barras para
DESCUBRIR patrones (no aún para comunicar). Rearmado 2026: lección sobre matrícula
escolar 2025 (MINEDUC); profundiza = transferencia con sismos reales (USGS).
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
  "El **histograma** muestra cómo se distribuye un número. El tamaño de los establecimientos tiene "
  "cola larga: muchas escuelas chicas y pocos colegios enormes (recortamos al p99 para verlo mejor).",
  "Dibuja el histograma de la matrícula",
  '''matriculas = df["mat_total"].clip(upper=df["mat_total"].quantile(0.99))
fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(matriculas, bins=40, color="#4240e5")
ax.set_xlabel("Matrícula (recortada al p99)"); ax.set_ylabel("Frecuencia"); ax.set_title("Tamaño de los establecimientos")
plt.show()''',
  '''matriculas = df["mat_total"].clip(upper=df["mat_total"].quantile(0.99))
fig, ax = plt.subplots(figsize=(6, 4))
# TODO: dibuja un histograma de 'matriculas' con 40 bins
...
ax.set_xlabel("Matrícula (recortada al p99)"); ax.set_ylabel("Frecuencia"); ax.set_title("Tamaño de los establecimientos")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(ax.patches) > 0''',
  "ax.hist(matriculas, bins=40).",
  None),

 ("## 2. Boxplot: comparar grupos",
  "El **boxplot** compara la distribución entre grupos. ¿Difiere el tamaño de los establecimientos "
  "según su dependencia?",
  "Boxplot de la matrícula por dependencia",
  '''orden = ["Municipal", "Particular subvencionado", "Particular pagado", "Servicio Local de Educación"]
tope = df["mat_total"].quantile(0.99)
grupos = [df[df["dependencia"] == d]["mat_total"].clip(upper=tope) for d in orden]
fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot(grupos, labels=["Municipal", "P. subv.", "P. pagado", "SLEP"])
ax.set_ylabel("Matrícula"); ax.set_title("Matrícula por dependencia")
plt.show()''',
  '''orden = ["Municipal", "Particular subvencionado", "Particular pagado", "Servicio Local de Educación"]
tope = df["mat_total"].quantile(0.99)
grupos = [df[df["dependencia"] == d]["mat_total"].clip(upper=tope) for d in orden]
fig, ax = plt.subplots(figsize=(8, 4))
# TODO: dibuja un boxplot de 'grupos' con labels cortos
...
ax.set_ylabel("Matrícula"); ax.set_title("Matrícula por dependencia")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(grupos) == 4''',
  "ax.boxplot(grupos, labels=[...]).",
  None),

 ("## 3. Dispersión: ¿se relacionan dos variables?",
  "El **gráfico de dispersión** revela relaciones. ¿Más cursos implica más estudiantes? "
  "¿Y qué tan dispersa es esa relación?",
  "Dispersión cursos vs matrícula",
  '''m = df.sample(800, random_state=42)
fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(m["cursos"], m["mat_total"], s=10, alpha=0.4, color="#ff6b35")
ax.set_xlabel("Nº de cursos"); ax.set_ylabel("Matrícula"); ax.set_title("Cursos vs matrícula")
plt.show()''',
  '''m = df.sample(800, random_state=42)
fig, ax = plt.subplots(figsize=(6, 4))
# TODO: dibuja un scatter de m["cursos"] vs m["mat_total"]
...
ax.set_xlabel("Nº de cursos"); ax.set_ylabel("Matrícula"); ax.set_title("Cursos vs matrícula")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(ax.collections) > 0''',
  "ax.scatter(m['cursos'], m['mat_total']).",
  None),

 ("## 4. Barras: comparar categorías",
  "Las **barras** comparan magnitudes entre categorías. ¿Qué región concentra más estudiantes?",
  "Matrícula por región (barras horizontales)",
  '''g = df.groupby("region")["mat_total"].sum().sort_values()
fig, ax = plt.subplots(figsize=(6, 5))
ax.barh(g.index, g.values, color="#4240e5")
ax.set_xlabel("Estudiantes matriculados"); ax.set_title("Matrícula por región")
plt.show()''',
  '''g = df.groupby("region")["mat_total"].sum().sort_values()
fig, ax = plt.subplots(figsize=(6, 5))
# TODO: dibuja barras horizontales (barh) con g.index y g.values
...
ax.set_xlabel("Estudiantes matriculados"); ax.set_title("Matrícula por región")
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(g) == df["region"].nunique()''',
  "ax.barh(g.index, g.values).",
  None),
]

CIERRE = '''## Cierre

- El **histograma** muestra la forma; el **boxplot** compara grupos.
- La **dispersión** revela relaciones; las **barras** comparan categorías.
- Esta visualización es para **descubrir** (para ti). En R1-08 aprenderás a **comunicar** (para otros).

> *Ver para entender: una victoria temprana — un buen gráfico vale más que una tabla de números.
> En la profundización aplicarás las mismas herramientas a un dominio nuevo: los sismos de Chile.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-07", "Visualización exploratoria — ver para entender", "R1", "Analista de Datos", "8",
                      ["Leer la **forma** de una variable con histogramas.",
                       "Comparar grupos con **boxplots**.",
                       "Detectar relaciones con **dispersión**.",
                       "Comparar categorías con **barras**."],
                      "usar gráficos para descubrir patrones en datos públicos.",
                      "matrícula escolar 2025 (MINEDUC): tamaño, dependencia, cursos, región.",
                      n_checks=4),
        h.setup_cell("matricula.csv", IMPORTS),
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
CSV = "sismos.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/sismos.csv", CSV)
df = pd.read_csv(CSV)
print("Sismos M>=4.5 en Chile 2020-2025 (catálogo USGS):", df.shape)'''

PROF_EJ = [
 ("## 1. Transferencia: mismas herramientas, dominio nuevo",
  "Ahora el dataset son **1.601 sismos reales** de Chile (2020–2025, magnitud ≥ 4,5). La distribución "
  "de magnitudes es muy asimétrica — la **escala log** en el eje y deja ver la ley de Gutenberg-Richter: "
  "por cada grado de magnitud, los sismos son ~10 veces menos frecuentes.",
  "Histograma de magnitudes en escala log",
  '''fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["magnitud"], bins=25, color="#4240e5")
ax.set_yscale("log")
ax.set_xlabel("Magnitud"); ax.set_ylabel("Frecuencia (log)")
plt.show()''',
  '''fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df["magnitud"], bins=25, color="#4240e5")
# TODO: pon el eje y en escala logarítmica
...
ax.set_xlabel("Magnitud"); ax.set_ylabel("Frecuencia (log)")
plt.show()''',
  '''assert ax.get_yscale() == "log"''',
  "ax.set_yscale('log')."),

 ("## 2. Detección de outliers con la regla IQR",
  "Más allá del gráfico: calcula los límites estadísticos de outlier (Q1−1.5·IQR, Q3+1.5·IQR) "
  "para la profundidad de los sismos.",
  "Calcula los límites de outlier de la profundidad",
  '''q1, q3 = df["profundidad_km"].quantile([0.25, 0.75])
iqr = q3 - q1
lim_sup = q3 + 1.5 * iqr
n_outliers = int((df["profundidad_km"] > lim_sup).sum())
print("límite superior:", round(lim_sup, 1), "km | sismos más profundos que eso:", n_outliers)''',
  '''q1, q3 = df["profundidad_km"].quantile([0.25, 0.75])
iqr = q3 - q1
# TODO: lim_sup = Q3 + 1.5*IQR ; n_outliers = cuántos sismos lo superan
lim_sup = ...
n_outliers = ...
print("límite superior:", round(lim_sup, 1), "km | sismos más profundos que eso:", n_outliers)''',
  '''assert lim_sup > df["profundidad_km"].median()
assert n_outliers == int((df["profundidad_km"] > lim_sup).sum())''',
  "lim_sup = q3 + 1.5*iqr ; (df['profundidad_km'] > lim_sup).sum()."),

 ("## 3. Pequeños múltiplos: una distribución por grupo",
  "Comparar la forma entre grupos: un histograma de magnitud por zona del país en una grilla. "
  "¿Se ve igual la sismicidad del norte que la del sur?",
  "Grilla de histogramas por zona",
  '''zonas = ["norte", "centro", "sur", "austral"]
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, z in zip(axes.ravel(), zonas):
    ax.hist(df[df["zona"] == z]["magnitud"], bins=20, color="#4240e5")
    ax.set_title(z)
fig.tight_layout()
plt.show()''',
  '''zonas = ["norte", "centro", "sur", "austral"]
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
for ax, z in zip(axes.ravel(), zonas):
    # TODO: histograma de la magnitud para la zona z y título z
    ...
fig.tight_layout()
plt.show()''',
  '''assert fig.__class__.__name__ == "Figure"
assert len(fig.axes) == 4''',
  "Dentro del bucle: ax.hist(...) del subconjunto y ax.set_title(z)."),
]

PROF_HEADER = '''# R1-07 · Visualización exploratoria — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas herramientas de la lección, ahora sobre un dominio
nuevo — **1.601 sismos reales de Chile** (2020–2025, catálogo USGS). **Escala logarítmica**,
**outliers (IQR)** y **pequeños múltiplos**.

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

Histograma, boxplot, dispersión y barras para **descubrir** patrones en la matrícula escolar
2025 (`matricula.csv`, MINEDUC). La profundización transfiere las mismas herramientas a los
**sismos de Chile** (`sismos.csv`, catálogo USGS 2020–2025).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: escala log, outliers (IQR), pequeños múltiplos, con sismos.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
