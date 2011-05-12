from modules.core.model.session.abstract import AbstractSession
from models import User

class UserSession(AbstractSession):
    namespace = 'user'

    def isLogged(self):
        if 'user_key' in self:
            return True
        else:
            return False

    def getUser(self):
        if 'user_key' in self:
            user = User.get(self['user_key'])
            if not user:
                raise BaseException('User with key %s not found' % (self['user_key']))
            return user
        return False

    def setUserAsLogged(self, user):
        self['user_key'] = str(user.key())

    def setUserAsLoggedByKey(self, key):
        self['user_key'] = key
        