# coding: utf-8


from . import app
from muxi import url, views
from .forms import TestForm


@url(app, "/test")
@views("test.html")  # TestForm obj
def test():
	form = TestForm()
	return {'form':form}
