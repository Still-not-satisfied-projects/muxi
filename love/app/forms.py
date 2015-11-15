# coding: utf-8

from muxi.form import Form
from muxi.form.fields import StringField, SubmitField
from muxi.form.validators import Required


class MuxiForm(Form):
	name = StringField(validators=[Required()])
	submit = SubmitField("submit")
