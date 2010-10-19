# -*- coding: utf-8 -*-

import logging

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

from google.appengine.ext import db

from models import User

def datah(**kwargs):
    data = {
        'user': {},
        'log_in_out': '/login',
    }
    user = users.get_current_user()
    if user:
        data['logged_in'] = True
        data['user']['id'] = user.user_id()
        try:
            nickname = mget(key=user.user_id(), namespace='users')
            if nickname is None:
                user_prefs = db.get(user.user_id())
                nickname = user.prefs.nickname
                if not mset(key=user.user_id(), value=nickname, time=10, namespace='users'):
                    pass
            data['user']['nickname'] = nickname
        except:
            data['user']['nickname'] = user.nickname()
    data.update(kwargs)
    return data

def data(**kwargs):
    data = {'user': {}}
    user = users.get_current_user()
    if user:
        data['log_in_out'] = users.create_logout_url('/')
        data['logged_in'] = True
        data['user']['id'] = user.user_id()
        try:
            nickname = mget(key=user.user_id(), namespace='usernames')
            if nickname is None:
                user_prefs = User.all().filter('id', user.user_id()).fetch(1)
                nickname = user_prefs[0].nickname
                if not mset(key=user.user_id(), value=nickname, time=10, namespace='usernames'):
                    logging.error('Could not set memcache value!')
            data['user']['nickname'] = nickname
        except:
            data['user']['nickname'] = user.nickname()
    else:
        data['log_in_out'] = users.create_login_url('/')
    data.update(kwargs)
    return data
