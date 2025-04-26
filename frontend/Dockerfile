FROM node:20 AS builder

ARG REACT_APP_API_URL

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

FROM node:20-slim

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build

EXPOSE 3000

CMD ["/bin/sh", "-c", "\
    serve -s build -l 3000"]
