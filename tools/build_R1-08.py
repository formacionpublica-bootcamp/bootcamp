"""build_R1-08.py — módulo R1-08 (Visualización para comunicar + ética).

Rama R1 (Análisis y Visualización). Split de A6, parte comunicación: gráfico honesto
y claro para audiencia directiva — eje desde 0, título/etiquetas, anotación, evitar
engaños visuales. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-08.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-08-visualizacion-comunicar-etica")

IMPORTS = "import pandas as pd\nimport matplotlib.pyplot as plt"

PREP = '''# Trabajaremos con el gasto por región (top 6) en todos los ejercicios.
g = df.groupby("region_comprador")["monto_total"].sum().sort_values(ascending=False).head(6)
print(g.round(0))'''

EJ = [
 ("## 1. El eje Y empieza en cero",
  "El engaño visual más común es **truncar el eje Y**: exagera diferencias pequeñas. Un gráfico de "
  "barras honesto **empieza en 0**.",
  "Dibuja barras con el eje desde 0",
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
ax.set_ylim(bottom=0)
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
# TODO: fuerza que el eje Y empiece en 0
...
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''assert ax.get_ylim()[0] == 0''',
  "ax.set_ylim(bottom=0).",
  None),

 ("## 2. Título y etiquetas: que se entienda solo",
  "Un gráfico para otros necesita **título** y **etiquetas de ejes**: debe entenderse sin explicación oral.",
  "Agrega título y etiquetas",
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
ax.set_ylim(bottom=0)
ax.set_title("Gasto en compras públicas por región (top 6)")
ax.set_xlabel("Región"); ax.set_ylabel("Gasto total (CLP)")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
ax.set_ylim(bottom=0)
# TODO: pon un título y etiquetas de eje X e Y
...
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''assert ax.get_title() != ""
assert ax.get_xlabel() != "" and ax.get_ylabel() != ""''',
  "ax.set_title(...), ax.set_xlabel(...), ax.set_ylabel(...).",
  None),

 ("## 3. Anotar el dato clave",
  "Una buena visualización **guía la mirada** al mensaje. Anota el valor más importante.",
  "Anota la región de mayor gasto",
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
ax.set_ylim(bottom=0)
ax.annotate(f"Mayor gasto: {g.idxmax()}", xy=(0, g.max()), xytext=(1, g.max() * 0.9),
            arrowprops=dict(arrowstyle="->"))
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color="#4240e5")
ax.set_ylim(bottom=0)
# TODO: usa ax.annotate(...) para señalar la región de mayor gasto (g.idxmax())
...
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.show()''',
  '''assert len(ax.texts) > 0''',
  "ax.annotate('texto', xy=(...), xytext=(...)).",
  None),

 ("## 4. Engañoso vs honesto, lado a lado",
  "Comparemos el mismo dato con eje **truncado** (engañoso) y desde **cero** (honesto). La diferencia "
  "es ética, no estética.",
  "Construye las dos versiones",
  '''fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.bar(g.index, g.values, color="#ff6b35"); ax1.set_ylim(bottom=g.min() * 0.98); ax1.set_title("Enganoso (eje truncado)")
ax2.bar(g.index, g.values, color="#4240e5"); ax2.set_ylim(bottom=0); ax2.set_title("Honesto (desde 0)")
for a in (ax1, ax2):
    a.set_xticklabels(g.index, rotation=45, ha="right")
honesto_desde_cero = ax2.get_ylim()[0] == 0
plt.tight_layout(); plt.show()''',
  '''fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
# engañoso: eje truncado
ax1.bar(g.index, g.values, color="#ff6b35"); ax1.set_ylim(bottom=g.min() * 0.98); ax1.set_title("Enganoso (eje truncado)")
# TODO: versión honesta en ax2 con eje desde 0 y título
ax2.bar(g.index, g.values, color="#4240e5")
...
ax2.set_title("Honesto (desde 0)")
for a in (ax1, ax2):
    a.set_xticklabels(g.index, rotation=45, ha="right")
honesto_desde_cero = ax2.get_ylim()[0] == 0
plt.tight_layout(); plt.show()''',
  '''assert honesto_desde_cero
assert ax1.get_ylim()[0] > 0''',
  "En ax2: ax2.set_ylim(bottom=0).",
  None),
]

CIERRE = '''## Cierre

- Barras **desde 0**: truncar el eje es el engaño más común.
- **Título y etiquetas** hacen que el gráfico se entienda solo.
- **Anota** el mensaje clave para guiar la mirada.
- La honestidad visual es **ética**: en el Estado, comunicar bien es comunicar con integridad.

> *Ética distribuida: aquí la responsabilidad es no engañar con un gráfico, aunque sea sin querer.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-08", "Visualización para comunicar + ética", "A", "Analista de Datos", "9",
                      ["Hacer barras **honestas** con el eje desde 0.",
                       "Poner **título y etiquetas** claros.",
                       "**Anotar** el dato clave.",
                       "Reconocer y evitar **engaños visuales**."],
                      "comunicar un hallazgo con un gráfico claro y honesto para una audiencia directiva.",
                      "gasto en compras públicas por región (ChileCompra).",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Preparación"), h.code(PREP),
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


PROF_PREP = '''import pandas as pd, os, urllib.request
import matplotlib.pyplot as plt
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
g = df.groupby("region_comprador")["monto_total"].sum().sort_values(ascending=False).head(6)
print("Listo:", len(g), "regiones")'''

PROF_EJ = [
 ("## 1. Destacar una sola barra",
  "El color guía la atención. Pinta de acento solo la barra del máximo, el resto en gris suave.",
  "Colorea destacando el máximo",
  '''colores = ["#ff6b35" if r == g.idxmax() else "#c1c1ff" for r in g.index]
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color=colores); ax.set_ylim(bottom=0)
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()''',
  '''# TODO: lista de colores: "#ff6b35" para la región de mayor gasto (g.idxmax()), "#c1c1ff" el resto
colores = ...
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index, g.values, color=colores); ax.set_ylim(bottom=0)
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()''',
  '''assert colores.count("#ff6b35") == 1''',
  '["#ff6b35" if r == g.idxmax() else "#c1c1ff" for r in g.index].'),

 ("## 2. Etiquetas de valor sobre las barras",
  "Mostrar el número sobre cada barra evita que la audiencia tenga que estimarlo del eje.",
  "Pon el valor (en millones) sobre cada barra",
  '''fig, ax = plt.subplots(figsize=(7, 4))
barras = ax.bar(g.index, g.values, color="#4240e5"); ax.set_ylim(bottom=0)
for b, v in zip(barras, g.values):
    ax.text(b.get_x() + b.get_width() / 2, v, f"{v/1e6:.0f}M", ha="center", va="bottom")
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()''',
  '''fig, ax = plt.subplots(figsize=(7, 4))
barras = ax.bar(g.index, g.values, color="#4240e5"); ax.set_ylim(bottom=0)
for b, v in zip(barras, g.values):
    # TODO: ax.text(...) con el valor v en millones sobre la barra
    ...
plt.xticks(rotation=45, ha="right"); plt.tight_layout(); plt.show()''',
  '''assert len(ax.texts) == len(g)''',
  "ax.text(b.get_x()+b.get_width()/2, v, f'{v/1e6:.0f}M', ha='center', va='bottom')."),

 ("## 3. Checklist de honestidad",
  "Automatiza la revisión: una función que verifica si un gráfico cumple lo mínimo ético.",
  "Escribe `revisar_grafico`",
  '''def revisar_grafico(ax):
    return {
        "eje_desde_cero": ax.get_ylim()[0] == 0,
        "tiene_titulo": ax.get_title() != "",
        "tiene_etiquetas": ax.get_xlabel() != "" and ax.get_ylabel() != "",
    }

fig, ax = plt.subplots()
ax.bar(g.index, g.values); ax.set_ylim(bottom=0)
ax.set_title("Gasto por región"); ax.set_xlabel("Región"); ax.set_ylabel("CLP")
chequeo = revisar_grafico(ax)
print(chequeo)''',
  '''def revisar_grafico(ax):
    # TODO: dict con eje_desde_cero, tiene_titulo, tiene_etiquetas (booleanos)
    ...

fig, ax = plt.subplots()
ax.bar(g.index, g.values); ax.set_ylim(bottom=0)
ax.set_title("Gasto por región"); ax.set_xlabel("Región"); ax.set_ylabel("CLP")
chequeo = revisar_grafico(ax)
print(chequeo)''',
  '''assert chequeo["eje_desde_cero"]
assert all(chequeo.values())''',
  "Devuelve los 3 booleanos leyendo ax.get_ylim()[0]==0, ax.get_title(), ax.get_xlabel()/ylabel."),
]

PROF_HEADER = '''# R1-08 · Visualización para comunicar — Profundización (opcional) 🔬

**Formación Pública — Línea A · Analista de Datos · Notebook de profundización**

Opcional. **Destacar** una barra con color, **etiquetas de valor** sobre las barras y un **checklist
de honestidad** automatizado. Mismos datos de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-08.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-08 · Visualización para comunicar + ética

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-08-visualizacion-comunicar-etica/leccion.ipynb)

Construir un gráfico **honesto y claro** para audiencia directiva: eje desde 0, título/etiquetas,
anotación del mensaje clave y cómo evitar engaños visuales. Datos reales de compras públicas.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: destacar una barra, etiquetas de valor, checklist de honestidad.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
