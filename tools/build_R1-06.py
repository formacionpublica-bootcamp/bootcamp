"""build_R1-06.py — módulo R1-06 (Estadística descriptiva).

Rama R1 (Análisis y Visualización). Resumir una variable sin engañarse: media vs
mediana con asimetría, dispersión (rango, desviación, CV), percentiles e IQR,
atípicos (regla IQR: atípico ≠ error), estudiantes por curso (promedio de razones
vs razón de totales) y comparar grupos (rural/urbano) con la medida correcta.

Rearmado 2026 (reemplaza la versión sobre 30 comunas): lección con la matrícula
2025 por establecimiento (matricula.csv, MINEDUC). Profundiza = transferencia:
población de 30 comunas (comunas.csv, Censo 2024) — robustez, IQR, puntaje z.
Convención de la casa.

Uso:  /opt/anaconda3/bin/python tools/build_R1-06.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_helpers as h

DEST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "ramas", "R1-analisis-visualizacion", "R1-06-estadistica-descriptiva")

RAW = h.REPO_RAW

INTRO = '''## ¿Cuántos estudiantes tiene un establecimiento «típico»?

Parece una pregunta simple. Pero en Chile conviven escuelas rurales de **un solo estudiante** con
liceos de **casi 4.000**. Un único número —el promedio— puede contar una historia muy distinta a
la realidad de la mayoría. La **estadística descriptiva** resume una columna con varias medidas a
la vez:

- **Centro:** ¿alrededor de qué valor se agrupan? (media, mediana)
- **Dispersión:** ¿qué tan separados están? (rango, desviación estándar, coeficiente de variación)
- **Posición:** ¿cómo se reparten? (cuartiles, percentiles, rango intercuartílico)

Trabajaremos con `mat_total` (estudiantes por establecimiento) y `cursos` de la matrícula oficial
2025: **10.945 establecimientos**.'''

EJ = [
 ("## 1. Centro: media y mediana",
  '''- **Media** (`.mean()`): suma todo y reparte en partes iguales. **Sensible a los extremos**:
  un liceo gigante la arrastra hacia arriba.
- **Mediana** (`.median()`): el valor del medio cuando ordenas. La mitad queda abajo, la mitad
  arriba. Es **robusta**: los extremos casi no la mueven.

Cuando hay **muchos valores chicos y pocos muy grandes** (asimetría a la derecha), la media queda
**por encima** de la mediana. Compararlas es la primera alarma.''',
  None,
  "Media y mediana de la matrícula",
  '''media = df["mat_total"].mean()
mediana = df["mat_total"].median()
razon = media / mediana
print(f"media: {media:.1f} | mediana: {mediana:.0f} | media/mediana: {razon:.2f}")''',
  '''# TODO: media y mediana de mat_total, y la razón media/mediana
media = ...
mediana = ...
razon = ...
print("media:", media, "| mediana:", mediana, "| razón:", razon)''',
  '''assert abs(media - df["mat_total"].mean()) < 1e-6, "media = df['mat_total'].mean()"
assert abs(mediana - df["mat_total"].median()) < 1e-6, "mediana = df['mat_total'].median()"
assert abs(razon - media / mediana) < 1e-9
assert razon > 1, "La media debería quedar sobre la mediana (asimetría a la derecha)"''',
  ".mean(), .median() y razon = media / mediana.",
  None),

 ("## 2. Dispersión: rango, desviación estándar y coeficiente de variación",
  '''- **Rango** = máximo − mínimo: rápido, pero depende solo de los dos extremos.
- **Desviación estándar** (`.std()`): cuánto se alejan los datos de la media, **en las mismas
  unidades** (estudiantes).
- **Coeficiente de variación** (CV) = desviación / media: la dispersión **relativa**, sin
  unidades. Permite comparar variables distintas. Un CV mayor que 1 indica que la desviación
  supera a la propia media: datos **muy** heterogéneos.''',
  None,
  "Mide la dispersión",
  '''rango = df["mat_total"].max() - df["mat_total"].min()
desviacion = df["mat_total"].std()
cv = desviacion / df["mat_total"].mean()
print(f"rango: {rango} | desviación: {desviacion:.1f} | CV: {cv:.2f}")''',
  '''# TODO: rango (máx − mín), desviación estándar y coeficiente de variación de mat_total
rango = ...
desviacion = ...
cv = ...
print("rango:", rango, "| desviación:", desviacion, "| CV:", cv)''',
  '''_s = df["mat_total"]
assert rango == _s.max() - _s.min(), "rango = máximo − mínimo"
assert abs(desviacion - _s.std()) < 1e-6, "desviacion = df['mat_total'].std()"
assert abs(cv - _s.std() / _s.mean()) < 1e-9, "cv = desviación / media"''',
  'df["mat_total"].max() - df["mat_total"].min(); .std(); cv = desviacion / media.',
  None),

 ("## 3. Posición: cuartiles, percentiles y rango intercuartílico",
  '''Los **percentiles** cortan los datos ordenados: el percentil 90 deja al 90% por debajo. Los
**cuartiles** son los percentiles 25 (Q1), 50 (la mediana) y 75 (Q3). Se calculan con
`.quantile(0.25)`, `.quantile(0.75)`, etc.

El **rango intercuartílico** (IQR = Q3 − Q1) mide el ancho del **50% central**: a diferencia del
rango, no le importan los extremos. `describe()` muestra casi todo de una vez:''',
  '''df["mat_total"].describe()''',
  "Cuartiles, IQR y percentil 90",
  '''q1 = df["mat_total"].quantile(0.25)
q3 = df["mat_total"].quantile(0.75)
iqr = q3 - q1
p90 = df["mat_total"].quantile(0.90)
print(f"Q1: {q1:.0f} | Q3: {q3:.0f} | IQR: {iqr:.0f} | P90: {p90:.0f}")
print(f"La mitad central de los establecimientos tiene entre {q1:.0f} y {q3:.0f} estudiantes.")''',
  '''# TODO: Q1, Q3, IQR (Q3 − Q1) y percentil 90 de mat_total
q1 = ...
q3 = ...
iqr = ...
p90 = ...
print("Q1:", q1, "| Q3:", q3, "| IQR:", iqr, "| P90:", p90)''',
  '''_s = df["mat_total"]
assert q1 == _s.quantile(0.25) and q3 == _s.quantile(0.75), "Usa .quantile(0.25) y .quantile(0.75)"
assert iqr == q3 - q1, "iqr = q3 - q1"
assert p90 == _s.quantile(0.90), "p90 = .quantile(0.90)"''',
  ".quantile(0.25), .quantile(0.75), iqr = q3 - q1, .quantile(0.90).",
  None),

 ("## 4. Atípicos con la regla del IQR (atípico ≠ error)",
  '''Una regla estándar marca como **atípico** todo valor sobre `Q3 + 1,5 × IQR` (o bajo
`Q1 − 1,5 × IQR`). Es la regla que dibujan los gráficos de caja.

Pero ojo: **atípico no significa error**. En R1-04 un -1 era imposible y había que corregirlo;
aquí un liceo con 3.000 estudiantes es raro, pero **real**. Lo que corresponde es mirarlo, no
borrarlo.''',
  None,
  "Cuenta los atípicos y mira el más grande",
  '''limite_sup = q3 + 1.5 * iqr
atipicos = df[df["mat_total"] > limite_sup]
n_atipicos = len(atipicos)
el_mas_grande = df.loc[df["mat_total"].idxmax(), "nombre"]
print(f"límite: {limite_sup:.0f} estudiantes | atípicos: {n_atipicos} ({n_atipicos / len(df):.1%})")
print("el más grande:", el_mas_grande)
atipicos.sort_values("mat_total", ascending=False)[["nombre", "comuna", "dependencia", "mat_total"]].head()''',
  '''# TODO: límite superior de la regla IQR, tabla de atípicos, cuántos son, y el nombre del más grande
limite_sup = ...
atipicos = ...
n_atipicos = ...
el_mas_grande = ...
print("límite:", limite_sup, "| atípicos:", n_atipicos, "| el más grande:", el_mas_grande)''',
  '''_s = df["mat_total"]
_q1, _q3 = _s.quantile(0.25), _s.quantile(0.75)
_lim = _q3 + 1.5 * (_q3 - _q1)
assert abs(limite_sup - _lim) < 1e-9, "limite_sup = q3 + 1.5 * iqr"
assert n_atipicos == int((_s > _lim).sum()), "Cuenta las filas con mat_total > limite_sup"
assert el_mas_grande == df.loc[_s.idxmax(), "nombre"], "Usa df.loc[df['mat_total'].idxmax(), 'nombre']"''',
  'limite_sup = q3 + 1.5 * iqr ; atipicos = df[df["mat_total"] > limite_sup] ; idxmax() para el más grande.',
  None),

 ("## 5. Leer el sesgo: ¿cuántos están sobre el promedio?",
  '''Si el promedio fuera un buen «valor típico», más o menos la mitad de los establecimientos
estaría por encima. Con datos asimétricos, **la mayoría queda por debajo**: unos pocos grandes
levantan el promedio.''',
  None,
  "Proporción de establecimientos sobre el promedio",
  '''pct_sobre_promedio = 100 * (df["mat_total"] > df["mat_total"].mean()).mean()
print(f"{pct_sobre_promedio:.1f}% de los establecimientos supera el promedio de {df['mat_total'].mean():.0f}")''',
  '''# TODO: % de establecimientos con mat_total MAYOR al promedio
# pista: la media de una condición (True/False) es la proporción de True
pct_sobre_promedio = ...
print(pct_sobre_promedio)''',
  '''_esp = 100 * (df["mat_total"] > df["mat_total"].mean()).mean()
assert abs(pct_sobre_promedio - _esp) < 1e-6, "100 * (df['mat_total'] > df['mat_total'].mean()).mean()"
assert pct_sobre_promedio < 50''',
  '100 * (df["mat_total"] > df["mat_total"].mean()).mean()',
  None),

 ("## 6. Estudiantes por curso: promedio de razones vs razón de totales",
  '''`mat_total / cursos` aproxima el **tamaño de curso** de cada establecimiento. Hay dos formas de
resumirlo y **no dan lo mismo**:

- **Promedio de razones**: calculas la razón en cada establecimiento y promedias. Cada
  establecimiento pesa igual → responde «¿cómo es el curso en el **establecimiento** típico?».
- **Razón de totales**: total de estudiantes / total de cursos. Cada **estudiante** pesa igual →
  responde «¿en qué tamaño de curso está el **estudiante** típico?».

Como las escuelas pequeñas (rurales, multigrado) tienen cursos chicos y son muchas, el primer
número sale más bajo. Ninguno está «mal»: hay que **decir cuál usaste**.''',
  None,
  "Calcula ambas medidas",
  '''df["est_por_curso"] = df["mat_total"] / df["cursos"]
promedio_de_razones = df["est_por_curso"].mean()
razon_de_totales = df["mat_total"].sum() / df["cursos"].sum()
print(f"promedio de razones: {promedio_de_razones:.1f} | razón de totales: {razon_de_totales:.1f} estudiantes por curso")''',
  '''# TODO: columna est_por_curso = mat_total / cursos
df["est_por_curso"] = ...
# TODO: promedio de esa columna, y total de estudiantes / total de cursos
promedio_de_razones = ...
razon_de_totales = ...
print("promedio de razones:", promedio_de_razones, "| razón de totales:", razon_de_totales)''',
  '''_r = df["mat_total"] / df["cursos"]
assert abs(df["est_por_curso"] - _r).max() < 1e-9, "est_por_curso = mat_total / cursos"
assert abs(promedio_de_razones - _r.mean()) < 1e-9
assert abs(razon_de_totales - df["mat_total"].sum() / df["cursos"].sum()) < 1e-9, "Suma todos los estudiantes y divide por la suma de todos los cursos"
assert razon_de_totales > promedio_de_razones''',
  'df["mat_total"] / df["cursos"]; luego .mean() de esa columna vs df["mat_total"].sum() / df["cursos"].sum().',
  None),

 ("## 7. Comparar grupos: rural vs urbano",
  '''Para comparar grupos, `groupby` + `agg` calcula varias medidas a la vez. Compara el tamaño de
curso en establecimientos **rurales** (`rural = 1`) y **urbanos** (`rural = 0`) mirando la
cantidad, la media **y** la mediana.''',
  None,
  "Tamaño de curso por ruralidad",
  '''resumen = df.groupby("rural")["est_por_curso"].agg(["count", "mean", "median"]).round(1)
brecha = resumen.loc[0, "median"] / resumen.loc[1, "median"]
print(resumen)
print(f"El curso urbano típico es {brecha:.1f} veces el rural típico (medianas).")''',
  '''# TODO: count, mean y median de est_por_curso por rural
resumen = ...
# TODO: mediana urbana (rural = 0) dividida por mediana rural (rural = 1)
brecha = ...
print(resumen)
print("brecha:", brecha)''',
  '''_g = df.groupby("rural")["est_por_curso"]
assert list(resumen.columns) == ["count", "mean", "median"], "Usa .agg(['count', 'mean', 'median'])"
assert abs(resumen.loc[1, "median"] - _g.median()[1]) < 0.06
assert abs(brecha - _g.median()[0] / _g.median()[1]) < 0.02, "brecha = mediana urbana / mediana rural"''',
  'df.groupby("rural")["est_por_curso"].agg(["count", "mean", "median"]); brecha con resumen.loc[0, "median"] / resumen.loc[1, "median"].',
  None),

 ("## 8. Interpretar sin engañarse: ¿en qué grupo miente más el promedio?",
  '''Usa la razón **media/mediana** de `mat_total` en cada grupo: mientras más lejos de 1, más
asimétrico el grupo y más engaña su promedio. Guarda en `razones` una Serie con la razón para
rural (1) y urbano (0), y elige la conclusión en `conclusion`:

- **A.** El grupo **urbano** es el más asimétrico: su promedio exagera el tamaño de la escuela urbana típica.
- **B.** El grupo **rural** es el más asimétrico: unas pocas escuelas rurales grandes inflan su
  promedio, y la escuela rural típica es mucho más pequeña de lo que el promedio sugiere.
- **C.** Ambos grupos son simétricos (razón cercana a 1): el promedio describe bien a los dos.''',
  None,
  "Razón media/mediana por grupo",
  '''g = df.groupby("rural")["mat_total"]
razones = g.mean() / g.median()
print(pd.DataFrame({"media": g.mean().round(1), "mediana": g.median(), "media/mediana": razones.round(2)}))
conclusion = "B"''',
  '''g = df.groupby("rural")["mat_total"]
# TODO: razón media/mediana por grupo (una Serie con índice 0 y 1)
razones = ...
print(razones)
# TODO: "A", "B" o "C"
conclusion = ...''',
  '''_g = df.groupby("rural")["mat_total"]
_raz = _g.mean() / _g.median()
assert abs(razones[0] - _raz[0]) < 1e-9 and abs(razones[1] - _raz[1]) < 1e-9, "razones = g.mean() / g.median()"
_letra = "C" if (abs(_raz - 1) < 0.15).all() else ("B" if _raz[1] > _raz[0] else "A")
assert str(conclusion).strip().upper() == _letra, "Mira cuál de las dos razones está más lejos de 1"''',
  "razones = g.mean() / g.median(); el grupo con la razón más alta es el más asimétrico.",
  None),
]

REFLEXION = '''## ✍️ Reflexión (no se corrige, pero es lo más importante)

Un informe dice: «La escuela rural chilena tiene en promedio 89 estudiantes». Con lo que viste hoy,
¿qué número le reportarías a una autoridad que decide el financiamiento de escuelas rurales, y cómo
lo acompañarías (mediana, percentiles, cantidad de escuelas) para que no se lleve una idea equivocada?'''

CIERRE = '''## Errores típicos

- **Reportar solo el promedio** con datos asimétricos → acompáñalo de la mediana.
- **Borrar atípicos porque «se ven raros»** → atípico ≠ error; mira primero si es real.
- **Promediar razones sin decirlo** → el promedio de razones y la razón de totales responden preguntas distintas.
- **Comparar grupos solo por la media** → compara también mediana y cantidad de casos.
- **Olvidar las unidades** → la desviación está en estudiantes; el CV no tiene unidades.

## Cierre

- Centro (media/mediana), dispersión (rango, desviación, CV) y posición (cuartiles, IQR, percentiles): **siempre juntos**.
- La razón media/mediana es una alarma rápida de asimetría.
- Comparar grupos sin engañarse = misma medida, la correcta, y declarada.

> *En R1-07 vas a ver estas mismas distribuciones en gráficos: histogramas y cajas que muestran
> de un vistazo lo que hoy calculaste.*'''


def build_leccion(con_sol):
    nb = h.new_notebook()
    cells = [
        h.header_cell("R1-06", "Estadística descriptiva", "R1", "Analista de Datos", "7",
                      ["Comparar **media y mediana** y leer la asimetría.",
                       "Medir **dispersión**: rango, desviación estándar y coeficiente de variación.",
                       "Usar **percentiles, cuartiles e IQR**, y detectar **atípicos** sin confundirlos con errores.",
                       "Distinguir **promedio de razones** y **razón de totales** (estudiantes por curso).",
                       "**Comparar grupos** (rural/urbano) sin dejarse engañar por un promedio."],
                      "resumir e interpretar una variable con varias medidas a la vez, y comunicar el número correcto.",
                      "matrícula oficial 2025 por establecimiento (MINEDUC): estudiantes y cursos de 10.945 establecimientos.",
                      n_checks=len(EJ)),
        h.setup_cell("matricula.csv"),
        h.md(INTRO),
    ]
    for i, (sec_t, sec_b, demo, ej_t, sol, todo, chk, hint, post) in enumerate(EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        if demo:
            cells.append(h.code(demo))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
        if post:
            cells.append(h.code(post))
    cells.append(h.md(REFLEXION))
    cells.append(h.md(CIERRE))
    nb.cells = cells
    return nb


# ── Profundiza: transferencia a la población comunal ───────────────────────────
PROF_PREP = f'''import pandas as pd, os, urllib.request
CSV = "comunas.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("{RAW}/comunas.csv", CSV)
com = pd.read_csv(CSV)   # 30 comunas de muy distintos tamaños (INE, Censo 2024)
print(com.shape)
com["poblacion"].describe()'''

PROF_EJ = [
 ("## 1. Centro y sesgo en otra variable",
  "Dominio nuevo: la **población** de 30 comunas de muy distintos tamaños (Censo 2024), desde "
  "Puente Alto hasta Pichilemu. ¿Se repite el patrón de la matrícula?",
  "Razón media/mediana de la población",
  '''razon = com["poblacion"].mean() / com["poblacion"].median()
asimetrica_derecha = razon > 1.15
print(f"media: {com['poblacion'].mean():,.0f} | mediana: {com['poblacion'].median():,.0f} | razón: {razon:.2f}")''',
  '''# TODO: razón media/mediana de la población y si es claramente mayor que 1 (> 1.15)
razon = ...
asimetrica_derecha = ...
print(razon, asimetrica_derecha)''',
  '''assert abs(razon - com["poblacion"].mean() / com["poblacion"].median()) < 1e-9
assert asimetrica_derecha == (razon > 1.15)''',
  'com["poblacion"].mean() / com["poblacion"].median() y la comparación razon > 1.15.'),

 ("## 2. Robustez: ¿qué medida se mueve si saco una comuna?",
  "Una medida **robusta** casi no cambia si quitas un valor extremo. Saca la comuna más poblada "
  "y mide cuánto cambian (en %) la media y la mediana.",
  "Quita la comuna más grande y compara",
  '''sin_mayor = com[com["poblacion"] != com["poblacion"].max()]
cambio_media = 100 * (sin_mayor["poblacion"].mean() - com["poblacion"].mean()) / com["poblacion"].mean()
cambio_mediana = 100 * (sin_mayor["poblacion"].median() - com["poblacion"].median()) / com["poblacion"].median()
print(f"la media cambia {cambio_media:.1f}% | la mediana cambia {cambio_mediana:.1f}%")''',
  '''sin_mayor = com[com["poblacion"] != com["poblacion"].max()]
# TODO: cambio porcentual de la media y de la mediana al sacar la comuna más grande
cambio_media = ...
cambio_mediana = ...
print(cambio_media, cambio_mediana)''',
  '''_m0, _m1 = com["poblacion"].mean(), sin_mayor["poblacion"].mean()
_d0, _d1 = com["poblacion"].median(), sin_mayor["poblacion"].median()
assert abs(cambio_media - 100 * (_m1 - _m0) / _m0) < 1e-9
assert abs(cambio_mediana - 100 * (_d1 - _d0) / _d0) < 1e-9
assert abs(cambio_media) > abs(cambio_mediana), "La media debería moverse más que la mediana"''',
  "100 * (nuevo - original) / original, para .mean() y para .median()."),

 ("## 3. Atípicos con la regla del IQR",
  "Aplica la misma regla de la lección: atípico = sobre `Q3 + 1,5 × IQR`. ¿Qué comunas lo son?",
  "Comunas atípicas",
  '''q1, q3 = com["poblacion"].quantile([0.25, 0.75])
limite = q3 + 1.5 * (q3 - q1)
atipicas = sorted(com.loc[com["poblacion"] > limite, "comuna"])
print(f"límite: {limite:,.0f} habitantes | atípicas: {atipicas}")''',
  '''q1, q3 = com["poblacion"].quantile([0.25, 0.75])
# TODO: límite superior y lista ORDENADA de comunas sobre ese límite
limite = ...
atipicas = ...
print(limite, atipicas)''',
  '''_q1, _q3 = com["poblacion"].quantile([0.25, 0.75])
_lim = _q3 + 1.5 * (_q3 - _q1)
assert abs(limite - _lim) < 1e-6
assert list(atipicas) == sorted(com.loc[com["poblacion"] > _lim, "comuna"])''',
  'limite = q3 + 1.5 * (q3 - q1); sorted(com.loc[com["poblacion"] > limite, "comuna"]).'),

 ("## 4. Puntaje z: ¿a cuántas desviaciones del promedio?",
  "El **puntaje z** = (valor − media) / desviación dice cuán lejos está cada dato del promedio, en "
  "«desviaciones». Un |z| > 2 suele considerarse lejano. Pero cuidado: con datos asimétricos la "
  "media y la desviación ya están infladas por los extremos, así que el z **detecta menos** "
  "atípicos que la regla IQR.",
  "Calcula z y cuenta los lejanos",
  '''com["z"] = (com["poblacion"] - com["poblacion"].mean()) / com["poblacion"].std()
n_lejanos = int((com["z"].abs() > 2).sum())
comuna_max_z = com.loc[com["z"].idxmax(), "comuna"]
print(com.sort_values("z", ascending=False).head(4)[["comuna", "poblacion", "z"]].round(2))
print("comunas con |z| > 2:", n_lejanos, "| mayor z:", comuna_max_z)''',
  '''# TODO: columna z, cuántas comunas tienen |z| > 2, y la comuna con mayor z
com["z"] = ...
n_lejanos = ...
comuna_max_z = ...
print(n_lejanos, comuna_max_z)''',
  '''_z = (com["poblacion"] - com["poblacion"].mean()) / com["poblacion"].std()
assert abs(com["z"] - _z).max() < 1e-9, "z = (poblacion - media) / desviación"
assert n_lejanos == int((_z.abs() > 2).sum())
assert comuna_max_z == com.loc[_z.idxmax(), "comuna"]''',
  '(com["poblacion"] - com["poblacion"].mean()) / com["poblacion"].std(); luego .abs() > 2 y idxmax().'),
]

PROF_HEADER = '''# R1-06 · Estadística descriptiva — Profundización (opcional) 🔬

**Formación Pública — Rama R1 · Analista de Datos · Notebook de profundización**

Opcional y de **transferencia**: las mismas herramientas sobre otra variable — la **población de
30 comunas** de muy distintos tamaños (INE, Censo 2024). Medidas nuevas: **robustez** (qué pasa
al sacar un extremo) y **puntaje z**, comparado con la regla del IQR.

> Ojo: son 30 comunas elegidas para cubrir distintos tamaños, **no** todas las comunas del país:
> los resúmenes describen esta muestra, no «la comuna chilena».

> Cada ejercicio termina en una **celda de chequeo** con ✅ / pista.'''


def build_profundiza(con_sol):
    nb = h.new_notebook()
    cells = [h.md(PROF_HEADER), h.code(PROF_PREP)]
    for i, (sec_t, sec_b, ej_t, sol, todo, chk, hint) in enumerate(PROF_EJ, 1):
        cells.append(h.md(sec_t + "\n\n" + sec_b))
        cells.append(h.exercise_md(i, ej_t))
        cells.append(h.code(sol if con_sol else todo))
        cells.append(h.check_cell(i, chk, hint))
    cells.append(h.md("---\n\n*Fin de la profundización de R1-06.*"))
    nb.cells = cells
    return nb


README = '''# R1-06 · Estadística descriptiva

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-06-estadistica-descriptiva/leccion.ipynb)

Resumir una variable **sin engañarse**: media vs mediana y asimetría, dispersión (rango,
desviación estándar, coeficiente de variación), percentiles e IQR, atípicos con la regla del IQR
(atípico ≠ error), **estudiantes por curso** (promedio de razones vs razón de totales) y comparar
grupos rural/urbano con la medida correcta.

**Datos.** `matricula.csv`: matrícula oficial 2025 (MINEDUC) de 10.945 establecimientos, con
estudiantes (`mat_total`), cursos, dependencia y ruralidad. La profundización usa `comunas.csv`:
población de 30 comunas de distintos tamaños (INE, Censo 2024).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: robustez, atípicos por IQR y puntaje z sobre población comunal.
- [`GUIA_APRENDIZAJE.md`](GUIA_APRENDIZAJE.md) — pistas progresivas, errores frecuentes y autoevaluación.
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
