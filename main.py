# -*- coding: utf-8 -*-

from sys import path

from google.appengine.api.memcache import get as mget
from google.appengine.api.memcache import set as mset

path.insert(0, 'lib/')

import web
import register
import template

urls = (
    '/register', register.app,
    '/', 'home',
)

class home:
    def GET(self):
        t = mget(key='home', namespace='templates')
        if t is not None:
            return t
        else:
            t = template.env.get_template('home.html').render()
            mset(key='home', value=t, time=60, namespace='templates')
            return t


app = web.application(urls, locals())

def main():
    app.cgirun()

def prof_main():
    # This is the main function for profiling 
    import cProfile, pstats, StringIO
    import logging
    prof = cProfile.Profile()
    prof = prof.runctx("main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    # The rest is optional.
    stats.print_callees()
    stats.print_callers()
    logging.info("Profile data:\n%s", stream.getvalue())

if __name__ == '__main__':
    main()
