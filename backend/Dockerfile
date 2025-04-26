FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
 
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --only main

RUN pip install gunicorn

COPY . /app/

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
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --timeout 120"]
