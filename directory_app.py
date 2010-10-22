# -*- coding: utf-8 -*-

import web
import template
import util

from models import User
from models import User_Bio
from models import User_Permissions

from google.appengine.ext import db

urls = (
    '/', 'index',
    '', 'redis',
    '/allmembers', 'allmembers',
)

t = template.env.get_template('allmembers.html')

class allmembers:
    """This class displays all members."""
    def GET(self):

        userlist = []
        for i in User.all():
            x = util.stripPrivateData(i)
            if x is not None:
                userlist.append(x)

        web.debug("AAA")
        web.debug(userlist)

        return t.render(util.data(
                    title ='Display all members',
                    instructions='''This forms shows all members''',
                    users = userlist
                    ))

class index:
    def GET(self):
        pass

class redis:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
