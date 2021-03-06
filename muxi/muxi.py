# coding: utf-8
"""
    muxi
	~~~~

        :a decorated python web framework:
		:copyright: (c) 2016 by neo1218(朱承浩)
"""

# models import
# basic models
from basedir import _basedir
import os
import sys
import pkg_resources
from threading import local

# werkzeug
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug import LocalStack, LocalProxy
from werkzeug.exceptions import HTTPException
from werkzeug.contrib.securecookie import SecureCookie
from werkzeug.test import create_environ
from werkzeug.test import create_environ
environ = create_environ()

# jinja
from jinja2 import Environment, PackageLoader

# try to import the json helpers
# simplejson is more efficient than json, so
# we first want import simplejson, if it meet ImportError
# than import json
try:
	from simplejson import loads as load_json, dumps as dump_json
except ImportError:
	try:
		from json import loads as load_json, dumps as dump_json
	except ImportError:
		pass

# models not used in this file but are exported as public interface
from werkzeug import abort, redirect, secure_filename, cached_property,\
		html, import_string, generate_password_hash, check_password_hash
from jinja2 import Markup, escape


# context locals
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_request_ctx_stack = LocalStack()							  #|
current_app = LocalProxy(lambda: _request_ctx_stack.top.app)  #|
request = LocalProxy(lambda: _request_ctx_stack.top.request)  #|
session = LocalProxy(lambda: _request_ctx_stack.top.session)  #|
g = LocalProxy(lambda: _request_ctx_stack.top.g)              #|
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# I love MuxiStudio


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
			mimetype = "text/json"
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
		@url(app, "/muxi")
		@views("muxi.html")
		def muxi():
			return {"name":"name"}
	"""
	def _views(view_func):
		def __views(*args):
			context = view_func(*args)
			return current_app.jinja_env.get_template(template).render(**context)
		return __views
	return _views


def url(app, rule, **options):
	"""
	@url:
	a decorator that is used to register a view function
	for a given URL rule
	:ex:
		@url(app,'/index', methods=["GET"])
		@views('index.html')
		def index():
			return
	we may be notice that we should wrap the views decorator
	into url decorator, which to protect the request context
	"""
	def decorator(f):
		if 'endpoint' not in options:
			options['endpoint'] = f.__name__
		app.url_map.add(Rule(rule, **options))
		app.view_functions[options['endpoint']] = f
		return f
	return decorator


class ActiveRequestContext(object):
	"""
	a context manage class:
	~_request_ctx_stack~ store the active request context
	"""
	def __init__(self, app, environ):
		self.app = app
		self.environ = environ

	def __enter__(self):
		_request_ctx_stack.push(_RequestContext(self.app, self.environ))

	def __exit__(self, *unused):
		_request_ctx_stack.pop()


class Muxi(object):
	"""
	The :class~Muxi: obj implements a WSGI application and
	automatically config the app & register view functions through
	the name of the module or package passed.
	:ex:

		from muxi import Muxi
		app = Muxi(__name__)
		app.secret_key = "I love muxi"

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
		# endpoint => views func -> dict
		self.view_functions = {}
		# error => error handle func -> dict
		self.error_handlers = {}
		# the func run before request
		self.request_init_funcs = []
		self.request_shutdown_functions = []
		self.url_map = Map()
		self.secret_key = "I love muxi"


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
				# jinja_env globals
				gen_url = gen_url,
				request = request,
				# so we can use session in jinja
				session = session,
				g = g,
				get_show_msg = get_show_msg
				)


	def create_jinja_loader(self):
		"""create jinja loader,which can auto find templates floder"""
		return PackageLoader(self.package_name)


	def run(self, host="localhost", port=3044, **options):
		"""run muxi application~:root URL:~http://muxihost:304"""
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


	def open_resource(self, resource):
		"""
		open a resource from app's resource floder
		return a readable file-like object for specified resource
		"""
		return pkg_resources.resource_stream(self.package_name, resource)


	def open_session(self, resource):
		"""creates or opens a new session"""
		key = self.secret_key
		if key is not None:
			return SecureCookie.load_cookie(
					# here, we should use global request
					# which is a context-local object
          # request,  # so this request is the global request...
					Request(environ),
					# request,
					self.session_cookie_name,
					secret_key=key
					)


	def save_session(self, session, response):
		"""Saves the session if it needs updates."""
		if session is not None:
			session.save_cookie(response, self.session_cookie_name)


	def request_init(self, f):
		"""registers a function to run before each request"""
		self.request_init_funcs.append(f)
		return f


	def preprocess_request(self):
		"""make sure return value is not None"""
		for func in self.request_init_funcs:
			rv = func()
			if rv is not None:
				return rv


	def match_request(self):
		"""
		match the current(active) URL according to the URL Map,
		and stores the endpoint and view arguments on the request obj,
		else:
			the exception is stored
		"""
		rv = _request_ctx_stack.top.url_adapter.match()
		request.endpoint, request.view_args = rv
		return rv


	def dispatch_request(self):
		"""
		When a request happend, matchs the URL and
		returns the return value of view function
		dispatch the URL to the viewfunction and
		also pass http code and info
		"""
		try:
			endpoint, values = self.match_request()
			return self.view_functions[endpoint](**values)
		except HTTPException, e:
			# still not handle error
			return e
		except Exception, e:
			return e


	def error_handler(self, code):
		"""
		a decorator:
			give a code and return a message
		:ex:
			@app.error_handler
			def page_not_found():
				return 'this page is not found', 404
		"""
		def decorator(f):
			self.error_handlers[code] = f
			return f
		return decorator


	def make_response(self, rv):
		"""
		turn a view function's rv(return~value) to
		a true response object
		"""
		if isinstance(rv, self.response_class):
			return rv
		if isinstance(rv, basestring):
			return self.response_class(rv)
		if isinstance(rv, tuple):
			return self.response_class(*rv)
		return self.response_class.force_type(rv, request.environ)


	def process_response(self, response):
		"""
		not need now:
		now I need:
		"""
		return response


	def wsgi_app(self, environ, start_response):
		"""
		muxi is a WSGI application
		more detail on {WSGI}
		[https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface]

		so: this is wsgi on web framework part
		"""
		with ActiveRequestContext(self, environ):
			rv = self.preprocess_request()
			if rv is None:
				# so: rv is a func return value which
				# run before request
				rv = self.dispatch_request()
			response = self.make_response(rv)
			# response = self.process_response(response)
			return response(environ, start_response)


	def __call__(self, environ, start_response):
		# call for `wsgi_app`
		return self.wsgi_app(environ, start_response)
