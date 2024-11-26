# papd-pd-hackathon
Código y materiales utilizados para el Proyecto Final - Hackathon del curso Product Development del postgrado en Análisis y Predicción de Datos de la Maestría en Data Science en la Universidad Galileo.

## Construcción del contenedor Docker

Primero, debes construir la imagen Docker utilizando el siguiente comando. Este comando crea la imagen auto-ml con la última versión:

`
docker build -t pd:latest .
`

Este comando buscará el archivo Dockerfile en el directorio actual y construirá la imagen Docker. Asegúrate de ejecutar este comando en el directorio raíz del proyecto, donde se encuentra el Dockerfile.


## Ejecución del contenedor Docker

Una vez que la imagen se haya construido, puedes ejecutar el contenedor con el siguiente comando. Asegúrate de tener el archivo de configuración (test.env), que debe contener las variables de entorno necesarias.

`
docker run --env-file test.env -v "localpath/data":/app/data pd:latest
`
