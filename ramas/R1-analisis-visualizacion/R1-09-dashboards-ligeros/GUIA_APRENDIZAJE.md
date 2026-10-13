# Guía de Aprendizaje — R1-09 · Dashboards ligeros con Gradio

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 9 · Semana 10

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-09 · Dashboards ligeros |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Intermedio — requiere R1-07 y R1-08 (visualización) |
| **Prerrequisitos** | Funciones, `groupby`, gráficos con `fig, ax` |
| **Competencia de salida** | Publicar un tablero interactivo simple sobre datos públicos, sin instalar nada |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ (el tablero Gradio se lanza en Colab) |
| **Dataset** | `matricula.csv` — matrícula oficial 2025 (MINEDUC) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

Hay un momento en que el informe estático deja de bastar: el equipo regional quiere ver *su* región, la jefatura quiere cambiar el filtro *ella misma*, y tú no quieres regenerar el PDF cada vez. Ese es el momento del **dashboard**.

Este módulo enseña el camino más corto entre un DataFrame y una aplicación web interactiva: **Gradio**. Sin servidores, sin permisos de TI, sin instalar nada localmente — corre dentro de Colab y `demo.launch(share=True)` genera un enlace público temporal que puedes mandar por correo.

Igual de importante es la arquitectura que practica el módulo: el tablero se construye como **funciones puras de pandas** (filtrar, KPIs, tabla, figura) que se prueban por separado, y la interfaz solo las envuelve. Esa separación — lógica de datos vs interfaz — es la diferencia entre un tablero mantenible y uno que nadie se atreve a tocar.

Y la pregunta final del módulo es de criterio, no de código: **¿cuándo NO hacer un dashboard?** Si la pregunta se responde una vez, basta un gráfico.

---

## 3. Mapa Conceptual del Módulo

| Pieza | ¿Qué hace? | Equivalente en el trabajo del Estado |
|-------|-----------|--------------------------------------|
| **`filtrar(df, ...)`** | Reduce los datos según la selección del usuario | Los combos de un sistema de consulta |
| **`kpis(d)`** | Los 2-3 números grandes del tablero | El resumen ejecutivo de la minuta |
| **Tabla resumen** | `groupby` ordenado que alimenta el panel | La tabla anexa del informe |
| **Función que devuelve `fig`** | Gráfico como componente reutilizable | La lámina que se actualiza sola |
| **`gr.Interface`** | Envuelve funciones en una página web | El formulario de consulta ciudadana |
| **`demo.launch(share=True)`** | Publica un enlace temporal desde Colab | Compartir el tablero sin pasar por TI |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Escribir una función con parámetros por defecto (`def f(x, y=1):`) | ☐ |
| Agrupar y ordenar con `groupby(...).sum().sort_values()` | ☐ |
| Construir una figura con `fig, ax = plt.subplots()` y devolverla | ☐ |

Si respondiste No a alguna, repasa R1-00 (funciones) y R1-07 (gráficos).

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Cargar la matrícula 2025.

✅ **Señal de que entendiste:** Ves las columnas `dependencia`, `region`, `comuna`, `mat_total` — las cuatro que usará el tablero.

---

### Sección 1 · Filtrar

🎯 **Objetivo:** Una función que filtra por dependencia y región, con `"(todas)"` como valor neutro.

💡 **Concepto clave:** El valor centinela `"(todas)"` permite que el mismo código sirva con y sin filtro: solo se aplica la condición cuando el usuario eligió algo distinto. `df.copy()` al inicio evita modificar el DataFrame original — una función de tablero **nunca** debe mutar los datos de entrada.

⚠️ **Error frecuente:** Filtrar siempre, sin el `if`. Con `dependencia="(todas)"` el filtro `d["dependencia"] == "(todas)"` devolvería 0 filas.

✅ **Señal de que entendiste:** `filtrar(df)` devuelve las 10.945 filas; `filtrar(df, dependencia="Municipal")` solo las municipales.

---

### Sección 2 · KPIs

🎯 **Objetivo:** Los tres números grandes: establecimientos, estudiantes, tamaño promedio.

💡 **Concepto clave:** Un KPI es un número con nombre. Devolverlos como **diccionario** (`{"n_establecimientos": ..., ...}`) los hace autodescriptivos y fáciles de mostrar. El `if len(d) else 0.0` protege del caso borde: un filtro sin resultados no debe romper el tablero con una división por cero.

✅ **Señal de que entendiste:** `kpis(filtrar(df, region="Aysén"))` devuelve números más chicos pero la misma estructura.

---

### Sección 3 · Tabla resumen

🎯 **Objetivo:** Matrícula por región, ordenada de mayor a menor.

💡 **Concepto clave:** La tabla del tablero es un `groupby` con `sort_values(ascending=False)`: un ranking listo para mostrar. La ilustración muestra cómo se vería como panel con `barh`.

✅ **Señal de que entendiste:** La serie resultante está ordenada y tiene 16 filas.

---

### Sección 4 · Gráfico como componente

🎯 **Objetivo:** Una función que **devuelve** la figura del top de comunas (no la muestra: la retorna).

💡 **Concepto clave:** La diferencia entre `plt.show()` (muestra y termina) y `return fig` (entrega el objeto). Gradio necesita el objeto `Figure` para renderizarlo en la página — por eso el componente se escribe como función que retorna. Es el mismo principio de las funciones puras: la interfaz decide qué hacer con el resultado.

✅ **Señal de que entendiste:** `type(figura_top_comunas(df)).__name__` imprime `Figure`.

---

### Sección 5 · Arma el tablero

🎯 **Objetivo:** Envolver las cuatro funciones en `gr.Interface` y (en Colab) publicarlo.

💡 **Concepto clave:** `gr.Interface(fn, inputs, outputs)`: la función `tablero(dependencia, region)` recibe lo que el usuario elige en los dos `Dropdown` y devuelve lo que muestran los dos componentes de salida (`Text` y `Plot`). La celda está protegida con `try/except` porque Gradio no siempre está instalado fuera de Colab; en Colab, `!pip -q install gradio` y `demo.launch(share=True)`.

⚠️ **Error frecuente:** Esperar que el enlace `share=True` sea permanente. Dura unas horas: para publicar en serio, el camino es Hugging Face Spaces (gratis).

✅ **Señal de que entendiste:** En Colab ves tu tablero funcionando y puedes mandarle el enlace a un colega.

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Escribe la función `filtrar`

**Objetivo:** El corazón del tablero: reducir los datos según la selección.
**Habilidad que entrena:** Funciones con valores por defecto, filtros condicionales.

**Pistas progresivas:**
- 🟢 Pista suave: Son dos `if` con la misma forma: si el parámetro no es `"(todas)"`, aplica el filtro correspondiente.
- 🟡 Pista media: `if dependencia != "(todas)": d = d[d["dependencia"] == dependencia]` — y lo mismo para región.
- 🔴 Pista directa: Dos bloques: `if dependencia != "(todas)": d = d[d["dependencia"] == dependencia]` y `if region != "(todas)": d = d[d["region"] == region]`.

**¿Qué significa el ✅?** Que sin argumentos devuelve todo, y con `dependencia="Municipal"` devuelve solo establecimientos municipales.

---

### Ejercicio 2 — Escribe la función `kpis`

**Objetivo:** Los tres indicadores del tablero como diccionario.
**Habilidad que entrena:** Agregaciones básicas empaquetadas.

**Pistas progresivas:**
- 🟢 Pista suave: Cada valor del diccionario es una agregación de una línea sobre `d`.
- 🟡 Pista media: `len(d)`, `d["mat_total"].sum()`, `d["mat_total"].mean()`.
- 🔴 Pista directa: `"n_establecimientos": int(len(d))`, `"estudiantes": int(d["mat_total"].sum())`, `"tamano_promedio": float(d["mat_total"].mean()) if len(d) else 0.0`.

**¿Qué significa el ✅?** Que los tres KPIs coinciden con los cálculos directos de pandas sobre el DataFrame completo.

---

### Ejercicio 3 — Escribe `matricula_por_region`

**Objetivo:** El ranking regional que alimenta el panel principal.
**Habilidad que entrena:** `groupby` + `sort_values` como función reutilizable.

**Pistas progresivas:**
- 🟢 Pista suave: Es una sola línea: agrupar, sumar, ordenar descendente.
- 🟡 Pista media: `groupby("region")["mat_total"].sum()` y luego `.sort_values(ascending=False)`.
- 🔴 Pista directa: `return d.groupby("region")["mat_total"].sum().sort_values(ascending=False)`.

**¿Qué significa el ✅?** Que la serie está ordenada de mayor a menor y tiene una fila por región.

---

### Ejercicio 4 — Escribe `figura_top_comunas`

**Objetivo:** Un gráfico que se **devuelve** como objeto, listo para Gradio.
**Habilidad que entrena:** Funciones que retornan figuras.

**Pistas progresivas:**
- 🟢 Pista suave: El `top` ya está calculado. Falta dibujar las barras horizontales y retornar la figura.
- 🟡 Pista media: `ax.barh(top.index, top.values)` y al final `return fig` (ya está escrito).
- 🔴 Pista directa: `ax.barh(top.index, top.values, color="#ff6b35")` — y verifica que el `return fig` esté fuera del TODO.

**¿Qué significa el ✅?** Que la función devuelve un objeto `Figure` con al menos un eje dibujado.

---

> 🔬 **En la profundización:** tres componentes más para tu tablero — matrícula por **dependencia** (el KPI de política educativa), `formato_miles()` para mostrar «3.541.783» en vez de «3541783», y `participacion()`: qué % de los estudiantes está en cada dependencia.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué `filtrar` hace `d = df.copy()` al inicio?

- A) Para que corra más rápido
- B) Para no modificar el DataFrame original: la función debe ser pura, sin efectos secundarios ✅
- C) Porque pandas lo exige
- D) Para ahorrar memoria

**Explicación:** Si la función mutara `df`, cada filtro del usuario iría degradando los datos del tablero. Copiar garantiza que cada llamada parte de los datos completos.

---

**Pregunta 2:** ¿Para qué sirve el valor `"(todas)"` en los parámetros?

- A) Es un valor mágico de pandas
- B) Es un centinela: indica «sin filtro» y permite que la misma función sirva con y sin selección ✅
- C) Filtra las filas que digan «todas»
- D) Es obligatorio en Gradio

**Explicación:** El dropdown siempre entrega *algún* valor. `"(todas)"` es la opción neutra: la función la reconoce y omite ese filtro.

---

**Pregunta 3:** ¿Cuál es la diferencia clave entre `plt.show()` y `return fig` en un componente de tablero?

- A) Ninguna
- B) `plt.show()` muestra y descarta; `return fig` entrega el objeto para que la interfaz lo renderice ✅
- C) `return fig` es más lento
- D) `plt.show()` solo funciona en Colab

**Explicación:** Gradio (y cualquier framework de UI) necesita recibir el objeto figura para incrustarlo en la página. Mostrar no es entregar.

---

**Pregunta 4:** ¿Qué pasa con el enlace de `demo.launch(share=True)`?

- A) Es permanente
- B) Es temporal (horas): para publicación estable se usa Hugging Face Spaces ✅
- C) Solo funciona en la misma red
- D) Requiere permisos de administrador

**Explicación:** El enlace `share` es un túnel temporal ideal para demos. La publicación permanente y gratuita es via Spaces.

---

**Pregunta 5:** Tu jefatura pide «un dashboard» para un dato que se consulta una vez al año en la cuenta pública. ¿Qué respondes?

- A) Lo construyo igual, más tecnología es mejor
- B) Propongo un gráfico o informe estático: el dashboard se justifica solo con exploración recurrente ✅
- C) Es imposible hacerlo
- D) Solo si usamos otra herramienta

**Explicación:** El criterio del módulo: el tablero tiene costo de mantención. Si la pregunta se responde una vez, la respuesta es un gráfico honesto (R1-08), no una app.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Dashboard** | Interfaz para explorar datos con filtros | Sistema de consulta interno |
| **Función pura** | Misma entrada → misma salida, sin efectos laterales | Procedimiento que no toca el original |
| **Centinela `"(todas)"`** | Valor que significa «sin filtro» | La opción «Todos» de un combo |
| **KPI** | Indicador clave, un número con nombre | La cifra del resumen ejecutivo |
| **Gradio** | Librería que convierte funciones en páginas web | El camino corto a la app de consulta |
| **`gr.Interface`** | Une función + entradas + salidas en una UI | El formulario del sistema |
| **`Dropdown`** | Selector de opciones | Combo de región/dependencia |
| **`launch(share=True)`** | Publica un enlace temporal desde Colab | Demo compartible sin infraestructura |
| **Hugging Face Spaces** | Hosting gratuito permanente para apps Gradio | Publicación estable sin servidores propios |

---

## 9. Conexión con el Módulo Siguiente

En R1-09 cerraste el ciclo técnico de la rama: traer el dato → explorarlo → limpiarlo → analizarlo → visualizarlo → **entregarlo como producto interactivo**.

En **R1-CAP · Capstone** lo juntas todo: elegirás un dataset público —idealmente de tu propio servicio— y construirás de punta a punta un análisis con visualizaciones y conclusiones honestas, presentable como portafolio. Es el módulo donde el curso deja de darte los datos y el problema pasa a ser tuyo.

> 💡 **Pregunta para reflexionar:** ¿Qué consulta repetitiva de tu servicio merecería un tablero como el que acabas de construir? ¿Quién lo usaría cada semana, y con qué dos filtros?
