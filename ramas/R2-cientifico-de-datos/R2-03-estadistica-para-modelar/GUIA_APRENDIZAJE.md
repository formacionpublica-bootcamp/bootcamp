# Guía de Aprendizaje — R2-03 · Estadística para modelar

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Módulo 3 · Semanas 5–6

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-03 · Estadística para modelar |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2–3 horas |
| **Nivel** | Intermedio — requiere R2-00 y R2-01 |
| **Prerrequisitos** | Filtrar con máscaras, `groupby`, `dropna`, columnas de fecha (`.dt.month`) |
| **Competencia de salida** | Usar estadística descriptiva e inferencial para sustentar —y cuestionar— decisiones de modelado: asimetría, estacionalidad, intervalos (t y *bootstrap*), prueba de hipótesis y correlación con confusores |
| **Entregable** | Las 6 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `aire_diario.csv` — PM2.5 diario 2020–2025 de 14 estaciones SINCA (MMA); estación ancla: Cerro Navia, con temperatura y humedad. Profundización: `matricula.csv` (MINEDUC 2025) × `comunas.csv` |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Antes de entrenar un modelo hay que **conocer el dato**, porque el modelo hereda todo lo que no viste. Este módulo usa la calidad del aire —un tema de salud pública con norma propia: **50 µg/m³ de PM2.5 en 24 horas** (D.S. 12/2011 del MMA)— para practicar las preguntas que cualquier informe técnico debería responder antes de afirmar algo:

- ¿Cómo se reparte la variable? El PM2.5 tiene **cola larga**: la media (15,5 µg/m³) queda bien arriba de la mediana (11).
- ¿Cuándo pasa? En Cerro Navia, **julio** promedia 57,0 µg/m³ y hubo **332 días sobre la norma** entre 2020 y 2025.
- ¿Con qué incertidumbre lo digo? La media invernal es 47,9 µg/m³, pero con un **intervalo** de [45,8 ; 50,0].
- ¿Es real esta mejora? El invierno 2025 (48,6) fue algo más limpio que el 2024 (50,1)… pero la diferencia **no es distinguible del azar** (p = 0,69). Un anuncio de «bajó la contaminación» no se sostiene con esos datos.
- ¿Esto causa aquello? La humedad *parece* subir el PM2.5 (r = +0,36), pero dentro del invierno la relación se **invierte** (r = −0,50): el invierno era el que movía ambas.

> 🏛️ **Mensaje clave:** la estadística no es un trámite antes del modelo; es la forma de **hablar con honestidad** de los datos ante una autoridad.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel / en el trabajo |
|----------|-----------|----------------------|
| **Media / mediana / p90** | Centro y extremo alto de la distribución | `PROMEDIO`, `MEDIANA`, `PERCENTIL` |
| **Asimetría (`skew`)** | Mide cuán cargada está la cola: 0 simétrico, > 1 muy asimétrico | `COEFICIENTE.ASIMETRIA` |
| **`np.log1p`** | Logaritmo de (1 + x): comprime la cola larga y admite ceros | Graficar en escala logarítmica |
| **Estacionalidad** | Patrón que se repite cada año (invierno alto, verano bajo) | Tabla dinámica por mes |
| **Intervalo de confianza 95%** | Rango plausible para la media real | El «margen de error» de una encuesta |
| **`stats.t.interval`** | IC por fórmula (distribución t) | — |
| **Bootstrap** | IC por remuestreo con reemplazo, sin supuestos | Simular miles de «otros inviernos» |
| **Test de Welch** | Compara dos medias sin asumir varianzas iguales | ¿La diferencia es real o ruido? |
| **p-valor** | Probabilidad de ver una diferencia así si no hubiera diferencia real | < 0,05 → «significativa» |
| **Pearson / Spearman** | Correlación lineal / correlación de rangos (robusta) | `COEF.DE.CORREL` |
| **Variable de confusión** | Un tercero que mueve a las dos variables a la vez | «El invierno» detrás de humedad y PM2.5 |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar un DataFrame con una condición (`df[df["mes"] == 7]`) | ☐ |
| Usar `.isin([6, 7, 8])` para filtrar por varios valores | ☐ |
| Hacer `groupby("columna")["otra"].mean()` | ☐ |
| Explicar qué es un valor nulo y quitarlo con `.dropna()` | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `aire_diario.csv` (30.674 filas: un día × una estación) con la fecha como fecha, agregar `mes` y `anio`, y separar la estación ancla `cn` = **Cerro Navia** (2.191 días).

💡 **Concepto clave:** Solo 7 de las 14 estaciones traen temperatura y humedad en este archivo; Cerro Navia sí mide temperatura y humedad. Por eso los ejercicios con clima usan `cn`.

---

### Sección 1 · Describir antes de modelar

🎯 **Objetivo:** Calcular media, mediana, p90 y asimetría del PM2.5 de todas las estaciones, y la asimetría tras `np.log1p`.

💡 **Concepto clave:** Media 15,5 > mediana 11 y asimetría **3,39**: muchos días tranquilos, pocos días muy malos. El logaritmo baja la asimetría a **0,43**. Muchos modelos funcionan mejor con variables menos asimétricas — esto vuelve en R2-04.

⚠️ **Error frecuente:** Usar `np.log` en vez de `np.log1p`: hay 80 días con PM2.5 = 0 y log(0) = −∞.

---

### Sección 2 · Estacionalidad

🎯 **Objetivo:** Promedio de PM2.5 por mes en Cerro Navia, el peor mes y cuántos días superaron 50 µg/m³.

💡 **Concepto clave:** El peor mes es **julio** (57,0 µg/m³ promedio) y hubo **332 días** sobre la norma en seis años. El gráfico de cajas muestra que en junio-julio la mitad de los días ya rondan o superan la norma: calefacción a leña e inversión térmica.

✅ **Señal de que entendiste:** Puedes explicar por qué un promedio anual esconde el problema.

---

### Sección 3 · Intervalo de confianza

🎯 **Objetivo:** IC 95% de la media invernal (junio-agosto) con `stats.t.interval`.

💡 **Concepto clave:** Con 546 días de invierno, la media es **47,9** y el IC **[45,8 ; 50,0]** µg/m³. El intervalo habla de la **media**, no de los días: muchos días individuales están muy por encima de 50.

⚠️ **Error frecuente:** Asignar el resultado a una sola variable. `stats.t.interval` devuelve dos números: `ic_low, ic_high = ...`.

---

### Sección 4 · Bootstrap

🎯 **Objetivo:** IC 95% de la diferencia invierno − verano remuestreando 2.000 veces.

💡 **Concepto clave:** La diferencia observada es **33,6 µg/m³** y el IC bootstrap **[31,5 ; 35,8]** no toca el cero. El bootstrap no usa fórmulas ni supone normalidad: es la herramienta de referencia cuando la distribución es rara.

✅ **Señal de que entendiste:** Puedes decir qué significa «remuestrear con reemplazo» con un ejemplo.

---

### Sección 5 · Prueba de hipótesis

🎯 **Objetivo:** Comparar los inviernos 2024 y 2025 con el test de Welch.

💡 **Concepto clave:** 50,1 vs 48,6 µg/m³, **p = 0,69**: no hay evidencia de mejora. Un p-valor alto **también es un resultado** y protege de anunciar logros que son variación normal (la meteorología cambia de un invierno a otro).

⚠️ **Letra chica:** Los días consecutivos se parecen (autocorrelación), así que los p-valores con series diarias son **optimistas**. Aquí ni siquiera así sale significativo.

---

### Sección 6 · Correlación ≠ causalidad

🎯 **Objetivo:** Comparar la correlación humedad–PM2.5 en todo el año y solo en junio-julio.

💡 **Concepto clave:** Todo el año, **r = +0,36**; solo en pleno invierno, **r = −0,50**. El signo se invierte porque el **invierno** trae a la vez aire húmedo y más contaminación: es una **variable de confusión**. La temperatura (r = −0,55) tampoco «causa» nada por sí sola: actúa a través de la calefacción y la inversión térmica.

✅ **Señal de que entendiste:** Puedes explicar por qué «subir la temperatura» no es una política de aire limpio.

---

### Reflexión final

La pregunta sobre qué variable **sí** se puede intervenir (uso de leña, restricción vehicular, fiscalización en episodios) no tiene celda de chequeo: es la conversación que el analista debe tener con quien diseña la política.

---

## 6. Guía de los 6 Ejercicios

### Ejercicio 1 — Resumen descriptivo y asimetría

**Pistas progresivas:**
- 🟢 Pista suave: Son cuatro métodos de pandas sobre `x`, más uno para la asimetría del logaritmo.
- 🟡 Pista media: `mean()`, `median()`, `quantile(0.90)`, `skew()`; el log es `np.log1p(x)`.
- 🔴 Pista directa: `"asimetria": float(x.skew())` y `asim_log = float(np.log1p(x).skew())`.

**¿Qué significa el ✅?** Que mediste la cola larga (asimetría 3,39) y viste que el log la reduce (0,43).

---

### Ejercicio 2 — Estacionalidad en Cerro Navia

**Pistas progresivas:**
- 🟢 Pista suave: Agrupa por mes, y busca el índice del máximo.
- 🟡 Pista media: `cn.groupby("mes")["pm25"].mean()` y `.idxmax()`; los días sobre la norma son una condición sumada.
- 🔴 Pista directa: `mes_peor = int(por_mes.idxmax())` y `dias_sobre_norma = int((cn["pm25"] > 50).sum())`.

**¿Qué significa el ✅?** Que encontraste julio como el peor mes y contaste los 332 días sobre la norma.

---

### Ejercicio 3 — IC 95% de la media invernal

**Pistas progresivas:**
- 🟢 Pista suave: La función necesita el nivel de confianza, los grados de libertad, la media y el error estándar.
- 🟡 Pista media: Grados de libertad = `len(inv) - 1`; error estándar = `stats.sem(inv)`.
- 🔴 Pista directa: `ic_low, ic_high = stats.t.interval(0.95, len(inv) - 1, loc=media_inv, scale=stats.sem(inv))`.

**¿Qué significa el ✅?** Que acompañaste la media invernal con su incertidumbre (± ~2 µg/m³).

---

### Ejercicio 4 — Bootstrap de la diferencia invierno − verano

**Pistas progresivas:**
- 🟢 Pista suave: Repite 2.000 veces: remuestrea cada grupo, calcula la diferencia de medias y guárdala.
- 🟡 Pista media: `rng.choice(inv.values, len(inv))` remuestrea con reemplazo; usa una lista por comprensión.
- 🔴 Pista directa: `difs = [rng.choice(inv.values, len(inv)).mean() - rng.choice(ver.values, len(ver)).mean() for _ in range(2000)]` y `b_low, b_high = np.percentile(difs, [2.5, 97.5])`.

**¿Qué significa el ✅?** Que el intervalo [31,5 ; 35,8] no toca el cero: el invierno es claramente peor.

---

### Ejercicio 5 — ¿El invierno 2025 fue más limpio?

**Pistas progresivas:**
- 🟢 Pista suave: Los dos grupos ya están filtrados; falta la función que compara medias.
- 🟡 Pista media: `stats.ttest_ind(a, b, equal_var=False)` es el test de Welch; devuelve dos valores.
- 🔴 Pista directa: `t_stat, p_valor = stats.ttest_ind(inv_2024, inv_2025, equal_var=False)` y `significativa = p_valor < 0.05`.

**¿Qué significa el ✅?** Que comprobaste que la baja de 1,5 µg/m³ cabe en la variación normal entre inviernos (p = 0,69).

---

### Ejercicio 6 — Correlaciones globales vs dentro del invierno

**Pistas progresivas:**
- 🟢 Pista suave: Calcula la misma correlación dos veces: en todos los días (`s`) y solo en junio-julio (`pleno`).
- 🟡 Pista media: `stats.pearsonr(x, y)` da (r, p); `serie1.corr(serie2)` da solo r.
- 🔴 Pista directa: `r_temp, p_temp = stats.pearsonr(s["temp_media"], s["pm25"])`, `r_hum_todo = s["pm25"].corr(s["humedad_media"])` y `r_hum_invierno = pleno["pm25"].corr(pleno["humedad_media"])`.

**¿Qué significa el ✅?** Que viste un signo invertirse al controlar por la estación del año: la firma de un confusor.

---

> 🔬 **En la profundización:** transferencia a otro dato del Estado — la **matrícula 2025** cruzada con la **población** de 30 comunas. Construyes la tasa de estudiantes por 1.000 habitantes (de 148 en Pirque a 255 en Linares), ves que dos **conteos** correlacionan casi perfecto solo por tamaño (r = 0,99), comparas **Pearson (−0,44, p = 0,014) con Spearman (−0,17, p = 0,37)** y mides con *bootstrap* cuán frágil es una correlación con solo 30 casos (IC [−0,75 ; −0,04]).

---

## 7. Autoevaluación Final

**Pregunta 1:** El PM2.5 diario tiene media 15,5 y mediana 11. ¿Qué indica?

- A) Que los datos tienen errores
- B) Una cola larga a la derecha: pocos días muy contaminados arrastran la media hacia arriba ✅
- C) Que la mitad de los días supera la norma
- D) Nada: media y mediana siempre difieren un poco

**Explicación:** Con asimetría positiva, la media queda sobre la mediana. Para describir el «día típico», la mediana es más fiel.

---

**Pregunta 2:** El IC 95% de la media invernal es [45,8 ; 50,0]. ¿Qué significa?

- A) Que el 95% de los días de invierno está entre 45,8 y 50,0
- B) Que la media real del PM2.5 invernal está, con 95% de confianza, en ese rango ✅
- C) Que ningún día de invierno superó la norma
- D) Que hay un 5% de datos erróneos

**Explicación:** El intervalo es sobre la **media**, no sobre los días individuales; muchos días superan los 50 µg/m³.

---

**Pregunta 3:** Comparando los inviernos 2024 y 2025 se obtiene p = 0,69. ¿Qué concluyes?

- A) Que 2025 fue 69% más limpio
- B) Que la diferencia observada es compatible con la variación normal entre inviernos; no hay evidencia de mejora ✅
- C) Que la medición está mal
- D) Que 2024 fue significativamente peor

**Explicación:** p > 0,05 → no se puede descartar el azar. No prueba que «no cambió nada», pero no respalda anunciar una mejora.

---

**Pregunta 4:** ¿Por qué usar *bootstrap* en vez de la fórmula t?

- A) Porque siempre da intervalos más angostos
- B) Porque no necesita suponer una distribución: remuestrea los datos que tienes ✅
- C) Porque no requiere computador
- D) Porque elimina la asimetría

**Explicación:** El bootstrap reemplaza supuestos por cómputo; es especialmente útil con colas largas o estadísticos raros (como una correlación).

---

**Pregunta 5:** La humedad correlaciona +0,36 con el PM2.5 en el año, pero −0,50 dentro de junio-julio. ¿Qué explica el cambio de signo?

- A) Un error de cálculo
- B) La estación del año es una variable de confusión que mueve a ambas ✅
- C) La humedad causa contaminación en verano
- D) Que en invierno no se mide la humedad

**Explicación:** El invierno trae aire húmedo **y** más contaminación (calefacción, inversión térmica). Al mirar solo el invierno, ese efecto común desaparece y aparece otra relación.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **PM2.5** | Material particulado fino (≤ 2,5 micrones), en µg/m³ | El contaminante con norma diaria de 50 µg/m³ |
| **Asimetría (skew)** | Cuán cargada a un lado está la distribución | «Pocos casos extremos» en un indicador |
| **`np.log1p`** | Logaritmo de 1 + x | Escala log que admite ceros |
| **Estacionalidad** | Patrón que se repite cada año | La «temporada alta» de un servicio |
| **Intervalo de confianza** | Rango plausible del valor real | Margen de error de una encuesta |
| **Bootstrap** | Remuestrear con reemplazo para medir incertidumbre | Simular muchos «otros años» |
| **Test de Welch** | Prueba que compara dos medias | ¿El programa cambió algo o es ruido? |
| **p-valor** | Probabilidad de ver una diferencia así por azar | < 0,05 → significativa |
| **Pearson / Spearman** | Correlación lineal / por rangos | `COEF.DE.CORREL` / su versión robusta |
| **Variable de confusión** | Tercer factor que mueve a dos variables | El invierno, el tamaño de la comuna |
| **Autocorrelación** | Días seguidos se parecen entre sí | Por qué los p-valores de series diarias son optimistas |

---

## 9. Conexión con el Módulo Siguiente

En R2-03 aprendiste a describir, estimar con incertidumbre, contrastar y desconfiar de las correlaciones — sobre seis años de PM2.5 real.

En **R2-04 · Fundamentos de Machine Learning** usarás lo que viste aquí para construir tu primer modelo: **predecir el PM2.5 de mañana** en Cerro Navia con la temperatura, la humedad, el mes, el día de la semana y el PM2.5 de ayer. La estacionalidad y las correlaciones de hoy son, literalmente, las *features* de mañana — y la honestidad estadística será el **baseline** que el modelo tendrá que batir.

> 💡 **Pregunta para reflexionar:** si el PM2.5 de hoy se parece tanto al de ayer, ¿qué tan difícil será que un modelo le gane a la regla «mañana será igual que hoy»?
