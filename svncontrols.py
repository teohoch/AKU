import pysvn
from os import remove
from os.path import isfile, join
from shutil import copy2
import filecmp



class AkuSvn():
	def __init__(self, URL, destinationPath, pathInRepo ):
		self.URL = URL
		self.destinationPath = destinationPath
		self.pathInRepo = pathInRepo
		self.client = pysvn.Client()
		self.client.callback_get_login = self.get_login
		self.client.checkout(URL, destinationPath)

	def get_login(self, realm, username, may_save ):
		username='teohoch'
		password='1234'
		return True, username, password, True


	def add_or_update(self,filename):
		# True -> add, False -> update
		return not isfile(join(self.destinationPath, self.pathInRepo,filename))

	def addFile(self,filepath, filename):
		try:
			finalPosition = join(self.destinationPath,self.pathInRepo,filename)
			copy2(join(filepath, filename),finalPosition)
			self.client.add(finalPosition)
			return True
		except:
			return False

	def updateFile(self, filepath, filename):
		finalPosition = join(self.destinationPath,self.pathInRepo,filename)

		if filecmp.cmp(join(filepath, filename), finalPosition):
			try:
				copy2(join(filepath, filename), finalPosition)
				return True
			except:
				raise
		else:
			return False

	def uploadToRepo(self, filepath,filename, user):
		# True -> Success, False -> Nothing to update
		self.client.update(self.destinationPath, recurse=True)
		doaction = self.add_or_update(filename)
		status = True

		if doaction:
			status = self.addFile(filepath, filename)
		else:
			status = self.updateFile(filepath, filename)

		if status:
			message = "The configuration file " + filename
			action = ('added' if doaction else 'updated')
			message += " has been " + action + ' by ' + user + ' according to '

			self.client.checkin(self.destinationPath, message, recurse=True)
			remove(join(filepath,filename))

		return status

svn = AkuSvn('http://localhost/svn/almarepo/', 'svnrepo', 'TMCDB_DATA/')
svn.uploadToRepo('/home/teohoch/PycharmProjects/AKU/xmlTest', 'WCA10-33.xml', 'teohoch')