"""build_R1-09.py — módulo R1-09 (Dashboards ligeros con Gradio).

Rama R1 (Análisis y Visualización), sin ML. Enseña a construir funciones puras de
pandas (filtros + KPIs) y envolverlas en un tablero Gradio. Sigue la convención
de la casa (ver tools/build_R2-07.py). Datos reales: compras_ml.csv.

OJO verificación: gradio puede no estar instalado en el verificador → su uso va en
una celda final protegida con try/except; los assert prueban las funciones de pandas.

Uso:  /opt/anaconda3/bin/python tools/build_R1-09.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-09-dashboards-ligeros")

IMPORTS = "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt"

EJ = [
 ("## 1. Filtrar es la base de todo tablero",
  "Un dashboard es, en el fondo, **filtrar** datos y mostrar el resultado. Empezamos por una "
  "función pura de pandas que filtra por categoría y región (`'(todas)'` = sin filtro).",
  "Escribe la función `filtrar`",
  '''def filtrar(df, categoria="(todas)", region="(todas)"):
    d = df.copy()
    if categoria != "(todas)":
        d = d[d["categoria"] == categoria]
    if region != "(todas)":
        d = d[d["region_comprador"] == region]
    return d

print("Sin filtro:", filtrar(df).shape[0], "| panadería:", filtrar(df, categoria="Productos de panadería").shape[0])''',
  '''def filtrar(df, categoria="(todas)", region="(todas)"):
    d = df.copy()
    # TODO: si categoria != "(todas)", filtra d por esa categoria
    # TODO: si region != "(todas)", filtra d por esa region
    return d

print("Sin filtro:", filtrar(df).shape[0])''',
  '''assert filtrar(df).shape[0] == df.shape[0]
sub = filtrar(df, categoria="Productos de panadería")
assert set(sub["categoria"].unique()) == {"Productos de panadería"}''',
  "Compara d['categoria'] == categoria y d['region_comprador'] == region solo cuando no sea '(todas)'.",
  None),

 ("## 2. Los KPIs: los números grandes del tablero",
  "Un buen tablero muestra **2-3 indicadores claros**. Calculemos gasto total, nº de órdenes y ticket promedio.",
  "Escribe la función `kpis`",
  '''def kpis(d):
    return {
        "gasto_total": float(d["monto_total"].sum()),
        "n_ordenes": int(len(d)),
        "ticket_promedio": float(d["monto_total"].mean()) if len(d) else 0.0,
    }

print(kpis(filtrar(df)))''',
  '''def kpis(d):
    return {
        "gasto_total": ...,        # TODO: suma de monto_total
        "n_ordenes": ...,          # TODO: nº de filas
        "ticket_promedio": ...,    # TODO: promedio de monto_total
    }

print(kpis(filtrar(df)))''',
  '''k = kpis(df)
assert k["n_ordenes"] == len(df)
assert k["gasto_total"] > 0
assert abs(k["ticket_promedio"] - df["monto_total"].mean()) < 1e-6''',
  "Usa d['monto_total'].sum(), len(d) y d['monto_total'].mean().",
  None),

 ("## 3. Una tabla resumen: gasto por región",
  "El tercer ingrediente: agrupar y ordenar. Esta tabla alimentará el tablero.",
  "Escribe `gasto_por_region`",
  '''def gasto_por_region(d):
    return d.groupby("region_comprador")["monto_total"].sum().sort_values(ascending=False)

print(gasto_por_region(df).head(3))''',
  '''def gasto_por_region(d):
    # TODO: agrupa por region_comprador, suma monto_total y ordena de mayor a menor
    return ...

print(gasto_por_region(df).head(3))''',
  '''g = gasto_por_region(df)
assert list(g.values) == sorted(g.values, reverse=True)
assert len(g) == df["region_comprador"].nunique()''',
  "df.groupby('region_comprador')['monto_total'].sum().sort_values(ascending=False).",
  '''# (ilustración) Gasto por región — así se vería el panel principal del tablero
g = gasto_por_region(df).head(10)
plt.figure(figsize=(6, 4))
plt.barh(g.index[::-1], g.values[::-1], color="#4240e5")
plt.xlabel("Gasto total (CLP)"); plt.title("Gasto por región (top 10)")
plt.tight_layout(); plt.show()'''),

 ("## 4. Un gráfico como componente del tablero",
  "Gradio puede mostrar una figura de matplotlib. Escribe una función que **devuelva** la figura.",
  "Escribe `figura_top_categorias`",
  '''def figura_top_categorias(d, n=8):
    top = d.groupby("categoria")["monto_total"].sum().sort_values().tail(n)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top.index, top.values, color="#ff6b35")
    ax.set_xlabel("Gasto total"); ax.set_title("Top categorías por gasto")
    fig.tight_layout()
    return fig

print(type(figura_top_categorias(df)).__name__)''',
  '''def figura_top_categorias(d, n=8):
    top = d.groupby("categoria")["monto_total"].sum().sort_values().tail(n)
    fig, ax = plt.subplots(figsize=(6, 4))
    # TODO: dibuja un barh con top.index y top.values y devuelve fig
    ...
    return fig

print(type(figura_top_categorias(df)).__name__)''',
  '''fig = figura_top_categorias(df)
assert fig.__class__.__name__ == "Figure"
assert len(fig.axes) >= 1''',
  "ax.barh(top.index, top.values) y recuerda 'return fig'.",
  None),
]

GRADIO_CELL = '''# ── El tablero con Gradio (se ejecuta en Colab) ───────────────────────────────
# gradio puede no estar instalado aquí; lo envolvemos para no romper la ejecución.
try:
    import gradio as gr

    def tablero(categoria, region):
        d = filtrar(df, categoria, region)
        k = kpis(d)
        resumen = f"Gasto total: ${k['gasto_total']:,.0f}  ·  Órdenes: {k['n_ordenes']:,}"
        return resumen, figura_top_categorias(d)

    cats = ["(todas)"] + sorted(df["categoria"].unique())
    regs = ["(todas)"] + sorted(df["region_comprador"].unique())
    demo = gr.Interface(
        tablero,
        [gr.Dropdown(cats, value="(todas)", label="Categoría"),
         gr.Dropdown(regs, value="(todas)", label="Región")],
        [gr.Text(label="Resumen"), gr.Plot(label="Top categorías")],
        title="Compras públicas — tablero de gasto",
    )
    # En Colab, descomenta para publicar un link público (sin túnel):
    # demo.launch(share=True)
    print("✔ App Gradio construida. En Colab ejecuta: demo.launch(share=True)")
except ModuleNotFoundError:
    print("ℹ Gradio no está instalado aquí. En Colab corre primero:  !pip -q install gradio")'''

CIERRE = '''## Cierre

- Un dashboard = **filtrar** + **KPIs** + **una visualización**, envueltos en una interfaz.
- Construye y prueba las **funciones de datos por separado** (como aquí) antes de armar la interfaz.
- **Gradio** corre dentro de Colab con `demo.launch(share=True)` y se publica gratis en Hugging Face Spaces.

> *¿Cuándo NO un dashboard? Si la pregunta se responde una sola vez, un gráfico o un informe basta. El tablero se justifica cuando alguien va a explorar y filtrar de forma recurrente.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-09", "Dashboards ligeros con Gradio", "A", "Analista de Datos", "10",
                      ["Construir funciones de **filtro** y **KPIs** con pandas.",
                       "Crear una **visualización** reutilizable como componente.",
                       "Envolver todo en un **tablero Gradio** publicable desde Colab.",
                       "Juzgar **cuándo un dashboard aporta** y cuándo no."],
                      "publicar un tablero interactivo simple sobre datos públicos, sin instalar nada.",
                      "compras públicas de alimentos por categoría y región (ChileCompra).",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Cargamos los datos (ya hecho arriba). Construyamos el tablero por partes."),
    ]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint, viz) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if viz:
            cells.append(h.code(viz))
    cells.append(h.md("## 5. Arma el tablero"))
    cells.append(h.code(GRADIO_CELL))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundización ───────────────────────────────────────────────────────────
PROF_PREP = '''import pandas as pd, os, urllib.request
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Otra mirada: gasto por tamaño de proveedor",
  "Las micro y pequeñas empresas son foco de política pública. Agrupemos el gasto por `tamano_proveedor`.",
  "Escribe `gasto_por_tamano`",
  '''def gasto_por_tamano(d):
    return d.groupby("tamano_proveedor")["monto_total"].sum().sort_values(ascending=False)

print(gasto_por_tamano(df))''',
  '''def gasto_por_tamano(d):
    # TODO: agrupa por tamano_proveedor y suma monto_total, ordenado desc
    return ...

print(gasto_por_tamano(df))''',
  '''g = gasto_por_tamano(df)
assert len(g) == df["tamano_proveedor"].nunique()
assert g.iloc[0] >= g.iloc[-1]''',
  "df.groupby('tamano_proveedor')['monto_total'].sum().sort_values(ascending=False)."),

 ("## 2. Formato amable de los números",
  "Un tablero se lee mejor con montos formateados. Escribe un formateador de pesos chilenos.",
  "Escribe `formato_clp`",
  '''def formato_clp(x):
    return "$" + f"{int(round(x)):,}".replace(",", ".")

print(formato_clp(1234567))''',
  '''def formato_clp(x):
    # TODO: devuelve un string como "$1.234.567" (punto como separador de miles)
    return ...

print(formato_clp(1234567))''',
  '''s = formato_clp(1234567)
assert s.startswith("$")
assert s == "$1.234.567"''',
  "Formatea con f'{int(round(x)):,}' y reemplaza ',' por '.'; antepone '$'."),

 ("## 3. Participación de una categoría",
  "¿Qué porcentaje del gasto total se va en una categoría? Útil como KPI de contexto.",
  "Escribe `participacion`",
  '''def participacion(d, categoria):
    total = d["monto_total"].sum()
    cat = d[d["categoria"] == categoria]["monto_total"].sum()
    return 100 * cat / total if total else 0.0

print(round(participacion(df, "Productos de panadería"), 2), "%")''',
  '''def participacion(d, categoria):
    # TODO: % del gasto total que corresponde a 'categoria'
    return ...

print(participacion(df, "Productos de panadería"))''',
  '''p = participacion(df, "Productos de panadería")
assert 0.0 <= p <= 100.0''',
  "100 * (gasto de la categoria) / (gasto total)."),
]

PROF_HEADER = '''# R1-09 · Dashboards ligeros — Profundización (opcional) 🔬

**Formación Pública — Línea A · Analista de Datos · Notebook de profundización**

Opcional. Más componentes para tu tablero: gasto por **tamaño de proveedor**, **formato** de montos
en pesos y un KPI de **participación** por categoría. Mismos datos reales de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-09.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R1-09 · Dashboards ligeros con Gradio

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-09-dashboards-ligeros/leccion.ipynb)

Construye un tablero interactivo con **Gradio** sobre datos reales de compras públicas:
funciones de filtro + KPIs + visualización, publicable desde Colab con `demo.launch(share=True)`.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: gasto por tamaño, formato CLP, participación.
- En Colab: `!pip -q install gradio` antes de la última celda.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
