#!/bin/bash

python3 manage.py migrate --noinput

python3 manage.py collectstatic --noinput

celery -A settings worker --loglevel=INFO  --detach

celery -A settings beat --loglevel=INFO  --detach

gunicorn settings.wsgi:application --workers 4 -b 0.0.0.0:8000 --timeout 180 -k gevent --capture-output