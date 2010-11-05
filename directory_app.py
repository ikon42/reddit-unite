# -*- coding: utf-8 -*-

import web
import template
import util

from models import User

from forms import search_form

urls = (
    '/search/?', 'search',
    '', 'redis',
    '/([a-zA-Z0-9_]+)?/?', 'index',
    '/map/(.*)/?', 'user_map',
)

class index:
    '''Displays a user list or a list of user lists'''
    def GET(self, name):
        t = template.env.get_template('user_list.html')
        list_list = [ # list_list should be generated somehow
            'global', 'Lists all users from all locales.',
        ]
        user_list = []
        if (name is None):
            return t.render(util.data(
                title='User Lists',
                instructions='''Users are grouped into "user lists" that group them geographically.
            These lists are automatically generated and will change based upon
            the relative size of various user populations.''',
                list_list=map(
                    lambda (li): {'name': li[0], 'scope': li[1]},
                    zip(*[list_list[i::2] for i in range(2)]),
                ),
            ))
        elif (name.lower() in list_list[::2]):
            for i in User.all():
                x = util.strip_private_data(i)
                if x is not None:
                    user_list.append(x)
        else:
            raise web.notfound()
        return t.render(util.data(
            title='Display all members',
            instructions='''Public member listing''',
            users=user_list,
        ))


class user_map:
    '''Generates all different kinds of maps!'''
    def GET(self, name):
        t = template.env.get_template('user_map.html')
        return t.render(util.data())


class search:
    '''Allows users to search for other users based on public information'''
    def GET(self):
        q = web.input()
        t = template.env.get_template('search.html')
        f = search_form()
        try:
            if q.query:
                results = []
                user_list = []
                query = q.query.split(' ')
                for i in User.all():
                    x = util.strip_private_data(i)
                    if x is not None:
                        user_list.append(x)
                for p in user_list:
                    for i in query:
                        if i in dict(p).values():
                            results.append(p)
                return t.render(util.data(
                    title='Find who you\'re looking for!',
                    form=f,
                    results=results if results else None,
                ))
            else:
                web.debug('q.query doesn\'t exist and it didn\'t thow an exception!')
                raise Warning('Odd, huh?')
        except:
            return t.render(util.data(
                title='Find who you\'re looking for!',
                form=f,
            ))


class redis:
    def GET(self):
        raise web.seeother('/')


app = web.application(urls, locals())
