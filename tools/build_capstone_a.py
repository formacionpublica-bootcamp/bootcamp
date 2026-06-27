# -*- coding: utf-8 -*-
"""Construye el Capstone A: dataset provisto real (ChileCompra) + notebook scaffold
+ ejemplo resuelto + README con rúbrica. Carpeta: A8-capstone."""
import json, os

BASE = "A8-capstone"
RAW = os.path.join("data", "02OCLicitacion.csv")
REPO = "formacionpublica-bootcamp/bootcamp"
os.makedirs(BASE, exist_ok=True)

# --------------------------------------------------------------------------- #
# 1. Dataset provisto real
# --------------------------------------------------------------------------- #
def construir_dataset():
    import pandas as pd
    cols = ['codigoOC','FechaEnvioOC','Institucion','RegionUnidadCompra','RubroN1','Proveedor','MontoNetoOC_CLP']
    df = pd.read_csv(RAW, encoding='latin1', sep=';', decimal=',', usecols=cols, nrows=150000)
    df = df.dropna(subset=cols)
    df = df[(df['MontoNetoOC_CLP'] >= 200_000) & (df['MontoNetoOC_CLP'] <= 300_000_000)]
    fecha = pd.to_datetime(df['FechaEnvioOC'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
    df = df[fecha.notna()].copy()
    fecha = fecha[fecha.notna()]
    out = pd.DataFrame({
        'codigo_oc': df['codigoOC'].astype(str).str.strip(),
        'fecha': fecha.dt.strftime('%Y-%m-%d'),
        'mes': fecha.dt.month,
        'organismo': df['Institucion'].astype(str).str.strip(),
        'region': df['RegionUnidadCompra'].astype(str).str.strip(),
        'rubro': df['RubroN1'].astype(str).str.strip(),
        'proveedor': df['Proveedor'].astype(str).str.strip(),
        'monto': df['MontoNetoOC_CLP'].astype(int),
    })
    out = out.sample(n=min(4000, len(out)), random_state=42).sort_values('fecha').reset_index(drop=True)
    out.to_csv(os.path.join(BASE, 'compras_capstone.csv'), index=False)
    print(f"Dataset: {len(out)} filas | {out['region'].nunique()} regiones | {out['rubro'].nunique()} rubros | {out['organismo'].nunique()} organismos")

if os.path.exists(RAW):
    construir_dataset()
else:
    print("Aviso: falta data/02OCLicitacion.csv; conservo el CSV existente.")

# --------------------------------------------------------------------------- #
# 2. Celdas (scaffold y ejemplo comparten la mayoría; difieren en los pasos resueltos)
# --------------------------------------------------------------------------- #
TITULO = """# Capstone A · Tu pregunta, tus datos

**Formación Pública — Capa A · Datos sin miedo · Proyecto final**

Tu proyecto de cierre de la Capa A. No hay una "respuesta correcta": **eliges una pregunta real, la
respondes con datos y la comunicas**. Usarás todo lo aprendido: pandas (A1), cruzar y resumir (A2),
limpieza (A3), estadística (A5), visualización y ética (A6) y, si quieres, IA como copiloto (A7).

Sigue los 6 pasos del **Ciclo Pública**. Al final hay una **autoevaluación con la rúbrica**.

**Entregable:** este notebook completo, con tu pregunta respondida, un gráfico honesto y una
conclusión. Idealmente, súbelo a tu GitHub como pieza de portafolio."""

PASO0 = """## Paso 0 · Elige tus datos
- **Opción A — Dataset provisto (recomendado para partir):** órdenes de compra reales de ChileCompra
  (`compras_capstone.csv`): `fecha`, `mes`, `organismo`, `region`, `rubro`, `proveedor`, `monto`.
- **Opción B — Trae tu propio dato:** si tienes un CSV de tu institución, súbelo a Colab (panel
  izquierdo → 📁 → subir) y cámbialo en `pd.read_csv(...)`.

Ejecuta la celda para cargar los datos."""

CARGA = """import os, urllib.request
import pandas as pd

ARCHIVO = "compras_capstone.csv"   # cámbialo por tu archivo si usas la Opción B
if not os.path.exists(ARCHIVO):
    try:
        url = "https://raw.githubusercontent.com/%s/main/A8-capstone/compras_capstone.csv"
        urllib.request.urlretrieve(url, ARCHIVO)
    except Exception:
        print("Si estás en Colab, sube el archivo manualmente.")

df = pd.read_csv(ARCHIVO)
print(f"{len(df)} filas, {len(df.columns)} columnas")
df.head()""" % REPO

PASO1 = """## Paso 1 · Pregunta
¿Qué decisión o curiosidad pública quieres responder? Una buena pregunta es concreta y se puede
responder con estos datos. Ejemplos: *¿qué región concentra más gasto?*, *¿en qué rubro se va la
plata?*, *¿en qué meses se dispara el gasto?*, *¿hay proveedores que concentran muchas órdenes?*"""

PASO1_TODO = """**✍️ Tu pregunta:** _(escríbela aquí, reemplazando esta línea)_"""
PASO1_SOL = """**✍️ Mi pregunta:** ¿En qué **rubros** se concentra el gasto en licitaciones? (¿Dónde se va la plata?)"""

PASO2 = """## Paso 2 · Limpia
Mira los datos y déjalos listos. Revisa nulos (`df.info()`), tipos, y texto inconsistente
(`.str.strip()`). Guarda el resultado en `df_limpio`."""

PASO2_TODO = """# TODO: inspecciona y limpia. Mínimo: revisa nulos y tipos. Guarda en df_limpio.
df_limpio = df.copy()
# ... tu limpieza aquí ...
df_limpio.info()"""

PASO2_SOL = """df_limpio = df.copy()
# Normalizamos el texto del rubro por si hay espacios o mayúsculas inconsistentes
df_limpio["rubro"] = df_limpio["rubro"].str.strip()
# Confirmamos que no falten datos en las columnas que usaremos
print("Nulos por columna:\\n", df_limpio[["rubro", "monto"]].isna().sum())
df_limpio.info()"""

PASO3 = """## Paso 3 · Explora y responde
Usa filtrar, `value_counts`, `groupby(...).sum()`, `mean`/`median`… para **responder tu pregunta**.
Guarda el resultado principal en `respuesta`."""

PASO3_TODO = """# TODO: calcula la respuesta a tu pregunta (ej. gasto por region/rubro/mes).
# Pista: df_limpio.groupby("region")["monto"].sum().sort_values(ascending=False)
respuesta = None
respuesta"""

PASO3_SOL = """# Gasto total por rubro, de mayor a menor (top 10)
respuesta = (df_limpio.groupby("rubro")["monto"].sum()
             .sort_values(ascending=False)
             .head(10))
respuesta"""

PASO4 = """## Paso 4 · Comunica (un gráfico honesto)
Haz **un** gráfico claro que muestre tu respuesta. Recuerda A6: título, ejes rotulados, fuente, y
nada de ejes que engañen. Barras para categorías, líneas para evolución en el tiempo."""

PASO4_TODO = """import matplotlib.pyplot as plt
# TODO: grafica tu 'respuesta' (ej. respuesta.head(10).plot(kind="barh"))
# Recuerda título, etiqueta de eje y fuente.
plt.show()"""

PASO4_SOL = """import matplotlib.pyplot as plt

ax = (respuesta / 1_000_000).sort_values().plot(kind="barh", figsize=(8, 5), color="#0a7e7e")
ax.set_title("Gasto en licitaciones por rubro (top 10)")
ax.set_xlabel("Gasto (millones de CLP)")
ax.set_ylabel("Rubro")
plt.figtext(0.99, -0.02, "Fuente: ChileCompra / MercadoPúblico", ha="right", fontsize=8)
plt.tight_layout()
plt.show()"""

PASO5 = """## Paso 5 · (Opcional) IA como copiloto
Si hiciste A7, pídele a un LLM que te ayude a **redactar** el resumen de tu hallazgo — y luego
**verifica** que las cifras coincidan con tu análisis. Nunca pegues datos personales."""

PASO6 = """## Paso 6 · Conclusión y reflexión
Responde en tus palabras:

- **Hallazgo:** ¿qué encontraste?
- **Para la jefatura:** ¿qué decisión o acción sugiere tu resultado?
- **Nota ética (A6):** ¿qué **no** se puede concluir de estos datos? ¿algún sesgo o límite?"""

PASO6_TODO = PASO6 + """

_(reemplaza estas líneas con tus respuestas)_"""

PASO6_SOL = PASO6 + """

- **Hallazgo:** el gasto se concentra fuertemente en unos pocos rubros (encabezados por alimentos y
  servicios), mientras la mayoría de los rubros suma montos pequeños.
- **Para la jefatura:** conviene mirar de cerca los contratos de los 2–3 rubros líderes: ahí están
  las decisiones de mayor impacto presupuestario.
- **Nota ética:** este es solo el monto de **licitaciones** de la muestra; no incluye convenio marco
  ni trato directo, así que **no** representa el gasto total del Estado ni permite juzgar a un
  organismo. Es una foto parcial."""

AUTOEVAL_CODE = """# Autoevaluación suave — no califica tu respuesta, solo confirma que hiciste cada paso.
hechos = {
    "Cargaste datos": "df" in dir() and len(df) > 0,
    "Limpiaste (df_limpio)": "df_limpio" in dir(),
    "Calculaste una respuesta": "respuesta" in dir() and respuesta is not None,
}
for paso, ok in hechos.items():
    print(("✅ " if ok else "⬜ ") + paso)
print("\\nAhora evalúate con la rúbrica de abajo (aprobado: 12/18).")"""

RUBRICA = """## Rúbrica (autoevalúate, 0–3 cada una)
| Criterio | 0–3 |
|---|---|
| Pregunta clara y pública | |
| Datos bien tratados (limpieza) | |
| Análisis válido que responde la pregunta | |
| Visualización honesta y legible | |
| Conclusión accionable | |
| Reflexión (qué no concluir / ética) | |

**Aprobado: 12 de 18.** Cuando estés conforme, sube el notebook a tu GitHub: es tu primera pieza de
portafolio de datos públicos. 🎉

> Esto te certifica la **Alfabetización de datos públicos** (Capa A). Si quieres seguir, te espera la
> Capa B (Ciencia de datos) o la Capa C (IA aplicada)."""


def md(t, cid): return {"cell_type": "markdown", "metadata": {}, "id": cid, "source": t}
def code(t, cid): return {"cell_type": "code", "metadata": {}, "id": cid, "execution_count": None, "outputs": [], "source": t}

def build(resuelto):
    p1 = PASO1_SOL if resuelto else PASO1_TODO
    p2 = PASO2_SOL if resuelto else PASO2_TODO
    p3 = PASO3_SOL if resuelto else PASO3_TODO
    p4 = PASO4_SOL if resuelto else PASO4_TODO
    p6 = PASO6_SOL if resuelto else PASO6_TODO
    cells = [
        md(TITULO, "c00"), md(PASO0, "c01"), code(CARGA, "c02"),
        md(PASO1, "c03"), md(p1, "c04"),
        md(PASO2, "c05"), code(p2, "c06"),
        md(PASO3, "c07"), code(p3, "c08"),
        md(PASO4, "c09"), code(p4, "c10"),
        md(PASO5, "c11"),
        md(p6, "c12"),
        code(AUTOEVAL_CODE, "c13"), md(RUBRICA, "c14"),
    ]
    return {"cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python"}},
            "nbformat": 4, "nbformat_minor": 5}

json.dump(build(False), open(os.path.join(BASE, "proyecto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(build(True), open(os.path.join(BASE, "ejemplo_resuelto.ipynb"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# --------------------------------------------------------------------------- #
# 3. README
# --------------------------------------------------------------------------- #
README = """# Capstone A · Tu pregunta, tus datos

**Proyecto final de la Capa A (Datos sin miedo)** del Bootcamp **Formación Pública**.
Se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/%s/blob/main/A8-capstone/proyecto.ipynb)

## Qué es
Tu primera pieza de portafolio: **eliges una pregunta pública, la respondes con datos reales y la
comunicas**. Integra todo lo de la Capa A (pandas, cruzar y resumir, limpieza, estadística,
visualización y ética, e IA como copiloto). No hay una respuesta única.

## Cómo entregar
- **Opción A (recomendada para partir):** usa el dataset provisto `compras_capstone.csv` (órdenes de
  compra reales de ChileCompra).
- **Opción B:** trae un CSV de **tu propia institución** y cámbialo en la celda de carga.

## Los 6 pasos (Ciclo Pública)
1. **Pregunta** — una pregunta concreta y pública.
2. **Limpia** — deja la tabla lista (`df_limpio`).
3. **Explora y responde** — `groupby`/`value_counts`/estadística → `respuesta`.
4. **Comunica** — un gráfico honesto (título, ejes, fuente).
5. *(Opcional)* **IA como copiloto** — redactar y **verificar** con un LLM.
6. **Conclusión y reflexión** — hallazgo, qué le dirías a tu jefatura y qué **no** concluir.

## Rúbrica (0–3 cada una · aprobado 12/18)
| Criterio | Qué se evalúa |
|---|---|
| Pregunta clara y pública | Es concreta y respondible con los datos. |
| Datos bien tratados | Revisó nulos/tipos/texto; documentó. |
| Análisis válido | El cálculo responde de verdad la pregunta. |
| Visualización honesta | Clara, rotulada, sin engañar. |
| Conclusión accionable | Dice algo útil para una jefatura. |
| Reflexión / ética | Reconoce límites y qué no concluir. |

## Archivos
| Archivo | Para qué |
| --- | --- |
| `proyecto.ipynb` | El scaffold del estudiante (los 6 pasos con TODO). |
| `ejemplo_resuelto.ipynb` | Un ejemplo completo de referencia (uso interno / modelo). |
| `compras_capstone.csv` | Dataset provisto: órdenes de compra reales de ChileCompra. |
| `README.md` | Esta portada + rúbrica. |

## Datos
Órdenes de compra de licitaciones de **ChileCompra / MercadoPúblico** (datos-abiertos.chilecompra.cl):
`codigo_oc`, `fecha`, `mes`, `organismo`, `region`, `rubro`, `proveedor`, `monto`. Es una **muestra
de licitaciones** (no incluye convenio marco ni trato directo): sirve para aprender, no para juzgar
a un organismo.

→ Al aprobarlo obtienes la **certificación de Alfabetización de datos públicos** (Capa A).

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Dirección ChileCompra (datos-abiertos.chilecompra.cl)
""" % REPO

open(os.path.join(BASE, "README.md"), "w", encoding="utf-8").write(README)
print("Capstone A generado en:", BASE)
print("Archivos:", sorted(os.listdir(BASE)))
