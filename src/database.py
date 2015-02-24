import sqlite3 as lite
import ConfigParser

class Database():
	"""
	General purpose class for connecting to a Sqlite Database
	"""
	connected = False
	pointer = None



	def __init__(self, confPath):
		"""
		Initializes the instance, setting the path to the database
		:param confPath: path to the configuration file
		:return: None
		"""
		config = ConfigParser.ConfigParser()
		config.read(confPath)
		self.name = config.get('Database', 'PATH_TO_DB')

	def connect(self):
		"""
		Connects to the specified database. If it doesn't exists, it creates it
		:return: If successful, returns True
		"""
		try:
			self.pointer = lite.connect(self.name)
			self.connected = True
			return  True
		except lite.Error, e:
			print "Error %s:" % e.args[0]
			return False


	def disconnect(self):
		"""
		Disconnects from the Database
		:return: None
		"""
		if self.pointer:
			self.pointer.close()
			self.connected = False

	def executeReadSQL(self,sentence):
		"""
		Executes a read SQL command, such as SELECT
		:param sentence: Command to be executed
		:return: The response from the Database
		"""
		self.connect()
		resp = self.pointer.execute(sentence)
		data = resp.fetchall()
		self.disconnect()
		return data


	def executeWriteSQL(self,sentence):
		"""
		Executes a SQL Write command, such as Insert, Delete or Modify
		:param sentence: Command to be executed
		:return: None
		"""
		self.connect()
		resp = self.pointer.execute(sentence)
		self.pointer.commit()
		self.disconnect()


class Aku_Database(Database):
	"""
	A more specialized version of the database class, adapted specifically for AKU
	"""

	def get_device_id(self,deviceName):
		"""
		Returns the device id from the name
		:param deviceName: name of the device
		:return: Device ID
		"""
		command = "SELECT id FROM device WHERE name == '" + deviceName + "';"
		return self.executeReadSQL(command)[0][0]

	def get_ste_id(self,steName):
		"""
		Returns the Ste id from the name
		:param steName: name of the Ste
		:return: STE ID
		"""
		command = "SELECT id FROM ste WHERE name == '" + steName + "';"
		return self.executeReadSQL(command)[0][0]

	def get_all_ste(self):
		"""
		Returns all the STE's present in the Database
		:return: All the STE's in the Database
		"""
		command = "SELECT id, name FROM ste;"
		return self.executeReadSQL(command)

	def get_all_devices(self):
		"""
		Returns all the devices in the Database
		:return: List of all devices, eac device in the form [value, name]
		"""
		command = "SELECT value, name FROM device;"
		return self.executeReadSQL(command)
	def get_all_devices_with_id(self):
		"""
		Returns all the devices in the Database
		:return: List of all devices, eac device in the form [value, name]
		"""
		command = "SELECT id, name FROM device;"
		return self.executeReadSQL(command)

	def get_device_from_value(self, value):
		"""
		:param value: Value assigned to the device
		:return: Name of the device
		"""
		command = "SELECT name FROM device WHERE value=='" + value + "';"
		return self.executeReadSQL(command)

	def add_upload(self, data):
		"""
		Adds a new entry into the Uploads table.
		:param data: a dictionary with the following keys: ste, device, ticket, filename, username, action and serial (optional)
		:return:
		"""
		ste_id = str(self.get_ste_id(data['ste']))
		device_id = str(self.get_device_id(data['device']))
		ticket = data['ticket']
		filename = data['filename']
		username = data['username']
		action = str(int(data['action']))
		if 'serial' in data:
			serial = str(data['serial'])

		scheme = "INSERT INTO uploads (ste_id, device_id, ticket, filename, username, action"
		values = "VALUES (" + ste_id + ", " + device_id + ", '" + ticket + "', '"+ filename + "', '"+ username + "', "+ action

		if data['device']=="IFProc":
			scheme += ", serial_number"
			values += ", " + str(serial)

		scheme += ") "
		values += ");"


		command = scheme + values
		try:
			self.executeWriteSQL(command)
			return True
		except Exception as e:
			print 'error in sqlwrite'
			print e
			raise

	def get_all_uploads(self):
		command = 'SELECT * FROM uploads ORDER BY date DESC LIMIT;'
		return self.executeReadSQL(command)

	def get_n_uploads(self, n):
		command = 'SELECT * FROM uploads ORDER BY date DESC LIMIT ' + str(n) + ';'
		return self.executeReadSQL(command)

	def get_device_regex(self, device):
		command = "SELECT regex, regex_message FROM device WHERE name=='" + device+ "';"
		return self.executeReadSQL(command)[0]
