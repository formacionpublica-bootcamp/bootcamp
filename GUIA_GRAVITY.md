# Guía — Antigravity ("Gravity") como tu tutor de IA

**Bootcamp de Datos para Funcionarios Públicos · Formación Pública**

> **Antigravity es opcional.** Todo el bootcamp se puede completar solo con Google Colab —
> ningún ejercicio, chequeo ni certificado requiere instalar nada. Esta guía es para quienes
> quieran un nivel extra de ayuda: un asistente de IA que ve **todo el material del curso** y
> responde tus dudas en modo tutor, disponible 24/7.

---

## 1. ¿Qué es y para qué lo usarás?

**Google Antigravity** (le decimos "Gravity") es el IDE gratuito de Google con un agente de IA
integrado (Gemini). En este curso lo usamos para **una** cosa: como **canal de dudas y
consultas**. Le cargas la carpeta del bootcamp, activas el *modo tutor*, y le preguntas lo que
sea: qué hace una celda, por qué tu código da error, o pistas para un ejercicio trabado.

Tu escalera de ayuda completa, en orden:

| Nivel | Dónde | Cuándo usarlo |
|---|---|---|
| 0 | `GUIA_APRENDIZAJE.md` del módulo | Siempre primero: tiene pistas y los errores frecuentes |
| 1 | Gemini dentro de Colab (botón ✨) | Dudas rápidas sobre la celda que estás mirando |
| **2** | **Gravity en modo tutor (esta guía)** | Dudas de fondo, ejercicios trabados, tu capstone |
| 3 | Sesión semanal en vivo + comunidad | Lo que la IA no destrabó, y para no avanzar en solitario |

**¿Cuándo conviene dar el salto a Gravity?** Cuando llegues al capstone (proyecto con datos de
tu organismo) o cuando notes que tus dudas son de comprensión ("¿por qué se hace así?") y no
solo de sintaxis. Si estás en los primeros módulos y Colab te basta, quédate en Colab.

## 2. Requisitos

- Un computador donde **puedas instalar programas** (si tu equipo institucional no lo permite,
  usa tu computador personal — o simplemente sigue con el nivel 1, que no requiere nada).
- Tu **cuenta de Google** (la misma que usas para Colab).
- Conexión a internet.

## 3. Instalación (una sola vez, ~10 minutos)

1. Entra a **https://antigravity.google** y descarga el instalador para tu sistema
   (Windows, Mac o Linux).
2. Instala y abre la aplicación.
3. **Inicia sesión con tu cuenta de Google** cuando te lo pida. El plan gratuito basta para
   este curso.
4. Descarga el material del bootcamp (elige una):
   - **Sin git (recomendado si recién empiezas):** entra a
     https://github.com/formacionpublica-bootcamp/bootcamp → botón verde **Code** →
     **Download ZIP** → descomprime en una carpeta que encuentres fácil (p. ej. `Documentos/bootcamp`).
   - **Con git:** `git clone https://github.com/formacionpublica-bootcamp/bootcamp.git`
5. En Antigravity: **abrir carpeta** → selecciona la carpeta `bootcamp` que descargaste.

## 4. Activar el modo tutor (el paso que importa)

El agente de IA por defecto está hecho para **resolver** — y un tutor que resuelve por ti mata
tu aprendizaje. Por eso el repo incluye [TUTOR_IA.md](TUTOR_IA.md), que lo convierte en tutor.

Abre el panel del agente y escribe **como primer mensaje de cada sesión**:

```
Lee el archivo TUTOR_IA.md de la raíz del repositorio y compórtate según
sus reglas durante toda esta sesión. Estoy en el módulo [R1-04] del curso.
```

(Cambia `[R1-04]` por el módulo en que vas.) Si tu IDE soporta archivos de reglas del agente
(p. ej. `AGENTS.md` o las *rules* del workspace), puedes copiar ahí el contenido de
`TUTOR_IA.md` para no repetir este paso.

**Sabrás que funcionó** porque ante un ejercicio te dará pistas (🟢 → 🟡 → 🔴) en vez de
pegarte el código resuelto.

## 5. Cómo preguntar bien (ejemplos reales)

- ❌ "no me funciona" → ✅ *"Estoy en el ejercicio 2 de R1-04. Mi celda da
  `KeyError: 'monto_total'`. Aquí está mi código: […] ¿Qué significa ese error?"*
- ✅ *"Explícame con una analogía de Excel qué hace `groupby` en la sección 3 de R1-03."*
- ✅ *"Ya intenté el ejercicio 3 dos veces y el chequeo sigue en ❌. No me des el código:
  dame una pista de qué estoy entendiendo mal."*
- ✅ (capstone) *"Quiero responder si mi servicio compra más caro que el promedio de la región.
  ¿Qué estructura de análisis me propones con lo que aprendí en R1?"*

Regla del curso: **Read → Ask AI → Ask Community.** Primero la guía del módulo, después la IA,
y lo que no se destrabe, a la comunidad o a la sesión semanal.

## 6. Privacidad: la regla que no se negocia

- **Nunca pegues en la IA datos personales o sensibles**: RUT con nombres, fichas de
  beneficiarios, datos de salud, documentos internos no públicos. Vale para Gravity, Gemini,
  ChatGPT y cualquier servicio.
- Los datos del curso (MINEDUC, SINCA, ChileAtiende, USGS…) son públicos: úsalos con libertad.
- Para el **capstone** con datos de tu organismo: anonimiza primero (quita nombres y RUT,
  reemplaza por códigos). El modo tutor está instruido para frenarte si lo olvidas — no
  dependas de eso.

## 7. Si algo falla

| Problema | Solución |
|---|---|
| No puedo instalar (equipo institucional bloqueado) | Usa tu computador personal, o quédate con Gemini en Colab (nivel 1) — el curso completo funciona así |
| La red de mi institución bloquea la app | Igual que arriba; y avísanos en la comunidad para documentarlo |
| El agente me da el código resuelto | Se te olvidó activar el modo tutor (sección 4), o empezaste sesión nueva sin repetirlo |
| El agente inventa cosas del curso | Pídele que cite el archivo del repo en que se basa; si no puede, confía en la `GUIA_APRENDIZAJE.md` del módulo |
| Dudas de la herramienta misma | Tráelas a la sesión semanal |

---

*Formación Pública · CC BY 4.0 · Antigravity es un producto de Google; sus términos y plan
gratuito pueden cambiar — esta guía se reverifica antes de cada cohorte.*
