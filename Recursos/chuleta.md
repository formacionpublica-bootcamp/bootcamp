# Chuleta — Python + pandas

Una hoja para tener al lado mientras trabajas. No hay que memorizar nada: se consulta.

## Python básico

```python
# Variables y tipos
gasto = 18430546563769      # int  (entero)
promedio = 9871357.5        # float (decimal)
pais = "Chile"              # str  (texto)
es_alto = True              # bool (verdadero/falso)

# Operadores:  +  -  *  /   (la / siempre da decimal)
promedio = gasto / 1867076

# Condicionales
if gasto > 10_000_000_000_000:
    nivel = "alto"
elif gasto > 1_000_000_000_000:
    nivel = "medio"
else:
    nivel = "bajo"

# Bucle for + acumulador
total = 0
for monto in [100, 200, 300]:
    total = total + monto

# Función
def gasto_total(montos):
    return sum(montos)

# f-string y formato de número grande
print(f"Gasto: ${gasto:,.0f} CLP")   # Gasto: $18,430,546,563,769 CLP
```

## Texto (limpieza)

```python
"  Salud  ".strip()              # "Salud"        (quita espacios)
"MINSAL".lower()                 # "minsal"
"ministerio de salud".title()    # "Ministerio De Salud"
"S.A.G.".replace(".", "")        # "SAG"
"a,b,c".split(",")               # ["a", "b", "c"]
"  Min DE Salud ".strip().title()  # encadenado
```

## pandas

```python
import pandas as pd

df = pd.read_csv("datos.csv")    # cargar una tabla

# Mirar
df.head()            # primeras filas
df.shape             # (filas, columnas)
df.info()            # tipos y nulos
df.columns           # nombres de columnas

# Seleccionar y filtrar
df["monto"]                       # una columna
df[["organismo", "monto"]]        # varias columnas
df[df["region"] == "Maule"]       # filtrar filas
df[df["monto"] > 1_000_000]       # filtrar por número

# Contar y resumir
df["region"].value_counts()       # cuántas filas por categoría
df["monto"].mean()                # promedio (.sum / .max / .min / .median)
df.describe()                     # resumen estadístico

# Agrupar y sumar (la "tabla dinámica")
df.groupby("sector")["monto"].sum().sort_values(ascending=False)

# Cruzar dos tablas (el BUSCARV)
pd.merge(ordenes, organismos, on="entcode")              # solo coincidencias (inner)
pd.merge(ordenes, organismos, on="entcode", how="left")  # conserva todas las órdenes

# Ordenar y guardar
df.sort_values("monto", ascending=False)
df.to_csv("resultado.csv", index=False)
```

## SQL (recordatorio)

```sql
SELECT region, SUM(monto) AS gasto
FROM ordenes
WHERE anio = 2025
GROUP BY region
ORDER BY gasto DESC
LIMIT 10;
```

## ¿Te trancaste?

Lee la **última línea** del error. Si no la entiendes, **pégale el error + tu código a la IA**
(Gemini/ChatGPT) y pídele que te explique qué significa — **sin pegar datos personales**.

---
*CC BY 4.0 · Formación Pública*
