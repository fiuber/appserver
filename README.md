Build status:   [![Build Status](https://travis-ci.org/fiuber/appserver.svg?branch=master)](https://travis-ci.org/fiuber/appserver)

# Manual de configuracion e instalacion

## Instalacion
Para la instalacion del APP server de manera local se deberan seguir los siguientes pasos:

- Realizar un clone del repositorio de la siguiente forma "git clone https://github.com/fiuber/appserver.git" previamente navegando al directorio en el que se quiera clonar el repositorio.

- Correr el script ./lanzar que se encarga hacer el build de la imagen de docker y correrla exponiendo el puerto 5000.

- Ya se pueden realizar request al App Server en la direccion localhost:5000 con el programa postman o similar. 

Si en cambio se desea realizar pruebas al servidor de produccion se pueden enviar requests a la direccion "http://fiuberappserver.herokuapp.com/" donde esta el mismo. 

## Configuracion
Se incluye un archivo de configuracion por defecto pero el servidor puede ser configurado a gusto utilizando el archivo "__init__.py" ubicado en el directorio "src/" del App Server en donde se encuentran todos los parametros que se pueden variar del servidor tales como:

- "app.config['MONGO_DBNAME']": Es el nombre que tenga la base de datos en mongoDB.
- "app.config['MONGO_URI']": Las credenciales para acceder a la base de datos de mongoDB en formato URI.
- "directionsAPIKey": Es la clave del API de google Directions a utilizar en las request de rutas.
- "URLSharedServer": Direcction URL en la cual esta el Shared Server.

## Modelo de datos
En el siguiente enlace puede verse una descripcion del modelo de datos usado para almacenar la informacion en mongoDB:

https://github.com/fiuber/appserver/blob/master/documentacion/modelo%20de%20datos%20.pdf
