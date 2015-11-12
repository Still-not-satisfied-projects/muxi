# coding: utf-8

"""
	test_muxi_session.py
	~~~~~~~~~~~~~~~~~~~~

		test session

"""

from muxi import session
from muxi import Muxi
from muxi import views, url


app = Muxi(__name__)
app.secret_key = "I love muxi"


@url(app, "/index")
@views("index.html")  # name
def index():
	session['name'] = "neo1218"
	return {'session':session}


if __name__ == "__main__":
	app.run(debug=True)
