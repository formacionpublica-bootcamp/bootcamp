# 📘 Guía de Aprendizaje — R2-03 · Estadística para modelar

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-03 · Estadística para modelar |
| **Pista / Rama** | R2 — Científico/a de Datos · Línea B |
| **Duración estimada** | 3–4 horas (Semanas 5–6) |
| **Nivel** | Intermedio |
| **Prerrequisitos** | R2-01 completado (pandas básico, filtros, groupby). Nociones básicas de promedio y porcentaje. |
| **Competencia de salida** | Usar estadística inferencial —distribución, intervalos de confianza, pruebas de hipótesis y correlación— para sustentar decisiones de modelado. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de ChileCompra (monto, cantidad, tamaño de proveedor). |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Un informe de gestión que dice “el monto promedio de compras fue $X” está incompleto si no dice: ¿qué tan variable es ese monto? ¿Esa diferencia entre grupos es real o producto del azar? ¿Hay una relación entre cantidad y costo?

Este módulo responde exactamente esas preguntas con herramientas estadísticas concretas. Cada una tiene uso directo en el Estado:

- **Estadística descriptiva:** entender la distribución del gasto público antes de reportarlo o modelarlo.
- **Intervalos de confianza:** acompañar cualquier estimación con su incertidumbre, como en encuestas o estudios de línea base.
- **Prueba de hipótesis:** verificar si la diferencia entre grupos (ej. gasto en contratos con empresas grandes vs micro) es estadísticamente significativa.
- **Correlación:** identificar relaciones entre variables para orientar el diseño de *features* en un modelo.

> 🏛️ **Mensaje clave:** la estadística no es teoría separada. Es la caja de herramientas que te permite **hablar con honestidad sobre los datos** antes de tomar decisiones o entregar un informe.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|---|---|---|
| **Media** | Promedio aritmético | Gasto promedio por contrato |
| **Mediana** | Valor central que divide en dos mitades | El gasto “típico” cuando hay casos extremos |
| **Percentil 90 (p90)** | Umbral bajo el cual está el 90% de los datos | El gasto máximo “normal” (sin considerar el 10% más caro) |
| **Desviación estándar (std)** | Dispersión alrededor de la media | Cuánto varía el gasto entre contratos similares |
| **Distribución de cola larga** | La mayoría de valores son pequeños, pero hay pocos valores enormes | Muchas compras pequeñas y algunas licitaciones de gran escala |
| **Intervalo de confianza (IC)** | Rango donde probablemente está el valor real de la población | “El gasto promedio real está entre $X y $Y con 95% de confianza” |
| **Prueba de hipótesis (t-test)** | Contrasta si la diferencia entre dos grupos es significativa | ¿Es real la diferencia de gasto entre proveedores grandes y micro? |
| **p-valor** | Probabilidad de observar esa diferencia por azar si no hubiera diferencia real | Menor a 0.05 = diferencia significativa |
| **Correlación de Pearson (r)** | Mide la relación lineal entre dos variables (-1 a 1) | ¿A mayor cantidad pedida, mayor monto? |
| `stats.t.interval()` | Calcula el IC 95% para una media | Rango estadístico alrededor del promedio |
| `stats.ttest_ind()` | T-test para comparar dos grupos independientes | Comparación entre dos tipos de proveedores |
| `stats.pearsonr()` | Calcula la correlación y su p-valor | Relación lineal entre dos columnas numéricas |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Cargar un DataFrame con pandas y filtrar filas | ✅ | Repasa R2-01 si esto te cuesta |
| Entender qué significa “promedio” y “valor central” | ✅ | Piensa en promedios de notas o de gastos mensuales |
| Importar librerías en Python (`from scipy import stats`) | ✅ | Si nunca lo has hecho, no te preocupes: es solo copiar la primera celda |
| Ejecutar celdas en Colab y leer mensajes ✅ / ❌ | ✅ | Ya lo hiciste en módulos anteriores |
| Entender intuitivamente que “menos del 5%” suena a “poco probable” | ✅ | Eso es suficiente para entender el p-valor |

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno

**🎯 Objetivo:** Cargar las librerías necesarias y el dataset `compras_ml.csv`.

**💡 Concepto clave:** Además de `pandas`, `numpy` y `matplotlib`, aquí usamos `scipy.stats`, que es la librería de referencia para estadística inferencial en Python. No necesitas saber cómo funciona por dentro, solo cómo llamarla.

**🔍 Qué hace el código:** Importa las librerías, descarga el CSV si es necesario y lo carga en un DataFrame. Igual que en los módulos anteriores.

**⚠️ Error frecuente:** No ejecutar esta celda o ejecutarla parcialmente. `stats` no existirá en el entorno y los ejercicios 2, 3 y 4 fallarán con `NameError`.

**✅ Señal de comprensión:** El dataset carga sin errores y puedes ver las columnas: `monto_total`, `cantidad`, `tamano_proveedor`, entre otras.

---

### 🔷 Sección 1 — Describir antes de modelar

**🎯 Objetivo:** Calcular media, mediana, percentil 90 y desviación estándar del monto de compras.

**💡 Concepto clave:** Antes de construir cualquier modelo, necesitas conocer la forma de tus datos. El monto de compras públicas tiene **cola larga**: muchos contratos pequeños y unos pocos enormes. En ese escenario, la media puede ser muchísimo mayor que la mediana, y esa diferencia es información crítica para elegir el modelo correcto.

**🔍 Qué hace el código:**
- `x.mean()` calcula la media aritmética.
- `x.median()` calcula la mediana (el valor que divide la distribución por la mitad).
- `x.quantile(0.90)` calcula el percentil 90 (el 90% de las compras está por debajo de este valor).
- `x.std()` mide la dispersión: cuánto se alejan los datos del promedio.

**⚠️ Error frecuente:** Confundir media y mediana. En datos con valores extremos (como contratos de gran escala), la media es arrastrada hacia arriba por esos extremos. La mediana es más representativa del caso “típico”.

**✅ Señal de comprensión:** Puedes explicar por qué en compras públicas la media y la mediana son muy distintas, y qué implica eso para un analista.

---

### 🔷 Sección 2 — Intervalo de confianza para la media

**🎯 Objetivo:** Calcular el intervalo de confianza al 95% para la media del monto.

**💡 Concepto clave:** Un estimado puntual (“el promedio es $X”) siempre tiene incertidumbre. El intervalo de confianza dice: “on 95% de confianza, el promedio real de la población está entre $A y $B”. Es como reportar una encuesta con margen de error: no es imprecisión, es honestidad.

**🔍 Qué hace el código:**
- `stats.sem(x)` calcula el error estándar de la media (cuánto varía la media entre muestras).
- `stats.t.interval(0.95, len(x)-1, loc=media, scale=stats.sem(x))` construye el intervalo usando la distribución t de Student.

**⚠️ Error frecuente:** Asignar mal el desempaquetado. La función devuelve una tupla `(low, high)`, y hay que capturarla como `ic_low, ic_high = ...`. Si se asigna a una sola variable, el chequeo fallará.

**✅ Señal de comprensión:** La media está dentro del intervalo (`ic_low < media < ic_high`) y puedes explicar en palabras simples qué significa ese rango.

---

### 🔷 Sección 3 — Prueba de hipótesis: Grande vs Micro

**🎯 Objetivo:** Determinar si el monto promedio de compras con proveedores Grandes es significativamente distinto al de proveedores Micro.

**💡 Concepto clave:** El t-test de Welch (con `equal_var=False`) compara las medias de dos grupos sin asumir que tienen la misma varianza. Devuelve un **p-valor**: si es menor a 0.05, la diferencia entre grupos es difícilmente explicable por el azar. En política pública esto se traduce en: “¿la diferencia que veo en los datos es real o podría ser coincidencia?”

**🔍 Qué hace el código:**
- Filtra el DataFrame en dos grupos: compras a proveedores `Grande` y a proveedores `Micro`.
- `stats.ttest_ind(grande, micro, equal_var=False)` ejecuta el test de Welch y devuelve el estadístico `t` y el `p_valor`.

**⚠️ Error frecuente:** Olvidar `equal_var=False`. Con `True` (por defecto) se aplica el t-test clásico que asume varianzas iguales, lo cual no suele cumplirse en datos reales de compras públicas.

**✅ Señal de comprensión:** El p-valor está entre 0 y 1, y puedes interpretar si la diferencia es o no significativa al 5%.

---

### 🔷 Sección 4 — Correlación entre cantidad y monto

**🎯 Objetivo:** Medir si la cantidad de artículos pedidos tiene relación lineal con el monto total.

**💡 Concepto clave:** La correlación de Pearson mide la fuerza de la relación lineal entre dos variables numéricas. Va de -1 (relación inversa perfecta) a 1 (relación directa perfecta). Un valor cercano a 0 indica que no hay relación lineal. Lo más importante: **correlación no implica causalidad**. Dos variables pueden moverse juntas por razones totalmente distintas.

**🔍 Qué hace el código:**
- `stats.pearsonr(df["cantidad"], df["monto_total"])` devuelve el coeficiente `r` y el `p-valor`.

**⚠️ Error frecuente:** Interpretar una correlación alta como causalidad. Decir “a mayor cantidad, mayor monto *porque*...” sin más evidencia es un error común en informes de gestión.

**✅ Señal de comprensión:** Puedes decir si la correlación es débil, moderada o fuerte, y por qué el p-valor importa para saber si esa correlación es significativa o podría ser producto del azar.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Resumen descriptivo del monto

**Habilidad que desarrolla:** Caracterizar una distribución con medidas de tendencia central y dispersión.

**Pista 1 (conceptual):** Necesitas cuatro números que describan la columna `monto_total`: su valor central, su valor típico, su percentil alto y su variabilidad.

**Pista 2 (técnica):** Los métodos son `mean()`, `median()`, `quantile(0.90)` y `std()`, todos sobre la variable `x = df["monto_total"]`.

**Pista 3 (casi solución):** El diccionario ya tiene las claves definidas. Solo reemplaza cada `...` por la llamada al método correspondiente.

**Lógica de solución:** Completar el diccionario `desc` con los cuatro métodos estadísticos de pandas sobre la columna.

---

### ✍️ Ejercicio 2 — Intervalo de confianza al 95%

**Habilidad que desarrolla:** Cuantificar la incertidumbre de una estimación estadística.

**Pista 1 (conceptual):** La función `stats.t.interval` recibe el nivel de confianza, los grados de libertad, la media y el error estándar.

**Pista 2 (técnica):** El error estándar se calcula con `stats.sem(x)`. Los grados de libertad son `len(x)-1`.

**Pista 3 (casi solución):** `stats.t.interval(0.95, len(x)-1, loc=media, scale=stats.sem(x))` devuelve directamente el par `(ic_low, ic_high)`.

**Lógica de solución:** Desempaquetar la tupla que devuelve `stats.t.interval(...)` en `ic_low, ic_high`.

---

### ✍️ Ejercicio 3 — T-test Grande vs Micro

**Habilidad que desarrolla:** Contrastar grupos con una prueba de hipótesis.

**Pista 1 (conceptual):** Los dos grupos ya están definidos (`grande` y `micro`). Solo necesitas la función que los compara.

**Pista 2 (técnica):** `stats.ttest_ind(grupo1, grupo2, equal_var=False)` ejecuta el test de Welch.

**Pista 3 (casi solución):** Desempaqueta el resultado en `t_stat, p_valor = ...`. Si `p_valor < 0.05`, la diferencia es estadísticamente significativa.

**Lógica de solución:** Aplicar `stats.ttest_ind` con `equal_var=False` y desempaquetar los dos valores de retorno.

---

### ✍️ Ejercicio 4 — Correlación entre cantidad y monto

**Habilidad que desarrolla:** Medir y describir la relación lineal entre dos variables.

**Pista 1 (conceptual):** `stats.pearsonr` recibe dos columnas de igual largo y devuelve el coeficiente de correlación y su p-valor.

**Pista 2 (técnica):** Los argumentos son `df["cantidad"]` y `df["monto_total"]`, en ese orden.

**Pista 3 (casi solución):** Desempaqueta como `r, p = stats.pearsonr(...)`. `r` está entre -1 y 1.

**Lógica de solución:** Llamar a `stats.pearsonr` con las dos columnas y desempaquetar en `r, p`.

---

## 7. Sección en Profundidad: Ejercicio 3 — Prueba de hipótesis aplicada a política pública

El ejercicio 3 es el más relevante para la toma de decisiones basada en evidencia, que es exactamente lo que busca la política pública moderna.

### ¿Por qué el t-test importa en el sector público?

En el Estado muchas veces se toman decisiones basadas en diferencias observadas: “los contratos con empresas grandes tienen montos mayores, entonces las regulaciones deben cambiar”. Pero esa diferencia observada puede ser puro ruido estadístico.

El t-test responde: **¿cambiaríamos de opinión si esta diferencia fuera producto del azar?**

### Interpretación del p-valor en lenguaje público

| p-valor | Interpretación |
|---|---|
| p < 0.001 | Diferencia muy significativa — muy poco probable que sea azar |
| 0.001 ≤ p < 0.05 | Diferencia significativa — suficiente evidencia para actuar |
| 0.05 ≤ p < 0.10 | Diferencia marginal — hay tendencia pero no es concluyente |
| p ≥ 0.10 | Diferencia no significativa — podría ser azar |

### Advertencia importante: significancia estadística ≠ importancia práctica

Con muchos datos (como los miles de contratos de ChileCompra), es muy fácil obtener un p-valor pequeño aunque la diferencia real sea mínima. Un p-valor < 0.05 no siempre implica una diferencia que valga la pena gestionar.

> 🧠 **Regla práctica:** combina el p-valor con el tamaño del efecto (cuánto es la diferencia en términos absolutos o relativos) para saber si la diferencia es **significativa Y relevante**.

### Aplicaciones directas en el Estado chileno

| Pregunta | Herramienta |
|---|---|
| ¿El gasto difiere significativamente entre regiones? | T-test o ANOVA |
| ¿La tasa de adjudicación mejoró después de una política? | T-test de comparación antes/después |
| ¿Los proveedores MIPYME tienen montos distintos a los grandes? | T-test |
| ¿La diferencia en tiempos de pago entre organismos es real? | T-test o Mann-Whitney |

---

## 8. Conexión con profundiza.ipynb

El profundiza lleva las herramientas de la lección a un nivel más robusto y profesional.

### Comparativa leccion vs. profundiza

| Tema | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| Intervalo de confianza | T de Student (fórmula paramétrica) | Bootstrap (sin supuestos de distribución) |
| Comparación de grupos | T-test de Welch (asume distribución) | Mann-Whitney (no paramétrico) |
| Regresión | No aborda | Regresión OLS con statsmodels |
| Complejidad | ⭐⭐⭐ Intermedio | ⭐⭐⭐⭐ Avanzado |

### Guía de decisión

```
¿Tienes las 4 celdas en ✅?
    ├── No → Termina la lección principal primero.
    └── Sí → ¿Tus datos tienen distribuciones raras o muchos valores extremos?
              ├── Sí → El bootstrap y Mann-Whitney del profundiza son muy relevantes para ti.
              └── No → Avanza a R2-04 y vuelve al profundiza cuando necesites robustez.
```

**Ejercicio más valioso del profundiza:** El bootstrap (ejercicio 1), porque en datos públicos con colas largas (como montos de contratos), los métodos clásicos pueden ser imprecisos y el bootstrap ofrece una alternativa computacional sin supuestos.

---

## 9. Autoevaluación Final

**Pregunta 1:** En una distribución con cola larga (muchos contratos pequeños y pocos enormes), ¿qué ocurre con la media?

- a) La media es siempre igual a la mediana
- b) La media es arrastrada hacia arriba por los valores extremos y queda por encima de la mediana
- c) La media baja porque hay muchos valores pequeños
- d) La media no se puede calcular en distribuciones así

✅ **Respuesta correcta: b)**
**Explicación:** Los valores extremos (contratos muy grandes) inflan la media. Por eso en datos con colas largas, la mediana es más representativa del caso típico que la media.

---

**Pregunta 2:** Un intervalo de confianza del 95% para la media indica que:

- a) El 95% de los contratos están dentro de ese rango
- b) Con 95% de confianza, la media real de la población está dentro de ese intervalo
- c) El 5% de los datos son errores
- d) El intervalo contiene el 95% de los valores extremos

✅ **Respuesta correcta: b)**
**Explicación:** El IC no describe los datos individuales sino la estimación de la media poblacional. Dice: si repitiéramos el muestreo muchas veces, el 95% de los intervalos contendrían la media real.

---

**Pregunta 3:** Si el p-valor del t-test es 0.003, ¿qué concluyes?

- a) La diferencia entre grupos es del 0.3%
- b) La diferencia observada tiene sólo un 0.3% de probabilidad de ser aleatoria; es estadísticamente significativa
- c) El error del modelo es del 0.3%
- d) Hay un 99.7% de contratos con esa diferencia

✅ **Respuesta correcta: b)**
**Explicación:** El p-valor indica la probabilidad de observar esa diferencia (o mayor) si en realidad no hubiera diferencia. Un p = 0.003 < 0.05 implica que la diferencia es estadísticamente significativa.

---

**Pregunta 4:** Una correlación de Pearson de r = 0.87 entre cantidad y monto significa:

- a) Que el 87% del monto es causado por la cantidad
- b) Existe una fuerte relación lineal positiva: a mayor cantidad, mayor monto tiende a ser
- c) Que no hay relación entre las variables
- d) Que cantidad y monto son iguales en el 87% de los casos

✅ **Respuesta correcta: b)**
**Explicación:** Un r cercano a 1 indica relación lineal positiva fuerte. Pero cuidado: no dice nada sobre causalidad. La relación puede deberse a otras variables.

---

**Pregunta 5:** ¿Cuál es la advertencia más importante sobre la correlación?

- a) Solo funciona con menos de 1.000 datos
- b) La correlación no implica causalidad
- c) Solo es válida si el p-valor es mayor a 0.05
- d) No se puede usar con datos de compras públicas

✅ **Respuesta correcta: b)**
**Explicación:** Dos variables pueden correlacionarse por una tercera causa común, por coincidencia, o por una relación espuria. Siempre hay que complementar la correlación con análisis adicional antes de inferir causalidad.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente sector público / Excel |
|---|---|---|
| **Media** | Promedio aritmético de los valores | `PROMEDIO()` en Excel |
| **Mediana** | Valor del centro al ordenar todos los datos | Valor que deja la mitad del gasto por encima y la mitad por debajo |
| **Percentil 90** | El 90% de los datos está por debajo de este valor | El corte de gasto “normal” en una distribución |
| **Desviación estándar** | Medida de cuánto se dispersan los datos alrededor del promedio | `DESVEST()` en Excel |
| **Distribución de cola larga** | Muchos valores pequeños y pocos enormes | Patrón típico del gasto público |
| **Intervalo de confianza** | Rango probable donde está el valor real de la población | Margen de error en encuestas o estudios |
| **Prueba de hipótesis** | Herramienta para decidir si una diferencia es real o aleatoria | Verificar si un cambio en una política tuvo efecto real |
| **p-valor** | Probabilidad de observar esa diferencia si no hubiera ninguna real | < 0.05 = diferencia significativa |
| **T-test de Welch** | Comparación de medias de dos grupos sin asumir varianzas iguales | Comparar grupos con diferentes tamaños y variabilidades |
| **Correlación de Pearson** | Medida de relación lineal entre dos variables (-1 a 1) | `COEF.DE.CORREL()` en Excel |
| **Error estándar** | Cuánto varía la media entre distintas muestras | Precisión de la estimación promedio |
| **Estadística inferencial** | Herramientas para concluir sobre poblaciones a partir de muestras | Base para informes de evaluación basados en evidencia |

---

## 11. Conexión con el Módulo Siguiente

En R2-03 aprendiste a describir y probar relaciones en los datos con rigor estadístico. Ahora estás listo para el siguiente paso.

**El siguiente módulo es R2-04 · Fundamentos de Machine Learning.**

Allí darás el salto de la estadística descriptiva al modelado predictivo:

- Entenderás qué es un modelo de ML y para qué sirve.
- Aprenderás a separar datos en entrenamiento y validación.
- Entrenarás tu primer modelo de regresión o clasificación sobre datos reales.

> 🔗 **Conexión pedagógica:** R2-03 te enseña a entender los datos con honestidad estadística; R2-04 te enseña a usarlos para construir predicciones. La base que aprendiste aquí —distribuciones, grupos, correlaciones— es exactamente lo que te permite elegir y evaluar un modelo con criterio.

¡Muy bien! Llevas más de la mitad del camino de la Rama R2 💪
