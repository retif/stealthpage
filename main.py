#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext.webapp import util

import wsgi

from routing import CrudMapper
from beaker.middleware import SessionMiddleware

map = CrudMapper(explicit = True).addCustomRoutes()


def main():

    application = wsgi.WSGIApplication(map, debug = True)

    application = SessionMiddleware(application, {'session.auto' : True, 'session.type' : 'ext:google'})

    util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
