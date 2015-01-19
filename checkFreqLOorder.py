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

def getFreqLO(node, void):
	return False


# Command line output
def usage():
	print "Usage:", __file__, "-f|--filename FILENAME [--debug] [-h|--help]"

	sys.exit(2)

def command_help():
	print __doc__
	sys.exit(0)


# Main routine
def main():

	filename = ""
	debug=False

	try:
		optlist, sys.argv = getopt.getopt(sys.argv[1:], 'f:h', ["debug", "filename", "help"])
	except getopt.GetoptError:
		usage()


	# Parse opts
	for opt, val in optlist:
		if opt=="-f" or opt=="--filename":
			filename = val
		if opt=="--debug":
			debug = True
		if opt=="-h" or opt=="--help":
			command_help()

	# Check for mandatory args
	if filename=="":
		usage()


	# Parsing XML File
	try:
		xml = parse(filename)
	  	if debug: print "...Parsing", filename
	except:
	  	print "Error reading and parsing", filename
	  	sys.exit(1)

	tagnames = mapNodes(xml, uniqueTagNames, [])


	# foreach tagname do a search
	for tagname in tagnames:
		if debug: print "...Searching by tag =", tagname
		tagdom = xml.getElementsByTagName(tagname)

		try:
			for node in tagdom:
				print node.getAttribute("FreqLO")
				print type(node.getAttribute("FreqLO"))

			FreqLO = [ float ( node.getAttribute("FreqLO") )for node in tagdom]
			if debug: print "......FreqLO =", FreqLO
			FreqSorted = copy(FreqLO)
			FreqSorted.sort()
			if debug: print "......Sorted =", FreqSorted
			if FreqLO != FreqSorted:
				print tagname, "not sorted!"

		except:
			print "......FreqLO = []"



if __name__=="__main__":
	main()
