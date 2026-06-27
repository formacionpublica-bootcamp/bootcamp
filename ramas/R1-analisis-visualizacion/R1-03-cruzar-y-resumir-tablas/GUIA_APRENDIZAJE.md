# Guía de Aprendizaje — R1-03 · Cruzar y resumir tablas

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
**Pista:** R1 · Análisis y Visualización
**Módulo:** R1-03 (M3B)
**Duración estimada:** 90–120 minutos
**Nivel:** Básico–Intermedio
**Prerrequisitos:** Haber completado R1-02 · Exploración con pandas (saber cargar un CSV, usar `head`, `shape`, `value_counts`)
**Competencia de salida:** Cruzar dos tablas por su llave común (`merge`), elegir el tipo de cruce correcto y detectar filas huérfanas; resumir el resultado con `groupby` para responder una pregunta real de gestión pública.

---

## 1. ¿Para qué me sirve esto como funcionario público?

En R1-02 aprendiste a explorar **una** tabla. Pero en el Estado casi nunca la información vive junta: los **montos** de compra están en una tabla de órdenes, y el **nombre del organismo y su región** en otra. Para responder *"¿qué región concentra más gasto?"* necesitas **cruzar** ambas.

Este módulo te enseña la habilidad que transforma *"sé abrir un Excel"* en *"puedo responder una pregunta real de política pública"*: relacionar tablas por una llave y resumir el resultado.

### Ejemplos reales en el sector público chileno

| Pregunta de gestión | Tabla 1 | Tabla 2 | Llave |
|---|---|---|---|
| ¿Qué región concentra más gasto en licitaciones? | Órdenes de compra (monto, entcode) | Catálogo de organismos (entcode, región) | `entcode` |
| ¿Cuántos funcionarios tiene cada ministerio? | Dotación (RUT, código ministerio) | Catálogo de ministerios (código, nombre) | código ministerio |
| ¿Qué comunas tienen más denuncias? | Denuncias (ID, código comuna) | Catálogo de comunas (código, nombre, región) | código comuna |

En este módulo trabajamos con **órdenes de compra reales de ChileCompra / MercadoPúblico** para responder la primera pregunta de la tabla.

---

## 2. Mapa conceptual del módulo

```
Dos tablas separadas
     │                    │
  ordenes.csv         organismos.csv
 (monto, entcode)   (entcode, organismo, region)
     │                    │
     └─────── merge() ────┘
              (por entcode)
                   │
            Tabla combinada
         (monto + organismo + region)
                   │
               groupby()
                   │
         Gasto total por región
                   │
             Decisión informada
```

### Analogías con el trabajo del Estado

| Concepto pandas | Equivalente en Excel / administración pública |
|---|---|
| `pd.merge()` | BUSCARV / VLOOKUP que trae datos de otra hoja |
| `on="entcode"` | La columna que usas en el BUSCARV para buscar |
| `how="inner"` | Solo filas que calzan en ambas tablas |
| `how="left"` | Todas las filas de la tabla principal, aunque no calzen |
| `groupby()` | Tabla dinámica (pivot) de Excel |
| `sum()` | Campo de valor "Suma" en la tabla dinámica |
| Fila huérfana | Una fila sin pareja en el BUSCARV (devuelve #N/A) |

---

## 3. Antes de empezar: Verificación de prerrequisitos

### Conocimientos necesarios del módulo R1-02

- [ ] Sé cargar un CSV con `pd.read_csv("archivo.csv")`
- [ ] Sé ver las primeras filas con `.head()`
- [ ] Sé conocer el tamaño de una tabla con `.shape` o `len(df)`
- [ ] Sé ver los nombres de columnas con `.columns`
- [ ] Entiendo qué es un DataFrame y qué es una columna

> 💡 Si marcaste menos de 4, te recomiendo repasar R1-02 antes de continuar.

### Dataset de este módulo

Trabajarás con **dos archivos CSV** de datos reales de ChileCompra:

- `ordenes.csv` — órdenes de compra (columnas: `codigo_oc`, `entcode`, `rubro`, `monto`)
- `organismos.csv` — catálogo de organismos (columnas: `entcode`, `organismo`, `region`)

Ambos se cargan automáticamente en la primera celda del notebook si estás en Google Colab.

---

## 4. Guía paso a paso por sección del notebook

### Sección de carga: Cargar los datos

🎯 **Objetivo:** Tener dos DataFrames listos en memoria y verificar que se cargaron bien.

💡 **Concepto clave:** A diferencia de R1-02 donde cargabas *una* tabla, ahora cargas *dos* tablas separadas. Esto refleja cómo los datos reales del Estado están organizados: en bases de datos relacionales, los datos se guardan separados para no repetir información.

🔍 **Qué hace el código:**
```python
df_ordenes = pd.read_csv("ordenes.csv")
df_organismos = pd.read_csv("organismos.csv")
print(f"Órdenes: {len(df_ordenes)} filas  |  Organismos: {len(df_organismos)} filas")
```
- Línea 1: carga las órdenes de compra en un DataFrame
- Línea 2: carga el catálogo de organismos en otro DataFrame
- Línea 3: imprime cuántas filas tiene cada uno para verificar

⚠️ **Error frecuente:** Si ves `FileNotFoundError`, el archivo no está en la carpeta correcta. En Colab, la celda de descarga automática lo resuelve; si falla, sube el archivo manualmente con el botón de archivos de Colab.

✅ **Sabes esta sección cuando puedes:** decir cuántas órdenes hay y cuántos organismos hay en el catálogo, mirando el output del `print`.

---

### Sección 1: ¿Por qué dos tablas? La llave que las une

🎯 **Objetivo:** Entender por qué los datos están separados y qué es una llave.

💡 **Concepto clave — La analogía del BUSCARV:** ¿Alguna vez usaste `BUSCARV` para traer, desde otra hoja, el nombre del ministerio que corresponde a un código? `merge` hace exactamente eso, pero para **toda la tabla de una vez** y sin arrastrar fórmulas fila por fila.

La razón por la que los datos están separados es eficiencia: guardar el nombre completo del organismo en cada una de las 1,8 millones de órdenes de ChileCompra significaría repetir "Ministerio de Salud" cientos de miles de veces. Y si alguien escribe mal el nombre en una fila, el error se propaga. Por eso los sistemas guardan solo el **código** en las órdenes, y el catálogo aparte dice qué significa ese código.

La columna que está en **ambas tablas** y permite unirlas se llama la **llave** (aquí, `entcode`).

⚠️ **Error frecuente:** Asumir que la llave se llama igual en ambas tablas. Siempre revisa `df.columns` en cada una antes de cruzar.

✅ **Sabes esta sección cuando puedes:** identificar cuál columna es la llave mirando las columnas de ambas tablas, y explicar en tus palabras por qué los datos están separados.

---

### Sección 2: El cruce — `pd.merge()`

🎯 **Objetivo:** Ejecutar el cruce básico y verificar que el resultado tiene las columnas de ambas tablas.

💡 **Concepto clave:** `pd.merge()` es la operación de pegar dos tablas por una columna en común. El resultado es una **tabla ancha**: cada orden, ahora con su nombre de organismo y región al lado.

```python
pd.merge(df_ordenes, df_organismos, on="entcode")
```

🔍 **Qué hace el código, línea por línea:**
- `df_ordenes` → la tabla **izquierda** (la principal, la que manda)
- `df_organismos` → la tabla **derecha** (la que trae información adicional)
- `on="entcode"` → la columna llave por la que se emparejan las filas
- El resultado: una fila por cada orden, ahora con las columnas de organismos pegadas al lado

⚠️ **Error frecuente:** Poner los argumentos al revés. Aunque en este caso el resultado es similar, la convención es: la tabla con todos los datos que quieres conservar va **a la izquierda** (`df_ordenes`).

✅ **Sabes esta sección cuando puedes:** verificar con `.columns` que el resultado tiene columnas de las dos tablas originales (`monto` de órdenes y `region` del catálogo).

---

### Sección 3: Tipos de cruce — `inner` vs `left`

🎯 **Objetivo:** Entender qué filas se pierden con `inner` y cómo recuperarlas con `left`.

💡 **Concepto clave — La fila huérfana:** Imagina que tienes una lista de proveedores y haces BUSCARV para traer su nombre. Si el RUT del proveedor no está en el catálogo, esa fila devuelve `#N/A`. En pandas, el comportamiento depende del tipo de cruce:

| Tipo | ¿Qué conserva? | Equivalente en Excel |
|---|---|---|
| `how="inner"` (defecto) | Solo filas con pareja en **ambas** tablas | BUSCARV que elimina los #N/A |
| `how="left"` | **Todas** las filas de la tabla izquierda | BUSCARV que deja los #N/A como NaN |

> ⚠️ El `inner` es **el defecto** y el **error más silencioso de datos**: si usas `inner` y hay órdenes cuyo `entcode` no está en el catálogo, esas órdenes desaparecen sin ningún aviso. Compara siempre `len()` antes y después del cruce.

🔍 **Qué hace el código:**
```python
inner = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")
left  = pd.merge(df_ordenes, df_organismos, on="entcode", how="left")

print(f"Órdenes originales:  {len(df_ordenes)}")
print(f"Tras cruce inner:    {len(inner)}  (perdidas: {len(df_ordenes) - len(inner)})")
print(f"Tras cruce left:     {len(left)}")

print(left[left["region"].isna()])  # muestra las filas huérfanas
```
- Compara los tamaños de los tres DataFrames
- Las filas donde `region` es vacía (`NaN`) son las órdenes sin organismo en el catálogo

✅ **Sabes esta sección cuando puedes:** explicar cuántas filas se pierden con `inner` y por qué, y saber cuándo usar `left` en tu trabajo.

---

### Sección 4: Unir y resumir con `groupby()`

🎯 **Objetivo:** Usar `groupby` para sumar el monto de compras por región y responder la pregunta de gestión.

💡 **Concepto clave — La tabla dinámica real:** En R1-02 usaste `value_counts()` para **contar** cuántas filas hay por categoría. Cuando necesitas **sumar** una columna numérica (como el monto) por categoría, usas `groupby`:

```python
df.groupby("region")["monto"].sum()
```

Esto es exactamente una **tabla dinámica de Excel**: agrupa las filas por región y suma el monto de cada grupo.

🔍 **Qué hace el código:**
```python
gasto_region = df_cruce.groupby("region")["monto"].sum().sort_values(ascending=False)
```
- `.groupby("region")` → agrupa el DataFrame por los valores únicos de la columna `region`
- `["monto"]` → dentro de cada grupo, trabaja con la columna `monto`
- `.sum()` → suma todos los montos de cada grupo
- `.sort_values(ascending=False)` → ordena de mayor a menor para ver quién lidera

⚠️ **Error frecuente:** Aplicar `groupby` antes del `merge`. Si lo haces sobre `df_ordenes` que no tiene `region`, obtendrás un `KeyError`.

✅ **Sabes esta sección cuando puedes:** leer el output del `groupby` e identificar qué región lidera el gasto, y explicarle a tu jefatura qué significa ese número.

---

### Errores típicos al cruzar (guía de referencia rápida)

| Error | Causa | Solución |
|---|---|---|
| `KeyError: 'entcode'` | La llave no existe o tiene distinto nombre en cada tabla | Revisar `.columns` en ambas; si difieren, usar `left_on=` y `right_on=` |
| El cruce devuelve 0 filas | La llave existe pero con tipos distintos (número vs. texto) | Convertir a mismo tipo antes del merge: `df["entcode"] = df["entcode"].astype(str)` |
| Se perdieron filas sin aviso | Se usó `inner` con filas huérfanas | Comparar `len()` antes y después; usar `how="left"` para no perder filas |
| La tabla creció más de lo esperado | La llave está duplicada en la tabla derecha | Verificar que la llave sea única en el catálogo: `df.duplicated("entcode").sum()` |

---

## 5. Guía de los 4 ejercicios

### Ejercicio 01 · Encontrar la llave

**Qué habilidad entrena:** Antes de cruzar, siempre hay que identificar la columna que es común a las dos tablas. Este ejercicio entrena ese hábito.

**Qué debes hacer:** Guardar en `llave` el nombre (como texto entre comillas) de la columna que está en ambas tablas; en `n_ordenes` la cantidad de filas de `df_ordenes`; y en `n_organismos` la cantidad de filas de `df_organismos`.

**Pistas progresivas:**
- 🟢 *Pista suave:* Usa `.columns` en ambos DataFrames y busca el nombre que aparece en las dos listas.
- 🟡 *Pista media:* La llave es siempre el código que conecta ambas tablas. En el ejemplo de la sección 1, ¿cuál columna aparece en la tabla de órdenes Y en el catálogo?
- 🔴 *Pista directa:* Mira los encabezados de los datos del módulo: `ordenes.csv` tiene `codigo_oc, entcode, rubro, monto` y `organismos.csv` tiene `entcode, organismo, region`. ¿Cuál es la única columna común?

**Lógica de la solución:** La llave es la columna `entcode` porque es la única que aparece en ambas tablas. Para los conteos, `len(df)` o `df.shape[0]` te dan la cantidad de filas.

**Qué significa el ✅:** Que identificaste correctamente la columna llave y tienes los conteos correctos de ambas tablas. Estás listo para cruzar.

---

### Ejercicio 02 · El primer cruce

**Qué habilidad entrena:** Ejecutar el merge básico y verificar que el resultado tiene las columnas de ambas tablas.

**Qué debes hacer:** Cruzar `df_ordenes` con `df_organismos` por `entcode` usando el tipo de cruce por defecto (inner), guardar en `df_cruce` y en `n_cruce` la cantidad de filas.

**Pistas progresivas:**
- 🟢 *Pista suave:* La sintaxis básica es `pd.merge(tabla_izquierda, tabla_derecha, on="llave")`.
- 🟡 *Pista media:* El primer argumento es `df_ordenes`, el segundo es `df_organismos`, el tercer argumento es `on="entcode"`.
- 🔴 *Pista directa:* `df_cruce = pd.merge(df_ordenes, df_organismos, on="entcode")` — sin especificar `how`, usa `inner` por defecto.

**Lógica de la solución:** Con `inner`, el resultado tendrá solo las órdenes cuyo `entcode` existe en el catálogo. Por eso `n_cruce` será *menor* que `n_ordenes`: las órdenes huérfanas desaparecen.

**Qué significa el ✅:** Que tu cruce tiene las columnas correctas (incluyendo `region` que viene del catálogo) y el número de filas esperado (menor que el original por las huérfanas).

---

### Ejercicio 03 · Inner vs left: cazar la fila huérfana

**Qué habilidad entrena:** Usar `how="left"` para no perder filas y detectar los registros sin pareja en el catálogo.

**Qué debes hacer:** Guardar en `df_left` el cruce con `how="left"` y en `n_perdidas` cuántas filas quedaron con `region` vacía.

**Pistas progresivas:**
- 🟢 *Pista suave:* Es igual al Ejercicio 02 pero agrega `how="left"` como cuarto argumento.
- 🟡 *Pista media:* Para contar los valores nulos de la columna `region`, puedes usar `.isna()` que devuelve True/False para cada fila, y `.sum()` cuenta los True.
- 🔴 *Pista directa:* `df_left = pd.merge(df_ordenes, df_organismos, on="entcode", how="left")` y luego `n_perdidas = df_left["region"].isna().sum()`.

**Lógica de la solución:** Con `how="left"`, el DataFrame resultante tiene **exactamente** las mismas filas que `df_ordenes`. Las órdenes sin organismo en el catálogo quedan con `NaN` en `organismo` y `region`. Contar esos `NaN` revela las filas huérfanas.

**Qué significa el ✅:** Que `df_left` tiene el mismo número de filas que `df_ordenes` (ninguna fila se perdió) y que identificaste al menos 1 orden sin organismo en el catálogo. Esto es un hallazgo real: esa orden existe en MercadoPúblico pero no tiene organismo registrado en el catálogo.

---

### Ejercicio 04 · La pregunta real: ¿qué región concentra más gasto?

**Qué habilidad entrena:** Usar `groupby` para responder una pregunta de política pública concreta a partir de datos cruzados.

**Qué debes hacer:** Guardar en `gasto_por_region` el gasto total por región (ordenado de mayor a menor) y en `region_top` el nombre de la región que más gasta. Luego reflexionar en la celda de texto qué le dirías a tu jefatura.

**Pistas progresivas:**
- 🟢 *Pista suave:* Usa `df_cruce` (del Ejercicio 02, que ya tiene la columna `region`). Aplica `.groupby("region")` seguido de `["monto"].sum()`.
- 🟡 *Pista media:* Para ordenar de mayor a menor agrega `.sort_values(ascending=False)`. Para obtener la primera región del resultado usa `.index[0]`.
- 🔴 *Pista directa:* `gasto_por_region = df_cruce.groupby("region")["monto"].sum().sort_values(ascending=False)` y `region_top = gasto_por_region.index[0]`.

**Lógica de la solución:** `groupby` crea grupos de filas con el mismo valor en `region`, luego `sum()` suma el `monto` dentro de cada grupo. El resultado es una Serie indexada por nombre de región. `.index[0]` accede al nombre de la primera región (la de mayor gasto).

**Qué significa el ✅:** Que calculaste correctamente el gasto por región y que identificaste la región líder. Completaste todo el módulo — ahora puedes responder una pregunta real de gestión pública con datos.

---

## 6. El ejercicio 04 en profundidad: Interpretar para decidir

### ¿Qué nos dice la distribución del gasto por región?

Cuando el groupby muestra que una región concentra la mayor parte del gasto en compras públicas, ese dato tiene varias lecturas posibles:

- **Puede ser esperado:** si es la Región Metropolitana, es donde está la mayoría de los organismos y la mayor cantidad de funcionarios, por lo que más gasto no es necesariamente un problema.
- **Puede ser relevante para la gestión:** si una región periférica aparece con gasto desproporcionado en un rubro específico, merece investigación.
- **Puede ser un artefacto del dato:** si la región con más gasto corresponde a organismos con `entcode` sin región identificada o con errores en el catálogo, el dato puede estar distorsionado.

### Reflexión guiada

1. ¿La región con más gasto tiene proporción de organismos similar a su participación en el gasto? ¿O hay desproporción?
2. ¿El resultado cambiaría si miraras por **rubro** en vez de por región? (Pista: cambia `"region"` por `"rubro"` en el groupby)
3. ¿Qué pasaría si incluyeras las filas huérfanas del `df_left`? ¿Cuánto monto representan?

### Pregunta de debate

> ¿Qué otro dato pedirías para decidir si la concentración de gasto en la región líder es un problema de política pública o es simplemente reflejo del tamaño de esa región?

Algunas respuestas posibles: número de licitaciones (no solo monto), cantidad de organismos por región, población regional, presupuesto asignado por región.

---

## 7. Conexión con el módulo de profundización (`profundiza.ipynb`)

| Tema | `leccion.ipynb` (nivel práctico) | `profundiza.ipynb` (nivel teórico) |
|---|---|---|
| Tipos de cruce | Inner y left con ejemplos concretos | Right, outer y full join; cuándo usar cada uno |
| Llaves duplicadas | Mención en errores típicos | Análisis de cardinalidad (1:1, 1:N, N:M) |
| groupby | sum() por una columna | agg() con múltiples funciones, transform(), apply() |
| Datos faltantes tras merge | Detectar NaN con `.isna()` | Imputación, decisiones de diseño |
| Rendimiento | Sin mención | merge con índices para grandes datasets |

**¿Cuándo ir al profundiza?**
- Si tienes datos reales con llaves duplicadas y no sabes cómo manejarlos
- Si necesitas múltiples funciones de agregación a la vez (suma, promedio, conteo en una sola operación)
- Si tu institución trabaja con tablas de más de 100.000 filas y el merge es lento

**¿Para quién es?** Analistas de datos con experiencia previa en bases de datos o SQL, o participantes que quieran prepararse para R1-05 · SQL con más fundamentos conceptuales.

---

## 8. Autoevaluación Final

Responde sin mirar el notebook:

**1. ¿Qué significa `on="entcode"` en `pd.merge()`?**
- a) Que se deben usar solo las columnas llamadas `entcode` en el resultado
- b) Que las filas se emparejarán comparando los valores de esa columna en ambas tablas ✅
- c) Que se ordena el resultado por esa columna
- d) Que se eliminan las filas donde `entcode` sea nulo

*Explicación:* `on=` indica la columna llave. pandas busca cada valor de `entcode` en la tabla izquierda y lo empareja con la fila de la tabla derecha que tiene el mismo valor. Es exactamente el mecanismo del BUSCARV.

---

**2. ¿Qué diferencia hay entre `how="inner"` y `how="left"`?**
- a) `inner` es más lento que `left`
- b) `inner` solo conserva filas con pareja en ambas tablas; `left` conserva todas las de la tabla izquierda ✅
- c) `left` solo funciona cuando la llave está en la columna del lado izquierdo
- d) No hay diferencia práctica

*Explicación:* `inner` es como una intersección: solo filas que calzan. `left` es más conservador: no bota ninguna fila de la tabla principal, aunque queden con `NaN` en las columnas del catálogo.

---

**3. Tienes `df_ordenes` (50 filas) y haces un merge inner con `df_organismos`. El resultado tiene 47 filas. ¿Qué significa?**
- a) pandas eliminó filas duplicadas automáticamente
- b) El catálogo de organismos tiene 47 entradas
- c) 3 órdenes tenían un `entcode` que no existe en el catálogo ✅
- d) El merge siempre reduce el tamaño del DataFrame

*Explicación:* Con `inner`, cada fila del resultado necesita pareja en ambas tablas. Si 3 órdenes tienen un `entcode` que no aparece en `organismos.csv`, esas 3 filas desaparecen silenciosamente.

---

**4. ¿Qué hace `df_cruce.groupby("region")["monto"].sum()`?**
- a) Selecciona solo las columnas `region` y `monto`
- b) Agrupa las filas por región y suma el monto total de cada región ✅
- c) Ordena el DataFrame por región y luego por monto
- d) Cuenta cuántas filas hay por región

*Explicación:* `groupby("region")` crea grupos de filas con el mismo valor en `region`. `["monto"].sum()` suma los valores de `monto` dentro de cada grupo. Es la tabla dinámica de pandas.

---

**5. ¿Cuál es el orden correcto de las operaciones para responder "¿qué región gasta más"?**
- a) groupby → merge → sum
- b) sum → groupby → merge
- c) merge → groupby → sum ✅
- d) merge → sum → groupby

*Explicación:* Primero debes **cruzar** las tablas (merge) para que cada orden tenga su región. Luego **agrupar** por región (groupby). Finalmente **sumar** el monto de cada grupo. Sin el merge previo, `df_ordenes` no tiene la columna `region` y el groupby fallaría.

---

## 9. Glosario del Módulo

| Término | Definición simple | Equivalente en Excel / administración |
|---|---|---|
| **merge** | Operación que pega dos tablas comparando una columna en común | BUSCARV / VLOOKUP |
| **llave (key)** | Columna que existe en ambas tablas y sirve para emparejar filas | La columna de búsqueda del BUSCARV |
| **entcode** | Código único que identifica a cada organismo público | RUT del organismo |
| **inner join** | Tipo de cruce que solo conserva filas con pareja en ambas tablas | BUSCARV que devuelve #N/A para los no encontrados (y los elimina) |
| **left join** | Tipo de cruce que conserva todas las filas de la tabla izquierda | BUSCARV que deja los #N/A visibles |
| **fila huérfana** | Fila de la tabla izquierda cuya llave no existe en la tabla derecha | Una fila con #N/A en el BUSCARV |
| **NaN** | Valor vacío (Not a Number) — aparece cuando no hay pareja en el join | Celda vacía o #N/A |
| **groupby** | Operación que agrupa filas por una categoría y aplica una función | Tabla dinámica (pivot table) de Excel |
| **sum()** | Suma los valores de un grupo | Campo "Suma de monto" en tabla dinámica |
| **sort_values()** | Ordena el resultado de mayor a menor (o viceversa) | Ordenar columna en Excel |
| **catálogo** | Tabla que traduce códigos a nombres y describe entidades | Hoja de referencia con la lista de organismos |
| **base de datos relacional** | Sistema donde la información se guarda en tablas separadas que se relacionan por llaves | Múltiples hojas de Excel relacionadas por BUSCARV |

---

## 10. Conexión con el siguiente módulo

### ¿Qué viene en R1-04 · Limpieza de datos?

En este módulo cruzaste tablas suponiendo que los datos están limpios: que `entcode` en `ordenes.csv` y en `organismos.csv` tienen exactamente el mismo formato. Pero en el mundo real del Estado chileno, una tabla puede tener `" 6931"` (con espacio al inicio) y la otra `"6931"`. Para `merge`, esos son valores distintos y la fila queda huérfana aunque el organismo sí existe en el catálogo.

R1-04 te enseña a dejar las llaves impecables antes de cruzar: eliminar espacios, estandarizar mayúsculas, convertir tipos, detectar y reparar inconsistencias.

### Pregunta motivadora

> Terminaste este módulo sabiendo cruzar tablas perfectas. Pero, ¿qué pasa cuando el `entcode` en las órdenes tiene espacios, guiones o letras mayúsculas que en el catálogo no? ¿Cuántas órdenes "huérfanas" son en realidad errores de tipeo que se pueden reparar?

Esa es la pregunta que responde **R1-04 · Limpieza de datos**. ¡Nos vemos allá!

---

*Guía elaborada para el Bootcamp de Datos para Funcionarios Públicos — Formación Pública. Rama R1 · Análisis y Visualización. Módulo R1-03.*