# coding: utf-8
"""
	木muxi犀
	~~~~~~~~

		a python web framework ~ on top of flask
		baseon werkzeug ~ jinja ~ mana

		:copyright: (c) 2015 by neo1218(朱承浩)
		:license: MIT, see LICENSE for more details.
"""

# models import
# basic models
from basedir import _basedir

# werkzeug
from werkzeug.wrappers import Request

# jinja

# mana

# models not used in this file but are exported as public interface


class MuxiRequest(Request):
	"""this request obj used by default in muxi"""

	def __init__(self, environ):
		Request.__init__(self, environ)
		self.endpoint = None
		self.view_args = None
