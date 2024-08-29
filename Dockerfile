# nginx setup
FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY dash_app.conf /etc/nginx/conf.d/

# The builder image, used to build the virtual environment
FROM python:3.12-bookworm AS builder

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 -

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN /root/.local/bin/poetry install --without docs,jupyter,dev,testes,webscraping --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12-slim-bookworm AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Arquivos na render
COPY .env /app

COPY gunicorn_prod.py /app

# Arquivos repositorios
COPY src /app/src

COPY assets /app/assets

# Define permissões de execução para o script
RUN chmod +x /app/src/script_docker.sh

EXPOSE 80
ENTRYPOINT ["/app/src/script_docker.sh"]
