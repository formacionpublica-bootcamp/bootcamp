# Glosario

Términos del bootcamp explicados en simple. Vuelve aquí cuando una palabra te suene a chino.

## Python y programación

- **Variable** — una "caja con etiqueta" donde guardas un valor (`gasto = 1000`).
- **Tipo de dato** — qué clase de valor es: `int` (entero), `float` (decimal), `str` (texto), `bool` (verdadero/falso).
- **Operador** — símbolo de cálculo o comparación: `+ - * /`, `>`, `<`, `==` (¿son iguales?).
- **Condicional (`if`/`elif`/`else`)** — el programa toma una decisión según se cumpla una regla.
- **Indentación** — los espacios al inicio de una línea que indican qué código va "dentro" de un `if`, `for` o función.
- **Lista** — una colección ordenada de valores: `[100, 200, 300]`.
- **Diccionario** — datos con etiqueta: `{"organismo": "MINSAL", "monto": 1000}`.
- **Bucle (`for`)** — repetir una acción para cada elemento de una colección.
- **Función (`def`)** — un "trámite" con nombre que recibe datos (parámetros) y **devuelve** (`return`) un resultado.
- **`print` vs `return`** — `print` solo muestra en pantalla; `return` entrega el valor al programa para seguir usándolo.
- **Método** — una herramienta pegada a un dato, se usa con punto: `"texto".strip()`.
- **f-string** — plantilla de texto con variables dentro: `f"Gasto: {monto}"`.
- **Error / traceback** — el mensaje (a veces rojo) que explica qué falló; la última línea es la pista clave.

## Datos y análisis

- **CSV** — un archivo de tabla en texto plano (valores separados por comas).
- **pandas** — la librería estándar para trabajar tablas en Python.
- **DataFrame** — una tabla en pandas (filas y columnas), como una planilla Excel en memoria.
- **Series** — una sola columna de un DataFrame.
- **Filtrar** — quedarse con las filas que cumplen una condición.
- **`groupby`** — agrupar por categoría y resumir (sumar, promediar): la "tabla dinámica".
- **`merge` / JOIN** — cruzar dos tablas por una columna común (la "llave"); el BUSCARV de Excel.
- **Llave** — la columna que comparten dos tablas y permite cruzarlas.
- **Valor nulo (`NaN`)** — un dato que falta en una celda.
- **SQL** — lenguaje para consultar bases de datos (`SELECT ... FROM ... WHERE`).

## Estadística

- **Media (promedio)** — la suma dividida por la cantidad; se deja "arrastrar" por valores extremos.
- **Mediana** — el valor del medio; describe mejor "lo típico" cuando hay datos sesgados.
- **Dispersión** — cuánto varían los datos (rango, desviación estándar).
- **Percentil** — el valor bajo el cual cae un % de los datos (el percentil 50 es la mediana).
- **Correlación** — cuánto se mueven juntas dos variables. **Correlación ≠ causalidad.**

## Machine Learning (Capa B)

- **Modelo** — un programa que aprende un patrón de ejemplos para predecir casos nuevos.
- **Feature (variable predictora)** — un dato de entrada que el modelo usa para predecir.
- **Objetivo (target)** — lo que el modelo intenta predecir.
- **Train/test** — separar datos para entrenar y otros, aparte, para evaluar con honestidad.
- **Sobreajuste (overfitting)** — el modelo "se aprende de memoria" el entrenamiento y falla con datos nuevos.
- **Regresión** — predecir un número (ej. un monto).
- **Clasificación** — predecir una categoría (ej. tamaño del proveedor).
- **Clustering** — descubrir grupos sin etiquetas previas (ej. K-Means).
- **Pipeline** — encadenar los pasos (limpieza + modelo) en un flujo reproducible.
- **Desplegar** — dejar un modelo usable por otras personas o sistemas.

## IA aplicada (Capa C)

- **LLM** — *Large Language Model*; un modelo que entiende y genera lenguaje (ej. Gemini).
- **Prompt** — la instrucción que le das a un LLM.
- **Alucinación** — cuando un LLM responde algo falso con total seguridad. Siempre verifica cifras.
- **RAG** — darle al LLM tus propios documentos para que responda **citando la fuente**, sin inventar.
- **Embedding** — convertir texto en números para poder buscar por significado.
- **Agente** — un asistente que **decide** qué herramienta usar, la ejecuta y responde.
- **API** — la "ventanilla" por la que un programa pide datos o servicios a otro.
- **JSON** — formato de datos con etiquetas, muy usado en APIs.

---
*CC BY 4.0 · Formación Pública*
