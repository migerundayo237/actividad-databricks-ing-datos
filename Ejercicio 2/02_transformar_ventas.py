# Databricks notebook source
# MAGIC %md
# MAGIC # 02_transformar_ventas
# MAGIC Bronze -> Silver (limpieza + total_venta) y tabla resumen por categoría. Es idempotente (usa overwrite).

# COMMAND ----------

from pyspark.sql import functions as F

CATALOGO = "workspace"
ESQUEMA = "ingenieria_datos_miguel"
P = f"{CATALOGO}.{ESQUEMA}"

# COMMAND ----------

bronze = spark.read.table(f"{P}.ventas_bronze")
n_bronze = bronze.count()

# 1) Eliminar registros idénticos duplicados
sin_duplicados = bronze.dropDuplicates()
n_sin_dup = sin_duplicados.count()

# 2) Reglas de calidad: producto presente, cantidad > 0, precio > 0
#    (los nulos en cantidad/precio también se descartan, porque null > 0 no es True)
limpias = sin_duplicados.filter(
    F.col("producto").isNotNull()
    & (F.trim(F.col("producto")) != "")
    & (F.col("cantidad") > 0)
    & (F.col("precio_unitario") > 0)
)

# 3) total_venta = cantidad * precio_unitario
silver = limpias.withColumn("total_venta", F.round(F.col("cantidad") * F.col("precio_unitario"), 2))
n_silver = silver.count()

print(f"Registros en bronze:                 {n_bronze}")
print(f"Después de quitar duplicados:        {n_sin_dup}")
print(f"Después de reglas de calidad (silver): {n_silver}")

# COMMAND ----------

# 4) Guardar silver (overwrite => la re-ejecución no acumula registros)
(silver.write.format("delta").mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(f"{P}.ventas_silver"))

# 5) Ventas por categoría
por_categoria = (spark.read.table(f"{P}.ventas_silver")
                 .groupBy("categoria")
                 .agg(F.round(F.sum("total_venta"), 2).alias("total_vendido"))
                 .orderBy(F.col("total_vendido").desc()))

(por_categoria.write.format("delta").mode("overwrite")
              .option("overwriteSchema", "true")
              .saveAsTable(f"{P}.ventas_por_categoria"))

display(spark.read.table(f"{P}.ventas_por_categoria"))

# COMMAND ----------

# Verificación de idempotencia: ejecuta TODO el notebook dos veces y compara estos conteos.
print("silver:", spark.read.table(f"{P}.ventas_silver").count())
print("por_categoria:", spark.read.table(f"{P}.ventas_por_categoria").count())
# Opcional: historial Delta (cada ejecución crea una versión, pero el número de filas no crece)
display(spark.sql(f"DESCRIBE HISTORY {P}.ventas_silver"))
