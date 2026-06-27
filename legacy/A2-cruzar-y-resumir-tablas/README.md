# M3B · Cruzar tablas: relacionar y resumir

Módulo puente del **tronco común (Pista A)** del **Bootcamp de Datos para Funcionarios Públicos — Formación Pública**.
Va entre **M3 (pandas)** y **M4 (limpieza)**. Modalidad autoguiada, se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A2-cruzar-y-resumir-tablas/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

## ¿Qué vas a aprender?
A **relacionar dos tablas** por una llave común con `pd.merge()` (el BUSCARV de Excel, pero para toda la tabla), a elegir el **tipo de cruce** correcto (`inner` vs `left`) y detectar las **filas huérfanas** que se pierden en silencio, y a **resumir** el resultado con `groupby` para responder una pregunta real de gestión.

**Competencia de salida:** cruzar dos tablas por su llave, elegir el cruce correcto, detectar filas perdidas y resumir el resultado para responder una pregunta de gestión pública.

## Datos
Caso conductor: **compras públicas reales (ChileCompra)** — órdenes de compra de licitaciones, en **dos tablas** relacionadas por `entcode`:

| Archivo | Qué es |
| --- | --- |
| `ordenes.csv` | Órdenes de compra: `codigo_oc`, `entcode`, `rubro`, `monto`. |
| `organismos.csv` | Catálogo de organismos: `entcode`, `organismo`, `region`. |

Son **órdenes de compra reales** del portal de datos abiertos de ChileCompra (datos-abiertos.chilecompra.cl). Se modelan como en una base real (las órdenes guardan solo el `entcode`; nombre y región viven en el catálogo) y **se omite a propósito un organismo del catálogo** para enseñar el cruce de la fila huérfana.

## Archivos
| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante: teoría + ejercicios + celdas de chequeo. |
| `solucion.ipynb` | Soluciones de referencia (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `ordenes.csv` | Tabla de órdenes de compra. |
| `organismos.csv` | Catálogo de organismos. |
| `README.md` | Esta portada. |

## Los 4 ejercicios
1. **Encontrar la llave** — identificar la columna común a ambas tablas.
2. **El primer cruce** — `pd.merge(..., on="entcode")` (inner por defecto).
3. **Inner vs left** — conservar todas las órdenes con `how="left"` y cazar la fila huérfana.
4. **La pregunta real** — `merge` + `groupby` para el gasto por región e interpretarlo.

## 🔬 Profundización (opcional)
¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: los **cuatro tipos de cruce** (`inner` / `left` / `right` / `outer`) vistos como
**teoría de conjuntos**; la **cardinalidad** de una relación (**uno-a-muchos** vs **muchos-a-muchos**);
la **explosión** de filas cuando la llave está **duplicada** —que infla el gasto en silencio— y cómo
**blindarse** con `validate=`; el modelo **dividir-aplicar-combinar** (*split-apply-combine*) detrás de
`groupby`; y la diferencia entre **agregar** (un valor por grupo) y **transformar** (un valor por fila).
Con 4 ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A2-cruzar-y-resumir-tablas/profundiza.ipynb)

## Verificación de calidad
- Solución ejecutada: **4/4 ✅** (cruce inner pierde la huérfana; left la conserva con region vacía; gasto por región calculado).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Dirección ChileCompra (datos-abiertos.chilecompra.cl)
