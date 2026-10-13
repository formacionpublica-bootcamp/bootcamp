# R1-05 · SQL para análisis

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/ramas/R1-analisis-visualizacion/R1-05-sql-para-analisis/leccion.ipynb)

Consultar una base de datos con **SQL** desde Python (SQLite en memoria, `sqlite3` +
`pandas.to_sql` / `read_sql_query`): `SELECT`/`WHERE`, `ORDER BY`/`LIMIT`, `GROUP BY`/`HAVING`,
`JOIN` y `LEFT JOIN ... IS NULL` para auditar, y SQL + pandas para interpretar promedio vs mediana.

**Datos.** La matrícula 2025 (MINEDUC) en dos tablas relacionales: `matricula_rbd.csv` (10.949
conteos por RBD) y `directorio_establecimientos.csv` (10.945 establecimientos oficiales, con
dependencia, ruralidad, región y comuna) — con 4 RBD huérfanos reales. La profundización usa
`parques.csv`: 24 parques nacionales de Chile (CONAF / SNASPE).

- `leccion.ipynb` — completa los `TODO`; cada ejercicio se autoverifica (✅).
- `profundiza.ipynb` — opcional 🔬: `LIKE`, subconsultas, `CASE WHEN`, `WHERE` + `HAVING` sobre parques nacionales.
- [`GUIA_APRENDIZAJE.md`](GUIA_APRENDIZAJE.md) — pistas progresivas, errores frecuentes y autoevaluación.
