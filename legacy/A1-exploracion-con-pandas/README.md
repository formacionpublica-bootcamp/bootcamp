# M3 · Exploración con pandas

Cuarto módulo (primero del tronco común) del **Bootcamp de Datos para Funcionarios Públicos — Formación Pública**.
Módulo compartido. Modalidad autoguiada, se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A1-exploracion-con-pandas/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

## ¿Qué vas a aprender?
A dar el salto del prework a pandas: cargar un dataset desde un archivo, inspeccionarlo (`head`, `shape`, `columns`, `info`), seleccionar columnas, filtrar filas, contar por categoría (`value_counts`) y calcular estadísticos básicos (`mean`, `describe`).

**Dataset:** Muestra real de la base de datos de *Establecimientos de Salud Vigentes* de Chile (`establecimientos.csv`), enfocada en las sedes del Servicio Médico Legal (SML), el cual viene pre-construido de forma fija en la carpeta del módulo.

**Competencia de salida:** cargar un dataset con pandas, inspeccionarlo y obtener un primer resumen exploratorio.

## Cómo empezar
1. Abre `leccion.ipynb` con **Open in Colab**.
2. El cuaderno cargará automáticamente el archivo `establecimientos.csv` (cuenta con descargador automático en caso de ejecutarse en Google Colab).
3. Completa los `# TODO` y corre la celda de chequeo para obtener tu ✅ o pista.
4. Terminas cuando las cinco celdas de chequeo muestran ✅.

## Archivos
| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante. |
| `solucion.ipynb` | Soluciones de referencia (uso interno). |
| `establecimientos.csv` | Dataset de establecimientos de salud (SML) para la práctica. |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `README.md` | Esta portada. |

## Contenido
- Qué es pandas y el DataFrame; `pd.read_csv`.
- Inspección: `head`, `shape`, `columns`, `info`.
- Seleccionar columnas (ocultar/mostrar) y filtrar filas (el embudo de filtros).
- Contar por categoría con la tabla dinámica rápida `value_counts`.
- Estadísticos rápidos: `mean`, `min`, `max`, `describe`.
- Errores típicos.
- 5 ejercicios auto-corregidos.

## 🔬 Profundización (opcional)
¿Quieres entender el *porqué* y no solo el *cómo* de pandas? El notebook **`profundiza.ipynb`** va un
nivel más hondo en teoría: **qué es un DataFrame por dentro** (Series, índice y columnas), la
**vectorización** (por qué pandas vuela sin bucles `for`), **`.loc` vs `.iloc`** (etiqueta vs posición),
las **máscaras booleanas** por debajo del filtrado, **vistas vs. copias** y el `SettingWithCopyWarning`,
los **tipos de dato (`dtype`) y la memoria**, y la **semántica del valor faltante (`NaN`)**. Con 4
ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A1-exploracion-con-pandas/profundiza.ipynb)

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** Ministerio de Salud (MINSAL) en datos.gob.cl
