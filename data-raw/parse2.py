import os, sys, re
sys.path.append('../src/')
from uaobj import *
from uasparser import UASparser

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
	osdict = {}
	typdict = {}
	familydict = {}
	osversiondict = {}
	# also make unique only list of all properties
	for (i,x) in enumerate(ualist):
#		if i > 10:
#			break
		print "parsing UA string ", i
		result = uas_parser.parse(x.uaString)
		ostype, osversion = osparse(result['os_name'])

		if result['typ'] != 'unknown':
#			x.typ = result['typ']
			x.data['Type'] = result['typ']
			typdict[result['typ']] = i
		if result['ua_family'] != 'unknown':	
#			x.family = result['ua_family']
			x.data['Family'] = result['ua_family']
			familydict[result['ua_family']] = i
		if ostype != 'unknown': 
#			x.os = ostype
			x.data['OS'] = ostype
			osdict[ostype] = i
		if osversion != '':
#			x.osversion = osversion
			x.data['OS Version'] = osversion
			osversiondict[osversion] = i

	f = open('../data/uadata.txt','w')		
	fos = open('../data/os.txt','w')
	ftyp = open('../data/types.txt','w')
	ffamily = open('../data/families.txt','w')
	fosversion = open('../data/osversion.txt','w')
	for k in osdict.keys():
		fos.write(k+'\n')
	for k in typdict.keys():
		ftyp.write(k+'\n')
	for k in familydict.keys():
		ffamily.write(k+'\n')
	for k in osversiondict.keys():
		fosversion.write(k+'\n')
	for x in ualist:
		f.write(x + '\n')
	ftyp.close()
	ffamily.close()
	fos.close()
	fosversion.close()
	f.close()
	return 0


def osparse(osstring):
	windic = dict()
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
	if re.match('Windows',osstring):
		ostype = windic[osstring][0]
		osversion = windic[osstring][1]
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

	return ostype,osversion


if __name__ == "__main__":
	main()
