# -*- coding: utf-8 -*-

import web

from google.appengine.api import users

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

from google.appengine.ext import db

from models import User
from models import User_Bio
from models import User_Permissions

def data(**kwargs):
    '''Makes sure that certain pieces of information are always sent to
    the template engine along with the information supplied by the
    different handlers.
    '''
    data = {
        'site': web.ctx.homedomain,
        'user': {},
    }
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

def strip_private_data(user):
    """This method takes in a user object and returns a dict that holds
    all the users public data. This method assumes that if nothing is
    stored in the permissions then the user doesn't want to share anything
    """
    if user.shared != None: #Assume that none == share nowt
        x = {
            'id': user.id,
            'nickname': user.nickname,
        }
        for attr in user.shared.public:
            try:
                x[attr] = getattr(user.bio,attr)
            except AttributeError:
                pass
        #web.debug(x)
        return x 
    else:
        return None

def get_user(user=None, user_id=None):
    '''Get a user from the DataStore using a User object or a user ID'''
    id = user.user_id() if user else user_id
    e = mget(key=id, namespace='profile_data')
    if e is None:
        try:
            q = User.all().filter('id', id).fetch(1)
            e = q[0]
        except:
            u = User(
                id=id,
                user=user,
                nickname=user.nickname(),
            )
            e = db.get(u.put())
    if e.bio is None or e.shared is None:
        if e.bio is None:
            m = User_Bio().put()
            e.bio = m
        if e.shared is None:
            p = User_Permissions().put()
            e.shared = p
        e = db.get(db.put(e))
    mset(key=id, value=e, time=10, namespace='profile_data')
    return e

def user_exists(user_id):
    '''Checks for the existence of a particular user.'''
    try:
        user = get_user(user_id=user_id)
        if user is None:
            return False
        else:
            return True
    except:
        return False
