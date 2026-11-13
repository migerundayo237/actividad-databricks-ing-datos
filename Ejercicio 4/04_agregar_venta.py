# Databricks notebook source
# MAGIC %md
# MAGIC # 04_agregar_venta (Ejercicio 4, paso 7)
# MAGIC Inserta UNA venta válida en ventas_bronze SIN volver a ejecutar 01_cargar_ventas.
# MAGIC Ejecuta antes el pipeline una vez y guarda el resumen "antes".

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM workspace.ingenieria_datos_miguel.pipeline_ventas_por_categoria ORDER BY categoria;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Venta nueva: Lácteos, 5 x 10.000 = 50.000 (debe sumarse a Lácteos)
# MAGIC INSERT INTO workspace.ingenieria_datos_miguel.ventas_bronze
# MAGIC VALUES (18, DATE'2026-10-10', 'Kumis 1L', 'Lácteos', 5, 10000.0);

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS registros_bronze FROM workspace.ingenieria_datos_miguel.ventas_bronze;
