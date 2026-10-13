# Guía de Aprendizaje — R1-07 · Visualización exploratoria: ver para entender

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 7 · Semana 8

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-07 · Visualización exploratoria |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Intermedio — requiere R1-02 (pandas) y R1-06 (estadística descriptiva) |
| **Prerrequisitos** | Filtrar DataFrames, `groupby`, cuantiles |
| **Competencia de salida** | Usar histogramas, boxplots, dispersión y barras para descubrir patrones en datos públicos |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula.csv` — matrícula oficial 2025 (MINEDUC). Profundización: `sismos.csv` — 1.601 sismos M≥4,5 de Chile 2020–2025 (catálogo USGS) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Una tabla de 10.945 filas no se puede *leer*. Un gráfico sí.

La visualización exploratoria es la herramienta más rápida para entender un dataset nuevo: en cuatro gráficos descubres si la variable tiene valores extremos, si los grupos difieren de verdad, si dos variables se mueven juntas y qué categoría concentra el fenómeno. Todo eso **antes** de calcular un solo modelo o escribir un informe.

Este módulo es para **descubrir** (gráficos para ti). El siguiente, R1-08, es para **comunicar** (gráficos para otros, con las reglas éticas de la visualización pública). La distinción importa: un gráfico exploratorio puede ser feo; un gráfico comunicativo no puede ser engañoso.

---

## 3. Mapa Conceptual del Módulo

| Gráfico | ¿Qué pregunta responde? | Ejemplo en este módulo |
|---------|------------------------|------------------------|
| **Histograma** | ¿Cómo se distribuye una variable? | ¿Predominan las escuelas chicas o grandes? |
| **Boxplot** | ¿Difieren los grupos? | ¿Los particulares pagados son más grandes que los municipales? |
| **Dispersión** | ¿Se relacionan dos variables? | ¿Más cursos implica más estudiantes? |
| **Barras** | ¿Qué categoría concentra más? | ¿Qué región tiene más matrícula? |
| **`clip(upper=p99)`** | Recortar extremos para ver la masa de los datos | Sin el colegio gigante, ¿cómo se ve el resto? |
| **`sample(n, random_state)`** | Muestra reproducible para no saturar el gráfico | 800 puntos en vez de 10.945 |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Filtrar un DataFrame con una condición (`df[df["col"] == valor]`) | ☐ |
| Usar `groupby` con `sum()` | ☐ |
| Explicar qué es un percentil (p99) | ☐ |

Si respondiste No a alguna, repasa R1-02 y R1-06 antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación del entorno

🎯 **Objetivo:** Cargar la matrícula 2025 y tener matplotlib listo.

💡 **Concepto clave:** `matplotlib` es la librería base de gráficos en Python. El patrón que usarás siempre: `fig, ax = plt.subplots()` crea la figura (el lienzo) y los ejes (donde se dibuja); luego llamas métodos sobre `ax` (`ax.hist`, `ax.boxplot`, `ax.scatter`, `ax.barh`); al final `plt.show()` muestra el resultado.

✅ **Señal de que entendiste:** Ves la tabla con `mat_total`, `dependencia`, `cursos`, `region`.

---

### Sección 1 · Histograma

🎯 **Objetivo:** Ver la forma de la distribución del tamaño de los establecimientos.

💡 **Concepto clave:** El histograma parte el rango de la variable en **bins** (cajones) y cuenta cuántos valores caen en cada uno. La matrícula tiene **cola larga**: la mayoría de los establecimientos son chicos y unos pocos son enormes. Por eso se recorta al percentil 99 con `clip(upper=...)`: sin ese recorte, los pocos colegios gigantes aplastan el gráfico y no se ve nada.

🔍 **Qué hace el código:**
- `df["mat_total"].quantile(0.99)` → el valor bajo el cual está el 99% de los establecimientos
- `.clip(upper=...)` → reemplaza los valores por sobre ese tope por el tope mismo (no los elimina)
- `ax.hist(matriculas, bins=40)` → dibuja el histograma con 40 cajones

⚠️ **Error frecuente:** Confundir `clip` con filtrar. `clip` conserva las 10.945 filas (cambia los valores extremos); un filtro las eliminaría.

✅ **Señal de que entendiste:** Puedes decir dónde está la moda del tamaño de establecimiento mirando el gráfico.

---

### Sección 2 · Boxplot

🎯 **Objetivo:** Comparar la distribución del tamaño entre dependencias.

💡 **Concepto clave:** El boxplot resume cada grupo en 5 números: mínimo, Q1, mediana, Q3, máximo (más los outliers como puntos). Poner varios lado a lado permite comparar grupos de un vistazo: ¿la mediana de los particulares pagados es mayor? ¿la caja municipal es más ancha (más heterogénea)?

🔍 **Qué hace el código:**
- `grupos = [df[df["dependencia"] == d]["mat_total"]... for d in orden]` → una lista de Series, una por dependencia
- `ax.boxplot(grupos, tick_labels=[...])` → un boxplot por elemento de la lista

✅ **Señal de que entendiste:** Puedes decir qué dependencia tiene la mediana de matrícula más alta sin calcular nada.

---

### Sección 3 · Dispersión

🎯 **Objetivo:** Ver si el número de cursos y la matrícula se mueven juntos.

💡 **Concepto clave:** Cada punto es un establecimiento: x = cursos, y = estudiantes. Si los puntos forman una franja ascendente, hay relación positiva. El grosor de la franja también informa: cursos con ~45 estudiantes y cursos con ~15 conviven en el sistema (¡y eso es un hallazgo!). Se grafica una **muestra** de 800 con `random_state=42` para que el gráfico no se sature y sea reproducible.

⚠️ **Error frecuente:** Olvidar `alpha=0.4` (transparencia). Con puntos sólidos, las zonas densas se ven como una mancha uniforme.

✅ **Señal de que entendiste:** Puedes explicar qué significa un punto que está muy por sobre la franja (muchos estudiantes por curso).

---

### Sección 4 · Barras

🎯 **Objetivo:** Comparar la matrícula total entre las 16 regiones.

💡 **Concepto clave:** Para categorías, la barra es el gráfico honesto por defecto. `barh` (horizontal) deja leer los nombres largos de las regiones sin girar la cabeza. `.sort_values()` ordena de menor a mayor, lo que convierte el gráfico en un ranking instantáneo.

✅ **Señal de que entendiste:** El gráfico muestra la Metropolitana muy por sobre el resto — y puedes decir cuáles son las 3 regiones siguientes.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Dibuja el histograma de la matrícula

**Objetivo:** Graficar la distribución del tamaño de los establecimientos.
**Habilidad que entrena:** `ax.hist`, manejo de colas largas con `clip`.

**Pistas progresivas:**
- 🟢 Pista suave: El método para histogramas se llama como el gráfico, y vive en `ax`.
- 🟡 Pista media: Recibe la serie de datos y el número de cajones: `ax.hist(datos, bins=N)`.
- 🔴 Pista directa: `ax.hist(matriculas, bins=40, color="#4240e5")`.

**¿Qué significa el ✅?** Que la figura existe y tiene barras dibujadas (`ax.patches`).

---

### Ejercicio 2 — Boxplot de la matrícula por dependencia

**Objetivo:** Comparar la distribución del tamaño entre 4 dependencias.
**Habilidad que entrena:** `ax.boxplot` sobre una lista de grupos.

**Pistas progresivas:**
- 🟢 Pista suave: `grupos` ya es una lista con los datos de cada dependencia. El método recibe esa lista completa.
- 🟡 Pista media: `ax.boxplot(grupos, tick_labels=nombres)` — un boxplot por grupo, con su etiqueta.
- 🔴 Pista directa: `ax.boxplot(grupos, tick_labels=["Municipal", "P. subv.", "P. pagado", "SLEP"])`.

**¿Qué significa el ✅?** Que la figura existe y los 4 grupos están construidos.

---

### Ejercicio 3 — Dispersión cursos vs matrícula

**Objetivo:** Graficar la relación entre número de cursos y estudiantes.
**Habilidad que entrena:** `ax.scatter`, muestreo reproducible.

**Pistas progresivas:**
- 🟢 Pista suave: El gráfico de dispersión recibe dos columnas: la de x y la de y.
- 🟡 Pista media: `ax.scatter(x, y, s=tamaño, alpha=transparencia)`.
- 🔴 Pista directa: `ax.scatter(m["cursos"], m["mat_total"], s=10, alpha=0.4, color="#ff6b35")`.

**¿Qué significa el ✅?** Que la figura tiene una colección de puntos (`ax.collections`).

---

### Ejercicio 4 — Matrícula por región

**Objetivo:** Ranking regional con barras horizontales.
**Habilidad que entrena:** `groupby` + `sort_values` + `ax.barh`.

**Pistas progresivas:**
- 🟢 Pista suave: `g` ya tiene las regiones (índice) y sus totales (valores), ordenados.
- 🟡 Pista media: Las barras horizontales usan `barh(etiquetas, valores)`.
- 🔴 Pista directa: `ax.barh(g.index, g.values, color="#4240e5")`.

**¿Qué significa el ✅?** Que hay una barra por cada una de las 16 regiones.

---

> 🔬 **En la profundización** cambia el dominio pero no las herramientas: **1.601 sismos reales de Chile** (USGS, 2020–2025). Verás la ley de Gutenberg-Richter con una escala logarítmica, detectarás sismos anormalmente profundos con la regla IQR y compararás la sismicidad de las zonas del país con pequeños múltiplos. Si puedes hacer eso, la técnica ya es tuya — no del dataset.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué se recorta la matrícula al percentil 99 antes del histograma?

- A) Porque los datos sobre el p99 son errores
- B) Porque sin recorte, los pocos establecimientos gigantes comprimen el resto del gráfico y no se ve la forma de la distribución ✅
- C) Porque matplotlib no acepta valores grandes
- D) Para que el gráfico corra más rápido

**Explicación:** Los valores extremos son reales (colegios enormes), pero estiran el eje x. `clip` los lleva al tope para poder ver la masa de los datos. En un análisis formal, se reportaría el recorte.

---

**Pregunta 2:** En un boxplot, ¿qué representa la línea dentro de la caja?

- A) El promedio
- B) La mediana ✅
- C) El valor más frecuente
- D) El máximo

**Explicación:** La caja va de Q1 a Q3 y la línea interior es la mediana (Q2). El promedio no aparece en un boxplot estándar.

---

**Pregunta 3:** ¿Para qué sirve `random_state=42` en `df.sample(800, random_state=42)`?

- A) Para que la muestra tenga exactamente 800 filas
- B) Para que la muestra sea siempre la misma cada vez que se ejecuta (reproducibilidad) ✅
- C) Para ordenar la muestra
- D) Es obligatorio en pandas

**Explicación:** Sin semilla, cada ejecución tomaría una muestra distinta y el gráfico cambiaría. Con semilla fija, tu análisis es reproducible: cualquiera obtiene lo mismo.

---

**Pregunta 4:** Ves una franja ascendente y angosta en un gráfico de dispersión. ¿Qué concluyes?

- A) Las dos variables tienen una relación positiva fuerte ✅
- B) Las dos variables no se relacionan
- C) Hay un error en los datos
- D) La variable y causa la variable x

**Explicación:** Franja ascendente = relación positiva; angosta = poca dispersión (relación fuerte). Ojo: relación no es causalidad — eso se discute en R1-08.

---

**Pregunta 5:** ¿Cuándo conviene `barh` (horizontal) en vez de `bar` (vertical)?

- A) Nunca, son equivalentes
- B) Cuando las etiquetas de las categorías son largas y muchas (como 16 nombres de regiones) ✅
- C) Cuando los valores son negativos
- D) Cuando hay menos de 5 categorías

**Explicación:** Con barras horizontales, las etiquetas se leen de corrido en el eje y. Con 16 regiones en vertical, los nombres chocarían o habría que girarlos.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Histograma** | Cuenta de valores por rango (bins) | Distribución de sueldos por tramo |
| **Bin** | Cada cajón del histograma | Tramo de la tabla |
| **Cola larga** | Pocos valores enormes junto a muchos chicos | Pocos contratos gigantes, muchos menores |
| **`clip(upper=x)`** | Lleva los valores sobre x al valor x | Topear para visualizar |
| **Boxplot** | Resumen de 5 números por grupo, en cajas | Comparar unidades de un vistazo |
| **Outlier** | Valor anormalmente lejos del resto | El caso que amerita revisión |
| **Dispersión (scatter)** | Un punto por observación en dos ejes | Cruce de dos indicadores |
| **`alpha`** | Transparencia de los puntos | Ver densidad en zonas pobladas |
| **Pequeños múltiplos** | Misma gráfica repetida por grupo | Una lámina por región, mismo formato |
| **Escala logarítmica** | Eje que crece por múltiplos (1, 10, 100…) | Ver lo chico y lo enorme en un mismo gráfico |
| **Regla IQR** | Outlier si está a más de 1,5·IQR de la caja | Criterio estándar de caso atípico |

---

## 9. Conexión con el Módulo Siguiente

En R1-07 aprendiste a **ver para entender**: cuatro gráficos que revelan forma, grupos, relaciones y rankings. Son gráficos para ti, para descubrir.

En **R1-08 · Visualización para comunicar + ética** darás el paso profesional: convertir el hallazgo en un gráfico para **otros** — con título que afirma, ejes honestos, fuentes citadas — y conocerás las reglas éticas de la visualización pública: ejes truncados, cherry-picking, correlación vs causalidad. Con datos como la brecha de matrícula por dependencia, la honestidad del gráfico no es un detalle técnico: es un deber público.

> 💡 **Pregunta para reflexionar:** De los cuatro gráficos que hiciste, ¿cuál mostrarías a tu jefatura para pedir una decisión? ¿Qué le falta a ese gráfico para sostenerse solo, sin que tú lo expliques al lado?
