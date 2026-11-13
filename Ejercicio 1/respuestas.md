### ¿Qué es Unity Catalog en Databricks?

Unity Catalog es la capa de gobierno de datos de Databricks. Es un catálogo centralizado donde se registran los datos y los activos de IA (tablas, vistas, volúmenes, modelos) y desde el cual se controla quién puede acceder a cada uno. Además de los permisos, ofrece auditoría, linaje (de dónde viene un dato y qué lo consume) y descubrimiento de datos.

Organiza los objetos en tres niveles: **catálogo → esquema → tabla**. Por eso en la actividad se referencian las tablas como `catalogo.esquema.tabla`. Los objetos se pueden explorar y administrar desde el Explorador de Catálogo (Catalog Explorer), SQL, la CLI o la API REST. Las tablas pueden ser *gestionadas* (Unity Catalog administra todo su ciclo de vida) o *externas* (solo administra el acceso, mientras los archivos viven en el almacenamiento del proveedor de nube).

### ¿Qué diferencia hay entre un DataFrame de Spark y una tabla Delta?

- Un **DataFrame de Spark** es una estructura de datos con filas y columnas que existe en memoria durante la sesión o el notebook. Describe cómo leer y transformar datos, pero por sí mismo no los conserva: si termina la sesión, desaparece.
- Una **tabla Delta** es un dato **persistente** almacenado en el lakehouse. Delta Lake extiende los archivos Parquet con un registro de transacciones, lo que aporta transacciones ACID, validación de esquema al escribir y versiones de la tabla (cada escritura crea una versión que se puede consultar después).

Se relacionan así: un DataFrame se puede guardar como tabla Delta (`df.write.format("delta").saveAsTable(...)`), y una tabla Delta se puede leer de nuevo como DataFrame (`spark.read.table(...)`). En Databricks, las tablas son Delta por defecto.

**Fuentes consultadas**
- Databricks. *What is Unity Catalog?* https://docs.databricks.com/aws/data-governance/unity-catalog
- Databricks. *What is Delta Lake in Databricks?* https://docs.databricks.com/aws/delta/