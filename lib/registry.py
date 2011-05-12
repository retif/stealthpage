def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Registry(dict):
    def set(self, key, value):
        self[key] = value
    def get(self, key):
        if self.has_key(key):
            return self[key]
        else:
            return False
Registry = singleton(Registry)