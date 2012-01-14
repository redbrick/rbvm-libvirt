import sys

from rbvm.cli.base import CliBase
from rbvm.model.database import *
import rbvm.config as config
import smtplib

class ResetPw(CliBase):
    def resetpw(self):
        """
        Resets a user's password
        """
        username = self.args[0]

        password = "".join(random.sample(string.letters + string.digits,8))
        user = self.session.query(User).filter(User.username==username).first()
        if user is None:
            print "User %s not found." % username
            sys.exit(1)

        user.set_password(password)
        self.session.commit()
        print "Password for user %s has been changed to: %s" % (username, password)
        print "Emailing user at %s" % user.email_address
        s = smtplib.SMTP()
        s.connect()
        s.sendmail(config.EMAIL_ADDRESS, user.email_address, "From: %s\nTo: %s\nSubject: Your VM account password has been reset\n\nYour VM account password has been reset. The new password is:\n\n%s\n\nRegards,\n-Automated mailing monkey" % (config.EMAIL_ADDRESS, user.email_address, password))
        s.quit()
