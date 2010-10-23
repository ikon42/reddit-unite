# -*- coding: utf-8 -*-

import markdown2
import jinja2.ext

from os import path

from jinja2 import Environment
from jinja2 import FileSystemLoader

template_dir = path.join(path.dirname(__file__), 'templates')

class Markdown2Extension(jinja2.ext.Extension):
    tags = set(['markdown'])
    def __init__(self, environment):
        super(Markdown2Extension, self).__init__(environment)
        environment.extend(
            markdowner=markdown2.Markdown()
        )   

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(
            ['name:endmarkdown'],
            drop_needle=True
        )
        return jinja2.nodes.CallBlock(
            self.call_method('_markdown_support'),
            [],
            [],
            body,
        ).set_lineno(lineno)

    def _markdown_support(self, caller):
        return self.environment.markdowner.convert(caller()).strip()

env = Environment(
    loader=FileSystemLoader(template_dir),
    extensions=[Markdown2Extension],
)
