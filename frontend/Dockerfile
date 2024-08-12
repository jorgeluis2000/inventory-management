# Usar una imagen de Node.js oficial como base
FROM node:18-alpine

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo package.json y package-lock.json al contenedor
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar todo el código fuente al contenedor
COPY . .

# Construir la aplicación
RUN npm run build

# Usar una imagen de servidor web para servir la aplicación
FROM nginx:stable-alpine

# Copiar los archivos construidos de la etapa anterior
COPY --from=0 /app/dist /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Comando para ejecutar Nginx
CMD ["nginx", "-g", "daemon off;"]
