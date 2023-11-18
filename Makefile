run:
	python app/manage.py runserver

shell:
	python app/manage.py shell

makemigrations:
	python app/manage.py makemigrations

migrate1:
	python app/manage.py migrate

migrate: makemigrations \
	migrate1

shell_plus:
	python app/manage.py shell_plus --print-sql

show_urls:
	python app/manage.py show_urls

celery:
	cd app && celery -A settings worker --loglevel=INFO

celery_beat:
	cd app && celery -A settings beat --loglevel=INFO

stripe:
	stripe listen --forward-to localhost:8000/payment/webhook/

gun:
	cd app && gunicorn settings.wsgi:application -c div.py