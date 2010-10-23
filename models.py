# -*- coding: utf-8 -*-

from google.appengine.ext.db import Model
from google.appengine.ext.db import StringProperty
from google.appengine.ext.db import TextProperty
from google.appengine.ext.db import StringListProperty
from google.appengine.ext.db import ReferenceProperty
from google.appengine.ext.db import UserProperty
from google.appengine.ext.db import IntegerProperty

class User_Bio(Model):
    first_name = StringProperty()
    middle_name = StringProperty()
    last_name = StringProperty()
    city = StringProperty()
    state = StringProperty()
    postal_code = StringProperty()
    country = StringProperty()
    bio = TextProperty()
    skills = StringListProperty()


class User_Permissions(Model):
    public = StringListProperty()
    user = StringListProperty()


class User(Model):
    id = StringProperty()
    user = UserProperty()
    nickname = StringProperty()
    shared = ReferenceProperty(User_Permissions)
    bio = ReferenceProperty(User_Bio)

