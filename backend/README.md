# Inventory Management Backend

Este es el backend del proyecto.

## Ejecutar

Se debe ejecutar el comando `python manage.py makemigrations` para realizar la migración de los modelos generados en el api rest y el comando `python manage.py migrate`.

para arrancar el servidor hay que ejecutar este comando `python manage.py runserver` luego de esto acceder a `http://localhost:8000/doc`; allí encontraras la documentación del api.

## Coverage

Para generar el coverage podemos usar los comandos `coverage run manage.py test` y el comando `coverage report` y por ultimo para generar lo en un formato visible en html se usa el comando `coverage html`.
