# M2 · Funciones y lectura de archivos

Tercer módulo (cierre del prework) del **Bootcamp de Datos para Funcionarios Públicos — Formación Pública**.
Módulo compartido. Modalidad autoguiada, se ejecuta en Google Colab.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/formacionpublica-bootcamp/bootcamp/blob/main/P3-funciones-y-archivos/leccion.ipynb)

> Reemplaza `formacionpublica-bootcamp/bootcamp` por la ruta real del repositorio al publicar.

## ¿Qué vas a aprender?
A empaquetar código en funciones (con parámetros y valores por defecto), usar módulos estándar (`statistics`, `csv`) y leer datos externos desde un archivo CSV. 

**Dataset:** Serie histórica de compras públicas reales de la plataforma de ChileCompra (`compras.csv`), la cual viene pre-construida de forma fija en la carpeta del módulo.

**Competencia de salida:** leer datos externos desde un archivo y organizarlos con funciones para resumirlos.

## Cómo empezar
1. Abre `leccion.ipynb` con **Open in Colab**.
2. El cuaderno cargará automáticamente el archivo `compras.csv` (incluye un descargador automático en caso de ejecutarse en la nube de Google Colab).
3. Completa los `# TODO` y corre la celda de chequeo para obtener tu ✅ o pista.
4. Terminas cuando las cuatro celdas de chequeo muestran ✅.

## Archivos
| Archivo | Para qué |
| --- | --- |
| `leccion.ipynb` | Cuaderno del estudiante. |
| `solucion.ipynb` | Soluciones de referencia (uso interno). |
| `compras.csv` | Dataset de compras públicas para la práctica. |
| `README.md` | Esta portada. |

## Contenido
- Funciones: parámetros, `return` y parámetro por defecto.
- Módulos (`import`): `statistics` y funciones integradas.
- Leer un archivo de texto con `with open() as f:`.
- Leer un CSV con `csv.DictReader` y la conversión obligatoria de texto a número.
- Errores típicos (`FileNotFoundError`, olvidar `return`, sumar sin convertir).
- 4 ejercicios prácticos auto-corregidos.

---
Licencia: CC BY 4.0 · Formación Pública · **Datos:** ChileCompra / MercadoPúblico (datos.gob.cl)
