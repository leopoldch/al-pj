# Personal Website for Me and My Girlfriend ❤️🌸

This project consists of a **frontend** developed with **React** and a **backend** powered by **Django**.  
It is intended for deployment via **Docker Compose** for production environments.

---

## Frontend

Technologies: **React**, **Material-UI (MUI)**, **React Query**

### Installation and Usage

```bash
npm install

npm start

npm run lint:fix

npm run format
```

---

## Backend

Technology: **Django**

### Installation and Usage

```bash
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

### Launching

```bash
docker-compose up --build
```

---

## TODO

- [ ] Add a development container
- [X] Add a `TODO` feature
- [ ] Write full testing suites (unit and integration tests)
- [X] Set up CI/CD (Continuous Integration and Delivery)
- [ ] Improve frontend responsiveness for mobile devices
- [X] Implement user authentication and authorization
- [X] Secure environment variables management (use `.env` file with Docker Compose)
- [X] Configure HTTPS for production
