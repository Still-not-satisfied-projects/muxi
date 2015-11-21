# coding: utf-8

from . import app
from muxi import url, views
from .forms import MuxiForm


@url(app, "/form")
def form():
	form = MuxiForm()
	return "<h1>great! ok! but... </h1>"
