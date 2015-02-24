#!/usr/bin/python

from os import mkdir, listdir
from os.path import abspath, isdir, join, isfile
from shutil import copy2
import ConfigParser
import sqlite3 as lite

from src.secure_storage import setup as SecureSetup
from src.svncontrols import setup as SvnSetup


directories_to_create = ['SecureStorage', 'SvnRepository', 'Uploads', 'Database','XmlSchemas']
AKU_Files = abspath(raw_input("'Please enter where do you want to store AKU's Files: \n"))
config = ConfigParser.ConfigParser()


def create_directories():
	if not isdir(join(AKU_Files, "AkuFiles/")):
		mkdir(join(AKU_Files, "AkuFiles/"))

	for dire in directories_to_create:
		if not isdir(join(AKU_Files, "AkuFiles/", dire)):
			print('Creating Directory ' + dire)
			mkdir(join(AKU_Files, "AkuFiles/", dire))
		else:
			print(dire + " directory has already been created")

		print('\tDirectory Created at ' + abspath(join(AKU_Files, "AkuFiles/", dire)))


def create_config():

	config.add_section('Locations')

	for dire in directories_to_create:
		config.set('Locations', dire, abspath(join(AKU_Files, "AkuFiles/", dire)))

	config.add_section('Database')
	config.set('Database', 'PATH_TO_DB',abspath(join(AKU_Files, "AkuFiles/", 'Database/history.db')))

	# Set the URL for the SVN Repository
	config.add_section('SVN')
	config.set('SVN', 'URL','https://svn.alma.cl/p2/trunk/ITS/config/CDB-COMMON/TMCDB_DATA/')
	config.set('SVN', 'PATH_IN_REPO', 'TMCDB_DATA/')

	cfg_file = open(join(AKU_Files, 'Configuration/conf.ini'), 'w')
	config.write(cfg_file)
	cfg_file.close()


def create_database():
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


def copy_necessary_files():
	my_path = 'xmlschemas'
	only_files = [f for f in listdir(my_path) if (isfile(join(my_path,f)))]
	print(only_files)
	for file in only_files:
		try:
			copy2(join(my_path, file), config.get('Locations', 'XmlSchemas'))
		except Exception as e:
			print(e)
			raise e



create_directories()
create_config()
create_database()
copy_necessary_files()

SecureSetup('Configuration/conf.ini')
SvnSetup('Configuration/conf.ini')


