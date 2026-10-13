# Guía de Aprendizaje — R1-08 · Visualización para comunicar + ética

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R1 · Analista de Datos · Módulo 8 · Semana 9

---

## 1. Datos del Módulo

| Campo | Detalle |
|-------|---------|
| **Módulo** | R1-08 · Visualización para comunicar + ética |
| **Rama** | R1 — Análisis y Visualización |
| **Duración estimada** | 90 minutos |
| **Nivel** | Intermedio — requiere R1-07 (visualización exploratoria) |
| **Prerrequisitos** | `groupby`, `ax.bar`, el patrón `fig, ax = plt.subplots()` |
| **Competencia de salida** | Comunicar un hallazgo con un gráfico claro y honesto para una audiencia directiva |
| **Entregable** | Las 4 celdas de chequeo deben mostrar ✅ |
| **Dataset** | `matricula.csv` — matrícula oficial 2025 por región (MINEDUC). Profundización: `aire_diario.csv` — PM2.5 por estación (SINCA) |

---

## 2. ¿Para qué me sirve esto como funcionario público?

En R1-07 hiciste gráficos para ti. Este módulo es sobre gráficos **para otros**: la minuta que sube a la jefatura, la lámina de la cuenta pública, el informe que llega a la prensa.

Y ahí cambia todo, porque un gráfico público tiene **consecuencias**. Un eje truncado puede convertir una diferencia del 2% entre dependencias en un abismo visual; un ranking sin fuente puede instalar una conclusión errada; un color mal elegido puede acusar sin datos. En el Estado, el gráfico ES la comunicación oficial — y la honestidad visual no es una preferencia estética, es integridad pública.

Este módulo te da las cuatro reglas mínimas del gráfico honesto (eje desde 0, título que se entiende solo, etiquetas, anotación del mensaje) y te entrena para reconocer el engaño visual más común, con el mismo dato mostrado de las dos maneras.

---

## 3. Mapa Conceptual del Módulo

| Regla | ¿Por qué importa? | Herramienta |
|-------|-------------------|-------------|
| **Eje Y desde 0** | El eje truncado exagera diferencias pequeñas | `ax.set_ylim(bottom=0)` |
| **Título que afirma** | El gráfico debe entenderse sin ti al lado | `ax.set_title(...)` |
| **Etiquetas de ejes** | Sin unidades, el número no significa nada | `ax.set_xlabel/ylabel` |
| **Anotar el mensaje** | Guiar la mirada al hallazgo | `ax.annotate(...)` |
| **Comparar versiones** | Ver el engaño entrena a no cometerlo | dos `ax` lado a lado |

---

## 4. Verificación de Prerrequisitos

| ¿Puedo...? | Sí / No |
|-----------|---------|
| Crear un gráfico con `fig, ax = plt.subplots()` | ☐ |
| Hacer barras con `ax.bar(etiquetas, valores)` | ☐ |
| Agrupar con `groupby(...).sum()` y ordenar con `sort_values()` | ☐ |

Si respondiste No a alguna, vuelve a R1-07 antes de continuar.

---

## 5. Guía Paso a Paso por Sección del Notebook

### Sección 0 · Preparación

🎯 **Objetivo:** Construir la serie con la que trabajarás todo el módulo: matrícula total por región, las 6 mayores.

💡 **Concepto clave:** `groupby("region")["mat_total"].sum()` colapsa los 10.945 establecimientos en 16 filas regionales; `.sort_values(ascending=False).head(6)` se queda con el top 6. Toda la lección usa esta misma serie `g` — el foco del módulo no es calcular, es **comunicar**.

✅ **Señal de que entendiste:** Ves 6 regiones con sus totales, encabezadas por la Metropolitana.

---

### Sección 1 · El eje Y empieza en cero

🎯 **Objetivo:** Dibujar barras cuyo eje vertical parte de 0.

💡 **Concepto clave:** La barra codifica el valor con su **altura**. Si el eje parte en otro número, las alturas dejan de ser proporcionales a los valores y el ojo lee diferencias infladas. Por eso la regla profesional es: barras, siempre desde 0 (para líneas la discusión es distinta, pero eso viene después).

⚠️ **Error frecuente:** Creer que matplotlib parte de 0 por defecto. A veces sí, pero no está garantizado: `set_ylim(bottom=0)` lo hace explícito y auditable.

✅ **Señal de que entendiste:** `ax.get_ylim()[0]` devuelve `0.0`.

---

### Sección 2 · Título y etiquetas

🎯 **Objetivo:** Que el gráfico se entienda sin explicación oral.

💡 **Concepto clave:** La prueba del pasillo: si alguien encuentra tu lámina impresa en el pasillo, ¿entiende qué está viendo? Necesita saber **qué** se mide (título), **dónde** (eje x) y **en qué unidad** (eje y). Un buen título afirma («Matrícula escolar por región, 2025»), no describe vagamente («Gráfico de barras»).

✅ **Señal de que entendiste:** Los tres textos existen y el título incluye el año del dato.

---

### Sección 3 · Anotar el dato clave

🎯 **Objetivo:** Señalar dentro del gráfico el mensaje principal.

💡 **Concepto clave:** `ax.annotate(texto, xy=punto_señalado, xytext=posición_del_texto, arrowprops=...)` dibuja el texto y una flecha. La anotación convierte un gráfico neutro en un gráfico con **mensaje**: no «aquí están los datos» sino «mira esto». `g.idxmax()` te da el nombre de la región con el máximo — así la anotación se actualiza sola si cambian los datos.

⚠️ **Error frecuente:** Confundir `xy` (a dónde apunta la flecha) con `xytext` (dónde queda el texto).

✅ **Señal de que entendiste:** `ax.texts` no está vacío y la flecha apunta a la barra correcta.

---

### Sección 4 · Engañoso vs honesto

🎯 **Objetivo:** Construir el mismo gráfico dos veces: con eje truncado y desde cero.

💡 **Concepto clave:** El truncado (`bottom=g.min()*0.98`) hace ver la sexta región como si casi no tuviera estudiantes comparada con la primera — cuando la diferencia real es visible pero no abismal. Poner ambos lado a lado es la vacuna: una vez que ves el truco, lo reconoces en cualquier informe. La diferencia entre ambos gráficos **no es de datos** — los datos son idénticos — es de **decisión editorial**.

✅ **Señal de que entendiste:** Puedes explicar por qué el gráfico truncado no es «más claro» sino menos honesto, aunque «se vea mejor».

---

## 6. Guía de los 4 Ejercicios

### Ejercicio 1 — Dibuja barras con el eje desde 0

**Objetivo:** Hacer explícito el punto de partida del eje Y.
**Habilidad que entrena:** `ax.set_ylim(bottom=0)`.

**Pistas progresivas:**
- 🟢 Pista suave: El límite inferior del eje Y es configurable con un método de `ax`.
- 🟡 Pista media: El método es `set_ylim` y acepta el argumento `bottom`.
- 🔴 Pista directa: `ax.set_ylim(bottom=0)`.

**¿Qué significa el ✅?** Que `ax.get_ylim()[0] == 0`: el eje efectivamente parte de cero.

---

### Ejercicio 2 — Agrega título y etiquetas

**Objetivo:** Hacer que el gráfico se sostenga solo.
**Habilidad que entrena:** `set_title`, `set_xlabel`, `set_ylabel`.

**Pistas progresivas:**
- 🟢 Pista suave: Son tres métodos de `ax`, uno para cada texto.
- 🟡 Pista media: `ax.set_title("...")`, `ax.set_xlabel("...")`, `ax.set_ylabel("...")`.
- 🔴 Pista directa: `ax.set_title("Matrícula escolar por región, 2025 (top 6)"); ax.set_xlabel("Región"); ax.set_ylabel("Estudiantes matriculados")`.

**¿Qué significa el ✅?** Que los tres textos son no vacíos. El check no evalúa la calidad del título — eso es criterio tuyo: que afirme, no que describa.

---

### Ejercicio 3 — Anota la región con más estudiantes

**Objetivo:** Guiar la mirada al mensaje.
**Habilidad que entrena:** `ax.annotate` con flecha.

**Pistas progresivas:**
- 🟢 Pista suave: `annotate` necesita el texto, el punto al que apunta (`xy`) y dónde poner el texto (`xytext`).
- 🟡 Pista media: El punto señalado es la primera barra: `xy=(0, g.max())`. El texto, un poco a la derecha y más abajo.
- 🔴 Pista directa: `ax.annotate(f"Más estudiantes: {g.idxmax()}", xy=(0, g.max()), xytext=(1, g.max()*0.9), arrowprops=dict(arrowstyle="->"))`.

**¿Qué significa el ✅?** Que existe al menos un texto anotado sobre el gráfico.

---

### Ejercicio 4 — Construye las dos versiones

**Objetivo:** Ver el mismo dato con eje truncado y desde cero, lado a lado.
**Habilidad que entrena:** Subplots múltiples, y el ojo crítico.

**Pistas progresivas:**
- 🟢 Pista suave: La versión engañosa ya está construida en `ax1`. A `ax2` le falta una sola línea.
- 🟡 Pista media: Es la misma línea del ejercicio 1, aplicada a `ax2`.
- 🔴 Pista directa: `ax2.set_ylim(bottom=0)`.

**¿Qué significa el ✅?** Que `ax2` parte de 0 y `ax1` no: tienes el par engañoso/honesto completo para comparar.

---

> 🔬 **En la profundización** cambia el dominio: **PM2.5 promedio por estación SINCA** (un adelanto de la rama R2, donde ese dataset es el ancla). Destacarás con color la estación más contaminada, pondrás etiquetas de valor sobre las barras y escribirás `revisar_grafico()`: un checklist de honestidad automatizado que puedes reutilizar en cualquier informe futuro.

---

## 7. Autoevaluación Final

**Pregunta 1:** ¿Por qué las barras deben partir de 0?

- A) Por convención estética
- B) Porque la barra codifica el valor con su altura: si el eje parte en otro número, las alturas dejan de ser proporcionales y las diferencias se exageran ✅
- C) Porque matplotlib da error si no
- D) Para que quepa el título

**Explicación:** El lector compara alturas, no lee números. Truncar el eje rompe la proporción altura/valor, que es todo el contrato visual del gráfico de barras.

---

**Pregunta 2:** ¿Cuál es el mejor título para el gráfico de este módulo?

- A) «Gráfico de barras»
- B) «Datos de matrícula»
- C) «Matrícula escolar por región, 2025 (top 6)» ✅
- D) «Figura 1»

**Explicación:** El título debe decir qué se mide, dónde y cuándo. «Figura 1» y «Gráfico de barras» describen el formato, no el contenido; «Datos de matrícula» omite el corte y el año.

---

**Pregunta 3:** ¿Qué diferencia hay entre `xy` y `xytext` en `annotate`?

- A) Son sinónimos
- B) `xy` es el punto al que apunta la flecha; `xytext` es donde se ubica el texto ✅
- C) `xy` es para el eje x y `xytext` para el eje y
- D) `xytext` solo funciona sin flecha

**Explicación:** La anotación tiene dos anclas: el dato señalado (`xy`) y la posición del rótulo (`xytext`); `arrowprops` dibuja la flecha entre ambos.

---

**Pregunta 4:** Un informe muestra la diferencia de matrícula entre dos dependencias con un eje que parte en 45.000. Las barras se ven una al doble de la otra, pero los valores son 46.000 y 47.000. ¿Qué es esto?

- A) Un gráfico correcto porque los números son verdaderos
- B) Un engaño visual por eje truncado: los datos son ciertos pero la percepción inducida es falsa ✅
- C) Un error de matplotlib
- D) Una técnica recomendada para destacar diferencias

**Explicación:** La mentira visual no necesita datos falsos: basta romper la proporción. La diferencia real es ~2%; la percibida, ~100%.

---

**Pregunta 5:** ¿Cuál de estos elementos NO es parte del mínimo ético de un gráfico público?

- A) Eje de barras desde 0
- B) Título y unidades claras
- C) Fuente del dato
- D) Colores corporativos de la institución ✅

**Explicación:** Los colores institucionales son deseables pero no éticos: un gráfico puede ser perfectamente honesto en blanco y negro. Eje, rotulación y fuente sí son el piso mínimo.

---

## 8. Glosario del Módulo

| Término | Definición simple | Equivalente en el trabajo del Estado |
|---------|-------------------|--------------------------------------|
| **Eje truncado** | Eje Y que no parte de 0 | El engaño visual más común en informes |
| **`set_ylim(bottom=0)`** | Fija el inicio del eje Y | Garantía de proporcionalidad |
| **Título que afirma** | Dice el hallazgo, no el formato | El asunto de un oficio bien escrito |
| **Anotación** | Texto + flecha dentro del gráfico | El destacado de la minuta |
| **`idxmax()`** | Índice (nombre) del valor máximo | «¿Quién lidera el ranking?» |
| **Engaño visual** | Percepción falsa con datos verdaderos | Falta a la integridad pública |
| **Checklist de honestidad** | Verificación automática del mínimo ético | Pauta de revisión antes de publicar |
| **Prueba del pasillo** | ¿Se entiende el gráfico sin su autor al lado? | Estándar de un documento oficial |

---

## 9. Conexión con el Módulo Siguiente

En R1-08 aprendiste a comunicar con integridad: eje desde 0, título que afirma, etiquetas, anotación, y el ojo entrenado contra el eje truncado.

En **R1-09 · Dashboards ligeros** darás el último paso de la rama antes del capstone: convertir tus gráficos en una **aplicación interactiva con Gradio** que cualquier persona puede usar desde el navegador — sin instalar nada — para explorar los datos por sí misma.

> 💡 **Pregunta para reflexionar:** Busca un gráfico publicado por una institución pública esta semana (prensa, redes, informes). Pásale mentalmente el `revisar_grafico()`: ¿eje desde 0?, ¿título que afirma?, ¿unidades? ¿Pasa el checklist?
