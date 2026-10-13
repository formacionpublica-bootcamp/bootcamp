# Guía de Aprendizaje — R1-CAP · Capstone: análisis sobre datos de tu organismo

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo final · Semanas 11–12

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-CAP · Capstone de análisis |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 2 semanas (proyecto, no lección) |
| **Nivel** | Cierre de rama — integra todos los módulos R1 |
| **Prerrequisitos** | R1-00 a R1-09 completos |
| **Competencia de salida** | Ejecutar un análisis de datos público de punta a punta y comunicarlo con integridad |
| **Entregable** | Notebook reproducible + figura honesta + brief de una plana |
| **Dataset** | **El tuyo.** La plantilla usa `matricula.csv` (MINEDUC) como ejemplo; elige datos de tu organismo, del banco del bootcamp o de datos.gob.cl |

---

## 2. ¿Para qué me sirve esto como funcionario público?

El capstone es el momento en que el curso deja de darte el problema. Hasta aquí, cada módulo traía su dataset y su pregunta; ahora **la pregunta es tuya** — y eso es exactamente lo que pasa el lunes siguiente en tu servicio.

El entregable no es «un notebook que corre»: es la evidencia de que puedes tomar un dato público real, limpiarlo con criterio, resumirlo para responder una pregunta de gestión, mostrarlo con una figura que no engaña, y escribir el brief de una plana que una jefatura lee en dos minutos y sabe qué hacer. Ese paquete — notebook + figura + brief — es tu **portafolio**: sirve para tu servicio, para postular a otros y para el certificado de la rama.

**La elección del dataset importa.** Orden de preferencia: (1) datos de tu propio organismo, porque el capstone vale el doble si responde una pregunta real; (2) el banco del bootcamp — `matricula`, `aire_diario`, `sismos`, `fichas`, `reclamos`, todos reales y curados; (3) cualquier dataset de datos.gob.cl, cuya API ya sabes usar desde R1-01.

---

## 3. Mapa Conceptual del Módulo

| Etapa | Módulos donde la aprendiste | Qué produce aquí |
|-------|----------------------------|------------------|
| **Enmarcar** | R1-08 (mensaje) | La pregunta de gestión en una frase |
| **Cargar** | R1-01 | El dato en el notebook, en vivo o caché |
| **Limpiar** | R1-04 | `df_limpio` sin nulos ni duplicados |
| **Analizar** | R1-02, R1-03, R1-06 | Una tabla `sum/mean/count` por dimensión |
| **Visualizar** | R1-07, R1-08 | Una figura honesta (eje desde 0, título, unidades) |
| **Comunicar** | R1-08 | El brief de una plana con límites declarados |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Cargar un CSV con el patrón en vivo o caché | ☐ |
| Limpiar nulos y duplicados con criterio | ☐ |
| Agrupar con `groupby(...).agg([...])` | ☐ |
| Hacer una figura que pasa el checklist de honestidad de R1-08 | ☐ |

Si alguna falla, vuelve al módulo correspondiente — el capstone los usa todos.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 1 · Enmarca el problema

🎯 **Objetivo:** Una frase que nombre la pregunta de gestión ANTES de tocar el dato.

💡 **Concepto clave:** La pregunta manda sobre el análisis, no al revés. «¿Dónde se concentran los establecimientos rurales chicos y qué apoyo habilita ese hallazgo?» es una pregunta de gestión; «analizar la matrícula» no lo es. La prueba: tu pregunta debe terminar en una **decisión posible**.

⚠️ **Error frecuente:** Partir explorando el dato «a ver qué sale». Sin pregunta, todo hallazgo parece relevante y el brief termina sin recomendación.

---

### Sección 2 · Carga y limpia

🎯 **Objetivo:** Construir `df_limpio`, tu base de trabajo.

💡 **Concepto clave:** `dropna().drop_duplicates().copy()` es el mínimo; tu dataset puede necesitar más (tipos, strings con espacios, códigos). Documenta en una celda markdown **qué limpiaste y por qué** — la limpieza no documentada es un hallazgo invisible para quien revisa.

✅ **Señal de que entendiste:** `n_nulos == 0` y sabes decir cuántas filas se fueron y si eso sesga algo.

---

### Sección 3 · Analiza

🎯 **Objetivo:** Una función `resumen_*(d, por=...)` que agrega tu variable clave por una dimensión.

💡 **Concepto clave:** `agg(["sum", "mean", "count"])` entrega las tres miradas de una vez: magnitud total, valor típico y tamaño del grupo. La función con parámetro `por=` te permite girar el análisis a otra dimensión (región → dependencia → comuna) sin reescribir nada — así verificas que tu hallazgo es robusto.

✅ **Señal de que entendiste:** La tabla responde directamente tu pregunta del paso 1, y puedes girarla a una segunda dimensión en una línea.

---

### Sección 4 · Visualiza (honesto)

🎯 **Objetivo:** LA figura del capstone: la que va al brief.

💡 **Concepto clave:** Todo R1-08 en una imagen: eje desde 0, título que afirma con año, etiquetas con unidades. El check lo verifica en parte (`ax.get_ylim()[0] == 0`), pero el estándar completo es tuyo: pásale mentalmente `revisar_grafico()`.

✅ **Señal de que entendiste:** La figura se sostiene sola: alguien que no ha visto el notebook entiende el hallazgo.

---

### Sección 5 · Comunica

🎯 **Objetivo:** El brief de una plana: pregunta, hallazgo con el número clave, recomendación accionable, límites.

💡 **Concepto clave:** La sección de **límites y ética** es la que distingue un análisis profesional: qué NO dice tu dato. Con matrícula, por ejemplo: es la foto de abril, no captura movimiento durante el año, y «matrícula» no es «asistencia». Declarar límites no debilita tu hallazgo — lo hace confiable.

---

## 6. Guía de los 3 Ejercicios

### Ejercicio 1 — Limpia el DataFrame

**Pistas progresivas:**
- 🟢 Pista suave: Son dos métodos encadenados de pandas más una copia.
- 🟡 Pista media: Uno elimina filas con nulos, el otro las repetidas.
- 🔴 Pista directa: `df_limpio = df.dropna().drop_duplicates().copy()`.

**¿Qué significa el ✅?** Cero nulos y no más filas que el original.

---

### Ejercicio 2 — Escribe `resumen_matricula`

**Pistas progresivas:**
- 🟢 Pista suave: Agrupar por la dimensión `por`, agregar la variable clave con tres funciones, ordenar por la suma.
- 🟡 Pista media: `groupby(por)["mat_total"].agg(["sum", "mean", "count"])` y ordena con `sort_values("sum", ascending=False)`.
- 🔴 Pista directa: `return d.groupby(por)["mat_total"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)`.

**¿Qué significa el ✅?** La tabla tiene la columna `sum` y una fila por región.

---

### Ejercicio 3 — Grafica el top 6

**Pistas progresivas:**
- 🟢 Pista suave: Le faltan al gráfico las tres marcas de honestidad de R1-08.
- 🟡 Pista media: `set_ylim(bottom=0)`, `set_title(...)`, `set_xlabel(...)`, `set_ylabel(...)`.
- 🔴 Pista directa: `ax.set_ylim(bottom=0); ax.set_title("Matrícula por región, 2025 (top 6)"); ax.set_xlabel("Región"); ax.set_ylabel("Estudiantes matriculados")`.

**¿Qué significa el ✅?** Figura creada y eje desde 0 — el resto de la honestidad la evalúa la rúbrica.

---

> 🔬 **En la profundización:** la **segunda dimensión** de análisis (por dependencia — ¿tu hallazgo regional sobrevive al girar la mirada?) y **exportar la figura como PNG** para pegarla en el brief.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Cuál es el orden correcto del capstone?

- A) Explorar el dato → encontrar algo → inventar la pregunta
- B) Pregunta de gestión → cargar → limpiar → analizar → visualizar → comunicar ✅
- C) Visualizar primero para ver qué hay
- D) Escribir el brief y luego buscar datos que lo apoyen

**Explicación:** La pregunta manda. El orden D es, además, un problema de integridad: buscar datos para una conclusión ya tomada.

---

**Pregunta 2:** ¿Por qué la limpieza debe documentarse en el notebook?

- A) Por formalidad
- B) Porque las filas eliminadas pueden sesgar el resultado, y quien revisa debe poder auditar esa decisión ✅
- C) Para que el notebook sea más largo
- D) No es necesario documentarla

**Explicación:** Reproducibilidad incluye las decisiones, no solo el código. «Eliminé 200 filas sin región» cambia la lectura de un ranking regional.

---

**Pregunta 3:** ¿Qué hace valioso el parámetro `por=` en la función de análisis?

- A) Es un requisito de pandas
- B) Permite girar el análisis a otra dimensión sin reescribir, para verificar que el hallazgo es robusto ✅
- C) Hace el código más corto
- D) Mejora el rendimiento

**Explicación:** Un hallazgo que solo aparece con un corte específico es frágil. Girar la dimensión en una línea es tu prueba de robustez.

---

**Pregunta 4:** ¿Qué va en «Límites y ética» del brief?

- A) Las limitaciones de Python
- B) Lo que el dato NO dice: cobertura temporal, definiciones (matrícula ≠ asistencia), sesgos posibles ✅
- C) Una disculpa por los errores
- D) Los módulos que faltaron por hacer

**Explicación:** Declarar el alcance real del dato es lo que permite que la recomendación se use bien — y es el estándar ético del análisis público.

---

**Pregunta 5:** ¿Cuál es el mejor dataset para TU capstone?

- A) El más grande disponible
- B) Uno de tu propio organismo que responda una pregunta real de gestión ✅
- C) Siempre matricula.csv
- D) Uno que ya venga limpio

**Explicación:** La rúbrica premia pertinencia. La plantilla con matrícula es el andamiaje; el capstone que te sirve de portafolio es el que habla de tu servicio.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Capstone** | Proyecto integrador de cierre | El informe anual que te toca liderar |
| **Pregunta de gestión** | Pregunta que termina en una decisión posible | El encargo real detrás del análisis |
| **`agg(["sum","mean","count"])`** | Tres agregaciones de una vez | Total, promedio y n de la tabla resumen |
| **Robustez** | El hallazgo sobrevive a otros cortes | «¿Y si lo miramos por dependencia?» |
| **Brief de una plana** | Pregunta + hallazgo + recomendación + límites | La minuta ejecutiva |
| **Límites del dato** | Lo que el dato no dice | La letra chica honesta |
| **Portafolio** | Evidencia mostrable de tu capacidad | El capstone bien hecho |
| **Rúbrica** | Criterios públicos de evaluación | Pauta de corrección conocida de antemano |

---

## 9. Conexión con lo que sigue

Con el capstone cierras la rama R1: eres capaz de tomar un dato público y convertirlo en una decisión comunicada con integridad.

Desde aquí hay dos caminos: la rama **R2 · Científico de Datos** (modelar y predecir: regresión, árboles, validación — sobre la calidad del aire de Chile) o la rama **R3 · IA Aplicada** (NLP, LLMs y RAG — sobre los trámites de ChileAtiende). Tu capstone es prerrequisito conceptual de ambas: modelar sin saber limpiar y comunicar es construir sobre arena.

> 💡 **Pregunta para reflexionar:** ¿Qué pregunta de tu servicio quedó SIN responder en tu capstone por falta de datos? Esa pregunta — y conseguir ese dato — puede ser tu proyecto real de los próximos meses.
