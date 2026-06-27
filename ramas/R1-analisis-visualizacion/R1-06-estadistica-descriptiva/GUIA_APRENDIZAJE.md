# Guía de Aprendizaje — R1-06 · Estadística descriptiva

> **Rama:** R1 · Análisis y Visualización | **Módulo:** R1-06 | **Nivel:** Introductorio-Intermedio  
> **Duración estimada:** 3–4 horas | **Prerrequisitos:** R1-05 · SQL para análisis  
> **Competencia de salida:** Resumir una columna numérica con medidas de tendencia central y dispersión, interpretar un `describe()` completo, y explicar por qué la mediana describe mejor que la media en datos sesgados.

---

## 1. ¿Para qué me sirve esto como funcionario/a público/a?

Cada vez que lees un titular como *"el ingreso promedio del país subió un 5%"* o *"el tiempo promedio de espera en urgencias es 3 horas"*, alguien calculó un promedio. Pero ¿realmente ese número representa a la mayoría de las personas?

Cuando los datos son muy desiguales — como la población de las comunas de Chile, donde Puente Alto tiene 568.086 habitantes y Pichilemu tiene 19.847 — **el promedio miente**. Suma todos los números y divide, y obtienes un valor que no representa a ninguna comuna real.

En este módulo aprenderás a elegir la medida correcta según los datos, usando **30 comunas reales de Chile del Censo 2024 (INE)**. Saber esto te permite leer informes oficiales con ojo crítico y producir resúmenes que no engañen.

---

## 2. Mapa conceptual del módulo

| Medida | ¿Qué responde? | Función pandas | Cuándo usarla |
|---|---|---|---|
| **Media** | ¿Cuál es el promedio? | `.mean()` | Datos simétricos, sin outliers extremos |
| **Mediana** | ¿Cuál es el valor del medio? | `.median()` | Datos sesgados, con outliers (salarios, población) |
| **Moda** | ¿Cuál es el valor más frecuente? | `.mode()` | Variables categóricas o discretas |
| **Rango** | ¿Cuánto varían los extremos? | `.max() - .min()` | Detectar el tamaño del espacio total |
| **Desv. estándar** | ¿Qué tan dispersos están? | `.std()` | Ver si los datos están concentrados o dispersos |
| **Cuartiles** | ¿Cómo se distribuye el 50% central? | `.quantile([.25,.75])` | Entender la distribución sin que outliers la distorsionen |
| **`describe()`** | Resumen completo de la columna | `.describe()` | Primera inspección de cualquier columna numérica |

---

## 3. Antes de empezar: Verificación de prerrequisitos

- [ ] Sé cargar un CSV con `pd.read_csv()` e inspeccionar con `.info()`
- [ ] Sé seleccionar una columna con `df["columna"]`
- [ ] Sé filtrar filas con una condición
- [ ] Entiendo qué es `NaN` y cómo detectarlo
- [ ] Sé usar `.groupby()` para resumir por categoría

Si tienes dudas, repasa **R1-02 · Exploración con pandas**.

---

## 4. El dataset real: 30 comunas de Chile — Censo 2024 (INE)

```
comuna,poblacion
Puente Alto,568086
Maipú,503635
Santiago,438856
Antofagasta,401096
...
Pichilemu,19847
```

**Datos clave para los ejercicios:**

| Estadístico | Valor |
|---|---|
| Número de comunas | 30 |
| Población máxima | 568.086 (Puente Alto) |
| Población mínima | 19.847 (Pichilemu) |
| Media | ~156.087 |
| Mediana | ~72.761 |
| Desviación estándar | ~163.991 |
| Q1 (25%) | ~35.651 |
| Q3 (75%) | ~198.282 |

> **La clave del módulo:** La media (~156.087) casi duplica la mediana (~72.761). Eso indica una distribución fuertemente sesgada hacia arriba: pocas comunas muy grandes jalan el promedio, mientras la mayoría de las comunas de la muestra son mucho más pequeñas.

---

## 5. Guía paso a paso por sección del notebook

### Sección 1 · Media y mediana: el duelo de los promedios

**🎯 Objetivo:** Calcular ambas medidas y entender cuándo cada una es más honesta.

**💡 Concepto clave:** La **media** suma todos los valores y divide por la cantidad. La **mediana** ordena los valores y toma el del medio. Con datos simétricos, ambas coinciden. Con datos sesgados (como ingresos, poblaciones, tiempos de espera), la media se jala hacia los extremos y la mediana permanece estable.

**Analogía del sector público:** Si en tu servicio hay 9 funcionarios que ganan $800.000 y un director que gana $8.000.000, el salario *promedio* es $1.520.000 — un número que no representa a nadie. El salario *mediano* es $800.000 — eso sí describe lo que gana la mayoría.

**🔍 Qué hace el código:**
```python
media = df["poblacion"].mean()
mediana = df["poblacion"].median()
print(f"Media: {media:,.0f}")
print(f"Mediana: {mediana:,.0f}")
print(f"Diferencia: {media - mediana:,.0f}")
```

**Resultado con el dataset real:**
- Media: **~156.087** hab.
- Mediana: **~72.761** hab.
- Diferencia: ~83.326 hab. — la media casi duplica la mediana.

**⚠️ Error frecuente:** Reportar siempre la media por costumbre, sin revisar si los datos son simétricos. Antes de publicar un promedio, siempre compara con la mediana.

**✅ Sabes esta sección cuando puedes:** Explicar en una oración por qué la media es mayor que la mediana en este dataset.

---

### Sección 2 · Dispersión: rango y desviación estándar

**🎯 Objetivo:** Medir qué tan separados están los datos entre sí.

**💡 Concepto clave:** Dos conjuntos de datos pueden tener el mismo promedio pero ser completamente distintos. Si 10 comunas tienen 100.000 habitantes cada una, la media es 100.000 y la dispersión es 0. Si 5 tienen 10.000 y 5 tienen 190.000, la media sigue siendo 100.000 pero la dispersión es enorme. La **desviación estándar** captura esa diferencia.

**🔍 Qué hace el código:**
```python
rango = df["poblacion"].max() - df["poblacion"].min()
desv = df["poblacion"].std()
print(f"Rango: {rango:,.0f}")
print(f"Desviación estándar: {desv:,.0f}")
```

**Resultado con el dataset real:**
- Rango: **548.239** hab. (de Pichilemu a Puente Alto)
- Desviación estándar: **~163.991** hab.

> La desviación estándar es mayor que la mediana. Eso confirma que las comunas son extremadamente heterogéneas: no hay un "tamaño típico" de comuna en Chile.

**⚠️ Error frecuente:** Confundir rango con desviación estándar. El rango sólo mira los dos extremos y puede ser engañoso si hay un solo outlier. La desviación estándar considera todos los valores.

**✅ Sabes esta sección cuando puedes:** Interpretar en palabras qué significa que la desviación estándar sea mayor que la mediana.

---

### Sección 3 · Cuartiles: el 50% central

**🎯 Objetivo:** Dividir los datos en cuatro partes iguales para entender la distribución sin que los extremos la distorsionen.

**💡 Concepto clave:** Los **cuartiles** dividen los datos ordenados en cuatro grupos del 25% cada uno. El Q1 (percentil 25) es el valor que deja el 25% más bajo debajo de él. Q2 es la mediana. Q3 (percentil 75) deja el 75% debajo. El **IQR** (rango intercuartílico = Q3 - Q1) describe dónde vive el 50% central de los datos — sin que los outliers lo afecten.

**🔍 Qué hace el código:**
```python
q1 = df["poblacion"].quantile(0.25)
q3 = df["poblacion"].quantile(0.75)
iqr = q3 - q1
print(f"Q1: {q1:,.0f}")
print(f"Q3: {q3:,.0f}")
print(f"IQR: {iqr:,.0f}")
```

**Resultado con el dataset real:**
- Q1: **~35.651** hab.
- Q3: **~198.282** hab.
- IQR: **~162.631** hab.

**Interpretación:** El 50% central de las comunas de la muestra tiene entre ~35.651 y ~198.282 habitantes. Ese es el rango "típico" de la distribución, sin contar los extremos.

**⚠️ Error frecuente:** Confundir percentil con porcentaje. Q1 = 35.651 no significa que el 25% de la población vive en comunas pequeñas — significa que el 25% de las **comunas de la muestra** tiene menos de 35.651 habitantes.

**✅ Sabes esta sección cuando puedes:** Calcular el IQR y explicar qué representa en el contexto de las comunas.

---

### Sección 4 · `describe()`: el resumen completo

**🎯 Objetivo:** Obtener todos los estadísticos básicos de una columna en una sola línea.

**💡 Concepto clave:** `df["columna"].describe()` entrega en un solo comando: count, mean, std, min, Q1, mediana (50%), Q3 y max. Es la primera cosa que debes ejecutar sobre cualquier columna numérica nueva.

**🔍 Resultado con el dataset real:**

```
count       30.000
mean    156087.333
std     163991.248
min      19847.000
25%      35650.750
50%      72761.000
75%     198282.250
max     568086.000
```

**Cómo leer este `describe()` de una mirada:**
- `count = 30` → 30 comunas, sin NaN
- `mean >> median (50%)` → distribución sesgada a la derecha (hay comunas muy grandes que jalan la media)
- `std > mean` → dispersión extrema, no hay un "tamaño típico"
- `min = 19.847` y `max = 568.086` → la comuna mayor es 28 veces más grande que la menor

**⚠️ Error frecuente:** Leer el `50%` como si fuera un porcentaje de la población. El `50%` en `describe()` es la **mediana** — el valor que divide los datos en dos mitades iguales.

**✅ Sabes esta sección cuando puedes:** Leer un `describe()` y decir en tres oraciones si los datos son simétricos, sesgados, y qué tan dispersos están.

---

### Sección 5 · Comparar grupos: estadísticas por categoría

**🎯 Objetivo:** Comparar estadísticos entre grupos usando `groupby` con métodos estadísticos.

**💡 Concepto clave:** Un promedio global puede esconder diferencias importantes entre grupos. En política pública, casi siempre te importa comparar: ¿las comunas del norte vs. el sur? ¿urbanidad vs. ruralidad? El `groupby` combinado con `.agg()` permite calcular varias estadísticas a la vez por grupo.

**🔍 Qué hace el código:**
```python
# Comunas sobre y bajo la mediana
mediana = df["poblacion"].median()
df["tamano"] = df["poblacion"].apply(
    lambda x: "grande" if x >= mediana else "pequeña"
)
df.groupby("tamano")["poblacion"].agg(["count", "mean", "median", "std"])
```

**⚠️ Error frecuente:** Usar `.mean()` directamente en el `groupby` sin considerar que los grupos pueden ser muy asimétricos. Siempre verifica con `.median()` también.

**✅ Sabes esta sección cuando puedes:** Dividir el dataset en dos grupos y calcular media y mediana para cada uno.

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 01 · Media y mediana

**Habilidad que entrena:** Calcular ambas medidas y comparar para detectar sesgo.

**Pista suave 🟢:** Calcula `.mean()` y `.median()` sobre `df["poblacion"]`. Guarda los resultados y compáralos.

**Pista media 🟡:** Si `media > mediana`, la distribución está sesgada a la derecha (hay valores muy grandes que empujan la media hacia arriba).

**Pista directa 🔴:**
```python
media = df["poblacion"].mean()
mediana = df["poblacion"].median()
```

**Lógica de la solución:** Media ≈ 156.087, Mediana ≈ 72.761. La diferencia de ~83.000 hab. confirma que Puente Alto, Maipú y Santiago distorsionan el promedio hacia arriba.

**✅ El chequeo automático valida que:** `media > mediana` y que ambos valores coinciden con los calculados desde el dataset real.

---

### Ejercicio 02 · Rango y desviación estándar

**Habilidad que entrena:** Medir la dispersión con dos instrumentos complementarios.

**Pista suave 🟢:** El rango es la diferencia entre el valor máximo y el mínimo. La desviación estándar se calcula con `.std()`.

**Pista media 🟡:** `rango = df["poblacion"].max() - df["poblacion"].min()`. Para `desv`, usa directamente `.std()`.

**Pista directa 🔴:**
```python
rango = df["poblacion"].max() - df["poblacion"].min()
desv = df["poblacion"].std()
```

**Lógica de la solución:** Rango = 548.239. Desviación estándar ≈ 163.991. Que la desviación estándar supere la mediana indica una dispersión extrema.

**✅ El chequeo automático valida que:** `rango == 548239` y `desv` coincide con el valor esperado.

---

### Ejercicio 03 · Cuartiles e IQR

**Habilidad que entrena:** Calcular Q1, Q3 e IQR para describir el 50% central.

**Pista suave 🟢:** Usa `.quantile(0.25)` para Q1 y `.quantile(0.75)` para Q3. El IQR es la diferencia.

**Pista media 🟡:** `iqr = q3 - q1`. El IQR describe el rango donde vive el 50% central de los datos.

**Pista directa 🔴:**
```python
q1 = df["poblacion"].quantile(0.25)
q3 = df["poblacion"].quantile(0.75)
iqr = q3 - q1
```

**Lógica de la solución:** Q1 ≈ 35.651, Q3 ≈ 198.282, IQR ≈ 162.631. El 50% central de las comunas tiene entre 35k y 198k habitantes.

**✅ El chequeo automático valida que:** `iqr == q3 - q1` y los valores coinciden con el dataset.

---

### Ejercicio 04 · Interpretar el `describe()`

**Habilidad que entrena:** Leer un resumen estadístico completo y extraer conclusiones.

**Pista suave 🟢:** Ejecuta `df["poblacion"].describe()` y lee cada fila. La fila `50%` es la mediana.

**Pista media 🟡:** Para extraer un valor específico del describe: `stats = df["poblacion"].describe()` y luego `stats["50%"]` para la mediana.

**Pista directa 🔴:**
```python
stats = df["poblacion"].describe()
mediana_describe = stats["50%"]
conteo = int(stats["count"])
```

**Lógica de la solución:** `count = 30` (sin NaN), `50% ≈ 72.761` (mediana real del dataset).

**✅ El chequeo automático valida que:** `conteo == 30` y `mediana_describe` coincide con `.median()`.

---

### Ejercicio 05 · Comunas sobre y bajo la mediana

**Habilidad que entrena:** Clasificar filas según una condición y comparar estadísticas entre grupos.

**Pista suave 🟢:** Crea una columna nueva `"tamano"` que valga `"grande"` si la población es mayor o igual a la mediana, y `"pequeña"` si no.

**Pista media 🟡:** Usa `.apply(lambda x: ...)` o `np.where()`. Luego usa `.groupby("tamano")["poblacion"].mean()` para comparar.

**Pista directa 🔴:**
```python
mediana = df["poblacion"].median()
df["tamano"] = df["poblacion"].apply(lambda x: "grande" if x >= mediana else "pequeña")
n_grandes = (df["tamano"] == "grande").sum()
n_pequenas = (df["tamano"] == "pequeña").sum()
```

**Lógica de la solución:** Por definición de mediana, hay 15 comunas grandes y 15 pequeñas.

**✅ El chequeo automático valida que:** `n_grandes == 15` y `n_pequenas == 15`.

---

## 7. Sección especial: Desigualdad demográfica y política pública

### Los números cuentan una historia

La brecha entre la media y la mediana en este dataset no es un detalle técnico — es un espejo de cómo se distribuye la población en Chile.

| Indicador | Valor | Interpretación |
|---|---|---|
| Media | ~156.087 hab. | Empujada por las grandes ciudades |
| Mediana | ~72.761 hab. | El valor "típico" real de la muestra |
| Comunas sobre la media | ~9 de 30 (30%) | Solo 9 comunas superan el promedio |
| Rango | 548.239 hab. | Puente Alto es 28x más grande que Pichilemu |

### La trampa del promedio en política pública

Imagina que el Ministerio del Interior debe distribuir recursos para atención primaria de salud entre las 30 comunas de esta muestra. Si usa el **promedio** (~156.087 hab.) como referencia, sobredimensiona los recursos para el 70% de las comunas y subdimensiona para el 30% más grande.

Si usa la **mediana** (~72.761 hab.) como referencia base, la asignación refleja mejor la realidad de la mayoría de las comunas. Para las comunas grandes, aplica un factor de ajuste por población.

> *¿Cómo cambiaría el diseño de una política de transferencias a municipios si se usa la mediana en lugar del promedio como referencia? ¿Qué comunas ganarían y cuáles perderían recursos?*

---

## 8. Conexión con el módulo `profundiza.ipynb`

| Aspecto | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| Media vs. mediana | Qué hacer y cuándo | Por qué la media "se rompe" (robustez) |
| Desviación estándar | Cómo calcularla | Varianza, CV, asimetría formal |
| Outliers | Se mencionan | Regla del IQR para detección rigurosa |
| Correlación | No se menciona | Correlación ≠ causalidad y Paradoja de Simpson |
| **¿Para quién?** | Todo participante | Quién deba justificar metodología en informes |

---

## 9. Autoevaluación Final

**Pregunta 1.** En un dataset con media = 156.000 y mediana = 72.000, ¿cómo se llama el tipo de distribución?
- A) Distribución simétrica
- B) Distribución sesgada a la izquierda
- C) Distribución sesgada a la derecha ✅
- D) Distribución normal

*Explicación: Cuando la media es mayor que la mediana, hay valores muy altos (outliers o valores extremos) que jalan la media hacia la derecha. La "cola" de la distribución apunta a la derecha.*

---

**Pregunta 2.** ¿Cuál es la medida más apropiada para describir el ingreso típico de los trabajadores de un país?
- A) La media, porque considera todos los valores
- B) La mediana, porque no se distorsiona con los salarios extremos de los más ricos ✅
- C) La moda, porque es el valor más frecuente
- D) El rango, porque muestra toda la variabilidad

*Explicación: Los ingresos son asimétricos: pocos muy ricos elevan la media, mientras la mayoría gana mucho menos. La mediana describe mejor el valor típico.*

---

**Pregunta 3.** ¿Qué representa el IQR (rango intercuartílico)?
- A) La diferencia entre el máximo y el mínimo
- B) El rango donde vive el 50% central de los datos ✅
- C) El promedio de los cuartiles
- D) La desviación estándar de los cuartiles

*Explicación: IQR = Q3 - Q1. Ese intervalo contiene exactamente el 50% central de los datos ordenados, sin verse afectado por los valores extremos.*

---

**Pregunta 4.** Ejecutas `df["poblacion"].describe()` y ves que `std` es mayor que `mean`. ¿Qué significa?
- A) Hay un error en el código
- B) Los datos están muy concentrados alrededor de la media
- C) Los datos son extremadamente heterogéneos; la dispersión supera al valor promedio ✅
- D) La columna tiene NaN

*Explicación: Cuando la desviación estándar supera la media, indica una variabilidad extrema. En este dataset, hay comunas desde ~20.000 hasta ~568.000 habitantes, lo que genera una dispersión mayor que el promedio.*

---

**Pregunta 5.** ¿Qué valor devuelve `df["poblacion"].describe()["50%"]`?
- A) El 50% de la población total
- B) El promedio de la columna
- C) La mediana de la columna ✅
- D) El percentil 50 del índice del DataFrame

*Explicación: En el resultado de `describe()`, la fila `"50%"` es el percentil 50, que es exactamente la mediana — el valor que deja la mitad de los datos por debajo y la mitad por encima.*

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **Media** | Suma de valores dividida por la cantidad | Promedio simple en Excel |
| **Mediana** | Valor del medio cuando los datos están ordenados | El dato que parte la lista en dos mitades iguales |
| **Moda** | Valor que aparece más veces | La respuesta más frecuente en una encuesta |
| **Rango** | Diferencia entre el máximo y el mínimo | Cuánto varían los extremos |
| **Desviación estándar** | Medida de qué tan lejos están los valores de la media | Qué tan disparejos son los datos |
| **Q1 / Percentil 25** | El 25% de los datos está por debajo de este valor | El piso del 50% central |
| **Q3 / Percentil 75** | El 75% de los datos está por debajo de este valor | El techo del 50% central |
| **IQR** | Q3 - Q1: rango del 50% central | El intervalo "típico" sin outliers |
| **Sesgo** | Asimetría de la distribución | Cuando pocos valores extremos jalan el promedio |
| **Outlier** | Valor extremo que se aleja mucho del resto | El dato que "no cuadra" con los demás |
| **`describe()`** | Resumen estadístico automático de pandas | El informe rápido de una columna numérica |
| **Distribución** | Cómo se reparten los valores de una variable | El patrón de cómo se concentran los datos |

---

## 11. Conexión con el siguiente módulo

Ya sabes resumir datos numéricos con rigor: elegir entre media y mediana, medir la dispersión y leer un `describe()` de una mirada. El siguiente paso natural es **ver** esos datos.

El próximo módulo es **R1-07 · Visualización exploratoria**, donde aprenderás a:
- Crear histogramas para ver la distribución de una variable
- Graficar con `matplotlib` y `seaborn` desde pandas
- Leer un boxplot y conectarlo con Q1, mediana y Q3
- Elegir el tipo de gráfico correcto según lo que quieres comunicar

Pregunta motivadora:

> *Sabemos que las comunas de Chile son muy heterogéneas en población — los números lo confirman. Pero ¿cómo se **ve** esa heterogeneidad? ¿Cómo mostrarías en un gráfico que pocas comunas concentran la mayoría de la población?*

Eso es lo que construirás en R1-07. ¡Nos vemos ahí!

---

*Guía elaborada para el Bootcamp de Datos — Formación Pública Chile · Licencia CC BY 4.0*
