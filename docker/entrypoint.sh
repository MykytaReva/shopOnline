#!/bin/bash

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn settings.wsgi:application -b 0.0.0.0:8000 --timeout 180 -k gevent