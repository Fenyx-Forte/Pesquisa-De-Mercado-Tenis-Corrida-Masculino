#!/bin/bash

# nginx
mkdir -p /var/log/nginx
touch ./var/log/nginx/error.log
touch ./var/log/nginx/access.log

# dash_app
touch ./var/log/nginx/dash_app.access.log
touch ./var/log/nginx/dash_app.error.log

chown -R www-data:www-data /var/log/nginx

# gunicorn
mkdir -p /var/log/gunicorn
touch ./var/log/gunicorn/access.log
touch ./var/log/gunicorn/error.log

chown -R www-data:www-data /var/log/gunicorn

# Iniciar o nginx
nginx -g 'daemon off;' &

cd src/

# Iniciar o Gunicorn
gunicorn -c ../gunicorn_prod.py
