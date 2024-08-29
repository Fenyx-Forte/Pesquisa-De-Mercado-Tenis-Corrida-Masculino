#!/bin/bash

# Iniciar o Gunicorn
gunicorn -c ../gunicorn_prod.py
