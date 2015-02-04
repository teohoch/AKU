import pxssh

def ssh_update_assemblies(ste):
	"""
	Simple function that connects to the corresponding STE through SSH and runs the UpdateAssemblies command
	:param ste: The STE where to update
	:return: Status of the operation
	"""
	host = ste + '-gns.osf.alma.cl'
	user = 'jreveco'
	password = 'mynewshinypass'
	try:
		s = pxssh.pxssh()
		if not s.login (host, username=user,password=password):
			#print "SSH session failed on login."
			#print str(s)
			print 'no Login'
			return False
		else:
			#print "SSH session login successful"
			s.sendline ('./updateAssembliesFake')
			s.prompt()         # match the prompt
			#print s.before     # print everything before the prompt.
			s.logout()
			return True
	except Exception as e:
		print e
		return False

