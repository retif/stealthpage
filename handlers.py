# -*- coding: utf-8 -*-
from modules.core.model.session import CoreSession
from modules.user.model.session import UserSession
import blocks
from modules.core.model.app import RequestHandler, logged, guest_only, is_admin
import models
import logging

from modules.user.model.session import UserSession
from lib.registry import Registry

class MainHandler(RequestHandler):
    def get(self):

        userSession = UserSession()

        if userSession.isLogged():
            chars = userSession.getUser().chars
            Registry().set('chars',chars)
        else:
            Registry().set('chars',[])
        Registry().set('user',userSession.getUser())
        Registry().set('sess_id',userSession.getSessId())

        self.response.out.write(blocks.render_template('home.html'))

    def post(self):
        accessKey = self.request.get('AccessKey')
        loginzaToken = self.request.get('token')
        if(accessKey):
            user = models.User.all().filter('access_key =', accessKey).get()
            if not user:
               self.response.out.write('You have invalid access key. You can get one on the site')
               return

            ini = self.request.get('Ini')
            ini = ini.replace('`', '=').replace('|n|','\n')
            logging.info(accessKey)
            logging.info(ini)
            from modules.stealth import importData
            importData(user, ini)
        if(loginzaToken):
            from google.appengine.api import urlfetch
            from django.utils import simplejson
            import urllib
            try:
                result = urlfetch.fetch('http://loginza.ru/api/authinfo?token='+loginzaToken)
                response = simplejson.loads(result.content)
                logging.debug(('loginzaToken',loginzaToken,response))
                if not response.has_key('error_type'):
                    name = 'Unnamed'
                    email = False;
                    if response.has_key('nickname'):
                        name = response['nickname']
                    elif response.has_key('name') and response['name'].has_key('full_name'):
                        name = response['name']['full_name']
                    if response.has_key('email'):
                        email = response['email']

                    if len(email)>0:
                        user = models.User.get_or_insert(email)
                        if not user.access_key:
                            user.name = name
                            user.email = email
                            user.generateAccessKey()
                            user.put()
                        UserSession().setUserAsLogged(user)
                        self.redirect('/')
                        return
                    logging.debug('some loginza error')
                    #make flash message
                    self.redirect('/')


            except urlfetch.Error:
                logging.error(('loginzaToken urlfetch Error',loginzaToken,str(Error)))
                #make flash message
                self.redirect('/')
            except ValueError:
                logging.error(('loginzaTokenError',loginzaToken,str(ValueError)))
                #make flash message
                self.redirect('/')




class AjaxTabsHandler(RequestHandler):
    def main(self,char):
        if UserSession().isLogged() and char!= 'stub':
            user = UserSession().getUser()
            char = models.Char.get_or_insert(str(user.key())+char, owner=user)
            charStats = models.CharStats.get_or_insert(char.key().name(), char=char)
            self.response.out.write(blocks.render_template('ajax/main.html', {'charStats':charStats}))
        else:
            self.response.out.write(blocks.render_template('ajax/main.html', {'charStats':models.CharStats()}))

    def skills(self,char):
        if UserSession().isLogged() and char!= 'stub':
            user = UserSession().getUser()
            char = models.Char.get_or_insert(str(user.key())+char, owner=user)
            skills= char.skills.fetch(1000)
            self.response.out.write(blocks.render_template('ajax/skills.html', {'skills':skills}))
        else:
            self.response.out.write(blocks.render_template('ajax/main.html', {'skills':[]}))

    def journal(self,char):
        if UserSession().isLogged() and char!= 'stub':
            user = UserSession().getUser()
            char = models.Char.get_or_insert(str(user.key())+char, owner=user)
            journal = models.CharJournal.get_or_insert(char.key().name(), char=char)
            self.response.out.write(blocks.render_template('ajax/journal.html', {'journal':journal}))
        else:
            self.response.out.write(blocks.render_template('ajax/journal.html', {'journal':[]}))

    def stub(self):
        pass

#update something
class UpdateHandler(RequestHandler):
    def get(self):
        self.redirect('/')

    def loginzaVerify(self):
        self.response.out.write('')

class LoginHandler(RequestHandler):
    @guest_only
    def get(self):
        if UserSession().isLogged():
            self.redirect('/');
        else:
            self.response.out.write(blocks.render_template('login/form.html', {}))

    @guest_only
    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")

        user = models.User.gql("WHERE email = :1", email).get()
        if user:
            if len(password)>0 and user.password == password:
                UserSession().setUserAsLogged(user)
                self.response.out.write(blocks.render_template('login.xml', {'user_key':user.key()}))
            else:
                self.response.out.write(blocks.render_template('error.xml', {'message':'Wrong password'}))
        else:
            self.response.out.write(blocks.render_template('error.xml', {'message':'User not found'}))

class LogoutHandler(RequestHandler):
    @logged
    def get(self):
        CoreSession().clear()
        self.redirect('/');
