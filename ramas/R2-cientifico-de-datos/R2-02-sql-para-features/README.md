# D8 · SQL para *features*

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Línea B · *Data Scientist* · Semana 9 · Módulo específico de la ruta de Ciencia de Datos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B1-sql-para-features/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace de arriba por la ruta real del repositorio al publicar.

---

## De qué trata

En el tronco común aprendiste a **consultar** datos con SQL (M5). Este módulo da el giro propio de la ciencia de datos: usar SQL para **fabricar variables nuevas** —*features*— que después alimentarán un modelo. Es el primer módulo de la Línea B y construye directamente sobre el SQL del tronco.

**Competencia de salida:** a partir de una tabla de sismos en bruto, construir con SQL una **tabla analítica** (una fila por entidad, varias columnas de *features*) lista para un modelo, usando agregaciones, lógica condicional y una *feature* temporal de rezago, y entendiendo qué es la *fuga de información* (*data leakage*).

## Dato real y Fuente

Trabajamos con los **15 últimos sismos** publicados por el **Centro Sismológico Nacional (CSN)** de la Universidad de Chile, capturados el **2026-06-18**. Cada fila es un sismo (fecha/hora, lugar, región, profundidad y magnitud).

**Dataset:** El archivo `sismos.csv` ya viene guardado estáticamente en la carpeta del módulo. El notebook lo cargará automáticamente (cuenta con un descargador de respaldo para Google Colab).

> Es el primer módulo que abre el bootcamp a un dominio distinto a las compras públicas. En la Línea B esto es deliberado: un *data scientist* debe manejar datos de cualquier tipo.

## Cómo empezar

1. Abre `leccion.ipynb` con el botón **Open in Colab** (solo necesitas una cuenta de Google).
2. Ejecuta las celdas en orden y completa cada `TODO`.
3. Cada ejercicio termina en una **celda de chequeo** que muestra ✅ si está correcto o una pista si todavía no. El módulo está logrado cuando las 4 dan ✅.

## Archivos

| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante. |
| `solucion.ipynb` | Soluciones de referencia (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `sismos.csv` | Dataset de sismos del CSN. |
| `README.md` | Esta portada. |

## Los 4 ejercicios

1. **Resumen sísmico por región** — *features* de agregación con `GROUP BY` (`COUNT`, `AVG`, `MAX`).
2. **Clasificar cada sismo por profundidad** — *feature* condicional con `CASE WHEN`.
3. **La magnitud del sismo anterior** — *feature* temporal de rezago con la función de ventana `LAG`, más el concepto de *data leakage*.
4. **Tu primera tabla analítica** — reunir las *features* en una fila por región, lista para entrenar un modelo en D9.

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: **qué hace a una buena *feature***, la **fuga de datos** (*leakage*) **temporal y de
objetivo**, la **corrección punto-en-el-tiempo** (usar solo lo conocido antes del evento) y la
**granularidad** del **tablón analítico** (una fila por entidad). Con 4 ejercicios conceptuales
auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B1-sql-para-features/profundiza.ipynb)

---

*Fuente de datos: Centro Sismológico Nacional (CSN), Universidad de Chile — [sismologia.cl](https://www.sismologia.cl/).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
