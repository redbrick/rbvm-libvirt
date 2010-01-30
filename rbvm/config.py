# Rudimentary config file for rbvm. To be replaced with a proper cfg file
# using that python config parser that I can't remember the name of.

DATABASE_URI = 'sqlite:////home/andrew/rbvm.db'

BASE_DIR = '/home/andrew/rbvm'
SESSION_DIR = BASE_DIR + '/sessions'
STATIC_DIR = BASE_DIR + '/static'
VIEW_DIR = BASE_DIR + '/views'
LOG_DIR = BASE_DIR + '/logs'

IMAGE_DIR = '/var/lib/rbvm/images'

# Default sizes - all in MB unless otherwise specified
DEFAULT_MEM = 128
DEFAULT_IMAGE_SIZE = 4196
DEFAULT_CPU_CORES = 1

ACCESS_LOG = 'access.log'
ERROR_LOG = 'error.log'

HTTP_BIND_ADDRESS = '136.206.15.5'
HTTP_PORT = 8080

MGRD_DOMAIN_SOCK = '/var/lib/rbvm/mgrsock'

SHOW_TRACEBACKS = True
LOG_TO_SCREEN = True
ENVIRONMENT = 'production'

SESSION_TIMEOUT = 3600

EMAIL_ADDRESS = 'Redbrick Admins <admins@redbrick.dcu.ie>'
SITE_ADDRESS = 'http://localhost:8080/'

# Tools
TOOL_QEMU_IMG = '/usr/bin/qemu-img'
TOOL_KVM = '/usr/bin/kvm'
