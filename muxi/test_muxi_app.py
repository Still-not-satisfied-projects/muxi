# coding: utf-8
"""
	test_muxi_app.py
	~~~~~~~~~~~~~~~~

		test create muxi app
"""

from muxi import Muxi
from muxi import Response


app = Muxi('test_muxi_app')
app.secret_key = "I love muxi"


@app.url('/muxi')
def muxi():
	return Response(
			"<h1>Hello Muxi!</h1>"
			)


if __name__ == "__main__":
	app.run(debug=True)
