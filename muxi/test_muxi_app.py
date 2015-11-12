# coding: utf-8
"""
	test_muxi_app.py
	~~~~~~~~~~~~~~~~

		test create muxi app
"""

from muxi import Muxi, _RequestContext, url, views
from flask import render_template


app = Muxi(__name__)


@url(app, '/muxi')
@views("muxi.html")
def muxi():
	# so: context is just a dict
	# and when we push sth into the dict
	# we actually not push the variable
	# but the string
	# which means code generation
	return {'name':"muxi", 'name2':"muxi"}


if __name__ == "__main__":
	app.run(debug=True)
