import cherrypy
import traceback
import hashlib
import cherrypy.lib.sessions
import rbvm.lib.sqlalchemy_tool as database
import rbvm.lib.template as template
from rbvm.controller.rpc import Rpc
from rbvm.lib.auth import get_user, require_login, require_nologin, verify_token
from rbvm.model.database import *
import rbvm.config as config

class Root:
    _cp_config = {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': config.STATIC_DIR,
        'tools.staticdir.index' : 'ajax.html',
    }
    
    @cherrypy.expose
    @template.output('tokenerror.html')
    def tokenerror(self):
        """
        Display static token error page
        """
        return template.render(error=None)
    
    @cherrypy.expose
    @require_nologin
    @template.output('login.html')
    def login(self, username=None, password=None):
        if username and password:
            user_object = database.session.query(User).filter(User.username == username).first()
            if not user_object:
                return template.render(error='Invalid usernam   e or password')
            pwhash = hashlib.sha256()
            pwhash.update(password + user_object.salt)
            hash_hex = pwhash.hexdigest()
            
            if hash_hex == user_object.password:
                cherrypy.session['authenticated'] = True
                cherrypy.session['username'] = user_object.username
                raise cherrypy.HTTPRedirect(config.SITE_ADDRESS)
        
        return template.render()
    
    @cherrypy.expose
    @template.output('logout.html')
    def logout(self):
        cherrypy.lib.sessions.expire()
        return template.render()
    
    rpc = Rpc()