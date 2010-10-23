# -*- coding: utf-8 -*-

from wtforms import Form
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import validators

class profile_form(Form):
    nickname = TextField('Nickname')
    first_name = TextField('First Name')
    middle_name = TextField('Middle Name')
    last_name = TextField('Last Name')
    city = TextField('City')
    state = TextField('State or Province')
    postal_code = TextField('Postal Code')
    country = TextField('Country')
    bio = TextAreaField('Bio')


class prefs_form(Form):
    #nickname = BooleanField('Nickname')
    first_name = BooleanField('First Name')
    middle_name = BooleanField('Middle Name')
    last_name = BooleanField('Last Name')
    city = BooleanField('City')
    state = BooleanField('State or Province')
    postal_code = BooleanField('Postal Code')
    country = BooleanField('Country')
    bio = BooleanField('Bio')

