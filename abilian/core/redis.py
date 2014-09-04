# coding=utf-8
"""
"""
from __future__ import absolute_import

from redis import from_url as redis_from_url
from flask import current_app

class Extension(object):
  """
  Redis extension for flask
  """
  client = None

  def __init__(self, app=None):
    if app is not None:
      self.init_app(app)

  def init_app(self, app):
    app.extensions['redis'] = self
    self.setup_client(app)

  def setup_client(self, app=None, uri=None):
    if app is None:
      app = current_app
    if uri is None:
      uri = app.config.get('REDIS_URI')
    if uri:
      self.client = redis_from_url(uri)
    elif not (app.configured or app.testing):
      raise ValueError('Redis extension: REDIS_URI is not defined in '
                       'application configuration')