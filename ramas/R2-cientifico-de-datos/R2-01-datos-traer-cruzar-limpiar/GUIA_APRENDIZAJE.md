# 📘 Guía de Aprendizaje — R2-01 · Datos: traer, cruzar y limpiar

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Nombre del módulo** | R2-01 · Datos: traer, cruzar y limpiar |
| **Pista / Rama** | R2 — Científico/a de Datos |
| **Duración estimada** | 3–4 horas (Semana 3) |
| **Nivel** | Inicial-intermedio |
| **Prerrequisitos** | Haber completado R2-00: cargar DataFrames, filtrar, ordenar y usar `groupby`. |
| **Competencia de salida** | Construir un dataset analítico limpio y listo para modelar, cruzando tablas, tratando nulos, eliminando duplicados y corrigiendo tipos. |
| **Dataset** | `compras_ml.csv` — Compras públicas reales de ChileCompra (monto, categoría, región, tamaño de proveedor). |
| **Entregable** | Las 4 celdas de chequeo del `leccion.ipynb` muestran ✅. |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En el trabajo público, casi nunca recibes una base de datos perfecta. Lo más común es que te llegue una tabla con nombres repetidos, celdas vacías, columnas mal tipadas y otra planilla adicional que hay que unir para que el análisis tenga sentido.

Eso pasa todo el tiempo en ministerios, municipalidades, servicios y gobiernos regionales: una planilla de compras, otra de proveedores, otra de clasificación presupuestaria. Si no sabes **traer, cruzar y limpiar**, cualquier dashboard, informe o modelo posterior nace chueco.

Este módulo te entrena justamente en esa etapa crítica. Aprendes a:

- **Cruzar tablas** con `merge`, como cuando unes un Excel de compras con otro Excel de categorías.
- **Resolver nulos**, que en la práctica son celdas vacías que pueden romper un análisis.
- **Eliminar duplicados**, para no inflar conteos o montos.
- **Corregir tipos**, para que las columnas funcionen como lo que realmente son.

> 🏛️ **Traducción al mundo público:** antes de pedirle inteligencia a los datos, primero hay que dejarlos ordenados y confiables.

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|---|---|---|
| `merge` | Une dos tablas usando una clave común | BUSCARV/XLOOKUP entre dos planillas de Excel |
| `groupby` | Resume información por grupos | Tabla dinámica por categoría o región |
| `reset_index()` | Convierte el índice en una columna normal | "Aplanar" una tabla resumen para poder reutilizarla |
| `rename()` | Cambia el nombre de una columna | Renombrar encabezados para que sean claros en un informe |
| `isna()` | Detecta valores faltantes (`NaN`) | Identificar celdas vacías en una planilla |
| `dropna()` | Elimina filas con valores nulos | Sacar registros incompletos antes de reportar |
| `drop_duplicates()` | Elimina filas repetidas | Quitar registros duplicados de un listado oficial |
| `astype('category')` | Convierte una columna a tipo categórico | Tratar una columna como clasificación cerrada (Grande, Mediana, Pequeña) |
| `left join` | Mantiene todas las filas de la tabla principal | Mantener todas las órdenes de compra aunque falten datos de apoyo |
| `inner join` | Mantiene solo filas que tienen cruce en ambas tablas | Quedarse solo con registros que existen en ambos padrones |

---

## 4. Verificación de Prerrequisitos

Antes de entrar al notebook, revisa este checklist:

| ¿Puedo...? | ✅ Listo | 🔄 Revisar |
|---|---|---|
| Ejecutar celdas en Colab sin perderme | ✅ | Si no, repasa la dinámica del módulo R2-00 |
| Entender qué es un DataFrame y para qué sirve | ✅ | Piensa en una planilla Excel cargada en Python |
| Filtrar o seleccionar columnas con pandas | ✅ | Si te cuesta, vuelve a R2-00 |
| Leer mensajes de chequeo ✅ o ❌ sin frustrarme | ✅ | En este módulo el error es parte del aprendizaje |
| Entender la idea de “cruzar” dos tablas | ✅ | Piensa en BUSCARV o XLOOKUP entre dos Excels |

> 💬 Si alguna te quedó en “Revisar”, no pasa nada. Pero te conviene reforzar R2-00 antes de seguir, porque aquí ya empezamos a trabajar con calidad de datos.

---

## 5. Guía Paso a Paso por Sección del Notebook

### 🔷 Sección 0 — Preparación del entorno

**🎯 Objetivo:** Cargar el archivo `compras_ml.csv` y dejar listo el entorno para trabajar.

**💡 Concepto clave:** Igual que en R2-00, primero preparas la mesa antes de cocinar. Aquí se importan `pandas`, `numpy` y `matplotlib`, y luego se carga el dataset.

**🔍 Qué hace el código:**
1. Revisa si el CSV existe localmente.
2. Si no existe, lo descarga desde el repositorio.
3. Lo abre como DataFrame llamado `df`.
4. Muestra dimensiones y primeras filas.

**⚠️ Error frecuente:** Saltarse esta celda y luego intentar usar `df`, `np` o `plt`. Si eso ocurre, aparecerán errores tipo `NameError`.

**✅ Señal de comprensión:** Ves la tabla cargada y puedes explicar qué significa algo como `(5000, 8)`.

---

### 🔷 Sección 1 — Cruzar tablas con `merge`

**🎯 Objetivo:** Enriquecer cada compra con el promedio de monto de su categoría.

**💡 Concepto clave:** `merge` es el equivalente programable de un BUSCARV bien hecho. Tomas una tabla principal y le agregas información desde otra tabla usando una llave común. En el sector público esto se parece mucho a unir una base de órdenes de compra con una tabla maestra de rubros, proveedores o códigos presupuestarios.

**🔍 Qué hace el código:**
- Primero crea una tabla resumen con `groupby('categoria')['monto_total'].mean()`.
- Después usa `reset_index()` para que la categoría quede como columna.
- Luego cambia el nombre de la columna promedio a `monto_prom_categoria`.
- Finalmente, une esa tabla resumen con `df` usando `merge(..., on='categoria', how='left')`.

**⚠️ Error frecuente:** Usar un `how='inner'` sin darse cuenta. Eso puede eliminar filas si una categoría no aparece en ambos lados del cruce. En este caso se usa `left` porque queremos conservar todas las compras originales.

**✅ Señal de comprensión:** El DataFrame final `enriquecido` tiene la misma cantidad de filas que `df`, pero con una columna nueva adicional.

---

### 🔷 Sección 2 — Limpiar nulos

**🎯 Objetivo:** Detectar cuántos valores faltantes hay en `monto_total` y eliminarlos.

**💡 Concepto clave:** Un nulo es como una celda vacía en Excel, pero en pandas aparece como `NaN`. Si no lo detectas a tiempo, puede arruinar cálculos, gráficos o modelos. En el Estado esto pasa mucho cuando una planilla se llenó incompleta o cuando un sistema no capturó un dato obligatorio.

**🔍 Qué hace el código:**
- Se crea una copia del DataFrame llamada `sucio`.
- Se introducen 50 nulos artificiales en `monto_total` para practicar.
- Luego debes contarlos con `isna().sum()`.
- Finalmente, construir una versión limpia eliminando esas filas con `dropna(subset=['monto_total'])`.

**⚠️ Error frecuente:** Aplicar `dropna()` sobre todo el DataFrame sin especificar la columna. Eso puede borrar más filas de las necesarias si hay otros nulos en columnas no críticas.

**✅ Señal de comprensión:** Puedes explicar cuántos nulos había y por qué el DataFrame limpio tiene menos filas, pero ningún `NaN` en `monto_total`.

---

### 🔷 Sección 3 — Eliminar duplicados

**🎯 Objetivo:** Quitar filas repetidas para no inflar resultados.

**💡 Concepto clave:** Los duplicados son uno de los errores más peligrosos en analítica pública, porque parecen inocentes pero pueden duplicar gasto, duplicar usuarios o duplicar beneficiarios. En Excel muchas veces se detectan tarde; en pandas puedes removerlos de forma explícita y reproducible.

**🔍 Qué hace el código:**
- Crea un DataFrame llamado `con_dup` agregando las primeras 10 filas de nuevo al final.
- Luego debes aplicar `drop_duplicates()` para quedarte solo con registros únicos.

**⚠️ Error frecuente:** Pensar que `drop_duplicates()` modifica automáticamente la tabla original. Si no asignas el resultado a una nueva variable, no se guarda el cambio.

**✅ Señal de comprensión:** `sin_dup` queda con el mismo largo que `df.drop_duplicates()` y claramente menor que `con_dup`.

---

### 🔷 Sección 4 — Corregir tipos

**🎯 Objetivo:** Convertir `tamano_proveedor` al tipo `category`.

**💡 Concepto clave:** No todas las columnas son iguales. Algunas son numéricas, otras son texto libre y otras son categorías cerradas. Cuando una variable tiene pocas opciones repetidas —como Grande, Mediana o Pequeña— conviene marcarla como categórica. Es más eficiente y evita ciertos errores.

**🔍 Qué hace el código:**
- Crea una copia `df2`.
- Convierte la columna `tamano_proveedor` con `.astype('category')`.
- Luego verifica si el tipo quedó bien comparando `dtype.name == 'category'`.

**⚠️ Error frecuente:** Aplicar `astype('category')` pero olvidar reasignarlo a la columna. Si no lo reasignas, la columna queda igual que antes.

**✅ Señal de comprensión:** Puedes explicar por qué `tamano_proveedor` es una categoría y no una medida numérica ni texto libre.

---

## 6. Guía de Ejercicios

### ✍️ Ejercicio 1 — Enriquece cada fila con el promedio de su categoría

**Habilidad que desarrolla:** Cruce de tablas y enriquecimiento de datos.

**Pista 1 (conceptual):** Ya tienes la tabla resumen creada. La tarea no es recalcular nada, sino **pegar esa información** de vuelta en cada fila original usando la categoría como llave.

**Pista 2 (técnica):** La operación correcta es `merge`. Necesitas unir `df` con `resumen` usando `on='categoria'`.

**Pista 3 (casi solución):** Si quieres conservar todas las compras originales, el tipo de join adecuado es `left`.

**Lógica de solución:** Tomar la tabla principal `df`, cruzarla con `resumen` por la columna `categoria` y usar `how='left'`.

---

### ✍️ Ejercicio 2 — Cuenta y elimina los nulos

**Habilidad que desarrolla:** Diagnóstico y limpieza de valores faltantes.

**Pista 1 (conceptual):** Primero necesitas medir el problema. Antes de limpiar, cuenta cuántos valores faltan.

**Pista 2 (técnica):** Para contar nulos en una columna, usa `.isna().sum()`.

**Pista 3 (casi solución):** Para limpiar solo las filas donde falta `monto_total`, usa `dropna(subset=['monto_total'])`.

**Lógica de solución:** Contar nulos en la columna indicada y luego eliminar solo las filas donde esa columna está vacía.

---

### ✍️ Ejercicio 3 — Quita las filas duplicadas

**Habilidad que desarrolla:** Detección de repetidos en bases de datos.

**Pista 1 (conceptual):** La tabla `con_dup` fue creada con filas repetidas a propósito. No necesitas comparar manualmente; pandas ya trae una función lista.

**Pista 2 (técnica):** La función clave es `drop_duplicates()`.

**Pista 3 (casi solución):** Recuerda guardar el resultado en `sin_dup`, porque el método no se aplica “mágicamente” solo.

**Lógica de solución:** Aplicar `drop_duplicates()` al DataFrame con duplicados y guardar el resultado limpio.

---

### ✍️ Ejercicio 4 — Convierte `tamano_proveedor` a category

**Habilidad que desarrolla:** Corrección de tipos de datos.

**Pista 1 (conceptual):** La columna no representa texto libre, sino una clasificación cerrada con pocas opciones.

**Pista 2 (técnica):** El método que transforma el tipo es `.astype(...)`.

**Pista 3 (casi solución):** El string exacto del tipo que necesitas es `'category'`.

**Lógica de solución:** Reasignar la columna `tamano_proveedor` usando `.astype('category')`.

---

## 7. Sección en Profundidad: Ejercicio 1 — Cruzar tablas con `merge`

Este es el ejercicio más estratégico del módulo para política pública, porque **el Estado trabaja casi siempre con datos fragmentados**.

Una sola base rara vez basta. Para construir un buen análisis, casi siempre necesitas unir:

- una tabla de compras,
- una tabla de proveedores,
- una tabla de comunas o regiones,
- una tabla presupuestaria,
- o una tabla de clasificación programática.

### ¿Por qué este ejercicio importa tanto?

Porque `merge` es la habilidad que convierte datos aislados en información útil.

Ejemplos reales de uso público:

| Situación real | Cruce necesario |
|---|---|
| Analizar compras por región | Orden de compra + tabla de organismos + región |
| Revisar pagos a proveedores MIPYME | Compras + clasificación de tamaño de proveedor |
| Estudiar concentración de gasto | Compras + rubro + identificador proveedor |
| Armar tablero de control institucional | Varias tablas maestras unidas por llave común |

### Riesgos de un mal `merge`

- **Perder filas sin darte cuenta** si usas `inner` cuando debías usar `left`.
- **Duplicar registros** si la llave no es única en una de las tablas.
- **Cruzar mal** si los nombres de categoría están escritos distinto.

> 🧠 **Regla práctica:** cuando tu tabla principal son las compras y quieres enriquecerlas, normalmente el `left join` es tu amigo.

---

## 8. Conexión con profundiza.ipynb

La profundización de este módulo no repite la lección: la amplía hacia problemas reales más finos de integración y calidad de datos.

### Comparativa leccion vs. profundiza

| Tema | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| Cruce de tablas | `merge` básico con `left` | Comparación `left` vs `inner` |
| Nulos | Eliminación con `dropna` | Imputación con media del grupo |
| Calidad de texto | No aborda | Normalización con `str.strip().str.lower()` |
| Complejidad | ⭐⭐ Básico-intermedio | ⭐⭐⭐ Intermedio |
| Proyección | Dejar el dato limpio | Prepararse para linkage y features más robustos |

### Guía de decisión

```
¿Terminaste las 4 celdas con ✅?
    ├── No → Termina primero la lección principal.
    └── Sí → ¿Te interesa trabajar con cruces reales y bases imperfectas?
              ├── Sí → Haz el profundiza ahora.
              └── No → Avanza a R2-02 y vuelve después.
```

**Ejercicio más valioso del profundiza:** La imputación por media de categoría, porque enseña una decisión muy común en analítica pública: no siempre conviene eliminar filas; a veces conviene completarlas de forma razonable y trazable.

---

## 9. Autoevaluación Final

**Pregunta 1:** ¿Para qué sirve `merge` en pandas?

- a) Para ordenar columnas alfabéticamente
- b) Para unir tablas usando una clave común
- c) Para borrar nulos automáticamente
- d) Para cambiar nombres de columnas

✅ **Respuesta correcta: b)**
**Explicación:** `merge` permite combinar dos tablas usando una columna compartida. Es el equivalente más cercano a BUSCARV/XLOOKUP en Excel, pero con mayor control.

---

**Pregunta 2:** ¿Qué hace `isna().sum()` sobre una columna?

- a) Suma todos los valores numéricos
- b) Cuenta cuántos valores faltantes hay
- c) Elimina las filas vacías
- d) Convierte los nulos en cero

✅ **Respuesta correcta: b)**
**Explicación:** `isna()` marca con True/False dónde hay nulos, y `sum()` cuenta cuántos True hay. Es una forma rápida de medir cuántas celdas vacías tienes.

---

**Pregunta 3:** ¿Qué riesgo tienes si no eliminas duplicados en una base de compras?

- a) Que pandas no pueda abrir el archivo
- b) Que se borren todas las columnas categóricas
- c) Que se inflen conteos, montos o registros analizados
- d) Que los gráficos cambien de color

✅ **Respuesta correcta: c)**
**Explicación:** Los duplicados pueden hacer que parezca que hubo más compras, más gasto o más proveedores de los que realmente existieron. Es un problema serio de calidad de datos.

---

**Pregunta 4:** ¿Cuándo tiene sentido usar `astype('category')`?

- a) Cuando una columna contiene texto libre largo
- b) Cuando una columna tiene pocas categorías repetidas
- c) Cuando una columna tiene fechas
- d) Cuando una columna debe borrarse

✅ **Respuesta correcta: b)**
**Explicación:** El tipo categórico es útil para variables con pocas opciones posibles y mucha repetición, como tramo, región, estado o tamaño de proveedor.

---

**Pregunta 5:** Si quieres conservar todas las filas de la tabla principal al hacer un cruce, ¿qué tipo de join te conviene usar?

- a) `inner`
- b) `cross`
- c) `left`
- d) `outer` siempre

✅ **Respuesta correcta: c)**
**Explicación:** El `left join` mantiene todas las filas de la tabla de la izquierda, agregando información cuando existe coincidencia. Es muy útil cuando tu base principal no debe perder registros.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente sector público / Excel |
|---|---|---|
| **merge** | Unión de dos tablas por una llave común | BUSCARV/XLOOKUP entre dos planillas |
| **llave / clave** | Columna que permite relacionar tablas | RUT, ID de compra, código de categoría |
| **left join** | Mantiene todas las filas de la tabla principal | No perder compras aunque falten datos de apoyo |
| **inner join** | Mantiene solo filas con coincidencia en ambas tablas | Quedarse solo con registros que cruzan perfecto |
| **nulo / NaN** | Valor faltante | Celda vacía en Excel |
| **isna()** | Detecta valores faltantes | Marcar celdas vacías |
| **dropna()** | Elimina filas con nulos | Borrar registros incompletos |
| **duplicado** | Registro repetido | Fila repetida en una planilla |
| **drop_duplicates()** | Elimina filas repetidas | Quitar duplicados automáticamente |
| **tipo de dato** | Forma en que una columna es interpretada | Número, texto, fecha, categoría |
| **category** | Tipo para variables con opciones cerradas | Clasificación como Grande/Mediana/Pequeña |
| **enriquecimiento de datos** | Agregar atributos nuevos a cada fila desde otra tabla | Completar una base con datos maestros |

---

## 11. Conexión con el Módulo Siguiente

Después de este módulo ya no solo sabes mirar datos: ahora sabes **prepararlos con criterio**. Eso te deja listo para dar el siguiente salto.

**El siguiente módulo es R2-02 · SQL para features.**

Ahí vas a aprender a construir variables útiles para análisis y modelamiento a partir de consultas SQL. En otras palabras:

- pasarás de limpiar tablas a **diseñar atributos analíticos**,
- dejarás de trabajar solo en pandas para integrar lógica de base de datos,
- y empezarás a pensar como alguien que prepara datos para modelos reales.

> 🔗 **Conexión pedagógica:** R2-01 te enseña a dejar la base confiable; R2-02 te enseña a volverla inteligente.

Si en este módulo aprendiste a que la planilla “no esté sucia”, en el siguiente aprenderás a que además “sirva para predecir y explicar”. Vamos con todo 🚀
