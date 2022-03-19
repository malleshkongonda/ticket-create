#!/usr/bin/env bash

DB_FILE='db.sqlite3'
if [ ! -z $1 ]; then
    rm ${DB_FILE}
fi

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --user=maroshmka --email=maros@hmka.com

python3 manage.py runserver 0:8003
