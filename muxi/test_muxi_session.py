# coding: utf-8

"""
	test_muxi_session.py
	~~~~~~~~~~~~~~~~~~~~

		test session

"""

from muxi import session
from muxi import Muxi
from muxi import views, url, redirect, gen_url, request


app = Muxi(__name__)
app.secret_key = 'I love muxi'


@url(app, "/index")
# @views("index.html")  # name
def index():
	# app.secret_key = 'I love muxi'
	session["username"] = "neo1218"
	return "<h1>Hello %s</h1>" % session['username']
	# return "%s" % str(request.cookies)
	# name = request.args.get("name")
	# return "name = %s" % name
	# return "en..."

# so, I use session, but this session can not store anything !


@url(app, "/muxi")
# @views("index.html")  # session["username"]
def muxi():
	# return {'session':session}
	return "<h1>Hello %s</h1>" % session.get("username")


if __name__ == "__main__":
	app.run(debug=True)
