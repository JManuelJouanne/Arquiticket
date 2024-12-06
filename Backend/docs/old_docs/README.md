# 2023-1 / IIC2173 - E1 | PPE Ticket Seller
*aka. Procesamiento de Pagos como Eventos*

Integrantes:
- Cristóbal Rubio
- Pablo Kipreos
- Martin Jara
- Matias Guzman
- Manuel Jouanne
---
## **Nota importante**
Se ocupó más de una cuenta AWS para este proyecto, por lo que se adjuntan dos credenciales de acceso. 

`name_pending`: para Cognito y SES
`corrector`: para el resto (región principal us-east-1)

## **Herramientas utilizadas**
Las siguientes herramientas fueron utilizadas en el proyecto:

* Dominio(s): Namecheap, ocupamos 3 cuentas distintas para no complicarnos, se espera consolidar esto en la siguiente entrega de ser necesario. Los 3 certificados están ingresados en AWS Certificate Manager (la región depende del servicio).
* Frontend: Cloudfront, S3.
    * Programado con React.
* Backend: EC2, Api Gateway.
    * Programado con Python/FastApi
* CI/CD: Github Actions
* Base de datos: postgresql en EC2.


## **Rutas y dominios**

El producto final solo necesita de dos rutas (Front y api), sin embargo, dado que no era requisito privatizar el resto, decidimos dejar abiertas las rutas tal de poder debuguear. Además, en caso de que algo falle, es posible identificar si es el dominio o el servidor. 

**Dominios**
* Frontend: `https://www.arquiticket.me/`
* Backend (*esta ruta estaría privada para la siguiente entrega, ya que el front consume la api gateway*): `https://arquie0.me/`
* Api Gateway: `api.ticketsbycorubio.me`

**Origin Points**
* S3 Bucket: `http://entrega-arqui.s3-website.us-east-2.amazonaws.com`
* Cloudfront Distribution: `https://ds2x5sjhqf7r7.cloudfront.net`
* Api Gateway: `https://yxwrw33q37.execute-api.us-east-2.amazonaws.com/production`


### **Requisitos funcionales**
 
* ✅ **RF1 (registro)**
* ✅ **RF2 (lista de eventos)**
    * ❌ **Bonus** 
* ✅ **RF3: (Mostar detalle de eventos)** 
* ✅ **RF4: (Mostrar a los usuarios sus entradas)**
* ✅ **RF5: (Publicacion entradas):** se publica en event/requests y se espera la respuesta en event/validation.
* ✅ **RF6: (Se actulizan la cantidad de entradas):** se escucha continuamente el canal events/requests y events/validation.


### **Requisitos no funcionales**

* ✅ **RNF01 (implementación front-back)**
* ✅ **RNF02 (Docker)**
* ✅ **RNF03 (Budget Alert):** se puede encontrar con nombre My Monthly Cost Budget.
* ✅ **RNF04 (Api gateway) :** se puede encontrar una api con nombre **arquiticket**, con ruta `api.ticketsbycorubio.me`.
* ✅ **RNF05 (autentificación):** implementado con AWS Cognito.
    * ❌ **Bonus** 
* ✅ **RNF06 (S3 + Cloudfront)**
* ❌ **RNF07 (autentificación API)**
* ✅ **RNF08 (HTTPS)**
* ✅ **RNF09 (CI)**
    * ✅ **Bonus:** se implementó un test simple en `api/test_app.py` 



### **Documentación**
Se pueden encontrar los archivos correspondientes en `/docs`

* ✅ **RDOC01**
* ✅ **RDOC02**
* ✅ **RDOC03**