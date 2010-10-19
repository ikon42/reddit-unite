# -*- coding: utf-8 -*-

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

from google.appengine.ext import db

def data(**kwargs):
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