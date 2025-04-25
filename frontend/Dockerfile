FROM node:20 AS builder

ARG REACT_APP_API_URL

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

FROM node:20-slim

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/build ./build

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["serve", "-s", "build", "-l", "3000"]
