from lib.registry import Registry

class AbstractSession(dict):

    namespace = 'undefined'

    def __init__(self):

        if self.namespace == 'undefined':
            raise AttributeError('namespace attribute is not defined in subclass')

        session = Registry().get('session')

        if self.namespace not in session:
            session[self.namespace] = self
        else:
            self.update(session[self.namespace])
            session[self.namespace] = self

    def set(self, key, value):
        self[key] = value

    def getSessId(self):
        return Registry().get('session').id

    def clear(self):
        sess = Registry().get('session')

        import logging
        logging.info(str(sess))
        
        sess.delete()

#        Registry().get('session').delete()
#        Registry().get('session').load()