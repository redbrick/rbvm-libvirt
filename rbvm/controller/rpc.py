import cherrypy
import libvirt
import uuid

from rbvm.lib.rpclib import rpc, json_encode
from rbvm.lib.auth import require_login_rpc, get_user
from rbvm.model.transfer import *


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
    
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_vm_list():
        """
        Return VM list
        """
        user = get_user()
        vms = []
        
        hv_connections = {}
        
        for domain in user.domains:
            hv_conn = None
            
            if domain.hypervisor.uri in hv_connections:
                hv_conn = hv_connections[domain.hypervisor.uri]
            else:
                hv_conn = libvirt.open(domain.hypervisor.uri)
                hv_connections[domain.hypervisor.uri] = hv_conn
            
            model = TransferableDomain()
            model.initialise(hv_conn, domain.uuid)
            vms.append(model.to_dict())
        
        return json_encode(vms=vms)
    
    @cherrypy.expose
    @require_login_rpc
    @rpc
    def get_user_ability_list():
        abilities = []
        user = get_user()
        
        for ability in user.abilities:
            abilities.append(ability.system_name)
        
        for group in user.groups:
            for ability in group.abilities:
                if ability.system_name not in abilities:
                    abilities.append(ability.system_name)
        
        return json_encode(abilities=abilities)
