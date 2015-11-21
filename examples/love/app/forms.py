# coding: utf-8

from muxi.form import Form
from muxi.form.fields import StringField, SubmitField
from muxi.form.validators import Required


class MuxiForm(Form):
	username = StringField(validators=[Required()])
	submit = SubmitField(validators=[Required()])
