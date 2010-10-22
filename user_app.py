# -*- coding: utf-8 -*-

import web
import template
import util

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset
from google.appengine.api.memcache import delete as mdel

from google.appengine.ext import db

from models import User
from models import User_Bio
from models import User_Permissions

from forms import profile_form
from forms import prefs_form

urls = (
    '/profile', 'profile',
    '/preferences', 'preferences',
    '/([^a-zA-Z].+)', 'index',
    '', 'redir',
)

t = template.env.get_template('form.html')

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
                    f.nickname.value = e.nickname
                    f.first_name.value = e.bio.first_name
                    f.middle_name.value = e.bio.middle_name
                    f.last_name.value = e.bio.last_name
                    f.city.value = e.bio.city
                    f.state.value = e.bio.state
                    f.postal_code.value = e.bio.postal_code
                    f.country.value = e.bio.country
                    f.bio.value = e.bio.bio
            except:
                u = User(
                    id=user.user_id(),
                    user=user,
                    nickname=user.nickname(),
                )
                u.put()
            return t.render(util.data(
                form=f,
                title='Edit Profile',
                instructions='''Please enter whatever information you feel comfortable
        sharing. (Please note that your information is not shared.public until you
        grant us permission to share it in your Preferences)''',
            ))
        else:
            return t.render(util.data(
                title='Not Logged In!',
                instructions='Please Log in to Edit Your Profile',
            ))

    def POST(self):
        user = users.get_current_user()
        import logging
        logging.error(dir(self.POST))
        f = profile_form()
        if not f.validate():
            return t.render(util.data(
                form=f,
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
                e.nickname = f.nickname.data
                db.put(e)
            e.bio.first_name = f.first_name.data or ''
            e.bio.middle_name = f.middle_name.data or ''
            e.bio.last_name = f.last_name.data or ''
            e.bio.city = f.city.data or ''
            e.bio.state = f.state.data or ''
            e.bio.postal_code = f.postal_code.data or 0
            e.bio.country = f.country.data or ''
            e.bio.bio = f.bio.data or ''
            e.bio.put()
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
                f.first_name.value = 'first_name' in e.shared.public
                f.middle_name.value = 'middle_name' in e.shared.public
                f.last_name.value = 'last_name' in e.shared.public
                f.city.value = 'city' in e.shared.public
                f.state.value = 'state' in e.shared.public
                f.postal_code.value = 'postal_code' in e.shared.public
                f.country.value = 'country' in e.shared.public
                f.bio.value = 'bio' in e.shared.public
            except:
                pass
            return t.render(util.data(
                form=f,
                title='Preferences',
                instructions='Please indicate which items you wish to make public.',
            ))
        else:
            return t.render(util.data(
                title='Not Logged In',
                instructions='Please log in to have preferences!',
            ))
    def POST(self):
        import logging
        user = users.get_current_user()
        f = prefs_form(web.input())
        if not f.validate():
            return t.render(util.data(
                form=f,
                title='Preferences',
                instructions='Please indicate which items you wish to make public.',
            ))
        else:
            logging.error(dir(f))
            prefs = dict(f.d)
            f_prefs = prefs.copy()
            for o in prefs:
                if not prefs[o]:
                    del f_prefs[o]
            q = User.all().filter('id', user.user_id()).fetch(1)
            e = q[0]
            e.shared.public = list(f_prefs)
            e.shared.put()
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
                'bio': markdown(m.bio) if 'bio' in e.shared.public else '',
            }
        ))


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
