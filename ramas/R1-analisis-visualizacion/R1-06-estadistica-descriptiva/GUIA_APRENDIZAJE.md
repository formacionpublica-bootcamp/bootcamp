# Guía de Aprendizaje — R1-06 · Estadística descriptiva

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 6 · Semana 7

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-06 · Estadística descriptiva |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 2 a 3 horas |
| **Nivel** | Básico-intermedio — requiere R1-02 a R1-05 |
| **Prerrequisitos** | Seleccionar columnas, `groupby`, filtrar con condiciones |
| **Competencia de salida** | Resumir e interpretar una variable con varias medidas a la vez (centro, dispersión, posición), detectar atípicos sin confundirlos con errores, y comparar grupos con la medida correcta y declarada |
| **Entregable** | Las 8 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula.csv`: matrícula oficial 2025 (MINEDUC) de 10.945 establecimientos, con estudiantes (`mat_total`), `cursos`, dependencia y ruralidad. Profundización: `comunas.csv` (población de 30 comunas de distintos tamaños, Censo 2024) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Casi toda decisión pública empieza con un resumen: «el establecimiento promedio tiene X estudiantes», «el curso típico tiene Y». Ese número define asignaciones, metas y titulares. Y casi siempre es **un promedio**, que con datos asimétricos cuenta una historia equivocada.

La matrícula escolar chilena es un ejemplo perfecto: conviven escuelas rurales de un solo estudiante con liceos de casi 4.000. El promedio es 324 estudiantes, pero **la mitad de los establecimientos tiene 175 o menos** y solo un tercio supera el promedio. Si financias o planificas con el promedio, te equivocas con la mayoría.

Este módulo enseña a resumir con **varias medidas a la vez**, a distinguir un dato **atípico** de un **error**, a no confundir «el curso del establecimiento típico» con «el curso del estudiante típico», y a comparar escuelas rurales y urbanas sin dejarse engañar.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Media** (`.mean()`) | Suma y reparte en partes iguales; sensible a extremos | PROMEDIO() |
| **Mediana** (`.median()`) | Valor del medio; robusta | MEDIANA() |
| **Razón media/mediana** | Alarma rápida de asimetría | — |
| **Desviación estándar** (`.std()`) | Dispersión en las unidades del dato | DESVEST() |
| **Coeficiente de variación** | Desviación / media: dispersión relativa | — |
| **Percentiles / cuartiles** (`.quantile()`) | Cortes de los datos ordenados | PERCENTIL() / CUARTIL() |
| **IQR** | Q3 − Q1: ancho del 50% central | — |
| **Regla del IQR** | Atípico = sobre Q3 + 1,5 × IQR | Los puntos sueltos del gráfico de caja |
| **Promedio de razones vs razón de totales** | Cada unidad pesa igual vs cada persona pesa igual | PROMEDIO de una columna de % vs SUMA/SUMA |
| **`groupby().agg([...])`** | Varias medidas por grupo | Tabla dinámica con varios valores |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Seleccionar una columna y aplicarle `.mean()` | ☐ |
| Filtrar filas con una condición | ☐ |
| Usar `groupby(...)[col].mean()` | ☐ |
| Crear una columna nueva dividiendo dos columnas | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar `matricula.csv` (10.945 establecimientos, 17 columnas). Trabajaremos con `mat_total`, `cursos` y `rural`.

---

### Sección 1 · Centro: media y mediana

🎯 **Objetivo:** Media **323,6**, mediana **175**: la media es **1,85 veces** la mediana.

💡 **Concepto clave:** Muchos establecimientos chicos y pocos muy grandes (asimetría a la derecha) arrastran la media hacia arriba. Comparar ambas es la primera alarma.

---

### Sección 2 · Dispersión

🎯 **Objetivo:** Rango **3.922**, desviación estándar **394,6** estudiantes, coeficiente de variación **1,22**.

💡 **Concepto clave:** Un CV mayor que 1 significa que la desviación supera a la propia media: establecimientos muy heterogéneos. El rango depende solo de dos valores (el de 1 y el de 3.923 estudiantes); por eso se complementa con el IQR.

---

### Sección 3 · Posición

🎯 **Objetivo:** Q1 **56**, Q3 **450**, IQR **394**, percentil 90 **852**.

💡 **Concepto clave:** «La mitad central de los establecimientos tiene entre 56 y 450 estudiantes» es una frase que una autoridad entiende y que no se deja mover por los extremos.

---

### Sección 4 · Atípicos con la regla del IQR

🎯 **Objetivo:** Límite = 450 + 1,5 × 394 = **1.041**. Hay **692** establecimientos atípicos (6,3%). El más grande es el Liceo Bicentenario Domingo Santa María (Arica), con 3.923 estudiantes.

💡 **Concepto clave:** **Atípico ≠ error.** En R1-04 un -1 era imposible y se marcaba como faltante; aquí un liceo grande es raro pero real. Se mira, se entiende, y no se borra.

⚠️ **Error frecuente:** Eliminar los atípicos «para que el promedio quede más representativo». Eso cambia el universo del análisis sin decirlo. Si quieres un valor típico robusto, usa la mediana.

---

### Sección 5 · Leer el sesgo

🎯 **Objetivo:** Solo el **34,4%** de los establecimientos supera el promedio.

💡 **Concepto clave:** Si el promedio fuera «típico», cerca de la mitad estaría por encima. Que sea un tercio confirma que unos pocos grandes lo levantan.

---

### Sección 6 · Estudiantes por curso

🎯 **Objetivo:** Promedio de razones **20,2** estudiantes por curso; razón de totales **25,9**.

💡 **Concepto clave:** No es un error que den distinto: responden preguntas distintas. El promedio de razones pesa igual a cada **establecimiento** (y hay muchas escuelas pequeñas con cursos chicos); la razón de totales pesa igual a cada **estudiante** (que suele estar en establecimientos grandes). Para «¿en qué tamaño de curso estudia un niño típico?», la razón de totales; para «¿cómo es el curso del establecimiento típico?», el promedio de razones. Lo importante es **decir cuál usaste**.

---

### Sección 7 · Comparar grupos: rural vs urbano

🎯 **Objetivo:** Mediana de estudiantes por curso: urbano **23,8** (7.856 establecimientos), rural **11,5** (3.089). El curso urbano típico es **2,1 veces** el rural.

💡 **Concepto clave:** Al comparar grupos, mira cantidad de casos, media **y** mediana. En lo rural se explica por las escuelas multigrado: pocos estudiantes por curso.

---

### Sección 8 · ¿En qué grupo miente más el promedio?

🎯 **Objetivo:** Razón media/mediana de `mat_total`: urbano **1,45** (416,0 / 286); rural **2,46** (88,7 / 36).

💡 **Concepto clave:** El grupo rural es mucho más asimétrico: unas pocas escuelas rurales grandes inflan su promedio. Decir «la escuela rural tiene en promedio 89 estudiantes» esconde que la mitad tiene **36 o menos**.

---

### Reflexión final

Para una autoridad que decide financiamiento rural, el número más honesto es la mediana (36 estudiantes), acompañada de cuántas escuelas son (3.089) y de un rango (por ejemplo, entre qué valores está la mitad central). El promedio solo, sin contexto, induce a error.

---

## 6. Guía de los 8 Ejercicios

### Ejercicio 1 — Media y mediana de la matrícula

**Pistas progresivas:**
- 🟢 Pista suave: Dos métodos de pandas para el centro, y una división entre ellos.
- 🟡 Pista media: `.mean()` y `.median()` sobre `df["mat_total"]`.
- 🔴 Pista directa: `media = df["mat_total"].mean()`, `mediana = df["mat_total"].median()`, `razon = media / mediana`.

**¿Qué significa el ✅?** Que mediste el centro de dos formas y detectaste la asimetría (razón 1,85).

---

### Ejercicio 2 — Mide la dispersión

**Pistas progresivas:**
- 🟢 Pista suave: El rango usa el máximo y el mínimo; el CV usa la desviación y la media.
- 🟡 Pista media: `.max() - .min()`, `.std()`, `desviacion / media`.
- 🔴 Pista directa: `rango = df["mat_total"].max() - df["mat_total"].min()`, `desviacion = df["mat_total"].std()`, `cv = desviacion / df["mat_total"].mean()`.

**¿Qué significa el ✅?** Que cuantificaste qué tan distintos son los establecimientos entre sí (CV 1,22).

---

### Ejercicio 3 — Cuartiles, IQR y percentil 90

**Pistas progresivas:**
- 🟢 Pista suave: Todos salen del mismo método, cambiando la proporción.
- 🟡 Pista media: `.quantile(0.25)`, `.quantile(0.75)`, `.quantile(0.90)`.
- 🔴 Pista directa: `q1 = df["mat_total"].quantile(0.25)`, `q3 = df["mat_total"].quantile(0.75)`, `iqr = q3 - q1`, `p90 = df["mat_total"].quantile(0.90)`.

**¿Qué significa el ✅?** Que puedes describir dónde está el 50% central (56 a 450) sin depender de los extremos.

---

### Ejercicio 4 — Cuenta los atípicos y mira el más grande

**Pistas progresivas:**
- 🟢 Pista suave: Calcula el límite con Q3 y el IQR, filtra lo que está sobre él, y busca la fila del máximo.
- 🟡 Pista media: `q3 + 1.5 * iqr`; `df[df["mat_total"] > limite_sup]`; `idxmax()`.
- 🔴 Pista directa: `limite_sup = q3 + 1.5 * iqr`, `atipicos = df[df["mat_total"] > limite_sup]`, `n_atipicos = len(atipicos)`, `el_mas_grande = df.loc[df["mat_total"].idxmax(), "nombre"]`.

**¿Qué significa el ✅?** Que detectaste 692 atípicos con una regla estándar, y viste que son liceos reales, no errores.

---

### Ejercicio 5 — Proporción de establecimientos sobre el promedio

**Pistas progresivas:**
- 🟢 Pista suave: Compara la columna con su promedio: obtienes `True`/`False`.
- 🟡 Pista media: El promedio de una columna de `True`/`False` es la proporción de `True`.
- 🔴 Pista directa: `pct_sobre_promedio = 100 * (df["mat_total"] > df["mat_total"].mean()).mean()`.

**¿Qué significa el ✅?** Que comprobaste que solo el 34,4% supera el promedio.

---

### Ejercicio 6 — Calcula ambas medidas de estudiantes por curso

**Pistas progresivas:**
- 🟢 Pista suave: Una es el promedio de una columna nueva; la otra divide dos sumas.
- 🟡 Pista media: `df["mat_total"] / df["cursos"]` para la columna; `.sum() / .sum()` para la razón de totales.
- 🔴 Pista directa: `df["est_por_curso"] = df["mat_total"] / df["cursos"]`, `promedio_de_razones = df["est_por_curso"].mean()`, `razon_de_totales = df["mat_total"].sum() / df["cursos"].sum()`.

**¿Qué significa el ✅?** Que entiendes por qué 20,2 y 25,9 son ambas correctas y responden preguntas distintas.

---

### Ejercicio 7 — Tamaño de curso por ruralidad

**Pistas progresivas:**
- 🟢 Pista suave: Agrupa por `rural` y pide varias medidas de una vez.
- 🟡 Pista media: `.agg(["count", "mean", "median"])`; la brecha divide la mediana del grupo 0 por la del grupo 1.
- 🔴 Pista directa: `resumen = df.groupby("rural")["est_por_curso"].agg(["count", "mean", "median"]).round(1)` y `brecha = resumen.loc[0, "median"] / resumen.loc[1, "median"]`.

**¿Qué significa el ✅?** Que comparaste dos grupos con varias medidas: el curso urbano típico es 2,1 veces el rural.

---

### Ejercicio 8 — Razón media/mediana por grupo

**Pistas progresivas:**
- 🟢 Pista suave: Es la razón del ejercicio 1, pero calculada dentro de cada grupo.
- 🟡 Pista media: `g.mean() / g.median()` da una Serie con índice 0 y 1.
- 🔴 Pista directa: `razones = g.mean() / g.median()` y `conclusion = "B"` (el grupo rural tiene la razón más alta: 2,46).

**¿Qué significa el ✅?** Que sabes en qué grupo el promedio engaña más, y por qué la mediana rural (36) cuenta mejor la realidad.

---

> 🔬 **En la profundización:** las mismas herramientas sobre la **población de 30 comunas** (Censo 2024). La media (141.762) es **2,33 veces** la mediana (60.722). Al sacar Puente Alto, la media cae **10,4%** y la mediana solo **4,8%**: eso es robustez. La regla del IQR marca como atípicas a Maipú, Puente Alto y Santiago; el **puntaje z** (|z| > 2) solo a 2 (Puente Alto, z = 2,71, y Maipú, 2,30), porque con datos asimétricos la media y la desviación ya vienen infladas por los extremos. Ojo: son 30 comunas elegidas por tamaño, no una muestra de todo Chile.

---

## 7. Autoevaluación Final

**Pregunta 1:** La media de matrícula es 324 y la mediana 175. ¿Qué indica?

- A) Que hay un error de cálculo
- B) Asimetría a la derecha: muchos establecimientos chicos y pocos muy grandes que levantan la media ✅
- C) Que la mayoría de los establecimientos tiene más de 324 estudiantes
- D) Que los datos son simétricos

**Explicación:** Cuando la media supera claramente a la mediana, unos pocos valores grandes la arrastran.

---

**Pregunta 2:** Un liceo con 3.923 estudiantes es atípico según la regla del IQR. ¿Qué haces?

- A) Lo borras para no distorsionar
- B) Lo reemplazas por la mediana
- C) Lo revisas: si es real, se queda; usas medidas robustas si necesitas un valor típico ✅
- D) Lo corriges a 1.041

**Explicación:** Atípico ≠ error. Borrar datos reales cambia el universo del análisis.

---

**Pregunta 3:** Promedio de razones (20,2) y razón de totales (25,9) de estudiantes por curso. ¿Cuál responde «en qué tamaño de curso estudia el niño típico»?

- A) El promedio de razones
- B) La razón de totales, porque cada estudiante pesa igual ✅
- C) Ninguna
- D) Dan lo mismo

**Explicación:** El promedio de razones pesa igual a cada establecimiento, y hay muchas escuelas pequeñas con cursos chicos.

---

**Pregunta 4:** ¿Para qué sirve el coeficiente de variación?

- A) Para medir el centro
- B) Para comparar la dispersión de variables con unidades o escalas distintas ✅
- C) Para detectar duplicados
- D) Es lo mismo que la desviación estándar

**Explicación:** Al dividir por la media, el CV no tiene unidades: sirve para comparar.

---

**Pregunta 5:** «La escuela rural tiene en promedio 89 estudiantes». ¿Qué le falta a esa frase?

- A) Nada, es correcta
- B) Decir que la mitad de las escuelas rurales tiene 36 o menos: el promedio está inflado por unas pocas grandes ✅
- C) Redondear a 90
- D) Compararla con la región Metropolitana

**Explicación:** En el grupo rural la media es 2,46 veces la mediana. Sin la mediana, la frase induce a error.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Media** | Promedio aritmético | El «promedio» de los informes |
| **Mediana** | Valor del medio | El establecimiento típico |
| **Asimetría** | Los datos se estiran más hacia un lado | Muchas escuelas chicas, pocos liceos gigantes |
| **Desviación estándar** | Distancia típica a la media | Cuán parejos son los casos |
| **Coeficiente de variación** | Desviación / media | Dispersión comparable entre indicadores |
| **Percentil** | Valor bajo el cual queda un % de los datos | «El 90% tiene menos de 852 estudiantes» |
| **IQR** | Ancho del 50% central | El rango de la mayoría |
| **Atípico** | Valor lejos del resto según una regla | El caso que merece una mirada, no un borrado |
| **Promedio de razones** | Promediar un indicador calculado por unidad | Promedio de tasas por comuna |
| **Razón de totales** | Total / total | Tasa nacional |
| **Puntaje z** | A cuántas desviaciones de la media está un dato | — |

---

## 9. Conexión con el Módulo Siguiente

En R1-06 aprendiste a resumir sin engañarte: varias medidas juntas, atípicos que no son errores, razones que dependen de quién pesa, y grupos comparados con la medida correcta.

En **R1-07 · Visualización exploratoria** verás estas mismas distribuciones en gráficos: histogramas, cajas y comparaciones que muestran de un vistazo la asimetría y los atípicos que hoy calculaste.

> 💡 **Pregunta para reflexionar:** ¿Qué indicador de tu servicio se reporta solo como promedio? ¿Cambiaría la decisión si se reportara la mediana?
