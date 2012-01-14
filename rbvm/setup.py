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
    session = get_session()
    
    print "Adding system groups"
    admins = Group('Admins','admin')
    users = Group('Users','user')
    session.add(admins)
    session.add(users)
    session.commit()
    
    print "Adding abilities"
    user_admin = Ability('User administration','user_admin')
    vm_admin = Ability('VM administration','vm_admin')
    hypervisor_admin = Ability('Hypervisor administration','hypervisor_admin')
    
    user_admin.groups.append(admins)
    vm_admin.groups.append(admins)
    hypervisor_admin.groups.append(admins)
    
    session.add(user_admin)
    session.add(vm_admin)
    session.add(hypervisor_admin)
    session.commit()

def add_user_to_group(username, groupname):
    """
    Adds the user (username) to a group (groupname).
    """
    session = get_session()
    
    group = session.query(Group).filter(Group.name==groupname).first()
    user = session.query(User).filter(User.username==username).first()
    
    group.users.append(user)
    session.commit()

def install_hypervisor(name, uri):
    """
    Installs a hypervisor
    """
    session = get_session()
    
    print "Adding hypervisor"
    hypervisor = Hypervisor(name, uri)
    session.add(hypervisor)
    session.commit()

def get_session():
    print "Connecting to database..."
    engine = create_engine(config.DATABASE_URI)

    Session = sessionmaker()
    Session.configure(bind=engine)
    return Session()
