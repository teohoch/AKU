#!/usr/bin/python

from os import mkdir, remove
from os.path import abspath, isdir, join, isfile, dirname
from shutil import copy2, rmtree
import ConfigParser
import sqlite3 as lite
import argparse

from src.secure_storage import setup as SecureSetup
from src.svncontrols import setup as SvnSetup


directories_to_create = ['SecureStorage', 'SvnRepository', 'Uploads', 'Database']
AKU_Files = ''
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
	config.set('Locations', "AkuFiles" , abspath(join(AKU_Files, "AkuFiles/")))

	for dire in directories_to_create:
		config.set('Locations', dire, abspath(join(AKU_Files, "AkuFiles/", dire)))

	config.add_section('Database')
	config.set('Database', 'PATH_TO_DB',abspath(join(AKU_Files, "AkuFiles/", 'Database/history.db')))

	# Set the URL for the SVN Repository
	config.add_section('SVN')
	config.set('SVN', 'URL','https://svn.alma.cl/p2/trunk/ITS/config/CDB-COMMON/TMCDB_DATA/')
	config.set('SVN', 'PATH_IN_REPO', 'TMCDB_DATA/')

	# Set Configuration for SSH Connection
	config.add_section('SSH')
	config.set('SSH', 'USER', raw_input("'Please enter the Username to use when connecting by SSH: \n"))
	config.set('SSH', 'KEY_FILE', raw_input("'Please enter where the SSH Private Key used for authentication is stored: \n"))

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

parser = argparse.ArgumentParser()


parser.add_argument('-d', dest='create_database', action='store_true', help='Create database for AKU')
parser.add_argument('-wipe',dest='wipe', action='store_true', help='Erase Current AkuFiles, if they exist')
parser = parser.parse_args()

if parser.create_database:
	config.read(abspath(join(dirname(abspath(__file__)), 'Configuration/conf.ini')))
	if parser.wipe and isfile(config.get('Database', 'path_to_db')):
		print('Removing current database...')
		remove(config.get('Database', 'path_to_db'))
		print('\tDatabase Removed.')

	create_database()
elif parser.wipe:
	if isfile(abspath(join(dirname(abspath(__file__)), 'Configuration/conf.ini'))):
		config2 = ConfigParser.ConfigParser()
		config2.read(abspath(join(dirname(abspath(__file__)), 'Configuration/conf.ini')))
		rmtree(config2.get('Locations', 'AkuFiles'))
else:
	if parser.wipe:
		if isfile(abspath(join(dirname(abspath(__file__)), 'Configuration/conf.ini'))):
			config2 = ConfigParser.ConfigParser()
			config2.read(abspath(join(dirname(abspath(__file__)), 'Configuration/conf.ini')))
			rmtree(config2.get('Locations','AkuFiles'))

	AKU_Files = abspath(raw_input("'Please enter where do you want to store AKU's Files: \n"))
	create_directories()
	create_config()
	create_database()
	SecureSetup('Configuration/conf.ini')
	SvnSetup('Configuration/conf.ini')


