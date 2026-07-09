# Guía de Aprendizaje — R1-08 · Visualización para comunicar + ética

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 8 de 10 · Semana 9

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-08 · Visualización para comunicar + ética |
| **Pista** | R1 — Análisis y Visualización |
| **Duración estimada** | 75–90 minutos |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R1-07 · Visualización exploratoria |
| **Competencia de salida** | Comunicar un hallazgo con un gráfico claro y honesto para una audiencia directiva |
| **Dataset** | Compras públicas por región — ChileCompra (`compras_ml.csv`) |
| **Entregable** | 4 celdas de chequeo con ✅ |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Hasta ahora aprendiste a explorar datos para entender. Este módulo es sobre el siguiente paso: **comunicar lo que encontraste a otros**, especialmente a quienes toman decisiones.

En el Estado, los informes, presentaciones y reportes de gestión se basan en gráficos. Un gráfico mal construido puede llevar a conclusiones equivocadas, aunque los datos sean correctos. El engaño visual más común —truncar el eje Y— aparece constantemente en presentaciones de organismos públicos, medios de comunicación y reportes de ministerios.

Aprender a hacer gráficos honestos no es solo una habilidad técnica: es un **compromiso ético con la ciudadanía y con quienes toman decisiones basadas en tu trabajo**.

### Conexión con el dataset

Los datos del módulo muestran el **gasto en compras públicas por región** (ChileCompra). Con ellos practicarás preguntas como: ¿qué regiones concentran más gasto? ¿Cómo presentar esa diferencia sin inflarla ni minimizarla?

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|-----------------|-----------|------------------------|
| `ax.set_ylim(bottom=0)` | Fuerza que el eje Y parta desde cero | Un informe financiero que no oculta la escala real del gasto |
| `ax.set_title(...)` | Agrega título al gráfico | El nombre del cuadro en un informe de gestión |
| `ax.set_xlabel/ylabel(...)` | Etiqueta los ejes | Las columnas rotuladas en una tabla de Excel |
| `ax.annotate(...)` | Señala un dato clave con texto | El resaltado con color amarillo en un documento Word |
| Eje truncado vs. desde 0 | Comparación ética/visual | La diferencia entre un dato real y uno presentado de forma engañosa |

---

## 4. Verificación de Prerrequisitos

Antes de empezar, confirma que puedes hacer lo siguiente:

| ¿Puedo...? | Sí / Revisar |
|-----------|-------------|
| Crear un gráfico de barras con `matplotlib` | Del módulo R1-07 |
| Usar `groupby` + `sum` para agrupar datos | Del módulo R1-03 |
| Cargar un CSV con `pd.read_csv` | Del módulo R1-02 |
| Entender `fig, ax = plt.subplots(...)` | Del módulo R1-07 |

Si alguna respuesta es "revisar", vuelve un momento al módulo correspondiente antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección de Preparación: Cargar los datos

🎯 **Objetivo:** dejar listos los datos que usarás en todos los ejercicios.

💡 **Concepto clave:** el código de preparación agrupa el gasto por región y toma el top 6. Es el mismo patrón de `groupby` + `sort_values` que ya conoces.

🔍 **¿Qué hace el código?**
- `df.groupby("region_comprador")["monto_total"].sum()` → suma el gasto de todas las órdenes por región
- `.sort_values(ascending=False).head(6)` → ordena de mayor a menor y toma solo las 6 primeras
- El resultado se guarda en `g`, que usarás como insumo en los 4 ejercicios

⚠️ **Error frecuente:** modificar `g` en un ejercicio y olvidar que el siguiente la usa fresca. Si algo sale raro, vuelve a ejecutar la celda de preparación.

✅ **Sabes esta sección cuando puedes:** ejecutar la celda y leer correctamente qué región tiene mayor gasto total.

---

### Sección 1: El eje Y empieza en cero

🎯 **Objetivo:** comprender por qué truncar el eje Y es el engaño visual más común y cómo evitarlo.

💡 **Concepto clave — El eje truncado:** cuando el eje Y no parte desde cero, las diferencias entre barras se ven exageradas. Una región que gasta el doble que otra parece gastar diez veces más. Esto ocurre frecuentemente en noticias y presentaciones porque visualmente "resalta" las diferencias, pero distorsiona la realidad.

🔍 **¿Qué hace el código?**
- `ax.bar(g.index, g.values, color="#4240e5")` → dibuja las barras con los datos
- El TODO pide que agregues: `ax.set_ylim(bottom=0)` → fuerza que el eje empiece desde cero
- `plt.xticks(rotation=45, ha="right")` → rota las etiquetas del eje X para que no se superpongan

⚠️ **Error frecuente:** escribir `ax.ylim(0)` en vez de `ax.set_ylim(bottom=0)`. El método correcto es `set_ylim`.

✅ **Sabes esta sección cuando puedes:** explicar a un colega por qué un gráfico con eje truncado puede ser engañoso, aunque los datos sean reales.

---

### Sección 2: Título y etiquetas — que se entienda solo

🎯 **Objetivo:** hacer que un gráfico comunique por sí mismo, sin necesidad de explicación oral.

💡 **Concepto clave — Autonomía del gráfico:** en el trabajo del Estado, un gráfico muchas veces viaja solo: se adjunta a un correo, se pega en un informe, se proyecta en una reunión sin que estés presente. Si no tiene título ni etiquetas, la audiencia no sabe qué está mirando.

🔍 **¿Qué hace el código?**
- `ax.set_title("...")` → el título principal del gráfico; debe responder "¿qué muestra este gráfico?"
- `ax.set_xlabel("...")` → etiqueta del eje horizontal (aquí: las regiones)
- `ax.set_ylabel("...")` → etiqueta del eje vertical (aquí: el monto en pesos)

Un título bien escrito tiene tres elementos: **qué** se mide, **dónde/quiénes**, **cuándo** (si aplica). Ejemplo: *"Gasto en compras públicas por región — Top 6 — 2023"*.

⚠️ **Error frecuente:** poner un título genérico como "Gráfico 1" o dejar la etiqueta del eje Y vacía. La celda de chequeo verifica que los tres elementos existan y no estén vacíos.

✅ **Sabes esta sección cuando puedes:** mostrar el gráfico a un colega que no vio los datos y él entiende de qué trata sin que tengas que explicarle nada.

---

### Sección 3: Anotar el dato clave

🎯 **Objetivo:** guiar la mirada de la audiencia al mensaje central del gráfico.

💡 **Concepto clave — La anotación como argumento:** un gráfico exploratorio te ayuda a ti a descubrir patrones. Un gráfico comunicativo debe destacar el hallazgo principal. `ax.annotate(...)` es la herramienta para poner una flecha o texto que diga "mira aquí".

🔍 **¿Qué hace el código?**
- `g.idxmax()` → devuelve el nombre de la región con mayor gasto (el índice donde está el máximo)
- `ax.annotate("texto", xy=(posición_flecha), xytext=(posición_texto))` → dibuja texto con flecha apuntando a la barra más alta
- La celda de chequeo verifica que `ax.texts` tenga al menos un elemento (es decir, que hayas anotado algo)

Un ejemplo de uso básico:
```python
ax.annotate(
    f"Mayor gasto:\n{g.idxmax()}",
    xy=(0, g.max()),          # donde apunta la flecha (posición x=0 si es la primera barra)
    xytext=(1, g.max() * 0.9) # donde está el texto
)
```

⚠️ **Error frecuente:** confundir `xy` (dónde apunta la flecha) con `xytext` (dónde aparece el texto). Si el texto queda encima de la barra, ajusta `xytext` para moverlo a un lugar visible.

✅ **Sabes esta sección cuando puedes:** agregar una anotación que señale la región con mayor gasto y explica brevemente qué significa ese dato.

---

### Sección 4: Engañoso vs. honesto, lado a lado

🎯 **Objetivo:** ver con tus propios ojos la diferencia ética y visual entre un gráfico con eje truncado y uno honesto.

💡 **Concepto clave — La ética es visual:** este ejercicio no es técnicamente difícil, pero es el más importante del módulo. Ver los dos gráficos juntos hace evidente que el eje truncado distorsiona la percepción de las diferencias, aunque los datos sean idénticos. En el Estado, comunicar con integridad es parte del servicio público.

🔍 **¿Qué hace el código?**
- `fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))` → crea dos gráficos lado a lado
- `ax1` ya está configurado con el eje truncado (`g.min() * 0.98`), que exagera diferencias
- El TODO pide que configures `ax2` con `ax2.set_ylim(bottom=0)` para que sea honesto
- La variable `honesto_desde_cero` guarda si el eje de `ax2` parte desde cero (la celda de chequeo la usa)

⚠️ **Error frecuente:** olvidar asignar `honesto_desde_cero = ax2.get_ylim()[0] == 0`. Esta línea ya está en el código del notebook; solo asegúrate de no borrarla.

✅ **Sabes esta sección cuando puedes:** explicar a alguien la diferencia entre los dos gráficos y por qué el de la derecha es más honesto.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Dibuja barras con el eje desde 0

**Habilidad que entrena:** aplicar la regla fundamental de honestidad en gráficos de barras.

**Pistas progresivas:**
- 🟡 *Pista suave:* ¿qué método de `ax` controla los límites del eje Y?
- 🟠 *Pista media:* el método empieza con `set_` y termina con `lim`. Recibe el argumento `bottom`.
- 🔴 *Pista directa:* la línea que necesitas es `ax.set_ylim(bottom=0)`.

**Lógica de la solución:** `ax.set_ylim(bottom=0)` fija el límite inferior del eje Y en exactamente cero, sin importar cuál sea el valor mínimo de los datos. La celda de chequeo verifica que `ax.get_ylim()[0] == 0`.

---

### Ejercicio 2 — Agrega título y etiquetas

**Habilidad que entrena:** hacer que un gráfico se entienda sin explicación externa.

**Pistas progresivas:**
- 🟡 *Pista suave:* necesitas tres métodos de `ax`, uno para el título y dos para los ejes.
- 🟠 *Pista media:* los métodos son `set_title`, `set_xlabel` y `set_ylabel`. Cada uno recibe un string con el texto.
- 🔴 *Pista directa:* `ax.set_title("Gasto por región")`, `ax.set_xlabel("Región")`, `ax.set_ylabel("Monto total (CLP)")`.

**Lógica de la solución:** la celda de chequeo verifica que `ax.get_title() != ""` y que ambos ejes tengan etiqueta no vacía. Lo que escribas como texto es tuyo, siempre que no esté vacío.

---

### Ejercicio 3 — Anota la región de mayor gasto

**Habilidad que entrena:** guiar la mirada de la audiencia al hallazgo principal.

**Pistas progresivas:**
- 🟡 *Pista suave:* ¿cómo sabes cuál es la región de mayor gasto? El objeto `g` ya está ordenado.
- 🟠 *Pista media:* usa `g.idxmax()` para obtener el nombre de la región y `g.max()` para su valor. El método de anotación es `ax.annotate(...)`.
- 🔴 *Pista directa:* `ax.annotate(g.idxmax(), xy=(0, g.max()), xytext=(2, g.max() * 0.85))` — ajusta las coordenadas según cómo se vea.

**Lógica de la solución:** `ax.annotate` agrega un texto al gráfico y opcionalmente una flecha. La celda de chequeo verifica que `len(ax.texts) > 0`, es decir, que exista al menos un texto añadido manualmente.

---

### Ejercicio 4 — Construye las dos versiones (engañosa vs. honesta)

**Habilidad que entrena:** reconocer la diferencia ética entre gráficos con eje truncado y gráficos honestos.

**Pistas progresivas:**
- 🟡 *Pista suave:* el gráfico engañoso (`ax1`) ya está hecho. ¿Qué le falta a `ax2`?
- 🟠 *Pista media:* `ax2` necesita que su eje Y parta desde cero. Revisa el Ejercicio 1.
- 🔴 *Pista directa:* agrega `ax2.set_ylim(bottom=0)` en el espacio del TODO.

**Lógica de la solución:** la celda de chequeo verifica dos condiciones simultáneas: `honesto_desde_cero` (que `ax2` parte en 0) y `ax1.get_ylim()[0] > 0` (que `ax1` efectivamente está truncado). Ambas deben cumplirse para el ✅.

---

## 7. El Ejercicio 4 en Profundidad: Ética Visual en el Estado

El ejercicio 4 es el más importante del módulo porque toca un tema que va más allá del código: **la responsabilidad ética de quien comunica datos públicos**.

### ¿Por qué importa el eje desde cero en el sector público?

Imagina un informe de gestión que muestra el gasto de dos ministerios. Con eje truncado, la diferencia parece enorme. Con eje desde cero, es moderada. La decisión presupuestaria que tome un directivo basándose en ese gráfico puede ser completamente distinta.

### Reflexión guiada

Observa los dos gráficos que generaste:

- **¿Cuántas veces más grande parece la región de mayor gasto en el gráfico truncado comparado con el honesto?**
- **Si fueras un jefe de servicio viendo solo el gráfico de la izquierda, ¿qué decisión podrías tomar que sería diferente si vieras el de la derecha?**
- **¿En qué situaciones podría alguien truncar el eje "sin querer"?** (respuesta: muchas herramientas, incluyendo Excel, ajustan automáticamente el eje al rango de los datos)

### Pregunta de debate

> ¿Qué otros tipos de engaño visual conoces además del eje truncado? ¿Cómo los detectarías en un informe que recibes?

Pistas para explorar: gráficos de torta con más de 6 categorías, escalas logarítmicas sin aviso, tamaño de burbujas no proporcional al valor, colores que exageran contrastes.

---

## 8. Conexión con el Notebook `profundiza.ipynb`

| Aspecto | `leccion.ipynb` (nivel práctico) | `profundiza.ipynb` (nivel teórico) |
|---------|----------------------------------|-------------------------------------|
| Enfoque | Ejercicios guiados con chequeo automático | Exploración libre con más herramientas |
| Anotaciones | `ax.annotate` básico | Flechas con estilo, cajas de texto |
| Ética visual | Eje truncado vs. desde cero | Catálogo extendido de engaños visuales |
| Audiencias | Directivos y pares del servicio | Ciudadanía, medios, rendición de cuentas |
| Tiempo estimado | 75–90 min | 45–60 min adicionales |

**¿Cuándo ir al profundiza?** Cuando ya completaste los 4 ✅ y quieres aprender a hacer gráficos más pulidos para presentaciones formales, o cuando necesitas argumentar sobre ética de datos en una reunión.

---

## 9. Autoevaluación Final

**1. ¿Por qué un gráfico de barras debe tener el eje Y desde cero?**

- a) Porque matplotlib lo requiere por defecto
- b) Porque truncar el eje exagera las diferencias y puede llevar a decisiones incorrectas ✅
- c) Porque facilita el cálculo automático de porcentajes
- d) Porque mejora el rendimiento del código

*Explicación:* el truncamiento distorsiona la percepción visual. Las barras parecen más o menos diferentes de lo que los datos realmente muestran. Es un problema ético, no solo estético.

---

**2. ¿Qué método de matplotlib se usa para forzar que el eje Y parta desde cero?**

- a) `ax.ylim(0)`
- b) `ax.set_axis(0)`
- c) `ax.set_ylim(bottom=0)` ✅
- d) `ax.zero_y(True)`

*Explicación:* `set_ylim(bottom=0)` es el método estándar. El argumento `bottom` fija el límite inferior; `top` fijaría el superior.

---

**3. ¿Qué hace `ax.annotate("texto", xy=(...), xytext=(...))`?**

- a) Cambia el color de una barra específica
- b) Agrega una etiqueta al eje X
- c) Escribe texto con una flecha apuntando a una posición del gráfico ✅
- d) Guarda el gráfico como imagen

*Explicación:* `xy` es donde apunta la flecha (el dato), `xytext` es donde se muestra el texto. Si se omite `xytext`, el texto queda encima del punto `xy`.

---

**4. Un colega te manda un gráfico de barras donde la región A parece tener el doble de gasto que la región B. ¿Qué verificas primero?**

- a) El tipo de gráfico usado
- b) El color de las barras
- c) Si el eje Y parte desde cero o está truncado ✅
- d) El tamaño del archivo CSV

*Explicación:* el primer control de calidad en cualquier gráfico de barras es revisar el origen del eje Y. Si no parte desde cero, la proporción visual no refleja la proporción real de los datos.

---

**5. ¿Cuál de las siguientes afirmaciones sobre ética en visualización es correcta?**

- a) Solo importa la honestidad si el gráfico se publica en medios
- b) El truncamiento del eje solo afecta gráficos de más de 10 barras
- c) Comunicar con integridad visual es parte de la responsabilidad del funcionario público ✅
- d) Matplotlib trunca automáticamente todos los ejes para mejorar la visualización

*Explicación:* en el Estado, los gráficos apoyan decisiones de política pública, asignación de recursos y rendición de cuentas. Un gráfico engañoso —aunque sea por descuido— puede derivar en decisiones incorrectas con impacto real en la ciudadanía.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente en sector público |
|---------|------------------|------------------------------|
| **Eje Y** | El eje vertical de un gráfico | La escala de valores en una tabla de Excel |
| **Eje truncado** | Eje que no parte desde cero, exagerando diferencias | Un indicador de gestión mostrado solo en el rango "bueno" |
| **`set_ylim(bottom=0)`** | Fija el límite inferior del eje Y en cero | Pedir que el informe muestre la escala completa |
| **`set_title`** | Agrega un título al gráfico | El encabezado de un cuadro en un informe de gestión |
| **`set_xlabel` / `set_ylabel`** | Etiqueta los ejes horizontal y vertical | Los encabezados de columnas y filas en una tabla |
| **`annotate`** | Agrega texto o flecha señalando un punto del gráfico | El comentario escrito a mano en un gráfico impreso |
| **`g.idxmax()`** | Devuelve el índice del valor máximo de una Serie | "La región con el mayor presupuesto ejecutado" |
| **`g.max()`** | Devuelve el valor máximo de una Serie | El valor de la celda más alta en una columna de Excel |
| **`ax.texts`** | Lista de los textos anotados manualmente en el gráfico | Los comentarios y notas de un documento Word |
| **`plt.subplots(1, 2)`** | Crea dos gráficos lado a lado | Dos tablas comparativas en la misma hoja de Excel |
| **Ética visual** | Compromiso de representar datos sin distorsión intencional ni accidental | Integridad en la elaboración de informes públicos |
| **Audiencia directiva** | Personas que toman decisiones basadas en el gráfico | Jefe de servicio, directivos DIPRES, comité de gestión |

---

## 11. Conexión con el Módulo Siguiente

### Lo que viene: R1-09 · Dashboards ligeros con Gradio

En R1-08 aprendiste a hacer **un gráfico honesto y comunicativo**. En R1-09 vas a dar el siguiente salto: construir un **tablero interactivo** donde el usuario puede filtrar los datos y ver los gráficos actualizarse en tiempo real.

Usarás todo lo que aprendiste hasta aquí:
- `filtrar` datos con pandas (de R1-02 y R1-04)
- Calcular KPIs y agrupar (de R1-03 y R1-06)
- Hacer gráficos comunicativos (de R1-07 y R1-08)
- Envolver todo en una interfaz con Gradio

### Pregunta motivadora

> Tienes todos los ingredientes. ¿Puedes imaginar un tablero donde un directivo de tu servicio pueda filtrar el gasto por región y por categoría con un solo clic, sin saber nada de Python? Eso es exactamente lo que vas a construir.
