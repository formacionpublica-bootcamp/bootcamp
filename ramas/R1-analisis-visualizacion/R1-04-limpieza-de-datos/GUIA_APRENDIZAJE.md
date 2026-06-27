# Guía de Aprendizaje — R1-04 · Limpieza de datos

> **Rama:** R1 · Análisis y Visualización | **Módulo:** R1-04 | **Nivel:** Introductorio-Intermedio  
> **Duración estimada:** 3–4 horas | **Prerrequisitos:** R1-03 · Cruzar y resumir tablas  
> **Competencia de salida:** Diagnosticar los problemas de un dataset crudo, corregirlos con pandas (espacios, mayúsculas, tipos, faltantes, duplicados) y entregar los datos listos para analizar.

---

## 1. ¿Para qué me sirve esto como funcionario/a público/a?

El Estado chileno produce datos todos los días: órdenes de compra, registros de beneficiarios, informes de ejecución presupuestaria. Pero esos datos casi nunca llegan perfectos. Los sistemas heredados exportan montos como texto (`"$584.975.029.638"`), los formularios autocompletados mezclan mayúsculas (`"EQUIPAMIENTO Y SUMINISTROS MÉDICOS"` junto a `"Servicios de construcción"`), y los campos opcionales se quedan en blanco.

Si intentas analizar esos datos sin limpiarlos primero, tus conclusiones serán incorrectas — no porque hayas hecho mal el análisis, sino porque los datos de entrada estaban sucios. La limpieza no es un paso burocrático: **es el acto que define si tu análisis es confiable o no**.

En este módulo trabajarás con los **rubros más comprados por el Estado chileno en 2026** según datos reales de ChileCompra — con todos sus defectos originales incluidos.

---

## 2. Mapa conceptual del módulo

| Problema | Cómo se ve en el dato | Herramienta pandas | Equivalente en Excel |
|---|---|---|---|
| Espacios extra | `"  Medicamentos "` | `.str.strip()` | ESPACIOS() / TRIM() |
| Mayúsculas inconsistentes | `"EQUIPAMIENTO"` vs `"Tecnologías"` | `.str.capitalize()` | NOMPROPIO() |
| Monto como texto | `"$584.975.029.638"` | `.str.replace()` + `.astype(float)` | Pegar especial → valores |
| Valor faltante | Celda vacía / `NaN` | `.isna()`, `.fillna()`, `.dropna()` | ESBLANCO(), rellenar |
| Fila duplicada | Misma fila repetida exacta | `.duplicated()`, `.drop_duplicates()` | Quitar duplicados |
| Función reutilizable | Repetir los pasos cada mes | `def limpiar(df): ...` | Macro de Excel |

---

## 3. Antes de empezar: Verificación de prerrequisitos

Este módulo construye sobre R1-02 y R1-03. Marca cada punto honestamente:

- [ ] Sé cargar un CSV con `pd.read_csv()` e inspeccionarlo con `.info()`
- [ ] Entiendo qué es `NaN` y sé detectarlo con `.isna()`
- [ ] Sé filtrar filas con una condición
- [ ] Sé seleccionar una columna con `df["columna"]`
- [ ] Entiendo que una columna puede contener texto (`object`) o números (`float64`)

Si tienes dudas en alguno, repasa **R1-02 · Exploración con pandas** antes de continuar.

---

## 4. El dataset real: `compras_rubros.csv`

Este es el archivo tal como viene del portal de datos abiertos de ChileCompra — sin modificar:

```
rubro,monto
"  Medicamentos y productos farmacéuticos ","$584.975.029.638"
"Servicios de construcción y mantenimiento","$500.625.771.226"
"Servicios de construcción y mantenimiento","$500.625.771.226"
"EQUIPAMIENTO Y SUMINISTROS MÉDICOS","$432.209.437.744"
"Tecnologías de la información",
"Servicios de defensa nacional y orden","$181.577.319.021"
"Organizaciones y consultorías de administración pública","$713.645.989.343"
```

**¿Ves los problemas?** Hay 5 defectos deliberados en 7 filas:

| # | Problema | Fila afectada |
|---|---|---|
| 1 | Espacios al inicio y al final del rubro | `"  Medicamentos y productos farmacéuticos "` |
| 2 | Rubro en MAYÚSCULAS | `"EQUIPAMIENTO Y SUMINISTROS MÉDICOS"` |
| 3 | Monto como texto con `$` y `.` | Todas las filas con monto |
| 4 | Valor faltante en monto | `"Tecnologías de la información"` (monto vacío) |
| 5 | Fila duplicada exacta | `"Servicios de construcción y mantenimiento"` aparece dos veces |

Este es exactamente el tipo de export que recibirás al pedir datos a un sistema del Estado. Tu trabajo en este módulo es dejarlo limpio.

---

## 5. Guía paso a paso por sección del notebook

### Sección 1 · Diagnóstico: ¿qué tan sucio está?

**🎯 Objetivo:** Ver todos los problemas antes de tocar un solo dato.

**💡 Concepto clave:** Un médico no opera sin diagnóstico. Tú no limpias sin antes mapear los problemas. El diagnóstico tiene tres pasos: tipos de dato (`.dtypes`), faltantes (`.isna().sum()`), duplicados (`.duplicated().sum()`).

**🔍 Qué hace el código:**
```python
print(df.dtypes)          # ¿Qué tipo cree pandas que es cada columna?
print(df.isna().sum())    # ¿Cuántos NaN hay por columna?
print(df.duplicated().sum())  # ¿Cuántas filas son copia exacta de otra?
```

**Resultado esperado con el dataset real:**
```
dtypes:  rubro → object, monto → object   ← ¡monto debería ser número!
isna:    monto → 1                         ← 1 fila sin monto
duplicated: 1                              ← 1 fila duplicada
```

**⚠️ Error frecuente:** Saltar el diagnóstico y limpiar "de memoria". Siempre diagnostica primero — puede haber problemas que no viste.

**✅ Sabes esta sección cuando puedes:** Decir exactamente cuántos NaN y cuántos duplicados tiene el dataset antes de limpiarlo.

---

### Sección 2 · Limpiar texto: espacios y mayúsculas

**🎯 Objetivo:** Estandarizar la columna `rubro` para que los valores sean comparables.

**💡 Concepto clave:** `"  Medicamentos "` y `"Medicamentos"` son dos strings distintos para pandas — aunque para ti se ven igual. Si intentas hacer un `groupby` con esa diferencia, obtendrás grupos separados para lo que debería ser un solo rubro. El texto limpio es la base de cualquier agrupación confiable.

**🔍 Qué hace el código:**
```python
df["rubro"] = df["rubro"].str.strip()       # Elimina espacios al inicio y al final
df["rubro"] = df["rubro"].str.capitalize()  # Primera letra mayúscula, resto minúsculas
```

- `.str.strip()` → como la función `ESPACIOS()` de Excel, pero aplicada a toda la columna de una vez
- `.str.capitalize()` → primera letra mayúscula, todo lo demás minúsculas

**Antes y después:**

| Antes | Después |
|---|---|
| `"  Medicamentos y productos farmacéuticos "` | `"Medicamentos y productos farmacéuticos"` |
| `"EQUIPAMIENTO Y SUMINISTROS MÉDICOS"` | `"Equipamiento y suministros médicos"` |

**⚠️ Error frecuente:** Usar `.str.title()` en lugar de `.str.capitalize()`. `.title()` pone mayúscula en cada palabra (`"Equipamiento Y Suministros Médicos"`), lo que puede crear inconsistencias con siglas y preposiciones.

**✅ Sabes esta sección cuando puedes:** Verificar que `df["rubro"].str.startswith(" ").any()` devuelve `False` tras la limpieza.

---

### Sección 3 · Convertir monto: de texto a número

**🎯 Objetivo:** Transformar `"$584.975.029.638"` en el número `584975029638.0` para poder sumarlo.

**💡 Concepto clave:** Cuando pandas lee `"$584.975.029.638"` ve un texto, no un número. No puedes calcular un promedio ni ordenar de mayor a menor con texto. La conversión es siempre la misma receta: quita los caracteres que no son dígitos, luego convierte el tipo.

**🔍 Qué hace el código:**
```python
df["monto"] = (
    df["monto"]
    .str.replace("$", "", regex=False)   # Quita el signo pesos
    .str.replace(".", "", regex=False)   # Quita los separadores de miles
    .astype(float)                        # Convierte a número decimal
)
```

- `.str.replace("$", "")` → elimina el carácter `$`
- `.str.replace(".", "")` → elimina los puntos de miles (ojo: en Chile el punto separa miles, no decimales)
- `.astype(float)` → convierte la columna al tipo numérico

> **Nota importante:** La fila de `"Tecnologías de la información"` tiene `NaN` en monto. `.astype(float)` acepta `NaN` y lo conserva — no falla.

**⚠️ Error frecuente:** Confundir el punto de miles con el punto decimal. En Chile: `$1.500.000` = 1,5 millones. Si el separador decimal fuera una coma (`$1.500.000,50`), habría que quitar también la coma y reemplazarla por un punto antes de convertir.

**✅ Sabes esta sección cuando puedes:** Ejecutar `df["monto"].dtype` y ver `float64`.

---

### Sección 4 · Resolver faltantes y duplicados

**🎯 Objetivo:** Tomar una decisión explícita sobre qué hacer con el NaN y la fila duplicada.

**💡 Concepto clave:** No existe una sola respuesta correcta. Eliminar la fila con faltante (`dropna`) o rellenar con un valor (`fillna`) son dos supuestos distintos sobre el dato. Lo importante es **documentar qué elegiste y por qué** — eso es lo que distingue un análisis riguroso de uno descuidado.

**🔍 Qué hace el código:**
```python
# Opción A: eliminar la fila con faltante
df_limpio = df.dropna(subset=["monto"])

# Opción B: rellenar con 0 (si queremos conservar el rubro en el conteo)
df_limpio = df.fillna({"monto": 0})

# Eliminar duplicados exactos
df_limpio = df_limpio.drop_duplicates()
```

**Para el ejercicio del módulo se usa `dropna`** porque no tenemos información de cuánto gastó el Estado en Tecnologías de la información ese período, y poner 0 sería engañoso.

**Antes y después (resumen):**

| Paso | Filas |
|---|---|
| Dataset original | 7 |
| Tras `dropna` (quita el NaN) | 6 |
| Tras `drop_duplicates` (quita el duplicado) | 5 |

**⚠️ Error frecuente:** Aplicar `drop_duplicates` antes de limpiar el texto. Si el rubro tiene espacios o mayúsculas distintas, dos filas que deberían ser duplicados no se detectarán como tal.

**✅ Sabes esta sección cuando puedes:** Explicar por qué elegiste `dropna` o `fillna` y qué supuesto implica cada uno.

---

### Sección 5 · Empaquetar: la función de limpieza

**🎯 Objetivo:** Convertir todos los pasos anteriores en una función reutilizable.

**💡 Concepto clave:** Si el próximo mes recibes un nuevo export de ChileCompra, ¿vas a repetir cada paso manualmente? Una función es como una macro de Excel — ejecutas un nombre y los pasos ocurren solos.

**🔍 Qué hace el código:**
```python
def limpiar_compras(df):
    df = df.copy()                                        # No modificar el original
    df["rubro"] = df["rubro"].str.strip().str.capitalize()
    df["monto"] = (df["monto"]
                   .str.replace("$", "", regex=False)
                   .str.replace(".", "", regex=False)
                   .astype(float))
    df = df.dropna(subset=["monto"])
    df = df.drop_duplicates()
    return df

df_limpio = limpiar_compras(df_raw)
```

- `df.copy()` → hace una copia del DataFrame original para no modificarlo
- La función recibe el DataFrame crudo y devuelve el DataFrame limpio
- Puedes reutilizarla en cualquier notebook futuro con `from limpieza import limpiar_compras`

**⚠️ Error frecuente:** No usar `df.copy()` dentro de la función. Si no copias, pandas modifica el DataFrame original y puedes perder los datos crudos.

**✅ Sabes esta sección cuando puedes:** Llamar `limpiar_compras(df_raw)` y obtener un DataFrame con 5 filas, columna `monto` tipo `float64`, sin NaN ni duplicados.

---

## 6. Guía de los 5 Ejercicios

### Ejercicio 01 · Diagnóstico completo

**Habilidad que entrena:** Leer el estado de un dataset antes de tocarlo.

**Pista suave 🟢:** Carga el CSV e inspecciónalo con tres operaciones: `.dtypes`, `.isna().sum()` y `.duplicated().sum()`.

**Pista media 🟡:** Para el tipo de `monto`, espera ver `object` (texto), no `float64`. Eso confirma que necesita conversión.

**Pista directa 🔴:** `n_nulos = df["monto"].isna().sum()` → debe ser `1`. `n_duplicados = df.duplicated().sum()` → debe ser `1`. `tipo_monto = df["monto"].dtype` → debe ser `object`.

**Lógica de la solución:** El dataset tiene 7 filas, 1 NaN en monto, 1 duplicado exacto, y monto leído como texto. Ese es el diagnóstico completo.

**✅ El chequeo automático valida que:** `n_nulos == 1`, `n_duplicados == 1`, `str(tipo_monto) == "object"`.

---

### Ejercicio 02 · Limpiar la columna rubro

**Habilidad que entrena:** Estandarizar texto con `.str.strip()` y `.str.capitalize()`.

**Pista suave 🟢:** Aplica dos transformaciones encadenadas sobre `df["rubro"]` y guarda el resultado en la misma columna.

**Pista media 🟡:** El orden importa: primero `.strip()` (quita espacios), luego `.capitalize()` (estandariza mayúsculas). Encadénalos: `.str.strip().str.capitalize()`.

**Pista directa 🔴:** `df["rubro"] = df["rubro"].str.strip().str.capitalize()`. Luego verifica con `df["rubro"].str.startswith(" ").any()` → debe ser `False`.

**Lógica de la solución:** Tras la limpieza, `"  Medicamentos..."` pierde sus espacios y `"EQUIPAMIENTO..."` queda como `"Equipamiento y suministros médicos"`.

**✅ El chequeo automático valida que:** Ningún rubro empieza con espacio y ninguno está en mayúsculas completas.

---

### Ejercicio 03 · Convertir monto a número

**Habilidad que entrena:** Limpiar un campo monetario y convertir tipo de dato.

**Pista suave 🟢:** Necesitas quitar dos caracteres del texto (`$` y `.`) y luego convertir la columna a número decimal.

**Pista media 🟡:** Usa `.str.replace()` dos veces (una por carácter) y luego `.astype(float)`. Encadénalos con paréntesis.

**Pista directa 🔴:**
```python
df["monto"] = (df["monto"]
    .str.replace("$", "", regex=False)
    .str.replace(".", "", regex=False)
    .astype(float))
```

**Lógica de la solución:** `"$584.975.029.638"` → quita `$` → `"584.975.029.638"` → quita `.` → `"584975029638"` → `astype(float)` → `584975029638.0`.

**✅ El chequeo automático valida que:** `df["monto"].dtype == float64` y el mayor valor es `713645989343.0`.

---

### Ejercicio 04 · Resolver faltantes y duplicados

**Habilidad que entrena:** Eliminar filas problemáticas de forma explícita y documentar la decisión.

**Pista suave 🟢:** Hay dos problemas separados: una fila con `NaN` en monto y una fila duplicada exacta. Resuélvelos en dos pasos.

**Pista media 🟡:** Para el NaN: `dropna(subset=["monto"])`. Para el duplicado: `drop_duplicates()`. El orden correcto: primero `dropna`, luego `drop_duplicates`.

**Pista directa 🔴:**
```python
df_limpio = df.dropna(subset=["monto"])
df_limpio = df_limpio.drop_duplicates()
```

**Lógica de la solución:** `dropna` elimina la fila de Tecnologías de la información (7→6 filas). `drop_duplicates` elimina la copia de Servicios de construcción (6→5 filas).

**✅ El chequeo automático valida que:** `len(df_limpio) == 5` y `df_limpio["monto"].isna().sum() == 0`.

---

### Ejercicio 05 · La función de limpieza

**Habilidad que entrena:** Encapsular todos los pasos en una función reutilizable.

**Pista suave 🟢:** Una función recibe un DataFrame como argumento y devuelve un DataFrame limpio. Todos los pasos anteriores van dentro.

**Pista media 🟡:** Recuerda hacer `df = df.copy()` al inicio de la función para no modificar el original. La función debe terminar con `return df`.

**Pista directa 🔴:**
```python
def limpiar_compras(df):
    df = df.copy()
    df["rubro"] = df["rubro"].str.strip().str.capitalize()
    df["monto"] = (df["monto"]
                   .str.replace("$", "", regex=False)
                   .str.replace(".", "", regex=False)
                   .astype(float))
    df = df.dropna(subset=["monto"])
    df = df.drop_duplicates()
    return df
```

**Lógica de la solución:** La función reproduce los 4 pasos anteriores en orden. Al llamarla con `df_raw` devuelve un DataFrame limpio de 5 filas sin modificar el original.

**✅ El chequeo automático valida que:** `limpiar_compras(df_raw)` devuelve un DataFrame con 5 filas, `monto` de tipo `float64` y sin NaN.

---

## 7. Sección especial: Los datos del Estado y el principio de transparencia

### El dataset limpio y sus números reales

Una vez limpios, los datos del módulo revelan el gasto real del Estado chileno en los principales rubros de compras públicas 2026:

| Rubro (limpio) | Monto ($) |
|---|---|
| Organizaciones y consultorías de administración pública | $713.645.989.343 |
| Medicamentos y productos farmacéuticos | $584.975.029.638 |
| Servicios de construcción y mantenimiento | $500.625.771.226 |
| Equipamiento y suministros médicos | $432.209.437.744 |
| Servicios de defensa nacional y orden | $181.577.319.021 |

### La decisión que tomaste (y sus implicancias)

Elegiste usar `dropna` para eliminar la fila de **Tecnologías de la información**, que no tenía monto. Eso significa que el ranking anterior es **incompleto**: falta uno de los rubros más relevantes del Estado moderno.

Esto no es un error técnico — es un supuesto que debes declarar explícitamente si presentas este análisis:

> *"El análisis cubre 5 de los 6 rubros originales. El rubro 'Tecnologías de la información' fue excluido por no disponer de datos de monto en el período analizado."*

### Reflexión

> *Si tuvieras que presentar este ranking a tu jefatura, ¿incluirías o excluirías el rubro sin monto? ¿Qué le dirías sobre ese dato faltante?*

Respuesta posible: Lo incluirías con monto `0` y una nota de "sin dato", porque excluirlo sin mencionarlo podría crear una imagen incompleta del gasto público en tecnología.

---

## 8. Conexión con el módulo `profundiza.ipynb`

| Aspecto | `leccion.ipynb` (este módulo) | `profundiza.ipynb` (opcional) |
|---|---|---|
| **Enfoque** | Cómo limpiar paso a paso | Por qué cada decisión importa |
| **NaN** | `dropna` o `fillna` como herramienta | MCAR / MAR / MNAR: tipos de dato faltante y su sesgo |
| **Normalización** | `.strip()` y `.capitalize()` | Trampas con siglas y categorías que se fusionan |
| **Función** | Empaquetar los pasos | Reproducibilidad y linaje del dato |
| **¿Para quién?** | Todo participante | Quienes necesiten justificar decisiones ante auditores o pares |

**Guía de decisión:** Si en tu trabajo debes explicar metodología a otros (informes técnicos, auditorías, publicaciones), el `profundiza.ipynb` te da el lenguaje para hacerlo. Si solo necesitas limpiar y seguir, `leccion.ipynb` es suficiente.

---

## 9. Autoevaluación Final

**Pregunta 1.** Ejecutas `df.dtypes` y ves que la columna `monto` es `object`. ¿Qué significa?
- A) Que la columna tiene objetos Python especiales
- B) Que pandas la leyó como texto, no como número ✅
- C) Que la columna está vacía
- D) Que el tipo es correcto para montos monetarios

*Explicación: `object` es el tipo de dato de texto en pandas. Si una columna de montos aparece como `object`, pandas no pudo interpretarla como número — generalmente porque tiene caracteres como `$`, `.` o comas.*

---

**Pregunta 2.** ¿Cuál es la diferencia entre `.dropna()` y `.fillna(0)`?
- A) `.dropna()` es más rápido; `.fillna(0)` es más preciso
- B) `.dropna()` elimina las filas con NaN; `.fillna(0)` las conserva reemplazando NaN por 0 ✅
- C) `.dropna()` rellena con 0; `.fillna(0)` elimina la fila
- D) Son equivalentes

*Explicación: Ambas resuelven el NaN, pero con supuestos distintos. `dropna` asume que la fila no tiene datos útiles; `fillna(0)` asume que el valor real es cero.*

---

**Pregunta 3.** Tienes `"  Servicios de salud  "` en una celda. ¿Qué devuelve `.str.strip()`?
- A) `"servicios de salud"`
- B) `"Servicios De Salud"`
- C) `"Servicios de salud"` ✅ — en realidad devuelve `"Servicios de salud"` (sin espacios, sin cambio de mayúsculas)
- D) `"  Servicios de salud  "` (sin cambio)

*Explicación: `.str.strip()` solo elimina espacios al inicio y al final. No cambia mayúsculas ni minúsculas — para eso necesitas `.str.capitalize()` o `.str.lower()`.*

---

**Pregunta 4.** ¿Por qué es importante hacer `df.copy()` al inicio de una función de limpieza?
- A) Para hacer el código más rápido
- B) Para evitar que la función modifique el DataFrame original ✅
- C) Porque pandas exige una copia antes de cualquier operación
- D) Para poder usar `.str` en la columna

*Explicación: Sin `df.copy()`, pandas puede modificar el objeto original por referencia. Si después quieres comparar el dataset crudo con el limpio, habrás perdido el original.*

---

**Pregunta 5.** Tienes 7 filas. Aplicas `dropna` y quedan 6. Luego `drop_duplicates` y quedan 5. ¿Qué ocurrió?
- A) Se eliminaron 2 filas vacías y 1 duplicado
- B) Se eliminó 1 fila con NaN y 1 fila duplicada exacta ✅
- C) Se eliminaron 2 duplicados
- D) El orden de las operaciones fue incorrecto

*Explicación: `dropna` eliminó la 1 fila con NaN (7→6). `drop_duplicates` eliminó la 1 fila que era copia exacta de otra (6→5). Cada operación actúa sobre un problema distinto.*

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **limpieza de datos** | Proceso de detectar y corregir errores en un dataset | Revisar y corregir una planilla antes de entregar el informe |
| **`NaN`** | Not a Number — valor faltante o vacío en pandas | Celda en blanco en Excel |
| **`.isna()`** | Devuelve `True` en cada celda que está vacía | `ESBLANCO()` en Excel |
| **`.dropna()`** | Elimina las filas que tienen al menos un NaN | Borrar filas con celdas en blanco |
| **`.fillna(valor)`** | Reemplaza los NaN con el valor especificado | Reemplazar blancos con 0 o con "Sin dato" |
| **`.str.strip()`** | Elimina espacios al inicio y al final de un texto | `ESPACIOS()` / `TRIM()` en Excel |
| **`.str.capitalize()`** | Primera letra mayúscula, resto minúsculas | `NOMPROPIO()` parcial — solo primera palabra |
| **`.str.replace()`** | Reemplaza un texto dentro de una cadena | Buscar y reemplazar (Ctrl+H) en Excel |
| **`.astype(float)`** | Convierte una columna al tipo número decimal | "Pegar como valores" + dar formato número en Excel |
| **`.duplicated()`** | Identifica filas que son copia exacta de otra anterior | "Resaltar duplicados" en Excel |
| **`.drop_duplicates()`** | Elimina las filas duplicadas, conserva la primera | "Quitar duplicados" en Excel |
| **función de limpieza** | Función reutilizable que encapsula todos los pasos | Macro de Excel que repite los mismos pasos |

---

## 11. Conexión con el siguiente módulo

Ya sabes limpiar un dataset: estandarizar texto, convertir tipos, resolver faltantes y duplicados. A partir de ahora, cada dataset que recibas pasará primero por este proceso antes de cualquier análisis.

El próximo módulo es **R1-05 · SQL para análisis**, donde aprenderás a:
- Consultar bases de datos relacionales directamente desde pandas
- Escribir `SELECT`, `WHERE`, `GROUP BY` y `JOIN` en SQL
- Conectar Python con una base de datos SQLite real
- Decidir cuándo usar SQL y cuándo usar pandas

Pregunta motivadora:

> *Los datos de ChileCompra tienen millones de filas — demasiadas para cargar en un DataFrame sin filtrar antes. ¿Cómo pedirías al servidor solo las filas que necesitas, sin descargar todo el archivo?*

Eso es exactamente lo que resuelve SQL. ¡Nos vemos en R1-05!

---

*Guía elaborada para el Bootcamp de Datos — Formación Pública Chile · Licencia CC BY 4.0*
