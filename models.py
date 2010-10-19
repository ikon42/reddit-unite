# -*- coding: utf-8 -*-

from google.appengine.ext import db

class UserMeta(db.Model):
    first_name = db.StringProperty()
    middle_name = db.StringProperty()
    last_name = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    postal_code = db.StringProperty()
    country = db.StringProperty()
    skills = db.StringProperty()


class User(db.Model):
    id = db.StringProperty()
    nickname = db.StringProperty()
    shared_info = db.StringListProperty()
    meta_data = db.ReferenceProperty(reference_class=UserMeta)

