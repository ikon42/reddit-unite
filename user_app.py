# -*- coding: utf-8 -*-

import web
import template
import util

from web import form

from models import User

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset
from google.appengine.api.memcache import delete as mdel

from google.appengine.ext import db

from models import User_Bio
from models import User_Permissions

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
        'bio',
        description='bio',
    ),
)

prefs_form = form.Form(
    form.Checkbox(
        'first_name',
        description='First Name',
        value='True',
    ),
    form.Checkbox(
        'middle_name',
        description='Middle Name',
        value='True',
    ),
    form.Checkbox(
        'last_name',
        description='Last Name',
        value='True',
    ),
    form.Checkbox(
        'city',
        description='City',
        value='True',
    ),
    form.Checkbox(
        'state',
        description='State or Province',
        value='True',
    ),
    form.Checkbox(
        'postal_code',
        description='Postal Code',
        value='True',
    ),
    form.Checkbox(
        'country',
        description='Country',
        value='True',
    ),
    form.Checkbox(
        'bio',
        description='Bio',
        value='True',
    ),
)

class profile:
    def GET(self):
        user = users.get_current_user()
        f = profile_form()
        if user:
            try:
                e = mget(key=user.user_id, namespace='profile_data')
                if e is None:
                    q = User.all().filter('id', user.user_id()).fetch(1)
                    e = q[0]
                    mset(key=user_id, value=e, namespace='profile_data')
                if e.bio:
                    f.fill(
                        nickname=e.nickname,
                        first_name=e.bio.first_name,
                        middle_name=e.bio.middle_name,
                        last_name=e.bio.last_name,
                        city=e.bio.city,
                        state=e.bio.state,
                        postal_code=e.bio.postal_code,
                        country=e.bio.country,
                        bio=e.bio.bio,
                    )
            except:
                u = User(
                    id=user.user_id(),
                    user=user,
                    nickname=user.nickname(),
                )
                u.put()
            return t.render(util.data(
                form=f.render(),
                title='Edit Profile',
                instructions='''Please enter whatever information you feel comfortable
        sharing. (Please note that your information is not shared with the public until you
        grant us permission to share it in your Preferences)''',
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
                instructions='''Please enter whatever information you feel comfortable
        sharing. (Please note that your information is not shared.public until you
        grant us permission to share it in your Preferences)''',
            ))
        else:
            q = User.all().filter('id', user.user_id()).fetch(1)
            e = q[0]
            if e.bio is None or e.shared is None:
                if e.bio is None:
                    m = User_Bio().put()
                    e.bio = m
                if e.shared is None:
                    p = User_Permissions().put()
                    e.shared = p
                e = db.get(db.put(e))
            if e.nickname:
                e.nickname = f.d.nickname
                db.put(e)
            e.bio.first_name = f.d.first_name or ''
            e.bio.middle_name = f.d.middle_name or ''
            e.bio.last_name = f.d.last_name or ''
            e.bio.city = f.d.city or ''
            e.bio.state = f.d.state or ''
            e.bio.postal_code = f.d.postal_code or ''
            e.bio.country = f.d.country or ''
            e.bio.bio = f.d.bio or ''
            e.bio.put()
            e.put()
            raise web.seeother('/profile')


class preferences:
    def GET(self):
        user = users.get_current_user()
        f = prefs_form()
        if user:
            try:
                e = mget(key=user.user_id, namespace='profile_data')
                if e is None:
                    q = User.all().filter('id', user.user_id()).fetch(1)
                    e = q[0]
                    mset(key=user_id, value=e, namespace='profile_data')
                f.first_name.checked = 'first_name' in e.shared.public
                f.middle_name.checked = 'middle_name' in e.shared.public
                f.last_name.checked = 'last_name' in e.shared.public
                f.city.checked = 'city' in e.shared.public
                f.state.checked = 'state' in e.shared.public
                f.postal_code.checked = 'postal_code' in e.shared.public
                f.country.checked = 'country' in e.shared.public
                f.bio.checked = 'bio' in e.shared.public
            except:
                pass
            return t.render(util.data(
                form=f.render(),
                title='Preferences',
                instructions='Please indicate which items you wish to make public.',
            ))
        else:
            return t.render(util.data(
                title='Not Logged In',
                instructions='Please log in to have preferences!',
            ))
    def POST(self):
        user = users.get_current_user()
        f = prefs_form()
        if not f.validates():
            return t.render(util.data(
                form=f.render(),
                title='Preferences',
                instructions='Please indicate which items you wish to make public.',
            ))
        else:
            import logging
            prefs = dict(f.d)
            f_prefs = prefs.copy()
            for o in prefs:
                if not prefs[o]:
                    del f_prefs[o]
            q = User.all().filter('id', user.user_id()).fetch(1)
            e = q[0]
            e.shared.public = list(f_prefs)
            e.shared.put()
            e.put()
            mdel(key=user.user_id(), namespace='profile_data')
            raise web.seeother('/preferences')


class index:
    def GET(self, user_id):
        t = template.env.get_template('profile.html')
        e = mget(key=user_id, namespace='profile_data')
        if e is None:
            q = User.all().filter('id', user_id).fetch(1)
            e = q[0]
            mset(key=user_id, value=e, namespace='profile_data')
        m = e.bio
        return t.render(util.data(
            info={
                'nickname': e.nickname if 'nickname' in e.shared.public else '',
                'first_name': m.first_name if 'first_name' in e.shared.public else '',
                'middle_name': m.middle_name if 'middle_name' in e.shared.public else '',
                'last_name': m.last_name if 'last_name' in e.shared.public else '',
                'city': m.city if 'city' in e.shared.public else '',
                'state': m.state if 'state' in e.shared.public else '',
                'postal_code': m.postal_code if 'postal_code' in e.shared.public else '',
                'country': m.country if 'country' in e.shared.public else '',
                'bio': m.bio if 'bio' in e.shared.public else '',
            }
        ))


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
