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
from google.appengine.api.memcache import delete as mdel

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
        'skills',
        description='Skills',
        value='True',
    ),
)

class profile:
    def GET(self):
        user = users.get_current_user()
        f = profile_form()
        if user:
            try:
                q = User.all().filter('id', user.user_id()).fetch(1)
                e = q[0]
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
            except:
                u = User(
                    id=user.user_id(),
                    nickname=user.nickname()
                )
                u.put()
            return t.render(util.data(
                form=f.render(),
                title='Edit Profile',
                instructions='''Please enter whatever information you feel comfortable
        sharing. (Please note that your information is not shared until you
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
        sharing. (Please note that your information is not shared until you
        grant us permission to share it in your Preferences)''',
            ))
        else:
            q = User.all().filter('id', user.user_id()).fetch(1)
            e = q[0]
            if e.meta_data is None:
                m = UserMeta().put()
                e.meta_data = m
                e = db.get(db.put(e))
            if e.nickname:
                e.nickname = f.d.nickname
                db.put(e)
            e.meta_data.first_name = f.d.first_name or ''
            e.meta_data.middle_name = f.d.middle_name or ''
            e.meta_data.last_name = f.d.last_name or ''
            e.meta_data.city = f.d.city or ''
            e.meta_data.state = f.d.state or ''
            e.meta_data.postal_code = f.d.postal_code or ''
            e.meta_data.country = f.d.country or ''
            e.meta_data.skills = f.d.skills or ''
            e.meta_data.put()
            raise web.seeother('/profile')


class preferences:
    def GET(self):
        user = users.get_current_user()
        f = prefs_form()
        if user:
            try:
                q = User.all().filter('id', user.user_id()).fetch(1)
                e = q[0]
                f.first_name.checked = 'first_name' in e.shared_info
                f.middle_name.checked = 'middle_name' in e.shared_info
                f.last_name.checked = 'last_name' in e.shared_info
                f.city.checked = 'city' in e.shared_info
                f.state.checked = 'state' in e.shared_info
                f.postal_code.checked = 'postal_code' in e.shared_info
                f.country.checked = 'country' in e.shared_info
                f.skills.checked = 'skills' in e.shared_info
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
            mdel(key=user.user_id(), namespace='userdata')
            prefs = dict(f.d)
            f_prefs = prefs.copy()
            for o in prefs:
                if not prefs[o]:
                    del f_prefs[o]
            q = User.all().filter('id', user.user_id()).fetch(1)
            e = q[0]
            e.shared_info = list(f_prefs)
            db.put(e)
            raise web.seeother('/preferences')


class index:
    def GET(self, user_id):
        t = template.env.get_template('profile.html')
        e = mget(key=user_id, namespace='userdata')
        if e is None:
            q = User.all().filter('id', user_id).fetch(1)
            e = q[0]
            if mset(key=user_id, value=e, namespace='userdata'):
                pass
        m = e.meta_data
        return t.render(util.data(
            info={
                'nickname': e.nickname if 'nickname' in e.shared_info else '',
                'first_name': m.first_name if 'first_name' in e.shared_info else '',
                'middle_name': m.middle_name if 'middle_name' in e.shared_info else '',
                'last_name': m.last_name if 'last_name' in e.shared_info else '',
                'city': m.city if 'city' in e.shared_info else '',
                'state': m.state if 'state' in e.shared_info else '',
                'postal_code': m.postal_code if 'postal_code' in e.shared_info else '',
                'country': m.country if 'country' in e.shared_info else '',
                'skills': m.skills if 'skills' in e.shared_info else '',
            }
        ))


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
