from pyspark import pipelines as dp
from pyspark.sql import functions as F

# AJUSTA catálogo y esquema de la fuente
FUENTE = "workspace.ingenieria_datos_miguel.ventas_bronze"


@dp.materialized_view(
    name="pipeline_ventas_limpias",
    comment="Ventas sin duplicados, con reglas de calidad y total_venta",
)
def pipeline_ventas_limpias():
    return (
        spark.read.table(FUENTE)
        .dropDuplicates()
        .filter(
            F.col("producto").isNotNull()
            & (F.trim(F.col("producto")) != "")
            & (F.col("cantidad") > 0)
            & (F.col("precio_unitario") > 0)
        )
        .withColumn("total_venta", F.round(F.col("cantidad") * F.col("precio_unitario"), 2))
    )


@dp.materialized_view(
    name="pipeline_ventas_por_categoria",
    comment="Valor total vendido por categoría",
)
def pipeline_ventas_por_categoria():
    # Lee la vista anterior: así Databricks infiere la dependencia y la dibuja en el grafo
    return (
        spark.read.table("pipeline_ventas_limpias")
        .groupBy("categoria")
        .agg(F.round(F.sum("total_venta"), 2).alias("total_vendido"))
    )
