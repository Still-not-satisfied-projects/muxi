# coding: utf-8

"""
	views.py
	~~~~~~~~

		views functions
"""

from muxi import url, views
from . import app


@url(app, "/index")
@views("index.html")  # title, name
def index():
	return {
		"title":"first project",
		"name":"neo1218"
		}
