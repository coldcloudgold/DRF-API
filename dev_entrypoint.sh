#! /bin/sh


rm -r dev_database.db Book/__pycache__/ Book/migrations/__pycache__/ Book/migrations/0001_initial.py Book/tests/__pycache__/ REST/__pycache__/


python manage.py makemigrations


python manage.py migrate


python manage.py loaddata fixtures/initial_data.json


python manage.py runserver 8080
