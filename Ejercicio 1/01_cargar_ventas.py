# Databricks notebook source
# MAGIC %md
# MAGIC # 01_cargar_ventas
# MAGIC Crea el esquema, construye el DataFrame de ventas (con errores intencionales) y lo guarda como tabla Delta `ventas_bronze`.

# COMMAND ----------

# AJUSTA estos dos valores. Verifica tu catálogo en el explorador (en Free Edition suele ser "workspace").
CATALOGO = "workspace"
ESQUEMA = "ingenieria_datos_miguel"   # cambia "miguel" por tu nombre si lo necesitas

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{ESQUEMA}")
spark.sql(f"USE CATALOG {CATALOGO}")
spark.sql(f"USE SCHEMA {ESQUEMA}")

# COMMAND ----------

from datetime import date
from pyspark.sql.types import (StructType, StructField, IntegerType, DateType,
                               StringType, DoubleType)

schema = StructType([
    StructField("id_venta", IntegerType(), False),
    StructField("fecha", DateType(), True),
    StructField("producto", StringType(), True),
    StructField("categoria", StringType(), True),
    StructField("cantidad", IntegerType(), True),
    StructField("precio_unitario", DoubleType(), True),
])

datos = [
    (1,  date(2026, 10, 1),  "Arroz 1kg",        "Alimentos",  10,  4500.0),
    (2,  date(2026, 10, 1),  "Leche 1L",         "Lácteos",     8,  4200.0),
    (3,  date(2026, 10, 2),  "Jabón de baño",    "Aseo",        5,  3000.0),
    (4,  date(2026, 10, 2),  "Gaseosa 1.5L",     "Bebidas",    12,  5500.0),
    (5,  date(2026, 10, 3),  "Pan tajado",       "Alimentos",   6,  6800.0),
    (6,  date(2026, 10, 3),  "Queso 500g",       "Lácteos",     3, 14500.0),
    (7,  date(2026, 10, 4),  "Detergente 1kg",   "Aseo",        4, 12900.0),
    (8,  date(2026, 10, 4),  "Agua 600ml",       "Bebidas",    20,  2000.0),
    (9,  date(2026, 10, 5),  "Aceite 1L",        "Alimentos",   7, 11000.0),
    (10, date(2026, 10, 5),  "Yogurt 1L",        "Lácteos",     9,  7200.0),
    (11, date(2026, 10, 6),  "Jugo 1L",          "Bebidas",    11,  4800.0),
    (12, date(2026, 10, 6),  "Shampoo",          "Aseo",        2, 15900.0),
    (13, date(2026, 10, 7),  "Lentejas 500g",    "Alimentos",  15,  3600.0),
    # --- Errores intencionales ---
    (5,  date(2026, 10, 3),  "Pan tajado",       "Alimentos",   6,  6800.0),  # DUPLICADA (idéntica a id 5)
    (14, date(2026, 10, 7),  None,               "Bebidas",     4,  3500.0),  # SIN PRODUCTO
    (15, date(2026, 10, 8),  "Mantequilla",      "Lácteos",    -3,  5400.0),  # CANTIDAD NEGATIVA
    # --- Más ventas válidas ---
    (16, date(2026, 10, 8),  "Cerveza",          "Bebidas",    24,  3200.0),
    (17, date(2026, 10, 9),  "Papel higiénico",  "Aseo",       10,  1900.0),
]

df = spark.createDataFrame(datos, schema)
print(f"Registros en el DataFrame: {df.count()}")
display(df)

# COMMAND ----------

# Se usa overwrite para que re-ejecutar el notebook (o el job) no acumule duplicados.
(df.write
   .format("delta")
   .mode("overwrite")
   .option("overwriteSchema", "true")
   .saveAsTable(f"{CATALOGO}.{ESQUEMA}.ventas_bronze"))

print("Tabla ventas_bronze guardada")

# COMMAND ----------

# Columnas y tipos de datos (también puedes verlos en el explorador del catálogo)
display(spark.sql(f"DESCRIBE TABLE {CATALOGO}.{ESQUEMA}.ventas_bronze"))
