# -*- coding: utf-8 -*-

import web
import template
import util

from models import User

from forms import search_form

urls = (
    '/', 'index',
    '', 'redis',
    '/allmembers', 'allmembers',
    '/map/(.*)', 'user_map',
)

class allmembers:
    """This class displays all members."""
    def GET(self):
        t = template.env.get_template('allmembers.html')
        userlist = []
        for i in User.all():
            x = util.stripPrivateData(i)
            if x is not None:
                userlist.append(x)

        web.debug(userlist)

        return t.render(util.data(
            title='Display all members',
            instructions='''This forms shows all members''',
            users=userlist,
        ))


class user_map:
    '''Generates all different kinds of maps!'''
    def GET(self, name):
        t = template.env.get_template('user_map.html')
        return t.render(util.data())


class index:
    '''Allows users to search for other users based on public information'''
    def GET(self):
        q = web.input()
        t = template.env.get_template('search.html')
        f = search_form()
        results = []
        if q.query:
            pass
        return t.render(util.data(
            title='Find who you\'re looking for!',
            instructions='''(Doesn't work yet..)''',
            form=f,
            results=results if results else None,
        ))


class redis:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
