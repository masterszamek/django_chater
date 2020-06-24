### Django Chater 
Simple group chat application written in django with trello

## Online preview
[Chat server](http://maciex.myddns.me)

## Requirements:
* Python 3.6.X
* Redis 4.X.X
* VirtualEnv(Optionaly)

## Technologies:
* django
* django rest framework (rest-api branch)
* channels
* redis
* JWT (rest-api branch)

## Instalation
* pip3 install -r requirements.txt
* pip3 manage.py migrate
* pip3 manage.py makemigrations

## Run
* Run redis-server
* python3 manage.py runserver

## Goal
Make better chater than slack

## Future
I'm currently rewriting that chat using django rest framework and react on client side
* Rest-api branch -> server side using django rest framework
* [Client side](https://github.com/masterszamek/django_chater-front_end) -> repository contain client side app