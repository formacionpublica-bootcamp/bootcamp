# 📘 Guía de Aprendizaje — R2-00 · Fundamentos express: Python + pandas

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-00 · Fundamentos express: Python + pandas |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 2–3 horas (Semana 1–2) |
| **Nivel** | Inicial (cero conocimientos de Python) |
| **Prerrequisitos** | Ninguno. Solo necesitas una cuenta Google para usar Colab. |
| **Competencia de salida** | Manipular un DataFrame de datos públicos desde cero: cargar, inspeccionar, filtrar, seleccionar, ordenar y agregar con `groupby`. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de ChileCompra (monto, categoría, región, tamaño de proveedor). |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Imagina que tu jefatura te pide un informe urgente: *"¿Cuánto gastamos en tecnología por región el año pasado?"* Hasta ahora, eso significaba abrir un Excel enorme, filtrar a mano, copiar columnas y rezar para que no hubiera errores de fórmula.

Con Python y pandas puedes hacer exactamente lo mismo —y mucho más— en 5 líneas de código. En lugar de filtrar arrastrando el cursor, escribes una instrucción clara que puedes volver a ejecutar mañana con datos nuevos, sin tocar nada.

Este módulo usa el dataset real de **compras públicas de ChileCompra**: miles de órdenes de compra con monto, categoría, región y tamaño del proveedor. Cada ejercicio responde una pregunta que cualquier analista del Estado podría tener hoy: ¿cuántas compras se hicieron a grandes empresas?, ¿qué categoría tiene el mayor gasto promedio?, ¿cuáles son las 10 compras más altas?

> 💡 **La clave:** aprendes Python no como ejercicio abstracto, sino resolviendo preguntas reales sobre gasto público.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público |
|---|---|---|
| `DataFrame` | Tabla de datos en memoria (filas × columnas) | Una planilla Excel abierta en Python |
| `pd.read_csv()` | Carga un archivo .csv como DataFrame | Abrir un archivo descargado de ChileCompra |
| `df.shape` | Devuelve (N° filas, N° columnas) | Ver cuántas filas tiene tu registro |
| `df.columns` | Lista los nombres de columnas | Ver los encabezados de tu tabla |
| `df.head()` | Muestra las primeras 5 filas | Echar un vistazo rápido al informe |
| Máscara booleana `df[condición]` | Filtra filas que cumplen una condición | Filtro de Excel: "Mostrar solo Grande" |
| `df[['col1','col2']]` | Selecciona solo ciertas columnas | Ocultar columnas irrelevantes en Excel |
| `df.sort_values()` | Ordena por una columna | Ordenar por monto de mayor a menor |
| `groupby().mean()` | Agrupa y calcula promedios por categoría | Tabla dinámica en Excel |

---

## 4. Verificación de Prerrequisitos

Antes de empezar, respóndete estas preguntas. No necesitas saber programar, pero sí tener claro el punto de partida:

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Abrir Google Colab (colab.research.google.com) con mi cuenta Google | ✅ | Si no tienes cuenta Google, créala primero |
| Entender qué es una tabla con filas y columnas | ✅ | Piensa en Excel: filas son registros, columnas son campos |
| Ejecutar una celda en Colab con ▶︎ o Shift+Enter | ✅ | Mira el tutorial de 2 min de Colab en YouTube |
| Identificar qué es un archivo .csv | ✅ | Es una planilla de datos separada por comas, como las de ChileCompra |
| Tolerar ver mensajes de error sin pánico | ✅ | Los errores son normales; este módulo te enseña a leerlos |

> 🟢 Si marcaste todo ✅, ¡adelante! Si alguno dice 🔄, dedica 10 minutos a resolverlo antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno (celda inicial)

**🎯 Objetivo:** Cargar las librerías necesarias y el dataset de compras.

**💡 Concepto clave:** `import` es como decirle a Python "trae esta caja de herramientas". `pandas` es la caja de herramientas para tablas; `matplotlib` es para gráficos. Es exactamente como instalar un complemento en Excel antes de usarlo.

**🔍 Qué hace el código:**
1. Revisa si el archivo `compras_ml.csv` ya está en la carpeta local.
2. Si no está (como en Colab), lo descarga automáticamente desde el repositorio.
3. Lo carga como DataFrame y muestra cuántas filas y columnas tiene.

**⚠️ Error frecuente:** Ejecutar celdas en orden distinto. Siempre ejecuta primero esta celda de setup. Si ves `NameError: name 'df' is not defined`, es porque saltaste esta celda.

**✅ Señal de comprensión:** Ves el mensaje `Datos cargados: (XXXX, N) filas x columnas` y la tabla aparece abajo.

---

### 🔷 Sección 1 — Cargar e inspeccionar un DataFrame

**🎯 Objetivo:** Conocer la forma y los nombres de columnas del dataset antes de manipularlo.

**💡 Concepto clave:** Antes de analizar cualquier tabla, necesitas saber qué tiene. En Excel harías Ctrl+Fin para ver el tamaño. En pandas usas `df.shape` (tamaño) y `df.columns` (nombres). Es el equivalente a leer el encabezado del informe antes de analizarlo.

**🔍 Qué hace el código:**
- `df.shape` devuelve una tupla `(n_filas, n_columnas)` que puedes "desempaquetar" con `n_filas, n_cols = df.shape`.
- `list(df.columns)` convierte el índice de columnas en una lista de nombres legibles.

**⚠️ Error frecuente:** Escribir `df.shape()` con paréntesis. `shape` es un atributo, no una función. Escríbelo sin paréntesis.

**✅ Señal de comprensión:** Puedes decir de memoria cuántas filas tiene el dataset y nombrar al menos 3 columnas que existen.

---

### 🔷 Sección 2 — Filtrar filas con una condición

**🎯 Objetivo:** Quedarte solo con las compras realizadas a proveedores clasificados como "Grande".

**💡 Concepto clave:** Una **máscara booleana** es como un filtro de Excel, pero escrito en código. Le preguntas a cada fila: *¿esta condición es verdadera?* Y pandas devuelve solo las que dicen "Sí". Imagina marcar con color en una planilla solo las filas de una región específica.

**🔍 Qué hace el código:**
- `df["tamano_proveedor"] == "Grande"` crea una serie de True/False para cada fila.
- `df[esa_mascara]` devuelve solo las filas donde el resultado fue True.

**⚠️ Error frecuente:** Usar `=` en vez de `==`. En Python, `=` asigna variables; `==` compara valores. También asegúrate que el texto sea exacto: "Grande" con G mayúscula.

**✅ Señal de comprensión:** El número de filas de `grandes` es menor que el total del dataset y todas sus filas tienen `tamano_proveedor == "Grande"`.

---

### 🔷 Sección 3 — Seleccionar columnas y ordenar

**🎯 Objetivo:** Ver las 10 compras de mayor monto, mostrando solo categoría y monto.

**💡 Concepto clave:** En un informe, no necesitas todas las columnas. `df[['col1','col2']]` es como ocultar columnas en Excel para quedarte solo con lo relevante. `sort_values` es el botón "Ordenar de mayor a menor". Juntos, son la base de cualquier ranking.

**🔍 Qué hace el código:**
1. `df.sort_values('monto_total', ascending=False)` ordena el DataFrame de mayor a menor monto.
2. `.head(10)` toma las primeras 10 filas (las de mayor monto).
3. `[['categoria','monto_total']]` selecciona solo esas dos columnas.

**⚠️ Error frecuente:** Olvidar `ascending=False`. Por defecto, `sort_values` ordena de menor a mayor. Para un ranking de "top 10", necesitas `ascending=False`.

**✅ Señal de comprensión:** El DataFrame `top` tiene exactamente 10 filas, solo 2 columnas, y el primer monto es mayor que el último.

---

### 🔷 Sección 4 — Agregar: groupby

**🎯 Objetivo:** Calcular el monto promedio de compras para cada categoría de producto.

**💡 Concepto clave:** `groupby` es la **tabla dinámica de Python**. Le dices: "agrupa por esta columna" y luego "calcula este número para cada grupo". Es como en Excel cuando arrastras una categoría al área de filas de una tabla dinámica y un valor al área de valores.

**🔍 Qué hace el código:**
- `df.groupby('categoria')['monto_total'].mean()` agrupa todas las filas por categoría y para cada grupo calcula el promedio de `monto_total`.
- El resultado es una Series donde el índice es la categoría y el valor es el promedio.

**⚠️ Error frecuente:** Confundir `groupby('categoria')` (agrupa filas) con `df['categoria']` (selecciona columna). `groupby` crea grupos; la selección de columna posterior indica *qué calcular* dentro de cada grupo.

**✅ Señal de comprensión:** `gasto_categoria` tiene tantas filas como categorías únicas en el dataset, y el gráfico de barras muestra diferencias claras entre categorías.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Inspecciona la tabla

**Habilidad que desarrolla:** Exploración inicial de un DataFrame.

**Pista 1 (conceptual):** `df.shape` te da una tupla con dos números. ¿Puedes asignar esos dos números a dos variables distintas al mismo tiempo?

**Pista 2 (técnica):** En Python puedes "desempaquetar" una tupla: si `df.shape` devuelve `(5000, 8)`, entonces `a, b = df.shape` deja `a = 5000` y `b = 8`. Algo similar necesitas hacer.

**Pista 3 (casi solución):** Las variables que necesitas son `n_filas` y `n_cols`. Para `columnas`, necesitas convertir `df.columns` a lista. Hay una función built-in de Python que convierte cosas a lista...

**Lógica de solución:** Desempaquetar `df.shape` en dos variables, y convertir `df.columns` a lista con `list()`.

---

### ✍️ Ejercicio 2 — Filtra los proveedores Grande

**Habilidad que desarrolla:** Aplicar máscaras booleanas para filtrar filas.

**Pista 1 (conceptual):** ¿Cómo le preguntas a una columna si su valor es igual a algo? En Python comparas con dos signos igual, no uno.

**Pista 2 (técnica):** `df["tamano_proveedor"] == "Grande"` crea una máscara True/False. Pero eso solo crea la máscara. Para *aplicarla* al DataFrame, necesitas pasarla dentro de los corchetes del DataFrame.

**Pista 3 (casi solución):** La estructura es `df[df["columna"] == "valor"]`. Reemplaza "columna" por el nombre real y "valor" por el texto exacto que buscas (respeta mayúsculas).

**Lógica de solución:** Crear una máscara con `==` sobre la columna de tamaño y aplicarla al DataFrame completo entre corchetes.

---

### ✍️ Ejercicio 3 — Top 10 compras por monto

**Habilidad que desarrollas:** Ordenar y seleccionar columnas específicas.

**Pista 1 (conceptual):** Para obtener el "top", primero debes ordenar de mayor a menor. ¿Qué parámetro de `sort_values` controla la dirección del orden?

**Pista 2 (técnica):** `.sort_values('monto_total', ascending=False)` ordena el DataFrame. Luego `.head(10)` toma los primeros 10. ¿Cómo seleccionas solo dos columnas de esa tabla ordenada?

**Pista 3 (casi solución):** Para seleccionar varias columnas, usa corchetes dobles: `df[['col1', 'col2']]`. Encadena las tres operaciones una tras otra con punto.

**Lógica de solución:** Ordenar descendente → tomar head(10) → seleccionar las dos columnas, todo encadenado.

---

### ✍️ Ejercicio 4 — Monto promedio por categoría

**Habilidad que desarrollas:** Usar `groupby` para responder preguntas agregadas.

**Pista 1 (conceptual):** Piensa en una tabla dinámica de Excel donde las filas son categorías y el valor es el promedio de monto. `groupby` hace exactamente eso.

**Pista 2 (técnica):** `df.groupby('categoria')` crea los grupos. Luego seleccionas la columna que quieres calcular con `['monto_total']`. Finalmente aplicas la función de agregación: `.mean()`.

**Pista 3 (casi solución):** La estructura completa es `df.groupby('columna_grupo')['columna_valor'].funcion_agregacion()`. Reemplaza las partes con los nombres correctos.

**Lógica de solución:** `groupby` sobre categoría → selección de monto_total → `.mean()` al final.

---

## 7. Profundidad en Política Pública: Ejercicio 4 — Monto promedio por categoría

Este ejercicio es el más relevante para el trabajo del Estado porque **responde directamente una pregunta de gestión**: *¿en qué tipos de bienes o servicios gasta más el sector público por transacción?*

### ¿Por qué importa para política pública?

El análisis de gasto promedio por categoría permite:

- **Detectar anomalías:** Si una categoría tiene un promedio muy superior al resto, puede indicar sobreprecios o concentración en pocos proveedores.
- **Priorizar fiscalización:** La Contraloría y la Dirección de Compras pueden focalizar revisiones en categorías con mayor monto promedio o mayor varianza.
- **Diseñar marcos de referencia:** Los precios de referencia para licitaciones se basan justamente en promedios históricos por categoría.
- **Evaluar ahorro por convenios marco:** Comparar el promedio de compras en convenio vs. fuera de convenio en una misma categoría.

### Cómo profundizar este análisis

| Pregunta de política pública | Extensión del groupby |
|---|---|
| ¿Cuánto se gasta en total por categoría? | Cambiar `.mean()` por `.sum()` |
| ¿Cuántas transacciones hay por categoría? | Usar `.count()` |
| ¿Cuál es la dispersión del gasto? | Usar `.std()` (desviación estándar) |
| ¿Cuál es el mayor gasto individual por categoría? | Usar `.max()` |
| ¿Cómo varía por región y categoría a la vez? | `groupby(['region','categoria'])` |

> 🏛️ **Conexión con ChileCompra:** La plataforma Mercado Público publica estadísticas de gasto por rubro. Con este `groupby`, tú puedes reproducir —y profundizar— ese análisis con los datos completos.

---

## 8. Conexión con profundiza.ipynb

El `profundiza.ipynb` de este módulo es un complemento **opcional** que lleva las habilidades del `leccion.ipynb` un paso más adelante.

### Comparativa leccion vs. profundiza

| Tema | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| Filtrado | Una condición simple (`tamano == "Grande"`) | Condiciones combinadas con `&` y `\|` |
| Conteos | No incluye | `value_counts` para diagnóstico rápido |
| Columnas nuevas | No incluye | Crea `monto_por_unidad` (columna derivada) |
| Complejidad | ⭐⭐ Básico | ⭐⭐⭐ Intermedio |
| Prerrequisito para | R2-01 | R2-02 (feature engineering) |

### Guía de decisión

```
¿Completaste todas las ✅ del leccion.ipynb?
    ├── No → Termina primero la lección.
    └── Sí → ¿Tienes 30 minutos extra?
              ├── Sí → ¡Haz el profundiza! Te prepara mejor para R2-02.
              └── No → Avanza a R2-01. Puedes volver después.
```

**Ejercicio más importante del profundiza:** El Ejercicio 3 (columna derivada `monto_por_unidad`) es el preludio directo del **feature engineering** de R2-02. Si planeas completar la Rama R2 completa, este ejercicio es estratégicamente valioso.

---

## 9. Autoevaluación Final

Responde sin mirar el notebook.

---

**Pregunta 1:** ¿Qué devuelve `df.shape`?

- a) Una lista con los nombres de columnas
- b) Una tupla con el número de filas y columnas
- c) El número de filas solamente
- d) Un resumen estadístico de la tabla

✅ **Respuesta correcta: b)**
**Explicación:** `df.shape` devuelve una tupla `(n_filas, n_columnas)`. Es el primer comando que deberías ejecutar al explorar cualquier dataset nuevo. Para obtener solo las filas, usarías `len(df)`.

---

**Pregunta 2:** ¿Cuál de las siguientes líneas filtra correctamente las compras a proveedores "Grande"?

- a) `df["tamano_proveedor"] = "Grande"`
- b) `df.filter("tamano_proveedor" == "Grande")`
- c) `df[df["tamano_proveedor"] == "Grande"]`
- d) `df.where("tamano_proveedor", "Grande")`

✅ **Respuesta correcta: c)**
**Explicación:** La sintaxis correcta es `df[condicion]` donde la condición es una máscara booleana. La opción a) asigna un valor (un solo `=`), no filtra. Las opciones b) y d) no existen con esa sintaxis en pandas.

---

**Pregunta 3:** Quieres el top 5 de compras ordenadas de mayor a menor monto. ¿Qué código es correcto?

- a) `df.sort_values('monto_total').head(5)`
- b) `df.sort_values('monto_total', ascending=False).head(5)`
- c) `df.head(5).sort_values('monto_total', ascending=False)`
- d) `df.sort_values('monto_total', ascending=True).tail(5)`

✅ **Respuesta correcta: b)**
**Explicación:** `ascending=False` ordena de mayor a menor. Luego `.head(5)` toma los primeros 5. La opción c) es incorrecta: primero toma 5 filas cualquiera y luego las ordena, sin garantizar que sean las de mayor monto global.

---

**Pregunta 4:** ¿Qué hace `df.groupby('categoria')['monto_total'].mean()`?

- a) Filtra las filas donde monto_total es el promedio
- b) Calcula el promedio general de monto_total ignorando categorías
- c) Calcula el promedio de monto_total para cada categoría de forma separada
- d) Agrupa las categorías por su monto promedio

✅ **Respuesta correcta: c)**
**Explicación:** `groupby` divide el DataFrame en grupos según la columna indicada. `['monto_total'].mean()` calcula el promedio de esa columna dentro de cada grupo. El resultado es una tabla con una fila por cada categoría única.

---

**Pregunta 5:** En el contexto de compras públicas, ¿para qué sirve `value_counts` sobre la columna `tamano_proveedor`?

- a) Para ordenar los proveedores por tamaño
- b) Para ver cuántas compras hay por cada tamaño de proveedor (Grande, Mediana, Pequeña)
- c) Para calcular el monto total por tamaño de proveedor
- d) Para filtrar solo los proveedores grandes

✅ **Respuesta correcta: b)**
**Explicación:** `value_counts()` cuenta cuántas veces aparece cada valor único en una columna. Aplicado a `tamano_proveedor`, muestra cuántas transacciones corresponden a cada tamaño. Es el primer diagnóstico de distribución: ¿el Estado compra más a empresas grandes o pequeñas?

---

## 10. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **DataFrame** | Tabla de datos bidimensional (filas y columnas) en memoria | Una planilla Excel abierta como objeto |
| **pandas** | Librería de Python especializada en tablas de datos | El "Excel" de Python |
| **`pd.read_csv()`** | Función que carga un archivo .csv y lo convierte en DataFrame | Abrir archivo → Importar datos en Excel |
| **`df.shape`** | Atributo que devuelve (n_filas, n_columnas) | Ctrl+Fin en Excel para ver el tamaño |
| **`df.columns`** | Lista de nombres de columnas del DataFrame | Los encabezados de tu planilla |
| **Máscara booleana** | Serie de valores True/False que indica qué filas cumplen una condición | Filtro aplicado en Excel |
| **`df.sort_values()`** | Ordena las filas por una columna (ascendente o descendente) | Botón "Ordenar A→Z" o "Z→A" en Excel |
| **`df.head(n)`** | Devuelve las primeras n filas | Ver las primeras filas de una tabla |
| **`groupby`** | Agrupa filas por categoría y calcula estadísticas por grupo | Tabla dinámica en Excel |
| **`.mean()`** | Calcula el promedio de una columna numérica | Función PROMEDIO() en Excel |
| **`ascending=False`** | Parámetro que ordena de mayor a menor | Orden descendente en Excel |
| **`list(df.columns)`** | Convierte el índice de columnas a una lista de Python | Copiar los encabezados de una fila |

---

## 11. Conexión con el Módulo Siguiente

Has completado **R2-00 · Fundamentos express**. Ahora sabes cargar, inspeccionar, filtrar, ordenar y agregar datos con pandas. Ese es el vocabulario base.

**El próximo módulo es R2-01 · Datos: traer, cruzar y limpiar.**

En R2-01 vas a enfrentar el problema real de la ciencia de datos en el sector público: los datos nunca vienen perfectos. Vas a aprender a:

- **Traer datos** desde múltiples fuentes (archivos CSV, URLs, APIs básicas).
- **Cruzar tablas** con `merge` (el equivalente a BUSCARV/XLOOKUP de Excel, pero más potente).
- **Limpiar datos** sucios: valores nulos, formatos inconsistentes, duplicados.

> 🔗 **Por qué importa la secuencia:** En R2-00 aprendiste a *manipular* datos ya limpios. En R2-01 aprenderás a *obtenerlos y prepararlos* desde el mundo real. Es el paso previo obligatorio antes de construir cualquier modelo de datos públicos.

**Antes de pasar:** asegúrate de que tus 4 celdas de chequeo muestren ✅. ¡Ánimo, que vas bien! 🚀
