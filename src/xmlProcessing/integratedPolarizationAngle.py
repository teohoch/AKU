#! /usr/bin/env python
#
# ALMA - Atacama Large Millimiter Array
# (c) Associated Universities Inc., 2012
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to alarms_status the 
# Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#
import xml.dom.minidom
import traceback
import logging
import math


class AngleValidator:
	def __init__(self, filename):
		'''
        Initialize the class attributes.
        '''
		self.filename = filename
		self.angle = {1: [135.0, 225.0],
					  2: [45.0, 135.0],
					  3: [-10.0, 80.0],
					  4: [-170.0, -80.0],
					  5: [-45.0, 45.0],
					  6: [-135.0, -45.0],
					  7: [-53.55, 36.45],
					  8: [0.0, 90.0],
					  9: [-180.0, -90.0],
					  10: [90.0, 180.0]}
		logging.basicConfig(level=logging.ERROR, \
							format="%(asctime)s [%(levelname)s] %(message)s", \
							filename="ConfigurationFiles.log")

	def validate(self, correct):
		'''
        This method read the band from the configuration file and check if the
        FEED angles correspond to the band, if the option correct was set to
        True this function also correct the polarization angles in the
        configuration files.
        '''
		try:
			root = xml.dom.minidom.parse(self.filename)
			# Exist only 1 entry with the tag ASSEMBLY.
			#Get the assembly name and remove the string to get the band number.
			xml_assembly = root.getElementsByTagName("ASSEMBLY")
			assembly = xml_assembly[0].getAttribute("value")
			band = int(assembly.replace("ColdCart", ""))

			#Exist only 1 entry with the tag PolarizationOrientation.
			#Get the polarization angles and cast to float with 10 decimals.
			angles = root.getElementsByTagName("PolarizationOrientation")
			x_angle_file = round(float(angles[0].getAttribute("PolXAngle")), 10)
			y_angle_file = round(float(angles[0].getAttribute("PolYAngle")), 10)

			#Calcute the polarization angles according to the band number.
			x_angle_calc = round(self.angle[band][0] * math.pi / 180, 10)
			y_angle_calc = round(self.angle[band][1] * math.pi / 180, 10)

			#Compare the polarization angles get from the file with the angles calculated.
			if x_angle_file == x_angle_calc and y_angle_file == y_angle_calc:
				return True
			else:
				message = "File: %s use the values X:%.10f Y:%.10f -- Should use X:%.10f Y:%.10f" % \
						  (self.filename, x_angle_file, y_angle_file, x_angle_calc, y_angle_calc)
				print(message)
				logging.error(message)
				#If the option correct the polarization angle in xml file was selected.S
				return False

		except Exception:
			message = "File: %s \n %s" % (self.filename, str(traceback.format_exc()))
			print(message)
			logging.error(message)



from optparse import OptionParser
import subprocess
import os

def polarization_check(filename):
	check = AngleValidator(filename)
	return check.validate(False)



if __name__ == "__main__":
	print(polarization_check("xmlTest/ColdCart8-0.xml"))