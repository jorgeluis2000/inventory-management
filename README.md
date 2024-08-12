# Inventory Management

Es un pequeño desarrollo para administrar los inventarios de una empresa y las ventas.

## Pre requisitos

Se requieren ciertos requisitos para ejecutar el desarrollo, algunos son opcionales, a continuación se listaran.

1. Tener Docker y Docker Compose instalados ***`(opcional)`***.

2. Tener python en su versión 3.10.

3. Tener NodeJs en su versión 3.18 o 3.20+.

## Funcionalidades

El desarrollo tiene una serie de funcionalidades que al ejecutar el backend podrás acceder a las diferentes funcionalidades o ver su api desde la ruta `/docs`. A continuación se listan las diferentes funcionalidades que puedes encontrar en el desarrollo.

**1. Crear usuario:** El aplicativo tiene la manera para registrar nuevos usuarios para que puedan acceder a las demás funcionalidades.

**2. Iniciar sección:** El aplicativo permite el inicio de sección por un token de autenticación.

**3. Cerrar sección:** El aplicativo permite borrar el token de autenticación para asegurar que nadie más pueda editar información con dicho usuario.

**4. Listar productos:** El aplicativo permite listar todos los productos registrados.

**5. Agregar productos:** El aplicativo permite agregar productos.

**6. Actualizar productos:** El aplicativo permite actualizar los productos.

**7. Listar facturas:** El aplicativo permite listar las facturas generados.

**8. Crear facturas:** El aplicativo permite generar facturas.

**9. Agregar producto a la facturas:** El aplicativo permite agregar productos a la factura.

**10. Pagar facturas:** El aplicativo permite **pagar** la factura.

**11. Cancelar facturas:** El aplicativo permite **cancelar** la factura.

**12. Eliminar facturas:** El aplicativo permite **eliminar** la factura.

**13. Desvincular producto de la facturas:** El aplicativo permite **eliminar** productos o **desvincularlos** de la factura.

## Ejecutar programa desde Docker Compose

El programa se deja ejecutar desde docker compose pero debes seguir los siguientes pasos.

1. Se debe crear la **base de datos** por lo que se ejecuta el comando `docker compose up -d django-db`, aquí se esperan un momento para que la **base de datos** inicialice las tablas y los procedimientos almacenados.

2. Se debe crear un archivo `.env` en la carpeta `frontend` que contenga esto `VITE_API_URL=http://localhost:8000`.

3. Se debe desplegar el **backend** como el **frontend** por lo que se ejecuta ya este comando `docker compose up -d --build`, se espera un poco para que el backend cree o genere el usuario admin que inicializara las tablas de usuario y autenticación.

4. Luego de esto ya puede acceder a la documentación de la api desde `http://localhost:8000/docs` y además ya puedes acceder al frontend y crear un nuevo usuario para probar todas las funcionalidades del aplicativo.

## Ejecutar programa desde la propia maquina

1. Se debe tener ya una base de datos y tomar todo el contenido que se encuentra en el archivo `init.db` ubicado en la carpeta `backend`, este debera ser ejecutado dentro de la db para que se generen las tablas y procedimientos.

2. Se deberá crear un archivo llamado `.env` dentro de la carpeta `backend` que contenga esto:

```env
DATABASE_URL="postgres://<user>:<password>@<host>:<port>/inventory_management"
DEBUG=True
```

> Procura remplazar el environment DATABASE_URL por el que te da tu db y si deseas puedes desactivar el modo DEBUG cambiándolo por **`False`**.

3. Se deberá ejecutar los siguiente comando estando dentro de la carpeta backend para ejecutar el backend.

```bash
pip install -r requirements.txt
python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py runserver 0.0.0.0:8000
```

4. Se debe crear un archivo `.env` en la carpeta `frontend` que contenga esto `VITE_API_URL=http://localhost:8000`.

5. Para ejecutar el front-end del desarrollo se deberá primero ejecutar `pnpm i` o `npm i`, luego se deberá ejecutar el siguiente comando.

```bash
pnpm run dev --port 8282 --host
```

o

```bash
npm run dev --port 8282 --host
```

Ahora a probar las funcionalidades!!