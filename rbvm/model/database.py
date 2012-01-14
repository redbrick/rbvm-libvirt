# coding=utf-8
import sqlalchemy
import random
import string
import hashlib
import os
import base64
import datetime
import libvirt

from sqlalchemy import Table,Column,MetaData,ForeignKey
from sqlalchemy.schema import Sequence, ForeignKeyConstraint
from sqlalchemy import Integer,String,DateTime,Unicode,SmallInteger,Text,Binary,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation,backref
from sqlalchemy.ext.associationproxy import association_proxy

import rbvm.lib.sqlalchemy_tool as database

session = None # Initialised at runtime by single-threaded daemons (multi threaded daemons use sqlalchemy_tool)

Base = declarative_base()

class User(Base):
    """
    User
    """
    # {{{
    __tablename__ = 'user_table'
    
    id = Column(Integer,Sequence('user_table_id_seq'),primary_key=True)
    username = Column(String(255),unique=True,nullable=False)
    salt = Column(String(10),nullable=False)
    password = Column(String(255),nullable=False)
    email_address = Column(String(255),nullable=False)
    
    domains = relation('Domain', backref='user')
    
    def set_password(self,password_plain):
        salt = ''.join(random.Random().sample(string.letters + string.digits,9))
        hash = hashlib.sha256()
        hash.update(password_plain + salt)
        self.password = hash.hexdigest()
        self.salt = salt
        
    def __repr__(self):
        return "<User('%s')>" % (self.username)
    
    def __init__(self,username,email_address,password_plain=None):
        self.username = username
        
        if not password_plain:
            password_plain = "".join(random.sample(string.letters + string.digits,8))
        
        self.set_password(password_plain)
        self.email_address = email_address
    
    def has_ability(ability_name):
        for ability_obj in self.abilities:
            if ability_obj.system_name == ability_name:
                return True
            
        for group in self.groups:
            if group.has_ability(ability_name):
                return True
        
        return False
    
    # }}}

user_group = Table('user_group',Base.metadata, # {{{
    Column('user_id',Integer,ForeignKey('user_table.id')),
    Column('group_id',Integer,ForeignKey('group_table.id'))
) # }}}

class Group(Base):
    """
    User gorup
    """
    # {{{
    __tablename__ = 'group_table'

    id = Column(Integer,Sequence('group_table_id_seq'),primary_key=True)
    name = Column(String(255))
    system_name = Column(String(255))
    
    users = relation('User',secondary=user_group,backref='groups')

    def __repr__(self):
        return "<Group('%s')>" % (self.name)
    
    def __init__(self,name,system_name):
        self.name = name
        self.system_name = system_name
    
    def has_ability(self, ability_name):
        for ability_obj in self.abilities:
            if ability_obj.system_name == ability_name:
                return True
        
        return False
    
    # }}}

user_ability = Table('user_ability',Base.metadata, # {{{
    Column('user_id',Integer,ForeignKey('user_table.id')),
    Column('ability_id',Integer,ForeignKey('ability.id'))
) # }}}

group_ability = Table('group_ability',Base.metadata, # {{{
    Column('group_id',Integer,ForeignKey('group_table.id')),
    Column('ability_id',Integer,ForeignKey('ability.id'))
) # }}}

class Ability(Base):
    """
    Abilities, assigned to groups and users
    """
    # {{{
    __tablename__ = 'ability'
    
    id = Column(Integer,Sequence('ability_id_seq'),primary_key=True)
    name = Column(String(255))
    system_name = Column(String(255))
    
    users = relation('User',secondary=user_ability,backref="abilities")
    groups = relation('Group',secondary=group_ability,backref="abilities")
    
    def __repr__(self):
        return "<Ability('%s')>" % self.system_name
    
    def __init__(self, name, system_name):
        self.name = name
        self.system_name = system_name
    
    # }}}

class Hypervisor(Base):
    """
    A hypervisor
    """
    __tablename__ = 'hypervisor'
    
    id = Column(Integer,Sequence('hypervisor_id_seq'),primary_key=True)
    name = Column(String(255))
    uri = Column(String(1024))
    
    domains = relation('Domain',backref='hypervisor')
    
    _connection = None
    
    def __repr__(self):
        return "<Hypervisor('%s')>" % self.uri
    
    def __init__(self, name, uri):
        self.name = name
        self.uri = uri
    
    def connect(self):
        self._connection = libvirt.open(self.uri)
    
    def is_connected(self):
        return self._connection is not None and self._connection.isAlive() == 1
    
    def list_domains(self):
        if not self.is_connected():
            self.connect()
        
        return [self._connection.lookupByName(n) for n in self._connection.listDefinedDomains()] + [self._connection.lookupByID(i) for i in self._connection.listDomainsID()]

class Domain(Base):
    """
    Maps a domain (by UUID) to a user.
    """
    __tablename__ = 'domain'
    
    id = Column(Integer,Sequence('domain_id_seq'),primary_key=True)
    uuid = Column(String(36))
    user_id = Column(ForeignKey('user_table.id'))
    hypervisor_id = Column(ForeignKey('hypervisor.id'))
    
    def __repr__(self):
        return "<Domain('%s'>)" % (self.uuid)
    
    def __init__(self, uuid, user, hypervisor):
        self.uuid = uuid
        self.user_id = user.id
        self.hypervisor_id = hypervisor.id
    

class OneTimeToken(Base):
    """
    A token that can be sent to the client (in unreadable form) and sent
    back to verify a command's origin.
    """
    # {{{
    __tablename__ = 'one_time_token'
    
    id = Column(Integer,Sequence('one_time_token_id_seq'),primary_key=True)
    token = Column(String(255),index=True)
    timestamp = Column(DateTime)
    used = Column(Boolean)
    user_id = Column(ForeignKey('user_table.id'))
    
    def __repr__(self):
        return "<OneTimeToken('%s')>" % (self.token)
    
    def __init__(self,user):
        assert user is not None
        
        # Generate a random token
        self.token = base64.b64encode(os.urandom(200))[:255]
        self.timestamp = datetime.datetime.now()
        self.used = False
        self.user_id = user.id
    
    def check_and_expire(self,user):
        """
        Returns whether or not a token has been used before or is invalid,
        and marks the token as used.
        """
        
        seconds = 60 * 15
        delta = datetime.timedelta(seconds=seconds)
        
        try:
            assert user is not None
            assert self.user_id == user.id
            assert self.used == False and self.timestamp + delta > datetime.datetime.now()
        except AssertionError:
            return True
        
        self.used = True
        
        if session is None:
            database.session.commit()
        else:
            session.commit()
        
        return False
    # }}}
