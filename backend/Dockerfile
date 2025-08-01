FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && \
    pip install "poetry==$POETRY_VERSION" && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main

RUN pip install daphne

COPY . /app/

RUN poetry run python manage.py collectstatic --noinput


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
    : ${AWS_ACCESS_KEY:?Missing AWS_ACCESS_KEY} && \
    : ${AWS_ACCESS_SECRET:?Missing AWS_ACCESS_SECRET} && \
    : ${AWS_REGION:?Missing AWS_REGION} && \
    : ${AWS_BUCKET_NAME:?Missing AWS_BUCKET_NAME} && \
    daphne -b 0.0.0.0 -p 8000 backend.asgi:application"]