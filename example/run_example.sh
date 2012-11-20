#!/bin/bash


echo -e "Running example...\n"                                       &&\

#################
    pip install -r requirements.txt                                  &&\

#################
    python manage.py syncdb --noinput                                &&\
    python -m app.init                                               &&\

#################
    echo -e "\n\n"                                                   &&\
    echo -e "   PLEASE VISIT ADMIN AT: http://127.0.0.1:8000/admin/" &&\
    echo -e "\n\n"                                                   &&\
    python manage.py runserver

