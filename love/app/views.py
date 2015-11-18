# coding: utf-8

from . import app
from muxi import url, views, request
# from .forms import MuxiForm
from muxi.form import Form
from muxi.form.fields import StringField, SubmitField
from muxi.form.validators import Required
# from werkzeug.datastructures import MultiDict
# from flask.ext.wtf import Form
# from wtforms.fields import StringField, SubmitField
# from wtforms.validators import Required


class MuxiForm(Form):
	name = StringField(validators=[Required()])
	submit = SubmitField("submit")


@url(app, "/test")
# @views("index.html")
def test():
	# form = MuxiForm()  # so I think, flask-wtf will use request and request maybe the problem
	# return {'form':form}
	return "<h1>%s</h1>" % request.args.get('name')
