# Guía de Aprendizaje — R2-10 · Series temporales

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 10 (optativo) · Semana 16

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-10 · Series temporales |
| **Rama** | R2 — Científico de Datos (optativo) |
| **Duración estimada** | 120 minutos (lección) + 45 minutos (profundización opcional) |
| **Nivel** | Intermedio — requiere R2-04 y R2-07 |
| **Prerrequisitos** | pandas con fechas (`parse_dates`, `.dt`), `groupby`, MAE, idea de validación con datos no vistos |
| **Competencia de salida** | Dado un registro temporal real, describir su forma (tendencia, estacionalidad, ruido) y producir un pronóstico validado temporalmente, comparado con líneas base y comunicado con honestidad |
| **Entregable** | Las 7 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 diario, estación Cerro Navia, SINCA 2020–2025) y `aire_nuevos.csv` (enero–septiembre 2026). Profundización: `sismos.csv` (USGS, M≥4,5, Chile 2020–2025) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Casi toda pregunta de planificación mira hacia adelante y casi todo registro del Estado tiene fecha: solicitudes por semana, atenciones por mes, consultas de urgencia por día, PM2.5 por día. Cuando alguien pide «una proyección», lo que de verdad necesita saber es **cuánto confiar** en ella.

Este módulo trabaja con un caso donde el calendario manda: el PM2.5 de Cerro Navia, en Santiago. En julio promedia **57 µg/m³** y en noviembre **12** — el invierno multiplica casi por cinco la contaminación. Aprenderás a ver eso con números, a separar la tendencia de fondo del ciclo anual, y a pronosticar con la regla de oro: **esconder el final y ver si acertabas**. Y luego viene la parte que pocos cursos muestran: enfrentar tu método a lo que **de verdad pasó** en 2026, y descubrir que el ganador de un año puede perder el siguiente. La profundización aplica lo mismo a los sismos, donde la respuesta honesta es «no hay temporada».

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Índice de fechas** | Deja el tiempo como «nombre» de cada fila | Una columna de fechas ordenada a la izquierda |
| **`asfreq("D")`** | Fuerza un calendario completo; los días sin dato quedan `NaN` | Una fila por cada día, aunque esté vacía |
| **`resample("W"/"MS")`** | Cambia la escala del tiempo promediando | Tabla dinámica agrupada por semana o mes |
| **`rolling(30)`** | Media móvil: suaviza sin cambiar la frecuencia | `PROMEDIO` de las 30 celdas anteriores, arrastrado |
| **Perfil estacional** | Promedio por mes del calendario o por día de la semana | Tabla dinámica con «mes» en filas |
| **Descomposición** | Separa tendencia + estacionalidad + resto | Línea de tendencia + promedio por mes |
| **Validación temporal** | Entrena con el pasado, evalúa en el futuro escondido | Tapar los últimos meses y proyectarlos |
| **Ingenuo estacional** | «Este mes = el mismo mes del año pasado» | Copiar la fila del año anterior |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Leer un CSV con `parse_dates` y usar `.dt.month` | ☐ |
| Agrupar con `groupby(...).mean()` | ☐ |
| Calcular un error absoluto medio (MAE) e interpretarlo en las unidades del dato | ☐ |
| Explicar por qué no se evalúa un modelo con los mismos datos con que se entrenó | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar las 30.674 filas de `aire_diario.csv` (14 estaciones) y las de 2026, y fijar `ESTACION = "Cerro Navia"`.

💡 **Concepto clave:** El archivo trae todas las estaciones juntas, en formato «largo». Una serie temporal es **una** secuencia: por eso lo primero es elegir una estación.

---

### Sección 1 · Construir la serie

🎯 **Objetivo:** Una Serie con índice de fechas y calendario completo: **2.191 días**, de los cuales **51 (2,3%)** no tienen dato.

💡 **Concepto clave:** `.asfreq("D")` garantiza que cada día exista. Si un día falta y no lo marcas, un `shift(1)` o una media móvil «se saltan» el hueco sin avisar y mezclan días que no son vecinos.

⚠️ **Error frecuente:** Olvidar `.sort_index()`. Una serie desordenada produce medias móviles y desfases sin sentido.

---

### Sección 2 · Remuestreo y media móvil

🎯 **Objetivo:** Promedios semanales (314 semanas), mensuales (72 meses) y media móvil de 30 días.

💡 **Concepto clave:** El remuestreo **cambia la frecuencia** (de días a meses); la media móvil **no** (sigue siendo diaria, pero suavizada). El mes más contaminado del período fue **julio de 2021**, con **71,5 µg/m³** de promedio mensual — por encima de la norma diaria de 50 durante un mes entero, en promedio.

---

### Sección 3 · Estacionalidad anual y semanal

🎯 **Objetivo:** El perfil por mes del calendario y la diferencia fin de semana vs días hábiles.

💡 **Concepto clave:** El mes más alto es **julio (57,0 µg/m³)** y el más bajo **noviembre (11,9)**: el peor mes promedia **4,8 veces** el mejor. El ciclo semanal existe pero es pequeño: los fines de semana promedian **4,0 µg/m³ más** que los días hábiles. ¿Por qué? Puede haber varias explicaciones (más calefacción en los hogares, cambios en el tráfico y la ventilación), pero **estos datos no permiten afirmarlo**: describir un patrón no es explicarlo.

✅ **Señal de que entendiste:** Puedes decir qué ciclo pesa más (anual) y cuánto, en µg/m³.

---

### Sección 4 · Descomposición

🎯 **Objetivo:** `seasonal_decompose` sobre la serie mensual con `period=12`.

💡 **Concepto clave:** La **amplitud estacional** es de **44,6 µg/m³**: el calendario solo mueve el PM2.5 mensual en esa magnitud. La **tendencia** baja de **27,7** (mediados de 2020) a **24,3** (mediados de 2025): el aire de fondo mejora, lentamente. Ojo: la tendencia de `seasonal_decompose` es una media móvil centrada, por eso pierde 6 meses en cada extremo.

---

### Sección 5 · Validación temporal: tres pronósticos base

🎯 **Objetivo:** Entrenar con 2020–2024 y pronosticar los 12 meses de 2025 con ingenuo, ingenuo estacional y promedio estacional.

💡 **Concepto clave:** El **ingenuo** (todo 2025 = diciembre 2024) se equivoca en **14,5 µg/m³** en promedio: ignora el invierno. El **ingenuo estacional** baja a **2,8** y el **promedio estacional** queda en **4,1**. En una serie con estacionalidad fuerte, la vara mínima no es el ingenuo: es el **ingenuo estacional**.

⚠️ **Error frecuente:** Barajar los datos (`train_test_split` con `shuffle`) en una serie temporal. Eso deja que el modelo «vea» meses futuros: la validación pierde todo sentido.

---

### Sección 6 · Un modelo simple: mes + tendencia

🎯 **Objetivo:** Regresión lineal con 12 columnas de mes y una de tiempo; elegir el método con menor error en 2025.

💡 **Concepto clave:** La regresión logra **2,56 µg/m³** en 2025 y gana. Además estima una tendencia de **−0,93 µg/m³ por año**. Es un modelo que se puede explicar en una frase: «el nivel típico de cada mes, menos casi 1 µg/m³ por cada año que pasa».

---

### Sección 7 · Prueba de fuego: 2026

🎯 **Objetivo:** Reentrenar con 2020–2025 y comparar contra enero–septiembre de 2026.

💡 **Concepto clave:** En 2026 la regresión se equivoca **5,26 µg/m³** en promedio y el ingenuo estacional **5,07**: esta vez gana el ingenuo, por poco. El mes que arruina a ambos es **julio de 2026**: fue de **35,6 µg/m³** cuando los métodos esperaban entre 54 y 57. Ningún método basado solo en el calendario puede anticipar un invierno atípico. La lección no es «la regresión no sirve»: es que **un solo año de validación es poca evidencia**, y que hay que reportar el error histórico junto al pronóstico.

---

## 6. Guía de los 7 Ejercicios

### Ejercicio 1 — Arma la serie diaria y cuenta los días sin dato

**Pistas progresivas:**
- 🟢 Pista suave: Filtra la estación, pon la fecha como índice, toma la columna y ordena.
- 🟡 Pista media: La cadena es `filtrar → .set_index("fecha") → ["pm25"] → .sort_index() → .asfreq("D")`.
- 🔴 Pista directa: `pm = aire[aire["estacion"] == ESTACION].set_index("fecha")["pm25"].sort_index().asfreq("D")`, `n_dias = len(pm)`, `n_faltantes = int(pm.isna().sum())`.

**¿Qué significa el ✅?** Que tienes una serie diaria con calendario completo (2.191 días) y sabes cuántos huecos tiene (51).

---

### Ejercicio 2 — Serie semanal, mensual y media móvil de 30 días

**Pistas progresivas:**
- 🟢 Pista suave: Dos remuestreos y una ventana móvil, todos terminan en `.mean()`.
- 🟡 Pista media: `resample("W")`, `resample("MS")` y `rolling(30, min_periods=20)`.
- 🔴 Pista directa: `semanal = pm.resample("W").mean()`, `mensual = pm.resample("MS").mean()`, `movil_30 = pm.rolling(30, min_periods=20).mean()`.

**¿Qué significa el ✅?** Que sabes cambiar la escala del tiempo (72 meses) y suavizar sin cambiarla.

---

### Ejercicio 3 — Perfil mensual y semanal

**Pistas progresivas:**
- 🟢 Pista suave: Agrupa por una parte de la fecha: el mes, o el día de la semana.
- 🟡 Pista media: `pm.groupby(pm.index.month).mean()`; para el fin de semana, `pm.index.dayofweek >= 5`.
- 🔴 Pista directa: `perfil_mes = pm.groupby(pm.index.month).mean()`, `mes_peak = int(perfil_mes.idxmax())`, `razon_invierno_verano = perfil_mes.max() / perfil_mes.min()`, `dif_fin_de_semana = pm[pm.index.dayofweek >= 5].mean() - pm[pm.index.dayofweek < 5].mean()`.

**¿Qué significa el ✅?** Que mediste la estacionalidad: julio es el peor mes (4,8 veces el mejor) y el fin de semana suma 4,0 µg/m³.

---

### Ejercicio 4 — Descompón la serie mensual

**Pistas progresivas:**
- 🟢 Pista suave: La función ya está importada; necesita la serie, el tipo de modelo y el período.
- 🟡 Pista media: `seasonal_decompose(mensual, model="additive", period=12)`; los componentes están en `.seasonal` y `.trend`.
- 🔴 Pista directa: `desc = seasonal_decompose(mensual, model="additive", period=12)`, `amplitud_estacional = desc.seasonal.max() - desc.seasonal.min()`, `t = desc.trend.dropna()` y `cambio_tendencia = t.iloc[-1] - t.iloc[0]`.

**¿Qué significa el ✅?** Que separaste el ciclo anual (44,6 µg/m³ de amplitud) de la tendencia de fondo (que baja unos 3,4 µg/m³ en cinco años).

---

### Ejercicio 5 — Pronostica 2025 con los tres métodos

**Pistas progresivas:**
- 🟢 Pista suave: Cada pronóstico debe ser una Serie con el **índice de 2025**, para poder restarla de `real_2025`.
- 🟡 Pista media: El ingenuo estacional usa `entrena["2024"].values`; el promedio estacional, `entrena.groupby(entrena.index.month).mean().values`.
- 🔴 Pista directa: `pd.Series(entrena["2024"].values, index=real_2025.index)`, `pd.Series(entrena.groupby(entrena.index.month).mean().values, index=real_2025.index)` y `errores = {k: float((p - real_2025).abs().mean()) for k, p in pron.items()}`.

**¿Qué significa el ✅?** Que validaste sin trampas: 14,5 (ingenuo), 2,8 (ingenuo estacional) y 4,1 (promedio estacional).

---

### Ejercicio 6 — Entrena la regresión y elige el mejor método

**Pistas progresivas:**
- 🟢 Pista suave: `X_mes_tendencia` ya arma las columnas; tú haces `fit` y `predict`.
- 🟡 Pista media: Entrena con `X_mes_tendencia(entrena.index)` y predice con `X_mes_tendencia(real_2025.index)`.
- 🔴 Pista directa: `reg = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(entrena.index), entrena.values)`; `pron["regresion"] = pd.Series(reg.predict(X_mes_tendencia(real_2025.index)), index=real_2025.index)`; `errores["regresion"] = float((pron["regresion"] - real_2025).abs().mean())`; `mejor_metodo = min(errores, key=errores.get)`.

**¿Qué significa el ✅?** Que un modelo simple y explicable (2,56) le ganó a las líneas base en 2025.

---

### Ejercicio 7 — Evalúa contra enero–septiembre de 2026

**Pistas progresivas:**
- 🟢 Pista suave: Es la receta del ejercicio 1 sobre `nuevos`, más un remuestreo mensual.
- 🟡 Pista media: Reentrena con `mensual` completo; el ingenuo estacional son los primeros 9 meses de 2025.
- 🔴 Pista directa: `real_2026 = nuevos[nuevos["estacion"] == ESTACION].set_index("fecha")["pm25"].sort_index().asfreq("D").resample("MS").mean()`; `reg_total = LinearRegression(fit_intercept=False).fit(X_mes_tendencia(mensual.index), mensual.values)`; `pron_2026 = pd.Series(reg_total.predict(X_mes_tendencia(real_2026.index)), index=real_2026.index)`; `ingenuo_est_2026 = pd.Series(mensual["2025"].values[:len(real_2026)], index=real_2026.index)`; los MAE con `(p - real_2026).abs().mean()`.

**¿Qué significa el ✅?** Que pusiste tu pronóstico a prueba contra el futuro real (5,26 vs 5,07) y puedes contarlo con honestidad.

---

> 🔬 **En la profundización:** las mismas herramientas sobre los **sismos** M≥4,5 del USGS. Conviertes 1.601 eventos en un **conteo mensual** (72 meses, 22,2 sismos/mes en promedio) y descubres que vienen **en racimos** (varianza/media = 1,69). Septiembre parece el mes «más sísmico», pero lo explica un solo día: el **1 de septiembre de 2020**, con 18 sismos frente a Vallenar (el mayor, M6,8). Un chi-cuadrado ingenuo da p = 0,028 («¡estacionalidad!»), pero supone eventos independientes; la **permutación de meses completos** da p ≈ 0,29: no hay evidencia. Y la validación lo confirma: el promedio estacional (5,08) no le gana de forma apreciable al promedio plano (5,19).

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Para qué sirve `.asfreq("D")` al construir una serie diaria?

- A) Para ordenar las fechas
- B) Para que cada día del calendario exista y los días sin dato queden como NaN, en vez de desaparecer ✅
- C) Para rellenar los faltantes con cero
- D) Para convertir la serie a mensual

**Explicación:** Sin calendario completo, operaciones como `shift` o `rolling` tratan como vecinos a días que no lo son.

---

**Pregunta 2:** ¿Cuál es la diferencia entre `resample("MS").mean()` y `rolling(30).mean()`?

- A) Ninguna, ambas promedian 30 días
- B) `resample` cambia la frecuencia (un valor por mes); `rolling` suaviza manteniendo un valor por día ✅
- C) `rolling` solo sirve con datos mensuales
- D) `resample` elimina los faltantes y `rolling` no

**Explicación:** Una es una tabla dinámica del tiempo; la otra, un promedio que se desliza.

---

**Pregunta 3:** En una serie con estacionalidad anual fuerte, ¿cuál es la línea base que un modelo debe superar?

- A) El promedio de toda la serie
- B) El ingenuo (último valor)
- C) El ingenuo estacional (mismo período del año anterior) ✅
- D) Cero

**Explicación:** El ingenuo simple ignora el ciclo (14,5 µg/m³ de error en 2025); el ingenuo estacional ya lo captura (2,8). Superar al ingenuo simple no demuestra nada.

---

**Pregunta 4:** La regresión ganó en 2025 y perdió por poco en 2026. ¿Qué reportas?

- A) Solo el resultado de 2025, que fue el de validación
- B) Que la regresión no sirve
- C) Ambos resultados: un año de validación es poca evidencia, y el error esperado debe acompañar al pronóstico ✅
- D) Solo el método que ganó en 2026

**Explicación:** La honestidad es mostrar el historial de error. Elegir el método mirando el año que se quiere reportar es hacer trampa.

---

**Pregunta 5:** (Profundización) Un chi-cuadrado sobre sismos individuales da p = 0,028 para «los meses difieren». ¿Por qué no concluir que hay temporada sísmica?

- A) Porque el p-valor es mayor que 0,05
- B) Porque el test supone eventos independientes y los sismos vienen en racimos (réplicas) ✅
- C) Porque el USGS no mide bien los sismos
- D) Porque hay pocos sismos

**Explicación:** Un solo terremoto aporta decenas de eventos al mismo mes. Un test que permuta meses completos respeta los racimos y no encuentra evidencia (p ≈ 0,29).

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Serie temporal** | Valores ordenados en el tiempo a intervalos regulares | Un indicador de gestión medido mes a mes |
| **Tendencia** | Dirección de largo plazo | «Las solicitudes vienen subiendo» |
| **Estacionalidad** | Patrón que se repite en ciclos fijos | El peak de consultas respiratorias en invierno |
| **Remuestreo** | Cambiar la frecuencia (día → semana → mes) | Pasar el registro diario a un informe mensual |
| **Media móvil** | Promedio de una ventana que se desliza | El «promedio de los últimos 30 días» de un tablero |
| **Descomposición** | Separar tendencia, estacionalidad y resto | Distinguir el efecto del calendario del cambio de fondo |
| **Validación temporal** | Entrenar con el pasado y evaluar en el futuro escondido | Probar una proyección contra el año que ya cerró |
| **Ingenuo estacional** | Mismo período del año anterior como pronóstico | «Pidamos lo mismo que el invierno pasado» |
| **Racimos (*clustering*)** | Eventos que llegan agrupados, no de a uno | Una emergencia que dispara muchas solicitudes juntas |
| **Test de permutación** | Comparar lo observado con muchas versiones barajadas de los datos | Preguntarse «¿esto pasaría igual por azar?» |

---

## 9. Conexión con el Módulo Siguiente

En R2-10 aprendiste a tratar el tiempo como información: calendario completo, remuestreo, estacionalidad, descomposición y, sobre todo, validación temporal honesta con prueba contra el futuro real.

En el **R2-CAP · Capstone** juntarás todo el recorrido de la rama — datos, *features* sin fuga, modelo, evaluación contra una línea base, ficha de modelo — en un proyecto de punta a punta, idealmente con datos de **tu propio organismo**. Si tus datos tienen fecha, lo que aprendiste aquí es obligatorio: partición temporal, nada de barajar, y una línea base estacional que vencer.

> 💡 **Pregunta para reflexionar:** ¿Qué indicador de tu servicio tiene una «temporada» que todos dan por hecho? ¿La has medido alguna vez, o podría ser como los sismos: un patrón que existe solo en la memoria de un par de meses difíciles?
