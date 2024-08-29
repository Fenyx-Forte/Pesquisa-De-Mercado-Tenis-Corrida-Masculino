#!/bin/bash

# Iniciar o Nginx
/usr/sbin/nginx -g daemon off;

# Iniciar o Gunicorn
exec gunicorn -c ../gunicorn_prod.py;
