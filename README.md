Muxi
===

	a python web framework baseon werkzeug~jinja~mana

	yes, it's on the top of flask

## GET Muxi

	pip install muxi

## First Muxi App
First, you need to go to terminal, and use mana to init muxi project!

	$ mana init MuxiExample

Then, open app/__init__.py, create your muxi application

	from muxi import Muxi

	app = Muxi(__name__)

	from . import views

What's more, open app/views.py, and write views

	from . import app

	@app.url('/muxi')
	def muxi():
		return "<h1>I like muxi :) </h1>"

now, you can run your muxi app

	$ mana manage MuxiExample
	$ python manage.py runserver

this muxi app running on http://127.0.0.1:4399/muxi

## font-end template
muxi use jinja as font-end template

## SQL ORM
muxi use sqlalchemy as SQL ORM. <br/>
what you need todo is create 'models.py' and coding

	from muxi import db

	class User(db.Model):
		coding...

## DataBase
create migration floder to record database migrate

	python manage.py db init

create database and first migrate

	python manage.py db migrate -m "some note"

update database

	python manage.py db upgrade

teardown database

	config this option:
	app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

	and the database would be automatically teardown when sth oops...
