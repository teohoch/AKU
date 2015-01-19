#!/usr/bin/env python
"""
Check if a WCA or ColdCarts XML configuration file FILENAME with property FreqLO are sorted in ascending order, grouping by tagname.

Returns nothing on succeed, list of tagnames on failure. See JIRA:AIV-4386. Hint: to do a multiple search in bash use something like this:

  for i in $(ls ITS/config/CDB-COMMON/TMCDB_DATA/*.xml); do A=$(checkFreqLOorder.py -f $i); if [ "$A" != "" ]; then echo $i $A; fi; done

Usage: checkFreqLOorder.py -f|--filename FILENAME [--debug] [-h|--help]
"""
import sys, getopt
from copy import copy
import re
from xml.dom.minidom import parse



# Courtesy of Adam Ginsburg at http://casa.colorado.edu/~ginsbura/pygrep.htm
# syntax: grep(regexp_string,list_of_strings_to_search)

#Script Modified to a barebones version for use in AKU by Teodoro Hochfarber

def grep(string,list):
    expr = re.compile(string)
    return filter(expr.search,list)



# recursive search in xml node tree applying func(node, retval)
def mapNodes(xml, func, retval):
	for node in xml.childNodes:
		# XML tag only
		if node.nodeType==1:
			retval = func(node, retval)
			if len(node.childNodes):
				retval = mapNodes(node, func, retval)
	return retval


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def uniqueTagNames(node, tagnames):
	if not node.nodeName in tagnames:
		tagnames.append( str(node.nodeName))
	return tagnames


# Main routine
def freq_order_check(filename):
	print(filename)

	value = True

	# Parsing XML File
	try:
		xml = parse(filename)
	except:
	  	print "Error reading and parsing", filename
	  	sys.exit(1)

	tagnames = mapNodes(xml, uniqueTagNames, [])
	print len(tagnames)

	# foreach tagname do a search
	for tagname in tagnames:
		print 'hello'
		tagdom = xml.getElementsByTagName(tagname)


		try:
			for node in tagdom:
				print node.getAttribute("FreqLO")

			FreqLO = [ float ( node.getAttribute("FreqLO") )for node in tagdom]
			FreqSorted = copy(FreqLO)
			FreqSorted.sort()
			if FreqLO != FreqSorted:
				value = False

		except:
			print "......FreqLO = []"
	return value



if __name__=="__main__":
	print freq_order_check("xmlTest/WCA7-3.xml")
