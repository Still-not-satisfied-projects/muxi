# coding: utf-8

from app import app
from muxi import url, views


@url(app, '/muxi')
@views('muxi.html')  # name
def muxi():
  return {'name': 'neo1218'}
