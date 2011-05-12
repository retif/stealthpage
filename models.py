# -*- coding: utf-8 -*-
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()
    access_key = db.StringProperty()
    email = db.StringProperty()
    password = db.StringProperty()
    is_admin = db.BooleanProperty()

    @property
    def chars(self):
        return Char.all().filter('owner = ', self.key())

    def generateAccessKey(self):
        import random
        random.seed()
        hash = random.getrandbits(128)
        self.access_key =  "%016x" % hash

class Char(db.Model):
    owner = db.ReferenceProperty(User)
    name = db.StringProperty()

class CharStats(db.Model):
    char = db.ReferenceProperty(Char)
    shard = db.StringProperty()
    name = db.StringProperty()
    coordx = db.StringProperty()
    coordy = db.StringProperty()
    coordz = db.StringProperty()
    world = db.StringProperty()
    direction = db.StringProperty()
    connected = db.StringProperty()
    dead = db.StringProperty()
    str = db.StringProperty()
    dex  = db.StringProperty()
    int  = db.StringProperty()
    life = db.StringProperty()
    maxlife = db.StringProperty()
    stam= db.StringProperty()
    maxstam = db.StringProperty()
    mana = db.StringProperty()
    maxmana = db.StringProperty()


class CharJournal(db.Model):
    char = db.ReferenceProperty(Char)
    lines = db.StringListProperty()


class Skill(db.Model):
    char = db.ReferenceProperty(Char, collection_name='skills')
    name = db.StringProperty()
    current = db.FloatProperty()
    increased = db.FloatProperty()