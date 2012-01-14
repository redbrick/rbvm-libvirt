import rbvm.i18n as i18n

class CliBase:
    def __init__(self, session, args, force):
        self.session = session
        self.args = args
        self.force = force
    
    def run(self):
        raise NotImplementedError(i18n.NOT_IMPLEMENTED_YET)
