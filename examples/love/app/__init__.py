# coding: utf-8
"""

    ~~~~~~~

"""

from muxi import Muxi
# from flask import Flask


app = Muxi(__name__)
app.secret_key = "I love muxi"
# app = Flask(__name__)


from . import views, forms
