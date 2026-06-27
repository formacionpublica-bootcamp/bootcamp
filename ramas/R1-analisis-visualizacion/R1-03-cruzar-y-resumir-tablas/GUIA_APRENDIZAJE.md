# Guía de Aprendizaje — R1-03 · Cruzar y resumir tablas

> **Rama:** R1 · Análisis y Visualización | **Módulo:** R1-03 | **Nivel:** Introductorio-Intermedio
> **Duración estimada:** 3–4 horas | **Prerrequisitos:** R1-02 · Exploración con pandas
> **Competencia de salida:** Cruzar dos tablas por su llave con `merge`, detectar filas huérfanas, y resumir el resultado con `groupby` para responder preguntas reales de gestión pública.

---

## 1. ¿Para qué me sirve esto como funcionario/a público/a?

En el trabajo del Estado, la información casi nunca vive en un solo archivo. Los **montos** de las órdenes de compra están en una tabla; el **nombre del organismo y su región** en otra. Para responder *"¿qué región concentró más gasto en compras públicas?"* necesitas combinar ambas.

Eso es exactamente lo que aprenderás aquí: **cruzar tablas** (como el `BUSCARV` de Excel, pero para toda la tabla de una vez) y **resumir por grupos** (como una tabla dinámica completa). Son las dos habilidades que convierten "sé abrir un CSV" en "puedo responder una pregunta real a mi jefatura".

En este módulo trabajarás con **órdenes de compra reales de ChileCompra** — el portal de compras públicas del Estado chileno. Dos tablas, relacionadas por un código de organismo, igual que en cualquier base de datos del sector público.

---

## 2. Mapa conceptual del módulo

| Concepto pandas | Equivalente en tu trabajo | Para qué sirve |
|---|---|---|
| `pd.merge()` | BUSCARV / VLOOKUP en Excel | Unir dos tablas por una columna en común |
| `llave` (`entcode`) | El RUT o código del organismo | La columna que identifica de forma única cada entidad |
| `how="inner"` | Solo filas que coinciden en ambas tablas | Cruce estricto; puede perder datos |
| `how="left"` | Conservar todas las filas de la tabla izquierda | Cruce seguro; revela datos faltantes |
| `NaN` en el cruce | Celda en blanco tras el BUSCARV | Indica que no se encontró pareja en el catálogo |
| `groupby()` | Tabla dinámica de Excel | Agrupar por categoría y calcular suma/promedio |
| `.sum()` / `.mean()` | SUMA / PROMEDIO en tabla dinámica | Agregar valores dentro de cada grupo |

---

## 3. Antes de empezar: Verificación de prerrequisitos

Este módulo construye directamente sobre R1-02. Marca cada punto honestamente:

- [ ] Puedo cargar un CSV con `pd.read_csv()` y obtener un DataFrame
- [ ] Sé usar `.shape`, `.columns` e `.info()` para inspeccionar una tabla
- [ ] Sé filtrar filas con una condición: `df[df["columna"] == "valor"]`
- [ ] Sé usar `.value_counts()` para contar por categoría
- [ ] Entiendo qué es `NaN` (valor vacío/faltante)

Si tienes dudas en alguno, repasa **R1-02 · Exploración con pandas** antes de continuar.

---

## 4. Guía paso a paso por sección del notebook

### Sección 1 · ¿Por qué dos tablas? La llave que las une

**🎯 Objetivo:** Entender por qué los datos del Estado viven separados y qué es una llave.

**💡 Concepto clave:** Guardar el nombre completo de cada organismo en cada una de las millones de órdenes de compra sería repetir lo mismo infinitas veces — y arrastrar errores de tipeo en cada copia. Por eso las bases de datos del Estado guardan las órdenes con un **código** (`entcode`) y tienen un **catálogo aparte** que dice qué organismo es cada código.

Es exactamente como en Recursos Humanos: la planilla de pagos no repite el nombre del funcionario en cada línea — usa su RUT, y el RUT apunta al registro del funcionario.

**🔍 Estructura del dataset:**

`ordenes.csv` — 21 órdenes de compra reales de ChileCompra:
```
codigo_oc | entcode | rubro                    | monto
1         | 6919    | Servicios de transporte  | 1,584,900
2         | 6919    | Servicios agrícolas...   | 1,134,900
...
```

`organismos.csv` — catálogo de 6 organismos:
```
entcode | organismo                    | region
6919    | Servicio Agrícola y Ganadero | Region del Nuble
6924    | Corp Nacional Forestal       | Region de Antofagasta
...
```

⚠️ **Dato clave para los ejercicios:** El dataset tiene **un organismo huérfano a propósito** — el `entcode` 6956 aparece en 3 órdenes de `ordenes.csv` pero **no existe** en `organismos.csv`. Esto simula una situación real: códigos que aún no están en el catálogo.

**✅ Sabes esta sección cuando puedes:** Explicar qué es `entcode` y por qué existe en ambas tablas.

---

### Sección 2 · El cruce: `pd.merge()`

**🎯 Objetivo:** Unir las dos tablas para que cada orden tenga el nombre y región de su organismo.

**💡 Concepto clave:** `pd.merge()` es el BUSCARV de pandas, pero mejor: no arrastras fórmulas, no te equivocas de columna, y funciona con millones de filas en un segundo.

```python
df_cruce = pd.merge(df_ordenes, df_organismos, on="entcode")
```

**🔍 ¿Qué hace cada parte?**
- `df_ordenes` → la tabla **izquierda** (tus órdenes de compra)
- `df_organismos` → la tabla **derecha** (el catálogo)
- `on="entcode"` → la **llave**: la columna que existe en ambas tablas y permite emparejarlas
- El resultado: una tabla ancha donde cada orden tiene su `organismo` y `region` al lado

**⚠️ Error frecuente:** `KeyError: 'entcode'` — significa que la llave no se llama igual en ambas tablas. Usa `df.columns` en cada una para verificar. Si los nombres difieren, usa `left_on="nombre_en_izquierda"` y `right_on="nombre_en_derecha"`.

**✅ Sabes esta sección cuando puedes:** Ejecutar el merge y ver las columnas `organismo` y `region` en el resultado.

---

### Sección 3 · Tipos de cruce: `inner` vs `left` (la fila huérfana)

**🎯 Objetivo:** Entender qué pasa con las órdenes cuyo organismo no está en el catálogo.

**💡 Concepto clave:** El tipo de cruce define qué se hace con las filas que no encontraron pareja.

```python
# inner (defecto): solo conserva las filas con pareja en ambas tablas
inner = pd.merge(df_ordenes, df_organismos, on="entcode", how="inner")

# left: conserva TODAS las órdenes; las huérfanas quedan con NaN
left = pd.merge(df_ordenes, df_organismos, on="entcode", how="left")
```

**🔍 Con los datos reales del módulo:**

| Cruce | Filas resultado | ¿Qué pasó? |
|---|---|---|
| `inner` (defecto) | 18 | Se perdieron 3 órdenes (el organismo 6956 no está en el catálogo) |
| `left` | 21 | Se conservaron todas; las 3 de 6956 quedaron con `region = NaN` |

> **Regla práctica para el sector público:** Si la tabla izquierda es tu universo completo (todas las órdenes), usa siempre `how="left"` y luego revisa cuántas quedaron huérfanas. El cruce `inner` descarta datos **en silencio** — es la causa #1 de "me faltan registros y no sé por qué".

**⚠️ Error frecuente:** Usar `inner` sin darse cuenta de que se perdieron filas. Siempre compara `len(df_ordenes)` vs `len(resultado)` después de un merge.

**✅ Sabes esta sección cuando puedes:** Explicar por qué el cruce inner perdió 3 filas y dónde aparecen esas 3 filas en el cruce left.

---

### Sección 4 · Unir y resumir: la pregunta real (`groupby`)

**🎯 Objetivo:** Responder "¿qué región concentra más gasto?" con una sola operación.

**💡 Concepto clave:** En R1-02 usaste `value_counts()` para **contar** cuántas veces aparecía cada valor. Para **sumar** una columna numérica por categoría, se usa `groupby()`.

```python
gasto_region = df_cruce.groupby("region")["monto"].sum().sort_values(ascending=False)
```

**🔍 ¿Qué hace cada parte?**
- `.groupby("region")` → agrupa todas las filas que tienen la misma región
- `["monto"]` → selecciona la columna que quieres agregar
- `.sum()` → suma los montos de cada grupo
- `.sort_values(ascending=False)` → ordena de mayor a menor

**Resultado real con los datos del módulo:**

| Región | Gasto total |
|---|---|
| Region de Arica y Parinacota | $147,085,379 |
| Region de Tarapaca | $62,445,305 |
| Region de Coquimbo | $40,739,516 |
| Region Metropolitana de Santiago | $38,914,000 |
| Region de Antofagasta | $11,733,000 |
| Region del Nuble | $7,719,800 |

> **Nota de política pública:** Este resultado usa el cruce `inner`, que **descartó** $63,283,673 en órdenes del organismo huérfano (6956). Un analista riguroso informaría ese monto como "gasto no atribuido a región" antes de presentar el ranking.

**⚠️ Error frecuente:** Aplicar `groupby` antes de hacer el merge. Necesitas la columna `region` en la tabla para poder agrupar por ella.

**✅ Sabes esta sección cuando puedes:** Producir el ranking de gasto por región y explicar qué significa el primer lugar.

---

### Sección 5 · Errores típicos al cruzar

| Error | Mensaje | Causa | Solución |
|---|---|---|---|
| `KeyError: 'entcode'` | Llave no encontrada | La columna no se llama igual en ambas tablas | Verifica con `df.columns`; usa `left_on` / `right_on` |
| Cruce devuelve 0 filas | DataFrame vacío | Los tipos de dato difieren (número vs texto) | Convierte al mismo tipo antes: `df["entcode"] = df["entcode"].astype(str)` |
| Tabla creció más de lo esperado | Más filas que las originales | La llave está duplicada en la tabla derecha | Verifica con `df_organismos["entcode"].duplicated().sum()` |
| Se perdieron filas | Menos filas que las originales | Se usó `inner` con huérfanas | Usa `how="left"` y revisa los `NaN` |

---

## 5. Guía de los 4 Ejercicios

### Ejercicio 01 · Encontrar la llave

**Habilidad que entrena:** Identificar la columna común entre dos tablas antes de cruzar.

**Pista suave 🟢:** Mira `df_ordenes.columns` y `df_organismos.columns`. ¿Qué nombre aparece en ambas listas?

**Pista media 🟡:** La llave es el código que identifica al organismo comprador. Es la misma columna que conecta las dos tablas.

**Pista directa 🔴:** La columna se llama `"entcode"`. Guárdala como texto: `llave = "entcode"`. Para `n_ordenes` y `n_organismos` usa `.shape[0]` o `len()`.

**Lógica de la solución:** Antes de cualquier merge, debes confirmar que la llave existe en ambas tablas. `n_ordenes = 21`, `n_organismos = 6`.

**✅ El chequeo automático valida que:** `llave == "entcode"`, `n_ordenes == 21` y `n_organismos == 6`.

---

### Ejercicio 02 · El primer cruce

**Habilidad que entrena:** Ejecutar `pd.merge()` y entender que el tipo por defecto (`inner`) puede descartar filas.

**Pista suave 🟢:** Usa `pd.merge()` con tres argumentos: la tabla izquierda, la tabla derecha y `on="entcode"`.

**Pista media 🟡:** No necesitas especificar `how=` para este ejercicio. El cruce por defecto es `inner`. Guarda el resultado en `df_cruce` y cuenta sus filas.

**Pista directa 🔴:** `df_cruce = pd.merge(df_ordenes, df_organismos, on="entcode")`. El `n_cruce` será menor que 21.

**Lógica de la solución:** El cruce `inner` descarta las 3 órdenes del organismo 6956 (que no está en el catálogo). Resultado: `n_cruce = 18`.

**✅ El chequeo automático valida que:** `df_cruce` tiene 18 filas, contiene las columnas `monto` y `region`, y `n_cruce < 21`.

---

### Ejercicio 03 · Inner vs left: cazar la fila huérfana

**Habilidad que entrena:** Usar `how="left"` para no perder registros y detectar cuáles quedaron sin pareja.

**Pista suave 🟢:** El cruce `left` conserva todas las filas de la tabla izquierda. Las que no encontraron pareja tendrán `NaN` en las columnas del catálogo.

**Pista media 🟡:** Para contar los huérfanos: `df_left["region"].isna().sum()`. Piensa: ¿cuántas órdenes tiene el organismo 6956?

**Pista directa 🔴:** `df_left = pd.merge(df_ordenes, df_organismos, on="entcode", how="left")`. `n_perdidas = df_left["region"].isna().sum()`.

**Lógica de la solución:** El organismo 6956 tiene 3 órdenes que no encuentran pareja en el catálogo. Con `how="left"` esas 3 filas se conservan con `region = NaN`. Resultado: `n_perdidas = 3`.

**✅ El chequeo automático valida que:** `df_left` tiene 21 filas y `n_perdidas == 3`.

---

### Ejercicio 04 · La pregunta real: ¿qué región concentra más gasto?

**Habilidad que entrena:** Combinar `groupby` + `sum` + `sort_values` para producir un ranking de gestión pública.

**Pista suave 🟢:** Necesitas agrupar `df_cruce` por la columna `region` y sumar la columna `monto`. ¿Qué método de pandas hace eso?

**Pista media 🟡:** `groupby("region")["monto"].sum()` te da la suma por región. Para ordenar de mayor a menor agrega `.sort_values(ascending=False)`.

**Pista directa 🔴:** `gasto_por_region = df_cruce.groupby("region")["monto"].sum().sort_values(ascending=False)`. `region_top = gasto_por_region.index[0]`.

**Lógica de la solución:** Al agrupar por región y sumar montos, la Región de Arica y Parinacota encabeza el ranking con $147,085,379. Esto se explica porque el Servicio de Cooperación Técnica (6950), que tiene las órdenes más grandes del dataset, tiene su sede registrada en esa región.

**✅ El chequeo automático valida que:** `region_top == "Region de Arica y Parinacota"` y el monto del primer lugar coincide.

---

## 6. El Ejercicio 04 en profundidad: Interpretar para decidir

### Los números del ranking

| Región | Gasto total | % del total |
|---|---|---|
| Arica y Parinacota | $147,085,379 | ~47% |
| Tarapacá | $62,445,305 | ~20% |
| Coquimbo | $40,739,516 | ~13% |
| Metropolitana | $38,914,000 | ~12% |
| Antofagasta | $11,733,000 | ~4% |
| Ñuble | $7,719,800 | ~2% |
| **Sin atribuir** (6956) | **$63,283,673** | **~17%** |

### Reflexión guiada

La Región de Arica y Parinacota lidera el ranking, pero no porque esa región tenga más organismos o población. Es porque el **Servicio de Cooperación Técnica**, que registra sede en esa región, concentra las órdenes de mayor valor unitario del dataset.

Esto ilustra un problema clásico del análisis de compras públicas: **la región de la sede del organismo no es necesariamente donde se ejecuta el gasto**. Un organismo con sede en Arica puede estar comprando servicios que se prestan en todo el país.

Además, hay **$63,283,673 (17% del gasto total) que no se puede atribuir a ninguna región** porque el organismo 6956 no está en el catálogo. Presentar el ranking sin mencionar ese dato sería un análisis incompleto.

### Pregunta de debate

> *¿Qué le dirías a tu jefatura con este resultado? ¿Qué pregunta nueva te abre este análisis?*

Algunas respuestas posibles:
- ¿Cuál es el gasto por rubro dentro de la región líder?
- ¿Qué organismo específico dentro de Metropolitana gasta más?
- ¿Por qué el organismo 6956 no está en el catálogo? ¿Es un error de carga o un organismo nuevo?
- ¿Cómo cambia el ranking si se excluyen los servicios de consultoría y se mira solo gasto en servicios directos a la ciudadanía?

---

## 7. Autoevaluación Final

**Pregunta 1.** ¿Qué hace `pd.merge(df_a, df_b, on="codigo")`?
- A) Concatena las tablas una debajo de la otra
- B) Une las tablas emparejando filas donde `codigo` tiene el mismo valor en ambas ✅
- C) Multiplica los valores de la columna `codigo`
- D) Elimina duplicados en la columna `codigo`

*Explicación: `merge` es una unión horizontal (une columnas de dos tablas por una llave común), no vertical como `pd.concat`.*

---

**Pregunta 2.** ¿Cuál es la diferencia clave entre `how="inner"` y `how="left"`?
- A) `inner` es más rápido; `left` es más preciso
- B) `inner` conserva solo filas con pareja en ambas tablas; `left` conserva todas las de la tabla izquierda ✅
- C) `inner` une por la izquierda; `left` une por la derecha
- D) No hay diferencia, son sinónimos

*Explicación: El tipo de cruce define qué se hace con las filas que no tienen pareja. `inner` las descarta; `left` las conserva con NaN.*

---

**Pregunta 3.** Tienes 21 órdenes y haces un `inner merge`. El resultado tiene 18 filas. ¿Qué significa?
- A) Hay 3 filas duplicadas que se eliminaron
- B) Hay un error en el código
- C) 3 órdenes no encontraron pareja en el catálogo y se descartaron ✅
- D) La tabla derecha solo tiene 18 registros

*Explicación: El cruce `inner` descarta filas sin pareja. Si el resultado es menor que la tabla izquierda, hay filas huérfanas.*

---

**Pregunta 4.** ¿Qué hace `df.groupby("region")["monto"].sum()`?
- A) Filtra el DataFrame por región y suma todos los montos
- B) Suma los montos de cada grupo de filas que comparten el mismo valor de `region` ✅
- C) Cuenta cuántas filas hay por región
- D) Calcula el promedio de monto para toda la tabla

*Explicación: `groupby` divide la tabla en grupos y `.sum()` aplica la suma dentro de cada grupo, produciendo un valor por región.*

---

**Pregunta 5.** Después de un `how="left"` merge, ves que `df_left["region"].isna().sum()` devuelve 3. ¿Qué significa?
- A) Hay 3 filas con montos vacíos
- B) 3 organismos tienen nombre vacío en el catálogo
- C) 3 órdenes no encontraron su organismo en el catálogo ✅
- D) La columna `region` tiene 3 valores únicos

*Explicación: `NaN` en la columna `region` tras un `left merge` indica que esa orden no encontró pareja en el catálogo — es la "huella" de la fila huérfana.*

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **merge** | Operación que une dos tablas por una columna en común | BUSCARV / VLOOKUP en Excel |
| **llave** | Columna que identifica de forma única cada registro y aparece en ambas tablas | RUT, código de organismo, número de licitación |
| **inner join** | Cruce que conserva solo las filas con pareja en ambas tablas | BUSCARV que descarta los #N/A |
| **left join** | Cruce que conserva todas las filas de la tabla izquierda | BUSCARV que deja el #N/A visible |
| **fila huérfana** | Fila cuya llave no aparece en la tabla con la que se cruza | Código de organismo que no está en el catálogo |
| **`NaN`** | Valor vacío o faltante en pandas | Celda en blanco en Excel |
| **`groupby()`** | Agrupa filas por el valor de una columna para aplicar una operación | Tabla dinámica en Excel |
| **`.sum()`** | Suma los valores de cada grupo | Función SUMA en tabla dinámica |
| **`.mean()`** | Calcula el promedio de cada grupo | Función PROMEDIO en tabla dinámica |
| **catálogo** | Tabla que traduce códigos a nombres legibles | Hoja auxiliar de referencia en Excel |
| **`entcode`** | Código numérico que identifica a cada organismo comprador en ChileCompra | RUT del organismo |
| **`.isna()`** | Devuelve True para cada celda vacía | Función `ESBLANCO()` en Excel |

---

## 9. Conexión con el siguiente módulo

Ya sabes cruzar dos tablas y resumir el resultado. Pero para que `merge` funcione bien, las llaves deben estar **limpias**: sin espacios extra, sin mezcla de mayúsculas y minúsculas, sin que un campo sea número en una tabla y texto en otra.

El próximo módulo es **R1-04 · Limpieza de datos**, donde aprenderás a:
- Detectar y corregir valores nulos (`NaN`)
- Estandarizar texto (mayúsculas, espacios, tildes)
- Convertir tipos de datos antes de un merge
- Documentar los supuestos que tomaste al limpiar

Pregunta motivadora para que llegues con ganas:

> *En los datos de ChileCompra, ¿qué pasaría si el mismo organismo aparece como `"Corp Nacional Forestal"` en algunas órdenes y como `"CONAF"` en otras? ¿Cómo detectarías ese problema antes de cruzar?*

Eso es exactamente lo que resolverás en R1-04. ¡Nos vemos ahí!

---

*Guía elaborada para el Bootcamp de Datos — Formación Pública Chile · Licencia CC BY 4.0*
