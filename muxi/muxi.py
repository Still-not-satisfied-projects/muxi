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

# try to import the json helpers
# simplejson is more efficient than json, so
# we first want import simplejson, except ImportError...
try:
	from simplejson import loads as load_json, dumps as dump_json
except ImportError:
	try:
		from json import loads as load_json, dumps as dump_json
	except ImportError:
		pass

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


def gen_url(endpoint, **values):
	"""
	generate a URL through the given endpoint
	:param endpoint:  the endpoint of the url(the name of the view function)
	:param values:  the variable arguments of the URL rule
	"""
	#  MapAdapter.build can build endpoint and value dict as url
	#  follow the URL Rule
	#
	#  :URL build ex:
	#  m = Map([
	#      Rule('/', endpoint='index'),
	#  	Rule('/downloads/', endpoint='downloads/index'),
	#  	Rule('/downloads/<int:id>', endpoint='downloads/show')
	#  ])
	#
	#  urls = m.bind("ex.com", "/")  # urls is :class~MapAdapter: obj
	#
	#  urls.build("index", {})
	#  ...-->  '/'
	#  urls.build("downloads/show", {'id':32})
	#  ...-->  '/downloads/32'
	#  urls.build("downloads/show", {'id':32}, force_external=True)
	#  ...-->  'http://ex.com/downloads/32'
	#  urls.build("index", {'q':'muxi'})
	#  ...-->  '/?q=muxi'
	#  urls.build("index", {'q':['I', 'love', 'muxi']})
	#  ...-->  '/?q=I&q=love&q=muxi'

	return _request_ctx_stack.top.url_adapter.build(endpoint, values)


def jsonified(**values):
	"""return a json response"""
	return current_app.response_class(
		dump_json(values),
		mimetype = "text/html"
	)


def show(message):
	"""show a message to the next request"""
	session['_flashes'] = session.get('_shows', []) + [message]
# well ~
# :func show: means show, but it actually "push" the message into session
# and we can use :func get_show_msg: in template to "pop" the message and
# what's more: remove them!
# here we go ~
def get_show_msg():
	"""
	:func get_show_msg: can pop the message to show in
	next request
	"""
	shows = _request_ctx_stack.top.shows
	if shows is None:
		_request_ctx_stack.top.shows = shows = session.pop('_shows', [])


def views(template):
	"""
	:decorator views:
	:ex:
		@views("muxi.html")
		@app.route("/muxi")
		def muxi(name):
			name = "muxi"
			return {name:name}
	"""
	def _views(view_func):
		def __views(*args, **kwargs):
			context = view_func(*args, **kwargs)
			return current_app.jinja_env.get_template(template).render(context)


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
