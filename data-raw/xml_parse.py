import os, sys, re
sys.path.append('../src/')
from uaobj import *
from uasparser import UASparser
import elementtree.ElementTree as et
from csv_parse import osparse, parseua
from user_agent import UserAgent

def main():
	print "XML Parse Script"
	tree = et.parse("allagents.xml")

# these two iterations do the same thing
#	for elem in tree.getiterator("String"):
#		print elem.text.encode('utf-8')
	ualist = []
	for elem in tree.getiterator("user-agent"):
		stringelem = elem.find("String")
		x = uaobject()
		x.uaString = stringelem.text.encode('utf-8')
		typeelem = elem.find("Type")
		if typeelem.text == "R":
			x.data['Type'] = "Robot"
		elif typeelem.text == "B":
			x.data['Type'] = "Browser"
		elif typeelem.text == "C":
			x.data['Type'] = "Validator"
		elif typeelem.text == "P":
			x.data['Type'] = "Proxy"
		elif typeelem.text == "S":
			x.data['Type'] = "Malicious"
		elif typeelem.text == "D":
			x.data['Type'] = "Downloader"
		ualist.append(x)	


# run uas parsser
	uas_parser = UASparser()
	for (i,x) in enumerate(ualist):
		print "parsing UA string", i
		x = parseua(x,uas_parser)
#		result = uas_parser.parse(x.uaString)
#		ostype, osversion = osparse(result['os_name'])
#
#		if result['typ'] != 'unknown':
#			x.data['Type'] = result['typ']
#		if result['ua_family'] != 'unknown':
#			x.data['Family'] = result['ua_family']
#		if ostype != 'unknown':
#			x.data['OS'] = ostype
#		if osversion != '':
#			x.data['OS Version'] = osversion



	f = open('xmldata.txt','w')
	for x in ualist:
		f.write(x + '\n')
	f.close()	

	return 0
if __name__ == "__main__":
	main()


