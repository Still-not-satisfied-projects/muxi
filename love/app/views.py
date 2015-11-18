# coding: utf-8

from . import app
from muxi import url, views
from .forms import MuxiForm


@url(app, "/test")
@views("index.html")
def test():
	# form = MuxiForm()
	# return {'form':form}
	return {}
