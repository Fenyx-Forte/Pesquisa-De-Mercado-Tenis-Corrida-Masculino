#!/bin/bash

# Iniciar o Nginx
service nginx start

# Iniciar o Gunicorn
exec gunicorn -c ../gunicorn_prod.py
