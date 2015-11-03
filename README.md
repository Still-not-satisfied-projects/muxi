Muxi
===

	a python web framework baseon werkzeug~jinja~mana

	yes, it's on the top of flask

## GET Muxi

	pip install muxi

## So... Muxi
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
