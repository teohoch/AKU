from os import listdir, rename
from os.path import isfile, join, splitext
import subprocess



def transform(mypath):
	onlyfiles = [ f for f in listdir(mypath) if (isfile(join(mypath,f)) and splitext(f)[1]=='' )]

	regex = 'ASSEMBLY value=\"([a-zA-Z]+\d*)'
	number = 0
	for a in onlyfiles:
		try:
			output = subprocess.check_output(['grep', '-E', regex, join(mypath,a)])
			output= output.split('"')[1]

			rename(join(mypath,a),join(mypath, (output+'-'+str(number)+'.xml')))
			print a + '  ==>  ' + (output+'-'+str(number))
			number += 1


		except subprocess.CalledProcessError:
			pass

def lower(mypath):
	onlyfiles = [ f for f in listdir(mypath) if (isfile(join(mypath,f)))]
	for a in onlyfiles:
		filepath =join(mypath,a)
		rename(filepath, filepath.lower())


path = 'xmlTest'
xml_schemes = 'xmlschemas'

lower(xml_schemes)

