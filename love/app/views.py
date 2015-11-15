# coding: utf-8

from . import app
from muxi import url, views
from .forms import MuxiForm


@url(app, "/index")
@views("index.html")
def index():
	form = MuxiForm()
	return {'form':form}
