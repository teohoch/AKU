from Crypto.Cipher import AES
from os.path import isfile,join
import os
import base64
import pickle
import ConfigParser

from pbkdf2 import PBKDF2



### Settings ###

saltSeed = 'd9fy07weay98387f73'  # MAKE THIS YOUR OWN RANDOM STRING

PASSPHRASE_SIZE = 64  # 512-bit passphrase
KEY_SIZE = 32  # 256-bit key
BLOCK_SIZE = 16  # 16-bit blocks
IV_SIZE = 16  # 128-bits to initialise
SALT_SIZE = 8  # 64-bits of salt



class SecureKey():
	"""
	This class provides a semi-secure way to store sensitive information, such as repository passwords and usernames
	"""
	def __init__(self, key, configPath):
		"""
		Initialize the instance, saving the key, generating salt for encryption, and if the key already exists, loading
		its contents
		:param key: A symbol to identify the value stored ex: 'SVN', 'pass', etc.
		"""
		self.key = key
		Config = ConfigParser.ConfigParser()
		Config.read(configPath)
		self.storageLocation = Config.get('Locations', 'SecureStorage')
		self.passLocation = join(self.storageLocation, key)
		self.salt = self.__get_salt_for_key()
		if isfile(self.storageLocation+'/' + self.key + '.p') and isfile(self.storageLocation+'/' + self.key):
			self.__load_db()



	def __load_db(self):
		"""
		Load a existing instance of the class saved in the disk.
		"""
		try:
			with open(self.passLocation) as f:  # Load the file with the encrypted pass
				db = pickle.load(f)
				self.__encryptedpass = db[self.key]
			with open(self.passLocation + '.p') as fi:  # Load the file with the coded passphrase
				phrase = fi.read()
				if len(phrase)!=0:
					self.phrase = base64.b64decode(phrase)
					return True
				else:
					return False
		except:
			return False


	def __get_salt_for_key(self):
		"""
		Generates salt for the encryption, using a saltSeed predefined.
		:return:
		"""
		return PBKDF2(self.key, saltSeed).read(SALT_SIZE)  # Salt is generated as the hash of the key with it's own salt acting like a seed value

	def __encrypt(self, plaintext):
		""" Pad plaintext, then encrypt it with a new, randomly initialised cipher. Will not preserve trailing whitespace in plaintext!
			:returns encrypted pass
		"""

		# Initialise Cipher Randomly
		initvector = os.urandom(IV_SIZE)

		# Prepare cipher key:
		key = PBKDF2(self.phrase, self.salt).read(KEY_SIZE)

		cipher = AES.new(key, AES.MODE_CBC, initvector)  # Create cipher

		self.__encryptedpass = initvector + cipher.encrypt(plaintext + ' ' * (BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)))

	def __decrypt(self):
		""" Reconstruct the cipher object and decrypt. Will not preserve trailing whitespace in the retrieved value!
		:rtype : Plaintext Password
		"""

		salt = self.__get_salt_for_key()
		# Prepare cipher key:
		key = PBKDF2(self.phrase, salt).read(KEY_SIZE)

		# Extract IV:
		initVector = self.__encryptedpass[:IV_SIZE]
		ciphertext = self.__encryptedpass[IV_SIZE:]

		cipher = AES.new(key, AES.MODE_CBC, initVector)  # Reconstruct cipher (IV isn't needed for decryption so is set to zeros)

		return cipher.decrypt(ciphertext).rstrip(' ')  # Decrypt and depad

	def store(self, plaintext):
		""" Store key-value pair safely and save to disk.

		"""
		with open(self.passLocation + '.p', 'w') as f:
			self.phrase = os.urandom(PASSPHRASE_SIZE) # Random passphrase
			f.write(base64.b64encode(self.phrase))

		self.__encrypt(plaintext)
		db = {self.key : self.__encryptedpass}
		with open(self.passLocation, 'w') as fi:
			pickle.dump(db, fi)

	def retrieve(self):
		return self.__decrypt()

def setup(path):
	from getpass import getpass

	user = SecureKey('SvnUser', path)
	password = SecureKey('SvnPass', path)

	user.store(raw_input('Please input the User for the ALMA Configuration Repository: \n'))
	password.store(getpass('Please input the Password for the ALMA Configuration Repository:\n'))


if __name__ == '__main__':

	path = (os.path.abspath('../Configuration/conf.ini'))
