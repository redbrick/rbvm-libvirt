INFO_OK = 0
INFO_HYPERVISOR_DOWN = 1
INFO_DOMAIN_NOT_FOUND = 2
INFO_UNKNOWN = 3

class TransferableDomain:
   
    data = {
        'name': None,
        'uuid': None,
        'ostype': None,
        'autostart': None,
        'active': None,
        'persistent': None,
        'memory': None,
        'vcpus': None,
        'infostatus': INFO_UNKNOWN
    }
    
    def set_status(self, status):
        self.data['infostatus'] = status
    
    def populate(self, c):
        self.data['name'] = c.name()
        self.data['uuid'] = c.UUIDString()
        self.data['ostype'] = c.OSType()
        self.data['autostart'] = c.autostart()
        self.data['active'] = c.isActive()
        self.data['persistent'] = c.isPersistent()
        self.data['memory'] = c.maxMemory()
        self.data['vcpus'] = c.vcpus()
        self.data['infostatus'] = INFO_OK
    
    def to_dict(self):
        return self.data

