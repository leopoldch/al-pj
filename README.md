# Personal Website for Me and My Girlfriend ❤️🌸

This project consists of a **frontend** developed with **React** and a **backend** powered by **Django**.  
It is intended for deployment via **Docker Compose** for production environments.

---

## Frontend

Technologies: **React**, **Material-UI (MUI)**, **React Query**

### Installation and Usage

```bash

cd frontend/

npm install

npm start

npm run lint:fix

npm run format
```

---

## Backend

Technology: **Django**

### Installation and Usage

> Make sure to have poetry installed and ready to use (necessary to run the app)

```bash

cd backend

poetry shell

poetry install

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

```

---

## Production Deployment

The application is containerized using **Docker Compose**.

### Required Environment Variables

Before running `docker-compose up`, configure the following environment variables:

| Variable            | Description                           | Example                   |
|---------------------|---------------------------------------|----------------------------|
| `DEBUG`             | Enable debug mode (`True`/`False`)    | `True`                     |
| `SECRET_KEY`        | Django secret key                     | `your-secret-key`          |
| `ALLOWED_HOSTS`     | Comma-separated allowed hosts         | `127.0.0.1,localhost,example.fr` |
| `ALLOWED_CORS`      | Allowed CORS origins                  | `example.fr`               |
| `DATABASE_NAME`     | Database name                         | `dbname`                   |
| `DATABASE_PASSWORD` | Database user password                | `dbpass`                   |
| `DATABASE_USERNAME` | Database username                     | `dbusername`               |
| `DATABASE_HOST`     | Database host                         | `db.example.fr`            |
| `DATABASE_PORT`     | Database port                         | `3306`                     |
| `MAIL_HOST`         | SMTP server host                      | `smtp.example.com`         |
| `MAIL_PORT`         | SMTP server port                      | `587`                      |
| `MAIL_USERNAME`     | SMTP username                         | `user@example.com`         |
| `MAIL_PASSWORD`     | SMTP password                         | `your-password`            |
| `AWS_ACCESS_SECRET` | AWS secret key                        | `xxxxxxxxxxxxx`            |
| `AWS_BUCKET_NAME`   | AWS bucket name                       | `my-bucket-name`           |
| `AWS_REGION`        | AWS region you are using              | `eu-west-3`                |
| `AWS_ACCESS_KEY`    | AWS access key                        | `abcdefgh`                 |


### Launching using docker-composer

> MAKE SURE TO HAVE DECLARED THE ENV VARIABLES BEFORE RUNNING THE COMMAND BELOW

```bash
docker-compose up --build
```
