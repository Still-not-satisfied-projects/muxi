# coding: utf-8
"""
	wtfExample
    ~~~~~~~~~~

		using muxi form system
"""

from muxi import Muxi


app = Muxi(__name__)


from . import views, forms
