# -*- coding: utf-8 -*-

import sys.path.insert

sys.path.insert(0, 'libs/')

import web

urls = (
    '/', 'home',
)

def main():
    app = web.application(urls, locals())
    app.cgirun()

def prof_main():
    pass

if __name__ == '__main__':
    main()
