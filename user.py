# -*- coding: utf-8 -*-

import web
import template
import util

from web import form

from google.appengine.api import users

urls = (
    '/profile', 'profile',
    '/preferences', 'preferences',
    '/([^a-zA-Z].+)', 'index',
    '', 'redir',
)

t = template.env.get_template('form.html')

profile_form = form.Form(
    form.Textbox(
        'first_name',
        description='First Name',
    ),
    form.Textbox(
        'middle_name',
        description='Middle Name',
    ),
    form.Textbox(
        'last_name',
        description='Last Name',
    ),
    form.Textbox(
        'city',
        description='City',
    ),
    form.Textbox(
        'state',
        description='State or Province',
    ),
    form.Textbox(
        'postal_code',
        description='Postal Code',
    ),
    form.Textbox(
        'country',
        description='Country',
    ),
    form.Textarea(
        'skills',
        description='Skills',
    ),
)

prefs_form = form.Form(
    form.Checkbox(
        'first_name',
        description='First Name',
    ),
    form.Checkbox(
        'middle_name',
        description='Middle Name',
    ),
    form.Checkbox(
        'last_name',
        description='Last Name',
    ),
    form.Checkbox(
        'city',
        description='City',
    ),
    form.Checkbox(
        'state',
        description='State or Province',
    ),
    form.Checkbox(
        'postal_code',
        description='Postal Code',
    ),
    form.Checkbox(
        'country',
        description='Country',
    ),
    form.Checkbox(
        'skills',
        description='Skills',
    ),
)

class profile:
    def GET(self):
        f = profile_form()
        return t.render(util.data(
            form=f.render(),
            title='Edit Profile',
            instructions='',
        ))
    def POST(self):
        f = profile_form()
        if not f.validates():
            return t.render(util.data(
                form=f.render(),
                title='Edit Profile',
                instructions='',
            ))
        else:
            raise web.seeother('/profile')


class preferences:
    def GET(self):
        f = prefs_form()
        return t.render(util.data(
            form=f.render(),
            title='Preferences',
            instructions='',
        ))
    def POST(self):
        f = prefs_form()
        if not f.validates():
            return t.render(util.data(
                form=f.render(),
                title='Preferences',
                instructions='',
            ))
        else:
            raise web.seeother('/preferences')


class index:
    def GET(self, user_id):
        pass


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())