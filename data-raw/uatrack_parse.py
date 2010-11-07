import os, sys, re
sys.path.append('../src/')
from uaobj import *
from uasparser import UASparser
from csv_parse import osparse, parseua
from user_agent import UserAgent

def main():
	print "www.ua-tracker.org parse script"
	ualist = []
	fr = open("www.ua-tracker.com user_agents.txt",'r')
	for line in fr:
		uaString = line.rstrip('\n')
		uaString = uaString.rstrip()
		uaString = uaString.lstrip()
		if uaString != '':
			x = uaobject()
			x.uaString = uaString
			ualist.append(x)
	fr.close()

	uas_parser = UASparser()
	for (i,x) in enumerate(ualist):
#		if i > 10: # debug
#			break
		print x.uaString
		print "parsing UA string", i
		x = parseua(x,uas_parser)

	f = open("uatrack_data.txt",'w')
	for x in ualist:
		f.write(x+'\n')
	f.close()	

	return 0

if __name__=="__main__":
	main()
