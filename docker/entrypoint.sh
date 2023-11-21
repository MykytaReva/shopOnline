#!/bin/bash

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

gunicorn settings.wsgi:application --workers 4 -b 0.0.0.0:8000 --timeout 180 -k gevent --capture-output