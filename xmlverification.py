import xml.parsers.expat
import subprocess
from lxml import etree

from os.path import join

SCHEMA_PATH = 'xmlschemas'

def parsefile(filename):
	parser = xml.parsers.expat.ParserCreate()
	parser.ParseFile(open(filename, "r"))


def xml_well_formed(filename):
	try:
		parsefile(filename)
		return True
	except Exception, e:
		return False

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

path = 'xmlTest'

print(xml_well_formed(join(path, 'ColdCart3-17.xml')))
print correspond_to_device(join(path, 'ColdCart3-17.xml'), 'ColdCart3')
print validate_scheme(join(path, 'ColdCart3-17.xml'), 'dtx')