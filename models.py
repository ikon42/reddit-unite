# -*- coding: utf-8 -*-

from google.appengine.ext import db

class User(db.Model):
    uid = db.UserProperty()
    frist_name = db.StringProperty()
    middle_name = db.StringProperty()
    last_name = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    postal_code = db.StringProperty()
    country = db.StringProperty()
    shared_info = db.ListProperty()
    skills = db.ListProperty()



