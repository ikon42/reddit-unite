# -*- coding: utf-8 -*-

from os import path

from jinja2 import Environment
from jinja2 import FileSystemLoader

template_dir = path.join(path.dirname(__file__), 'templates')

env = Environment(loader=FileSystemLoader(template_dir))
