import paramiko

def ssh_update_assemblies(ste):
	"""
	Simple function that connects to the corresponding STE through SSH and runs the UpdateAssemblies command
	:param ste: The STE where to update
	:return: Status of the operation
	"""
	host = ste + '-gns.osf.alma.cl'
	user = 'jreveco'
	password = 'mynewshinypass'

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(host, username=user, password=password)
		stdin, stdout, stderr = client.exec_command('./updateAssembliesFake')
		client.close()
		return True
	except:
		client.close()
		return False



