# coding: utf-8

"""
	test_muxi_session.py
	~~~~~~~~~~~~~~~~~~~~

		test session

"""

from muxi import session
from muxi import Muxi
from muxi import views, url, redirect, gen_url


# SECRET_KEY = "I love muxi"


app = Muxi(__name__)
# app.config.from_object(__name__)
# app.secret_key = "I love muxi"


# @url(app, "/index")
# @views("index.html")  # name
# def index():
# 	session['name'] = "neo1218"
# 	return {'session':session}


@url(app, "/muxi/<name>")
def muxi(name):
	if name == 'muxi':
		return redirect(gen_url("muxi", name="neo1218"))
	else:
		return "<h1>HELLO %s</h1>" % name


if __name__ == "__main__":
	app.run(debug=True)
