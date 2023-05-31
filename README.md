# 2023-1 / IIC2173 - E2 | CPE Ticket Seller

_aka. Procesamiento de Pagos como Eventos_

Integrantes:

- Cristóbal Rubio
- Pablo Kipreos
- Martin Jara
- Matias Guzman
- Manuel Jouanne

---

## **Herramientas utilizadas**

Las siguientes herramientas fueron utilizadas en el proyecto:

- Dominio(s): Namecheap, ocupamos 3 cuentas distintas para no complicarnos, se espera consolidar esto en la siguiente entrega de ser necesario. Los 3 certificados están ingresados en AWS Certificate Manager (la región depende del servicio).
- Frontend: Cloudfront, S3.
  - Programado con React.
- Backend: EC2, Api Gateway.
  - Programado con Python/FastApi
- CI/CD: Github Actions
- Base de datos: postgresql en EC2.

## **Rutas y dominios**

El producto final solo necesita de dos rutas (Front y api), sin embargo, dado que no era requisito privatizar el resto, decidimos dejar abiertas las rutas tal de poder debuguear. Además, en caso de que algo falle, es posible identificar si es el dominio o el servidor.

**Dominios**

- Frontend: `https://www.arquiticket.me/`
- Backend (_esta ruta estaría privada para la siguiente entrega, ya que el front consume la api gateway_): `https://arquie0.me/`
- Api Gateway: `api.ticketsbycorubio.me`

**Origin Points**

- S3 Bucket: `http://entrega-arqui.s3-website.us-east-2.amazonaws.com`
- Cloudfront Distribution: `https://ds2x5sjhqf7r7.cloudfront.net`
- Api Gateway: `https://yxwrw33q37.execute-api.us-east-2.amazonaws.com/production`

### **Requisitos funcionales (13 ptos)**

- ✅ **RF1** (3 ptos) (Esencial): Cada usuario debe tener la capacidad de agregar dinero a una
  "billetera" dentro de su aplicación.
- ✅ **RF2** (2 ptos) (Esencial): Cuando un usuario compre una entrada dentro de su aplicación, se debe validar que tenga el dinero suficiente en su billetera, y si es así, descontarle el dinero internamente para enviarlo a la API central.
- ✅ **RF3** (3 ptos) (Esencial): Para validar su compra deben hacer la llamada como se explica
  previamente y realizar el cálculo de los challenges mediante workers.
- ✅ **RF4** (2 ptos): Debe haber un indicador que muestre si el servicio maestro de workers está disponible.
- ✅ **RF5** (3 ptos): Los usuarios deben poder descargar su entrada si esta se validó
  correctamente desde su vista de compras.

### **Requisitos no funcionales (38 ptos)**

- ✅ **RNF01** (15 ptos): Deben crear el servicio que hace el cálculo de la prueba criptográfica de pagos indicada en el enunciado, el cual asigna tareas a workers, lleva el registro de trabajos y los resultados. Este servicio existe en un container independiente, se conecta via HTTP ofreciendo una API REST y posee workers conectados mediante un broker con capacidad de encolado/pubsub (Redis/rabbitMQ), así como conexión a la base de datos del backend principal.
  - ✅ **Bonus** (5 ptos) Separar los workers en contenedores propios tiene un bonus de 5 ptos
- ✅ **RNF02** (4 ptos): Una vez que se reciba una validación de un pago hecho en su aplicación,
  deberán enviar una notificación vía correo a los usuarios que lo solicitaron.
- ✅ **RNF03** (5 ptos): La aplicación tiene que ofrecer un servicio de generacion de tickets PDF desde AWS Lambda (como los que genera la página kupos.cl). Este ticket debe tener el nombre de su grupo y los datos del usuario y la entrada que compró. Además, debe almacenarse en S3 y se le debe entregar al usuario un enlace público para descargarlo desde S3. Deben utilizar Serverless.js o AWS SAM para manejar y desplegar esta función.
  - ❌ **Bonus** Crear un pipe CI/CD para este servicio tiene un bonus de 4 ptos
- ✅ **RNF04** (9 ptos): Deben implementar CD en su pipeline CI/CD para backend. Como
  proveedores aceptados de CI están Github Actions, Codebuild y CircleCI. Para deployment
  deben usar AWS codedeploy.
- ✅ **RNF05** (5 ptos): Deben implementar CD en su pipeline CI/CD para frontend. Como
  proveedores aceptados de CI están Github Actions, Codebuild y CircleCI. Para deployment
  deben subir su frontend a AWS S3 e invalidar la caché de Cloudfront que sirve su frontend.

### **Documentación**

Se pueden encontrar los archivos correspondientes en `/docs`

- ✅ **RDOC01** (2 ptos): Deben actualizar su diagrama UML de componentes con lo realizado en esta entrega, con explicaciones y detalle sobre el sistema.
- ✅ **RDOC02** (2 ptos): Deben actualizar su documentación del pipeline CI para incluir los pasos extras necesarios para la realización del CD.
- ❌ **RDOC03** (2 ptos): Deben incluir una documentación de cómo subir su aplicación en
  Serverless/SAM, paso a paso
- ✅ **RDOC04** (3 ptos): Deben documentar todas las posibles llamadas a sus APIs expuestas a sus clientes con algún estandar (Postman, Swagger u otra).
