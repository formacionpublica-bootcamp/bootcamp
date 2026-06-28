# Guía de Aprendizaje — R1-09 · Dashboards ligeros con Gradio

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 9 de 10 · Semana 10

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-09 · Dashboards ligeros con Gradio |
| **Pista** | R1 — Análisis y Visualización |
| **Duración estimada** | 90–120 minutos |
| **Nivel** | Intermedio-avanzado |
| **Prerrequisitos** | R1-03 (groupby), R1-07 (gráficos), R1-08 (comunicar) |
| **Competencia de salida** | Publicar un tablero interactivo simple sobre datos públicos, sin instalar nada |
| **Dataset** | Compras públicas de alimentos por categoría y región — ChileCompra (`compras_ml.csv`) |
| **Entregable** | 4 celdas de chequeo con ✅ + tablero Gradio funcionando |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Hasta aquí aprendiste a **analizar datos y hacer gráficos**. Pero esos gráficos los hacemos nosotros, corremos el código, y entregamos una imagen estática. ¿Qué pasa cuando un directivo quiere explorar los datos por su cuenta, sin pedirte un nuevo gráfico cada vez que cambia de pregunta?

Ahí entra el **dashboard interactivo**: una interfaz donde la persona elige filtros (región, categoría, período) y ve los resultados actualizarse automáticamente. No necesitan saber Python; tú construyes la herramienta, ellos la usan.

**Gradio** es la biblioteca que lo hace posible directamente desde Google Colab, sin servidores ni infraestructura adicional. Es la opción más rápida para un prototipo funcional en el sector público.

### Conexión con el dataset

Los datos de ChileCompra incluyen columnas `categoria`, `region_comprador` y `monto_total`. Con ellos construirás un tablero que responde: ¿cuánto gastó el Estado en esta categoría, en esta región?

---

## 3. Mapa Conceptual del Módulo

| Concepto técnico | ¿Qué hace? | Analogía sector público |
|-----------------|-----------|------------------------|
| Función `filtrar(df, cat, reg)` | Reduce el DataFrame según los filtros elegidos | El filtro de una tabla Excel con criterios múltiples |
| Función `kpis(d)` | Calcula indicadores clave del subconjunto filtrado | Los KPIs del tablero de control de un JEFE DAEM |
| `groupby + sum + sort_values` | Agrega y ordena para la tabla resumen | El subtotal por categoría en un informe de gasto |
| Función `figura_top_categorias(d)` | Devuelve una figura matplotlib reutilizable | Un gráfico que se actualiza al cambiar el período en un informe dinámico |
| `gr.Interface(...)` | Ensambla filtros + salidas en una interfaz web | El formulario de consulta de un sistema de información DIPRES |
| `demo.launch(share=True)` | Publica el tablero en una URL pública temporal | Compartir un dashboard por enlace a un equipo de trabajo |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / Revisar |
|-----------|-------------|
| Usar `groupby` + `sum` para agrupar un DataFrame | Del módulo R1-03 |
| Crear un gráfico de barras horizontal con matplotlib | Del módulo R1-07 |
| Escribir una función en Python que recibe y retorna un valor | Prework Python básico |
| Filtrar filas de un DataFrame con condiciones booleanas | Del módulo R1-02 y R1-04 |
| Cargar un CSV con pandas | Del módulo R1-02 |

Si alguna respuesta es "revisar", dedica 10 minutos a repasar el módulo indicado antes de continuar. Este módulo es el que más integra todo lo anterior.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección de Preparación: Cargar los datos

🎯 **Objetivo:** dejar el DataFrame `df` listo con los datos de compras públicas.

💡 **Concepto clave:** el dataset tiene columnas `categoria`, `region_comprador` y `monto_total`. Las categorías son tipos de productos (pan, lácteos, etc.), las regiones son las 16 regiones de Chile. Cada fila es una orden de compra.

🔍 **¿Qué hace el código?** Carga el CSV local o lo descarga del repositorio si no existe. Imprime las dimensiones (`shape`) para confirmar que la carga fue correcta.

⚠️ **Error frecuente:** si corres el notebook fuera de Colab y el archivo no existe en la ruta relativa, la descarga del repo puede fallar si no hay internet. Asegúrate de tener `compras_ml.csv` en la misma carpeta que el notebook.

✅ **Sabes esta sección cuando puedes:** ejecutar la celda y leer las dimensiones del DataFrame sin errores.

---

### Sección 1: Filtrar es la base de todo tablero

🎯 **Objetivo:** escribir la función central del tablero: filtrar datos por categoría y/o región.

💡 **Concepto clave — El tablero como filtro inteligente:** todo dashboard, en el fondo, hace una cosa: **filtrar** el conjunto de datos según lo que el usuario eligió, y mostrar el resultado. Si el usuario no eligió nada (`"(todas)"`), se muestran todos los datos. Si eligió una región, se muestran solo las órdenes de esa región.

🔍 **¿Qué hace el código?**
- La función recibe `df`, `categoria` y `region`
- Comienza con `d = df.copy()` para no modificar el original
- El TODO pide que apliques dos filtros condicionales: uno para categoría y otro para región
- La condición para cada filtro es: «si el argumento NO es `"(todas)"`, filtra por ese valor»

⚠️ **Error frecuente:** usar `==` en vez de comparar con `"(todas)"`. Si escribes `if categoria:` en vez de `if categoria != "(todas)":`, el filtro se aplica aunque el usuario haya elegido "todas".

✅ **Sabes esta sección cuando puedes:** ejecutar `filtrar(df, categoria="Productos de panadería")` y obtener solo filas de esa categoría.

---

### Sección 2: Los KPIs — los números grandes del tablero

🎯 **Objetivo:** calcular los 3 indicadores principales que mostrará el tablero.

💡 **Concepto clave — KPI (Key Performance Indicator):** en un dashboard, los KPIs son los números grandes que aparecen primero. Dan el contexto de "cuánto". En este tablero: gasto total (suma del monto), número de órdenes (filas) y ticket promedio (media del monto).

🔍 **¿Qué hace el código?**
- La función recibe un DataFrame ya filtrado `d`
- Devuelve un diccionario con tres claves: `gasto_total`, `n_ordenes`, `ticket_promedio`
- Cada TODO corresponde a una operación simple de pandas:
  - `gasto_total`: `d["monto_total"].sum()`
  - `n_ordenes`: `len(d)` o `d.shape[0]`
  - `ticket_promedio`: `d["monto_total"].mean()`

⚠️ **Error frecuente:** devolver un DataFrame en vez de un diccionario, o calcular `mean()` sobre todo el DataFrame en vez de sobre la columna `monto_total`.

✅ **Sabes esta sección cuando puedes:** llamar `kpis(filtrar(df))` y ver tres números con sentido económico.

---

### Sección 3: Una tabla resumen — gasto por región

🎯 **Objetivo:** construir la función que agrupa el gasto por región, ordenado de mayor a menor.

💡 **Concepto clave:** este es el patrón `groupby + sum + sort_values` que ya practicaste en R1-03 y R1-06. La diferencia es que ahora lo encapsulas en una función para reutilizarlo dentro del tablero.

🔍 **¿Qué hace el código?**
- Agrupa `d` por `"region_comprador"`, suma `"monto_total"`
- Ordena de mayor a menor con `sort_values(ascending=False)`
- La celda de chequeo verifica que los valores estén en orden descendente y que haya tantas filas como regiones únicas

Además, hay una celda de ilustración que genera un gráfico de barras horizontal (`.barh`) con el top 10. Así te haces una idea de cómo se verá en el tablero.

⚠️ **Error frecuente:** usar `sort_values(ascending=True)` y que los valores queden al revés. La celda de chequeo falla en ese caso.

✅ **Sabes esta sección cuando puedes:** llamar `gasto_por_region(df).head(3)` y ver las 3 regiones con mayor gasto, de mayor a menor.

---

### Sección 4: Un gráfico como componente del tablero

🎯 **Objetivo:** escribir una función que devuelve una figura matplotlib, lista para ser usada por Gradio.

💡 **Concepto clave — Funciones que devuelven figuras:** Gradio espera que le entregues objetos `Figure` de matplotlib, no que llames a `plt.show()`. La diferencia es crucial: en vez de mostrar el gráfico en pantalla, lo devuelves como valor de retorno para que Gradio lo ponga en la interfaz.

🔍 **¿Qué hace el código?**
- La función recibe `d` (DataFrame filtrado) y `n` (cuántas categorías mostrar, por defecto 8)
- Calcula el top `n` de categorías por gasto con `groupby + sum + sort_values + tail`
- Crea `fig, ax = plt.subplots(...)` y el TODO pide que dibujes el gráfico de barras horizontal y devuelvas `fig`
- El `return fig` al final es obligatorio para que Gradio pueda mostrarlo

⚠️ **Error frecuente:** poner `plt.show()` dentro de la función y olvidar el `return fig`. Gradio no puede capturar lo que se "muestra" con `plt.show()`; necesita el objeto `fig` directamente.

✅ **Sabes esta sección cuando puedes:** ejecutar `print(type(figura_top_categorias(df)).__name__)` y ver `Figure` en la salida.

---

### Sección 5: Arma el tablero (Gradio)

🎯 **Objetivo:** entender cómo Gradio ensambla los componentes en una interfaz web.

💡 **Concepto clave — Gradio como pegamento:** Gradio toma tus funciones de Python y las convierte en una interfaz web con campos de entrada (dropdowns, sliders) y áreas de salida (texto, gráficos). No necesitas saber HTML ni JavaScript.

🔍 **¿Qué hace el código?**
- La función `tablero(categoria, region)` llama a `filtrar`, `kpis` y `figura_top_categorias` en secuencia
- `gr.Interface(tablero, inputs=[...], outputs=[...])` conecta la función con la interfaz
- Los inputs son dos `gr.Dropdown` con las listas de categorías y regiones
- Los outputs son un `gr.Text` para el resumen y un `gr.Plot` para el gráfico
- `demo.launch(share=True)` publica un link temporal público (funciona en Colab)

Esta sección no tiene celda de chequeo con `assert`. La prueba es visual: el tablero se lanza y funciona.

⚠️ **Error frecuente:** intentar ejecutar la celda de Gradio sin tener Gradio instalado. Si ves `ModuleNotFoundError`, ejecuta primero `!pip -q install gradio` en una nueva celda.

✅ **Sabes esta sección cuando puedes:** lanzar el tablero, cambiar el filtro de región, y ver que el gráfico y los KPIs cambian automáticamente.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Escribe la función `filtrar`

**Habilidad que entrena:** aplicar filtros condicionales sobre un DataFrame sin modificar el original.

**Pistas progresivas:**
- 🟡 *Pista suave:* la función ya tiene la estructura. Solo necesitas agregar dos bloques `if` dentro, uno para `categoria` y otro para `region`.
- 🟠 *Pista media:* el patrón es: `if categoria != "(todas)": d = d[d["categoria"] == categoria]`. Repite lo mismo para `region`.
- 🔴 *Pista directa:*
```python
if categoria != "(todas)":
    d = d[d["categoria"] == categoria]
if region != "(todas)":
    d = d[d["region_comprador"] == region]
```

**Lógica de la solución:** la celda de chequeo verifica dos cosas: que `filtrar(df)` sin argumentos devuelve el mismo número de filas que `df`, y que `filtrar(df, categoria="Productos de panadería")` devuelve solo filas de esa categoría.

---

### Ejercicio 2 — Escribe la función `kpis`

**Habilidad que entrena:** calcular métricas de resumen sobre un subconjunto de datos.

**Pistas progresivas:**
- 🟡 *Pista suave:* ¿cómo calculas la suma de una columna? ¿Y el número de filas?
- 🟠 *Pista media:* `d["monto_total"].sum()`, `len(d)` y `d["monto_total"].mean()` son las tres operaciones que necesitas.
- 🔴 *Pista directa:*
```python
return {
    "gasto_total": d["monto_total"].sum(),
    "n_ordenes": len(d),
    "ticket_promedio": d["monto_total"].mean(),
}
```

**Lógica de la solución:** la celda verifica que `n_ordenes == len(df)` (sin filtro), que `gasto_total > 0` y que `ticket_promedio` es igual a la media de la columna completa.

---

### Ejercicio 3 — Escribe `gasto_por_region`

**Habilidad que entrena:** agrupar, agregar y ordenar datos como insumo para una visualización.

**Pistas progresivas:**
- 🟡 *Pista suave:* ¿cuál es el patrón que usaste en R1-03 para sumar por grupo? Es el mismo aquí.
- 🟠 *Pista media:* `df.groupby("region_comprador")["monto_total"].sum()` — a eso agregás el `.sort_values(ascending=False)`.
- 🔴 *Pista directa:* `return d.groupby("region_comprador")["monto_total"].sum().sort_values(ascending=False)`

**Lógica de la solución:** la celda verifica que la lista de valores esté ordenada de mayor a menor y que el número de filas sea igual al número de regiones únicas (`nunique()`).

---

### Ejercicio 4 — Escribe `figura_top_categorias`

**Habilidad que entrena:** encapsular una visualización en una función que devuelve un objeto Figure.

**Pistas progresivas:**
- 🟡 *Pista suave:* ¿qué tipo de gráfico es más fácil de leer para muchas categorías largas?
- 🟠 *Pista media:* usa `ax.barh(top.index, top.values)` para un gráfico de barras horizontal. Recuerda terminar con `return fig`.
- 🔴 *Pista directa:*
```python
ax.barh(top.index, top.values)
plt.tight_layout()
return fig
```

**Lógica de la solución:** la celda verifica que el resultado de la función sea una instancia de `Figure` y que tenga al menos un eje (`len(fig.axes) >= 1`). El `return fig` es la clave; sin él la función devuelve `None` y el chequeo falla.

---

## 7. El Tablero en Profundidad: ¿Cuándo un Dashboard Aporta?

El cierre del notebook plantea una pregunta crítica: **¿cuándo un dashboard realmente vale la pena?** Construir un tablero toma tiempo. A veces un gráfico estático o un informe es suficiente.

### ¿Cuándo SÍ un dashboard?

- Alguien necesita **filtrar y explorar de forma recurrente** (cada semana, cada mes)
- Hay **múltiples usuarios** con preguntas distintas sobre el mismo dataset
- La respuesta cambia con el tiempo y se necesita **actualización automática**
- El usuario final **no sabe Python** pero necesita acceso directo a los datos

### ¿Cuándo NO un dashboard?

- La pregunta se responde **una sola vez** (un gráfico o informe es suficiente)
- Los datos son estáticos y no cambian
- El resultado requiere **interpretación experta** que un filtro no puede dar
- El costo de mantener el tablero supera el valor que aporta

### Reflexión para tu servicio

> Piensa en un proceso de tu trabajo donde hoy generas informes manualmente cada cierto tiempo. ¿Cuánto tiempo podrías ahorrar con un tablero que cualquier persona del equipo pueda consultar directamente? ¿Qué datos necesitarías?

---

## 8. Conexión con el Notebook `profundiza.ipynb`

| Aspecto | `leccion.ipynb` (nivel práctico) | `profundiza.ipynb` (nivel teórico) |
|---------|----------------------------------|-------------------------------------|
| Interfaz | `gr.Interface` (simple, una función) | `gr.Blocks` (más control, diseño avanzado) |
| Outputs | Texto + gráfico | Tablas, múltiples gráficos, KPIs en tarjetas |
| Deploy | `demo.launch(share=True)` en Colab | Hugging Face Spaces (publicación permanente) |
| Mantenimiento | Prototipo descartable | Tablero productivo con control de versiones |
| Tiempo estimado | 90–120 min | 60–90 min adicionales |

**¿Cuándo ir al profundiza?** Cuando ya tienes el tablero básico funcionando y quieres publicarlo de forma permanente, o cuando necesitas más de un gráfico en la misma pantalla.

---

## 9. Autoevaluación Final

**1. ¿Por qué la función `filtrar` comienza con `d = df.copy()`?**

- a) Para hacer el código más lento y seguro
- b) Para no modificar el DataFrame original al aplicar filtros ✅
- c) Porque Gradio requiere copias de todos los DataFrames
- d) Para convertir el DataFrame a formato CSV

*Explicación:* en Python, los DataFrames se pasan por referencia. Si filtras `df` directamente dentro de la función, modificarías el DataFrame original y los siguientes llamados a `filtrar` no tendrían todos los datos. `.copy()` crea una copia independiente.

---

**2. ¿Qué diferencia hay entre `plt.show()` y `return fig` dentro de una función que usa Gradio?**

- a) No hay diferencia; Gradio acepta ambas formas
- b) `plt.show()` es más rápido
- c) `return fig` devuelve el objeto Figure que Gradio puede mostrar; `plt.show()` lo renderiza en pantalla y Gradio no puede capturarlo ✅
- d) `return fig` solo funciona en Jupyter, no en Colab

*Explicación:* Gradio recibe el valor de retorno de la función y lo muestra en el output. Si usas `plt.show()`, el gráfico se imprime en la celda de Colab pero Gradio recibe `None` y el panel de gráfico queda en blanco.

---

**3. ¿Qué hace `demo.launch(share=True)` en Colab?**

- a) Sube el notebook a GitHub
- b) Instala Gradio en el entorno
- c) Publica el tablero en una URL temporal pública accesible desde cualquier navegador ✅
- d) Guarda el tablero como archivo HTML

*Explicación:* `share=True` crea un túnel hacia el servidor de Gradio y genera una URL pública temporal (válida por 72 horas). Es la forma más rápida de compartir un prototipo sin infra adicional.

---

**4. Ejecutas `filtrar(df, categoria="X")` y obtienes 0 filas, pero sabes que la categoría existe. ¿Cuál es la causa más probable?**

- a) El DataFrame está vacío
- b) La categoría "X" tiene mayúsculas o espacios distintos a los del dataset ✅
- c) La función `filtrar` tiene un bug en la condición `if`
- d) Pandas no soporta filtros de texto

*Explicación:* el filtro `d["categoria"] == "X"` es sensible a mayúsculas, minúsculas y espacios. Si el dato real es `" x"` o `"x"`, la comparación falla. Usa `df["categoria"].unique()` para ver los valores exactos antes de filtrar.

---

**5. ¿Cuál de estos escenarios justifica mejor construir un dashboard interactivo en tu servicio?**

- a) Necesitas un gráfico de barras para una presentación que se hace una vez al año
- b) Quieres explorar un dataset nuevo por primera vez
- c) El jefe de servicio revisa semanalmente el gasto por programa y siempre pide distintos cortes (por región, por mes, por proveedor) ✅
- d) Tienes que limpiar un CSV con valores nulos

*Explicación:* el dashboard se justifica cuando hay consultas recurrentes, múltiples cortes posibles y un usuario no técnico que necesita acceso directo. Para consultas únicas o limpieza de datos, un script o notebook es más eficiente.

---

## 10. Glosario del Módulo

| Término | Definición simple | Equivalente en sector público |
|---------|------------------|------------------------------|
| **Dashboard** | Interfaz interactiva que muestra datos filtrados en tiempo real | Sistema de información de gestión (SIG) de un servicio público |
| **Gradio** | Biblioteca Python para crear interfaces web sin HTML/JS | Formulario web de consulta que tú mismo construiste |
| **`gr.Interface`** | Forma simple de crear un tablero con una sola función | Pantalla única de consulta con filtros y resultado |
| **`gr.Dropdown`** | Lista desplegable de opciones para elegir un filtro | Lista desplegable en un formulario de contrataciones |
| **`gr.Plot`** | Área de salida que muestra una figura matplotlib | El panel de gráficos de un informe dinámico |
| **`demo.launch(share=True)`** | Publica el tablero con una URL pública temporal | Compartir un informe interactivo por enlace sin infraestructura |
| **KPI** | Indicador clave de desempeño; número que resume el estado de algo | Número grande en la portada de un tablero de control ministerial |
| **Función pura** | Función que recibe datos y devuelve un resultado sin efectos secundarios | Un cálculo que siempre da el mismo resultado con los mismos datos |
| **`df.copy()`** | Crea una copia independiente del DataFrame para no modificar el original | Duplicar una hoja de Excel antes de filtrarla |
| **`barh`** | Gráfico de barras horizontal (mejor para muchas categorías con texto largo) | Gráfico de ranking de proveedores en un informe de compras |
| **Prototipo** | Versión funcional pero simplificada de una herramienta | Prueba de concepto antes de implementar un sistema formal |
| **Hugging Face Spaces** | Plataforma gratuita para publicar tableros Gradio de forma permanente | Servidor público donde vive el sistema |

---

## 11. Conexión con el Módulo Siguiente

### Lo que viene: R1-CAP · Capstone de Análisis

En R1-09 construiste tu primer tablero interactivo. En **R1-CAP** vas a usar todo lo que aprendiste en la Rama R1 para resolver un problema real de principio a fin:

- Cargar y limpiar un dataset de compras públicas
- Hacer el análisis exploratorio
- Calcular estadísticas descriptivas
- Crear visualizaciones comunicativas y honestas
- Presentar los hallazgos con un informe o tablero

El Capstone no tiene celdas de chequeo automático: tú defines las preguntas, tú exploras, tú concluyes.

### Pregunta motivadora

> Llegas al Capstone con 9 módulos de herramientas. ¿Qué pregunta de tu trabajo diario podrías responder ahora que antes no podías? ¿Sobre qué dataset del Estado te gustaría aplicar todo esto?
