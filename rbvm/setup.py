from rbvm.model.database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import rbvm.config as config

session = None

def install(drop_all=False):
    """
    Installs the database, and if necessary, wipes it first.
    """

    print "Connecting to database..."
    engine = create_engine(config.DATABASE_URI)
    Base.metadata.bind = engine

    if drop_all:
        print "Dropping old tables..."
        Base.metadata.drop_all()
    
    print "Installing new schema..."
    Base.metadata.create_all(engine)

def install_groups():
    """
    Installs base groups
    """
    
    print "Connecting to database..."
    engine = create_engine(config.DATABASE_URI)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    print "Adding system groups"
    admins = Group('Admins','admin')
    users = Group('Users','user')
    session.add(admins)
    session.add(users)
    session.commit()
    
    print "Adding abilities"
    user_admin = Ability('User administration','user_admin')
    vm_admin = Ability('VM administration','vm_admin')
    
    user_admin.groups.append(admins)
    vm_admin.groups.append(admins)
    session.add(user_admin)
    session.add(vm_admin)
    session.commit()
    
def install_hypervisor(name, uri):
    """
    Installs a hypervisor
    """
    print "Connecting to database..."
    engine = create_engine(config.DATABASE_URI)

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    print "Adding hypervisor"
    hypervisor = Hypervisor(name, uri)
    session.add(hypervisor)
    session.commit()
