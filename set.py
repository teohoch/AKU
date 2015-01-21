from os import mkdir
from os.path import abspath
import ConfigParser

directories_to_create = ['SecureStorage', 'SvnRepository', 'Uploads', 'Configuration']

mkdir('AkuFiles')


Config = ConfigParser.ConfigParser()
Config.add_section('Locations')
for directory in directories_to_create:
	print('Creating Directory ' + directory)
	mkdir("AkuFiles/" + directory)

	Config.set('Locations', directory, abspath("AkuFiles/" + directory))
	print('Directory Created at ' + abspath("AkuFiles/" + directory))

cfgFile = open('/AkuFiles/Configuration/conf.ini', 'w')

Config.write(cfgFile)



