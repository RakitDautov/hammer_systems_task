#! /bin/bash

python3 manage.py makemigrations users

python3 manage.py migrate --no-input

python3 manage.py collectstatic --no-input

gunicorn api_referal.wsgi:application --bind 0.0.0.0:8000