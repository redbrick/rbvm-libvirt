import cherrypy
from rbvm.model.database import *
import rbvm.lib.sqlalchemy_tool as database
import rbvm.config as config

def get_user():
    """
    Returns the currently logged in user
    """

    if cherrypy.session.get('authenticated') != True:
        return None
    else:
        username = cherrypy.session.get('username')
        user = database.session.query(User).filter(User.username == username).first()
        return user

def require_ability(name):
    """
    Ensure that the current user has the ability called name
    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            user = get_user()
            
            if user is None:
                raise cherrypy.HTTPError(403)
            
            if user.has_ability(name):
                return func(*args, **kwargs)
            
            raise cherrypy.HTTPError(403)
        return wrapper
    return decorate

def require_any_ability(names):
    """
    Ensure that the current user has any of the abilities listed
    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            user = get_user()
            
            if user is None:
                raise cherrypy.HTTPError(403)
            
            for name in names:
                if user.has_ability(name):
                    return func(*args, **kwargs)
            
            raise cherrypy.HTTPError(403)
        return wrapper
    return decorate

def require_all_abilities(names):
    """
    Ensure that the current user has all of the abilities listed
    """
    def decorate(func):
        def wrapper(*args, **kwargs):
            user = get_user()
            
            if user is None:
                raise cherrypy.HTTPError(403)
            
            for name in names:
                if not user.has_ability(name):
                    raise cherrypy.HTTPError(403)
            
            return func(*args, **kwargs)
        return wrapper
    return decorate

def require_login(func):
    """
    Decorator to require a user to be logged in
    """
    def wrapper(*args, **kwargs):
        if cherrypy.session.get('authenticated') == True:
            return func(*args, **kwargs)
        else:
            raise cherrypy.HTTPRedirect(config.SITE_ADDRESS + 'login')
    return wrapper

def require_login_rpc(func):
    """
    Decorator to require a user to be logged in to carry out an RPC function
    """
    def wrapper(*args, **kwargs):
        if cherrypy.session.get('authenticated') == True:
            return func(*args, **kwargs)
        else:
            raise cherrypy.HTTPError(403)
    return wrapper

def require_nologin(func):
    """
    Decorator to ensure that a user is not logged in
    """

    def wrapper(*args, **kwargs):
        if cherrypy.session.get('authenticated') == True:
            raise cherrypy.HTTPRedirect(config.SITE_ADDRESS)
        else:
            return func(*args,**kwargs)
    return wrapper

def verify_token(func):
    """
    Verifies that the current action token is valid.
    """
    def wrapper(*args, **kwargs):
        user = get_user()
        
        if 'token' not in kwargs:
            raise cherrypy.HTTPRedirect(config.SITE_ADDRESS + 'tokenerror')
        
        token_object = database.session.query(OneTimeToken).filter(OneTimeToken.token==kwargs['token']).first()
        
        if token_object is None or token_object.check_and_expire(user) is True:
            raise cherrypy.HTTPRedirect(config.SITE_ADDRESS + 'tokenerror')
        else:
            return func(*args, **kwargs)
    return wrapper

def is_administrator():
    """
    Finds the Administrator group, and checks if the current user is a member.
    """
    user = get_user()

    admin_group = database.session.query(Group).filter(Group.name=='Admins').first()
    if admin_group is None:
        return False
    
    if admin_group in user.groups:
        return True
    
    return False
