# -*- coding: utf-8 -*-
from google.appengine.ext import db

class JobPost(db.Models):
	title = db.StringProperty()
	author = db.UserProperty()
	post = db.StringProperty()


class JobPostComment(db.Models):
	pass
