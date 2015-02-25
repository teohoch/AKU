import ConfigParser

import paramiko


def ssh_update_assemblies(ste, config_file):
	"""
	Simple function that connects to the corresponding STE through SSH and runs the UpdateAssemblies command
	:param ste: The STE where to update
	:return: Status of the operation
	"""
	config = ConfigParser.ConfigParser()
	config.read(config_file)
	host = ste + '-gns.osf.alma.cl'
	user = config.get('SSH', 'USER')
	key = paramiko.RSAKey.from_private_key_file(config.get('SSH', 'KEY_FILE'))

	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		client.connect(host, username=user, pkey=key)
		stdin, stdout, stderr = client.exec_command('./updateAssembliesFake')
		client.close()
		return True
	except:
		client.close()
		return False

if __name__ == '__main__':
	import os
	path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Configuration/conf.ini'))
	ssh_update_assemblies('AOS',path)


