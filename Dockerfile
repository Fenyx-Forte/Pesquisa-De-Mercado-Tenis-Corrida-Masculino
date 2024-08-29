FROM ubuntu:latest

# Instala nginx e supervisord
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor

# Dependencias python
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    make \
    build-essential \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    liblzma-dev \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    libbz2-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    libnss3-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libdb-dev \
    uuid-dev \
    libedit-dev \
    xz-utils \
    libxml2-dev \
    libxmlsec1-dev \
    python3-openssl

# pyenv
RUN curl https://pyenv.run | bash

# Variáveis de ambiente para o pyenv
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Instale o Python usando o pyenv
RUN bash -c "source ~/.bashrc && pyenv install 3.12.4 && pyenv global 3.12.4"

# Defina o Python 3.12.4 como versão global
ENV PATH="$PYENV_ROOT/versions/3.12.4/bin:$PATH"

# Verifique se o Python foi instalado corretamente
RUN python --version

# Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.3 python3 -
# Adicione o Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Ambiente virtual
WORKDIR /app

COPY pyproject.toml /app
COPY poetry.lock /app
RUN touch README.md

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN poetry install --without docs,jupyter,dev,testes,webscraping --no-root && rm -rf $POETRY_CACHE_DIR

# Configura o Nginx
WORKDIR /
COPY nginx.conf /etc/nginx/nginx.conf
COPY dash_app.conf /etc/nginx/conf.d/

# Arquivos na render
COPY .env /app
COPY gunicorn_prod.py /app

# Arquivos repositorios
COPY src /app/src
COPY assets /app/assets

# Define permissões de execução para o script
RUN chmod +x /app/src/script_docker.sh

# Expõe as portas necessárias
EXPOSE 8501

# Define o entrypoint para o supervisord
ENTRYPOINT [ "/app/src/script_docker.sh" ]
