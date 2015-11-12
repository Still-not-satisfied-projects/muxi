# coding: utf-8

"""
   _base.py
   ~~~~~~~~

        基础预填代码
            app/__init__.py
"""


_init_py ='''# coding: utf-8
"""

    ~~~~~~~

"""

from muxi import Muxi


app = Muxi(__name__)


from . import views, forms
'''


_init_sql_py = '''# coding: utf-8
"""

    ~~~~~~~

"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


app = Flask(__name__)


app.config.from_object(config['default'])


db = SQLAlchemy(app)


from . import views, models, forms
'''


_init_config_py='''# coding: utf-8
"""

    ~~~~~~~~

"""

from flask import Flask
from config import config

app = Flask(__name__)


app.config.from_object(config['default'])


from . import views, models, forms
'''
