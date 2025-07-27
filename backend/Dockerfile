FROM python:3.12-slim AS builder

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && \
    pip install "poetry==$POETRY_VERSION" && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root

RUN pip install daphne

COPY . /app/

RUN poetry run python manage.py collectstatic --noinput

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 8000

CMD ["/bin/sh", "-c", "\
    : ${DEBUG:?Missing DEBUG} && \
    : ${SECRET_KEY:?Missing SECRET_KEY} && \
    : ${DATABASE_NAME:?Missing DATABASE_NAME} && \
    : ${DATABASE_USERNAME:?Missing DATABASE_USERNAME} && \
    : ${DATABASE_PASSWORD:?Missing DATABASE_PASSWORD} && \
    : ${DATABASE_HOST:?Missing DATABASE_HOST} && \
    : ${DATABASE_PORT:?Missing DATABASE_PORT} && \
    : ${MAIL_HOST:?Missing MAIL_HOST} && \
    : ${MAIL_PORT:?Missing MAIL_PORT} && \
    : ${MAIL_USERNAME:?Missing MAIL_USERNAME} && \
    : ${MAIL_PASSWORD:?Missing MAIL_PASSWORD} && \
    : ${ALLOWED_HOSTS:?Missing ALLOWED_HOSTS} && \
    : ${ALLOWED_CORS:?Missing ALLOWED_CORS} && \
    python manage.py migrate --noinput && \
    daphne -b 0.0.0.0 -p 8000 backend.asgi:application"]
