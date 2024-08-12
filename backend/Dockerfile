# Usa una imagen base oficial de Python
FROM python:3.10-alpine

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

RUN  apk update \
	&& apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev \
	&& pip install --upgrade pip

# Copia el archivo de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

# Establece el comando por defecto para ejecutar la aplicación
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py runserver 0.0.0.0:8000"]
