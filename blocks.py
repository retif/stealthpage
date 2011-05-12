import os

from google.appengine.ext.webapp import template

from lib.registry import Registry
import genshi
from genshi.template import TemplateLoader
from genshi import Markup


def render_template(template_name, template_vals={}):
    loader = TemplateLoader('theme/frontend')
    template = loader.load(template_name)
    template_vals['render']=render_template
    template_vals['Registry']=Registry
    stream = template.generate(**template_vals)
    rendered = stream.render()
    return Markup(rendered.decode('utf-8'))

def render_django_template(template_name, template_vals=None):
    path = os.path.join(os.path.dirname(__file__), 'theme/frontend', template_name + '.html')
    rendered = template.render(path, template_vals)
    return rendered

class Block(object):
    child_blocks = {}
    template_file = ''
    template_vals = {}
    name = ''
    template_engine = 'genshi'

    def __init__(self, template_name=False, name=False):
      self.template_name = template_name
      self.name = name

    def render(self):
        html = ''
        if self.blocks:
            for block in self.blocks.values():
                html += block.render()
        else:
            html = {
                'genshi': render_template,
                'django': render_django_template
            }[self.template_engine](self.template_file, self.template_vals)
        return html
  
class Layout(object):
    blocks = {}
    root = Block('layout', 'root')
    def render(self):
        return self.root.render()
	
    @classmethod
    def addBlock(cls,template_file=None,name=None, BlockObj=None):
        if BlockObj:
          block = BlockObj()
        else:
          block = Block()
        if name:
            block.name = name
        else:
            block.name = cls._generateName()
        block.template_file = template_file
        cls.blocks[block.name] = block
        return block

    @classmethod
    def _generateName(cls):
        return "anonymous_%i" % len(cls.blocks)

class Head(Block):
  title = ''
  css_links = []

class Header(Block):
  title = ''

