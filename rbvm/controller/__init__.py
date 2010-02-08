import cherrypy
import hashlib
import cherrypy.lib.sessions
import rbvm.lib.sqlalchemy_tool as database
import rbvm.lib.template as template
from rbvm.lib.auth import get_user, require_login, require_nologin
from rbvm.model.database import *
import rbvm.config as config
import rbvm.vmmon

class Root:
	@cherrypy.expose
	@require_login
	@template.output('index.html')
	def index(self):
		"""
		Render the homepage
		"""
		user = get_user()
		vms = database.session.query(VirtualMachine).filter(VirtualMachine.user_id==user.id).all()
		
		vm_list = []
		for vm in vms:
			vm_d = {'id':vm.id,'name':vm.name,'disk_images':[],'ram':None,'cpu_cores':None}
			for property in list(vm.properties):
				if property.key == 'ram':
					vm_d['ram'] = property.value
				elif property.key == 'disk_image':
					vm_d['disk_images'].append(property.value)
				elif property.key == 'cpu_cores':
					vm_d['cpu_cores'] = property.value
			vm_list.append(vm_d)
		
		return template.render(vm_list=vm_list)
	
	@cherrypy.expose
	@require_login
	@template.output('manage.html')
	def manage(self, id=None):
		"""
		Show all VM information and management options
		"""
		try:
			id = int(id)
		except ValueError:
			return template.render(vm=None,error="Invalid virtual machine ID")
		
		user = get_user()
		try:
			vm = database.session.query(VirtualMachine).filter(VirtualMachine.id==id).filter(VirtualMachine.user_id==user.id).one()
			assert vm is not None
		except:
			return template.render(vm=None,error="Virtual machine was not found")
		
		vm.status = rbvm.vmmon.check_vm_status(vm)
		
		token = OneTimeToken(user)
		database.session.add(token)
		database.session.commit()
		
		return template.render(vm=vm,token=token)
	
	@cherrypy.expose
	@require_login
	@template.output('poweron.html')
	def poweron(self, id=None, token=None):
		"""
		Check the one time token and power on the VM
		"""
		if id is None or token is None:
			print "a"
			return template.render(error="Missing ID or token",vm=None,message=None,vnc_password=None,hostname=None,vnc_port=None)
		
		user = get_user()
		if user is None:
			print "b"
			return template.render(error="Invalid login",vm=None,message=None,vnc_password=None,hostname=None,vnc_port=None)
		
		token_object = database.session.query(OneTimeToken).filter(OneTimeToken.token==token).first()
		if token_object is None or token_object.check_and_expire(user) is True:
			print "c"
			return template.render(error="Token error",vm=None,message=None,vnc_password=None,hostname=None,vnc_port=None)
		
		try:
			id = int(id)
		except ValueError:
			print "d"
			return template.render(error="Invalid ID",vm=None,message=None,vnc_password=None,hostname=None,vnc_port=None)
		
		vm = database.session.query(VirtualMachine).filter(VirtualMachine.id==id).first()
		if vm is None:
			return template.render(error="Virtual machine not found",vm=None,message=None,vnc_password=None,hostname=None,vnc_port=None)
		
		try:
			assert vm.user_id == user.id
		except:
			return template.render(error=None,vm=vm,message="VM permissions error",vnc_password=None,hostname=None,vnc_port=None)
		
		vnc_password = rbvm.vmmon.power_on(vm)
		if vnc_password is not None:
			return template.render(error=None,vm=vm,message="VM power on successful",vnc_password=vnc_password,hostname=config.VNC_IP,vnc_port=5900+vm.id)
		else:
			return template.render(error=None,vm=vm,message="VM power on failed",vnc_password=None,hostname=None,vnc_port=None)
	
	@cherrypy.expose
	@require_nologin
	@template.output('login.html')
	def login(self, username=None, password=None):
		if username and password:
			user_object = database.session.query(User).filter(User.username == username).first()
			if not user_object:
				return template.render(error='Invalid username or password')
			pwhash = hashlib.sha256()
			pwhash.update(password + user_object.salt)
			hash_hex = pwhash.hexdigest()
			
			if hash_hex == user_object.password:
				cherrypy.session['authenticated'] = True
				cherrypy.session['username'] = user_object.username
				raise cherrypy.HTTPRedirect('/')
		
		return template.render()
	
	@cherrypy.expose
	@template.output('logout.html')
	def logout(self):
		cherrypy.lib.sessions.expire()
		return template.render()
