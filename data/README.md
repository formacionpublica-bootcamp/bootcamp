# Datos del curso

Todos los datos son **públicos y reales**: vienen de fuentes oficiales chilenas (y de USGS
para sismos). Se descargan y se curan con un solo script reproducible,
[`tools/make_datasets.py`](../tools/make_datasets.py) (semilla 42). Los notebooks los leen
de esta carpeta con el patrón «en vivo o caché»: usan la copia local o, en Colab, la bajan de
`raw.githubusercontent.com/formacionpublica-bootcamp/bootcamp/main/data/`.

[`MANIFEST.json`](MANIFEST.json) registra, para cada archivo, su fuente, licencia, número de
filas, columnas, huella `sha256` y fecha de generación. Si un número de una guía no calza,
compara primero el `sha256`.

## Anclas por rama (modelo 70/20/10)

Cada rama tiene **un dataset ancla** en sus lecciones, para que la atención vaya a la técnica
y no a entender datos nuevos. Cada `profundiza` usa **un dataset distinto** (transferencia), y
el capstone es **a elección**.

| Rama | Ancla | Archivo(s) |
|---|---|---|
| R1 · Análisis y Visualización | Matrícula escolar 2025 (MINEDUC) | `matricula.csv`, `matricula_rbd.csv`, `directorio_establecimientos.csv`, `matricula_sucia.csv` |
| R2 · Científico de Datos | Calidad del aire, PM2.5 + meteorología (SINCA) | `aire_diario.csv`, `estaciones.csv`, `aire_nuevos.csv` |
| R3 · IA Aplicada | Fichas de trámites (ChileAtiende) | `fichas.csv` |

## Catálogo

| Archivo | Filas | Qué es | Fuente | Período |
|---|---:|---|---|---|
| `matricula.csv` | 10.945 | Establecimientos con matrícula: dependencia, ruralidad, región, comuna, matrícula por nivel y sexo, cursos. Filtro oficial (funcionando y con matrícula > 0): calza con la cifra oficial. | [MINEDUC datos abiertos](https://datosabiertos.mineduc.cl/) | 2025 (último año publicado) |
| `matricula_rbd.csv` | 10.949 | Conteos por RBD **sin** filtro de estado (4 RBD huérfanos reales: sirven para enseñar *left join*). | MINEDUC | 2025 |
| `directorio_establecimientos.csv` | 10.945 | Directorio de establecimientos funcionando. | MINEDUC | 2025 |
| `matricula_sucia.csv` | 1.545 | Muestra de `matricula.csv` con errores típicos de planilla inyectados con semilla: espacios, sinónimos, `"2.425"` y `"s/i"` como texto, faltantes, duplicados, valores imposibles. | Derivado | 2025 |
| `aire_diario.csv` | 30.674 | PM2.5 diario (µg/m³) + temperatura y humedad agregadas del dato horario, 14 estaciones en 8 regiones. Meteorología solo en 7 de 14 estaciones: los faltantes son reales. | [SINCA · MMA](https://sinca.mma.gob.cl/) | 2020-01-01 → 2025-12-30 |
| `aire_nuevos.csv` | 3.808 | Mismas estaciones y columnas, **datos que ningún modelo del curso vio** (despliegue y monitoreo en R2-09). | SINCA · MMA | 2026-01-01 → 2026-09-29 |
| `estaciones.csv` | 14 | Comuna, región y coordenadas de cada estación (mapa oficial SINCA). | SINCA · MMA | — |
| `fichas.csv` | 245 | Fichas de trámites con texto completo (secciones `## `), 18 temas, 64 instituciones. | [ChileAtiende](https://www.chileatiende.gob.cl/) | descargadas ago-2026 |
| `reclamos.csv` | 20.000 | Muestra de reclamos (solo categorías: mercado, motivo, resultado). **Dato histórico**: SERNAC no publica una base abierta más reciente. | [datos.gob.cl](https://datos.gob.cl/) | 2011 |
| `sismos.csv` | 1.601 | Sismos de magnitud ≥ 4,5 en Chile, con zona (norte, centro, sur, austral). | [USGS FDSN](https://earthquake.usgs.gov/fdsnws/event/1/) | 2020 → 2025 |
| `comunas.csv` | 30 | Población censada de 30 comunas. | INE · Censo de Población y Vivienda | 2024 |
| `parques.csv` | 24 | Parques nacionales: región, año de creación, superficie. | CONAF · SNASPE | — |
| `establecimientos.csv` | 38 | Sedes del Servicio Médico Legal con coordenadas. | Servicio Médico Legal | — |

## Mantener los datos al día

```bash
# Requiere: pip install -r requirements-datos.txt  y  `unar` (brew install unar)
python tools/make_datasets.py todo        # descarga, cura, escribe MANIFEST.json y publica en data/
python tools/check_fuentes.py             # ¿siguen vivas las fuentes? ¿hay un año nuevo de MINEDUC?
python tools/run_notebooks.py             # todos los chequeos deben quedar en ✅
```

- El workflow mensual **Revisar fuentes de datos** avisa cuando una fuente se cae o cuando
  MINEDUC publica un año nuevo (suele pasar hacia fines de año).
- Al cambiar de año, también cambian las cifras que citan las guías (`GUIA_APRENDIZAJE.md`):
  re-ejecuta los builders, verifica y actualiza las cifras.
- Los archivos crudos descargados quedan en `data/rearmado/raw/`, que **no** se versiona.

## Lo que este curso NO usa

Este curso no usa datos de compras públicas (Mercado Público / ChileCompra). Se retiraron en
2026 por conflicto de interés del autor.
