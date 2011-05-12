from modules.user.model.session import UserSession
from google.appengine.ext import webapp
from lib.registry import Registry

#decorator
def logged(f):
    def _inner(*args, **kwargs):
        if not UserSession().isLogged():
            raise BaseException('You are not authorized')
        return f(*args, **kwargs)

    return _inner

#decorator
def guest_only(f):
    def _inner(*args, **kwargs):
        if UserSession().isLogged():
            raise BaseException('You are not authorized')
        return f(*args, **kwargs)

    return _inner

#decorator
def is_admin(f):
    def _inner(*args, **kwargs):
        if not UserSession().isLogged() or not UserSession().getUser().is_admin:
            raise BaseException('You are not authorized')
        return f(*args, **kwargs)

    return _inner

class RequestHandler(webapp.RequestHandler):
      def initialize(self, *args, **kwargs):
          super(RequestHandler, self).initialize(*args, **kwargs)

          Registry().set('request', self.request)
          Registry().set('response', self.response)
          Registry().set('session', self.request.environ['beaker.session'])

          self.response.headers['Content-Type'] = 'text/html; charset=utf-8'

