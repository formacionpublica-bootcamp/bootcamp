# Guía de Aprendizaje — R2-CAP · Capstone: modelo predictivo de punta a punta

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Capstone · Semanas 17–18

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R2-CAP · Capstone — modelo predictivo de punta a punta |
| **Rama** | R2 — Científico de Datos |
| **Duración estimada** | 2 semanas de proyecto (la plantilla de ejemplo: 90 minutos) |
| **Nivel** | Integrador — requiere R2-04 a R2-09 (R2-10 si tus datos tienen fecha) |
| **Prerrequisitos** | Pipelines, partición temporal, F1/recall/precision, fuga de datos, ficha de modelo |
| **Competencia de salida** | Ejecutar el ciclo de vida de un modelo de forma responsable: enmarcar una decisión pública, construir *features* sin fuga, validar contra una línea base y documentar con ficha y brief |
| **Entregable** | Notebook reproducible (las 4 celdas de chequeo en ✅ con el ejemplo, o adaptadas a tus datos) + ficha de modelo + brief de una plana |
| **Dataset** | Ejemplo: `aire_diario.csv` (PM2.5 diario, 14 estaciones SINCA, 2020–2025). Para tu proyecto: datos de tu organismo > banco del bootcamp > datos.gob.cl |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Un modelo predictivo en el Estado no se juzga por su F1: se juzga por la **decisión** que mejora y por los **errores** que comete con personas y territorios reales. Este capstone te pide recorrer el camino completo una vez, con la honestidad como criterio central: ¿le gana el modelo a la regla simple que ya usaría cualquiera?, ¿para quién funciona peor?, ¿qué pasa si alguien lo usa para lo que no fue diseñado?

El ejemplo guía es concreto: anticipar con un día de aviso si una estación de monitoreo superará la norma diaria de PM2.5 (50 µg/m³). El resultado es una lección en sí misma: el modelo obtiene un F1 de **0,630** y la regla «si hoy superó, mañana también» obtiene **0,619**. Un modelo que apenas le gana a la persistencia **no es un fracaso**: es un hallazgo que se reporta, y que orienta qué datos faltan (por ejemplo, meteorología). Lo que sí sería un fracaso es esconderlo.

---

## 3. Mapa Conceptual del Módulo

| Concepto | ¿Qué hace? | Equivalente en Excel |
|----------|-----------|----------------------|
| **Enmarcar** | Escribir la decisión, el usuario y el objetivo antes del modelo | La pregunta que va en el título del informe |
| **Unidad de análisis** | Qué es una fila (aquí: una estación en un día) | Qué representa cada fila de la planilla |
| **Fuga de datos** | Una *feature* que contiene la respuesta o viene del futuro | Una columna que se llenó después del hecho |
| **Partición temporal** | Entrenar con el pasado, probar con el futuro | Proyectar el último año tapando sus datos |
| **Pipeline** | Preprocesamiento + modelo en un solo objeto | Una plantilla con las fórmulas encadenadas |
| **Línea base** | La regla simple que el modelo debe superar | La proyección inercial («igual que ayer») |
| **F1 / recall / precision** | Métricas para clases raras | Aciertos sobre los casos que importan |
| **Ficha de modelo + brief** | Documentación técnica + mensaje para quien decide | Anexo metodológico + resumen ejecutivo |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Explicar con un ejemplo qué es la fuga de datos | ☐ |
| Armar un `Pipeline` con `ColumnTransformer` y un clasificador | ☐ |
| Explicar por qué en datos con fecha no se baraja al separar entrenamiento y prueba | ☐ |
| Interpretar *recall* y *precision* en palabras de la decisión («de cada 10 episodios, avisamos…») | ☐ |
| Escribir una ficha de modelo (R2-09) | ☐ |

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar el dataset (ejemplo: 30.674 filas de `aire_diario.csv`).

💡 **Concepto clave:** La variable `CSV` es el único lugar donde cambias el archivo. Si usas datos de tu organismo, revisa antes que no contengan datos personales innecesarios para la pregunta.

---

### Sección 1 · Enmarca el problema

🎯 **Objetivo:** Escribir la decisión pública, quién usa el modelo y la regla simple contra la que se medirá.

💡 **Concepto clave:** El orden de preferencia de datos es **tu organismo > banco del bootcamp > datos.gob.cl**. El criterio de **Pertinencia** de la rúbrica premia que el proyecto responda una pregunta real de gestión.

⚠️ **Error frecuente:** Empezar por el algoritmo («quiero usar un bosque aleatorio») en vez de por la decisión.

---

### Sección «Tabla de modelado»

🎯 **Objetivo:** Entender la tabla de ejemplo: 28.786 filas estación-día, con 4,4% de días seguidos de un episodio.

💡 **Concepto clave:** La función usa un **calendario completo** por estación (`asfreq("D")`) para que «ayer» y «mañana» sean de verdad el día anterior y el siguiente. La tabla incluye a propósito `pm25_manana`: es la respuesta.

---

### Sección 2 · Features sin fuga

🎯 **Objetivo:** Elegir solo columnas conocidas **hoy**.

💡 **Concepto clave:** Si incluyes `pm25_manana`, el F1 en la prueba sube a ≈ 0,99. Ese número no es un logro: es la señal de alarma clásica de la fuga. **Desconfía de los resultados demasiado buenos.**

---

### Sección 3 · Partición temporal

🎯 **Objetivo:** Entrenar con 2020–2024 (24.288 filas) y probar con 2025 (4.498 filas, 154 episodios).

💡 **Concepto clave:** El PM2.5 de hoy se parece mucho al de ayer. Si barajas, el modelo se entrena con el día anterior y el siguiente de cada día de prueba: no es la situación que enfrentará en producción.

---

### Sección 4 · Entrena el modelo

🎯 **Objetivo:** Pipeline con one-hot (estación, mes) + escalado (numéricas) + regresión logística.

💡 **Concepto clave:** Empezar por un modelo **simple y explicable** es una virtud. Si un modelo más complejo no le gana claramente, no lo justifica.

---

### Sección 5 · Evalúa contra la línea base

🎯 **Objetivo:** Comparar F1 y *recall* del modelo con los de la persistencia.

💡 **Concepto clave:** Modelo: F1 **0,630**, *recall* **0,552**, *precision* **0,733**. Persistencia: F1 **0,619**, *recall* **0,623**, *precision* **0,615**. El modelo da menos falsas alarmas pero **avisa menos episodios** que la regla simple. ¿Cuál es mejor? Depende de qué error le cuesta más a la decisión — y eso va en el brief.

✅ **Señal de que entendiste:** Puedes explicar en una frase, sin jerga, qué gana y qué pierde el modelo frente a la regla simple.

---

### Secciones 6 y 7 · Ficha de modelo y brief

🎯 **Objetivo:** Documentar para dos públicos: el técnico (ficha) y quien decide (brief).

💡 **Concepto clave:** La ficha dice **qué no hacer** con el modelo. El brief dice **qué hacer** con el resultado. Ninguno de los dos esconde la línea base.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Define FEATURES y el objetivo, sin fuga

**Pistas progresivas:**
- 🟢 Pista suave: Pregúntate por cada columna: ¿la conozco hoy, antes de que pase mañana?
- 🟡 Pista media: Todas las columnas con «manana» vienen del futuro.
- 🔴 Pista directa: `FEATURES = ["estacion", "pm25", "pm25_ayer", "media_7d", "mes"]`.

**¿Qué significa el ✅?** Que tu modelo solo usa información disponible al momento de predecir.

---

### Ejercicio 2 — Separa entrenamiento (≤ 2024) y prueba (2025)

**Pistas progresivas:**
- 🟢 Pista suave: Una máscara booleana por fecha, y su negación con `~`.
- 🟡 Pista media: `tabla["fecha"] >= "2025-01-01"` marca la prueba.
- 🔴 Pista directa: `en_prueba = tabla["fecha"] >= "2025-01-01"`; `Xtr, ytr = X[~en_prueba], y[~en_prueba]`; `Xte, yte = X[en_prueba], y[en_prueba]`.

**¿Qué significa el ✅?** Que todo el entrenamiento ocurre antes que toda la prueba.

---

### Ejercicio 3 — Entrena el pipeline

**Pistas progresivas:**
- 🟢 Pista suave: El preprocesamiento (`pre`) ya está; falta unirlo con el clasificador y entrenar.
- 🟡 Pista media: `Pipeline([("pre", pre), ("clf", ...)])` y luego `.fit(Xtr, ytr)`.
- 🔴 Pista directa: `modelo = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))]).fit(Xtr, ytr)`.

**¿Qué significa el ✅?** Que el modelo está entrenado y conoce las dos clases (0 y 1).

---

### Ejercicio 4 — F1 del modelo vs F1 de la persistencia

**Pistas progresivas:**
- 🟢 Pista suave: Dos predicciones: la del modelo y la de la regla «hoy > 50».
- 🟡 Pista media: La regla es `(Xte["pm25"] > 50).astype(int)`.
- 🔴 Pista directa: `f1_modelo = f1_score(yte, pred)`, `recall_modelo = recall_score(yte, pred)`, `base = (Xte["pm25"] > 50).astype(int)`, `f1_base = f1_score(yte, base)`.

**¿Qué significa el ✅?** Que evaluaste como corresponde: en la prueba, con una métrica para clases raras, y contra una línea base.

---

> 🔬 **En la profundización:** tres preguntas que un comité técnico te haría. **¿Cuánto varía?** La validación cruzada temporal (5 pliegues) da F1 entre 0,41 y 0,67 (media 0,59 ± 0,10): una sola cifra esconde mucha variación. **¿A quién le falla?** Entre las estaciones con al menos 10 episodios en 2025, el *recall* va de 0,67 (Cerro Navia) a 0,48 (Rancagua I y Nielol): equidad territorial. **¿Qué error preferimos?** Con `class_weight="balanced"` el *recall* sube de 0,55 a 0,94, pero las alertas pasan de 116 a 397 y la *precision* cae a 0,37: una decisión de política, no técnica.

---

## 7. Autoevaluación Final

**Pregunta 1:** Tu modelo obtiene F1 = 0,99 en la prueba. ¿Qué haces primero?

- A) Celebrar y desplegarlo
- B) Buscar una fuga de datos: alguna *feature* que contenga la respuesta o venga del futuro ✅
- C) Probar un modelo más complejo
- D) Reportarlo tal cual

**Explicación:** En el ejemplo, incluir `pm25_manana` produce exactamente ese número. Un resultado demasiado bueno es una pregunta, no una respuesta.

---

**Pregunta 2:** ¿Por qué no usar `train_test_split` al azar con datos diarios de PM2.5?

- A) Porque es más lento
- B) Porque días vecinos (muy parecidos) quedarían a ambos lados y la evaluación sería optimista respecto del uso real ✅
- C) Porque scikit-learn no lo permite con fechas
- D) Porque la prueba quedaría muy chica

**Explicación:** En producción, el modelo predice el futuro. La prueba debe imitar esa situación.

---

**Pregunta 3:** El modelo tiene F1 0,630 y la persistencia 0,619. ¿Qué dice el brief?

- A) «El modelo es mejor», sin más
- B) Que el modelo apenas supera a la regla simple, que da menos falsas alarmas pero avisa menos episodios, y qué haría falta para mejorarlo ✅
- C) Nada sobre la persistencia, para no confundir
- D) Que el proyecto fracasó

**Explicación:** La comparación con la línea base es el dato más útil para quien decide.

---

**Pregunta 4:** En la profundización, el *recall* varía entre estaciones. ¿Por qué importa en el sector público?

- A) No importa si el promedio es bueno
- B) Porque un modelo que avisa peor en ciertas comunas distribuye desigualmente la protección ✅
- C) Porque hay que eliminar esas estaciones
- D) Porque el modelo está mal entrenado

**Explicación:** La equidad territorial es parte de la evaluación de un modelo público, y va en la ficha como limitación.

---

**Pregunta 5:** ¿Qué agrega el criterio de **Pertinencia** de la rúbrica?

- A) Puntos por usar el modelo más moderno
- B) Reconocimiento a proyectos que usan datos del propio organismo o responden una pregunta real de gestión ✅
- C) Puntos por la cantidad de datos
- D) Nada: es opcional

**Explicación:** El capstone vale más cuando deja una herramienta o un aprendizaje útil para tu servicio.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Capstone** | Proyecto integrador que demuestra la competencia de la rama | El trabajo de título del bootcamp |
| **Enmarcar** | Definir decisión, usuario y objetivo antes del modelo | Los términos de referencia de un estudio |
| **Fuga de datos** | Información de la respuesta o del futuro dentro de las *features* | Evaluar un programa con datos que se produjeron por el mismo programa |
| **Partición temporal** | Pasado para entrenar, futuro para probar | Validar una proyección contra el año cerrado |
| **Persistencia** | Línea base «mañana igual que hoy» | La proyección inercial |
| **Recall** | De los casos que importan, cuántos detectas | Cobertura de un programa de alerta |
| **Precision** | De tus alertas, cuántas eran ciertas | Focalización: cuántos alertados lo necesitaban |
| **`class_weight`** | Hacer que los errores en la clase rara pesen más | Priorizar no dejar a nadie sin aviso |
| **Ficha de modelo** | Documento técnico del modelo, con límites y usos no recomendados | Anexo metodológico |
| **Brief** | Mensaje de una plana para quien decide | Minuta para la jefatura |

---

## 9. Conexión con el Módulo Siguiente

Con el R2-CAP cierras la rama **Científico de Datos**: llevaste un problema público desde la pregunta hasta un modelo evaluado con honestidad, documentado y comunicado. Esta es la base para la certificación en ciencia de datos aplicada al sector público.

Si quieres seguir, la rama **R3 · IA aplicada** trabaja con texto, modelos de lenguaje, RAG y agentes — siempre con la misma disciplina que aprendiste aquí: medir contra una línea base, documentar límites y mantener a un humano en el bucle. Y si tu modelo de capstone resultó útil, el paso siguiente es **R2-09** en la vida real: desplegarlo con monitoreo.

> 💡 **Pregunta para reflexionar:** Si tu modelo le gana por poco a la regla simple, ¿vale la pena el costo de mantenerlo? ¿Qué dato nuevo cambiaría esa respuesta?
