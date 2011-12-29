from rbvm.lib.rpclib import rpc, json_encode
from rbvm.lib.auth import require_login_rpc, get_user
import cherrypy


class Rpc:
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_user_domains(hello=None):
        domains = [('test', 10, 20), ('test2', 10, 30)]
        return json_encode(domains=domains)
    
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_user_details():
        user = get_user()
        return json_encode(username=user.username,id=user.id)
