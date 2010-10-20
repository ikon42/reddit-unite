# -*- coding: utf-8 -*-

import web
import template
import util

from google.appengine.api import users

urls = (
    '/', 'index',
    '', 'redir',
)

openid_providers = (
    'Google.com/accounts/o8/id',
    'Yahoo.com',
    'Myopenid.com'
)

class index:
    def GET(self):
        input = web.input(provider=None)
        if input.provider:
            url = users.create_login_url('/', federated_identity=input.provider)
            raise web.redirect(web.ctx.homedomain + url)
        t = template.env.get_template('login.html')
        providers = {}
        for p in openid_providers:
            providers[p.split('.')[0].lower()] = users.create_login_url('/', federated_identity=p.lower())
        return t.render(util.data(
            login=providers,
        ))


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
