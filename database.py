import sqlite3 as lite


class Database():
	connected = False
	pointer = None



	def __init__(self, dbName):
		self.name = dbName

	def connect(self):
		try:
			self.pointer = lite.connect(self.name)
			self.connected = True
			return  True
		except lite.Error, e:
			print "Error %s:" % e.args[0]
			return False


	def disconnect(self):
		if self.pointer:
			self.pointer.close()
			self.connected = False

	def executeReadSQL(self,sentence):
		self.connect()
		resp = self.pointer.execute(sentence)
		data = resp.fetchall()
		self.disconnect()
		return data


	def executeWriteSQL(self,sentence):
		self.connect()
		resp = self.pointer.execute(sentence)
		self.pointer.commit()
		self.disconnect()


class Aku_Database(Database):

	def get_device_id(self,deviceName):
		command = "SELECT id FROM device WHERE name == '" + deviceName + "';"
		return self.executeReadSQL(command)[0][0]

	def get_ste_id(self,steName):
		command = "SELECT id FROM ste WHERE name == '" + steName + "';"
		return self.executeReadSQL(command)[0][0]

	def get_all_ste(self):
		command = "SELECT name FROM ste;"
		return self.executeReadSQL(command)

	def get_all_devices(self):
		command = "SELECT name FROM device;"
		return self.executeReadSQL(command)

	def add_upload(self, data):
		ste_id = str(self.get_ste_id(data['ste']))
		device_id = str(self.get_device_id(data['device']))
		ticket = data['ticket']
		filename = data['filename']
		username = data['username']
		if 'serial' in data:
			serial = str(data['serial'])

		scheme = "INSERT INTO uploads (ste_id, device_id, ticket, filename, username"
		values = "VALUES (" + ste_id + ", " + device_id + ", '" + ticket + "', '"+ filename + "', '"+ username

		if data['device']=="IFProc":
			scheme += ", serial_number"
			values += "', " + str(serial)

		scheme += ") "
		values += ");"


		command = scheme + values
		print(command)
		self.executeWriteSQL(command)



#test_dic = {'ste' : 'AOS',
#			'device' : 'IFProc',
#			'ticket' : 'AAA-123',
#			'filename' : 'Archivotest.xml',
#			'serial' : 23234,\
#			'username' : 'teohoch'}



