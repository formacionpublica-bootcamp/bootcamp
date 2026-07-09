# Guía de Aprendizaje · R1-CAP · Capstone — Análisis sobre datos de tu organismo

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Semana 11–12 · Google Colab

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Módulo** | R1-CAP · Capstone — análisis sobre datos de tu organismo |
| **Rama** | R1 · Análisis y Visualización |
| **Semanas** | 11–12 (cierre de rama) |
| **Duración estimada** | 4–6 horas de trabajo autónomo |
| **Nivel** | Integrador — aplica todo lo aprendido en R1-00 a R1-09 |
| **Prerrequisitos** | Haber completado R1-00 a R1-09 con ✅ en todos los notebooks |
| **Dataset de ejemplo** | `compras_ml.csv` — compras públicas del Servicio de Salud o datos de tu propio organismo |
| **Competencia de salida** | Ejecutar un análisis de datos público de punta a punta — cargar → limpiar → analizar → visualizar → comunicar — y entregarlo como notebook reproducible con figura honesta y brief de una plana |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

Este capstone es el momento en que dejas de practicar con ejemplos y aplicas todo lo aprendido a **datos reales de tu organismo**.

En el trabajo del Estado, los datos existen pero rara vez se convierten en decisiones. Hay planillas de compras, registros de beneficiarios, bases de infraestructura, reportes de dotación — información que duerme en carpetas compartidas. **Este proyecto te enseña a despertar ese dato.**

El ciclo completo que aprenderás — *enmarcar → cargar → limpiar → analizar → visualizar → comunicar* — es exactamente el que sigue un analista de datos en DIPRES, ChileCompra, una SEREMI o cualquier servicio público que quiera tomar mejores decisiones. Al terminar este capstone, tendrás un notebook que podrás mostrar como evidencia concreta de tu capacidad.

---

## 3. Mapa conceptual del Capstone

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CICLO COMPLETO DE ANÁLISIS DE DATOS PARA EL SECTOR PÚBLICO              │
├──────────────────┬───────────────────────────────────────────────────────┤
│ Etapa            │ Analogía con tu trabajo                               │
├──────────────────┼───────────────────────────────────────────────────────┤
│ 1. ENMARCAR      │ Definir la pregunta de gestión antes de abrir Excel   │
│ 2. CARGAR        │ Abrir el archivo de la unidad compartida              │
│ 3. LIMPIAR       │ Quitar filas duplicadas y vacíos del registro         │
│ 4. ANALIZAR      │ Hacer la tabla dinámica que responde la pregunta      │
│ 5. VISUALIZAR    │ El gráfico que va en el informe de la jefatura        │
│ 6. COMUNICAR     │ El brief de una plana para quien toma la decisión     │
└──────────────────┴───────────────────────────────────────────────────────┘
```

**Lo que integra este capstone:**

| Módulo anterior | Habilidad que aplicas aquí |
|---|---|
| R1-02 Pandas | Cargar y explorar el dataset |
| R1-04 Limpieza | `dropna()`, `drop_duplicates()` |
| R1-03 Cruzar tablas | `groupby().agg()` con múltiples métricas |
| R1-07/08 Visualización | Figura honesta con eje desde 0 y etiquetas |
| R1-08 Ética del dato | Declarar límites y sesgos en el brief |

---

## 4. Antes de empezar: Verificación de prerrequisitos

### ¿Qué necesito saber?

Checklist de verificación — responde honestamente:

| ¿Puedo…? | Módulo donde lo viste | ¿OK? |
|---|---|---|
| Cargar un CSV con `pd.read_csv()` y ver sus columnas | R1-02 | ☐ |
| Eliminar nulos con `dropna()` y duplicados con `drop_duplicates()` | R1-04 | ☐ |
| Hacer un `groupby().agg()` con `sum`, `mean` y `count` | R1-03 | ☐ |
| Crear un gráfico de barras con `matplotlib` | R1-07 | ☐ |
| Poner título, etiquetas y fijar el eje Y desde 0 | R1-07 | ☐ |
| Explicar qué **no** dice un dato (límites y ética) | R1-08 | ☐ |

Si alguna casilla queda vacía, vuelve al módulo correspondiente antes de empezar el capstone. No es retroceder — es construir sobre terreno firme.

### Configuración del entorno

1. Abre `leccion.ipynb` en Google Colab
2. Ejecuta la **primera celda de preparación** (descarga el CSV si no está local)
3. Verifica que aparezca: `Datos cargados: (XXXX, YY) filas x columnas`
4. Si ves un error de importación, ejecuta: `!pip install pandas matplotlib`

---

## 5. Guía paso a paso por sección del notebook

---

### Sección 1 · Enmarca el problema

🎯 **Objetivo:** Escribir la pregunta de gestión que guiará todo el análisis antes de tocar el dato.

💡 **Concepto clave:** En el sector público, el análisis sin pregunta es el equivalente a hacer una auditoría sin saber qué buscas. La **pregunta de gestión** es la brújula: todo lo que hagas después (limpiar, agrupar, graficar) debe servir para responderla.

Ejemplo del módulo: *¿En qué regiones y categorías se concentra el gasto, y qué decisión habilita ese hallazgo?*

La pregunta buena tiene tres ingredientes:
- Una **dimensión de análisis** (región, categoría, año, proveedor…)
- Una **métrica** (gasto total, número de órdenes, promedio por compra…)
- Una **implicación para la gestión** (qué se puede hacer con ese hallazgo)

⚠️ **Error frecuente:** Empezar a limpiar y graficar sin haber definido la pregunta. Resultado: análisis bonito que no dice nada útil.

✅ **Sabes esta sección cuando puedes:** Escribir en una frase qué pregunta de tu organismo vas a responder con los datos.

---

### Sección 2 · Carga y limpia

🎯 **Objetivo:** Construir un `df_limpio` sin nulos ni duplicados en las variables esenciales.

💡 **Concepto clave:** Los datos del Estado tienen historia. Un registro puede estar duplicado porque el sistema lo ingresó dos veces, tener campos vacíos porque el formulario no era obligatorio, o tener fechas malformadas porque nadie las validó en origen. Limpiar no es desconfiar del dato — es ser honesto sobre lo que tienes.

🔍 **Qué hace el código:**

```python
df_limpio = df.dropna().drop_duplicates().copy()
```

- `dropna()` → elimina toda fila que tenga al menos un valor vacío
- `drop_duplicates()` → elimina filas 100% idénticas
- `.copy()` → crea un DataFrame nuevo (no modifica el original)
- `df_limpio.isna().sum().sum()` → cuenta todos los nulos; debe dar 0

⚠️ **Error frecuente:** Aplicar `dropna()` sin saber cuántos registros eliminas. Antes de limpiar, corre `df.isnull().sum()` para saber cuántos nulos hay por columna. Si el 40% de una columna es nulo, quizás es mejor imputar o excluir esa columna, no toda la fila.

✅ **Sabes esta sección cuando puedes:** Explicar cuántas filas perdiste al limpiar y por qué.

---

### Sección 3 · Analiza

🎯 **Objetivo:** Construir la función `resumen_gasto` que agrega el dato por una dimensión y responde la pregunta de gestión.

💡 **Concepto clave:** En Excel harías una tabla dinámica. En pandas haces `groupby().agg()`. La función `resumen_gasto` encapsula esa lógica: la llamas con diferentes columnas (`region_comprador`, `categoria`, `proveedor`) y siempre te devuelve la misma estructura de resumen. Eso es reutilización — una habilidad valiosa cuando tienes que hacer el mismo análisis para 15 servicios distintos.

🔍 **Qué hace el código:**

```python
def resumen_gasto(d, por="region_comprador"):
    return d.groupby(por)["monto_total"].agg(["sum", "mean", "count"]).sort_values("sum", ascending=False)
```

- `d.groupby(por)` → agrupa el DataFrame por la columna indicada
- `["monto_total"]` → selecciona solo la columna de valores monetarios
- `.agg(["sum", "mean", "count"])` → calcula tres métricas a la vez: total, promedio y número de compras
- `.sort_values("sum", ascending=False)` → ordena de mayor a menor gasto total

⚠️ **Error frecuente:** Olvidar el `sort_values`. La tabla sin ordenar no te dice de inmediato quién concentra más gasto — y ese es exactamente el hallazgo que buscas.

✅ **Sabes esta sección cuando puedes:** Llamar `resumen_gasto(df_limpio, por="categoria")` y leer correctamente cuál categoría tiene el mayor gasto total.

---

### Sección 4 · Visualiza (honesto)

🎯 **Objetivo:** Producir una figura de barras del top 6 que sea clara, honesta y lista para un informe.

💡 **Concepto clave:** Una figura honesta no es solo estética — es ética. El principio más importante: **el eje Y siempre desde 0**. Un gráfico que empieza en 80 millones en vez de 0 hace parecer que la diferencia entre regiones es enorme cuando en realidad puede ser pequeña. En el sector público, esas decisiones visuales tienen consecuencias reales.

🔍 **Qué hace el código:**

```python
top = tabla.head(6)                        # las 6 regiones/categorías con más gasto
fig, ax = plt.subplots(figsize=(7, 4))     # crea la figura y el eje
ax.bar(top.index, top["sum"])              # dibuja las barras
ax.set_ylim(bottom=0)                      # ← HONESTIDAD: eje desde 0
ax.set_title("Gasto por región")           # título descriptivo
ax.set_xlabel("Región")                    # etiqueta eje X
ax.set_ylabel("Monto total ($)")           # etiqueta eje Y con unidad
plt.xticks(rotation=45, ha="right")        # rota etiquetas para que quepan
plt.tight_layout()                         # evita que se corten las etiquetas
plt.show()
```

⚠️ **Error frecuente:** Olvidar `ax.set_ylim(bottom=0)`. La celda de chequeo verifica exactamente eso — si el eje no empieza en 0, el ✅ no aparece.

✅ **Sabes esta sección cuando puedes:** Mostrarle la figura a un colega que no sabe programar y que entienda el hallazgo sin explicación adicional.

---

### Sección 5 · Comunica — brief de una plana

🎯 **Objetivo:** Completar el brief de una plana que convierte el análisis en una recomendación accionable para quien decide.

💡 **Concepto clave:** El brief de una plana es el entregable más importante del capstone — más que el notebook. El jefe o la jefa de servicio no va a ejecutar celdas de Python. Va a leer una página. La habilidad de traducir datos a lenguaje de gestión es lo que diferencia a un analista que impacta de uno que solo produce reportes.

🔍 **Estructura del brief:**

| Sección | Qué escribes | Extensión |
|---|---|---|
| **Pregunta** | La que enmarcaste en el paso 1 | 1 frase |
| **Hallazgo** | Qué muestran los datos, con el número clave | 1-2 frases |
| **Recomendación** | Qué debería hacer el organismo | 1-2 frases |
| **Límites y ética** | Qué NO dice este dato; sesgos o cautelas | 1-2 frases |

Ejemplo completo:
> **Pregunta:** ¿En qué regiones se concentra el gasto en compras públicas del SML?
>
> **Hallazgo:** El 45% del gasto total se concentra en 3 regiones (Metropolitana, Biobío y Valparaíso), mientras que regiones extremas como Aysén y Magallanes acumulan menos del 3%.
>
> **Recomendación:** Revisar si la distribución responde a densidad poblacional o si existen déficits de abastecimiento en regiones con menor gasto relativo.
>
> **Límites y ética:** Este análisis muestra montos, no necesidades. Una región con bajo gasto puede estar bien abastecida o puede estar desatendida — el dato solo no lo dice.

⚠️ **Error frecuente:** Escribir el hallazgo sin el número clave ("hay diferencias entre regiones" en vez de "el 45% del gasto se concentra en 3 regiones"). Sin el número, el brief no es accionable.

✅ **Sabes esta sección cuando puedes:** Leer el brief en voz alta en 30 segundos y que quien escucha entienda el problema, el hallazgo y qué hacer.

---

## 6. Guía de los 3 Ejercicios del Notebook

---

### Ejercicio 1 · Limpia el DataFrame

**Objetivo:** Construir `df_limpio` sin nulos ni duplicados.

**Habilidad que entrena:** Aplicar una secuencia de limpieza estándar y verificar el resultado.

**Pistas progresivas:**

- 🟢 **Pista suave:** pandas tiene métodos para eliminar filas con valores vacíos y filas duplicadas. Puedes encadenarlos.
- 🟡 **Pista media:** Usa `.dropna()` para los nulos y `.drop_duplicates()` para los duplicados. Añade `.copy()` al final.
- 🔴 **Pista directa:** La estructura es `df.dropna().drop_duplicates().copy()`. Asígnala a `df_limpio`.

**Lógica de la solución:** Limpiar es una cadena de transformaciones. Cada método devuelve un DataFrame nuevo, así que puedes encadenarlos con punto. El `.copy()` al final evita advertencias de pandas cuando modificas el DataFrame más adelante.

**Qué significa el ✅:** La celda verifica que `df_limpio` no tenga ningún nulo (la suma de todos los nulos es 0) y que tenga igual o menos filas que el original (no creaste filas nuevas).

---

### Ejercicio 2 · Escribe `resumen_gasto`

**Objetivo:** Crear una función reutilizable que agrega el gasto por cualquier dimensión.

**Habilidad que entrena:** Escribir funciones con parámetros por defecto y usar `groupby().agg()` con múltiples funciones.

**Pistas progresivas:**

- 🟢 **Pista suave:** La función recibe un DataFrame `d` y un nombre de columna `por`. Debe devolver una tabla resumen.
- 🟡 **Pista media:** Usa `d.groupby(por)["monto_total"].agg(["sum", "mean", "count"])`. Ordena por `"sum"` descendente.
- 🔴 **Pista directa:** `return d.groupby(por)["monto_total"].agg(["sum","mean","count"]).sort_values("sum", ascending=False)`

**Lógica de la solución:** `groupby` agrupa las filas por categoría, `.agg()` calcula varias métricas en paralelo, y `sort_values` ordena de mayor a menor para que el hallazgo principal quede arriba. El parámetro `por="region_comprador"` es el valor por defecto, pero la función funciona con cualquier columna categórica.

**Qué significa el ✅:** La celda verifica que la tabla resultante tenga una columna llamada `"sum"` y que el número de filas sea igual al número de regiones únicas en el dataset limpio.

---

### Ejercicio 3 · Grafica el top 6

**Objetivo:** Producir una figura de barras honesta del top 6 con título, etiquetas y eje desde 0.

**Habilidad que entrena:** Configurar un gráfico de matplotlib para comunicación pública, no solo exploración.

**Pistas progresivas:**

- 🟢 **Pista suave:** Ya tienes `top` y `ax`. Solo necesitas agregar: fijar el límite inferior del eje Y, un título y las etiquetas de los ejes.
- 🟡 **Pista media:** Usa `ax.set_ylim(bottom=0)`, `ax.set_title(...)`, `ax.set_xlabel(...)` y `ax.set_ylabel(...)`.
- 🔴 **Pista directa:** Agrega estas 4 líneas después del `ax.bar(...)`: `ax.set_ylim(bottom=0)` / `ax.set_title("Gasto por región compradora")` / `ax.set_xlabel("Región")` / `ax.set_ylabel("Monto total ($)")`

**Lógica de la solución:** `ax.bar()` dibuja las barras pero no configura nada más. Los métodos `set_ylim`, `set_title`, `set_xlabel` y `set_ylabel` son los que convierten un gráfico exploratorio en uno listo para presentar. El `bottom=0` es la línea más importante: garantiza que el gráfico no engañe al lector.

**Qué significa el ✅:** La celda verifica que `fig` sea un objeto `Figure` de matplotlib y que el límite inferior del eje Y sea exactamente 0.

---

## 7. El brief de una plana en profundidad: comunicar para decidir

Esta sección es el corazón del capstone. Un análisis que no se comunica bien no existe para quien decide.

### Por qué importa la estructura del brief

En el sector público, los informes suelen ser largos, densos y llenos de tablas que nadie lee. El brief de una plana es la contrapropuesta: **todo lo que necesitas saber en el tiempo que dura leer un email**.

### Reflexión guiada sobre los datos de compras

Si usas el dataset `compras_ml.csv`, considera estas preguntas antes de escribir tu brief:

1. **¿La distribución regional del gasto refleja las necesidades del territorio?** El hecho de que la Región Metropolitana concentre más compras puede ser proporcional a su densidad de servicios — o puede indicar centralización excesiva.

2. **¿Qué categorías de compra tienen el mayor gasto promedio por orden?** Un alto gasto total puede deberse a muchas compras pequeñas o pocas compras muy grandes. Eso cambia completamente la recomendación.

3. **¿Hay alguna región con pocas compras pero montos altos?** Eso podría indicar contratos grandes, no necesariamente mayor cobertura.

### El límite más importante que debes declarar

Los datos de compras públicas muestran **lo que se gastó**, no **lo que se necesitaba**. Una región con bajo gasto puede tener necesidades desatendidas — o puede estar más eficientemente abastecida. El brief honesto siempre separa *hallazgo* de *interpretación*.

### Pregunta de debate

> Si los datos mostraran que el 60% del gasto en suministros médicos se concentra en dos regiones, ¿qué dato adicional pedirías para saber si eso es un problema o es proporcional? ¿Población, número de establecimientos, o algo más?

---

## 8. Rúbrica de evaluación — cómo interpretar cada criterio

El notebook incluye una rúbrica de 5 criterios. Aquí está la guía para entender qué se evalúa en cada uno:

| Criterio | ✅ Cumple | ❌ No cumple |
|---|---|---|
| **Correctitud del dato** | La limpieza elimina todos los nulos, las agregaciones son reproducibles y los números cuadran | Hay nulos en `df_limpio` o el `groupby` no agrega correctamente |
| **Claridad visual** | La figura se entiende sola: alguien que no programó el análisis puede leerla y extraer el hallazgo | La figura no tiene título, las etiquetas son crípticas o hay demasiada información |
| **Honestidad / ética** | El eje Y empieza en 0, los límites del dato están declarados en el brief | El eje empieza en otro valor, o el brief no menciona qué no dice el dato |
| **Reproducibilidad** | El notebook corre de principio a fin sin intervención manual: `Runtime > Run all` funciona sin errores | Hay celdas que requieren cambiar variables a mano o que fallan si se ejecutan fuera de orden |
| **Comunicación** | El brief tiene los 4 elementos (pregunta, hallazgo con número, recomendación, límites) y se lee en 30 segundos | El brief es vago, sin cifras concretas, o mezcla hallazgo con interpretación |

---

## 9. Conexión con `profundiza.ipynb`

| Aspecto | `leccion.ipynb` | `profundiza.ipynb` |
|---|---|---|
| **Enfoque** | Ciclo aplicado sobre tu dataset | Análisis más profundo y técnico |
| **Audiencia** | Todos los participantes de R1 | Quienes quieren ir más allá |
| **Habilidades** | Limpieza + agregación + visualización básica + brief | Análisis multivariable, correlaciones, visualizaciones avanzadas |
| **Obligatorio** | ✅ Sí — es el entregable del capstone | ☐ Opcional — recomendado para quienes buscan la rama R2 |

¿Cuándo ir al `profundiza`? Si ya completaste el `leccion.ipynb` con ✅ en los 3 ejercicios y sientes que tu análisis podría ir más lejos, el `profundiza` te da las herramientas para hacerlo. También es una buena preparación si planeas continuar con la Rama R2 (Científico de Datos).

---

## 10. Autoevaluación Final

Responde estas preguntas antes de dar por terminado el capstone:

**1. ¿Qué hace `df.dropna()` exactamente?**

- a) Elimina las columnas que tienen nulos
- b) Elimina las filas que tienen al menos un valor nulo ✅
- c) Reemplaza los nulos por 0
- d) Cuenta cuántos nulos hay en el DataFrame

*Respuesta correcta: b) — `dropna()` elimina filas con valores vacíos. Para eliminar columnas, usarías `dropna(axis=1)`.*

---

**2. ¿Por qué es importante poner el eje Y desde 0 en un gráfico de barras?**

- a) Porque matplotlib lo exige por defecto
- b) Para que el gráfico ocupe más espacio en el informe
- c) Para que la diferencia visual entre barras sea proporcional a la diferencia real en los datos ✅
- d) Es solo una convención estética sin impacto

*Respuesta correcta: c) — Un eje que no empieza en 0 amplifica visualmente las diferencias, lo que puede llevar a conclusiones erróneas o engañosas.*

---

**3. En `groupby("region_comprador")["monto_total"].agg(["sum","mean","count"])`, ¿qué representa la columna `count`?**

- a) El número de regiones únicas
- b) El número de órdenes de compra por región ✅
- c) El monto máximo por región
- d) El número de columnas del DataFrame

*Respuesta correcta: b) — `count` cuenta cuántas filas hay en cada grupo después del `groupby`, es decir, cuántas órdenes de compra tiene cada región.*

---

**4. ¿Cuál es el propósito del `.copy()` en `df.dropna().drop_duplicates().copy()`?**

- a) Hacer una copia de seguridad del archivo CSV original
- b) Duplicar todas las filas del DataFrame
- c) Crear un DataFrame independiente para evitar advertencias de pandas al modificarlo después ✅
- d) Es redundante y no tiene efecto

*Respuesta correcta: c) — Sin `.copy()`, pandas puede generar una advertencia `SettingWithCopyWarning` porque el nuevo DataFrame podría ser una vista del original. El `.copy()` garantiza independencia.*

---

**5. ¿Qué elemento del brief de una plana es el más importante para quien toma decisiones?**

- a) La descripción técnica de cómo se limpió el dato
- b) La recomendación accionable con cifras concretas ✅
- c) La lista completa de columnas del dataset
- d) El nombre del software utilizado

*Respuesta correcta: b) — La recomendación accionable con cifras es lo que convierte el análisis en gestión. Sin ella, el brief es solo un resumen descriptivo.*

---

## 11. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **Ciclo de análisis** | Secuencia completa: cargar → limpiar → analizar → visualizar → comunicar | El proceso de hacer un informe de gestión con datos |
| **`dropna()`** | Elimina filas con valores vacíos | Borrar las filas en blanco de tu tabla de Excel |
| **`drop_duplicates()`** | Elimina filas exactamente iguales | Quitar registros duplicados de un padrón |
| **`groupby().agg()`** | Agrupa y calcula métricas por categoría | Tabla dinámica de Excel |
| **Función reutilizable** | Bloque de código que puedes llamar múltiples veces con distintos parámetros | Una macro de Excel que aplicas a diferentes hojas |
| **`figsize`** | Tamaño de la figura en pulgadas (ancho, alto) | Ajustar el tamaño del gráfico en Word |
| **`ax.set_ylim(bottom=0)`** | Fija el límite inferior del eje Y en 0 | Asegurarse de que el gráfico no engañe al lector |
| **Brief de una plana** | Resumen ejecutivo de una página con pregunta, hallazgo, recomendación y límites | El resumen ejecutivo de un informe de DIPRES |
| **Reproducibilidad** | El notebook corre completo sin intervención manual | Un informe que cualquier colega puede replicar |
| **Figura honesta** | Gráfico que no manipula la percepción visual del dato | Un gráfico que muestra la realidad, no la embellecer |
| **Pregunta de gestión** | La pregunta concreta que guía el análisis | El objetivo de un informe de auditoría |
| **Capstone** | Proyecto integrador que aplica todo lo aprendido | La memoria de práctica de un proceso formativo |

---

## 12. Has llegado al final de la Rama R1 🎉

Si completaste el capstone con ✅ en los 3 ejercicios, un brief completo y un notebook reproducible, has demostrado algo concreto: **puedes tomar datos del Estado, analizarlos y traducirlos en decisiones**.

### ¿Qué sigue?

Con la Rama R1 completada, tienes tres caminos:

| Opción | Para quién | Primer módulo |
|---|---|---|
| **Rama R2 · Científico de Datos** | Quieres ir más profundo: modelos, estadística inferencial, ML | R2-00 · Probabilidad y distribuciones |
| **Rama R3 · IA Aplicada al Estado** | Quieres aplicar IA a problemas de tu organismo | R3-00 · IA para el sector público |
| **Consolidar R1** | Quieres aplicar lo aprendido a otro dataset de tu organismo antes de seguir | Repetir el capstone con tus propios datos |

**Pregunta motivadora para lo que sigue:** Ahora que sabes analizar y comunicar un dato, ¿qué pasaría si pudieras predecir cuándo ese gasto va a subir, o detectar automáticamente anomalías en las compras? Eso es lo que construyes en R2 y R3.

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos · Formación Pública · Chile*
*Versión 1.0 · Junio 2026*
