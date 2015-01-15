import xml.parsers.expat
import subprocess

def parsefile(filename):
	parser = xml.parsers.expat.ParserCreate()
	parser.ParseFile(open(filename, "r"))


def xml_well_formed(filename):
	try:
		parsefile(filename)
		return True
	except Exception, e:
		return False

def correspond_to_device(filename):

	output = subprocess.check_output(['grep', 'py2.py', '-i', 'test.txt'])
	return False

