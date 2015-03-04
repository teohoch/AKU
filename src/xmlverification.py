import subprocess
import ConfigParser
from lxml import etree
from xml.dom.minidom import parse
from os.path import join

from database import Aku_Database
from xmlProcessing.integratedFreqCheck import freq_order_check
from xmlProcessing.integratedPolarizationAngle import polarization_check
from xmlProcessing.ifpProccesing import ifpgenerator


class XmlVerification():
	def __init__(self, conf_path, filename, device):

		self.config = ConfigParser.ConfigParser()
		self.config.read(conf_path)

		self.conf_path = conf_path
		self.filename = filename
		self.device = device
		self.SCHEMA_PATH = join(self.config.get('Locations', 'svnrepository'), self.config.get('SVN', 'path_in_repo'))

	def xml_well_formed(self):
		try:
			parse(self.filename)
			return [True,'File is well formed']
		except:
			return [False,'File is NOT well formed, according to the XML standard.']

	def correspond_to_device(self):
		try:
			p = subprocess.Popen(["grep", '-c', self.device, self.filename], stdout=subprocess.PIPE)
			if p.communicate()[0][0]=='1':
				return [True,'File corresponds to the inputted device.']
			else:
				return [False, "File doesn't correspond to the inputted device."]
		except subprocess.CalledProcessError:
			return [False, "File doesn't correspond to the inputted device."]

	def validate_scheme(self):
		db = Aku_Database(self.conf_path)
		a = self.SCHEMA_PATH
		b = db.get_device_scheme(self.device)
		c = join(a,b)
		print a
		print b
		print(c)
		f = open(c)
		schema_doc = etree.parse(f)
		schema = etree.XMLSchema(schema_doc)

		d = open(self.filename)
		file_doc = etree.parse(d)

		if schema.validate(file_doc):
			return [True,'The configuration file corresponds to its Schema.']
		log = schema.error_log.last_error
		return [False, "The configuration file doesn't correspond to its Schema. Line: " +str(log.line) + " <"+log.message + '>']

	def freq_order_file_check(self):
		if freq_order_check(self.filename):
			return [True, "The configuration file has its Frequencies sorted correctly."]
		return [False, "The configuration file doesn't have it Frequencies sorted correctly."]

	def polarization_angle_check(self):
		if polarization_check(self.filename):
			return [True, "The configuration file has its Polarization Angles correctly set."]
		return [False, "The configuration file has its Polarization Angles INCORRECTLY set."]

	def ifpProcessing(self, serial):
		return ifpgenerator(self.filename, serial, self.config.get('Locations','Uploads'))







