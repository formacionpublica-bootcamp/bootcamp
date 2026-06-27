# M5 · SQL fundamentos

Sexto módulo (tronco común) del **Bootcamp de Datos para Funcionarios Públicos — Formación Pública**.
Módulo compartido. Modalidad autoguiada, se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A4-sql-fundamentos/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

## ¿Qué vas a aprender?
A consultar una base de datos con SQL: `SELECT`/`FROM` (elegir columnas), `WHERE` (filtrar filas), `ORDER BY`/`LIMIT` (ordenar y rankear) y funciones de agregación (`COUNT`, `SUM`, `AVG`, `MAX`, `MIN`) con `GROUP BY` (resumir por grupo). Se usa **SQLite** mediante el módulo `sqlite3`, incluido en Python (cero instalación en Colab).

## Datos
Tema: **medio ambiente**. Listado real de **Parques Nacionales de Chile** (nombre, región, año de declaración, superficie en hectáreas). Fuente: Corporación Nacional Forestal (CONAF) — Sistema Nacional de Áreas Silvestres Protegidas del Estado (SNASPE). Son hechos públicos; se usan 24 parques con datos reales.

## Contenido
- `leccion.ipynb` — teoría + ejercicios + celdas de chequeo (para el estudiante).
- `solucion.ipynb` — soluciones de referencia (uso interno).
- `profundiza.ipynb` — **notebook opcional de profundización teórica** (ver abajo).
- `profundiza_solucion.ipynb` — solución del profundiza (uso interno).
- `README.md` — esta presentación.

## Cómo se cursa
1. Abre `leccion.ipynb` con el botón **Open in Colab**.
2. Lee y ejecuta cada sección.
3. Resuelve los cinco ejercicios y ejecuta sus celdas de chequeo hasta ver ✅.

## 🔬 Profundización (opcional)
¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo en teoría: pensar por **conjuntos** vs. fila a fila (el modelo relacional), el **orden lógico de
ejecución** (`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`) y por qué `WHERE` filtra filas pero
`HAVING` filtra grupos, la **lógica de tres valores del `NULL`** (la trampa clásica de `WHERE x != valor`),
y por qué existen los **índices** (consultas instantáneas vs. eternas). Con 4 ejercicios conceptuales
auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/A4-sql-fundamentos/profundiza.ipynb)

## Licencia
Contenido bajo **CC BY 4.0**.
