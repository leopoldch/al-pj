# Personal Website for Me and My Girlfriend ❤️🌸

This project consists of a **frontend** developed with **React** and a **backend** powered by **Django**.  
It allows for an easy production deployment via **Docker Compose** or local development.

---

## Quick Start (Production / Docker)

The easiest way to run the application is using Docker Compose.

### 1. Configure Environment Variables
Create a `.env` file in the root directory (or ensure these variables are available in your environment).  
See the [Environment Variables](#environment-variables) section below for details.

### 2. Run with Docker Compose
```bash
docker-compose up --build -d
```
The application will be accessible at `http://localhost:3000` (frontend) and `http://localhost:8000` (backend).

---

## Local Development (Without Docker)

If you prefer running services locally for development:

### Prerequisites
- **Node.js** (v20+)
- **Python** (v3.12+)
- **uv** (Fast Python package installer and resolver)
- **Redis** (Required for WebSocket/Channels functionality)

### 1. Database & Redis
Ensure you have a Postgres (or your configured DB) and Redis running.  
You can quickly start Redis with Docker if needed:
```bash
docker run -d -p 6379:6379 redis:7
```

### 2. Backend Setup
We use `uv` for blazing fast dependency management.

```bash
# From project root
uv sync

uv run python manage.py migrate

uv run python manage.py runserver
```

### 3. Frontend Setup

```bash
# From project root
npm run install-all

npm start
```

### 4. Code Quality
- **Backend Tests**: `uv run pytest`
- **Frontend Lint**: `npm run lint` or `npm run lint:fix`

---

## Environment Variables

Required variables for both Docker and local setups:

| Variable | Description | Example |
|---|---|---|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | `super-secret-key` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `ALLOWED_CORS` | Allowed CORS origins | `http://localhost:3000` |
| `DATABASE_NAME` | Database name | `al_db` |
| `DATABASE_USERNAME`| Database username | `postgres` |
| `DATABASE_PASSWORD`| Database password | `password` |
| `DATABASE_HOST` | Database host | `localhost` (or `db` in docker) |
| `DATABASE_PORT` | Database port | `5432` |
| `REDIS_HOST` | Redis host | `localhost` (or `redis` in docker)|
| `MAIL_HOST` | SMTP server host | `smtp.example.com` |
| `MAIL_PORT` | SMTP server port | `587` |
| `MAIL_USERNAME` | SMTP username | `user@example.com` |
| `MAIL_PASSWORD` | SMTP password | `password` |
| `AWS_ACCESS_KEY` | AWS Access Key | `AKI...` |
| `AWS_ACCESS_SECRET`| AWS Secret Key | `secret...` |
| `AWS_REGION` | AWS Region | `eu-west-3` |
| `AWS_BUCKET_NAME` | S3 Bucket Name | `my-bucket` |

### Optional Build Arguments (Docker)
| Variable | Description |
|---|---|
| `RELEASE_TAG` | Injects the release version (e.g., `v1.0.0`) into the footer. |
