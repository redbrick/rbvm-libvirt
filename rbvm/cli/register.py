import sys
import rbvm.usage
from rbvm.model.database import *
from rbvm.cli.base import CliBase

class Register(CliBase):
    def run(self):
        if len(self.args) < 3:
            print rbvm.usage.usage['register']
        
        hypervisor_uri = self.args[0]
        uuid = self.args[1]
        username = self.args[2]
        
        user = self.session.query(User).filter(User.username==username).first()
        hypervisor = self.session.query(Hypervisor).filter(Hypervisor.uri==hypervisor_uri).first()
        domain = self.session.query(Domain).filter(Domain.uuid==uuid).first()
        
        if user is None:
            print "User not found"
            sys.exit(1)
        
        if hypervisor is None:
            print "Hypervisor not found"
            sys.exit(1)
        
        if domain is not None:
            print "Domain with that UUID already registered!"
            sys.exit(1)
        
        domain = Domain(uuid, user, hypervisor)
        self.session.add(domain)
        self.session.commit()
        
        print "Domain added:\n"
        print "UUID: %s" % domain.uuid
        print "Hypervisor URI: %s" % hypervisor.uri
        print "Owner username: %s" % user.username

