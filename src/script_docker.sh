#!/bin/bash

# Iniciar o nginx
# nginx -g 'daemon off;' &

# Iniciar o venv
cd /app/src
source /app/.venv/bin/activate

# Iniciar o Gunicorn
gunicorn -c /app/gunicorn_prod.py
