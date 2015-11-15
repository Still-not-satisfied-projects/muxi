# coding: utf-8
"""
	love
    ~~~~~~~
		this is a love project
"""

from muxi import Muxi


app = Muxi(__name__)


from . import views, forms
