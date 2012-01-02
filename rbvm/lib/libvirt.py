import rbvm.lib.sqlalchemy_tool as database
import rbvm.lib.template as template
from rbvm.controller.rpc import Rpc
from rbvm.lib.auth import get_user, require_login, require_nologin, verify_token
from rbvm.model.database import *
import rbvm.config as config
import libvirt

def get_hypervisor_connection(hypervisor):
    return libvirt.open(hypervisor.uri)

