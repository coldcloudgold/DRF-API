#! /bin/sh


sleep 5


rm -r static/* Book/migrations/0001_initial.py


python3 manage.py makemigrations


python3 manage.py migrate


python3 manage.py loaddata fixtures/initial_data.json


python3 manage.py collectstatic


gunicorn REST.wsgi:application -b 0.0.0.0:8000 --reload
