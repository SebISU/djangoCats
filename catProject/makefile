
all:
	@ echo "Check available commands."

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

requirements:
	pip3 install -r requirements.txt

migration:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createadmin

run:
	python manage.py runserver 0.0.0.0:80


.PHONY: requirements clean-pyc migration migrate superuser run

