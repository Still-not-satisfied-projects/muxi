# coding: utf-8

from . import app
from muxi import url


@url(app, "/test")
def test():
	return "<h1>just for test</h1>"
