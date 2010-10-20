# -*- coding: utf-8 -*-

import web

urls = (
    '/', 'index',
    '', 'redis',
)

class index:
    def GET(self):
        pass

class redis:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
