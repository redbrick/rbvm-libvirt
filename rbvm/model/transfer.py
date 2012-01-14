import uuid

INFO_OK = 0
INFO_HYPERVISOR_DOWN = 1
INFO_DOMAIN_NOT_FOUND = 2
INFO_UNKNOWN = 3

class TransferableDomain:
   
    data = {
        'name': None,
        'id': None,
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
    
    def initialise(self, hv_conn, uuid_string):
        if hv_conn is None:
            self.data['infostatus'] = INFO_HYPERVISOR_DOWN
            return
        
        dom_uuid = uuid.UUID(uuid_string).bytes
        dom_conn = hv_conn.lookupByUUID(dom_uuid)
        
        if dom_conn is None:
            self.data['infostatus'] = INFO_DOMAIN_NOT_FOUND
            return
        
        self.populate(dom_conn)
    
    def populate(self, c):
        self.data['name'] = c.name()
        self.data['id'] = c.ID()
        self.data['uuid'] = c.UUIDString()
        self.data['ostype'] = c.OSType()
        self.data['autostart'] = c.autostart()
        self.data['active'] = c.isActive()
        self.data['persistent'] = c.isPersistent()
        self.data['memory_kbs'] = c.maxMemory()
        self.data['vcpus'] = c.vcpus()
        self.data['infostatus'] = INFO_OK
    
    def to_dict(self):
        return self.data

