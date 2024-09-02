#!/bin/bash

# Iniciar o Gunicorn
cd /app/src
gunicorn -c /app/gunicorn_prod.py &

# Iniciar o nginx
nginx -g 'daemon off;'
