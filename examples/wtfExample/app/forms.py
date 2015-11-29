# coding: utf-8

from muxi.form import Form
from muxi.form.fields import StringField, SubmitField


class TestForm(Form):
	username = StringField("username")
	submit = SubmitField("submit")
