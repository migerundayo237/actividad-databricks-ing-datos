## Ejercicio 4. Construir un pipeline declarativo

### ¿Qué es un pipeline de datos y cuáles son sus etapas habituales?

Un pipeline de datos es una secuencia automatizada de pasos que mueve datos desde sus fuentes hasta un destino donde se puedan usar, transformándolos por el camino. Las etapas habituales son:
1. **Ingesta:** traer los datos desde sus orígenes (archivos, bases de datos, flujos de eventos).
2. **Transformación:** limpiar, validar, enriquecer y agregar.
3. **Almacenamiento o publicación:** guardar los resultados en tablas listas para consulta.
4. **Consumo:** reportes, dashboards o modelos que usan esas tablas.

En Databricks suele organizarse con la arquitectura *medallion* (bronze → silver → gold), que es la que usa esta actividad: `ventas_bronze` (datos crudos), `ventas_silver` (limpios) y el resumen por categoría (agregado).

### ¿Qué significa que un pipeline sea declarativo?

Que en lugar de programar paso a paso *cómo* ejecutar el proceso, se **declara qué conjuntos de datos se quieren** (por ejemplo, una vista materializada definida por una consulta), y el motor decide cómo calcularlos. Databricks analiza las dependencias entre los objetos definidos, determina el orden de ejecución, paraleliza lo que puede y gestiona el procesamiento incremental y los reintentos. Por eso `pipeline_ventas_por_categoria` se actualiza después de `pipeline_ventas_limpias` sin que yo se lo indique: la dependencia se infiere porque la lee.

### ¿En qué se diferencian un job que ejecuta notebooks y un pipeline declarativo que define conjuntos de datos?

| | Job con notebooks | Pipeline declarativo |
|---|---|---|
| Enfoque | Procedimental: yo defino los pasos y el orden | Declarativo: yo defino los datasets y el motor orquesta |
| Dependencias | Se configuran manualmente entre tareas | Se infieren de las referencias entre datasets |
| Unidad de trabajo | Tarea (notebook, script, etc.) | Dataset (tabla en streaming, vista materializada) |
| Actualización de datos | Depende de cómo lo programe (por ejemplo, `overwrite`) | El motor recalcula las vistas materializadas, de forma incremental cuando es posible |
| Uso típico | Orquestar procesos de distintos tipos | Definir transformaciones de datos ETL |

Ambos se pueden combinar: un job puede tener una tarea que ejecute un pipeline.

**Fuentes consultadas**
- Databricks. *What is Lakeflow Spark Declarative Pipelines?* https://docs.databricks.com/aws/en/ldp/concepts/
- Databricks. *Lakeflow Spark Declarative Pipelines concepts.* https://docs.databricks.com/gcp/en/ldp/concepts
- Databricks. *Lakeflow Jobs.* https://docs.databricks.com/jobs
- Databricks. *What is Delta Lake in Databricks?* (arquitectura medallion) https://docs.databricks.com/aws/delta/