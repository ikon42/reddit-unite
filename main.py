# -*- coding: utf-8 -*-

from sys import path

path.insert(0, 'lib/')

import web
import user
import template
import util

urls = (
    '/user', user.app,
    '/', 'index',
)

class index:
    def GET(self):
        t = template.env.get_template('home.html')
        return t.render(util.data())


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
