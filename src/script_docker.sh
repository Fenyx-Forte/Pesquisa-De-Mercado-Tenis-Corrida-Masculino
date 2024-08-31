#!/bin/bash

# Iniciar o nginx
nginx -g 'daemon off;' &

# Iniciar o Gunicorn
cd /app/src
gunicorn -c /app/gunicorn_prod.py
