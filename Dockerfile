# nginx
FROM nginx:latest AS stage_nginx


# The builder image, used to build the virtual environment
FROM python:3.12.5-bookworm AS stage_builder

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 -
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml /app
COPY poetry.lock /app
RUN touch README.md && \
    poetry install --without etl,docs,jupyter,dev,testes,webscraping --no-root && rm -rf $POETRY_CACHE_DIR


# The runtime image, used to just run the code provided its virtual environment
FROM python:3.12.5-slim-bookworm AS stage_runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copia o virtual environment do poetry
COPY --from=stage_builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copia os binários e configurações necessários do nginx
COPY --from=stage_nginx /etc/nginx /etc/nginx
COPY --from=stage_nginx /usr/sbin/nginx /usr/sbin/nginx
COPY --from=stage_nginx /usr/lib/nginx /usr/lib/nginx
COPY --from=stage_nginx /var/log/nginx /var/log/nginx
COPY --from=stage_nginx /var/cache/nginx /var/cache/nginx
COPY --from=stage_nginx /usr/share/nginx /usr/share/nginx

# nginx
RUN mkdir -p /var/run/nginx && \
    chown -R www-data:www-data /var/run/nginx /var/log/nginx /var/cache/nginx /usr/lib/nginx /usr/share/nginx && \
    chmod 750 /usr/sbin/nginx && \
    chmod -R 750 /var/run/nginx /var/log/nginx /var/cache/nginx && \
    chmod -R 640 /etc/nginx

# gunicorn
RUN mkdir -p /var/log/gunicorn && \
    mkdir -p /var/run/gunicorn && \
    touch /var/run/gunicorn/gunicorn_prod.pid && \
    # touch /var/log/gunicorn/access.log && \
    # touch /var/log/gunicorn/error.log && \
    chown -R www-data:www-data /var/run/gunicorn && \
    chown -R www-data:www-data /var/log/gunicorn

# Copiar arquivos para o container
COPY nginx.conf /etc/nginx/nginx.conf
COPY dash_app.conf /etc/nginx/conf.d/
COPY gunicorn_prod.py /app
# COPY .env /app
COPY src /app/src
COPY assets /usr/share/nginx/html/assets
COPY /dados/duckdb_database.db /app/dados/duckdb_database.db

# Permissões para o nginx acessar assets
RUN chown -R www-data:www-data /usr/share/nginx/html/assets && \
    find /usr/share/nginx/html/assets -type d -exec chmod 750 {} \; && \
    find /usr/share/nginx/html/assets -type f -exec chmod 640 {} \;

# Define permissões de execução para o script
RUN chmod +x /app/src/script_docker.sh

# Instalacao extensao postgresql
# COPY extensao_postgresql.py /app
# RUN python /app/extensao_postgresql.py

ENTRYPOINT ["/app/src/script_docker.sh"]
