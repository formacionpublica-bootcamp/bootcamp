# Cómo desarrollaría el bootcamp — Formación Pública

> Blueprint de diseño para un bootcamp **gratuito, independiente y autoguiado** de datos para
> funcionarios públicos chilenos con **cero código**, enfocado en **upskilling** (mejorar en el
> puesto), no en reconversión de carrera. Toma como referencia de **estructura** el ONS Data
> Science Campus (UK) y como referencia de **contenido práctico** a 4Geeks y similares.
>
> Este documento NO reemplaza al diseño actual: propone cómo lo reorganizaría aprovechando casi
> todo lo que ya está construido (M0–M17).

---

## 0. El problema a resolver (por qué reorganizar)

El programa actual está muy bien hecho, pero tiene una **contradicción de fondo**: dice
"upskilling, no cambio de carrera", pero el perfil de salida es *Data Scientist capaz de modelar,
desplegar, monitorear, RAG y agentes* — eso **es** un cambio de carrera. El resultado es un solo
itinerario de 16–21 semanas, en solitario, que sobre-promete y que el funcionario mediano no va a
terminar.

La solución no es recortar ambición: es **escalonarla por niveles de ambición** (como hace el ONS)
y ser **honesto con el estudiante** sobre qué le da cada nivel. Así el 90% obtiene lo que de verdad
necesita en pocas semanas, y el 10% que quiere más tiene a dónde seguir.

---

## 1. Cinco principios de diseño

1. **Escalonado por ambición, no monolítico.** Tres pistas independientes, cada una con su propio
   certificado y su propio capstone. Terminar la Pista A ya es un logro completo, no "ir a medias".
2. **Práctica primero (ADN 4Geeks).** Se aprende construyendo. Cada módulo termina en un
   entregable pequeño; cada pista termina en un proyecto con **datos de la propia institución del
   estudiante**. Menos teoría leída, más código escrito.
3. **Datos públicos reales como columna vertebral.** Compras públicas (ChileCompra/MercadoPúblico
   vía MCP) atraviesa todo, abriéndose a salud/presupuesto/educación cuando aporta variedad.
4. **Nativo-IA (esto es 2026).** No peleamos contra ChatGPT/Gemini: enseñamos a usarlos como
   copiloto y **evaluamos comprensión y aplicación**, no coincidencia de output.
5. **Baja fricción y resiliente.** Google Colab (cero instalación), auto-chequeos amables, patrón
   "en vivo o caché" para que todo funcione sin red. (Esto ya lo tienes y es excelente — se queda.)

---

## 2. La decisión estructural: 3 pistas escalonadas

| Pista | Nombre | Para quién | Duración realista | Qué logra (honesto) |
|---|---|---|---|---|
| **A** | **Datos sin miedo** (alfabetización) | **Todos** los funcionarios. El producto estrella. | ~6 sem · 4–5 h/sem | Responder preguntas con datos reales, limpiar tablas sin sufrir Excel, consultar con SQL, hacer un gráfico honesto, usar IA con criterio. **Esto es el upskilling.** |
| **B** | **Ciencia de datos aplicada** (practitioner, opcional) | Quien quedó enganchado y quiere modelar. | ~6 sem · 6–8 h/sem | Plantear y entrenar modelos de ML, evaluarlos con honestidad, armar pipelines reproducibles. *Aquí se dice claro: esto ya es un paso hacia un rol nuevo.* |
| **C** | **IA aplicada al Estado** (opcional, muy actual) | Quien quiere construir con IA generativa. | ~5 sem · 6–8 h/sem | Resolver tareas de texto con LLMs, dar a un LLM tus propios documentos (RAG) y encadenar agentes. |

**Prework de programación (M0–M2)**: comprimido y enmarcado como "lo mínimo de Python para
sobrevivir", no como un curso de CS. La meta es llegar **rápido a pandas y SQL**, que son la
habilidad del puesto.

Regla de oro de honestidad: en la portada de cada pista se dice **qué te llevas y qué NO**. La
Pista A no te convierte en data scientist, y está perfecto: te convierte en alguien que ya no le
teme a los datos.

---

## 3. Cómo reusar lo que ya construiste (no se bota casi nada)

| Módulo actual | Destino propuesto | Acción |
|---|---|---|
| M0 Setup/sintaxis | Prework | **Reusar**, comprimir |
| M1 Colecciones y bucles | Prework | **Reusar**, comprimir |
| M2 Funciones y archivos | Prework | **Reusar**, comprimir |
| M2b JSON y APIs | Prework (opcional) | **Reusar**, marcar opcional |
| M3 Exploración con pandas | **Pista A** | **Reusar tal cual** (núcleo) |
| M4 Limpieza de datos | **Pista A** | **Reusar tal cual** (núcleo) |
| M5 SQL fundamentos | **Pista A** | **Reusar tal cual** (núcleo) |
| M6 Estadística descriptiva | **Pista A** | **Reusar**, enfatizar "no dejarse engañar" |
| M7 Visualización y ética | **Pista A** | **Reusar tal cual** (núcleo) |
| D16 IA generativa y LLMs | **Pista A** (cierre) + Pista C | **Adelantar**: traerlo a A como alfabetización de IA |
| D8 SQL para features | **Pista B** | Reusar |
| D9 Fundamentos de ML | **Pista B** | Reusar (ver nota dato abajo) |
| D10 Modelos de árboles | **Pista B** | Reusar |
| D11 Clasificación y clustering | **Pista B** | Reusar |
| D12 Pipelines reproducibles | **Pista B** | Reusar |
| D13 Despliegue de modelos | **Pista B** | **De-escalar a conceptual** (awareness, no "competencia: desplegar") |
| D14 Series temporales | **Pista B o C** | Reusar |
| D15 NLP | **Pista C** | Reusar |
| D17 RAG | **Pista C** | Reusar |
| D18 Agentes | **Pista C** | Reusar |

**Nota sobre D9:** hoy usa latitud→temperatura (18 ciudades). Es limpio, pero rompe la columna de
compras públicas y roza el "dataset de juguete" que tu propia guía prohíbe. Recomiendo migrar el
primer ML a una pregunta de compras públicas (ej. predecir monto adjudicado a partir de
características de la licitación) para mantener coherencia.

Cambios netos: **0 módulos botados**, 1 de-escalado (D13), 1 adelantado (D16). El grueso del
trabajo de construcción ya hecho se conserva; solo cambia el **empaque y el orden**.

---

## 4. Pista A en detalle (el producto estrella, semana a semana)

Cada semana = 1 concepto + práctica guiada + 1 mini-entregable real. Tono y plantilla de M0.

| Sem | Tema | Mini-entregable (datos reales) |
|---|---|---|
| 0 | **Prework express**: notebook, variables, tipos, condicionales (M0–M2 condensado) | "Mi primer programa": calcular y mostrar una cifra del gasto público |
| 1 | **pandas para explorar** (M3): abrir una tabla, filtrar, ordenar, agrupar | Top 10 organismos por gasto 2025, en 5 líneas |
| 2 | **Limpieza** (M4): nulos, duplicados, tipos, RUTs, montos | Tomar un CSV sucio real y dejarlo usable |
| 3 | **SQL** (M5): SELECT/WHERE/GROUP BY sobre los mismos datos | Responder 3 preguntas con consultas, no con Excel |
| 4 | **Estadística para no engañarse** (M6): promedio vs mediana, outliers, % engañosos | Desmentir o confirmar un titular con los datos |
| 5 | **Visualización honesta + ética** (M7): el gráfico correcto, ejes que no mienten | Un gráfico claro que tu jefatura entendería |
| 6 | **IA como copiloto** (D16 adelantado): pedirle análisis, clasificar y extraer texto con criterio y privacidad | Clasificar 50 glosas de compra con un LLM, verificando |
| **Capstone A** | **Tu pregunta, tus datos** | Responder una pregunta real de **tu propia institución** con una tabla limpia + 1 gráfico + 1 párrafo de conclusión |

Resultado de la Pista A: un funcionario que **reemplaza un reporte manual por una consulta**, hace
un gráfico que no miente y usa IA sin meter la pata con datos personales. Ese es el upskilling que
prometiste, y es alcanzable.

---

## 5. Pistas B y C (esquema)

**Pista B · Ciencia de datos aplicada** (reusa D8–D14)
1. SQL para *features* (D8) · 2. Fundamentos de ML, train/test, sobreajuste (D9) · 3. Árboles (D10)
· 4. Clasificación y clustering (D11) · 5. Pipelines reproducibles (D12) · 6. *Awareness* de
despliegue + monitoreo (D13 conceptual) o Series temporales (D14).
**Capstone B:** un proyecto predictivo de punta a punta sobre datos públicos, con evaluación honesta.

**Pista C · IA aplicada al Estado** (reusa D15–D18)
1. NLP básico (D15) · 2. LLMs para tareas de gobierno (repaso/profundización D16) · 3. RAG sobre
tus documentos (D17) · 4. Agentes (D18) · 5. Proyecto integrador.
**Capstone C:** un asistente que responde sobre normativa/fichas de compra **citando la fuente**, o
un agente que automatiza una tarea repetitiva del Estado.

---

## 6. ADN práctico: qué tomar de 4Geeks (y cómo)

Tu foco está en el mejor contenido práctico. Esto es lo que vale la pena copiar de esa escuela:

- **Aprender construyendo, no leyendo.** Ratio sugerido por módulo: ≤30% teoría, ≥70% manos. Ya
  tienes 4 ejercicios auto-corregidos por módulo; mantenlo y asegúrate de que cada uno produzca
  algo *visible* (un número, una tabla, un gráfico).
- **Proyecto al final de cada nivel**, no solo ejercicios sueltos. El portafolio en GitHub es la
  credencial real (más que el certificado, dado que no hay institución que lo respalde).
- **Read–Search–Ask (la regla de oro 4Geeks para destrancarse).** Sin mentor presencial, hay que
  enseñar **auto-rescate**: cómo leer un error, cómo buscar, cómo preguntarle bien a la IA. Un
  módulo corto de "cómo me destranco solo" al inicio sube la completitud más que cualquier teoría.
- **Repetición espaciada.** Conceptos clave (filtrar, agrupar, unir tablas) reaparecen en módulos
  posteriores con datos distintos. No se enseña una vez y se abandona.
- **Dificultad en rampa, sin acantilados.** Mete un **módulo-puente a pandas** entre el prework y
  M3 (es el muro clásico), y otro entre estadística (M6/A) y ML (D9/B).

---

## 7. Evaluación y capstone en la era de la IA

El chequeo por `assert` es bueno para *feedback inmediato*, pero es **gameable** (se acierta por
tanteo o copiando de un LLM) y no mide comprensión. Diseño de evaluación en dos capas:

- **Capa formativa (automática, ya la tienes):** los `assert` amables, para que el estudiante sepa
  al instante si va bien. Se queda.
- **Capa sumativa (capstone por pista):** un proyecto aplicado a **datos de la propia institución**
  del estudiante, con **rúbrica pública**. Componentes anti-IA:
  - **Aplicación a un problema propio** (la IA no conoce tu repartición ni tu dato).
  - **Reflexión escrita**: "explica con tus palabras por qué elegiste este gráfico / esta métrica".
  - **Defensa breve** (en cohorte: 5 min; self-serve: video Loom de 3 min).
- **Credencial:** certificado auto-emitido por pista **+ portafolio público en GitHub Pages**. Sin
  institución, el portafolio *es* la prueba de habilidad — vale más que un PDF.

Rúbrica mínima de capstone (0–3 cada uno): pregunta clara · datos correctamente tratados ·
análisis válido · visual honesta · conclusión accionable · reflexión. Aprobado ≥ 12/18.

---

## 8. Mecánica de completitud (sin institución detrás)

Este es el verdadero riesgo. Un MOOC autoguiado completa 5–15%. Palancas, de mayor a menor impacto,
que **no** requieren respaldo institucional:

1. **Cohortes ligeras con fecha de inicio.** Una fecha de partida y un ritmo común multiplican la
   completitud vs. "siempre abierto". Pueden ser asíncronas (no necesitas clases en vivo).
2. **Comunidad** (Discord/WhatsApp/Slack). Un canal donde preguntar y ver a otros avanzando.
   El sentido de "no estoy solo" es el factor #1 de retención en cursos gratuitos.
3. **(Opcional) 1 hora en vivo a la semana.** Mencionaste evaluarlo: con 1 sesión semanal de
   dudas/avances la completitud sube fuerte y el costo es bajo. Recomiendo probarlo en la **primera
   cohorte piloto** y medir.
4. **Hitos visibles y rachas.** Barra de progreso, "X/6 módulos", badge al terminar cada pista,
   compartir el logro. Pequeño pero funciona.
5. **Entregable propio temprano.** Que en la semana 1 ya produzcan algo útil con datos de *su*
   trabajo. La utilidad inmediata retiene mejor que la promesa de un certificado lejano.

Recomendación: **no lances "siempre abierto" como producto principal.** Lanza una **cohorte piloto
de ~30 personas, una sola pista (A), con comunidad y la sesión semanal opcional**, y mide todo.

---

## 9. Cómo medir el éxito (KPIs)

No midas solo inscritos. Mide:

- **Completitud por pista** (meta piloto Pista A: >40% con cohorte+comunidad).
- **Tiempo real a completar** vs. estimado (ajusta la carga semanal con esto).
- **Punto de abandono** (qué módulo bota gente → ahí va un puente).
- **Impacto en el puesto (el que importa):** encuesta simple post-curso — *"¿aplicaste algo en tu
  trabajo?"* con ejemplos: "reemplacé un reporte Excel por una query", "armé un gráfico que mi
  equipo usa". Esto, además, es tu mejor marketing y lo que algún día te consigue un aliado.

---

## 10. Mantención y riesgos (un curso gratis que se rompe, mata la confianza)

- **Dueño de mantención + CI.** Un script/acción que re-ejecute los notebooks periódicamente y
  avise si algo falla. Las dependencias rotan (versiones de librerías, API de Gemini, MCP de
  ChileCompra).
- **Riesgos externos:** el tier gratuito de Gemini y el MCP de ChileCompra pueden cambiar. El
  patrón "en vivo o caché" ya te protege parcialmente — mantenlo en todo módulo con red.
- **Accesibilidad:** Colab + cuenta Google es buena decisión; deja documentado un plan B por si una
  red institucional bloquea Colab.

---

## 11. Roadmap de construcción (dado lo ya hecho)

> **Estado:** ✅ M18 (Agentes) extraído y colocado en la Pista C. ✅ Reempaquetado aplicado de
> forma no destructiva en el índice raíz [README.md](README.md) (las carpetas M0–M18 no se movieron,
> para no romper los enlaces Open-in-Colab ni el sync con Notion).

1. **Reempaquetar, no reconstruir.** ✅ Hecho vía índice raíz. Reagrupa M0–M18 en las 3 pistas
   (sección 3). Pendiente: ajustar las portadas internas de cada módulo (qué te llevas / qué no por
   pista) — por ahora solo M18 quedó alineado.
2. **Construir lo que falta de la Pista A:** módulo "cómo me destranco solo" (Read–Search–Ask) +
   módulo-puente a pandas + **Capstone A con rúbrica**. Adelantar D16 a la Pista A.
3. **Corregir D9** para que use compras públicas (coherencia de columna vertebral).
4. **Cerrar Pistas B y C:** de-escalar D13 a conceptual; construir capstones B y C; terminar
   D18/PF si falta.
5. **Montar la mecánica de cohorte:** página de entrada (GitHub Pages o Notion público), formulario
   de inscripción, canal de comunidad, calendario.
6. **Piloto Pista A** (~30 personas) → medir KPIs (sección 9) → iterar antes de abrir B y C.

---

*Resumen en una línea: mismo gran contenido que ya tienes, reordenado en 3 niveles honestos, con
la práctica y el proyecto propio al centro, y la completitud diseñada a propósito. La Pista A sola
ya cumple la misión de upskilling; B y C son para quien quiera más.*

*Licencia sugerida: CC BY 4.0 · Formación Pública.*
