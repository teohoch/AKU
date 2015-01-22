from os import mkdir
from os.path import abspath, isdir, join
from shutil import copy2
import ConfigParser
import sqlite3 as lite
from src.secure_storage import setup as SecureSetup
from src.svncontrols import setup as SvnSetup

directories_to_create = ['SecureStorage', 'SvnRepository', 'Uploads', 'Database']
AKU_Files = abspath(raw_input("'Please enter where do you want to store AKU's Files: \n"))

if not isdir(join(AKU_Files, "AkuFiles/")):
	mkdir(join(AKU_Files, "AkuFiles/"))


config = ConfigParser.ConfigParser()
config.add_section('Locations')
for directory in directories_to_create:
	if not isdir(join(AKU_Files, "AkuFiles/", directory)):
		print('Creating Directory ' + directory)
		mkdir(join(AKU_Files, "AkuFiles/", directory))
	else:
		print(directory + " directory has already been created")

	config.set('Locations', directory, abspath(join(AKU_Files, "AkuFiles/", directory)))
	print('\tDirectory Created at ' + abspath(join(AKU_Files, "AkuFiles/", directory)))

config.add_section('Database')
config.set('Database', 'PATH_TO_DB',abspath(join(AKU_Files, "AkuFiles/", 'Database/history.db')))

# Create Database
print('Creating Sqlite Database...')
qry = open('aku_create.sql', 'r').read()
conn = lite.connect(config.get('Database', 'PATH_TO_DB'))
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()

print '\tDatabase created at ' + config.get('Database', 'PATH_TO_DB')

# Copy seed file to Database Directory
copy2('aku_create.sql',join(config.get('Locations', 'Database')))

# Set the URL for the SVN Repository
config.add_section('SVN')
config.set('SVN', 'URL','http://localhost/svn/almarepo/')
config.set('SVN', 'PATH_IN_REPO', 'TMCDB_DATA/')

cfgFile = open(join(AKU_Files, 'Configuration/conf.ini'), 'w')
config.write(cfgFile)
cfgFile.close()

SecureSetup('Configuration/conf.ini')
SvnSetup('Configuration/conf.ini')


