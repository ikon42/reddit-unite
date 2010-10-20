# -*- coding: utf-8 -*-

from google.appengine.ext import db

class User_Bio(db.Model):
    first_name = db.StringProperty()
    middle_name = db.StringProperty()
    last_name = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    postal_code = db.StringProperty()
    country = db.StringProperty()
    bio = db.TextProperty()
    skills = db.StringListProperty()


class User_Permissions(db.Model):
    public = db.StringListProperty()
    user = db.StringListProperty()


class User(db.Model):
    id = db.StringProperty()
    user = db.UserProperty()
    nickname = db.StringProperty()
    shared = db.ReferenceProperty(reference_class=User_Permissions)
    bio = db.ReferenceProperty(reference_class=User_Bio)

