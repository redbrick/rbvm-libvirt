from rbvm.cli.base import CliBase
from rbvm.model.database import *
import rbvm.config as config


class ListUsers(CliBase):
    def run(self):
        """
        Outputs a list of users in tabular format
        """
        users = self.session.query(User).all()
        print "%-10s | %s" % ("Username","Email address")

        for user in users:
            print "%-10s | %s" % (user.username, user.email_address)
