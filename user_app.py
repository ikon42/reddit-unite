# -*- coding: utf-8 -*-

import web
import template
import util

from google.appengine.api import users
from google.appengine.api.memcache import delete as mdel

try:
    from google.appengine.api.labs import taskqueue
except ImportError:
    from google.appengine.api import taskqueue

from google.appengine.ext import db

from models import User

from forms import profile_form
from forms import prefs_form
from forms import contact_form

urls = (
    '', 'redir',
    '/([^a-zA-Z].+)/contact', 'contact',
    '/([^a-zA-Z].+)', 'index',
    '/profile', 'profile',
    '/preferences', 'preferences',
)

t = template.env.get_template('form.html')

class contact:
    def GET(self, user_id):
        if util.user_exists(user_id):
            t = template.env.get_template('contact.html')
            f = contact_form()
            user = users.get_current_user()
            if user:
                return t.render(util.data(
                    title='Get in touch!',
                    instructions='''You will always reveal your email address
                when you send a message!''',
                    form=f,
                    subject=' '.join([user.nickname(), 'wants to get in touch!']),
                ))
            else:
                return t.render(util.data(
                    title='Not allowed!',
                    instructions='You must be signed in to send messages!',
                ))
        else:
            raise web.seeother('/' + user_id)
    def POST(self, user_id):
        user = users.get_current_user()
        if user:
            d = web.input()
            f = contact_form(message=d.message)
            if f.validate():
                taskqueue.add(
                    url='/task/send_mail',
                    queue_name='email-throttle',
                    params={
                        'sender_id': user.user_id(),
                        'recipient_id': user_id,
                        'message': f.message.data,
                    },
                )
                raise web.seeother('/' + user_id)
            else:
                return t.render(util.data(
                    title='Get in touch!',
                    instructions='''You will always reveal your email address
                when you send a message!''',
                    form=f,
                    subject=' '.join([user.nickname(), 'wants to get in touch!']),
                ))
        else:
            return t.render(util.data(
                title='Not allowed!',
                instructions='You must be signed in to send messages!',
            ))
        


class profile:
    def GET(self):
        user = users.get_current_user()
        if user:
            e = util.get_user(user=user)
            f = profile_form()
            if e.bio:
                f = profile_form(
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
            return t.render(util.data(
                form=f,
                title='Edit Profile',
                instructions='''Please enter whatever information you feel comfortable
            sharing. (Please note that your information is not public until you
            grant us permission to share it in your Preferences)''',
            ))
        else:
            return t.render(util.data(
                title='Not Logged In!',
                instructions='Please Log in to Edit Your Profile',
            ))

    def POST(self):
        user = users.get_current_user()
        d = web.input()
        f = profile_form(
            nickname=d.nickname,
            first_name=d.first_name,
            middle_name=d.middle_name,
            last_name=d.last_name,
            city=d.city,
            state=d.state,
            postal_code=d.postal_code,
            country=d.country,
            bio=d.bio,
        )
        if not f.validate():
            return t.render(util.data(
                form=f,
                title='Edit Profile',
                instructions='''Please enter whatever information you feel comfortable
            sharing. (Please note that your information is not shared.public until you
            grant us permission to share it in your Preferences)''',
            ))
        else:
            e = util.get_user(user=user)
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
            mdel(key=user.user_id(), namespace='profile_data')
            raise web.seeother('/profile')


class preferences:
    def GET(self):
        user = users.get_current_user()
        if user:
            e = util.get_user(user=user)
            if e.shared is not None:
                f = prefs_form(
                    first_name='first_name' in e.shared.public,
                    middle_name='middle_name' in e.shared.public,
                    last_name='last_name' in e.shared.public,
                    city='city' in e.shared.public,
                    state='state' in e.shared.public,
                    postal_code='postal_code' in e.shared.public,
                    country='country' in e.shared.public,
                    bio='bio' in e.shared.public,
                )
            else: #If e.shared if empty then set default to False.
                f = prefs_form(
                    first_name=False,
                    middle_name=False,
                    last_name=False,
                    city=False,
                    state=False,
                    postal_code=False,
                    country=False,
                    bio=False
                )
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
        user = users.get_current_user()
        d = web.input(
            first_name=False,
            middle_name=False,
            last_name=False,
            city=False,
            state=False,
            postal_code=False,
            country=False,
            bio=False,
        )
        f = profile_form(
            first_name=d.first_name,
            middle_name=d.middle_name,
            last_name=d.last_name,
            city=d.city,
            state=d.state,
            postal_code=d.postal_code,
            country=d.country,
            bio=d.bio,
        )
        if not f.validate():
            return t.render(util.data(
                form=f,
                title='Preferences',
                instructions='Please indicate which items you wish to make public.',
            ))
        else:
            prefs = [i.name for i in f if i.data]
            e = util.get_user(user=user)
            e.shared.public = prefs
            e.shared.put()
            mdel(key=user.user_id(), namespace='profile_data')
            raise web.seeother('/preferences')



class index:
    def GET(self, user_id):
        t = template.env.get_template('profile.html')
        try:
            e = util.get_user(user_id=user_id)
            user_info = util.strip_private_data(e)
        except AttributeError:
            user_info = {
                'nickname': '[deleted]',
                'first_name': 'No',
                'middle_name': 'such',
                'last_name': 'user',
                'city': 'reddit.com',
                'country': 'The Internet',
            }
        return t.render(util.data(
            info=user_info
        ))


class redir:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
