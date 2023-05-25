# 2023-1 / IIC2173 - E2 | CPE Ticket Seller
*aka. Procesamiento de Pagos como Eventos*

Integrantes:
- Cristóbal Rubio
- Pablo Kipreos
- Martin Jara
- Matias Guzman
- Manuel Jouanne
---

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
