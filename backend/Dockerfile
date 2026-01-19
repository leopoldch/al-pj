FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-dev --no-install-project

COPY . /app/

RUN uv sync --frozen --no-dev

RUN DJANGO_SETTINGS_MODULE=backend.settings_test SECRET_KEY=build-key uv run python manage.py collectstatic --noinput

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
    uv run daphne -b 0.0.0.0 -p 8000 backend.asgi:application"]