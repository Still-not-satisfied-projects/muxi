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
	return {'name':"muxi", 'name2':"muxi"}


if __name__ == "__main__":
	app.run(debug=True)
