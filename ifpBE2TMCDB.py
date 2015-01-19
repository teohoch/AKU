#! /usr/bin/env python
#*******************************************************************************
# ALMA - Atacama Large Millimiter Array
# (c) Associated Universities Inc., 2010
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
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
#
# "@(#) $Id: ifpBE2TMCDB.py 199174 2013-12-19 15:19:14Z rmarson $"
#
# who       when      what
# --------  --------  ----------------------------------------------
# jgil      20120908  added --serial restriction
#
'''
Check https://adcwiki.alma.cl/bin/view/Software/IFProcConfigProcedure
'''

__version__ = "$Revision: 1.3 $"
# $Source: /diskb/tmp/stefano/project2/CVS/CONTROL/Device/HardwareDevice/IFProc/src/ifpBE2TMCDB.py,v $

import sys
from optparse import OptionParser
from xml.dom.minidom import parse, parseString

def main():
    parser = OptionParser(usage="Generates a specific ifp_XXX.xml given IFP_Cal.xml and a given serial number. Use -h for more help")
    parser.set_defaults(serial = 0)
    parser.add_option("-s", "--serial",
        dest="serial", type="int",
        help="Required value. Serial number to generate from IFP_Cal.xml")
    (options, args) = parser.parse_args()

    if options.serial == 0:
        parser.error("Serial needed!")

    try:
       dom1 = parse('IFP_Cal.xml')
    except:
       print "Error trying to open the 'IFP_Cal.xml' file\n"
       sys.exit(1)
    
    ifp_configs = dom1.getElementsByTagName("IFP")
    
    xml_header  = "<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n"
    xml_header += "<ConfigData\n"
    xml_header += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n"
    xml_header += "xsi:noNamespaceSchemaLocation=\"membuffer.xsd\">\n"
    
    FOUND=False
    available_sn = []
    for config in ifp_configs:
        sn_m = int(config.getAttribute('SN'))
        available_sn.append(sn_m)
        if sn_m == options.serial:
            FOUND = True
            detectors_m = []
            attenuators_m = []
            detectors = config.getElementsByTagName("DET")
            for det in detectors:
                tmp = str(det.childNodes[0].data).strip().split(' ')
                coeff = [float(tmp[0]),float(tmp[1])]
                detectors_m.append([str(det.getAttribute('ch')),coeff])
            attenuators = config.getElementsByTagName("ATT")
            for att in attenuators:
                tmp = str(att.childNodes[0].data).strip().split(' ')
                real_att = []
                for rval in tmp:
                    real_att.append(float(rval))
                attenuators_m.append([str(att.getAttribute('ch')),real_att])
            # create this xml
            filename = "ifp_%d.xml" %sn_m
            print "Creating.. %s" % filename
            fd = open (filename,'w')
            fd.write(xml_header)
            fd.write("<SN value=\"%03d\"/>\n" % sn_m)
            for i in detectors_m:
                fd.write("<DET ch=\"%s\" slope=\"%f\" icept=\"%f\"/>\n" % (i[0],i[1][0],i[1][1]))
            for i in attenuators_m:
                fd.write("<ATT ch=\"%s\"" % i[0])
                idx = 0
                for atts in i[1]:
                    fd.write(" att_%d_%d=\"%f\"" % (idx/2,(idx%2)*5,atts))
                    idx+=1
                    #PATCH for now
                    if i[1].__len__() != 64:
                        fd.write(" att_31_5=\"30.0\"")
        
                fd.write("/>\n")
            fd.write("</ConfigData>\n")
            fd.close()
    if not FOUND:
        sys.exit("SN not found. Available SN are:\n\n%s" % available_sn)

if __name__=="__main__":
    main()