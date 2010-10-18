# -*- coding: utf-8 -*-

import web

urls = (
    '', 'redir',
    '/', 'index',
)

class redir:
    def GET(self):
        raise web.seeother('/')


class index:
    def GET(self):
        return 'Register coming soon!'


app = web.application(urls, locals())
