"""build_R1-09.py — módulo R1-09 (Dashboards ligeros con Gradio).

Rama R1 (Análisis y Visualización), sin ML. Funciones puras de pandas (filtros +
KPIs) envueltas en un tablero Gradio. Rearmado 2026: dataset ancla = matrícula
escolar 2025 (MINEDUC). Convención de la casa.

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
  "función pura de pandas que filtra por dependencia y región (`'(todas)'` = sin filtro).",
  "Escribe la función `filtrar`",
  '''def filtrar(df, dependencia="(todas)", region="(todas)"):
    d = df.copy()
    if dependencia != "(todas)":
        d = d[d["dependencia"] == dependencia]
    if region != "(todas)":
        d = d[d["region"] == region]
    return d

print("Sin filtro:", filtrar(df).shape[0], "| municipales:", filtrar(df, dependencia="Municipal").shape[0])''',
  '''def filtrar(df, dependencia="(todas)", region="(todas)"):
    d = df.copy()
    # TODO: si dependencia != "(todas)", filtra d por esa dependencia
    # TODO: si region != "(todas)", filtra d por esa region
    return d

print("Sin filtro:", filtrar(df).shape[0])''',
  '''assert filtrar(df).shape[0] == df.shape[0]
sub = filtrar(df, dependencia="Municipal")
assert set(sub["dependencia"].unique()) == {"Municipal"}''',
  "Compara d['dependencia'] == dependencia y d['region'] == region solo cuando no sea '(todas)'.",
  None),

 ("## 2. Los KPIs: los números grandes del tablero",
  "Un buen tablero muestra **2-3 indicadores claros**. Calculemos establecimientos, estudiantes "
  "y tamaño promedio.",
  "Escribe la función `kpis`",
  '''def kpis(d):
    return {
        "n_establecimientos": int(len(d)),
        "estudiantes": int(d["mat_total"].sum()),
        "tamano_promedio": float(d["mat_total"].mean()) if len(d) else 0.0,
    }

print(kpis(filtrar(df)))''',
  '''def kpis(d):
    return {
        "n_establecimientos": ...,   # TODO: nº de filas
        "estudiantes": ...,          # TODO: suma de mat_total
        "tamano_promedio": ...,      # TODO: promedio de mat_total
    }

print(kpis(filtrar(df)))''',
  '''k = kpis(df)
assert k["n_establecimientos"] == len(df)
assert k["estudiantes"] == int(df["mat_total"].sum())
assert abs(k["tamano_promedio"] - df["mat_total"].mean()) < 1e-6''',
  "Usa len(d), d['mat_total'].sum() y d['mat_total'].mean().",
  None),

 ("## 3. Una tabla resumen: matrícula por región",
  "El tercer ingrediente: agrupar y ordenar. Esta tabla alimentará el tablero.",
  "Escribe `matricula_por_region`",
  '''def matricula_por_region(d):
    return d.groupby("region")["mat_total"].sum().sort_values(ascending=False)

print(matricula_por_region(df).head(3))''',
  '''def matricula_por_region(d):
    # TODO: agrupa por region, suma mat_total y ordena de mayor a menor
    return ...

print(matricula_por_region(df).head(3))''',
  '''g = matricula_por_region(df)
assert list(g.values) == sorted(g.values, reverse=True)
assert len(g) == df["region"].nunique()''',
  "df.groupby('region')['mat_total'].sum().sort_values(ascending=False).",
  '''# (ilustración) Matrícula por región — así se vería el panel principal del tablero
g = matricula_por_region(df).head(10)
plt.figure(figsize=(6, 4))
plt.barh(g.index[::-1], g.values[::-1], color="#4240e5")
plt.xlabel("Estudiantes matriculados"); plt.title("Matrícula por región (top 10)")
plt.tight_layout(); plt.show()'''),

 ("## 4. Un gráfico como componente del tablero",
  "Gradio puede mostrar una figura de matplotlib. Escribe una función que **devuelva** la figura.",
  "Escribe `figura_top_comunas`",
  '''def figura_top_comunas(d, n=8):
    top = d.groupby("comuna")["mat_total"].sum().sort_values().tail(n)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(top.index, top.values, color="#ff6b35")
    ax.set_xlabel("Estudiantes matriculados"); ax.set_title("Top comunas por matrícula")
    fig.tight_layout()
    return fig

print(type(figura_top_comunas(df)).__name__)''',
  '''def figura_top_comunas(d, n=8):
    top = d.groupby("comuna")["mat_total"].sum().sort_values().tail(n)
    fig, ax = plt.subplots(figsize=(6, 4))
    # TODO: dibuja un barh con top.index y top.values y devuelve fig
    ...
    return fig

print(type(figura_top_comunas(df)).__name__)''',
  '''fig = figura_top_comunas(df)
assert fig.__class__.__name__ == "Figure"
assert len(fig.axes) >= 1''',
  "ax.barh(top.index, top.values) y recuerda 'return fig'.",
  None),
]

GRADIO_CELL = '''# ── El tablero con Gradio (se ejecuta en Colab) ───────────────────────────────
# gradio puede no estar instalado aquí; lo envolvemos para no romper la ejecución.
try:
    import gradio as gr

    def tablero(dependencia, region):
        d = filtrar(df, dependencia, region)
        k = kpis(d)
        resumen = f"Establecimientos: {k['n_establecimientos']:,}  ·  Estudiantes: {k['estudiantes']:,}"
        return resumen, figura_top_comunas(d)

    deps = ["(todas)"] + sorted(df["dependencia"].unique())
    regs = ["(todas)"] + sorted(df["region"].unique())
    demo = gr.Interface(
        tablero,
        [gr.Dropdown(deps, value="(todas)", label="Dependencia"),
         gr.Dropdown(regs, value="(todas)", label="Región")],
        [gr.Text(label="Resumen"), gr.Plot(label="Top comunas")],
        title="Matrícula escolar 2025 — tablero regional",
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

> *¿Cuándo NO un dashboard? Si la pregunta se responde una sola vez, un gráfico o un informe basta. El tablero se justifica cuando alguien va a explorar y filtrar de forma recurrente — como un equipo regional mirando su propia matrícula.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-09", "Dashboards ligeros con Gradio", "R1", "Analista de Datos", "10",
                      ["Construir funciones de **filtro** y **KPIs** con pandas.",
                       "Crear una **visualización** reutilizable como componente.",
                       "Envolver todo en un **tablero Gradio** publicable desde Colab.",
                       "Juzgar **cuándo un dashboard aporta** y cuándo no."],
                      "publicar un tablero interactivo simple sobre datos públicos, sin instalar nada.",
                      "matrícula escolar oficial 2025 por dependencia, región y comuna (MINEDUC).",
                      n_checks=4),
        h.setup_cell("matricula.csv", IMPORTS),
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
CSV = "matricula.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/matricula.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Otra mirada: matrícula por dependencia",
  "La distribución pública/particular es foco permanente de política educativa. Agrupemos "
  "los estudiantes por `dependencia`.",
  "Escribe `matricula_por_dependencia`",
  '''def matricula_por_dependencia(d):
    return d.groupby("dependencia")["mat_total"].sum().sort_values(ascending=False)

print(matricula_por_dependencia(df))''',
  '''def matricula_por_dependencia(d):
    # TODO: agrupa por dependencia y suma mat_total, ordenado desc
    return ...

print(matricula_por_dependencia(df))''',
  '''g = matricula_por_dependencia(df)
assert len(g) == df["dependencia"].nunique()
assert g.iloc[0] >= g.iloc[-1]''',
  "df.groupby('dependencia')['mat_total'].sum().sort_values(ascending=False)."),

 ("## 2. Formato amable de los números",
  "Un tablero se lee mejor con números formateados. Escribe un formateador con separador "
  "de miles a la chilena.",
  "Escribe `formato_miles`",
  '''def formato_miles(x):
    return f"{int(round(x)):,}".replace(",", ".")

print(formato_miles(3541783))''',
  '''def formato_miles(x):
    # TODO: devuelve un string como "3.541.783" (punto como separador de miles)
    return ...

print(formato_miles(3541783))''',
  '''s = formato_miles(3541783)
assert s == "3.541.783"''',
  "Formatea con f'{int(round(x)):,}' y reemplaza ',' por '.'."),

 ("## 3. Participación de una dependencia",
  "¿Qué porcentaje de los estudiantes está en cada dependencia? Útil como KPI de contexto.",
  "Escribe `participacion`",
  '''def participacion(d, dependencia):
    total = d["mat_total"].sum()
    dep = d[d["dependencia"] == dependencia]["mat_total"].sum()
    return 100 * dep / total if total else 0.0

print(round(participacion(df, "Municipal"), 2), "%")''',
  '''def participacion(d, dependencia):
    # TODO: % de los estudiantes que corresponde a 'dependencia'
    return ...

print(participacion(df, "Municipal"))''',
  '''p = participacion(df, "Municipal")
assert 0.0 <= p <= 100.0''',
  "100 * (estudiantes de esa dependencia) / (estudiantes totales)."),
]

PROF_HEADER = '''# R1-09 · Dashboards ligeros — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional. Más componentes para tu tablero: matrícula por **dependencia**, **formato** de números
con separador de miles y un KPI de **participación**. Mismos datos de matrícula escolar.

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

Construye un tablero interactivo con **Gradio** sobre la matrícula escolar 2025 (MINEDUC):
funciones de filtro + KPIs + visualización, publicable desde Colab con `demo.launch(share=True)`.

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: matrícula por dependencia, formato de miles, participación.
- En Colab: `!pip -q install gradio` antes de la última celda.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
