from rbvm.cli.base import CliBase
import rbvm.usage

class Help(CliBase):
    def run(self):
        """
        Displays help
        """
        if len(self.args) < 1:
            key = 'index'
        else:
            key = self.args[0]

        if key not in rbvm.usage.usage:
            print "Unknown command"
        else:
            print rbvm.usage.usage[key]
