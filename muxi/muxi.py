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
from werkzeug.wrappers import Request, Response

# jinja

# mana

# models not used in this file but are exported as public interface


class MuxiRequest(Request):
	"""this request obj used by default in muxi"""

	def __init__(self, environ):
		Request.__init__(self, environ)
		self.endpoint = None
		self.view_args = None


class MuxiResponse(Response):
	"""
	Response obj used by default in muxi
	but set default mimetype as html
	"""
	default_mimetype = 'text/html'


class _RequestGlobals(object):
	pass


class _RequestContext(object):
	"""
	request context contains all request relevant info,
	it is created at the beginning of the request and
	pushed to :_request_ctx_stack: and
	removed at the end of it,
	it will create the URL adapter and request obj for
	the WSGI environment provided.
	"""

	def __init__(self, app, environ):
		self.app = app
		self.url_adapter = app.url_map.bind_to_environ(environ)
		self.request = app.request_class(environ)
		self.session = app.open_session(self.request)
		# g is in request ctx
		# and used to store anything
		self.g = _RequestGlobals()
		self.showes = None


class Muxi(object):
	"""
	The :class~Muxi: obj implements a WSGI application and
	automatically config the app & register view functions through
	the name of the module or package passed.
	"""

	# the class for request obj
	request_class = MuxiRequest

	# the class for response obj
	response_class = MuxiResponse
