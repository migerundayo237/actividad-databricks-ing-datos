## Ejercicio 3. Automatizar el proceso mediante un job

### ¿Qué es un job en Databricks y para qué sirve?

Un job es el recurso principal de Databricks para coordinar, programar y ejecutar trabajo de forma automática, como un flujo de trabajo (workflow). Sirve para que procesos repetitivos, por ejemplo una carga y una transformación de datos, se ejecuten sin abrir cada notebook manualmente. Puede tener un disparador (trigger) que lo inicie en un horario o ante un evento, parámetros, y notificaciones si falla o tarda demasiado.

### ¿Qué es una tarea y cómo se diferencia de un job?

Una tarea es una unidad de trabajo concreta dentro de un job, por ejemplo ejecutar un notebook, un script de Python o un pipeline. El **job** es el contenedor que agrupa y organiza las tareas, y define cuándo y cómo corren; la **tarea** es cada paso individual. Un job puede tener desde una sola tarea hasta cientos, y sus tareas se representan como un grafo.

### ¿Qué significa establecer dependencias entre tareas?

Significa definir el **orden de ejecución**: una tarea solo corre cuando otra (o varias) de las que depende ha terminado. Por defecto, una tarea espera a que sus tareas previas hayan terminado con éxito. En esta actividad, `02_transformar_ventas` depende de `01_cargar_ventas`, de modo que la transformación no corre si la carga falla. El conjunto de tareas y dependencias forma un grafo acíclico dirigido (DAG).

### ¿Qué información del historial de ejecuciones permite identificar un fallo?

- La **vista de matriz** de la pestaña *Runs*, que muestra el estado de cada tarea en cada ejecución (exitosa, fallida u omitida por fallo de una dependencia).
- Los **detalles de la ejecución de la tarea**: el estado, las fechas de inicio y fin, la duración, la salida del notebook y el **mensaje de error** (por ejemplo, que una columna no se puede resolver).
- La opción **Repair run**, que permite volver a ejecutar solo las tareas fallidas y las que dependen de ellas.

**Fuentes consultadas**
- Databricks. *Lakeflow Jobs.* https://docs.databricks.com/jobs
- Databricks. *Troubleshoot and repair job failures.* https://docs.databricks.com/aws/jobs/repair-job-failures