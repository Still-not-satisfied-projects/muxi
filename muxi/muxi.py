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
from werkzeug.routing import Map, Rule
from werkzeug import LocalStack, LocalProxy

# jinja
from jinja2 import Environment, PackageLoader

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

	  MapAdapter.build can build endpoint and value dict as url
	  follow the URL Rule

	  :URL build ex:
	  m = Map([
		  Rule('/', endpoint='index'),
		Rule('/downloads/', endpoint='downloads/index'),
		Rule('/downloads/<int:id>', endpoint='downloads/show')
	  ])

	  urls = m.bind("ex.com", "/")  # urls is :class~MapAdapter: obj

	  urls.build("index", {})
	  ...-->  '/'
	  urls.build("downloads/show", {'id':32})
	  ...-->  '/downloads/32'
	  urls.build("downloads/show", {'id':32}, force_external=True)
	  ...-->  'http://ex.com/downloads/32'
	  urls.build("index", {'q':'muxi'})
	  ...-->  '/?q=muxi'
	  urls.build("index", {'q':['I', 'love', 'muxi']})
	  ...-->  '/?q=I&q=love&q=muxi'
	"""
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
	:ex:
		from muxi import Muxi
		app = Muxi(__name__)
	and app is ~WSGI~application
	"""

	# the class for request obj
	request_class = MuxiRequest

	# the class for response obj
	response_class = MuxiResponse

	# static path
	# path for the static file
	# if we don't want use static files
	# we can set this to None !
	static_path = '/static'

	# if secret_key is set, we can use this to
	# sign cookies or some auth info
	# follow this you can simple have a secret_key
	#	..--> import os
	#	..--> os.urandom(24)
	#	'YkB\xe4\x11\xef\xa0\xe4\x9e\x8cZ\xb2}^>T\x12a\x96\x90\xcc\xfd;b'
	# and it is better to set secret_key into environment variable
	secret_key = None

	session_cookie_name = 'session'

	# options that are passed directly to the jinja environment
	jinja_options = dict(
			autoescape = True,
			extensions = ['jinja2.ext.autoescape', 'jinja2.ext.with_']
			)

	def __init__(self, package_name):
		# app = Muxi(__name__)
		self.debug = False
		self.package_name = package_name
		self.view_functions = {}
		self.error_handlers = {}
		# the func run before request
		self.request_init_funcs = []
		self.request_shutdown_functions = []
		self.url_map = Map()

		if self.static_path is not None:
			# auto add ~endpoint:static~
			self.url_map.add(Rule(
				self.static_path + "/<filename>",
				build_only = True,
				endpoint = 'static'
				))

		self.jinja_env = Environment(loader=self.create_jinja_loader(),
				**self.jinja_options)

		self.jinja_env.globals.update(
				url_for = url_for,
				request = request,
				session = session,
				g = g,
				get_show_msg = get_show_msg
				)

		def create_jinja_loader(self):
			# create jinja loader
			# which can auto find templates floder
			return PackageLoader(self.package_name)

		def run(self,	host="muxihost", port=304, **options):
			# run muxi application~:root URL:~http://muxihost:304
			from werkzeug import run_simple
			if 'debug' in options:
				self.debug = options.pop('debug')
			if self.static_path is not None:
				options['static_files'] = {
						self.static_path:(self.package_name, 'static')
						}
			options.setdefault('use_reloader', self.debug)
			options.setdefault('use_debugger', self.debug)
			return run_simple(host, port, self, **options)

		@staticmethod
		def url(rule, **options):
			# @url:
			# a decorator that is used to register a view function
			# for a given URL rule
			# :ex:
			#	@url('app','/ )
			#	@views('index.html')
			#	def index():
			#		return
			def decorator(f):
				if 'endpoint' not in options:
					options['endpoint'] = f.__name__
				self.url_map.add(Rule(rule, **options))
				self.view_functons[options['endpoint']] = f
				return f
			return decorator

		def request_init(self, f):
			# registers a function to run before each request
			self.request_init_funcs.append(f)
			return f

		def preprocess_request(self):
			for func in self.request_init_funcs:
				rv = func()
				if rv is not None:
					return rv

		def match_request(self):
			# match the current(active) URL according to the URL Map,
			# and stores the endpoint and view arguments on the request obj,
			# else:
			# 	the exception is stored
			rv = _request_ctx_stack.top.url_adapter.match()
			request.endpoint, request.view_args = rv
			return rv

		def dispatch_request(self):
			# When a request happend, matchs the URL and
			# returns the return value of view
			# dispatch the URL to the viewfunction and
			# also pass http code and info
			try:
				endpoint, values = self.match_request()
				return self.view_functons[endpoint](**values)
			except HTTPException, e:
				# still not handle error
				return e
			except Exception, e:
				return e

		def make_response(self, rv):
			# turn a view function's rv(return~value) to
			# a true response object
			if isinstance(rv, self.response_class):
				return rv
			if isinstance(rv, basestring):
				return self.response_class(rv)
			if isinstance(rv, tuple):
				return self.response_class(*rv)
			return self.response_class.force_type(rv, request.environ)

		def process_response(self, response):
			# not need now
			return response

		def wsgi_app(self, environ, start_response):
			"""
			muxi is a WSGI application
			more detail on {WSGI}
			[https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface]
			"""
			_request_ctx_stack.push(_RequestContext(self, environ))
			try:
				rv = self.preprocess_request()
				if rv is None:
					# so: rv is a func return value which
					# run before request
					rv = self.dispatch_request()
				response = self.make_response(rv)
				response = self.process_response(response)
				return response(environ, start_response)
			finally:
				_request_ctx_stack.pop()

		def __call__(self, environ, start_response):
			# call for `wsgi_app`
			return self.wsgi_app(environ, start_response)


# context locals
# make the ~global~ctx proxy the local~but~active ctx
# LocalStack == Local + "stack"~pop&push
# _request_ctx_stack.top == _request_ctx_stack._local.stack[-1]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_request_ctx_stack = LocalStack()							 #|
current_app = LocalProxy(lambda: _request_ctx_stack.top.app) #|
request = LocalProxy(lambda: _request_ctx_stack.top.request) #|
session = LocalProxy(lambda: _request_ctx_stack.top.session) #|
g = LocalProxy(lambda: _request_ctx_stack.top.g)             #|
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# I love MuxiStudio
