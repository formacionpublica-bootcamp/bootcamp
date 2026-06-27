# Prompt Maestro — Generación de Guías de Aprendizaje

> Archivo complementario al notebook de cada módulo.  
> Úsalo para generar la `GUIA_APRENDIZAJE.md` de cualquier módulo del bootcamp.

---

## Instrucciones de uso

1. Copia el bloque de prompt que aparece más abajo
2. Rellena los parámetros marcados con `[COMPLETAR]`
3. Pégalo en Claude, ChatGPT o Perplexity
4. Revisa el output y ajusta si es necesario
5. Guarda como `GUIA_APRENDIZAJE.md` en la carpeta del módulo correspondiente

---

## Prompt Maestro (versión parametrizable)

```
Actúa como un diseñador instruccional experto en formación para el sector público y en ciencia de datos aplicada.

Tu tarea es generar una **Guía de Aprendizaje completa** para el módulo [NOMBRE_MODULO] del Bootcamp de Datos para Funcionarios Públicos de Chile (Formación Pública).

---

### CONTEXTO DEL MÓDULO

**Nombre:** [NOMBRE_MODULO] (p.ej. R1-02 · Exploración con pandas)
**Rama:** [RAMA] (p.ej. R1 · Análisis y Visualización)
**Audiencia:** Funcionarios públicos chilenos sin experiencia previa en programación
**Modalidad:** Autoguiada, ejecutada en Google Colab
**Dataset real:** [NOMBRE_DATASET] — fuente: [FUENTE_DATASET]
**Competencia de salida:** [COMPETENCIA_DE_SALIDA]

**Contenidos del módulo:**
[LISTA_DE_SECCIONES_DEL_NOTEBOOK]

**Prerrequisitos:** [MODULOS_ANTERIORES]

---

### ESTRUCTURA OBLIGATORIA DE LA GUÍA

Genera la guía con las siguientes secciones, en ese orden:

**1. Portada y Datos del Módulo**
- Nombre del módulo, rama, duración estimada, nivel, prerrequisitos, competencia de salida

**2. ¿Para qué me sirve esto como funcionario público?**
- Explica la utilidad práctica en el contexto del trabajo del Estado chileno
- Conecta con el dataset real del módulo: ¿qué decisiones de política pública se pueden tomar?

**3. Mapa conceptual del módulo**
- Tabla Markdown con los conceptos clave y su analogía con Excel/trabajo del sector público

**4. Antes de empezar: Verificación de prerrequisitos**
- Lista de conocimientos previos requeridos
- Checklist: "¿Puedo...? Sí/No"

**5. Guía paso a paso por sección del notebook**
Para cada sección del `leccion.ipynb`, genera:
- 🎯 Objetivo de la sección
- 💡 Concepto clave con analogía del sector público
- 🔍 Qué hace el código (línea por línea, lenguaje simple)
- ⚠️ Error frecuente y cómo evitarlo
- ✅ Señal de comprensión: "Sabes esta sección cuando puedes..."

**6. Guía de los ejercicios**
Para cada ejercicio del notebook:
- Nombre y objetivo
- Habilidad que entrena
- Pistas progresivas (3 niveles: pista suave 🟢 → media 🟡 → directa 🔴)
- Lógica de la solución en prosa (sin revelar el código)
- Qué valida el chequeo automático ✅

**7. Sección especial: El ejercicio de política pública**
- Reflexión guiada sobre las implicancias de los resultados
- Pregunta de debate abierta
- Ejemplos de otros datos que complementarían el análisis

**8. Autoevaluación Final**
- 5 preguntas de opción múltiple (conceptuales, sin código)
- Respuesta correcta marcada con ✅
- Explicación de cada respuesta

**9. Glosario del Módulo**
- 10–12 términos clave, definición simple, equivalente en Excel/administración pública

**10. Conexión con el siguiente módulo**
- Resumen de lo que viene en [SIGUIENTE_MODULO]
- Una pregunta motivadora

---

### DATOS REALES DEL DATASET (para usar en ejemplos)

[DESCRIPCION_DEL_DATASET]
- Archivo: [NOMBRE_ARCHIVO.csv]
- Columnas: [LISTA_DE_COLUMNAS]
- Total de registros: [N]
- Distribución relevante: [STATS_CLAVE]
- Uso temático: [CONTEXTO_DE_POLÍTICA_PÚBLICA]

---

### LINEAMIENTOS DE ESTILO (OBLIGATORIOS)

- Tono: cercano, motivador, empático, orientado al impacto público. Sin elitismo técnico.
- Lenguaje: español neutro con giros del español chileno cuando sea pertinente.
- Formato: Markdown limpio, emojis funcionales, tablas y bloques de código cuando corresponda.
- Analogías: anclar conceptos técnicos en situaciones del trabajo del Estado (Excel, informes, licitaciones, registros de servicios).
- Nunca revelar directamente el código solución de los ejercicios; usar pistas progresivas.
- Extensión: guía completa, cada sección auto-contenida.

---

Genera ahora la guía completa siguiendo exactamente la estructura indicada.
```

---

## Parámetros de referencia — Módulos ya documentados

| Módulo | Dataset | Competencia de salida | Guía |
|--------|---------|----------------------|------|
| R1-02 · Exploración con pandas | Establecimientos SML (`establecimientos.csv`) | Cargar, inspeccionar y resumir un dataset con pandas | ✅ `GUIA_APRENDIZAJE.md` |
| R1-03 · Cruzar y resumir tablas | Por definir | Por definir | ⬜ Pendiente |
| R1-04 · Limpieza de datos | Por definir | Por definir | ⬜ Pendiente |
| R1-05 · SQL para análisis | Por definir | Por definir | ⬜ Pendiente |
| R1-06 · Estadística descriptiva | Por definir | Por definir | ⬜ Pendiente |
| R1-07 · Visualización exploratoria | Por definir | Por definir | ⬜ Pendiente |
| R1-08 · Visualización: comunicar y ética | Por definir | Por definir | ⬜ Pendiente |
| R1-09 · Dashboards ligeros | Por definir | Por definir | ⬜ Pendiente |

---

## Criterios de calidad de una buena guía

Antes de subir una guía al repositorio, verifica que:

- [ ] Todos los datos numéricos están verificados contra el dataset real
- [ ] Las pistas de ejercicios no revelan el código directamente
- [ ] Cada sección es auto-contenida (se entiende sin leer las otras)
- [ ] Las analogías conectan con el trabajo real del sector público chileno
- [ ] El glosario cubre todos los términos nuevos del módulo
- [ ] La autoevaluación tiene respuesta correcta y explicación
- [ ] La conexión con el siguiente módulo termina con una pregunta motivadora

---

*Documento de diseño instruccional — Formación Pública Chile · Licencia CC BY 4.0*
