import subprocess
from lxml import etree
from xml.dom.minidom import parse
from os.path import join

from xmlProcessing.integratedFreqCheck import freq_order_check
from xmlProcessing.integratedPolarizationAngle import polarization_check
from xmlProcessing.ifpProccesing import ifpgenerator


SCHEMA_PATH = '/home/teohoch/PycharmProjects/AKU/xmlschemas'


def xml_well_formed(filename):
	try:
		parse(filename)
		return [True,'File is well formed']
	except:
		return [False,'File is NOT well formed, according to the XML standard.']

def correspond_to_device(filename, device):
	try:
		subprocess.check_output(['grep','-c', device, filename])
		return [True,'File corresponds to the inputted device.']
	except subprocess.CalledProcessError:
		return [False, "File doesn't correspond to the inputted device."]

def validate_scheme(filename, device):
	f = open(join(SCHEMA_PATH, (device.lower()+'.xsd')))
	schema_doc = etree.parse(f)
	schema = etree.XMLSchema(schema_doc)

	d = open(filename)
	file_doc = etree.parse(d)

	if schema.validate(file_doc):
		return [True,'The configuration file corresponds to its Schema.']
	log = schema.error_log.last_error
	return [False, "The configuration file doesn't correspond to its Schema. Line: " +str(log.line) + " <"+log.message + '>']

def freq_order_file_check(filename):
	if freq_order_check(filename):
		return [True, "The configuration file has its Frequencies sorted correctly."]
	return [False, "The configuration file doesn't have it Frequencies sorted correctly."]

def polarization_angle_check(filename):
	if polarization_check(filename):
		return [True, "The configuration file has its Polarization Angles correctly set."]
	return [False, "The configuration file has its Polarization Angles INCORRECTLY set."]

def ifpProcessing(filename, serial, destpath):
	return ifpgenerator(filename,serial,destpath)

path = '/home/teohoch/PycharmProjects/AKU/xmlTest'

#print(xml_well_formed(join(path, 'ColdCart3-17.xml')))
#print correspond_to_device(join(path, 'ColdCart3-17.xml'), 'ColdCart3')
#print validate_scheme(join(path, 'ColdCart3-17.xml'), 'Coldcart3')