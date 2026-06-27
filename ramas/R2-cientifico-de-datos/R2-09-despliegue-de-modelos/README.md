# B6 · Despliegue de modelos

**Bootcamp de Datos para Funcionarios Públicos — Formación Pública**
Capa B · Ciencia de datos aplicada · Módulo final. *Práctico hasta "modelo usable"; la puesta en producción se ve a nivel conceptual.*

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B6-despliegue-de-modelos/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` en el enlace por la ruta real del repositorio al publicar.

---

## De qué trata

El módulo que **cierra la Línea B**. Un modelo que vive solo en un cuaderno no le sirve a nadie;
**desplegar** es ponerlo a trabajar para que otras personas o sistemas lo usen sobre datos nuevos.
A partir del modelo guardado en D12, el estudiante construye lo esencial de cualquier despliegue:
una **función de predicción**, la **puntuación por lotes**, la **validación de entradas** y la
**generación del archivo de resultados**, y conoce cómo se convierte en un servicio y por qué hay
que **monitorearlo y reentrenarlo**.

**Competencia de salida (manos a la obra):** dejar un modelo guardado **usable** — función de
predicción con validación, puntuación por lotes y archivo de resultados.

**A nivel conceptual (awareness, no se construye aquí):** qué implica llevar el modelo a *producción*
(API/servicio, monitoreo, reentrenamiento) y por qué eso ya es trabajo de un equipo técnico. **En
este módulo no montas un servicio en producción**: dejas el modelo listo y entiendes el panorama.

## Dato real y Fuente

Dataset de compras de alimentos de la ChileCompra / MercadoPúblico (`compras_ml.csv`), más **5 órdenes de compra nuevas** (`compras_nuevas.csv`) para realizar la puntuación por lotes.

**Datasets:** Los archivos `compras_ml.csv` y `compras_nuevas.csv` ya vienen guardados estáticamente en la carpeta del módulo. El notebook los cargará automáticamente (cuenta con un descargador de respaldo para Google Colab).

## Cómo se usa

1. Abre `leccion.ipynb` con **Open in Colab** (solo necesitas una cuenta de Google).
2. Ejecuta las celdas en orden y completa cada `TODO`.
3. Cada ejercicio termina en una **celda de chequeo** que muestra ✅ o una pista. Logrado cuando las 4 dan ✅.

## Contenido

| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante. |
| `solucion.ipynb` | Soluciones de referencia (uso interno del equipo). |
| `profundiza.ipynb` | **Notebook opcional de profundización teórica** (ver abajo). |
| `profundiza_solucion.ipynb` | Solución del profundiza (uso interno). |
| `compras_ml.csv` | Dataset de compras de alimentos para inicializar/entrenar. |
| `compras_nuevas.csv` | Dataset con las 5 nuevas órdenes de compra por puntuar. |
| `README.md` | Esta portada. |

## Los 4 ejercicios

1. **Función de predicción** — `predecir_monto(cantidad, tamano_num)` que carga el formato correcto.
2. **Puntuación por lotes** — `predecir_lote(tabla)` agrega `monto_estimado` a una tabla de casos nuevos.
3. **Validar la entrada** — `predecir_seguro(...)` devuelve un dict con `ok` y rechaza cantidades imposibles.
4. **Generar el entregable** — guardar las predicciones en `predicciones_monto.csv`.

## Verificación de calidad

- Solución ejecutada: **4/4 ✅** (predicción puntual para cant=100 y tamaño=2 es 243,166.7 CLP; lote de 5 compras puntuado; validación rechaza cantidad 800; CSV generado).
- Cuaderno del estudiante (con los `TODO` sin completar): **4/4 ❌ amables, sin crashes**.

## Checklist de revisión

- [ ] ¿El nivel sigue la plantilla de M0?
- [ ] ¿Queda clara la idea de despliegue (función de predicción) y la diferencia en línea vs lote?
- [ ] ¿Se entiende el "contrato" del modelo y por qué validar la entrada?
- [ ] ¿La sección de API/Gradio + monitoreo/reentrenamiento cierra bien el panorama?
- [ ] ¿El cierre de la Línea B (recorrido D8–D13 → Proyecto Final) es claro y motivador?
- [ ] Verificado → "En revisión" → aprobar → GitHub → enlace → "Publicado".

## 🔬 Profundización (opcional)

¿Quieres entender el *porqué* y no solo el *cómo*? El notebook **`profundiza.ipynb`** va un nivel más
hondo, **a nivel conceptual** (no se monta ningún servicio), en qué implica producción de verdad: el
**contrato del modelo**, la **validación de entrada**, el **monitoreo y el *drift*** (de datos y de
concepto), la **cadencia de reentrenamiento**, la ***model card*** y el **humano en el bucle**. Con 4
ejercicios conceptuales auto-corregidos.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/B6-despliegue-de-modelos/profundiza.ipynb)

---

*Fuente de datos: Dirección de Compras y Contratación Pública (ChileCompra / MercadoPúblico).*
*Contenido bajo licencia CC BY 4.0 · Formación Pública.*
