# Serverless

Esta documentación describe el proceso para subir la aplicación de compra de tickets online, que utiliza AWS Lambda para generar tickets en PDF y almacenarlos en Amazon S3 usando Serverless.

## Requisitos previos:
Configuración del entorno local: Hay que tener configurado el entorno local con las credenciales de acceso a tu cuenta de AWS.

## Pasos:

**2. Creación de la función Lambda:**

Creamos una función Lambda en AWS que genera los tickets en formato PDF con python. Configuramos los permisos de la función Lambda para tenga acceso a los recursos necesarios, como S3.

**3. Configuración de S3:**

Creamos un bucket de Amazon S3 para almacenar los tickets generados en formato PDF. Configuramos los permisos en el bucket para que la función Lambda pueda escribir y leer los archivos de tickets.

**4. Empaquetado de la aplicación:**

Empaquetamos las dependencias necesarias en archivos ZIP. En este caso fue la librería `pdfkit` con el ejecutable `wkhtmltopdf`.

**5. Configuración y despliegue de la aplicación en Serverless:**

Instalamos Serverless con el siguiente comando:
```
npm install -g serverless
```
Configuramos Serverless ejecutando el comando serverless en la terminal y siguiendo las instrucciones para vincular tu cuenta de AWS.
Creamos un archivo serverless.yml y definimos la configuración necesaria para la aplicación. Incluir la función Lambda y los recursos relacionados.
Dentro del archivo serverless.yml, especificamos el nombre del bucket de S3 que creastemos como destino para almacenar los archivos de tickets generados.

**6. Prueba de la aplicación:**

Verificamos que la aplicación funcione correctamente. Realizamos pruebas para asegurarnos de que la generación de tickets en PDF y el almacenamiento en S3 se realicen correctamente.
