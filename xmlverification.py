import subprocess
from lxml import etree
from xml.dom.minidom import parse
from integratedFreqCheck import freq_order_check
from integratedPolarizationAngle import polarization_check


from os.path import join

SCHEMA_PATH = '/home/teohoch/PycharmProjects/AKU/xmlschemas'


def xml_well_formed(filename):
	try:
		return parse(filename)
	except:
		raise

def correspond_to_device(filename, device):
	try:
		subprocess.check_output(['grep','-c', device, filename])
		return True
	except subprocess.CalledProcessError:
		return False

def validate_scheme(filename, device):
	f = open(join(SCHEMA_PATH, (device.lower()+'.xsd')))
	schema_doc = etree.parse(f)
	schema = etree.XMLSchema(schema_doc)

	d = open(filename)
	file_doc = etree.parse(d)

	return schema.validate(file_doc)

def freq_order_file_check(filename):
	return freq_order_check(filename)

def polarization_angle_check(filename):
	return polarization_check(filename)

path = '/home/teohoch/PycharmProjects/AKU/xmlTest'

#print(xml_well_formed(join(path, 'ColdCart3-17.xml')))
#print correspond_to_device(join(path, 'ColdCart3-17.xml'), 'ColdCart3')
#print validate_scheme(join(path, 'ColdCart3-17.xml'), 'Coldcart3')