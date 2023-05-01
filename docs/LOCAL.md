# **Documentación deploy local**

# Deploy del Backend

## 1. Clonar el repositorio

Para clonar el repositorio se debe insertar lo siguiente en la línea de comandos

```bash
git clone https://github.com/iic2173/e1-2023-1-grupo-20-backend.git
```

## 2. Configurar variables de entorno

Para el correcto funcionamiento se debe crear un archivo `.env` en el directorio `./subscriber` y
el mismo archivo en el directorio `./publisher`. El contenido de este debe ser:

```bash
HOST=passline.iic2173.net
PORT=9000
USER_MQTT=students
PASSWORD=iic2173-2023-1-students
```

## 3. Ejecutar el programa

En primar lugar es necesario tener docker instalado en el computador.

Luego es necesario crear las imagenes de los contenedores

```bash
docker compose build
```

Por último, se deben levantar los contenedores

```bash
docker compose up
```

#

# Deploy del Frontend

## 1. Clonar el repositorio

Para clonar el repositorio se debe insertar lo siguiente en la línea de comandos

```bash
git clone https://github.com/iic2173/e1-2023-1-grupo-20-frontend.git
```

## 2. Instalar dependencias

Para instalar las dependencias se debe ejecutar el siguiente comando

```bash
npm install
```

## 3. Configurar variables de entorno

Para el correcto funcionamiento se debe crear un archivo `.env` en el directorio raiz `./` y el
contenido de este archivo si se quiere correr con el host local debe ser

```bash
REACT_APP_BACKEND_HOST="http://localhost:8008/"
```

Y si se desea conectar con el backend en EC2 el archivo `.env` debe tener el siguiente contenido

```bash
REACT_APP_BACKEND_HOST="https://arquie0.me"
```

## 4. Ejecutar el programa

Para ejecutar el programa se debe ejecutar el siguiente comando

```bash
npm run start
```

#
