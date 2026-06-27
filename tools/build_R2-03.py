"""build_R2-03.py — módulo R2-03 (Estadística para modelar).

Rama R2 (Científico de Datos). Refactor de A5 + parte INFERENCIAL nueva. Enseña,
sobre compras_ml.csv: estadística descriptiva, intervalo de confianza, prueba de
hipótesis (t-test) y correlación, con scipy/statsmodels. Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R2-03.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R2-cientifico-de-datos", "R2-03-estadistica-para-modelar")

IMPORTS = "import pandas as pd, numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import stats"

EJ = [
 ("## 1. Describir antes de modelar",
  "Antes de cualquier modelo hay que **conocer la distribución**: centro, dispersión y cola. "
  "El monto de compras públicas tiene cola larga (pocas compras enormes).",
  "Calcula el resumen descriptivo del monto",
  '''x = df["monto_total"]
desc = {
    "media":   float(x.mean()),
    "mediana": float(x.median()),
    "p90":     float(x.quantile(0.90)),
    "std":     float(x.std()),
}
print(desc)''',
  '''x = df["monto_total"]
desc = {
    "media":   ...,   # TODO: x.mean()
    "mediana": ...,   # TODO: x.median()
    "p90":     ...,   # TODO: percentil 90 -> x.quantile(0.90)
    "std":     ...,   # TODO: x.std()
}
print(desc)''',
  '''assert set(desc) == {"media", "mediana", "p90", "std"}
assert desc["p90"] >= desc["mediana"]
assert desc["std"] > 0''',
  "x.mean(), x.median(), x.quantile(0.90) y x.std().",
  '''# (ilustración) Distribución del monto (escala log por la cola larga)
plt.figure(figsize=(6, 4))
plt.hist(df["monto_total"].clip(upper=df["monto_total"].quantile(0.99)), bins=40, color="#4240e5")
plt.xlabel("Monto total (CLP, recortado al p99)"); plt.ylabel("Frecuencia")
plt.title("Distribución del monto de compra"); plt.tight_layout(); plt.show()'''),

 ("## 2. Intervalo de confianza para la media",
  "La media de la muestra es un **estimado**. El **intervalo de confianza (95%)** dice en qué rango "
  "está, con incertidumbre, la media real.",
  "Calcula el IC 95% de la media del monto",
  '''x = df["monto_total"]
media = x.mean()
ic_low, ic_high = stats.t.interval(0.95, len(x) - 1, loc=media, scale=stats.sem(x))
print("media:", round(media), "| IC95%: [", round(ic_low), ",", round(ic_high), "]")''',
  '''x = df["monto_total"]
media = x.mean()
# TODO: usa stats.t.interval(0.95, len(x)-1, loc=media, scale=stats.sem(x))
ic_low, ic_high = ...
print("media:", round(media), "| IC95%: [", round(ic_low), ",", round(ic_high), "]")''',
  '''assert ic_low < media < ic_high
assert ic_high - ic_low > 0''',
  "stats.t.interval(0.95, len(x)-1, loc=media, scale=stats.sem(x)) devuelve (low, high).",
  None),

 ("## 3. Prueba de hipótesis: ¿difieren dos grupos?",
  "¿El monto de las compras a proveedores **Grandes** difiere del de los **Micro** más allá del azar? "
  "Un **t-test** lo responde: si el *p-valor* < 0.05, la diferencia es significativa.",
  "Compara montos: Grande vs Micro",
  '''grande = df[df["tamano_proveedor"] == "Grande"]["monto_total"]
micro  = df[df["tamano_proveedor"] == "Micro"]["monto_total"]
t_stat, p_valor = stats.ttest_ind(grande, micro, equal_var=False)
print("t:", round(t_stat, 2), "| p-valor:", p_valor)
print("¿Diferencia significativa al 5%?", p_valor < 0.05)''',
  '''grande = df[df["tamano_proveedor"] == "Grande"]["monto_total"]
micro  = df[df["tamano_proveedor"] == "Micro"]["monto_total"]
# TODO: stats.ttest_ind(grande, micro, equal_var=False) -> (t_stat, p_valor)
t_stat, p_valor = ...
print("t:", round(t_stat, 2), "| p-valor:", p_valor)
print("¿Diferencia significativa al 5%?", p_valor < 0.05)''',
  '''assert 0.0 <= p_valor <= 1.0
assert np.isfinite(t_stat)''',
  "stats.ttest_ind(grande, micro, equal_var=False) (test de Welch).",
  None),

 ("## 4. Correlación: ¿se mueven juntas dos variables?",
  "¿A mayor **cantidad** de artículos, mayor **monto**? La correlación de Pearson mide la relación "
  "lineal (−1 a 1) y su *p-valor* dice si es significativa.",
  "Correlación entre cantidad y monto",
  '''r, p = stats.pearsonr(df["cantidad"], df["monto_total"])
print("r de Pearson:", round(r, 3), "| p-valor:", p)''',
  '''# TODO: stats.pearsonr(df["cantidad"], df["monto_total"]) -> (r, p)
r, p = ...
print("r de Pearson:", round(r, 3), "| p-valor:", p)''',
  '''assert -1.0 <= r <= 1.0
assert 0.0 <= p <= 1.0''',
  "stats.pearsonr(df['cantidad'], df['monto_total']) devuelve (coef, p_valor).",
  '''# (ilustración) Cantidad vs monto (muestra, por la masa de puntos)
m = df.sample(min(800, len(df)), random_state=42)
plt.figure(figsize=(6, 4))
plt.scatter(m["cantidad"], m["monto_total"], s=10, alpha=0.4, color="#ff6b35")
plt.xlabel("Cantidad"); plt.ylabel("Monto total"); plt.title("Cantidad vs monto")
plt.tight_layout(); plt.show()'''),
]

CIERRE = '''## Cierre

- La **descriptiva** (media, mediana, p90, dispersión) revela la forma del dato antes de modelar.
- Un **intervalo de confianza** acompaña cada estimación con su incertidumbre.
- Una **prueba de hipótesis** distingue una diferencia real del azar (p-valor < 0.05).
- La **correlación** sugiere relaciones, pero *correlación no es causalidad*.

> *Estadística just-in-time: la usamos para tomar decisiones honestas, no como teoría aparte.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R2-03", "Estadística para modelar", "B", "Data Scientist", "5–6",
                      ["Describir una distribución real (centro, dispersión, cola).",
                       "Estimar con **intervalos de confianza**.",
                       "Contrastar grupos con una **prueba de hipótesis** (t-test).",
                       "Medir **correlación** e interpretarla con cuidado."],
                      "usar estadística inferencial para sustentar decisiones de modelado.",
                      "monto, cantidad y tamaño de proveedor de compras públicas (ChileCompra).",
                      n_checks=4),
        h.setup_cell("compras_ml.csv", IMPORTS),
        h.md("### Datos cargados arriba. A explorarlos con rigor."),
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


# ── Profundización ───────────────────────────────────────────────────────────
PROF_PREP = '''import pandas as pd, numpy as np, os, urllib.request
from scipy import stats
import statsmodels.api as sm
CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/compras_ml.csv", CSV)
df = pd.read_csv(CSV)
print("Datos:", df.shape)'''

PROF_EJ = [
 ("## 1. Intervalo por *bootstrap* (sin fórmulas)",
  "Cuando la distribución es rara, el **bootstrap** estima el intervalo remuestreando los datos. "
  "Sin supuestos: solo computación.",
  "Construye un IC 95% por bootstrap para la media",
  '''x = df["monto_total"].values
rng = np.random.default_rng(42)
medias = [rng.choice(x, size=len(x), replace=True).mean() for _ in range(300)]
ic_low, ic_high = np.percentile(medias, [2.5, 97.5])
print("IC95% bootstrap: [", round(ic_low), ",", round(ic_high), "]")''',
  '''x = df["monto_total"].values
rng = np.random.default_rng(42)
# TODO: 300 medias de remuestras (rng.choice(x, size=len(x), replace=True).mean())
medias = ...
ic_low, ic_high = np.percentile(medias, [2.5, 97.5])
print("IC95% bootstrap: [", round(ic_low), ",", round(ic_high), "]")''',
  '''assert ic_low < df["monto_total"].mean() < ic_high''',
  "Lista por comprensión de 300 rng.choice(x, size=len(x), replace=True).mean()."),

 ("## 2. Alternativa robusta: Mann–Whitney",
  "El t-test asume normalidad. Con colas largas, el test no paramétrico de **Mann–Whitney** es más seguro.",
  "Compara Grande vs Micro sin asumir normalidad",
  '''grande = df[df["tamano_proveedor"] == "Grande"]["monto_total"]
micro  = df[df["tamano_proveedor"] == "Micro"]["monto_total"]
u, p = stats.mannwhitneyu(grande, micro, alternative="two-sided")
print("U:", round(u, 1), "| p-valor:", p)''',
  '''grande = df[df["tamano_proveedor"] == "Grande"]["monto_total"]
micro  = df[df["tamano_proveedor"] == "Micro"]["monto_total"]
# TODO: stats.mannwhitneyu(grande, micro, alternative="two-sided") -> (u, p)
u, p = ...
print("U:", round(u, 1), "| p-valor:", p)''',
  '''assert 0.0 <= p <= 1.0''',
  "stats.mannwhitneyu(grande, micro, alternative='two-sided')."),

 ("## 3. Una primera regresión (statsmodels)",
  "La inferencia se conecta con el modelado: una **regresión lineal** estima cuánto sube el monto por "
  "unidad de cantidad, con su significancia.",
  "Ajusta monto ~ cantidad con OLS",
  '''X = sm.add_constant(df["cantidad"])
modelo = sm.OLS(df["monto_total"], X).fit()
r2 = modelo.rsquared
print("R²:", round(r2, 4), "| coef cantidad:", round(modelo.params["cantidad"], 2))''',
  '''X = sm.add_constant(df["cantidad"])
# TODO: ajusta sm.OLS(df["monto_total"], X).fit() y toma .rsquared
modelo = ...
r2 = ...
print("R²:", round(r2, 4))''',
  '''assert 0.0 <= r2 <= 1.0''',
  "sm.OLS(y, X).fit(); el atributo .rsquared es el R²."),
]

PROF_HEADER = '''# R2-03 · Estadística para modelar — Profundización (opcional) 🔬

**Formación Pública — Línea B · Data Scientist · Notebook de profundización**

Opcional. Herramientas más finas: **bootstrap** para intervalos sin supuestos, el test no paramétrico
de **Mann–Whitney** y una primera **regresión lineal** con statsmodels. Mismos datos de compras públicas.

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R2-03.*"))
    nb.cells = cells
    return nb


def main():
    os.makedirs(DEST, exist_ok=True)
    h.write_notebook(build_leccion(False),    os.path.join(DEST, "leccion.ipynb"))
    h.write_notebook(build_leccion(True),     os.path.join(DEST, "solucion.ipynb"))
    h.write_notebook(build_profundiza(False), os.path.join(DEST, "profundiza.ipynb"))
    h.write_notebook(build_profundiza(True),  os.path.join(DEST, "profundiza_solucion.ipynb"))
    open(os.path.join(DEST, "README.md"), "w", encoding="utf-8").write(
        '''# R2-03 · Estadística para modelar

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R2-cientifico-de-datos/R2-03-estadistica-para-modelar/leccion.ipynb)

Descriptiva + **inferencial** (intervalo de confianza, prueba de hipótesis, correlación) con
scipy/statsmodels sobre datos reales de compras públicas (`compras_ml.csv`).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: bootstrap, Mann–Whitney, regresión OLS.
''')
    print("Generado en", DEST)


if __name__ == "__main__":
    main()
