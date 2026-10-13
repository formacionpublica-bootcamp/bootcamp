# Guía de Aprendizaje — R2-09 · Despliegue, ficha de modelo y monitoreo

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 9 · Semana 15

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-09 · Despliegue, ficha de modelo y monitoreo |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 120 minutos (lección) + 45 minutos (profundización opcional) |
| **Nivel** | Intermedio — requiere R2-07 y R2-08 |
| **Prerrequisitos** | Pipelines de scikit-learn, `joblib`, MAE, partición temporal, recall/precision |
| **Competencia de salida** | Dejar un modelo usable y vigilado: predicción en línea con validación, puntuación por lotes sin inventar, entregable, monitoreo de desempeño y *drift*, y ficha de modelo honesta |
| **Entregable** | Las 7 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` (PM2.5 diario, 14 estaciones SINCA, 2020–2025) para entrenar y probar; `aire_nuevos.csv` (enero–septiembre 2026) como datos de **producción** que el modelo nunca vio |

---

## 2. ¿Para qué me sirve esto como funcionario público?

La mayoría de los modelos que se construyen en el Estado **nunca se usan**: quedan en el computador de quien los hizo, en un cuaderno que solo esa persona sabe ejecutar. Desplegar es la diferencia entre un ejercicio y una herramienta: que un equipo de gestión ambiental, una SEREMI o un municipio pueda pedirle al modelo «¿cómo estará el aire mañana en esta estación?» y recibir una respuesta **confiable, documentada y vigilada**.

Este módulo usa un caso real: un pronóstico del PM2.5 del día siguiente para 14 estaciones del SINCA, entrenado con 2020–2024 y puesto en «producción» sobre los datos de **2026**. Y la producción real trae sorpresas: El Bosque (Santiago) dejó de reportar entre abril de 2025 y abril de 2026, Copiapó perdió el 40% de sus días, y una de cada siete filas de 2026 no se puede predecir porque falta el dato de hoy o de ayer. Aquí aprenderás a **no inventar** cuando falta el dato, a **comparar con justicia** cuando el desempeño cambia, y a escribir la **ficha** que le dice a quien decide para qué sirve el modelo y para qué no.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Artefacto (`joblib`)** | El modelo entrenado guardado en un archivo, listo para cargarse en otro lugar | Una planilla «plantilla» con las fórmulas ya armadas |
| **Predicción en línea** | Una función que recibe un caso y devuelve la predicción | Una celda con fórmula donde escribes los datos y ves el resultado |
| **Validación de entrada** | Rechazar con un mensaje claro los datos imposibles o faltantes | Validación de datos (lista desplegable, rango permitido) |
| **Puntuación por lotes** | Predecir una tabla entera de un viaje | Arrastrar la fórmula a toda la columna |
| **`estado = "sin_prediccion"`** | Marcar la fila que no se pudo predecir, en vez de inventar | Dejar visible el `#N/A` en vez de rellenarlo con cero |
| **Monitoreo de desempeño** | Comparar el error en producción con el de la prueba | Comparar la proyección con lo ejecutado, mes a mes |
| ***Drift*** | Cambio en la distribución de los datos de entrada | Notar que este mes la planilla llegó con muchas celdas vacías |
| **Ficha de modelo** | Documento que acompaña al modelo: qué hace, cuánto se equivoca, para qué no usarlo | La hoja «Léame» de una planilla oficial |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar qué hace un `Pipeline` y por qué se guarda completo con `joblib` | ☐ |
| Calcular un MAE con `mean_absolute_error` y explicar qué significa en las unidades del dato | ☐ |
| Explicar por qué en datos temporales se entrena con el pasado y se prueba con el futuro | ☐ |
| Distinguir *recall* de *precision* (solo para la profundización) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación y el modelo que vas a desplegar

🎯 **Objetivo:** Cargar la historia (30.674 filas, 2020-01-01 → 2025-12-30) y los datos nuevos (3.808 filas, 2026-01-01 → 2026-09-29), y reconstruir el modelo.

💡 **Concepto clave:** La celda del modelo ya viene hecha: es una variante más simple del pipeline de R2-08, **sin meteorología** (solo 7 de 14 estaciones la miden), reconstruida aquí para que el módulo no dependa de otro archivo. Fíjate en tres decisiones de oficio: (1) la receta de *features* es **una sola función** (`construir_features`) que se usa igual al entrenar y en producción; (2) la partición es **temporal**: entrena con 2020–2024 y prueba con 2025; (3) el modelo se guarda en `modelo_pm25.joblib` y **se vuelve a cargar**, como lo haría otro equipo. El modelo logra un MAE de **3,94 µg/m³** en la prueba 2025, frente a **4,19** de la línea base «mañana = hoy»: le gana, pero por poco. Ese dato irá a la ficha.

⚠️ **Error frecuente:** Pensar que, si el modelo vive en el cuaderno, ya está desplegado. Desplegar es que **otra persona u otro sistema** pueda usarlo sin ti.

---

### Sección 1 · La función de predicción

🎯 **Objetivo:** Envolver `modelo.predict` en una función que reciba los datos de un caso y devuelva un número.

💡 **Concepto clave:** Como el pipeline incluye el codificador de la estación, la función no transforma nada a mano. Para Cerro Navia con 60 µg/m³ hoy, 55 ayer, media semanal de 48 y mes 6, el modelo estima unos 50 µg/m³ para mañana.

---

### Sección 2 · Validar la entrada

🎯 **Objetivo:** Rechazar estaciones desconocidas, valores faltantes, valores fuera de rango y meses inválidos, con un mensaje claro.

💡 **Concepto clave:** El bosque aleatorio de scikit-learn (desde la versión 1.4) **acepta NaN sin reclamar** y entrega un número igual. Es decir: sin validación, el modelo **inventa en silencio**. Y una estación desconocida no produce error (el codificador la ignora): produce una predicción «promedio» que nadie pidió. La validación no es burocracia: es lo que impide que un sistema responda tonterías con cara de seguridad.

⚠️ **Error frecuente:** Usar `v == np.nan` para detectar faltantes. `NaN` no es igual a nada, ni siquiera a sí mismo: usa `pd.isna(v)`.

---

### Sección 3 · Puntuación por lotes en producción

🎯 **Objetivo:** Predecir todas las filas de 2026 que traen los datos completos y marcar el resto como `sin_prediccion`.

💡 **Concepto clave:** De las 3.808 filas de 2026, **542 (14,2%) no se pueden predecir** porque falta el PM2.5 de hoy, de ayer o de la semana. No se reparten parejo: El Bosque (51%), Copiapó (44%), Concón (37%) y Coquimbo (27%) concentran casi todos los huecos. Un lote que «rellena» esos huecos con un promedio entregaría pronósticos que parecen datos y no lo son.

✅ **Señal de que entendiste:** Puedes explicar por qué es mejor una fila vacía y marcada que una predicción inventada.

---

### Sección 4 · Entregar el resultado

🎯 **Objetivo:** Guardar `predicciones_pm25_2026.csv` con la columna `fecha_objetivo` (el día pronosticado) y el `estado` de cada fila.

💡 **Concepto clave:** Quien recibe el archivo no tiene tu cuaderno. Si la columna dice `fecha` sin más, ¿es el día del dato o el día pronosticado? Un buen entregable **no obliga a adivinar**.

---

### Sección 5 · Monitoreo de desempeño

🎯 **Objetivo:** Calcular el MAE en 2026 y compararlo con la prueba de los **mismos meses** y con la línea base.

💡 **Concepto clave:** El MAE de 2026 (**4,92**) es mayor que el de la prueba 2025 completa (**3,94**). ¿Se rompió el modelo? No tan rápido: 2026 cubre enero–septiembre, que incluye el invierno, cuando el PM2.5 es más alto y más difícil de pronosticar. Contra la prueba 2025 de **enero–septiembre** (**4,58**), la diferencia es mucho menor. Y el modelo **sigue ganándole** a la línea base en 2026 (**5,03**). Moraleja: comparar el error de un período con el de otro solo vale si los períodos son comparables.

✅ **Señal de que entendiste:** Puedes explicar por qué comparar 4,92 con 3,94 sería injusto con el modelo.

---

### Sección 6 · *Drift* de los datos de entrada

🎯 **Objetivo:** Comparar, por estación, la proporción de días sin dato en la historia y en 2026, y listar las estaciones con más de 20% de faltantes en 2026.

💡 **Concepto clave:** El desempeño se conoce con un día de atraso; la entrada se puede vigilar **el mismo día**. Cuatro estaciones superan el 20% de faltantes en 2026: **Concón, Copiapó, Coquimbo y El Bosque**. Copiapó pasó de 2,5% a 40%. La tabla también muestra cambios de nivel: Concón promedia 18,7 µg/m³ en 2026 contra 13,5 en enero–septiembre de la historia. Eso no es un error del modelo, pero es una señal para mirar.

---

### Sección 7 · La ficha de modelo

🎯 **Objetivo:** Completar la ficha con frases reales y con los números verificados (MAE de prueba, de línea base y de 2026).

💡 **Concepto clave:** Una ficha honesta dice lo incómodo: que el modelo le gana **por poco** a «mañana = hoy», que no usa meteorología (solo 7 de 14 estaciones la miden), que no predice si falta el dato de hoy, y que **no debe** decretar episodios por sí solo.

---

### Sección 8 · (Opcional) Gradio

La celda arma una app con `predecir_seguro` por dentro. Está protegida: si Gradio no está instalado, solo muestra un aviso. En Colab: `!pip -q install gradio` y descomenta `demo.launch(share=True)`.

---

## 6. Guía de los 7 Ejercicios

### Ejercicio 1 — Escribe `predecir_pm25`

**Pistas progresivas:**
- 🟢 Pista suave: La tabla `entrada` ya está armada; solo falta pedirle la predicción al modelo.
- 🟡 Pista media: `modelo.predict(entrada)` devuelve un arreglo de un elemento; tómalo con `[0]`.
- 🔴 Pista directa: `return round(float(modelo.predict(entrada)[0]), 1)`.

**¿Qué significa el ✅?** Que tu función devuelve un número igual al del modelo para un caso de prueba.

---

### Ejercicio 2 — Escribe `predecir_seguro`

**Pistas progresivas:**
- 🟢 Pista suave: Son tres revisiones antes de predecir: ¿falta algo?, ¿está en rango?, ¿el mes existe?
- 🟡 Pista media: `any(pd.isna(v) for v in valores)` detecta faltantes; `all(0 <= v <= 1000 for v in valores)` revisa el rango.
- 🔴 Pista directa: Agrega `if any(pd.isna(v) for v in valores): return {"ok": False, "error": "Dato faltante"}`, luego `if not all(0 <= v <= 1000 for v in valores): return {...}` y `if mes not in range(1, 13): return {...}`.

**¿Qué significa el ✅?** Que el caso bueno predice y los cuatro casos malos (faltante, negativo, mes 13, estación inventada) se rechazan.

---

### Ejercicio 3 — Escribe `puntuar_lote` y aplícalo a 2026

**Pistas progresivas:**
- 🟢 Pista suave: `completo` ya marca qué filas traen todos los datos. Predice solo esas.
- 🟡 Pista media: Usa `resultado.loc[completo, "pm25_predicho"] = ...` y, adentro, `resultado.loc[completo, FEATURES]`.
- 🔴 Pista directa: `resultado.loc[completo, "pm25_predicho"] = modelo.predict(resultado.loc[completo, FEATURES]).round(1)` y `n_sin_prediccion = int((pred_2026["estado"] == "sin_prediccion").sum())`.

**¿Qué significa el ✅?** Que predijiste exactamente las filas completas (3.266) y contaste las 542 que no se pueden predecir.

---

### Ejercicio 4 — Genera `predicciones_pm25_2026.csv`

**Pistas progresivas:**
- 🟢 Pista suave: Primero la columna nueva, después guardar.
- 🟡 Pista media: Sumarle un día a una fecha: `+ pd.Timedelta(days=1)`.
- 🔴 Pista directa: `entregable["fecha_objetivo"] = entregable["fecha"] + pd.Timedelta(days=1)` y `entregable.to_csv("predicciones_pm25_2026.csv", index=False)`.

**¿Qué significa el ✅?** Que el archivo existe, tiene la fecha pronosticada explícita y una fila por cada fila de producción.

---

### Ejercicio 5 — MAE en 2026 vs prueba (mismos meses) vs línea base

**Pistas progresivas:**
- 🟢 Pista suave: Son tres MAE: modelo en 2026, modelo en la prueba de enero a septiembre, y «mañana = hoy» en 2026.
- 🟡 Pista media: `mean_absolute_error(real, predicho)`; el filtro de meses es `prueba["fecha"].dt.month <= 9`.
- 🔴 Pista directa: `mae_2026 = mean_absolute_error(con_verdad["pm25_manana"], con_verdad["pm25_predicho"])`; `prueba_mismos_meses = prueba[prueba["fecha"].dt.month <= 9]`; `mae_prueba_mismos_meses = mean_absolute_error(prueba_mismos_meses[OBJETIVO], modelo.predict(prueba_mismos_meses[FEATURES]))`; `mae_ingenuo_2026 = mean_absolute_error(con_verdad["pm25_manana"], con_verdad["pm25_hoy"])`.

**¿Qué significa el ✅?** Que sabes medir el desempeño en producción y ponerlo en contexto: 4,92 en 2026 vs 4,58 en la prueba comparable vs 5,03 de la línea base.

---

### Ejercicio 6 — Compara faltantes entre historia y 2026

**Pistas progresivas:**
- 🟢 Pista suave: Copia la línea de `falt_hist` y cambia `historia` por `nuevos`.
- 🟡 Pista media: Para filtrar una Serie: `falt_2026[falt_2026 > 0.20]`; los nombres están en `.index`.
- 🔴 Pista directa: `falt_2026 = nuevos["pm25"].isna().groupby(nuevos["estacion"]).mean()` y `estaciones_alerta = sorted(falt_2026[falt_2026 > 0.20].index)`.

**¿Qué significa el ✅?** Que detectaste las 4 estaciones con más de 20% de días sin dato en 2026.

---

### Ejercicio 7 — Completa la ficha de modelo

**Pistas progresivas:**
- 🟢 Pista suave: Cada `...` es una frase entre comillas o un número redondeado.
- 🟡 Pista media: Los números ya están calculados: `mae_prueba` (setup) y `mae_2026` (ejercicio 5).
- 🔴 Pista directa: `"mae_prueba": round(mae_prueba, 2)`, `"mae_2026": round(mae_2026, 2)`, y escribe frases de al menos una línea en `uso_previsto`, `no_usar_para` y `limitaciones`.

**¿Qué significa el ✅?** Que la ficha tiene todas las secciones y sus números calzan con los verificados.

---

> 🔬 **En la profundización:** dos preguntas de equipo de producción. **¿Dónde se degrada?** El MAE por estación muestra que El Bosque pasa de 2,12 en la prueba a 9,06 en 2026 (4,3 veces) — y el «por qué» no está en el modelo sino en la prueba: El Bosque **no tuvo ni un día de invierno** en la prueba 2025 porque dejó de reportar en abril. **¿Cuándo alertar?** Con umbral 50 el modelo detecta solo el 55% de los días que superaron la norma en 2025; eligiendo el umbral con 2025 para lograr *recall* ≥ 0,80 (resulta **39 µg/m³**) y evaluándolo recién en 2026, detecta el 80% de los 176 días sobre la norma, con *precision* de 0,51.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué la receta de *features* debe ser una sola función usada al entrenar y en producción?

- A) Para ahorrar líneas de código
- B) Porque si las recetas difieren, el modelo recibe datos con otro significado y se equivoca sin avisar ✅
- C) Porque scikit-learn lo exige
- D) Para que el modelo entrene más rápido

**Explicación:** Si en producción la «media de 7 días» se calcula distinto (por ejemplo, incluyendo el día de mañana o saltándose los huecos), el modelo no lanza error: simplemente predice mal.

---

**Pregunta 2:** Llega una fila de producción sin el PM2.5 de hoy. ¿Qué hace un buen despliegue?

- A) Rellenar con el promedio histórico y predecir
- B) Predecir igual: el modelo acepta NaN
- C) No predecir esa fila y marcarla (`sin_prediccion`) para que se vea y se cuente ✅
- D) Borrar la fila del archivo

**Explicación:** Rellenar o predecir con NaN produce un número que parece un pronóstico y no lo es. Borrar la fila esconde el problema. Marcarla lo deja auditable.

---

**Pregunta 3:** El MAE en 2026 (enero–septiembre) es 4,92 y el de la prueba 2025 (año completo) es 3,94. ¿Qué concluyes primero?

- A) El modelo se rompió y hay que reentrenarlo ya
- B) Hay que comparar con la prueba de los mismos meses, porque el invierno es más difícil ✅
- C) Que 2026 fue un año con más contaminación
- D) Nada: el MAE no sirve para monitorear

**Explicación:** Con la prueba de enero–septiembre (4,58) la brecha se achica mucho, y el modelo sigue ganándole a la línea base. Monitorear es comparar con justicia.

---

**Pregunta 4:** ¿Qué tipo de *drift* puedes detectar el mismo día, sin esperar a conocer la verdad?

- A) La caída del MAE
- B) Los cambios en los datos de entrada, como la proporción de faltantes por estación ✅
- C) El error de la línea base
- D) Ninguno: todo monitoreo requiere esperar

**Explicación:** El desempeño necesita el valor real (que llega después); la entrada se puede vigilar en cuanto llega.

---

**Pregunta 5:** ¿Qué debe decir la ficha de un modelo que le gana por poco a la línea base?

- A) Omitirlo para no restarle confianza
- B) Decirlo con los números, junto con sus límites y los usos que NO se recomiendan ✅
- C) Reportar solo el MAE del modelo
- D) Reportar el mejor MAE entre todos los meses

**Explicación:** La ficha existe para que quien decide sepa cuánto confiar. Esconder la línea base es vender humo.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Despliegue** | Poner un modelo a trabajar para otras personas o sistemas | Pasar un piloto a operación |
| **Artefacto** | El archivo con el modelo entrenado (`.joblib`) | La versión aprobada de una planilla de cálculo |
| **En línea / por lotes** | Predecir un caso al instante / una tabla de un viaje | Atención de ventanilla / proceso masivo de cierre de mes |
| **Validación de entrada** | Rechazar datos imposibles o faltantes con un mensaje claro | El formulario que no deja enviar un RUT inválido |
| **Producción** | Uso real, con datos que el modelo nunca vio | La operación diaria del servicio |
| **Monitoreo** | Vigilar el desempeño y los datos del modelo en el tiempo | El control de gestión mensual |
| ***Drift*** | Cambio en los datos (o en la relación con el objetivo) respecto del entrenamiento | «Este año la población que atendemos cambió» |
| **Línea base** | La regla simple que el modelo debe superar («mañana = hoy») | La proyección inercial |
| **Ficha de modelo** | Documento con uso, datos, desempeño, límites y responsable | La ficha técnica de un indicador |
| **Norma de PM2.5** | 50 µg/m³ como concentración de 24 horas (D.S. 12/2011 del MMA) | El estándar de calidad que fiscaliza la autoridad ambiental |

---

## 9. Conexión con el Módulo Siguiente

En R2-09 cerraste el ciclo de vida de un modelo: lo cargaste desde un artefacto, lo pusiste a predecir en línea y por lotes sin inventar, lo vigilaste en producción con comparaciones justas y lo documentaste con una ficha honesta.

En **R2-10 · Series temporales** (optativo) mirarás el PM2.5 como lo que es: una **serie en el tiempo**, con estacionalidad anual (el invierno que hoy complicó el monitoreo), patrones semanales, remuestreo y pronósticos que deben superar a una línea base estacional. Y en el **R2-CAP** harás todo esto de punta a punta con datos de tu propio organismo.

> 💡 **Pregunta para reflexionar:** Si mañana tu servicio pusiera en uso un modelo, ¿quién vería la tabla de faltantes cada semana? Si la respuesta es «nadie», el modelo no está desplegado: está abandonado.
