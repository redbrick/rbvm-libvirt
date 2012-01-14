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
            model = TransferableDomain()
            
            
            if domain.hypervisor.uri in hv_connections:
                hv_conn = hv_connections[domain.hypervisor.uri]
            else:
                hv_conn = libvirt.open(domain.hypervisor.uri)
                hv_connections[domain.hypervisor.uri] = hv_conn
            print hv_conn
            if hv_conn is None:
                model.set_status(INFO_HYPERVISOR_DOWN)
                vms.append(model.to_dict())
                continue
                
            dom_conn = hv_conn.lookupByUUID(uuid.UUID(domain.uuid).bytes)
            if dom_conn is None:
                model.set_status(INFO_DOMAIN_NOT_FOUND)
                vms.append(model.to_dict())
                continue
            
            model.populate(dom_conn)
            
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
