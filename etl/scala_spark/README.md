# Teoría de Lenguaje 75.31 - Trabajo Práctico - ETL de CSV de Kaggle

Esta carpeta contiene el código del ETL para generar la base de datos de propiedades que estan en venta o alquiler en la Ciudad de Buenos Aires de los años 2019, 2020 y 2021.

## Configuración

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```bash
UID= # ID de usuario (se puede obtener con el comando "id -u")
GID= # ID de grupo (se puede obtener con el comando "id -g")
SUPABASE_API_KEY= # API Key de Supabase
SUPABASE_API_URL= # URL de Supabase
DATABASE_URL= # URL de la base de datos de Supabase
DATABASE_USER= # Usuario de la base de datos de Supabase
DATABASE_PASSWORD= # Contraseña de la base de datos de Supabase
DATABASE_CSVS= # Nombre de la base de datos de donde se levantan los CSVs
DATABASE_PROPERTIES= # Nombre de la base de datos donde se guardan los datos históricos de las propiedades
```

## Ejecución

```bash
sudo make runAssembly
```

## Demo
Dado que se tuvo que hacer un video explicando el funcionamiento del ETL, en el archivo `Demo.zpln` se encuentra el notebook de Zeppelin con el código que se utilizó para la demostración.

Para visualizar el notebook, se puede bajar una extensión en Visual Studio Code llamada "Zeppelin Notebook" y abrir el archivo `Demo.zpln`.

También se puede visualizar el notebook corriendo un servidor de Zeppelin y subiendo el archivo `Demo.zpln`.