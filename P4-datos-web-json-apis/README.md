# M2b · Datos desde la web: JSON y APIs

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Tronco común · *Derivado de M2 (Funciones y lectura de archivos)* · Fase Prework · Semana 3.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/P4-datos-web-json-apis/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

Es la continuación natural de **M2**: pasar de *"leer un archivo"* a *"pedir datos a la web"*. El
estudiante aprende qué es una **API** y qué es **JSON**, hace su primera llamada a una API pública
con Python, y navega la respuesta (diccionarios y listas, lo de M1) para extraer lo que necesita.
Cierra transformando el JSON en una lista de registros, lista para volverse tabla en M3.

Llena el hueco más claro detectado al comparar con 4Geeks: **adquisición de datos vía API**. Como es
del **tronco común**, lo reciben las dos líneas (Análisis y Ciencia de Datos).

**Competencia de salida:** entender API y JSON, pedir datos a una API pública con Python y navegar
la respuesta para extraer información.

## Dato real

API pública de **mindicador.cl** — indicadores del **Banco Central de Chile** (dólar, UF, UTM, IPC,
etc.) en JSON, sin clave ni registro. Son los mismos valores que usan los bancos y el SII.

## Detalle técnico importante (en vivo o caché)

El cuaderno define un ayudante `obtener_json(url)` que **intenta la llamada real** y, si no hay
internet, usa una **copia real de la respuesta** capturada el 2026-06-20. Así:
- En **Colab** el estudiante obtiene los valores **del día, en vivo**.
- La lección **nunca se cae** por falta de red, y es verificable en cualquier entorno.
- Los chequeos validan **estructura y relaciones** (no valores exactos, que cambian a diario), por lo
  que dan ✅ tanto con datos en vivo como con la copia.

## Cómo se usa

1. Abre `leccion.ipynb` con **Open in Colab**.
2. Ejecuta las celdas en orden y completa cada `TODO`.
3. Cada ejercicio termina en una **celda de chequeo** (✅ o pista). Logrado cuando las 4 dan ✅.

## Contenido

- `README.md` — esta portada.
- `leccion.ipynb` — cuaderno del estudiante (teoría + 4 ejercicios + celdas de chequeo).
- `solucion.ipynb` — cuaderno resuelto (uso interno).

## Los 4 ejercicios

1. **Pedir datos a la API** — `obtener_json(URL_INDICADORES)` → diccionario de indicadores.
2. **Navegar el JSON** — llegar a `datos["dolar"]["valor"]`.
3. **Extraer una serie** — obtener la lista `datos_dolar["serie"]`, contarla y tomar el último.
4. **De JSON a registros** — armar una lista de `(fecha, valor)` (puente a pandas/M3).

## Verificación de calidad

- Solución ejecutada (ruta caché, sin red): **4/4 ✅** (dólar $897,19; serie de 31 puntos; registros).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Lugar en el flujo

Derivado de **M2**, en el **Prework** del tronco común. No altera la numeración del resto: las líneas
A y B y el resto de los módulos mantienen sus códigos. El programa pasa de 21 a 22 módulos.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0?
- [ ] ¿Quedan claras las analogías de API (ventanilla) y JSON (= diccionarios/listas de M1)?
- [ ] ¿Se entiende la navegación de JSON (claves encadenadas y listas)?
- [ ] ¿El puente a M3 (pandas) y la nota de "buen ciudadano / caché" están claros?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

---

*Fuente de datos: mindicador.cl (indicadores del Banco Central de Chile), API pública. Copia de respaldo capturada el 2026-06-20.*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
