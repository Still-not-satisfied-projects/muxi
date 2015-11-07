# coding: utf-8
"""
	test_muxi_app.py
	~~~~~~~~~~~~~~~~

		test create muxi app
"""

from muxi import Muxi, url, _RequestContext
from werkzeug.test import create_environ
from werkzeug import LocalStack


# create wsgi
environ = create_environ()


app = Muxi('test_muxi_app')
app.secret_key = "I love muxi"


req_ctx = _RequestContext(app, environ)
_request_ctx_stack = LocalStack()


_request_ctx_stack.push(req_ctx)


# global request
request = _request_ctx_stack.top.request


@url(app, '/muxi')
def muxi():
	return "<h1>Hello Muxi!</h1>"


if __name__ == "__main__":
	app.run(debug=True)
