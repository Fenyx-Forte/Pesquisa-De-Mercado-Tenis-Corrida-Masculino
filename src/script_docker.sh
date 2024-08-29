#!/bin/bash

# Iniciar o Nginx
nginx

# Iniciar o Gunicorn
exec gunicorn -c ../gunicorn_prod.py
