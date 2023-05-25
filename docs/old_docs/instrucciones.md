# 2023-1 / IIC2173 - E1 | PPE Ticket Seller
*aka. Procesamiento de Pagos como Eventos*

***Fecha de entrega:** 30/04/2023 - 4 Semanas*

Después de un alto éxito en la obtención y recopilación de eventos, los contrata formalmente su consultora favorita LegitBusiness, y les pide que pasen a una versión mas poderosa de su plataforma. Dado que los eventos por si solos no presentan mucho valor para sus Stakeholders, se les ha pedido que mejoren su sistema para que permita a usuarios y clientes poder comprar las entradas usando sus servicios de pagos de forma que se puedan coordinar entre todos los grupos fácilmente.

## Objetivo

Deben extender su API web para que sea capaz de conectarse a un canal del broker para publicar sus solicitudes de compra, y luego validarlos con mensajes que les enviaremos desde otro canal.

Utilizando a la conexión que ya poseen con el broker de eventos, su app debe seguir recolectando los datos según el formato de la E0:

```json
{
   "name": string,
   "date": string (ISO 8601 https://es.wikipedia.org/wiki/ISO_8601),
   "price": number,
   "quantity": number,
   "location": string,
   "latitude": number,
   "longitude": number
},
```

Usando esta data, le presentará a los usuarios una lista de los eventos, de forma paginada en una interfaz de usuario. Los usuarios podrán escoger un evento y solicitar la compra de entradas que se explicará en la siguiente sección.

Será importante manejar una correcta gestión de usuarios, y para evitar problemas de colapso en su aplicación deberán usar un servicio de terceros y conectarlo con su aplicación mediante una API Gateway.

Adicionalmente, para empezar a lograr un proceso de implementación más expedita de su proyecto, se les pedirá que creen su solución en frontend y backend separados, además de implementar un proceso de *Continuous Integration*.

### Solicitudes de Compra de Entradas

El flujo para la compra de una entrada consistirá en poder manejar una integración masiva entre diversas apps que estarán queriendo vender entradas. Para esto se les pedirá que se conecten a un nuevo canal de broker con un nuevo script para que puedan publicar eventos de solicitud de compra, y que luego reciban por otro canal las validaciones de las solicitudes de compra correspondientes.

Para explicar el flujo la idea es que un usuario ya ingresado en su aplicación vea un evento que le interese y aprete en su detalle donde saldrá la opción de compra. Luego de indicar cuantas entradas quiere, ustedes en su aplicación gestionarán si les paga correctamente y su asignación a ese usuario. Ahora viene lo entretenido, validarlo entre todos.

Una vez que su usuario les compre la entrada, **deberán publicar en el broker en el canal `events/requests`** que su aplicación quiere comprar una entrada con el siguiente formato:
```json
{
    "request_id": string (token de idempotencia),
    "group_id": string (número de grupo),
    "event_id": string,
    "deposit_token": "",
    "quantity": number,
    "seller": 0
}
```

En el body que mandará, `request_id` será un [uuid](https://www.howtogeek.com/devops/what-are-uuids-and-why-are-they-useful/) de su solicitud que manejarán ustedes que para cada una deberá ser distinta (en la sección de enlaces útiles hay links que les pueden servir), y `group_id` es su número de grupo. Finalmente `deposit_token` será un token que usarán para futuras entregas y que en está deben enviarlo como un string vacío. El atributo `selller` siempre deberá ser 0 para esta entrega.

Como todos los grupos mandarán mensajes por este canal, deberán estar escuchandolo para recibir las solicitudes de los otros grupos y disminuir su cantidad de entradas disponibles.

**Para poder validar las compras, tendrán que escuchar el canal `events/validation`.** Acá se les enviarán respuestas en el formato:
```json
{
    "request_id": string,
    "group_id": string,
    "seller": 0,
    "valid": bool (indica si fue válida la solicitud)
}
```

Si reciben una respuesta de que esa transacción es válida, entonces deben marcarla como completada. En otro caso (solicitud inválida), deberán marcarla como que no se logró y deberán volver a disponibilizar las entradas que tenía ese evento.

### Requisito de Integración Continua

Para el requisito de continuous integration, les recomendamos usar los siguientes proveedores junto a su repo de GitHub (esto para evitar cobros):

* CircleCI
    * (*Habra cápsula disponible*)
    * No tiene minutos por organización, así que podrán usarlo al 100% aprovechando los minutos gratis
* Github Actions

## Ejemplo de flujo a nivel de usuario

Un usuario ingresa en la plataforma con credenciales creadas anteriormente a su aplicación. Este va a una lista de eventos disponibles y los revisa página por página. Para comenzar, escogera uno y revisara el detalle de este. Tendrá la opción de poder comprar entradas a este evento si quedan cupos. Se gestionará su "pago" y se le que su compra está en proceso. Finalmente, luego de un rato, el usuario revisará y su compra se marcará como completada correctamente o no.

## Especificaciones

**Si un requisito está marcado como *Esencial*, el no cumplirlo en un grado mínimo (al menos un punto) reducirá la nota máxima a *4.0*. NO se revisaran entregas que no estén en la nube.**

Por otro lado, debido a que esta entrega presenta una buena cantidad de *bonus*, la nota no puede sumar más de 8, para que decidan bien que les gustaría aprovechar.

Al final de la entrega, la idea es que se pongan de acuerdo con su ayudante para agendar una hora y hacer una demo en vivo para su corrección. Se revisarán algunas features esenciales de código (conexión al broker). Pueden utilizar Github Copilot (recomendado) para multiplicar su productividad y ChatGPT (poco recomendado) para dudas de implementacion.

### Requisitos funcionales (14 ptos)

* **RF1 *(2 ptos) (Esencial)*:** Sus usuarios deben poder registrarse en la plataforma con datos de contacto y un correo electrónico
* **RF2 *(2 ptos)*:** Los usuarios deben poder ver una lista paginada (de a 25 eventos) de los eventos disponibles en el servidor por orden de llegada.
    * Mostrar un mapa con los eventos de esa página tiene un bonus<sup>1</sup>  de (5 ptos)
* **RF3 *(2 ptos) (Esencial)*:** Debe poder verse el detalle de cada evento y dar la opción de compra si hay entradas disponibles.
* **RF4 *(2 ptos)*:** Deben poder mostrarle a su usuario las entradas compradas y si su solitud se completó correctamente. 
* **RF5 *(3 ptos) (Esencial)*:** Al comprar una entrada se deberá enviar la solicitud por el canal `events/requests` y esperar la respuesta de si es válida por el canal `events/validation`.
* **RF6 *(3 ptos) (Esencial)*:** Deberán estar escuchando los canales de `events/requests` y `events/validation` continuamente para ir actualizando su cantidad de entradas disponibles.


### Requisitos no funcionales (40 ptos)

* **RNF01 *(6 ptos) (Esencial)*:** Deben usar un formato de Backend-Frontend separado: una API con respuestas JSON y un frontend. Esto es muy importante puesto que es crítico para las siguientes entregas. Usen un combo como Koa-React, Express-Flutter, FastAPI-Vue o cualquier otra combinación que les acomode. El Frontend debe ser ojalá una SPA **con un Framework que permita exportar el build de su frontend**.

* **RNF02 *(2 ptos) (Esencial)*:** Sus aplicaciones en backend deben estar en un container docker, cada una. Debe coordinarse el levantamiento mediante docker compose.

* **RNF03 *(2 ptos) (Esencial)*:** Deben tener configuradas *Budget alerts*, para no alejarse del Free tier de AWS.

* **RNF04** (***6 ptos***) ***(Esencial)*** : Su API debe estar detrás de una AWS API gateway tipo REST, con los endpoints declarados en esta. Debe asociarse un subdominio a esta (e.g. api.miapp.com) y debe tener CORS correctamente configurado.

* **RNF05** (***7 ptos***) ***(Esencial)***: Deben implementar un servicio de autenticacion/autorización (auth). Este servicio puede ser en base a un servicio de terceros como Auth0, cognito o pueden hacerlo ustedes. Este RNF requiere que ustedes extraigan toda la lógica de los usuarios de la app principal y la trasladen a el servicio hecho por ustedes o el externo. Recomendamos fuertemente usar el modelo Oauth o como mínimo intercambiar tokens JWT con la audiencia e issuer correctos.
    * Si hacen un servicio ustedes desde 0, tienen un bonus de **5 ptos**.

* **RNF06** (***3 ptos***): Su frontend debe estar desplegado en S3 con una distribución Cloudfront.

* **RNF07** (***3 ptos***): Su API Gateway debe poder usar al servicio del RNF05 para autenticar a los usuarios directamente.

* **RNF08** (***3 ptos***) ***(Esencial)*** : Su app debe ofrecer su backend y frontend utilizando HTTPS

* **RNF09 *(8 ptos)*:** Deben implementar un pipeline de CI. Como proveedores aceptados están CircleCI, Github Actions y AWS codebuild. Recomendamos los dos primeros porque los ayudantes tienen experiencia en estos dos. Esta implementación debe correr un script que genere una imagen para containers de su servicio
    * Implementar un test trivial que pueda fallar (tipo `assert false` o similar) tiene un bonus de **3 ptos**

### Documentación (6 ptos)

Todos estos documentos los deben dejar dentro de su repositorio de Github en una carpeta `/docs`. 

* **RDOC01 *(3 ptos)*:** Deben crear un diagrama UML  de componentes de la entrega, con **explicaciones y detalle** sobre el sistema. Esto deben tenerlo para la fecha final de entrega.
* **RDOC02 *(2 ptos)*:** Deben documentar los pasos necesarios para replicar el pipe CI que usaron en su aplicación (Qué pasos sigue si CI).
* **RDOC03 *(1 ptos)*:** Deben dejar una documentación de alguna forma de correr su aplicación en un ambiente local para propósitos de testeo (que instalar, que poner en el .env, como correr la app, etc).


## Recomendaciones

* Comiencen la entrega lo antes posible, puesto que es mas sencillo ir trabajando de a partes y seguro tendrán dudas. Se les dio plazo extra para que se adecuen a sus equipos de trabajo.
* Planifiquen con antelación: pregunten dudas o ambigüedades a sus ayudantes.
* Ojo con los deploys a última hora, la maldición de la demo es muy real.
* Ocupen el Free Tier de AWS, que tiene capacidad para todos estos requerimientos. Deberían usar los siguientes servicios:
	* **EC2**: AWS les proporciona una instancia t2.micro gratuita al mes.
	* **S3**: Tienen 5 GB de almacenamiento y 20000 solicitudes GET.
	* **RDS** (Opcional, Recomendado): Tienen 20GB y una instancia básica al mes.
	* **API Gateway**: 1 MM de llamadas al mes
	* **Lambda (Opcional)**: Tienen 400K GB/s y 1 MM de solicitudes.
	* **EBS**: 30 GB al mes para almacenamiento de discos de sistema.
	* **Cloudfront**: 50 GB al mes de transferencia.
	* **Amazon SES**: 62000 mensajes salientes / mes.
* **NO** está planificado hacer devolución por uso de dolares en AWS. Para la entrega el free tier de AWS es suficiente para conseguir todos los puntos. En caso de utilizar dólares en su solución, el curso no puede hacerles devolución de estos bajo ninguna causa.
* Usen una cuenta nueva o de alguien que no tenga otras cargas en AWS, para evitar cargos por ahora, además de usar una tarjeta prepago y los budget alerts de AWS para evitar costos oculto<sup>4</sup> .
* **USEN LEAFLET** para los mapas, o la API de google maps que tiene un free tier bastante generoso.

### Consideraciones

No se considerarán entregas:
* Con componentes que corran en sus computadores o servidores que no sean los básicos de AWS. Algunos ejemplos, los servicios de AWS serían:
    * EC2
    * VPC
    * IAM
    * S3
    * AWS API Gateway
    * CloudFront
    * Lambda
* Montadas en Heroku/Firebase/Elastic beanstalk/Lightsail/Netlify o similares.
* Que no estén documentadas.

Pueden utilizar cualquiera de los siguientes lenguajes. Los frameworks son los recomendados. Sugerimos que utilizen en cada grupo el lenguaje que todos sepan usar más o les parezca más sencillo de aprender. Los lenguajes en cursiva poseen ayudantes capaces de ayudarlos en su implementación de código.

* *Python*
    * FastAPI
    * Django
* *Javascript (js)*
    * Koa
    * Express
    * NestJS (solo si tienen muuuucha experiencia, aprenderan mucho)
* *Ruby*
    * Rails
* C# 
* Go 
* Rust

# Puntaje

### Atraso

Para esta entrega se les descontará 0.5 puntos en la nota máxima por horas Fibonacci con F1 = 6 y F2 = 6. 

Se considerará como atraso cualquier modificación en features o implementación que tenga que ver solo con lo que se pide en esta entrega.

| Fibonacci | Hora               | Nota maxima |
|-----------|--------------------|-------------|
| 6         | 0:01 - 5:59        | 6.5         |
| 6         | 6:00 - 11:59       | 6           |
| 12        | 12:00 - 23:59      | 5           |
| 18        | 24:00 - 41:59      | 4.5         |
| 30        | 42:00 - 71:59      | 4           |
| ...       | 72:00 en adelante  | 1           |

### Grupal

La nota se calcula como:

**E<sub>1 grupal</sub> = 1 + E<sub>1 RF</sub> + E<sub>1 RNF</sub> + E<sub>1 RDOC</sub>**

Siendo **E<sub>1 RF</sub>** el puntaje ponderado de los requisitos funcionales, y **E<sub>1 RNF</sub>** el correspondiente a los requisitos no funcionales y **E<sub>1 RDOC</sub>** de la documentación.

### Individual

Segun el programa del curso<sup>5</sup> , esto se evalua como:

**E<sub>1</sub> = 1 + ((E<sub>1 grupal</sub> - 1) * F<sub>g</sub>)**			
Donde F<sub>g</sub> es un factor de coevaluación asignado por el grupo que va de 0 a 1.2. Para esto se enviará un form de coevaluación donde cada integrante deberá evaluar a sus compañeros de grupo con una puntuación entre 1 y 5. 

**No podrán asignarle 5 puntos a más de un compañero, y sí lo hacen, se considerará que se entregó un máximo de 4 puntos a cada compañero**.

De no realizar la coevaluación, asumiremos que se le entregó el mismo puntaje de coevaluación a cada integrante, es decir 4 puntos.

## Links útiles

* [API Gateway - Rest API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)
* [Documentación de Auth0 con API Gateway](https://auth0.com/docs/customize/integrations/aws/aws-api-gateway-custom-authorizers)
* [Circle CI Blogs - CI para Django](https://circleci.com/blog/continuous-integration-for-django-projects/)
* Librerías UUID
    * [Python](https://pypi.org/project/uuid6/)
    * [NodeJS](https://www.npmjs.com/package//uuid)
    * [Ruby](https://www.uuidgenerator.net/dev-corner/ruby)

## Apoyo

Cada grupo tendrá un ayudante asignado el cuál podrán elegir mediante un link que se les mandará oportunamente. Este ayudante está encargado de hacerles seguimiento y orientar sus dudas para responderlas ellos mismos y el equipo de ayudantes. Les recomendamos **fuertemente** que pregunten sus dudas a su ayudante de seguimiento puesto que conocen del proyecto o pueden dirigir sus dudas a otros ayudantes. Puede ser de enunciado, código o algún tópico<sup>3</sup>  que tenga que ver con el proyecto

Dado que cada ayudante puede tener pequeñas diferencias en sus correcciones, queda a criterio de este hacer relajos o hacer mas estrictas ciertas particularidades. Intenten tener un flujo de comunicación directo con sus ayudantes para aclarar posibles diferencias o decisiones de diseño.

Pueden usar el Slack del curso para dudas más rápidas. Usen el [canal #e1](https://arqui-software.slack.com/archives/C037YKULFQF) para sus dudas.

Las ayudantías programadas relevantes para esto por ahora son:

* S3 Upload - 31/03
* Continuous Integration [Cápsula] - 06/04
* API Gateway + CORS - 21/04

También está presupuestada una sala de ayuda para el proyecto con fecha a anunciarse.

Se les avisará con antelación cuándo son y si habrá más.
