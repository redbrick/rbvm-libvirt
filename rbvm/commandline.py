"""
Command-line utilities
"""

import rbvm.cli.help
import rbvm.cli.listusers
import rbvm.cli.register
import rbvm.cli.resetpw

commands = {
    'listusers': rbvm.cli.listusers.ListUsers,
    'help': rbvm.cli.help.Help,
    'resetpw': rbvm.cli.resetpw.ResetPw,
    'register': rbvm.cli.register.Register,
}
