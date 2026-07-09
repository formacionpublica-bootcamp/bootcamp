# 📘 Guía de Aprendizaje — R2-10 · Series temporales

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-10 · Series temporales (pronóstico) |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Carácter** | ⭐ **OPTATIVO** — no es requisito para el capstone, pero es una de las habilidades más pedidas en el Estado |
| **Duración estimada** | 2–3 horas (+1 hora si haces el `profundiza.ipynb` opcional) |
| **Nivel** | Intermedio–avanzado |
| **Prerrequisitos** | Núcleo de la rama R2 completo (hasta R2-09). Se da por sabido `pandas`, `numpy` y `matplotlib` |
| **Competencia de salida** | Dado un registro temporal real del Estado, producir un pronóstico defendible y justificar por qué es confiable |
| **Dataset** | `gasto_anual.csv` — gasto anual del Estado en compras públicas (2019–2025 + 2026 parcial), ChileCompra / MercadoPúblico |
| **Entregable** | Las 4 celdas de chequeo del notebook mostrando ✅ |

> **¿Por qué optativo?** La rama R2 se completa con el capstone (R2-CAP) usando lo aprendido hasta R2-09. Este módulo abre una puerta extra: datos donde **el orden en el tiempo importa**. Si en tu servicio te piden proyecciones —de gasto, demanda, atenciones, solicitudes— este módulo es para ti.

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Hay una pregunta que tarde o temprano llega a todo equipo del Estado: **"¿y cuánto va a ser el próximo año?"**. Cuánto gasto proyectamos para el presupuesto exploratorio, cuántas atenciones esperamos en el CESFAM, cuántas solicitudes de transparencia llegarán el próximo semestre. Hasta ahora, en el bootcamp, cada fila de datos era independiente: una orden de compra no "sabía nada" de la anterior. En este módulo cambia todo: trabajas con datos **ordenados en el tiempo**, donde el pasado dice algo sobre el futuro.

Y trabajas con datos de verdad: el **gasto público de Chile en compras**, año a año, desde 2019 (unos $8,14 billones de pesos) hasta 2025 (más de $18,43 billones). En siete años el gasto **más que se duplicó**, y tú vas a medir exactamente cómo y a proyectar el 2026.

**Lo concreto que aprenderás:**
- Qué es una **serie temporal** y sus tres componentes: tendencia, estacionalidad y ruido.
- Cargar una serie real, graficarla y describir su tendencia **con números** (crecimiento año a año).
- Construir tres pronósticos base: **ingenuo**, **crecimiento medio** y **tendencia lineal**.
- **Validar** un pronóstico de forma honesta (hold-out / backtest) y elegir el mejor método.

**Lo más valioso no es el pronóstico, es la defensa.** Cualquiera puede decir "el próximo año el gasto será X". La diferencia entre una opinión y un análisis es poder responder: *"probé tres métodos, los validé escondiendo el último año conocido, y este fue el que menos se equivocó"*. Eso es lo que este módulo te enseña a decir — y a demostrar.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía en el sector público / Excel |
|---|---|---|
| **Serie temporal** | Valores ordenados en el tiempo a intervalos regulares | La planilla de ejecución presupuestaria: una fila por período, y el orden importa |
| **Tendencia** | Dirección de largo plazo: sube, baja o se aplana | "El gasto en compras viene subiendo hace años" — la dirección general del indicador |
| **Estacionalidad** | Patrones que se repiten en ciclos fijos | Diciembre dispara el gasto (cierre presupuestario), enero lo desploma. **Ojo:** solo se ve con datos mensuales; aquí trabajamos datos anuales |
| **Ruido** | Fluctuaciones que no explica ni la tendencia ni la estacionalidad | El "año raro": una emergencia, una licitación gigante puntual |
| **Año parcial** | Período aún en curso, no comparable con años cerrados | Comparar el gasto acumulado a marzo con un año completo: media película |
| **`pct_change()`** | Variación porcentual respecto del período anterior | La columna "% variación vs año anterior" de todo informe de ejecución |
| **Pronóstico ingenuo** | "El próximo año será igual al último" | Repetir el presupuesto del año pasado tal cual. La vara mínima a vencer |
| **Crecimiento medio** | Proyectar con el promedio histórico de crecimiento | "Venimos creciendo ~14% al año, proyectemos eso" |
| **Tendencia lineal** | Ajustar una recta a los puntos y extenderla | Trazar la línea de tendencia en un gráfico de Excel y estirarla un año |
| **Hold-out / backtest** | Esconder el último dato, pronosticar sin verlo, y recién ahí comparar | Ponerse a prueba con el año pasado antes de prometer el próximo |
| **Error absoluto** | Distancia (sin signo) entre pronóstico y realidad | "Nos equivocamos por $600 mil millones" — el tamaño del error, sin importar la dirección |

---

## 4. Antes de Empezar: Verificación de Prerrequisitos

Este módulo asume el núcleo de la rama R2 completo. Responde honestamente:

| ¿Puedo...? | Estado |
|---|---|
| Cargar un CSV con `pd.read_csv()` | ✅ Sí / 🔄 Revisar R2-00 |
| Filtrar filas de un DataFrame con una condición booleana | ✅ Sí / 🔄 Revisar R2-01 |
| Usar `.set_index()` y `.loc[]` para acceder por etiqueta | ✅ Sí / 🔄 Revisar R2-01 |
| Distinguir una **Serie** de un **DataFrame** de pandas | ✅ Sí / 🔄 Revisar R2-01 |
| Graficar con `.plot()` de pandas / matplotlib | ✅ Sí / 🔄 Revisar R1-07 o R2-02 |
| Explicar por qué se separa train y test (evaluación honesta) | ✅ Sí / 🔄 Revisar R2-07 |
| Usar diccionarios de Python (`{clave: valor}`) | ✅ Sí / 🔄 Revisar R2-00 |

Si tienes más de dos "Revisar", refuerza primero R2-01 (pandas) y R2-07 (evaluación honesta): son la base conceptual directa de este módulo.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 1: ¿Qué es una serie temporal?

🎯 **Objetivo:** entender qué hace especial a una serie temporal y conocer sus tres componentes.

💡 **Concepto clave — el orden es la información:**
Si te doy las edades de 50 funcionarios, da igual el orden: la media es la misma. Pero si te doy el gasto del Estado de 2019 a 2025 **desordenado**, perdiste lo más valioso: si venía subiendo, si hubo un salto en pandemia, hacia dónde apunta. Toda serie se puede pensar como suma de **tendencia** (dirección de largo plazo), **estacionalidad** (ciclos que se repiten) y **ruido** (lo demás).

🔍 **Qué dice el notebook:** es una sección de teoría, sin código. Presenta las tres piezas con ejemplos de compras públicas (diciembre dispara el gasto por cierre de presupuesto; enero lo desploma).

⚠️ **Error frecuente:** buscar estacionalidad en datos anuales. Con una fila por año, los ciclos mensuales quedan "promediados hacia adentro" y **no se pueden observar**. El notebook lo dice con todas sus letras: en este módulo se trabaja la tendencia, no la estacionalidad.

✅ **Señal de comprensión:** puedes explicar con tus palabras por qué desordenar una serie temporal destruye información, y por qué aquí no veremos estacionalidad.

---

### 🔷 Sección 2: Preparación

🎯 **Objetivo:** cargar librerías y configurar la visualización de montos grandes.

💡 **Concepto clave — nada nuevo que instalar:** el módulo usa solo `pandas`, `numpy` y `matplotlib`, las herramientas de siempre. Lo nuevo es la *forma de pensar*.

🔍 **Qué hace el código:**
- Importa las tres librerías.
- `pd.set_option("display.float_format", ...)` formatea los números con separador de miles. Con montos de billones de pesos, sin esto verías notación científica (`1.84e+13`) — ilegible para un informe.

⚠️ **Error frecuente:** saltarse esta celda. Si más adelante ves números como `8.14e+12`, probablemente no la ejecutaste.

✅ **Señal de comprensión:** aparece "Librerías listas ✔".

---

### 🔷 Sección 3: Los datos — gasto público de Chile, año a año

🎯 **Objetivo:** cargar `gasto_anual.csv` y entender su estructura, en especial la marca de año parcial.

💡 **Concepto clave — el año a medias:**
El dataset tiene 8 filas (2019 a 2026) con columnas `anio`, `gasto_clp`, `ordenes` y `parcial`. El **2026 está incompleto** (año en curso al momento de tomar el dato: $6,19 billones acumulados) y viene marcado con `parcial = True`. Es como comparar la ejecución presupuestaria a mitad de año con un año cerrado: no se puede, y el dataset te lo advierte con una columna.

🔍 **Qué hace el código:**
- Si `gasto_anual.csv` no existe localmente (por ejemplo en Colab), intenta descargarlo automáticamente desde GitHub.
- `pd.read_csv("gasto_anual.csv")` carga la tabla.
- La convierte a la lista de diccionarios `DATOS` (para las celdas de chequeo) y arma el DataFrame `df` que usarás en todo el cuaderno.

⚠️ **Error frecuente:** en Colab, si la descarga automática falla, verás un aviso: sube el archivo manualmente antes de continuar. Sin `df`, ningún ejercicio funciona.

✅ **Señal de comprensión:** al mostrar `df` ves 8 filas, y puedes señalar cuál es el año parcial y por qué habrá que excluirlo.

---

### 🔷 Ejercicios 1 a 4 (el corazón del módulo)

Las secciones restantes del notebook **son los cuatro ejercicios**, que se construyen uno sobre otro: primero armas la serie, luego mides su crecimiento, después pronosticas con tres métodos, y al final validas y proyectas el 2026. La guía detallada de cada uno está en la sección siguiente.

---

### 🔷 Sección de cierre: Lo que te llevas

🎯 **Objetivo:** consolidar las cuatro ideas del módulo y llevarlas al trabajo.

💡 **Concepto clave — el método es transferible:** la próxima vez que te pidan "una proyección" de cualquier indicador que avance en el tiempo, ya tienes la receta: grafica, mide el crecimiento, prueba varios pronósticos simples y valida escondiendo el último período.

✅ **Señal de comprensión:** puedes recitar la regla de oro sin mirar: *sin validación, un pronóstico es solo una opinión con decimales*.

---

### 🔬 Extra opcional: `profundiza.ipynb`

Si terminaste la lección y te quedaste con ganas de entender el **porqué** y no solo el **cómo**, el módulo incluye un segundo notebook: `profundiza.ipynb`. Va un nivel más hondo en teoría:

- Por qué la **validación es temporal**: sin barajar los datos, sin "fuga del futuro" hacia el entrenamiento.
- **Tendencia / estacionalidad / ruido** en profundidad, y qué es la **estacionariedad**.
- Los **baselines ingenuos** y el **backtesting walk-forward** (validar en varias ventanas, no solo una).
- Por qué la **incertidumbre crece con el horizonte**: pronosticar a 1 año es una cosa; a 5 años, otra muy distinta.

Trae 4 ejercicios conceptuales auto-corregidos. Es 100% opcional dentro de un módulo que ya es optativo — pero si en tu servicio las proyecciones son pan de cada día, vale la pena la hora extra.

---

## 6. Guía de los Ejercicios

### ✍️ Ejercicio 1 — Construir y graficar la serie

**Objetivo:** transformar la tabla `df` en una Serie de pandas llamada `gasto`, indexada por año, solo con años completos, y graficarla.

**Habilidad que entrena:** preparar una serie temporal para el análisis (filtrar períodos parciales + poner el tiempo como índice).

**Pistas progresivas:**
1. 🟢 *Pista suave:* son dos pasos encadenados: primero filtrar las filas donde `parcial` es `False`, después quedarte con una sola columna indexada por el año. El resultado debe ser una **Serie**, no un DataFrame.
2. 🟡 *Pista media:* para filtrar ya conoces el patrón `df[df["columna"] == valor]`. Para indexar por año, pandas tiene un método que convierte una columna en índice; después seleccionas `"gasto_clp"` con corchetes simples.
3. 🔴 *Pista directa:* el propio notebook te la regala: filtra con `df[df["parcial"] == False]` y luego encadena `.set_index("anio")["gasto_clp"]`.

**Lógica de la solución en prosa:** de las 8 filas del dataset, descartas la del 2026 (parcial) y te quedas con las 7 de años cerrados. Al poner `anio` como índice y seleccionar `gasto_clp`, obtienes una Serie donde `gasto.loc[2025]` devuelve directamente el gasto de ese año. Graficada con `marker="o"`, verás una curva que sube de $8,14 billones (2019) a $18,43 billones (2025).

**Qué valida el chequeo ✅:** que `gasto` sea una Serie de pandas, que su índice sean exactamente los 7 años completos (2019–2025, sin el 2026 parcial) y que los valores coincidan con `gasto_clp`. Si pasa, imprime el gasto de 2019 y 2025.

---

### ✍️ Ejercicio 2 — Medir la tendencia: crecimiento año a año

**Objetivo:** calcular `crecimiento`, la tasa de variación porcentual de cada año respecto del anterior.

**Habilidad que entrena:** pasar de "la línea sube" (cualitativo) a "creció 25,0% en 2024" (cuantitativo).

**Pistas progresivas:**
1. 🟢 *Pista suave:* pandas tiene un método que calcula la variación relativa fila a fila en una sola llamada. No necesitas ningún bucle.
2. 🟡 *Pista media:* el método es `pct_change()`, pero devuelve **fracciones** (0.10 = 10%). El chequeo espera porcentajes: falta una multiplicación.
3. 🔴 *Pista directa:* la fórmula completa está en el enunciado del notebook — es una sola línea que aplica `pct_change()` sobre `gasto` y multiplica por 100.

**Lógica de la solución en prosa:** cada valor se divide por el del año anterior y se le resta 1; multiplicado por 100 es el crecimiento porcentual. El 2019 queda en `NaN` (no tiene año previo — es normal, no un error). Verás años "de crucero" en torno al 9–10% (2020 y 2021: 9,9%), un 16,9% en 2022, un 8,6% en 2023, y el salto fuerte: **25,0% en 2024** y 18,1% en 2025.

**Qué valida el chequeo ✅:** que `crecimiento` sea una Serie y que los porcentajes (ignorando el `NaN` inicial) coincidan con los reales. Si pasa, imprime el crecimiento de 2024 y 2025.

---

### ✍️ Ejercicio 3 — Tres pronósticos base (backtest sobre 2025)

**Objetivo:** esconder el 2025, entrenar solo con 2019–2024 y pronosticar el 2025 con tres métodos: ingenuo, crecimiento medio y tendencia lineal.

**Habilidad que entrena:** la idea más importante del módulo — **nunca evalúes un pronóstico con los datos que usaste para construirlo**. Es el mismo principio del train/test de R2-07, aplicado al tiempo.

**Pistas progresivas:**
1. 🟢 *Pista suave:* primero construye `train` recortando la serie a 2019–2024 (`.loc` acepta rangos de índice). Los tres pronósticos usan **solo** `train` — si el 2025 se cuela, el ejercicio pierde el sentido.
2. 🟡 *Pista media:* el ingenuo es simplemente el último valor conocido (el de 2024). El de crecimiento medio toma ese mismo valor y lo multiplica por `(1 + promedio de pct_change() de train)`. Para la recta, `numpy` tiene un par de funciones: una ajusta el polinomio de grado 1, la otra lo evalúa en un punto.
3. 🔴 *Pista directa:* las funciones son `np.polyfit(train.index, train.values, 1)` (devuelve los coeficientes de la recta) y `np.polyval(coef, 2025)` (la evalúa en 2025). El crecimiento medio de train es `train.pct_change().mean()`.

**Lógica de la solución en prosa:** el **ingenuo** repite el 2024 ($15,60 billones) — parece tonto, pero es la vara mínima que todo método debe superar. El **crecimiento medio** proyecta el promedio histórico de train (~14,1% anual) sobre el 2024 y llega a unos $17,79 billones. La **tendencia lineal** ajusta una recta a los seis puntos y la extiende a 2025: unos $16,04 billones (queda corta porque la recta no captura la aceleración de los últimos años). Los tres van al diccionario `pronosticos_2025`.

**Qué valida el chequeo ✅:** que las tres claves del diccionario existan y que cada valor coincida con la fórmula esperada (entrenada solo con 2019–2024). Si pasa, imprime los tres pronósticos en CLP.

---

### ✍️ Ejercicio 4 — Evaluar, elegir el mejor y pronosticar 2026

**Objetivo:** destapar el 2025 real, medir el error absoluto de cada método, coronar al ganador y usarlo para pronosticar el 2026.

**Habilidad que entrena:** cerrar el ciclo completo de un pronóstico defendible: validar → elegir → proyectar.

**Pistas progresivas:**
1. 🟢 *Pista suave:* son cuatro pasos y cada uno es corto: el 2025 real ya está en la serie (`gasto.loc[2025]`); los errores son "distancia sin signo" entre cada pronóstico y ese valor; el mejor es el de menor error; y el pronóstico 2026 aplica el método ganador sobre **toda** la serie.
2. 🟡 *Pista media:* para los errores, recorre `pronosticos_2025.items()` en una comprensión de diccionario aplicando `abs()`. Para encontrar la clave del mínimo, `min()` acepta un argumento `key`.
3. 🔴 *Pista directa:* `min(errores, key=errores.get)` te da la clave del menor error. El pronóstico 2026 con crecimiento medio es `gasto.loc[2025] * (1 + gasto.pct_change().mean())` — ahora con la serie completa 2019–2025.

**Lógica de la solución en prosa:** el 2025 real fue $18,43 billones. El ingenuo se equivocó por ~$2,83 billones y la recta por ~$2,39 billones; el **crecimiento medio** se equivocó por apenas ~$0,64 billones y gana el backtest. Con ese método validado, y ahora usando toda la serie (crecimiento medio 2019–2025: ~14,7% anual), el pronóstico para 2026 queda en torno a **$21,15 billones de pesos**.

**Qué valida el chequeo ✅:** que los tres errores absolutos coincidan, que `mejor_metodo` sea el de menor error (`crecimiento_medio`) y que `pronostico_2026` use el crecimiento medio sobre toda la serie 2019–2025.

⚠️ **Tentación a evitar (el notebook insiste, y con razón):** NO compares tu pronóstico 2026 con el dato parcial de 2026 ($6,19 billones acumulados). Ese número es un año a medias; compararlo con tu proyección de año completo te haría creer que erraste por un factor de 3, cuando en realidad estás mirando media película.

---

## 7. Sección Especial: El Ejercicio de Política Pública

**Reflexión guiada:** tu análisis muestra que el gasto del Estado en compras públicas pasó de $8,14 billones en 2019 a $18,43 billones en 2025 — más que el doble en pesos corrientes — con un salto de 25,0% solo en 2024, y proyecta ~$21,15 billones para 2026. Pero antes de poner ese número en un informe, conviene hacerse las preguntas que haría un buen jefe de servicio (o la DIPRES):

- **¿Crecimiento real o inflación?** Los montos están en pesos **corrientes**. Parte del alza es inflación acumulada, no más bienes y servicios comprados. Un análisis serio deflactaría la serie (con IPC o UF) antes de hablar de "duplicación del gasto".
- **¿Más gasto = más compras?** La columna `ordenes` cuenta otra historia: en 2019 se emitieron 2.273.449 órdenes de compra y en 2025 fueron 1.867.076 — **menos órdenes que hace seis años, pero por mucho más plata**. El monto promedio por orden creció fuertemente. ¿Consolidación de compras (¿eficiencia?), contratos más grandes (¿concentración en pocos proveedores?), o cambio en la mezcla de lo que se compra?
- **¿El pronóstico es un compromiso?** Un pronóstico de $21,15 billones para 2026 no es una promesa: es "si la tendencia 2019–2025 continúa". Un cambio de gobierno, una ley de presupuestos restrictiva o una crisis pueden quebrar la tendencia — y ningún método basado solo en el pasado lo anticipará.

**Pregunta de debate abierta:** si fueras analista de la Dirección de Presupuestos y este pronóstico llegara a tu escritorio, ¿lo usarías para planificar? ¿Qué le exigirías al autor antes de confiar en él: más años de historia, la serie deflactada, un rango de incertidumbre en vez de un número único?

**Otros datos que complementarían el análisis:**
- La serie **mensual** de gasto, para ver la estacionalidad (¿diciembre realmente dispara el gasto?).
- El **IPC** o la UF, para pasar de pesos corrientes a reales.
- El desglose por **rubro y organismo comprador**: ¿qué explica el salto de 2024?
- El número de **proveedores adjudicados** por año, para evaluar concentración del mercado.

---

## 8. Autoevaluación Final

**Pregunta 1:** ¿Qué distingue a una serie temporal de una tabla común de datos?

- a) Que tiene más filas
- b) Que solo contiene números
- c) **Que los valores están ordenados en el tiempo, y ese orden es información ✅**
- d) Que no se puede graficar

**Explicación:** en una tabla común (edades de funcionarios, órdenes de compra), el orden de las filas da igual. En una serie temporal, desordenar las filas destruye lo más valioso: la tendencia, los ciclos, la dirección.

---

**Pregunta 2:** ¿Por qué el notebook excluye el año 2026 antes de construir la serie?

- a) Porque tiene errores de digitación
- b) **Porque es un año parcial (en curso) y no es comparable con años cerrados ✅**
- c) Porque pandas no acepta más de 7 filas
- d) Porque el 2026 no tiene órdenes de compra

**Explicación:** el 2026 registra solo el gasto acumulado hasta la fecha de corte ($6,19 billones). Incluirlo haría que la tendencia "parezca caer de golpe" al final del gráfico y distorsionaría cualquier cálculo de crecimiento.

---

**Pregunta 3:** ¿Para qué sirve el pronóstico ingenuo ("el próximo año será igual al último")?

- a) Es el método más preciso que existe
- b) **Es la vara mínima: si un método elaborado no le gana, ese método no sirve ✅**
- c) Solo sirve para series mensuales
- d) Es obligatorio por normativa de la DIPRES

**Explicación:** el ingenuo es deliberadamente simple. Su rol es de línea base: cualquier método más sofisticado debe demostrar que le gana en el backtest. En este módulo, el crecimiento medio lo venció con claridad (~$0,64 billones de error contra ~$2,83 billones).

---

**Pregunta 4:** ¿En qué consiste la validación hold-out (backtest) de un pronóstico?

- a) En pedirle a un colega que revise el código
- b) En comparar el pronóstico con el promedio de la serie
- c) En ejecutar el pronóstico dos veces y ver si da lo mismo
- d) **En esconder el último dato real, pronosticarlo sin verlo, y recién después compararlo ✅**

**Explicación:** es el mismo principio del train/test de R2-07 llevado al tiempo: nunca evaluar con datos que el método ya vio. Aquí se escondió el 2025, se entrenó con 2019–2024, y solo al final se "destapó" el valor real para medir el error de cada método.

---

**Pregunta 5:** El crecimiento medio ganó el backtest y con él proyectaste ~$21,15 billones para 2026. ¿Qué afirmación es la más honesta para tu informe?

- a) "El gasto 2026 será de $21,15 billones"
- b) "El pronóstico está mal, porque el dato de 2026 dice $6,19 billones"
- c) **"Si la tendencia 2019–2025 continúa, el gasto 2026 cerraría en torno a $21 billones; el método fue validado contra el 2025 real" ✅**
- d) "No se puede pronosticar el gasto público"

**Explicación:** un pronóstico es condicional, no una promesa: supone que el patrón histórico se mantiene. Y la opción b) cae en la trampa del año parcial: los $6,19 billones del 2026 son un acumulado a medio camino, no un año cerrado — no son comparables.

---

## 9. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en sector público / Excel |
|---|---|---|
| **Serie temporal** | Secuencia de valores ordenados en el tiempo a intervalos regulares | Planilla de ejecución mensual/anual: una fila por período |
| **Tendencia (trend)** | Dirección de largo plazo de la serie: sube, baja o se aplana | "El gasto viene subiendo hace años" |
| **Estacionalidad (seasonality)** | Patrones que se repiten en ciclos fijos (meses, trimestres) | El peak de gasto de diciembre por cierre presupuestario |
| **Ruido (noise)** | Fluctuaciones que no explica ni la tendencia ni la estacionalidad | El año atípico por una emergencia o compra extraordinaria |
| **Año parcial** | Período aún en curso, con datos incompletos | Ejecución acumulada a mitad de año: no comparable con años cerrados |
| **`pct_change()`** | Método de pandas: variación relativa de cada valor respecto del anterior | Columna "% variación año anterior" hecha con fórmula en Excel |
| **Pronóstico ingenuo (naïve)** | Proyectar que el próximo período será igual al último | Repetir el presupuesto del año pasado tal cual |
| **Crecimiento medio** | Proyectar aplicando el promedio histórico de crecimiento | "Crecemos ~14% al año, proyectemos 14%" |
| **Tendencia lineal** | Ajustar una recta a los datos y extenderla al futuro | La línea de tendencia de un gráfico de Excel, estirada |
| **Hold-out / backtest** | Validar escondiendo el último dato y pronosticándolo "a ciegas" | Ponerse a prueba con el año pasado antes de prometer el próximo |
| **Error absoluto** | Distancia sin signo entre pronóstico y valor real | "Erramos por $600 mil millones", da igual si por arriba o por abajo |
| **`np.polyfit` / `np.polyval`** | Funciones de numpy: ajustar una recta y evaluarla en un punto | Calcular la ecuación de la línea de tendencia y leerla en 2026 |

---

## 10. Conexión con el Módulo Siguiente

**Módulo siguiente:** R2-CAP · Capstone

Este era el último módulo optativo de la rama. Lo que viene ahora es distinto a todo lo anterior: en el **capstone** no hay TODOs que rellenar ni celdas de chequeo que te digan ✅. Eres tú, un dataset real del Estado, y el ciclo completo que aprendiste en la rama R2: pregunta → datos → features → modelo → evaluación honesta → entrega con documentación (incluida la model card de R2-09).

Todo lo que practicaste aquí te acompaña al capstone: la disciplina de validar antes de afirmar, la humildad de partir por la línea base más simple, y la honestidad de reportar el error junto con el resultado. Si tu proyecto de capstone incluye datos con dimensión temporal —y en el Estado casi todos la tienen— este módulo te dio la caja de herramientas para tratarlos como corresponde.

**Pregunta motivadora:** de todos los datos que pasan por tu escritorio en el servicio — gasto, atenciones, solicitudes, licencias, reclamos — ¿cuál elegirías para tu capstone, y qué pregunta le harías que hoy nadie en tu institución puede responder con evidencia?

---

*Formación Pública Chile · Licencia CC BY 4.0*
