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