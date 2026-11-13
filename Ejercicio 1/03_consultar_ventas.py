# Databricks notebook source
# MAGIC %md
# MAGIC # 03_consultar_ventas
# MAGIC Notebook distinto al de carga: lee la tabla con su nombre completo `catalogo.esquema.tabla`.

# COMMAND ----------

df = spark.read.table("workspace.ingenieria_datos_miguel.ventas_bronze")   # ajusta catálogo/esquema

print("Total de registros:", df.count())

# COMMAND ----------

# Ventas de una categoría a elección
display(df.filter(df.categoria == "Bebidas"))

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Equivalente en SQL
# MAGIC SELECT COUNT(*) AS total_registros FROM workspace.ingenieria_datos_miguel.ventas_bronze;
# MAGIC SELECT * FROM workspace.ingenieria_datos_miguel.ventas_bronze WHERE categoria = 'Bebidas';
