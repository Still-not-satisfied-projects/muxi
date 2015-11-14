To Do List
===

	Ready To D0 :)

## 1. Fix ISSUE #2
https://github.com/neo1218/muxi/issues/2 <br/>

## 2. Form System

	from muxi.form import Form
	from muxi.form.field import StringField, SubmitField
	from muxi.form.validators import Required

	class EditForm(Form):
		username = StringField(validators=[Required()])
		submit = SubmitField("submit")

## 3. Sql ORM:(SQLAlchemy)
maybe like:

	from muxi import db

	class User(db.Model):
		coding....

## 4. Manage.py

	python manage.py runserver

	python manage.py db init
	python manage.py db migrate -m "#"
	python manage.py db upgrade

	python manage.py test

## What's More...

	ing ......
