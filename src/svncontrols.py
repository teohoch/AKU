import pysvn
from os import remove
from os.path import isfile, join
from shutil import copy2
from secure_storage import SecureKey
import filecmp
import ConfigParser
from diffchecker import show_differences


class AkuSvn():
	"""
	Class for adding the configuration files to the Repository

	Allows for checking if the file must be updated or added, as well as copying the files from other directories to the
	repository's directory
	"""

	def __init__(self, confPath):
		"""
		Init function for the class, initialices the repository, doing a checkout if it isn't
		:param URL:  URL to the SVN Repository
		:param destinationPath: Local directory where the repository will be created
		:param pathInRepo: Path within the repository to the configuration files
		:return: None
		"""

		self.configPath = confPath

		config = ConfigParser.ConfigParser()
		config.read(confPath)

		self.URL = config.get('SVN', 'URL')
		self.destinationPath = config.get('Locations', 'SvnRepository')
		self.pathInRepo = config.get('SVN', 'PATH_IN_REPO')
		self.client = pysvn.Client()
		self.client.callback_ssl_server_trust_prompt = self.__callback_ssl_server_trust_prompt
		self.client.callback_get_login = self.__get_login
		self.client.checkout(self.URL, self.destinationPath)


	def __callback_ssl_server_trust_prompt( trust_data ):
		return True, trust_data['failures'], True

	def __get_login(self, realm, username, may_save):
		user = SecureKey('SvnUser', self.configPath)
		password = SecureKey('SvnPass', self.configPath)

		return True, user.retrieve(), password.retrieve(), True

	def __add_or_update(self, filename):
		"""
		Checks if the file is in the repository, as a way to know if we have to update or add the file

		:param filename:
		:return: True -> add, False -> update
		"""
		return not isfile(join(self.destinationPath, self.pathInRepo, filename))

	def __addFile(self, filepath, filename):
		"""
		Add the specied file to the repository.

		First we copy the file to the repository directory, then we add it to the repository.

		:param filepath: Path to the directory where the file is
		:param filename: Name of the file to add
		:return: Status of the operation. True is success, False is Failure
		"""
		try:
			finalPosition = join(self.destinationPath, self.pathInRepo, filename)
			copy2(join(filepath, filename), finalPosition)
			self.client.add(finalPosition)
			return True
		except:
			return False

	def __updateFile(self, filepath, filename):
		finalPosition = join(self.destinationPath, self.pathInRepo, filename)

		if not filecmp.cmp(join(filepath, filename), finalPosition):
			try:
				copy2(join(filepath, filename), finalPosition)
				return True
			except:
				raise
		else:
			return False

	def uploadToRepo(self, filepath, filename, user, force):
		"""
		Uploads the file to the repository
		:param filepath: The path to the file to be uploaded
		:param filename: The name of the file to be uploaded
		:param user: The username of the user uploading the file
		:return: An array containing the action taken by Svn (add => True or update => False), the status of the action
		(True if it was a success, False if there was nothing to update, or adding failed)
		and a message. If the update wasn't forced, it'll return the differences between the files. If the update was
		forced but it failed, it will return  the differences between the files. Any other way, message will be empty
		"""
		self.client.update(self.destinationPath, recurse=True)
		doaction = self.__add_or_update(filename)

		status = True
		out_message = ''

		if doaction:
			status = self.__addFile(filepath, filename)
		else:
			if force:
				status = self.__updateFile(filepath, filename)
				print 'with force ' + str(status)
				if not status:
					out_message = show_differences(join(filepath, filename), join(self.destinationPath,self.pathInRepo, filename))
			else:
				status = not filecmp.cmp(join(filepath, filename), join(self.destinationPath, self.pathInRepo, filename))
				if status:
					out_message = show_differences(join(filepath, filename), join(self.destinationPath,self.pathInRepo, filename))

		if status and (force or doaction):
			message = "The configuration file " + filename
			action = ('added' if doaction else 'updated')
			message += " has been " + action + ' by ' + user + ' according to '

			try:
				print self.client.checkin(self.destinationPath, message, recurse=True)
				remove(join(filepath, filename))
			except Exception as e:
				print e

		print([doaction, status, out_message])
		return [doaction, status, out_message]


def setup(configPath):
	print('Checking Out the ALMA Configurations Repository')
	AkuSvn(configPath)
	print('\tCheckout Complete.')


if __name__ == '__main__':
	setup('../Configuration/conf.ini')