# Guía de Aprendizaje — R1-02 · Exploración con pandas

> **Rama:** R1 · Análisis y Visualización | **Módulo:** R1-02 | **Nivel:** Introductorio  
> **Duración estimada:** 3–4 horas | **Prerrequisitos:** R1-00 Fundamentos, R1-01 Traer el dato  
> **Competencia de salida:** Cargar un dataset con pandas, inspeccionarlo y obtener un primer resumen exploratorio con datos reales del sector público chileno.

---

## 1. ¿Para qué me sirve esto como funcionario/a público/a?

Cada día, miles de funcionarios del Estado chileno trabajan con datos: registros de beneficiarios, licitaciones, inventarios, estadísticas de atención, nóminas. La herramienta más usada para eso es Excel, y está bien. Pero Excel tiene límites: se pone lento con archivos grandes, no deja registrar los pasos que seguiste, y es difícil repetir el mismo análisis el mes siguiente.

**pandas es el Excel del mundo del análisis de datos profesional.** Te permite hacer todo lo que harías en Excel —filtrar, contar, calcular promedios— pero de forma reproducible, documentada y escalable.

En este módulo trabajarás con el dataset de **establecimientos del Servicio Médico Legal (SML)** de Chile. Son datos reales, públicos, de `datos.gob.cl`. Con ellos podrás responder preguntas como:

- ¿Cuántos SML hay en cada región?
- ¿Qué región tiene más establecimientos y cuál tiene menos?
- ¿La distribución territorial del SML es equitativa?

Estas preguntas —aparentemente técnicas— tienen implicancias directas en política pública de acceso a la justicia y servicios del Estado.

---

## 2. Mapa conceptual del módulo

Antes de entrar al notebook, mira este mapa. Cada concepto nuevo tiene su equivalente en el mundo que ya conoces:

| Concepto pandas | Equivalente en tu trabajo | Para qué sirve |
|---|---|---|
| `pd.read_csv()` | Abrir un archivo en Excel | Cargar los datos al entorno de trabajo |
| `DataFrame` | La hoja de cálculo | La tabla donde viven todos tus datos |
| `.head()` / `.shape` | Ver las primeras filas y el tamaño del archivo | Entender de qué tamaño es el dataset |
| `.value_counts()` | Tabla dinámica de recuento | Contar cuántos hay por categoría |
| `.describe()` | Estadísticas rápidas en Excel | Obtener mínimo, máximo, promedio de un golpe |

---

## 3. Antes de empezar: Verificación de prerrequisitos

Este módulo asume que puedes hacer lo siguiente. Marca cada uno honestamente:

- [ ] Puedo ejecutar una celda en Google Colab con `Shift + Enter`
- [ ] Sé qué es una variable en Python (por ejemplo, `nombre = "Felipe"`)
- [ ] Entiendo qué es una función y cómo llamarla (por ejemplo, `print("hola")`)
- [ ] Puedo subir o enlazar un archivo CSV desde Google Drive o URL
- [ ] Sé qué es `import` y para qué se usa

Si marcaste todos: ¡estás listo/a! Si te quedaron pendientes, revisa **R1-00 Fundamentos** y **R1-01 Traer el dato** antes de continuar.

---

## 4. Guía paso a paso por sección del notebook

### Sección 1 · ¿Qué es pandas y el DataFrame?

**🎯 Objetivo:** Cargar el dataset de establecimientos SML y entender qué es un DataFrame.

**💡 Concepto clave:** Un `DataFrame` es una tabla. Igual que en Excel, tiene filas y columnas. La diferencia es que en pandas esa tabla vive en la memoria del computador y puedes manipularla con código.

```python
import pandas as pd
df = pd.read_csv("establecimientos.csv")
```

**🔍 ¿Qué hace este código?**
- `import pandas as pd` → carga la librería pandas y le pone el apodo `pd` para escribir menos
- `pd.read_csv(...)` → lee el archivo CSV y lo convierte en un DataFrame
- `df` → es el nombre que le damos a nuestra tabla (podría llamarse cualquier cosa, pero `df` es la convención)

**⚠️ Error frecuente:** `FileNotFoundError` — significa que el archivo no está en la misma carpeta que tu notebook. Verifica la ruta del archivo o que lo subiste correctamente a Colab.

**✅ Sabes esta sección cuando puedes:** Ejecutar la celda sin errores y ver que `df` existe.

---

### Sección 2 · Inspección inicial

**🎯 Objetivo:** Entender qué hay en el dataset antes de hacer cualquier análisis.

**💡 Concepto clave:** Antes de trabajar con cualquier dato del Estado, necesitas saber qué tienes. ¿Cuántos registros? ¿Qué columnas? ¿Hay datos vacíos? Es como revisar el expediente antes de la reunión.

```python
df.head()        # muestra las primeras 5 filas
df.shape         # devuelve (filas, columnas)
df.columns       # lista los nombres de las columnas
df.info()        # tipo de dato de cada columna y valores nulos
```

**🔍 ¿Qué hace cada línea?**
- `.head()` → las primeras 5 filas, como ver el encabezado de un informe
- `.shape` → te dice `(38, 5)`, es decir: 38 establecimientos, 5 columnas
- `.columns` → lista los campos: `establecimiento`, `region`, `comuna`, `latitud`, `longitud`
- `.info()` → te dice si hay celdas vacías (en este dataset no hay)

**⚠️ Error frecuente:** Escribir `df.head` sin paréntesis — no muestra nada, solo describe la función. Siempre con `()`.

**✅ Sabes esta sección cuando puedes:** Decir de memoria cuántas filas y columnas tiene el dataset y cómo se llaman las columnas.

---

### Sección 3 · Seleccionar columnas y filtrar filas

**🎯 Objetivo:** Quedarte solo con los datos que necesitas, como aplicar un filtro en Excel.

**💡 Concepto clave:** En Excel usas el filtro automático para mostrar solo ciertas filas. En pandas haces lo mismo con una condición dentro de corchetes. Lo llamamos el "embudo": entran todos los datos, salen solo los que cumplen el criterio.

```python
# Seleccionar solo la columna de región
df["region"]

# Filtrar solo los SML de la Región del Maule
df[df["region"] == "Maule"]
```

**🔍 ¿Qué hace cada línea?**
- `df["region"]` → extrae una sola columna, como hacer clic en la cabecera en Excel
- `df[df["region"] == "Maule"]` → crea una condición verdadero/falso y la aplica como filtro

**⚠️ Error frecuente:** Usar `=` en vez de `==` dentro del filtro. Un `=` es asignación; `==` es comparación.

**✅ Sabes esta sección cuando puedes:** Filtrar el dataset por cualquier región y ver solo sus establecimientos.

---

### Sección 4 · Contar por categoría con `value_counts`

**🎯 Objetivo:** Saber cuántos SML hay en cada región con una sola línea de código.

**💡 Concepto clave:** Es exactamente la tabla dinámica de Excel, pero en una línea. `value_counts()` cuenta cuántas veces aparece cada valor único en una columna.

```python
df["region"].value_counts()
```

**🔍 ¿Qué hace este código?**
Devuelve una tabla ordenada de mayor a menor con el recuento por región. Resultado:
```
Maule           6
Valparaíso      4
O'Higgins       3
...
```

**⚠️ Error frecuente:** Aplicar `value_counts()` a todo el DataFrame en vez de a una columna. Siempre especifica la columna primero: `df["columna"].value_counts()`.

**✅ Sabes esta sección cuando puedes:** Responder de inmediato "¿qué región tiene más SML?" mirando el output.

---

### Sección 5 · Estadísticos rápidos

**🎯 Objetivo:** Obtener mínimo, máximo, promedio y más con una sola instrucción.

**💡 Concepto clave:** En Excel usarías funciones separadas: `=PROMEDIO()`, `=MIN()`, `=MAX()`. En pandas, `.describe()` te da todo eso junto para las columnas numéricas.

```python
df["latitud"].describe()
df["latitud"].mean()
df["latitud"].min()
df["latitud"].max()
```

**🔍 Interpretación con el dataset SML:**
- `max` de latitud → `-18.47` → Arica (más al norte, valor menos negativo)
- `min` de latitud → `-53.15` → Punta Arenas (más al sur, valor más negativo)
- `mean` → `-35.13` → el "centro geográfico" promedio de la red SML está en la zona centro-sur

**⚠️ Error frecuente:** Confundirse con los valores negativos de latitud. En el hemisferio sur, el valor más cercano a cero es el más al norte, y el más negativo es el más al sur.

**✅ Sabes esta sección cuando puedes:** Leer el output de `.describe()` y explicar qué significa cada línea.

---

### Sección 6 · Errores típicos

**🎯 Objetivo:** Reconocer y resolver los errores más comunes antes de que te frustren.

| Error | Mensaje | Causa | Solución |
|---|---|---|---|
| `FileNotFoundError` | No se encontró el archivo | La ruta del CSV es incorrecta | Verificar nombre y ubicación del archivo |
| `KeyError: 'Region'` | Columna no encontrada | Mayúsculas incorrectas | Usar `df.columns` para ver el nombre exacto |
| `SyntaxError` | Error de sintaxis | Falta `==` o comillas | Revisar la condición del filtro |
| `AttributeError` | No existe el método | Se escribió mal el método | Verificar ortografía: `.head()` no `.Head()` |

---

## 5. Guía de los 5 Ejercicios

### Ejercicio 01 · ¿Cuántos establecimientos hay en total?

**Habilidad que entrena:** Usar `.shape` para conocer el tamaño del dataset.

**Pista suave 🟢:** El dataset tiene filas y columnas. ¿Qué atributo de pandas te da esa información de una vez?

**Pista media 🟡:** `df.shape` devuelve una tupla. El primer número es lo que buscas.

**Pista directa 🔴:** Accede al primer elemento de `.shape` con `df.shape[0]`.

**Lógica de la solución:** `.shape` devuelve `(filas, columnas)`. Para quedarte solo con las filas, usa el índice `[0]`. Resultado esperado: `38`.

**✅ El chequeo automático valida que:** el valor sea exactamente 38.

---

### Ejercicio 02 · Lista de columnas

**Habilidad que entrena:** Inspeccionar la estructura del DataFrame con `.columns`.

**Pista suave 🟢:** ¿Qué atributo de un DataFrame muestra los nombres de todas sus columnas?

**Pista media 🟡:** Es una sola palabra: `columns`. Se accede directamente sin paréntesis.

**Pista directa 🔴:** `df.columns` devuelve un Index con los nombres. Para convertirlo a lista: `list(df.columns)`.

**Lógica de la solución:** `.columns` es un atributo, no un método, por eso no lleva `()`. El resultado incluye las 5 columnas del dataset.

**✅ El chequeo automático valida que:** la lista contenga exactamente los 5 nombres de columna correctos.

---

### Ejercicio 03 · Región con más establecimientos

**Habilidad que entrena:** Usar `.value_counts()` e identificar el valor más frecuente.

**Pista suave 🟢:** Necesitas contar cuántas veces aparece cada región. ¿Qué método hace eso?

**Pista media 🟡:** `value_counts()` ordena de mayor a menor automáticamente. El primer resultado es el que buscas.

**Pista directa 🔴:** Usa `.value_counts().index[0]` para extraer el nombre de la región con más establecimientos.

**Lógica de la solución:** `value_counts()` devuelve una Serie ordenada. El índice `[0]` corresponde al valor más frecuente. Resultado esperado: `"Maule"`.

**✅ El chequeo automático valida que:** la respuesta sea `"Maule"`.

---

### Ejercicio 04 · Establecimiento más al norte

**Habilidad que entrena:** Combinar `.max()` con filtrado para obtener un registro específico.

**Pista suave 🟢:** "Más al norte" en Chile significa la latitud menos negativa (más cercana a cero). ¿Qué función te da el máximo de una columna?

**Pista media 🟡:** Primero calcula `df["latitud"].max()`, luego úsalo como condición de filtro.

**Pista directa 🔴:** `df[df["latitud"] == df["latitud"].max()]["establecimiento"].values[0]`

**Lógica de la solución:** El máximo de latitud en un dataset del hemisferio sur es el valor menos negativo, que corresponde a la ubicación más septentrional. Resultado esperado: `"Servicio Médico Legal Arica"`.

**✅ El chequeo automático valida que:** el nombre del establecimiento sea el de Arica.

---

### Ejercicio 05 · Interpretar para decidir (Política Pública)

**Habilidad que entrena:** Leer un resultado de `value_counts()` e interpretarlo en contexto de política pública.

**Pista suave 🟢:** Compara el número de SML en la Región Metropolitana versus la Región del Maule. ¿Qué te dice esa diferencia?

**Pista media 🟡:** La Región Metropolitana concentra el 40% de la población del país. ¿Tiene sentido que el Maule tenga más SML que ella?

**Pista directa 🔴:** Usa `value_counts()` para obtener los números exactos y selecciona la opción que mejor interpreta la distribución territorial.

**Lógica de la solución:** El dataset muestra Maule=6 y Metropolitana=2. Si se mide solo por número de establecimientos (sin ajustar por población), el Maule tiene 3 veces más SML que la Región Metropolitana, lo que podría indicar una distribución geográfica más que proporcional a la población. La respuesta correcta es la opción **B**.

**✅ El chequeo automático valida que:** se seleccione la opción B.

---

## 6. El Ejercicio 05 en profundidad: Interpretar para decidir

Este ejercicio no es técnico: es de **lectura crítica de datos para política pública**.

### Los números

| Región | N° SML | % Población aprox. |
|---|---|---|
| Metropolitana | 2 | ~40% |
| Maule | 6 | ~5% |
| Valparaíso | 4 | ~10% |
| Tarapacá | 1 | ~3% |

### Reflexión guiada

La distribución territorial del SML parece estar orientada a **cobertura geográfica** más que a **proporción poblacional**. Esto tiene sentido en servicios que deben estar físicamente cerca de donde ocurren los hechos (defunciones, pericias), no necesariamente donde vive más gente.

Sin embargo, una región con alta densidad poblacional y solo 2 establecimientos puede tener **listas de espera más largas** y **peores tiempos de respuesta**, lo que afecta el acceso equitativo a la justicia.

### Pregunta de debate

> ¿Qué otro dato pedirías para confirmar si la distribución es equitativa o no?

Algunas respuestas posibles:
- Número de pericias realizadas por establecimiento al año
- Tiempo promedio de respuesta por región
- Distancia promedio que recorre un ciudadano para llegar al SML más cercano
- Tasa de defunciones por región que requieren autopsia

Esta es la diferencia entre un analista de datos que entrega números y uno que **entrega decisiones**.

---

## 7. Autoevaluación Final

**Instrucciones:** Responde sin mirar el notebook. Son preguntas conceptuales, no de código.

**Pregunta 1.** ¿Qué devuelve `df.shape` para un dataset de 38 filas y 5 columnas?
- A) `[38, 5]`
- B) `(38, 5)` ✅
- C) `{filas: 38, columnas: 5}`
- D) `38`

*Explicación: `.shape` devuelve una tupla (tipo de dato inmutable), no una lista ni un diccionario.*

---

**Pregunta 2.** ¿Cuál es la diferencia entre `df["region"]` y `df[["region"]]`?
- A) No hay diferencia
- B) La primera devuelve una Serie; la segunda devuelve un DataFrame ✅
- C) La primera filtra; la segunda cuenta
- D) La segunda falla con error

*Explicación: Un corchete simple extrae una Serie (una columna). Doble corchete extrae un DataFrame de una sola columna. Es útil cuando quieres mantener el formato tabular.*

---

**Pregunta 3.** ¿Qué hace `df[df["region"] == "Maule"]`?
- A) Elimina las filas donde región es Maule
- B) Devuelve solo las filas donde la región es Maule ✅
- C) Cuenta cuántas filas tienen región igual a Maule
- D) Renombra la columna región

*Explicación: La condición entre corchetes crea una máscara booleana (True/False por cada fila) y la aplica como filtro.*

---

**Pregunta 4.** En el dataset SML, ¿qué significa que el `min` de latitud sea `-53.15`?
- A) Es un error en los datos
- B) Ese establecimiento está más al norte
- C) Ese establecimiento está más al sur ✅
- D) La latitud no tiene relación con la posición geográfica

*Explicación: En el hemisferio sur, las latitudes son negativas. El valor más negativo corresponde a la posición más austral: Punta Arenas.*

---

**Pregunta 5.** ¿Cuál es la forma más rápida de obtener el número de valores únicos en la columna `region`?
- A) `df.shape[0]`
- B) `df["region"].count()`
- C) `df["region"].nunique()` ✅
- D) `df["region"].describe()`

*Explicación: `.nunique()` cuenta los valores únicos (no nulos). `.count()` cuenta todos los valores no nulos (incluyendo repetidos). `.nunique()` para el dataset SML devuelve 16.*

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **DataFrame** | Tabla de datos en pandas | Hoja de cálculo de Excel |
| **Serie** | Una sola columna de un DataFrame | Una columna de Excel |
| **índice** | El número de fila que pandas asigna automáticamente | El número de fila en Excel |
| **`pd.read_csv()`** | Función que carga un archivo CSV como tabla | Abrir un archivo en Excel |
| **`.head()`** | Muestra las primeras 5 filas | Hacer scroll al inicio del archivo |
| **`.shape`** | Tupla con (filas, columnas) | Ver el tamaño del archivo |
| **`.info()`** | Resumen técnico: tipos de dato y valores nulos | Revisar el formato de cada columna |
| **`.value_counts()`** | Recuento por categoría, ordenado de mayor a menor | Tabla dinámica de recuento en Excel |
| **`.describe()`** | Estadísticos descriptivos de columnas numéricas | Funciones PROMEDIO, MIN, MAX, etc. |
| **filtro booleano** | Condición que devuelve True/False por cada fila | Filtro automático de Excel |
| **`NaN`** | Celda vacía o valor faltante | Celda en blanco en Excel |
| **latitud** | Coordenada geográfica norte-sur. Negativa en el hemisferio sur | Fila en un mapa |

---

## 9. Conexión con el siguiente módulo

Ya sabes explorar un dataset: cargarlo, inspeccionarlo, filtrar, contar y calcular estadísticos básicos. Es un logro real.

El próximo módulo es **R1-03 · Cruzar y resumir tablas**, donde aprenderás a:
- **Combinar dos tablas** que comparten una columna en común (como hacer un `BUSCARV` en Excel, pero mejor)
- **Resumir por grupos** con `groupby` (como una tabla dinámica completa)

Pregunta motivadora para que llegues con hambre:

> *¿Qué pasaría si tuvieras el dataset de SML y además una tabla con la población de cada región? ¿Cómo calcularías el número de SML por cada 100.000 habitantes?*

Eso es exactamente lo que harás en R1-03. ¡Nos vemos ahí!

---

*Guía elaborada para el Bootcamp de Datos — Formación Pública Chile · Licencia CC BY 4.0*
