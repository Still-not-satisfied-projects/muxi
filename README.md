Water
===

	a python web framework baseon werkzeug~jinja~mana

	yes, it's on the top of flask

## GET Water

	pip install water

## So... Water
First, you need to go to terminal, and use mana to init water project!

	$ mana init WaterExample

Then, open app/__init__.py, create your water application

	from water import Warter

	app = Warter(__name__)

	from . import views

What's more, open app/views.py, and write views

	from . import app

	@app.url('/water')
	def water():
		return "<h1>I want to drink water:) </h1>"

now, you can run your water app

	$ mana manage WaterExample
	$ python manage.py runserver

this water app running on http://127.0.0.1:4399/water
