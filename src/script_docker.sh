#!/bin/bash

# Iniciar o Nginx
sudo service nginx start

# Iniciar o Gunicorn
gunicorn -c ../gunicorn_prod.py
