# coding=utf-8
import os

from unittest import TestCase, skip
from flask import Flask
from wtforms import Form, TextField, IntegerField
from wtforms.validators import required
from yaka.web.widgets import TableView, SingleView, Panel, Row, ModelWrapper, \
  linkify_url


class DummyModel(object):
  """
  Mock model.
  """
  def __init__(self, **kw):
    for k, v in kw.items():
      setattr(self, k, v)


class DummyForm(Form):
  name = TextField(u'Nom du véhicule')
  price = IntegerField(u"Prix du véhicule")


class ModelWrapperTestCase(TestCase):

  def test_non_empty_panels(self):
    model = DummyModel(name="Renault Megane", price=10000)
    panels = [Panel('main', Row('name'), Row('price'))]
    wrapper = ModelWrapper(model)
    self.assertEquals(wrapper.filter_non_empty_panels(panels), panels)

  def test_empty_panels(self):
    model = DummyModel(name="", maker="")
    panels = [Panel('main', Row('name'), Row('maker'))]
    wrapper = ModelWrapper(model)
    self.assertEquals(wrapper.filter_non_empty_panels(panels), [])


class BaseTestCase(TestCase):

  def setUp(self):
    # Hack to set up the template folder properly.
    template_dir = os.path.dirname(__file__) + "/../../yaka/templates"
    template_dir = os.path.normpath(template_dir)
    self.app = Flask(__name__, template_folder=template_dir)


class TableViewTestCase(BaseTestCase):

  def test_table_view(self):
    with self.app.test_request_context():
      columns = ['name', 'price']
      view = TableView(columns)

      model1 = DummyModel(name="Renault Megane", _name="toto", price=10000)
      model2 = DummyModel(name="Peugeot 308", _name="titi", price=12000)

      models = [model1, model2]

      res = view.render(models)

      assert "Renault Megane" in res
      assert "10000" in res


class ModelViewTestCase(BaseTestCase):
  # Hack to silence test harness bug
  __name__ = "ModelView test case"

  def test_single_view(self):
    with self.app.test_request_context():
      panels = [Panel('main', Row('name'), Row('price'), Row('email'))]
      view = SingleView(*panels)

      model = DummyModel(name="Renault Megane",
                    price=10000, email="joe@example.com")
      res = view.render(model)

      assert "Renault Megane" in res
      assert "10000" in res
      assert "mailto:joe@example.com" in res

  @skip
  def test_edit_view(self):
    with self.app.test_request_context():
      panels = [Panel('main', Row('name'), Row('price'))]
      view = SingleView(*panels)

      model = DummyModel(name="Renault Megane", price=10000)
      form = DummyForm(obj=model)
      res = view.render_form(form)

      assert "Renault Megane" in res
      assert "10000" in res


class TestLinkify(TestCase):

  EXPECTED = '<a href="http://example.com">example.com</a><i class="icon-share-alt"></i>'

  def test_http(self):
    value = "http://example.com"
    result = linkify_url(value)
    self.assertEquals(result, self.EXPECTED)

  def test_no_http(self):
    value = "example.com"
    result = linkify_url(value)
    self.assertEquals(result, self.EXPECTED)
