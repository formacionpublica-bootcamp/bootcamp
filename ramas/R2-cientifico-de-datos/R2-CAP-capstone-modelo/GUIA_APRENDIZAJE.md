# Guía de Aprendizaje · R2-CAP · Capstone — Modelo predictivo sobre datos de tu organismo

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**
Rama R2 · Científico de Datos · Semana 17–18 · Google Colab

---

## 1. Portada y Datos del Módulo

| Campo | Detalle |
|---|---|
| **Módulo** | R2-CAP · Capstone — modelo predictivo sobre datos de tu organismo |
| **Rama** | R2 · Científico de Datos |
| **Semanas** | 17–18 (cierre de rama) |
| **Duración estimada** | 4–6 horas de trabajo autónomo |
| **Nivel** | Integrador — aplica todo lo aprendido en R2-00 a R2-10 |
| **Prerrequisitos** | Haber completado R2-00 a R2-10 con ✅ en todos los notebooks |
| **Dataset de ejemplo** | `compras_ml.csv` — 7.412 órdenes de compra pública de alimentos (estilo ChileCompra), o datos de tu propio organismo |
| **Competencia de salida** | Ejecutar el ciclo de vida completo de un modelo de ML de forma responsable — enmarcar → features sin fuga → entrenar → evaluar honestamente → documentar en una model card |
| **Entregable** | Notebook reproducible con las 3 celdas de chequeo en ✅ + model card completa |

---

## 2. ¿Para qué me sirve esto como funcionario/a público/a?

En el capstone de R1 demostraste que puedes **analizar** un dato y comunicarlo. Este capstone da el paso siguiente: demostrar que puedes **construir un modelo que apoye una decisión pública** — y hacerlo de forma responsable.

En el Estado, los modelos predictivos ya están operando: priorización de fiscalizaciones en el SII, alertas tempranas de deserción escolar en Mineduc, listas de espera en salud. Pero un modelo mal construido no es neutro — puede concentrar fiscalizaciones en los mismos de siempre, invisibilizar regiones o automatizar un sesgo histórico. **La diferencia entre un modelo útil y uno peligroso no es la técnica: es el proceso.** Y ese proceso es exactamente lo que este capstone evalúa: framing claro, features sin trampa, evaluación honesta y una model card que declara los límites.

El ejemplo del módulo usa compras públicas de alimentos: predecir si una orden la adjudicará un **proveedor grande**, para entender la concentración del mercado. Es la misma lógica que usarías para anticipar demanda de un servicio, priorizar casos o detectar patrones atípicos en tu institución.

### ⚠️ Si usas datos de tu propio organismo — lee esto primero

El capstone te invita a reemplazar `compras_ml.csv` por datos reales de tu servicio. Antes de hacerlo:

1. **Anonimiza los datos personales.** Elimina o reemplaza RUT, nombres, direcciones, correos, teléfonos y cualquier combinación que permita reidentificar a una persona. La Ley 19.628 (y su reforma) te obliga; el sentido común también.
2. **No subas datos sensibles a herramientas de IA** (ChatGPT, Claude, Gemini…) ni a repositorios públicos de GitHub: lo que subes puede quedar fuera de tu control.
3. **Pide autorización** a tu jefatura o encargado/a de datos si dudas de si el dataset es publicable. Si no puedes anonimizar con seguridad, **usa el dataset de ejemplo**: el aprendizaje es el mismo y el riesgo es cero.

Regla simple: si el dato no podría aparecer en Transparencia Activa tal como está, no lo subas a ninguna parte.

---

## 3. Mapa conceptual del Capstone

```
┌────────────────────────────────────────────────────────────────────────────┐
│  CICLO DE VIDA RESPONSABLE DE UN MODELO EN EL SECTOR PÚBLICO               │
├────────────────────┬────────────────────────────────────────────────────────┤
│ Etapa              │ Analogía con tu trabajo                                │
├────────────────────┼────────────────────────────────────────────────────────┤
│ 1. ENMARCAR        │ Definir qué decisión apoya el modelo antes de programar│
│ 2. FEATURES SIN    │ No usar como "pista" un dato que ya contiene la        │
│    FUGA            │ respuesta — como calificar un concurso mirando el acta │
│ 3. ENTRENAR        │ Armar el procedimiento estándar (pipeline) que         │
│    (PIPELINE)      │ cualquier colega puede repetir igual                   │
│ 4. EVALUAR         │ Medir con datos que el modelo nunca vio, con la        │
│    HONESTAMENTE    │ métrica correcta para clases desbalanceadas            │
│ 5. MODEL CARD      │ La "ficha técnica" del modelo: qué hace, qué no hace,  │
│                    │ y bajo qué condiciones se puede usar                   │
└────────────────────┴────────────────────────────────────────────────────────┘
```

**Lo que integra este capstone:**

| Módulo anterior | Habilidad que aplicas aquí |
|---|---|
| R2-01 Datos: traer, cruzar, limpiar | Cargar y preparar `compras_ml.csv` (o tu dataset) |
| R2-03 Estadística para modelar | Entender el desbalance de clases (solo 2,4% son "Grande") |
| R2-04 Fundamentos de ML | `train_test_split`, target binario, regresión logística |
| R2-06 Clasificación | Clasificador binario y `OneHotEncoder` para categóricas |
| R2-07 Evaluación y validación | F1 en test, fuga de datos, validación cruzada (profundiza) |
| R2-08 Pipelines reproducibles | `Pipeline` + `ColumnTransformer` de scikit-learn |
| R2-09 Despliegue de modelos | La model card como documento que acompaña al modelo |

---

## 4. Antes de empezar: Verificación de prerrequisitos

### ¿Qué necesito saber?

Checklist de verificación — responde honestamente:

| ¿Puedo…? | Módulo donde lo viste | ¿OK? |
|---|---|---|
| Cargar un CSV con `pd.read_csv()` y explorar sus columnas | R2-01 | ☐ |
| Explicar qué es un target binario y crear uno con una condición | R2-04 | ☐ |
| Separar train/test con `train_test_split` y explicar por qué | R2-04 | ☐ |
| Explicar qué es la fuga de datos (*data leakage*) con un ejemplo | R2-07 | ☐ |
| Armar un `Pipeline` con `ColumnTransformer` + clasificador | R2-08 | ☐ |
| Explicar por qué accuracy engaña con clases desbalanceadas | R2-07 | ☐ |
| Calcular e interpretar un F1-score | R2-07 | ☐ |

Si alguna casilla queda vacía, vuelve al módulo correspondiente antes de empezar. Un capstone se construye sobre terreno firme, no sobre memoria frágil.

### Configuración del entorno

Abre `leccion.ipynb` en Google Colab y ejecuta la **celda de preparación** (descarga el CSV si no está local). Debe aparecer `Datos cargados: (7412, 6) filas x columnas`. Si falta alguna librería: `!pip install pandas scikit-learn`.

### Conoce el dataset de ejemplo

`compras_ml.csv` — 7.412 órdenes de compra de alimentos, 6 columnas, sin nulos:

| Columna | Qué contiene |
|---|---|
| `cantidad` | Unidades compradas en la orden (0 a 492) |
| `monto_total` | Monto de la orden en pesos ($100 a $4.947.600; promedio ≈ $108.992) |
| `categoria` | 12 categorías de alimentos (lácteos, panadería, pescados, bebidas…) |
| `region_comprador` | 15 regiones de Chile |
| `tamano_proveedor` | Tamaño del proveedor: Pequeña (5.976), Mediana (1.137), Grande (178), Micro (121) |
| `tamano_num` | Versión numérica de la columna anterior (1=Micro … 4=Grande) — ⚠️ **fuga** |

El target del ejemplo es **"¿el proveedor es Grande?"**: solo el **2,4%** de las órdenes. Ese desbalance extremo es el corazón pedagógico del capstone.

---

## 5. Guía paso a paso por sección del notebook

---

### Sección 1 · Enmarca el problema de modelado

🎯 **Objetivo:** Escribir en una frase la **decisión pública** que el modelo va a apoyar y por qué un modelo aporta.

💡 **Concepto clave:** Un modelo sin decisión asociada es un adorno estadístico. El framing responde tres preguntas: *¿qué se predice?, ¿quién usa la predicción?, ¿qué hace distinto gracias a ella?* El ejemplo del módulo: *predecir si una orden la adjudicará un proveedor grande, para entender la concentración del mercado de compras públicas* — útil, por ejemplo, para una unidad de abastecimiento que quiere fomentar la participación de pymes.

⚠️ **Error frecuente:** Enmarcar el problema como "quiero probar machine learning con mis datos". Eso es empezar por la herramienta. Empieza por la decisión: si nadie haría nada distinto con la predicción, no necesitas un modelo — necesitas un buen análisis descriptivo (eso ya lo dominas desde R1).

✅ **Sabes esta sección cuando puedes:** Completar sin dudar la frase: *"Este modelo predice ___ para que ___ pueda ___".*

---

### Sección 2 · Features sin fuga de datos

🎯 **Objetivo:** Seleccionar variables predictoras honestas, dejando fuera todo lo que "es" la respuesta.

💡 **Concepto clave:** La **fuga de datos** (*data leakage*) es incluir entre las features información que contiene el target. En este dataset, `tamano_num` es literalmente `tamano_proveedor` en números (Micro=1 … Grande=4). Un modelo entrenado con ella tendría 100% de acierto en el notebook y 0% de utilidad en la realidad. Es como evaluar un concurso público mirando el acta de adjudicación: aciertas siempre, pero no aprendiste nada.

🔍 **Qué hace el código de esta sección:**

```python
y = (df["tamano_proveedor"] == "Grande").astype(int)
X = df[FEATURES]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
```

- La primera línea crea el target binario: 1 si el proveedor es Grande, 0 si no
- `train_test_split(..., test_size=0.3, ...)` reserva el 30% para prueba: con este dataset, 5.188 filas de entrenamiento y 2.224 de test
- `stratify=y` garantiza que el 2,4% de positivos se reparta igual en ambos conjuntos — crítico cuando la clase de interés es tan escasa
- `random_state=42` fija la semilla: cualquiera que corra el notebook obtiene la misma partición

⚠️ **Error frecuente:** Pensar que la fuga siempre es tan obvia como `tamano_num`. En datos reales se disfraza: una columna "estado del trámite" que se llena *después* de la decisión que quieres predecir, o un promedio calculado sobre todo el dataset (incluido el test). Pregunta siempre: *¿esta variable existiría en el momento en que necesito la predicción?*

✅ **Sabes esta sección cuando puedes:** Mirar las 6 columnas del dataset y explicar cuáles son features legítimas, cuáles son el target y cuál es fuga — y por qué.

---

### Sección 3 · Entrena el modelo (pipeline)

🎯 **Objetivo:** Armar y entrenar un `Pipeline` que encapsula preprocesamiento + clasificador.

💡 **Concepto clave:** El pipeline es el "procedimiento estándar" del modelo: define en un solo objeto cómo se transforman los datos y cómo se predice. Además de orden, da **seguridad**: como el preprocesamiento se ajusta solo con datos de entrenamiento, el pipeline evita fugas silenciosas en esa etapa. Es la diferencia entre un trámite con protocolo escrito y uno que "cada funcionario hace a su manera".

🔍 **Qué hace el código:**

```python
pre = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), ["categoria", "region_comprador"])],
    remainder="passthrough")
```

- `ColumnTransformer` aplica transformaciones distintas según la columna
- `OneHotEncoder` convierte las categóricas (12 categorías + 15 regiones) en columnas de 0/1 — tras esta expansión, el modelo trabaja con 29 features
- `handle_unknown="ignore"` evita que el modelo se caiga si en el test aparece una categoría nueva
- `remainder="passthrough"` deja pasar las numéricas (`cantidad`, `monto_total`) sin tocarlas

Luego el pipeline une preprocesador y clasificador (`LogisticRegression(max_iter=1000)`) y se entrena con `.fit(Xtr, ytr)` — solo con datos de entrenamiento.

⚠️ **Error frecuente:** Entrenar con `X` completo en vez de `Xtr`. Si el modelo ve los datos de test durante el entrenamiento, la evaluación posterior queda contaminada y el F1 que reportes será una ilusión.

✅ **Sabes esta sección cuando puedes:** Explicarle a un colega qué hace cada pieza del pipeline y por qué las categóricas necesitan one-hot antes de entrar a una regresión logística.

---

### Sección 4 · Evalúa honestamente

🎯 **Objetivo:** Medir el desempeño en el conjunto de **prueba** con una métrica adecuada al desbalance.

💡 **Concepto clave:** Con solo 2,4% de positivos, un "modelo" que responda siempre "No es Grande" acierta el 97,6% de las veces — accuracy altísima, utilidad nula. Por eso el capstone exige **F1-score**, que combina precisión (de los que marqué como Grande, ¿cuántos lo eran?) y recall (de los Grande reales, ¿cuántos encontré?). Es la métrica que le importa a quien fiscaliza: no sirve un detector que nunca detecta.

🔍 **Qué hace el código:**

```python
pred = modelo.predict(Xte)
f1 = f1_score(yte, pred, zero_division=0)
```

- `modelo.predict(Xte)` genera predicciones sobre las 2.224 filas que el modelo **nunca vio**
- `f1_score(yte, pred, ...)` compara predicción contra realidad
- `zero_division=0` evita errores si el modelo no predice ningún positivo
- Con la solución de referencia, la regresión logística logra un F1 cercano a **0,44** en test — modesto, y eso es parte de la lección

⚠️ **Error frecuente:** Frustrarse por un F1 "bajo" y sentir que fallaste. Un F1 de 0,44 con 2,4% de positivos es un resultado honesto y reportable; un F1 de 0,99 en este problema debería hacerte sospechar de una fuga, no celebrar. En el `profundiza` verás que un árbol de decisión con validación cruzada llega bastante más arriba — comparar modelos es justamente trabajo de científico de datos.

✅ **Sabes esta sección cuando puedes:** Explicar por qué el F1 se calcula sobre `yte` (test) y qué significaría calcularlo sobre `ytr` (entrenamiento).

---

### Sección 5 · Model card (ficha del modelo)

🎯 **Objetivo:** Completar la ficha que acompaña al modelo cuando lo entregas.

💡 **Concepto clave:** La model card es al modelo lo que la ficha técnica es a un medicamento: dice para qué sirve, en qué dosis, y cuáles son las contraindicaciones. En el Estado, donde un modelo puede afectar derechos de personas, entregarlo sin ficha es negligencia profesional.

🔍 **Estructura de la model card del notebook:**

| Campo | Qué escribes |
|---|---|
| **Nombre / versión** | p. ej. `clasificador-proveedor-grande v1` |
| **Objetivo y uso previsto** | Qué decide y quién lo usa |
| **Datos de entrenamiento** | Fuente, features usadas (cantidad, monto, categoría, región) |
| **Métrica y desempeño** | F1 en test y % de la clase positiva (≈ 2,4% en el ejemplo) |
| **Limitaciones y sesgos** | Grupos donde rinde peor; qué NO predice |
| **Riesgos / uso responsable** | p. ej. no usar para decisiones punitivas automáticas; siempre con revisión humana |

⚠️ **Error frecuente:** Llenar "Limitaciones" con generalidades ("todo modelo tiene limitaciones"). Sé concreto: *el modelo se entrenó con compras de alimentos; nada garantiza que funcione en otras categorías de compra. Con solo 178 casos positivos, el desempeño por región individual no es confiable.*

✅ **Sabes esta sección cuando puedes:** Entregarle la model card a alguien que no programó el modelo y que esa persona sepa si puede usarlo para su caso — o no.

---

## 6. Guía de los 3 Ejercicios del Notebook

---

### Ejercicio 1 · Define X, y y la partición — sin fuga

**Objetivo:** Definir la lista `FEATURES` con variables honestas (sin `tamano_num` ni `tamano_proveedor`).

**Habilidad que entrena:** Detectar y excluir fugas de datos antes de entrenar — la habilidad más valiosa de R2-07.

**Pistas progresivas:**

- 🟢 **Pista suave:** El dataset tiene 6 columnas. Dos de ellas hablan del tamaño del proveedor — y el tamaño es justamente lo que quieres predecir. ¿Cuántas columnas legítimas quedan?
- 🟡 **Pista media:** Las features honestas son las que describen la **orden de compra**, no al proveedor: cuánto se compró, por cuánto dinero, de qué categoría y desde qué región.
- 🔴 **Pista directa:** `FEATURES` es una lista de 4 strings con los nombres exactos de las columnas `cantidad`, `monto_total`, `categoria` y `region_comprador`, en ese espíritu (el orden no importa). Nada más.

**Lógica de la solución:** El target se construye desde `tamano_proveedor`, así que ni esa columna ni su gemela numérica `tamano_num` pueden ser features: el modelo estaría "leyendo la respuesta". Las otras cuatro columnas describen la transacción y estarían disponibles al momento de predecir.

**Qué significa el ✅:** La celda verifica que ni `tamano_num` ni `tamano_proveedor` estén en `FEATURES`. Si además la celda anterior imprimió `positivos: 2.4 %`, vas perfecto.

---

### Ejercicio 2 · Entrena un pipeline

**Objetivo:** Construir el objeto `modelo` como un `Pipeline` (preprocesador + regresión logística) ya entrenado.

**Habilidad que entrena:** Ensamblar pipelines reproducibles de scikit-learn (R2-08) con un clasificador (R2-06).

**Pistas progresivas:**

- 🟢 **Pista suave:** El preprocesador `pre` ya está creado en la celda. Te falta unirlo con un clasificador dentro de un `Pipeline` y llamar al método que entrena.
- 🟡 **Pista media:** Un `Pipeline` recibe una lista de pares `(nombre, objeto)`: primero el paso `pre`, después un paso con `LogisticRegression(max_iter=1000)`. Recuerda que `.fit()` recibe los datos de **entrenamiento**, no todos.
- 🔴 **Pista directa:** Son dos pasos encadenables en una sola línea: crea el `Pipeline` con los pasos `("pre", pre)` y `("clf", LogisticRegression(max_iter=1000))`, y entrénalo con `Xtr` e `ytr` usando `.fit()`.

**Lógica de la solución:** El pipeline aplica primero el one-hot a las categóricas y deja pasar las numéricas; luego el clasificador aprende sobre esa matriz transformada. Como `.fit()` se llama sobre el pipeline completo, el preprocesamiento se ajusta solo con datos de entrenamiento — sin fuga.

**Qué significa el ✅:** La celda verifica que `modelo` exista y tenga el método `.predict` — es decir, que sea un estimador entrenado y funcional.

---

### Ejercicio 3 · Calcula el F1 en test

**Objetivo:** Obtener la variable `f1` con el F1-score del modelo sobre el conjunto de prueba.

**Habilidad que entrena:** Evaluar con la métrica correcta para clases desbalanceadas (R2-07).

**Pistas progresivas:**

- 🟢 **Pista suave:** Ya tienes `pred` (las predicciones sobre el test) y `yte` (la verdad). Falta la función de `sklearn.metrics` que compara ambas y que ya está importada arriba.
- 🟡 **Pista media:** La función recibe primero los valores reales, después las predicciones. Agrégale el argumento `zero_division=0` para que no falle si no hay positivos predichos.
- 🔴 **Pista directa:** Llama a `f1_score` con `yte` y `pred` como argumentos posicionales (en ese orden) y `zero_division=0` como argumento con nombre; asigna el resultado a `f1`.

**Lógica de la solución:** El F1 es la media armónica de precisión y recall sobre la clase positiva. Calculado sobre test, estima cómo se comportaría el modelo con órdenes de compra nuevas. Con este dataset y esta semilla, deberías ver un valor cercano a **0,44** — anótalo, porque va directo a tu model card.

**Qué significa el ✅:** La celda verifica que `f1` sea un número entre 0 y 1, es decir, que calculaste una métrica válida (el chequeo no exige un valor mínimo: la honestidad importa más que el puntaje).

---

## 7. Sección especial: el modelo como decisión de política pública

Un modelo predictivo en el Estado nunca es solo técnica. Antes de dar por cerrado tu capstone, trabaja estas reflexiones:

### Reflexión guiada sobre el ejemplo de compras

1. **¿Qué pasaría si este modelo se usara para adjudicar en vez de para entender?** Si alguien lo usara para filtrar proveedores automáticamente, un error dejaría fuera a una pyme legítima. El mismo modelo, otro uso, otro nivel de riesgo — por eso la model card fija el **uso previsto**.
2. **¿A quién perjudica un falso positivo y a quién un falso negativo?** Marcar como "Grande" a un proveedor pequeño no pesa lo mismo que lo contrario. La métrica que optimizas es una decisión de política, no solo de estadística.
3. **¿El dato histórico arrastra sesgos?** Si históricamente las regiones extremas compran menos a grandes proveedores, el modelo aprenderá ese patrón. ¿Realidad del mercado o desigualdad que no quieres perpetuar? El dato solo no lo dice.

### Datos que complementarían el análisis

Padrón de proveedores por región (¿la concentración refleja oferta disponible?), historial de cumplimiento de contratos (¿los grandes cumplen mejor, o solo ganan más?) y licitaciones desiertas (demanda no satisfecha que el modelo no ve).

### Pregunta de debate

> Tu modelo alcanza F1 ≈ 0,44 detectando proveedores grandes. La jefatura pregunta: *"¿Lo ponemos en producción para priorizar revisiones?"* ¿Qué necesitas responder antes de decir que sí — sobre la métrica, sobre los sesgos y sobre quién revisa las alertas? ¿Hay algún escenario en que la respuesta correcta sea "este problema no necesita un modelo"?

---

## 8. Rúbrica de evaluación — cómo interpretar cada criterio

El notebook cierra con una rúbrica de 5 criterios. Así se lee cada uno:

| Criterio | ✅ Cumple | ❌ No cumple |
|---|---|---|
| **Framing** | El problema y el uso del modelo están planteados en una frase clara: qué predice, quién lo usa, qué decisión apoya | "Quería probar ML" o un objetivo que nadie usaría para decidir |
| **Calidad del dato** | Features razonables y disponibles al momento de predecir; dataset entendido (desbalance incluido) | Features elegidas al azar o sin justificación |
| **Evaluación honesta** | Sin fuga de datos; F1 (no accuracy) por el desbalance; medido en test | `tamano_num` entre las features, o métricas calculadas sobre entrenamiento |
| **Model card** | Documenta datos, desempeño con cifras, límites concretos y condiciones de uso responsable | Campos vacíos o llenos de generalidades |
| **Reproducibilidad** | `Runtime > Run all` corre de principio a fin sin errores y las 3 celdas de chequeo muestran ✅ | Celdas que fallan o requieren intervención manual |

> **Entregable completo:** notebook reproducible + modelo entrenado + model card + informe de validación.

---

## 9. Conexión con `profundiza.ipynb`

| Aspecto | `leccion.ipynb` | `profundiza.ipynb` 🔬 |
|---|---|---|
| **Enfoque** | Ciclo completo: framing → features → pipeline → F1 → model card | Robustez: validación cruzada e importancia de variables |
| **Modelo** | Regresión logística | Árbol de decisión (`max_depth=6`) |
| **Ejercicios** | 3 con chequeo automático | 2 con chequeo automático |
| **Obligatorio** | ✅ Sí — es el entregable del capstone | ☐ Opcional, muy recomendado |

En el `profundiza` descubrirás dos cosas valiosas: que un solo split puede engañar (el 5-fold CV entrega cinco mediciones de F1 en vez de una — con el árbol, la media ronda 0,90) y que `feature_importances_` revela **qué variables pesan más**. Ambas van derecho a fortalecer tu model card y tu informe de validación.

---

## 10. Autoevaluación Final

Responde estas preguntas antes de dar por terminado el capstone:

**1. ¿Por qué `tamano_num` no puede estar en `FEATURES`?**

- a) Porque es una columna numérica y el modelo solo acepta texto
- b) Porque codifica el target: usarla es fuga de datos ✅
- c) Porque tiene valores nulos
- d) Porque scikit-learn no admite más de 4 features

*Respuesta correcta: b) — `tamano_num` es el tamaño del proveedor en números (Grande=4). Es la respuesta disfrazada: el modelo "acertaría" en el notebook y fracasaría en la realidad, donde ese dato no existe antes de la predicción.*

---

**2. Con solo 2,4% de casos positivos, ¿por qué el F1 es mejor métrica que el accuracy?**

- a) Porque el F1 siempre da valores más altos
- b) Porque el accuracy no funciona con variables categóricas
- c) Porque un modelo que nunca predice la clase positiva logra ~97,6% de accuracy sin detectar nada ✅
- d) Porque el F1 es más rápido de calcular

*Respuesta correcta: c) — Con clases desbalanceadas, el accuracy premia al modelo inútil que siempre dice "No". El F1 obliga a rendir en la clase que importa: precisión y recall sobre los positivos.*

---

**3. ¿Qué garantiza `stratify=y` en el `train_test_split`?**

- a) Que el test tenga exactamente 42 filas positivas
- b) Que la proporción de positivos (≈ 2,4%) sea la misma en train y test ✅
- c) Que las filas queden ordenadas por monto
- d) Que no haya duplicados en el test

*Respuesta correcta: b) — Sin estratificar, con una clase tan escasa el azar podría dejar casi todos los positivos en un solo conjunto, y la evaluación perdería sentido.*

---

**4. ¿Por qué entrenar dentro de un `Pipeline` ayuda a evitar fugas?**

- a) Porque el pipeline elimina automáticamente las columnas sospechosas
- b) Porque el preprocesamiento se ajusta solo con datos de entrenamiento cuando haces `.fit(Xtr, ytr)` ✅
- c) Porque el pipeline encripta los datos
- d) Porque impide usar más de un modelo a la vez

*Respuesta correcta: b) — Si transformaras los datos completos antes de separar train/test, información del test se filtraría al entrenamiento. El pipeline aplica cada transformación en el momento correcto, con los datos correctos.*

---

**5. ¿Cuál es el propósito principal de la model card?**

- a) Demostrar cuánto código sabes escribir
- b) Reemplazar el notebook como entregable técnico
- c) Documentar qué hace el modelo, cómo rinde, sus límites y las condiciones de uso responsable ✅
- d) Registrar los hiperparámetros para reproducir el entrenamiento

*Respuesta correcta: c) — La model card es el contrato entre quien construye el modelo y quien lo usa. Sin ella, alguien podría aplicar el modelo fuera de su ámbito y tomar decisiones injustas con toda confianza.*

---

## 11. Glosario del Módulo

| Término técnico | Definición simple | Equivalente en tu trabajo |
|---|---|---|
| **Fuga de datos (leakage)** | Incluir en las features información que contiene la respuesta | Calificar un concurso mirando el acta de adjudicación |
| **Target (y)** | La variable que el modelo aprende a predecir | La casilla del formulario que quieres anticipar |
| **Feature (X)** | Variable de entrada que el modelo usa para predecir | Los antecedentes disponibles antes de resolver |
| **`train_test_split`** | Separa los datos en entrenamiento y prueba | Guardar expedientes bajo llave para auditar después |
| **`stratify`** | Mantiene la proporción de clases en ambos conjuntos | Una muestra que respeta la composición del universo |
| **Desbalance de clases** | La clase de interés es muy minoritaria (aquí 2,4%) | Buscar las pocas licitaciones irregulares entre miles correctas |
| **`OneHotEncoder`** | Convierte categorías en columnas de 0/1 | Transformar "Región" en 15 casillas de sí/no |
| **`Pipeline`** | Encadena preprocesamiento y modelo en un solo objeto | Un protocolo escrito que todos ejecutan igual |
| **F1-score** | Media armónica de precisión y recall sobre la clase positiva | Qué tan bien detectas los casos que importan, sin inflar alertas |
| **Validación cruzada** | Evaluar con varios splits en vez de uno | Pedir cinco contramuestras antes de firmar el informe |
| **Model card** | Ficha del modelo: objetivo, datos, desempeño, límites, uso responsable | La ficha técnica que acompaña a un medicamento |
| **Uso responsable** | Condiciones bajo las cuales el modelo puede (y no puede) usarse | El reglamento de uso de un sistema institucional |

---

## 12. Has llegado al final de la Rama R2 🎓

Si completaste este capstone con las 3 celdas en ✅, una model card honesta y un notebook que corre de punta a punta, demostraste algo que pocos funcionarios pueden mostrar: **sabes construir un modelo predictivo responsable, de los datos a la ficha de entrega**.

### Certificación

Al aprobar el capstone según la rúbrica de 5 criterios, obtienes la **certificación de la rama R2 · Científico de Datos** de Formación Pública. No es un diploma de asistencia: certifica un proyecto real, evaluado, que cualquiera puede revisar.

### Tu portafolio es tu credencial

Sube tu capstone a GitHub (recuerda: **solo con datos anonimizados o con el dataset de ejemplo**). Un repositorio con tus capstones de R1 y R2 — notebooks reproducibles, model card, informe — vale más que cualquier línea en un currículum: es evidencia verificable, no promesa.

### ¿Qué sigue?

| Opción | Para quién | Qué encontrarás |
|---|---|---|
| **Rama R3 · IA Aplicada** | Quieres llevar modelos de lenguaje y IA generativa a problemas de tu organismo | Prompting riguroso, RAG sobre documentos públicos, automatización responsable |
| **Comunidad Formación Pública** | Quieres seguir aprendiendo con otros funcionarios | Comparte tu capstone, revisa los de otros, encuentra colaboradores en otros servicios |
| **Consolidar R2** | Quieres afianzar antes de seguir | Repite el capstone con otro problema de tu institución: cada iteración te hace mejor |

**Pregunta motivadora para lo que sigue:** Ya sabes hacer que un modelo prediga a partir de datos estructurados. ¿Y si pudieras hacer que una IA lea los miles de documentos, oficios y resoluciones de tu servicio y te ayude a responder con esa evidencia? Eso es lo que construyes en la rama R3.

---

*Formación Pública Chile · Licencia CC BY 4.0*
