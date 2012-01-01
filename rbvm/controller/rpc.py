from rbvm.lib.rpclib import rpc, json_encode
from rbvm.lib.auth import require_login_rpc, get_user
import cherrypy


class Rpc:
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_user_details():
        user = get_user()
        return json_encode(username=user.username,id=user.id)
        
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_sparse_vm_list():
        """
        Return a list of VMs that the user owns
        """
        return json_encode(vms=[])
