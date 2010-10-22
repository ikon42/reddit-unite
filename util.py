# -*- coding: utf-8 -*-

import web

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

from google.appengine.ext import db

from models import User

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
                q = User.all().filter('id', user.user_id()).fetch(1)
                nickname = q[0].nickname
                if not mset(key=user.user_id(), value=nickname, time=10, namespace='usernames'):
                    logging.error('Could not set memcache value!')
            data['user']['nickname'] = nickname
        except:
            data['user']['nickname'] = user.nickname()
    else:
        data['log_in_out'] = users.create_login_url('/')
    data.update(kwargs)
    return data

def stripPrivateData(user):
    """This method takes in a user object and returns a dict that holds all the users public data. This method assumes that if nothing is stored in the permissions then the user doesn't want to share anything"""
    
    if user.shared != None: #Assume that none == share nowt
        x = {'nickname':user.nickname}
        for attr in user.shared.public:
            x[attr] = getattr(user.bio,attr)
        web.debug(x)
        return x 
    else:
        return None
