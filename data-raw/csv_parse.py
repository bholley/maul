import os, sys, re
sys.path.append('../src/')
from uaobj import *
from uasparser import UASparser
from user_agent import UserAgent

def main():
# start with OS file
	f = open('uasOS_example_20101014-01.csv')
	ualist = list()
	for (i,line) in enumerate(f):
		m = re.split(r"\",",line)
		m[0] = m[0].replace('"','') # clean up quotes
		m[1] = m[1].replace('"','')
		m[1] = m[1].replace('\n','')
		x = uaobject()
		x.uaString = m[1];
# pull in parse from parser on ua-string-info.com
		ualist.append(x)	
	print "number of ua strings from OS file " + str(i)	
# now load other file, compare strings as well
	f = open('uas_example_20101014-01.csv')
	newcnt = 0
	for (i,line) in enumerate(f):
		m = re.split(r"\",",line)
		m[0] = m[0].replace('"','') # clean up quotes
		m[0] = m[0].lower()
		m[1] = m[1].replace('"','')
		m[2] = m[2].replace('\n','')
		m[2] = m[2].replace('"','')
		hit = 0
		for (j,x) in enumerate(ualist):
			if x.uaString == m[2]:
				hit = 1
				break
		if hit == 0:
			newcnt = newcnt+1
			x = uaobject()
			x.uaString = m[2]
			ualist.append(x)
	print "number of new ua strings main example file " + str(newcnt)	
# now bring in bot csv file	 THERE ARE NO NEW STRINGS IN BOT FILE
#	f = open('botIP.csv')	
#	newcnt = 0
#	for (i,line) in enumerate(f):
#		m = re.split(r"\",",line)
#		m[0] = m[0].replace('"','')
#		m[5] = m[5].replace('"','')
#		m[6] = m[6].replace('"','')
#		m[6] = m[6].replace('\n','')
#		hit = 0
#		for (j,x) in enumerate(ualist):
#			if x.uaString == m[6]:
#				hit = 1
#				break
#		if hit == 0:
#			newcnt = newcnt+1
#			x = uaobject()
#			x.uaString = m[6]
#			ualist.append(x)
#	print "number of new UAs in botIP.csv: " + str(newcnt)
	
	uas_parser = UASparser()
	for (i,x) in enumerate(ualist):
		print "parsing UA string ", i
		x = parseua(x,uas_parser)	
#		result = uas_parser.parse(x.uaString)
#		ostype, osversion = osparse(result['os_name'])
#		result2 = UserAgent.factory(x.uaString).pretty()	
#		result2 = UserAgent.parse_pretty(result2)
#		version = result2[1:4]
#		for (j, k) in enumerate(version):
#			if j == 0:
#				s = version[0]
#			elif k:
#					s = ".".join([s, k])
#		if s:
#			x.data['Family Version'] = s
#		if result['typ'] != 'unknown':
#			x.data['Type'] = result['typ']
#		if result['ua_family'] != 'unknown':	
#			x.data['Family'] = result['ua_family']
#		elif result2[0] != "Other":
#			x.data['Family'] = result2[0]
#		if ostype != 'unknown': 
#			x.data['OS'] = ostype
#		if osversion != '':
#			x.data['OS Version'] = osversion

	f = open('csvdata.txt','w')		
	for x in ualist:
		f.write(x + '\n')
	f.close()
	return 0


def parseua(uaobject,uas_parser):
	x = uaobject
	result = uas_parser.parse(x.uaString)
	ostype, osversion = osparse(result['os_name'])
	result2 = UserAgent.factory(x.uaString).pretty()	
	result2 = UserAgent.parse_pretty(result2)
	version = result2[1:4]
	for (j, k) in enumerate(version):
		if j == 0:
			s = version[0]
		elif k:
				s = ".".join([s, k])
	if s:
		x.data['Family Version'] = s
	if result['typ'] != 'unknown':
		x.data['Type'] = result['typ']
	if result['ua_family'] != 'unknown':	
		x.data['Family'] = result['ua_family']
	elif result2[0] != "Other":
		x.data['Family'] = result2[0]
	if ostype != 'unknown': 
		x.data['OS'] = ostype
	if osversion != '':
		x.data['OS Version'] = osversion
	return x	
	

def osparse(osstring):
	windic = dict()
	macdic = dict()
	windic['Windows XP'] = ['Windows', 'XP']
	windic['Windows 2003 Server'] = ['Windows','2003 Server']
	windic['Windows 7'] = ['Windows','7']
	windic['Windows 95'] = ['Windows','95']
	windic['Windows Phone 7'] = ['Windows Phone 7','']
	windic['Windows ME'] = ['Windows','ME']
	windic['Windows'] = ['Windows','']
	windic['Windows Mobile'] = ['Windows','Mobile']
	windic['Windows NT'] = ['Windows','NT']
	windic['Windows 3.x'] = ['Windows','3.x']
	windic['Windows Vista'] = ['Windows','Vista']
	windic['Windows 2000'] = ['Windows','2000']
	windic['Windows 98'] = ['Windows','98']
	windic['Windows CE'] = ['Windows','CE']
	macdic['Mac OS X 10.4 Tiger'] = ['Mac OS X','10.4 Tiger']
	macdic['Mac OS X 10.6 Snow Leopard'] = ['Mac OS X','10.6 Snow Leopard']
	macdic['Mac OS X 10.5 Leopard'] = ['Mac OS X','10.5 Leopard']
	macdic['Mac OS'] = ['Mac OS','']
	macdic['Mac OS X 10.3 Panther'] = ['Mac OS X','10.3 Panther']
	macdic['Mac OS X'] = ['Mac OS X','']
	if re.match('Windows',osstring):
		ostype = windic[osstring][0]
		osversion = windic[osstring][1]
	elif re.match('Mac OS',osstring):
		ostype = macdic[osstring][0]
		osversion = macdic[osstring][1]
	elif(osstring.find('Linux') != -1):	
		if(osstring == 'Linux'):
			ostype = 'Linux'
			osversion = ""
		else:
			m = re.search(r"(\w+) \((\w+)\)",osstring)
			try:
				ostype = m.group(1)
				osversion = m.group(2)
			except:
				m = re.search(r"(\w+) \((\w+)\s(\w+)\)",osstring)
				ostype = m.group(1)
				osversion = m.group(2) + ' ' + m.group(3)
	else:	
		ostype = osstring
		osversion = ""

	return ostype, osversion

if __name__ == "__main__":
	main()
