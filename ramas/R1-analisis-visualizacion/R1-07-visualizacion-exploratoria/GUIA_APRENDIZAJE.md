# 📊 Guía de Aprendizaje · R1-07 · Visualización Exploratoria — Ver para Entender

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Semana 8 · Google Colab

| Dato | Detalle |
|------|---------|
| 🎯 Competencia de salida | Usar gráficos para descubrir patrones en datos públicos |
| ⏱️ Duración estimada | 90 minutos |
| 📊 Dataset real | `compras_ml.csv` — compras públicas de ChileCompra |
| ✅ Entregable | 4 celdas de chequeo con ✅ |
| 🔗 Prerrequisito | R1-06 · Estadística descriptiva |
| 🔜 Siguiente | R1-08 · Visualización: comunicar y ética |

---

## ¿Para qué me sirve esto como funcionario público?

En el Estado se trabaja con datos constantemente: montos de compras, cantidades, proveedores, regiones. El problema es que **una tabla de 10.000 filas no le dice nada a nadie**. Un buen gráfico, en cambio, revela en segundos si el gasto está concentrado, si hay valores atípicos, o si dos variables se relacionan.

Este módulo te enseña a usar gráficos como **herramienta de descubrimiento personal** — no para presentar (eso viene en R1-08), sino para entender los datos tú primero antes de sacar conclusiones.

> 💡 **La diferencia clave:** R1-07 es el gráfico que te haces a ti mismo para entender. R1-08 es el gráfico que le muestras a tu jefatura o directorio.

---

## 🗺️ Mapa Conceptual del Módulo

| Gráfico | Pregunta que responde | Analogía sector público | Función matplotlib |
|---------|----------------------|------------------------|-------------------|
| **Histograma** | ¿Cómo se distribuyen los montos? | Ver cuántas compras caen en cada rango de precio | `ax.hist()` |
| **Boxplot** | ¿Difiere el comportamiento entre grupos? | Comparar gasto de proveedores micro vs. grande | `ax.boxplot()` |
| **Dispersión** | ¿Más cantidad implica más monto? | ¿Los pedidos grandes cuestan proporcionalmente más? | `ax.scatter()` |
| **Barras horizontales** | ¿Qué región concentra más gasto? | Ranking de regiones por gasto total ChileCompra | `ax.barh()` |

---

## ✅ Antes de empezar: Verificación de Prerrequisitos

Deberías poder responder **sí** a todo esto antes de continuar:

- [ ] ¿Puedo calcular media, mediana y desviación estándar con pandas?
- [ ] ¿Sé qué es un percentil y para qué sirve (`.quantile()`)?
- [ ] ¿Puedo usar `groupby()` para resumir por categoría?
- [ ] ¿Sé importar `matplotlib.pyplot as plt` y crear una figura con `plt.subplots()`?
- [ ] ¿Entiendo qué es `fig` y qué es `ax` en matplotlib?

Si alguna respuesta es "no", repasa rápidamente R1-06 antes de continuar.

---

## 📖 Guía Sección por Sección

### Sección 0 · Preparación del entorno (celda inicial)

🎯 **Objetivo:** cargar los datos de compras públicas en memoria.

💡 **Concepto clave:** el notebook descarga automáticamente `compras_ml.csv` desde el repositorio si no lo encuentra localmente. Así funciona igual en tu máquina que en Colab.

🔍 **Qué hace el código:**
```python
import os, urllib.request
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

CSV = "compras_ml.csv"
if not os.path.exists(CSV):
    urllib.request.urlretrieve("https://...compras_ml.csv", CSV)

df = pd.read_csv(CSV)
print("Datos cargados:", df.shape, "filas x columnas")
df.head()
```
- `os.path.exists(CSV)` — pregunta: ¿ya existe el archivo?
- Si no existe, lo baja desde GitHub con `urlretrieve`
- `df.head()` — muestra las primeras 5 filas para confirmar que todo cargó bien

⚠️ **Error frecuente:** ejecutar las celdas de ejercicio antes de ejecutar esta celda de preparación. Resultado: `NameError: name 'df' is not defined`.

✅ **Señal de que entendiste:** puedes ver el shape del DataFrame y las columnas `monto_total`, `cantidad`, `region_comprador`, `tamano_proveedor`.

---

### Sección 1 · Histograma: la forma de una variable

🎯 **Objetivo:** dibujar la distribución del monto de compras usando un histograma.

💡 **Concepto clave:** los datos de compras públicas tienen **cola larga** — la mayoría de las órdenes son pequeñas, pero unas pocas son gigantes. Si graficas todo sin filtrar, las barras pequeñas se aplanan y no ves nada. Por eso se "recorta" al percentil 99 (`.clip(upper=...quantile(0.99))`). Es como decir: "ignoremos el 1% más extremo para ver mejor el resto".

🔍 **Qué hace el código línea por línea:**
```python
montos = df["monto_total"].clip(upper=df["monto_total"].quantile(0.99))
# → Recorta los valores mayores al p99. No los elimina, los "topa".

fig, ax = plt.subplots(figsize=(6, 4))
# → Crea una figura de 6x4 pulgadas. fig = el lienzo, ax = el área de dibujo.

# TODO: ax.hist(montos, bins=40)
# → Divide los montos en 40 rangos y dibuja una barra por rango.

ax.set_xlabel("Monto (recortado al p99)"); ax.set_ylabel("Frecuencia")
ax.set_title("Distribución del monto")
plt.show()
```

⚠️ **Error frecuente:** usar `plt.hist()` en lugar de `ax.hist()`. Ambos funcionan, pero la celda de chequeo verifica `ax.patches` (las barras del `ax`). Usa siempre el objeto `ax`.

✅ **Señal de que entendiste:** ves un gráfico donde la mayoría de las compras se concentran en montos bajos (sesgo a la derecha). La celda muestra ✅.

---

### Sección 2 · Boxplot: comparar grupos

🎯 **Objetivo:** comparar la distribución del monto entre proveedores Micro, Pequeña, Mediana y Grande.

💡 **Concepto clave:** un boxplot es como un resumen de 5 números dibujado. La **caja** muestra el rango intercuartil (Q1 a Q3, el 50% central de los datos), la **línea del medio** es la mediana, y los **bigotes** llegan hasta los valores extremos razonables. Los puntos sueltos son **outliers**.

Analogía: imagina que tienes 4 grupos de funcionarios con distintos sueldos. El boxplot te dice de un vistazo si los sueldos de cada grupo son similares o muy dispersos, y dónde está el "típico" de cada uno.

🔍 **Qué hace el código:**
```python
orden = ["Micro", "Pequeña", "Mediana", "Grande"]
tope = df["monto_total"].quantile(0.99)
grupos = [df[df["tamano_proveedor"] == t]["monto_total"].clip(upper=tope) for t in orden]
# → Crea una lista de 4 series, una por tamaño de proveedor, todas recortadas al p99.

fig, ax = plt.subplots(figsize=(6, 4))
# TODO: ax.boxplot(grupos, labels=orden)
```
- La **list comprehension** filtra el DataFrame para cada categoría en un solo paso
- `labels=orden` pone los nombres debajo de cada caja en el gráfico

⚠️ **Error frecuente:** pasar `df["tamano_proveedor"]` directamente en vez de la lista `grupos`. `ax.boxplot()` necesita una lista de arrays, no una columna de texto.

✅ **Señal de que entendiste:** ves 4 cajas. Los proveedores grandes tienen cajas más altas (montos mayores) y más dispersión. La celda muestra ✅.

---

### Sección 3 · Dispersión: ¿se relacionan dos variables?

🎯 **Objetivo:** visualizar si existe relación entre la cantidad comprada y el monto total.

💡 **Concepto clave:** el gráfico de dispersión (scatter) dibuja un punto por cada orden de compra, usando cantidad en X y monto en Y. Si los puntos forman una nube diagonal ascendente, hay correlación positiva. Si la nube es horizontal, no hay relación.

Analogía: es como el informe de auditoría donde preguntas "¿Los contratos con más ítems cuestan proporcionalmente más, o hay alguno que con pocas unidades tiene un monto desproporcionado?"

🔍 **Qué hace el código:**
```python
m = df.sample(800, random_state=42)
# → Toma 800 filas al azar (muestra). Graficar 10.000 puntos superpondría todo.
# random_state=42 asegura que siempre salga la misma muestra (reproducibilidad).

fig, ax = plt.subplots(figsize=(6, 4))
# TODO: ax.scatter(m["cantidad"], m["monto_total"])
```

⚠️ **Error frecuente:** usar `plt.scatter()` en lugar de `ax.scatter()`. La celda de chequeo verifica `ax.collections` (los puntos del scatter en el `ax`). Siempre usa el objeto `ax`.

✅ **Señal de que entendiste:** ves una nube de puntos. Puedes notar que hay valores atípicos (puntos muy alejados). La celda muestra ✅.

---

### Sección 4 · Barras horizontales: comparar categorías

🎯 **Objetivo:** identificar qué región concentra más gasto total en compras públicas.

💡 **Concepto clave:** las barras horizontales (barh) son ideales cuando las etiquetas del eje son texto largo (nombres de regiones). Son más fáciles de leer que las barras verticales para ese caso.

Analogía: es el gráfico que usarías en un informe de ChileCompra para decirle al director: "Mire, la Región Metropolitana concentra X% del gasto total. Las regiones de Maule y La Araucanía están en los últimos lugares."

🔍 **Qué hace el código:**
```python
g = df.groupby("region_comprador")["monto_total"].sum().sort_values()
# → Agrupa por región, suma el monto total de cada una, y ordena de menor a mayor.
# El .sort_values() hace que la región con más gasto quede arriba en el gráfico.

fig, ax = plt.subplots(figsize=(6, 5))
# TODO: ax.barh(g.index, g.values)
# g.index = nombres de las regiones (el eje Y)
# g.values = montos totales (el largo de cada barra)
```

⚠️ **Error frecuente:** usar `ax.bar()` en lugar de `ax.barh()`. La celda de chequeo no fallará por esto, pero el gráfico quedará con las regiones en el eje X y serán ilegibles.

✅ **Señal de que entendiste:** ves un ranking de regiones con las barras ordenadas. Puedes responder: ¿qué región tiene mayor gasto? ¿Cuánto más gasta que la que tiene menos? La celda muestra ✅.

---

## 🎯 Guía de los 4 Ejercicios

### Ejercicio 1 · Histograma del monto

**Habilidad que entrena:** dibujar una distribución numérica con `ax.hist()`.

| Nivel | Pista |
|-------|-------|
| 🟢 Suave | El método del objeto `ax` que dibuja histogramas se llama `hist`. Recibe la serie de datos como primer argumento. |
| 🟡 Media | `ax.hist(datos, bins=N)` — `datos` ya está preparado en la variable `montos`. `N` es el número de barras que quieres. |
| 🔴 Directa | `ax.hist(montos, bins=40)` — completa el `TODO` con exactamente eso. |

**Lógica de la solución:** `montos` ya tiene los valores recortados al p99. Solo necesitas pasarlos a `ax.hist()` con `bins=40` para que matplotlib divida el rango en 40 intervalos iguales y cuente cuántas compras caen en cada uno.

---

### Ejercicio 2 · Boxplot por tamaño de proveedor

**Habilidad que entrena:** comparar distribuciones entre grupos con `ax.boxplot()`.

| Nivel | Pista |
|-------|-------|
| 🟢 Suave | `ax.boxplot()` recibe una **lista de arrays**, no una columna del DataFrame. Esa lista ya está en `grupos`. |
| 🟡 Media | También necesitas el parámetro `labels=` para que cada caja tenga su etiqueta. Los labels están en la variable `orden`. |
| 🔴 Directa | `ax.boxplot(grupos, labels=orden)` |

**Lógica de la solución:** `grupos` es una lista de 4 Series (una por tamaño). `labels=orden` les pone nombre. Matplotlib dibuja una caja por cada elemento de la lista, alineada con su etiqueta.

---

### Ejercicio 3 · Dispersión cantidad vs. monto

**Habilidad que entrena:** visualizar relaciones entre dos variables numéricas con `ax.scatter()`.

| Nivel | Pista |
|-------|-------|
| 🟢 Suave | El método para scatter en matplotlib se llama `scatter`. Recibe dos arrays: uno para X y otro para Y. |
| 🟡 Media | `ax.scatter(eje_x, eje_y)` — los datos están en `m["cantidad"]` y `m["monto_total"]`. |
| 🔴 Directa | `ax.scatter(m["cantidad"], m["monto_total"])` |

**Lógica de la solución:** `m` es una muestra de 800 filas para no sobrecargar el gráfico. Cada punto representa una orden de compra: su posición horizontal es la cantidad pedida, su posición vertical es el monto pagado.

---

### Ejercicio 4 · Barras horizontales por región

**Habilidad que entrena:** construir un ranking categórico con `ax.barh()`.

| Nivel | Pista |
|-------|-------|
| 🟢 Suave | Las barras horizontales en matplotlib usan `barh` (de *bar horizontal*). |
| 🟡 Media | `ax.barh(etiquetas, valores)` — las etiquetas son los nombres de las regiones (`g.index`) y los valores son los montos (`g.values`). |
| 🔴 Directa | `ax.barh(g.index, g.values)` |

**Lógica de la solución:** `g` ya viene ordenado de menor a mayor gracias al `.sort_values()`. Al pasar `g.index` como eje Y y `g.values` como longitud de las barras, el gráfico queda automáticamente ordenado de abajo (menor) a arriba (mayor).

---

## 🔬 Conexión con `profundiza.ipynb`

| Aspecto | `leccion.ipynb` (este módulo) | `profundiza.ipynb` (opcional) |
|---------|-------------------------------|-------------------------------|
| Nivel | Práctico, funcional | Teórico + avanzado |
| Histograma | Básico con bins | Escala logarítmica para colas largas |
| Boxplot | Visual directo | Detección formal de outliers con IQR |
| Gráficos múltiples | Uno por sección | Pequeños múltiplos (subplots comparativos) |
| ¿Para quién? | Todos los participantes | Quienes quieran profundidad estadística |

> **¿Cuándo ir al profundiza?** Cuando termines los 4 ejercicios y quieras entender *por qué* se recorta al p99, *cómo* se detectan outliers matemáticamente, o *cómo* comparar varias variables a la vez en una sola figura.

---

## 🧠 Autoevaluación Final

**1.** Tienes una columna con montos que va de $1.000 a $500.000.000. Quieres ver cómo se distribuye la mayoría, ignorando los valores extremos. ¿Qué harías?
- a) Un boxplot directamente
- b) Un histograma de todos los datos
- **c) Recortar al percentil 99 con `.clip()` y luego hacer el histograma** ✅
- d) Ordenar de mayor a menor con `.sort_values()`

> *El clip permite enfocarse en el comportamiento típico sin que los extremos distorsionen la visualización.*

**2.** ¿Qué gráfico usarías para responder: "¿Los proveedores grandes tienen montos más altos que los micro?"
- a) Histograma
- **b) Boxplot** ✅
- c) Dispersión
- d) Barras

> *El boxplot está diseñado para comparar distribuciones entre grupos.*

**3.** En un gráfico de dispersión con `cantidad` en X y `monto_total` en Y, ¿qué indica una nube de puntos totalmente horizontal?
- a) Correlación positiva fuerte
- b) Correlación negativa
- **c) No hay relación entre las dos variables** ✅
- d) Error en los datos

> *Si los puntos no suben al aumentar X, las dos variables no están relacionadas.*

**4.** ¿Por qué en el Ejercicio 4 se usa `ax.barh()` en lugar de `ax.bar()`?
- a) Porque los montos son muy grandes
- **b) Porque los nombres de regiones son largos y se leen mejor en el eje Y** ✅
- c) Porque es obligatorio para datos de ChileCompra
- d) Porque `ax.bar()` no acepta strings

> *Las barras horizontales son preferibles cuando las etiquetas del eje son texto extenso.*

**5.** ¿Cuál es la diferencia principal entre R1-07 y R1-08?
- a) En R1-07 se usa matplotlib y en R1-08 se usa seaborn
- b) R1-07 es para números y R1-08 para categorías
- **c) R1-07 es para descubrir patrones (para ti); R1-08 es para comunicar hallazgos (para otros)** ✅
- d) No hay diferencia, son lo mismo

> *La visualización exploratoria y la comunicativa tienen propósitos distintos: una es personal, la otra es pública.*

---

## 📚 Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Histograma** | Gráfico que muestra cuántos datos caen en cada rango | Distribución de montos de contratos por tramo |
| **Bins** | Los rangos (intervalos) del histograma | "¿Cuántos contratos entre $1M y $5M?" |
| **Boxplot** | Resumen visual de 5 números para comparar grupos | Comparar sueldos entre distintos estamentos |
| **Percentil p99** | El valor bajo el cual cae el 99% de los datos | El contrato más caro que no sea una excepción extrema |
| **Clip** | Recortar valores extremos a un tope | Topar montos para analizar sin distorsión |
| **Dispersión (scatter)** | Gráfico que muestra la relación entre dos números | ¿Más ítems = más costo en una licitación? |
| **Correlación** | Qué tan relacionadas están dos variables | Si el N° de funcionarios sube, ¿sube el presupuesto? |
| **Barras horizontales (barh)** | Barras que van de izquierda a derecha | Ranking de regiones por gasto |
| **Outlier** | Dato muy alejado del resto | Contrato con monto 100× el promedio |
| **`ax`** | El área de dibujo dentro de una figura matplotlib | La "hoja" donde dibujas el gráfico |
| **`fig`** | El marco completo que contiene uno o más `ax` | El "marco" que envuelve la hoja |
| **Muestra (`sample`)** | Subconjunto aleatorio de los datos | Auditar 100 contratos de 10.000 para un análisis rápido |

---

## 🔜 Conexión con R1-08 · Visualización: Comunicar y Ética

En R1-07 aprendiste a **ver para entender**: gráficos rápidos, sin formato, para descubrir patrones tú mismo. En R1-08 darás el siguiente paso: **ver para mostrar**.

Aprenderás a:
- Elegir el gráfico correcto según el mensaje que quieres transmitir
- Agregar títulos, etiquetas y anotaciones que expliquen sin necesidad de texto
- Evitar gráficos que distorsionan la realidad (manipulación visual)
- Adaptar visualizaciones para informes a autoridades o ciudadanía

> 💬 **Pregunta motivadora para R1-08:** Con el gráfico de gasto por región que hiciste hoy, ¿cómo lo presentarías en una reunión de directivos para que el mensaje llegue en menos de 10 segundos?
