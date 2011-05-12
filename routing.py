from routes import Mapper

class CrudMapper(Mapper):

    def connectCrud(self, *args, **kwds):
        """Create and connect crud Route to the Mapper. """

        args = list(args)
        route = args.pop(0)
        args = tuple(args)
        
        self.connect(route, action="index", *args, **kwds)
        self.connect(route+'/{id}', *args, **kwds)

    def addCustomRoutes(self):
        self.connect('/', controller="handlers:MainHandler")
        self.connect('/main/:char', controller="handlers:AjaxTabsHandler", action="main")
        self.connect('/skills/:char', controller="handlers:AjaxTabsHandler", action="skills")
        self.connect('/journal/:char', controller="handlers:AjaxTabsHandler", action="journal")
        self.connect('/stub', controller="handlers:AjaxTabsHandler", action="stub")
        self.connect('/update', controller="handlers:UpdateHandler")
        self.connect('/login', controller="handlers:LoginHandler")
        self.connect('/logout', controller="handlers:LogoutHandler")
        self.connect('/loginza_.html', controller="handlers:UpdateHandler",action="loginzaVerify")
        return self

