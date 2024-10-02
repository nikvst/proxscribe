FROM python:3.12-slim as base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends \
    gettext \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD pyproject.toml /app
ADD uv.lock /app
ADD .env.ci /app/.env

RUN uv sync --frozen --no-dev

ADD src /app

RUN uv run python ./manage.py collectstatic --noinput

RUN rm /app/.env

EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000" ]
