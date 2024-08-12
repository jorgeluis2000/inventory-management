FROM node:20-alpine

WORKDIR /app
RUN npm i -g pnpm

ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}


COPY package*.json ./
COPY pnpm-lock.yaml ./

RUN pnpm i --frozen-lockfile

COPY . .

RUN pnpm build

CMD ["pnpm", "dev", "--port", "8282", "--host"]
