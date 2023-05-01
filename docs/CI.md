# **Documentación CI/CD**

## **¿CD? ¿Así es!**

Es importante destacar que no solo hicimos CI, si no que CD para agilizar el trabajo, aprovechando que ya ibamos a trabajar con Actions, por eso los workflows son un poco más extensos.

Para implementar CI/CD solamente utilizamos Github Actions. El repositorio de backend tiene 3 workflows y el frontend 1, explicados a continuación.

### **Un poco sobre nuestro setup...**

Para nuestro trabajo, usamos las herramientas de Github para armar un proyecto bien integrado. Para comprender bien como funciona cada parte, hay que mencionar los siguientes puntos:

- Nuestro proyecto utiliza dos repositorios: `e1-2023-1-grupo-20-backend` para el backend y `e1-2023-1-grupo-20-frontend` para el frontend.
- Ambos repositorios están enlazados por un Github Proyect, donde levantamos un tablero con los requisitos. Aquí se puede notar que se generan issues y se linkean con PRs.
- Main es la rama principal que hace el deploy (explicado más adelante). Esta rama está protegida por accions y reglas.

---

## **Backend**

### **Secretos de repositorio**

Los siguientes secretos fueron definidos para las acciones:

- `EC2_SSH_KEY`: clave secreta generada desde el par de llaves utilizado en la E0 (ie: el `.pem`)
- `HOST_DNS`: dirección DNS pública del
- `USERNAME`: usuario para entrar con ssh a la instancia EC2
- `TARGET_DIR`: directorio dentro de la instancia EC2 donde se realiza el deploy

### **Deploy automático al servidor (CD)**

Cuando se hace un push a la rama `main`, automáticamente se corre este workflow para levantar el código en la instancia de EC2.

Se siguen los siguientes pasos:

- `Checkout the files`: paso de checkout básico para utilizar el workspace de github
- ` Clone files to server`: se utiliza ssh para entrar al EC2 y correr comandos para pullear los cambios, rebuildear la aplicación e iniciarla.

**Archivo**

```
name: Push to AWS (EC2)

on:
  push:
    branches:
      - main

jobs:
  deploy:
    name: Deploy to EC2 on master branch push
    runs-on: ubuntu-latest

    steps:
      - name: Checkout the files
        uses: actions/checkout@v2

      - name: Clone files to server
        uses: appleboy/ssh-action@master
        with:
          key: ${{ secrets.EC2_SSH_KEY }}
          host: ${{ secrets.HOST_DNS }}
          username: ${{ secrets.USERNAME }}
          # For now, this only starts the app without any additional changes
          # this should be different once lambda and S3 is implemented
          script: |
            cd ~/${{ secrets.TARGET_DIR }}
            git pull
            docker-compose stop
            docker-compose build --no-cache
            docker-compose up -d
```

### **Lint**

Para las pull requests (que son obligatorias para pushear a `main`), se utiliza Flake8 para confirmar que se siga el formato pep8.

Se siguen los siguientes pasos:

- `Checkout the files`: paso de checkout básico para utilizar el workspace de github (_en este caso se nos pasó nombrarlo D:_).
- `Set up Python`: se define el Python a utilizar, en nuestro caso estamos utilizando 3.11
- `Install dependencies`: se instala Python `pip` y `flake8` para analizar el código (no es necesario el resto de las dependencias, puesto que no haremos build).
- `Analysing the code with flake8`: se corre `flake8` para todos los archivos `.py`

**Archivo**

```
name: Flake8

on:
  pull_request:
    types: [opened, ready_for_review, synchronize, reopened]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11"]
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8
    - name: Analysing the code with flake8
      run: |
        flake8 $(git ls-files '*.py')
```

_Cabe destacar que se tiene un Makefile para arreglar errores de pep8 con `autopep8` de manera local_

### **Build y test**

Cuando se hace un push a la rama `main` y un pull request hacia esta misma, automáticamente se corre este workflow para asegurar que la aplicación sea capaz de levantarse y corran todos los tests.

**Importante:** este workflow se implementó para cumplir con el bonus, el test está en el archivo `api/test_app.py`

Se siguen los siguientes pasos:

- `Checkout the files`: paso de checkout básico para utilizar el workspace de github
- `Set up Python`: se define el Python a utilizar, en nuestro caso estamos utilizando 3.11
- `Install dependencies`: se instalan las dependencias para correr la api.
- `Test with pytest`: se corre `pytest`.

**Archivo**

```
name: Build application

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

permissions:
  contents: read

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v3
        with:
          python-version: "3.11"
      - name: Install dependencies
        working-directory: ./api
        run: |
          python -m pip install --upgrade pip
          pip install flake8 pytest
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Test with pytest
        working-directory: ./api
        run: |
          pytest
```

---

## **Frontend**

Aparte del setup de ramas y proyecto en general, puesto que estamos utilizando una aplicación React simple, no hay workflows de CI, pero si CD.

### **Secretos de repositorio**

En este caso, se ocupo la acción s3-sync, por lo que simplemente generamos un par de llaves y se las dimos al repositorio (la pública y secreta), los nombres respectivos son:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

### **Script de deploy**

Se siguen los siguientes pasos:

- `Checkout the files`: paso de checkout básico para utilizar el workspace de github
- `Setup node`: se instala el node para construir la app (en nuestro caso v16)
- `Install dependencies`: se instalan las dependencias necesarias
- `Build`: se construye la app. Como el sitio es estático, este paso es necesario para generar los archivos HTML/CSS/JS para subirlos al bucket.
- `Deploy to S3`: se suben al bucket los archivos que se generaron en el directorio `build`, mencionados anteriormente

**Archivo**

```
name: Deploy Frontend

on:
  push:
    branches:
    - main
jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup node
        uses: actions/setup-node@v3
        with:
          node-version: 16
      - name: Install dependencies
        run: npm install
      - name: Build
        run: npm run build

      - name: Deploy to S3
        uses: jakejarvis/s3-sync-action@master
        with:
          args: --acl public-read --delete
        env:
          AWS_S3_BUCKET: entrega-arqui
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY}}
          AWS_REGION: us-east-2
          SOURCE_DIR: "build"
```
