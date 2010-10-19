# -*- coding: utf-8 -*-

import web
import template
import util

from web import form

from models import User
from models import UserMeta

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

from google.appengine.ext import db

urls = (
    '/profile', 'profile',
    '/preferences', 'preferences',
    '/([^a-zA-Z].+)', 'index',
    '', 'redir',
)

t = template.env.get_template('form.html')

profile_form = form.Form(
    form.Textbox(
        'nickname',
        description='Nickname',
    ),
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
        user = users.get_current_user()
        f = profile_form()
        if user:
            e = User.all().filter('id', user.user_id()).fetch(1)[0]
            if not e:
                u = User(
                    id=user.user_id(),
                    nickname=user.nickname()
                )
                u.put()
            else:
                if e.meta_data:
                    m = e.meta_data
                    f.fill(
                        nickname=e.nickname,
                        first_name=m.first_name,
                        middle_name=m.middle_name,
                        last_name=m.last_name,
                        city=m.city,
                        state=m.state,
                        postal_code=m.postal_code,
                        country=m.country,
                        skills=m.skills,
                    )
            return t.render(util.data(
                form=f.render(),
                title='Edit Profile',
                instructions='',
                message='',
            ))
        else:
            return t.render(util.data(
                title='Not Logged In!',
                instructions='Please Log in to Edit Your Profile',
            ))

    def POST(self):
        user = users.get_current_user()
        f = profile_form()
        if not f.validates():
            return t.render(util.data(
                form=f.render(),
                title='Edit Profile',
                instructions='',
            ))
        else:
            e = User.all().filter('id', user.user_id()).fetch(1)[0]
            meta = e.meta_data
            if meta is None:
                m = UserMeta().put()
                e.meta_data = m.key()
                e = db.get(db.put(e))
            if e.nickname:
                e.nickname = f.d.nickname
                db.put(e)
            meta.first_name = f.d.first_name or ''
            meta.middle_name = f.d.middle_name or ''
            meta.last_name = f.d.last_name or ''
            meta.city = f.d.city or ''
            meta.state = f.d.state or ''
            meta.postal_code = f.d.postal_code or ''
            meta.country = f.d.country or ''
            meta.skills = f.d.skills or ''
            meta.put()
            raise web.seeother('/profile')


class preferences:
    def GET(self):
        user = users.get_current_user()
        f = prefs_form()
        return t.render(util.data(
            form=f.render(),
            title='Preferences',
            instructions='',
        ))
    def POST(self):
        user = users.get_current_user()
        f = prefs_form()
        if not f.validates():
            return t.render(util.data(
                form=f.render(),
                title='Preferences',
                instructions='',
            ))
        else:
            import logging
            prefs = dict(f.d)
            f_prefs = prefs.copy()
            for o in prefs:
                logging.error(prefs[o])
                if not prefs[o]:
                    del f_prefs[o]
            e = User.all().filter('id', user.user_id()).fetch(1)[0]
            e.shared_info = list(f_prefs)
            db.put(e)
            raise web.seeother('/preferences')


class index:
    def GET(self, user_id):
        pass


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
