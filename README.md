🌼 木Muxi犀🌸 
===

	a python web framework

### =====================start=========================
## GET Muxi

	pip install muxi

## First Muxi Project
at First, you need to go to terminal, and init your muxi project!

	$ muxi init MuxiExample

init will automatically create muxi application :) <br/>
and Then, open app/views.py, and write views(sth you want to response)

	from . import app

	@url(app, '/muxi')
	def muxi():
		return "<h1>Hello Muxi</h1>"

now, you can run your muxi app

	$ python manage.py run

this muxi app running on http://127.0.0.1:3044/muxi
### =====================detail=========================

#### very easy but powerful !

## Debug Mode

	DebugToolbar

## Font-end Template
muxi use jinja2 as font-end template <br/>
you can use ~@views~ to add jinja template in your Response, and <br/>
use dict to push sth into jinja


	from . import app

	@views("muxi.html")
	@url(app, "/muxi/name")
	def muxi(name):
		name = "neo1218"
		return {name = name}

## SQL ORM
muxi use sqlalchemy as SQL ORM. <br/>
what you need todo is create 'app/models.py' and coding

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

## Form System

## Admin Site

## Rest API

## NoSql DataBase

## Isolate App

## Manage Muxi Project
muxi use manage.py script to manage your muxi project, you can see:<br/>
we can use manage to run your project and create & update your database and<br/>
get into shell, and deploy your project

	you can also config the ~manage.py~ script file by yourself :)

### :About Name:

	The original meaning of 木犀(muxi) is {{ a sweet-scented osmanthus }} and
	used as my :team name ~ MuxiStudio:
	beacause I love my team, so I chose muxi as this web framework's name

![muxi](http://7xj431.com1.z0.glb.clouddn.com/slogan_bg.png)
