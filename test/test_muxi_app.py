# coding: utf-8

"""
	test_muxi_app.py
	~~~~~~~~~~~~~~~~

		test create muxi app
"""

from muxi import Muxi


app = Muxi(__name__)
app.secret_key = "I love muxi"


@app.url('/muxi')
def muxi():
	return "<h1>hello muxi</h1>"


if __name__ == "__main__":
	app.run(debug=True)
